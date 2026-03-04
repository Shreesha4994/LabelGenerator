#!/usr/bin/env python3
"""
Flask API Service for Food Label Generation
Supports India (FSSAI), US (FDA/USDA), and EU (Regulation 1169/2011)
With Translation Support via SAP Translation Hub
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys
from pathlib import Path

# Import label generators
from label_generator import IndiaLabelGenerator, FSSAIValidator
from label_generator_us import USLabelGenerator, FDAValidator
from label_generator_eu import EULabelGenerator, EUValidator
from ai_label_front_generator import AIFrontLabelGenerator
from label_translator import LabelTranslator

app = Flask(__name__)

# Enable CORS for all routes
CORS(app, resources={
    r"/api/*": {
        "origins": os.getenv("CORS_ORIGINS", "*"),
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Configuration
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv("MAX_CONTENT_LENGTH", 16 * 1024 * 1024))  # 16MB default
app.config['JSON_SORT_KEYS'] = False


# Initialize translator
translator = LabelTranslator()


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "success": True,
        "status": "healthy",
        "service": "Food Label Generator API",
        "version": "1.1.0",
        "regions": ["india", "us", "eu"],
        "features": ["label_generation", "translation"],
        "supported_languages": list(translator.get_supported_languages().keys())
    }), 200


@app.route('/api/languages', methods=['GET'])
def get_supported_languages():
    """Get list of supported translation languages"""
    return jsonify({
        "success": True,
        "languages": translator.get_supported_languages(),
        "source_language": "en-US",
        "usage": "Pass 'translate': true and 'target_language': '<code>' in your request"
    }), 200


@app.route('/api/generate/india', methods=['POST'])
def generate_india_label():
    """
    Generate FSSAI compliant label for India
    
    Request Body: JSON with product data
    Returns: JSON with HTML label or validation errors
    """
    try:
        # Get JSON data from request
        if not request.is_json:
            return jsonify({
                "success": False,
                "error": "Content-Type must be application/json"
            }), 400
        
        product_data = request.get_json()
        
        if not product_data:
            return jsonify({
                "success": False,
                "error": "Empty request body"
            }), 400
        
        # Validate data
        is_valid, errors = FSSAIValidator.validate(product_data)
        
        if not is_valid:
            return jsonify({
                "success": False,
                "errors": errors,
                "region": "india"
            }), 400
        
        # Generate AI front label
        ai_generator = AIFrontLabelGenerator(country='india')
        front_html = ai_generator.generate_front_label(product_data)
        
        # Generate template back label
        back_generator = IndiaLabelGenerator()
        back_html = back_generator.generate(product_data)
        
        # Check if translation is requested
        translate = product_data.get("translate", False)
        target_language = product_data.get("target_language", "hi-IN")
        
        response_data = {
            "success": True,
            "front_label_html": front_html,
            "back_label_html": back_html,
            "product_name": product_data.get("product_name", "Unknown"),
            "region": "india",
            "category": product_data.get("category", "Unknown")
        }
        
        # Translate if requested
        if translate:
            if not translator.is_language_supported(target_language):
                return jsonify({
                    "success": False,
                    "error": f"Unsupported language: {target_language}",
                    "supported_languages": list(translator.get_supported_languages().keys())
                }), 400
            
            try:
                translated_front = translator.translate_html_label(front_html, 'en-US', target_language)
                translated_back = translator.translate_html_label(back_html, 'en-US', target_language)
                
                response_data["translated_front_label_html"] = translated_front
                response_data["translated_back_label_html"] = translated_back
                response_data["translation_language"] = target_language
                response_data["translation_language_name"] = translator.get_supported_languages().get(target_language)
            except Exception as e:
                app.logger.error(f"Translation error: {str(e)}")
                response_data["translation_error"] = str(e)
        
        return jsonify(response_data), 200
        
    except ValueError as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "region": "india"
        }), 400
        
    except Exception as e:
        app.logger.error(f"Error generating India label: {str(e)}")
        return jsonify({
            "success": False,
            "error": "Internal server error",
            "details": str(e) if app.debug else None
        }), 500


@app.route('/api/generate/us', methods=['POST'])
def generate_us_label():
    """
    Generate FDA/USDA compliant label for US
    
    Request Body: JSON with product data
    Returns: JSON with HTML label or validation errors
    """
    try:
        # Get JSON data from request
        if not request.is_json:
            return jsonify({
                "success": False,
                "error": "Content-Type must be application/json"
            }), 400
        
        product_data = request.get_json()
        
        if not product_data:
            return jsonify({
                "success": False,
                "error": "Empty request body"
            }), 400
        
        # Validate data
        is_valid, errors = FDAValidator.validate(product_data)
        
        if not is_valid:
            return jsonify({
                "success": False,
                "errors": errors,
                "region": "us"
            }), 400
        
        # Generate AI front label
        ai_generator = AIFrontLabelGenerator(country='us')
        front_html = ai_generator.generate_front_label(product_data)
        
        # Generate template back label
        back_generator = USLabelGenerator()
        back_html = back_generator.generate(product_data)
        
        # Check if translation is requested
        translate = product_data.get("translate", False)
        target_language = product_data.get("target_language", "es-ES")
        
        response_data = {
            "success": True,
            "front_label_html": front_html,
            "back_label_html": back_html,
            "product_name": product_data.get("product_name", "Unknown"),
            "region": "us",
            "category": product_data.get("category", "Unknown")
        }
        
        # Translate if requested
        if translate:
            if not translator.is_language_supported(target_language):
                return jsonify({
                    "success": False,
                    "error": f"Unsupported language: {target_language}",
                    "supported_languages": list(translator.get_supported_languages().keys())
                }), 400
            
            try:
                translated_front = translator.translate_html_label(front_html, 'en-US', target_language)
                translated_back = translator.translate_html_label(back_html, 'en-US', target_language)
                
                response_data["translated_front_label_html"] = translated_front
                response_data["translated_back_label_html"] = translated_back
                response_data["translation_language"] = target_language
                response_data["translation_language_name"] = translator.get_supported_languages().get(target_language)
            except Exception as e:
                app.logger.error(f"Translation error: {str(e)}")
                response_data["translation_error"] = str(e)
        
        return jsonify(response_data), 200
        
    except ValueError as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "region": "us"
        }), 400
        
    except Exception as e:
        app.logger.error(f"Error generating US label: {str(e)}")
        return jsonify({
            "success": False,
            "error": "Internal server error",
            "details": str(e) if app.debug else None
        }), 500


@app.route('/api/generate/eu', methods=['POST'])
def generate_eu_label():
    """
    Generate EU Regulation 1169/2011 compliant label
    
    Request Body: JSON with product data
    Returns: JSON with HTML label or validation errors
    """
    try:
        # Get JSON data from request
        if not request.is_json:
            return jsonify({
                "success": False,
                "error": "Content-Type must be application/json"
            }), 400
        
        product_data = request.get_json()
        
        if not product_data:
            return jsonify({
                "success": False,
                "error": "Empty request body"
            }), 400
        
        # Validate data
        is_valid, errors = EUValidator.validate(product_data)
        
        if not is_valid:
            return jsonify({
                "success": False,
                "errors": errors,
                "region": "eu"
            }), 400
        
        # Generate AI front label
        ai_generator = AIFrontLabelGenerator(country='eu')
        front_html = ai_generator.generate_front_label(product_data)
        
        # Generate template back label
        back_generator = EULabelGenerator()
        back_html = back_generator.generate(product_data)
        
        # Check if translation is requested
        translate = product_data.get("translate", False)
        target_language = product_data.get("target_language", "de-DE")
        
        response_data = {
            "success": True,
            "front_label_html": front_html,
            "back_label_html": back_html,
            "product_name": product_data.get("product_name", "Unknown"),
            "region": "eu",
            "category": product_data.get("category", "Unknown")
        }
        
        # Translate if requested
        if translate:
            if not translator.is_language_supported(target_language):
                return jsonify({
                    "success": False,
                    "error": f"Unsupported language: {target_language}",
                    "supported_languages": list(translator.get_supported_languages().keys())
                }), 400
            
            try:
                translated_front = translator.translate_html_label(front_html, 'en-US', target_language)
                translated_back = translator.translate_html_label(back_html, 'en-US', target_language)
                
                response_data["translated_front_label_html"] = translated_front
                response_data["translated_back_label_html"] = translated_back
                response_data["translation_language"] = target_language
                response_data["translation_language_name"] = translator.get_supported_languages().get(target_language)
            except Exception as e:
                app.logger.error(f"Translation error: {str(e)}")
                response_data["translation_error"] = str(e)
        
        return jsonify(response_data), 200
        
    except ValueError as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "region": "eu"
        }), 400
        
    except Exception as e:
        app.logger.error(f"Error generating EU label: {str(e)}")
        return jsonify({
            "success": False,
            "error": "Internal server error",
            "details": str(e) if app.debug else None
        }), 500


@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle request too large error"""
    return jsonify({
        "success": False,
        "error": "Request payload too large",
        "max_size": f"{app.config['MAX_CONTENT_LENGTH'] / (1024 * 1024)}MB"
    }), 413


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        "success": False,
        "error": "Endpoint not found",
        "available_endpoints": [
            "GET /api/health",
            "GET /api/languages",
            "POST /api/generate/india",
            "POST /api/generate/us",
            "POST /api/generate/eu"
        ]
    }), 404


