---
name: decision-trace-writer
description: Secondary persistence workflow for durably recording a stable engineering decision, finding, or user-clarified constraint after the primary review, diagnosis, architecture, or implementation work establishes it. Use when the user or repository explicitly requests a decision trace, or when a settled decision should be preserved for future agents; do not use as the primary workflow for every review, diagnosis, or architecture task.
---

# Decision Trace Writer

Write a local, agent-facing decision trace that lets a future Codex instance recover what happened, why it mattered, which constraints were clarified, what was decided, and what remains. Follow the current repository's durable-memory convention rather than inventing one.

Use this as a secondary persistence workflow. Complete the relevant review, diagnosis, architecture, or implementation reasoning first; then preserve only a stable result that passes the gate below. Do not create a trace merely because the skill loaded or to manufacture training data.

## Reference Navigation

Load only the reference needed for the current trace:

| Need | Read |
| --- | --- |
| Expanded or compact trace structure, section guidance, and quality prompts | [Trace formats](references/trace-formats.md) |
| TraceGym schema, skill-application evidence, field rules, sanitized-derivation boundary, or skill-proposal signal | [TraceGym metadata](references/tracegym-metadata.md) |
| A concrete fictional walkthrough of the workflow | [Export idempotency example](examples/export-idempotency-trace.md) |

Do not load the example just to write an ordinary trace. Load the TraceGym reference only when the trace has reusable workflow, eval, evaluator, benchmark, or skill-improvement value.

## Worth-Recording Gate

Before inspecting placement or writing files, decide whether a durable trace is warranted.

Record or update a trace when at least one condition holds:

- The user explicitly asks to preserve context for future Codex runs, agent memory, durable local guidance, or a decision trace.
- A stable engineering decision, finding, or constraint has been clarified and future agents are likely to need it.
- Local evidence confirmed, weakened, or disproved a review claim, bug hypothesis, or architecture concern that should not be re-litigated.
- The decision rejects an obvious alternative that a future agent might otherwise reintroduce.
- The decision affects architecture boundaries, integration contracts, user-facing behavior, correctness, data integrity, migrations, evaluations, or cross-surface behavior.
- Implementation or validation changed an existing trace's status.
- The session established a reusable agent-workflow signal such as a repeated failure mode, missing validation gate, better decomposition boundary, or corrected skill behavior.

Do not write a trace for a routine implementation detail, transient plan or TODO list, meeting-style recap, unresolved investigation, unchanged duplicate, raw transcript, raw training data, or matter better captured by a final response, inline comment, issue, ADR, or ordinary project document.

If the gate fails, stop this workflow and briefly state why no durable trace was created. If the result is borderline in an interactive session, explain the tradeoff and ask or propose before creating a new trace.

This skill does not replace a formal ADR. When a decision changes public architecture, APIs, integration contracts, or team policy, recommend updating the relevant human-facing documentation too.

## Core Workflow

1. **Read local truth.** Inspect relevant context files, code, tests, diffs, logs, prior traces, and repository instructions. Do not reconstruct the decision from conversation memory alone.
2. **Choose create or update.** Search existing traces. Update the same decision when its status, validation, revisit triggers, or metadata changed. Create a new trace only for a materially different problem, decision axis, affected surface, or stable constraint.
3. **Separate evidence from interpretation.** Distinguish the original claim, source evidence, repository constraints, user-clarified constraints, final decision, rejected alternatives, and rationale.
4. **Preserve the user's design signal.** Summarize what important follow-up questions or pushback imply about risk tolerance, system semantics, operational cost, test boundaries, and priorities; do not merely quote the user.
5. **Make the result actionable.** Record concrete affected files and behavior boundaries, required and prohibited behavior, invariants, validation expectations, current status, unresolved boundaries, and revisit triggers.
6. **Choose the right trace size.** Read [Trace formats](references/trace-formats.md) and select compact or expanded structure using its impact criteria.
7. **Classify every trace.** Write an explicit privacy class in the trace whether or not TraceGym metadata will be present. Use `local_raw_trace` for the normal repository-grounded trace. Use `sanitized_trace_seed` or `public_benchmark_candidate` only for a separately authorized derived artifact that satisfies the corresponding publication gate.
8. **Add reusable-signal metadata conditionally.** When the trace has reusable workflow, eval, benchmark, evaluator, or skill-improvement value, read [TraceGym metadata](references/tracegym-metadata.md) and append its appropriate final-footer template. When metadata is included, write exactly one final `## TraceGym Metadata` section, immediately followed by a YAML fence whose opening line is exactly three backticks followed by `yaml`; its fence begins with `tracegym_metadata:` and, after the closing fence, the trace contains no non-whitespace content. The Full or Compact template is the body of that final footer, not an arbitrary code sample elsewhere in the trace. When present, `skill_application_evidence` is the final metadata field. Use its canonical skill-application entry fields only for observed loading or use, record human review honestly, and keep application evidence distinct from skills that might learn from the case. Omit metadata altogether when this conditional gate fails; record the omission reason while retaining the standalone privacy classification.
9. **Respect privacy and publication boundaries.** Keep private or ignored traces unstaged unless the user explicitly asks otherwise. Treat any future sanitized or public derivative as separate work requiring separate review.
10. **Verify the artifact.** Check existence, readability, filename, evidence accuracy, current status, privacy class, version-control state, and honest validation claims.

