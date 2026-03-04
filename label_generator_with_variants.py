"""
Food-Type-Specific Label Generator
Generates different label styles based on food category without AI
"""

import json
import sys
from jinja2 import Template

def get_food_type_template(category):
    """Get HTML/CSS template based on food type"""
    
    # Base template with food-type-specific styling
    if category in ['packaged_snack', 'biscuit', 'cookie']:
        # Warm, appetizing colors for snacks
        return """
<style>
.front-label-variant {
    width: 420px;
    height: 650px;
    background: linear-gradient(135deg, #ff6b35 0%, #f7931e 50%, #ffd700 100%);
    position: relative;
    overflow: hidden;
}
.front-label-variant::before {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    width: 600px;
    height: 600px;
    background: repeating-conic-gradient(from 0deg, rgba(255,255,255,0.1) 0deg 10deg, transparent 10deg 20deg);
    transform: translate(-50%, -50%);
}
.veg-symbol-v { position: absolute; top: 15px; right: 15px; width: 45px; height: 45px; border: 3px solid {{ veg_color }}; border-radius: 6px; background: white; display: flex; align-items: center; justify-content: center; z-index: 20; box-shadow: 0 4px 12px rgba(0,0,0,0.3); }
.veg-dot-v { width: 22px; height: 22px; background: {{ veg_color }}; border-radius: 50%; }
.premium-badge-v { position: absolute; top: 0; left: 0; background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%); color: #8B4513; padding: 8px 25px 8px 15px; font-size: 13px; font-weight: 900; text-transform: uppercase; letter-spacing: 1px; clip-path: polygon(0 0, 100% 0, 85% 100%, 0% 100%); box-shadow: 0 4px 12px rgba(0,0,0,0.3); z-index: 20; }
.brand-circle-v { position: relative; width: 140px; height: 140px; margin: 50px auto 20px; background: linear-gradient(135deg, #8B4513 0%, #654321 100%); border-radius: 50%; display: flex; align-items: center; justify-content: center; box-shadow: 0 8px 24px rgba(0,0,0,0.4); border: 6px solid white; z-index: 10; }
.brand-text-v { font-size: 42px; font-weight: 900; color: white; font-family: Arial Black, sans-serif; text-shadow: 3px 3px 6px rgba(0,0,0,0.5); }
.product-name-v { text-align: center; font-size: 64px; font-weight: 900; color: white; padding: 20px 30px; text-shadow: 4px 4px 0px rgba(0,0,0,0.3), 6px 6px 12px rgba(0,0,0,0.5); font-family: Arial Black, sans-serif; line-height: 0.9; transform: skewY(-2deg); z-index: 10; position: relative; }
.product-visual-v { width: 200px; height: 200px; margin: 20px auto; background: radial-gradient(circle, rgba(255,255,255,0.3) 0%, transparent 70%); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 120px; z-index: 10; position: relative; }
.benefit-ribbons-v { position: absolute; left: -10px; top: 200px; z-index: 15; }
.benefit-ribbon-v { background: linear-gradient(90deg, #e74c3c 0%, #c0392b 100%); color: white; padding: 8px 20px 8px 15px; margin-bottom: 8px; font-size: 12px; font-weight: 900; text-transform: uppercase; letter-spacing: 0.5px; box-shadow: 0 4px 12px rgba(0,0,0,0.4); clip-path: polygon(0 0, 95% 0, 100% 50%, 95% 100%, 0 100%); }
.bottom-info-v { position: absolute; bottom: 0; left: 0; right: 0; z-index: 10; }
.net-qty-v { background: rgba(255,255,255,0.95); text-align: center; padding: 15px; border-top: 4px solid #8B4513; }
.mrp-v { background: linear-gradient(90deg, #8B4513 0%, #654321 100%); text-align: center; padding: 15px; color: white; }
</style>
<div class="front-label-variant">
    <div class="premium-badge-v">PREMIUM</div>
    <div class="veg-symbol-v"><div class="veg-dot-v"></div></div>
    <div class="brand-circle-v"><div class="brand-text-v">{{ brand }}</div></div>
    <div class="product-name-v">{{ product_name|upper }}</div>
    <div class="product-visual-v">🍪</div>
    <div class="benefit-ribbons-v">
        <div class="benefit-ribbon-v">100% NATURAL</div>
        <div class="benefit-ribbon-v" style="background: linear-gradient(90deg, #3498db 0%, #2980b9 100%);">NO PRESERVATIVES</div>
    </div>
    <div class="bottom-info-v">
        <div class="net-qty-v">
            <div style="font-size: 11px; font-weight: 700; color: #666;">NET QUANTITY</div>
            <div style="font-size: 32px; font-weight: 900; color: #d35400;">{{ net_qty }}</div>
        </div>
        <div class="mrp-v">
            <div style="font-size: 11px; font-weight: 700;">MRP (Incl. of all taxes)</div>
            <div style="font-size: 34px; font-weight: 900;">₹{{ mrp }}</div>
        </div>
    </div>
</div>
"""
    
    elif category in ['beverage', 'juice', 'drink']:
        # Fresh, vibrant colors for beverages
        return """
<style>
.front-label-variant {
    width: 420px;
    height: 650px;
    background: linear-gradient(135deg, #00b4d8 0%, #0077b6 50%, #023e8a 100%);
    position: relative;
    overflow: hidden;
}
.front-label-variant::before {
    content: '';
    position: absolute;
    width: 100%;
    height: 100%;
    background: radial-gradient(circle at 30% 40%, rgba(255,255,255,0.2) 0%, transparent 50%);
}
.veg-symbol-v { position: absolute; top: 15px; right: 15px; width: 45px; height: 45px; border: 3px solid {{ veg_color }}; border-radius: 6px; background: white; display: flex; align-items: center; justify-content: center; z-index: 20; box-shadow: 0 4px 12px rgba(0,0,0,0.3); }
.veg-dot-v { width: 22px; height: 22px; background: {{ veg_color }}; border-radius: 50%; }
.premium-badge-v { position: absolute; top: 0; left: 0; background: linear-gradient(135deg, #90e0ef 0%, #48cae4 100%); color: #023e8a; padding: 8px 25px 8px 15px; font-size: 13px; font-weight: 900; text-transform: uppercase; letter-spacing: 1px; clip-path: polygon(0 0, 100% 0, 85% 100%, 0% 100%); box-shadow: 0 4px 12px rgba(0,0,0,0.3); z-index: 20; }
.brand-circle-v { position: relative; width: 140px; height: 140px; margin: 50px auto 20px; background: linear-gradient(135deg, #0077b6 0%, #023e8a 100%); border-radius: 50%; display: flex; align-items: center; justify-content: center; box-shadow: 0 8px 24px rgba(0,0,0,0.4); border: 6px solid white; z-index: 10; }
.brand-text-v { font-size: 42px; font-weight: 900; color: white; font-family: Arial Black, sans-serif; text-shadow: 3px 3px 6px rgba(0,0,0,0.5); }
.product-name-v { text-align: center; font-size: 64px; font-weight: 900; color: white; padding: 20px 30px; text-shadow: 4px 4px 0px rgba(0,0,0,0.3), 6px 6px 12px rgba(0,0,0,0.5); font-family: Arial Black, sans-serif; line-height: 0.9; z-index: 10; position: relative; }
.product-visual-v { width: 200px; height: 200px; margin: 20px auto; background: radial-gradient(circle, rgba(255,255,255,0.3) 0%, transparent 70%); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 120px; z-index: 10; position: relative; }
.benefit-ribbons-v { position: absolute; left: -10px; top: 200px; z-index: 15; }
.benefit-ribbon-v { background: linear-gradient(90deg, #48cae4 0%, #0096c7 100%); color: white; padding: 8px 20px 8px 15px; margin-bottom: 8px; font-size: 12px; font-weight: 900; text-transform: uppercase; letter-spacing: 0.5px; box-shadow: 0 4px 12px rgba(0,0,0,0.4); clip-path: polygon(0 0, 95% 0, 100% 50%, 95% 100%, 0 100%); }
.bottom-info-v { position: absolute; bottom: 0; left: 0; right: 0; z-index: 10; }
.net-qty-v { background: rgba(255,255,255,0.95); text-align: center; padding: 15px; border-top: 4px solid #0077b6; }
.mrp-v { background: linear-gradient(90deg, #0077b6 0%, #023e8a 100%); text-align: center; padding: 15px; color: white; }
</style>
<div class="front-label-variant">
    <div class="premium-badge-v">FRESH</div>
    <div class="veg-symbol-v"><div class="veg-dot-v"></div></div>
    <div class="brand-circle-v"><div class="brand-text-v">{{ brand }}</div></div>
    <div class="product-name-v">{{ product_name|upper }}</div>
    <div class="product-visual-v">🥤</div>
    <div class="benefit-ribbons-v">
        <div class="benefit-ribbon-v">100% NATURAL</div>
        <div class="benefit-ribbon-v">NO ADDED SUGAR</div>
    </div>
    <div class="bottom-info-v">
        <div class="net-qty-v">
            <div style="font-size: 11px; font-weight: 700; color: #666;">NET QUANTITY</div>
            <div style="font-size: 32px; font-weight: 900; color: #0077b6;">{{ net_qty }}</div>
        </div>
        <div class="mrp-v">
            <div style="font-size: 11px; font-weight: 700;">MRP (Incl. of all taxes)</div>
            <div style="font-size: 34px; font-weight: 900;">₹{{ mrp }}</div>
        </div>
    </div>
</div>
"""
    
    elif category in ['dairy', 'milk', 'yogurt', 'cheese']:
        # Clean, pure colors for dairy
        return """
<style>
.front-label-variant {
    width: 420px;
    height: 650px;
    background: linear-gradient(135deg, #ffffff 0%, #e3f2fd 50%, #bbdefb 100%);
    position: relative;
    overflow: hidden;
}
.veg-symbol-v { position: absolute; top: 15px; right: 15px; width: 45px; height: 45px; border: 3px solid {{ veg_color }}; border-radius: 6px; background: white; display: flex; align-items: center; justify-content: center; z-index: 20; box-shadow: 0 4px 12px rgba(0,0,0,0.2); }
.veg-dot-v { width: 22px; height: 22px; background: {{ veg_color }}; border-radius: 50%; }
.premium-badge-v { position: absolute; top: 0; left: 0; background: linear-gradient(135deg, #2196f3 0%, #1976d2 100%); color: white; padding: 8px 25px 8px 15px; font-size: 13px; font-weight: 900; text-transform: uppercase; letter-spacing: 1px; clip-path: polygon(0 0, 100% 0, 85% 100%, 0% 100%); box-shadow: 0 4px 12px rgba(0,0,0,0.3); z-index: 20; }
.brand-circle-v { position: relative; width: 140px; height: 140px; margin: 50px auto 20px; background: linear-gradient(135deg, #2196f3 0%, #1565c0 100%); border-radius: 50%; display: flex; align-items: center; justify-content: center; box-shadow: 0 8px 24px rgba(0,0,0,0.3); border: 6px solid white; z-index: 10; }
.brand-text-v { font-size: 42px; font-weight: 900; color: white; font-family: Arial Black, sans-serif; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); }
.product-name-v { text-align: center; font-size: 64px; font-weight: 900; color: #1565c0; padding: 20px 30px; text-shadow: 2px 2px 4px rgba(0,0,0,0.1); font-family: Arial Black, sans-serif; line-height: 0.9; z-index: 10; position: relative; }
.product-visual-v { width: 200px; height: 200px; margin: 20px auto; background: radial-gradient(circle, rgba(33,150,243,0.1) 0%, transparent 70%); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 120px; z-index: 10; position: relative; }
.benefit-ribbons-v { position: absolute; left: -10px; top: 200px; z-index: 15; }
.benefit-ribbon-v { background: linear-gradient(90deg, #2196f3 0%, #1976d2 100%); color: white; padding: 8px 20px 8px 15px; margin-bottom: 8px; font-size: 12px; font-weight: 900; text-transform: uppercase; letter-spacing: 0.5px; box-shadow: 0 4px 12px rgba(0,0,0,0.3); clip-path: polygon(0 0, 95% 0, 100% 50%, 95% 100%, 0 100%); }
.bottom-info-v { position: absolute; bottom: 0; left: 0; right: 0; z-index: 10; }
.net-qty-v { background: white; text-align: center; padding: 15px; border-top: 4px solid #2196f3; }
.mrp-v { background: linear-gradient(90deg, #2196f3 0%, #1565c0 100%); text-align: center; padding: 15px; color: white; }
</style>
<div class="front-label-variant">
    <div class="premium-badge-v">PURE</div>
    <div class="veg-symbol-v"><div class="veg-dot-v"></div></div>
    <div class="brand-circle-v"><div class="brand-text-v">{{ brand }}</div></div>
    <div class="product-name-v">{{ product_name|upper }}</div>
    <div class="product-visual-v">🥛</div>
    <div class="benefit-ribbons-v">
        <div class="benefit-ribbon-v">100% PURE</div>
        <div class="benefit-ribbon-v">FRESH DAILY</div>
    </div>
    <div class="bottom-info-v">
        <div class="net-qty-v">
            <div style="font-size: 11px; font-weight: 700; color: #666;">NET QUANTITY</div>
            <div style="font-size: 32px; font-weight: 900; color: #2196f3;">{{ net_qty }}</div>
        </div>
        <div class="mrp-v">
            <div style="font-size: 11px; font-weight: 700;">MRP (Incl. of all taxes)</div>
            <div style="font-size: 34px; font-weight: 900;">₹{{ mrp }}</div>
        </div>
    </div>
</div>
"""
    
    else:
        # Default: warm colors
        return get_food_type_template('packaged_snack')


