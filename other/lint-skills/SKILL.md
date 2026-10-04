---
model_tier: medium
name: lint-skills
description: "Use when running the package's skill linter against all skills and rules to validate frontmatter, required sections, and execution metadata."
domain: process
scope:
  write: []
  verification_reason: "the declared command is a read-only linter: grep -c 'writeFileSync|mkdirSync|appendFileSync' src/scripts/skill_linter.ts returns 0. Absence of a write is not something a command can prove."
execution:
  type: assisted
  handler: shell
  timeout_seconds: 120
  allowed_tools: []
  command:
    - ./scripts-run
    - src/scripts/skill_linter
    - "--all"
runtime_requires:
  bins:
    - bash
    - node
  network: []
workspaces:
  - agent-config-maintainer
packs:
  - meta
---

# lint-skills

## When to use

Use this skill when:

- Validating the shape of every skill and rule in `src/`
- Verifying execution metadata (`execution.type`, `handler`, `command`) is well-formed
- Checking locally before opening a PR that CI's skill-lint job will pass
- Investigating a reported linter failure on a specific skill or rule

Do NOT use when:

- Linting only one file — call `./scripts-run src/scripts/skill_linter <path>` directly
- Checking cross-references between files — use `check-refs` instead
- Checking condensation freshness — use `bash scripts/condense.sh --check` instead

## Procedure

### 1. Inspect the environment

Confirm `./scripts-run` is executable and the working directory is the agent-config
repository root — the linter expects to find `src/skills/`
and related directories relative to `cwd`.

### 2. Dispatch via the runtime layer

Invoke the skill through the runtime dispatcher so the `execution:` block in
this skill's frontmatter governs the call:

```bash
./scripts-run src/scripts/runtime_dispatcher run --skill lint-skills
```

The dispatcher resolves the request, the shell handler runs
`./scripts-run src/scripts/skill_linter --all`, captures stdout/stderr, and returns
a typed `ExecutionResult`.

### 3. Verify the result

Check the returned `ExecutionResult`:

- `status: success` and `exit_code: 0` → all skills and rules are clean
- `exit_code: 1` → warnings only — review `stdout` for the listed warnings
- `exit_code: 2` → errors present — fix the flagged files before continuing
- `status: timeout` → the linter exceeded `timeout_seconds` — investigate
- `status: error` → the runner could not launch — check that `./scripts-run`
  is on `PATH` and the repository root is the current working directory

## Output format

1. One-line summary: `success | failure | timeout | error`, exit code,
   duration in milliseconds
2. Count of skills and rules the linter inspected, if known
3. List of files with errors (first 10), each with code and message
4. Next action: fix errors, re-run, or surface the raw `stdout` for review

## Gotchas

- The command uses `--all`, which walks the full tree — expect several seconds
  of runtime on a warm repo; bump `timeout_seconds` if the repo has grown
- Running outside the agent-config repo root will make the linter report zero
  skills, which looks like a pass but is actually a no-op
- Warnings (`exit_code: 1`) do not fail CI by default; do not dismiss them as
  "green" when the task is to get to zero warnings

## Do NOT

- Do NOT invoke `src/scripts/skill_linter.ts` directly when the intent is to test
  the runtime path — use the dispatcher so the handler and result object are
  exercised
- Do NOT raise `timeout_seconds` to hide a genuinely slow linter pass —
  investigate the slowdown first
- Do NOT add shell redirection or pipes to `command` — the handler runs
  `subprocess.run` with `shell=False`; only argv form is supported
