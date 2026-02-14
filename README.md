# India FSSAI Compliant Food Label Generator

A Python-based system to generate production-ready, FSSAI-compliant food labels for India. This tool ensures all mandatory labeling requirements are met according to Food Safety and Standards Authority of India regulations.

## 🎯 Features

### ✅ All Mandatory FSSAI Requirements Covered

1. **Name of Food** - Clear product identification
2. **Ingredient List** - Descending order by weight with INS numbers for additives
3. **Nutritional Information** - Per 100g/100ml format
4. **Veg/Non-Veg Logo** - Prominent green/brown dot symbol
5. **Net Quantity** - Metric units (g, kg, ml, L)
6. **Manufacturer Details** - Complete name and address
7. **FSSAI License Number** - 14-digit validation
8. **Batch/Lot Number** - Traceability
9. **Date Marking** - MFG date + Best Before/Use By
10. **Allergen Declaration** - Clear allergen warnings
11. **MRP** - Maximum Retail Price including all taxes

### 📦 Category-Specific Compliance

- **Dairy Products**: Fat %, milk source, reconstituted status
- **Beverages**: Caffeine warnings, fruit % content
- **Meat/Fish/Egg**: Use-by dates, storage temperatures
- **Fortified Foods**: +F logo, fortification details
- **Organic Foods**: Jaivik Bharat logo, certification
- **Frozen Foods**: Storage temperature, thawing instructions
- **Imported Foods**: Importer details, country of origin

## 🚀 Quick Start

### Installation

```bash
# Clone or download the repository
cd labellingcss

# Install dependencies
pip install -r requirements.txt
```

### Basic Usage

```bash
# Generate a label from product data
python label_generator.py --input product_data.json --output generated_label.html

# Validate data only (no label generation)
python label_generator.py --input product_data.json --validate-only
```

### Python API Usage

```python
from label_generator import IndiaLabelGenerator

# Load your product data
product_data = {
    "product_name": "Organic Millet Energy Bar",
    "category": "packaged_processed_food",
    "veg_status": "veg",
    # ... more fields
}

# Generate label
generator = IndiaLabelGenerator()
html = generator.generate(product_data, output_path="my_label.html")
```

## 📋 Product Data Format

### Required Fields

```json
{
  "product_name": "Product Name",
  "category": "packaged_processed_food",
  "veg_status": "veg",
  "net_quantity": {
    "value": 50,
    "unit": "g"
  },
  "ingredients": [
    {
      "name": "Ingredient Name",
      "percentage": 30
    }
  ],
  "nutrition_per_100g": {
    "energy_kcal": 450,
    "protein": 12,
    "carbohydrates": 60,
    "fat": 18
  },
  "fssai_license": "10012345678901",
  "manufacturer": {
    "name": "Company Name",
    "address": "Complete Address"
  },
  "batch_number": "BATCH123",
  "mfg_date": "2026-02-14",
  "mrp": 40.00
}
```

### Optional Fields

```json
{
  "allergens": ["tree nuts", "milk"],
  "best_before_months": 6,
  "storage_instructions": "Store in cool, dry place",
  "is_organic": true,
  "is_fortified": false,
  "is_imported": false,
  "customer_care": {
    "phone": "1800-XXX-XXXX",
    "email": "care@example.com",
    "website": "www.example.com"
  }
}
```

## 🏷️ Valid Categories

- `packaged_processed_food` - Snacks, biscuits, noodles
- `dairy` - Milk, cheese, yogurt
- `beverage_carbonated` - Soft drinks, soda
- `beverage_juice` - Fruit juices, drinks
- `meat_fish_egg` - Non-veg products
- `fresh_produce` - Packaged fruits/vegetables
- `fortified` - Fortified foods
- `organic` - Organic certified products
- `frozen` - Frozen foods
- `ready_to_eat` - RTE meals
- `imported` - Imported products

## 🔍 Validation Rules

The generator automatically validates:

- ✅ FSSAI license is exactly 14 digits
- ✅ Veg status is 'veg' or 'non-veg'
- ✅ Category is valid
- ✅ Net quantity has value and unit
- ✅ Required nutrients present
- ✅ Ingredients list not empty
- ✅ Manufacturer has name and address
- ✅ All mandatory fields present

## 📝 Ingredient Formatting

### Basic Ingredient
```json
{
  "name": "Organic Oats"
}
```

### With Percentage
```json
{
  "name": "Organic Oats",
  "percentage": 30
}
```

### Additive with INS Number
```json
{
  "name": "Citric Acid",
  "ins_number": "330",
  "class_name": "Acidity Regulator"
}
```

