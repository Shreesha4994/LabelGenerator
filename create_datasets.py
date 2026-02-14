#!/usr/bin/env python3
"""
Script to create comprehensive sample datasets for all three regions
"""

import json
import os

# India Dataset Samples
india_samples = {
    "02_dairy_milk.json": {
        "product_name": "Full Cream Milk",
        "category": "dairy",
        "veg_status": "veg",
        "net_quantity": {"value": 500, "unit": "ml"},
        "ingredients": [
            {"name": "Fresh Cow Milk", "percentage": 100}
        ],
        "nutrition_per_100g": {
            "energy_kcal": 66,
            "protein": 3.2,
            "carbohydrates": 4.8,
            "fat": 3.5,
            "saturated_fat": 2.2,
            "sugar": 4.8,
            "sodium": 0.04
        },
        "fssai_license": "10012345678902",
        "manufacturer": {
            "name": "Pure Dairy Products Ltd",
            "address": "Village Khera, Sonipat, Haryana 131001, India"
        },
        "batch_number": "MD2026014",
        "mfg_date": "2026-02-14",
        "best_before_days": 3,
        "mrp": 28.00,
        "fat_percentage": 3.5,
        "milk_source": "Cow",
        "storage_instructions": "Keep refrigerated at 4°C or below"
    },
    
    "03_beverage_juice.json": {
        "product_name": "Mango Fruit Drink",
        "category": "beverage_juice",
        "veg_status": "veg",
        "net_quantity": {"value": 200, "unit": "ml"},
        "ingredients": [
            {"name": "Water", "percentage": 55},
            {"name": "Mango Pulp", "percentage": 40},
            {"name": "Sugar", "percentage": 4},
            {"name": "Citric Acid", "ins_number": "330", "class_name": "Acidity Regulator"},
            {"name": "Vitamin C", "ins_number": "300", "class_name": "Antioxidant"}
        ],
        "nutrition_per_100g": {
            "energy_kcal": 52,
            "protein": 0.2,
            "carbohydrates": 13,
            "fat": 0,
            "sugar": 12,
            "sodium": 0.01
        },
        "fssai_license": "10012345678903",
        "manufacturer": {
            "name": "Tropical Beverages Pvt Ltd",
            "address": "Survey No. 123, MIDC Area, Pune, Maharashtra 411019, India"
        },
        "batch_number": "MJ2026014",
        "mfg_date": "2026-02-14",
        "best_before_months": 9,
        "mrp": 20.00,
        "fruit_percentage": 40,
        "storage_instructions": "Store in a cool, dry place. Refrigerate after opening"
    },
    
    "04_meat_chicken.json": {
        "product_name": "Fresh Chicken Breast",
        "category": "meat_fish_egg",
        "veg_status": "non-veg",
        "net_quantity": {"value": 500, "unit": "g"},
        "ingredients": [
            {"name": "Fresh Chicken Breast", "percentage": 100}
        ],
        "nutrition_per_100g": {
            "energy_kcal": 165,
            "protein": 31,
            "carbohydrates": 0,
            "fat": 3.6,
            "saturated_fat": 1,
            "sodium": 0.07
        },
        "fssai_license": "10012345678904",
        "manufacturer": {
            "name": "Fresh Poultry Farms Ltd",
            "address": "Khasra No. 456, Village Bahadurgarh, Haryana 124507, India"
        },
        "batch_number": "CB2026014",
        "mfg_date": "2026-02-14",
        "best_before_days": 2,
        "mrp": 250.00,
        "storage_temperature": "Store below 4°C",
        "storage_instructions": "Keep refrigerated. Cook thoroughly before consumption"
    },
    
    "05_fortified_flour.json": {
        "product_name": "Fortified Wheat Flour (Atta)",
        "category": "fortified",
        "veg_status": "veg",
        "net_quantity": {"value": 5, "unit": "kg"},
        "ingredients": [
            {"name": "Whole Wheat", "percentage": 99.5},
            {"name": "Iron", "percentage": 0.003},
            {"name": "Folic Acid", "percentage": 0.00001},
            {"name": "Vitamin B12", "percentage": 0.000001}
        ],
        "nutrition_per_100g": {
            "energy_kcal": 341,
            "protein": 12,
            "carbohydrates": 69,
            "fat": 1.7,
            "fiber": 11,
            "sodium": 0.01
        },
        "fssai_license": "10012345678905",
        "manufacturer": {
            "name": "Healthy Grains Mills Pvt Ltd",
            "address": "Industrial Plot 789, Ludhiana, Punjab 141003, India"
        },
        "batch_number": "FA2026014",
        "mfg_date": "2026-02-14",
        "best_before_months": 6,
        "mrp": 250.00,
        "is_fortified": True,
        "fortification_details": "Fortified with Iron (28-42.5 ppm), Folic Acid (75-125 mcg/kg), Vitamin B12 (0.75-1.25 mcg/kg)",
        "storage_instructions": "Store in a cool, dry place in an airtight container"
    },
    
    "06_organic_cookies.json": {
        "product_name": "Organic Oat Cookies",
        "category": "organic",
        "veg_status": "veg",
        "net_quantity": {"value": 150, "unit": "g"},
        "ingredients": [
            {"name": "Organic Oats", "percentage": 50},
            {"name": "Organic Jaggery", "percentage": 25},
            {"name": "Organic Coconut Oil", "percentage": 15},
            {"name": "Organic Raisins", "percentage": 8},
            {"name": "Organic Cardamom Powder", "percentage": 2}
        ],
        "allergens": ["tree nuts"],
        "nutrition_per_100g": {
            "energy_kcal": 420,
            "protein": 8,
            "carbohydrates": 58,
            "fat": 16,
            "fiber": 6,
            "sugar": 22,
            "sodium": 0.02
        },
        "fssai_license": "10012345678906",
        "manufacturer": {
            "name": "Organic Foods India Pvt Ltd",
            "address": "Eco Park, Sector 15, Faridabad, Haryana 121007, India"
        },
        "batch_number": "OC2026014",
        "mfg_date": "2026-02-14",
        "best_before_months": 4,
        "mrp": 120.00,
        "is_organic": True,
        "organic_certification": "India Organic (NPOP)",
        "storage_instructions": "Store in a cool, dry place"
    },
    
    "07_frozen_vegetables.json": {
        "product_name": "Mixed Frozen Vegetables",
        "category": "frozen",
        "veg_status": "veg",
        "net_quantity": {"value": 400, "unit": "g"},
        "ingredients": [
            {"name": "Green Peas", "percentage": 30},
            {"name": "Carrots", "percentage": 25},
            {"name": "Beans", "percentage": 25},
            {"name": "Corn", "percentage": 20}
        ],
        "nutrition_per_100g": {
            "energy_kcal": 65,
            "protein": 3.5,
            "carbohydrates": 12,
            "fat": 0.5,
            "fiber": 4,
            "sodium": 0.03
        },
        "fssai_license": "10012345678907",
        "manufacturer": {
            "name": "Frozen Fresh Foods Ltd",
            "address": "Cold Storage Complex, NH-44, Panipat, Haryana 132103, India"
        },
        "batch_number": "FV2026014",
        "mfg_date": "2026-02-14",
        "best_before_months": 12,
        "mrp": 80.00,
        "storage_temperature": "-18°C or below",
        "thawing_instructions": "Do not refreeze after thawing. Cook from frozen or thaw in refrigerator",
        "storage_instructions": "Keep frozen at -18°C or below"
    },
    
    "08_ready_to_eat_meal.json": {
        "product_name": "Dal Makhani Ready to Eat",
        "category": "ready_to_eat",
        "veg_status": "veg",
        "net_quantity": {"value": 300, "unit": "g"},
        "ingredients": [
            {"name": "Black Lentils", "percentage": 40},
            {"name": "Water", "percentage": 30},
            {"name": "Tomato Puree", "percentage": 15},
            {"name": "Butter", "percentage": 8},
            {"name": "Cream", "percentage": 5},
            {"name": "Spices", "percentage": 2}
        ],
        "allergens": ["milk"],
        "nutrition_per_100g": {
            "energy_kcal": 145,
            "protein": 6,
            "carbohydrates": 15,
            "fat": 6,
            "fiber": 3,
            "sodium": 0.45
        },
        "fssai_license": "10012345678908",
        "manufacturer": {
            "name": "Ready Meals India Pvt Ltd",
            "address": "Food Park, Plot 234, Manesar, Haryana 122051, India"
        },
        "batch_number": "DM2026014",
        "mfg_date": "2026-02-14",
        "best_before_months": 12,
        "mrp": 85.00,
        "storage_instructions": "Store in a cool, dry place. Refrigerate after opening and consume within 2 days"
    },
    
    "09_imported_chocolate.json": {
        "product_name": "Swiss Dark Chocolate",
        "category": "imported",
        "veg_status": "veg",
        "net_quantity": {"value": 100, "unit": "g"},
        "ingredients": [
            {"name": "Cocoa Mass", "percentage": 70},
            {"name": "Sugar", "percentage": 28},
            {"name": "Cocoa Butter", "percentage": 1.5},
            {"name": "Emulsifier (Soy Lecithin)", "ins_number": "322", "percentage": 0.5}
        ],
        "allergens": ["soy"],
        "nutrition_per_100g": {
            "energy_kcal": 550,
            "protein": 8,
            "carbohydrates": 35,
            "fat": 42,
            "saturated_fat": 25,
            "sugar": 28,
            "sodium": 0.01
        },
        "fssai_license": "10012345678909",
        "manufacturer": {
            "name": "Swiss Chocolates SA",
            "address": "Zurich, Switzerland"
        },
        "importer_name": "Premium Imports India Pvt Ltd",
        "importer_address": "Import House, Connaught Place, New Delhi 110001, India",
        "batch_number": "SC2026014",
        "mfg_date": "2026-01-15",
        "best_before_months": 18,
        "mrp": 450.00,
        "is_imported": True,
        "country_of_origin": "Switzerland",
        "storage_instructions": "Store in a cool, dry place below 20°C"
    },
    
    "10_beverage_soda.json": {
        "product_name": "Lemon Lime Soda",
        "category": "beverage_carbonated",
        "veg_status": "veg",
        "net_quantity": {"value": 600, "unit": "ml"},
        "ingredients": [
            {"name": "Carbonated Water", "percentage": 88},
            {"name": "Sugar", "percentage": 10},
            {"name": "Citric Acid", "ins_number": "330", "class_name": "Acidity Regulator"},
            {"name": "Natural Lemon Flavour"},
            {"name": "Natural Lime Flavour"},
            {"name": "Sodium Benzoate", "ins_number": "211", "class_name": "Preservative"}
        ],
        "nutrition_per_100g": {
            "energy_kcal": 42,
            "protein": 0,
            "carbohydrates": 10.5,
            "fat": 0,
            "sugar": 10.5,
            "sodium": 0.01
        },
        "fssai_license": "10012345678910",
        "manufacturer": {
            "name": "Refreshing Beverages Ltd",
            "address": "Beverage Park, Sector 59, Noida, Uttar Pradesh 201301, India"
        },
        "batch_number": "LL2026014",
        "mfg_date": "2026-02-14",
        "best_before_months": 9,
        "mrp": 40.00,
        "contains_caffeine": False,
        "storage_instructions": "Store in a cool, dry place. Best served chilled"
    },
    
    "11_fresh_produce.json": {
        "product_name": "Pre-washed Baby Spinach",
        "category": "fresh_produce",
        "veg_status": "veg",
        "net_quantity": {"value": 200, "unit": "g"},
        "ingredients": [
            {"name": "Fresh Baby Spinach", "percentage": 100}
        ],
        "nutrition_per_100g": {
            "energy_kcal": 23,
            "protein": 2.9,
            "carbohydrates": 3.6,
            "fat": 0.4,
            "fiber": 2.2,
            "sodium": 0.08
        },
        "fssai_license": "10012345678911",
        "manufacturer": {
            "name": "Fresh Greens Farms Pvt Ltd",
            "address": "Farm House 567, Okhla, New Delhi 110020, India"
        },
        "batch_number": "SP2026014",
        "mfg_date": "2026-02-14",
        "best_before_days": 5,
        "mrp": 60.00,
        "storage_instructions": "Keep refrigerated at 4°C or below. Consume within 5 days of opening"
    }
}

# Create India samples
print("Creating India dataset samples...")
for filename, data in india_samples.items():
    filepath = f"india_dataset/{filename}"
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"✓ Created {filepath}")

print(f"\n✓ Created {len(india_samples)} India sample files")
print("India dataset complete!")