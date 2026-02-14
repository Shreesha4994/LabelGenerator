# 🚀 SAP BTP Cloud Foundry Deployment Guide

Complete guide for deploying the Food Label Generator API to SAP BTP Cloud Foundry.

---

## 📋 Prerequisites

1. **SAP BTP Account** with Cloud Foundry environment
2. **Cloud Foundry CLI** installed
   ```bash
   # Check if installed
   cf --version
   
   # Install if needed (macOS)
   brew install cloudfoundry/tap/cf-cli
   ```

3. **Access to your BTP subaccount**
   - API Endpoint: `https://api.cf.eu11.hana.ondemand.com`
   - Organization: Your org name
   - Space: Your space name

---

## 🎯 Deployment Files Created

All necessary files for SAP BTP deployment have been created:

| File | Purpose |
|------|---------|
| `manifest.yml` | Cloud Foundry app configuration |
| `runtime.txt` | Python version specification |
| `Procfile` | Process type definition |
| `.cfignore` | Files to exclude from deployment |
| `requirements-cf.txt` | Python dependencies |
| `deploy-to-btp.sh` | Automated deployment script |

---

## 🚀 Quick Deployment (Automated)

### Step 1: Login to Cloud Foundry

```bash
# Login to SAP BTP CF
cf login -a https://api.cf.eu11.hana.ondemand.com

# Enter your credentials when prompted
# Select your org and space
```

### Step 2: Run Deployment Script

```bash
# Make script executable
chmod +x deploy-to-btp.sh

# Run deployment
./deploy-to-btp.sh
```

The script will:
- ✅ Check CF CLI installation
- ✅ Verify login status
- ✅ Copy requirements file
- ✅ Deploy application
- ✅ Show application URL

---

## 📝 Manual Deployment (Step-by-Step)

### Step 1: Login to Cloud Foundry

```bash
cf login -a https://api.cf.eu11.hana.ondemand.com
```

**Enter:**
- Email: your-email@sap.com
- Password: your-password
- Org: AI-POC-CPR_test-nbhfe3tt (or your org)
- Space: db (or your space)

### Step 2: Verify Target

```bash
cf target
```

**Expected output:**
```
API endpoint:   https://api.cf.eu11.hana.ondemand.com
API version:    3.209.0
user:           your-email@sap.com
org:            AI-POC-CPR_test-nbhfe3tt
space:          db
```

### Step 3: Prepare Requirements

```bash
# Copy CF requirements to requirements.txt
cp requirements-cf.txt requirements.txt
```

### Step 4: Deploy Application

```bash
# Deploy using manifest.yml
cf push
```

**This will:**
1. Upload application files
2. Install Python buildpack
3. Install dependencies from requirements.txt
4. Start application with Gunicorn
5. Run health check on `/api/health`
6. Assign route

### Step 5: Verify Deployment

```bash
# Check app status
cf app label-generator-api

# View recent logs
cf logs label-generator-api --recent

# Stream live logs
cf logs label-generator-api
```

---

## 🔧 Configuration

### Application Settings (manifest.yml)

```yaml
applications:
- name: label-generator-api
  memory: 512M              # Memory allocation
  disk_quota: 1G           # Disk space
  instances: 1             # Number of instances
  buildpacks:
    - python_buildpack
  command: gunicorn -w 4 -b 0.0.0.0:$PORT --timeout 60 app:app
  health-check-type: http
  health-check-http-endpoint: /api/health
  env:
    FLASK_HOST: 0.0.0.0
    FLASK_DEBUG: false
    CORS_ORIGINS: "*"
    MAX_CONTENT_LENGTH: "16777216"
  routes:
    - route: label-generator-api.cfapps.eu11.hana.ondemand.com
```

### Environment Variables

Set additional environment variables:

```bash
# Set environment variable
cf set-env label-generator-api CORS_ORIGINS "https://example.com"

# Restart app to apply changes
cf restart label-generator-api
```

---

## 📊 Scaling

### Scale Instances

```bash
# Scale to 2 instances
cf scale label-generator-api -i 2

# Scale memory
cf scale label-generator-api -m 1G

# Scale disk
cf scale label-generator-api -k 2G
```

### Auto-Scaling (Optional)

Install App Autoscaler service:

```bash
# Create autoscaler service
cf create-service autoscaler standard label-api-autoscaler

# Bind to app
cf bind-service label-generator-api label-api-autoscaler

# Restage app
cf restage label-generator-api
```

---

## 🧪 Testing Deployed Application

### Get Application URL

```bash
cf app label-generator-api
```

Look for the `routes:` line, e.g.:
```
routes: label-generator-api.cfapps.eu11.hana.ondemand.com
```

### Test Endpoints

```bash
# Set your app URL
APP_URL="https://label-generator-api.cfapps.eu11.hana.ondemand.com"

# Health check
curl $APP_URL/api/health

# Generate India label
curl -X POST $APP_URL/api/generate/india \
  -H "Content-Type: application/json" \
  -d @india_dataset/01_packaged_snack.json

# Generate US label
curl -X POST $APP_URL/api/generate/us \
  -H "Content-Type: application/json" \
  -d @us_dataset/01_packaged_food.json

# Generate EU label
curl -X POST $APP_URL/api/generate/eu \
  -H "Content-Type: application/json" \
  -d @eu_dataset/01_packaged_food.json
```

