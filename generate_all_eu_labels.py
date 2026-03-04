#!/usr/bin/env python3
"""
Generate EU labels for all 10 food categories
"""

import json
import os
from label_generator_eu import EULabelGenerator, EUValidator

# Create output directory
os.makedirs('eu_labels_output', exist_ok=True)

# Sample data for all 10 EU categories
EU_SAMPLE_DATA = {
    # 1. Packaged Food
    "packaged_food": {
        "product_name": "Organic Granola Bars",
        "category": "packaged_food",
        "brand_name": "NatureBite",
        "product_description": "Crunchy Oat & Honey Bars",
        "net_quantity": {"value": 200, "unit": "g"},
        "ingredients": [
            {"name": "Rolled Oats", "percentage": 45, "is_allergen": True},
            {"name": "Honey", "percentage": 20},
            {"name": "Almonds", "percentage": 12, "is_allergen": True},
            {"name": "Sunflower Oil", "percentage": 8},
            {"name": "Rice Syrup", "percentage": 7},
            {"name": "Dried Cranberries", "percentage": 5},
            {"name": "Salt", "percentage": 1},
            {"name": "Emulsifier", "e_number": "E322", "functional_class": "Emulsifier"}
        ],
        "allergens": ["gluten", "tree nuts"],
        "nutrition_per_100g": {
            "energy_kj": 1850,
            "energy_kcal": 440,
            "fat": 18,
            "saturates": 2.5,
            "carbohydrate": 58,
            "sugars": 22,
            "fibre": 6,
            "protein": 9,
            "salt": 0.3
        },
        "date_type": "best_before",
        "best_before": "31/12/2026",
        "lot_number": "L2026045",
        "storage_conditions": "Store in a cool, dry place away from direct sunlight",
        "business_operator": {
            "name": "NatureBite GmbH",
            "address": "Hauptstraße 123, 80331 München, Germany",
            "phone": "+49 89 123456",
            "website": "www.naturebite.de"
        },
        "country_of_origin": "Germany",
        "ean_code": "4 012345 678901"
    },

    # 2. Fresh Meat
    "meat_fresh": {
        "product_name": "Premium Beef Sirloin Steak",
        "category": "meat_fresh",
        "brand_name": "FarmFresh",
        "product_description": "Grass-Fed Beef Steak",
        "net_quantity": {"value": 300, "unit": "g"},
        "ingredients": [
            {"name": "Beef Sirloin", "percentage": 100}
        ],
        "allergens": [],
        "nutrition_per_100g": {
            "energy_kj": 720,
            "energy_kcal": 172,
            "fat": 8.5,
            "saturates": 3.5,
            "carbohydrate": 0,
            "sugars": 0,
            "protein": 24,
            "salt": 0.1
        },
        "date_type": "use_by",
        "use_by": "25/02/2026",
        "lot_number": "M2026018",
        "storage_conditions": "Keep refrigerated at 0-4°C. Once opened, consume within 2 days",
        "business_operator": {
            "name": "FarmFresh Meats Ltd",
            "address": "Rural Lane 45, Dublin D12, Ireland",
            "phone": "+353 1 234567"
        },
        "country_of_origin": "Ireland",
        "country_of_rearing": "Ireland",
        "country_of_slaughter": "Ireland",
        "previously_frozen": False,
        "ean_code": "5 390123 456789"
    },

    # 3. Fish & Seafood
    "fish_seafood": {
        "product_name": "Atlantic Salmon Fillet",
        "category": "fish_seafood",
        "brand_name": "OceanCatch",
        "product_description": "Fresh Salmon Fillet, Skin-On",
        "net_quantity": {"value": 250, "unit": "g"},
        "ingredients": [
            {"name": "Atlantic Salmon (Salmo salar)", "percentage": 100, "is_allergen": True}
        ],
        "allergens": ["fish"],
        "nutrition_per_100g": {
            "energy_kj": 920,
            "energy_kcal": 220,
            "fat": 13,
            "saturates": 2.5,
            "carbohydrate": 0,
            "sugars": 0,
            "protein": 25,
            "salt": 0.1
        },
        "date_type": "use_by",
        "use_by": "22/02/2026",
        "lot_number": "F2026022",
        "storage_conditions": "Keep refrigerated at 0-2°C. Consume on day of purchase",
        "business_operator": {
            "name": "OceanCatch AS",
            "address": "Havnegata 12, 5003 Bergen, Norway",
            "phone": "+47 55 123456"
        },
        "country_of_origin": "Norway",
        "catch_method": "Farmed",
        "catch_area": "FAO 27 - Northeast Atlantic",
        "wild_or_farmed": "Farmed",
        "latin_name": "Salmo salar",
        "ean_code": "7 038010 123456"
    },

    # 4. Dairy
    "dairy": {
        "product_name": "Greek Style Yogurt",
        "category": "dairy",
        "brand_name": "Olympus",
        "product_description": "Authentic Greek Strained Yogurt",
        "net_quantity": {"value": 500, "unit": "g"},
        "ingredients": [
            {"name": "Pasteurized Cow's Milk", "percentage": 98, "is_allergen": True},
            {"name": "Live Yogurt Cultures", "percentage": 2}
        ],
        "allergens": ["milk"],
        "nutrition_per_100g": {
            "energy_kj": 420,
            "energy_kcal": 100,
            "fat": 5,
            "saturates": 3.5,
            "carbohydrate": 4,
            "sugars": 4,
            "protein": 9,
            "salt": 0.1
        },
        "fat_percentage": 5,
        "date_type": "use_by",
        "use_by": "05/03/2026",
        "lot_number": "D2026048",
        "storage_conditions": "Keep refrigerated at 2-6°C. Once opened, consume within 3 days",
        "business_operator": {
            "name": "Olympus Dairy SA",
            "address": "Thessaloniki Industrial Zone, 57001 Greece",
            "phone": "+30 231 0123456"
        },
        "country_of_origin": "Greece",
        "pasteurization": "Pasteurized",
        "ean_code": "5 201234 567890"
    },

    # 5. Frozen Food
    "frozen_food": {
        "product_name": "Mixed Garden Vegetables",
        "category": "frozen_food",
        "brand_name": "FrostFresh",
        "product_description": "Premium Frozen Vegetable Mix",
        "net_quantity": {"value": 750, "unit": "g"},
        "ingredients": [
            {"name": "Green Peas", "percentage": 30},
            {"name": "Carrots", "percentage": 25},
            {"name": "Green Beans", "percentage": 20},
            {"name": "Sweetcorn", "percentage": 15},
            {"name": "Broccoli", "percentage": 10}
        ],
        "allergens": [],
        "nutrition_per_100g": {
            "energy_kj": 280,
            "energy_kcal": 67,
            "fat": 0.5,
            "saturates": 0.1,
            "carbohydrate": 10,
            "sugars": 4,
            "fibre": 4,
            "protein": 4,
            "salt": 0.02
        },
        "date_type": "best_before",
        "best_before": "31/12/2027",
        "lot_number": "FZ2026015",
        "storage_conditions": "Keep frozen at -18°C or below. Do not refreeze once thawed",
        "frozen_date": "15/01/2026",
        "defrosting_instructions": "Cook from frozen. Do not thaw before cooking",
        "business_operator": {
            "name": "FrostFresh BV",
            "address": "Industrieweg 78, 1234 AB Amsterdam, Netherlands",
            "phone": "+31 20 1234567"
        },
        "country_of_origin": "Netherlands",
        "ean_code": "8 710123 456789"
    },

    # 6. Organic
    "organic": {
        "product_name": "Extra Virgin Olive Oil",
        "category": "organic",
        "brand_name": "Terra Verde",
        "product_description": "Cold-Pressed Organic Olive Oil",
        "net_quantity": {"value": 500, "unit": "ml"},
        "ingredients": [
            {"name": "Organic Extra Virgin Olive Oil", "percentage": 100}
        ],
        "allergens": [],
        "nutrition_per_100g": {
            "energy_kj": 3700,
            "energy_kcal": 884,
            "fat": 100,
            "saturates": 14,
            "carbohydrate": 0,
            "sugars": 0,
            "protein": 0,
            "salt": 0
        },
        "is_organic": True,
        "organic_certification": "IT-BIO-006",
        "organic_percentage": 100,
        "organic_origin": "EU Agriculture",
        "date_type": "best_before",
        "best_before": "30/06/2027",
        "lot_number": "OL2026008",
        "storage_conditions": "Store in a cool, dark place. Best consumed within 6 months of opening",
        "business_operator": {
            "name": "Terra Verde Srl",
            "address": "Via Oliveto 45, 50125 Firenze, Italy",
            "phone": "+39 055 123456",
            "website": "www.terraverde.it"
        },
        "country_of_origin": "Italy",
        "ean_code": "8 001234 567890"
    },

    # 7. Food Supplement
    "food_supplement": {
        "product_name": "Vitamin D3 1000 IU",
        "category": "food_supplement",
        "brand_name": "VitaPlus",
        "product_description": "High Strength Vitamin D3 Capsules",
        "net_quantity": {"value": 60, "unit": "g"},
        "serving_size": "1 capsule",
        "servings_per_container": 90,
        "ingredients": [
            {"name": "Sunflower Oil"},
            {"name": "Gelatin (Bovine)", "is_allergen": False},
            {"name": "Glycerol"},
            {"name": "Cholecalciferol (Vitamin D3)"},
            {"name": "Antioxidant", "e_number": "E306", "functional_class": "Antioxidant"}
        ],
        "allergens": [],
        "nutrition_per_100g": {
            "energy_kj": 2500,
            "energy_kcal": 600,
            "fat": 65,
            "saturates": 8,
            "carbohydrate": 5,
            "sugars": 0,
            "protein": 10,
            "salt": 0
        },
        "supplement_facts": {
            "vitamin_d3": {"amount": "25μg (1000 IU)", "nrv": "500%"}
        },
        "date_type": "best_before",
        "best_before": "31/12/2027",
        "lot_number": "VS2026033",
        "storage_conditions": "Store in a cool, dry place below 25°C. Keep out of reach of children",
        "warnings": "Do not exceed the recommended daily dose. Food supplements should not be used as a substitute for a varied diet.",
        "business_operator": {
            "name": "VitaPlus Supplements Ltd",
            "address": "Health Park 12, London SW1A 1AA, United Kingdom",
            "phone": "+44 20 12345678"
        },
        "country_of_origin": "United Kingdom",
        "ean_code": "5 012345 678901"
    },

    # 8. Alcoholic Beverage
    "alcoholic_beverage": {
        "product_name": "Château Bordeaux Rouge",
        "category": "alcoholic_beverage",
        "brand_name": "Château Margaux",
        "product_description": "2020 Vintage Red Wine",
        "net_quantity": {"value": 750, "unit": "ml"},
        "ingredients": [
            {"name": "Grapes (Merlot, Cabernet Sauvignon)"},
            {"name": "Sulphites", "is_allergen": True, "e_number": "E220"}
        ],
        "allergens": ["sulphites"],
        "nutrition_per_100g": {
            "energy_kj": 290,
            "energy_kcal": 70,
            "fat": 0,
            "saturates": 0,
            "carbohydrate": 2.5,
            "sugars": 0.5,
            "protein": 0.1,
            "salt": 0
        },
        "abv": 13.5,
        "contains_sulphites": True,
        "vintage": 2020,
        "grape_varieties": ["Merlot (60%)", "Cabernet Sauvignon (40%)"],
        "date_type": "best_before",
        "best_before": "Best enjoyed within 10 years",
        "lot_number": "W2020045",
        "storage_conditions": "Store horizontally in a cool, dark place at 12-16°C",
        "business_operator": {
            "name": "Château Margaux SARL",
            "address": "33460 Margaux, Bordeaux, France",
            "phone": "+33 5 57 88 83 83"
        },
        "country_of_origin": "France",
        "appellation": "Margaux AOC",
        "ean_code": "3 012345 678901"
    },

    # 9. Fresh Produce
    "fresh_produce": {
        "product_name": "Valencia Oranges",
        "category": "fresh_produce",
        "brand_name": "SunCitrus",
        "product_description": "Premium Spanish Oranges",
        "net_quantity": {"value": 1, "unit": "kg"},
        "ingredients": [
            {"name": "Fresh Oranges (Citrus sinensis)", "percentage": 100}
        ],
        "allergens": [],
        "nutrition_per_100g": {
            "energy_kj": 197,
            "energy_kcal": 47,
            "fat": 0.1,
            "saturates": 0,
            "carbohydrate": 12,
            "sugars": 9,
            "fibre": 2.4,
            "protein": 0.9,
            "salt": 0
        },
        "variety": "Valencia Late",
        "class": "Class I",
        "size": "Medium (70-80mm)",
        "date_type": "best_before",
        "best_before": "28/02/2026",
        "lot_number": "P2026007",
        "storage_conditions": "Store at room temperature or refrigerate for longer freshness",
        "business_operator": {
            "name": "SunCitrus Cooperativa",
            "address": "Carretera Valencia 45, 46001 Valencia, Spain",
            "phone": "+34 96 123 4567"
        },
        "country_of_origin": "Spain",
        "ean_code": "8 412345 678901"
    },

    # 10. Infant Food
    "infant_food": {
        "product_name": "Organic Baby Rice Cereal",
        "category": "infant_food",
        "brand_name": "BabyNature",
        "product_description": "First Foods Rice Cereal - From 4 Months",
        "net_quantity": {"value": 200, "unit": "g"},
        "ingredients": [
            {"name": "Organic Rice Flour", "percentage": 95},
            {"name": "Vitamin B1 (Thiamin)"},
            {"name": "Iron (Ferric Pyrophosphate)"}
        ],
        "allergens": [],
        "nutrition_per_100g": {
            "energy_kj": 1600,
            "energy_kcal": 380,
            "fat": 1.5,
            "saturates": 0.3,
            "carbohydrate": 82,
            "sugars": 0.5,
            "fibre": 1,
            "protein": 7,
            "salt": 0.01
        },
        "is_organic": True,
        "organic_certification": "DE-ÖKO-001",
        "organic_percentage": 95,
        "suitable_from_months": 4,
        "preparation_instructions": "Mix 1-2 tablespoons with breast milk, formula, or water. Stir until smooth. Always test temperature before feeding.",
        "date_type": "best_before",
        "best_before": "30/09/2026",
        "lot_number": "IF2026012",
        "storage_conditions": "Store in a cool, dry place. Once opened, use within 4 weeks and keep tightly sealed",
        "warnings": "Important: Breast milk is best for babies. This product should only be used on the advice of a healthcare professional.",
        "business_operator": {
            "name": "BabyNature GmbH",
            "address": "Kinderstraße 10, 80333 München, Germany",
            "phone": "+49 89 987654"
        },
        "country_of_origin": "Germany",
        "ean_code": "4 001234 567890"
    }
}


def generate_all_labels():
    """Generate labels for all EU categories"""
    generator = EULabelGenerator()
    
    print("=" * 60)
    print("EU LABEL GENERATOR - All 10 Categories")
    print("=" * 60)
    
    for category, data in EU_SAMPLE_DATA.items():
        print(f"\n📦 Generating: {category}")
        
        # Save JSON data
        json_path = f"eu_dataset/{category}.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"   ✓ Data saved: {json_path}")
        
        # Validate
        is_valid, errors = EUValidator.validate(data)
        if not is_valid:
            print(f"   ✗ Validation failed:")
            for error in errors:
                print(f"     - {error}")
            continue
        
        # Generate label
        try:
            output_path = f"eu_labels_output/eu_label_{category}.html"
            generator.generate(data, output_path)
            print(f"   ✓ Label generated: {output_path}")
        except Exception as e:
            print(f"   ✗ Error: {e}")
    
    print("\n" + "=" * 60)
    print("✓ All EU labels generated successfully!")
    print("=" * 60)
    print("\nOutput files in: eu_labels_output/")
    print("Data files in: eu_dataset/")


if __name__ == "__main__":
    generate_all_labels()