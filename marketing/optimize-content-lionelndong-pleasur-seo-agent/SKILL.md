---
name: optimize-content
description: Optimize the cited draft against Semrush ContentShake AI scores. Calls .claude/skills/optimize-content/scripts/contentshake_optimize.py for SEO + Quality scoring + recommendations, then judgment-rewrites the additions in brand voice. Iterates until both scores ≥ 8 or voice drift triggers a rollback. No Chrome MCP, no TipTap injection — pure API.
allowed-tools: Read, Write, Edit, Bash
---

# Optimize Content Skill (ContentShake AI)

Drives Semrush ContentShake AI via the `contentshake_optimize.py` helper to surface what the cited draft is missing relative to the SERP top-rankers, then applies the recommendations **rewritten in brand voice** — not pasted verbatim. Re-runs `/quality-check` after each iteration to catch any voice drift the optimization caused.

## What's different on Semrush vs the prior Ahrefs Content Helper version

The Ahrefs Content Helper flow drove `app.ahrefs.com/content-helper` through the Claude in Chrome MCP. It depended on:
- A connected browser extension
- A Sonnet sub-agent driving navigation
- TipTap editor injection at `window.__pleasurEditor`
- A localhost CORS server on port 8766
- Windows CRLF base64 splitting
- A 50-doc/month Lite-plan cap tracked in `document-budget.md`

**All of that is gone.** ContentShake AI ships an HTTP API that returns the same signal (SEO score, missing terms, missing topics, competitor topic coverage) without a browser, an editor instance, or a port-8766 server. The skill drops to:

1. Call `contentshake_optimize.py` — Doppler-loaded API key, retry/backoff baked in.
2. Parse the JSON response.
3. Judgment-rewrite the accepted recommendations in brand voice (this is the only step that genuinely needs Opus).
4. Edit the draft. Re-score. Re-quality-check. Repeat until win or rollback.

> **Read [`../keyword-research-pipeline/references/semrush-metric-translation.md`](../keyword-research-pipeline/references/semrush-metric-translation.md)** before applying any threshold. The "Content Helper score → ContentShake SEO + Quality" row is the call-out for this skill: the score moves from `0-100` (one number) to `0-10 SEO + 0-10 Quality` (two numbers). The win target shifts from "≥ 90" to "**SEO ≥ 8 AND Quality ≥ 8**".

## Hard constraints

### Voice-drift safety net (UNCHANGED — the user explicitly called this out)

Voice integrity is the load-bearing constraint. ContentShake recommendations are useless if applying them breaks the brand's voice. After every iteration's local edits, run `/quality-check` and compare against the pre-optimization baseline (saved at iteration 0):

- **Voice drift > 8 pts** → REVERT the latest iteration's edits and stop the loop. Surface: `Voice drift triggered at iteration N. Best score reached without drift: X. Final draft is the iteration N-1 version.`
- **Voice drift 4–8 pts** → continue, but flag the iteration in the report so the editor can review whether a partial revert is warranted.
- **Voice drift < 4 pts** → no action; continue.

This rule is non-negotiable. Score lift means nothing if the article reads like AI-stuffed SEO afterwards.

### API-call budget — `BLOG_AGENT_CONTENTSHAKE_MONTHLY_CAP` (default 100)

The legacy 50-doc/month doc-count budget is replaced with an API-call budget. Each `--action optimize` call is 1 unit; each `--action score` call is also 1 unit (the cheaper endpoint still consumes a slot). Budget tracked in `content-pipeline/optimization/api-budget.md`:

- **At < 80% of cap:** call freely
- **At 80–99% of cap:** warn the user, list the slug + iteration, ask explicit confirmation before each remaining call
- **At 100% of cap:** REFUSE further calls. Save a stub report at `content-pipeline/optimization/{slug}.md` noting the cap was hit; recommend either waiting for monthly reset or raising `BLOG_AGENT_CONTENTSHAKE_MONTHLY_CAP`. Pipeline continues without the optimization step.

Reset is automatic at the start of each calendar month (UTC) — the budget file's `month: YYYY-MM` line decides the rollover.

### Missing API key — fail soft, pipeline continues

If neither `SEMRUSH_API_KEY_BLOG_AGENT` nor `SEMRUSH_API_KEY_CONTENTSHAKE` is set:

1. Write a stub report to `content-pipeline/optimization/{slug}.md`:
   ```markdown
   # optimize-content — skipped

   - Reason: SEMRUSH_API_KEY not set in environment.
   - Action: load via `doppler run -- claude` or export `SEMRUSH_API_KEY_BLOG_AGENT`.
   - Pipeline: continues without ContentShake optimization. Re-run `/optimize-content {slug}` once the key is loaded.
   ```
