#!/usr/bin/env python3
"""
US FDA/USDA Compliant Food Label Generator
Generates production-ready HTML labels following FDA and USDA regulations

Supports:
- Standard packaged foods (FDA)
- Meat/Poultry/Egg products (USDA)
- Dietary Supplements (DSHEA)
- Infant Formula (FDA)
- Organic products (USDA Organic)
- Bioengineered food disclosure (NBFDS)
- Nutrition and health claims validation
"""

import json
import sys
import math
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from jinja2 import Template


class FDANutritionClaimsValidator:
    """Validates nutrition claims against FDA criteria (21 CFR 101.13, 101.54-101.67)"""
    
    # FDA-defined criteria for nutrition claims (per RACC or per serving)
    CLAIM_CRITERIA = {
        # Fat claims (per RACC and per labeled serving)
        'fat_free': {'total_fat': {'max': 0.5}},  # Less than 0.5g fat
        'low_fat': {'total_fat': {'max': 3}},  # 3g or less fat
        'reduced_fat': {'total_fat': {'reduction': 25}},  # 25% less than reference
        
        # Saturated fat claims
        'saturated_fat_free': {'saturated_fat': {'max': 0.5}, 'trans_fat': {'max': 0.5}},
        'low_saturated_fat': {'saturated_fat': {'max': 1}},
        
        # Cholesterol claims (per RACC and per labeled serving)
        'cholesterol_free': {'cholesterol': {'max': 2}},  # Less than 2mg
        'low_cholesterol': {'cholesterol': {'max': 20}},  # 20mg or less
        
        # Sodium claims
        'sodium_free': {'sodium': {'max': 5}},  # Less than 5mg
        'very_low_sodium': {'sodium': {'max': 35}},  # 35mg or less
        'low_sodium': {'sodium': {'max': 140}},  # 140mg or less
        'reduced_sodium': {'sodium': {'reduction': 25}},
        
        # Calorie claims
        'calorie_free': {'calories': {'max': 5}},  # Less than 5 calories
        'low_calorie': {'calories': {'max': 40}},  # 40 calories or less
        'reduced_calorie': {'calories': {'reduction': 25}},
        
        # Sugar claims
        'sugar_free': {'total_sugars': {'max': 0.5}},  # Less than 0.5g
        'no_added_sugars': {'added_sugars': {'max': 0}},  # No added sugars
        'reduced_sugar': {'total_sugars': {'reduction': 25}},
        
        # Fiber claims (per RACC)
        'high_fiber': {'fiber': {'min': 5}},  # 5g or more (20% DV)
        'good_source_fiber': {'fiber': {'min': 2.5}},  # 2.5g-4.9g (10-19% DV)
        
        # Protein claims
        'high_protein': {'protein': {'min': 10}},  # 10g or more (20% DV)
        'good_source_protein': {'protein': {'min': 5}},  # 5g-9.9g (10-19% DV)
        
        # Vitamin/Mineral claims (% DV)
        'excellent_source': {'nutrient_dv': {'min': 20}},  # 20% DV or more
        'good_source': {'nutrient_dv': {'min': 10, 'max': 19}},  # 10-19% DV
        'more': {'nutrient_dv': {'increase': 10}},  # 10% DV more than reference
    }
    
    # FDA-authorized health claims
    HEALTH_CLAIMS = {
        'calcium_osteoporosis': {
            'requirements': {'calcium': {'min_dv': 20}},
            'claim': 'Adequate calcium throughout life, as part of a well-balanced diet, may reduce the risk of osteoporosis.'
        },
        'sodium_hypertension': {
            'requirements': {'sodium': {'max': 140}},
            'claim': 'Diets low in sodium may reduce the risk of high blood pressure, a disease associated with many factors.'
        },
        'fat_cancer': {
            'requirements': {'total_fat': {'max': 3}},
            'claim': 'Development of cancer depends on many factors. A diet low in total fat may reduce the risk of some cancers.'
        },
        'fiber_cancer': {
            'requirements': {'fiber': {'min': 2.5}, 'total_fat': {'max': 3}},
            'claim': 'Low fat diets rich in fiber-containing grain products, fruits, and vegetables may reduce the risk of some types of cancer.'
        },
        'fiber_heart_disease': {
            'requirements': {'fiber': {'min': 2.5}, 'total_fat': {'max': 3}, 'saturated_fat': {'max': 1}},
            'claim': 'Diets low in saturated fat and cholesterol and rich in fruits, vegetables, and grain products that contain some types of dietary fiber may reduce the risk of heart disease.'
        },
        'potassium_blood_pressure': {
            'requirements': {'potassium': {'min_dv': 10}, 'sodium': {'max': 140}},
            'claim': 'Diets containing foods that are a good source of potassium and that are low in sodium may reduce the risk of high blood pressure and stroke.'
        }
    }
    
    @staticmethod
    def validate_claim(claim_type: str, nutrition_facts: Dict[str, Any], reference_food: Optional[Dict] = None) -> Tuple[bool, str]:
        """Validate if a nutrition claim meets FDA criteria"""
        if claim_type not in FDANutritionClaimsValidator.CLAIM_CRITERIA:
            return False, f"Unknown claim type: {claim_type}"
        
        criteria = FDANutritionClaimsValidator.CLAIM_CRITERIA[claim_type]
        
        for nutrient, requirements in criteria.items():
            if nutrient == 'nutrient_dv':
                continue  # Special handling for vitamin/mineral claims
            
            # Get nutrient value from nutrition facts
            nutrient_data = nutrition_facts.get(nutrient, {})
            if isinstance(nutrient_data, dict):
                value = nutrient_data.get('value', 0)
            else:
                value = nutrient_data
            
            # Check max requirement
            if 'max' in requirements:
                if value > requirements['max']:
                    return False, f"{claim_type} requires {nutrient} ≤ {requirements['max']}, but product has {value}"
            
            # Check min requirement
            if 'min' in requirements:
                if value < requirements['min']:
                    return False, f"{claim_type} requires {nutrient} ≥ {requirements['min']}, but product has {value}"
            
            # Check reduction requirement (needs reference food)
            if 'reduction' in requirements:
                if not reference_food:
                    return False, f"{claim_type} requires comparison to reference food"
                ref_value = reference_food.get(nutrient, {})
                if isinstance(ref_value, dict):
                    ref_value = ref_value.get('value', 0)
                if ref_value > 0:
                    reduction_pct = ((ref_value - value) / ref_value) * 100
                    if reduction_pct < requirements['reduction']:
                        return False, f"{claim_type} requires {requirements['reduction']}% reduction, but only {reduction_pct:.1f}% achieved"
        
        return True, f"Claim '{claim_type}' is valid"
    
    @staticmethod
    def get_valid_claims(nutrition_facts: Dict[str, Any]) -> List[str]:
        """Get all valid nutrition claims for given nutrition facts"""
        valid_claims = []
        for claim_type in FDANutritionClaimsValidator.CLAIM_CRITERIA:
            is_valid, _ = FDANutritionClaimsValidator.validate_claim(claim_type, nutrition_facts)
            if is_valid:
                valid_claims.append(claim_type)
        return valid_claims


