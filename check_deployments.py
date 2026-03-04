"""List available SAP AI Core deployments using REST API"""
import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

# Get credentials
auth_url = os.getenv('SAP_AI_CORE_AUTH_URL')
client_id = os.getenv('SAP_AI_CORE_CLIENT_ID')
client_secret = os.getenv('SAP_AI_CORE_CLIENT_SECRET')
api_url = os.getenv('SAP_AI_CORE_API_URL')
current_deployment = os.getenv('SAP_AI_CORE_DEPLOYMENT_ID')

print("=" * 60)
print("SAP AI Core Deployment Checker")
print("=" * 60)
print(f"\nAPI URL: {api_url}")
print(f"Current Deployment ID: {current_deployment}")

# Get token
print("\n🔐 Getting access token...")
try:
    token_resp = requests.post(
        f'{auth_url}/oauth/token',
        data={
            'grant_type': 'client_credentials',
            'client_id': client_id,
            'client_secret': client_secret
        },
        timeout=10
    )
    token_resp.raise_for_status()
    token = token_resp.json()['access_token']
    print("✅ Token obtained!")
except Exception as e:
    print(f"❌ Token error: {e}")
    exit(1)

# List deployments
print("\n📋 Listing deployments...")
try:
    resp = requests.get(
        f'{api_url}/v2/lm/deployments',
        headers={
            'Authorization': f'Bearer {token}',
            'AI-Resource-Group': 'default'
        },
        timeout=15
    )
    print(f"Status: {resp.status_code}")
    
    if resp.status_code == 200:
        data = resp.json()
        deployments = data.get('resources', [])
        
        if deployments:
            print(f"\n✅ Found {len(deployments)} deployment(s):\n")
            for i, dep in enumerate(deployments, 1):
                dep_id = dep.get('id', 'N/A')
                status = dep.get('status', 'N/A')
                config = dep.get('configurationName', 'N/A')
                model = dep.get('details', {}).get('resources', {}).get('backend_details', {}).get('model', {}).get('name', 'N/A')
                
                print(f"{i}. Deployment ID: {dep_id}")
                print(f"   Status: {status}")
                print(f"   Configuration: {config}")
                print(f"   Model: {model}")
                
                if dep_id == current_deployment:
                    print("   ⭐ THIS IS YOUR CURRENT DEPLOYMENT")
                print()
        else:
            print("⚠️ No deployments found!")
            print("\nFull response:")
            print(json.dumps(data, indent=2)[:1000])
    else:
        print(f"❌ Error: {resp.status_code}")
        print(resp.text[:500])
        
except Exception as e:
    print(f"❌ Error listing deployments: {e}")

# Test current deployment
print("\n" + "=" * 60)
print("Testing current deployment...")
print("=" * 60)

try:
    test_resp = requests.post(
        f'{api_url}/v2/inference/deployments/{current_deployment}/chat/completions',
        headers={
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
            'AI-Resource-Group': 'default'
        },
        json={
            'messages': [{'role': 'user', 'content': 'Say hello'}],
            'max_tokens': 10
        },
        timeout=30
    )
    print(f"Status: {test_resp.status_code}")
    
    if test_resp.status_code == 200:
        print("✅ Deployment is working!")
        result = test_resp.json()
        content = result.get('choices', [{}])[0].get('message', {}).get('content', '')
        print(f"Response: {content}")
    else:
        print(f"❌ Deployment error: {test_resp.status_code}")
        print(test_resp.text[:300])
        
except Exception as e:
    print(f"❌ Test error: {e}")