Output: `Acidity Regulator (Citric Acid (INS 330))`

## 🎨 Customization

### Custom Template

Create your own template and use it:

```bash
python label_generator.py \
  --input product_data.json \
  --output label.html \
  --template custom_template.html
```

### Template Variables

All product data fields are available in the template as Jinja2 variables:

- `{{ product_name }}`
- `{{ veg_status }}`
- `{{ nutrition_per_100g.energy_kcal }}`
- `{{ ingredients_formatted }}`
- `{{ fssai_license_formatted }}`
- And many more...

## 📊 Example Products

### Example 1: Packaged Snack (Organic)

```json
{
  "product_name": "Organic Millet Bar",
  "category": "packaged_processed_food",
  "veg_status": "veg",
  "is_organic": true,
  "net_quantity": {"value": 50, "unit": "g"},
  "mrp": 40.00
}
```

### Example 2: Dairy Product

```json
{
  "product_name": "Full Cream Milk",
  "category": "dairy",
  "veg_status": "veg",
  "fat_percentage": 6.0,
  "milk_source": "Cow",
  "net_quantity": {"value": 500, "unit": "ml"}
}
```

### Example 3: Fortified Food

```json
{
  "product_name": "Fortified Wheat Flour",
  "category": "fortified",
  "is_fortified": true,
  "fortification_details": "Fortified with Iron (28-42.5 ppm), Folic Acid (75-125 mcg/kg), Vitamin B12 (0.75-1.25 mcg/kg)"
}
```

### Example 4: Frozen Food

```json
{
  "product_name": "Frozen Vegetables",
  "category": "frozen",
  "storage_temperature": "-18°C or below",
  "thawing_instructions": "Thaw in refrigerator before use"
}
```

## 🛠️ Advanced Features

### Batch Generation

Generate multiple labels from a CSV or JSON array:

```python
import json
from label_generator import IndiaLabelGenerator

generator = IndiaLabelGenerator()

# Load multiple products
with open('products.json', 'r') as f:
    products = json.load(f)

# Generate labels for each
for i, product in enumerate(products):
    generator.generate(product, f"label_{i+1}.html")
```

### Validation Only

Check if your data is compliant without generating labels:

```bash
python label_generator.py --input product_data.json --validate-only
```

## 📖 FSSAI Compliance Checklist

- [x] Product name clearly stated
- [x] Ingredients in descending order by weight
- [x] Additives with class name and INS number
- [x] Nutrition information per 100g/100ml
- [x] Veg/Non-veg symbol prominent on front
- [x] Net quantity in metric units
- [x] FSSAI license number (14 digits)
- [x] Manufacturer/Packer details with complete address
- [x] Batch/Lot number for traceability
- [x] MFG date and Best Before date
- [x] MRP including all taxes
- [x] Allergen declarations
- [x] Storage instructions
- [x] Customer care information
- [x] Country of origin

## 🔧 Troubleshooting

### Common Errors

**Error: "FSSAI license must be exactly 14 digits"**
- Solution: Ensure license number is 14 digits, no spaces or special characters

**Error: "Missing mandatory field: X"**
- Solution: Add the required field to your JSON data

**Error: "Invalid category"**
- Solution: Use one of the valid categories listed above

**Error: "template not found"**
- Solution: Ensure `label_template.html` is in the same directory as `label_generator.py`

## 📄 File Structure

```
labellingcss/
├── label_generator.py       # Main generator script
├── label_template.html      # Jinja2 template
├── product_data.json        # Sample product data
├── requirements.txt         # Python dependencies
├── README.md               # This file
└── generated_label.html    # Output (after generation)
```

## 🤝 Contributing

To add support for new categories or features:

1. Update `FSSAIValidator.CATEGORIES` in `label_generator.py`
2. Add category-specific logic in `_get_category_specific_data()`
3. Update template with new conditional sections
4. Add example data in README

## 📜 License

This tool is provided as-is for generating FSSAI-compliant labels. Users are responsible for ensuring their labels meet all current FSSAI regulations.

## ⚠️ Disclaimer

While this tool follows FSSAI guidelines, regulations may change. Always verify compliance with current FSSAI standards before using labels in production. Consult with legal/regulatory experts for commercial use.

## 📞 Support

For issues or questions:
- Check the troubleshooting section
- Review example data files
- Ensure all mandatory fields are present
- Validate JSON syntax

## 🔄 Updates

**Version 1.0.0** (February 2026)
- Initial release
- All mandatory FSSAI requirements
- Category-specific compliance
- Validation system
- Template-based generation

---

**Made with ❤️ for Indian Food Industry**