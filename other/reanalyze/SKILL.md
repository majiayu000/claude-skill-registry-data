---
name: reanalyze
description: |
  Re-run the analysis pipeline on all runs matching an RQ, reaggregate
  metrics, and propose findings updates against the fresh data.
  Trigger when the user says "reanalyze RQ-N", "reanalyse RQ-N",
  "Runs neu analysieren", or wants to refresh metrics/findings after
  a pipeline change (analyze-run.sh fix, adapter added, ESLint config).
---

# Skill: reanalyze

Re-run `analyze-run.sh` on every run matching an RQ selector, reaggregate via `aggregate-by-query.py`, and propose findings updates. **No new runs are started** — this skill only refreshes existing data.

Typical use cases:
- Pipeline fix (analyze-run.sh changed, verification adapter added)
- Manual run cleanup (crash runs deleted, runs re-added)
- ESLint/SonarJS config change affecting smell metrics
- New fields added to metrics.json

## Argument

- `RQ-N` (e.g. `RQ-prompt-known-kata`) or a direct path to an RQ dir.
- If not given: ask back ("Which RQ? e.g. RQ-prompt-known-kata").
- RQ dirs live in four subtrees: `research/questions-claude/<chapter>-*/`, `research/questions-opencode/<chapter>-*/`, `research/questions-cross/<chapter>-*/`, and `research/workflow-dev/<chapter>-*/`. The chapter prefix is an ordering label; the stable id is the frontmatter `id:` (a slug like `RQ-prompt-known-kata`). Resolve it to a path by exact-line id-grep across all subtrees:
  ```bash
  RQ_DIR=$(grep -rlE "^id:[[:space:]]*RQ-prompt-known-kata[[:space:]]*$" \
             research/questions-claude/*/README.md \
             research/questions-opencode/*/README.md \
             research/questions-cross/*/README.md \
             research/workflow-dev/*/README.md \
           2>/dev/null | head -1 | xargs -r dirname)
  ```

## Phases

Run sequentially. On errors in any phase, **stop and ask the user**, do not skip ahead.

---

### Phase 1 — Resolve & Match

1. Resolve the RQ path into `$RQ_DIR` via the id-grep in "Argument" above. On no match, ask the user; on multiple, take the first and inform.
2. Read `$RQ_DIR/README.md` — parse frontmatter for `controls` and `factors` (needed to build the selector).
3. Find all matching runs in `experiments/runs/`:
   ```bash
   for d in experiments/runs/*/; do
       jq -e 'select(
           .kata == "<expected>" and
           .workflow == "<expected>" and
           (.model | test("<model-pattern>"))
       )' "$d/metrics.json" > /dev/null 2>&1 && echo "$d"
   done
   ```
   The selector logic mirrors `aggregate-by-query.py`: `kata = kata_base + "-" + prompt` for each prompt value (from factors or controls), model from factors or controls, workflow from controls. Match against `.kata`, `.workflow`, `.model` in each run's `metrics.json`.
4. Report: "Found N runs matching RQ-X selector."
5. If N == 0: STOP — "No matching runs found. Check that experiments/runs/ contains runs with the expected kata/workflow/model."

---

### Phase 2 — Reanalyse

1. Get user confirmation: "Reanalyze N runs? This re-runs analyze-run.sh on each (ESLint, verification, metrics extraction). Estimated time: ~N × 10s."
2. After "yes": iterate over all matched run dirs:
   ```bash
   count=0; total=N
   for d in <matched_dirs>; do
       count=$((count+1))
       echo "[${count}/${total}] $(basename $d)"
       ./experiments/analyze-run.sh "$d" > /dev/null 2>&1
   done
   ```
3. Report: "Reanalyzed N runs."

---

### Phase 3 — Reaggregate

1. Run:
   ```bash
   ./experiments/aggregate-by-query.py "$RQ_DIR"
   ```
2. Read the generated `summary.md`.
3. Show the cell coverage table to the user.
4. Show the primary outcome pivot table (typically `verification_pct` or the first outcome in the frontmatter).

---

### Phase 4 — Findings update (write-first)

**Write directly to `findings.md`, then notify the user to review.** Markdown tables and trophy assignments are much easier to evaluate as rendered output than as a chat proposal; reverting is cheap (it's only markdown). After writing, send one line (in the user's language), e.g. "written — please review", with a brief list of what changed (STALE / STATUS / NEW).

Exception: **deletions** of existing findings still require explicit user confirmation before the `edit` — losing a documented finding is more expensive than re-reading a fresh write.

