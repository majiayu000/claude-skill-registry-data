---
name: nano-banana-assets
description: Generate any kind of visual asset using OpenRouter's Nano Banana Pro (Google Gemini 3 Pro Image Preview). Handles images, graphics, illustrations, icons, banners, backgrounds, UI elements, stickers, characters, and more. Flexible and adaptable to any creative request.
license: MIT
metadata:
  author: shelbeely
  version: "1.0.0"
  category: design-and-media
  keywords: image-generation, assets, web-design, branding, openrouter, gemini, flexible, creative
compatibility: Requires internet access and OpenRouter API key. Works with any agent that can make HTTP API calls.
allowed-tools: fetch http-client curl bash
---

# Nano Banana Assets Generator Skill

This skill enables AI agents to generate **any kind of visual asset** using OpenRouter's Nano Banana Pro model (Google Gemini 3 Pro Image Preview). 

**Use this skill when users request:**
- Any image, graphic, or visual content
- Icons, logos, banners, backgrounds, UI elements
- Illustrations, characters, stickers, avatars
- Product mockups, designs, compositions
- Social media graphics, marketing materials
- Creative artwork of any style or type

**Key Philosophy:** Be flexible and creative. Adapt to the user's needs rather than forcing predefined templates.

## About Nano Banana Pro

Nano Banana Pro is Google's most advanced image-generation and editing model, built on Gemini 3 Pro. It extends the original Nano Banana with significantly improved multimodal reasoning, real-world grounding, and high-fidelity visual synthesis.

**Key Features:**
- **Multi-Image Support**: Can blend and edit up to **14 reference images** per request
- **Identity Preservation**: Maintains consistency across up to **5 distinct subjects/characters** simultaneously
- **Multi-Image Blending**: Consistent style across multiple generations with superior quality
- **Text Rendering**: Industry-leading text placement in images (94-96% accuracy) with multilingual layouts
- **Fine-Grained Controls**: Localized edits, lighting adjustments, focus control, camera transformations
- **Flexible Outputs**: Support for 2K/4K outputs and multiple aspect ratios (1:1, 16:9, 9:16, 4:3, 3:4, 21:9, 9:21, 2:3, 3:2, 5:4, 4:5)
- **Context-Rich Graphics**: From infographics and diagrams to cinematic composites
- **Conversational Editing**: Iterative, multi-turn editing workflows for refinement
- **Photorealistic Quality**: Advanced multimodal reasoning for professional-quality outputs

**Understanding Image Limits:**
- **Reference Images**: You can include up to 14 reference images in a single API request
- **Identity Subjects**: The model can maintain consistency for up to 5 different characters/subjects within those references
- **Series Generation**: For generating series of many images (10+, 20+, 50+), use the **sliding window technique** (detailed in section 5 below) to maintain visual consistency across the entire collection by using the most recent 5-14 generated images as references for each new image.

## Known Limitations

### ⚠️ Transparent Backgrounds Not Supported

**IMPORTANT:** Nano Banana Pro (Google Gemini 3 Pro Image Preview) **does not generate images with true alpha transparency**. This is a model limitation, not a configuration issue.

**What Actually Happens:**
- Generated images are RGB PNG files (color type 2) without alpha channels
- When you request "transparent background," the model paints a solid color or pattern
- The background may appear white, gray, or have a checkered pattern painted as pixels
- The resulting PNG files cannot be overlaid on other backgrounds with transparency