def generate_label_with_variant(input_file, output_file):
    """Generate label with food-type-specific styling"""
    
    # Load product data
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    # Extract info
    category = data.get('category', 'packaged_snack')
    product_name = data.get('product_name', 'Product')
    brand = data.get('manufacturer', {}).get('name', 'Brand').split()[0][:3].upper()
    veg_status = data.get('veg_status', 'veg')
    veg_color = '#138808' if veg_status == 'veg' else '#8B4513'
    net_qty = f"{data.get('net_quantity', {}).get('value', '')}{data.get('net_quantity', {}).get('unit', '')}"
    mrp = f"{data.get('mrp', 0):.2f}"
    
    # Get template
    template_html = get_food_type_template(category)
    template = Template(template_html)
    
    # Render
    front_html = template.render(
        product_name=product_name,
        brand=brand,
        veg_color=veg_color,
        net_qty=net_qty,
        mrp=mrp
    )
    
    # Read back label template for back
    with open('label_template.html', 'r') as f:
        full_template = f.read()
    
    # Replace front label section
    # For now, just create a simple HTML file
    output_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{product_name} - Food Label</title>
</head>
<body style="display: flex; justify-content: center; align-items: center; min-height: 100vh; background: #f0f0f0; margin: 0; padding: 20px;">
    <div style="background: white; border-radius: 12px; box-shadow: 0 20px 60px rgba(0,0,0,0.3); overflow: hidden;">
        {front_html}
    </div>
</body>
</html>"""
    
    with open(output_file, 'w') as f:
        f.write(output_html)
    
    print(f"✓ Label generated: {output_file}")
    print(f"  Category: {category}")
    print(f"  Product: {product_name}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python label_generator_with_variants.py <input_json> <output_html>")
        sys.exit(1)
    
    generate_label_with_variant(sys.argv[1], sys.argv[2])