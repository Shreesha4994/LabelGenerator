#!/usr/bin/env python3
"""
Flask API Service for Food Label Generation
Supports India (FSSAI), US (FDA/USDA), and EU (Regulation 1169/2011)
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


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "success": True,
        "status": "healthy",
        "service": "Food Label Generator API",
        "version": "1.0.0",
        "regions": ["india", "us", "eu"]
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
        
        # Generate label
        generator = IndiaLabelGenerator()
        html = generator.generate(product_data)
        
        return jsonify({
            "success": True,
            "html": html,
            "product_name": product_data.get("product_name", "Unknown"),
            "region": "india",
            "category": product_data.get("category", "Unknown")
        }), 200
        
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
        
        # Generate label
        generator = USLabelGenerator()
        html = generator.generate(product_data)
        
        return jsonify({
            "success": True,
            "html": html,
            "product_name": product_data.get("product_name", "Unknown"),
            "region": "us",
            "category": product_data.get("category", "Unknown")
        }), 200
        
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
        
        # Generate label
        generator = EULabelGenerator()
        html = generator.generate(product_data)
        
        return jsonify({
            "success": True,
            "html": html,
            "product_name": product_data.get("product_name", "Unknown"),
            "region": "eu",
            "category": product_data.get("category", "Unknown")
        }), 200
        
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
║   Version: 1.0.0                                         ║
╠══════════════════════════════════════════════════════════╣
║   Server: http://{host}:{port}                      ║
║   Health: http://{host}:{port}/api/health           ║
╠══════════════════════════════════════════════════════════╣
║   Endpoints:                                             ║
║   • POST /api/generate/india  (FSSAI)                   ║
║   • POST /api/generate/us     (FDA/USDA)                ║
║   • POST /api/generate/eu     (EU Reg 1169/2011)        ║
╚══════════════════════════════════════════════════════════╝
    """)
    
    app.run(host=host, port=port, debug=debug)