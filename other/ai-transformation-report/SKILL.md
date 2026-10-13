---
name: ai-transformation-report
description: >-
  Generate a Spanish, business-facing HTML report (with real-data charts) showing
  how commits, code volume, features shipped, and quality changed across the
  CIDCA/Nimbus repos since the team started working with AI (2026-04-13). Uses
  REAL git + gh data only — never mocked. Frames it as impact, not as a bill.
  Trigger when the user says "reporte de transformación AI / IA", "cuánto hemos
  producido desde el plan Max", "reporte para negocio del impacto de la IA", or
  invokes /ai-transformation-report.
---

# AI Transformation Report (CIDCA / Nimbus)

Produce a **Spanish**, MVP/startup-toned, business-facing **HTML report** that a
non-technical stakeholder can read to see how working with AI changed the team's
delivery since **2026-04-13**. It must be built on **real data only** — every
number comes from `git`/`gh`. **Never fabricate or estimate a number you can't
pull.** If a value can't be measured, omit it and say so.

**Framing: impact, not an invoice.** Do NOT include plan costs, $/feature math,
"lo pagamos de nuestra bolsa", or any reimbursement ask. The report shows what the
team shipped and how the work changed — nothing about billing.

## Steps

1. **Collect real metrics.** Run the bundled collector (it shells `git log` on the
   local clones + `gh pr list`):
   ```bash
   python3 <skill_dir>/collect_metrics.py --since 2026-04-13 --json <scratch>/ai_metrics.json
   ```
   - `--since` = the AI-era boundary (default 2026-04-13). It auto-computes an
     equal-length **"before"** window for the comparison, and a weekly timeline.
   - Confirm the local clones exist at the paths in the script; if a repo moved,
     update `REPOS` there. If `gh` isn't authed, PR counts come back `null` —
     fall back to `feat`-commit counts for the "features" KPI and note it.

2. **De-dup rule (critical).** `cidca-platform` holds the FULL migrated history of
   `ecg_auto` + `ecg-ui` (consolidated ~2026-05-19; both now archived). The
   collector marks those two as `legacy=True` and **excludes them from all
   totals** — they appear only in a "legacy tapered off vs monorepo ramped up"
   view. Do not add legacy commits to any total.

3. **Design the charts** — load the **`dataviz`** skill first, then **`artifact-design`**.
   Charts are **inline SVG rendered by a tiny vanilla-JS snippet from the embedded
   JSON** (Artifacts run under a strict CSP — no external scripts/CDNs). Embed the
   collector's JSON verbatim in a `<script type="application/json">` so the report
   is self-contained and auditable.

4. **Write the report** — follow `references/report_spec.md` for the exact section
   order, Spanish copy, KPI formulas, and chart list. Theme-aware (light/dark),
   responsive, wide tables/charts scroll inside their own container.

5. **Publish** as a private **Artifact** (`favicon: "📈"`). Title in Spanish, e.g.
   "Transformación con IA — CIDCA". Tell the user it's private until they share it.

## Methodology to state IN the report (transparency = credibility)
- Commits are `--no-merges`. Churn (líneas) **excludes** lockfiles + generated
  artifacts (`*.lock`, `dist/`, `build/`, `*.min.js`, `*.map`) so it reflects real
  code. "Features" = Conventional-Commits `feat` count **and** merged PRs to the
  preprod branch (`dev`). "Antes vs Después" compares two equal-length windows
  around 2026-04-13, measured on the SAME repo set (so it's apples-to-apples —
  the monorepo's pre-consolidation history covers the "before" side).
- Quality proxies: Conventional-Commit adoption %, feat:fix ratio, and the
  commit-type distribution. Never invent a "quality score".

## Guardrails
- **No mocked data, ever.** Real git/gh only. If asked to embellish, refuse and
  keep it honest — this goes in front of stakeholders.
- **No money.** No plan cost, no $/feature, no reimbursement ask.
- Keep it in **Spanish**, concrete, and short enough for a founder/finance reader;
  put the raw table + methodology at the end for auditability.
- Re-run any time with a different `--since` to reframe the window.
