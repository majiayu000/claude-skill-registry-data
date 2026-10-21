---
name: seo-reposition
description: >
  Reposition a LIVE site whose category/keyword phrasing is not ranking or is
  being mis-filed by Google/LLMs into unrelated concepts (GSC shows brand-only
  demand; category pages pull ~0 non-brand impressions). Method proven on two
  sites: SERP trap-test every candidate phrase → find the winnable wedge →
  rewording plan with a target-vs-copy rule → GUARD TESTS FIRST (red→green
  ratchet) → phased gated implementation → ship → schedule a
  predicted-vs-actual grading run. Review at the plan and PR gates is the
  owner's choice (the phase gates state the options). Trigger phrases:
  "reposition the site's SEO", "our keywords collide with X", "we're not
  ranking for our category", "Google files us under the wrong thing",
  "trap-phrase audit", "rewording plan", "find our SEO wedge".
---

# SEO reposition — escape the wrong category, rank in a winnable one

The core failure this fixes: a site's own phrasing collides with an unrelated
established concept, so Google (and LLMs) file it under the wrong thing —
"contacts" → contact lenses, "frequent flyer" → airline miles, "travel
networking app" → meet-strangers apps. No amount of on-page polish fixes a
mis-filed site; the vocabulary itself must move to winnable ground, and guard
tests must keep it there.

Prereqs: `search-console-insights` connected (GSC data + `serp_check.py` with a
Serper key). Inputs to confirm up front: target **market, language, device** —
always pass explicit `gl`/`hl` to the SERP fetch, never rely on the helper's
defaults (a US default is wrong for a DACH-market site and vice versa).

## Phase 1 — Diagnose → `SEO-FINDINGS.md`

- **GSC pull**: brand vs non-brand demand, per-page impressions. The tell:
  brand queries dominate and category pages get ~0 non-brand impressions.
- **SERP trap-test** (the core technique): for each candidate phrase, fetch the
  top-10 (`serp_check.py`, explicit market/lang) and read results by *intent*,
  not keyword overlap. Classify: **✅ wedge** (on-intent, no entrenched
  incumbent) · **🟠 crowded** (right category, owned by incumbents) ·
  **🚫 trap** (resolves to a different concept entirely). Keep the raw SERP
  snapshots with each verdict — graders re-check them later.
  The model assists the read; a human confirms each 🚫/🟠/✅ call.
- ≥2 rounds: replacement candidates are themselves frequently traps.
- Write `SEO-FINDINGS.md` from `references/seo-findings-template.md`.

## Phase 2 — Strategy → rewording plan + `WORDING-GUIDE.md`

- **The target-vs-copy rule** (load-bearing): a phrase can be fine as *body
  copy* but toxic as a *rank target*. Only trap-clean phrases may appear in
  title / H1 / anchor text / slug / schema / llms.txt (the "slots").
- Produce `WORDING-GUIDE.md` (`references/wording-guide-template.md`): the
  blacklist (with what Google returns instead — the *why*), approved vocabulary,
  route decisions (retarget / 301 / rename), canonical product description.
- **Gate (owner's choice — explain, then ask, don't default silently):**
  a repositioning plan can misjudge the wedge and ship confidently wrong, so
  it's a reasonable candidate for extra scrutiny — but it's still website
  content strategy, not application code, so `website-review`'s free
  two-pass audit (or `/code-review` alone) is a legitimate, sufficient
  choice on its own. If the owner wants an external second opinion on top,
  run ONE reviewer, not independent-review's own default of two:
  `independent_review.sh WORDING-GUIDE.md --plan --first-success`. State the
  tradeoff plainly (free+now vs. a few extra minutes / a credit) and let
  them pick — see `website-review`'s "Review depth" section for the full
  reasoning.

## Phase 3 — Guard tests FIRST (red → green ratchet)

Write failing specs from the WORDING-GUIDE before touching copy; they ratchet
green as pages land and stay as regression guards forever:

- **trap-guard** — mechanical scan of built HTML + llms.txt + OG source for
  blacklisted phrases; source of truth = the WORDING-GUIDE blacklist, **filtered
  to `Scope: everywhere` entries only** — `slots-only` phrases are legal in body
  copy and belong to slot-guard, so scanning them here would false-fail valid
  pages. Normalize per surface (visible text, JSON-LD, anchors, llms.txt) — a
  flat regex false-positives on scripts and misses entity/casing variants.
- **slot-guard** — bans copy-legal-but-not-a-target phrases from the slots.
  Needs a per-route slot extractor (parse title/H1/JSON-LD/anchors per built
  page); **templated + hand-finished per site** — a generator can't infer the
  allowed qualifiers.
- **two-label / product-honesty guard** — where the product has two distinct
  mechanics, every matching page must name both (prevents blur-back).
- **Negative-test every guard with fixtures**: a broken sample must make the
  guard fire with its intended message — not by editing live copy. A guard that
  has never fired is a hypothesis.

## Phase 4 — Phased, gated implementation

- Sequence by leverage: site-wide config/footer/schema cascade first (one edit
  clears many pages) → money pages → supporting sweep (related-card anchors
  hide stale phrasing) → new comparison pages.
- Stop after each phase; show the guard burn-down (e.g. trap-guard 143→0).
  Commit per phase. Full QA via `website-qa` where available.
- **Gate (owner's choice, same as Phase 2):** `website-review` / `/code-review`
  by default; `independent_review.sh <diff> --diff --first-success` (one
  reviewer) only if the owner opts in for this PR specifically. Ask, don't
  assume the heavier option.

## Phase 5 — Ship → grade (close the loop)

- Deploy via the repo's own deploy model; submit sitemap / IndexNow; request
  indexing for the top changed pages.
- Fill `SEO-CHANGELOG.md` (`references/seo-changelog-template.md`): one row per
  change — page, old→new target, expected GSC query, outcome (blank). Flip
  `planned → deployed <date>`.
- **Schedule the grading run** (~3–6 weeks out) with a concrete mechanism —
  a scheduled agent task, CI cron, or calendar entry with the exact re-check
  steps. Grading re-pulls GSC + SERP and fills the outcome column. Without this
  the changelog is a write-only log and the method never learns.

## Boundaries

- Delegates, never reimplements: SERP/GSC → `search-console-insights`; QA →
  `website-qa`; review gates → `website-review` by default (the site-wide
  pass; note it still assumes Claude Code — under a Codex host use the
  vendored `double-knuth` generic path instead), with `independent-review`
  as an owner-approved optional single-reviewer escalation, never its own
  two-reviewer default. Owns Phases 1–3, orchestrates 4–5.
- Never promise ranking outcomes — record predictions and grade them.
