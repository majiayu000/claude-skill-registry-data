---
name: ozor-prompt-optimizer
description: "Analyze and improve existing Ozor.ai video prompts for better output quality. Use this skill whenever the user has an Ozor prompt that produced mediocre results, wants to improve a video prompt, needs help debugging why a video didn't turn out well, or wants expert feedback on their prompt before running it. Trigger on phrases like 'improve this prompt', 'optimize my Ozor prompt', 'why did my video look bad', 'fix this prompt', 'make this prompt better', 'review my Ozor prompt', 'the video didn't turn out right', 'prompt feedback', 'better results from Ozor', or any request to refine, debug, or enhance an existing Ozor video prompt."
---

# Ozor Prompt Optimizer

Analyze existing Ozor.ai video prompts and transform them from vague or underperforming into specific, high-quality prompts that produce great results on the first try. This skill acts as a prompt quality reviewer — it identifies what's missing, what's vague, and what can be improved, then rewrites the prompt.

## When to Use This Skill

- User has a prompt that produced a mediocre video
- User wants a prompt reviewed before running it
- User is iterating on a video and can't get the result they want
- User asks "why does my video look generic/bad/wrong?"
- User pastes an existing prompt and asks for improvements

## The Prompt Quality Framework

Every Ozor prompt is scored on six dimensions. A great prompt scores high on all six.

### 1. Specificity (most impactful)

**Bad:** "Show the product"
**Good:** "Show the TaskFlow dashboard with 3 task columns (To Do, In Progress, Done), each containing 2–3 task cards. Zoom in on a card being dragged from 'To Do' to 'In Progress'."

Ozor generates better output when it knows exactly what to render. Vague prompts force the AI to guess, and its guesses will be generic.

**Check for:**
- Are visual descriptions concrete? (colors, layouts, animations)
- Is text on screen explicitly written out, not just described?
- Are scene transitions specified?
- Is the overall visual style defined beyond just "clean" or "modern"?

### 2. Structure

**Bad:** A long paragraph describing the whole video.
**Good:** Numbered scenes, each with a clear title and single purpose.

**Check for:**
- Is the prompt broken into numbered scenes?
- Does each scene have exactly one job?
- Is there a logical flow (hook → content → CTA)?
- Are scenes ordered for maximum impact?

### 3. Constraints

**Bad:** "Make a video about my product"
**Good:** "Create a 45-second landscape (16:9) video with 12 scenes"

**Check for:**
- Duration specified?
- Aspect ratio specified (16:9 or 9:16)?
- Scene count specified?
- Maximum text per scene implied or stated?

### 4. Visual Direction

**Bad:** "Make it look nice"
**Good:** "Dark background (#1a1a2e), white text, electric blue (#3B82F6) accents. Minimal style — no gradients, no 3D effects. Clean sans-serif typography."

**Check for:**
- Background color/style specified?
- Accent colors provided (hex codes are best)?
- Animation style described?
- Typography direction given?
- Mood/atmosphere defined?

### 5. Audience Awareness

**Bad:** No mention of who the video is for.
**Good:** "Audience: startup founders who are frustrated with project management tool sprawl. Tone: empathetic but confident."

**Check for:**
- Target audience stated?
- Tone of voice defined?
- Language level appropriate for the audience?
- Jargon calibrated to audience expertise?

### 6. Actionable CTA

**Bad:** No CTA, or "Check us out"
**Good:** "Final scene: 'Start your free trial — taskflow.app'. Large centered text, logo below, subtle pulse animation on the URL."

**Check for:**
- Is there a final scene with a CTA?
- Is the CTA specific (URL, action, benefit)?
- Is the CTA visually prominent?

## Optimization Workflow

### Step 1 — Diagnose

Read the user's prompt and score each dimension:

```
## Prompt Analysis

| Dimension | Score | Issue |
|-----------|-------|-------|
| Specificity | Low/Medium/High | [what's missing] |
| Structure | Low/Medium/High | [what's missing] |
| Constraints | Low/Medium/High | [what's missing] |
| Visual Direction | Low/Medium/High | [what's missing] |
| Audience Awareness | Low/Medium/High | [what's missing] |
| CTA | Low/Medium/High | [what's missing] |

**Overall:** [Quick summary of the main issues]
```

