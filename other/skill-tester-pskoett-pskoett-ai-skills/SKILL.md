---
name: skill-tester
description: "Validates all interactive skills in this repo against the Agent Skills spec, project conventions, and structural requirements. Runs quick_validate.py, checks line limits, verifies cross-references, and tests hook scripts. Use when skills have been added or modified and you want to verify everything passes before committing or submitting."
---

# Skill Tester

Validates all interactive (non-CI) skills in this repo. Runs the Anthropic skill-creator's `quick_validate.py` plus project-specific checks.

## When to Use

- After adding or modifying a skill
- Before committing changes
- Before submitting the plugin for Anthropic review
- As part of the outer loop when eval-creator needs to verify skill quality

## Checks

### 1. Anthropic Spec Validation

Run `quick_validate.py` on every skill in `skills/` (excluding `-ci` variants):

```bash
for d in skills/*/; do
  skill=$(basename "$d")
  [[ "$skill" == *-ci ]] && continue
  python3 .claude/skills/skill-creator/scripts/quick_validate.py "$d"
done
```

**Pass criteria:** Exit code 0 for every skill. Frontmatter has only allowed keys (`name`, `description`, `license`, `allowed-tools`, `metadata`, `compatibility`). Name is kebab-case, max 64 chars. Description max 1024 chars, no angle brackets.

### 2. Project Convention Checks

For each skill directory:

| Check | Rule | Severity |
|-------|------|----------|
| Name matches folder | Frontmatter `name` == directory name | Error |
| Line limit | SKILL.md at or under 600 lines | Error |
| No README.md | Skill folders must not contain README.md | Error |
| Scripts executable | All `.sh` files in `scripts/` must have execute permission | Error |
| References exist | Files referenced in SKILL.md body actually exist in `references/` (agent-performed — not covered by run-tests.sh) | Warning |
| Description non-empty | Description field is present and non-empty | Error |

### 3. Instruction File Validation

Validate this finite instruction-file set:

- `CLAUDE.md`
- `AGENTS.md`
- `.github/copilot-instructions.md`

`AGENTS.md` and `CLAUDE.md` must be byte-identical. The Copilot file may use
provider-specific framing but must retain the same durable principles.

Do not require instruction files to enumerate every skill. Those inventories
go stale and contradict this repository's instruction-file conventions.
Validate only deliberate skill references in workflow prose: when a named
skill is referenced, its canonical directory must exist. The public catalog in
`README.md` is maintained and validated separately from agent instructions.

### 4. Hook Script Testing

For each skill with a `scripts/` directory:

```bash
# Syntax check
bash -n scripts/*.sh

# Verify bash shebang (either form used in this repo)
head -1 scripts/*.sh | grep -qE "^#!(/bin/bash|/usr/bin/env bash)"

# Verify executable
test -x scripts/*.sh
```

### 5. Plugin Skill Validation (agent-performed — not covered by run-tests.sh)

For skills that exist in both `skills/` and `plugin/skills/`:

| Check | Rule |
|-------|------|
| Plugin frontmatter keys | Only Claude Code-specific keys (`hooks`, `user-invocable`, `argument-hint`) added beyond spec |
| Content alignment | Body content matches or plugin has extracted references |
| Beta markers consistent | If `skills/` copy has `[Beta]`, plugin copy should too |

### 6. Portable Agent Plugins Validation (agent-performed — not covered by run-tests.sh)

After regenerating with `./scripts/sync-plugin.sh`, run:

```bash
python3 scripts/test-sync-plugin.py
uv run --with jsonschema==4.25.1 --with PyYAML==6.0.3 \
  python3 scripts/validate-agent-plugin.py
```

This validates the portable manifest against the vendored official Agent
Plugins 1.0.0 schema, checks curated skill membership, rejects non-portable
frontmatter, verifies canonical bytes and executable modes, and enforces
release-version alignment. Use the Agent Skills reference CLI for an independent
format check of generated `agent-plugin/skills/*`.

## Output Format

```markdown
## Skill Test Results

**Date:** YYYY-MM-DD
**Skills tested:** N
**Passed:** N
**Warnings:** N
**Failed:** N
**Instruction files:** passed|failed

### Failures
- [skill-name]: [check]: [error message]

### Warnings
- [skill-name]: [check]: [warning message]

### Passed
- [list of clean skills]
```

## Running

Invoke manually:
```
/skill-tester
```

Or run the script directly:
```bash
bash skills/skill-tester/scripts/run-tests.sh
```

Coverage note: `run-tests.sh` automates Checks 1-4 (minus the
references-exist portion of Check 2 and provider-specific semantic comparison
in Check 3). Checks 5-6 and those semantic/reference checks are performed by
the agent when `/skill-tester` is invoked -- a green script run alone does not
mean they passed.

## What This Skill Does NOT Do

- Does not test CI skills (use `skill-tester-ci` for those)
- Does not modify skills — reports findings only
- Does not run behavioral evals (trigger testing) — use skill-creator's `run_eval.py` for that
- Does not replace the eval-creator regression framework — this tests skill structure, not promoted rules
