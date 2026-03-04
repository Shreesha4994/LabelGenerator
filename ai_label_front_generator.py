"""
AI-Powered Front Label Generator
Supports India (FSSAI), USA (FDA), and EU with country + category-specific styling
"""

import os
import json
from dotenv import load_dotenv
from gen_ai_hub.proxy.native.openai import OpenAI
from gen_ai_hub.proxy.core.proxy_clients import get_proxy_client

load_dotenv()


class AIFrontLabelGenerator:
    """Generate AI-powered front labels for different countries and food categories"""
    
    def __init__(self, country='india'):
        """
        Initialize AI label generator
        
        Args:
            country: 'india', 'us', or 'eu'
        """
        self.country = country.lower()
        self.proxy_client = get_proxy_client('gen-ai-hub')
        self.client = OpenAI(proxy_client=self.proxy_client)
        self.deployment_id = os.getenv('SAP_AI_CORE_DEPLOYMENT_ID')
        
        # Country-specific configurations
        self.country_config = {
            'india': {
                'style': 'Bold, vibrant Indian FMCG style',
                'currency': '₹',
                'special_elements': 'Veg/Non-veg symbol prominent',
                'typography': 'Large, bold, uppercase',
                'aesthetic': 'Colorful, energetic, traditional Indian packaging'
            },
            'us': {
                'style': 'Clean, modern American packaging',
                'currency': '$',
                'special_elements': 'Nutrition Facts emphasis, FDA compliant',
                'typography': 'Clear, readable, professional',
                'aesthetic': 'Minimalist, trustworthy, health-focused'
            },
            'eu': {
                'style': 'Elegant, minimalist European design',
                'currency': '€',
                'special_elements': 'E-number compliance, sustainability focus',
                'typography': 'Refined, sophisticated, clean',
                'aesthetic': 'Premium, understated, eco-conscious'
            }
        }
        
        # Category-specific color guidance
        self.category_colors = {
            'packaged_snack': 'Warm colors (orange, brown, gold, red)',
            'beverage': 'Cool colors (blue, green, cyan, turquoise)',
            'dairy': 'Clean colors (white, cream, light blue, soft yellow)',
            'meat': 'Rich colors (red, brown, burgundy)',
            'organic': 'Earth tones (green, brown, beige, natural)',
            'frozen': 'Cool colors (ice blue, white, silver)',
            'ready_to_eat': 'Appetizing colors (red, orange, yellow)',
            'fortified': 'Health colors (green, blue, white)',
            'imported': 'Premium colors (gold, black, deep blue)'
        }
    
    def get_ai_design_params(self, product_data):
        """
        Use AI to generate design parameters based on country and category
        
        Args:
            product_data: Dictionary with product information
            
        Returns:
            Dictionary with design parameters
        """
        product_name = product_data.get('product_name', 'Product')
        category = product_data.get('category', 'packaged_snack')
        veg_status = product_data.get('veg_status', 'veg')
        
        # Get country and category guidance
        country_style = self.country_config.get(self.country, self.country_config['india'])
        category_color_guide = self.category_colors.get(category, 'Warm, appetizing colors')
        
        prompt = f"""You are a food packaging design expert. Generate design parameters for a food label.

PRODUCT INFORMATION:
- Product Name: {product_name}
- Category: {category}
- Country/Region: {self.country.upper()}
- Veg Status: {veg_status}

COUNTRY STYLE REQUIREMENTS ({self.country.upper()}):
- Style: {country_style['style']}
- Aesthetic: {country_style['aesthetic']}
- Typography: {country_style['typography']}
- Special Elements: {country_style['special_elements']}

CATEGORY COLOR GUIDANCE:
- {category_color_guide}

INSTRUCTIONS:
Generate colors that blend BOTH the country aesthetic AND food category appropriately.
For example:
- Indian snack: Vibrant orange/gold (Indian bold + snack warmth)
- US beverage: Clean blue/white (American modern + beverage cool)
- EU dairy: Elegant cream/white (European minimal + dairy clean)

Return ONLY valid JSON with these exact fields:
{{
    "primary_color": "#hex color for main background",
    "secondary_color": "#hex color for gradient",
    "accent_color": "#hex color for brand circle and price section",
    "badge_text": "short text like Premium/Fresh/Quality/Organic",
    "benefit_1": "short benefit text (max 20 chars)",
    "benefit_2": "short benefit text (max 20 chars)",
    "benefit_3": "short benefit text (max 20 chars)",
    "tagline": "short catchy tagline (max 30 chars)"
}}

Make the design appropriate for {self.country.upper()} market and {category} category."""

        try:
            response = self.client.chat.completions.create(
                deployment_id=self.deployment_id,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a food packaging design expert specializing in international markets. Return ONLY valid JSON, no explanations."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=400,
                temperature=0.7
            )
            
            content = response.choices[0].message.content.strip()
            
            # Clean markdown if present
            if '```json' in content:
                content = content.split('```json')[1].split('```')[0].strip()
            elif '```' in content:
                content = content.split('```')[1].split('```')[0].strip()
            
            design_params = json.loads(content)
            print(f"✓ AI generated design for {self.country.upper()} {category}")
            return design_params
            
        except Exception as e:
            print(f"⚠️ AI error, using defaults: {e}")
            return self._get_default_params(category)
    
    def _get_default_params(self, category):
        """Fallback design parameters by category"""
        defaults = {
            'packaged_snack': {
                'primary_color': '#ff6b35',
                'secondary_color': '#ffd700',
                'accent_color': '#138808',
                'badge_text': 'Premium',
                'benefit_1': 'Rich Flavor',
                'benefit_2': 'Crispy Texture',
                'benefit_3': 'Made with Love',
                'tagline': 'Deliciously Crafted'
            },
            'beverage': {
                'primary_color': '#00bcd4',
                'secondary_color': '#4caf50',
                'accent_color': '#006064',
                'badge_text': 'Fresh',
                'benefit_1': 'Refreshing',
                'benefit_2': 'Natural',
                'benefit_3': 'Energizing',
                'tagline': 'Pure Refreshment'
            },
            'dairy': {
                'primary_color': '#e3f2fd',
                'secondary_color': '#ffffff',
                'accent_color': '#1976d2',
                'badge_text': 'Pure',
                'benefit_1': 'Farm Fresh',
                'benefit_2': 'Rich Calcium',
                'benefit_3': 'Nutritious',
                'tagline': 'Naturally Good'
            }
        }
        return defaults.get(category, defaults['packaged_snack'])
    
    def generate_front_label(self, product_data):
        """
        Generate AI-powered front label HTML
        
        Args:
            product_data: Dictionary with product information
            
        Returns:
            HTML string for front label
        """
        # Get AI design parameters
        design = self.get_ai_design_params(product_data)
        
        # Extract product data
        product_name = product_data.get('product_name', 'Product')
        brand_name = product_data.get('manufacturer', {}).get('name', 'Brand').split()[0][:3].upper()
        veg_status = product_data.get('veg_status', 'veg')
        net_quantity = product_data.get('net_quantity', {})
        
        # Get price based on country
        if self.country == 'india':
            price = product_data.get('mrp', 0)
            currency = '₹'
            price_label = 'MRP (Incl. of all taxes)'
        elif self.country == 'us':
            price = product_data.get('price_usd', 0)
            currency = '$'
            price_label = 'Price'
        else:  # eu
            price = product_data.get('price_eur', 0)
            currency = '€'
            price_label = 'Price (VAT incl.)'
        
        veg_color = '#138808' if veg_status == 'veg' else '#8B4513'
        
        # Generate structured HTML with AI design parameters
        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{product_name} - Front Label</title>
    <style>
        body {{
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            background: #f0f0f0;
            margin: 0;
            font-family: Arial, sans-serif;
        }}
        
        .front-label {{
            width: 420px;
            height: 650px;
            background: linear-gradient(135deg, {design['primary_color']} 0%, {design['secondary_color']} 100%);
            position: relative;
            overflow: hidden;
            box-shadow: 0 10px 40px rgba(0,0,0,0.3);
        }}
        
        .badge {{
            position: absolute;
            top: 15px;
            left: 15px;
            background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%);
            padding: 8px 16px;
            font-weight: 900;
            font-size: 14px;
            color: #000;
            border-radius: 4px;
            transform: rotate(-5deg);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            z-index: 10;
        }}
        
        .veg-symbol {{
            position: absolute;
            top: 15px;
            right: 15px;
            width: 45px;
            height: 45px;
            border: 3px solid {veg_color};
            border-radius: 6px;
            background: white;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            z-index: 10;
        }}
        
        .veg-dot {{
            width: 22px;
            height: 22px;
            background: {veg_color};
            border-radius: 50%;
        }}
        
        .brand-circle {{
            width: 140px;
            height: 140px;
            margin: 60px auto 20px;
            background: linear-gradient(135deg, {design['accent_color']} 0%, {design['accent_color']}dd 100%);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            border: 6px solid white;
            box-shadow: 0 8px 24px rgba(0,0,0,0.4);
        }}
        
        .brand-text {{
            font-size: 42px;
            font-weight: 900;
            color: white;
            font-family: Arial Black, sans-serif;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        
        .product-name {{
            text-align: center;
            font-size: 42px;
            font-weight: 900;
            color: white;
            padding: 15px 20px;
            text-shadow: 3px 3px 6px rgba(0,0,0,0.5);
            font-family: Arial Black, sans-serif;
            line-height: 1.1;
        }}
        
        .tagline {{
            text-align: center;
            font-size: 14px;
            color: white;
            font-style: italic;
            margin-top: 5px;
            margin-bottom: 15px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.4);
        }}
        
        .benefits {{
            position: absolute;
            left: 0;
            top: 400px;
            width: 200px;
        }}
        
        .benefit-ribbon {{
            background: linear-gradient(90deg, #ff6b35 0%, #ff8c5a 100%);
            color: white;
            padding: 6px 15px 6px 10px;
            margin: 6px 0;
            font-weight: 700;
            font-size: 12px;
            box-shadow: 3px 3px 8px rgba(0,0,0,0.3);
            border-radius: 0 15px 15px 0;
        }}
        
        .product-visual {{
            width: 160px;
            height: 160px;
            position: absolute;
            right: 20px;
            top: 400px;
            background: radial-gradient(circle, rgba(255,255,255,0.9) 0%, rgba(255,255,255,0.7) 100%);
            border-radius: 50%;
            box-shadow: inset 0 4px 12px rgba(0,0,0,0.2), 0 8px 20px rgba(0,0,0,0.3);
        }}
        
        .bottom-info {{
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
        }}
        
        .net-qty {{
            background: rgba(255,255,255,0.95);
            text-align: center;
            padding: 15px;
            border-top: 4px solid {design['accent_color']};
        }}
        
        .net-qty-label {{
            font-size: 11px;
            font-weight: 700;
            color: #666;
            letter-spacing: 1px;
        }}
        
        .net-qty-value {{
            font-size: 32px;
            font-weight: 900;
            color: {design['primary_color']};
            margin-top: 5px;
        }}
        
        .price-section {{
            background: linear-gradient(90deg, {design['accent_color']} 0%, {design['accent_color']}dd 100%);
            text-align: center;
            padding: 15px;
            color: white;
        }}
        
        .price-label {{
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 0.5px;
        }}
        
        .price-value {{
            font-size: 34px;
            font-weight: 900;
            margin-top: 5px;
        }}
    </style>
</head>
<body>
    <div class="front-label">
        <div class="badge">{design['badge_text']}</div>
        
        <div class="veg-symbol">
            <div class="veg-dot"></div>
        </div>
        
        <div class="brand-circle">
            <div class="brand-text">{brand_name}</div>
        </div>
        
        <div class="product-name">{product_name.upper()}</div>
        <div class="tagline">{design['tagline']}</div>
        
        <div class="benefits">
            <div class="benefit-ribbon">{design['benefit_1']}</div>
            <div class="benefit-ribbon">{design['benefit_2']}</div>
            <div class="benefit-ribbon">{design['benefit_3']}</div>
        </div>
        
        <div class="product-visual"></div>
        
        <div class="bottom-info">
            <div class="net-qty">
                <div class="net-qty-label">NET QUANTITY</div>
                <div class="net-qty-value">{net_quantity.get('value', '')}{net_quantity.get('unit', '')}</div>
            </div>
            <div class="price-section">
                <div class="price-label">{price_label}</div>
                <div class="price-value">{currency}{price:.2f}</div>
            </div>
        </div>
    </div>
</body>
</html>"""
        
        return html


if __name__ == "__main__":
    # Test with India dataset
    generator = AIFrontLabelGenerator(country='india')
    
    with open('india_dataset/01_packaged_snack.json', 'r') as f:
        sample_data = json.load(f)
    
    print("=" * 60)
    print(f"AI Front Label Generator - {generator.country.upper()}")
    print("=" * 60)
    print()
    
    html = generator.generate_front_label(sample_data)
    
    output_file = f'test_ai_front_{generator.country}.html'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✓ Front label generated: {output_file}")
    print(f"\nCountry: {generator.country.upper()}")
    print(f"Category: {sample_data.get('category')}")
    print(f"Product: {sample_data.get('product_name')}")