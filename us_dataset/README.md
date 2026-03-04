# US Dataset - FDA/USDA Compliant Samples

This folder contains sample JSON files for US FDA/USDA compliant food labels covering all major regulatory categories.

## 📋 Sample Files

| File | Product | Category | Key Features |
|------|---------|----------|--------------|
| `01_packaged_food.json` | Organic Almond Butter | packaged_food | Dual units, %DV, FALCPA allergens, USDA Organic |
| `02_meat_poultry.json` | Premium Ground Beef | meat_poultry_egg | USDA inspection mark, safe handling instructions, establishment number |
| `03_dietary_supplement.json` | Vitamin D3 + K2 | dietary_supplement | Supplement Facts panel, FDA disclaimer |
| `04_infant_formula.json` | Infant Formula Powder | infant_formula | Full nutrient panel, preparation instructions, physician statement |
| `05_bioengineered.json` | Corn Tortilla Chips | packaged_food | Bioengineered (BE) food disclosure |
| `06_organic_certified.json` | Organic Olive Oil | packaged_food | USDA Organic seal, certifying agent, nutrition/health claims |

## 🚀 Usage

```bash
# Generate a label
python label_generator_us.py --input us_dataset/01_packaged_food.json --output test.html

# Validate only
python label_generator_us.py --input us_dataset/02_meat_poultry.json --validate-only

# Check valid nutrition claims
python label_generator_us.py --input us_dataset/06_organic_certified.json --check-claims
```

## ✅ FDA/USDA Requirements Implemented

### Core FDA Requirements (All Products)
- ✅ Statement of Identity (product name)
- ✅ Net Quantity (dual units: US customary + metric)
- ✅ Nutrition Facts Panel (2020 format)
- ✅ Ingredient List (descending order by weight)
- ✅ FALCPA Allergen Declaration (9 major allergens including sesame)
- ✅ Manufacturer/Distributor Information
- ✅ Country of Origin (for imported products)

### USDA Meat/Poultry/Egg Products
- ✅ USDA Inspection Legend
- ✅ Establishment Number (EST.)
- ✅ Safe Handling Instructions
- ✅ Storage Temperature Requirements

### USDA Organic Products
- ✅ USDA Organic Seal (100%, 95%, 70% levels)
- ✅ Certifying Agent Information
- ✅ Organic Percentage Validation

### Dietary Supplements (DSHEA)
- ✅ Supplement Facts Panel (different from Nutrition Facts)
- ✅ FDA Disclaimer Statement
- ✅ Suggested Use
- ✅ Other Ingredients Section

### Infant Formula (21 CFR 107)
- ✅ Complete Nutrient Panel (29+ nutrients)
- ✅ Preparation Instructions
- ✅ Use-By Date
- ✅ Storage After Opening Instructions
- ✅ "Use as directed by physician" Statement

### Bioengineered Food Disclosure (NBFDS)
- ✅ "Bioengineered Food" disclosure
- ✅ "Derived from Bioengineering" option
- ✅ "Contains Bioengineered Food Ingredients" option

### Nutrition Claims Validation
- ✅ Fat claims: Fat Free, Low Fat, Reduced Fat
- ✅ Sodium claims: Sodium Free, Low Sodium, Very Low Sodium
- ✅ Calorie claims: Calorie Free, Low Calorie
- ✅ Sugar claims: Sugar Free, No Added Sugars
- ✅ Fiber claims: High Fiber, Good Source of Fiber
- ✅ Protein claims: High Protein, Good Source of Protein

### Health Claims (FDA-Authorized)
- ✅ Calcium & Osteoporosis
- ✅ Sodium & Hypertension
- ✅ Fat & Cancer
- ✅ Fiber & Cancer
- ✅ Fiber & Heart Disease
- ✅ Potassium & Blood Pressure

### Font Size Requirements (21 CFR 101.7)
- ✅ PDP Area Calculation
- ✅ Minimum Font Size Validation

