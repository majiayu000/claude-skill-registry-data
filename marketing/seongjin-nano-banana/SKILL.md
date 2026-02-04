---
name: Seongjin_Nano-Banana
description: Generate PPT slide images from JSON slide outlines using Gemini Image Generation API (gemini-3-pro-image-preview). Use when creating presentation slides from JSON, generating slide images in batch, or converting slide outlines to visual slides.
allowed-tools: Read, Bash, Glob
version: 2.2.0
updated: 2026-01-04
status: active
---

# Nano-Banana PPT Slide Image Generator

Generate high-quality PPT slide images from JSON slide outlines using the Gemini Image Generation API (Nano Banana Pro - gemini-3-pro-image-preview).

---

## Quick Reference (30 seconds)

**Purpose**: Generate PPT slide images from JSON outlines containing Nano-Banana optimized prompts.

**Execution Command**:
```bash
# Generate all slides
uv run python "{skill_scripts_dir}/Generate_Slides.py" "{json_file}" --output-dir "{output_dir}"

# Generate specific slides only (for recovery/retry)
uv run python "{skill_scripts_dir}/Generate_Slides.py" "{json_file}" --output-dir "{output_dir}" --slides 5
uv run python "{skill_scripts_dir}/Generate_Slides.py" "{json_file}" --output-dir "{output_dir}" --slides 5,7,9
```

**Script Location**:
`.claude/skills/Seongjin_Skill_Nano-Banana/Scripts/Generate_Slides.py`

**Prerequisites**:
- Python dependencies: `google-genai`, `python-dotenv`, `pillow`
- API Key: `.claude/skills/Seongjin_Skill_Nano-Banana/Scripts/.env` with `GOOGLE_API_KEY=your_key_here`

**Output**: PNG images saved as `slide_001.png`, `slide_002.png`, etc.

---

## Implementation Guide (5 minutes)

### Basic Usage

**Step 1**: Ensure prerequisites are installed
```bash
pip install google-genai python-dotenv pillow
```

**Step 2**: Create `.env` file in skill Scripts directory
```bash
# Create at: .claude/skills/Seongjin_Skill_Nano-Banana/Scripts/.env
GOOGLE_API_KEY=your_google_api_key_here
```

**Step 3**: Execute the script
```bash
# Basic execution (output: {json_name}_images/)
uv run python "/path/to/Generate_Slides.py" "slides.json"

# With custom output directory
uv run python "/path/to/Generate_Slides.py" "slides.json" --output-dir "./output"

# With custom .env file path
uv run python "/path/to/Generate_Slides.py" "slides.json" --env-file "/path/to/.env"

# Generate specific slides only (for recovery/retry)
uv run python "/path/to/Generate_Slides.py" "slides.json" --slides 5           # Single slide
uv run python "/path/to/Generate_Slides.py" "slides.json" --slides 5,7,9       # Multiple slides
uv run python "/path/to/Generate_Slides.py" "slides.json" --slides 1-5         # Range
uv run python "/path/to/Generate_Slides.py" "slides.json" --slides 1-3,5,7-9   # Mixed
```

### Input JSON Schema

The script expects a JSON file with the following structure:

```json
{
  "source_file": "/path/to/source.md",
  "created_at": "2024-12-05T14:30:22",
  "total_slides": 10,
  "theme": "light_warm",
  "target_audience": "general",
  "reference_images": ["/path/to/global_ref.png"],
  "slides": [
    {
      "page": 1,
      "title": "Slide Title",
      "key_message": "Reading Deck detailed explanation (2-4 sentences)",
      "nano_banana_prompt": "Self-contained English instructions with Korean text",
      "reference_images": ["/path/to/slide_specific_ref.png"]
    }
  ]
}
```

**Top-Level Field Descriptions**:
- `source_file`: Original source file path
- `reference_images`: (Optional) Global reference images applied to ALL slides

**Slide Field Descriptions**:
- `page`: Slide number (starts from 1)
- `title`: Slide title (Korean, max 10 words)
- `key_message`: Reading Deck detailed explanation (Korean, 2-4 sentences)
- `nano_banana_prompt`: Self-contained image generation prompt (English instructions with quoted Korean text)
- `reference_images`: (Optional) Slide-specific reference images (combined with global references)

### nano_banana_prompt 4-Layer Structure

All prompts must include these 4 layers:

**Layer 1 - Scene Declaration**: Slide format, text position, layout composition
**Layer 2 - Photography/Style**: Background style, lighting, color mood, visual elements
**Layer 3 - Text Rendering**: All Korean text in quotes for exact rendering
**Layer 4 - Technical Specs**: 16:9 aspect ratio, 1920x1080 resolution, readability requirements

### Script Configuration

Configurable constants in the script:

```python
MODEL = "gemini-3-pro-image-preview"  # Gemini model
ASPECT_RATIO = "16:9"                  # Image aspect ratio
IMAGE_SIZE = "2K"                      # Image resolution
MAX_RETRIES = 50                       # Maximum retry attempts
RETRY_DELAY_SECONDS = 30               # Delay for quota/rate limit errors
MAX_WORKERS = 50                       # Maximum parallel workers
```

### Output Example

```
============================================================
Starting PARALLEL image generation for 22 slides
Output directory: slides_images
Model: gemini-3-pro-image-preview
Max workers: 50
Max retries: 50
Retry delay: 30 seconds
============================================================

[Slide 01/22] Title Slide - Starting...
  [Attempt 1/50] Generating image...
[Slide 01] Success - Saved to slide_001.png
...

============================================================
Generation Complete!
============================================================
Total slides processed: 22
Successful: 22
Failed: 0
Total time: 163.4 seconds
Average time per slide: 7.4 seconds
============================================================
```

