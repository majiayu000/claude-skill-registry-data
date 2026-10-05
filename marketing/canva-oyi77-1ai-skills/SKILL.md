---
name: canva
description: Use when creating, exporting, and managing Canva designs via the Connect
  API. Generate social posts, carousels, and graphics programmatically.
domain: marketing
author: oyi77
license: Apache-2.0
subdomain: marketing
tags:
- api
- canva
- growth
- marketing
- seo
- social-media
version: 1.0.0
homepage: https://github.com/abgohel/canva-skill
metadata:
  clawdbot:
    emoji: 🎨
    category: design
    requires:
      env:
      - CANVA_CLIENT_ID
      - CANVA_CLIENT_SECRET
category: marketing
---

# Canva

## When to Use
**Trigger phrases:**
- "canva"
- "Create, export, and manage Canva designs via the Connect API"


- "Create an Instagram post about [topic]"
- "Export my Canva design as PNG"
- "List my recent designs"
- "Create a carousel from these points"
- "Upload this image to Canva"


## When NOT to Use

- When the audience is too small to justify the effort
- For regulated industries without compliance review
- When the campaign budget does not support the channel


## Overview

Canva's Connect API provides programmatic access to the entire design lifecycle — from template selection and brand-controlled customization to multi-format export and publishing. It enables developers and marketers to automate graphic creation at scale without requiring design tools or manual intervention. The API covers social media posts, presentations, documents, videos, and carousels, all while enforcing brand guidelines through Brand Kits and asset libraries.

The design automation lifecycle follows a predictable pipeline: select a branded template, populate it with dynamic content (text, images, data), apply brand kit styling, and export to the target format (PNG, PDF, MP4, GIF). Each stage is accessible via REST endpoints, making it possible to embed Canva-powered design generation into any application or workflow — from e-commerce product imagery to social media scheduling bots.

Key capabilities include: Brand Kit enforcement for consistent typography, colors, and logos across every asset; asset upload and management for images, fonts, and videos; team collaboration with folder organization and permission controls; auto-resize to adapt a single design into multiple formats simultaneously; and headless design generation where templates are populated entirely through API calls without any manual interaction.

Integration patterns range from simple one-off exports to high-throughput batch generation. Common use cases include: social media content calendars producing 50+ platform-specific variants weekly, e-commerce product imagery dynamically populated from inventory feeds, programmatic ad creative generation with A/B test variants, and automated report/document generation with live data integration.
## Workflow

```python
# Canva Connect API — create a social media post from a brand template
import requests
import os

CANVA_API = "https://api.canva.com/rest/v1"
HEADERS = {
    "Authorization": f"Bearer {os.environ['CANVA_ACCESS_TOKEN']}",
    "Content-Type": "application/json",
}

def create_and_export_post(template_id: str, brand_id: str, text_overrides: dict, image_urls: list[str]) -> str:
    """Create a design from a brand template and export as PNG."""
    # Step 1: Create design from template
    design_resp = requests.post(f"{CANVA_API}/designs", headers=HEADERS, json={
        "template_id": template_id,
        "brand_template_id": brand_id,
    })
    design_resp.raise_for_status()
    design_id = design_resp.json()["design"]["id"]

    # Step 2: Replace text placeholders
    for element_id, new_text in text_overrides.items():
        requests.patch(f"{CANVA_API}/designs/{design_id}/elements/{element_id}", headers=HEADERS, json={
            "text": new_text,
        })

    # Step 3: Replace image placeholders
    for idx, url in enumerate(image_urls):
        asset = requests.post(f"{CANVA_API}/assets/uploads", headers=HEADERS, json={"url": url}).json()
        requests.patch(f"{CANVA_API}/designs/{design_id}/elements/image-{idx}", headers=HEADERS, json={
            "asset_id": asset["asset"]["id"],
        })

    # Step 4: Export as PNG
    export = requests.post(f"{CANVA_API}/designs/{design_id}/exports", headers=HEADERS, json={
        "type": "png",
        "pages": [{"page_number": 1}],
    }).json()
    job_id = export["job"]["id"]
    return design_id, job_id
```

### Design Generation Workflow

1. **Authentication** — Obtain an OAuth 2.0 access token via the Canva OAuth flow (authorization code grant). Store the refresh token for long-lived access. Scopes required: `design:content:read`, `design:content:write`, `asset:read`, `asset:write`.

2. **Template Selection** — Query available designs with `GET /designs` or browse brand templates from the Brand Kit. Identify the template ID and map its placeholder element IDs (text, image slots, charts) for dynamic population.

3. **Content Preparation** — Prepare text copy, image URLs (publicly accessible for upload), data arrays for charts/tables, and brand color overrides. Validate content fits template constraints before API calls.

