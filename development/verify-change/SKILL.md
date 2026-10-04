---
name: verify-change
description: Mechanical Go verification of a scoped mivia change. Run test, vet, build, race, invariant and contract gates, then report mivia-report/v1. Use after implementation or before merge.
triggers:
  - verify change
  - verify this
  - run verification
  - pre-merge verify
tools:
  - read_file
  - list_dir
  - grep
  - glob
  - find_references
  - run_command
---

# Verify Change

Mechanical, project-bound verifier for the `mivia` Go agent CLI. It runs the real
gates that exist in this repo and reports `mivia-report/v1`. It does NOT reason
about blast radius or risk tiers, and it is not portable: that is the job of the
`verify-code-change` skill.

Use this skill when the change is inside `mivia` Go source (`cmd/`, `internal/`,
`pkg/`) or its `.mivia/` control surface and a `project-runtime.yaml` contract
applies. Use `verify-code-change` instead when no project contract applies, or
when you need the blast-radius reasoning and the PASS/PARTIAL/FAIL report it
provides.

## Read First

- `AGENTS.md`
- `.agents/templates/agent-report-v1.md`
- `.agents/quality/contracts/project-runtime.yaml` (the contract whose `paths` match the scope)
- `.mivia/invariants.md` (when scope touches a listed invariant area)
- `.agents/quality/defect-taxonomy.md` (the recurring defect classes; read the classes the diff touches)
- Diff scope named by the user

## Method

1. Confirm exact scope (packages/files) and baseline (branch/commit/diff). You need the baseline to separate a change-caused failure from a pre-existing one (step 7).
2. Map scope to the matching contract in `.agents/quality/contracts/project-runtime.yaml`. Only the contract whose `paths` overlap the scope is required; do not invent gates for paths the change does not touch.
3. Run the narrowest real gates first, expanding only as the scope demands:
   - package tests for touched packages: `go test ./<affected>/...`
   - `go vet ./<affected>/...` (or `make vet` for the whole module)
   - build: `make build` (produces the `mivia` binary from `./cmd/mivia`)
   - structure gate when the change adds or grows code: `make structure-check` (LOC/function/file-size limits)
4. When scope touches concurrency (goroutines, channels, locks, the agent loop, subagent pools, the event bus, the ledger, cancellation), run the race detector: `make race` (`go test -race ./...`) or `go test -race ./<affected>/...`. A single green run is not proof for order/timing-sensitive paths; re-run a bounded number of times and treat pass-once-fail-on-retry as a failure to investigate, not a pass.
5. When scope touches a `.mivia/invariants.md` area (TUI, agent loop, security/privacy), run `make validate-invariants` (every referenced test must exist) and `make invariants` (runs the invariant tests via a hardcoded `-run` selector in the Makefile). If you add or rename an invariant test, add it to that selector or `make invariants` silently skips it and `make validate-invariants` then fails. When scope touches model-facing tool text (`tool.Description()`, parameter schema descriptions) or compiled default prompts, the generic-surface tests in `internal/tools/generic_surface_test.go` and `internal/cli/chat/prompt_generic_test.go` (run by `make invariants`) must pass: they enforce rule 60 that the tool surface stays project/language-generic.
6. Match the diff to the classes in `.agents/quality/defect-taxonomy.md`. For each matched class, run its probes against the diff and record the class identifier with a one-line result. This step is a gate: an unaddressed probe for a matched class blocks `PASS`. The classes that recur most in this repository are `DC-1` terminal state with no return edge, `DC-2` claim and fence, `DC-4` crash and resume, `DC-6` bounds and truncation, `DC-9` silent failure, and `DC-12` retention across interrupt. When the diff fixes a defect, also run the chain-control sweep from that document and record which other sites of the class you found.
7. When a check fails, reproduce it against the baseline in the same environment before concluding the change is at fault. Baseline-fails-too means environmental or pre-existing; baseline-passes means caused by the change. Continue all remaining safe checks either way, and record which kind it was.
8. Run the matching contract verifier lines from `project-runtime.yaml` for the affected contract.
9. For full pre-merge, run `make verify` - the complete offline gate (agent config, docs, secrets, structure, semgrep, contract tests, invariants, go-check).
10. Record every command with its exit status and a one-line summarized result. Do not invent metrics or paste full successful logs.

## Rules

- Binary under test is `mivia` (`cmd/mivia/`). Brand is MiviaLabs. Host language is Go.
- Do not bypass git hooks.
- Do not use Semgrep suppressions.
- Severity never gates approval; open gaps block `PASS`.
- Do not claim a gate passed unless it was executed. `NOT_RUN` is an honest result.
- Coverage percentage is not a gate here; contract and invariant coverage is. Do not invent a coverage threshold.

## Required Report

When a resource catalogue and its scoped reader are available, load
`report-template` before producing the report. Without that capability, use the
canonical inline fallback from `.agents/templates/agent-report-v1.md`.
Always emit the compact `mivia-report/v1` structure.

Inline fallback:

```text
ReportFormat: mivia-report/v1
Skill: verify-change
Result: PASS|BLOCK|PARTIAL|NOT_RUN
Scope: <exact files/packages>
Summary: <one sentence>
Evidence:
- <command or method>: PASS|FAIL|NOT_RUN - <short note>
Findings:
- none
ResidualRisk: none|<short exact risk>
NextAction: none|<exact action>
```

Result semantics:

- `PASS` - all required gates for scope ran green; no open gap rows; `ResidualRisk: none`.
- `BLOCK` - a failed gate, missing test, or fixable gap remains.
- `PARTIAL` - useful evidence but a named gated dependency or tool (for example `make verify` could not complete) remains.
- `NOT_RUN` - plan only, or verification could not start.
