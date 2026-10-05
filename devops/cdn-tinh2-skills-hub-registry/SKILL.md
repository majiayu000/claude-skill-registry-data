---
name: cdn
description: "Configure a CDN with optimized caching, SSL/TLS, security headers, and cache invalidation — auto-detects hosting provider and app type, generates CloudFront, Cloudflare, or Vercel config with per-content-type cache rules, edge functions, and compression. Use when deploying a static site, SPA, SSR app, or adding a CDN layer to an existing API."
version: "2.0.0"
category: deploy
platforms:
  - CLAUDE_CODE
---

You are in AUTONOMOUS MODE. Do NOT ask questions. Do NOT pause for confirmation.
Execute every phase below in sequence, making decisions based on what you find.

============================================================
PHASE 0 -- INPUT
============================================================

$ARGUMENTS may contain:
- A CDN provider: `cloudfront`, `cloudflare`, `vercel`, `fastly`, `akamai`
- A custom domain: `example.com` or `app.example.com`
- `--edge` -- set up edge functions/workers
- `--terraform` -- generate CDN config as Terraform (instead of provider-specific config)
- `--spa` -- optimize for single-page application (custom error responses, rewrites)
- `--static` -- optimize for static site (aggressive caching, no dynamic content)
- If no arguments, auto-detect from existing infrastructure

============================================================
PHASE 1 -- INFRASTRUCTURE DETECTION
============================================================

Scan the project to determine hosting and CDN needs:

**Current hosting**:
- Vercel: `vercel.json`, `.vercel/`
- Netlify: `netlify.toml`, `_redirects`
- AWS: S3 bucket references, CloudFront in Terraform, `amplify.yml`
- Cloudflare: `wrangler.toml`, Cloudflare in Terraform
- Self-hosted: `nginx.conf`, `Caddyfile`, Docker with reverse proxy

**Application type**:
- Static site: `next export`, `gatsby build`, `vite build`, `astro build` -- output in `dist/`, `out/`, `build/`, `.next/`
- SPA: React, Vue, Angular without SSR -- single `index.html` entry point
- SSR: Next.js, Nuxt, Remix, SvelteKit with server rendering
- API: Express, Fastify, Django, Flask -- no static assets to cache at CDN level
- Hybrid: both static assets and API routes

**Asset analysis**:
- Check `public/` or `static/` directory for static assets
- Check build output for hashed filenames (e.g., `main.a1b2c3.js`)
- Identify large assets: images, fonts, videos
- Check for existing cache headers in application code

**Existing CDN**:
- Read any existing CDN configuration
- Check DNS records for CNAME pointing to CDN providers
- Check response headers for `x-cache`, `cf-cache-status`, `x-amz-cf-id`

============================================================
PHASE 2 -- CACHING STRATEGY
============================================================

Define cache rules based on content type:

**Immutable assets** (hashed filenames -- `main.a1b2c3.js`):
```
Cache-Control: public, max-age=31536000, immutable
```
- JS, CSS, images with content hash in filename
- Maximum cache duration (1 year)
- Never needs revalidation

**Static assets** (non-hashed -- `/favicon.ico`, `/robots.txt`):
```
Cache-Control: public, max-age=86400, stale-while-revalidate=604800
```
- 1 day cache, serve stale for up to 7 days while revalidating
- Fonts: `max-age=31536000` (versioned by URL path)

**HTML pages**:
```
Cache-Control: public, max-age=300, stale-while-revalidate=3600
```
- 5 minute cache, stale-while-revalidate for 1 hour
- For SSR pages with dynamic content
- Static site HTML: `max-age=3600` (1 hour)

**API responses**:
```
Cache-Control: private, no-cache, no-store, must-revalidate
```
- No CDN caching for authenticated API calls
- Public API endpoints can use short TTL: `public, max-age=60, s-maxage=300`

**Media**:
```
Cache-Control: public, max-age=604800
```
- Images, videos, PDFs: 7 days
- User-uploaded content: 1 day with revalidation

============================================================
PHASE 3 -- CDN CONFIGURATION
============================================================

Generate configuration for the detected/specified provider:

