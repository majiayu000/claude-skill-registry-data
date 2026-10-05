---
name: claude-design
description: "Use when generating, prototyping, or iterating on UI designs (prototypes, wireframes, slide decks, landing/dashboard mockups) with Anthropic's Claude Design tool at claude.ai/design — particularly when you want a design system applied automatically and a clean handoff into Claude Code for implementation."
---

# Claude Design — UI generation with prompt + design-system + Claude Code handoff

## Overview

Claude Design (claude.ai/design, Anthropic Labs, launched 2026-04-17, powered by Opus 4.8) is a chat-driven visual canvas. You describe what you want in plain English; Claude generates a working design on the right pane; you iterate via chat or by clicking individual elements to leave inline comments. **A major 2026-06-17 overhaul** repositioned it from a flashy demo into a design-system *compliance layer* with a bidirectional Claude Code round-trip + a fix for its token-burning problem. The standout features for engineering teams:

1. **Org-wide design system (import from GitHub repo / local codebase / design files / raw uploads)** — bring one or several design systems in ONCE; Claude builds with your real components, **checks its output against the system, and auto-corrects before you see it**. A new admin role can approve ONE standard system + lock edits (enterprise brand control).
2. **Bidirectional Claude Code round-trip (the 2026-06-17 headline)** — from a Claude Code terminal: **`/design-sync`** imports your local codebase's design system INTO Claude Design (so prototypes start from real components, not approximations); **`/design`** creates/edits/syncs design projects without leaving the terminal. When a design is ready it hands off to Claude Code, which picks up exactly where you left off — no screenshot, no rebuild. *(This Claude Code environment exposes a `DesignSync` tool for this.)*
3. **Multi-output export + connectors** — standalone HTML, PDF, PPTX, .zip, org-scoped share link (view/comment/edit), or push to a connected app: **Adobe, Base44, Canva, Gamma, Lovable, Miro, Replit, Vercel, Wix** (more added over time).

Available on **Pro / Max / Team / Enterprise**. NOT on Free. Usage now **shares your subscription pool with chat / Cowork / Code** (see Pricing). Still beta — treat as exploratory tooling, not a system of record (no audit logs yet).

## When to use

- Generate a prototype / wireframe / high-fidelity mock from a verbal spec before you commit any engineering
- Build a pitch deck, investor slides, or sales one-pager that needs to look on-brand
- Produce dashboard/landing mockups using your real component library — then hand off to Claude Code with full context
- Explore 3-5 visual directions in parallel for a design crit without burning eng time
- Generate marketing assets (emails, banners, social posts) that match brand

## When NOT to use

