---
name: research
description: Researches questions when they need current sources, explicit uncertainty, adversarial fact-checking, or evidence-backed consensus in a Markdown deliverable.
argument-hint: "[--quick] [research-question]"
---

# Codex-reviewed research

## Overview

The orchestrator performs the requested research, writes the report, and owns every conclusion. The configured Codex reviewer peer-reviews the completed draft in one persistent read-only thread. `codex-invoke.mjs round` runs the loop mechanics (prompts, secret redaction, diffs, finding IDs, ledger, repeat suppression, stall detection, round limit, resumable state). The orchestrator checks sources, decides, and revises.

**Core principle:** No evidence, no blocking finding. Model agreement is not research evidence.

**Shape of a run:** round 1 is the one broad fact-check. Later rounds only confirm the orchestrator's corrections and check the changed text. A later round can raise a new blocker only for an error introduced by the revision or a VERIFIED critical error round 1 missed.

Produce one final Markdown report. Do not implement code, create an implementation plan, or dispatch implementation subagents.

## Input and output

Treat `$ARGUMENTS` as the research question, scope, constraints, optional output path, and an optional `--quick` flag (one review pass: add `--max-rounds 1` to the first `round` call). If empty, use the research request active in the conversation. Ask only when missing scope would materially change the answer.

Choose the Markdown path in this order:

1. An explicit path in the request.
2. The repository's existing research-report convention.
3. `research/YYYY-MM-DD-<topic>.md`.

Keep working notes in context rather than producing sidecar deliverables. The final Markdown file is the source of truth.

## Preflight

This skill runs on the session's current model and effort; it does not switch models.

**In pi:** pi does not substitute `${CLAUDE_PLUGIN_ROOT}`; replace it with the absolute path two directories above this SKILL.md. `$ARGUMENTS` is the text appended after `/skill:NAME`.

```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/codex-invoke.mjs" setup --cwd "$(pwd)"
```

Proceed only when setup reports `Status: ready`. The first round freezes the reviewer model, effort, and round limit for the run.

## Phase 1: The orchestrator researches and drafts

Research the question completely before asking Codex to review it.

### Scope the answer

Record internally:

- The exact question and intended reader.
- Time, geography, version, or jurisdiction constraints.
- What would change the conclusion.
- Which unknowns cannot be resolved with available evidence.

Do not broaden the assignment into adjacent research the user did not request.

### Gather evidence

- Prefer primary sources: official documentation, specifications, first-party data, statutes, filings, source code, and original papers.
- Use secondary sources to orient or corroborate, not to replace an available primary source.
- For current claims, retrieve current sources rather than relying on model memory.
- Record the source URL or repository location, publication or version date when relevant, and the exact passage supporting each material claim.
- Corroborate consequential claims when independent evidence is available.
- Distinguish source facts, the orchestrator's inferences, and unresolved unknowns.
- Do not cite a search-result snippet as evidence.

### Write the first draft

Write one Markdown report with the smallest structure that answers the request. Include:

1. Research question and scope.
2. Executive answer.
3. Findings with inline citations or footnotes.
4. Evidence and reasoning supporting each material conclusion.
5. Counterevidence, tradeoffs, or plausible alternative interpretations.
6. Uncertainties and evidence gaps.
7. Sources.
8. A peer-review record placeholder.

Every material factual claim must be traceable to a source. Label inference as inference. Use `Unknown` when the evidence does not support a conclusion.

## Phase 2: Codex peer review

If `report --artifact REPORT_PATH` shows `AWAITING ADJUDICATION`, resume that run instead of starting a new one. Otherwise write the research request to a temporary file and start:

```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/codex-invoke.mjs" round \
  --cwd "$(pwd)" --kind research --artifact REPORT_PATH \
  --request-file REQUEST_FILE [--new] [--max-rounds 1]
```

Add `--new` only when a finished run for this report exists. Do not put protected content (`*.env*`, `*.secret*`, `*credentials*`, `**/secrets/**`) in the request or report; the runner also redacts credential-shaped values.

