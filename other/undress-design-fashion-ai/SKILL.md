---
name: undress-design-fashion-ai
description: AI-powered fashion visualization and virtual try-on toolkit for consent-based garment editing and creative design workflows
triggers:
  - "integrate undress design API"
  - "use undress.design for virtual try-on"
  - "generate fashion visualizations with AI"
  - "implement garment replacement with undress design"
  - "add virtual styling to my app"
  - "create outfit variations using undress design"
  - "build consent-based fashion editing"
  - "integrate AI fashion visualization"
---

# Undress Design Fashion AI Skill

> Skill by [ara.so](https://ara.so) — Design Skills collection

## Overview

Undress Design is an AI-powered fashion visualization platform for consent-based garment editing, virtual try-on experiences, outfit prototyping, and creative design workflows. It provides API-driven tools for clothing segmentation, garment replacement, style variations, and fashion concept generation.

**Key capabilities:**
- Virtual garment visualization and try-on
- Outfit and style variations
- Fashion concept prototyping
- Clothing segmentation and masking
- Design reference generation
- Consent-based image editing workflows

**Official platform:** https://undress.design/edit

## Installation

### Web Platform Access

Access the platform directly through the web interface:

```bash
# Open in browser
https://undress.design/edit
```

### API Integration

For programmatic access, integrate via HTTP API:

```javascript
// Node.js example
const UNDRESS_API_KEY = process.env.UNDRESS_API_KEY;
const UNDRESS_API_URL = 'https://api.undress.design/v1';
```

```python
# Python example
import os

UNDRESS_API_KEY = os.environ.get('UNDRESS_API_KEY')
UNDRESS_API_URL = 'https://api.undress.design/v1'
```

### Environment Variables

Set up required credentials:

```bash
# .env file
UNDRESS_API_KEY=your_api_key_here
UNDRESS_API_URL=https://api.undress.design/v1
```

## Core API Operations

### Authentication

All API requests require authentication via API key:

```javascript
// JavaScript/Node.js
const axios = require('axios');

const client = axios.create({
  baseURL: process.env.UNDRESS_API_URL,
  headers: {
    'Authorization': `Bearer ${process.env.UNDRESS_API_KEY}`,
    'Content-Type': 'application/json'
  }
});
```

```python
# Python
import requests

class UndressClient:
    def __init__(self, api_key, base_url):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
    
    def request(self, method, endpoint, **kwargs):
        url = f"{self.base_url}/{endpoint}"
        return requests.request(method, url, headers=self.headers, **kwargs)

client = UndressClient(
    api_key=os.environ.get('UNDRESS_API_KEY'),
    base_url=os.environ.get('UNDRESS_API_URL')
)
```

### Virtual Try-On

Generate virtual try-on visualizations:

```javascript
// JavaScript example
async function virtualTryOn(imageData, garmentData, options = {}) {
  try {
    const response = await client.post('/virtual-tryon', {
      source_image: imageData, // base64 or URL
      garment_image: garmentData, // base64 or URL
      style: options.style || 'realistic',
      preserve_details: options.preserveDetails || true,
      consent_verified: true // Required
    });
    
    return response.data;
  } catch (error) {
    console.error('Virtual try-on failed:', error.response?.data || error.message);
    throw error;
  }
}

// Usage
const result = await virtualTryOn(
  'https://example.com/person.jpg',
  'https://example.com/dress.jpg',
  { style: 'realistic', preserveDetails: true }
);

console.log('Generated image:', result.output_url);
```

```python
# Python example
def virtual_tryon(image_data, garment_data, **options):
    """Generate virtual try-on visualization"""
    payload = {
        'source_image': image_data,  # base64 or URL
        'garment_image': garment_data,  # base64 or URL
        'style': options.get('style', 'realistic'),
        'preserve_details': options.get('preserve_details', True),
        'consent_verified': True  # Required
    }
    
    response = client.request('POST', 'virtual-tryon', json=payload)
    response.raise_for_status()
    return response.json()

# Usage
result = virtual_tryon(
    'https://example.com/person.jpg',
    'https://example.com/dress.jpg',
    style='realistic'
)

print(f"Generated image: {result['output_url']}")
```

### Garment Replacement

Replace specific garments in an image:

```javascript
// JavaScript
async function replaceGarment(sourceImage, targetGarment, region) {
  const response = await client.post('/garment-replace', {
    source_image: sourceImage,
    target_garment: targetGarment,
    region: region, // 'top', 'bottom', 'full', 'accessories'
    blend_mode: 'seamless',
    consent_verified: true
  });
  
  return response.data;
}

// Usage
const replaced = await replaceGarment(
  './images/model.jpg',
  './images/shirt.jpg',
  'top'
);
```

```python
# Python
def replace_garment(source_image, target_garment, region):
    """Replace specific garment in image"""
    payload = {
        'source_image': source_image,
        'target_garment': target_garment,
        'region': region,  # 'top', 'bottom', 'full', 'accessories'
        'blend_mode': 'seamless',
        'consent_verified': True
    }
    
    response = client.request('POST', 'garment-replace', json=payload)
    return response.json()

# Usage
replaced = replace_garment(
    './images/model.jpg',
    './images/shirt.jpg',
    'top'
)
```

### Style Variations

Generate outfit variations and style alternatives:

```javascript
// JavaScript
async function generateStyleVariations(baseImage, count = 4) {
  const response = await client.post('/style-variations', {
    base_image: baseImage,
    variation_count: count,
    preserve_pose: true,
    style_range: 'moderate', // 'subtle', 'moderate', 'bold'
    consent_verified: true
  });
  
  return response.data.variations;
}

// Usage
const variations = await generateStyleVariations('./base-outfit.jpg', 6);
variations.forEach((variant, idx) => {
  console.log(`Variation ${idx + 1}: ${variant.url}`);
});
```

```python
# Python
def generate_style_variations(base_image, count=4):
    """Generate outfit variations"""
    payload = {
        'base_image': base_image,
        'variation_count': count,
        'preserve_pose': True,
        'style_range': 'moderate',  # 'subtle', 'moderate', 'bold'
        'consent_verified': True
    }
    
    response = client.request('POST', 'style-variations', json=payload)
    return response.json()['variations']

# Usage
variations = generate_style_variations('./base-outfit.jpg', count=6)
for idx, variant in enumerate(variations, 1):
    print(f"Variation {idx}: {variant['url']}")
```

### Clothing Segmentation

Segment and mask garments in images:

```javascript
// JavaScript
async function segmentClothing(image) {
  const response = await client.post('/segment', {
    image: image,
    return_masks: true,
    categories: ['top', 'bottom', 'dress', 'outerwear', 'accessories']
  });
  
  return response.data.segments;
}

// Usage
const segments = await segmentClothing('./photo.jpg');
segments.forEach(segment => {
  console.log(`Found ${segment.category}: confidence ${segment.confidence}`);
  console.log(`Mask URL: ${segment.mask_url}`);
});
```

```python
# Python
def segment_clothing(image):
    """Segment and identify garments"""
    payload = {
        'image': image,
        'return_masks': True,
        'categories': ['top', 'bottom', 'dress', 'outerwear', 'accessories']
    }
    
    response = client.request('POST', 'segment', json=payload)
    return response.json()['segments']

# Usage
segments = segment_clothing('./photo.jpg')
for segment in segments:
    print(f"Found {segment['category']}: confidence {segment['confidence']}")
    print(f"Mask URL: {segment['mask_url']}")
```

## Common Patterns

### E-commerce Virtual Try-On Integration

```javascript
// JavaScript - E-commerce integration
class FashionVisualization {
  constructor(apiKey) {
    this.client = axios.create({
      baseURL: process.env.UNDRESS_API_URL,
      headers: { 'Authorization': `Bearer ${apiKey}` }
    });
  }
  
  async customerTryOn(customerPhoto, productId) {
    // Verify consent
    if (!this.verifyConsent(customerPhoto)) {
      throw new Error('Customer consent required');
    }
    
    // Fetch product image
    const productImage = await this.getProductImage(productId);
    
    // Generate try-on
    const result = await this.client.post('/virtual-tryon', {
      source_image: customerPhoto,
      garment_image: productImage,
      style: 'photorealistic',
      consent_verified: true
    });
    
    return result.data.output_url;
  }
  
  verifyConsent(photo) {
    // Implement consent verification logic
    return photo.consent_token !== undefined;
  }
  
  async getProductImage(productId) {
    // Fetch from product catalog
    return `https://cdn.example.com/products/${productId}.jpg`;
  }
}

