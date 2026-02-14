# EU Dataset - Regulation 1169/2011 Compliant Samples

This folder contains sample JSON files for EU compliant food labels.

## 📋 Base Sample:

| File | Product | Category | Features |
|------|---------|----------|----------|
| `01_packaged_food.json` | Organic Hazelnut Bar | packaged_food | kJ+kcal, E-numbers, 14 allergens |

## 🚀 Usage:

```bash
# Test the sample
python label_generator_eu.py --input eu_dataset/01_packaged_food.json --output test.html

# Validate
python label_generator_eu.py --input eu_dataset/01_packaged_food.json --validate-only
```

## ✅ Sample Includes:

- Metric units only (with ℮ mark)
- Nutrition Declaration (kJ + kcal both required)
- 14 EU allergens (bold in ingredient list)
- E-numbers with functional class
- Business operator (EU-based)
- Best before / Use by date
- EU Organic certification
- EAN barcode

## 📝 How to Create More Samples:

1. Copy `01_packaged_food.json`
2. Modify for your category:
   - `meat_fresh` - Add country of rearing/slaughter
   - `fish_seafood` - Add FAO catch area, wild/farmed
   - `dairy` - Add fat %, pasteurization status
   - `frozen_food` - Add frozen date, defrosting instructions
   - `organic` - Add certification code (e.g., FR-BIO-01)
   - `food_supplement` - Add supplement warnings
   - `alcoholic_beverage` - Add ABV, sulphite warning

## 🎯 EU Categories:

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

## 🌍 EU 14 Allergens:

milk, eggs, fish, crustaceans, molluscs, peanuts, tree nuts, soy, gluten, celery, mustard, sesame, lupin, sulphites

---

**Made for EU Regulation 1169/2011 Compliance**