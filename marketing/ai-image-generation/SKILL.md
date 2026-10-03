---
name: ai-image-generation
description: Generate high-quality AI images using Replicate's black-forest-labs/flux-2-pro model. Use for blog featured images, social media, marketing materials, and visual content creation.
---

# AI Image Generation with Replicate

This skill guides you through generating high-quality, contextual images using Replicate's `black-forest-labs/flux-2-pro` model for any use case - blog posts, social media, marketing materials, presentations, and more.

## Overview

Generate professional AI images tailored to your specific needs. Perfect for content creation, marketing, product design, and visual storytelling.

**Model:** `black-forest-labs/flux-2-pro` via Replicate API
**Image Quality:** High-resolution, photorealistic
**Generation Time:** ~30-60 seconds per image
**Cost:** $0.015 per input image megapixel (~66 megapixels for $1)

- ~$0.009 for 576x1024 (9:16 portrait - cheapest!)
- ~$0.011 for 960x768 (5:4 classic)
- ~$0.012 for 1344x576 (21:9 ultrawide)
- ~$0.015 for 1024x1024 (1:1 square)
- ~$0.03 for 1920x1080 (16:9 widescreen)

## Prerequisites

- Replicate API token (stored in `.env.api` as `REPLICATE_API_TOKEN`)
- Node.js/TypeScript environment
- Admin access to blog API (`BLOG_API_KEY`)

## Setup

### Local Development

```bash
# Ensure REPLICATE_API_TOKEN is in your .env.api file
grep REPLICATE_API_TOKEN .env.api

# If missing, add it:
echo "REPLICATE_API_TOKEN=your-token-here" >> .env.api
```

---

## Quick Start

### 1. Generate Image with Node.js/Replicate SDK

```bash
# Install Replicate SDK (if not already installed)
yarn add replicate

# Run the generation script (uses width x height, not aspect ratio)
yarn tsx .claude/skills/ai-image-generation/scripts/generate-ai-image.ts "Your prompt here"
yarn tsx .claude/skills/ai-image-generation/scripts/generate-ai-image.ts "Your prompt here" output.png 1024 1024  # Square (~$0.015)
yarn tsx .claude/skills/ai-image-generation/scripts/generate-ai-image.ts "Your prompt here" output.png 1200 630   # Blog featured (default)
yarn tsx .claude/skills/ai-image-generation/scripts/generate-ai-image.ts "Your prompt here" output.png 1920 1080  # Widescreen
```

### 2. Upload to Supabase Storage

After generating an image, upload it to our Supabase Storage bucket:

```bash
# Load environment
source scripts/load-env.sh
API_KEY=$(grep BLOG_API_KEY .env.api | cut -d'=' -f2)

# Upload the generated image
UPLOAD=$(curl -s -X POST http://localhost:3000/api/blog/images/upload \
  -H "x-api-key: $API_KEY" \
  -F "file=@generated-image.png" \
  -F "alt_text=AI generated image for blog post")

# Extract the URL
IMAGE_URL=$(echo "$UPLOAD" | jq -r '.data.url')
echo "Image URL: $IMAGE_URL"
```

**Response format:**

```json
{
  "success": true,
  "data": {
    "url": "https://xxx.supabase.co/storage/v1/object/public/blog-images/2026/01/timestamp-filename.webp",
    "key": "2026/01/timestamp-filename.webp",
    "filename": "2026/01/timestamp-filename.webp"
  }
}
```

### 3. Use Generated Image in Blog Post

```bash
# Create post with the uploaded image
curl -s -X POST http://localhost:3000/api/blog/posts \
  -H "x-api-key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"slug\": \"your-post-slug\",
    \"title\": \"Your Post Title\",
    \"description\": \"Post description\",
    \"content\": \"# Introduction\\n\\nYour content here...\",
    \"category\": \"Guides\",
    \"tags\": [\"AI\", \"tutorial\"],
    \"featured_image_url\": \"$IMAGE_URL\",
    \"featured_image_alt\": \"AI generated image description\"
  }" | jq .
```

---

## Complete Workflow: Generate + Upload + Publish