// Usage
const fashion = new FashionVisualization(process.env.UNDRESS_API_KEY);
const tryOnUrl = await fashion.customerTryOn(
  { url: userPhoto, consent_token: '...' },
  'PROD-12345'
);
```

### Batch Processing for Design Catalogs

```python
# Python - Batch processing
import asyncio
from typing import List

class FashionCatalogProcessor:
    def __init__(self, api_key):
        self.client = UndressClient(api_key, os.environ.get('UNDRESS_API_URL'))
    
    async def process_catalog(self, model_image: str, garment_urls: List[str]):
        """Process entire catalog with single model"""
        results = []
        
        for garment_url in garment_urls:
            try:
                result = self.client.request('POST', 'virtual-tryon', json={
                    'source_image': model_image,
                    'garment_image': garment_url,
                    'style': 'catalog',
                    'consent_verified': True
                })
                results.append(result.json())
            except Exception as e:
                print(f"Failed for {garment_url}: {e}")
                results.append(None)
        
        return results
    
    def save_results(self, results, output_dir):
        """Save generated images"""
        import os
        from urllib.request import urlretrieve
        
        os.makedirs(output_dir, exist_ok=True)
        
        for idx, result in enumerate(results):
            if result:
                filename = f"{output_dir}/tryon_{idx:03d}.jpg"
                urlretrieve(result['output_url'], filename)
                print(f"Saved: {filename}")

