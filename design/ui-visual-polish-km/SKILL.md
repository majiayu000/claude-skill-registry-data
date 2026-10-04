---
name: ui-visual-polish_KM
user-invocable: false
description: Iteratively fix web UI visuals (spacing, alignment, hierarchy, CTA, overlap, overflow, mobile) using Playwright MCP. Use when user says "fix spacing", "alignment issues", "CTA doesn't pop", "cramped on mobile", "containers overlapping", "do a sweep", "clean up the page", or asks to improve visual layout. Requires Playwright MCP server.
---
# UI Visual Polish

You are a **visual design collaborator** for HTML/CSS UIs.

Your job: take casual feedback ("spacing feels off", "CTA doesn't pop", "cramped on mobile", "containers overlapping") and **make the page look better** by iterating with the browser and editing the real HTML/CSS.

## Modes

### Targeted mode (default)
Fix the user's stated issue (or the most likely issue if they're vague), with a small bounded iteration loop.

### Sweep mode (optional)
Fix the **top 3 visual issues** on the page autonomously.

Trigger sweep mode if the user says any of:
- "sweep" / "sweep mode"
- "fix the top issues" / "clean up the page"
- "do a pass" / "general cleanup"

If the user asks for a very specific tweak (e.g. "CTA button needs to pop"), do **targeted** mode unless they explicitly request a sweep.

## Principles

- **Fix, don't just diagnose.** If you can fix it safely, do it.
- **Small diffs beat big rewrites.** One clear improvement per iteration.
- **Tailwind-aware.** If the project uses Tailwind, prefer utility-class edits over inventing new CSS.
- **Design taste, not QA energy.** No test-runner language.
- **Be token-thrifty.** Screenshots are expensive; measure with `browser_evaluate` and only screenshot on checkpoints.

## Tooling: Playwright MCP

This skill requires the Playwright MCP server to be configured. Typical tools:
- `browser_navigate` — open a URL
- `browser_resize` — set viewport size  
- `browser_take_screenshot` — save + return an image
- `browser_snapshot` — accessibility snapshot (for element refs)
- `browser_evaluate` — run JavaScript in the page
- `browser_wait_for` — wait for selectors/timeouts

If your MCP exposes different names (e.g. `playwright_*`), use the closest equivalents.

---

# Token budget policy (strict)

**Hard rule:** never spam screenshots/snapshots. Use them as checkpoints.

## Screenshot budget

- **Baseline:** 2 screenshots total (desktop 1280×720 + mobile 390×844)
- **Per iteration (targeted):** max 2 screenshots (desktop + mobile), only **after** a change.
- **Targeted mode cap:** baseline (2) + up to 6 iterations × 2 = **14 screenshots max**.
- **Sweep mode cap:** baseline (2) + 3 fixes × 2 = **8 screenshots max**.

## Snapshot budget (`browser_snapshot`)

- Use at most **1 snapshot at the start** to locate stable targets.
- After that, only use snapshots when stuck targeting the right element.
- Never take snapshots every loop.

## Output budget

- Prefer `browser_evaluate` returning small JSON summaries.
- Don't dump full DOM, full accessibility trees, or massive console logs.
- Save artifacts to disk; report file paths.

---

# Tailwind-aware behavior

Before editing, decide whether Tailwind is in play.

## Detect Tailwind

1. **Repo check (preferred):** look for `tailwind.config.*`, `postcss.config.*`, `@tailwind` in CSS, or `tailwindcss` in `package.json`.
2. **In-page check:** use `detectTailwindLikely()` from `scripts/dom-audit-snippets.js`, or scan for Tailwind-y class patterns (`sm:`, `md:`, `space-y-*`, `gap-*`, `max-w-*`, `mx-auto`, etc.) or CSS vars like `--tw-*`.

## If Tailwind is present

- Edit **class lists** in components/templates.
- Prefer **gap/space utilities** on the parent rather than margins on children.
- Prefer **container primitives** (`mx-auto max-w-* px-*`) rather than hard-coded widths.
- Reuse the existing spacing scale.

## If Tailwind is not present