### Step 2 — Explain

For each low-scoring dimension, explain briefly:
- What's wrong
- Why it matters for Ozor's output
- What the fix looks like

Keep explanations concise — the user wants a better prompt, not a lecture.

### Step 3 — Rewrite

Produce a complete, optimized prompt that the user can copy-paste directly into Ozor. The rewrite should:

- Fix every identified issue
- Preserve the user's intent and content
- Add specificity where it was vague
- Add structure where it was unstructured
- Add constraints where they were missing
- Add visual direction where it was absent
- Maintain the same overall message

Present the rewrite in this format:

```
## Optimized Prompt (copy and paste into Ozor)

Create a [duration] [format] video for [product/topic].

[N] scenes:

(1) [Scene title] — [Detailed, specific direction]

(2) [Scene title] — [Detailed, specific direction]

[...all scenes...]

Style: [specific visual direction with colors, mood, typography].
Tone: [defined tone].
Audience: [specified audience].
```

### Step 4 — Explain Changes

After the rewrite, provide a brief diff summary:

```
## What Changed

- **Added:** [what was missing and is now included]
- **Improved:** [what was vague and is now specific]
- **Restructured:** [what was reorganized]
- **Removed:** [what was unnecessary or counterproductive]
```

## Common Problems and Fixes

### Problem: "The video looks generic"
**Cause:** Prompt lacks specificity and visual direction.
**Fix:** Add concrete visual descriptions, brand colors, specific text content, and animation style.

### Problem: "The text is too long on screen"
**Cause:** Prompt includes full sentences or paragraphs as on-screen text.
**Fix:** Rewrite on-screen text as short headlines (5–8 words) and brief bullets (3–6 words). Move detailed explanations to narration notes or cut them.

### Problem: "The scenes don't flow well"
**Cause:** Prompt has no clear narrative structure.
**Fix:** Reorganize into Hook → Problem → Solution → CTA. Ensure each scene logically leads to the next.

### Problem: "The style doesn't match my brand"
**Cause:** No brand colors, no style direction, or conflicting style cues.
**Fix:** Add specific hex colors, define background style (dark/light), specify typography mood, and reference brand assets.

### Problem: "The video is too long/boring"
**Cause:** Too many scenes, too much content per scene, or no hook.
**Fix:** Cut to essential scenes only. One idea per scene. Ensure scene 1 is a strong hook that creates curiosity.

### Problem: "The CTA is weak"
**Cause:** No CTA scene, or CTA is vague ("learn more").
**Fix:** Add a dedicated final scene with specific action text, URL, and visual emphasis.

### Problem: "Ozor didn't understand what I wanted"
**Cause:** Ambiguous language, conflicting instructions, or too many requests in one prompt.
**Fix:** Use direct, unambiguous language. One instruction per scene. Remove contradictory style cues.

## Before/After Examples

### Example 1: Vague → Specific

**Before:**
```
Make a video about our new AI feature. Show how it works and make it look professional.
```

**After:**
```
Create a 30-second landscape (16:9) video announcing Smart Assist, [Product]'s new AI feature.

10 scenes:

(1) Hook — Bold white text on dark navy (#0f172a) background: "Your assistant just got smarter." Text appears with a typewriter animation.

(2) Problem Setup — A user staring at a cluttered inbox, overwhelmed expression. Text: "Sound familiar?" Subtle zoom-in on the overflowing email list.

(3) Problem Impact — Split screen: left side shows repetitive tasks piling up (emails, reports, calendar invites), right side shows a clock counting up. Text: "Hours lost to repetitive tasks."

(4) Solution Reveal — Screen clears to a clean dark background. The Smart Assist logo animates in with a soft glow. Text: "Meet Smart Assist." Green (#22c55e) accent pulses around the logo.

(5) Feature Detail — Show a clean UI with an AI suggestion popup appearing. The popup reads: "I noticed you send this report every Monday. Want me to automate it?" A cursor clicks "Yes". Smooth animation.

(6) How It Works — Three-step animation: (a) Smart Assist scans your workflow, (b) identifies patterns, (c) suggests automations. Each step appears as a minimal icon with a label, connected by animated lines.

(7) Before/After — Side-by-side comparison. Left: "Before" — cluttered dashboard, 12 manual tasks. Right: "After" — clean dashboard, 3 tasks remaining. A green checkmark animates over the "After" panel.

(8) Social Proof — Text: "Saving teams 6+ hours per week." A subtle counter animates from 0 to 6. Small quote: "It's like having a second brain." — Beta User.

(9) CTA Text — Large centered text: "Try Smart Assist today." Subtext: "product.com/smart-assist". Subtle glow animation on the URL.

(10) Logo Close — Product logo centered on dark navy background, tagline beneath: "Work smarter, not harder." Gentle fade out.

Style: dark navy background (#0f172a), white text, green (#22c55e) accent for the AI elements. Clean, minimal, modern. No gradients.
Tone: confident and forward-looking.
Audience: existing users who handle repetitive workflows.
```

