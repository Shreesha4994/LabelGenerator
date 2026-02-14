# US Dataset - FDA/USDA Compliant Samples

This folder contains sample JSON files for US FDA/USDA compliant food labels.

## 📋 Base Sample:

| File | Product | Category | Features |
|------|---------|----------|----------|
| `01_packaged_food.json` | Organic Almond Butter | packaged_food | Dual units, %DV, FALCPA allergens |

## 🚀 Usage:

```bash
# Test the sample
python label_generator_us.py --input us_dataset/01_packaged_food.json --output test.html

# Validate
python label_generator_us.py --input us_dataset/01_packaged_food.json --validate-only
```

## ✅ Sample Includes:

- Dual units (US customary + metric)
- FDA Nutrition Facts with % Daily Value
- FALCPA allergen declaration (9 allergens)
- Manufacturer details (city, state, ZIP)
- USDA Organic certification
- UPC code
- Storage instructions

## 📝 How to Create More Samples:

1. Copy `01_packaged_food.json`
2. Modify for your category:
   - `meat_poultry_egg` - Add USDA establishment number
   - `beverage_alcoholic` - Add ABV, Surgeon General warning
   - `dietary_supplement` - Use supplement_facts instead
   - `infant_formula` - Add preparation instructions
   - `organic` - Specify organic_level (100%, 95%, 70%)

## 🎯 US Categories:

- `packaged_food` - Standard FDA
- `meat_poultry_egg` - USDA regulated
- `dairy` - Milk products
- `beverage_alcoholic` - TTB regulated
- `beverage_nonalcoholic` - Standard beverages
- `dietary_supplement` - DSHEA rules
- `infant_formula` - Highly regulated
- `organic` - USDA Organic
- `frozen_food` - Frozen products
- `fresh_produce` - Packaged produce

---

**Made for FDA/USDA Compliance**