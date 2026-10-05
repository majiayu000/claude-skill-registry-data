---
name: generate-image-by-image
description: Edit and transform existing images based on text descriptions. It provides integration with Tencent Hunyuan's image editing API, supporting style transfer, background replacement, color adjustment, and various image modifications. Commonly used for image enhancement, style conversion, and creative editing.
---

# Generate Image By Image

## Overview

Edit and transform existing images using text descriptions with Tencent Hunyuan's generate-image-by-image API. This skill enables intelligent image editing with customizable parameters including editing strength, size, quality, style, and output format.

## When to Use This Skill

Use this skill when:
- Image editing and enhancement
- Style transfer and artistic conversion
- Background replacement or modification
- Color and lighting adjustments
- Creative image transformations
- Product photo optimization

## Quick Start

### Basic Usage

To edit an image, use the `edit_image.py` script:

```bash
python3 scripts/edit_image.py "编辑描述" --image-url "图片路径"
```

Then you can visit the edited image by `/{filename}` via HTTP protocol in application codes.

**⚠️ Important Note:**
- The API endpoints required by this script do not support parallel execution and must be called one by one sequentially. Parallel calls will result in execution failures.
- If an execution fails, retrying the request.
- Input images must be in supported formats (PNG, JPEG, WebP)
- Maximum file size limitations apply (check API documentation)

### Common Options

```bash
# High quality editing with custom size
python3 scripts/edit_image.py "转换为油画风格" --image-url portrait.jpg --size 768x1280 --quality high

# Add custom watermark and enable prompt revision
python3 scripts/edit_image.py "专业后期处理" --image-url photo.jpg --footnote "我的水印" --revise

# Generate multiple edited versions
python3 scripts/edit_image.py "不同光线效果" --image-url landscape.png --n 3

# Adjust editing strength
python3 scripts/edit_image.py "轻微色彩增强" --image-url selfie.jpg --strength 0.3

# Background processing
python3 scripts/edit_image.py "去除背景" --image-url product.jpg --background transparent

# Save response to file
python3 scripts/edit_image.py "艺术化处理" --image-url artwork.png --output result.json
```

## Image Editing Workflow

### Step 1: Understand User Requirements

Analyze the user's request to determine:
1. **Input Image**: What image needs to be edited?
2. **Edit Description**: What changes should be made?
3. **Editing Strength**: How strong should the modifications be? (0.0-1.0)
4. **Size**: What dimensions are needed? (640x1408, 704x1344, 768x1280, 832x1216, 896x1152, 960x1088, 1024x1024, 1088x960, 1152x896, 1216x832, 1280x768, 1344x704, 1408x640)
5. **Quality**: What quality level is appropriate? (low, medium, high)
6. **Style**: Any specific style requirements?
7. **Format**: What output format? (png, webp, jpeg)
8. **Quantity**: How many edited versions to generate?

### Step 2: Prepare Parameters

Based on requirements, select appropriate parameters:

**Editing Strength Selection:**
- `0.1-0.3` - Subtle adjustments (color correction, light enhancement)
- `0.4-0.6` - Moderate editing (style adjustments, background changes)
- `0.7-0.9` - Strong transformation (style transfer, major modifications)
- `1.0` - Maximum transformation (complete regeneration)

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
- `low` - Fast processing, lower quality
- `medium` - Balanced (default)
- `high` - Best quality, slower processing

**Format Selection:**
- `png` - Best quality, larger file size (default)
- `webp` - Good balance of quality and size
- `jpeg` - Smaller file size, lossy compression

**Optional Enhancements:**
- Use `--revise` to enable automatic prompt improvement
- Use `--footnote` to add custom watermarks (max 16 characters)
- Use `--background transparent` for transparent backgrounds

### Step 3: Execute Editing

Run the `edit_image.py` script with selected parameters:

```bash
python3 .codebuddy/skills/generate-image-by-image/scripts/edit_image.py "prompt" --image-url "path" [options]
```

### Step 4: Handle Response

The script will:
1. Encode the input image to base64
2. Call the API with specified parameters
3. Display the response JSON
4. Extract and display edited image URLs
5. Show revised prompts (if `--revise` was used)

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

After successful editing:
1. Show the edited image URL(s)
2. If `--revise` was used, show the revised prompt
3. Provide context about the editing performed
4. Offer to generate variations with different strengths if needed

## Advanced Features

### Prompt Revision

Enable automatic prompt improvement for better editing results:

```bash
python3 scripts/edit_image.py "增强图片质量" --image-url photo.jpg --revise
```

The API will:
- Analyze the original editing prompt
- Enhance it with details about specific modifications
- Generate more precise edits
- Return both the original and revised prompts

### Multiple Edited Versions

Generate multiple variations in one request:

```bash
python3 scripts/edit_image.py "不同艺术风格" --image-url portrait.jpg --n 3
```

**Note**: Each edited image counts toward API usage.

### Custom Watermarks

Add business watermarks to edited images:

```bash
python3 scripts/edit_image.py "专业后期处理" --image-url product.jpg --footnote "品牌名称"
```

**Limitation**: Maximum 16 characters.

### Editing Strength Control

Fine-tune the intensity of modifications:

```bash
python3 scripts/edit_image.py "轻微美化" --image-url selfie.jpg --strength 0.2
```

