"""
AI-Powered Label Generator - Alternatives to Chat Completion
Uses various AI approaches: Embeddings, Text Completion, Structured Output, Function Calling
"""

import os
import json
import requests
from dotenv import load_dotenv
from typing import Dict, Any, Optional

load_dotenv()


class AILabelAlternatives:
    """Multiple AI approaches for label generation without chat completion"""
    
    def __init__(self):
        """Initialize with SAP AI Core credentials"""
        self.auth_url = os.getenv('SAP_AI_CORE_AUTH_URL') or os.getenv('AICORE_AUTH_URL')
        self.api_url = os.getenv('SAP_AI_CORE_API_URL') or os.getenv('AICORE_BASE_URL')
        self.client_id = os.getenv('SAP_AI_CORE_CLIENT_ID') or os.getenv('AICORE_CLIENT_ID')
        self.client_secret = os.getenv('SAP_AI_CORE_CLIENT_SECRET') or os.getenv('AICORE_CLIENT_SECRET')
        self.deployment_id = os.getenv('SAP_AI_CORE_DEPLOYMENT_ID')
        self.embedding_deployment_id = os.getenv('SAP_AI_CORE_EMBEDDING_DEPLOYMENT_ID')
        self.resource_group = os.getenv('AICORE_RESOURCE_GROUP', 'default')
        self.token = None
        
        # Pre-defined label templates for embedding-based selection
        self.template_library = self._load_template_library()
    
    def get_token(self) -> Optional[str]:
        """Get OAuth2 access token"""
        if self.token:
            return self.token
            
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
            self.token = response.json()["access_token"]
            return self.token
        except Exception as e:
            print(f"❌ Token error: {e}")
            return None

    # =========================================================================
    # APPROACH 1: TEXT COMPLETION (Simpler than Chat)
    # =========================================================================
    def generate_with_text_completion(self, product_data: Dict[str, Any]) -> str:
        """
        Use text completion API instead of chat completion.
        Simpler, often faster, and sometimes cheaper.
        """
        if not self.get_token():
            return self._get_fallback(product_data)
        
        product_name = product_data.get('product_name', 'Product')
        category = product_data.get('category', 'packaged_snack')
        
        # Single prompt (no system/user roles)
        prompt = f"""Complete the following HTML code for a {category} food label:

Product: {product_name}
Category: {category}
Brand: {product_data.get('manufacturer', {}).get('name', 'Brand')[:3].upper()}
Veg Status: {product_data.get('veg_status', 'veg')}
Net Quantity: {product_data.get('net_quantity', {}).get('value', '')} {product_data.get('net_quantity', {}).get('unit', '')}
MRP: ₹{product_data.get('mrp', 0):.2f}

<style>
.front-label {{
    width: 420px;
    height: 650px;
    background: linear-gradient(135deg,"""

        # Use completions endpoint (not chat/completions)
        endpoint = f"{self.api_url}/v2/inference/deployments/{self.deployment_id}/completions"
        
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "AI-Resource-Group": self.resource_group
        }
        
        payload = {
            "prompt": prompt,
            "max_tokens": 1500,
            "temperature": 0.7,
            "stop": ["</div>\n\n", "```"]  # Stop sequences
        }
        
        try:
            response = requests.post(endpoint, headers=headers, json=payload, timeout=30)
            if response.status_code == 200:
                result = response.json()
                # Text completion returns in 'choices[0].text' not 'message.content'
                generated = result.get('choices', [{}])[0].get('text', '')
                # Reconstruct full HTML
                full_html = prompt.split('<style>')[1] + generated
                return f"<style>{full_html}"
            else:
                print(f"Text completion failed: {response.status_code}")
                return self._get_fallback(product_data)
        except Exception as e:
            print(f"Error: {e}")
            return self._get_fallback(product_data)

    # =========================================================================
    # APPROACH 2: EMBEDDINGS + TEMPLATE SELECTION
    # =========================================================================
    def generate_with_embeddings(self, product_data: Dict[str, Any]) -> str:
        """
        Use embeddings to find the most similar template.
        AI selects the best template, then fills in data.
        """
        if not self.get_token():
            return self._get_fallback(product_data)
        
        # Create description of the product
        description = f"{product_data.get('category', '')} {product_data.get('product_name', '')} {product_data.get('veg_status', '')}"
        
        # Get embedding for product description
        product_embedding = self._get_embedding(description)
        if not product_embedding:
            return self._get_fallback(product_data)
        
        # Find most similar template
        best_template = self._find_best_template(product_embedding)
        
        # Fill template with product data
        return self._fill_template(best_template, product_data)
    
    def _get_embedding(self, text: str) -> Optional[list]:
        """Get embedding vector for text"""
        deployment_id = self.embedding_deployment_id or self.deployment_id
        endpoint = f"{self.api_url}/v2/inference/deployments/{deployment_id}/embeddings"
        
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "AI-Resource-Group": self.resource_group
        }
        
        payload = {
            "input": text,
            "model": "text-embedding-ada-002"  # or your embedding model
        }
        
        try:
            response = requests.post(endpoint, headers=headers, json=payload, timeout=15)
            if response.status_code == 200:
                return response.json()['data'][0]['embedding']
        except Exception as e:
            print(f"Embedding error: {e}")
        return None
    
    def _find_best_template(self, product_embedding: list) -> Dict:
        """Find template with highest cosine similarity"""
        import math
        
        def cosine_similarity(a, b):
            dot = sum(x*y for x, y in zip(a, b))
            norm_a = math.sqrt(sum(x*x for x in a))
            norm_b = math.sqrt(sum(x*x for x in b))
            return dot / (norm_a * norm_b) if norm_a and norm_b else 0
        
        best_score = -1
        best_template = self.template_library[0]
        
        for template in self.template_library:
            if 'embedding' in template:
                score = cosine_similarity(product_embedding, template['embedding'])
                if score > best_score:
                    best_score = score
                    best_template = template
        
        print(f"✓ Selected template: {best_template['name']} (similarity: {best_score:.3f})")
        return best_template

    # =========================================================================
    # APPROACH 3: STRUCTURED OUTPUT (JSON Mode)
    # =========================================================================
    def generate_with_structured_output(self, product_data: Dict[str, Any]) -> str:
        """
        Use AI to generate structured JSON, then render to HTML.
        More reliable than generating raw HTML.
        """
        if not self.get_token():
            return self._get_fallback(product_data)
        
        endpoint = f"{self.api_url}/v2/inference/deployments/{self.deployment_id}/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "AI-Resource-Group": self.resource_group
        }
        
        # Ask AI to generate structured design decisions, not HTML
        payload = {
            "messages": [
                {
                    "role": "user",
                    "content": f"""For a {product_data.get('category', 'food')} product label, provide design choices as JSON:

Product: {product_data.get('product_name', 'Product')}
Category: {product_data.get('category', 'packaged_snack')}

Return ONLY valid JSON with these fields:
{{
    "primary_color": "#hex",
    "secondary_color": "#hex", 
    "accent_color": "#hex",
    "gradient_direction": "135deg",
    "font_style": "bold/normal",
    "badge_text": "Premium/Fresh/etc",
    "tagline": "short tagline"
}}"""
                }
            ],
            "max_tokens": 300,
            "temperature": 0.7,
            "response_format": {"type": "json_object"}  # Force JSON output
        }
        
        try:
            response = requests.post(endpoint, headers=headers, json=payload, timeout=20)
            if response.status_code == 200:
                result = response.json()
                design_json = result['choices'][0]['message']['content']
                design = json.loads(design_json)
                
                # Use AI-generated design choices with template
                return self._render_with_design(product_data, design)
            else:
                print(f"Structured output failed: {response.status_code}")
        except Exception as e:
            print(f"Error: {e}")
        
        return self._get_fallback(product_data)
    
    def _render_with_design(self, product_data: Dict, design: Dict) -> str:
        """Render HTML using AI-generated design choices"""
        product_name = product_data.get('product_name', 'Product')
        brand = product_data.get('manufacturer', {}).get('name', 'Brand')[:3].upper()
        veg_status = product_data.get('veg_status', 'veg')
        net_qty = product_data.get('net_quantity', {})
        mrp = product_data.get('mrp', 0)
        
        primary = design.get('primary_color', '#ff6b35')
        secondary = design.get('secondary_color', '#ffd700')
        accent = design.get('accent_color', '#138808')
        direction = design.get('gradient_direction', '135deg')
        badge = design.get('badge_text', 'Premium')
        tagline = design.get('tagline', '')
        
        veg_color = '#138808' if veg_status == 'veg' else '#8B4513'
        
        return f"""
<style>
.front-label-ai {{
    width: 420px; height: 650px;
    background: linear-gradient({direction}, {primary} 0%, {secondary} 100%);
    position: relative; overflow: hidden; font-family: Arial Black, sans-serif;
}}
.badge {{ position: absolute; top: 15px; left: 15px; background: gold; padding: 8px 15px; font-weight: bold; transform: rotate(-15deg); }}
.veg-symbol {{ position: absolute; top: 15px; right: 15px; width: 45px; height: 45px; border: 3px solid {veg_color}; background: white; display: flex; align-items: center; justify-content: center; border-radius: 6px; }}
.veg-dot {{ width: 22px; height: 22px; background: {veg_color}; border-radius: 50%; }}
.brand-circle {{ width: 140px; height: 140px; margin: 60px auto 20px; background: {accent}; border-radius: 50%; display: flex; align-items: center; justify-content: center; border: 6px solid white; box-shadow: 0 8px 24px rgba(0,0,0,0.4); }}
.brand-text {{ font-size: 42px; font-weight: 900; color: white; }}
.product-name {{ text-align: center; font-size: 48px; font-weight: 900; color: white; padding: 20px; text-shadow: 3px 3px 6px rgba(0,0,0,0.5); }}
.tagline {{ text-align: center; font-size: 18px; color: white; font-style: italic; }}
.bottom-info {{ position: absolute; bottom: 0; left: 0; right: 0; }}
.net-qty {{ background: rgba(255,255,255,0.95); text-align: center; padding: 15px; border-top: 4px solid {accent}; }}
.mrp {{ background: {accent}; text-align: center; padding: 15px; color: white; }}
</style>
<div class="front-label-ai">
    <div class="badge">{badge}</div>
    <div class="veg-symbol"><div class="veg-dot"></div></div>
    <div class="brand-circle"><div class="brand-text">{brand}</div></div>
    <div class="product-name">{product_name.upper()}</div>
    <div class="tagline">{tagline}</div>
    <div class="bottom-info">
        <div class="net-qty">
            <div style="font-size: 11px; font-weight: 700; color: #666;">NET QUANTITY</div>
            <div style="font-size: 32px; font-weight: 900; color: {primary};">{net_qty.get('value', '')}{net_qty.get('unit', '')}</div>
        </div>
        <div class="mrp">
            <div style="font-size: 11px;">MRP (Incl. of all taxes)</div>
            <div style="font-size: 34px; font-weight: 900;">₹{mrp:.2f}</div>
        </div>
    </div>
</div>
"""

    # =========================================================================
    # APPROACH 4: FUNCTION CALLING
    # =========================================================================
    def generate_with_function_calling(self, product_data: Dict[str, Any]) -> str:
        """
        Use function calling to get structured design parameters.
        AI calls a 'design_label' function with specific parameters.
        """
        if not self.get_token():
            return self._get_fallback(product_data)
        
        endpoint = f"{self.api_url}/v2/inference/deployments/{self.deployment_id}/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "AI-Resource-Group": self.resource_group
        }
        
        # Define the function the AI should call
        functions = [
            {
                "name": "design_label",
                "description": "Design a food product label with specific colors and style",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "primary_color": {
                            "type": "string",
                            "description": "Primary background color in hex format"
                        },
                        "secondary_color": {
                            "type": "string",
                            "description": "Secondary/gradient color in hex format"
                        },
                        "accent_color": {
                            "type": "string",
                            "description": "Accent color for highlights in hex format"
                        },
                        "style": {
                            "type": "string",
                            "enum": ["vibrant", "elegant", "fresh", "traditional", "modern"],
                            "description": "Overall design style"
                        },
                        "badge_text": {
                            "type": "string",
                            "description": "Text for the premium badge"
                        }
                    },
                    "required": ["primary_color", "secondary_color", "accent_color", "style"]
                }
            }
        ]
        
        payload = {
            "messages": [
                {
                    "role": "user",
                    "content": f"Design a label for: {product_data.get('product_name', 'Product')} ({product_data.get('category', 'food')})"
                }
            ],
            "functions": functions,
            "function_call": {"name": "design_label"},  # Force this function
            "max_tokens": 200,
            "temperature": 0.7
        }
        
        try:
            response = requests.post(endpoint, headers=headers, json=payload, timeout=20)
            if response.status_code == 200:
                result = response.json()
                function_call = result['choices'][0]['message'].get('function_call', {})
                if function_call:
                    design = json.loads(function_call.get('arguments', '{}'))
                    return self._render_with_design(product_data, design)
        except Exception as e:
            print(f"Function calling error: {e}")
        
        return self._get_fallback(product_data)

    # =========================================================================
    # APPROACH 5: SIMPLE INFERENCE (Classification)
    # =========================================================================
    def generate_with_classification(self, product_data: Dict[str, Any]) -> str:
        """
        Use AI for simple classification, then use pre-built templates.
        Minimal AI usage - just for decision making.
        """
        if not self.get_token():
            category = product_data.get('category', 'packaged_snack')
        else:
            # Ask AI to classify the product style
            endpoint = f"{self.api_url}/v2/inference/deployments/{self.deployment_id}/chat/completions"
            
            headers = {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
                "AI-Resource-Group": self.resource_group
            }
            
            payload = {
                "messages": [
                    {
                        "role": "user",
                        "content": f"""Classify this product into ONE style category.
Product: {product_data.get('product_name', '')}
Category: {product_data.get('category', '')}

Reply with ONLY one word: vibrant, fresh, elegant, traditional, or healthy"""
                    }
                ],
                "max_tokens": 10,
                "temperature": 0
            }
            
            try:
                response = requests.post(endpoint, headers=headers, json=payload, timeout=10)
                if response.status_code == 200:
                    style = response.json()['choices'][0]['message']['content'].strip().lower()
                else:
                    style = 'vibrant'
            except:
                style = 'vibrant'
        
        # Use pre-defined style templates
        styles = {
            'vibrant': {'primary': '#ff6b35', 'secondary': '#ffd700', 'accent': '#138808'},
            'fresh': {'primary': '#4caf50', 'secondary': '#81c784', 'accent': '#2e7d32'},
            'elegant': {'primary': '#1a237e', 'secondary': '#3949ab', 'accent': '#c9b037'},
            'traditional': {'primary': '#8d6e63', 'secondary': '#d7ccc8', 'accent': '#5d4037'},
            'healthy': {'primary': '#66bb6a', 'secondary': '#a5d6a7', 'accent': '#2e7d32'}
        }
        
        design = styles.get(style, styles['vibrant'])
        design['badge_text'] = style.capitalize()
        
        return self._render_with_design(product_data, design)

    # =========================================================================
    # HELPER METHODS
    # =========================================================================
    def _load_template_library(self) -> list:
        """Load pre-defined templates with embeddings"""
        return [
            {
                'name': 'snack_vibrant',
                'category': 'packaged_snack',
                'colors': {'primary': '#ff6b35', 'secondary': '#ffd700', 'accent': '#138808'},
                'embedding': None  # Would be pre-computed
            },
            {
                'name': 'beverage_fresh',
                'category': 'beverage',
                'colors': {'primary': '#00bcd4', 'secondary': '#4caf50', 'accent': '#006064'},
                'embedding': None
            },
            {
                'name': 'dairy_clean',
                'category': 'dairy',
                'colors': {'primary': '#e3f2fd', 'secondary': '#ffffff', 'accent': '#1976d2'},
                'embedding': None
            }
        ]
    
    def _fill_template(self, template: Dict, product_data: Dict) -> str:
        """Fill selected template with product data"""
        colors = template.get('colors', {})
        design = {
            'primary_color': colors.get('primary', '#ff6b35'),
            'secondary_color': colors.get('secondary', '#ffd700'),
            'accent_color': colors.get('accent', '#138808'),
            'badge_text': template.get('name', 'Premium').split('_')[0].capitalize()
        }
        return self._render_with_design(product_data, design)
    
    def _get_fallback(self, product_data: Dict) -> str:
        """Fallback template when AI fails"""
        return self._render_with_design(product_data, {
            'primary_color': '#ff6b35',
            'secondary_color': '#ffd700',
            'accent_color': '#138808',
            'badge_text': 'Premium'
        })