**Implications for Agents:**
- ❌ **Do NOT promise users transparent backgrounds** or alpha channel support
- ❌ **Do NOT include "transparent background" in prompts** - it creates fake checkered patterns
- ✅ **DO use chroma key colors** for easy background removal (#00FF00 bright green recommended)
- ✅ **DO inform users** that post-processing is needed for true transparency

**Recommended Approach: Chroma Key Backgrounds**

When users need transparency, use a **bright chroma key color** that can be easily removed:

**Best Chroma Key Colors:**
1. **Bright Green (#00FF00)** - Most common, rarely appears in subjects
2. **Bright Magenta (#FF00FF)** - Alternative if subject contains green
3. **Bright Blue (#0000FF)** - For subjects with green/magenta elements

**Example Prompts:**
```
- "Solid bright green background (#00FF00) for chroma key removal"
- "Pure #00FF00 green background, flat and uniform"
- "Subject isolated on solid bright green (#00FF00) chroma key background"
```

**Why This Works:**
- ✅ Model generates clean, uniform color fills
- ✅ No fake checkered patterns painted as pixels
- ✅ Easy to select and remove using color-based tools
- ✅ Chroma key removal is cleaner than edge detection
- ✅ Works perfectly with standard video/photo editing workflows

**Automated Scripts Available:**

The skill includes several helper scripts in `scripts/` directory for various workflows:

**1. Single Asset with Transparency (Recommended):**
```bash
cd .github/skills/nano-banana-assets/scripts
python generate_with_transparency.py "Your prompt" "1:1" "1024x1024"
```
- ✅ Generates with #00FF00 chroma key (no fake checkered patterns)
- ✅ Removes background with rembg (AI-powered)
- ✅ Outputs transparent RGBA PNG files
- ✅ Saves both transparent and original versions

**2. Batch Generation:**
```bash
# From config file
python batch_generate.py --config example_batch_config.json --transparent

# From prompts
python batch_generate.py --prompts "Icon 1" "Icon 2" "Icon 3" --transparent
```
- ✅ Generate multiple assets at once
- ✅ Optional transparency support
- ✅ Progress tracking and error handling

**3. Post-Process Existing Images:**
```bash
# Remove backgrounds from already-generated images
python remove_backgrounds.py --directory ./images/

# Or with chroma key
python remove_backgrounds.py --chroma-key "#00FF00" image.png
```
- ✅ AI-powered removal with rembg
- ✅ Chroma key color removal
- ✅ Batch directory processing

**See `scripts/README.md` for complete documentation and examples.**

**Requirements:**
```bash
pip install rembg requests Pillow
```

**Post-Processing Background Removal:**

**Recommended: Using rembg (AI-powered removal)**

The **rembg** tool provides automated, high-quality background removal that works with any background color (including chroma key backgrounds):

1. **Install rembg:**
   ```bash
   pip install rembg[gpu]  # For GPU acceleration
   # or
   pip install rembg       # CPU only
   ```

2. **Remove background (single file):**
   ```bash
   rembg i input.png output.png
   ```

3. **Batch process all files:**
   ```bash
   # Process all PNG files in directory
   for file in *.png; do
     rembg i "$file" "transparent_$file"
   done
   
   # Or use rembg's built-in batch processing
   rembg p input_folder output_folder
   ```

4. **Python API (for integration):**
   ```python
   from rembg import remove
   from PIL import Image
   
   input_path = 'input.png'
   output_path = 'output.png'
   
   with open(input_path, 'rb') as i:
       with open(output_path, 'wb') as o:
           input_data = i.read()
           output_data = remove(input_data)
           o.write(output_data)
   ```

**Why rembg is Best:**
- ✅ AI-powered edge detection (U²-Net model)
- ✅ Works with any background color (chroma key or natural)
- ✅ High-quality results with fine details (hair, fur, transparent objects)
- ✅ Fully automated - no manual selection needed
- ✅ Fast batch processing
- ✅ Open source and free

**Alternative: Manual Chroma Key Removal**

If you prefer manual control or don't want to install rembg:

1. **Using ImageMagick (CLI):**
   ```bash
   # Remove bright green background with tolerance
   convert input.png -fuzz 5% -transparent "#00FF00" output.png
   
   # Batch process all files
   for file in *.png; do
     convert "$file" -fuzz 5% -transparent "#00FF00" "transparent_$file"
   done
   ```

2. **Using Photoshop:**
   - Select → Color Range → Sample the green background
   - Adjust tolerance as needed
   - Delete selection → Save as PNG with transparency

3. **Using GIMP:**
   - Colors → Color to Alpha → Select the green (#00FF00)
   - Export as PNG with alpha channel

4. **Using FFmpeg (for batch):**
   ```bash
   ffmpeg -i input.png -filter_complex "colorkey=0x00FF00:0.3:0.2" output.png
   ```

**Not Recommended:**

1. **Plain White/Gray Backgrounds:**
   - ⚠️ Harder to remove if subject has similar colors
   - Requires more manual editing around edges

2. **Request "Transparent" (Avoid):**
   - ❌ Creates fake checkered patterns painted as pixels
   - ❌ Very difficult to remove cleanly

**What to Tell Users:**
```
Note: Generated images have solid backgrounds (RGB PNG format). 
The model cannot create true transparent backgrounds (RGBA). 

For transparency removal, I recommend using rembg (AI-powered):
  pip install rembg
  rembg i input.png output.png

Or for manual chroma key removal with the bright green (#00FF00) background:
  convert image.png -fuzz 5% -transparent "#00FF00" output.png

The chroma key approach avoids the "fake checkered pattern" issue.
```

## Core Capabilities

1. **Generate Single Assets**: Create icons, banners, backgrounds, UI elements, and more
2. **Generate Asset Packs**: Create cohesive sets of related assets with consistent branding
3. **Edit Existing Assets**: Apply fine-grained edits to existing images
4. **Ensure Brand Consistency**: Analyze and maintain visual identity across multiple assets
5. **Generate Consistent Series (6+ Images)**: Create large image series maintaining consistency using the sliding window technique

## Prerequisites

Before using this skill, ensure you have:

- OpenRouter API key (get one from https://openrouter.ai/)
- The API key should be stored as `OPENROUTER_API_KEY` environment variable
- Internet access to call the OpenRouter API

## API Configuration

### Base URL
```
https://openrouter.ai/api/v1/chat/completions
```

### Model
```
google/gemini-3-pro-image-preview
```

### Authentication
```
Authorization: Bearer <OPENROUTER_API_KEY>
```

## Core Operations

### 1. Generate a Single Asset

Use this when the user needs one specific asset (icon, banner, background, etc.).

**When to use:**
- User asks for "create an icon"
- User wants "generate a banner"
- User needs "make a background image"
- User requests any single graphic asset

**Steps:**
1. Collect requirements:
   - What type of asset (icon, banner, background, UI element, etc.)
   - Description/prompt (be detailed and specific)
   - Aspect ratio (1:1, 16:9, 9:16, 4:3, 21:9, etc.)
   - Resolution (1080x1080, 1920x1080, 2K, 4K)
   - Color palette (hex codes)
   - Any reference images or logos

2. Build the prompt using the **Six-Element Framework** (Google's recommended approach):
   ```
   Generate a high-quality [asset type] with the following specifications:
   
   Subject: [Who/what is in the image - be specific about physical attributes, elements]
   Composition: [Framing, perspective, layout - e.g., "centered", "rule of thirds", "close-up", "wide shot"]
   Action: [What is happening - static pose, interaction, movement]
   Location: [Setting, environment, context - where the scene takes place]
   Style: [Overall aesthetic - photorealistic, flat design, minimalist, bold, etc.]
   Lighting: [Specific lighting setup - "soft diffused daylight", "dramatic side lighting", "golden hour", etc.]
   
   Camera Details: [Optional - "85mm lens", "shallow depth of field", "low angle", etc.]
   Materiality: [Optional - texture details like "matte finish", "brushed steel", "translucent glass"]
   
   Technical Specifications:
   Aspect Ratio: [ratio]
   Resolution: [resolution]
   Color Palette: [hex codes]
   
   Requirements:
   - Professional, web-ready quality
   - Modern and visually appealing design
   - Optimized for digital use
   - Clean and polished appearance
   ```

3. Make the API call (see API Call Format section below)

4. Extract generated images from response.choices[0].message.images array

5. Present the images to the user

**Example prompt (using Six-Element Framework):**
```
Generate a high-quality hero banner with the following specifications:

Subject: Abstract geometric shapes (floating hexagons, connecting lines, particles) creating a tech-forward atmosphere
Composition: Wide shot with visual weight on right side, negative space on left for text overlay, balanced with rule of thirds
Action: Subtle sense of movement with particles drifting upward, energy flowing through connecting lines
Location: Digital space with infinite depth, contemporary tech environment
Style: Modern minimalist with vibrant gradients, clean professional aesthetic suitable for SaaS landing page
Lighting: Soft ambient glow from gradient background, subtle rim lighting on geometric elements to create depth

Camera Details: Slight elevated perspective, as if viewing a 3D space, medium depth of field
Materiality: Gradient elements have smooth glass-like quality, geometric shapes with subtle metallic sheen

Technical Specifications:
Aspect Ratio: 16:9
Resolution: 1920x1080
Color Palette: #667EEA (primary blue), #764BA2 (deep purple), #F093FB (accent pink)

Requirements:
- Professional, web-ready quality
- Eye-catching yet not overwhelming
- Clear space on left third for headline text
- Optimized for digital use
```

### 2. Generate Asset Pack

Use this when the user needs multiple related assets maintaining brand consistency.

**When to use:**
- User asks for "social media kit"
- User wants "complete branding package"
- User needs "set of icons" or "icon set"
- User requests multiple related assets

**Steps:**
1. Collect requirements:
   - Overall purpose/description
   - List of asset types needed (e.g., "instagram-post", "facebook-cover", "icon-set")
   - Brand guidelines (style, tone, values)
   - Color palette
   - Logo file (if any)
   - Default aspect ratio and resolution

2. Build the prompt using the **Six-Element Framework**:
   ```
   Generate a complete, brand-consistent asset pack for web development:
   
   Project Description: [description]
   
   Asset Types to Generate:
   1. [asset type 1] - Subject: [...], Composition: [...], Style: [...]
   2. [asset type 2] - Subject: [...], Composition: [...], Style: [...]
   3. [asset type 3] - Subject: [...], Composition: [...], Style: [...]
   ...
   
   Brand Guidelines:
   Subject Matter: [What visual elements represent the brand]
   Composition Approach: [How elements should be arranged - balanced, dynamic, minimal, etc.]
   Visual Actions: [Static vs dynamic, energy level, mood]
   Contextual Environment: [Where these assets exist - digital, physical, abstract]
   Overall Style: [Aesthetic direction - minimalist, bold, elegant, playful, etc.]
   Lighting Treatment: [Consistent lighting approach across all assets]
   
   Camera & Materiality:
   [Any specific perspective or texture requirements]
   
   Brand Color Palette: [colors]
   Default Aspect Ratio: [ratio]
   Default Resolution: [resolution]
   
   Requirements:
   - All assets must maintain visual consistency
   - Follow the brand guidelines strictly
   - Use the provided color palette throughout
   - Professional, production-ready quality
   - Each asset should be optimized for its specific use case
   - Cohesive design language across all assets
   ```

3. Make the API call with reference images if provided

4. Extract all generated images from the response

5. Present each asset with its type/purpose labeled

**Example prompt (with Six-Element Framework):**
```
Generate a complete, brand-consistent asset pack for web development:

Project Description: Social media kit for an eco-friendly coffee brand targeting young professionals

Asset Types to Generate:
1. Instagram post (square, 1:1) - Subject: Coffee cup with natural elements, Composition: Centered product shot, Style: Warm and inviting
2. Instagram story (vertical, 9:16) - Subject: Brewing process with eco messaging, Composition: Vertical flow top to bottom, Style: Dynamic and engaging
3. Facebook cover (wide banner) - Subject: Coffee beans and sustainable packaging, Composition: Wide panoramic layout, Style: Professional and earthy
4. Twitter header (wide banner) - Subject: Brand story visual elements, Composition: Horizontal narrative, Style: Clean and modern
5. App icon (square, simple) - Subject: Stylized coffee cup or bean, Composition: Centered symbol, Style: Minimalist and recognizable

Brand Guidelines:
Subject Matter: Natural coffee elements (beans, cups, plants), sustainable packaging, organic textures, eco-friendly themes
Composition Approach: Clean, balanced layouts with breathing room, focus on product and nature harmony
Visual Actions: Static, serene presentations with subtle organic movement suggestions
Contextual Environment: Natural light settings, wooden surfaces, green plants, sustainable materials backdrop
Overall Style: Minimalist, nature-inspired, earthy aesthetics. Modern organic fusion with professional polish.
Lighting Treatment: Warm, soft natural light (golden hour quality), gentle shadows, inviting and cozy atmosphere

Camera & Materiality:
Slight top-down or 3/4 angles for product shots, natural wood grain textures, matte ceramic finishes, organic paper textures

Brand Color Palette: #2ECC71 (eco green), #27AE60 (forest), #8B4513 (coffee brown), #F5F5DC (cream)
Default Aspect Ratio: 1:1
Default Resolution: 1080x1080

Requirements:
- All assets must maintain visual consistency
- Follow the brand guidelines strictly
- Use the provided color palette throughout
- Professional, production-ready quality
- Each asset should be optimized for its specific use case
- Cohesive design language across all assets
```

### 3. Edit Existing Asset

Use this when the user wants to modify an existing image.

**When to use:**
- User says "edit this image"
- User wants "adjust the lighting"
- User needs "change the colors"
- User requests any modification to an existing asset

**Steps:**
1. Get the source image (URL or base64 data)

2. Collect edit requirements:
   - Specific edit instructions (be precise)
   - Elements to preserve (logo, text, specific objects)
   - Target aspect ratio (if changing)
   - Target resolution (if changing)

3. Build the prompt with detailed editing instructions:
   ```
   Edit the provided image with the following instructions:
   
   Edit Instructions: [Specific edits using the Six-Element Framework]
   - Subject modifications: [What elements to add, remove, or change]
   - Composition adjustments: [Layout, framing, perspective changes]
   - Action changes: [Modify movement, energy, or static elements]
   - Location alterations: [Background, environment, context changes]
   - Style refinements: [Aesthetic adjustments, visual treatment]
   - Lighting adjustments: [Specific lighting changes - "warmer tones", "increase contrast", "soften shadows"]
   
   Camera & Detail Changes:
   - [Optional: focal point, depth of field, perspective adjustments]
   - [Optional: texture, materiality, surface quality changes]
   
   Preserve These Elements: [elements to keep]
   Target Aspect Ratio: [ratio]
   Target Resolution: [resolution]
   
   Editing Requirements:
   - Apply edits precisely as instructed
   - Maintain image quality and professional appearance
   - Preserve specified elements without alteration
   - Ensure smooth transitions and natural-looking results
   - Output should be web-ready and optimized
   ```

4. Make the API call with the source image included in the content array

5. Extract edited image from the response

6. Present the edited image to the user

**Example prompt with image (using Six-Element Framework):**
```
Edit the provided image with the following instructions:

Edit Instructions:
- Subject modifications: Enhance the main product to appear more premium, add subtle glow effect around edges
- Composition adjustments: Maintain current centered composition but add slight depth with background blur
- Action changes: Keep static presentation but add subtle energy with light particles
- Location alterations: Keep current setting but add warmer, more inviting environmental tones
- Style refinements: Shift toward more premium, upscale aesthetic while maintaining brand identity
- Lighting adjustments: Adjust to golden hour lighting quality - warm amber tones from top-left, increase contrast by 20%, soften hard shadows to create more inviting mood, add subtle vignette effect around edges for focus

Camera & Detail Changes:
- Simulate shallow depth of field effect (85mm equivalent)
- Enhance material quality: make surfaces appear more premium with subtle highlights
- Add subtle warm color grading throughout

Preserve These Elements: logo in top-left corner, main product in center, text overlay at bottom, brand colors in text elements

Editing Requirements:
- Apply edits precisely as instructed
- Maintain image quality and professional appearance
- Preserve specified elements without alteration
- Ensure smooth transitions and natural-looking results
- Output should be web-ready and optimized
```

### 4. Ensure Brand Consistency

Use this when the user wants to check if multiple assets follow brand guidelines.

**When to use:**
- User says "check these assets for consistency"
- User wants "review brand compliance"
- User needs "validate branding"
- User asks if assets "match the guidelines"

**Steps:**
1. Collect all assets to analyze (URLs or base64 data)

2. Get brand guidelines:
   - Detailed style requirements
   - Color palette (official brand colors)
   - Reference images showing desired style
   - Logo file
   - Typography preferences
   - Tone and values

3. Build the prompt:
   ```
   Analyze the following assets for brand consistency and provide recommendations:
   
   Brand Guidelines:
   [detailed guidelines]
   
   Brand Colors: [hex codes]
   
   Analysis Requirements:
   - Check adherence to brand guidelines
   - Verify consistent use of colors, typography, and style
   - Identify inconsistencies across assets
   - Provide specific recommendations for improvements
   - Suggest refinements to maintain brand identity
   - Ensure logo usage is consistent and appropriate
   - Verify visual cohesion across all assets
   
   I have [N] assets to analyze. Please review them for consistency.
   ```

4. Make the API call with all assets and reference images

5. Extract analysis text and any corrected images

6. Present the analysis with specific recommendations

**Example prompt:**
```
Analyze the following assets for brand consistency and provide recommendations:

Brand Guidelines:
- Style: Modern, minimalist, professional
- Tone: Trustworthy, innovative, forward-thinking
- Colors must be limited to the brand palette
- Logo must always be visible and properly sized
- Typography: Clean, sans-serif, high readability
- Imagery: High-tech, futuristic, abstract geometric patterns preferred

Brand Colors: #667EEA, #764BA2, #FFFFFF, #2D3748

Analysis Requirements:
- Check adherence to brand guidelines
- Verify consistent use of colors, typography, and style
- Identify inconsistencies across assets
- Provide specific recommendations for improvements
- Suggest refinements to maintain brand identity
- Ensure logo usage is consistent and appropriate
- Verify visual cohesion across all assets

I have 4 assets to analyze. Please review them for consistency.
```

### 5. Generate Consistent Series (More than 5 Images)

Use this when the user needs to generate **a large series of images** (10+, 20+, 50+) that must maintain consistency across the entire series.

**Background**: Nano Banana Pro can process up to **14 reference images** per request and maintain identity for up to **5 distinct subjects/characters**. For generating extensive series (many more images than can be used as references), use a **sliding window approach** where you use the most recent 5-14 generated images as references for each new image.

**When to use:**
- User asks for "20+ icons in the same style"
- User wants "a storyboard with 15+ frames"
- User needs "30-day social media calendar with consistent branding"
- User requests any extensive image series (icon libraries, product catalogs, etc.)

**Steps:**

1. **Initial Setup**:
   - Collect series requirements:
     - Overall series description
     - Individual descriptions for each image
     - Brand guidelines and style requirements
     - Color palette
     - Aspect ratio and resolution
     - Any initial reference images or logo (up to 14 images)

2. **Generate First Image**:
   - Use any initial reference images provided
   - Include brand guidelines and color palette
   - This establishes the baseline style

3. **Generate Subsequent Images (Sliding Window)**:
   - For images 2-14: Use ALL previously generated images as references (accumulating)
   - For image 15 onwards: Use only the LAST 10-14 generated images as references (sliding window)
   - This maintains consistency while respecting the model's 14-image reference limit
   - Recommended: Use 10-12 recent images to leave room for logo/initial references

4. **Workflow Pattern**:

   **For each image in the series:**
   
   a. Build the prompt:
   ```
   Generate image [N] of [TOTAL] for this series:
   
   Series Context: [overall description]
   
   This Image: [specific description for this image]
   
   Brand Guidelines:
   [guidelines]
   
   Color Palette: [colors]
   Aspect Ratio: [ratio]
   Resolution: [resolution]
   
   Consistency Requirements:
   - Maintain the same visual style as the reference images
   - Use consistent design language, color treatment, and composition
   - Ensure this image feels like part of the same cohesive series
   - Professional, web-ready quality
   - Modern and polished appearance
   
   IMPORTANT: The reference images show the previously generated images in this series. Match their style, tone, and visual identity exactly while creating this new variation.
   ```
   
   b. Prepare reference images (up to 14 total):
   ```
   reference_images = []
   
   # Add logo if provided (takes 1 slot)
   if logo_file:
       reference_images.append(logo_file)
   
   # Add initial style references only for first image (up to 3-5 slots)
   if current_image == 1 and initial_references:
       reference_images.extend(initial_references[:5])  # Limit to first 5
   
   # Add previously generated images (sliding window approach)
   if generated_images:
       # Calculate how many slots remain (max 14 total)
       remaining_slots = 14 - len(reference_images)
       
       # For images 2-14: Use all previous images (if they fit)
       if current_image <= 14:
           reference_images.extend(generated_images[:remaining_slots])
       else:
           # For image 15+: Use last 10-12 images (sliding window)
           # Keep 2-4 slots for logo and initial references
           window_size = min(remaining_slots, 12)
           start_index = max(0, len(generated_images) - window_size)
           reference_images.extend(generated_images[start_index:])
   ```
   
   c. Make API call with reference images (max 14)
   
   d. Store the generated image for use in next iteration
   
   e. Repeat for next image

5. **Present results with clear tracking**:
   - Show each image with its number and description
   - Indicate which images were used as references
   - Confirm consistency across the series

**Example workflow for 20-icon series:**

```
User Request: "Create 20 minimalist weather icons with consistent style"

Your Workflow:

Step 1: Generate Icon 1 (Sunny)
---
Prompt: "Generate icon 1 of 20 for this series:

Series Context: Weather icon set with minimalist design. Clean lines, modern style, consistent 2px stroke weight, rounded line caps, monochrome design (#2D3748) on solid bright green (#00FF00) chroma key background for easy removal.

This Image: Sunny weather - sun with rays

Aspect Ratio: 1:1
Resolution: 512x512

Consistency Requirements:
- Professional, web-ready quality
- Modern and polished appearance
- Clean, simple design with consistent visual language"

References: [initial style guide images if any, logo if any]
[Make API call]
[Store generated icon 1]

Step 2: Generate Icon 2 (Cloudy)
---
Prompt: "Generate icon 2 of 20 for this series:

Series Context: Weather icon set with minimalist design, matching the previous icon's stroke weight and design language.

This Image: Cloudy weather - cloud shape

Consistency Requirements:
- Maintain the same visual style as the reference images
- Use consistent design language, stroke weight, line caps
- Ensure this icon feels like part of the same icon family

IMPORTANT: The reference images show the previously generated icons. Match their style exactly."

References: [logo if any, icon 1]
[Make API call]
[Store generated icon 2]

Steps 3-14: Generate Icons 3-14
---
Same process, accumulating all previous icons as references
- Icon 3 references: [logo, icons 1-2]
- Icon 4 references: [logo, icons 1-3]
- Icon 5 references: [logo, icons 1-4]
...
- Icon 14 references: [logo, icons 1-13] (at or near 14-image limit)

Step 15: Generate Icon 15 (Heavy Rain) - SLIDING WINDOW STARTS
---
Prompt: [same structure emphasizing consistency]

References: [logo, icons 4-14] ← Last 11 icons (11 + 1 logo = 12 references)
[Make API call]
[Store generated icon 15]

Steps 16-20: Generate Icons 16-20
---
Continue with sliding window:
- Icon 16 references: [logo, icons 5-15]
- Icon 17 references: [logo, icons 6-16]
- Icon 18 references: [logo, icons 7-17]
- Icon 19 references: [logo, icons 8-18]
- Icon 20 references: [logo, icons 9-19] ← Last 11 + logo
[Store generated icon 8]

Final Response:
Final Response:
"✅ Generated 20 consistent weather icons!

Icons created with sliding window consistency:
- Icons 1-14: Each new icon referenced all previous icons (accumulating references)
- Icons 15-20: Each used the last 11 icons + logo (sliding window of 12 references)

Consistency maintained throughout:
- Same stroke weight (2px)
- Same line caps (rounded)
- Same color (#2D3748)
- Same minimalist style
- Cohesive visual family

All 20 icons maintain perfect consistency across the entire series!"

[Present all 20 icons]
```

**Key Points:**

- **14-image reference limit**: Model can process up to 14 reference images per request
- **Sliding window**: Use last 10-14 images as references for extensive series
- **5 subject identities**: Model maintains consistency for up to 5 different characters/subjects
- **Explicit instructions**: Tell the model the reference images are from the same series
- **Consistency emphasis**: Emphasize matching style, tone, and identity in every prompt
- **Series context**: Always include the overall series description
- **Track progress**: Keep track of which images are used as references
- **Quality control**: After generation, visually verify consistency

**Common Use Cases:**
- Large icon sets (20+, 50+, 100+ icons)
- Storyboards with many frames (15-30+ frames)
- Social media calendar (30-90 days of posts)
- Product catalog (extensive product variations)
- UI component libraries (complete design systems)
- Brand asset collections (comprehensive asset libraries)
- Character variations (same character in different poses/scenes)

## API Call Format

### Basic Request Structure

```json
{
  "model": "google/gemini-3-pro-image-preview",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "YOUR PROMPT HERE"
        }
      ]
    }
  ],
  "modalities": ["image", "text"],
  "temperature": 0.7,
  "max_tokens": 4096
}
```

### With Image Input (for editing or reference)

```json
{
  "model": "google/gemini-3-pro-image-preview",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "image_url",
          "image_url": {
            "url": "https://example.com/image.png"
          }
        },
        {
          "type": "text",
          "text": "YOUR PROMPT HERE"
        }
      ]
    }
  ],
  "modalities": ["image", "text"],
  "temperature": 0.7,
  "max_tokens": 4096
}
```

### With Aspect Ratio Control

```json
{
  "model": "google/gemini-3-pro-image-preview",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "YOUR PROMPT HERE"
        }
      ]
    }
  ],
  "modalities": ["image", "text"],
  "image_config": {
    "aspect_ratio": "16:9"
  },
  "temperature": 0.7,
  "max_tokens": 4096
}
```

### Required Headers

```
Authorization: Bearer YOUR_OPENROUTER_API_KEY
Content-Type: application/json
HTTP-Referer: https://github.com/shelbeely/Openrouter-Nano-banana-assets-generator-MCP
X-Title: Nano Banana Assets Generator
```

### Response Format

```json
{
  "choices": [
    {
      "message": {
        "content": "Description of generated assets...",
        "images": [
          {
            "image_url": {
              "url": "data:image/png;base64,iVBORw0KGgoAAAANS..."
            }
          }
        ]
      }
    }
  ]
}
```

## Supported Aspect Ratios

The following aspect ratios are supported by Gemini/Nano Banana Pro (per official Google documentation):

**Landscape formats:**
- `21:9` - Ultra-wide cinematic (ideal for hero banners, cinematic compositions)
- `16:9` - Widescreen (YouTube thumbnails, web banners, hero sections, presentations)
- `4:3` - Traditional landscape (presentations, older displays)
- `3:2` - Standard photo landscape (traditional photography)
- `5:4` - Landscape with slight squareness

**Square format:**
- `1:1` - Square (Instagram posts, icons, profile pictures, avatars)

**Portrait formats:**
- `9:16` - Vertical widescreen (Instagram/Facebook stories, mobile screens, TikTok)
- `3:4` - Traditional portrait (traditional photography)
- `2:3` - Portrait photo standard (magazine covers, portraits)
- `4:5` - Portrait with slight width
- `9:21` - Ultra-tall portrait (rare, specialized mobile UI)

## Supported Resolutions

- `1080x1080` - Standard square (1:1)
- `1920x1080` - Full HD (16:9)
- `1080x1920` - Full HD vertical (9:16)
- `2K` (2560x1440) - High quality
- `4K` (3840x2160) - Ultra high quality
- `3840x2160` - 4K explicit
- `2560x1440` - 2K explicit
- `1280x720` - HD ready

## Best Practices

### Writing Effective Prompts (Google's Six-Element Framework)

Google's research shows that prompts structured around six core elements produce the best results with Gemini models:

1. **Subject: Define Who/What**
   - Be specific about the main elements, characters, or objects
   - Include physical attributes, characteristics, and details
   - ❌ "A banner"
   - ✅ "A modern SaaS hero banner featuring abstract geometric shapes (floating hexagons, connecting nodes, light particles)"

2. **Composition: Describe Framing & Layout**
   - Specify camera angles, framing, and perspective
   - Use standard photography/design terms
   - ❌ "Nice layout"
   - ✅ "Wide shot with rule of thirds composition, negative space on left third for text overlay, visual weight balanced on right"

3. **Action: Explain What's Happening**
   - Describe movement, interactions, or static positioning
   - Define energy level and dynamics
   - ❌ "Some movement"
   - ✅ "Subtle upward particle drift creating sense of innovation and progress, energy flowing through connecting lines"

4. **Location: Set the Environment**
   - Describe setting, context, and surroundings
   - Include environmental details that enhance the scene
   - ❌ "Tech background"
   - ✅ "Contemporary digital workspace with infinite depth, clean minimal environment suggesting cloud/SaaS platform"

5. **Style: Define the Aesthetic**
   - Be specific about visual treatment and design approach
   - Reference design movements, art styles, or specific aesthetics
   - ❌ "Modern look"
   - ✅ "Modern minimalist with vibrant gradients, flat design principles, clean professional aesthetic suitable for enterprise SaaS"

6. **Lighting: Specify Illumination Details**
   - Describe light sources, quality, direction, and mood
   - Include shadows, highlights, and atmospheric effects
   - ❌ "Good lighting"
   - ✅ "Soft ambient glow from gradient background, subtle rim lighting on geometric elements from top-right creating depth, gentle shadows"

### Advanced Prompt Enhancements

1. **Camera Details** (Optional but Powerful)
   - Lens specifications: "85mm portrait lens", "24mm wide angle"
   - Focal properties: "shallow depth of field", "everything in focus"
   - Perspective: "low angle looking up", "bird's eye view", "eye level"
   - Example: "Shot with 85mm equivalent focal length, f/2.8 aperture for subtle background blur"

2. **Materiality & Texture** (For Product/Design Assets)
   - Surface qualities: "matte finish", "glossy", "brushed metal", "frosted glass"
   - Texture details: "smooth gradient", "paper texture", "fabric weave", "metallic sheen"
   - Example: "Gradient elements have smooth glass-like quality, geometric shapes with subtle metallic sheen, soft velvety background"

3. **Full Sentence Narratives**
   - Use natural language, not just keywords
   - Brief the AI like a creative director
   - ❌ "blue purple gradient tech shapes modern"
   - ✅ "Create a hero shot featuring an abstract technology landscape with flowing gradients from deep blue to vibrant purple, populated with geometric shapes that suggest connectivity and innovation"

### Iterative Conversational Editing

Nano Banana Pro excels at multi-turn refinement. Instead of regenerating, use conversational edits:

**Initial Prompt:**
```
Generate a product banner for smart home device...
```

**Follow-up Edit 1:**
```
Make the lighting warmer and more inviting, shift from cool tones to golden hour quality
```

**Follow-up Edit 2:**
```
Add the brand logo in top-left corner, subtle drop shadow, 15% opacity
```

**Follow-up Edit 3:**
```
Increase the contrast of the main product by 20%, make it pop more against the background
```

This preserves composition and layout while refining specific aspects.

### Writing Effective Prompts (Legacy Guidelines - Still Valid)

1. **Be Specific and Detailed**
   - ❌ "Make a banner"
   - ✅ "Create a modern tech startup hero banner with gradient background from blue to purple, abstract geometric elements, and space for overlaying text"

2. **Include Context**
   - Mention where the asset will be used (website, social media, email, app)
   - Specify the target audience
   - Describe the desired mood/emotion

3. **Define Style Clearly**
   - Use descriptive terms: minimalist, vibrant, elegant, playful, professional
   - Reference art styles: flat design, material design, glassmorphism, etc.
   - Mention specific elements: gradients, shadows, textures, patterns

4. **Specify Technical Requirements**
   - Always include aspect ratio for the intended use case
   - Mention resolution if quality is critical
   - List any technical constraints

### Color Guidance

1. **Provide Hex Codes**
   - ✅ Use: "#667EEA", "#764BA2"
   - ❌ Avoid: "blue", "purple"

2. **Include 3-5 Brand Colors**
   - Primary color
   - Secondary color
   - Accent color(s)
   - Background color (if applicable)

3. **Consider Color Harmony**
   - Complementary colors for contrast
   - Analogous colors for harmony
   - Triadic colors for vibrancy

### Reference Images

1. **Use Up to 14 Reference Images (Not Just 5)**
   - Nano Banana Pro supports up to **14 reference images** per request
   - Use for style guidance, composition examples, and identity preservation
   - Categories of references:
     - **Style references**: Overall aesthetic and visual treatment (1-3 images)
     - **Composition references**: Layout and arrangement examples (1-2 images)
     - **Color treatment references**: Mood and color grading (1-2 images)
     - **Subject/identity references**: For maintaining character or product consistency (up to 5 distinct subjects)
     - **Technical references**: Quality level and detail expectations (1-2 images)
     - **Brand assets**: Logos and brand elements (1-2 images)

2. **Provide Context for References**
   - Explain what aspect to emulate from each reference
   - Clarify what to avoid from the reference
   - Specify if it's for style, composition, color, or subject identity
   - Example: "Reference image 1 shows the composition layout to follow. Reference image 2 demonstrates the lighting quality desired."

3. **Identity Preservation Across References**
   - Model can maintain consistency for up to **5 distinct subjects/characters** across the 14 references
   - Use multiple angles/views of same subject to strengthen identity preservation
   - Explicitly mention: "Maintain the visual identity shown in reference images 1-3"

### Brand Consistency

1. **Establish Guidelines First**
   - Define style clearly
   - Document color usage rules
   - Specify typography preferences
   - Outline logo usage rules

2. **Use Identity Preservation**
   - Include brand reference images
   - Provide logo in all requests
   - Maintain color palette strictly

3. **Iterate and Refine**
   - Generate initial assets
   - Check consistency
   - Refine as needed
   - Validate final outputs

## Common Use Cases

### Website Assets
- Hero banners (16:9, 21:9)
- Section backgrounds (16:9, various)
- Icon sets (1:1, small resolution)
- Call-to-action buttons (custom sizes)
- Feature images (4:3, 16:9)

### Social Media
- Instagram posts (1:1, 1080x1080)
- Instagram stories (9:16, 1080x1920)
- Facebook covers (wide, custom)
- Twitter headers (3:1, custom)
- LinkedIn banners (4:1, custom)
- YouTube thumbnails (16:9, 1280x720)

### Branding
- Logo variations (1:1, vector-style)
- Brand patterns (tileable, various)
- Color palette visualizations
- Style guide assets
- Presentation templates

### UI/UX Design
- App icons (1:1, multiple sizes)
- Splash screens (9:16, device-specific)
- Empty states (custom)
- Error states (custom)
- Loading animations (conceptual)

## Error Handling

### Common Issues

1. **Missing API Key**
   - Check that OPENROUTER_API_KEY is set
   - Verify the key is valid
   - Ensure the key has sufficient credits

2. **API Errors**
   - 401: Invalid API key
   - 402: Insufficient credits
   - 429: Rate limit exceeded
   - 500: Server error (retry)

3. **Invalid Parameters**
   - Check aspect ratio format (use colons, not "x")
   - Verify resolution is supported
   - Ensure image URLs are accessible
   - Validate hex color codes start with #

4. **Quality Issues**
   - Provide more detailed prompts
   - Add reference images
   - Specify style more clearly
   - Include brand guidelines
   - Try multiple iterations

### Troubleshooting Steps

1. Verify API key is set correctly
2. Check internet connectivity
3. Validate request format
4. Review prompt quality
5. Check for model availability
6. Retry with exponential backoff for transient errors

## Examples

### Example 1: Simple Icon

**User Request:** "Create a home icon for my website"

**Your Response:**
```
I'll generate a home icon for your website using the Six-Element Framework for optimal results.

API Request:

Subject: Simple house silhouette with pitched roof and centered door, clean geometric shape
Composition: Centered in frame, balanced proportions, suitable for small sizes
Action: Static, stable presentation representing home/safety
Location: Isolated on solid bright green (#00FF00) chroma key background, no environmental context
Style: Minimalist line art, modern flat design, professional and recognizable
Lighting: Even lighting, no shadows, clean silhouette optimized for UI

Technical Specifications:
- Aspect Ratio: 1:1
- Resolution: 512x512
- Color: Single color (#2D3748) on bright green (#00FF00) chroma key background
- Format: Clean vector-style appearance

Note: Use chroma key removal for transparency: convert image.png -fuzz 5% -transparent "#00FF00" output.png

Requirements:
- Professional and instantly recognizable
- Works at small sizes (24px to 128px)
- Clear silhouette
- Web-optimized for navigation use

[Make API call with these parameters]

Generated icon:
[Present the generated image]
```

### Example 2: Social Media Kit

**User Request:** "I need a social media kit for my coffee shop"

**Your Response:**
```
I'll create a comprehensive social media kit for your coffee shop using the Six-Element Framework. What's your coffee shop's style and brand colors?

[After getting details: "Artisan style, warm colors #6F4E37 (coffee brown), #DEB887 (burlywood), #FFFDD0 (cream)"]

I'll generate 4 assets for your coffee shop with consistent visual identity:

API Request:

Project Description: Social media kit for artisan coffee shop

Asset Types with Specifications:

1. Instagram Post (1:1, 1080x1080)
   Subject: Artisan coffee cup on rustic wooden table with steam rising
   Composition: Center-weighted, rule of thirds, product hero shot
   Action: Steam gently rising, suggesting fresh brew
   Location: Rustic coffee shop interior, warm wood surfaces
   Style: Cozy artisan aesthetic, warm inviting tones, handcrafted feel
   Lighting: Warm natural light from window (golden hour quality), soft shadows

2. Instagram Story (9:16, 1080x1920)
   Subject: Barista hands crafting latte art, close-up of pour
   Composition: Vertical flow, action in center, text-safe zones top/bottom
   Action: Dynamic pour in motion, showcasing craft
   Location: Behind the bar, coffee shop environment
   Style: Same artisan aesthetic, authentic craftsmanship
   Lighting: Soft overhead lighting, warm tones

3. Facebook Cover (wide format)
   Subject: Coffee shop interior panorama with products
   Composition: Wide horizontal sweep, welcoming view
   Action: Inviting static scene, warm atmosphere
   Location: Full coffee shop interior view
   Style: Cohesive with artisan brand, professional yet cozy
   Lighting: Ambient warm lighting throughout

4. Profile Picture (1:1, circular crop-safe)
   Subject: Coffee cup logo or stylized coffee bean
   Composition: Centered, circular-safe design
   Action: Static, iconic
   Location: Isolated, clean background
   Style: Simplified brand mark, recognizable
   Lighting: Even, professional

Brand Guidelines:
Colors: #6F4E37 (coffee brown primary), #DEB887 (warm accent), #FFFDD0 (cream highlights)
Consistent Elements: Warm wood textures, artisan handcrafted feel, natural lighting
Materiality: Ceramic cups, wood surfaces, natural textures

[Make API call]

Generated assets:
[Present all generated images labeled by type]
```

### Example 3: Edit Existing Asset

**User Request:** "Make this image warmer and brighter" [provides image]

**Your Response:**
```
I'll adjust the image to be warmer and brighter using the Six-Element Framework for precise edits.

API Request:

Edit Instructions (Six-Element Framework):

Subject modifications: Maintain all existing elements, enhance warmth without altering composition
Composition adjustments: Keep current layout and framing unchanged
Action changes: Preserve any existing movement or static positioning
Location alterations: Keep environment as-is, adjust only atmospheric qualities
Style refinements: Shift color temperature toward warmer spectrum, enhance vibrancy
Lighting adjustments: 
  - Add golden/amber color cast throughout (color temperature shift to ~3500K)
  - Increase overall brightness by 20-25%
  - Enhance warm highlights while maintaining detail
  - Soften any harsh shadows with warm fill light effect
  - Add subtle golden glow to light sources

Camera & Detail: Maintain existing perspective and depth of field

Preserve Elements: 
- Original composition and layout
- All subjects and main elements
- Any text or logos
- Core image structure

Technical:
- Maintain original aspect ratio and resolution
- Ensure smooth, natural-looking color transitions
- Preserve image detail and sharpness

[Make API call with the provided image]

Edited image:
[Present the edited result]

Changes applied:
- Color temperature shifted to warm golden tones
- Overall brightness increased by 20%
- Warm lighting effect added throughout
- Natural and inviting atmosphere enhanced
- Original composition and elements preserved
```

### Example 4: Consistent Series (10 Icons)

**User Request:** "Create 10 weather icons in a consistent style: sunny, cloudy, rainy, stormy, snowy, windy, foggy, partly cloudy, thunderstorm, and hail"

**Your Response:**
```
I'll create a consistent set of 10 weather icons using the Six-Element Framework and sliding window technique for maintaining consistency throughout the series.

Series Overview (applies to all icons):
- Subject: Weather symbols in minimalist line art style
- Composition: Centered, balanced, circular-safe design
- Action: Static, iconic representation
- Location: Isolated on solid bright green (#00FF00) chroma key background
- Style: Modern minimalist, clean line art, 2px stroke weight, rounded line caps
- Lighting: Even, no shadows, optimized for UI usage
- Color: Monochrome #2D3748
- Technical: 1:1 aspect ratio, 512x512 resolution
- Note: Chroma key background allows easy removal with: convert image.png -fuzz 5% -transparent "#00FF00" output.png

[Icon 1 - Sunny]
API Request using Six-Element Framework:

Subject: Sun symbol - circular center with evenly spaced rays (8 rays radiating outward)
Composition: Perfectly centered, balanced radial symmetry
Action: Static, stable representation of sunshine
Location: Isolated on solid bright green (#00FF00) chroma key background, no context
Style: Minimalist line art, 2px stroke weight, rounded line caps, modern and clean
Lighting: Even illumination, no shadows, pure line work

Technical: 1:1, 512x512, #2D3748 on bright green (#00FF00) chroma key background
This is icon 1 of 10 in weather icon series - establishing baseline style

References: None (establishing baseline)
[Generate and store Icon 1]

[Icon 2 - Cloudy]
API Request:

Subject: Cloud shape - rounded, fluffy cloud form with smooth curves
Composition: Centered, following same centered approach as icon 1
Action: Static cloud representation
Location: Isolated on bright green (#00FF00) chroma key background, matching icon 1 treatment
Style: Match icon 1's minimalist line art exactly, same 2px stroke, rounded caps
Lighting: Even, matching icon 1's treatment

Consistency Requirements:
- Match the visual style of reference icon exactly
- Same stroke weight (2px) and line caps (rounded)
- Same level of detail and simplification
- Cohesive with icon 1 in same family

IMPORTANT: Reference image shows the previously generated sunny icon. Match its stroke weight, line caps, and minimalist approach exactly.

References: [Icon 1]
[Generate and store Icon 2]

[Icons 3-5: Rainy, Stormy, Snowy]
Continue same pattern, adding all previous icons as references:

Icon 3 (Rainy):
Subject: Rain cloud with falling rain drops
Same framework structure...
References: [Icon 1, Icon 2]

Icon 4 (Stormy):
Subject: Dark storm cloud with lightning bolt
Same framework structure...
References: [Icon 1, Icon 2, Icon 3]

Icon 5 (Snowy):
Subject: Cloud with falling snowflakes
Same framework structure...
References: [Icon 1, Icon 2, Icon 3, Icon 4]

[Icon 6 - Windy] ← Sliding window begins (using last 4-5 icons)
API Request:

Subject: Wind lines showing air movement, curved flowing lines
Composition: Centered following established pattern
Action: Suggests movement while remaining iconic
Location: Isolated on bright green (#00FF00) chroma key background, consistent with series
Style: Match established minimalist line art, 2px stroke, rounded caps
Lighting: Even, no shadows

Consistency Requirements:
- Maintain same visual style as reference images
- Same stroke weight, line caps, and design language
- Part of cohesive weather icon family

IMPORTANT: Reference images show previously generated icons. Match their style exactly.

References: [Icon 2, Icon 3, Icon 4, Icon 5] ← Sliding window (last 4 icons)
[Generate and store Icon 6]

[Icons 7-10: Foggy, Partly Cloudy, Thunderstorm, Hail]
Continue with sliding window approach:

Icon 7: References [Icon 3, Icon 4, Icon 5, Icon 6]
Icon 8: References [Icon 4, Icon 5, Icon 6, Icon 7]
Icon 9: References [Icon 5, Icon 6, Icon 7, Icon 8]
Icon 10: References [Icon 6, Icon 7, Icon 8, Icon 9]

✅ Complete! Generated 10 weather icons with perfect consistency.

Consistency strategy:
- Icons 1-5: Each new icon referenced all previous ones (accumulating)
- Icons 6-10: Sliding window of last 4 icons maintained consistency
- All icons share: 2px stroke weight, rounded line caps, centered composition, minimalist style

[Present all 10 icons in a grid]
```

## Integration Tips

### With Code Editors
- Agents can directly generate assets during development
- Assets can be saved to project directories
- Quick iteration on UI components

### With Design Tools
- Export generated assets for further refinement
- Use as starting points for complex designs
- Maintain consistency across design systems

### With Workflow Automation
- Batch generate assets for multiple projects
- Automate social media content creation
- Generate variations for A/B testing

## Security Considerations

1. **API Key Management**
   - Never hardcode API keys
   - Use environment variables
   - Rotate keys regularly
   - Monitor usage

2. **Input Validation**
   - Validate user inputs
   - Sanitize prompts
   - Check image URLs for security
   - Limit request sizes

3. **Rate Limiting**
   - Implement request throttling
   - Handle rate limit errors gracefully
   - Cache results when appropriate
   - Monitor API usage

## Performance Tips

1. **Optimize Requests**
   - Batch related assets when possible
   - Use appropriate resolutions (don't request 4K unless needed)
   - Cache frequently used assets
   - Reuse similar prompts

2. **Manage Costs**
   - Monitor API usage
   - Use appropriate model parameters
   - Avoid unnecessary regenerations
   - Implement result caching

3. **Quality vs Speed**
   - Lower resolution for drafts/previews
   - Higher resolution for final outputs
   - Use reference images to improve first-try success
   - Iterate on prompts to reduce regenerations

## Version History

- **1.0.0** (2024): Initial release
  - Basic asset generation
  - Asset pack creation
  - Image editing capabilities
  - Brand consistency checking

## Support and Resources

- **OpenRouter Documentation**: https://openrouter.ai/docs
- **Model Information**: https://openrouter.ai/models
- **GitHub Repository**: https://github.com/shelbeely/Openrouter-Nano-banana-assets-generator-MCP
- **MCP Server**: Available as a full MCP server implementation in this repository

## Related Skills

- Image optimization and compression
- Color palette generation
- Typography pairing
- Layout generation
- Brand identity creation

---

**Remember**: This skill uses OpenRouter's API which requires credits. Monitor your usage and implement appropriate rate limiting and error handling in production environments.
