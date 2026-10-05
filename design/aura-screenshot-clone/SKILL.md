---
name: aura-screenshot-clone
description: "Use when the user wants to clone or adapt a UI pattern from any website into gotcontext.ai, or asks to \"build something like X\", \"make our nav look like Y\", or \"clone that component\". Prefer aura.build Pro when available; without a Pro subscription, skip Aura and go straight to Phase 2.5 direct rebuild. Aura's clone is now NATIVE — paste a URL or drag a screenshot into aura.build and it generates React/Tailwind directly; the Anima/Chrome-extension flow is only a fallback for login-gated pages Aura can't fetch server-side."
---

# Aura Screenshot-to-Component Pipeline

## Overview

Full pipeline for cloning any web UI pattern into a gotcontext.ai React/Next.js component: paste a URL or drag a screenshot into aura.build → it generates React/Tailwind directly → adapt in Claude Code. The user points at a reference; you handle everything else.

> **No Aura Pro subscription?** Skip Phases 2–2d and go straight to **Phase 2.5 — Direct rebuild fallback**. Capture reference screenshots (Phase 1) when useful, then rebuild in React/Tailwind without aura.build.

> **Clone primitive (updated 2026-06-06, per `docs/audits/2026-06-06-ui-ux-design-pipeline-playbook.md` gap #3):** Aura's clone is **NATIVE** — paste a URL or drag in a screenshot and Aura converts it to React-mode components in-app. No Chrome browser extension is required for the core flow. The Anima/Chrome-extension path is only a **fallback for login-gated pages** Aura can't fetch server-side (use the screenshot-upload path below). Figma export (Phase 3) is optional/downstream for design review only.

**Core principle:** Never write layout from scratch when you can URL-import / screenshot → convert → adapt. AI vision at ~90% in one shot; you spend effort only on the 10% that makes it uniquely gotcontext.ai.

> This is one branch of the broader design-to-code router (**Path 1C**). Sibling paths:
> - **1A** Claude Design → `claude-design`
> - **1B** Figma SoT → Figma MCP / `figma-design-to-code`
> - **1C** Clone reference URL/screenshot → **this skill** (`aura-screenshot-clone`)
> - **1D** Google Stitch MCP (NL → high-fi screens → code) → `stitch-mcp-design`
>
> Use Stitch when you are **authoring** a new UI in Stitch, not when cloning an existing live site (Aura).

---

## Decision gate — which input path to use

Before anything else, pick the **input path** to aura. Two options, order of preference:

1. **URL import (preferred)** — aura fetches and screenshots the reference itself. Skip manual screenshots entirely. **Fails on sites that block server-side fetches** (Cloudflare, anti-bot WAFs, login-walled content). Known to fail: `artificialanalysis.ai`, `openrouter.ai`, many high-traffic SaaS comparison sites. Known to work: most marketing pages (Anthropic, Vercel, Stripe, GitHub pricing), Wikipedia, blog posts.
2. **Screenshot upload** — you capture via `mcp__claude-in-chrome__computer action=screenshot` and attach via aura's paperclip. Works for any site you can load in the browser, including login-walled content. Slower and requires juggling an OS file dialog — **only reachable if the image is saved to a local path that the browser file picker can reach**, which the MCP screenshot pipeline does not provide out of the box. In practice this path is unreliable from Claude Code without a local-filesystem helper.

**Rule:** Try URL import first. If aura shows "URL import failed — Failed to fetch" (within ~3s), don't retry on the same domain — pick a different reference or fall back to the **no-aura direct rebuild** (see Phase 2.5 below).

Do **not** spend more than one URL attempt per reference. If two references in a row fail, stop the aura path and go direct.

---

## Phase 1 — Capture the Inspiration

### 1a. Get a tab context first
```
mcp__claude-in-chrome__tabs_context_mcp
```
Always do this before any browser action.

### 1b. Create a fresh tab, navigate, resize to 1440×900
```
mcp__claude-in-chrome__tabs_create_mcp
mcp__claude-in-chrome__resize_window  width=1440  height=900  tabId=NEW_TAB
mcp__claude-in-chrome__navigate  url="INSPIRATION_URL"  tabId=NEW_TAB
```

### 1c. Optional — take reference screenshots for your own understanding

Even when using URL import (Phase 2a), you should take 1–2 screenshots **yourself** so you can describe what to preserve vs. change in the prompt. Aura only gets the URL; the prompt is where you express taste.

```
mcp__claude-in-chrome__computer  action="screenshot"  tabId=TAB
mcp__claude-in-chrome__computer  action="scroll"     scroll_direction=down  scroll_amount=10  tabId=TAB
mcp__claude-in-chrome__computer  action="screenshot"  tabId=TAB
```

Save a note of the 3–5 visual patterns you want to carry over (left nav, summary pills, bar chart, provider colors, etc.).

---

## Phase 2 — Convert in aura.build

### 2a. Navigate to aura Create
```
mcp__claude-in-chrome__navigate  url="https://www.aura.build/create"  tabId=TAB
```

### 2b. Default model is fine — usually

As of 2026-04, the default model on aura's create page is **Gemini 3.1 Pro** (labeled "Best For UI"). That's a valid choice — skip the model-switch step unless you need to change it. If it's showing **Nano Banana** (image generator) or similar, switch to Claude 4.6 Opus or Gemini 3.1 Pro first; the image generators produce garbage for this task.

### 2c. Use URL import (the chain-link icon)

The chain-link icon in the composer toolbar opens an **Import Website** modal. This is the preferred input path — aura fetches + screenshots the URL itself. Approximate coordinates at 1440×900: the icon is in the bottom bar of the prompt composer, between the paperclip and the Figma logo.

Flow:
1. Click the chain-link icon → "Import Website" modal appears.
2. Type the URL in the input field.
3. Click **Different** (not "Exactly") — tells aura to **adapt the pattern** rather than reproduce pixel-for-pixel. Essential for rebranding.
4. Click **Import**.
5. Wait for the toast. **Failure signature**: a "URL import failed — Failed to fetch" toast near the top of the viewport. This is definitive — don't retry the same URL.

If the toast appears, cancel the modal and either (a) try a different reference or (b) bail to the direct rebuild path (Phase 2.5).

### 2d. Prompt template

After URL import succeeds, aura pre-populates the prompt with placeholder text like "Paste a design screenshot". Click the prompt area and add the conversion brief:

```
Reference: [short description, e.g. "LLM model comparison page"]

KEEP from reference:
- Overall layout structure and spacing rhythm
- Component hierarchy and grouping (e.g., summary-pill row, left-nav, per-section cards)
- Responsive breakpoint logic

CHANGE to gotcontext.ai brand:
- Background: #030304 (near-black)
- Primary accent: #33d2ff (cyan)
- Secondary accent: #4a8cff (blue)
- Text main: #f4f4f6 (off-white)
- Text muted: #888894
- Font: Inter (body), Outfit (display/headings)
- All copy: change to gotcontext.ai context (AI compression, tokens, MCP)
- Remove all unrelated branding, logos, images

IMPLEMENTATION:
- Pure Tailwind CSS + vanilla JS (no frameworks)
- Responsive: mobile-first, lg: breakpoint for desktop nav
- Dark theme throughout
- Add hover states with opacity/transform transitions
- Use Lucide icons where icons are needed
```

If URL import is working you do **not** also attach a screenshot via the paperclip — aura already has the captured image. Attaching both confuses the model.

### 2d. Submit and wait for generation (~15–60 seconds)

### 2e. Iterate with targeted edits if needed

For specific fixes, use the "Ask for revisions" input with targeted prompts:
```
"Change only the CTA button: apply linear-gradient(135deg, #33d2ff, #4a8cff) background with 8px border-radius and glow box-shadow"
"Fix the nav: reduce font to 13px uppercase tracking-widest"
"Make the mobile hamburger use the animated X pattern"
```

### 2f. Switch to Code view to review the HTML

Click the **Code** tab. Verify:
- [ ] Background colors are dark (#030304 or rgba variations)
- [ ] Cyan accent (#33d2ff) used for highlights/CTAs
- [ ] No proprietary frameworks in `<script>` tags
- [ ] Tailwind CDN is loaded

---

## Phase 2.5 — Direct rebuild fallback (when aura fails)

If URL import fails on 2+ references, or aura generation stalls, **bail out and build directly in React**. Aura's best case is a clean single-screen marketing layout; it's hit-or-miss on data-dense analytics pages.

When you fall back:

1. Keep the screenshots you captured in Phase 1c. They're still the reference.
2. Identify the 3–5 patterns you want to carry over: structural (e.g., left-side section nav, summary-pill row, horizontal bar chart, per-section cards) and visual (provider color coding, badge style, divider treatments).
3. Build directly in the target React component. Use pure Tailwind + inline styles where needed for provider-specific colors. Avoid chart libraries — CSS-only horizontal bars (`<div>` with width % and gradient background) render beautifully and ship zero kB.
4. Match the gotcontext brand tokens from Phase 2d exactly (`#030304` bg, `#33d2ff` cyan, etc.).
5. Every data-dense section should have a keyword-rich H2/H3 — SEO pays back the manual-build cost.

Total time for direct rebuild on a medium-complexity page: ~10–15 minutes once the reference is in your head. Faster than fighting aura when it's not cooperating.

## Known reference-site behavior (for Phase 2c)

Update this list as you find new ones. The goal: skip URLs you know will fail before trying.

| Site | URL import | Notes |
|---|---|---|
| `artificialanalysis.ai` | ❌ blocks | Cloudflare / anti-scrape. Use it as a visual reference only. |
| `openrouter.ai` | ❌ blocks | Same as above. |
| `anthropic.com/pricing` | ✅ usually works | Clean dark-tolerant layout. |
| `stripe.com/pricing` | ✅ works | High-quality pricing table reference. |
| `vercel.com/pricing` | ✅ works | Good card-based pricing pattern. |
| `openai.com/api/pricing` | ⚠️ intermittent | Sometimes works, sometimes blocks. Try once, don't retry. |
| Logged-in dashboards | ❌ always | Aura has no session; use screenshot upload if essential. |
| Medium / blog posts | ✅ works | Fine for typography + article references. |

---

## Phase 3 — Export to Figma (optional, for design review)

### New clipboard method (Chrome only):
1. Click **Export to Figma** in aura
2. Code auto-copies to clipboard
3. Open Figma document
4. Press `Cmd+V` / `Ctrl+V` directly — design appears with organized layers

No console commands needed with the new method.

Skip this phase if going straight to implementation.

---

## Phase 4 — Adapt to React/Next.js in Claude Code

### 4a. Copy the full HTML from aura Code view

### 4b. Analyze the structure before converting

Read the HTML carefully. Identify:
- State that needs `useState` (menu open/close, tab active, scroll)
- Repeated elements that need `.map()` over data arrays
- Inline styles that should become design-token / shared CSS classes
- Hard-coded text that should be props

### 4c. Conversion rules

| HTML pattern | React equivalent |
|---|---|
| `onclick="toggleMenu()"` | `const [open, setOpen] = useState(false)` |
| `class="..."` | `className="..."` |
| Inline `style="color:..."` | Prefer existing token/class; else keep inline briefly |
| `<a href="/pricing">` | Framework `Link` when routing is client-side |
| Hardcoded text | Move to props or i18n key |
| `<script>` event listeners | `useEffect` + `addEventListener` |
| Vanilla JS animations | Prefer CSS transitions/keyframes in shared styles |

### 4d. Placement decisions

Put marketing sections with other landing surfaces, dashboard pieces under the
feature area that owns them, and shared primitives in the design-system / UI kit
folder — follow the target app’s existing layout conventions.

### 4e. Extend the design-token / shared stylesheet

If the component introduces new CSS patterns, add them to the product’s shared
token/stylesheet with the project’s naming convention. Keep `@keyframes` at
module or global scope consistently with the rest of the codebase.

### 4f. Run quality gates before committing

Run the target app’s typecheck and lint on modified files (zero errors required).

Fix all errors. Commit with descriptive message referencing the inspiration source.

---

## Brand Context Quick Reference

Always available for aura prompts:

```
gotcontext.ai — AI-powered semantic compression SaaS
Tagline: "Compress everything your AI reads"
Audience: Developers, AI engineers, teams using LLMs

Colors:
  --bg-base: #030304
  --bg-alt: #08080a
  --accent-cyan: #33d2ff
  --accent-blue: #4a8cff
  --text-main: #f4f4f6
  --text-dim: #888894
  --border-light: rgba(255,255,255,0.08)

Typography:
  Display/headings: Outfit, font-weight 400–600
  Body/UI: Inter, font-weight 400–600
  Nav items: 13px, uppercase, letter-spacing 0.06em

Key UI patterns already in codebase:
  - aura-nav-links (spinning border glow CTA)
  - aura-pill-btn (spinning border glow button)
  - aura-header (sticky glassmorphism nav)
  - .gc-docs-* (docs page components)
```

---

## Common Mistakes

| Mistake | Fix |
|---|---|
| Using the paperclip for Chrome-captured screenshots | The paperclip requires a local-file path. Browser-automation screenshots live on the MCP server, not on disk. Use the **chain-link URL import** instead. |
| Retrying the same URL after "Failed to fetch" | Aura caches the result and will fail again. Pick a different reference or switch to Phase 2.5 direct rebuild. |
| Choosing "Exactly" in Import Website | Copies the reference pixel-for-pixel including branding. Always pick **Different** when rebranding. |
| Using Nano Banana model | Switch to Claude Opus or Gemini Pro BEFORE submitting. Gemini 3.1 Pro is usually the default now. |
| Cloning without changing branding | Always include "CHANGE" section in prompt |
| Forgetting `<Link>` for internal routes | Search for `href="/"` patterns after conversion |
| Inline styles that conflict with shared tokens | Prefer existing classes; extend rather than duplicate |
| Missing `overflow-x: hidden` on new sections | Add to section wrapper if content bleeds |
| Spending >15 min on aura when it's stuck | Bail to Phase 2.5. Direct React rebuild is faster than fighting the tool when it's not cooperating. |

---

## Speed Tier — When to Skip Phases

| Goal | Skip | Time |
|---|---|---|
| Quick component prototype | Skip Phase 3 (Figma) | ~15 min |
| Design review needed | All phases | ~30 min |
| Exact pixel match required | All phases + Figma inspection | ~45 min |
| Tiny UI fix (button style, color) | Skip Phase 1 (use aura create directly) | ~5 min |
| Reference site is known-blocked (see table above) | Skip Phase 2, go to Phase 2.5 direct rebuild | ~10–15 min |
| Data-dense analytics page (tables, charts, sections) | Often faster via Phase 2.5 — aura struggles with non-marketing layouts | ~10–15 min |

## Aura's own best-practices guide (aura.build/skills) — prompting + HTML/SEO export

Aura publishes a first-party usage guide at **`https://www.aura.build/skills/2fe2aabf-9602-4ef3-9402-6442e9a3ee63/aura-ai-website-builder`** (TOC: Introduction · How to Prompt · SEO Settings · Sell Templates · HTML Designs · Screen Recording). Consult it when you drive aura's **generative** builder (prompt → landing page) rather than a URL/screenshot clone. Two takeaways that affect OUR export→adapt pipeline:

- **HTML export is SEO-bare off aura's own domain.** Aura injects a static-SEO
  block tagged `data-static-seo="true"`, but an inline script strips those nodes
  on subdomains/custom domains. Never assume exported `<head>` carries usable
  SEO — author metadata in the target app.
- **Prompting aura's builder:** aura is strong on marketing/landing layouts and
  weaker on data-dense app UIs (prefer a direct rebuild there). Prompt with a
  concrete section list + tone. Treat output as a **layout reference**; adapt to
  the product’s design tokens and real data (never ship placeholder copy/numbers).
