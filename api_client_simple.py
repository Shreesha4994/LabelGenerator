#!/usr/bin/env python3
"""
Simple API Client for Food Label Generator
Makes requests to the deployed SAP BTP API with embedded JSON data
"""

import requests
import json
import os

# API Base URL
API_URL = "https://label-generator-api.cfapps.eu11.hana.ondemand.com"

# Load sample data from files
def load_sample_data():
    """Load sample product data from JSON files"""
    with open('india_dataset/01_packaged_snack.json', 'r') as f:
        india_data = json.load(f)
    
    with open('us_dataset/01_packaged_food.json', 'r') as f:
        us_data = json.load(f)
    
    with open('eu_dataset/01_packaged_food.json', 'r') as f:
        eu_data = json.load(f)
    
    return india_data, us_data, eu_data

# Sample product data for India (FSSAI) - Embedded version
INDIA_PRODUCT_EMBEDDED = {
    "product_name": "Chocolate Chip Cookies",
    "category": "packaged_processed_food",
    "veg_status": "veg",
    "brand_owner": "Delicious Snacks Pvt Ltd",
    "manufacturer_name": "Delicious Snacks Pvt Ltd",
    "manufacturer_address": "Plot 123, Food Park, Mumbai, Maharashtra 400001",
    "fssai_license": "12345678901234",
    "net_quantity": "200g",
    "ingredients": [
        "Wheat Flour (Maida)",
        "Sugar",
        "Chocolate Chips (15%)",
        "Vegetable Oil (Palm Oil)",
        "Milk Solids",
        "Raising Agents (E500, E503)",
        "Emulsifier (E322)",
        "Salt",
        "Natural Vanilla Flavour"
    ],
    "allergens": ["Contains Wheat", "Contains Milk", "May contain traces of Nuts"],
    "nutritional_info": {
        "serving_size": "30g (2 cookies)",
        "servings_per_package": "6-7",
        "energy_kcal": 150,
        "energy_kj": 628,
        "protein_g": 2.1,
        "carbohydrates_g": 19.5,
        "total_sugars_g": 8.2,
        "added_sugars_g": 7.5,
        "total_fat_g": 7.2,
        "saturated_fat_g": 3.8,
        "trans_fat_g": 0.1,
        "cholesterol_mg": 5,
        "sodium_mg": 95
    },
    "best_before": "6 months from date of manufacture",
    "storage_instructions": "Store in a cool, dry place away from direct sunlight",
    "customer_care": "1800-123-4567 | care@delicioussnacks.com"
}

# Sample product data for US (FDA)
US_PRODUCT = {
    "product_name": "Organic Almond Butter",
    "brand": "Nature's Best",
    "category": "packaged_food",
    "manufacturer": "Nature's Best Foods Inc.",
    "manufacturer_address": "123 Organic Way, Portland, OR 97201",
    "distributor": "Healthy Foods Distribution LLC",
    "net_weight": "16 oz (454g)",
    "ingredients": [
        "Organic Dry Roasted Almonds",
        "Sea Salt"
    ],
    "allergens": {
        "contains": ["Tree Nuts (Almonds)"],
        "may_contain": ["Peanuts", "Other Tree Nuts"]
    },
    "nutrition_facts": {
        "serving_size": "2 tbsp (32g)",
        "servings_per_container": "14",
        "calories": 190,
        "total_fat_g": 17,
        "saturated_fat_g": 1.5,
        "trans_fat_g": 0,
        "cholesterol_mg": 0,
        "sodium_mg": 75,
        "total_carbohydrate_g": 6,
        "dietary_fiber_g": 3,
        "total_sugars_g": 2,
        "added_sugars_g": 0,
        "protein_g": 7,
        "vitamin_d_mcg": 0,
        "calcium_mg": 80,
        "iron_mg": 1.2,
        "potassium_mg": 220
    },
    "daily_values_note": "The % Daily Value tells you how much a nutrient in a serving of food contributes to a daily diet. 2,000 calories a day is used for general nutrition advice.",
    "storage": "Refrigerate after opening. Stir before use as natural separation may occur.",
    "best_by": "See date on lid",
    "certifications": ["USDA Organic", "Non-GMO Project Verified"],
    "contact": "www.naturesbest.com | 1-800-555-0123"
}

