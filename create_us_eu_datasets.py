#!/usr/bin/env python3
"""
Script to create US and EU sample datasets
"""

import json
import os

# US Dataset Samples
us_samples = {
    "01_packaged_food.json": {
        "product_name": "Organic Almond Butter",
        "category": "packaged_food",
        "net_quantity": {
            "us_value": 16,
            "us_unit": "oz",
            "metric_value": 454,
            "metric_unit": "g"
        },
        "nutrition_facts": {
            "serving_size": "2 tbsp (32g)",
            "servings_per_container": 14,
            "calories": 190,
            "total_fat": {"value": 17, "dv": 22},
            "saturated_fat": {"value": 1.5, "dv": 8},
            "trans_fat": 0,
            "cholesterol": {"value": 0, "dv": 0},
            "sodium": {"value": 0, "dv": 0},
            "total_carb": {"value": 6, "dv": 2},
            "fiber": {"value": 3, "dv": 11},
            "total_sugars": 2,
            "added_sugars": {"value": 0, "dv": 0},
            "protein": 7,
            "vitamin_d": {"value": 0, "dv": 0},
            "calcium": {"value": 80, "dv": 6},
            "iron": {"value": 1, "dv": 6},
            "potassium": {"value": 240, "dv": 5}
        },
        "ingredients": ["Organic Dry Roasted Almonds", "Sea Salt"],
        "allergens": ["tree nuts (almonds)"],
        "manufacturer": {
            "name": "American Harvest Foods LLC",
            "city": "Portland",
            "state": "OR",
            "zip": "97201",
            "phone": "1-800-555-FOOD",
            "website": "www.americanharvestfoods.com"
        },
        "is_organic": True,
        "organic_level": "100_percent",
        "best_before": "12/31/2026",
        "lot_code": "2026US014",
        "upc_code": "0 12345 67890 5",
        "storage_instructions": "Store in a cool, dry place. Refrigerate after opening."
    },
    
    "02_meat_poultry.json": {
        "product_name": "Fresh Ground Turkey",
        "category": "meat_poultry_egg",
        "net_quantity": {
            "us_value": 1,
            "us_unit": "lb",
            "metric_value": 454,
            "metric_unit": "g"
        },
        "nutrition_facts": {
            "serving_size": "4 oz (112g)",
            "servings_per_container": 4,
            "calories": 170,
            "total_fat": {"value": 8, "dv": 10},
            "saturated_fat": {"value": 2.5, "dv": 13},
            "trans_fat": 0,
            "cholesterol": {"value": 90, "dv": 30},
            "sodium": {"value": 70, "dv": 3},
            "total_carb": {"value": 0, "dv": 0},
            "fiber": {"value": 0, "dv": 0},
            "total_sugars": 0,
            "added_sugars": {"value": 0, "dv": 0},
            "protein": 22,
            "vitamin_d": {"value": 0, "dv": 0},
            "calcium": {"value": 20, "dv": 2},
            "iron": {"value": 1.5, "dv": 8},
            "potassium": {"value": 300, "dv": 6}
        },
        "ingredients": ["Ground Turkey"],
        "manufacturer": {
            "name": "Fresh Farms Poultry Inc",
            "city": "Minneapolis",
            "state": "MN",
            "zip": "55401"
        },
        "usda_establishment_number": "P-1234",
        "safe_handling_instructions": "Keep refrigerated or frozen. Thaw in refrigerator or microwave. Keep raw meat and poultry separate from other foods. Wash working surfaces, utensils, and hands after touching raw meat or poultry. Cook thoroughly to 165°F. Keep hot foods hot. Refrigerate leftovers immediately.",
        "best_before": "02/20/2026",
        "lot_code": "GT2026014"
    },
    
    "03_dairy_cheese.json": {
        "product_name": "Sharp Cheddar Cheese",
        "category": "dairy",
        "net_quantity": {
            "us_value": 8,
            "us_unit": "oz",
            "metric_value": 227,
            "metric_unit": "g"
        },
        "nutrition_facts": {
            "serving_size": "1 oz (28g)",
            "servings_per_container": 8,
            "calories": 110,
            "total_fat": {"value": 9, "dv": 12},
            "saturated_fat": {"value": 6, "dv": 30},
            "trans_fat": 0,
            "cholesterol": {"value": 30, "dv": 10},
            "sodium": {"value": 180, "dv": 8},
            "total_carb": {"value": 1, "dv": 0},
            "fiber": {"value": 0, "dv": 0},
            "total_sugars": 0,
            "added_sugars": {"value": 0, "dv": 0},
            "protein": 7,
            "vitamin_d": {"value": 0, "dv": 0},
            "calcium": {"value": 200, "dv": 15},
            "iron": {"value": 0, "dv": 0},
            "potassium": {"value": 30, "dv": 0}
        },
        "ingredients": ["Pasteurized Milk", "Cheese Cultures", "Salt", "Enzymes"],
        "allergens": ["milk"],
        "manufacturer": {
            "name": "Wisconsin Cheese Co",
            "city": "Madison",
            "state": "WI",
            "zip": "53703"
        },
        "milk_fat_percentage": 33,
        "best_before": "04/15/2026",
        "lot_code": "CH2026014",
        "storage_instructions": "Keep refrigerated"
    },
    
    "04_alcoholic_beer.json": {
        "product_name": "Craft IPA Beer",
        "category": "beverage_alcoholic",
        "net_quantity": {
            "us_value": 12,
            "us_unit": "fl oz",
            "metric_value": 355,
            "metric_unit": "ml"
        },
        "nutrition_facts": {
            "serving_size": "12 fl oz (355ml)",
            "servings_per_container": 1,
            "calories": 180,
            "total_fat": {"value": 0, "dv": 0},
            "saturated_fat": {"value": 0, "dv": 0},
            "trans_fat": 0,
            "cholesterol": {"value": 0, "dv": 0},
            "sodium": {"value": 15, "dv": 1},
            "total_carb": {"value": 14, "dv": 5},
            "fiber": {"value": 0, "dv": 0},
            "total_sugars": 0,
            "added_sugars": {"value": 0, "dv": 0},
            "protein": 2,
            "vitamin_d": {"value": 0, "dv": 0},
            "calcium": {"value": 20, "dv": 2},
            "iron": {"value": 0, "dv": 0},
            "potassium": {"value": 100, "dv": 2}
        },
        "ingredients": ["Water", "Malted Barley", "Hops", "Yeast"],
        "manufacturer": {
            "name": "Craft Brewing Company",
            "city": "Denver",
            "state": "CO",
            "zip": "80202"
        },
        "abv": 6.5,
        "contains_sulfites": True,
        "surgeon_general_warning": "GOVERNMENT WARNING: (1) According to the Surgeon General, women should not drink alcoholic beverages during pregnancy because of the risk of birth defects. (2) Consumption of alcoholic beverages impairs your ability to drive a car or operate machinery, and may cause health problems.",
        "best_before": "08/01/2026",
        "lot_code": "IPA2026014"
    },
    
    "05_dietary_supplement.json": {
        "product_name": "Vitamin C 1000mg",
        "category": "dietary_supplement",
        "net_quantity": {
            "us_value": 100,
            "us_unit": "tablets",
            "metric_value": 100,
            "metric_unit": "tablets"
        },
        "supplement_facts": {
            "serving_size": "1 tablet",
            "servings_per_container": 100,
            "vitamin_c": {"amount": "1000mg", "dv": "1111%"}
        },
        "ingredients": ["Ascorbic Acid (Vitamin C)", "Microcrystalline Cellulose", "Stearic Acid", "Silicon Dioxide"],
        "manufacturer": {
            "name": "Health Supplements USA Inc",
            "city": "Los Angeles",
            "state": "CA",
            "zip": "90001"
        },
        "best_before": "12/31/2027",
        "lot_code": "VC2026014",
        "storage_instructions": "Store in a cool, dry place"
    },
    
    "06_infant_formula.json": {
        "product_name": "Infant Formula Powder",
        "category": "infant_formula",
        "net_quantity": {
            "us_value": 12.4,
            "us_unit": "oz",
            "metric_value": 352,
            "metric_unit": "g"
        },
        "nutrition_facts": {
            "serving_size": "5 fl oz prepared (148ml)",
            "servings_per_container": 26,
            "calories": 100,
            "total_fat": {"value": 5.3, "dv": 7},
            "saturated_fat": {"value": 2.3, "dv": 12},
            "trans_fat": 0,
            "cholesterol": {"value": 5, "dv": 2},
            "sodium": {"value": 27, "dv": 1},
            "total_carb": {"value": 11, "dv": 4},
            "fiber": {"value": 0, "dv": 0},
            "total_sugars": 11,
            "added_sugars": {"value": 0, "dv": 0},
            "protein": 2.1,
            "vitamin_d": {"value": 1.5, "dv": 8},
            "calcium": {"value": 78, "dv": 6},
            "iron": {"value": 1.8, "dv": 10},
            "potassium": {"value": 108, "dv": 2}
        },
        "ingredients": ["Nonfat Milk", "Lactose", "Palm Olein", "Soy Oil", "Coconut Oil", "Whey Protein Concentrate"],
        "allergens": ["milk", "soy"],
        "manufacturer": {
            "name": "Baby Nutrition Corp",
            "city": "Columbus",
            "state": "OH",
            "zip": "43004"
        },
        "preparation_instructions": "Wash hands. Measure and pour desired amount of water into bottle. Add powder. Cap bottle and shake. Feed or store immediately in refrigerator.",
        "best_before": "10/01/2026",
        "lot_code": "IF2026014"
    },
    
    "07_organic_granola.json": {
        "product_name": "Organic Granola",
        "category": "organic",
        "net_quantity": {
            "us_value": 12,
            "us_unit": "oz",
            "metric_value": 340,
            "metric_unit": "g"
        },
        "nutrition_facts": {
            "serving_size": "1/2 cup (55g)",
            "servings_per_container": 6,
            "calories": 250,
            "total_fat": {"value": 10, "dv": 13},
            "saturated_fat": {"value": 1, "dv": 5},
            "trans_fat": 0,
            "cholesterol": {"value": 0, "dv": 0},
            "sodium": {"value": 5, "dv": 0},
            "total_carb": {"value": 37, "dv": 13},
            "fiber": {"value": 5, "dv": 18},
            "total_sugars": 12,
            "added_sugars": {"value": 10, "dv": 20},
            "protein": 6,
            "vitamin_d": {"value": 0, "dv": 0},
            "calcium": {"value": 40, "dv": 4},
            "iron": {"value": 2, "dv": 10},
            "potassium": {"value": 200, "dv": 4}
        },
        "ingredients": ["Organic Rolled Oats", "Organic Honey", "Organic Almonds", "Organic Coconut Oil", "Organic Raisins"],
        "allergens": ["tree nuts (almonds)"],
        "manufacturer": {
            "name": "Organic Harvest Foods",
            "city": "Seattle",
            "state": "WA",
            "zip": "98101"
        },
        "is_organic": True,
        "organic_level": "95_percent",
        "best_before": "06/30/2026",
        "lot_code": "GR2026014"
    },
    
    "08_frozen_pizza.json": {
        "product_name": "Pepperoni Pizza",
        "category": "frozen_food",
        "net_quantity": {
            "us_value": 20.5,
            "us_unit": "oz",
            "metric_value": 581,
            "metric_unit": "g"
        },
        "nutrition_facts": {
            "serving_size": "1/4 pizza (145g)",
            "servings_per_container": 4,
            "calories": 320,
            "total_fat": {"value": 13, "dv": 17},
            "saturated_fat": {"value": 6, "dv": 30},
            "trans_fat": 0,
            "cholesterol": {"value": 30, "dv": 10},
            "sodium": {"value": 760, "dv": 33},
            "total_carb": {"value": 37, "dv": 13},
            "fiber": {"value": 2, "dv": 7},
            "total_sugars": 5,
            "added_sugars": {"value": 3, "dv": 6},
            "protein": 14,
            "vitamin_d": {"value": 0, "dv": 0},
            "calcium": {"value": 200, "dv": 15},
            "iron": {"value": 2, "dv": 10},
            "potassium": {"value": 250, "dv": 6}
        },
        "ingredients": ["Enriched Flour", "Water", "Mozzarella Cheese", "Pepperoni", "Tomato Paste", "Yeast", "Salt"],
        "allergens": ["wheat", "milk"],
        "manufacturer": {
            "name": "Frozen Foods America Inc",
            "city": "Chicago",
            "state": "IL",
            "zip": "60601"
        },
        "cooking_instructions": "Preheat oven to 425°F. Remove pizza from packaging. Place directly on center oven rack. Bake 12-15 minutes or until cheese is melted and edges are golden brown.",
        "storage_temperature": "Keep frozen",
        "best_before": "12/31/2026",
        "lot_code": "PZ2026014"
    },
    
    "09_fresh_produce.json": {
        "product_name": "Organic Baby Carrots",
        "category": "fresh_produce",
        "net_quantity": {
            "us_value": 1,
            "us_unit": "lb",
            "metric_value": 454,
            "metric_unit": "g"
        },
        "nutrition_facts": {
            "serving_size": "3 oz (85g)",
            "servings_per_container": 5,
            "calories": 35,
            "total_fat": {"value": 0, "dv": 0},
            "saturated_fat": {"value": 0, "dv": 0},
            "trans_fat": 0,
            "cholesterol": {"value": 0, "dv": 0},
            "sodium": {"value": 65, "dv": 3},
            "total_carb": {"value": 8, "dv": 3},
            "fiber": {"value": 2, "dv": 7},
            "total_sugars": 5,
            "added_sugars": {"value": 0, "dv": 0},
            "protein": 1,
            "vitamin_d": {"value": 0, "dv": 0},
            "calcium": {"value": 30, "dv": 2},
            "iron": {"value": 0, "dv": 0},
            "potassium": {"value": 250, "dv": 6}
        },
        "ingredients": ["Organic Baby Carrots"],
        "manufacturer": {
            "name": "Fresh Valley Farms",
            "city": "Salinas",
            "state": "CA",
            "zip": "93901"
        },
        "is_organic": True,
        "organic_level": "100_percent",
        "country_of_origin": "USA",
        "best_before": "02/28/2026",
        "lot_code": "BC2026014",
        "storage_instructions": "Keep refrigerated"
    },
    
    "10_nonalcoholic_juice.json": {
        "product_name": "100% Orange Juice",
        "category": "beverage_nonalcoholic",
        "net_quantity": {
            "us_value": 64,
            "us_unit": "fl oz",
            "metric_value": 1.89,
            "metric_unit": "L"
        },
        "nutrition_facts": {
            "serving_size": "8 fl oz (240ml)",
            "servings_per_container": 8,
            "calories": 110,
            "total_fat": {"value": 0, "dv": 0},
            "saturated_fat": {"value": 0, "dv": 0},
            "trans_fat": 0,
            "cholesterol": {"value": 0, "dv": 0},
            "sodium": {"value": 0, "dv": 0},
            "total_carb": {"value": 26, "dv": 9},
            "fiber": {"value": 0, "dv": 0},
            "total_sugars": 22,
            "added_sugars": {"value": 0, "dv": 0},
            "protein": 2,
            "vitamin_d": {"value": 2.5, "dv": 10},
            "calcium": {"value": 350, "dv": 25},
            "iron": {"value": 0, "dv": 0},
            "potassium": {"value": 450, "dv": 10}
        },
        "ingredients": ["100% Orange Juice", "Calcium Hydroxide", "Vitamin D3"],
        "manufacturer": {
            "name": "Sunshine Juice Company",
            "city": "Orlando",
            "state": "FL",
            "zip": "32801"
        },
        "best_before": "03/15/2026",
        "lot_code": "OJ2026014",
        "storage_instructions": "Keep refrigerated. Shake well before serving"
    }
}