- **Cloning a specific reference UI screenshot/URL** → use `aura-screenshot-clone` skill (aura.build Pro is the project's asset source-of-truth)
- **Greenfield high-fi UI from natural language via Google Stitch MCP** → use `stitch-mcp-design` (remote MCP + optional google-labs-code/stitch-skills)
- **Translating an existing Figma file into code** → use `figma-design-to-code`
- **Mass image picking for hero/landing imagery** → use `mengto-aura-asset-images`
- **Production component edits in the app repo** → edit the code directly; Claude Design is for the design phase, not codebase surgery
- **Anything that needs an audit trail** (compliance, legal review, regulated industry) — research preview has no audit logs yet
- **Free-plan users** — feature isn't available

## Quick start (fresh session, 5 minutes)

1. Navigate to `https://claude.ai/design` (drive it programmatically via logged-in browser automation when available — `navigate` → prompt → upload reference screenshots → screenshot each state. DevTools-only MCP often has no logged-in session.)
2. **Connect a real design system first.** Prefer **`/design-sync`** from Claude Code (GitHub / design files / local app codebase) so generation starts from real components and tokens; or use org **Set up design system** → upload library / brand assets → **Published** ON.
3. From the homepage, pick a project type:
   - **Prototype** → New prototype / Wireframe / High fidelity
   - **Slide deck**
   - **From template**
   - **Other**
4. Describe what you want. Attach screenshots, images, codebases, existing design files, or website captures as context.
5. Iterate:
   - **Chat (broad changes):** "Make the color scheme darker and more minimal", "Move the metrics row above the chart"
   - **Inline comment (targeted):** click an element on the canvas → "Make this button padding larger", "Change this to a dropdown instead of radio buttons"
6. **Export (upper-right Export button)** when ready: **Handoff to Claude Code** (local or web — the direct-to-repo path, preferred for us), **Send to Vercel** (then pull with `mcp__plugin_vercel_vercel__import-claude-design-from-url`), `.zip` / PDF / PPTX / Canva / standalone HTML, or a share URL. **No native Figma export** — see the Figma-bridge row in `design-to-code-pipeline`.

## Design system setup — the load-bearing step

Skip this and Claude Design produces generic-looking output that doesn't match your brand. Doing it once unlocks every future project.

| Input type | What Claude extracts | Recommended fidelity |
|---|---|---|
| **Codebase (React component library)** | Components, prop shapes, design tokens, layout patterns | **Highest** — use this if available |
| **Slide decks (PPTX) or PDFs** | Color palette, typography, layout patterns | Medium |
| **Screenshots / design files** | Color palette, typography, isolated component visuals | Medium |
| **Individual logos, color palettes, typography files** | Tokens only, no component shape | Lowest |

**Steps (verbatim from the docs):**
1. Click your organization name in the **lower-left corner**.
2. Select or create an organization → complete the onboarding flow.
3. Upload brand materials. Per docs: "If your design system lives in code (for example, a React component library)" you can upload the codebase directly.
4. Claude extracts and organizes color palettes, typography specs, UI components, and layout patterns. Validate with sample test prompts.
5. Toggle **Published** ON. After publishing, every project created from the homepage while in your organization uses your design system.
6. To update later: Organization Settings → click **Open** next to your design system → click **Remix** → edit via chat.

Scope is **organization-wide** — auto-applies for all team members on Team/Enterprise plans.

## Export and handoff matrix

| Export option | Best for |
|---|---|
| **Handoff to Claude Code (local)** | You want to immediately implement in your repo. Opens a Claude Code session with the design context attached. |
| **Handoff to Claude Code (web)** | Implement in a sandbox / shareable session. |
| **Standalone HTML** | Self-contained preview for non-technical stakeholders — AND the source for the Figma bridge (below). |
| **Send to Vercel** | Direct deploy path; pull into a session with the `mcp__plugin_vercel_vercel__import-claude-design-from-url` MCP tool. Also sends to Adobe/Base44/Gamma/Lovable/Miro/Replit/Wix. |
| **Download .zip** | Local asset bundle for manual implementation or offline versioning. |
| **PDF** | Read-only review, contract attachments, archival. |
| **PPTX** | Slide deck for an investor / sales / all-hands. |
| **Send to Canva** | Marketing team continues in their tool of record (fully editable). |
| **Share link** | View / Comment / Edit roles for collaborators inside your org. |

**Figma: no native export.** Confirmed 2026-07-02 (Anthropic docs + 3 sources) — Claude Design cannot export to Figma directly. To get a design INTO Figma: export **standalone HTML** → **html.to.design** (Chrome-extension "Copy to Clipboard" → paste into Figma with Ctrl/Cmd+V, OR the html.to.design Figma-plugin drop-zone), or the **Anima** Figma design-agent. For OUR repo you usually don't need Figma at all — **Handoff to Claude Code** is the direct path; reach for Figma only when a human designer must edit layers.

## Pricing & usage

| Plan | Use case (per Anthropic) |
|---|---|
| **Pro** | Quick explorations, one-off use |
| **Max** | Semi-regular — PMs and engineers producing regular mockups |
| **Team (standard seat)** | Quick explorations, one-off use |
| **Team (premium seat)** | Power users — designers and creatives |
| **Enterprise (legacy standard)** | Semi-regular — PMs and engineers producing occasional mockups |
| **Enterprise (legacy premium)** | Power users — designers and creatives |
| **Free** | Not available |

- **Usage SHARES your subscription pool with chat, Claude Cowork, and Claude Code** (2026-06-17 change — a heavy design session eats the SAME limits as a coding session; budget accordingly). The older "separate weekly allowance" framing is superseded; check the Help Center for current shared-limit details.
- Buy more usage (enable extra usage) if you blow through the shared cap.
- **Enterprise usage-based**: one-time ~20-prompt credit per Claude Design user, **expires July 17**.
- No exact "per-prompt" cost is published — Anthropic tunes the meter during research preview.
- **No audit logs, no usage tracking yet** — Labs release.

## Common mistakes

| Mistake | Fix |
|---|---|
| Skipping the design-system setup → output looks generic | Lower-left org name → set up + Publish before creating projects |
| Uploading just colors/fonts when a React codebase exists | Upload the codebase — extracts components AND tokens, not just tokens |
| Treating exported HTML as production-ready | It's a high-fidelity mockup; use **Handoff to Claude Code** to integrate with your real component library, lint, tests |
| Using Claude Design for a 1:1 reference clone | Use `aura-screenshot-clone` skill instead — that's its job |
| Not toggling **Published** ON | New projects won't pick up your design system; the toggle is the gate |
| Inline comments occasionally disappear before processing | Re-add the comment; document quirk; verify the change actually applied before iterating further |
| Large codebases choke the canvas | Upload only the design-system-relevant subset (components/, tokens/, theme files) — not the full repo |
| Compact view triggers save errors | Switch to default view layout when saving |

## Decision matrix vs other UI tools in this stack

Canonical copy: repo `AGENTS.md` § Design path matrix

| Situation | First reach for |
|---|---|
| Brand-new feature mockup, no existing reference | **claude-design** |
| Pitch deck or slide work for the company | **claude-design** (Slide deck mode) |
| Match a specific reference UI screenshot/URL | `aura-screenshot-clone` |
| Generate/iterate UI in Google Stitch via MCP | `stitch-mcp-design` |
| Convert an existing Figma file → React | `figma-design-to-code` |
| Hero/landing imagery picking | `mengto-aura-asset-images` |
| Direct edit of a live app component | Edit the code directly — no design tool needed |
| Visual review of a live deployed page | `frontend-audit` skill + claude-in-chrome MCP |

## What to verify after handing off to Claude Code

The handoff seeds the next session with design context, but Claude Code still needs to:
1. Map design components → your real component library imports (not the extracted clones)
2. Run `npm run check-types` + project lint before claiming the implementation matches
3. Verify in the browser at 375 / 1024 / 1440 viewports — `frontend-audit` skill or claude-in-chrome MCP
4. Pin a regression test if the design encodes a non-obvious invariant

## Recommended path + design→code landscape

Prefer **`/design-sync`** so prototypes start from the product’s real components and
design tokens. Visuals round-trip; **state logic stays in application code**.

- **aura.build** — HTML/Tailwind/vanilla JS (+ React projects); Figma import/export
  on Pro. Use `aura-screenshot-clone` + `mengto-aura-asset-images`.
- **Figma** — Figma MCP (`https://mcp.figma.com/mcp`) into the IDE; Dev Mode /
  Code Connect for implementation.
- **Google Stitch** — Stitch MCP + pack skills via `stitch-mcp-design`
  (~400 credits/day).

## Sources

- News announcement (launch 2026-04-17): <https://www.anthropic.com/news/claude-design-anthropic-labs>
- **2026-06-17 overhaul (design-system import + `/design-sync` code round-trip + connectors + token-burn fix):** <https://venturebeat.com/technology/anthropic-ships-major-claude-design-overhaul-with-design-system-imports-code-round-trips-and-a-fix-for-its-token-burning-problem>
- Product page (current features): <https://claude.com/product/design>
- Get started: <https://support.claude.com/en/articles/14604416-get-started-with-claude-design>
- Set up design system: <https://support.claude.com/en/articles/14604397-set-up-your-design-system-in-claude-design>
- Subscription, usage, pricing: <https://support.claude.com/en/articles/14667344-claude-design-subscription-usage-and-pricing>
- Tool: <https://claude.ai/design>
