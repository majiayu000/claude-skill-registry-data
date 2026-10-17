---
name: plan-design
description: Design planning entry point — reads DESIGN.md, CONTEXT.md, and ADRs plus a Linear issue, identifies all UI surfaces that need design, lets you choose which to work through, then for each surface conducts an alignment interview, generates three layout-archetype mockups via OpenAI image generation, lets you pick one, produces an HTML/CSS implementation, and attaches it to the Linear issue. Use when starting design work on any feature, when you need visual options before committing to layout, or any time you want a Linear ticket to carry its own design artifacts.
version: 0.2.0
---

# Plan Design

You are the design planning entry point for this project. Your job is to read the project's documentation, understand the feature from a Linear issue, identify every UI surface the issue requires, let the developer choose which surface(s) to design, and then walk through each one in turn: align on decisions, generate three layout mockups, produce an HTML/CSS implementation, and attach it to Linear so the artifacts travel with the ticket through development and review.

## Before you start

Verify `OPENAI_API_KEY` is available:

```bash
[ -z "$OPENAI_API_KEY" ] && echo "ERROR: OPENAI_API_KEY is not set. Export it first: export OPENAI_API_KEY=sk-..." && exit 1
echo "OPENAI_API_KEY is set."
```

Stop and show the error if it's missing — the image generation step has no fallback.

Also read `references/image-prompts.md` now so you have the prompt templates ready for Phase 2.

---

## Phase 0: Load Context

Build a complete picture before asking the user anything.

### 1. Fetch the Linear issue
The user invoked this skill with an issue ID (e.g. `/plan-design ENG-42`). Use `mcp__plugin_linear_linear__get_issue` to retrieve:
- Title
- Description
- Acceptance criteria (usually in the description body)
- Any linked issues that add context

### 2. Read project documentation
These files define the visual constraints the design must stay within:

- `DESIGN.md` — design tokens (colors, typography, spacing, border radius, shadows, breakpoints)
- `CONTEXT.md` — domain model, user types, product tone and voice
- `docs/ADR/*.md` — any ADRs that constrain the UI (accessibility requirements, framework choices, existing component decisions)

If `DESIGN.md` doesn't exist, warn the user before proceeding:
> "No DESIGN.md found in this project. Mockups will use sensible placeholder values but won't match your design system. Consider creating DESIGN.md before running this skill."
Continue with reasonable defaults (a clean neutral palette, system sans-serif font).

### 3. Extract design tokens
Pull these values from DESIGN.md for use in image prompts and HTML output:

| Token | Where used |
|-------|-----------|
| Primary color (hex) | Sidebar/nav background, image prompts |
| Accent/secondary color (hex) | CTAs, highlights, image prompts |
| Background color (hex) | Page background, image prompts |
| Text color (hex) | Body text, image prompts |
| Font family | Typography, HTML CSS, image prompts |
| Base font size + scale | HTML typography system |
| Border radius | Cards, buttons in HTML |
| Spacing scale | Layout and padding in HTML |

---

## Phase 0.5: Identify Surfaces

Before asking any design questions, enumerate every distinct UI surface the issue requires. A surface is any screen, view, modal, or drawer that needs its own layout design.

**Rules for identifying surfaces:**
- Each distinct route or full-page view = one surface
- Each modal or drawer with meaningful content = one surface
- Empty states, error states, and loading states count only if they have unique layout requirements distinct from the main view
- Inline edits, tooltips, and hover states do NOT count as separate surfaces

Present the list to the user:

```
Found N surfaces in [KEY] — [issue title]:

1. [Surface Name] — [one sentence: what the user does here]
2. [Surface Name] — ...
...

Which surface(s) would you like to design?
Enter a number, a comma-separated list (e.g. "1, 3"), or "all".
```

Wait for the user's selection. Record the chosen surfaces in order — this becomes the work queue. Each surface will go through Phases 1–5 in sequence.

---

## Per-Surface Loop: Phases 1–5

Repeat Phases 1 through 5 for each chosen surface. At the start of each iteration, announce which surface you're working on:

```
--- Surface [N of M]: [Surface Name] ---
```

Derive a **surface slug** from the surface name (lowercase, spaces → hyphens, e.g. "Profile Edit Form" → `profile-edit-form`). Use this slug in all file names for this surface.

---

## Phase 1: Alignment Interview

Before generating anything, align on what you're actually designing for this specific surface. The goal is to surface decisions that aren't in the docs.

Ask these questions, scoping them to the current surface:

1. **User:** Who is the primary person using the **[surface name]** screen? (admin, logged-in user, guest, etc.)
2. **Primary action:** What is the single most important thing they should be able to do on this screen?
3. **Clarification:** Is anything about this surface unclear or ambiguous before we start?
4. **Constraints:** Any hard constraints? (mobile-first, accessibility requirements, data density)
5. **References:** Any existing screens this should feel similar to?

Skip questions the docs or issue already clearly answer. Confirm your understanding in one or two sentences before proceeding.

---

## Phase 2: Generate Three Layout Archetype Mockups

The three options differ in information architecture — all three use the same design tokens and should feel like the same product family.

| Option | Archetype | Best for |
|--------|-----------|----------|
| A | **Sidebar nav** — persistent left panel + main content | Many nav sections, admin tools, content-heavy apps |
| B | **Top nav + card grid** — horizontal bar + responsive cards | Discrete items, dashboards, listings |
| C | **Full-width scroll** — no persistent nav, section-based | Onboarding flows, editorial content, landing pages |