2. Print the same message to stdout.
3. Exit 0. The blog pipeline must not block on a missing key — same convention `/research` uses for a missing OpenRouter key.

## Input

For slug `{slug}`:
- `content-pipeline/6-drafts-cited/{slug}.md` (preferred — the cited draft)
- `content-pipeline/5-drafts/{slug}.md` (fallback if not cited yet)
- `content-pipeline/1-research/{slug}.md` (for the target keyword and SERP context)
- `brand-config.md` + 2 `examples/voice/*.md` (voice anchors for the rewrite step; read `examples/README.md` first)

The Python script auto-discovers the draft path (cited → uncited preference); the skill only needs to pass `--slug` and `--keyword`.

## Process

### Phase A — preflight

1. **Load the target keyword** from `content-pipeline/1-research/{slug}.md` frontmatter (or fall back to the slug itself with hyphens replaced by spaces).
2. **Read the budget file** at `content-pipeline/optimization/api-budget.md`. If absent, create with `month: YYYY-MM` and `calls: 0`. If month rolled over, reset.
3. **Verify the API key is in env** by inspecting `SEMRUSH_API_KEY_CONTENTSHAKE` then `SEMRUSH_API_KEY_BLOG_AGENT`. If both missing → write stub report, exit 0 (see "Missing API key" above).
4. **Snapshot the baseline draft** to `content-pipeline/optimization/{slug}-iter-0.md` and run `/quality-check {slug}` to capture the pre-optimization quality score. Persist to `content-pipeline/optimization/{slug}-baseline-quality.md`.

### Phase B — initial ContentShake call

5. **Call the script:**
   ```bash
   doppler run -- python .claude/skills/optimize-content/scripts/contentshake_optimize.py \
     --slug {slug} --keyword "{keyword}" --action optimize
   ```
6. **Parse the JSON response** from stdout. Increment the budget file's `calls` counter.
7. **If the script exits 75 (quota):** save what we have to `content-pipeline/optimization/{slug}.md` noting quota exhaustion, exit 0 cleanly. Pipeline continues.
8. **If the script exits non-zero with a different error:** save the stderr to `content-pipeline/optimization/{slug}-errors.log` and exit 0 with a stub report. Don't crash the pipeline on a transient API error.
9. **Save the raw response** to `content-pipeline/optimization/{slug}-raw-iter-1.json`.

### Phase C — iteration loop (max 5)

For each iteration `i` in 1..5:

- Read the latest ContentShake response (`{slug}-raw-iter-{i}.json`).
- **Stopping conditions** (check BEFORE doing more edits):
  - **Win:** `seo_score ≥ 8 AND quality_score ≥ 8` → stop with verdict `WIN`
  - **Voice protection:** quality-check dropped by > 8 pts vs baseline → REVERT iteration `i`'s edits, stop with verdict `ROLLBACK`
  - **Stagnation:** the last two iterations each lifted `seo_score` by < 0.5 pts (or both scores moved < 0.5 pts) → stop with verdict `PLATEAU`
  - **Cap:** `i == 5` → stop with verdict `CAPPED`
- **Otherwise, do the edit pass:**
  - Identify the lowest-scoring topics and the highest-importance recommended terms not yet `in_draft`. Pick **1–3 surgical edits** per iteration (a new paragraph, a term weave, a section expansion).
  - **Read 1 example article** from `examples/` first to anchor voice for this pass. The voice in those files is the source of truth.
  - For each accepted edit:
    - **Skip if** the term is a synonym for content already in the draft (saturated), OR the topic doesn't fit the brand's positioning, OR adding it would distort the article's thesis, OR it includes forbidden phrases from `brand-config.md`.
    - **Add if** it names a concept the article should cover but doesn't AND it can be incorporated without forcing.
    - **Aim** for applying 60–80% of recommendations; rejecting the rest is normal.
    - **Compose 1–3 sentences in brand voice** — NOT ContentShake's suggested phrasing. Use the recommended term once, naturally, where it fits. Do not keyword-stuff.
  - Apply edits via `Edit`. Preserve existing prose, citations, and `[VISUAL:...]` placeholders.
  - Save the post-edit draft as `content-pipeline/optimization/{slug}-iter-{i}.md` (so revert is a file copy, not a diff replay).
  - **Re-call ContentShake** with `--action optimize` (full payload) for iterations 1–3, or `--action score` (lightweight) for iterations 4–5 to conserve budget when nearing the win threshold.
  - Persist the new response to `{slug}-raw-iter-{i+1}.json`. Increment budget.
  - **Run `/quality-check {slug}`** locally. Compare against baseline. Append the result + voice-drift delta to `content-pipeline/optimization/{slug}-iterations.md`.

