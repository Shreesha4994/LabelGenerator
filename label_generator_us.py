#!/usr/bin/env python3
"""
US FDA/USDA Compliant Food Label Generator
Generates production-ready HTML labels following FDA and USDA regulations
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
from jinja2 import Template


class FDAValidator:
    """Validates product data against FDA/USDA requirements"""
    
    MANDATORY_FIELDS = [
        'product_name', 'category', 'net_quantity', 'ingredients',
        'nutrition_facts', 'manufacturer'
    ]
    
    CATEGORIES = [
        'packaged_food', 'meat_poultry_egg', 'dairy', 'beverage_alcoholic',
        'beverage_nonalcoholic', 'dietary_supplement', 'infant_formula',
        'organic', 'frozen_food', 'fresh_produce'
    ]
    
    # FALCPA - 9 Major Allergens (including sesame as of 2023)
    MAJOR_ALLERGENS = [
        'milk', 'eggs', 'fish', 'shellfish', 'tree nuts',
        'peanuts', 'wheat', 'soy', 'sesame'
    ]
    
    @staticmethod
    def validate(data: Dict[str, Any]) -> tuple[bool, List[str]]:
        """Validate product data and return (is_valid, errors)"""
        errors = []
        
        # Check mandatory fields
        for field in FDAValidator.MANDATORY_FIELDS:
            if field not in data:
                errors.append(f"Missing mandatory field: {field}")
        
        if not errors:
            # Validate category
            if data.get('category') not in FDAValidator.CATEGORIES:
                errors.append(f"Invalid category. Must be one of: {', '.join(FDAValidator.CATEGORIES)}")
            
            # Validate net quantity has both US and metric units
            net_qty = data.get('net_quantity', {})
            if not isinstance(net_qty, dict):
                errors.append("net_quantity must be a dictionary")
            else:
                required_keys = ['us_value', 'us_unit', 'metric_value', 'metric_unit']
                for key in required_keys:
                    if key not in net_qty:
                        errors.append(f"net_quantity missing required key: {key}")
            
            # Validate nutrition facts (different for supplements)
            if data.get('category') == 'dietary_supplement':
                # Supplement Facts validation
                if 'supplement_facts' not in data:
                    errors.append("dietary_supplement category requires 'supplement_facts' field")
            else:
                # Nutrition Facts validation
                nutrition = data.get('nutrition_facts', {})
                required_nutrients = [
                    'serving_size', 'servings_per_container', 'calories',
                    'total_fat', 'saturated_fat', 'trans_fat', 'cholesterol',
                    'sodium', 'total_carb', 'fiber', 'total_sugars',
                    'added_sugars', 'protein'
                ]
                for nutrient in required_nutrients:
                    if nutrient not in nutrition:
                        errors.append(f"Missing required nutrient: {nutrient}")
            
            # Validate ingredients list
            ingredients = data.get('ingredients', [])
            if not isinstance(ingredients, list) or len(ingredients) == 0:
                errors.append("ingredients must be a non-empty list")
            
            # Validate manufacturer details
            manufacturer = data.get('manufacturer', {})
            required_mfr = ['name', 'city', 'state', 'zip']
            for key in required_mfr:
                if key not in manufacturer:
                    errors.append(f"manufacturer missing required key: {key}")
            
            # Validate USDA-specific requirements for meat/poultry
            if data.get('category') == 'meat_poultry_egg':
                if 'usda_establishment_number' not in data:
                    errors.append("meat_poultry_egg requires 'usda_establishment_number'")
                if 'safe_handling_instructions' not in data:
                    errors.append("meat_poultry_egg requires 'safe_handling_instructions'")
        
        return len(errors) == 0, errors


class USLabelGenerator:
    """Generates FDA/USDA compliant food labels"""
    
    def __init__(self, template_path: Optional[str] = None):
        """Initialize generator with optional custom template"""
        if template_path and Path(template_path).exists():
            with open(template_path, 'r', encoding='utf-8') as f:
                self.template = Template(f.read())
        else:
            # Use embedded template
            self.template = self._get_default_template()
    
    def generate(self, product_data: Dict[str, Any], output_path: Optional[str] = None) -> str:
        """Generate label HTML from product data"""
        
        # Validate data
        is_valid, errors = FDAValidator.validate(product_data)
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
        
        # Format net quantity display
        nq = data['net_quantity']
        enriched['net_quantity_display'] = f"{nq['us_value']} {nq['us_unit']} ({nq['metric_value']}{nq['metric_unit']})"
        
        # Format ingredients with allergens highlighted
        enriched['ingredients_formatted'] = self._format_ingredients(
            data['ingredients'],
            data.get('allergens', [])
        )
        
        # Format allergen statement (FALCPA format)
        if 'allergens' in data and data['allergens']:
            enriched['allergen_statement'] = "Contains: " + ", ".join(
                allergen.title() for allergen in data['allergens']
            )
        
        # Add category-specific data
        enriched.update(self._get_category_specific_data(data))
        
        # Format manufacturer address
        mfr = data['manufacturer']
        enriched['manufacturer_address'] = f"{mfr['city']}, {mfr['state']} {mfr['zip']}"
        
        # Add organic seal level if applicable
        if data.get('is_organic'):
            organic_level = data.get('organic_level', '95_percent')
            enriched['organic_seal_text'] = self._get_organic_seal_text(organic_level)
        
        return enriched
    
    def _format_ingredients(self, ingredients: List[Any], allergens: List[str]) -> str:
        """Format ingredients list with allergens in bold"""
        formatted = []
        allergen_keywords = set()
        
        # Extract allergen keywords for highlighting
        for allergen in allergens:
            # Handle formats like "tree nuts (almonds)"
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
            else:
                name = str(ing)
            
            # Check if ingredient contains allergen
            name_lower = name.lower()
            is_allergen = any(keyword in name_lower for keyword in allergen_keywords)
            
            if is_allergen:
                formatted.append(f"<strong>{name}</strong>")
            else:
                formatted.append(name)
        
        return ', '.join(formatted)
    
    def _get_category_specific_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Add category-specific requirements"""
        category_data = {}
        category = data.get('category', '')
        
        # USDA Meat/Poultry/Egg
        if category == 'meat_poultry_egg':
            category_data['show_usda_inspection'] = True
            category_data['show_safe_handling'] = True
            category_data['is_usda_regulated'] = True
        
        # Dairy specific
        elif category == 'dairy':
            category_data['show_pasteurization'] = True
            if 'milk_fat_percentage' in data:
                category_data['show_fat_percentage'] = True
        
        # Alcoholic beverages (TTB)
        elif category == 'beverage_alcoholic':
            category_data['show_abv'] = True
            category_data['show_surgeon_general_warning'] = True
            category_data['show_sulfite_warning'] = data.get('contains_sulfites', False)
        
        # Dietary supplements
        elif category == 'dietary_supplement':
            category_data['is_supplement'] = True
            category_data['show_fda_disclaimer'] = True
        
        # Infant formula
        elif category == 'infant_formula':
            category_data['is_infant_formula'] = True
            category_data['show_preparation_instructions'] = True
        
        # Organic
        if data.get('is_organic'):
            category_data['show_usda_organic_seal'] = True
        
        # Frozen foods
        if category == 'frozen_food':
            category_data['show_cooking_instructions'] = True
            category_data['show_storage_temp'] = True
        
        # Imported
        if data.get('is_imported', False):
            category_data['show_country_of_origin'] = True
        
        return category_data
    
    def _get_organic_seal_text(self, level: str) -> str:
        """Get USDA organic seal text based on level"""
        levels = {
            '100_percent': '100% Organic',
            '95_percent': 'Organic',
            '70_percent': 'Made with Organic Ingredients'
        }
        return levels.get(level, 'Organic')
    
    def _get_default_template(self) -> Template:
        """Return default Jinja2 template"""
        template_path = Path(__file__).parent / 'label_template_us.html'
        if template_path.exists():
            with open(template_path, 'r', encoding='utf-8') as f:
                return Template(f.read())
        else:
            raise FileNotFoundError("label_template_us.html not found. Please create it first.")


def main():
    """CLI entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Generate FDA/USDA compliant food labels for USA'
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
    is_valid, errors = FDAValidator.validate(product_data)
    
    if not is_valid:
        print("✗ Validation failed:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)
    
    print("✓ Validation passed")
    
    if args.validate_only:
        print("✓ Data is FDA/USDA compliant")
        return
    
    # Generate label
    try:
        generator = USLabelGenerator(args.template)
        generator.generate(product_data, args.output)
        print(f"✓ Label successfully generated: {args.output}")
    except Exception as e:
        print(f"✗ Error generating label: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()