**Range**: 0.0 (minimal changes) to 1.0 (maximum transformation).

### Compression Control

Adjust output file size with compression:

```bash
python3 scripts/edit_image.py "优化图片" --image-url large_photo.jpg --output-compression 80
```

**Range**: 0 (no compression) to 100 (maximum compression).

## Error Handling

### API Request Failures

If the API request fails:
- Check network connectivity
- Verify API key is valid
- Check API endpoint availability
- Verify input image format and size
- Review error message in response

### Invalid Input Image

If the input image is invalid:
- Verify the image file exists
- Check if the image format is supported (PNG, JPEG, WebP)
- Ensure the image file is not corrupted
- Check if the image size is within limits

### Invalid Parameters

If parameters are invalid:
- Verify size is one of the supported dimensions
- Verify quality is one of: low, medium, high
- Verify format is one of: png, webp, jpeg
- Verify footnote is ≤ 16 characters
- Verify n is between 1-10
- Verify strength is between 0.0-1.0

## Best Practices

### Prompt Writing

**Good editing prompts are:**
- Specific about the desired changes
- Include details about style, color, lighting modifications
- Use action verbs to describe transformations
- Specify the desired visual outcome

**Example:**
- ❌ Bad: "改善这张图片"
- ✅ Good: "增强色彩饱和度,调整曝光使图片更明亮,添加温暖的色调,保持人物面部细节清晰"

### Parameter Selection

**For production use:**
- Use `--quality high` for final outputs
- Use `--revise` for better prompt interpretation
- Use `--output-format webp` for web optimization
- Save responses with `--output` for record keeping
- Choose appropriate `--strength` based on editing needs

**For testing/iteration:**
- Use `--quality medium` for faster processing
- Use `--n` to generate multiple variations
- Experiment with different strength values
- Test different sizes for optimal results

### Resource Management

**Token efficiency:**
- Longer prompts consume more input tokens
- Higher quality settings may affect processing time
- Multiple images (--n) multiply token usage
- Larger input images may require more processing

**File management:**
- Edited images are hosted on cloud storage
- URLs are temporary (check expiration)
- Download and save important edited images locally
- Keep original images as backup

## Resources

### scripts/edit_image.py

Python script for calling the Tencent Hunyuan generate-image-by-image API. Handles:
- Input image encoding to base64
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

### 1. Style Transfer

**User request**: "Convert this photo to Van Gogh painting style"

**Action**:
```bash
python3 scripts/edit_image.py "转换为梵高风格的油画,保持原有构图和主要元素" \
  --image-url photo.jpg \
  --strength 0.7 \
  --quality high \
  --revise
```

### 2. Background Replacement

**User request**: "Replace the background with a modern office environment"

**Action**:
```bash
python3 scripts/edit_image.py "将背景替换为现代办公室环境,保持人物清晰" \
  --image-url portrait.png \
  --strength 0.6 \
  --quality high \
  --revise
```

### 3. Color and Lighting Enhancement

**User request**: "Enhance the colors and improve lighting in this landscape photo"

**Action**:
```bash
python3 scripts/edit_image.py "增强色彩饱和度,改善光线平衡,提升整体亮度" \
  --image-url landscape.jpg \
  --strength 0.4 \
  --quality high \
  --revise
```

### 4. Product Photo Optimization

**User request**: "Optimize this product photo for e-commerce"

**Action**:
```bash
python3 scripts/edit_image.py "专业产品摄影后期处理,白色背景,完美光线,增强产品细节" \
  --image-url product.jpg \
  --background transparent \
  --quality high \
  --footnote "品牌名称" \
  --strength 0.5 \
  --output-format webp
```

### 5. Artistic Transformation

**User request**: "Transform this photo into a watercolor painting"

**Action**:
```bash
python3 scripts/edit_image.py "转换为水彩画风格,柔和的色彩过渡,艺术化处理" \
  --image-url photo.jpg \
  --strength 0.8 \
  --quality high \
  --revise
```

## Workflow Integration

When request image editing:

1. **Clarify requirements** if the editing request is vague
2. **Verify input image** exists and is accessible
3. **Select appropriate parameters** based on editing needs
4. **Execute editing** using the script
5. **Present results** with edited image URLs
6. **Offer iterations** if wants different strength or variations

**Example conversation flow:**

```
User: "Edit this image to make it look more professional"

A: I'll help you enhance this image for a more professional look. Let me apply 
professional photo editing techniques with high quality settings.

[Executes: python3 scripts/edit_image.py "专业摄影后期处理,增强清晰度,
调整色彩平衡,改善光线,提升整体质感" --image-url image.jpg --quality high 
--strength 0.5 --revise]

I've processed your image with professional editing techniques. Here's the result:
- Edited Image URL: https://...
- Revised prompt: "专业摄影后期处理,采用高端商业摄影标准..."

The editing enhanced clarity, improved color balance, and optimized lighting. 
Would you like me to try a different editing strength or generate additional variations?
```

## Notes

- Always verify input image path before processing
- Use `--revise` for better prompt interpretation and editing quality
- Recommend appropriate strength values based on editing type
- Present edited image URLs clearly to the user
- Offer to generate variations with different parameters if needed
- Save important responses with `--output` for record keeping
- Consider file size and format optimization for different use cases