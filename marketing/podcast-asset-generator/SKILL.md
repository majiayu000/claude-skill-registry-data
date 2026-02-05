---
name: podcast-asset-generator
description: "Automated generation of promotional assets for podcast episodes from transcripts. Use when the user provides a podcast episode transcript (markdown file) and needs: (1) a one-paragraph episode summary, (2) AI-generated featured image, (3) compelling quotes for social media, (4) short promotional video. Orchestrates transcript analysis, AI image generation via Replicate MCP, and video creation for complete episode marketing asset package."
---

# Podcast Asset Generator

## Overview

Transform raw podcast transcripts into a complete package of promotional assets. This skill analyzes transcript content, generates professional summaries, creates custom artwork via AI image generation, extracts shareable quotes, and produces short promotional videos—all optimized for podcast marketing workflows.

## Configuration

**All model settings and preferences are centralized in `config.md`.**  
This makes it easy to update models, aspect ratios, and other settings in one place.

**Current Models** (see config.md to change):
- **Image**: Read from config.md
- **Video**: Read from config.md

**Integration Method**: This skill uses the Replicate MCP server for direct API access through Claude's tool system. No Python scripts or API token management needed.

## Core Workflow

When a user provides a podcast transcript, follow this sequential process:

### 1. Analyze Transcript

**Input**: Markdown file containing episode transcript

**Expected Formats**:
- **Solo episodes** (most common): Plain text transcript without speaker labels
- **Interview episodes** (occasional): Transcript with speaker labels (e.g., "Noah:", "Guest:")
- **No timestamps**: Transcripts do not include time markers
- **Structure**: May include episode title/number at top, followed by content

**Process**:
- Read the full transcript to understand content, themes, and tone
- If interview format detected (speaker labels present), extract quotes from both speakers
- Use `scripts/analyze_transcript.py` to extract candidate quotes
- Identify key concepts and episode themes
- Assess overall tone and mood (contemplative, energetic, philosophical, etc.)
- Note: Script handles both solo and interview formats automatically

**Output**: Understanding of episode content and extracted quote candidates

### 2. Generate Episode Summary

**Requirements**:
- One paragraph, 100-150 words
- Structure: Hook → Core Content → Takeaway
- Conversational yet professional tone
- Present tense for describing content
- Specific enough to be meaningful, intriguing enough to attract listeners

**Reference**: See `references/prompt_guidelines.md` for detailed summary guidelines

**Process**:
1. Identify the main question or problem the episode addresses
2. Extract 2-3 core topics or teachings
3. Articulate the key takeaway or learning outcome
4. Craft engaging opening and closing sentences

**Example Structure**:
```
[Hook: What question does this answer?] [Core: Main topics explored] 
[Integration: How concepts connect] [Takeaway: What listeners will gain]
```

### 3. Create Image Prompt

**Requirements**:
- Generate prompt for AI image generation (Replicate FLUX or similar)
- Match episode tone and themes
- Visual metaphor for abstract concepts
- Clean, professional aesthetic suitable for podcast cover art
- Text-free design (text will be added separately)

**Reference**: See `references/prompt_guidelines.md` for proven prompt patterns

**Prompt Structure**:
```
[Style/Medium], [Main Subject], [Mood/Atmosphere], [Lighting], 
[Color Palette], [Composition], professional podcast cover art
```

**Process**:
1. Translate episode themes into visual metaphors
2. Determine appropriate style based on content:
   - Mindfulness topics → Minimalist, zen-inspired, nature elements
   - Philosophy topics → Abstract, geometric, conceptual
   - Practice topics → Clean modern, illustrative, actionable feel
3. Specify mood/atmosphere that matches episode tone
4. Include composition guidance (centered, rule of thirds, negative space)
5. Add quality modifiers (8k, professional, cinematic if appropriate)

### 4. Generate Image

**Using Replicate MCP Server**:

The skill uses Claude's Replicate MCP integration to generate images directly. No API token configuration needed.

**Model Selection**: Check `config.md` for the current image generation model.  
**Current Default**: `bytedance/seedream-3`

