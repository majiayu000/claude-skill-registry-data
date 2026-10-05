---
name: mk:rubric
version: 1.0.0
preamble-tier: 3
description: Use when loading, listing, composing, or validating graded evaluation rubrics — PASS/WARN/FAIL grading with weighted criteria and balanced PASS/FAIL anchor examples. Triggers on /mk:rubric, "load rubric", "compose rubric preset", "validate rubric", or evaluator-style code review that needs anchor-grounded judgments.
argument-hint: '[list | load <name> | compose <preset> | validate]'
allowed-tools:
  - Bash
  - Read
  - Grep
  - Glob
source: local
keywords:
  - rubric
  - graded-evaluation
  - weighted-criteria
  - pass-warn-fail
  - anchor-examples
  - calibration
when_to_use: Use when loading, listing, composing, or validating graded evaluation rubrics with PASS/WARN/FAIL grading.
user-invocable: true
owner: testing
criticality: medium
status: active
runtime: claude-code
---

# Rubric Library API

Discovery, composition, and validation for the rubric library at `.claude/rubrics/`.

> **Path convention:** Commands below assume cwd is `$CLAUDE_PROJECT_DIR` (project root). Prefix paths with `"$CLAUDE_PROJECT_DIR/"` when invoking from subdirectories.

> **Consumed by `evaluator` agent + `mk:evaluate` skill (Phase 3, shipped 260408).** The dedicated `evaluator` subagent (`.claude/agents/evaluator.md`) drives the running build via active verification and grades it against rubrics composed from this library. The `mk:evaluate` skill (`.claude/skills/evaluate/`) is the orchestration shell. This skill (`mk:rubric`) remains independently invokable via `/mk:rubric <subcommand>` for manual rubric inspection, validation, or composition outside the evaluator workflow.

## When to Use

Activate when:
- User runs `/mk:rubric [subcommand]`
- An evaluator subagent needs to load rubrics for grading
- Sprint-contract negotiation references a rubric by path
- CI validates rubric schema conformance after edits

## Subcommands

| Subcommand | Purpose | Output |
|---|---|---|
| `list` | List all available rubrics + presets | Table: name, weight_default, applies_to |
| `load <name>` | Load a single rubric and emit prompt-ready fragment | Markdown block ready to inject into evaluator prompt |
| `compose <preset>` | Load a composition preset and return all member rubrics + weights | Composed prompt fragment with weight table |
| `validate [path]` | Validate one rubric (or all if no path) against schema.md | PASS / FAIL with diagnostics |
| `validate --preset [path]` | Validate composition preset (weights sum to 1.0 ±0.01) | PASS / FAIL |

## Usage Examples

```bash
# List all rubrics
.claude/skills/rubric/scripts/load-rubric.sh --list

# Load one rubric for the evaluator
.claude/skills/rubric/scripts/load-rubric.sh design-quality

# Compose a preset (returns all member rubrics + weight table)
.claude/skills/rubric/scripts/load-rubric.sh --preset frontend-app

# Validate every rubric file in the library
.claude/skills/rubric/scripts/validate-rubric.sh
```

## Output Schema

### `load <name>` output

```markdown
## Rubric: {name} (weight: {weight_default}, hard_fail: {threshold})

{Intent paragraph}

### Criteria
{bullets}

### Grading
{table}

### Anti-patterns
{bullets}

### Few-Shot Examples
{PASS + FAIL examples, balanced — section name matches schema.md and the actual rubric files}
```

### `compose <preset>` output

```markdown
## Composition: {preset-name}

| Rubric | Weight | Hard-Fail Threshold |
|---|---|---|
| ... | ... | ... |

(All member rubrics inlined below)
```

## Schema

Rubrics MUST conform to `.claude/rubrics/schema.md`. The validator enforces:
- Required frontmatter fields (`name`, `version`, `weight_default`, `applies_to`, `hard_fail_threshold`)
- Required sections in order
- ≥1 PASS + ≥1 FAIL anchor example, balanced (±1)
- File ≤200 lines

Composition presets MUST have all weights summing to 1.0 ±0.01.

## Calibration

Few-shot anchor examples MUST be added per the rules in `references/calibration-guide.md`:
- Balanced PASS/FAIL counts (positive bias mitigation)
- Randomized presentation order (position bias mitigation)
- Drawn from real prior reviews where possible (synthetic examples only as backup)

## Gotchas

- **Adding a new rubric:** drop a `.md` file into `.claude/rubrics/`, run `validate-rubric.sh`, register weight in any preset that should include it.
- **Weight drift:** if you change a rubric's `weight_default`, all presets that reference it must be re-checked for sum=1.0.
- **Anti-patterns are FIXED:** they trigger FAIL regardless of the surrounding criteria. Don't add subjective ones.
- **Don't load all rubrics:** the evaluator should load only the relevant preset, not the whole library — context efficiency.

## References

| File | Purpose |
|---|---|
| `scripts/load-rubric.sh` | Load + emit prompt fragment for one rubric or preset |
| `scripts/validate-rubric.sh` | Schema conformance + weight-sum validator |
| `references/calibration-guide.md` | How to add few-shot examples (balanced + randomized) |
| `../../rubrics/schema.md` | Canonical rubric format specification |
| `../../agents/evaluator.md` | The agent that consumes composed rubrics during behavioral active verification (Phase 3, shipped) |
| `../mk:evaluate/SKILL.md` | The orchestration shell that drives the evaluator + invokes this skill via `compose <preset>` (Phase 3, shipped) |

## Start

For interactive use, run `scripts/load-rubric.sh --list` to discover available rubrics.
For evaluator-internal use, the `evaluator` agent (via `mk:evaluate`) loads `compose <preset>` automatically based on the target type detected by `mk:evaluate/scripts/run-evaluator.sh`. Sprint-contract-based filtering is gated until Phase 4 ships (step-01 of mk:evaluate stub-guards on the `contract_schema_version:` marker).
