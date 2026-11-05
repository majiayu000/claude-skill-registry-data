---
name: workloop-audit
description: Read-only health check of Workloop runs. Counts what each run's records show about its reviews, rework and delivery, and flags what the workflow's rules expect but the records contradict. Use at a run's retro, or when the user asks to check how the workflow is doing across runs.
---

# Workloop audit

Workloop's rules are partly enforced by its script and partly followed by agents. This skill reads the records a run leaves — `state.json`, `events.jsonl`, reviews, messages, reports and Git — and reports facts, so whether a rule held is checked rather than remembered. It never writes to a run, a repository or the requirement ledger, and the workflow runs the same without it.

`AUDIT` below means `node <this skill's directory>/scripts/audit.mjs`. It needs the `paseo-workloop` skill beside it, whose parsers it uses to read reports exactly as the gates do. Runs live under `$WORKLOOP_ROOT` (default `~/.workloop`).

## One run: at retro

The [retro](../retro/SKILL.md) skill starts a run's assessment with `AUDIT run <project>/<feature>`. It prints:

- **Counts:** tickets, reviews, rework rounds, rounds past the cap, final review rounds, waivers by kind, failed and conflicting integrations, retries, takeovers, how long the integration checks took, and the ledger's sync state when the project keeps a ledger.
- **Every blocking finding of every re-review, by where it lands:**
  - `carried` — the previous review blocked on the same ID: the fix fell short.
  - `in-change` — it names a line the change since the previous review touched: the fix broke something nearby, which the re-review method allows.
  - `late` — it names tracked code the change left alone. A re-review may block there only on a failing command; otherwise it went beyond its method.
  - `outside-repo` — it names only files outside the repository, such as run-directory evidence, so where it lands cannot be checked.
  - `unplaced` / `unverifiable` — its location names no file, or a commit is gone.
  - `out` — outside the review boundary: a suggestion, which gates nothing.
- **Flags.** A `check` flag is a contradiction to explain: a `late` finding, a rework report without its `## Findings` section, a retro skipped despite signals, a ledger that missed a `sync`, a run directory still over 200 MB after archive, or a `scratch/` that archive did not delete. An `info` flag is context: a finding blocked again, a new finding where the previous round already blocked, rounds past the cap, an override, the orchestrator reworking a candidate itself.

Answer each `check` flag in the retro with its cause or why it was expected. A flag is a question, not a verdict: open the report it names before concluding.

## Across runs: when the user asks

When the user asks how the workflow is doing, run the check in a session that did not orchestrate the runs it judges — a separate agent, so no orchestrator grades its own work.

1. `AUDIT all` for the counts across runs, the change since the last saved check, and every `check` flag. Add `--project <name>` to narrow it.
2. **Verify before concluding.** Read the reports behind each `check` flag and a sample of each category. A `late` finding may be a failing command the method allows. A `carried` finding from a review written before IDs were unique may be a different finding under a reused ID: compare the two rows. Say how many you checked and how many held.
3. Write the result for the user: what the counts show against the last check and against `$WORKLOOP_ROOT/.workloop-audit/baseline.md` if it exists, which rules held and which did not, and suggested changes with their evidence. Suggestions are the user's to decide; change nothing.
4. When the user accepts the result, `AUDIT all --save` keeps it as the point the next check compares against.

`AUDIT run` prints a reminder once three or more runs have finished since the last saved check. Retro passes it to the user; it is a suggestion, not a schedule.

## Limits

- Where a finding lands is read from its `Location` cell. A vague location is `unplaced`, and a finding about run-directory evidence is `outside-repo`; neither is guessed.
- IDs identify a finding across rounds only in reviews whose brief asked for unique IDs. Older `carried` counts include reused IDs, and the output says how many.
- A rework report's `## Findings` section shows the method was reported, not how well it was followed. Judge that from the report and the next review.