```bash
# 1. Generate the image (1200x630 is default for blog featured images)
yarn tsx .claude/skills/ai-image-generation/scripts/generate-ai-image.ts \
  "Modern laptop showing AI image upscaling interface, before and after comparison, professional setup, blue lighting, photorealistic" \
  ./generated-featured.png \
  1200 630

# 2. Upload to Supabase Storage
source scripts/load-env.sh
API_KEY=$(grep BLOG_API_KEY .env.api | cut -d'=' -f2)

UPLOAD=$(curl -s -X POST http://localhost:3000/api/blog/images/upload \
  -H "x-api-key: $API_KEY" \
  -F "file=@generated-featured.png" \
  -F "alt_text=AI image upscaling before and after comparison")

IMAGE_URL=$(echo "$UPLOAD" | jq -r '.data.url')

# 3. Create blog post with the image
curl -s -X POST http://localhost:3000/api/blog/posts \
  -H "x-api-key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"slug\": \"ai-upscaling-guide\",
    \"title\": \"AI Image Upscaling: Complete Guide [2026]\",
    \"description\": \"Transform low-res photos into print-quality images with AI.\",
    \"content\": \"# AI Image Upscaling\\n\\nYour full content here...\",
    \"category\": \"Guides\",
    \"tags\": [\"upscale\", \"AI\", \"tutorial\"],
    \"featured_image_url\": \"$IMAGE_URL\",
    \"featured_image_alt\": \"AI image upscaling before and after comparison\"
  }" | jq .

# 4. Publish the post
curl -s -X POST http://localhost:3000/api/blog/posts/ai-upscaling-guide/publish \
  -H "x-api-key: $API_KEY" | jq .
```

---

## Prompt Engineering for High-Quality Images

Crafting effective prompts is crucial for generating high-quality, contextually relevant images.

### Prompt Structure Template

```text
[Subject] + [Style] + [Composition] + [Colors] + [Mood] + [Technical details]
```

### Examples for Image Upscaling Content

#### Tutorial/How-To Content

```text
Good Prompts:
"Modern laptop screen showing AI photo upscaling interface, before and after comparison, professional setup, blue lighting, photorealistic, high quality"

"Computer monitor showing pixelated vs sharp image comparison, professional photo editing workspace, clean modern design, detailed"

"Step-by-step visual showing low-resolution image transforming to high-resolution, infographic style, modern flat design, educational"
```

#### Technology/Innovation Content

```text
Good Prompts:
"Futuristic AI interface processing and enhancing images, holographic data streams, modern tech aesthetic, blue and purple neon accents, sleek design"

"Neural network visualization overlaid on photo enhancement process, abstract technology concept, vibrant colors, digital transformation"
```

#### Problem/Solution Content

```text
Good Prompts:
"Split image comparison: left side pixelated blurry photo, right side crystal clear enhanced photo, dramatic before after, high contrast"

"Frustrated photographer looking at pixelated image on screen transforming into happy expression with sharp enhanced image, storytelling"
```

### Prompt Modifiers for Quality

**Always include these for best results:**

- `photorealistic` or `professional photography` - For realistic images
- `high detail` or `sharp focus` - For clarity
- `professional` or `modern` - For polished look
- `clean` or `organized` - For professional feel
- `natural lighting` or `soft lighting` - For professional feel

**Color guidance:**

- `blue and white color scheme` - Professional, trustworthy (matches our brand)
- `modern tech aesthetic` - Technology-forward
- `muted colors` - Sophisticated
- `blue gradient background` - Modern, tech-forward

**Avoid these (may reduce quality):**

- `cartoon` or `anime` - Wrong style for our brand
- `abstract` - Often too vague
- `dark` or `gloomy` - Negative associations
- `busy` or `cluttered` - Unprofessional
- Generic terms without specifics

---

## Model Configuration Options

The `black-forest-labs/flux-2-pro` model supports various parameters:

### Basic Parameters

```typescript
{
  prompt: string,                    // Image description (required)
  aspect_ratio: string,              // Format: "width:height" (e.g., "16:9", "1:1", "4:3")
  num_inference_steps: number,       // Quality (10-50, default: 28)
  output_quality: number,            // Output quality 1-100 (default: 100)
  go_fast: boolean,                  // Use fast mode (default: false)
}
```

### Aspect Ratios

- `1:1` - Square (1024x1024)
- `16:9` - Widescreen (1920x1080, 1280x720)
- `21:9` - Ultrawide (1920x832, 1344x576)
- `3:2` - Photo standard (1152x768)
- `4:3` - Standard (1024x768)
- `5:4` - Classic (960x768)
- `9:16` - Portrait (576x1024, 720x1280)

