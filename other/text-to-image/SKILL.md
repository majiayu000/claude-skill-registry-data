---
name: text-to-image
description: generate images from text descriptions. It provides integration with Tencent Hunyuan's text-to-image API, supporting multiple styles, sizes, and output formats. Commonly used for retrieving/generating application asset images.
---

# Text To Image

## Overview

Generate high-quality images from text descriptions using Tencent Hunyuan's text-to-image API. This skill enables creating images with customizable parameters including size, quality, style, and output format.

## When to Use This Skill

Use this skill when:
- Image generation from text descriptions
- Visual content creation
- Concept visualization
- Artistic image generation
- Custom illustrations

## Quick Start

### Basic Usage

To generate an image, use the `generate_image.py` script:

```bash
python3 scripts/generate_image.py "图片描述"
```

Then you can visit it by `/{filename}` via HTTP protocol in application codes.

**⚠️ Important Note:**
- The API endpoints required by this script do not support parallel execution and must be called one by one sequentially. Parallel calls will result in execution failures.
- If an execution fails, retrying the request.

### Common Options

```bash
# High quality image with custom size
python3 scripts/generate_image.py "未来城市" --size 768x1280 --quality high

# Add custom watermark and enable prompt revision
python3 scripts/generate_image.py "夕阳下的海滩" --footnote "我的水印" --revise

# Generate multiple images
python3 scripts/generate_image.py "可爱的小猫" --n 3

# Transparent background
python3 scripts/generate_image.py "logo设计" --background transparent

# Save response to file
python3 scripts/generate_image.py "山水画" --output result.json
```

## Image Generation Workflow

### Step 1: Understand User Requirements

Analyze the user's request to determine:
1. **Prompt**: What image should be generated?
2. **Size**: What dimensions are needed? (640x1408, 704x1344, 768x1280, 832x1216, 896x1152, 960x1088, 1024x1024, 1088x960, 1152x896, 1216x832, 1280x768, 1344x704, 1408x640)
3. **Quality**: What quality level is appropriate? (low, medium, high)
4. **Style**: Any specific style requirements?
5. **Format**: What output format? (png, webp, jpeg)
6. **Quantity**: How many images to generate?

### Step 2: Prepare Parameters

Based on requirements, select appropriate parameters:

**Size Selection:**
- `640x1408` - Ultra tall portrait
- `704x1344` - Very tall portrait
- `768x1280` - Tall portrait
- `832x1216` - Portrait
- `896x1152` - Portrait
- `960x1088` - Portrait
- `1024x1024` - Square images (default, good for general use)
- `1088x960` - Landscape
- `1152x896` - Landscape
- `1216x832` - Landscape
- `1280x768` - Wide landscape
- `1344x704` - Very wide landscape
- `1408x640` - Ultra wide landscape

**Quality Selection:**
- `low` - Fast generation, lower quality
- `medium` - Balanced (default)
- `high` - Best quality, slower generation

**Format Selection:**
- `png` - Best quality, larger file size (default)
- `webp` - Good balance of quality and size
- `jpeg` - Smaller file size, lossy compression

**Optional Enhancements:**
- Use `--revise` to enable automatic prompt improvement
- Use `--footnote` to add custom watermarks (max 16 characters)
- Use `--background transparent` for transparent backgrounds

### Step 3: Execute Generation

Run the `generate_image.py` script with selected parameters:

```bash
python3 .codebuddy/skills/text-to-image/scripts/generate_image.py "prompt" [options]
```

### Step 4: Handle Response

The script will:
1. Call the API with specified parameters
2. Display the response JSON
3. Extract and display image URLs
4. Show revised prompts (if `--revise` was used)

**Success Response Example:**
```json
{
  "code": 0,
  "msg": "OK",
  "requestId": "...",
  "data": {
    "created": 1761902312,
    "data": [
      {
        "url": "https://...",
        "revised_prompt": "..."
      }
    ]
  }
}
```

### Step 5: Present Results to User

After successful generation:
1. Show the image URL(s)
2. If `--revise` was used, show the revised prompt
3. Provide context about the generated image
4. Offer to generate variations if needed

## Advanced Features

### Prompt Revision

Enable automatic prompt improvement for better results:

```bash
python3 scripts/generate_image.py "城市" --revise
```

The API will:
- Analyze the original prompt
- Enhance it with details about composition, lighting, style
- Generate a more detailed image
- Return both the original and revised prompts

### Multiple Images

Generate multiple variations in one request:

```bash
python3 scripts/generate_image.py "抽象艺术" --n 3
```

**Note**: Each image counts toward API usage.

### Custom Watermarks

Add business watermarks (Hunyuan model only):