**Specifications**:
- Aspect ratio: 1:1 (square) for universal podcast compatibility
- Alternative: 16:9 for YouTube thumbnails
- Quality: High
- Number of outputs: 1

**Process**:
1. Read current model from config.md
2. Use Replicate MCP tool with the crafted image prompt
3. Wait for generation (typically 5-15 seconds depending on model)
4. Retrieve output URL from result
5. If result doesn't match episode tone, iterate on prompt and regenerate

**To Change Models**: Edit the "Image Generation Model" section in `config.md`

### 5. Select Best Quotes

**Requirements**:
- Extract 1-3 quotes from transcript
- Each quote: 50-150 characters optimal
- Standalone clarity (make sense without context)
- Emotionally resonant or thought-provoking
- Suitable for text overlay on video/social media

**Reference**: See `references/prompt_guidelines.md` for quote selection guidelines

**Process**:
1. Review quotes extracted by `analyze_transcript.py` script
2. Manually review transcript for additional compelling moments
3. Evaluate each quote against criteria:
   - ✓ Clear and concise
   - ✓ Emotionally engaging
   - ✓ Works without context
   - ✗ Avoid inside references
   - ✗ Avoid questions needing answers
   - ✗ Avoid complex multi-clause sentences
4. Select top 1-3 quotes
5. Clean up any filler words or minor grammar issues for readability

### 6. Create Video Prompt

**Requirements**:
- Generate prompt for 10-second promotional video
- Motion should enhance, not distract
- Space for text overlay (quote will be added in post)
- Cohesive with generated image style
- Loopable if possible

**Reference**: See `references/prompt_guidelines.md` for video prompt patterns

**Video Categories** (choose based on episode theme):

**Nature-Based** (Most Reliable):
```
Slow motion ocean waves gently rolling on sandy beach, warm golden hour lighting, 
peaceful and meditative, 10 seconds, seamless loop, space for centered text overlay
```

**Abstract Motion**:
```
Soft bokeh background with warm amber and teal tones, gentle floating particles 
moving upward, calm atmosphere, 10 seconds, text overlay compatible
```

**Symbolic/Metaphorical**:
```
Time-lapse of clouds moving over still mountain peak, representing impermanence 
and stability, slow horizontal pan, contemplative mood, 10 seconds
```

**Process**:
1. Choose video category that matches episode themes
2. Describe main visual element and motion
3. Specify pacing (slow/gentle for contemplative content, energetic for actionable)
4. Ensure description leaves space for text overlay
5. Add technical specs (10 seconds, loopable if appropriate)

### 7. Generate Video

**Using Replicate MCP Server**:

The skill uses Claude's Replicate MCP integration to generate videos directly. No API token configuration needed.

**Model Selection**: Check `config.md` for the current video generation model.  
**Current Default**: `bytedance/seedance-1-lite`

**Specifications**:
- Duration: 5-10 seconds (model dependent, aim for 10)
- Aspect ratio: 9:16 for Instagram Reels/Stories, or 1:1 for feed posts
- Quality: High

**Process**:
1. Read current model from config.md
2. Use Replicate MCP tool with the crafted video prompt
3. Wait for generation (typically 30-120 seconds depending on model and duration)
4. Retrieve output URL from result
5. Preview to ensure motion is smooth and appropriate

**To Change Models**: Edit the "Video Generation Model" section in `config.md`

**Note**: Different models may have specific parameter requirements or limitations. If generation has issues, simplify the prompt or try nature-based concepts (water, clouds) which tend to be most reliable across models.

### 8. Compile Final Output

**Deliverables**:

Present all assets in organized format:

