---
name: self-augment
description: "Run the self-augmentation loop for issueops or another repository: use GENIUS_THINK.md, repo evidence, and research-backed agent improvement patterns to choose a necessary feature, performance, quality, or documentation improvement, implement one safe high-value diff, and verify it with the self-verification loop. Use when the user asks for self-augmentation, autonomous improvement, repo enhancement, 95-point gate loops, or to decide and execute the next valuable improvement."
---

# Self-augmentation loop

## Goal

Autonomously identify, select, implement, and verify one improvement that makes the repository materially better. A report-only analysis or test-only run is not enough.

## Required distinction

- **Self-verification loop**: verifies that the service/harness behaves as intended, including tests and QA. Deterministic gate: `./bin/issueops self-verify --seed=100 --target-score=95 --llm-eval=false --json`; collect-all evidence pass: add `--collect-all-steps --progress=jsonl`.
- **Self-augmentation loop**: directly implements one needed feature, performance improvement, quality improvement, or documentation improvement, then verifies it with the self-verification loop.

## Exit criteria

Completion requires all goals below to exceed `target_score`. The default target is 95. If any score is 95 or below, keep improving or report the blocker.

1. Improvement selection: use repo evidence and `GENIUS_THINK.md` to produce at least 10 candidates, then score value, feasibility, and risk.
2. Implementation: the selected candidate appears as an actual code, docs, or skill diff. Cosmetic-only changes do not count.
3. Verification and QA: targeted tests, QA checks, and `self-verify` pass.
4. Learning capture: record decisions, failure lessons, and next candidates in state or docs where appropriate.

## Workflow

1. **Baseline**
   - Read the nearest `AGENTS.md`/`CLAUDE.md`, `GENIUS_THINK.md`, and `skills/self-augment/SELF_AUGMENTATION.md` when present.
   - Run or inspect `./bin/issueops self-augment --json` for the current candidate curriculum.
   - Use `./bin/issueops self-augment --save-state --state-key self-augment-latest --json` when the selected plan should become durable memory for the next cycle.
   - Use `./bin/issueops self-augment --cycles 3 --json` to plan multiple improvement cycles at once (default 1).
   - Use `./bin/issueops self-augment lesson --lesson "..." --next-action "..." --json` to store reusable Reflexion lessons.
   - Run a baseline self-verification loop when feasible; otherwise capture why it cannot run.

2. **Candidate curriculum**
   - Generate at least 10 concrete improvement candidates.
   - Use at least two `GENIUS_THINK.md` formulas, preferring problem reframing, innovative solution generation, thought evolution, and complexity resolution.
   - Score each candidate by impact, feasibility, novelty, risk, verification cost, and user value.
   - Treat candidates marked `already_satisfied` by the planner as audit history only; select the highest-value `open` candidate so repeated cycles keep moving to the next necessary improvement.
   - Prefer high-value, low-risk, reversible improvements over broad rewrites.

3. **Select and implement**
   - Choose one candidate whose expected score can exceed 95 after implementation.
   - Make small, reviewable diffs. Do not add dependencies unless the user explicitly asked or evidence shows they are necessary.
   - Preserve host-neutral core boundaries: shared behavior in Go contract/domain/application/ports, host-specific details in Codex/Claude/Omo/omp/opencode adapters.

4. **Feedback and retry**
   - Convert every failing test, QA issue, or design concern into a short Reflexion-style lesson.
   - Apply the lesson and retry until the goal scores exceed 95 or a hard blocker remains.

5. **Verify**
   - Run targeted tests for the changed behavior.
   - Run `go test ./... -count=1`, relevant golden tests, risk-tier QA checks (`go vet ./...` / `go test -race ./... -count=1` when Go risk is present), skill validation, and build checks as applicable.
   - Finish with `./bin/issueops self-verify --seed=100 --target-score=95 --llm-eval=false --json` when practical; add `--collect-all-steps --progress=jsonl` when every deterministic step must run after an earlier failure.

6. **Capture**
   - Store durable lessons only when reusable: `issueops state`, `.issueops/`; prefer `self-augment --save-state` for the selected candidate curriculum and `self-augment lesson` for reusable failure/QA/design lessons.
   - Final report includes selected candidate, implemented diff, goal scores, verification evidence, and remaining risk.

## Reference

For the detailed loop contract and research rationale, read `SELF_AUGMENTATION.md` in this skill directory. The self-verification candidate catalog in `skills/self-verify/CANDIDATES.md` is the source of truth.