# Sample product data for EU (Regulation 1169/2011)
EU_PRODUCT = {
    "product_name": "Organic Hazelnut Energy Bar",
    "brand": "EcoSnack",
    "category": "packaged_food",
    "food_business_operator": "EcoSnack GmbH, Hauptstraße 45, 10115 Berlin, Germany",
    "country_of_origin": "Germany",
    "net_quantity": "45g",
    "ingredients": [
        "Dates* (40%)",
        "Hazelnuts* (25%)",
        "Almonds* (15%)",
        "Cocoa powder* (8%)",
        "Coconut oil*",
        "Sea salt",
        "Natural vanilla extract*"
    ],
    "ingredients_note": "*From organic farming",
    "allergens": {
        "contains": ["Nuts (hazelnuts, almonds)"],
        "may_contain": ["Other nuts", "Sesame"]
    },
    "nutrition_declaration": {
        "per_100g": {
            "energy_kj": 1850,
            "energy_kcal": 442,
            "fat_g": 24.5,
            "saturates_g": 4.2,
            "carbohydrate_g": 42.0,
            "sugars_g": 35.0,
            "protein_g": 8.5,
            "salt_g": 0.15
        },
        "per_serving": {
            "serving_size": "45g (1 bar)",
            "energy_kj": 833,
            "energy_kcal": 199,
            "fat_g": 11.0,
            "saturates_g": 1.9,
            "carbohydrate_g": 18.9,
            "sugars_g": 15.8,
            "protein_g": 3.8,
            "salt_g": 0.07
        }
    },
    "storage_conditions": "Store in a cool, dry place. Once opened, consume within 3 days.",
    "best_before": "See date on package",
    "lot_number": "L2024-001",
    "certifications": ["EU Organic", "Vegan Society"],
    "recycling_info": "Wrapper: Recyclable plastic #4 (LDPE)",
    "contact": "info@ecosnack.de | www.ecosnack.de"
}


def test_health():
    """Test the health check endpoint"""
    print("\n" + "="*60)
    print("Testing Health Check Endpoint")
    print("="*60)
    
    try:
        response = requests.get(f"{API_URL}/api/health")
        response.raise_for_status()
        
        data = response.json()
        print(f"✓ Status: {data['status']}")
        print(f"✓ Service: {data['service']}")
        print(f"✓ Version: {data['version']}")
        print(f"✓ Regions: {', '.join(data['regions'])}")
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def generate_label(region, product_data):
    """Generate a food label for the specified region"""
    print("\n" + "="*60)
    print(f"Generating {region.upper()} Label")
    print("="*60)
    
    endpoint = f"{API_URL}/api/generate/{region}"
    
    try:
        # Make API request
        print(f"→ Sending request to: {endpoint}")
        print(f"→ Product: {product_data['product_name']}")
        
        response = requests.post(
            endpoint,
            json=product_data,
            headers={"Content-Type": "application/json"}
        )
        
        # Parse response (even if error)
        data = response.json()
        
        # Check for errors before raising
        if response.status_code != 200:
            print(f"✗ HTTP {response.status_code}: {data.get('error', 'Unknown error')}")
            if 'errors' in data:
                print("Validation errors:")
                for error in data['errors']:
                    print(f"  - {error}")
            return False
        
        if data.get('success'):
            print(f"✓ Success!")
            print(f"✓ Product: {data['product_name']}")
            print(f"✓ Region: {data['region']}")
            print(f"✓ HTML Length: {len(data['html'])} characters")
            
            # Save HTML to file
            filename = f"label_{region}_{product_data['product_name'].replace(' ', '_').lower()}.html"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(data['html'])
            print(f"✓ Saved to: {filename}")
            
            return True
        else:
            print(f"✗ Failed: {data.get('error', 'Unknown error')}")
            if 'errors' in data:
                print("Validation errors:")
                for error in data['errors']:
                    print(f"  - {error}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"✗ Request Error: {e}")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def main():
    """Main function to run all tests"""
    print("\n" + "="*60)
    print("Food Label Generator API Client")
    print("SAP BTP Deployment")
    print("="*60)
    print(f"API URL: {API_URL}")
    
    # Test health check
    if not test_health():
        print("\n✗ Health check failed. Exiting.")
        return
    
    # Load sample data from files
    try:
        india_data, us_data, eu_data = load_sample_data()
        print("\n✓ Loaded sample data from files")
    except Exception as e:
        print(f"\n✗ Error loading sample data: {e}")
        return
    
    # Generate labels for all regions
    results = []
    
    # India label
    results.append(("India", generate_label("india", india_data)))
    
    # US label
    results.append(("US", generate_label("us", us_data)))
    
    # EU label
    results.append(("EU", generate_label("eu", eu_data)))
    
    # Summary
    print("\n" + "="*60)
    print("Summary")
    print("="*60)
    
    for region, success in results:
        status = "✓ Success" if success else "✗ Failed"
        print(f"{region:10} {status}")
    
    total = len(results)
    passed = sum(1 for _, success in results if success)
    
    print(f"\nTotal: {passed}/{total} labels generated successfully")
    
    if passed == total:
        print("\n✓ All labels generated successfully!")
        print("\nGenerated files:")
        print("  - label_india_chocolate_chip_cookies.html")
        print("  - label_us_organic_almond_butter.html")
        print("  - label_eu_organic_hazelnut_energy_bar.html")
    else:
        print(f"\n✗ {total - passed} label(s) failed to generate")


if __name__ == "__main__":
    main()