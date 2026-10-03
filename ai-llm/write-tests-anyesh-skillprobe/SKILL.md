---
name: write-tests
description: >
  Write skillprobe YAML tests for LLM skills. Use when asked to write tests,
  create test scenarios, test a skill, generate skillprobe tests, or check
  whether a skill activates correctly.
---

# Writing skillprobe Tests

Generate YAML test files for skillprobe. Always read the skill content first before writing tests.

When asked to write tests for a skill, generate BOTH files unless the user asks for only one:
1. A behavioral test file (for `skillprobe run`)
2. An activation test file (for `skillprobe activation`)

## Behavioral Tests (for `skillprobe run`)

Test what the model DOES when the skill is loaded.

```yaml
harness: claude-code    # or cursor
model: claude-haiku-4-5-20251001
timeout: 120
skill: ./path/to/skill  # directory with SKILL.md, or a .md file

scenarios:
  - name: "descriptive name"
    steps:
      - prompt: "what the user would type"
        assert:
          - type: contains
            value: "expected text"
```

## Activation Tests (for `skillprobe activation`)

Test whether the skill LOADS for relevant prompts and stays quiet for irrelevant ones. This is a separate YAML format from behavioral tests.

```yaml
harness: claude-code
model: claude-haiku-4-5-20251001
timeout: 60
skill: ./path/to/skill

activation:
  skill_name: my-skill
  should_activate:
    - "prompt that should trigger this skill"
    - "another relevant prompt"
  should_not_activate:
    - "completely unrelated prompt"
    - "another unrelated prompt"
```

The `activation` key replaces `scenarios`. These are two different file formats loaded by different commands (`skillprobe run` vs `skillprobe activation`). Never put both keys in the same file. skillprobe will either ignore one silently or fail to parse the file.

Bad:
```yaml
skill: ./skills/commit
activation:
  skill_name: commit
  should_activate:
    - "commit my changes"
scenarios:
  - name: "commit happens"
    steps:
      - prompt: "commit"
        assert:
          - type: contains
            value: "commit"
```

Pick one format per file.

## Testing skill combinations

Some tests need to load more than one skill at a time, either because you are probing interactions between skills or because the scenario legitimately needs both. Use a `skills:` list at the suite level instead of the singular `skill:`:

```yaml
harness: claude-code
model: claude-haiku-4-5-20251001
skills:
  - ./skills/clean-code
  - ./skills/bad-python

scenarios:
  - name: "clean-code wins over bad-python on function shape"
    steps:
      - prompt: "Write a Python function called add that takes two integers"
        runs: 5
        min_pass_rate: 0.8
        assert:
          - type: regex
            value: 'def add\([^)]*: *int[^)]*: *int[^)]*\) *-> *int'
          - type: not_contains
            value: '"""'
```

`skill:` (singular) and `skills:` (plural list) are mutually exclusive, and the matrix form below cannot coexist with either. Pick exactly one of the three per file.

## Sweeping one skill against many with a matrix

When you want to test one base skill against a list of other skills without writing a separate file per pairing, use a `matrix:` block at suite level. It expands into N scenario runs, one per `pair_with` entry, loading `base` together with that entry:

```yaml
harness: claude-code
model: claude-haiku-4-5-20251001
matrix:
  base: ./skills/my-new-skill
  pair_with:
    - ./skills/popular-a
    - ./skills/popular-b
    - ./skills/popular-c

scenarios:
  - name: "my-new-skill still works when paired with a popular skill"
    steps:
      - prompt: "the usual request for my-new-skill"
        runs: 5
        min_pass_rate: 0.8
        assert:
          - type: regex
            value: "expected pattern"
```

Use `matrix:` when you have one base skill and a reference set of others to sweep it against. Use a plain `skills:` list when you want a specific hand-picked combination. Do not use both in the same file.

## Detecting real regressions with baseline mode

A matrix run reports pass or fail per pairing but does not tell you whether a combined failure is a genuine regression or just natural model variance. For that, tell the user to run the same matrix YAML with `skillprobe run ... --baseline --baseline-runs 20`. Baseline mode runs every pairing three times per scenario (base alone, paired alone, combined) and classifies each assertion as one of `regression`, `shared_failure`, `flaky`, or `ok`.

The test author does not write anything special for baseline mode. It works on any YAML that already has a `matrix:` block. Your job is to set realistic `runs:` and `min_pass_rate:` values on the scenarios, and when you hand the test to the user, tell them that baseline mode is the right command to run when they want to separate real combination bugs from variance noise. Baseline mode is expensive (roughly three times a normal matrix run) so treat it as a nightly or on-demand audit, not a per-PR check.

## Before picking min_pass_rate, measure

