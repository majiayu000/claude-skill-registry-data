---
name: cf-tdd-gate
description: When the user asks to enforce TDD, set up test-first workflow, add test gates, or block code edits without tests — activate this TDD enforcement skill
---

# TDD Gate — Test-First Enforcement

## Concept

TDD Gate is a PreToolUse hook that blocks edits to production code unless a corresponding test file
already exists. It enforces the **Red-Green-Refactor** cycle at the tooling level: Claude cannot
touch implementation files until you have written a failing test first.

The hook intercepts `Edit` and `Write` tool calls, inspects the target file path, and checks
whether a test file exists for that module. If no test is found, the edit is rejected with a
clear message telling you to write the test first.

## How It Works

1. Claude attempts to edit a production source file (e.g., `src/auth/login.ts`)
2. The PreToolUse hook fires and runs `scripts/tdd-gate.sh`
3. The script checks whether a matching test file exists (e.g., `login.test.ts`, `loginTest.ts`)
4. **Test found** -- edit proceeds normally (exit 0)
5. **No test found** -- edit is blocked (exit 2) with a message to write tests first

## Supported Languages

`cs`, `py`, `ts`, `tsx`, `js`, `jsx`, `go`, `rs`, `rb`, `php`, `java`, `kt`, `swift`, `dart`

## What Gets Skipped

- **Test files themselves**: `*Test.*`, `*.test.*`, `*_test.*`, `test_*`
- **Test directories**: `*/test/*`, `*/tests/*`, `*/__tests__/*`
- **Config files**: `*.json`, `*.yaml`, `*.yml`, `*.toml`, `*.xml`, `*.config.*`
- **Migrations**: `**/migrations/**`, `**/migrate/**`
- **DTOs / models**: `*.dto.*`, `*.model.*`, `*.entity.*`
- **Infrastructure**: `Dockerfile`, `docker-compose.*`, `*.tf`, `*.hcl`, `Makefile`

## Installation

Add the following hook to your `.claude/settings.json` (project-level) or
`~/.claude/settings.json` (global):

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "bash /path/to/skills/skills/tdd-gate/scripts/tdd-gate.sh",
            "statusMessage": "TDD Gate: checking for test coverage..."
          }
        ]
      }
    ]
  }
}
```

Replace `/path/to/` with the actual absolute path to this repo on your machine.

## Script Reference

The enforcement logic lives in `scripts/tdd-gate.sh`. It reads tool input from stdin as JSON,
extracts the `file_path`, and performs a multi-strategy test file search:

1. **Same directory** -- looks for `<name>.test.<ext>`, `<name>_test.<ext>`, `<name>Test.<ext>`,
   `test_<name>.<ext>` alongside the file
2. **Nearby test directories** -- checks `../test/`, `../tests/`, `../__tests__/` relative to the file
3. **Project-wide search** -- uses `find` with `maxdepth 6` from the git root to locate any matching
   test file anywhere in the project

## Customizing Strictness

- To make the gate a **warning** instead of a blocker, change the script's exit code from `2` to `0`
  on the "no test found" path
- To add more file extensions, edit the `PROD_EXTENSIONS` regex in `tdd-gate.sh`
- To exclude additional directories (e.g., `generated/`, `proto/`), add them to the skip patterns

## Gotchas

- **Monorepos**: The project-wide search uses `git rev-parse --show-toplevel` as root. In monorepos
  with deeply nested packages, the search may be slow. Increase or decrease `maxdepth` as needed.
- **Non-standard test naming**: If your project uses `spec` files (`*.spec.ts`) instead of `test`,
  you need to add those patterns to the script's search. The default covers `test`, `Test`, `_test`,
  and `test_` but not `spec`.
- **Generated code**: Files in `generated/`, `proto/`, or codegen output directories should be added
  to the skip list -- you don't write tests for generated code.
- **First file in a new module**: When bootstrapping a brand new module, the gate will block you
  immediately. Write a minimal test file first (even just an empty test suite), then proceed.
- **CI environments**: This hook runs in Claude Code sessions only. It does not replace your CI test
  requirements -- keep your existing test gates in CI/CD.
- **Exit code semantics**: Exit 0 = allow, exit 2 = block. Exit 1 means the hook itself errored,
  which Claude treats differently from a deliberate block.

## Pairing With Other Skills

- Use `/cf-plan-gate` alongside TDD Gate for full spec-driven + test-first enforcement
- Use `dr-dev:test-writer` to quickly generate test stubs that satisfy the gate
- Use `dr-review:code` after implementation to verify the tests are meaningful, not just stubs
