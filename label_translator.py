#!/usr/bin/env python3
"""
Label Translator using SAP Translation Hub
Translates food label HTML content while preserving structure
"""

import os
import re
import requests
from dotenv import load_dotenv

load_dotenv()


class LabelTranslator:
    """Translate food labels using SAP Translation Hub"""
    
    def __init__(self):
        """Initialize translator with SAP Translation Hub credentials"""
        self.client_id = os.getenv('TRANSLATION_HUB_CLIENT_ID', 
            'sb-4c7fd105-8928-41e0-837c-10763f2be6bc!b14569|sap-translation-hub-eu11!b999')
        self.client_secret = os.getenv('TRANSLATION_HUB_CLIENT_SECRET',
            'e0cfe629-7418-4383-82fa-5c2c048b268c$uhPSnGG2PnUXvWapECIkhPh3HNp203-9eobZLiFVvXY=')
        self.auth_url = os.getenv('TRANSLATION_HUB_AUTH_URL',
            'https://test-nbhfe3tt.authentication.eu11.hana.ondemand.com')
        self.api_url = os.getenv('TRANSLATION_HUB_API_URL',
            'https://document-translation.api.eu11.translationhub.cloud.sap')
        
        self._token = None
        self._token_expires = 0
        
        # Supported language codes
        self.supported_languages = {
            'de-DE': 'German',
            'fr-FR': 'French',
            'es-ES': 'Spanish',
            'it-IT': 'Italian',
            'pt-BR': 'Portuguese (Brazil)',
            'pt-PT': 'Portuguese (Portugal)',
            'hi-IN': 'Hindi',
            'ta-IN': 'Tamil',
            'te-IN': 'Telugu',
            'bn-IN': 'Bengali',
            'ja-JP': 'Japanese',
            'zh-CN': 'Chinese (Simplified)',
            'zh-TW': 'Chinese (Traditional)',
            'ko-KR': 'Korean',
            'ar-SA': 'Arabic',
            'ru-RU': 'Russian',
            'nl-NL': 'Dutch',
            'pl-PL': 'Polish',
            'sv-SE': 'Swedish',
            'da-DK': 'Danish',
            'fi-FI': 'Finnish',
            'no-NO': 'Norwegian',
            'tr-TR': 'Turkish',
            'th-TH': 'Thai',
            'vi-VN': 'Vietnamese',
            'id-ID': 'Indonesian',
            'ms-MY': 'Malay'
        }
    
    def _get_token(self):
        """Get OAuth token from SAP Translation Hub"""
        try:
            response = requests.post(
                f"{self.auth_url}/oauth/token",
                data={"grant_type": "client_credentials"},
                auth=(self.client_id, self.client_secret),
                timeout=30
            )
            response.raise_for_status()
            token_data = response.json()
            self._token = token_data["access_token"]
            return self._token
        except Exception as e:
            print(f"Error getting translation token: {e}")
            raise ValueError(f"Failed to authenticate with Translation Hub: {e}")
    
    def translate_text(self, text, source_language='en-US', target_language='de-DE'):
        """
        Translate text using SAP Translation Hub
        
        Args:
            text: Text to translate
            source_language: Source language code (default: en-US)
            target_language: Target language code (e.g., de-DE, hi-IN)
            
        Returns:
            Translated text
        """
        if not text or not text.strip():
            return text
        
        # Get fresh token
        token = self._get_token()
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(
                f"{self.api_url}/api/v1/translation",
                headers=headers,
                json={
                    "data": text,
                    "sourceLanguage": source_language,
                    "targetLanguage": target_language
                },
                timeout=60
            )
            response.raise_for_status()
            result = response.json()
            return result.get('data', text)
        except Exception as e:
            print(f"Translation error: {e}")
            return text  # Return original text on error
    
    def _should_translate(self, text):
        """
        Check if text should be translated
        Skip numbers, units, percentages, special characters only
        """
        if not text or not text.strip():
            return False
        
        stripped = text.strip()
        
        # Skip if it's just whitespace
        if not stripped:
            return False
        
        # Skip if it's just numbers with optional units
        if re.match(r'^[\d.,]+\s*(g|mg|mcg|kg|ml|l|oz|lb|%|kcal)?$', stripped, re.IGNORECASE):
            return False
        
        # Skip if it's just a percentage
        if re.match(r'^[\d.,]+%$', stripped):
            return False
        
        # Skip if it's just special characters
        if re.match(r'^[*#@$%^&()_+=\-\[\]{}|\\:";\'<>,.?/~`!]+$', stripped):
            return False
        
        # Skip if it's a barcode number pattern
        if re.match(r'^[\d\s]+$', stripped):
            return False
        
        # Skip single characters
        if len(stripped) <= 1:
            return False
        
        # Skip CSS-like values
        if re.match(r'^#[0-9a-fA-F]{3,6}$', stripped):
            return False
        
        # Skip URLs
        if stripped.startswith('http') or stripped.startswith('www.'):
            return False
        
        # Skip email addresses
        if '@' in stripped and '.' in stripped:
            return False
        
        # Skip phone numbers
        if re.match(r'^[\d\s\-\+\(\)]+$', stripped) and len(stripped) > 5:
            return False
        
        return True
    
    def translate_html_label(self, html_content, source_language='en-US', target_language='de-DE'):
        """
        Translate HTML label content while preserving structure
        Uses a robust approach to maintain HTML integrity for all languages including Hindi
        
        Args:
            html_content: HTML string to translate
            source_language: Source language code
            target_language: Target language code
            
        Returns:
            Translated HTML string
        """
        if not html_content:
            return html_content
        
        # Store all protected content with unique markers
        protected_content = {}
        marker_counter = [0]  # Use list to allow modification in nested function
        
        def create_marker(prefix):
            """Create a unique marker that won't be affected by translation"""
            marker = f"⟦{prefix}{marker_counter[0]}⟧"
            marker_counter[0] += 1
            return marker
        
        def protect_content(match, prefix):
            """Save content and return a marker"""
            marker = create_marker(prefix)
            protected_content[marker] = match.group(0)
            return marker
        
        working_html = html_content
        
        # Step 1: Protect DOCTYPE
        doctype_pattern = re.compile(r'<!DOCTYPE[^>]*>', re.IGNORECASE)
        working_html = doctype_pattern.sub(lambda m: protect_content(m, 'DOC'), working_html)
        
        # Step 2: Protect all HTML comments
        comment_pattern = re.compile(r'<!--[\s\S]*?-->', re.DOTALL)
        working_html = comment_pattern.sub(lambda m: protect_content(m, 'CMT'), working_html)
        
        # Step 3: Protect style blocks (including content)
        style_pattern = re.compile(r'<style[^>]*>[\s\S]*?</style>', re.IGNORECASE | re.DOTALL)
        working_html = style_pattern.sub(lambda m: protect_content(m, 'STY'), working_html)
        
        # Step 4: Protect script blocks (including content)
        script_pattern = re.compile(r'<script[^>]*>[\s\S]*?</script>', re.IGNORECASE | re.DOTALL)
        working_html = script_pattern.sub(lambda m: protect_content(m, 'SCR'), working_html)
        
        # Step 5: Protect SVG content
        svg_pattern = re.compile(r'<svg[^>]*>[\s\S]*?</svg>', re.IGNORECASE | re.DOTALL)
        working_html = svg_pattern.sub(lambda m: protect_content(m, 'SVG'), working_html)
        
        # Step 6: Protect all HTML tags (opening, closing, self-closing)
        # This preserves the structure while allowing text content to be translated
        tag_pattern = re.compile(r'<[^>]+>')
        working_html = tag_pattern.sub(lambda m: protect_content(m, 'TAG'), working_html)
        
        # Step 7: Protect HTML entities
        entity_pattern = re.compile(r'&[a-zA-Z0-9#]+;')
        working_html = entity_pattern.sub(lambda m: protect_content(m, 'ENT'), working_html)
        
        # Step 8: Now we have only text content left - collect unique texts to translate
        # Split by markers and translate each text segment
        marker_pattern = re.compile(r'(⟦[A-Z]+\d+⟧)')
        segments = marker_pattern.split(working_html)
        
        # Collect unique texts that need translation
        texts_to_translate = {}
        for segment in segments:
            if not segment.startswith('⟦') and segment.strip():
                stripped = segment.strip()
                if self._should_translate(stripped) and stripped not in texts_to_translate:
                    texts_to_translate[stripped] = None
        
        # Translate all unique texts
        for text in texts_to_translate.keys():
            try:
                translated = self.translate_text(text, source_language, target_language)
                if translated:
                    texts_to_translate[text] = translated
            except Exception as e:
                print(f"Failed to translate '{text[:50]}...': {e}")
                texts_to_translate[text] = text  # Keep original on error
        
        # Step 9: Rebuild HTML with translated text
        result_segments = []
        for segment in segments:
            if segment.startswith('⟦'):
                # This is a marker - will be restored later
                result_segments.append(segment)
            elif segment.strip():
                # This is text content - replace with translation if available
                stripped = segment.strip()
                if stripped in texts_to_translate and texts_to_translate[stripped]:
                    # Preserve leading/trailing whitespace
                    leading_ws = segment[:len(segment) - len(segment.lstrip())]
                    trailing_ws = segment[len(segment.rstrip()):]
                    result_segments.append(f"{leading_ws}{texts_to_translate[stripped]}{trailing_ws}")
                else:
                    result_segments.append(segment)
            else:
                # Whitespace only - preserve it
                result_segments.append(segment)
        
        working_html = ''.join(result_segments)
        
        # Step 10: Restore all protected content in reverse order of protection
        # Sort markers by their numeric suffix in descending order to restore correctly
        sorted_markers = sorted(protected_content.keys(), 
                               key=lambda x: int(re.search(r'\d+', x).group()), 
                               reverse=True)
        
        for marker in sorted_markers:
            working_html = working_html.replace(marker, protected_content[marker])
        
        # Step 11: Update the lang attribute in HTML tag if present
        working_html = re.sub(
            r'(<html[^>]*\slang=")[^"]*(")',
            f'\\g<1>{target_language}\\g<2>',
            working_html,
            flags=re.IGNORECASE
        )
        
        # Also update lang attribute without quotes
        working_html = re.sub(
            r"(<html[^>]*\slang=')[^']*(')",
            f"\\g<1>{target_language}\\g<2>",
            working_html,
            flags=re.IGNORECASE
        )
        
        return working_html
    
    def get_supported_languages(self):
        """Return list of supported language codes and names"""
        return self.supported_languages
    
    def is_language_supported(self, language_code):
        """Check if a language code is supported"""
        return language_code in self.supported_languages