# Usage
processor = FashionCatalogProcessor(os.environ.get('UNDRESS_API_KEY'))
garments = [
    'https://cdn.example.com/dress1.jpg',
    'https://cdn.example.com/dress2.jpg',
    'https://cdn.example.com/shirt1.jpg'
]

results = processor.process_catalog('./model.jpg', garments)
processor.save_results(results, './output')
```

### Consent Management System

```javascript
// JavaScript - Consent workflow
class ConsentManager {
  constructor() {
    this.consentRecords = new Map();
  }
  
  async requestConsent(userId, imageId, purpose) {
    // Generate consent request
    const consentId = `consent_${Date.now()}_${Math.random().toString(36)}`;
    
    const record = {
      userId,
      imageId,
      purpose,
      requestedAt: new Date(),
      status: 'pending',
      consentId
    };
    
    this.consentRecords.set(consentId, record);
    
    // Send to user for approval
    await this.sendConsentRequest(userId, record);
    
    return consentId;
  }
  
  async grantConsent(consentId) {
    const record = this.consentRecords.get(consentId);
    if (!record) throw new Error('Consent record not found');
    
    record.status = 'granted';
    record.grantedAt = new Date();
    
    return record;
  }
  
  async verifyConsent(consentId) {
    const record = this.consentRecords.get(consentId);
    return record?.status === 'granted';
  }
  
  async sendConsentRequest(userId, record) {
    // Implementation for sending consent request to user
    console.log(`Consent request sent to user ${userId}`);
  }
}

// Usage with API
const consentMgr = new ConsentManager();
const consentId = await consentMgr.requestConsent('user123', 'img456', 'virtual_tryon');

// After user grants consent
await consentMgr.grantConsent(consentId);

// Verify before processing
if (await consentMgr.verifyConsent(consentId)) {
  const result = await virtualTryOn(sourceImage, garmentImage, {
    consentId: consentId
  });
}
```

## Configuration Options

### API Request Parameters

```javascript
// Common configuration options
const config = {
  // Image quality and resolution
  output_format: 'jpg', // 'jpg', 'png', 'webp'
  output_quality: 95, // 1-100
  max_resolution: 2048, // max width/height in pixels
  
  // Processing options
  style: 'realistic', // 'realistic', 'artistic', 'catalog'
  preserve_details: true,
  blend_mode: 'seamless', // 'seamless', 'natural', 'sharp'
  
  // Garment-specific
  fit_adjustment: 'auto', // 'auto', 'tight', 'loose', 'exact'
  wrinkle_simulation: true,
  lighting_match: true,
  
  // Safety and compliance
  consent_verified: true, // Always required
  detect_minors: true,
  content_filter: 'strict' // 'strict', 'moderate'
};
```

### Webhook Configuration

```python
# Python - Webhook setup for async processing
def setup_webhook(callback_url):
    """Configure webhook for async results"""
    payload = {
        'webhook_url': callback_url,
        'events': ['tryon.completed', 'tryon.failed'],
        'secret': os.environ.get('WEBHOOK_SECRET')
    }
    
    response = client.request('POST', 'webhooks', json=payload)
    return response.json()

