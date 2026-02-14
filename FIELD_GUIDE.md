# 📋 Food Label Generator - Field Guide

**Quick reference for creating your product JSON files**

---

## 🚀 Quick Start

### Minimal Example (India)
```json
{
  "product_name": "Chocolate Cookies",
  "category": "packaged_processed_food",
  "veg_status": "veg",
  "net_quantity": {"value": 100, "unit": "g"},
  "ingredients": ["Wheat flour", "Sugar", "Cocoa powder"],
  "nutrition_per_100g": {
    "energy_kcal": 450,
    "protein": 6,
    "carbohydrates": 65,
    "fat": 18
  },
  "fssai_license": "10012345678901",
  "manufacturer": {
    "name": "ABC Foods Ltd",
    "address": "123 Main St, Mumbai, Maharashtra 400001"
  },
  "batch_number": "BATCH123",
  "mfg_date": "2026-02-14",
  "mrp": 50.00
}
```

---

## 📊 Required Fields by Region

### 🇮🇳 India (FSSAI)

| Field | Type | Example | Notes |
|-------|------|---------|-------|
| ✅ `product_name` | string | `"Chocolate Cookies"` | Product name |
| ✅ `category` | string | `"packaged_processed_food"` | See categories below |
| ✅ `veg_status` | string | `"veg"` or `"non-veg"` | Mandatory symbol |
| ✅ `net_quantity` | object | `{"value": 100, "unit": "g"}` | Metric units |
| ✅ `ingredients` | array | `["Flour", "Sugar"]` | Descending order |
| ✅ `nutrition_per_100g` | object | See nutrition table | Per 100g/100ml |
| ✅ `fssai_license` | string | `"10012345678901"` | Exactly 14 digits |
| ✅ `manufacturer` | object | `{"name": "...", "address": "..."}` | Complete details |
| ✅ `batch_number` | string | `"BATCH123"` | Traceability |
| ✅ `mfg_date` | string | `"2026-02-14"` | YYYY-MM-DD format |
| ✅ `mrp` | number | `50.00` | Including all taxes |

### 🇺🇸 USA (FDA/USDA)

| Field | Type | Example | Notes |
|-------|------|---------|-------|
| ✅ `product_name` | string | `"Almond Butter"` | Statement of identity |
| ✅ `category` | string | `"packaged_food"` | See categories below |
| ✅ `net_quantity` | object | `{"us_value": 16, "us_unit": "oz", "metric_value": 454, "metric_unit": "g"}` | Dual units required |
| ✅ `ingredients` | array | `["Almonds", "Salt"]` | Descending by weight |
| ✅ `nutrition_facts` | object | See nutrition table | FDA format with %DV |
| ✅ `manufacturer` | object | `{"name": "...", "city": "Portland", "state": "OR", "zip": "97201"}` | City, state, ZIP |

### 🇪🇺 EU (Regulation 1169/2011)

| Field | Type | Example | Notes |
|-------|------|---------|-------|
| ✅ `product_name` | string | `"Hazelnut Bar"` | Name of food |
| ✅ `category` | string | `"packaged_food"` | See categories below |
| ✅ `net_quantity` | object | `{"value": 50, "unit": "g"}` | Metric only with ℮ |
| ✅ `ingredients` | array | See ingredient format | With E-numbers |
| ✅ `nutrition_per_100g` | object | See nutrition table | kJ + kcal required |
| ✅ `date_type` | string | `"best_before"` or `"use_by"` | Date marking type |
| ✅ `storage_conditions` | string | `"Store in cool, dry place"` | If required |
| ✅ `business_operator` | object | `{"name": "...", "address": "..."}` | EU-based contact |

---

## 🔧 Optional Fields (All Regions)