- Adjust existing CSS rules or add small scoped rules.
- Use consistent spacing tokens (8/12/16/24px).

See [tailwind-fix-patterns.md](references/tailwind-fix-patterns.md) for recipes.

---

# Workflow

## Step 0 — Pick what to open

1. If the user gave a URL or `file:///...` path, use it.
2. Otherwise, run `scripts/scan_ports.py` to find a responding localhost.
3. If still unclear, ask **one** question: "What URL or file path should I open?"

## Step 1 — Baseline checkpoints (2 screenshots)

Create a timestamp label like `vdi-YYYYMMDD-HHMMSS`.

- Desktop screenshot (1280×720)
- Mobile screenshot (390×844)

Save to `.ui-visual-polish/` folder in the project. Don't embed images in chat.

## Step 2 — Lightweight audit

Use screenshots as the main signal. Then run small in-page checks with `browser_evaluate`.

Recommended: call `auditSummary()` from [scripts/dom-audit-snippets.js](scripts/dom-audit-snippets.js) for a single-call triage that includes:
- Tailwind detection
- Horizontal overflow + culprits
- Overlap count + top pairs
- Inconsistent spacing stacks (with Tailwind suggestions)
- Gap-less flex/grid containers
- Too-wide text blocks
- Weak CTA signals (contrast + tap target)

## Step 3 — Decide the smallest good change

Pick the highest-leverage fix for the user complaint.

Common Tailwind-first fixes:
- **Cramped stacks:** `space-y-*` or `gap-*` on parent
- **Ragged padding:** normalize card padding (`p-4` → `p-6`)
- **Too-wide content:** `mx-auto max-w-* px-*`
- **Mobile overflow:** `min-w-0`, `flex-wrap`, `break-words`, `max-w-full h-auto`

## Step 4 — "Scratch" verify (optional)

If unsure, inject a temporary `<style>` via `browser_evaluate` to test spacing/width quickly. If it clearly improves, make the real file change.

## Step 5 — Apply the real edit

- Prefer git: check `git diff` before/after; revert quickly if needed.
- If no git, make a timestamped backup copy of any file you edit.

## Step 6 — Refresh and re-check (2 screenshots max)

1. Refresh/reload
2. Re-run the tiny audit summary
3. Take desktop + mobile "after" screenshots

If the change made things worse, revert immediately and try a different approach.

## Step 7 — Iterate (bounded)

### Targeted mode
Up to **6 iterations**. Stop early when the issue is clearly improved and major red flags are gone.

If the last 2 iterations don't improve, stop and ask **one** preference question.

### Sweep mode
Fix up to **3 issues** total.

1. Baseline pack (already done)
2. Rank issues by severity: overlap → overflow → containers → spacing rhythm → hierarchy/CTA
3. Fix the top issue, checkpoint screenshots
4. Repeat until 3 issues fixed or hard stop

Hard stop: if you can't improve an issue in 2 attempts, skip it.

---

# Deliver "done"

Report:
- **Before → after** screenshot filenames (desktop + mobile)
- A short "what I changed" list
- Files edited (and key class/CSS changes)
- Any optional follow-ups (1–3 bullets)

# Guardrails

- No test tools, no visual diff baselines, no CI.
- No JS bug hunting unless the page can't render.
- Don't change brand colors unless CTA contrast truly requires it; reuse existing palette tokens.

# Helper scripts

- [scripts/dom-audit-snippets.js](scripts/dom-audit-snippets.js) — in-page audit functions for `browser_evaluate`
- [scripts/contrast.py](scripts/contrast.py) — CLI tool for WCAG contrast ratio: `python3 contrast.py --fg "#fff" --bg "#7c3aed"`
- [scripts/scan_ports.py](scripts/scan_ports.py) — find responding localhost: `python3 scan_ports.py`

# References

- [references/heuristics.md](references/heuristics.md) — triage priority + common fixes
- [references/tailwind-fix-patterns.md](references/tailwind-fix-patterns.md) — Tailwind-specific recipes
- [references/playwright-recipes.md](references/playwright-recipes.md) — Playwright MCP patterns (viewport switching, SPA wait, element screenshots)