**CloudFront** (Terraform or console config):
```hcl
resource "aws_cloudfront_distribution" "main" {
  enabled             = true
  is_ipv6_enabled     = true
  default_root_object = "index.html"
  aliases             = [var.domain]
  price_class         = "PriceClass_100"  # US, Canada, Europe
  http_version        = "http2and3"

  origin {
    domain_name = aws_s3_bucket.static.bucket_regional_domain_name
    origin_id   = "s3-static"
    origin_access_control_id = aws_cloudfront_origin_access_control.main.id
  }

  default_cache_behavior {
    allowed_methods  = ["GET", "HEAD", "OPTIONS"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = "s3-static"

    cache_policy_id          = aws_cloudfront_cache_policy.optimized.id
    origin_request_policy_id = "88a5eaf4-2fd4-4709-b370-b4c650ea3fcf"  # CORS-S3Origin

    viewer_protocol_policy = "redirect-to-https"
    compress               = true
  }

  # API origin (if applicable)
  origin {
    domain_name = var.api_domain
    origin_id   = "api"
    custom_origin_config {
      http_port              = 80
      https_port             = 443
      origin_protocol_policy = "https-only"
      origin_ssl_protocols   = ["TLSv1.2"]
    }
  }

  ordered_cache_behavior {
    path_pattern     = "/api/*"
    target_origin_id = "api"
    allowed_methods  = ["DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT"]
    cached_methods   = ["GET", "HEAD"]
    cache_policy_id  = "4135ea2d-6df8-44a3-9df3-4b5a84be39ad"  # CachingDisabled
    viewer_protocol_policy = "https-only"
    compress               = true
  }

  # SPA custom error response
  custom_error_response {
    error_code         = 403
    response_code      = 200
    response_page_path = "/index.html"
  }

  viewer_certificate {
    acm_certificate_arn      = var.certificate_arn
    ssl_support_method       = "sni-only"
    minimum_protocol_version = "TLSv1.2_2021"
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }
}
```

**Cloudflare** (`wrangler.toml` + page rules or `_headers`):
```toml
name = "{project-name}"
compatibility_date = "2024-01-01"

[site]
bucket = "./dist"

[[headers]]
for = "/_next/static/*"
[headers.values]
Cache-Control = "public, max-age=31536000, immutable"

[[headers]]
for = "/api/*"
[headers.values]
Cache-Control = "no-store"
```

Generate Cloudflare page rules or cache rules:
- `*.js`, `*.css`: Cache Level = Cache Everything, Edge TTL = 1 year
- `/api/*`: Cache Level = Bypass
- `*.html`: Cache Level = Cache Everything, Edge TTL = 5 minutes

**Vercel** (`vercel.json`):
```json
{
  "headers": [
    {
      "source": "/(.*).js",
      "headers": [
        { "key": "Cache-Control", "value": "public, max-age=31536000, immutable" }
      ]
    },
    {
      "source": "/api/(.*)",
      "headers": [
        { "key": "Cache-Control", "value": "no-store" }
      ]
    }
  ]
}
```

**Application-level headers** (if no CDN config file available):
Generate middleware to set Cache-Control headers in the application code.

============================================================
PHASE 4 -- SSL/TLS CONFIGURATION
============================================================

Ensure HTTPS is properly configured:

**CloudFront + ACM**:
- Generate Terraform for `aws_acm_certificate` with DNS validation
- Must be in `us-east-1` for CloudFront
- Configure minimum TLS 1.2

**Cloudflare**:
- Enable Full (strict) SSL mode
- Enable Always Use HTTPS
- Enable Automatic HTTPS Rewrites
- Enable HSTS with `max-age=31536000; includeSubDomains`

**Let's Encrypt** (self-hosted):
- Generate Certbot renewal config or Caddy auto-TLS
- Set up auto-renewal cron job

Generate security headers in CDN config:
```
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 0
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), microphone=(), geolocation=()
Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline'
```

============================================================
PHASE 5 -- EDGE FUNCTIONS (if --edge)
============================================================

Generate edge function/worker for common patterns:

**A/B testing**:
- Read cookie for experiment assignment
- Route to different origins or rewrite response