| Field | Type | Example | Purpose |
|-------|------|---------|---------|
| `allergens` | array | `["tree nuts", "milk"]` | Allergen declarations |
| `best_before_months` | number | `6` | Auto-calculate expiry |
| `storage_instructions` | string | `"Refrigerate after opening"` | Storage guidance |
| `customer_care` | object | `{"phone": "1800-XXX", "email": "..."}` | Contact info |
| `is_organic` | boolean | `true` | Organic certification |
| `is_fortified` | boolean | `true` | Fortified foods |
| `is_imported` | boolean | `true` | Imported products |

---

## 📖 Complete Field Reference

### Product Information

```json
{
  "product_name": "Organic Millet Bar",           // ✅ Required (all)
  "product_description": "Energy bar",            // 🔧 Optional
  "product_variant": "Chocolate flavor",          // 🔧 Optional
  "brand_name": "HEALTHY BITES"                   // 🔧 Optional
}
```

### Category

**India Categories:**
- `packaged_processed_food` - Snacks, biscuits, noodles
- `dairy` - Milk, cheese, yogurt
- `beverage_carbonated` - Soft drinks
- `beverage_juice` - Fruit juices
- `meat_fish_egg` - Non-veg products
- `fresh_produce` - Packaged fruits/vegetables
- `fortified` - Fortified foods
- `organic` - Organic certified
- `frozen` - Frozen foods
- `ready_to_eat` - RTE meals
- `imported` - Imported products

**US Categories:**
- `packaged_food` - Standard FDA foods
- `meat_poultry_egg` - USDA regulated
- `dairy` - Milk products
- `beverage_alcoholic` - TTB regulated
- `beverage_nonalcoholic` - Standard beverages
- `dietary_supplement` - DSHEA rules
- `infant_formula` - Highly regulated
- `organic` - USDA Organic
- `frozen_food` - Frozen products
- `fresh_produce` - Packaged produce

**EU Categories:**
- `packaged_food` - Standard EU food
- `meat_fresh` - Fresh meat with traceability
- `fish_seafood` - With catch area
- `dairy` - With fat % and pasteurization
- `frozen_food` - With frozen date
- `organic` - EU Organic logo
- `food_supplement` - With warnings
- `alcoholic_beverage` - With ABV
- `fresh_produce` - With origin
- `infant_food` - Strict rules

### Net Quantity

**India (metric only):**
```json
{
  "net_quantity": {
    "value": 100,
    "unit": "g"        // g, kg, ml, L
  }
}
```

**US (dual units):**
```json
{
  "net_quantity": {
    "us_value": 16,
    "us_unit": "oz",
    "metric_value": 454,
    "metric_unit": "g"
  }
}
```

**EU (metric only):**
```json
{
  "net_quantity": {
    "value": 50,
    "unit": "g"        // g, kg, ml, L
  }
}
```

### Ingredients

**Simple format:**
```json
{
  "ingredients": ["Wheat flour", "Sugar", "Palm oil"]
}
```

**With percentages:**
```json
{
  "ingredients": [
    {"name": "Organic Oats", "percentage": 30},
    {"name": "Honey", "percentage": 15}
  ]
}
```

**With additives (India - INS numbers):**
```json
{
  "ingredients": [
    {"name": "Wheat flour"},
    {
      "name": "Citric Acid",
      "ins_number": "330",
      "class_name": "Acidity Regulator"
    }
  ]
}
```

**With additives (EU - E-numbers):**
```json
{
  "ingredients": [
    {"name": "Organic HAZELNUTS", "is_allergen": true},
    {
      "name": "Emulsifier",
      "e_number": "E322",
      "functional_class": "Emulsifier"
    }
  ]
}
```

### Nutrition Information

**India (per 100g/100ml):**
```json
{
  "nutrition_per_100g": {
    "energy_kcal": 450,      // ✅ Required
    "protein": 12,           // ✅ Required
    "carbohydrates": 60,     // ✅ Required
    "fat": 18,               // ✅ Required
    "saturated_fat": 8,      // 🔧 Optional
    "trans_fat": 0,          // 🔧 Optional
    "sugar": 20,             // 🔧 Optional
    "sodium": 0.5,           // 🔧 Optional
    "fiber": 3               // 🔧 Optional
  }
}
```