# EU Dataset Samples
eu_samples = {
    "01_packaged_food.json": {
        "product_name": "Organic Hazelnut Energy Bar",
        "category": "packaged_food",
        "net_quantity": {"value": 50, "unit": "g"},
        "nutrition_per_100g": {
            "energy_kj": 2010,
            "energy_kcal": 480,
            "fat": 28,
            "saturates": 5.0,
            "carbohydrate": 44,
            "sugars": 20,
            "protein": 16,
            "salt": 0.28,
            "fibre": 6.0
        },
        "ingredients": [
            {"name": "Organic HAZELNUTS", "percentage": 35, "is_allergen": True},
            {"name": "Organic Dates", "percentage": 25},
            {"name": "Organic Dark Chocolate", "percentage": 15},
            {"name": "Organic OAT Flakes", "percentage": 12, "is_allergen": True},
            {"name": "Organic Agave Syrup", "percentage": 8},
            {"name": "Emulsifier", "e_number": "E322", "functional_class": "Emulsifier"},
            {"name": "Sea Salt"},
            {"name": "Natural Vanilla Extract"}
        ],
        "allergens": ["tree nuts (hazelnuts)", "gluten (oats)"],
        "date_type": "best_before",
        "best_before": "2026-12-31",
        "storage_conditions": "Store in a cool, dry place away from direct sunlight. Once opened, consume within 3 days.",
        "business_operator": {
            "name": "Europa Naturals SAS",
            "address": "45 Rue de la Santé, 75014 Paris, France",
            "phone": "+33 1 45 67 89 00",
            "website": "www.europanaturals.eu"
        },
        "is_organic": True,
        "organic_percentage": 98,
        "organic_certification": "FR-BIO-01",
        "organic_origin": "EU Agriculture",
        "country_of_origin": "France",
        "lot_number": "EU2026014",
        "ean_code": "5 412345 678901"
    },
    
    "02_meat_fresh.json": {
        "product_name": "Fresh Beef Steak",
        "category": "meat_fresh",
        "net_quantity": {"value": 250, "unit": "g"},
        "nutrition_per_100g": {
            "energy_kj": 1050,
            "energy_kcal": 250,
            "fat": 15,
            "saturates": 6.0,
            "carbohydrate": 0,
            "sugars": 0,
            "protein": 26,
            "salt": 0.15
        },
        "ingredients": [
            {"name": "Fresh Beef", "percentage": 100}
        ],
        "date_type": "use_by",
        "use_by": "2026-02-18",
        "storage_conditions": "Keep refrigerated at 0-4°C. Once opened, consume within 24 hours.",
        "business_operator": {
            "name": "French Meat Suppliers SARL",
            "address": "Zone Industrielle, 69100 Lyon, France"
        },
        "country_of_rearing": "France",
        "country_of_slaughter": "France",
        "previously_frozen": False,
        "traceability_code": "FR-69-123-001",
        "lot_number": "BF2026014",
        "ean_code": "5 412345 678902"
    },
    
    "03_fish_seafood.json": {
        "product_name": "Wild Atlantic Salmon Fillet",
        "category": "fish_seafood",
        "net_quantity": {"value": 200, "unit": "g"},
        "nutrition_per_100g": {
            "energy_kj": 880,
            "energy_kcal": 210,
            "fat": 13,
            "saturates": 2.5,
            "carbohydrate": 0,
            "sugars": 0,
            "protein": 23,
            "salt": 0.12
        },
        "ingredients": [
            {"name": "Wild Atlantic Salmon", "percentage": 100}
        ],
        "allergens": ["fish"],
        "date_type": "use_by",
        "use_by": "2026-02-17",
        "storage_conditions": "Keep refrigerated at 0-4°C. Do not refreeze once thawed.",
        "business_operator": {
            "name": "Nordic Seafood AS",
            "address": "Havnegata 12, 5003 Bergen, Norway"
        },
        "wild_or_farmed": "Wild",
        "catch_area": "FAO 27 (Northeast Atlantic)",
        "catch_method": "Trawl nets",
        "country_of_origin": "Norway",
        "lot_number": "SA2026014",
        "ean_code": "5 412345 678903"
    },
    
    "04_dairy_yogurt.json": {
        "product_name": "Greek Style Yogurt",
        "category": "dairy",
        "net_quantity": {"value": 500, "unit": "g"},
        "nutrition_per_100g": {
            "energy_kj": 420,
            "energy_kcal": 100,
            "fat": 4.5,
            "saturates": 3.0,
            "carbohydrate": 5.5,
            "sugars": 5.5,
            "protein": 9.0,
            "salt": 0.15
        },
        "ingredients": [
            {"name": "Pasteurised MILK", "percentage": 95, "is_allergen": True},
            {"name": "MILK Proteins", "percentage": 3, "is_allergen": True},
            {"name": "Yogurt Cultures", "percentage": 2}
        ],
        "allergens": ["milk"],
        "date_type": "best_before",
        "best_before": "2026-03-15",
        "storage_conditions": "Keep refrigerated at 2-6°C",
        "business_operator": {
            "name": "Hellenic Dairy Products SA",
            "address": "Industrial Park, 15125 Athens, Greece"
        },
        "fat_percentage": 4.5,
        "is_pasteurized": True,
        "country_of_origin": "Greece",
        "lot_number": "YG2026014",
        "ean_code": "5 412345 678904"
    },
    
    "05_frozen_food.json": {
        "product_name": "Frozen Mixed Berries",
        "category": "frozen_food",
        "net_quantity": {"value": 300, "unit": "g"},
        "nutrition_per_100g": {
            "energy_kj": 180,
            "energy_kcal": 43,
            "fat": 0.3,
            "saturates": 0,
            "carbohydrate": 8.5,
            "sugars": 8.0,
            "protein": 0.8,
            "salt": 0.01,
            "fibre": 3.5
        },
        "ingredients": [
            {"name": "Strawberries", "percentage": 40},
            {"name": "Blueberries", "percentage": 30},
            {"name": "Raspberries", "percentage": 30}
        ],
        "date_type": "best_before",
        "best_before": "2027-02-14",
        "storage_conditions": "Keep frozen at -18°C or below. Do not refreeze once thawed.",
        "business_operator": {
            "name": "Nordic Frozen Foods AB",
            "address": "Industrivägen 45, 12345 Stockholm, Sweden"
        },
        "frozen_on": "2026-02-14",
        "defrosting_instructions": "Thaw in refrigerator or use directly from frozen in smoothies or cooking.",
        "country_of_origin": "Sweden",
        "lot_number": "FB2026014",
        "ean_code": "5 412345 678905"
    },
    
    "06_organic_bar.json": {
        "product_name": "Organic Fruit & Nut Bar",
        "category": "organic",
        "net_quantity": {"value": 40, "unit": "g"},
        "nutrition_per_100g": {
            "energy_kj": 1680,
            "energy_kcal": 400,
            "fat": 18,
            "saturates": 2.5,
            "carbohydrate": 50,
            "sugars": 35,
            "protein": 8,
            "salt": 0.02,
            "fibre": 7
        },
        "ingredients": [
            {"name": "Organic Dates", "percentage": 45},
            {"name": "Organic ALMONDS", "percentage": 25, "is_allergen": True},
            {"name": "Organic Raisins", "percentage": 20},
            {"name": "Organic Cashews", "percentage": 10, "is_allergen": True}
        ],
        "allergens": ["tree nuts (almonds, cashews)"],
        "date_type": "best_before",
        "best_before": "2026-08-31",
        "storage_conditions": "Store in a cool, dry place",
        "business_operator": {
            "name": "Bio Snacks GmbH",
            "address": "Ökostraße 23, 80331 München, Germany"
        },
        "is_organic": True,
        "organic_percentage": 100,
        "organic_certification": "DE-ÖKO-001",
        "organic_origin": "Non-EU Agriculture",
        "country_of_origin": "Germany",
        "lot_number": "FN2026014",
        "ean_code": "5 412345 678906"
    },
    
    "07_food_supplement.json": {
        "product_name": "Omega-3 Fish Oil Capsules",
        "category": "food_supplement",
        "net_quantity": {"value": 60, "unit": "capsules"},
        "nutrition_per_100g": {
            "energy_kj": 3700,
            "energy_kcal": 900,
            "fat": 100,
            "saturates": 20,
            "carbohydrate": 0,
            "sugars": 0,
            "protein": 0,
            "salt": 0
        },
        "ingredients": [
            {"name": "Fish Oil", "percentage": 95, "is_allergen": True},
            {"name": "Gelatin (Capsule)", "percentage": 4},
            {"name": "Glyc