**Redirects**:
- Handle URL redirects at the edge (faster than origin)
- Migrate from `_redirects` file to edge function

**Geolocation**:
- Read `CF-IPCountry` or `CloudFront-Viewer-Country` header
- Route to regional origins or localized content

**Bot protection**:
- Check User-Agent and known bot patterns
- Rate limiting at edge

**Image optimization**:
- Resize/format images at edge using Cloudflare Images or CloudFront Functions

============================================================
PHASE 6 -- CACHE INVALIDATION
============================================================

Set up cache invalidation for deployments:

**CloudFront**:
```bash
aws cloudfront create-invalidation \
  --distribution-id $DISTRIBUTION_ID \
  --paths "/*"
```
- Add to CI/CD deploy step
- For targeted invalidation: only HTML files (`/index.html`, `/about/index.html`)

**Cloudflare**:
```bash
curl -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/purge_cache" \
  -H "Authorization: Bearer $CF_API_TOKEN" \
  -d '{"purge_everything": true}'
```

**Vercel**: automatic on deploy (no manual invalidation needed)

Generate CI/CD step for invalidation after deploy.

============================================================
PHASE 7 -- PERFORMANCE OPTIMIZATION
============================================================

Configure additional optimizations:

- **Compression**: Enable Brotli (preferred) and Gzip compression
- **HTTP/2 and HTTP/3**: Enable where supported
- **Early Hints**: Send 103 Early Hints for critical resources
- **Preconnect hints**: Add `Link: <https://cdn.example.com>; rel=preconnect` headers
- **Image formats**: Serve WebP/AVIF via Accept header content negotiation


============================================================
SELF-HEALING VALIDATION (max 2 iterations)
============================================================

After completing deployment/infrastructure changes, validate:

1. Verify all generated files are syntactically valid (YAML, JSON, HCL, Dockerfile).
2. Run validation commands if available (terraform validate, docker build --check, kubectl dry-run).
3. Verify no secrets, credentials, or sensitive values are hardcoded.
4. If validation fails, diagnose and fix the specific syntax or config error.
5. Repeat up to 2 iterations.

IF STILL FAILING after 2 iterations:
- Document what failed and the exact error
- Include partial output if available

============================================================
OUTPUT
============================================================

```
## CDN Configuration Complete

### Provider: {provider}
### Domain: {domain}

### Files Created
{list of files}

### Caching Rules
| Content Type | Cache Duration | Revalidation |
|-------------|---------------|--------------|
| Hashed assets (JS/CSS) | 1 year | Immutable |
| Static assets | 1 day | 7 day stale-while-revalidate |
| HTML pages | 5 minutes | 1 hour stale-while-revalidate |
| API responses | No cache | -- |
| Media files | 7 days | -- |

### Security Headers
{list of security headers configured}

### Cache Invalidation
{command or CI step to invalidate cache}

### Performance
- Compression: Brotli + Gzip
- Protocol: HTTP/2 + HTTP/3
- TLS: 1.2 minimum
```

============================================================
NEXT STEPS
============================================================

1. Point DNS to CDN (CNAME or alias record)
2. Verify SSL certificate is valid and serving correctly
3. Test cache behavior: `curl -I https://yourdomain.com/asset.js` -- check Cache-Control header
4. Monitor cache hit rate in CDN dashboard (target: >90% for static assets)
5. Set up Real User Monitoring (RUM) to track performance impact
6. Run Lighthouse/WebPageTest before and after to measure improvement


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /cdn — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.

============================================================
DO NOT
============================================================

- Do NOT cache authenticated API responses at the CDN
- Do NOT set long TTLs on HTML without a cache invalidation strategy
- Do NOT use `Cache-Control: no-cache` when you mean `no-store` (no-cache still caches, just revalidates)
- Do NOT bypass CDN for static assets -- that defeats the purpose
- Do NOT configure TLS below version 1.2
- Do NOT serve mixed content (HTTP resources on HTTPS pages)
- Do NOT invalidate entire cache on every deploy -- target specific paths
- Do NOT overwrite existing CDN configuration without reading it first
- Do NOT store CDN API tokens in source code -- use CI/CD secrets
