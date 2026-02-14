#!/bin/bash
# Deployment script for SAP BTP Cloud Foundry

echo "=========================================="
echo "SAP BTP Cloud Foundry Deployment"
echo "Food Label Generator API"
echo "=========================================="

# Check if cf CLI is installed
if ! command -v cf &> /dev/null; then
    echo "❌ Error: Cloud Foundry CLI not found"
    echo "Please install: https://docs.cloudfoundry.org/cf-cli/install-go-cli.html"
    exit 1
fi

# Check if logged in
echo ""
echo "Checking CF login status..."
cf target

if [ $? -ne 0 ]; then
    echo "❌ Not logged in to Cloud Foundry"
    echo "Please run: cf login"
    exit 1
fi

# Copy requirements file
echo ""
echo "Preparing requirements..."
cp requirements-cf.txt requirements.txt

# Deploy application
echo ""
echo "Deploying application..."
cf push

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✅ Deployment successful!"
    echo "=========================================="
    echo ""
    echo "Application URL:"
    cf app label-generator-api | grep routes
    echo ""
    echo "To view logs:"
    echo "  cf logs label-generator-api --recent"
    echo ""
    echo "To check status:"
    echo "  cf app label-generator-api"
else
    echo ""
    echo "❌ Deployment failed"
    echo "Check logs with: cf logs label-generator-api --recent"
    exit 1
fi