**US (FDA format with %DV):**
```json
{
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
  }
}
```

**EU (per 100g/100ml with kJ + kcal):**
```json
{
  "nutrition_per_100g": {
    "energy_kj": 2010,       // ✅ Required
    "energy_kcal": 480,      // ✅ Required
    "fat": 28,               // ✅ Required
    "saturates": 5.0,        // ✅ Required
    "carbohydrate": 44,      // ✅ Required
    "sugars": 20,            // ✅ Required
    "protein": 16,           // ✅ Required
    "salt": 0.28,            // ✅ Required
    "fibre": 6.0             // 🔧 Optional
  }
}
```

### Allergens

**India:**
```json
{
  "allergens": ["tree nuts", "milk", "soy"]
}
```

**US (FALCPA - 9 allergens):**
```json
{
  "allergens": ["tree nuts (almonds)", "soy"]
}
```
Major allergens: milk, eggs, fish, shellfish, tree nuts, peanuts, wheat, soy, sesame

**EU (14 allergens):**
```json
{
  "allergens": ["tree nuts (hazelnuts)", "gluten (oats)"]
}
```
Major allergens: milk, eggs, fish, crustaceans, molluscs, peanuts, tree nuts, soy, gluten, celery, mustard, sesame, lupin, sulphites

### Manufacturer/Business Operator

**India:**
```json
{
  "manufacturer": {
    "name": "ABC Foods Ltd",
    "address": "123 Main Street, Mumbai, Maharashtra 400001, India"
  }
}
```

**US:**
```json
{
  "manufacturer": {
    "name": "American Harvest Foods LLC",
    "city": "Portland",
    "state": "OR",
    "zip": "97201",
    "phone": "1-800-555-FOOD",
    "website": "www.example.com"
  }
}
```

**EU:**
```json
{
  "business_operator": {
    "name": "Europa Naturals SAS",
    "address": "45 Rue de la Santé, 75014 Paris, France",
    "phone": "+33 1 45 67 89 00",
    "website": "www.example.eu"
  }
}
```

### Dates

**India:**
```json
{
  "mfg_date": "2026-02-14",           // ✅ Required (YYYY-MM-DD)
  "best_before_months": 6,            // 🔧 Optional (auto-calculates)
  "best_before_days": 180             // 🔧 Alternative to months
}
```

**US:**
```json
{
  "best_before": "12/31/2026",        // 🔧 Optional
  "lot_code": "2026US014"             // 🔧 Optional
}
```

**EU:**
```json
{
  "date_type": "best_before",         // ✅ Required ("best_before" or "use_by")
  "best_before": "2026-12-31",        // ✅ Required if date_type is "best_before"
  "use_by": "2026-03-15"              // ✅ Required if date_type is "use_by"
}
```

---

## 🎯 Category-Specific Fields

### Dairy Products

**India:**
```json
{
  "category": "dairy",
  "fat_percentage": 3.5,
  "milk_source": "Cow",
  "is_reconstituted": false
}
```

**US:**
```json
{
  "category": "dairy",
  "milk_fat_percentage": 3.5
}
```

**EU:**
```json
{
  "category": "dairy",
  "fat_percentage": 3.5,
  "is_pasteurized": true
}
```

### Meat/Poultry/Fish

**India:**
```json
{
  "category": "meat_fish_egg",
  "storage_temperature": "Store below 4°C"
}
```

**US:**
```json
{
  "category": "meat_poultry_egg",
  "usda_establishment_number": "1234",
  "safe_handling_instructions": "Keep refrigerated..."
}
```

**EU:**
```json
{
  "category": "meat_fresh",
  "country_of_rearing": "France",
  "country_of_slaughter": "France",
  "previously_frozen": false
}
```