```bash
python3 scripts/generate_image.py "产品照片" --footnote "品牌名称"
```

**Limitation**: Maximum 16 characters.

### Compression Control

Adjust output file size with compression:

```bash
python3 scripts/generate_image.py "风景照" --output-compression 80
```

**Range**: 0 (no compression) to 100 (maximum compression).

### API Request Failures

If the API request fails:
- Check network connectivity
- Verify API key is valid
- Check API endpoint availability
- Review error message in response

### Invalid Parameters

If parameters are invalid:
- Verify size is one of: 640x1408, 704x1344, 768x1280, 832x1216, 896x1152, 960x1088, 1024x1024, 1088x960, 1152x896, 1216x832, 1280x768, 1344x704, 1408x640
- Verify quality is one of: low, medium, high
- Verify format is one of: png, webp, jpeg
- Verify footnote is ≤ 16 characters
- Verify n is between 1-10

## Best Practices

### Prompt Writing

**Good prompts are:**
- Specific and detailed
- Include style, composition, lighting details
- Use descriptive adjectives
- Specify desired mood or atmosphere

**Example:**
- ❌ Bad: "一只猫"
- ✅ Good: "一只橘色的短毛猫坐在窗台上，温暖的阳光从窗外照进来，背景是模糊的室内环境"

### Parameter Selection

**For production use:**
- Use `--quality high` for final outputs
- Use `--revise` for better prompt interpretation
- Use `--output-format webp` for web optimization
- Save responses with `--output` for record keeping

**For testing/iteration:**
- Use `--quality medium` for faster generation
- Use `--n` to generate multiple variations
- Experiment with different sizes

### Resource Management

**Token efficiency:**
- Longer prompts consume more input tokens
- Higher quality settings may affect generation time
- Multiple images (--n) multiply token usage

**File management:**
- Images are hosted on cloud storage
- URLs are temporary (check expiration)
- Download and save important images locally

## Resources

### scripts/generate_image.py

Python script for calling the Tencent Hunyuan text-to-image API. Handles:
- Parameter validation
- Request construction
- Response parsing
- Error handling

**Dependencies**: `requests` library (install with `pip install requests`)

### references/api_reference.md

Comprehensive API documentation including:
- Complete parameter specifications
- Response structure details
- Field descriptions and constraints
- Request/response examples
- Error handling guidance

Load this reference when need:
- Detailed parameter information
- API response structure details
- Advanced configuration options
- Troubleshooting API issues

## Common Use Cases

### 1. Quick Image Generation

**User request**: "Generate an image of a sunset over the ocean"

**Action**:
```bash
python3 scripts/generate_image.py "夕阳下的海洋，温暖的橙色和粉色天空，平静的海面反射着落日的光芒"
```

### 2. High-Quality Production Image

**User request**: "Create a high-quality landscape image for a website banner"

**Action**:
```bash
python3 scripts/generate_image.py "壮丽的山脉风景，清晨的薄雾，柔和的光线" \
  --size 1280x768 \
  --quality high \
  --revise \
  --output-format webp
```

### 3. Multiple Variations

**User request**: "Generate several versions of a logo concept"

**Action**:
```bash
python3 scripts/generate_image.py "现代简约的科技公司logo，蓝色和白色配色" \
  --n 3 \
  --background transparent \
  --revise
```

### 4. Custom Watermarked Image

**User request**: "Create a product photo with our brand watermark"

**Action**:
```bash
python3 scripts/generate_image.py "专业的产品摄影，白色背景，柔和的工作室灯光" \
  --quality high \
  --footnote "品牌名称" \
  --revise
```

## Workflow Integration

When request image generation:

1. **Clarify requirements** if the prompt is vague
2. **Select appropriate parameters** based on use case
3. **Execute generation** using the script
4. **Present results** with image URLs
5. **Offer iterations** if wants variations

**Example conversation flow:**

```
User: "Generate an image of a futuristic city"

Assistant: I'll generate a futuristic city image for you. Let me use high quality
and enable prompt revision for better results.

[Executes: python3 scripts/generate_image.py "未来城市，高耸的摩天大楼，
流线型建筑，悬浮的交通工具，霓虹灯光" --quality high --revise]

I've generated the image. Here's the result:
- Image URL: https://...
- Revised prompt: "一个未来城市的全景景观，采用极致真实的摄影风格..."

Would you like me to generate variations with different styles or sizes?
```

## Notes

- Use `--revise` for better prompt interpretation and image quality
- Recommend appropriate sizes based on use case (banner, portrait, square)
- Present image URLs clearly to the user
- Offer to generate variations if the first result doesn't meet expectations
- Save important responses with `--output` for record keeping