## 📝 Category-Specific Fields

### Meat/Poultry/Egg (`meat_poultry_egg`)
```json
{
  "category": "meat_poultry_egg",
  "usda_establishment_number": "12345",
  "safe_handling_instructions": "Keep refrigerated...",
  "storage_temperature": "Keep Refrigerated at 40°F or below"
}
```

### Dietary Supplement (`dietary_supplement`)
```json
{
  "category": "dietary_supplement",
  "supplement_facts": {
    "serving_size": "1 Softgel",
    "servings_per_container": 60,
    "ingredients": [
      {"name": "Vitamin D3", "amount": "125 mcg", "dv": 625}
    ],
    "other_ingredients": ["Olive Oil", "Gelatin Capsule"]
  },
  "fda_disclaimer": true
}
```

### Infant Formula (`infant_formula`)
```json
{
  "category": "infant_formula",
  "preparation_instructions": "1. Wash hands...",
  "use_by_date": "See bottom of can",
  "storage_instructions_opened": "Use within 1 month...",
  "physician_statement": true,
  "nutrition_facts": {
    "vitamin_a": "300 IU",
    "vitamin_d": "60 IU",
    "calcium": "78 mg",
    "iron": "1.8 mg"
    // ... 29+ required nutrients
  }
}
```

### Organic Products
```json
{
  "is_organic": true,
  "organic_level": "100_percent",  // or "95_percent", "70_percent"
  "organic_certifier": {
    "name": "California Certified Organic Farmers (CCOF)",
    "code": "CCOF"
  }
}
```

### Bioengineered Products
```json
{
  "is_bioengineered": true,
  "be_disclosure_type": "contains_bioengineered_ingredients"
  // Options: "bioengineered", "derived_from_bioengineering", "contains_bioengineered_ingredients"
}
```

### Nutrition Claims
```json
{
  "nutrition_claims": ["cholesterol_free", "sodium_free", "low_fat"]
}
```

### Health Claims
```json
{
  "health_claims": ["calcium_osteoporosis", "sodium_hypertension"]
}
```

## 🎯 US Categories

| Category | Regulator | Key Requirements |
|----------|-----------|------------------|
| `packaged_food` | FDA | Standard Nutrition Facts |
| `meat_poultry_egg` | USDA | Inspection mark, safe handling |
| `dairy` | FDA | Fat %, pasteurization |
| `beverage_alcoholic` | TTB | ABV, Surgeon General warning |
| `beverage_nonalcoholic` | FDA | Standard labeling |
| `dietary_supplement` | FDA (DSHEA) | Supplement Facts, disclaimer |
| `infant_formula` | FDA (21 CFR 107) | 29+ nutrients, preparation |
| `organic` | USDA | Organic seal, certifier |
| `frozen_food` | FDA | Cooking instructions |
| `fresh_produce` | FDA | Country of origin |

## 🔍 Validation

The validator checks:
- ✅ All mandatory fields present
- ✅ Net quantity has US and metric units
- ✅ Nutrition Facts has all required nutrients
- ✅ USDA establishment number format (1-5 digits)
- ✅ Organic certifier for 95%+ organic products
- ✅ BE disclosure type for bioengineered products
- ✅ Nutrition claims meet FDA criteria
- ✅ Health claims are FDA-authorized
- ✅ Infant formula has all 29+ required nutrients

## 📞 Regulatory References

- **FDA Food Labeling Guide**: https://www.fda.gov/food/food-labeling-nutrition
- **USDA Meat & Poultry Labeling**: https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics/labeling
- **USDA Organic**: https://www.usda.gov/topics/organic
- **Bioengineered Food Disclosure**: https://www.ams.usda.gov/rules-regulations/be
- **DSHEA (Supplements)**: https://www.fda.gov/food/dietary-supplements

---

**Made for FDA/USDA Compliance**