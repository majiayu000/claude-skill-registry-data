---
name: allow1
description: "Use when generating, vectorizing, or converting images to SVG — logos, icons, illustrations, or 'allow1'/'quiver' references."
allowed-tools: ["Read", "Write", "Edit", "Bash", "Glob", "Grep", "AskUserQuestion", "WebFetch"]
argument-hint: "[generate|vectorize|batch] [prompt or image path]"
user-invocable: false
---

# ALLOW 1 (Quiver AI) — SVG Generation & Vectorization Skill

Uses the Quiver AI API to perform professional-level SVG generation from text prompts (Text-to-SVG) and raster image to SVG conversion (Image-to-SVG).

---

## Prerequisites

- `ALLOW1_API_KEY` environment variable is set
- Base URL: `https://api.quiver.ai/v1`
- Model: `arrow-preview` (current public model)

## Quick Reference

| Feature | Subcommand | Reference |
|------|-------------|-------------|
| **Text-to-SVG Generation** | `generate` | [references/text-to-svg.md](${CLAUDE_SKILL_DIR}/references/text-to-svg.md) |
| **Image-to-SVG Conversion** | `vectorize` | [references/image-to-svg.md](${CLAUDE_SKILL_DIR}/references/image-to-svg.md) |
| **Batch Generation** | `batch` | [references/batch-workflow.md](${CLAUDE_SKILL_DIR}/references/batch-workflow.md) |
| **API Reference** | — | [references/api-reference.md](${CLAUDE_SKILL_DIR}/references/api-reference.md) |
| **Prompt Guide** | — | [references/prompt-guide.md](${CLAUDE_SKILL_DIR}/references/prompt-guide.md) |

- "**Create SVG**" / "**Generate logo**" / "**Create icon**" → Text-to-SVG
- "**Convert image to SVG**" / "**Vectorize**" / "**Trace**" → Image-to-SVG
- "**allow1**" / "**quiver**" → This skill in general
- "**Batch SVG**" / "**Multiple SVG**" → Batch generation




---

## Execution Flow

```
/allow1 [generate|vectorize|batch] [prompt or image]
    |
    +--[Step 1] Environment check
    |   +-- Verify $ALLOW1_API_KEY exists
    |   +-- Verify connection by fetching model list (GET /v1/models)
    |
    +--[Step 2] Requirements gathering (AskUserQuestion as needed)
    |   +-- Purpose: Logo / Icon / Illustration / UI parts
    |   +-- Style: Minimal / Flat / Line art / Gradient
    |   +-- Output count (n): 1-16 (default 4)
    |   +-- Save path
    |
    +--[Step 3] API execution
    |   +-- generate: POST /v1/svgs/generations
    |   +-- vectorize: POST /v1/svgs/vectorizations
    |   +-- batch: Execute multiple requests sequentially (rate limit aware)
    |
    +--[Step 4] Result processing
    |   +-- Save as SVG file
    |   +-- Token usage report
    |   +-- Retry as needed (429 / 5xx errors)
    |
    +--[Step 5] Optimization (optional)
        +-- Optimization suggestions via SVGO
        +-- Advice on viewBox / color adjustments
```

---

## Basic Usage Examples

### Text-to-SVG

```bash
# Simple logo generation
/allow1 generate "A minimalist mountain logo for a hiking app"

# With style instructions
/allow1 generate "Dashboard icon set" --style flat --n 8
```

### Image-to-SVG

```bash
# Vectorize image file
/allow1 vectorize ./assets/logo.png

# Convert directly from URL
/allow1 vectorize https://example.com/image.png --auto-crop
```

### Batch Generation

```bash
# Batch-generate multiple icons
/allow1 batch "home icon" "settings icon" "profile icon" "search icon"
```

---

## API Call Patterns (curl)

### Environment Variable Check + Connection Verification

```bash
# Verify API key
if [ -z "$ALLOW1_API_KEY" ]; then
  echo "ERROR: ALLOW1_API_KEY is not set"
  exit 1
fi

# Connection test (fetch model list)
curl -s https://api.quiver.ai/v1/models \
  -H "Authorization: Bearer $ALLOW1_API_KEY" | jq .
```

### Text-to-SVG (Non-streaming)

```bash
curl -s https://api.quiver.ai/v1/svgs/generations \
  -H "Authorization: Bearer $ALLOW1_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "arrow-preview",
    "prompt": "A clean minimalist logo for a tech startup called Nexus",
    "instructions": "Use geometric shapes, monochrome palette, flat design",
    "n": 4,
    "temperature": 0.7,
    "stream": false
  }' | jq -r '.data[0].svg' > output.svg
```

### Image-to-SVG

```bash
curl -s https://api.quiver.ai/v1/svgs/vectorizations \
  -H "Authorization: Bearer $ALLOW1_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "arrow-preview",
    "image": { "url": "https://example.com/logo.png" },
    "auto_crop": true,
    "target_size": 1024,
    "n": 1,
    "stream": false
  }' | jq -r '.data[0].svg' > vectorized.svg
```

### Base64 Image Input

```bash
BASE64=$(base64 -i ./input.png)
curl -s https://api.quiver.ai/v1/svgs/vectorizations \
  -H "Authorization: Bearer $ALLOW1_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"model\": \"arrow-preview\",
    \"image\": { \"base64\": \"$BASE64\" },
    \"auto_crop\": true,
    \"stream\": false
  }" | jq -r '.data[0].svg' > vectorized.svg
```

---

## Rate Limiting and Error Handling

| Limit | Value |
|------|-----|
| Request limit | 20 req / 60 sec (per organization) |
| Response headers | `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset` |
| On 429 | Respect `Retry-After` header, exponential backoff |
| Billing | 1 request = 1 credit (regardless of n value) |

### Error Code Quick Reference

| HTTP | Code | Action |
|------|--------|------|
| 400 | `invalid_request` | Check request parameters |
| 401 | `invalid_api_key` | Check `$ALLOW1_API_KEY` |
| 402 | `insufficient_credits` | Credit purchase required |
| 403 | `account_frozen` | Check account status |
| 429 | `rate_limit_exceeded` | Wait `Retry-After` seconds |
| 500/502/503 | Server error | Retry with exponential backoff |

---

## Related Skills

- `generate-slide` — Slide Image Generation via Nano Banana Pro
- `generate-video` — Video generation with Remotion
- `ui` — UI component generation (for embedding SVG icons)
