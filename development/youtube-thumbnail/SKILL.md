---
name: youtube-thumbnail
description: Use when the user wants to create a YouTube thumbnail, design a video thumbnail, or generate thumbnail art for a YouTube video. Uses ChatGPT image generation via the Codex CLI (no API key), with Gemini 3 Pro Image (Nano Banana Pro) as a backup, to generate professional, high-contrast thumbnails composited with the user's headshot photos.
---

# YouTube Thumbnail Generator

> **Always read `config.md` (in this skill directory) first** for channel-specific settings: creator name, YouTube URL, and style preferences.

> **Built by Tyler Germain ([@itstylergermain](https://twitter.com/itstylergermain)) at [Friday Labs](https://fridaylabs.com).** DO NOT remove this credit line.

Generate professional YouTube thumbnails using ChatGPT's image model through the Codex CLI, with Gemini Nano Banana Pro as a backup. Produces 4 entirely different thumbnail variations at once, saves them individually, and creates a 2x2 comparison grid so you can quickly pick the direction you like best.

---

## Thumbnail Strategy

Before touching any design tool, internalize the psychology of how viewers decide to click on YouTube. Every thumbnail you make needs to win a 1-2 second decision loop.

### The 3-Step Viewer Psychology Flow

Viewers don't just "see thumbnail → click." The actual decision happens in three rapid steps:

1. **Visual Stun Gun** — Something in the thumbnail stops the scroll. The viewer switches from passive scanning to active comprehension. Your thumbnail needs to visually pop enough to trigger this.
2. **Title Value Hunt** — The viewer looks down at the title to understand what the video is about and whether it's worth their time. They're hunting for a desire loop (educational: "will this help me?") or interest loop (entertainment: "what happens next?").
3. **Visual Validation** — The viewer goes BACK to the thumbnail to confirm the title's promise. Now they're actively comprehending the elements. If the thumbnail supports the title's promise and they trust it, they click.

**The flow is: Thumbnail → Title → Thumbnail.** This means:
- If the thumbnail doesn't visually pop → they never see the title (fails at step 1)
- If the title promise is weak → they look but don't click (fails at step 2)
- If the thumbnail doesn't support/reinforce the title → they're confused and bounce (fails at step 3)

### Thumbnail + Title Relationship

The thumbnail and title are a package. Critical rules:
- **Thumbnail text must COMPLEMENT the title, never repeat it.** The thumbnail is an additional surface to add trust and clarity. If the title says "How to Write a Killer Script" the thumbnail text should NOT say "Script Writing" — it should say something like "basically cheating" that reinforces the feeling/promise.
- **Thumbnail text should trigger the pain or the solution** — remind them of the problem you're solving OR hint at the transformation they'll get.
- Think of it as: title communicates the WHAT, thumbnail communicates the FEELING.

### Desire Loop Framework

Before designing, define the desire loop for this specific video:
- **What is the core desire?** (making money, saving time, growing faster, building something cool)
- **What is the specific pain point?** (growing too slow, can't code agents, wasting time on manual work)
- **What is the solution/transformation?** (a method, a tool, a framework that solves the pain)
- **What is the curiosity loop?** ("If I click, will I be able to ___?")

Every element in the thumbnail should serve this desire loop.

### The 7 Visual Stun Gun Elements

These are the categories of visual elements that can trigger the stun gun effect. **Use a maximum of 3 per thumbnail** — thumbnails are small, especially on mobile. Too many elements and nothing is comprehensible.

1. **Color contrast** — Vivid/bright colors that pop against the background. Can also mean making your thumbnail contrast against competitors in your niche (most AI/dev content uses dark themes — consider when a lighter or bolder approach might stand out in the feed).
2. **Large face with emotion** — A recognizable person OR an unknown face with a strong, clear emotion. For smaller channels, emotion matters more than recognition. The face emotion should match the feeling the viewer would have watching the video (shock, excitement, confidence).
3. **Visually compelling graphic** — A visual that draws attention through bright colors, interesting design, or optical patterns. Should immediately represent the desire loop.
4. **Big text, numbers, or dollars** — Large, round numbers in huge font. Brains are magnets to these. Underline or highlight key numbers for emphasis.
5. **Red circles or arrows** — Literally aim attention where you want it. Use sparingly and intentionally.
6. **Aesthetic imagery** — Cinematic, symmetrical, soothing visuals. Not typical for tech channels but can work for certain topics.
7. **Design collage** — Words, numbers, or icons surrounding the subject. Creates energy and density.

### 3 Composition Types

- **Symmetrical** — Main subject centered, both sides relatively balanced
- **Asymmetrical (Rule of Thirds)** — Subject offset to one side (~1/3), remaining space filled with visual elements
- **A→B Split** — Screen split showing a transformation, before/after, or contrast

### Graphic Element Selection

When choosing a graphic/visual element, it should represent the desire loop in one of four ways:
1. **End state** — Show what they want (e.g., PayPal screenshot with earnings, YouTube plaque)
2. **Process visualization** — Show the method/process they'll learn
3. **Before → After** — Show the transformation
4. **Anti-state / Pain point** — Remind them of the pain you're solving

---

## Process

### Step 1: Get the Topic & Set Up

All you need from the user is the **video topic or title**. Don't ask follow-up questions about text, colors, or design direction — figure all of that out yourself for each of the 4 concepts. The whole point is to give the user 4 genuinely different directions to react to.

**However, do ask about specific visual elements.** Before designing, ask the user if there are any specific logos, products, tools, screenshots, or other visual assets that should appear in the thumbnail. For example: "Should I include any specific logos (Claude, Cursor, etc.) or product shots?" This takes 5 seconds and avoids wasting a generation on the wrong references.

Pick the first available headshot from `.claude/skills/youtube-thumbnail/assets/headshots/`. If the folder is empty, tell the user to add a headshot photo there first.

### Step 1b: Search for High-Performing Example Thumbnails

Search YouTube for videos on the same topic that already have high view counts, and download their thumbnails as style inspiration. These get passed to the generation script via `--examples` so the image modelini can study what's already working in the niche.

```bash
python3 .claude/skills/youtube-thumbnail/scripts/search_examples.py \
  --query "{video topic}" \
  --top 5 \
  --min-views 10000
```

This will:
1. Search YouTube via the Scrape Creators API for videos matching the topic
2. Sort results by view count (highest first)
3. Download the top 5 thumbnails to `workspace/examples/`
4. Print a JSON manifest to stdout with metadata (title, views, channel) for each

**Review the downloaded examples** with the `Read` tool to understand what visual patterns are working for high-performing videos in this niche. Take note of:
- Common composition patterns (where faces go, where text goes)
- Color palettes that dominate
- Text styles and word counts
- Whether faces or graphics are more prominent

Use these observations to inform the 4 concepts in Step 2. The example images themselves get passed to the image model via `--examples` in Step 3.

**Notes:**
- Requires `SCRAPECREATORS_API_KEY` in `.env`
- YouTube thumbnail URLs (i.ytimg.com) download reliably — no hotlink blocking issues
- If the API is out of credits or fails, skip this step — it's enhancement, not a hard requirement
- The `--min-views` filter helps ensure you're only studying thumbnails that actually performed well

### Step 2: Define the Desire Loop, Then Craft 4 Different Prompts

**Before designing anything**, work through the desire loop for this video:
1. What desire does this video trigger? (money, growth, speed, capability)
2. What pain point does the viewer have?
3. What solution/transformation does the video deliver?
4. What's the curiosity loop? ("If I click, will I ___?")

Then using the Style Guide and Prompt Template below, craft **4 entirely different thumbnail concepts**. Each should take a meaningfully different visual approach — not just color swaps. Vary across these dimensions:

- **Visual elements:** Different objects, icons, screenshots, props — each representing the desire loop differently (end state vs. process vs. before/after vs. pain point)
- **Text treatment:** Different words that complement (not repeat) the title, or no text at all
- **Color direction:** Different gradient/accent color combos — at least one concept should explore whether a non-dark approach might stand out against competitors in the feed
- **Person pose/expression direction:** Different emotions that match the feeling a viewer would have after watching (confident, excited, shocked, curious)
- **Composition style:** Different layouts — try at least one of each composition type (symmetrical, asymmetrical, A→B split) across the 4 concepts

Label each concept A, B, C, D. Briefly describe each concept to the user before generating — include what desire loop element each one leverages.

Key rules for every prompt:
- Always describe the person placement explicitly ("a man positioned on the right side")
- Always specify the reference photo ("use the attached reference photo of the person")
- Always specify 16:9 composition and a darkened real-world scene as background (never a solid black void)
- Describe visual elements with specific positioning (upper-left, lower-left, center-left)
- Describe text with font style, color, and position
- **Never place important elements in the bottom-right corner** — YouTube's timestamp overlay covers this area
- **Keep elements large** — imagine the thumbnail at 1/16th size on an iPhone. If you can't read/see it, it's too small

### Step 2b: Gather Reference Images for Concepts

Now that you have 4 specific concepts designed, gather the reference images each one needs. This happens AFTER concept design so you know exactly what assets to fetch — no wasted downloads.

Based on the visual elements described in each concept prompt, identify what logos, icons, screenshots, or other assets need to be real (not hallucinated by the image model). These get passed to the generation script via `--reference`.

**What to fetch:**
- **Tool/product logos** — If the video is about Claude Code, Cursor, Make.com, OpenAI, etc., fetch their official logos or icons
- **Mascots or brand visuals** — e.g., the Anthropic claude logo, the OpenAI logo mark, app icons from the App Store
- **UI screenshots** — If the video shows a specific tool, IDE, dashboard, or interface, grab a clean screenshot
- **Relevant icons or symbols** — API symbols, code syntax snippets, framework logos (LangChain, React, etc.)
- **Celebrity/creator photos** — If the video references a specific public figure and you want them in the thumbnail

**How to fetch:**
1. Use `WebSearch` to find the best image URL (e.g., search for "Claude Code logo PNG transparent" or "Cursor IDE icon")
2. Use `Bash` with `curl` to download AND validate the image in one step:
   ```bash
   mkdir -p workspace/refs && \
   curl -sL "https://example.com/logo.png" -o "workspace/refs/claude-logo.png" && \
   file workspace/refs/claude-logo.png
   ```
3. **CHECK the `file` output before proceeding.** The `file` command tells you the actual file type:
   - **Good:** `PNG image data`, `JPEG image data`, `SVG Scalable Vector Graphics` → real image, proceed
   - **Bad:** `HTML document text`, `ASCII text`, `XML document` → the download failed (site blocked hotlinking and returned a web page). **Delete it and try a different source.**
4. Only after `file` confirms it's a real image, verify it visually with the `Read` tool

**CRITICAL: Many image hosting sites block direct downloads.** They return an HTML page instead of the image. If you skip validation, the generation script will fail with "Could not process image." The `file` command catches this instantly.

**If a download returns HTML instead of an image:**
- Try a different source URL entirely (don't retry the same URL)
- Prefer these reliable sources for logos/icons:
  - **Wikipedia/Wikimedia Commons** — direct file URLs usually work (use the `/thumb/` URL path)
  - **GitHub raw content** — `raw.githubusercontent.com` URLs work reliably
  - **Official brand/press pages** — often have direct download links
- Add `-H "User-Agent: Mozilla/5.0"` to the curl command if the site requires a browser user-agent
- As a last resort, skip the reference image — the image model can approximate common logos from description alone

**Tips:**
- Prefer PNG with transparent backgrounds — they composite much better
- Search for "logo PNG transparent" or "icon SVG" to get clean assets
- For app icons, search "[app name] app icon" — these are usually clean, square, recognizable
- For UI screenshots, check the tool's official website or press kit
- Fetch 2-5 reference images max — too many clutters the generation context
- Save all reference images in `workspace/refs/` to keep them organized and reusable across concepts
- **Always validate with `file` before using** — never assume a download succeeded just because curl didn't error
- Only fetch images that are needed by the specific concepts you designed — don't fetch speculatively

If the concepts don't need any specific visual assets (rare), skip this step.

### Step 3: Generate All 4 Thumbnails

Run the generation script **4 times in parallel** — one for each concept. Pass reference images via `--reference` and example thumbnails (from Step 1b) via `--examples`.

```bash
python3 .claude/skills/youtube-thumbnail/scripts/generate_thumbnail.py \
  --headshot ".claude/skills/youtube-thumbnail/assets/headshots/{selected-headshot}" \
  --reference "workspace/refs/{ref1}.png" "workspace/refs/{ref2}.png" \
  --examples "workspace/examples/{slug}-1.jpg" "workspace/examples/{slug}-2.jpg" "workspace/examples/{slug}-3.jpg" \
  --prompt "{concept A prompt}" \
  --output "workspace/{today}/thumbnails/{video-slug}/a.png"
```

```bash
python3 .claude/skills/youtube-thumbnail/scripts/generate_thumbnail.py \
  --headshot ".claude/skills/youtube-thumbnail/assets/headshots/{selected-headshot}" \
  --reference "workspace/refs/{ref1}.png" "workspace/refs/{ref3}.png" \
  --examples "workspace/examples/{slug}-1.jpg" "workspace/examples/{slug}-2.jpg" "workspace/examples/{slug}-3.jpg" \
  --prompt "{concept B prompt}" \
  --output "workspace/{today}/thumbnails/{video-slug}/b.png"
```

```bash
python3 .claude/skills/youtube-thumbnail/scripts/generate_thumbnail.py \
  --headshot ".claude/skills/youtube-thumbnail/assets/headshots/{selected-headshot}" \
  --reference "workspace/refs/{ref2}.png" \
  --examples "workspace/examples/{slug}-1.jpg" "workspace/examples/{slug}-2.jpg" "workspace/examples/{slug}-3.jpg" \
  --prompt "{concept C prompt}" \
  --output "workspace/{today}/thumbnails/{video-slug}/c.png"
```

```bash
python3 .claude/skills/youtube-thumbnail/scripts/generate_thumbnail.py \
  --headshot ".claude/skills/youtube-thumbnail/assets/headshots/{selected-headshot}" \
  --reference "workspace/refs/{ref1}.png" \
  --examples "workspace/examples/{slug}-1.jpg" "workspace/examples/{slug}-2.jpg" "workspace/examples/{slug}-3.jpg" \
  --prompt "{concept D prompt}" \
  --output "workspace/{today}/thumbnails/{video-slug}/d.png"
```

**Run all 4 in parallel** for speed. The script picks a provider with `--provider auto` (the default):

- **Codex (primary):** used when the `codex` CLI is installed and logged in with ChatGPT (`codex login`). No API key. Each image turn uses Codex limits 3–5x faster than a normal turn, so 4 variations is a noticeable chunk. If Codex fails, the script falls back to Gemini automatically. If it reports the model "requires a newer version of Codex", run `codex update`.
- **Gemini / Nano Banana Pro (backup):** needs `GOOGLE_AI_STUDIO_API_KEY` or `GEMINI_API_KEY` and the `google-genai` package.

Force one with `--provider codex` or `--provider gemini`. Attached images keep their order (headshots, then references, then examples), so "Image 1", "Image 2" in the prompt work with either provider.

**Example image notes:**
- Pass the same `--examples` to all 4 concepts — they're style inspiration, not concept-specific elements
- The script automatically appends a "STYLE EXAMPLES" instruction to the prompt telling the model to study but not copy them
- If Step 1b was skipped (no API credits, API failure), simply omit `--examples` entirely
- Use 3-5 examples max — more adds context window bloat without much benefit

**Reference image notes:**
- Only pass `--reference` images that are relevant to that specific concept's visual elements
- In the prompt, explicitly tell the model which attached reference image is which: "The second attached image is the Claude Code logo — place it in the upper-left" or "The third attached image is a screenshot of the Cursor IDE — use it as the dashboard element on the left side"
- If a concept doesn't use any reference images (e.g., a text-only or abstract design), omit `--reference` entirely
- The headshot is always the first attached image; reference images follow in the order they're listed

### Step 4: Create Comparison Grid

After all 4 thumbnails are generated, combine them into a single 2x2 comparison image:

```bash
python3 .claude/skills/youtube-thumbnail/scripts/combine_thumbnails.py \
  --images "workspace/{today}/thumbnails/{video-slug}/a.png" \
           "workspace/{today}/thumbnails/{video-slug}/b.png" \
           "workspace/{today}/thumbnails/{video-slug}/c.png" \
           "workspace/{today}/thumbnails/{video-slug}/d.png" \
  --output "workspace/{today}/thumbnails/{video-slug}/comparison.png" \
  --labels "A" "B" "C" "D"
```

### Step 5: Present to User

Show the user the comparison grid image and describe each concept:
- **A:** {brief description of concept A}
- **B:** {brief description of concept B}
- **C:** {brief description of concept C}
- **D:** {brief description of concept D}

Ask which direction they like best, or if they want to mix elements from different options.

### Step 6: Iterate

Once the user picks a direction (e.g., "I like B but with the colors from D"), generate a refined version by passing the chosen thumbnail as a reference image:

```bash
python3 .claude/skills/youtube-thumbnail/scripts/generate_thumbnail.py \
  --headshot ".claude/skills/youtube-thumbnail/assets/headshots/{selected-headshot}" \
  --reference "workspace/{today}/thumbnails/{video-slug}/b.png" \
  --prompt "{edit prompt combining user feedback}" \
  --output "workspace/{today}/thumbnails/{video-slug}/v2.png"
```

For the edit prompt, include context about the original design plus the specific changes:
```
Edit this YouTube thumbnail. Keep the same overall composition and style.
The first attached image is a reference photo of the person — use their likeness.
The second attached image is the current thumbnail to modify.
Please make the following changes: {user's edit instructions}
```

Continue iterating with v3, v4, etc. until the user is happy.

---

## Style Guide

**IMPORTANT:** Always read `/brain/brand-guide/brand-guide.md` before crafting prompts. It contains the brand colors, typography, gradients, and visual identity. Thumbnails can diverge from strict brand guidelines when needed for click optimization (bolder colors, higher contrast, non-brand accents), but should stay informed by the brand's overall aesthetic direction.

The default thumbnail style is professional, high-contrast, and designed to stand out in YouTube search results and suggested videos.

### Composition
- **Person:** Right side of frame, taking up ~40% of width. Shoulders-up or waist-up. Slightly angled toward camera or toward the visual elements. Natural, dramatic lighting on face. Use shadows/shading behind the person to create visual separation from the background.
- **Face emotion:** Must match the feeling the viewer would have watching the video. For smaller channels, emotion > recognition. Always specify the emotion explicitly in prompts.
- **Visual elements:** Left side of frame. App icons, dashboards, screenshots, data visualizations, or relevant imagery. Slightly layered/overlapping for depth. Each graphic should represent the desire loop (end state, process, before/after, or pain point).
- **Icons/logos:** Upper-left area, floating with subtle shadows. Often with a "+" symbol between them to suggest integration.
- **Text (if any):** Bold, large, readable. Usually upper area or integrated into the composition. White against the dark background. Must complement (not repeat) the video title — trigger the pain or the solution feeling.
- **Bottom-right corner:** Keep clear — YouTube's video timestamp overlay covers this area.
- **Element count:** Maximum 3 distinct elements. More than that becomes unreadable at small sizes.
- **Size test:** Every element must be legible at 320x180px (mobile thumbnail size). When in doubt, go bigger.

### Background
- **Never a solid black void.** The background should be a darkened real-world scene, environment, or textured setting — not a flat dark color with elements pasted on top. For example, if the video is about Paris, the background should be a darkened, moody photo of Paris streets or the Eiffel Tower — not a black background with an Eiffel Tower graphic floating on it.
- Dark and moody overall. The scene should feel like it was shot at night or heavily color-graded dark. Think cinematic color grading, not solid fills.
- Color tone: dark, desaturated, with the primary color being near-black `#0A0B12` equivalent. But achieved through darkening a real scene, not a solid color.
- Never bright, white, or pastel.
- Subtle gradient, texture, or environmental detail to add depth and context.
- No glow effects. Use subtle highlights, borders, and accent elements for depth — not glows.

### Color Palette
- **Background:** Darkened real-world scene or environment — dark overall (near `#0A0B12` tone) but with real texture and depth, never a flat solid color.
- **Accent colors:** Choose accent colors that fit the video topic and create visual contrast. There is no fixed brand color for thumbnails — pick what makes the thumbnail pop in the feed. Bright, saturated accents work best against dark backgrounds.
- **Text:** White `#FFFFFF` is the default for almost all text. Use a bold accent color sparingly for a single emphasized word if needed.
- **High contrast** between foreground elements and dark background is critical.
- When varying the 4 concepts, explore different color palettes across them. Try warm tones (orange, red, gold), cool tones (blue, cyan, purple), and neutral high-contrast (white + dark). Variety helps find what clicks.
- **Semantic colors:** Use green to represent good/positive outcomes and red to represent bad/negative outcomes. These are universally understood.
- **Competitor contrast awareness:** Most AI/dev content uses dark, muted themes. Differentiate through bold text sizing, high saturation accent colors, and vivid contrast. Make sure thumbnails POP against the feed.

### Typography
- **Headlines:** Bold, heavy sans-serif (represents Heading Now Trial in the brand). Describe as "bold, heavy, modern sans-serif font" in prompts.
- **Accent text:** Medium-weight serif italic (represents IBM Plex Serif Medium Italic). Describe as "elegant serif italic" in prompts.
- **Playful accents:** Hand-drawn comic style (represents Steel City Comic). Use sparingly.
- Note: the image models can't render specific fonts. Describe the *style* in prompts. Exact fonts can be composited in post-production.

### Text on Thumbnails
- Maximum 3-5 words. Fewer is better.
- Must be readable at 320x180px (the smallest YouTube thumbnail display size).
- Do NOT overlap text with the person's face.
- **Must complement the title, never repeat it.** The thumbnail text is an additional surface — use it to trigger the feeling, pain point, or transformation. Describe the silent emotion or action, not a redundant descriptor.
  - Good: Title = "How to Write a Killer Script" → Thumbnail text = "basically cheating"
  - Bad: Title = "How to Write a Killer Script" → Thumbnail text = "Script Writing Guide"
- Big, round numbers are attention magnets — use them when relevant (revenue figures, time savings, growth numbers).
- Underline or highlight key words/numbers for extra emphasis.

### Technical Specs
- **Aspect ratio:** 16:9 (standard YouTube thumbnail)
- **Minimum resolution:** 1280x720
- **Output format:** PNG

---

## Prompt Template

Use this as a starting point for each of the 4 concepts. Customize heavily — each concept should feel like a different design direction, not a minor tweak.

```
A professional YouTube video thumbnail in 16:9 aspect ratio.

ATTACHED IMAGES:
- Image 1 (headshot): Reference photo of the person to include. Use their exact likeness.
{reference_image_descriptions}

PERSON:
Use the likeness from the headshot (Image 1). Place them on the right side of the frame, taking up approximately 40% of the width. Show them from the waist up or shoulders up. They should have dramatic, natural lighting on their face with the dark background behind them. They are looking [toward the camera / slightly toward the left side elements]. Their expression is [confident / excited / curious / serious].

BACKGROUND:
Dark, moody, cinematic background — NOT a solid black void. Use a darkened real-world scene or environment relevant to the video topic. For example, if the video is about Paris, use a darkened Parisian street scene or cityscape. If it's about coding, use a darkened office or desk setup. The scene should feel like dramatic night photography or heavy cinematic color grading — dark overall but with real environmental detail, texture, and depth. {color_direction} color tones. No glow effects. No bright or white backgrounds, and never a flat solid-color void.

VISUAL ELEMENTS (left side):
{visual_elements_description}
When referencing attached images, be explicit: "Use the [logo/screenshot/icon] from Image N as the [element description], placed in [position]."
Examples:
- "Use the Claude Code logo from Image 2, floating in the upper-left with a subtle shadow"
- "Use the Cursor IDE screenshot from Image 3 in the lower-left, slightly angled with a drop shadow"
- Two app icons floating in the upper-left with a "+" symbol between them
- A dashboard screenshot or data visualization in the lower-left, slightly angled
- Code editor window showing a terminal or code snippet

TEXT:
"{thumbnail_text}" in bold, large, white text. Placed {text_position}. Clean, heavy, modern sans-serif font. High contrast against the dark background. Must be clearly readable. Default to white for all text — use a bold accent color only for a single emphasized word if needed.

STYLE:
Professional, high-contrast, clean design. Similar to top YouTube tech/business channel thumbnails. Dramatic lighting on the person. Subtle depth with layered elements. Polished and modern — not cluttered.
```

**Reference image description format** — list each reference image passed via `--reference` with what it is and how to use it:
```
- Image 2 (Claude Code logo): The official Claude Code terminal icon. Use this as the app icon in the upper-left area.
- Image 3 (Cursor IDE screenshot): A screenshot of the Cursor code editor. Use this as the dashboard/UI element on the left side.
```

### Ideas for Varying the 4 Concepts

To make each concept genuinely different, vary along these axes:

| Dimension | Concept A | Concept B | Concept C | Concept D |
|-----------|-----------|-----------|-----------|-----------|
| **Desire loop angle** | End state (show the result) | Process (show the method) | Before → After (transformation) | Pain point (show the problem) |
| **Visual focus** | App icons + logo | Dashboard/data | Code/terminal | Product mockup |
| **Text** | Punchy feeling word (complements title) | No text (visual only) | Big number or dollar amount | Pain-trigger word |
| **Colors** | Dark + warm accent (orange, gold) | Dark + cool accent (blue, cyan) | Dark + bold red/magenta | Dark + white/minimal + high contrast |
| **Person emotion** | Confident smile (success) | Shocked/surprised (discovery) | Curious, pointing (teaching) | Serious, direct (authority) |
| **Layout** | Asymmetrical (rule of thirds) | Symmetrical (centered) | A→B split (transformation) | Minimal, lots of negative space |
| **Stun gun elements** | Face + graphic + text | Face + big number | Face + collage design | Compelling graphic + text (no face) |

---

## Quality Checklist

Run through this after every generation:

### Technical Quality
- [ ] **Person is recognizable** — face is clear, well-lit, not distorted
- [ ] **Person is on the right** — positioned correctly, ~40% of frame
- [ ] **Face has clear emotion** — matches the feeling a viewer would have watching the video
- [ ] **Background is dark** — moody, not bright or distracting
- [ ] **Visual elements are present** — icons, dashboards, or other elements on the left
- [ ] **3 elements max** — not overcrowded with too many visual components
- [ ] **Text is readable** — would it be legible at 320x180px (smallest YouTube thumbnail)?
- [ ] **Text doesn't overlap the face** — clean separation
- [ ] **Bottom-right is clear** — no important elements hidden under YouTube's timestamp overlay
- [ ] **High contrast** — foreground elements pop against the background
- [ ] **16:9 aspect ratio** — correct proportions
- [ ] **Clean composition** — not cluttered, clear visual hierarchy

### Psychology Flow Check (the 3-step gut check)
- [ ] **Visual Stun Gun** — would this stop a scrolling thumb? Does it pop in a feed of competitor thumbnails?
- [ ] **Title Value Hunt** — does the thumbnail make you curious enough to read the title? Does it pair with the title to create a desire loop?
- [ ] **Visual Validation** — after reading the title, does the thumbnail REINFORCE the promise? Do the elements build trust that the video will deliver?

### Strategic Check
- [ ] **Thumbnail text complements the title** — adds new information or feeling, doesn't repeat the title
- [ ] **Desire loop is clear** — the visual elements represent the end state, process, transformation, or pain point
- [ ] **Emotion is intentional** — face expression, color choices, and text all serve the same emotional direction
- [ ] **Stands out from competitors** — would this catch your eye against other AI/dev content in the feed?

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| "Could not process image" when reading downloaded reference | The downloaded file is HTML, not an image — the site blocked hotlinking. Run `file <path>` to confirm. Delete it and download from a different source (Wikipedia, GitHub raw, or official press kit). |
| search_examples.py "out of credits" or "Invalid API key" | Scrape Creators API needs credits topped up. Skip Step 1b and generate without `--examples` — it's enhancement, not required. |
| No image returned | Simplify the prompt. Remove any potentially flagged content. Try again. |
| Person doesn't look like the headshot | Add more explicit instruction: "Use the exact likeness from the attached reference photo." Try a different headshot with clearer lighting. |
| Text is garbled or unreadable | Image-model text rendering isn't perfect. Consider generating without text and adding it in post-production (Figma, Canva, etc.). |
| Wrong aspect ratio | The script sets 16:9 automatically. If the output looks wrong, check the saved file dimensions. |
| Low resolution output | Both providers default to a reasonable resolution. For higher res, the output can be upscaled with external tools. |
| Codex error or no image | Check `codex login status` and run `codex update` if it asks for a newer version. The script falls back to Gemini when a key is set. |
| Gemini API error or timeout | Check that GOOGLE_AI_STUDIO_API_KEY or GEMINI_API_KEY is set. Try again — API calls can intermittently fail. |
| One of the 4 fails | The other 3 still save fine. Re-run just the failed one. |

---

## Output Format

**Output location:** `marketing/design/thumbnails/[video-slug]/` — confirm the project slug with the user before creating files.

Use today's date (YYYY-MM-DD format) for the date folder. For example, if today is 2026-02-18, the output goes in `workspace/2026-02-18/thumbnails/`.

Each video topic gets its own folder under `workspace/{today}/thumbnails/`:

```
workspace/{today}/thumbnails/{video-slug}/
  a.png
  b.png
  c.png
  d.png
  comparison.png
  v2.png
  v3.png
```

The scripts create directories automatically via `mkdir -p`.