The command prints one JSON object with `status`, `next`, `summary`, `blockers`, `notes`, `questions`, `reviewer`, and `runFile`. Show the user only the `summary` line per round. Findings are numbered `R1`, `R2`, ...

| `next` | Action |
|---|---|
| `adjudicate` / `adjudicate-final` | Adjudicate every blocker, revise, continue. After `adjudicate-final`, revisions are unreviewed unless the user approves a closeout. |
| `stalled` | Ask the user: *Keep fixing*, *Waive these risks*, or *Stop here*. Ask the same when a verified blocker cannot be corrected; *Stop here* ends as `BLOCKED — NOT APPROVED`. |
| `cap` | Ask the user: *Run one closeout round* (`--closeout`), *Accept as is*, or *Stop here*. |
| `done` | Finish. |
| `retry` | Nothing was recorded. Rerun the identical command once; stop with the error if it fails again. |

A failed, timed-out, empty, or malformed reviewer turn is an incomplete review, never "no findings."

## Phase 3: The orchestrator adjudicates and revises

For each blocker:

1. Open the cited report passage and source.
2. Confirm the source exists, is current enough for the claim, and says what Codex claims it says.
3. Check that the finding's impact follows from the evidence.
4. Decide `ACCEPT`, `REJECT`, `COUNTER` (verified concern, more accurate correction), or `WAIVE` (only when the user explicitly accepts the risk).
5. Revise the report only for accepted or countered findings, and only as far as the evidence requires.

Blockers with a `priorDecision` are corrections the reviewer says did not land, or a one-time dispute of a rejection. Decide them again on the evidence.

Reject invented, stale, mismatched, or inaccessible citations. If the source identity is sufficient, check one obvious canonical or archived location; otherwise reject and say what evidence would change the decision. Do not perform an unbounded source hunt. Keep notes (minor, INFERENCE, UNVERIFIED) in uncertainties until evidence promotes them; recording a neutral evidence gap is not acceptance.

Continue with the decisions file:

```json
{"decisions":[{"id":"R1","decision":"ACCEPT","reason":"The 2026 release notes contradict the draft's date; corrected section 3."}]}
```

```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/codex-invoke.mjs" round \
  --cwd "$(pwd)" --artifact REPORT_PATH --adjudication-file DECISIONS_FILE
```

If every blocker is rejected or waived, the run converges without another reviewer turn.

Call the result `consensus` only when the reviewer's last verdict was `approve`. Otherwise describe it as `no verified blocking findings after adjudication`; never imply model agreement that did not occur.

If the user cancels, stop and report `CANCELLED — NOT APPROVED`. The run resumes on the next invocation for the same report.

## Final Markdown report

```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/codex-invoke.mjs" report --cwd "$(pwd)" --artifact REPORT_PATH
```

Put a short peer-review record in the report: outcome, rounds, reviewer model and effort, corrections made, rejected findings with one-line reasons, and remaining uncertainties. The `report` output has all of these.

Check every material citation one final time. Ensure the executive answer matches the evidence and uncertainty sections. Give the user the final Markdown path and the `report` output, and do not produce implementation changes.

## Common mistakes

| Mistake | Correct action |
|---|---|
| Treating a citation as proof without opening it | Read the current source and matching passage. |
| Using a secondary summary when a primary source exists | Cite the primary source; use the summary only for context. |
| Accepting a severe claim because Codex sounds certain | Verify its evidence and impact independently. |
| Hiding uncertainty to force consensus | Preserve it as inference or unknown. |
| Letting review expand the research question | Reject out-of-scope findings. |
| Producing recommendations as if they were facts | Tie each recommendation to stated evidence and assumptions. |

## Review red flags

Pause that finding when it relies on:

- A source that cannot be opened.
- A quote that does not appear in the cited source.
- A stale source for a time-sensitive claim.
- A search snippet rather than source content.
- A conclusion stronger than the cited passage.
- Agreement between the orchestrator and Codex instead of external evidence.

Reclassify, correct, or reject the finding before continuing.