## Repository Convention And Placement

Inspect `AGENTS.md`, `README.md`, documentation and ADR directories, agent-context directories such as `.agents/`, `.codex/`, or `.manifest/`, and existing trace, finding, benchmark, eval, or memory conventions.

Choose placement in this order:

1. Use the user-specified location.
2. Otherwise follow an existing trace, decision, or findings convention.
3. Otherwise follow an existing agent-memory or repository-context convention.
4. Otherwise ask or propose in an interactive session.
5. Otherwise use a conservative directory such as `decision-traces/` in a non-interactive session and state that no convention was found.

Never silently create a complex hierarchy or turn another repository's convention into a global rule. Use concrete project names only inside the generated repository-local trace, not in the reusable skill guidance.

Name every new trace:

```text
<trace directory>/YYYY-MM-DD_HHmm_<decision_slug>_trace.md
```

Preserve hour and minute to prevent same-day collisions and maintain chronological order. Use a focused decision slug. Mention or use `.manifest/decision-traces/` only when the repository already does so or the user requests it.

## Evidence Contract

Use this evidence hierarchy when sources conflict:

1. Current code, tests, specifications, configuration, schemas, diffs, and reproducible behavior.
2. Repository-local instructions, existing traces, ADRs, and durable documentation.
3. User clarifications made in the current task.
4. Logs or external evidence whose source and freshness are known.
5. Inference, clearly labeled.

When evidence is incomplete, state what was inspected and what remains unknown. Never invent code references or paths, and never present planned or blocked validation as completed.

## Asset Layers And Publication Gates

Keep these assets distinct:

1. `local_raw_trace`: private, repository-grounded memory for future debugging and context recovery. It may contain allowed local facts and evidence, but never secrets or real credentials.
2. `sanitized_trace_seed`: a future derived seed that retains a reusable workflow lesson after private names, paths, data, and links are removed or generalized. This skill may describe the sanitization boundary but does not produce this artifact unless separately requested.
3. `public_benchmark_candidate`: a possible future public eval, benchmark, evaluator, or skill-proposal candidate derived from a sanitized seed, never directly from a raw trace. It still requires curation, review, redaction, and usually synthetic fixtures.

Do not collapse or automatically transform these layers. Trace usefulness does not imply public safety. Do not turn this skill into a trace extractor, sanitizer, dataset generator, training pipeline, evaluator builder, or skill-proposal generator.

## Privacy And Sanitization

- Never copy secrets, credentials, tokens, private keys, authentication material, or raw session transcripts into a trace.
- Treat raw customer or personal data as prohibited unless the user explicitly authorizes local-only storage and the exact content is necessary.
- Prefer compact stable summaries over raw logs, payloads, screenshots, private messages, production data, or confidential excerpts.
- Redact identifiers unless required for reproducibility, and be especially conservative in version-controlled locations.
- A private raw trace may retain repository-local paths, implementation facts, commands and actual results, commit references, rejected alternatives, user clarification signals, and unresolved validation boundaries when allowed.
- Mark private-fixture cases private-only; never imply that a future benchmark is publishable merely because it is useful.
- Before any reuse outside the private boundary, record what must be removed or generalized, the reusable lesson that remains, whether a synthetic fixture can reproduce it, and whether the case is public-candidate, private-only, or unsuitable for export.

## Output Contract

The trace must capture, at the detail warranted by its risk:

- the problem and source of the claim;
- concrete evidence and any counter-evidence;
- repository and user-clarified constraints;
- alternatives considered and rejected;
- the final engineering contract, including required behavior, prohibited behavior, invariants, and revisit conditions;
- implementation or continuation shape;
- current implementation, commit, validation, or blocked status;
- future validation and follow-up boundaries;
- an explicit privacy class, normally `local_raw_trace`, even when TraceGym metadata is omitted;
- TraceGym metadata only when its conditional gate passes, as exactly one final `## TraceGym Metadata` section with its `yaml` fence and no later non-whitespace content.

In the final response, state the trace path, whether it was created or updated, the validation performed, and any privacy or version-control boundary relevant to the user.

## Failure Behavior

- If no repository convention exists and placement authority is required, ask or propose rather than guessing.
- If the decision is unresolved, keep it in active work context rather than presenting it as durable truth.
- If source evidence is unavailable or contradictory, record the uncertainty or do not write the trace.
- If an existing trace already captures the same decision with no material change, do not create a duplicate.
- If sanitization or publication is requested, treat it as a separate workflow and do not expose the raw trace.
- If validation is unsafe, unavailable, skipped, or blocked, state that exactly.

## Before Finishing

Verify that the trace exists and is readable; follows the filename and local placement convention; includes concrete evidence and user clarification; distinguishes facts, inference, decision, and status; contains no prohibited sensitive material; keeps ignored/private files unstaged absent explicit authorization; states an explicit privacy class whether TraceGym metadata is present or omitted; keeps any metadata privacy class consistent with the standalone classification; and reports only validation that actually ran.
