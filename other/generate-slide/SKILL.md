---
name: generate-slide
description: "Creates a single project slide or one-page visual summary for a repo. Use when generating a project intro image or promotional slide."
when_to_use: "create slide, project slide, one-page summary, promotional image, repo intro slide"
allowed-tools: ["Read", "Write", "Edit", "Bash", "Glob", "Grep", "AskUserQuestion"]
argument-hint: "[project-path|description]"
---

# Generate Slide Skill

Automatically generates single-slide images that introduce and explain a project, using the Nano Banana Pro (Gemini 3 Pro Image Preview) API.

---

## Overview

Generates 3 patterns x 2 candidates each = 6 images total → quality check per pattern → retry if NG → outputs the best 1 image per pattern, 3 images total.

## Prerequisites

- `GOOGLE_AI_API_KEY` environment variable is set
- Nano Banana Pro (Gemini 3 Pro Image Preview) is enabled in Google AI Studio

## Feature Details

| Feature | Details |
|---------|--------|
| **Slide Image Generation** | See [references/slide-generator.md](${CLAUDE_SKILL_DIR}/references/slide-generator.md) |
| **Quality Assessment** | See [references/slide-quality-check.md](${CLAUDE_SKILL_DIR}/references/slide-quality-check.md) |

---

## Execution Flow

```
/generate-slide
    |
    +--[Step 1] Information Gathering
    |   +-- User-specified text or automatic codebase analysis (README, package.json, etc.)
    |   +-- Extract project name, overview, key features, and tech stack
    |
    +--[Step 2] Specification Confirmation (AskUserQuestion)
    |   +-- Size and aspect ratio (default: 16:9 / 2K)
    |   +-- Tone (tech, casual, corporate, etc.)
    |   +-- Points to emphasize (ask only when ambiguous)
    |
    +--[Step 3] Generate 3 patterns x 2 images (Nano Banana Pro API x 6 calls)
    |   +-- Pattern A: Minimalist (2 images)
    |   +-- Pattern B: Infographic (2 images)
    |   +-- Pattern C: Hero Visual (2 images)
    |
    +--[Step 4] Quality check per pattern
    |   +-- Claude reads the 2 images per pattern via Read
    |   +-- 5-level scoring → higher score becomes the candidate
    |   +-- Both score 2 or below → improve prompt and retry (up to 3 times)
    |   +-- Retry limit reached → report to user, choose to continue or skip
    |
    +--[Step 5] Output the best 3 images
        +-- Copy the best 1 image per pattern to selected/
        +-- Present the results list (path + score + evaluation comment) to the user
```

---

## Design Patterns

| Pattern | Concept | Characteristics |
|---------|---------|----------------|
| **Minimalist** | Whitespace and typography focused | clean, whitespace, typography-driven, elegant |
| **Infographic** | Data/flow visualization | data visualization, metrics, flow diagram, structured |
| **Hero Visual** | Large visual + catchphrase | bold visual, impactful, hero image, catchy headline |

---

## Output Destination

```
out/slides/
+-- minimalist_1.png       # Pattern A candidate 1
+-- minimalist_2.png       # Pattern A candidate 2
+-- infographic_1.png      # Pattern B candidate 1
+-- infographic_2.png      # Pattern B candidate 2
+-- hero_1.png             # Pattern C candidate 1
+-- hero_2.png             # Pattern C candidate 2
+-- selected/
|   +-- minimalist.png     # Pattern A best
|   +-- infographic.png    # Pattern B best
|   +-- hero.png           # Pattern C best
+-- quality-report.md      # Quality check results report
```

---

## Execution Steps

### Step 1: Information Gathering

Collect project information in the following priority order:

1. **User-specified text**: Use the project description if provided as an argument
2. **Automatic codebase analysis**: If no argument is provided, automatically analyze the following:
   - `README.md` — Project overview
   - `package.json` / `Cargo.toml` / `pyproject.toml` — Project name, description, dependencies
   - `CLAUDE.md` — Project structure and purpose
   - `Plans.md` — In-progress tasks (if present)

Information to extract:

| Item | Example |
|------|---------|
| Project name | Claude Code Harness |
| Overview (1-2 sentences) | A plugin for autonomous operation of Claude Code via Plan-Work-Review |
| Key features (3-5) | Skill management, quality checks, parallel execution |
| Tech stack | TypeScript, Node.js, Claude Code Plugin |
| Colors (if available) | Brand colors or inferred |

### Step 2: Specification Confirmation

Confirm the following via AskUserQuestion (only ask when ambiguous, as defaults are available):

```
Question 1: What size and aspect ratio for the slide?
  - 16:9 / 2K (recommended)
  - 4:3 / 2K
  - 1:1 / 2K
  - Custom

Question 2: What tone?
  - Tech (dark theme, code aesthetic)
  - Casual (bright, friendly)
  - Corporate (formal, trustworthy)
  - Creative (bold, art-oriented)
```

### Step 3: Image Generation

Follow the steps in `slide-generator.md` to generate 3 patterns x 2 images = 6 images.

Since each pattern's generation is independent, run curl in parallel where possible:

```bash
# Parallel execution example (3 patterns x 2 images)
for pattern in minimalist infographic hero; do
  for i in 1 2; do
    # Execute the curl pattern from slide-generator.md
    # → Save to out/slides/${pattern}_${i}.png
  done
done
```

### Step 4: Quality Check

Evaluate the 2 images per pattern according to the criteria in `slide-quality-check.md`:

1. Read each image via Read
2. 5-level scoring (information conveyance, layout, text readability, professionalism, brand alignment)
3. Select the higher-scoring image within each pattern as the candidate
4. Both score 2 or below → improve prompt and regenerate (up to 3 times)

### Step 5: Result Output

```bash
# Copy the best images to selected/
mkdir -p out/slides/selected
cp out/slides/minimalist_best.png out/slides/selected/minimalist.png
cp out/slides/infographic_best.png out/slides/selected/infographic.png
cp out/slides/hero_best.png out/slides/selected/hero.png
```

Generate the quality report (`out/slides/quality-report.md`):

```markdown
# Slide Quality Report

## Generation Info
- Project: {project_name}
- Generated at: {datetime}
- Aspect ratio: {aspect_ratio}
- Tone: {tone}

## Results Summary

| Pattern | Candidate 1 | Candidate 2 | Selected | Score |
|---------|------------|------------|----------|-------|
| Minimalist | 3/5 | 4/5 | Candidate 2 | 4/5 |
| Infographic | 4/5 | 3/5 | Candidate 1 | 4/5 |
| Hero Visual | 5/5 | 4/5 | Candidate 1 | 5/5 |

## Detailed Evaluation
...
```

---

## Error Handling

### GOOGLE_AI_API_KEY Not Set

```
GOOGLE_AI_API_KEY is not set.

Setup instructions:
1. Get an API key from Google AI Studio: https://ai.google.dev/aistudio
2. export GOOGLE_AI_API_KEY="your-api-key"
```

### Retry Limit Reached for All Patterns

Present options via AskUserQuestion:

```
Images for pattern {pattern} did not meet the criteria after 3 retries.

Options:
1. Use the highest-scoring image and continue
2. Skip this pattern
3. Manually specify a prompt and regenerate
```

---

## Related Skills

- `generate-video` — Product demo video generation (shares the image generation engine)
- `notebook-lm` — Document and slide generation (different approach)