class FDAFontSizeValidator:
    """Validates font sizes based on FDA requirements (21 CFR 101.7)"""
    
    # Minimum type sizes based on PDP area (in square inches)
    # Font size in inches (height of lowercase 'o')
    PDP_FONT_REQUIREMENTS = [
        {'pdp_max': 5, 'min_font': 1/16},  # ≤5 sq in: 1/16 inch
        {'pdp_max': 25, 'min_font': 1/8},  # >5 to 25 sq in: 1/8 inch
        {'pdp_max': 100, 'min_font': 3/16},  # >25 to 100 sq in: 3/16 inch
        {'pdp_max': 400, 'min_font': 1/4},  # >100 to 400 sq in: 1/4 inch
        {'pdp_max': float('inf'), 'min_font': 1/2},  # >400 sq in: 1/2 inch
    ]
    
    @staticmethod
    def calculate_pdp_area(width_inches: float, height_inches: float, shape: str = 'rectangular') -> float:
        """Calculate Principal Display Panel area"""
        if shape == 'rectangular':
            return width_inches * height_inches
        elif shape == 'cylindrical':
            # For cylindrical containers, PDP = 40% of circumference × height
            circumference = width_inches  # width is circumference for cylindrical
            return 0.4 * circumference * height_inches
        else:
            return width_inches * height_inches
    
    @staticmethod
    def get_minimum_font_size(pdp_area: float) -> float:
        """Get minimum font size in inches based on PDP area"""
        for req in FDAFontSizeValidator.PDP_FONT_REQUIREMENTS:
            if pdp_area <= req['pdp_max']:
                return req['min_font']
        return 1/2  # Default to largest
    
    @staticmethod
    def inches_to_points(inches: float) -> float:
        """Convert inches to points (1 inch = 72 points)"""
        return inches * 72
    
    @staticmethod
    def validate_font_sizes(pdp_area: float, font_sizes: Dict[str, float]) -> Tuple[bool, List[str]]:
        """Validate font sizes against FDA requirements"""
        min_font_inches = FDAFontSizeValidator.get_minimum_font_size(pdp_area)
        min_font_points = FDAFontSizeValidator.inches_to_points(min_font_inches)
        
        errors = []
        for element, size_points in font_sizes.items():
            if size_points < min_font_points:
                errors.append(f"{element}: {size_points}pt is below minimum {min_font_points:.1f}pt for PDP area {pdp_area} sq in")
        
        return len(errors) == 0, errors