---

## Advanced Implementation (10+ minutes)

### Error Handling

The script implements sophisticated error handling:

**Rate Limit / Quota Errors**:
- Detection: Checks for "rate" or "quota" in error message
- Recovery: 30-second delay before retry
- Maximum: 50 retry attempts

**Safety Filter Blocks**:
- Detection: Checks for "blocked" or "safety" in error message
- Recovery: Skip the slide, log the error
- Impact: Slide will not be generated

**Other Errors**:
- Recovery: 5-second delay before retry
- Maximum: 50 retry attempts

### Performance Optimization

**Parallel Execution**:
- Uses ThreadPoolExecutor with configurable max workers (default: 50)
- Processes multiple slides concurrently
- Results are collected as tasks complete

**Average Performance Metrics**:
- Generation time per slide: 7-10 seconds
- Throughput: 6-9 slides per minute (with parallelization)
- Success rate: 95%+ (with retry logic)

### Reference Images

The script supports reference images to guide visual style and content generation.

**Use Cases**:
- Consistent character appearance across slides
- Brand asset integration (logos, icons)
- Style reference for visual consistency
- Photo-based slide generation

**Reference Image Types**:

1. **Global Reference Images** (top-level `reference_images`):
   - Applied to ALL slides in the presentation
   - Use for: brand assets, consistent characters, style guides

2. **Slide-Specific Reference Images** (per-slide `reference_images`):
   - Applied only to that specific slide
   - Combined with global references (slide-specific first, then global)
   - Use for: slide-specific photos, diagrams, charts

**Example JSON with Reference Images**:
```json
{
  "source_file": "/path/to/source.md",
  "reference_images": ["/path/to/logo.png", "/path/to/style_guide.png"],
  "slides": [
    {
      "page": 1,
      "title": "Title Slide",
      "nano_banana_prompt": "Create a title slide incorporating the provided logo...",
      "reference_images": ["/path/to/hero_image.png"]
    },
    {
      "page": 2,
      "title": "Team Introduction",
      "nano_banana_prompt": "Create a team photo slide using the provided photos...",
      "reference_images": ["/path/to/person1.png", "/path/to/person2.png"]
    }
  ]
}
```

**Output with Reference Images**:
```
[Global Reference] Found 2 global reference image(s)
[Slide 01/10] Title Slide (refs: 3) - Starting...
  [Reference Image] Loaded: hero_image.png
  [Reference Image] Loaded: logo.png
  [Reference Image] Loaded: style_guide.png
  [Attempt 1/10] Generating image with 3 reference(s)...
[Slide 01] Success - Saved to slide_001.png
```

**Best Practices**:
- Keep reference images under 5 per slide for optimal performance
- Use high-quality images (minimum 512x512 pixels recommended)
- Ensure reference images are accessible (absolute paths recommended)
- Reference images are optional - omit the field if not needed

### Integration Workflow

The complete PPT generation workflow:

**Step 1**: Source Analysis (PPT-Planner Agent)
- Analyzes markdown or PDF source files
- Generates JSON slide outline with nano_banana_prompt

**Step 2**: Image Generation (Nano-Banana Script)
- Reads JSON slide outline
- Generates PNG images for each slide

**Step 3**: Assembly (Manual or Automation)
- Combine generated images into final presentation

### Programmatic Integration

```python
from pathlib import Path
import subprocess

def generate_slides(json_path: str, output_dir: str = None) -> int:
    """Generate slides from JSON using Nano-Banana script."""
    script_path = "/path/to/Generate_Slides.py"
    cmd = ["uv", "run", "python", script_path, json_path]

    if output_dir:
        cmd.extend(["--output-dir", output_dir])

    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode
```

---

## Related Resources

**Related Agent**:
- `Seongjin_Agent_PPT-Planner`: Generates JSON slide outlines from source files

**Related Command**:
- `/ppt`: Orchestrates the complete PPT generation workflow

**Model Information**:
- Model: gemini-3-pro-image-preview (Nano Banana Pro)
- Capabilities: Text rendering, high-quality 2K images, 16:9 aspect ratio

**API Documentation**:
- Google AI Studio: https://aistudio.google.com/
- Gemini API: https://ai.google.dev/

---

## Works Well With

- `Seongjin_Agent_PPT-Planner` - Generates JSON slide outlines from markdown/PDF
- `/ppt` command - Orchestrates complete source-to-slides workflow

---

## Troubleshooting

**API Key Not Found**:
- Ensure `.env` file exists at `.claude/skills/Seongjin_Skill_Nano-Banana/Scripts/.env`
- Verify `GOOGLE_API_KEY` is set correctly

**Quota Exceeded**:
- Wait for quota reset or reduce MAX_WORKERS
- Check Google AI Studio for quota status

**Safety Filter Triggered**:
- Review prompt content for problematic terms
- Simplify or rephrase the nano_banana_prompt
- Avoid controversial or explicit content

**Image Generation Failed**:
- Check network connectivity
- Verify API key is valid
- Review prompt structure follows 4-layer format

**Partial Slide Recovery**:
- Use `--slides` parameter to regenerate only failed slides
- Example: `--slides 5,12,15` to regenerate slides 5, 12, and 15
- Supports single numbers, comma-separated lists, and ranges (e.g., `1-5`, `1-3,5,7-9`)
