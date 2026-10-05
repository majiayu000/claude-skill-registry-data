---
name: mk:story-sizer
description: Pre-ticket Fibonacci sizing for a paste-mode batch of user stories. Default mode is advisory-only (writes a Story Sizing Report). Opt-in `--auto-create` delegates ticket creation to mk:jira-issue + mk:jira-collaborate with mandatory dry-run + single batch confirmation gate. NOT for single-ticket estimation (mk:jira-estimator); NOT for sprint capacity (mk:planning-engine).
argument-hint: '--paste [--scout] [--story <id>] | --paste --auto-create --project <KEY> [--epic <KEY>]'
phase: on-demand
source: local
keywords:
  - story-sizer
  - pre-ticket-sizing
  - story-points
  - spec-to-sprint
  - fibonacci-estimation
  - split-recommendation
  - auto-create-gated
  - estimate
when_to_use: Use when sizing a batch of suggested user stories BEFORE Jira tickets exist (e.g., after a spec scan). Default emits a Story Sizing Report; --auto-create delegates ticket creation behind a single confirmation gate. NOT for sizing one Jira ticket (use mk:jira-estimator).
user-invocable: true
context: fork
agent: story-sizer
owner: lifecycle
criticality: medium
status: active
runtime: claude-code
---

# mk:story-sizer

Forks to the `story-sizer` agent (system prompt at `.claude/agents/story-sizer.md`). v1 ships paste-mode only: the user provides a markdown block of stories, the agent applies heuristics, and a Story Sizing Report is written to `tasks/reports/story-sizing-{YYMMDD}-{slug}.md`. No Jira side effects in default mode.

## Triggers

- "size these stories"
- "rough-size from spec"
- "pre-ticket sizing for these user stories"
- "Fibonacci size this story list"
- "story points for these candidates before we create tickets"

## Commands

| Mode        | Invocation                                                             | Side effects                                                              |
| ----------- | ---------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| Default     | `/mk:story-sizer --paste [--scout] [--story <id>]`                     | Writes Story Sizing Report only. No Jira calls.                           |
| Auto-create | `/mk:story-sizer --paste --auto-create --project <KEY> [--epic <KEY>]` | After dry-run + single confirmation, delegates ticket creation per story. |

## Input

Paste-mode contract: see `references/input-adapter.md` for the strict markdown template, `StoryRecord` schema, validation rules, and failure modes. The parser is `scripts/parse-paste-stories.py` (deterministic; SHA-256 source-hash recorded for the auto-create source-consistency check).

## Heuristics

Fibonacci sizing rules: see `references/sizing-heuristics.md` for complexity dimensions, scoring tables, inconsistency detection, split-proposal triggers, and DoR advisory. Scorer is `scripts/score-story.py` (integer-arithmetic over text-derived counts; same input → same numeric output).

## Output

Report template + slot semantics: `references/report-writer.md`. Renderer is `scripts/write-sizing-report.py`. Default path: `tasks/reports/story-sizing-{YYMMDD}-{slug}.md`. Idempotency by `source_hash` — repeated runs on the identical paste body re-prompt before overwriting.

Per-story suggested create commands obey the v1 field whitelist: `--project`, `--type`, `--summary`, `--story-points`, `--description`, optional `--epic`, `--components`, `--labels`. No `--assignee`, `--priority`, `--sprint`, `--blocks`, or `--custom-fields` in v1.

## Orchestration

End-to-end default flow + `--scout` extract-or-prompt pattern + filtering rules: `references/orchestration.md`. Story-sizer NEVER auto-invokes `/mk:scout` — it extracts existing session output or prompts the user to run scout first.

## Auto-create (opt-in)

`--auto-create --project <KEY> [--epic <KEY>]` runs 5 pre-flight checks (NO_ACS, Rule-1 injection, length cap, duplicate suspect via `mk:jira-search`, source-hash mismatch). If all pass, a markdown dry-run table renders + a single `AskUserQuestion` gate decides ship-or-abort. Gating rules: `references/auto-create-gating.md`. Rule-1 inventory copy: `references/injection-patterns.md`. Gating check: `scripts/check-auto-create-gating.py`.

## See also

- Agent: `../../agents/story-sizer.md`
- Peer intelligence: `mk:jira-evaluator` (post-ticket complexity), `mk:jira-estimator` (post-ticket estimation), `mk:planning-engine` (sprint capacity)
- Peer execution (delegated): `mk:jira-issue` (create), `mk:jira-collaborate` (audit comment via `--internal`)
- Shared: `../jira/references/estimation-guide.md` (Fibonacci heuristic conventions)

## Gotchas

- The `source_hash` recorded in the report header is the SHA-256 of the _exact_ paste body. If you edit the paste locally between sizing and `--auto-create`, the source-consistency check will ABORT — re-paste the modified body and re-run `--paste` to regenerate the report.
- `--scout` does not auto-invoke `/mk:scout`. Run `/mk:scout` first when you want codebase signals; otherwise the report carries `[NO_CODEBASE_CONTEXT]`.
- DoR advisory only appears when `mk:agent-detector` loaded `.claude/rules-conditional/agile-story-gates.md` for the current session.