# =============================================================================
# DEMO / TEST
# =============================================================================
if __name__ == "__main__":
    generator = AILabelAlternatives()
    
    # Sample product data
    sample_data = {
        "product_name": "Chocolate Chip Cookies",
        "category": "packaged_snack",
        "veg_status": "veg",
        "manufacturer": {"name": "Britannia Industries"},
        "net_quantity": {"value": 200, "unit": "g"},
        "mrp": 45.00
    }
    
    print("=" * 70)
    print("AI Label Generator - Alternatives to Chat Completion")
    print("=" * 70)
    
    # Test each approach
    approaches = [
        ("1. Structured Output (JSON Mode)", generator.generate_with_structured_output),
        ("2. Classification + Templates", generator.generate_with_classification),
        ("3. Function Calling", generator.generate_with_function_calling),
    ]
    
    for name, method in approaches:
        print(f"\n{name}")
        print("-" * 50)
        try:
            html = method(sample_data)
            filename = f"test_ai_{name.split('.')[0].strip()}.html"
            with open(filename, 'w') as f:
                f.write(f"""<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><title>{name}</title></head>
<body style="display: flex; justify-content: center; align-items: center; min-height: 100vh; background: #f0f0f0;">
{html}
</body>
</html>""")
            print(f"✓ Generated: {filename}")
        except Exception as e:
            print(f"✗ Error: {e}")
    
    print("\n" + "=" * 70)
    print("Summary of AI Approaches (No Chat Completion Required):")
    print("=" * 70)
    print("""
1. STRUCTURED OUTPUT (JSON Mode)
   - AI generates design parameters as JSON
   - You render HTML from structured data
   - More reliable, predictable output

2. CLASSIFICATION + TEMPLATES  
   - AI classifies product into style category
   - Pre-built templates for each category
   - Minimal AI usage, maximum control

3. FUNCTION CALLING
   - AI calls a defined function with parameters
   - Structured, type-safe output
   - Best for complex design decisions

4. EMBEDDINGS (Semantic Search)
   - AI finds most similar template
   - No generation, just selection
   - Fast and cost-effective

5. TEXT COMPLETION
   - Simpler than chat completion
   - Single prompt, no roles
   - Good for completing partial templates
""")