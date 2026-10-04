---
name: cdn
description: Content delivery network optimization
license: MIT
compatibility: opencode
metadata:
  audience: developer, devops-engineer
  category: devops
---

## What I do

- Design and implement CDN architectures for global content delivery
- Optimize cache strategies and invalidation policies
- Configure origin shielding and multi-CDN setups
- Implement edge computing logic at CDN locations
- Secure CDN endpoints against attacks
- Analyze CDN performance and optimize delivery

## When to use me

- When serving static assets to global audiences
- When reducing latency for geographically distributed users
- When protecting origin servers from traffic spikes
- When implementing DDoS protection and WAF
- When you need video streaming or large file delivery
- When optimizing costs for high-traffic applications

## Key Concepts

### Cache Configuration

```nginx
# Nginx CDN configuration
location /static/ {
    # Cache for 1 year for versioned assets
    expires 1y;
    add_header Cache-Control "public, immutable";
    
    # Enable CDN caching
    proxy_cache_valid 200 60m;
    proxy_cache_use_stale error timeout http_500;
    
    # Set cache key
    proxy_cache_key "$scheme$request_method$host$request_uri";
}

location /api/ {
    # Don't cache API responses by default
    proxy_cache_bypass $http_cache_control;
    add_header Cache-Control "no-store";
}
```

### CDN Provider Comparison

| Provider | Strengths | Use Cases |
|----------|----------|-----------|
| CloudFlare | DDoS protection, Workers | Security-focused, edge compute |
| AWS CloudFront | AWS integration, Lambda@Edge | AWS ecosystems |
| Fastly | Real-time purging, VCL | Custom caching, streaming |
| Akamai | Global reach, enterprise | Large-scale, video |
| Google Cloud CDN | GCP integration | GCP ecosystems |

### Cache Invalidation

```bash
# CloudFront invalidation
aws cloudfront create-invalidation \
    --distribution-id $DIST_ID \
    --paths "/static/*" "/images/*"

# CloudFlare purge
curl -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE/purge_cache" \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    --data '{"purge_everything": true}'
```

### Edge Computing

```javascript
// Cloudflare Worker example
addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request))
})

async function handleRequest(request) {
  const url = new URL(request.url)
  
  // A/B testing at the edge
  const variant = Math.random() < 0.5 ? 'a' : 'b'
  const response = await fetch(request)
  
  // Add variant header
  const newResponse = new Response(response.body, response)
  newResponse.headers.set('X-Variant', variant)
  
  return newResponse
}
```

### Performance Optimization

- Enable HTTP/2 or HTTP/3 for multiplexing
- Use compression (gzip, brotli)
- Implement image optimization at edge
- Enable HTTP secure headers
- Configure proper cache-control headers
- Use signed URLs for private content