4. **Design Generation** — Create the design from a template via `POST /designs`, then populate placeholders using `PATCH /designs/{id}/elements/{element_id}` for text and image replacement. Apply auto-resize for multi-format variants.

5. **Asset Management** — Upload images and videos via `POST /assets/uploads` (URL import or multipart upload). Manage brand assets in folders. List assets with `GET /assets` and apply them to design elements.

6. **Export & Publish** — Export designs to PNG, PDF, MP4, or GIF via `POST /designs/{id}/exports`. Poll the export job status until complete, then download the result URL. Optionally publish directly to connected social channels.

7. **Scale & Automate** — Wrap the pipeline in batch jobs for high-volume generation. Implement rate-limit handling (100 req/min default), retry logic for export polling, and webhook callbacks for async job completion.

## Key Metrics

- Reach and impressions
- Engagement rate (likes, shares, comments)
- Conversion rate (clicks → leads → customers)
- Customer acquisition cost (CAC)
- Return on ad spend (ROAS)

## Best Practices

- Test everything — headlines, images, CTAs, timing
- Focus on one channel at a time, then expand
- Build organic before scaling paid
- Track attribution across the full funnel

## Code Examples

### List Recent Designs
```python
def list_designs(limit: int = 20) -> list[dict]:
    """Fetch recent Canva designs from the authenticated account."""
    resp = requests.get(f"{CANVA_API}/designs", headers=HEADERS, params={"limit": limit})
    resp.raise_for_status()
    return resp.json()["data"]

# designs = list_designs(10)
# for d in designs:
#     print(f"{d['name']} — {d['id']} (updated {d['updated_at']})")
```

### Generate a Social Media Carousel
```python
def create_carousel(template_id: str, slides: list[dict]) -> list[str]:
    """Generate a multi-page carousel from a single template with per-slide overrides."""
    design_ids = []
    for slide in slides:
        resp = requests.post(f"{CANVA_API}/designs", headers=HEADERS, json={
            "template_id": template_id,
        })
        design_id = resp.json()["design"]["id"]
        for key, val in slide.items():
            requests.patch(f"{CANVA_API}/designs/{design_id}/elements/{key}", headers=HEADERS, json={"text": val})
        design_ids.append(design_id)
    return design_ids
```

### Upload an Image to Canva
```python
def upload_image(url: str, name: str = "uploaded-image") -> str:
    """Upload an image from a public URL to the Canva asset library."""
    resp = requests.post(f"{CANVA_API}/assets/uploads", headers=HEADERS, json={
        "name": name,
        "url": url,
    })
    resp.raise_for_status()
    return resp.json()["asset"]["id"]
```

### Query Brand Kit Assets
```python
def get_brand_kit(brand_id: str) -> dict:
    """Retrieve brand kit details including colors, fonts, and logos."""
    resp = requests.get(f"{CANVA_API}/brands/{brand_id}", headers=HEADERS)
    resp.raise_for_status()
    return resp.json()["brand"]
```

## Setup / Configuration

### Prerequisites
- Canva account with Developer Access (free tier available)
- Canva Connect API enabled in the developer dashboard
- Registered OAuth 2.0 application with redirect URI

### Environment Variables
```
CANVA_CLIENT_ID=your_client_id
CANVA_CLIENT_SECRET=your_client_secret
CANVA_REDIRECT_URI=https://your-app.com/oauth/callback
CANVA_ACCESS_TOKEN=obtained_via_oauth
CANVA_REFRESH_TOKEN=for_token_rotation
```

### OAuth 2.0 Authentication Flow
1. Redirect user to `https://www.canva.com/api/oauth/authorize` with `client_id`, `redirect_uri`, `response_type=code`, and `scope`.
2. Handle the callback containing an authorization `code`.
3. Exchange `code` for an access token via `POST /api/oauth/token`.
4. Store the `refresh_token` for silent re-authentication when the access token expires (typically 1 hour).

### Rate Limits
| Limit Type | Value |
|---|---|
| Requests per minute | 100 per user |
| Export jobs per minute | 20 per user |
| Max upload file size | 25 MB (URL import) |
| Max design pages | 100 per design |

## Common Issues / Troubleshooting

| Error | Cause | Solution |
|---|---|---|
| `401 Unauthorized` | Expired or invalid access token | Refresh the token using the stored `refresh_token`. Tokens expire every 60 minutes. |
| `403 Forbidden` | Insufficient OAuth scopes | Verify scopes include `design:content:write` and `asset:write`. Re-authorize with correct scope. |
| `404 template not found` | Template ID invalid or user lacks access | Confirm the template exists in the user's design list. Brand templates must be shared with the authenticated user. |
| `429 Too Many Requests` | Rate limit exceeded | Implement exponential backoff. 100 req/min per user. Batch exports with spacing. |
| Export job stuck on `in_progress` | Large design or high server load | Poll with 2-second intervals up to 120 seconds. For video exports, extend timeout to 5 minutes. |
| Image upload fails silently | URL not publicly accessible or unsupported format | Verify the URL returns a 200 and the file is JPEG/PNG/GIF under 25 MB. Use multipart upload for private assets. |
| Auto-resize produces misaligned elements | Template lacks responsive layout rules | Design templates with Canva's responsive layout feature enabled. Fixed-position templates do not auto-resize cleanly. |

