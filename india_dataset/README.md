# India Dataset - FSSAI Compliant Samples

This folder contains **11 sample JSON files** covering all FSSAI food categories.

## 📋 Samples Included:

| File | Product | Category | Features |
|------|---------|----------|----------|
| `01_packaged_snack.json` | Chocolate Chip Cookies | packaged_processed_food | INS numbers, allergens |
| `02_dairy_milk.json` | Full Cream Milk | dairy | Fat %, milk source |
| `03_beverage_juice.json` | Mango Fruit Drink | beverage_juice | Fruit %, INS numbers |
| `04_meat_chicken.json` | Fresh Chicken Breast | meat_fish_egg | Non-veg, storage temp |
| `05_fortified_flour.json` | Fortified Wheat Flour | fortified | +F logo, fortification details |
| `06_organic_cookies.json` | Organic Oat Cookies | organic | Organic certification |
| `07_frozen_vegetables.json` | Mixed Frozen Vegetables | frozen | Storage temp, thawing |
| `08_ready_to_eat_meal.json` | Dal Makhani RTE | ready_to_eat | Complete meal |
| `09_imported_chocolate.json` | Swiss Dark Chocolate | imported | Importer details |
| `10_beverage_soda.json` | Lemon Lime Soda | beverage_carbonated | Carbonated drink |
| `11_fresh_produce.json` | Pre-washed Baby Spinach | fresh_produce | Fresh vegetables |

## 🚀 Usage:

```bash
# Test any sample
python label_generator.py --input india_dataset/01_packaged_snack.json --output test.html

# Validate all samples
for file in india_dataset/*.json; do
    python label_generator.py --input "$file" --validate-only
done
```

## ✅ All Samples Include:

- All 11 mandatory FSSAI fields
- Proper veg/non-veg status
- Complete nutrition information (per 100g)
- FSSAI license (14 digits)
- Manufacturer details
- Batch numbers and dates
- MRP including all taxes
- Category-specific requirements

## 📝 How to Use:

1. Find a sample similar to your product
2. Copy the JSON file
3. Modify the values for your product
4. Generate your label!

## 🎯 Category Coverage:

✅ All 11 FSSAI categories covered
✅ Veg and non-veg examples
✅ Fortified and organic products
✅ Imported products
✅ Different units (g, kg, ml)
✅ Various shelf lives

---

**Made for FSSAI Compliance**