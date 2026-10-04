---
name: creative-review
category: video
description: "Meta-review skill for validating generated creative assets (videos, images, designs) against a reference style brief. Extracts frames, compares against style criteria, scores adherence, and produces actionable feedback for iteration. Self-improving feedback loop: each review refines the style brief for the next generation. Use when: (1) reviewing a generated video against a reference style, (2) validating visual quality of AI-generated content, (3) scoring style adherence of a Remotion composition, (4) comparing before/after creative iterations, (5) building a self-improving creative pipeline. Triggers on: 'review video', 'check style', 'creative review', 'style adherence', 'compare to reference', 'validate video', 'review reel', 'quality check'."
---

# Creative Review — Style Adherence & Feedback Loop

Validate generated creative assets against a reference style brief. Score adherence, produce actionable feedback, and feed improvements back into the generation pipeline.

## Compounding Skills

| Skill | Role |
|-------|------|
| `/agent-browser` | Watch generated videos, take screenshots, visual comparison |
| `/launch-video` | Style brief and quality checklist to validate against |
| `/content-creation` | Reference extraction, visual analysis with Gemini |
| `/blog-post` | Distribution quality gates |

## Review Pipeline

```
REFERENCE → EXTRACT BRIEF → GENERATE ASSET → REVIEW → SCORE → FEEDBACK → ITERATE
```

## Phase 1: Reference Extraction

When given a reference video or image:

1. **Download** the reference (`yt-dlp` for URLs, direct path for local files)
2. **Extract frames** at 1fps: `ffmpeg -i ref.mp4 -vf "fps=1" frames/frame_%03d.png`
3. **Analyze** each frame for:
   - Color palette (dominant colors, background, accent)
   - Typography (font style, size, placement, weight)
   - Composition (layout, perspective, depth)
   - Motion style (cuts, transitions, pacing)
   - Material treatment (glass, shadow, glow, reflection)
4. **Produce a style brief** — structured document capturing all visual attributes

### Style Brief Format

```markdown
## Style Brief: {Reference Name}

### Palette
- Background: {hex}
- Panel fill: {rgba}
- Text primary: {hex}
- Accent: {hex}

### Typography
- Font: {family}
- Weight: {bold/regular}
- Placement: {center/left/overlay}
- Max words per card: {N}

### Composition
- Panel perspective: {degrees}
- Panel material: {glass/solid/wireframe}
- Depth technique: {shadow/glow/parallax}
- Background treatment: {void/gradient/particles}

### Motion
- Entrance style: {spring/fade/slide}
- Scene duration: {N-N seconds}
- Transition type: {cut/crossfade/spring}
- Pacing: {fast/confident/slow}

### Audio
- Style: {ambient/narration/music}
- Sync points: {beat drops/scene changes}
```

## Phase 2: Asset Review

When given a generated asset to review:

### Video Review Process

1. **Extract frames** at 1fps from the generated video
2. **Compare frame-by-frame** against the style brief criteria
3. **Score each dimension** (0-10):

| Dimension | What to Check | Weight |
|-----------|---------------|--------|
| **Color adherence** | Does the palette match the brief? Dark void bg? Accent colors? | 15% |
| **Typography** | Font style, size, placement, word count per card | 10% |
| **3D perspective** | Are panels tilted? Proper perspective depth? | 15% |
| **Glass material** | Border glow, shadow, rounded corners, semi-transparency | 15% |
| **Motion quality** | Spring animations? Organic movement? No CSS transitions? | 15% |
| **Pacing** | Scene duration 3-5s? No rapid cuts? Confident rhythm? | 10% |
| **Particle/depth** | Background particles? Depth layering? | 5% |
| **Hook effectiveness** | Does the first 3s grab attention? | 10% |
| **Overall polish** | Does it feel professional? Would you stop scrolling? | 5% |

4. **Overall score**: Weighted average (0-100)

### Scoring Bands

| Score | Rating | Action |
|-------|--------|--------|
| 90-100 | Excellent | Ship it |
| 75-89 | Good | Minor tweaks, optional iteration |
| 50-74 | Needs work | Specific feedback, iterate before shipping |
| 0-49 | Redo | Major issues, regenerate with updated prompts |

## Phase 3: Feedback Generation

For each dimension scoring below 8/10, generate specific, actionable feedback:

### Feedback Format

```markdown
## Creative Review: {Asset Name}

**Overall Score**: {N}/100 ({Rating})
**Reference**: {Brief Name}

### Scores
| Dimension | Score | Notes |
|-----------|-------|-------|
| Color adherence | {N}/10 | {specific note} |
| Typography | {N}/10 | {specific note} |
| ... | ... | ... |

### Must Fix (score < 6)
1. {Specific issue} → {Specific fix with code/prompt change}
2. ...

### Should Fix (score 6-7)
1. {Issue} → {Fix}

### Nice to Have (score 8-9)
1. {Polish suggestion}

### What Worked Well
- {Positive observation}
- {Pattern to keep}
```

## Phase 4: Self-Evolution

### After Each Review Cycle

1. **If the fix worked** → Add the technique to the style brief as a confirmed pattern
2. **If the fix didn't work** → Document why and what was tried, update guidance
3. **If a new technique emerged** → Capture it and add to the relevant skill's references

### Style Brief Evolution

The style brief is a living document. After each review cycle:

```
Initial brief (from reference extraction)
  → Review #1 feedback applied
    → Review #2: new patterns discovered
      → Brief updated with confirmed patterns
        → Next generation starts from improved brief
```

### Cross-Skill Feedback

When review findings affect other skills, propagate:

| Finding | Update Target |
|---------|--------------|
| "Veo prompts produce static shots" | `/launch-video` Veo prompt patterns |
| "Subtitles are unreadable on mobile" | `/blog-post` reel-production.md |
| "Hook doesn't grab in 3 seconds" | `/blog-post` reel-production.md hook formulas |
| "Glass panels look flat" | `/launch-video` GlassPanel component |
| "Pacing too fast" | `/launch-video` scene duration guidance |

## Agent Behavior

### On Review Invocation

1. **Identify the asset** — video file path, URL, or generated content package
2. **Identify the reference** — style brief, reference URL, or skill defaults (e.g., `/launch-video` checklist)
3. **Extract frames** from both (if video)
4. **Score each dimension** against the brief
5. **Generate feedback** with specific fixes
6. **Report** — overall score, must-fix items, what worked

### Using /agent-browser for Video Review

When the asset is a deployed video (hosted URL):

```bash
# Install if needed
npm install -g @anthropic-ai/agent-browser

# Open and screenshot for review
agent-browser open "https://broomva.tech/images/writing/slug/reel.mp4"
agent-browser screenshot --output review-frame.png
```

For local files, use `ffmpeg` frame extraction instead.

### Quick Review Command

```
/creative-review /path/to/video.mp4 --against launch-video
```

This automatically:
1. Extracts frames from the video
2. Loads the `/launch-video` quality checklist
3. Scores each dimension
4. Reports findings with specific fixes

## Quality Gate Integration

The creative review can be wired as a **gate** in the `/blog-post` pipeline:

```
Phase 6 (Media) → Generate video
  → /creative-review scores the output
    → Score ≥ 75? → Proceed to Phase 7
    → Score < 75? → Iterate with feedback → Re-generate → Re-review
```

This creates an automatic quality loop — no substandard creative ships.
