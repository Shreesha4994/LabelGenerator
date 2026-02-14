# 🚀 Food Label Generator API

RESTful API service for generating compliant food labels for India (FSSAI), US (FDA/USDA), and EU (Regulation 1169/2011).

---

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [API Endpoints](#api-endpoints)
- [Request/Response Format](#requestresponse-format)
- [Examples](#examples)
- [Error Handling](#error-handling)
- [Deployment](#deployment)

---

## 🚀 Quick Start

### Installation

```bash
# Install dependencies
pip install -r api_requirements.txt

# Or if using virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r api_requirements.txt
```

### Run Development Server

```bash
# Simple start
python app.py

# With custom configuration
export FLASK_PORT=8000
export FLASK_DEBUG=True
python app.py

# Or using .env file
cp .env.example .env
# Edit .env with your settings
python app.py
```

Server will start at: **http://localhost:5000**

---

## 📡 API Endpoints

### Health Check

```
GET /api/health
```

Check if the API service is running.

**Response:**
```json
{
  "success": true,
  "status": "healthy",
  "service": "Food Label Generator API",
  "version": "1.0.0",
  "regions": ["india", "us", "eu"]
}
```

---

### Generate India Label (FSSAI)

```
POST /api/generate/india
```

Generate FSSAI compliant food label for India.

**Request Headers:**
```
Content-Type: application/json
```

**Request Body:** JSON with product data (see [India samples](india_dataset/))

**Success Response (200):**
```json
{
  "success": true,
  "html": "<html>...</html>",
  "product_name": "Chocolate Chip Cookies",
  "region": "india",
  "category": "packaged_processed_food"
}
```

**Validation Error (400):**
```json
{
  "success": false,
  "errors": [
    "FSSAI license must be exactly 14 digits",
    "Missing required nutrient: protein"
  ],
  "region": "india"
}
```

---

### Generate US Label (FDA/USDA)

```
POST /api/generate/us
```

Generate FDA/USDA compliant food label for US.

**Request Headers:**
```
Content-Type: application/json
```

**Request Body:** JSON with product data (see [US samples](us_dataset/))

**Success Response (200):**
```json
{
  "success": true,
  "html": "<html>...</html>",
  "product_name": "Organic Almond Butter",
  "region": "us",
  "category": "packaged_food"
}
```

---

### Generate EU Label (Regulation 1169/2011)

```
POST /api/generate/eu
```

Generate EU Regulation 1169/2011 compliant food label.

**Request Headers:**
```
Content-Type: application/json
```

**Request Body:** JSON with product data (see [EU samples](eu_dataset/))

**Success Response (200):**
```json
{
  "success": true,
  "html": "<html>...</html>",
  "product_name": "Organic Hazelnut Energy Bar",
  "region": "eu",
  "category": "packaged_food"
}
```

---

## 📝 Examples

### Using cURL

#### Health Check
```bash
curl http://localhost:5000/api/health
```

#### Generate India Label
```bash
curl -X POST http://localhost:5000/api/generate/india \
  -H "Content-Type: application/json" \
  -d @india_dataset/01_packaged_snack.json
```

#### Generate US Label
```bash
curl -X POST http://localhost:5000/api/generate/us \
  -H "Content-Type: application/json" \
  -d @us_dataset/01_packaged_food.json
```

#### Generate EU Label
```bash
curl -X POST http://localhost:5000/api/generate/eu \
  -H "Content-Type: application/json" \
  -d @eu_dataset/01_packaged_food.json
```

#### Save HTML to File
```bash
curl -X POST http://localhost:5000/api/generate/india \
  -H "Content-Type: application/json" \
  -d @india_dataset/01_packaged_snack.json \
  | jq -r '.html' > label.html
```

---

### Using Python

```python
import requests
import json

# API endpoint
url = "http://localhost:5000/api/generate/india"

# Load product data
with open('india_dataset/01_packaged_snack.json', 'r') as f:
    product_data = json.load(f)

# Make request
response = requests.post(url, json=product_data)

# Check response
if response.status_code == 200:
    result = response.json()
    html = result['html']
    
    # Save to file
    with open('label.html', 'w') as f:
        f.write(html)
    print(f"✓ Label generated: {result['product_name']}")
else:
    error = response.json()
    print(f"✗ Error: {error.get('errors', error.get('error'))}")
```

---

### Using JavaScript (Node.js)

```javascript
const fs = require('fs');
const axios = require('axios');

// API endpoint
const url = 'http://localhost:5000/api/generate/india';

// Load product data
const productData = JSON.parse(
  fs.readFileSync('india_dataset/01_packaged_snack.json', 'utf8')
);

// Make request
axios.post(url, productData)
  .then(response => {
    const { html, product_name } = response.data;
    
    // Save to file
    fs.writeFileSync('label.html', html);
    console.log(`✓ Label generated: ${product_name}`);
  })
  .catch(error => {
    const errors = error.response?.data?.errors || [error.message];
    console.error('✗ Error:', errors);
  });
```

---

### Using JavaScript (Browser/Fetch)

```javascript
// Load product data
const productData = {
  "product_name": "Chocolate Cookies",
  "category": "packaged_processed_food",
  "veg_status": "veg",
  // ... rest of the data
};

// Make request
fetch('http://localhost:5000/api/generate/india', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(productData)
})
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      // Display HTML in iframe or new window
      const iframe = document.createElement('iframe');
      iframe.srcdoc = data.html;
      document.body.appendChild(iframe);
    } else {
      console.error('Validation errors:', data.errors);
    }
  })
  .catch(error => console.error('Error:', error));
```

---

## ⚠️ Error Handling

### HTTP Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | Success | Label generated successfully |
| 400 | Bad Request | Validation errors or invalid JSON |
| 404 | Not Found | Endpoint doesn't exist |
| 405 | Method Not Allowed | Wrong HTTP method |
| 413 | Payload Too Large | Request body exceeds limit (16MB) |
| 500 | Internal Server Error | Server error |

### Error Response Format

```json
{
  "success": false,
  "error": "Error message",
  "errors": ["List of validation errors"],
  "region": "india"
}
```

### Common Errors

#### 1. Missing Content-Type Header
```json
{
  "success": false,
  "error": "Content-Type must be application/json"
}
```

**Solution:** Add header: `Content-Type: application/json`

#### 2. Empty Request Body
```json
{
  "success": false,
  "error": "Empty request body"
}
```

**Solution:** Include product data in request body

#### 3. Validation Errors
```json
{
  "success": false,
  "errors": [
    "FSSAI license must be exactly 14 digits",
    "veg_status must be 'veg' or 'non-veg'"
  ],
  "region": "india"
}
```

**Solution:** Fix data according to error messages. See [FIELD_GUIDE.md](FIELD_GUIDE.md) for field requirements.

---

## 🚀 Deployment

### Development Server

```bash
# Simple development server (not for production)
python app.py
```

### Production with Gunicorn

```bash
# Install gunicorn (included in api_requirements.txt)
pip install gunicorn

# Run with 4 workers
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# With timeout and logging
gunicorn -w 4 -b 0.0.0.0:5000 \
  --timeout 30 \
  --access-logfile - \
  --error-logfile - \
  app:app
```

### Using Environment Variables

```bash
# Set configuration
export FLASK_HOST=0.0.0.0
export FLASK_PORT=8000
export CORS_ORIGINS=https://example.com,https://app.example.com

# Run
python app.py
```

### Docker Deployment

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copy requirements
COPY api_requirements.txt .
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r api_requirements.txt -r requirements.txt

# Copy application files
COPY . .

# Expose port
EXPOSE 5000

# Run with gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

Build and run:

```bash
# Build image
docker build -t label-generator-api .

# Run container
docker run -p 5000:5000 label-generator-api
```

### Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_HOST=0.0.0.0
      - FLASK_PORT=5000
      - CORS_ORIGINS=*
    restart: unless-stopped
```

Run:

```bash
docker-compose up -d
```

---

## 🔧 Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `FLASK_HOST` | `0.0.0.0` | Server host |
| `FLASK_PORT` | `5000` | Server port |
| `FLASK_DEBUG` | `False` | Debug mode |
| `CORS_ORIGINS` | `*` | Allowed CORS origins |
| `MAX_CONTENT_LENGTH` | `16777216` | Max request size (bytes) |

### CORS Configuration

```python
# Allow all origins (development)
CORS_ORIGINS=*

# Allow specific origins (production)
CORS_ORIGINS=https://example.com,https://app.example.com
```

---

## 📊 Performance

### Benchmarks

Typical response times (on standard hardware):

- Health check: < 5ms
- India label generation: 50-100ms
- US label generation: 50-100ms
- EU label generation: 50-100ms

### Optimization Tips

1. **Use Gunicorn** with multiple workers for production
2. **Enable caching** for template loading
3. **Use CDN** for serving generated HTML
4. **Rate limiting** to prevent abuse
5. **Load balancing** for high traffic

---

## 🔒 Security

### Best Practices

1. **CORS**: Configure specific origins in production
2. **HTTPS**: Use SSL/TLS in production
3. **Rate Limiting**: Implement rate limiting
4. **Input Validation**: Already built-in
5. **Size Limits**: Max 16MB request size

### Production Checklist

- [ ] Set `FLASK_DEBUG=False`
- [ ] Configure specific `CORS_ORIGINS`
- [ ] Use HTTPS/SSL
- [ ] Implement rate limiting
- [ ] Set up monitoring/logging
- [ ] Use environment variables for secrets
- [ ] Run with Gunicorn (not Flask dev server)

---

## 📞 Support

- **Documentation**: [FIELD_GUIDE.md](FIELD_GUIDE.md)
- **Samples**: [india_dataset/](india_dataset/), [us_dataset/](us_dataset/), [eu_dataset/](eu_dataset/)
- **Issues**: Report bugs or request features

---

## 📄 License

This API service is part of the Food Label Generator project.

---

**Made with ❤️ for Food Industry Compliance**