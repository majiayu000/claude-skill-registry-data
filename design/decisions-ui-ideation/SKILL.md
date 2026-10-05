---
name: decisions-ui-ideation
description: Run before implementing UI — research real product patterns (Refero/Mobbin MCP), pick a design direction, and output tokens or a short DESIGN.md before writing code.
---

# Decisions UI Ideation

**I am running research and direction-setting so the user gets designed UI, not generic AI layout.**

Do this before the first line of UI code unless the ticket already includes an approved design spec.

## 1. Clarify the job (30 seconds)

- What screen or flow? Who uses it daily vs once?
- What must be scannable first (status, CTA, content)?
- Existing design system in the repo — reuse tokens/components?

## 2. Gather references (pick what you have access to)

| Source | How |
|--------|-----|
| **Refero MCP** | Search screens/flows; pull DESIGN.md tokens (color, type, spacing). Pro plan. |
| **Mobbin MCP** | Pattern search for mobile/web; OAuth once. Pro plan. |
| **Aceternity UI** | Open `https://ui.aceternity.com` component page; copy or adapt the shown React/Tailwind/Motion code. |
| **Godly** | Browse `https://godly.website`; attach 1–3 screenshot links the user (or you) picked as mood references. |
| **Repo** | Read existing pages/components — match patterns before importing new visual systems. |

If MCPs are not configured, say so once, then use Aceternity URLs + Godly screenshots + repo patterns. Do not block on paid tools.

Optional: install Refero’s agent methodology: `npx skills add https://github.com/referodesign/refero_skill`

## 3. Commit a direction (write it down)

Produce a short artifact (comment in ticket, `DESIGN.md` snippet, or result packet section):

- **Tone** (one phrase): e.g. dense ops tool, editorial landing, playful consumer.
- **Layout idea**: hierarchy, grid, one memorable detail.
- **Tokens**: font pairing, 3–5 colors as CSS variables, spacing rhythm.
- **Motion**: none / subtle / one hero moment (match Aceternity only if motion fits).

Pair with `frontend-design` or `frontend-design-direction` for implementation rules.

## 4. Then implement

- Ponytail: minimal diff, reuse project components.
- Fallow on JS/TS: audit before ship.
- `browser-qa` / `decisions-playwright` after build.

## MCP setup

See `~/.decisions/harness/mcp-recommendations.json` and run `~/.decisions/harness/mcp-setup-design.sh` once for Mobbin/Refero CLI hints.