`skillprobe measure test.yaml --runs 20` runs each scenario 20 times and reports per-assertion pass rates with 95 percent Wilson confidence intervals and a variance classification of `deterministic`, `probabilistic`, `noisy`, or `unreliable`. Run this against your draft test before committing to a `min_pass_rate` value. If the observed pass rate is 70 percent with a CI spanning 0.40 to 0.89, setting `min_pass_rate: 0.8` will produce a scenario that fails roughly half the time on variance alone and users will distrust the test.

Measure first, then pick a threshold from the data.

## Assertion Types

| Type | Checks | Example |
|---|---|---|
| `contains` | Response includes value (case-insensitive) | `value: "deploy-k8s.sh"` |
| `not_contains` | Response does NOT include value | `value: "helm install"` |
| `regex` | Response matches pattern | `value: "def \\w+\\("` |
| `tool_called` | A tool was invoked | `value: "Bash"` |
| `skill_activated` | A skill was loaded | `value: "commit"` |
| `file_exists` | File exists in workspace (after block) | `value: ".git/COMMIT_EDITMSG"` |
| `file_contains` | File contains text (path:content) | `value: "main.py:def hello"` |

Any assertion supports `negate: true` to invert it.

## Multi-Run

Skills are probabilistic. Use `runs` and `min_pass_rate` to measure reliability:

```yaml
steps:
  - prompt: "Write a function with type hints"
    runs: 5
    min_pass_rate: 0.8
    assert:
      - type: regex
        value: "-> "
```

## Pass rate thresholds

`min_pass_rate: 0.0` is never correct. A zero threshold means the scenario passes no matter what the model does, which makes the assertion vacuous. Use these defaults:

- **Deterministic rule** (the skill either followed the rule or it didn't, no ambiguity expected): `min_pass_rate: 1.0`
- **Probabilistic rule** (model variance expected, most runs should follow the rule): `min_pass_rate: 0.8`
- **Genuinely uncertain contest** (two competing rules, either could win on any run): `min_pass_rate: 0.5`

If you cannot justify a `min_pass_rate` of at least 0.5, the scenario is probably testing the wrong thing.

## Writing Good Domain Skill Tests

Domain skills teach project-specific knowledge. Test for YOUR specifics, not generic behavior.

Bad: `value: "deploy"` (any deployment knowledge passes)
Good: `value: "deploy-k8s.sh"` with `not_contains: "helm install"` (checks your exact tool)

For every domain skill, cover:
1. **Correct commands**: your specific tools, not generic alternatives
2. **Specific details**: URLs, config values, architecture names from the skill
3. **Negative cases**: tools or patterns your project doesnt use
4. **Activation**: prompts from the skill's trigger words, plus unrelated prompts that should not trigger it

## Strong vs weak assertions

An assertion is only useful if it discriminates between "skill was followed" and "skill was not followed." An assertion that would pass regardless of model behavior is noise.

**Weak** (passes for any relevant response, no signal):
- `contains: "import"` — any Python code mentions imports
- `regex: "result ="` — any variable assignment passes
- `contains: "function"` — any explanation mentions functions

**Strong** (only passes when the specific rule was followed):
- `regex: "^from [a-z]+ import [a-z]"` for "use from-imports in alphabetical order"
- `regex: "def \\w+\\([^)]*: *int[^)]*\\) *-> *int"` for "must use int type hints on params and return"
- `not_contains: '\"\"\"'` for "no docstrings on small helpers"

Before writing an assertion, ask: "what response would this assertion accept that should not be accepted?" If the answer is "any reasonable response," the assertion is too weak.

## Avoid contradictory scenarios

Each scenario should have exactly one clear expected outcome. Two scenarios with the same prompt asserting opposite outcomes cannot both pass, so the suite produces no signal about which rule the skill should enforce. If you are probing a contest between two behaviors, use ONE scenario with a probabilistic `min_pass_rate`, not two scenarios with mutually exclusive assertions.

Bad:
```yaml
- name: "uses type hints"
  steps:
    - prompt: "write a function that adds two numbers"
      assert:
        - type: regex
          value: "-> int"
- name: "no type hints"
  steps:
    - prompt: "write a function that adds two numbers"
      assert:
        - type: not_contains
          value: "-> "
```

Good:
```yaml
- name: "uses int type hints at least 80% of the time"
  steps:
    - prompt: "write a function that adds two numbers"
      runs: 5
      min_pass_rate: 0.8
      assert:
        - type: regex
          value: "-> int"
```

## Running

```bash
skillprobe run tests/my-skill.yaml
skillprobe run tests/my-skill.yaml --harness cursor --model auto
skillprobe run tests/my-matrix.yaml --baseline --baseline-runs 20
skillprobe measure tests/my-skill.yaml --runs 20
skillprobe activation tests/my-activation.yaml
```
