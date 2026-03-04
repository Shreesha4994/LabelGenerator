"""
AI-Powered Label Generator using SAP AI Core REST API
Direct REST API calls instead of SDK
"""

import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

class AILabelGeneratorREST:
    def __init__(self):
        """Initialize with SAP AI Core credentials"""
        self.auth_url = os.getenv('SAP_AI_CORE_AUTH_URL')
        self.api_url = os.getenv('SAP_AI_CORE_API_URL')
        self.client_id = os.getenv('SAP_AI_CORE_CLIENT_ID')
        self.client_secret = os.getenv('SAP_AI_CORE_CLIENT_SECRET')
        self.deployment_id = os.getenv('SAP_AI_CORE_DEPLOYMENT_ID')
        self.token = None
        
    def get_token(self):
        """Get OAuth2 access token"""
        print("🔐 Getting access token...")
        
        try:
            response = requests.post(
                f"{self.auth_url}/oauth/token",
                data={
                    "grant_type": "client_credentials",
                    "client_id": self.client_id,
                    "client_secret": self.client_secret
                },
                timeout=10
            )
            response.raise_for_status()
            
            token_data = response.json()
            self.token = token_data["access_token"]
            print(f"✅ Token obtained!")
            return self.token
            
        except Exception as e:
            print(f"❌ Failed to get token: {e}")
            return None
    
    def get_food_type_style(self, food_type):
        """Get style guidelines for different food types"""
        styles = {
            'packaged_snack': {
                'colors': 'warm oranges, browns, golds',
                'vibe': 'appetizing, fun, energetic',
                'imagery': 'cookies, biscuits, snacks visible'
            },
            'beverage': {
                'colors': 'fresh blues, greens, vibrant',
                'vibe': 'refreshing, clean, energetic',
                'imagery': 'liquid splash, freshness'
            },
            'dairy': {
                'colors': 'clean whites, creams, light blues',
                'vibe': 'pure, fresh, trustworthy',
                'imagery': 'milk drops, dairy products'
            }
        }
        return styles.get(food_type, styles['packaged_snack'])
    
    def generate_front_label_html(self, product_data):
        """Generate HTML/CSS for front label using AI"""
        
        # Get token if not already obtained
        if not self.token:
            if not self.get_token():
                print("⚠️ Using fallback template")
                return self._get_fallback_template(product_data)
        
        # Extract product information
        product_name = product_data.get('product_name', 'Product')
        category = product_data.get('category', 'packaged_snack')
        brand_name = product_data.get('manufacturer', {}).get('name', 'Brand').split()[0][:3].upper()
        veg_status = product_data.get('veg_status', 'veg')
        net_quantity = product_data.get('net_quantity', {})
        mrp = product_data.get('mrp', 0)
        
        # Get food-type-specific styling
        style_guide = self.get_food_type_style(category)
        
        # Create structured prompt
        prompt = f"""Generate ONLY the HTML code for a professional Indian food product front label. Follow these EXACT requirements:

MANDATORY STRUCTURE (DO NOT DEVIATE):
1. Container div with class "front-label-ai" (420px width, 650px height)
2. Veg/Non-Veg symbol (top-right, 45x45px, green border for veg, brown for non-veg)
3. Premium badge (top-left corner, gold/yellow)
4. Brand circle logo (centered top, 140px diameter, contains "{brand_name}")
5. Product name (large, bold, centered, "{product_name}")
6. Product visual area (circular, 200px, centered)
7. Benefit ribbons (left side, 3 ribbons with benefits)
8. Quality badges (right side, circular badges)
9. Net Quantity section (bottom, white background, "{net_quantity.get('value', '')}{net_quantity.get('unit', '')}")
10. MRP section (very bottom, green background, "₹{mrp:.2f}")

STYLING REQUIREMENTS:
- Food Type: {category}
- Color Scheme: {style_guide['colors']}
- Design Vibe: {style_guide['vibe']}
- Background: Vibrant gradient with sunburst rays effect
- Typography: Bold, Indian FMCG style (Arial Black)
- Shadows: Strong text shadows for depth

OUTPUT FORMAT:
Return ONLY the HTML code starting with <div class="front-label-ai"> and ending with </div>. Include <style> tag at the beginning. NO explanations, NO markdown, JUST the HTML code."""

        # Call SAP AI Core
        endpoint = f"{self.api_url}/v2/inference/deployments/{self.deployment_id}/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "AI-Resource-Group": "default"
        }
        
        payload = {
            "messages": [
                {
                    "role": "system",
                    "content": "You are an expert Indian food packaging designer. Generate clean, valid HTML/CSS code for food labels. Follow instructions exactly. Output ONLY HTML code, no explanations."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": 2000,
            "temperature": 0.7
        }
        
        try:
            print(f"🤖 Generating AI label for {product_name}...")
            response = requests.post(
                endpoint,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                generated_html = result['choices'][0]['message']['content'].strip()
                
                # Clean up markdown if present
                if '```html' in generated_html:
                    generated_html = generated_html.split('```html')[1].split('```')[0].strip()
                elif '```' in generated_html:
                    generated_html = generated_html.split('```')[1].split('```')[0].strip()
                
                print(f"✅ AI label generated successfully!")
                return generated_html
            else:
                print(f"❌ API Error: {response.status_code}")
                print(f"Response: {response.text[:200]}")
                return self._get_fallback_template(product_data)
                
        except Exception as e:
            print(f"❌ Error generating AI label: {e}")
            return self._get_fallback_template(product_data)
    
    def _get_fallback_template(self, product_data):
        """Fallback template if AI generation fails"""
        product_name = product_data.get('product_name', 'Product')
        brand_name = product_data.get('manufacturer', {}).get('name', 'Brand').split()[0][:3].upper()
        veg_status = product_data.get('veg_status', 'veg')
        net_quantity = product_data.get('net_quantity', {})
        mrp = product_data.get('mrp', 0)
        
        veg_color = '#138808' if veg_status == 'veg' else '#8B4513'
        
        return f"""
<style>
.front-label-ai {{
    width: 420px;
    height: 650px;
    background: linear-gradient(135deg, #ff6b35 0%, #f7931e 50%, #ffd700 100%);
    position: relative;
    overflow: hidden;
}}
.veg-symbol-ai {{
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
}}
.veg-dot-ai {{
    width: 22px;
    height: 22px;
    background: {veg_color};
    border-radius: 50%;
}}
.brand-circle-ai {{
    width: 140px;
    height: 140px;
    margin: 50px auto 20px;
    background: linear-gradient(135deg, #138808 0%, #0d5e06 100%);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 6px solid white;
    box-shadow: 0 8px 24px rgba(0,0,0,0.4);
}}
.brand-text-ai {{
    font-size: 42px;
    font-weight: 900;
    color: white;
    font-family: Arial Black, sans-serif;
}}
.product-name-ai {{
    text-align: center;
    font-size: 56px;
    font-weight: 900;
    color: white;
    padding: 20px;
    text-shadow: 4px 4px 8px rgba(0,0,0,0.5);
    font-family: Arial Black, sans-serif;
}}
.bottom-info-ai {{
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
}}
.net-qty-ai {{
    background: rgba(255,255,255,0.95);
    text-align: center;
    padding: 15px;
    border-top: 4px solid #138808;
}}
.mrp-ai {{
    background: linear-gradient(90deg, #138808 0%, #0d5e06 100%);
    text-align: center;
    padding: 15px;
    color: white;
}}
</style>
<div class="front-label-ai">
    <div class="veg-symbol-ai">
        <div class="veg-dot-ai"></div>
    </div>
    <div class="brand-circle-ai">
        <div class="brand-text-ai">{brand_name}</div>
    </div>
    <div class="product-name-ai">{product_name.upper()}</div>
    <div class="bottom-info-ai">
        <div class="net-qty-ai">
            <div style="font-size: 11px; font-weight: 700; color: #666;">NET QUANTITY</div>
            <div style="font-size: 32px; font-weight: 900; color: #d35400;">{net_quantity.get('value', '')}{net_quantity.get('unit', '')}</div>
        </div>
        <div class="mrp-ai">
            <div style="font-size: 11px; font-weight: 700;">MRP (Incl. of all taxes)</div>
            <div style="font-size: 34px; font-weight: 900;">₹{mrp:.2f}</div>
        </div>
    </div>
</div>
"""


if __name__ == "__main__":
    # Test the generator
    generator = AILabelGeneratorREST()
    
    # Load sample data
    with open('india_dataset/01_packaged_snack.json', 'r') as f:
        sample_data = json.load(f)
    
    print("=" * 60)
    print("AI-Powered Label Generator (REST API)")
    print("=" * 60)
    
    html = generator.generate_front_label_html(sample_data)
    
    # Save to file
    with open('test_ai_label_rest.html', 'w') as f:
        f.write(f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>AI Generated Label (REST API)</title>
</head>
<body style="display: flex; justify-content: center; align-items: center; min-height: 100vh; background: #f0f0f0;">
    {html}
</body>
</html>""")
    
    print("\n✅ Label saved to: test_ai_label_rest.html")