`findings.md` shows **only the current state**. No legacy comparisons, no "previously X" references, no "revised"/"confirmed" tags. Header form: `## F-x.y — Title` (no trailing suffix). The namespace before the last dot may carry dots itself (`F-4.4.1`, `F-1.12.5` are valid). Keep the em-dash `—`: the snapshot generator parses on it and drops non-matching headers silently.

**Trophy convention (🏆) in overview tables**: When refreshing the `## Overview` table at the top of `findings.md`, append 🏆 to the best value per outcome row alongside the bolded winner. Metric direction matters — note it in the column header or row label (`smell_total`, complexity metrics → "lower = better"; `refactorings_applied`, `predictions_correct_rate` → "higher = better"). Award 🏆 only where the spread is meaningful — if all values lie within 1 σ and the framing is "no effect", either award 🏆 to all tied or to none, don't fabricate winners from rounding noise. Trophies are for findings docs only; workflow files stay emoji-free.

1. Read current `findings.md` and fresh `summary.md`.
2. For each existing finding (`## F-x.y`):
   - Extract the numbers referenced in the finding (mean, σ, n, rates, spreads).
   - Look up the corresponding cell(s) in the fresh `summary.md` pivot tables.
   - Classify:
     - **OK** — numbers match (within rounding tolerance of 0.01).
     - **STALE** — numbers have changed. Show: `F-x.y: <metric> was <old>, now <new>`.
     - **STATUS CHANGE** — the status tag should change based on new data (e.g. n grew from 3 to 5 → "⚠️ bedingt" can become "✅ stabil"; or a previously stable pattern broke).
3. Check for **NEW patterns** not yet captured in findings:
   - Scan the pivot tables for cells with notable deviations (σ > 0.3, mean < 0.5 on verification_pct, or cross-cell spreads > 20 pp).
   - If a pattern is new and not covered by any existing finding, propose a new `F-x.y` block.
4. Apply the changes directly:
   - **STALE**: replace the affected numbers in the existing finding block via `edit`. Rewrite the Datenbasis table and any prose that references the changed numbers. Do NOT add "previously X" or "corrected from" — just write the current state.
   - **STATUS CHANGE**: update the status tag inline.
   - **NEW**: append at end of findings.md, after the last `---` separator.
   - **Update the overview table** at the top of findings.md to reflect any changed numbers.
   - **Deletion** (data contradicts a finding): ask the user first, then remove the block including its `---` separator on confirmation.
5. After writing, send one short line summarizing what changed:
   ```
   written — STALE: F-x.y, F-a.b · NEW: F-x.z · OK: F-c.d, F-e.f. Please review.
   ```

**Discipline-metric comparability**: if the RQ declares `tdd_discipline` or any of its Skip-fed siblings (`tdd_discipline_test_first`, `tdd_discipline_closure`, `test_first_rate`, `skip_events`, `cycles_total`, `chain_deviations`), check whether its cells span the test-list boundary — `aggregate-by-query.py` warns and names both groups. Those columns then measure the architecture rather than the discipline, so they are reported within a group and never carry a trophy across one. Full argument: README "Comparability: the test-list boundary".

**Glossary discipline**: use terms from the README glossary ("Code Mass (APP)", "Production LoC", "Correctness (external)", etc.) or metric IDs in backticks. Synonyms like "Code-Volumen" or "LoC-Größe" are forbidden.

---

## Abgrenzung zu /run-rq

| Aspect | `/run-rq` | `/reanalyze` |
|---|---|---|
| Starts new runs | Yes (Docker batch) | No |
| Calls analyze-run.sh | Only on new runs (inside container) | On ALL matching runs |
| Aggregates | Yes | Yes |
| Proposes findings | Yes (Phase 6) | Yes (Phase 4) |
| Use case | Fill missing replicates | Refresh metrics after pipeline fix |

## Out of scope

- Starting new experiment runs (use `/run-rq` for that).
- Cross-RQ aggregation or overview snapshots (use `/build-overview`).
- Editing prompts, workflows, or verification suites.
- Auto-commit/push — stays a user decision.

## Behavior on errors

- **Phase 1 no matches**: suggest checking the frontmatter selector against actual run metadata.
- **Phase 2 analyze-run.sh fails on a run**: report the specific run dir and error, continue with remaining runs (do not abort the whole batch).
- **Phase 3 aggregate fails**: show output, do not proceed to Phase 4.
