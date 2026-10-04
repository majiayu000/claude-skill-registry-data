---
name: legnext-midjourney
description: Generate AI images using Midjourney through the Legnext API. Use this skill when users request Midjourney-style image generation, visual content creation, or ask to create/generate images with natural language descriptions. Handles prompt engineering, API calls, task polling, and result retrieval.
---

# Legnext Midjourney

Generate professional AI images using Midjourney's capabilities through the Legnext API.

## Setup

**CRITICAL**: This skill requires a Legnext API key. Before running, check if the user has configured their API key:

### Check for existing configuration:
- Look for a `.env` file in the project directory or parent directories
- Check for `LEGNEXT_API_KEY=<key>` in the `.env` file
- Or check environment variable: `echo $LEGNEXT_API_KEY`

### If not found, inform the user they need to:

**Option 1: Create a .env file (recommended)**
```bash
# Create .env file in the project root
echo "LEGNEXT_API_KEY=your-api-key-here" > .env
```

**Option 2: Set environment variable**
```bash
export LEGNEXT_API_KEY=your-api-key-here
```

### Get an API key from:
**https://legnext.ai/app/api-keys**

### Verify API key:
```bash
python scripts/verify_api_key.py
```

The scripts will automatically detect the `.env` file and provide clear error messages if the API key is missing or invalid.

## Quick Start

For simple image generation requests:

```bash
python scripts/generate_and_wait.py "a beautiful sunset over mountains --v 7 --ar 16:9"
```

This handles the complete workflow: submit task → poll status → return results.

## Complete Workflow

### 1. Understand the User's Request

Identify what type of image the user wants:
- Subject matter (people, landscapes, objects, abstract)
- Style (photographic, illustrated, artistic)
- Mood and atmosphere
- Technical requirements (aspect ratio, quality)

### 2. Craft the Prompt

Transform the user's natural language request into an effective Midjourney prompt.

**Use the 7-Element Framework** for systematic prompts:
- Subject, Medium, Environment, Lighting, Color, Mood, Composition

**Quick structure:**
```
[Subject] [Description] [Environment] [Lighting] [Style] [Parameters]
```

**Example transformations:**

User request: "I need a professional headshot"
→ Prompt: `professional headshot, studio lighting, neutral background, sharp focus, 85mm lens --ar 2:3 --style raw`

User request: "Create a cyberpunk city scene"
→ Prompt: `cyberpunk city at night, neon lights, flying cars, rain-soaked streets, cinematic, blade runner aesthetic --ar 16:9`

**Key principles:**
- Be specific about what you want to SEE (not abstract concepts)
- Front-load important elements
- Trust V7's default quality — avoid junk words (4K, HDR, award-winning)
- Use `--style raw` for photorealism

For the complete 7-Element Framework and advanced techniques, see `references/prompt_engineering.md`.
For photography terminology (camera, lighting, film stocks), see `references/photography.md`.

### 3. Add Midjourney Parameters

Append parameters to optimize the generation:

**Common parameters:**
- `--v 7` - Use Midjourney v7 (recommended)
- `--ar 16:9` - Aspect ratio (1:1, 16:9, 9:16, 3:2, etc.)
- `--s 500` - Stylization level (0-1000)
- `--q 1` - Quality (0.25, 0.5, 1, 2)
- `--chaos 20` - Variation amount (0-100)

**Example:**
```
a majestic lion in savanna --v 7 --ar 16:9 --s 500 --q 1
```

For complete parameter reference, consult `references/midjourney_parameters.md`.

### 4. Submit and Monitor

Use the appropriate script based on your needs:

**Option A: Complete workflow (recommended)**
```bash
python scripts/generate_and_wait.py "your prompt here"
```

This automatically:
- Submits the task to Legnext API
- Polls every 5 seconds for status updates
- Returns final results when complete
- Times out after 5 minutes if not completed

**Option B: Manual control**

Submit task:
```bash
python scripts/imagine.py "your prompt here"
# Returns: {"job_id": "uuid", "status": "pending"}
```

Check status:
```bash
python scripts/get_task.py <job_id>
# Returns: {"status": "processing|completed|failed", "output": {...}}
```

### 5. Handle Results

When the task completes successfully:

**Output structure:**
```json
{
  "job_id": "uuid",
  "status": "completed",
  "output": {
    "images": ["url1", "url2", "url3", "url4"],
    "seed": 123456789
  }
}
```

**Typically 4 image variations are generated.**

Present the image URLs to the user. Images are:
- Accessible via HTTPS URLs
- Stored temporarily (download if needed for permanent storage)
- Usually high resolution