### Phase D — finalize

After the loop exits (win, rollback, plateau, or capped):

10. **Save the canonical optimized draft** to its original location (`6-drafts-cited/{slug}.md` if that's what was input, else `5-drafts/{slug}.md`).
11. **Write the optimization report** to `content-pipeline/optimization/{slug}.md`:
    - Verdict (WIN / ROLLBACK / PLATEAU / CAPPED)
    - SEO score before / after, Quality score before / after
    - Quality-check (voice) score before / after, drift delta
    - Iterations used; budget consumed; budget remaining
    - Recommendations applied (with reasoning per accepted)
    - Recommendations skipped (with reasoning)
    - If verdict == ROLLBACK: which iteration triggered the revert and what changed
12. **Re-trigger `/quality-check {slug}` once more** so the next pipeline stage sees fresh voice metrics. This call is free (local script).
13. **Print a one-line summary** to stdout, e.g.:
    `optimize-content: SEO 4.2→8.3, Quality 6.1→8.4, voice 78→74 (drift OK), 3 iterations, verdict=WIN, budget 38/100`

## Output

- `content-pipeline/optimization/{slug}.md` — final report (verdict + scores + recommendations applied/skipped + budget)
- `content-pipeline/optimization/{slug}-iterations.md` — per-iteration log with score lifts and voice drift
- `content-pipeline/optimization/{slug}-iter-{i}.md` — post-edit draft snapshot per iteration (for revert + audit)
- `content-pipeline/optimization/{slug}-raw-iter-{i}.json` — raw ContentShake API responses (for audit + future training data)
- `content-pipeline/optimization/{slug}-baseline-quality.md` — pre-optimization voice score
- `content-pipeline/optimization/api-budget.md` — running monthly API-call counter
- Updated `content-pipeline/6-drafts-cited/{slug}.md` (or `5-drafts/{slug}.md`) — the optimized draft
- Refreshed `content-pipeline/quality-checks/{slug}-metrics.md`

## Quality checklist

- [ ] API key present (or stub report written + exit 0)
- [ ] Budget file updated; not over cap
- [ ] Baseline quality-check captured at iteration 0
- [ ] At least 5 recommendations evaluated explicitly (accept or reject + reason)
- [ ] Every accepted addition rewritten in brand voice (NOT pasted from ContentShake response)
- [ ] Each addition uses the recommended term ONCE, not stuffed
- [ ] No forbidden phrases from `brand-config.md` introduced by additions
- [ ] `/quality-check` re-run after EVERY iteration's edits
- [ ] Voice-drift > 8 triggered a rollback (when applicable)
- [ ] Report file lists what was applied + skipped + reasoning
- [ ] One-line summary printed with budget status

## When ContentShake returns a partial response

The `contentshake_optimize.py` script normalizes missing fields to `null` (scores) or empty lists (terms / topics). If `seo_score` is `null` after a successful 200 response:

- Treat as: skip score-based stopping conditions for this iteration, but still apply judgment edits if recommendations are present.
- Note in the report: "ContentShake returned no SEO score for iteration N — treating as no-op for win-detection."
- Still run `/quality-check` so voice drift is monitored.

## When the iteration loop hits the budget cap mid-run

Persist whatever progress was made (last good iteration draft, last raw response). Save the report with verdict `BUDGET_EXHAUSTED`. The next `/optimize-content` run on this slug picks up from the saved iteration draft — no re-baselining needed unless the user passes `--regen`.

## When the score doesn't move across two iterations

This is the `PLATEAU` verdict. Most common cause: the brand-voice rewrites used synonyms or different phrasings rather than ContentShake's suggested terms verbatim. **This is FINE.** SEO scores are heuristics; voice integrity matters more long-term. Note in the report:

> "Score plateaued — additions used voice-appropriate phrasings rather than ContentShake's suggested terms verbatim. This is intentional."

Don't try harder. Plateau is an acceptable terminal state.

## Why we don't apply recommendations blindly

ContentShake recommendations are based on what's already ranking. Following them mechanically produces content that resembles existing top-rankers — middle-of-the-pack SEO. The article won't outperform what's already there because it'll BE what's already there.

The judgment step is what gets you BOTH ranking benefit AND differentiation. The voice rewrite step is what protects against the Helpful Content Update / AI-detection risks. Skip judgment + voice rewrite and you have an SEO-stuffing skill — that's not what this is.

## When `/draft-score` was already run

If `content-pipeline/optimization/{slug}-draft-score.json` exists from a `/draft-score` self-check pass during drafting, read it as a hint about which terms / topics are likely to come up — but still call `--action optimize` for the full recommendation payload at iteration 1. The score-only response from `/draft-score` doesn't include the term/topic lists this skill needs.
