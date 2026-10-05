---
name: design
description: Design and build frontend components/pages — from Figma, reference URL, or description. Wraps the official `frontend-design` skill with site-awareness.
allowed-tools:
  - Bash
  - Read
  - Edit
  - Write
  - Glob
  - Grep
  - Agent
  - Skill
  - TodoWrite
  - mcp__claude_ai_Figma__get_design_context
  - mcp__claude_ai_Figma__get_screenshot
  - mcp__claude_ai_Figma__get_variable_defs
  - mcp__claude_ai_Figma__search_design_system
model: opus
argument-hint: <"figma <URL>" | "like <reference-URL>" | free-form component description>
---

# Design — site-aware frontend component builder

You are running the `design` skill. Your job: create production-grade frontend components that match the target site's existing design system. You wrap the official `frontend-design` skill with pre-flight context loading and post-processing.

## Architecture

**Pre-flight:** Read the site's CSS variables, fonts, colors, and existing component patterns to build a design context brief.

**Delegation:** Pass the enriched context to the `frontend-design` skill for actual code generation.

**Post-processing:** Verify generated code uses existing CSS variables, replace hardcoded values where possible, validate accessibility.

## Step-by-step

### Step 0 — Determine site root and mode

Parse `$ARGUMENTS`:
- If starts with `figma ` → Mode A (Figma-to-code), extract URL
- If starts with `like ` → Mode B (reference-inspired), extract URL
- Otherwise → Mode C (from description)

Site root: `--root <path>` argument from `$ARGUMENTS`, or default to current working directory. Convention: site repos live at `~/Sites/<name>/`.

### Step 1 — Pre-flight: build design context brief

Read up to 3 CSS files from the site root. Extract:
1. CSS custom properties (`--variable-name: value`)
2. Font stack (font-family declarations)
3. Color palette (from CSS variables)
4. Spacing scale (from CSS variables)
5. Existing component patterns (read 1-2 HTML files to understand button, card, form styles)

Compile into a **design context brief** — a structured summary like:

```
DESIGN SYSTEM BRIEF:
- Colors: --electric: #6C5CE7, --neon: #00F5D4, --warm: #FF6B6B, --ink: #1A1A2E
- Fonts: Montserrat (headings), Nunito (body), JetBrains Mono (code)
- Spacing: --s1: 0.5rem, --s2: 1rem
- Patterns: .btn (rounded, uppercase), .card (border-radius, shadow), .fade-up (scroll animation)
```

### Step 2 — Mode-specific preparation

**Mode A (Figma):**
1. Parse fileKey and nodeId from the Figma URL
2. Call `mcp__claude_ai_Figma__get_design_context` with `clientLanguages: "html,css,javascript"`
3. Present to user: design context brief + which CSS vars can be reused + which are new

**Mode B (Reference URL):**
1. Use the `scrape_site.py` tool or WebFetch to get the reference page
2. Spawn an Opus Explore subagent to analyze: layout patterns, color usage, typography, interactions
3. Present to user: design brief (what to adopt from the reference, what to adapt to our brand)

**Mode C (Description):**
1. Present to user: proposed design approach before generating

**APPROVAL GATE:** In all modes, wait for user approval before generating code.

### Step 3 — Generate code via the `frontend-design` skill

Delegate code generation to the `frontend-design` skill (Skill tool, `skill: frontend-design`). The aesthetic principles — typography, color, motion, spatial composition, anti-generic-AI guidelines — live in `frontend-design`. Do not duplicate them here.

Compose the prompt you pass to `frontend-design` as a single brief covering:

1. **The user's request** (Mode A: Figma context blob; Mode B: reference brief from the Explore subagent; Mode C: free-form description).
2. **Site-awareness constraints** that `frontend-design` must respect:
   - **Brand variables** — list the site's CSS custom properties verbatim from the design context brief and instruct the skill to use `var(--name)` instead of fresh hex/font values whenever a matching variable exists.
   - **Output target** — vanilla HTML/CSS/JS unless the pre-flight scan detected an existing framework (React, Vue, Astro, etc.); name the framework if so.
   - **File structure** — how the site organizes pages and shared CSS (one HTML file per page, single shared stylesheet, etc.) so the generated code drops in cleanly.
3. **Aesthetic latitude** — `frontend-design` is encouraged to commit to a bold direction; the only hard constraints are the brand variables above. Do not pre-narrow its aesthetic choices.

Capture the generated code from the `frontend-design` result. Do not write it to disk yet — Step 4 may rewrite hardcoded values.

### Step 4 — Post-process

After generating code:
1. Scan for hardcoded hex colors that match existing CSS variables → suggest replacing with `var(--name)`
2. Scan for hardcoded font-family that matches the site's stack → suggest `var(--font-*)`
3. Flag any new CSS variables introduced → add them to the shared CSS file with comments
4. Run `python3 tools/site_audit.py --root "<site_root>" --mechanical-only --checks accessibility_mechanical,link_integrity` on the output

Report: what was generated, which files were created/modified, any CSS variables added.

## Important constraints

1. **Brand consistency first.** Always use existing CSS variables before introducing new ones.
2. **Approval gate is mandatory.** Show the approach before generating code.
3. **Plain HTML/CSS/JS by default.** Only use a framework if the site already has one.
4. **Post-process is mandatory.** Always check for hardcoded values and accessibility.

## See also

- [workflows/figma_to_code.md](../../../workflows/figma_to_code.md) — the SOP
- [tools/site_audit.py](../../../tools/site_audit.py) — post-process validation