@app.errorhandler(405)
def method_not_allowed(error):
    """Handle method not allowed errors"""
    return jsonify({
        "success": False,
        "error": "Method not allowed"
    }), 405


@app.errorhandler(500)
def internal_server_error(error):
    """Handle internal server errors"""
    app.logger.error(f"Internal server error: {str(error)}")
    return jsonify({
        "success": False,
        "error": "Internal server error"
    }), 500


if __name__ == '__main__':
    # Configuration from environment variables
    host = os.getenv("FLASK_HOST", "0.0.0.0")
    port = int(os.getenv("FLASK_PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    
    print(f"""
╔══════════════════════════════════════════════════════════╗
║   Food Label Generator API Service                       ║
║   Version: 1.1.0 (with Translation Support)              ║
╠══════════════════════════════════════════════════════════╣
║   Server: http://{host}:{port}                      ║
║   Health: http://{host}:{port}/api/health           ║
╠══════════════════════════════════════════════════════════╣
║   Endpoints:                                             ║
║   • GET  /api/languages       (Supported languages)     ║
║   • POST /api/generate/india  (FSSAI)                   ║
║   • POST /api/generate/us     (FDA/USDA)                ║
║   • POST /api/generate/eu     (EU Reg 1169/2011)        ║
╠══════════════════════════════════════════════════════════╣
║   Translation: Add "translate": true and                 ║
║   "target_language": "de-DE" to your request            ║
╚══════════════════════════════════════════════════════════╝
    """)
    
    app.run(host=host, port=port, debug=debug)