If the user wants variations of a specific result, note the `seed` value and include `--seed <value>` in future prompts for consistency.

## Common Usage Patterns

### Pattern 1: Single Image Request
User: "Generate a photo of a coffee shop interior"

Response workflow:
1. Craft prompt: `cozy coffee shop interior, wooden furniture, plants, warm lighting, customers, rustic decor --ar 16:9 --v 7`
2. Run: `python scripts/generate_and_wait.py "..."`
3. Present the 4 generated image URLs
4. Ask if they'd like variations or adjustments

### Pattern 2: Specific Style Request
User: "Create a logo design for a tech startup"

Response workflow:
1. Craft prompt: `minimalist logo design for tech startup, modern, clean lines, geometric, professional, simple icon --v 7 --ar 1:1 --s 250`
2. Generate and present results
3. If needed, iterate with `--seed` for consistency

### Pattern 3: Batch Generation
User: "I need several variations of a mountain landscape"

Response workflow:
1. Generate first set: `majestic mountain landscape, snow peaks, alpine lake, dramatic sky --ar 16:9 --v 7`
2. Use different `--chaos` or `--seed` values for variations
3. Or adjust prompt slightly for different moods/times of day

### Pattern 4: Iterative Refinement
User: "The image is too dark, can you make it brighter?"

Response workflow:
1. Add lighting keywords: "bright, well-lit, sunny, vibrant colors"
2. Keep successful elements from original prompt
3. Adjust `--s` (stylization) if needed
4. Use original `--seed` with modifications for consistency

## Troubleshooting

### API Key Issues
```
Error: LEGNEXT_API_KEY environment variable not set
```
→ User needs to set: `export LEGNEXT_API_KEY=their_key`

### Task Timeout
```
Error: Task did not complete within 300 seconds
```
→ Complex prompts may take longer. Manually check with `get_task.py <job_id>`

### Failed Tasks
```
Status: failed
```
→ Common causes:
- Invalid prompt (too short/long, forbidden content)
- Insufficient credits in Legnext account
- Invalid parameter combinations
Check error details in the response

### Generation Quality Issues
If results don't match expectations:
- Add more descriptive keywords
- Adjust `--s` (stylization) parameter
- Try different versions (`--v 6` vs `--v 7`)
- Consult `references/prompt_engineering.md` for techniques

## Advanced Features

### Using Reference Images
Include image URLs in prompts:
```
https://example.com/reference.jpg a painting in this style --v 7
```

### Negative Prompting
Exclude unwanted elements:
```
a bedroom interior --no clutter --no windows --v 7
```

### Multi-Prompting
Weight different concepts:
```
cat::2 dog::1 playing together --v 7
```
This emphasizes "cat" twice as much as "dog".

### Consistent Seeds
For variations of the same concept:
1. Note the seed from a successful generation
2. Use `--seed <value>` in subsequent prompts
3. Modify other aspects while maintaining consistency

## Reference Documentation

- **Midjourney Parameters**: See `references/midjourney_parameters.md` for complete parameter list and usage
- **Prompt Engineering**: See `references/prompt_engineering.md` for advanced techniques and patterns
- **API Reference**: See `references/api_reference.md` for detailed API documentation

## Scripts

This skill provides four Python scripts:

1. **verify_api_key.py** - Verify API key
   - Check API key validity and account balance
   - Usage: `python scripts/verify_api_key.py`

2. **generate_and_wait.py** - Complete workflow (recommended)
   - Submits task and waits for completion
   - Usage: `python scripts/generate_and_wait.py "prompt"`

3. **imagine.py** - Submit generation task
   - Returns job_id immediately
   - Usage: `python scripts/imagine.py "prompt"`

4. **get_task.py** - Check task status
   - Query any task by job_id
   - Usage: `python scripts/get_task.py <job_id>`

All scripts require `LEGNEXT_API_KEY` environment variable.

## Best Practices

1. **Start with clear descriptions** - More detail usually produces better results
2. **Use appropriate aspect ratios** - Match the intended use case
3. **Iterate based on results** - Refine prompts based on what works
4. **Save successful prompts** - Build a library of effective patterns
5. **Mind the credits** - Each generation consumes Legnext API points
6. **Download important images** - Temporary storage may expire

## Notes

- Generation typically takes 30-80 seconds
- Initial wait: 10s before first status check
- Polling: Every 5s, timeout after 3 minutes
- Each request usually generates 4 image variations
- Images are temporarily stored; download for permanent use
- API usage is tracked via points system in Legnext dashboard
