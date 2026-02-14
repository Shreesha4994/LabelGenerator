#!/usr/bin/env python3
"""
India FSSAI Compliant Food Label Generator
Generates production-ready HTML labels following all FSSAI regulations
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
from jinja2 import Template


class FSSAIValidator:
    """Validates product data against FSSAI requirements"""
    
    MANDATORY_FIELDS = [
        'product_name', 'category', 'veg_status', 'net_quantity',
        'ingredients', 'nutrition_per_100g', 'fssai_license',
        'manufacturer', 'batch_number', 'mfg_date', 'mrp'
    ]
    
    CATEGORIES = [
        'packaged_processed_food', 'dairy', 'beverage_carbonated',
        'beverage_juice', 'meat_fish_egg', 'fresh_produce',
        'fortified', 'organic', 'frozen', 'ready_to_eat', 'imported'
    ]
    
    @staticmethod
    def validate(data: Dict[str, Any]) -> tuple[bool, List[str]]:
        """Validate product data and return (is_valid, errors)"""
        errors = []
        
        # Check mandatory fields
        for field in FSSAIValidator.MANDATORY_FIELDS:
            if field not in data:
                errors.append(f"Missing mandatory field: {field}")
        
        if not errors:
            # Validate FSSAI license (14 digits)
            fssai = str(data.get('fssai_license', ''))
            if not fssai.isdigit() or len(fssai) != 14:
                errors.append("FSSAI license must be exactly 14 digits")
            
            # Validate veg status
            if data.get('veg_status') not in ['veg', 'non-veg']:
                errors.append("veg_status must be 'veg' or 'non-veg'")
            
            # Validate category
            if data.get('category') not in FSSAIValidator.CATEGORIES:
                errors.append(f"Invalid category. Must be one of: {', '.join(FSSAIValidator.CATEGORIES)}")
            
            # Validate net quantity has value and unit
            net_qty = data.get('net_quantity', {})
            if not isinstance(net_qty, dict) or 'value' not in net_qty or 'unit' not in net_qty:
                errors.append("net_quantity must have 'value' and 'unit' (g, kg, ml, L)")
            
            # Validate nutrition table
            nutrition = data.get('nutrition_per_100g', {})
            required_nutrients = ['energy_kcal', 'protein', 'carbohydrates', 'fat']
            for nutrient in required_nutrients:
                if nutrient not in nutrition:
                    errors.append(f"Missing required nutrient: {nutrient}")
            
            # Validate ingredients list
            ingredients = data.get('ingredients', [])
            if not isinstance(ingredients, list) or len(ingredients) == 0:
                errors.append("ingredients must be a non-empty list")
            
            # Validate manufacturer details
            manufacturer = data.get('manufacturer', {})
            if not isinstance(manufacturer, dict) or 'name' not in manufacturer or 'address' not in manufacturer:
                errors.append("manufacturer must have 'name' and 'address'")
        
        return len(errors) == 0, errors


class IndiaLabelGenerator:
    """Generates FSSAI compliant food labels"""
    
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
        is_valid, errors = FSSAIValidator.validate(product_data)
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
        
        # Calculate best before date
        if 'best_before_months' in data:
            mfg_date = datetime.strptime(data['mfg_date'], '%Y-%m-%d')
            best_before = mfg_date + timedelta(days=data['best_before_months'] * 30)
            enriched['best_before_date'] = best_before.strftime('%Y-%m-%d')
        elif 'best_before_days' in data:
            mfg_date = datetime.strptime(data['mfg_date'], '%Y-%m-%d')
            best_before = mfg_date + timedelta(days=data['best_before_days'])
            enriched['best_before_date'] = best_before.strftime('%Y-%m-%d')
        
        # Format MFG date for display
        mfg_date = datetime.strptime(data['mfg_date'], '%Y-%m-%d')
        enriched['mfg_date_display'] = mfg_date.strftime('%b %Y')
        
        # Format ingredients with additives
        enriched['ingredients_formatted'] = self._format_ingredients(data['ingredients'])
        
        # Format allergens
        if 'allergens' in data and data['allergens']:
            enriched['allergens_formatted'] = ', '.join(
                allergen.upper() for allergen in data['allergens']
            )
        
        # Add category-specific data
        enriched.update(self._get_category_specific_data(data))
        
        # Format FSSAI license for display
        fssai = str(data['fssai_license'])
        enriched['fssai_license_formatted'] = f"{fssai[:2]} {fssai[2:6]} {fssai[6:10]} {fssai[10:]}"
        
        return enriched
    
    def _format_ingredients(self, ingredients: List[Dict[str, Any]]) -> str:
        """Format ingredients list with percentages and INS numbers"""
        formatted = []
        for ing in ingredients:
            name = ing['name']
            
            # Add percentage if provided
            if 'percentage' in ing:
                name = f"{name} ({ing['percentage']}%)"
            
            # Add INS number for additives
            if 'ins_number' in ing:
                name = f"{name} (INS {ing['ins_number']})"
            
            # Add class name for additives
            if 'class_name' in ing:
                name = f"{ing['class_name']} ({name})"
            
            formatted.append(name)
        
        return ', '.join(formatted)
    
    def _get_category_specific_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Add category-specific requirements"""
        category_data = {}
        category = data.get('category', '')
        
        # Dairy products
        if category == 'dairy':
            category_data['show_fat_percentage'] = True
            category_data['show_milk_source'] = True
        
        # Beverages
        elif category in ['beverage_carbonated', 'beverage_juice']:
            category_data['show_caffeine_warning'] = data.get('contains_caffeine', False)
            if category == 'beverage_juice':
                category_data['show_fruit_percentage'] = True
        
        # Meat/Fish/Egg
        elif category == 'meat_fish_egg':
            category_data['show_use_by_date'] = True
            category_data['show_storage_temp'] = True
        
        # Fortified foods
        if data.get('is_fortified', False):
            category_data['show_fortified_logo'] = True
            category_data['fortification_details'] = data.get('fortification_details', '')
        
        # Organic foods
        if data.get('is_organic', False):
            category_data['show_organic_logo'] = True
            category_data['organic_certification'] = data.get('organic_certification', '')
        
        # Frozen foods
        if category == 'frozen':
            category_data['show_storage_temp'] = True
            category_data['show_thawing_instructions'] = True
        
        # Imported foods
        if data.get('is_imported', False):
            category_data['show_importer_details'] = True
            category_data['show_country_of_origin'] = True
        
        return category_data
    
    def _get_default_template(self) -> Template:
        """Return default Jinja2 template"""
        # Template will be loaded from label_template.html
        template_path = Path(__file__).parent / 'label_template.html'
        if template_path.exists():
            with open(template_path, 'r', encoding='utf-8') as f:
                return Template(f.read())
        else:
            raise FileNotFoundError("label_template.html not found. Please create it first.")


def main():
    """CLI entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Generate FSSAI compliant food labels for India'
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
    is_valid, errors = FSSAIValidator.validate(product_data)
    
    if not is_valid:
        print("✗ Validation failed:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)
    
    print("✓ Validation passed")
    
    if args.validate_only:
        print("✓ Data is FSSAI compliant")
        return
    
    # Generate label
    try:
        generator = IndiaLabelGenerator(args.template)
        generator.generate(product_data, args.output)
        print(f"✓ Label successfully generated: {args.output}")
    except Exception as e:
        print(f"✗ Error generating label: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()