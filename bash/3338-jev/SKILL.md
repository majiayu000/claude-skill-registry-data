---
name: jev
description: Mandatory for semantic decisions during search, debugging, planning, execution, and review — classify, rank, rate, route, or assess supplied evidence.
---

# Jev: typed judgments

## When to call

**Semantic decision + Jev available → MUST call before that decision.**
Explore first; supply evidence, candidates, and criteria. Reassess after new
evidence, failed hypotheses, or changed requirements. Batch independent questions
in one `ask`; wait for evidence/answers needed by dependent questions. Reuse
results while evidence, questions, and criteria are unchanged. No call quotas.

No semantic decision → say so once. Missing plugin, credentials, or service →
state limitation once per task; continue with explicit evidence-based reasoning.
Never invent results. Architecture, exact checks, arithmetic, reproduction,
tests, correctness, and authorization stay with the agent/tools.

## CLI

Requires Bun 1.4.x and environment `TYPESAFE_API_KEY`; never read `.env`.
Use the resolved Bun command injected by the hooks, even when `bun` is absent
from `PATH`. A missing key in a hook is not proof it is absent from the command
environment: check presence there without printing its value before reporting
unavailability. For manual setup, resolve Bun as below.
Use the active host's published wrapper; plugin lifecycle variables are unavailable
in ordinary shells:

```bash
# Codex
JEV="${TOOLU_CONFIG_DIR:-${CODEX_HOME:-$HOME/.codex}}/jev/jev.sh"
# Claude Code: use this assignment instead
# JEV="${TOOLU_CONFIG_DIR:-${CLAUDE_CONFIG_DIR:-$HOME/.claude}}/jev/jev.sh"
JEV_BUN=
for candidate in "${TOOLU_BUN:-}" "$(command -v bun 2>/dev/null)" "$HOME/.bun/bin/bun"; do
  if [ -n "$candidate" ] && [ -f "$candidate" ] && [ -x "$candidate" ]; then JEV_BUN="$candidate"; break; fi
done
```

Repository fallback, when not installed: `plugins/jev/hooks/dist/jev.js`.

User-provided executable overrides at `jev.sh` are preserved and invoked
directly with their own shebang/interpreter, including shell scripts and
JavaScript executables. They must provide an executable shebang; the resolved
Bun prefix applies to the published bundle symlink.

```text
"$JEV_BUN" "$JEV" noul   "question" -s STATE [--true DESC] [--false DESC]
"$JEV_BUN" "$JEV" choice "question" -s STATE -o KEY=DESC -o KEY=DESC
"$JEV_BUN" "$JEV" score  "question" -s STATE -l "lowest situation" -l "highest situation"
"$JEV_BUN" "$JEV" ask questions.json -s STATE
```

- `-s/--state`: literal text, `@FILE`, or `-` (stdin). Required.
- `ask`: question-map JSON file or `-` (stdin); keys become answer IDs. Each
  question needs `type` and `instructions`; `criteria` is required for Choice/Score,
  optional for Noul.
  Structured instructions/criteria use `ask`; other commands take strings.
- Options: `-m/--model` (default `jev-latest`), `--raw` (model/usage),
  `--id` (default `q`; single-question commands only).
- Choice: `-o/--option`, 2–255 options; bare `-o KEY` omits description.
  Score: `-l/--level`, 2–10 levels,
  lowest first. Read returned legend; fractional Scores are not exact quantities.
- Output: answer map (`noul`, or `choice`/`score` plus probabilities/confidence).
  Nonzero exit → fallback, never interpret absent output as a judgment.

## Question contract

- Minimal named evidence; reference fields explicitly, e.g. `source.text`.
- Exact condition + boundary criteria; instructions and criteria must agree.
  Meaning belongs here, not in IDs (the model never sees IDs).
- Split independently useful judgments; keep context for coherent judgments
  such as claim/source support. High Noul = stated condition holds.
- Score levels: self-contained situations, e.g. “Feature broken; workaround
  exists”. Avoid bare numbers or “worse than previous”.
- Include no-match/insufficient-evidence outcomes when candidates may not fit.
- Choice probabilities are relative alternatives; graded relevance needs
  comparable per-candidate Scores. Check answer existence separately from rank.
- Noul near 0.5 = uncertainty. Choice/Score confidence = concentration, not
  correctness. Inspect uncertain/conflicting results; gather missing evidence.
- Calibrate thresholds on representative data, separately per question/type;
  `P(yes)` need not equal `1-P(not yes)`. Pin model when thresholds depend on it.
- Record useful evidence → question → answer → next action. Use `--raw` for
  model/usage evaluation; extra questions cost tokens.

## Load on demand

- Need a pattern: read Setup + the matching section in
  [problem-solving](references/problem-solving.md), not all examples.
- Need transport limits/errors: [wrapper reference](../../README.md#wrapper-reference).
- Designing new question formats: check relevant [live docs](https://docs.typesafe.ai/llms.txt).
- Evaluation only: [record and scenarios](evals/README.md).
