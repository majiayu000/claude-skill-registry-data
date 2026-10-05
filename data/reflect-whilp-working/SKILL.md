---
name: reflect
description: Analyze workflow runs and produce a daily reflection.
---

# Reflect

You are running one phase of the reflect pipeline. The phase is specified after `---` below as `PHASE=<fetch|analyze-run|summarize>`.

---

## Phase: fetch

Download workflow run logs and artifacts for a date range.

### Environment

- `SINCE` — start date (YYYY-MM-DD).
- `UNTIL` — end date inclusive (YYYY-MM-DD).
- `OUTPUT_DIR` — directory to write fetched data into.
- `WORKFLOW` — workflow name to filter by (optional).

### Instructions

1. Run `get_workflow_runs` with:
   - `repo` set to `whilp/working`
   - `since` set to SINCE
   - `until_` set to UNTIL
   - `output_dir` set to OUTPUT_DIR
   - `workflow` set to WORKFLOW (if provided)
2. The tool downloads logs and artifacts for each run into OUTPUT_DIR.
3. Verify the manifest file exists at `OUTPUT_DIR/manifest.json`.
4. Write `OUTPUT_DIR/fetch-done` containing the number of runs fetched.

### Output

- `OUTPUT_DIR/manifest.json` — JSON array of run metadata with log/artifact paths.
- `OUTPUT_DIR/<run-id>/log.txt` — full log for each run.
- `OUTPUT_DIR/<run-id>/artifacts/` — downloaded artifacts for each run.
- `OUTPUT_DIR/fetch-done` — completion marker.

---

## Phase: analyze-run

Analyze a single workflow run. You are sandboxed with no network access.

### Environment

- `RUN_DIR` — directory containing this run's log and artifacts.
- `RUN_META` — JSON string with run metadata (from manifest).
- `OUTPUT_FILE` — path to write the analysis.

### Instructions

1. Parse RUN_META to get run metadata (workflowName, conclusion, displayTitle, etc.).
2. Analyze `RUN_DIR/log.txt` efficiently — **do not read the full log**. Logs are large (~100KB). Use targeted commands:
   - `grep -n "==>" RUN_DIR/log.txt` — phase transitions and timing
   - `grep -n "done in\|verdict\|failed\|error\|exit" RUN_DIR/log.txt` — outcomes and errors
   - `grep -n "no_issues\|pr_limit\|issue.json" RUN_DIR/log.txt` — pick results
   - `head -30 RUN_DIR/log.txt` and `tail -30 RUN_DIR/log.txt` — run boundaries
   - Use `read` with `offset` and `limit` to inspect specific line ranges when needed.
3. Check `RUN_DIR/artifacts/` for structured data (these are small, safe to read fully):
   - `*/pick/issue.json` — which issue was picked
   - `*/pick/reasoning.md` — why it was picked
   - `*/plan/plan.md` — what was planned
   - `*/do/do.md` — what was done
   - `*/check/actions.json` — verdict and actions
   - `*/do/feedback.md` — if needs-fixes, what feedback
   - `*/act.json` — final outcome
   - `**/session*.db` — session databases (note their presence/size)
4. Write a concise analysis to OUTPUT_FILE.

### Output

Write OUTPUT_FILE in this format:

```markdown
## <workflowName>: <displayTitle> (<conclusion>)

- **run**: <databaseId> | **event**: <event> | **branch**: <headBranch>
- **started**: <startedAt> | **conclusion**: <conclusion>

### Summary

1-3 sentence summary of what happened in this run.

### Issue

If a work run: issue number, title, verdict, PR link (if any).

### Failures

If failed: root cause, relevant log lines (keep brief).

### Notes

Anything notable: retries, feedback loops, unusual patterns.
```

Keep it concise — under 80 lines. Focus on what matters for the daily summary.

---

## Phase: summarize

Combine per-run analyses into a final reflection. You are sandboxed with no network access.

### Environment

- `ANALYSIS_DIR` — directory containing per-run analysis files.
- `DATE` — date string (YYYY-MM-DD).
- `OUTPUT_FILE` — path to write the reflection.

### Instructions

1. Read all `*.md` files in ANALYSIS_DIR.
2. Synthesize across all runs:
   - **success rate**: how many runs passed vs failed vs cancelled, by workflow.
   - **failure patterns**: common failure modes grouped by root cause.
   - **work loop outcomes**: issues attempted, verdicts, PRs created.
   - **patterns**: trends, flakiness, duration observations.
   - **recommendations**: concrete, actionable improvements — each specific enough to become an issue.
3. Write OUTPUT_FILE.

### Output

Write OUTPUT_FILE in this format:

```markdown
# Reflection: YYYY-MM-DD

## Summary

Brief overview of the day.

## Runs

| workflow | total | pass | fail | cancel |
|---|---|---|---|---|

## Failure Analysis

Group failures by root cause. Include brief log excerpts where helpful.

## Work Loop Outcomes

Issues attempted, verdicts, PRs created.

## Patterns

Trends, flakiness, duration.

## Recommendations

Concrete improvements. Each should be specific enough to become an issue.
```