if __name__ == "__main__":
    # Test the translator
    translator = LabelTranslator()
    
    print("Supported Languages:")
    for code, name in translator.supported_languages.items():
        print(f"  {code}: {name}")
    
    print("\n" + "=" * 50)
    print("Testing Translation...")
    print("=" * 50)
    
    # Test simple text translation
    test_text = "Hello World! Welcome to the Food Label Generator."
    print(f"\nOriginal: {test_text}")
    
    try:
        translated = translator.translate_text(test_text, 'en-US', 'de-DE')
        print(f"German:   {translated}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test HTML translation with a more complex example
    test_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Product Label</title>
    <style>
        .product { color: red; font-weight: bold; }
        .nutrition-table { border: 1px solid #000; }
    </style>
</head>
<body>
    <div class="product-name">Chocolate Chip Cookies</div>
    <div class="section-title">Nutrition Facts</div>
    <table class="nutrition-table">
        <tr>
            <td>Serving Size</td>
            <td>2 cookies (32g)</td>
        </tr>
        <tr>
            <td>Calories</td>
            <td>190</td>
        </tr>
        <tr>
            <td>Total Fat</td>
            <td>16g</td>
        </tr>
    </table>
    <div class="section-title">Ingredients:</div>
    <div class="ingredients">Flour, Sugar, Butter, Chocolate Chips</div>
    <div class="allergen"><strong>Contains:</strong> Wheat, Milk</div>
</body>
</html>"""
    
    print(f"\n{'=' * 50}")
    print("Testing HTML Translation to Hindi...")
    print("=" * 50)
    print(f"\nOriginal HTML:\n{test_html[:500]}...")
    
    try:
        translated_html = translator.translate_html_label(test_html, 'en-US', 'hi-IN')
        print(f"\nHindi HTML:\n{translated_html[:500]}...")
        
        # Verify structure is preserved
        if '<style>' in translated_html and '</style>' in translated_html:
            print("\n✓ Style tags preserved")
        else:
            print("\n✗ Style tags missing!")
            
        if '<table' in translated_html and '</table>' in translated_html:
            print("✓ Table structure preserved")
        else:
            print("✗ Table structure missing!")
            
        if 'lang="hi-IN"' in translated_html:
            print("✓ Language attribute updated")
        else:
            print("✗ Language attribute not updated")
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()