---

## 🔍 Monitoring & Logs

### View Logs

```bash
# Recent logs
cf logs label-generator-api --recent

# Stream live logs
cf logs label-generator-api

# Filter logs
cf logs label-generator-api --recent | grep ERROR
```

### Check App Health

```bash
# App status
cf app label-generator-api

# App events
cf events label-generator-api

# App environment
cf env label-generator-api
```

### Access Metrics

```bash
# Install CF metrics plugin (if not installed)
cf install-plugin -r CF-Community "log-cache"

# View metrics
cf tail label-generator-api
```

---

## 🔄 Updates & Redeployment

### Update Application

```bash
# Make your code changes, then:
cf push

# Or with zero-downtime (blue-green deployment)
cf push label-generator-api-new
cf map-route label-generator-api-new cfapps.eu11.hana.ondemand.com --hostname label-generator-api
cf unmap-route label-generator-api cfapps.eu11.hana.ondemand.com --hostname label-generator-api
cf delete label-generator-api -f
cf rename label-generator-api-new label-generator-api
```

### Restart Application

```bash
# Restart (keeps same container)
cf restart label-generator-api

# Restage (rebuilds container)
cf restage label-generator-api
```

---

## 🛑 Stop & Delete

### Stop Application

```bash
# Stop app (keeps it deployed)
cf stop label-generator-api

# Start again
cf start label-generator-api
```

### Delete Application

```bash
# Delete app completely
cf delete label-generator-api

# Delete with force (no confirmation)
cf delete label-generator-api -f
```

---

## 🔒 Security Best Practices

### 1. Configure CORS

```bash
# Set specific origins (production)
cf set-env label-generator-api CORS_ORIGINS "https://yourdomain.com,https://app.yourdomain.com"
cf restart label-generator-api
```

### 2. Enable HTTPS Only

The app is automatically served over HTTPS on SAP BTP.

### 3. Set Up Custom Domain (Optional)

```bash
# Map custom domain
cf map-route label-generator-api yourdomain.com --hostname api

# Requires domain verification in SAP BTP cockpit
```

### 4. Implement Rate Limiting

Consider adding rate limiting middleware or using SAP API Management.

---

## 📊 Resource Requirements

### Minimum Requirements

- **Memory**: 512MB
- **Disk**: 1GB
- **Instances**: 1

### Recommended for Production

- **Memory**: 1GB
- **Disk**: 2GB
- **Instances**: 2-4 (for high availability)

### Cost Estimation

Check SAP BTP pricing calculator:
https://www.sap.com/products/technology-platform/pricing.html

---

## 🐛 Troubleshooting

### App Won't Start

```bash
# Check logs
cf logs label-generator-api --recent

# Common issues:
# 1. Missing dependencies - check requirements.txt
# 2. Port binding - ensure using $PORT variable
# 3. Health check failing - verify /api/health endpoint
```

### Out of Memory

```bash
# Increase memory
cf scale label-generator-api -m 1G
```

### Slow Response Times

```bash
# Scale instances
cf scale label-generator-api -i 2

# Or increase workers in Procfile
# Edit: gunicorn -w 8 ...
```

### Health Check Failing

```bash
# Check health endpoint
curl https://label-generator-api.cfapps.eu11.hana.ondemand.com/api/health

# Increase health check timeout in manifest.yml
# Add: timeout: 180
```

---

## 📞 Support & Resources

### SAP BTP Documentation
- [Cloud Foundry on SAP BTP](https://help.sap.com/docs/btp/sap-business-technology-platform/cloud-foundry-environment)
- [Python Buildpack](https://docs.cloudfoundry.org/buildpacks/python/)

### CF CLI Documentation
- [CF CLI Reference](https://cli.cloudfoundry.org/en-US/v8/)
- [CF CLI Cheat Sheet](https://github.com/cloudfoundry/cli/wiki/CF-CLI-Cheat-Sheet)

### Application Documentation
- API Documentation: `API_README.md`
- Field Guide: `FIELD_GUIDE.md`
- Sample Data: `india_dataset/`, `us_dataset/`, `eu_dataset/`

---

## ✅ Deployment Checklist

Before deploying to production:

- [ ] Test application locally
- [ ] Update CORS_ORIGINS for production domains
- [ ] Set FLASK_DEBUG to false
- [ ] Configure appropriate memory/disk
- [ ] Set up monitoring and alerts
- [ ] Configure custom domain (if needed)
- [ ] Test all API endpoints
- [ ] Set up backup/disaster recovery plan
- [ ] Document deployment process
- [ ] Train team on CF commands

---

## 🎉 Success!

Once deployed, your API will be available at:

**https://label-generator-api.cfapps.eu11.hana.ondemand.com**

Test it:
```bash
curl https://label-generator-api.cfapps.eu11.hana.ondemand.com/api/health
```

Expected response:
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

**Made with ❤️ for SAP BTP**