### Example 2: Wall of Text → Structured

**Before:**
```
I want a video that talks about how our platform helps developers build faster with pre-built components, automatic deployment, real-time collaboration, built-in testing, and a great developer experience. It should also mention we have 50k users and were featured in TechCrunch. The video should end with a free trial CTA and be suitable for our website.
```

**After:**
```
Create a 45-second landscape (16:9) video for [Platform Name], a developer platform for building apps faster.

12 scenes:

(1) Hook — "Ship 10x faster." Large bold text, centered on dark background. Subtle code particles floating in the background.

(2) The Pain — A developer surrounded by terminal windows, config files, and loading spinners. Text: "Tired of boilerplate?" Frustrated emoji-free tone, code scrolling in the background.

(3) Platform Intro — Clean transition to the [Platform Name] logo on dark background (#0d1117). Text: "Meet [Platform Name]." Blue (#58a6ff) glow animates around the logo.

(4) Feature: Components — Show a component library panel with pre-built UI elements. A developer drags a button component into a canvas, and it renders instantly. Text: "Pre-built components. Zero config."

(5) Feature: Real-Time Preview — Split-panel code editor. Left: code being typed. Right: live preview updating character by character in real time. Text: "See changes instantly."

(6) Feature: Collaboration — Two cursors moving on the same code file, each labeled with a developer name. Edits appear simultaneously. Text: "Real-time collaboration. No merge conflicts."

(7) Feature: Testing — A test suite runs in a terminal panel. Green checkmarks cascade down the list. Text: "Built-in testing. Ship with confidence."

(8) Feature: Deployment — A single "Deploy" button is clicked. An animation shows the app going live — a progress bar fills, then a live URL appears. Text: "One-click deploy. Zero downtime."

(9) Social Proof — "50,000+ developers." Counter animates from 0 to 50,000 with a satisfying tick effect. Below: TechCrunch logo and a quote: "The fastest way to ship." — TechCrunch.

(10) Community Proof — A grid of small developer avatars populates the screen. Text: "Join the community." Avatars gently pulse.

(11) CTA — "Start building for free." URL: "[platform.com]". Large centered text with blue (#58a6ff) underline animation on the URL.

(12) Logo Close — [Platform Name] logo centered. Tagline: "Build faster. Ship sooner." Code particles drift softly in the background. Fade out.

Style: dark background (#0d1117), white and gray text, blue (#58a6ff) accents. Developer-tool aesthetic — monospace font for feature names, sans-serif for headlines.
Tone: technical but accessible. Confident, not hype-y.
Audience: full-stack developers evaluating new tools.
```

## Rules

1. **Always produce a complete rewrite.** Don't just list suggestions — give the user a finished, copy-pasteable prompt.
2. **Preserve the user's intent.** The optimized prompt should make the same video, just better. Don't change the message, product, or audience unless asked.
3. **Be honest about what's wrong.** If the prompt is mostly fine, say so. Don't invent problems to seem thorough.
4. **Specificity is the #1 lever.** When in doubt, make it more specific. Vague prompts are the most common cause of disappointing Ozor output.
5. **Don't over-engineer.** A clear, specific 12-scene prompt beats an unfocused 20-scene prompt. Simpler is better.
6. **Ask before assuming.** If the prompt is missing critical info (product name, audience, brand colors), flag it with `[VERIFY: ...]` rather than guessing.