class FDAValidator:
    """Validates product data against FDA/USDA requirements"""
    
    MANDATORY_FIELDS = [
        'product_name', 'category', 'net_quantity', 'ingredients',
        'manufacturer'
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
    
    # USDA Organic certification levels
    ORGANIC_LEVELS = ['100_percent', '95_percent', '70_percent', 'less_than_70']
    
    # Bioengineered disclosure options
    BE_DISCLOSURE_OPTIONS = [
        'bioengineered',
        'derived_from_bioengineering', 
        'contains_bioengineered_ingredients'
    ]
    
    @staticmethod
    def validate(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate product data and return (is_valid, errors)"""
        errors = []
        warnings = []
        
        # Check mandatory fields
        for field in FDAValidator.MANDATORY_FIELDS:
            if field not in data:
                errors.append(f"Missing mandatory field: {field}")
        
        if errors:
            return False, errors
        
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
        
        # Category-specific validation
        category = data.get('category', '')
        
        # Dietary Supplement validation
        if category == 'dietary_supplement':
            errors.extend(FDAValidator._validate_dietary_supplement(data))
        
        # Infant Formula validation
        elif category == 'infant_formula':
            errors.extend(FDAValidator._validate_infant_formula(data))
        
        # Meat/Poultry/Egg validation (USDA)
        elif category == 'meat_poultry_egg':
            errors.extend(FDAValidator._validate_meat_poultry(data))
        
        # Standard food validation
        else:
            # Nutrition Facts validation for non-supplements
            if 'nutrition_facts' not in data:
                errors.append("Missing required field: nutrition_facts")
            else:
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
        
        # Validate organic certification
        if data.get('is_organic'):
            errors.extend(FDAValidator._validate_organic(data))
        
        # Validate bioengineered disclosure
        if data.get('is_bioengineered'):
            errors.extend(FDAValidator._validate_bioengineered(data))
        
        # Validate nutrition claims
        if 'nutrition_claims' in data:
            errors.extend(FDAValidator._validate_nutrition_claims(data))
        
        # Validate health claims
        if 'health_claims' in data:
            errors.extend(FDAValidator._validate_health_claims(data))
        
        return len(errors) == 0, errors
    
    @staticmethod
    def _validate_dietary_supplement(data: Dict[str, Any]) -> List[str]:
        """Validate dietary supplement specific requirements"""
        errors = []
        
        if 'supplement_facts' not in data:
            errors.append("dietary_supplement category requires 'supplement_facts' field")
        else:
            sf = data['supplement_facts']
            required_fields = ['serving_size', 'servings_per_container']
            for field in required_fields:
                if field not in sf:
                    errors.append(f"supplement_facts missing required field: {field}")
            
            # Must have at least one supplement ingredient
            if 'ingredients' not in sf or len(sf.get('ingredients', [])) == 0:
                errors.append("supplement_facts must have at least one ingredient with amount and %DV")
        
        # FDA disclaimer is required
        if not data.get('fda_disclaimer', True):
            errors.append("Dietary supplements must include FDA disclaimer")
        
        return errors
    
    @staticmethod
    def _validate_infant_formula(data: Dict[str, Any]) -> List[str]:
        """Validate infant formula specific requirements (21 CFR 107)"""
        errors = []
        
        # Mandatory fields for infant formula
        required_fields = [
            'preparation_instructions',
            'use_by_date',
            'storage_instructions_opened'
        ]
        
        for field in required_fields:
            if field not in data:
                errors.append(f"infant_formula requires '{field}'")
        
        # Nutrition information is mandatory
        if 'nutrition_facts' not in data:
            errors.append("infant_formula requires 'nutrition_facts'")
        else:
            # Check for required nutrients in infant formula
            nf = data['nutrition_facts']
            required_nutrients = [
                'calories', 'protein', 'total_fat', 'total_carb',
                'vitamin_a', 'vitamin_d', 'vitamin_e', 'vitamin_k',
                'vitamin_c', 'thiamin', 'riboflavin', 'niacin',
                'vitamin_b6', 'vitamin_b12', 'folic_acid', 'pantothenic_acid',
                'biotin', 'calcium', 'phosphorus', 'magnesium', 'iron',
                'zinc', 'manganese', 'copper', 'iodine', 'sodium',
                'potassium', 'chloride'
            ]
            for nutrient in required_nutrients:
                if nutrient not in nf:
                    errors.append(f"infant_formula nutrition_facts missing required nutrient: {nutrient}")
        
        # Warning statement required
        if not data.get('physician_statement', True):
            errors.append("infant_formula must include 'Use as directed by physician' statement")
        
        return errors
    
    @staticmethod
    def _validate_meat_poultry(data: Dict[str, Any]) -> List[str]:
        """Validate USDA meat/poultry/egg requirements"""
        errors = []
        
        if 'usda_establishment_number' not in data:
            errors.append("meat_poultry_egg requires 'usda_establishment_number'")
        else:
            # Validate establishment number format (typically 1-5 digits)
            est_num = str(data['usda_establishment_number'])
            if not est_num.isdigit() or len(est_num) > 5:
                errors.append("usda_establishment_number must be 1-5 digits")
        
        if 'safe_handling_instructions' not in data:
            errors.append("meat_poultry_egg requires 'safe_handling_instructions'")
        
        # Keep refrigerated statement
        if 'storage_temperature' not in data:
            errors.append("meat_poultry_egg requires 'storage_temperature'")
        
        return errors
    
    @staticmethod
    def _validate_organic(data: Dict[str, Any]) -> List[str]:
        """Validate USDA Organic requirements"""
        errors = []
        
        organic_level = data.get('organic_level', '95_percent')
        if organic_level not in FDAValidator.ORGANIC_LEVELS:
            errors.append(f"organic_level must be one of: {', '.join(FDAValidator.ORGANIC_LEVELS)}")
        
        # Certifying agent required for 95% or more organic
        if organic_level in ['100_percent', '95_percent']:
            if 'organic_certifier' not in data:
                errors.append("Products labeled 'Organic' or '100% Organic' must include certifying agent information")
            else:
                certifier = data['organic_certifier']
                if not isinstance(certifier, dict) or 'name' not in certifier:
                    errors.append("organic_certifier must include 'name'")
        
        return errors
    
    @staticmethod
    def _validate_bioengineered(data: Dict[str, Any]) -> List[str]:
        """Validate Bioengineered Food Disclosure requirements (NBFDS)"""
        errors = []
        
        if 'be_disclosure_type' not in data:
            errors.append("Bioengineered products must specify 'be_disclosure_type'")
        else:
            disclosure_type = data['be_disclosure_type']
            if disclosure_type not in FDAValidator.BE_DISCLOSURE_OPTIONS:
                errors.append(f"be_disclosure_type must be one of: {', '.join(FDAValidator.BE_DISCLOSURE_OPTIONS)}")
        
        return errors
    
    @staticmethod
    def _validate_nutrition_claims(data: Dict[str, Any]) -> List[str]:
        """Validate nutrition claims against FDA criteria"""
        errors = []
        
        claims = data.get('nutrition_claims', [])
        nutrition_facts = data.get('nutrition_facts', {})
        
        for claim in claims:
            is_valid, message = FDANutritionClaimsValidator.validate_claim(claim, nutrition_facts)
            if not is_valid:
                errors.append(f"Invalid nutrition claim: {message}")
        
        return errors
    
    @staticmethod
    def _validate_health_claims(data: Dict[str, Any]) -> List[str]:
        """Validate health claims against FDA requirements"""
        errors = []
        
        claims = data.get('health_claims', [])
        
        for claim in claims:
            if claim not in FDANutritionClaimsValidator.HEALTH_CLAIMS:
                errors.append(f"Unknown health claim: {claim}. Must be FDA-authorized.")
        
        return errors


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
            
            # Add certifier info
            if 'organic_certifier' in data:
                certifier = data['organic_certifier']
                enriched['organic_certifier_display'] = certifier.get('name', '')
                if 'code' in certifier:
                    enriched['organic_certifier_display'] += f" ({certifier['code']})"
        
        # Add bioengineered disclosure
        if data.get('is_bioengineered'):
            enriched['be_disclosure_text'] = self._get_be_disclosure_text(data.get('be_disclosure_type', 'bioengineered'))
            enriched['show_be_disclosure'] = True
        
        # Add nutrition claims display
        if 'nutrition_claims' in data:
            enriched['nutrition_claims_display'] = [
                self._format_nutrition_claim(claim) for claim in data['nutrition_claims']
            ]
        
        # Add health claims display
        if 'health_claims' in data:
            enriched['health_claims_display'] = [
                FDANutritionClaimsValidator.HEALTH_CLAIMS.get(claim, {}).get('claim', '')
                for claim in data['health_claims']
            ]
        
        # Calculate font size requirements
        if 'pdp_dimensions' in data:
            pdp = data['pdp_dimensions']
            pdp_area = FDAFontSizeValidator.calculate_pdp_area(
                pdp.get('width', 4),
                pdp.get('height', 6),
                pdp.get('shape', 'rectangular')
            )
            min_font = FDAFontSizeValidator.get_minimum_font_size(pdp_area)
            enriched['min_font_size_inches'] = min_font
            enriched['min_font_size_points'] = FDAFontSizeValidator.inches_to_points(min_font)
        
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
            category_data['usda_establishment_number'] = data.get('usda_establishment_number', '')
            category_data['safe_handling_text'] = data.get('safe_handling_instructions', 
                'This product was prepared from inspected and passed meat and/or poultry. '
                'Some food products may contain bacteria that could cause illness if the product is mishandled or cooked improperly. '
                'For your protection, follow these safe handling instructions: '
                'Keep refrigerated or frozen. Thaw in refrigerator or microwave. '
                'Keep raw meat and poultry separate from other foods. Wash working surfaces, utensils, and hands after touching raw meat or poultry. '
                'Cook thoroughly. Keep hot foods hot. Refrigerate leftovers immediately or discard.')
            category_data['storage_temperature'] = data.get('storage_temperature', 'Keep Refrigerated at 40°F or below')
        
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
            category_data['surgeon_general_warning'] = (
                "GOVERNMENT WARNING: (1) According to the Surgeon General, women should not drink "
                "alcoholic beverages during pregnancy because of the risk of birth defects. "
                "(2) Consumption of alcoholic beverages impairs your ability to drive a car or "
                "operate machinery, and may cause health problems."
            )
        
        # Dietary supplements
        elif category == 'dietary_supplement':
            category_data['is_supplement'] = True
            category_data['show_fda_disclaimer'] = True
            category_data['fda_disclaimer_text'] = (
                "*These statements have not been evaluated by the Food and Drug Administration. "
                "This product is not intended to diagnose, treat, cure, or prevent any disease."
            )
            category_data['supplement_facts'] = data.get('supplement_facts', {})
        
        # Infant formula
        elif category == 'infant_formula':
            category_data['is_infant_formula'] = True
            category_data['show_preparation_instructions'] = True
            category_data['preparation_instructions'] = data.get('preparation_instructions', '')
            category_data['use_by_date'] = data.get('use_by_date', '')
            category_data['storage_instructions_opened'] = data.get('storage_instructions_opened', 
                'Use within 1 hour of preparation or refrigerate and use within 24 hours.')
            category_data['physician_statement'] = "Use as directed by a physician."
        
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
            '70_percent': 'Made with Organic Ingredients',
            'less_than_70': ''  # Cannot use USDA seal
        }
        return levels.get(level, 'Organic')
    
    def _get_be_disclosure_text(self, disclosure_type: str) -> str:
        """Get bioengineered disclosure text"""
        texts = {
            'bioengineered': 'Bioengineered Food',
            'derived_from_bioengineering': 'Derived from Bioengineering',
            'contains_bioengineered_ingredients': 'Contains Bioengineered Food Ingredients'
        }
        return texts.get(disclosure_type, 'Bioengineered Food')
    
    def _format_nutrition_claim(self, claim: str) -> str:
        """Format nutrition claim for display"""
        claim_display = {
            'fat_free': 'Fat Free',
            'low_fat': 'Low Fat',
            'reduced_fat': 'Reduced Fat',
            'saturated_fat_free': 'Saturated Fat Free',
            'low_saturated_fat': 'Low Saturated Fat',
            'cholesterol_free': 'Cholesterol Free',
            'low_cholesterol': 'Low Cholesterol',
            'sodium_free': 'Sodium Free',
            'very_low_sodium': 'Very Low Sodium',
            'low_sodium': 'Low Sodium',
            'reduced_sodium': 'Reduced Sodium',
            'calorie_free': 'Calorie Free',
            'low_calorie': 'Low Calorie',
            'reduced_calorie': 'Reduced Calorie',
            'sugar_free': 'Sugar Free',
            'no_added_sugars': 'No Added Sugars',
            'reduced_sugar': 'Reduced Sugar',
            'high_fiber': 'High Fiber',
            'good_source_fiber': 'Good Source of Fiber',
            'high_protein': 'High Protein',
            'good_source_protein': 'Good Source of Protein',
            'excellent_source': 'Excellent Source',
            'good_source': 'Good Source',
            'more': 'More'
        }
        return claim_display.get(claim, claim.replace('_', ' ').title())
    
    def _get_default_template(self) -> Template:
        """Return default Jinja2 template - BACK LABEL ONLY (no front)"""
        # Use back-only template (front is now AI-generated separately)
        template_path = Path(__file__).parent / 'label_template_us_back_only.html'
        if template_path.exists():
            with open(template_path, 'r', encoding='utf-8') as f:
                return Template(f.read())
        else:
            # Fallback to original template if back-only doesn't exist
            template_path = Path(__file__).parent / 'label_template_us.html'
            if template_path.exists():
                with open(template_path, 'r', encoding='utf-8') as f:
                    return Template(f.read())
            else:
                raise FileNotFoundError("label_template_us_back_only.html not found. Please create it first.")


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
        required=False,
        help='Output HTML file path (required unless --validate-only is used)'
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
    parser.add_argument(
        '--check-claims',
        action='store_true',
        help='Check and display valid nutrition claims for the product'
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
    
    # Check valid claims if requested
    if args.check_claims:
        nutrition_facts = product_data.get('nutrition_facts', {})
        valid_claims = FDANutritionClaimsValidator.get_valid_claims(nutrition_facts)
        if valid_claims:
            print("\n✓ Valid nutrition claims for this product:")
            for claim in valid_claims:
                print(f"  - {claim}")
        else:
            print("\n⚠ No standard nutrition claims qualify for this product")
    
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
