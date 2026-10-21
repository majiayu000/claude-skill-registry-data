---
name: self-verify
description: Run or interpret the issueops self-verification loop. Use when the user asks to verify the harness, run the 95-point gate, inspect self-verification candidates, compare or promote verification baselines, or confirm CLI/MCP/native integration health.
---

# Self-verification loop

## Goal

First-party hosts are exactly Codex, Claude Code, Omo native, omp, and opencode. Verify that
the harness behaves consistently across all five hosts and that CLI, MCP,
native integration, state, policy, docs, and skills work as intended.
This skill is a QA gate; it does not choose improvements by itself.

## Scope for an IssueOps cycle

When verifying a selected IssueOps cycle, first run
`issueops status --id "$ISSUEOPS_ID" --json` for that exact lifecycle ID. Read
`branch_prepare.base_sha` from the current result into `BASE_SHA` and pass it to
self-verify, including when the worktree is clean after committing:

```bash
./bin/issueops self-verify --base-ref "$BASE_SHA" --seed=100 --target-score=95 --llm-eval=false --json
```

A missing prepared base blocks cycle verification; do not fall back to an
unscoped run, infer origin/main, or select another cycle. MCP callers supply the
same commit as `self_verify.base_ref`. The scope combines that commit's tree to
the observed HEAD tree with staged, unstaged, and untracked paths. An invalid
ref or failed Git observation fails risk QA. The result's `risk QA tier` stdout
preserves `scope.base_sha`, `scope.head_sha`, and scope errors even when command
logs are truncated. A valid empty scope is a successful no-op. Standalone calls
that omit the optional ref retain working-tree-only scope.

## Commands

```bash
./bin/issueops self-verify --seed=100 --target-score=95 --llm-eval=false --json
./bin/issueops self-verify --seed=100 --target-score=95 --llm-eval=false --progress=jsonl --json
# Every gate runs even after a failure (concurrent regression diagnosis); each failure still fails the run:
./bin/issueops self-verify --seed=100 --target-score=95 --llm-eval=false --collect-all-steps --progress=jsonl --json
ISSUEOPS_SELF_VERIFY_LLM_EVAL=gate ./bin/issueops self-verify --seed=100 --target-score=95 --json
./bin/issueops self-verify candidates --json
./bin/issueops self-verify history --prefix self-verify --json
./bin/issueops self-verify compare --baseline-key self-verify-baseline --candidate-key self-verify-latest --json
./bin/issueops self-verify promote --from-key self-verify-latest --baseline-key self-verify-baseline --confirm --json
# Confirmed promote refuses a source snapshot that did not pass the gate; --allow-failed-source is an
# explicit, deliberate override for accepted deviations only — never a pressure/demo shortcut.
```

`self-verify` runs one complete deterministic evidence pass. Repeated `--full` and
`--iterations` modes were removed because they reran the same expensive build and
runtime gates without adding independent evidence. Seeded validators keep their
deterministic case batteries inside that pass. The `Python script tests` step checks
Python 3.10+ and runs `scripts/python_suite_runner.py`, which discovers root and
skill-owned Python suites, before risk QA/Go tests.
Missing or unsupported Python fails the step; discovery has a five-minute timeout
and contributes to test-suite scores and coverage. The native summary contract separates
this evidence from historical summaries while keeping snapshot schema v1.

The command never launches Codex,
Claude, or a live model. The normative live/reproduction and evidence rules are in
`.issueops/TESTING.md`.

`ISSUEOPS_SELF_VERIFY_LLM_EVAL` defaults to off. In the current implementation, setting it to `advisory` or `gate` only renders the read-only evaluator prompt after deterministic self-verification. No Z.AI request is sent. The `advisory` result exposes that prompt without changing deterministic success, while `gate` therefore returns a non-passing `llm_eval` result because no external verdict is ingested.

For the repository's deterministic completion gate, pass explicit `--llm-eval=false` when the environment intentionally exports `ISSUEOPS_SELF_VERIFY_LLM_EVAL=gate`; explicit CLI flags override the environment. Record that override and restart the verification sequence from its first gate after any interrupted or prompt-only run. Do not report a prompt-only result as an external LLM judgment.

`self-verify` owns one deterministic evidence pass for the checks it actually
runs. A passing result does not prove `go vet ./...` or `go test -race ./... -count=1` ran unless the `risk QA tier` step includes those exact commands. For
the final verification battery, use the base-to-head plus preserved work scope
from `.issueops/testing/self-verification.md`: clean committed Go changes still
need any missing vet/race members in the same evidence bundle.

## Gate

Completion requires every concrete goal score to exceed the target score. The default target is 95. If any item scores 95 or below, the state is not complete; improve, retry, or report the blocker.

If any self-verification candidate test, compilation, or general check fails during the loop, you can execute the `lint_diagnose` MCP tool (or run `issueops project lint-diagnose -- <failed_command>`) to quickly diagnose the root cause and receive a targeted fix proposal via Gemini 3.5 Flash. This enables fast auto-healing during the self-verify cycle.

다단계 검증에서 한 단계라도 실패하면 1단계부터 재실행하며 부분 통과 evidence를 재사용하지 않는다 (규범 출처: `.issueops/TESTING.md` 부분 검증 상태 금지 절).

## Candidate catalog

The self-verification improvement catalog in this skill's `CANDIDATES.md` is the source of truth.
