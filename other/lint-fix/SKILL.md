---
name: lint-fix
description: >
  Detect project linting and validation tools, build an execution
  pipeline, run all tools to zero errors, and fix issues using an
  atomic fix protocol. Auto-detects Makefile targets, package.json
  scripts, Go tools, Python tools, and other common linters. Use
  when fixing linting errors, running validation pipelines, or
  ensuring code quality before committing.
compatibility: >
  Requires at least one linting or validation tool installed.
  Works with any project that has a Makefile, package.json, go.mod,
  pyproject.toml, or language-specific linter configuration.
---
<!-- Copyright 2025-2026 Richard Shade. Licensed under Apache-2.0. -->
<!-- SPDX-License-Identifier: Apache-2.0 -->

# Lint and Validation Pipeline

Detect all linting, formatting, and validation tools in the project,
build an ordered execution pipeline, run everything to zero errors,
and fix issues atomically.

## Step 1: Detect project tools

Scan the project root for configuration files, Makefile targets,
and package manager scripts to identify available tools.

Check in order:

1. **Makefile** — discover targets: lint, test, validate, format,
   gen, build, check, vet
2. **package.json** — discover scripts: lint, test, format,
   prettier, eslint, build, typecheck
3. **go.mod** — check for golangci-lint, gofmt, go vet, go test
4. **pyproject.toml / setup.py** — check for ruff, black, flake8,
   mypy, pytest
5. **.csproj / .sln** — check for dotnet format, build, test
6. **Cargo.toml** — check for cargo clippy, fmt, test
7. **Standalone configs** — .eslintrc*, .prettierrc*, biome.json,
   .golangci.yml, .markdownlint*

For detailed detection commands per ecosystem, see
`references/tool-detection.md`.

If no tools are detected, report to the user and offer to help set
up linting. Do **not** proceed with an empty pipeline.

## Step 2: Check for code generation

If `make gen`, `make generate`, or an equivalent code generation
command is detected, run it **before** any linting.

Generated code can overwrite manual fixes. Always generate first.

```bash
make gen 2>&1
```

If generation fails, stop and fix the generation issue before
proceeding to linting.

## Step 3: Build ordered pipeline

Arrange detected tools in execution order:

1. Generation (make gen, code generators)
2. Formatting (prettier, black, gofmt, rustfmt, dotnet format)
3. Linting (eslint, golangci-lint, ruff, clippy, markdownlint)
4. Type checking (tsc --noEmit, mypy)
5. Validation (make validate, schema checks)
6. Testing (go test, pytest, jest, cargo test, dotnet test)
7. Building (go build, cargo build, dotnet build)

Present the detected pipeline to the user before executing:

```text
Detected validation pipeline:
  1. make gen
  2. gofmt -s -l .
  3. golangci-lint run
  4. markdownlint '**/*.md'
  5. go test ./...
  6. go build ./...

Proceed? (y/n)
```

If the user wants to add, remove, or reorder commands, adjust the
pipeline accordingly.

## Step 4: Execute pipeline

Run each command in order. Stop at the first failure.

```bash
# Run each command, stop on failure
for cmd in "${PIPELINE[@]}"; do
    echo "Running: $cmd"
    eval "$cmd" 2>&1
    if [ $? -ne 0 ]; then
        echo "FAILED: $cmd"
        # Proceed to atomic fix protocol for this command
        break
    fi
    echo "PASSED: $cmd"
done
```

Capture the full output of the failing command — file paths, line
numbers, rule names, and error messages are needed for fixing.

## Step 5: Atomic fix protocol

Fix issues from the failing command one at a time. This prevents
cascade failures where fixing one issue introduces others.

For each issue:

1. Fix exactly ONE issue (minimal change)
2. Re-run the failing command immediately
3. Verify: the issue is resolved AND no new issues appeared
4. If fix created new issues: revert and try a different approach
5. If fix is clean: move to the next issue

After all issues for the failing command are resolved, continue
the pipeline from the next command.

For detailed protocol, rollback strategies, and edge cases, see
`references/fix-protocol.md`.

## Step 6: Final verification

After all commands pass individually, run the full pipeline
end-to-end as a single sequence:

```bash
cmd1 && cmd2 && cmd3 && ... && echo "PASS" || echo "FAIL"
```

All commands must pass in sequence. If any command fails in the
final run, return to Step 5 for that command.

Present the final result:

```text
Validation pipeline: ALL PASSED

  1. make gen           PASS
  2. gofmt -s -l .      PASS
  3. golangci-lint run   PASS
  4. markdownlint        PASS
  5. go test ./...       PASS
  6. go build ./...      PASS

Zero errors across all validation tools.
```

## Common fix patterns

**Formatting issues**: run the formatter with `--write` or `-w` flag
instead of `--check`. Most formatters have an auto-fix mode.

**Import ordering**: most linters have auto-fix for import sorting.
Check for `--fix` flags.

**Trailing whitespace / EOF newlines**: fix with editor settings or
`sed -i 's/[[:space:]]*$//' file`.

**Type errors**: these usually require code changes, not auto-fix.
Read the error carefully and fix the root cause.

**Test failures**: investigate the failure — is it a real bug
introduced by your changes, or a pre-existing flaky test?
