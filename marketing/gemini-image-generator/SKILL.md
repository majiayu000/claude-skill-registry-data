---
name: gemini-image-generator
description: Generate images using Google Gemini Nano Banana (gemini-2.5-flash-image) model. Use when asked to create images, generate visuals, design graphics, or produce artwork for marketing materials like Fiverr gigs, social media, banners, or promotional content.
allowed-tools: Bash, Read, Write, Edit
---

# Gemini Nano Banana Image Generator Skill

Generate high-quality images using Google's Gemini 2.5 Flash Image model (codename: Nano Banana).

## Model Information

- **Model ID**: `gemini-2.5-flash-image`
- **Also known as**: Nano Banana
- **Pro version**: `gemini-3-pro-image` (Nano Banana Pro) - better text rendering, up to 14 reference images
- **Pricing**: ~$0.039 per image (1024x1024)

## Prerequisites

### 1. Google AI Studio API Key
Get your API key from: https://aistudio.google.com/app/apikey

### 2. Environment Variable
```bash
export GEMINI_API_KEY="your-api-key-here"
```

Or create `.env` file:
```
GEMINI_API_KEY=your-api-key-here
```

### 3. Install Dependencies
```bash
pip install google-genai pillow python-dotenv
```

## Usage

### Generate Single Image
```bash
python .claude/skills/gemini-image-generator/scripts/generate_image.py \
  --prompt "A professional tech banner with AI and cloud icons, modern blue color scheme" \
  --output "output/banner.png"
```

### Generate with Description (Recommended)
```bash
python .claude/skills/gemini-image-generator/scripts/generate_image.py \
  --prompt "Create a professional illustration showing an AI agent system. Include a central brain icon representing Claude AI, connected to nodes labeled Knowledge Base, User Input, and Response. Use a modern tech color palette with deep blue and electric purple on a clean dark gradient background. Enterprise-grade aesthetic." \
  --output "output/ai_agent.png"
```

### Batch Generate for Fiverr
```bash
python .claude/skills/gemini-image-generator/scripts/batch_generate.py \
  --config "opportunities/guang-digital/05-fiverr-image-prompts.md" \
  --output-dir "output/fiverr-images"
```

## Key Differences from Imagen

| Feature | Nano Banana | Imagen 3 |
|---------|-------------|----------|
| API Method | `generate_content()` | `generate_images()` |
| Style | Conversational prompts | Structured prompts |
| Image Editing | Yes (with reference images) | No |
| Text in Images | Good (Pro: Better) | Limited |
| Pricing | ~$0.039/image | $0.03/image |

## Best Practices for Prompts

### DO: Describe the Scene
```
Create a picture of a modern web dashboard with analytics charts,
user statistics, and a dark mode interface. Include navigation
sidebar and header with notifications. Professional SaaS aesthetic.
```

### DON'T: Just List Keywords
```
dashboard, charts, dark mode, analytics, modern
```

## Fiverr Image Specifications

- **Required Size**: 1280 x 769 pixels
- **Aspect Ratio**: ~16:9
- **Format**: PNG or JPG
- **Images per Gig**: 3 recommended

## Example Prompts for Guang Digital

### AI Agent Gig (Image 1)
```
Create a professional technical illustration showing an AI agent system architecture.
Design a central brain icon representing Claude AI connected to multiple nodes.
Include nodes for: User Input, AI Agent Processing, Knowledge Base (vector database),
and Response Output. Use modern tech color palette with deep blue (#1E40AF),
electric purple (#7C3AED), and cyan accents (#06B6D4). Clean dark gradient background.
Professional enterprise-grade aesthetic. No text overlays needed.
```

### Full-Stack Gig (Image 1)
```
Create a professional full-stack web development architecture diagram visualization.
Show three-tier architecture: Frontend layer at top with browser and mobile icons,
API/Backend layer in middle with server icons, Database layer at bottom with
PostgreSQL and Redis icons. Add cloud icons (AWS, Azure) floating in background.
Modern dark theme with gradient background. Glowing blue connection lines between
components. Professional enterprise software aesthetic.
```

### IoT Platform Gig (Image 1)
```
Create an industrial IoT platform architecture visualization.
Bottom layer shows industrial sensors and machinery icons (temperature, pressure gauges).
Middle layer shows edge gateway hub collecting data.
Top layer shows cloud platform with analytics dashboard.
Data flow arrows going upward from devices to cloud.
Industrial color scheme with steel blue, orange warning colors, white accents.
Professional industrial technology aesthetic.
```

## Output

The script saves generated images to the specified path and returns:
- **Success**: Full path to saved image
- **Failure**: Error message with troubleshooting steps

## Troubleshooting

### "API key not found"
```bash
export GEMINI_API_KEY="your-key"
# or create .env file
```

### "Content blocked"
Modify your prompt to avoid policy violations (violence, explicit content, copyrighted characters).

### Low quality output
- Use descriptive scene language, not keywords
- Specify colors, styles, and aesthetics explicitly
- Add "professional", "high quality", "detailed" to prompts

## Resources

- [Official Nano Banana Documentation](https://ai.google.dev/gemini-api/docs/image-generation)
- [Gemini API Pricing](https://ai.google.dev/gemini-api/docs/pricing)
- [Nano Banana Hackathon Kit](https://github.com/google-gemini/nano-banana-hackathon-kit)