### Building the prompts
Use `references/image-prompts.md` as your template. Fill every placeholder with real values from DESIGN.md tokens and the alignment interview. Include the surface name from the issue to anchor the content.

### Making the API calls

**IMPORTANT — use `chatgpt-image-latest` exactly as shown below. Do NOT use `dall-e-3`. Do NOT add `response_format` — this parameter is rejected by the current API. The model always returns base64; save it with `base64 -d`.**

Create the output directory and generate all three images (using the surface slug in the filenames):

```bash
mkdir -p ./design-assets

# Option A
curl -s https://api.openai.com/v1/images/generations \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d "{\"model\":\"chatgpt-image-latest\",\"prompt\":\"$PROMPT_A\",\"n\":1,\"size\":\"1536x1024\",\"quality\":\"high\"}" \
  | jq -r '.data[0].b64_json' | base64 -d > ./design-assets/[surface-slug]-option-a.png

# Option B
curl -s https://api.openai.com/v1/images/generations \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d "{\"model\":\"chatgpt-image-latest\",\"prompt\":\"$PROMPT_B\",\"n\":1,\"size\":\"1536x1024\",\"quality\":\"high\"}" \
  | jq -r '.data[0].b64_json' | base64 -d > ./design-assets/[surface-slug]-option-b.png

# Option C
curl -s https://api.openai.com/v1/images/generations \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d "{\"model\":\"chatgpt-image-latest\",\"prompt\":\"$PROMPT_C\",\"n\":1,\"size\":\"1536x1024\",\"quality\":\"high\"}" \
  | jq -r '.data[0].b64_json' | base64 -d > ./design-assets/[surface-slug]-option-c.png
```

If a call produces an empty file (0 bytes), retry that option once with the same prompt. If it fails again, note it and continue — two options are better than blocking.

---

## Phase 3: Present and Pick

```
Generated three layout options for [Surface Name] in ./design-assets/

Option A ([surface-slug]-option-a.png): Sidebar nav
  [2–3 sentences]

Option B ([surface-slug]-option-b.png): Top nav + card grid
  [2–3 sentences]

Option C ([surface-slug]-option-c.png): Full-width scroll
  [2–3 sentences]

Which direction would you like to go with? (A, B, or C — you can add notes)
```

Wait for their choice. Acknowledge any modifications before proceeding.

---

## Phase 4: Generate HTML/CSS Implementation

Delegate this step to a subagent via the `Task` tool to keep this session's context lean. Pass all context the subagent needs inline — it has no access to the conversation history.

**Spawn a Task with a prompt structured as follows:**

---
You are generating a production-quality static HTML/CSS mockup file.

**Output path:** `./design-assets/[surface-slug]-mockup.html`

**Surface:** [Surface Name]

**Chosen layout archetype:** [archetype name] [any user modifications from Phase 3]

**Design tokens (use these exact values as CSS custom properties at `:root`):**
- Primary: [primary-hex]
- Accent: [accent-hex]
- Background: [bg-hex]
- Surface: [surface-hex or white]
- Text: [text-hex]
- Font family: [font-family]
- Border radius: [radius value]
- Spacing scale: [spacing values]

**Linear issue:** [KEY] — [title]

**UI requirements from the issue and alignment interview:**
- [bullet each confirmed UI element, interaction, or constraint]

**Requirements:**
- Define all design tokens as CSS custom properties at `:root`
- Implement the chosen archetype structure faithfully
- Use realistic placeholder content (not "Lorem ipsum" — use plausible labels and data relevant to the feature)
- No external dependencies — inline all CSS, use system fonts as fallbacks, no CDN links
- First line of the file must be: `<!-- plan-design | Surface: [Surface Name] | Direction: [archetype name] | Issue: [KEY] | Date: [today's date] -->`

Write the file to `./design-assets/[surface-slug]-mockup.html` and confirm the path and file size when done.
---

Wait for the subagent to confirm completion before proceeding to Phase 5.

---

## Phase 5: Attach to Linear

Upload `[surface-slug]-mockup.html` only — no PNGs.

1. Use `mcp__plugin_linear_linear__prepare_attachment_upload` to get an upload URL
2. Upload the file content to that URL
3. Use `mcp__plugin_linear_linear__create_attachment_from_upload` to attach it to the issue

**Post a decision comment** using `mcp__plugin_linear_linear__save_comment`:

```
## [Surface Name] — Design Direction: [Archetype Name]

**Chosen for:** [brief rationale]

### Key decisions from alignment
- **Primary user:** [answer]
- **Primary action:** [answer]
- [any other decisions worth preserving]

### Asset (attached above)
- `[surface-slug]-mockup.html` — HTML/CSS implementation of the chosen direction

This asset is the implementation target and will be used for final review against the shipped feature.
```

---

## Continue to Next Surface?

After Phase 5, if more chosen surfaces remain in the queue, ask:

```
Surface [N] ([Surface Name]) complete. Ready to move on to surface [N+1]: [Next Surface Name]? (yes / skip / stop)
```

- **yes** — begin the next iteration from Phase 1
- **skip** — move to the surface after that
- **stop** — end the session now

---

## Done

After all surfaces are complete (or the user stops), tell the user:
- Which surfaces were completed and where their assets are locally (`./design-assets/`)
- That each surface's mockup.html is attached to [KEY] in Linear
- Any cross-surface structural notes worth flagging for implementation (e.g. shared nav patterns, consistent modal behavior)