## Monetization

| Approach | Timeframe | Description |
|---|---|---|
| Design-as-a-Service API | 2-4 weeks | Offer a subscription API that generates branded social media creatives, carousels, and ad banners on demand. Charge per-export or monthly tier. |
| E-commerce Product Imagery | 3-6 weeks | Build automated product photo pipelines that generate lifestyle, catalog, and ad variants from inventory feeds. Sell to Shopify/WooCommerce merchants. |
| Social Media Content Agency | 1-3 months | Operate a content agency producing 100+ branded posts/week per client using automated Canva generation. Monthly retainers of $500-$5,000. |
| Canva Template Marketplace | 2-4 weeks | Create and sell premium brand template packs on Canva's marketplace or your own store. Passive income with royalty per download. |
| Enterprise Brand Compliance Tool | 1-3 months | Build a tool that enforces brand consistency by auto-generating all marketing assets from approved templates only. Sell to marketing teams at mid-size companies. |
| White-Label Print-on-Demand | 4-8 weeks | Integrate Canva design generation with print-on-demand APIs (Printful, Printify) for automated merchandise creation from user templates. |

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I can design everything manually for free" | Manual design does not scale. Programmatic generation through the Connect API produces 10-20x more assets in the same time with brand consistency enforced automatically. |
| "Templates make everything look generic" | Properly customized templates with brand kit enforcement (colors, fonts, logos) produce unique, on-brand output at scale. The template is a starting point, not the final product. |
| "Canva is only for beginners, not enterprises" | Canva Enterprise + Connect API powers automated pipelines at Fortune 500 companies with SSO, brand governance, and audit trails. The API handles millions of designs/month at scale. |
| "Automated design will never match human quality" | For production workflows with defined templates and content slots, automated output matches or exceeds manual quality while enabling A/B testing at scale that one-off designs cannot. |
| "Batch-generated content feels spammy" | Platform-optimized variants (different sizes, copy, CTAs per channel) improve engagement. The key is template diversity and content variation, not cloning the same design repeatedly. |
| "API design requires a full engineering team" | The Connect API has straightforward REST endpoints. A single developer can build a working pipeline in a day. Low-code platforms (Zapier, Make) also offer Canva integrations. |


## Process

### Preparation
- Register a Canva developer application and configure OAuth redirect URIs
- Obtain the required OAuth scopes: `design:content:read`, `design:content:write`, `asset:read`, `asset:write`, `brand:read`
- Create or identify brand templates in Canva with mapped placeholder element IDs
- Prepare source content (text, images, data) and validate format compatibility
- Set up environment variables and test authentication with a simple `GET /designs` call

### Execution
- Authenticate via OAuth 2.0 and acquire an access token with appropriate scopes
- For each asset: create design from template, populate placeholders, apply brand kit styling
- Handle pagination for list endpoints (`GET /designs`, `GET /assets`) using `cursor` and `limit`
- Implement retry logic with exponential backoff for rate-limited or timed-out export jobs
- Poll export job status at 2-second intervals; download completed exports to destination storage

### Stewardship
- Monitor API usage against rate limits (100 req/min) and set up alerts for approaching limits
- Rotate OAuth refresh tokens periodically; invalidate old tokens after rotation
- Version-control brand template IDs and element mappings alongside API code
- Audit exported designs periodically for brand compliance drift
- Maintain a fallback design template for each use case in case the primary template is deleted or modified

## Verification

- [ ] OAuth 2.0 flow completes successfully: authorization code exchanged for access + refresh tokens
- [ ] `GET /designs` returns the expected design list with correct pagination
- [ ] Design creation from template succeeds with `POST /designs` and returns a valid `design_id`
- [ ] Text and image placeholder replacement through `PATCH /designs/{id}/elements/{element_id}` updates the design correctly
- [ ] Export job initiates, completes, and produces a downloadable file in the requested format (PNG/PDF/MP4)
- [ ] Image upload via URL import creates an accessible asset in the library
- [ ] Brand kit query returns correct colors, fonts, and logo references
- [ ] Auto-resize produces valid multi-format variants without content clipping
- [ ] Error handling covers 401 (token refresh), 429 (backoff), and timeout scenarios
- [ ] Rate limit compliance verified: batch generation stays under 100 req/min