### Fish/Seafood (EU only)

```json
{
  "category": "fish_seafood",
  "wild_or_farmed": "Wild",
  "catch_area": "FAO 27 (Northeast Atlantic)",
  "catch_method": "Trawl nets"
}
```

### Organic Products

**India:**
```json
{
  "is_organic": true,
  "organic_certification": "India Organic (NPOP)"
}
```

**US:**
```json
{
  "is_organic": true,
  "organic_level": "100_percent"    // "100_percent", "95_percent", "70_percent"
}
```

**EU:**
```json
{
  "is_organic": true,
  "organic_percentage": 98,
  "organic_certification": "FR-BIO-01",
  "organic_origin": "EU Agriculture"
}
```

### Fortified Foods (India)

```json
{
  "is_fortified": true,
  "fortification_details": "Fortified with Iron (28-42.5 ppm), Folic Acid (75-125 mcg/kg)"
}
```

### Alcoholic Beverages (US/EU)

**US:**
```json
{
  "category": "beverage_alcoholic",
  "abv": 5.0,
  "contains_sulfites": true
}
```

**EU:**
```json
{
  "category": "alcoholic_beverage",
  "abv": 12.5,
  "contains_sulphites": true
}
```

### Dietary Supplements (US)

```json
{
  "category": "dietary_supplement",
  "supplement_facts": {
    "serving_size": "2 capsules",
    "servings_per_container": 30,
    "vitamin_c": {"amount": "500mg", "dv": "556%"}
  }
}
```

---

## ⚠️ Common Mistakes

### ❌ Wrong: FSSAI License Format
```json
{
  "fssai_license": "1001234567890"    // Only 13 digits!
}
```
✅ **Correct:** Must be exactly 14 digits
```json
{
  "fssai_license": "10012345678901"
}
```

### ❌ Wrong: Veg Status
```json
{
  "veg_status": "vegetarian"          // Invalid value
}
```
✅ **Correct:** Must be "veg" or "non-veg"
```json
{
  "veg_status": "veg"
}
```

### ❌ Wrong: Net Quantity (India/EU)
```json
{
  "net_quantity": "100g"              // String instead of object
}
```
✅ **Correct:**
```json
{
  "net_quantity": {"value": 100, "unit": "g"}
}
```

### ❌ Wrong: Empty Ingredients
```json
{
  "ingredients": []                   // Empty array
}
```
✅ **Correct:** Must have at least one ingredient
```json
{
  "ingredients": ["Wheat flour", "Sugar"]
}
```

### ❌ Wrong: Missing Nutrition Fields
```json
{
  "nutrition_per_100g": {
    "energy_kcal": 450,
    "protein": 12
    // Missing carbohydrates and fat!
  }
}
```
✅ **Correct:** Include all required nutrients
```json
{
  "nutrition_per_100g": {
    "energy_kcal": 450,
    "protein": 12,
    "carbohydrates": 60,
    "fat": 18
  }
}
```

### ❌ Wrong: Date Format
```json
{
  "mfg_date": "14/02/2026"            // Wrong format
}
```
✅ **Correct:** Use YYYY-MM-DD
```json
{
  "mfg_date": "2026-02-14"
}
```

---

## 🎓 Usage Examples

### Generate Label
```bash
# India
python label_generator.py --input product_data.json --output label.html

# US
python label_generator_us.py --input product_data_us.json --output label_us.html

# EU
python label_generator_eu.py --input product_data_eu.json --output label_eu.html
```

### Validate Only
```bash
python label_generator.py --input product_data.json --validate-only
```

---

## 📞 Need Help?

- Check the full README.md for detailed documentation
- Look at sample files: `product_data.json`, `product_data_us.json`, `product_data_eu.json`
- Run with `--validate-only` to check your data before generating

---

**Made with ❤️ for Food Industry Compliance**