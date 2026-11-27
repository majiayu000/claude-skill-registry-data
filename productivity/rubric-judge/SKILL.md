---
name: rubric-judge
description: >-
  Run opt-in structured rubric checks through an OpenAI-compatible `/v1/decisions`
  decision model or `/v1/chat/completions` fallback. Use when a parent workflow
  or operator explicitly opts in to fast predicate, choice, or score triage across
  bundled presets (claim-audit, ci-triage, tool-risk, skill-review, memory-curation,
  pr-feedback-triage, citation-entailment, model-escalation, spec-readiness). Not
  a substitute for deterministic gates, artifact inspection, or primary agent sign-off.
  Use rubric-tune for iterative rubric optimization.
disable-model-invocation: true
metadata:
  revision: "1"
  areas: "software-development,work-management"
  targets: "runtime-agnostic"
  summary: "opt-in `/v1/decisions` and `/v1/chat/completions` rubric classifier with 9 bundled presets"
  summary_zh: "按需启用（opt-in）的 `/v1/decisions` 与 `/v1/chat/completions` 结构化 Rubric 分类器，内置 9 大日常预设"
  kind: "mechanism"
---

# rubric-judge

Opt-in structured rubric classifier for fast `predicate`, `choice`, and `score`
checks (`0 output tokens` on native `/v1/decisions` models, with
`/v1/chat/completions` fallback).

## Gates

- **Opt-in only.** If neither `--base-url`/`--model`, `RUBRIC_JUDGE_BASE_URL`/`RUBRIC_JUDGE_MODEL`,
  nor `$XDG_CONFIG_HOME/rubric-judge/config.yaml` (`~/.config/rubric-judge/config.yaml`)
  is configured, `hoa decide --if-configured` prints JSON with `"skipped": true`
  and a reason, then exits `0` (or exits `2` on direct required calls).
  Parent workflows must continue their deterministic verification without failing when
  this skill is unconfigured or unreachable.
- **Advisory triage, never sole acceptance.** A decision model does not run commands,
  inspect the filesystem, or prove a claim. Always re-derive numbers and run
  deterministic repository gates independently.
- **Atomic criteria.** Keep custom questions single-step (`predicate`, mutually
  exclusive `choice`, or `score` with 2–10 levels) and branch in code rather than
  asking for multi-hop reasoning.

## Usage

Run the `hoa` CLI via `uvx` as shown below. In a local checkout use
`uv run hoa decide ...`, or use `hoa decide ...` if installed via `uv tool install`.
Only if a command fails, read [references/troubleshooting.md](references/troubleshooting.md).

```bash
# List bundled presets
uvx --from git+https://github.com/wxxb789/hoa hoa decide --list-presets

# Run a preset only when the operator has configured rubric-judge (exits 0 with {"skipped": true} otherwise)
uvx --from git+https://github.com/wxxb789/hoa hoa decide --if-configured --preset claim-audit --state-file state.json

# Explicit one-shot call; set the URL and model to those approved by the operator
uvx --from git+https://github.com/wxxb789/hoa hoa decide --preset pr-feedback-triage \
  --base-url "$DECISION_BASE_URL" \
  --model "$DECISION_MODEL" \
  --api decisions \
  --state '{"finding":"...", "evidence":"...", "candidate":"..."}'
```

## Bundled Presets

| Preset | Questions (`type`) | Primary parent / use case |
|---|---|---|
| `claim-audit` | `verdict` (`choice`), `action_required` (`predicate`), `risk_score` (`score`) | `delegated-work-acceptance`, `report-claim-audit`, `hermes-ops-claim-verification` |
| `ci-triage` | `symptom` (`choice`), `root_cause_proven` (`predicate`), `triage_priority` (`score`) | CI / test / scheduled-job failure log triage |
| `tool-risk` | `tier` (`choice`), `out_of_scope` (`predicate`), `blast_radius` (`score`) | PreToolUse / permission hook shadow-mode risk classification |
| `skill-review` | `bucket` (`choice`: `change`/`verify`/`consider`), `has_direct_contradiction` (`predicate`) | `hoa-skill-review` intake and candidate grading |
| `memory-curation` | `durability` (`choice`), `relationship` (`choice`) | `distill-memory` pre-write deduplication and noise filtering |
| `pr-feedback-triage` | `resolution` (`choice`: `resolved_root_cause`/`symptom_patch`/`unaddressed`/`regression_introduced`) | `review-revision-candidates`, `ce-resolve-pr-feedback` |
| `citation-entailment` | `entailment` (`choice`: `strictly_entailed`/`temporal_or_scope_drift`/`unsupported_extrapolation`/`insufficient_evidence`) | `evidence-boundary-discipline`, `official-document-verification` |
| `model-escalation` | `route` (`choice`: `stay_fast_worker`/`escalate_single_reviewer`/`escalate_dual_audit`) | `gdd` review tier routing |
| `spec-readiness` | `readiness` (`choice`: `ready_to_dispatch`/`missing_acceptance_seam`/`unbounded_scope`) | `spec-convergence`, `define-goal` pre-dispatch gate |

## Configuration

See [references/configuration.md](references/configuration.md). After the skill-specific
lookup, unset keys fall back to `GHC_DECISIONS_*` (legacy alias) then `EVALS_*` environment variables.

| Key | Flag | Environment variable | Default |
|---|---|---|---|
| `base_url` | `--base-url` | `RUBRIC_JUDGE_BASE_URL` | none (opt-in; skips under `--if-configured`) |
| `model` | `--model` | `RUBRIC_JUDGE_MODEL` | none (opt-in; skips under `--if-configured`) |
| `api` | `--api` | `RUBRIC_JUDGE_API` | `decisions` (`decisions` or `chat-completions`) |
| `effort` | `--effort` | `RUBRIC_JUDGE_EFFORT` | `low` (used by `chat-completions`) |
| `api_key` | — | `RUBRIC_JUDGE_API_KEY` | `dummy` |

## Additional resources

- [agents/openai.yaml](agents/openai.yaml) — explicit-only invocation policy for Codex.
- [references/configuration.md](references/configuration.md) — configuration lookup order and file path.
- [references/troubleshooting.md](references/troubleshooting.md) — read only when a CLI command fails.