# Webhook handler
from flask import Flask, request
import hmac
import hashlib

app = Flask(__name__)

@app.route('/webhook/undress', methods=['POST'])
def handle_webhook():
    # Verify signature
    signature = request.headers.get('X-Undress-Signature')
    body = request.get_data()
    
    expected = hmac.new(
        os.environ.get('WEBHOOK_SECRET').encode(),
        body,
        hashlib.sha256
    ).hexdigest()
    
    if signature != expected:
        return 'Invalid signature', 401
    
    # Process event
    event = request.json
    if event['type'] == 'tryon.completed':
        print(f"Try-on completed: {event['data']['output_url']}")
    
    return 'OK', 200
```

## Troubleshooting

### Common Issues

**Authentication Failures**

```javascript
// Check API key configuration
if (!process.env.UNDRESS_API_KEY) {
  throw new Error('UNDRESS_API_KEY environment variable not set');
}

// Test authentication
async function testAuth() {
  try {
    const response = await client.get('/auth/verify');
    console.log('Authentication successful');
  } catch (error) {
    console.error('Auth failed:', error.response?.status, error.response?.data);
  }
}
```

**Consent Verification Errors**

```python
# Always verify consent before processing
def safe_process(image_data, consent_token):
    if not consent_token:
        raise ValueError('Consent token required')
    
    payload = {
        'source_image': image_data,
        'consent_verified': True,
        'consent_token': consent_token
    }
    
    response = client.request('POST', 'virtual-tryon', json=payload)
    
    if response.status_code == 403:
        raise PermissionError('Consent verification failed')
    
    return response.json()
```

**Image Format Issues**

```javascript
// Ensure proper image encoding
const fs = require('fs');

function encodeImage(filePath) {
  const buffer = fs.readFileSync(filePath);
  const base64 = buffer.toString('base64');
  const mimeType = filePath.endsWith('.png') ? 'image/png' : 'image/jpeg';
  
  return `data:${mimeType};base64,${base64}`;
}

// Use with API
const encodedImage = encodeImage('./photo.jpg');
```

**Rate Limiting**

```python
# Handle rate limits with retry logic
import time

def request_with_retry(endpoint, payload, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = client.request('POST', endpoint, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:  # Rate limit
                wait_time = int(e.response.headers.get('Retry-After', 60))
                print(f"Rate limited. Waiting {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise
    
    raise Exception('Max retries exceeded')
```

### Error Codes

| Code | Meaning | Solution |
|------|---------|----------|
| 400 | Invalid request | Check payload structure and required fields |
| 401 | Unauthorized | Verify API key is correct and active |
| 403 | Consent required | Ensure consent_verified is true and valid |
| 413 | Image too large | Resize image or reduce quality |
| 429 | Rate limit | Implement retry with exponential backoff |
| 500 | Server error | Contact support or retry later |

## Best Practices

1. **Always verify consent** before processing any image containing people
2. **Store consent records** with timestamps and audit trails
3. **Implement content filtering** to prevent misuse
4. **Label AI-generated content** clearly in output metadata
5. **Cache results** when appropriate to reduce API calls
6. **Handle errors gracefully** with proper user feedback
7. **Respect rate limits** and implement backoff strategies
8. **Use webhooks** for long-running operations
9. **Validate inputs** before sending to API
10. **Monitor usage** to prevent quota exhaustion

## Responsible AI Checklist

Before deploying any Undress Design integration:

- [ ] Consent collection mechanism implemented
- [ ] Age verification for all subjects
- [ ] Content moderation filters active
- [ ] Clear AI-generated content labeling
- [ ] Terms of service compliance verified
- [ ] Privacy policy updated
- [ ] Audit logging enabled
- [ ] User data retention policy defined
- [ ] Takedown request process established
- [ ] Legal review completed

## Additional Resources

- Official Documentation: https://undress.design/docs
- API Reference: https://undress.design/api-docs
- Consent Guidelines: https://undress.design/consent
- Community Forum: https://community.undress.design
- Support: support@undress.design
