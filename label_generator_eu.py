#!/usr/bin/env python3
"""
EU Regulation 1169/2011 Compliant Food Label Generator
Generates production-ready HTML labels following EU food labeling regulations
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from jinja2 import Template


class EUValidator:
    """Validates product data against EU Regulation 1169/2011 requirements"""
    
    MANDATORY_FIELDS = [
        'product_name', 'category', 'net_quantity', 'ingredients',
        'nutrition_per_100g', 'date_type', 'storage_conditions',
        'business_operator'
    ]
    
    CATEGORIES = [
        'packaged_food', 'meat_fresh', 'fish_seafood', 'dairy',
        'frozen_food', 'organic', 'food_supplement', 'alcoholic_beverage',
        'fresh_produce', 'infant_food'
    ]
    
    # EU 14 Allergens (Regulation 1169/2011 Annex II)
    EU_ALLERGENS = [
        'milk', 'eggs', 'fish', 'crustaceans', 'molluscs',
        'peanuts', 'tree nuts', 'soy', 'gluten', 'celery',
        'mustard', 'sesame', 'lupin', 'sulphites'
    ]
    
    @staticmethod
    def validate(data: Dict[str, Any]) -> tuple[bool, List[str]]:
        """Validate product data and return (is_valid, errors)"""
        errors = []
        
        # Check mandatory fields
        for field in EUValidator.MANDATORY_FIELDS:
            if field not in data:
                errors.append(f"Missing mandatory field: {field}")
        
        if not errors:
            # Validate category
            if data.get('category') not in EUValidator.CATEGORIES:
                errors.append(f"Invalid category. Must be one of: {', '.join(EUValidator.CATEGORIES)}")
            
            # Validate net quantity (metric only)
            net_qty = data.get('net_quantity', {})
            if not isinstance(net_qty, dict) or 'value' not in net_qty or 'unit' not in net_qty:
                errors.append("net_quantity must have 'value' and 'unit' (g, kg, ml, L)")
            elif net_qty.get('unit') not in ['g', 'kg', 'ml', 'L']:
                errors.append("net_quantity unit must be metric: g, kg, ml, or L")
            
            # Validate nutrition declaration (per 100g/100ml)
            nutrition = data.get('nutrition_per_100g', {})
            required_nutrients = [
                'energy_kj', 'energy_kcal', 'fat', 'saturates',
                'carbohydrate', 'sugars', 'protein', 'salt'
            ]
            for nutrient in required_nutrients:
                if nutrient not in nutrition:
                    errors.append(f"Missing required nutrient: {nutrient}")
            
            # Validate ingredients list
            ingredients = data.get('ingredients', [])
            if not isinstance(ingredients, list) or len(ingredients) == 0:
                errors.append("ingredients must be a non-empty list")
            
            # Validate date type
            if data.get('date_type') not in ['best_before', 'use_by']:
                errors.append("date_type must be 'best_before' or 'use_by'")
            
            # Validate business operator
            operator = data.get('business_operator', {})
            if not isinstance(operator, dict) or 'name' not in operator or 'address' not in operator:
                errors.append("business_operator must have 'name' and 'address'")
            
            # Category-specific validation
            category = data.get('category', '')
            
            if category == 'meat_fresh':
                if 'country_of_rearing' not in data or 'country_of_slaughter' not in data:
                    errors.append("meat_fresh requires 'country_of_rearing' and 'country_of_slaughter'")
            
            if category == 'fish_seafood':
                if 'catch_method' not in data or 'catch_area' not in data:
                    errors.append("fish_seafood requires 'catch_method' and 'catch_area'")
                if 'wild_or_farmed' not in data:
                    errors.append("fish_seafood requires 'wild_or_farmed'")
            
            if category == 'organic' and data.get('is_organic'):
                if 'organic_certification' not in data:
                    errors.append("organic products require 'organic_certification' code")
        
        return len(errors) == 0, errors


class EULabelGenerator:
    """Generates EU Regulation 1169/2011 compliant food labels"""
    
    def __init__(self, template_path: Optional[str] = None):
        """Initialize generator with optional custom template"""
        if template_path and Path(template_path).exists():
            with open(template_path, 'r', encoding='utf-8') as f:
                self.template = Template(f.read())
        else:
            self.template = self._get_default_template()
    
    def generate(self, product_data: Dict[str, Any], output_path: Optional[str] = None) -> str:
        """Generate label HTML from product data"""
        
        # Validate data
        is_valid, errors = EUValidator.validate(product_data)
        if not is_valid:
            raise ValueError(f"Invalid product data:\n" + "\n".join(f"  - {e}" for e in errors))
        
        # Enrich data with computed fields
        enriched_data = self._enrich_data(product_data)
        
        # Generate HTML
        html = self.template.render(**enriched_data)
        
        # Save to file if output path provided
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html)
            print(f"✓ Label generated: {output_path}")
        
        return html
    
    def _enrich_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Add computed fields to product data"""
        enriched = data.copy()
        
        # Format net quantity with ℮ mark
        nq = data['net_quantity']
        enriched['net_quantity_display'] = f"{nq['value']}{nq['unit']} ℮"
        
        # Format ingredients with allergens in bold and E-numbers
        enriched['ingredients_formatted'] = self._format_ingredients(
            data['ingredients'],
            data.get('allergens', [])
        )
        
        # Format allergen list
        if 'allergens' in data and data['allergens']:
            enriched['allergens_list'] = ', '.join(
                allergen.upper() for allergen in data['allergens']
            )
        
        # Add category-specific data
        enriched.update(self._get_category_specific_data(data))
        
        # Format date display
        date_type = data['date_type']
        if date_type == 'best_before' and 'best_before' in data:
            enriched['date_display'] = f"Best before: {data['best_before']}"
        elif date_type == 'use_by' and 'use_by' in data:
            enriched['date_display'] = f"Use by: {data['use_by']}"
        
        return enriched
    
    def _format_ingredients(self, ingredients: List[Any], allergens: List[str]) -> str:
        """Format ingredients list with allergens in bold and E-numbers"""
        formatted = []
        allergen_keywords = set()
        
        # Extract allergen keywords
        for allergen in allergens:
            if '(' in allergen:
                base = allergen.split('(')[0].strip().lower()
                specific = allergen.split('(')[1].replace(')', '').strip().lower()
                allergen_keywords.add(base)
                allergen_keywords.add(specific)
            else:
                allergen_keywords.add(allergen.lower())
        
        for ing in ingredients:
            if isinstance(ing, dict):
                name = ing['name']
                
                # Add E-number if present
                if 'e_number' in ing:
                    functional_class = ing.get('functional_class', '')
                    if functional_class:
                        name = f"{functional_class} ({name}, {ing['e_number']})"
                    else:
                        name = f"{name} ({ing['e_number']})"
                
                # Add percentage if present
                if 'percentage' in ing:
                    name = f"{name} ({ing['percentage']}%)"
                
                # Check if allergen
                is_allergen = ing.get('is_allergen', False) or any(
                    keyword in name.lower() for keyword in allergen_keywords
                )
                
                if is_allergen:
                    formatted.append(f"<strong>{name}</strong>")
                else:
                    formatted.append(name)
            else:
                name = str(ing)
                is_allergen = any(keyword in name.lower() for keyword in allergen_keywords)
                if is_allergen:
                    formatted.append(f"<strong>{name}</strong>")
                else:
                    formatted.append(name)
        
        return ', '.join(formatted)
    
    def _get_category_specific_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Add category-specific requirements"""
        category_data = {}
        category = data.get('category', '')
        
        # Meat & Fresh Meat
        if category == 'meat_fresh':
            category_data['show_meat_origin'] = True
            category_data['show_traceability'] = True
            if data.get('previously_frozen'):
                category_data['show_previously_frozen'] = True
        
        # Fish & Seafood
        elif category == 'fish_seafood':
            category_data['show_catch_info'] = True
            category_data['show_fishing_method'] = True
        
        # Dairy
        elif category == 'dairy':
            category_data['show_fat_percentage'] = 'fat_percentage' in data
            category_data['show_pasteurization'] = True
        
        # Frozen Foods
        elif category == 'frozen_food':
            category_data['show_frozen_date'] = True
            category_data['show_defrosting_instructions'] = True
        
        # Organic
        if data.get('is_organic'):
            category_data['show_eu_organic_logo'] = True
            # Check if ≥95% organic
            organic_percentage = data.get('organic_percentage', 95)
            category_data['organic_compliant'] = organic_percentage >= 95
        
        # Food Supplements
        if category == 'food_supplement':
            category_data['is_supplement'] = True
            category_data['show_supplement_warnings'] = True
        
        # Alcoholic Beverages
        if category == 'alcoholic_beverage':
            category_data['show_abv'] = True
            category_data['show_sulphite_warning'] = data.get('contains_sulphites', False)
        
        # Fresh Produce
        if category == 'fresh_produce':
            category_data['show_origin_mandatory'] = True
        
        # Infant Food
        if category == 'infant_food':
            category_data['is_infant_food'] = True
            category_data['show_preparation_instructions'] = True
        
        return category_data
    
    def _get_default_template(self) -> Template:
        """Return default Jinja2 template"""
        template_path = Path(__file__).parent / 'label_template_eu.html'
        if template_path.exists():
            with open(template_path, 'r', encoding='utf-8') as f:
                return Template(f.read())
        else:
            raise FileNotFoundError("label_template_eu.html not found. Please create it first.")


def main():
    """CLI entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Generate EU Regulation 1169/2011 compliant food labels'
    )
    parser.add_argument(
        '--input', '-i',
        required=True,
        help='Input JSON file with product data'
    )
    parser.add_argument(
        '--output', '-o',
        required=True,
        help='Output HTML file path'
    )
    parser.add_argument(
        '--template', '-t',
        help='Custom template file (optional)'
    )
    parser.add_argument(
        '--validate-only',
        action='store_true',
        help='Only validate data without generating label'
    )
    
    args = parser.parse_args()
    
    # Load product data
    try:
        with open(args.input, 'r', encoding='utf-8') as f:
            product_data = json.load(f)
    except FileNotFoundError:
        print(f"✗ Error: Input file not found: {args.input}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"✗ Error: Invalid JSON in input file: {e}")
        sys.exit(1)
    
    # Validate
    is_valid, errors = EUValidator.validate(product_data)
    
    if not is_valid:
        print("✗ Validation failed:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)
    
    print("✓ Validation passed")
    
    if args.validate_only:
        print("✓ Data is EU Regulation 1169/2011 compliant")
        return
    
    # Generate label
    try:
        generator = EULabelGenerator(args.template)
        generator.generate(product_data, args.output)
        print(f"✓ Label successfully generated: {args.output}")
    except Exception as e:
        print(f"✗ Error generating label: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()