### Recommended Settings by Use Case

**Blog Featured Images (16:9):**

```typescript
{
  aspect_ratio: "16:9",    // ~$0.014-0.03 per image
  num_inference_steps: 50,
  output_quality: 100
}
```

**Cheapest Option (9:16 - then crop):**

```typescript
{
  aspect_ratio: "9:16",    // Only ~$0.009 per image!
  num_inference_steps: 28,
  output_quality: 95
}
```

**Square Social Media (1:1):**

```typescript
{
  aspect_ratio: "1:1",     // ~$0.015 per image
  num_inference_steps: 50,
  output_quality: 100
}
```

---

## Image Storage Notes

**Supabase Storage Configuration:**

- **Bucket:** `blog-images`
- **Max file size:** 5MB (images are compressed before upload)
- **Output format:** WebP (auto-converted for optimal compression)
- **Max dimensions:** 1920x1080 (auto-resized if larger)
- **Cache control:** 1 year (CDN optimized)
- **Path format:** `YYYY/MM/timestamp-filename.webp`

Images are automatically:

1. Resized to max 1920x1080 (maintaining aspect ratio)
2. Converted to WebP format
3. Compressed to 80% quality
4. Served via Supabase CDN with 1-year cache

---

## Cost Management

**Pricing:** $0.015 per megapixel (~66 megapixels for $1)

**Cheapest to most expensive:**

- **9:16** (576x1024) = ~$0.009
- **5:4** (960x768) = ~$0.011
- **21:9** (1344x576) = ~$0.012
- **4:3** (1024x768) = ~$0.012
- **3:2** (1152x768) = ~$0.013
- **16:9** (1280x720) = ~$0.014
- **1:1** (1024x1024) = ~$0.015
- **16:9** (1920x1080) = ~$0.030

**Tips for maximum savings:**

- Use **9:16** (portrait) for cheapest at ~$0.009/image, then crop if needed
- Use `go_fast: true` for drafts/test images
- Reduce `num_inference_steps` (10-15 is often sufficient for testing)
- Lower `output_quality` to 90-95 for web use
- Generate once, use multiple times
- At $0.009/image = 111 images for $1!

---

## Quality Control

**Always review generated images for:**

- Professional appearance
- Brand alignment (blue/white, modern, clean)
- No watermarks or text artifacts
- Appropriate composition
- Clear focus and lighting

**Red flags:**

- Distorted faces or objects
- Text within image (often garbled)
- Brand logos (potential copyright)
- Inconsistent style

---

## Troubleshooting

### "Authentication failed" Error

```bash
# Check token is set
grep REPLICATE_API_TOKEN .env.api

# Verify token is valid at replicate.com/account
```

### "Generation timed out" Error

- Increase timeout in your code (default is 60s, try 120s)
- Try during off-peak hours
- Simplify the prompt (complex prompts take longer)

### Poor Quality Results

**Common fixes:**

1. Increase `num_inference_steps` (28 -> 50)
2. Increase `output_quality` (90 -> 100)
3. Add more specific details to prompt
4. Disable `go_fast` for higher quality
5. Try different aspect ratios for composition

### Upload Fails

- Check file size is under 10MB (pre-compression limit)
- Ensure MIME type is supported: jpeg, jpg, png, webp, gif
- Verify `BLOG_API_KEY` is correct

---

## Quick Reference

```bash
# Generate image (default 1200x630 - blog featured)
yarn tsx .claude/skills/ai-image-generation/scripts/generate-ai-image.ts "your prompt"

# Generate with specific dimensions
yarn tsx .claude/skills/ai-image-generation/scripts/generate-ai-image.ts "your prompt" output.png 1200 630  # Blog featured
yarn tsx .claude/skills/ai-image-generation/scripts/generate-ai-image.ts "your prompt" output.png 1024 1024 # Square
yarn tsx .claude/skills/ai-image-generation/scripts/generate-ai-image.ts "your prompt" output.png 1920 1080 # Widescreen

# Upload to Supabase Storage
curl -s -X POST http://localhost:3000/api/blog/images/upload \
  -H "x-api-key: $API_KEY" \
  -F "file=@image.png" \
  -F "alt_text=Description"

# Check Replicate token
grep REPLICATE_API_TOKEN .env.api
```

## Related Skills

- `/blog-publish` - Blog publishing workflow with SEO
- `/blog-edit` - Edit existing blog posts