```markdown
# Podcast Episode Assets

## Episode Summary
[One paragraph summary, 100-150 words]

## Featured Image
- **Image URL**: [Replicate MCP output URL]
- **Model Used**: [From config.md]
- **Prompt Used**: [Full image generation prompt]
- **Aspect Ratio**: 1:1 (or specify)
- **Suggested Use**: Podcast cover art, social media posts, episode thumbnail

## Selected Quotes
1. "[Quote 1 text]" (X characters)
2. "[Quote 2 text]" (X characters)  
3. "[Quote 3 text]" (X characters)

**Suggested Use**: Instagram stories, video text overlays, quote graphics

## Promotional Video
- **Video URL**: [Replicate MCP output URL]
- **Model Used**: [From config.md]
- **Duration**: 10 seconds
- **Prompt Used**: [Full video generation prompt]
- **Aspect Ratio**: [9:16 or 1:1]
- **Quote Overlay Suggestion**: Use Quote [#] with this video
- **Suggested Use**: Instagram Reels, YouTube Shorts, social media ads

## Next Steps
1. Download image and video assets (URLs may be temporary)
2. Add text overlays to video in editing software (CapCut, etc.)
3. Post summary to podcast show notes
4. Share assets across social media platforms
5. Save originals for future reference

## Technical Details
- Image Model: [From config.md]
- Video Model: [From config.md]
- Integration: Replicate MCP Server
- Generation Date: [timestamp]
```

**Format Options**:
- Markdown document (copy-paste ready)
- JSON structure (for programmatic use)
- Create artifact with visual presentation

## Quality Assurance Checklist

Before presenting final assets, verify:

**Summary**:
- ✓ 100-150 words
- ✓ Hook, content, takeaway structure
- ✓ No spoilers but specific enough to intrigue
- ✓ Free of typos and grammatical errors
- ✓ Tone matches episode

**Image**:
- ✓ Visually appealing and professional
- ✓ Reflects episode themes/mood
- ✓ Clean composition (not cluttered)
- ✓ Appropriate colors and lighting
- ✓ No unwanted text or artifacts

**Quotes**:
- ✓ Clear and standalone
- ✓ Appropriate length (50-150 chars)
- ✓ Emotionally engaging
- ✓ Free of context dependencies
- ✓ Clean grammar and punctuation

**Video**:
- ✓ Smooth motion (no jarring artifacts)
- ✓ 10 seconds duration
- ✓ Appropriate mood/pacing
- ✓ Space for text overlay
- ✓ Loops well (if applicable)

## Troubleshooting

**Issue**: Generated image doesn't match episode tone
- Adjust mood descriptors in prompt (serene → energetic, abstract → literal)
- Try different style keywords (minimalist, detailed, artistic, photographic)
- Review `references/prompt_guidelines.md` for alternative patterns

**Issue**: Quotes feel flat or generic
- Return to transcript for more specific moments
- Look for unique phrasings or unexpected insights
- Ensure quotes have emotional resonance, not just information

**Issue**: Video has artifacts or weird motion
- Simplify prompt (fewer elements, clearer motion description)
- Try nature-based prompts (more reliable)
- Consider using image-to-video instead of text-to-video

**Issue**: Summary is too vague or too specific
- Too vague: Add concrete examples of topics discussed
- Too specific: Remove minor details, focus on main themes
- Aim for "intriguing but informative" balance

## Bundled Resources

### config.md (PRIMARY CONFIGURATION)
**This is the single source of truth for all model settings.**  
Edit this file to change:
- Image generation model
- Video generation model
- Default aspect ratios
- Quality settings
- Brand preferences

**When to edit**: Whenever you need to change models or update generation preferences.

### scripts/analyze_transcript.py
Python script for automated transcript analysis. Extracts compelling quotes and identifies key themes. Use for initial quote candidates before manual curation.

**Usage**:
```bash
python scripts/analyze_transcript.py <transcript_file.md>
```

**Output**: JSON with extracted quotes and content analysis

### references/prompt_guidelines.md
Comprehensive guide to prompt engineering for podcast assets. Contains proven patterns, examples, and guidelines for:
- Image generation prompts by theme
- Video generation prompts by category
- Quote selection criteria
- Summary writing structure

**When to reference**: Before generating any images or videos, review relevant sections for best practices.

### Integration Notes
This skill uses the **Replicate MCP Server** for all AI generation:
- No API token management required
- Direct integration through Claude's tool system
- Access to all Replicate models
- Automatic credential handling

**Model Configuration**: All model selections are centralized in `config.md`. Change models by editing that file—no need to search through code or documentation.
