---
name: coding-guidance-bash
description: Bash implementation and review guidance for automation and repository scripts; not for one-off command execution, POSIX `sh`, or release-workflow design where `project-release-maintainer` is primary. Covers safe quoting, explicit failure handling, process ownership, and maintainable shell boundaries.
---

# Bash Coding Guidance

This skill adds portable Bash implementation, refactoring, and review guidance.

## Adjacent Skills

This skill provides portable Bash engineering principles. Compose with:

- **Workflow:** **thinking** (ambiguous decision framing),
  **recursive-thinking** (stress-testing),
  **security** (threat modeling)
- **Domain overlays:** **project-core-dev** (repo-specific completion discovery
  and reporting when needed),
  **project-platform-diagnose** (environment-sensitive diagnosis),
  **project-release-maintainer** (release or packaging workflows that happen to
  use Bash)

## Reference Map

Load references only when the task needs that depth:

- [references/failure-and-cleanup.md](references/failure-and-cleanup.md) for
  strict options, `errexit` edge cases, traps, temporary resources, and explicit
  failure propagation
- [references/process-and-filesystem-safety.md](references/process-and-filesystem-safety.md)
  for command construction, background process ownership, concurrent
  invocation, filename-safe iteration, and cross-platform tool boundaries

## When Not to Lean on This Skill

- non-shell work
- POSIX `sh` portability work where Bash-only features are not allowed
  (adapt the guidance to the repo's POSIX-shell contract instead of importing
  Bash-only defaults)
- large data processing jobs that should realistically move to Python, awk, or
  another language with stronger structure
- broader release, packaging, or publishing workflow design that only happens
  to call Bash; use `project-release-maintainer` first

## Implementation Workflow

1. Read the touched scripts, entrypoints, call sites, and nearby docs before
   editing.
2. Infer the intended contract from current usage text, flags, tests, and
   environment assumptions. Ask only when multiple plausible script behaviors
   would change semantics.
3. Keep the contract narrow: inputs, outputs, exit codes, environment
   dependencies, filesystem effects, and external tool requirements should be
   explicit.
4. Implement with deliberate failure handling, safe quoting, arrays for argv
   construction, functions for meaningful substeps, and cleanup traps for
   temporary state.
5. Add or update shell tests when the repo has them; otherwise add the smallest
   reproducible validation path you can run directly.
6. Run the narrowest relevant formatter, linter, and script tests the repo
   supports.

## Refactoring Workflow

Use this instead of the default implementation workflow when the task is
primarily cleanup or restructuring:

1. Capture current behavior, flags, environment assumptions, platform
   dependencies, and failure modes.
2. Break the refactor into small slices that preserve behavior.
3. Replace copy-pasted command assembly, hidden globals, unsafe loops, and
   tangled control flow one step at a time.
4. Keep tests or runnable validation passing after each slice; add
   characterization coverage first when behavior is unclear.
5. Stop when the script is easier to read, safer to invoke, and easier to
   debug.

## Review Workflow

When reviewing (not implementing), skip the implementation workflow and use this
instead:

1. Read the change in full before commenting.
2. Identify findings, ordered by severity: `Critical` > `Important` >
   `Suggestion`.
3. Prioritize quoting and word-splitting bugs, globbing hazards, accidental
   masking of failing commands, trap and cleanup bugs, unsafe temp-file
   handling, destructive command risks, portability mismatches, environment
   assumptions, and missing tests.
4. State findings with concrete evidence and the likely consequence.

Do not edit scripts or require findings to be fixed unless the user also asks
for remediation.

## Bash Rules

### First tier - causes bugs

- Start executable Bash scripts with `#!/usr/bin/env bash` unless the repo has
  a stricter shebang convention
- Follow the repo's failure-handling convention. Enable `-u`, `pipefail`, `-e`,
  and `-E` only after checking how optional values, conditionals, functions,
  pipelines, subshells, and command substitutions are expected to behave
- Use explicit status checks where `errexit` semantics are ambiguous or failure
  recovery is part of the contract
- Quote expansions by default: `"$var"`, `"${arr[@]}"`, and `"$(cmd)"`
- Use arrays for argument vectors; do not build command lines with string
  concatenation
- Distinguish stdout data from stderr diagnostics so callers can compose the
  script safely
- Check exit statuses deliberately; do not rely on pipelines, subshells, or
  command substitutions without understanding how failures propagate
- Clean up temp files and directories with `trap` when the script allocates
  them
- Treat `$IFS`, globs, current working directory, and environment variables as
  boundary conditions, not stable ambient assumptions

### Second tier - prevents mistakes

- Prefer functions for meaningful units of behavior; keep top-level script flow
  readable
- Use `local` inside functions unless a variable is intentionally shared
- Prefer `[[ ... ]]` for Bash conditionals and `case` for multi-branch string
  matching
- Prefer `printf` over `echo` when escaping, flags, or portability ambiguity
  matter
- Use command substitution `$()` instead of backticks
- Name flags, env vars, and functions for what they do; shell scripts become
  unreadable quickly when names get vague
- Introduce no new ShellCheck findings and explain any necessary scoped
  suppression; distinguish existing unrelated debt from regressions

### Input, output, and contract design

- Provide `--help` or usage text for non-trivial scripts
- Make required env vars, positional args, flags, and side effects explicit
  near the top of the file
- Exit with non-zero status on real failure and reserve zero for success
- Print machine-consumable output in a stable format when other tools are meant
  to parse it
- Avoid silent fallbacks on missing tools or files unless the script is
  explicitly best-effort
- Use stable exit-code meanings when the script is likely to be called by other
  automation

### Style, testing, and tooling

- Prefer long, readable option names for user-facing interfaces when the repo
  does not already prescribe a short-only style
- Keep functions small enough to understand locally; split when one function
  starts owning parsing, validation, execution, and reporting all at once
- Run `shellcheck` and `shfmt` where the repo uses them
- Prefer Bats or the repo's existing shell-test framework for non-trivial
  scripts
- Document required tools and minimum Bash features when the script depends on
  them

## Decision Heuristics

Use these when the right choice is not obvious:

- **Language fit:** if the task needs nested data structures, complex parsing,
  or large in-memory transforms, shell may be the wrong tool.
- **Quoting pressure:** if command construction becomes hard to reason about,
  switch to arrays or redesign the interface before adding more flags.
- **Failure visibility:** if `set -e` behavior is unclear in a construct, make
  the check explicit rather than assuming the shell will fail the right way.
- **Process ownership:** if the script backgrounds work, define who waits,
  cleans up, and reports failures before adding more parallelism.
- **Portability pressure:** if a script relies on GNU-only flags, a Bash 5.x
  feature, or OS-specific tools, document and validate that boundary instead of
  hiding it.
- **Repo conventions:** if the repo has established patterns for shebangs,
  strict mode, shellcheck, shfmt, or helper libraries, follow them unless they
  create a correctness or safety problem.
- **Narrowness vs. quality:** implement the narrowest change that solves the
  problem. When narrowness conflicts with correctness or safety, prefer
  correctness. When it conflicts with style alone, prefer narrowness unless the
  task is explicitly a cleanup.
- **Adjacent issues:** do not modify unrelated issues unless they are required
  for the requested change's correctness or safety; report them separately.
- **Abstraction threshold:** three similar command sequences or repeated flag
  parsing pain is a pattern; before extracting, check whether a function, a
  helper script, or a small move to another language is the simpler move.
- **External-tool boundary:** if a script depends on `jq`, `awk`, `sed`, or
  platform-specific tooling, treat that dependency as part of the user-facing
  contract.

## Validation

For implementation, a change is done when:

- shellcheck or the repo's equivalent linter reports no new findings
- shell formatting is run when the repo has a formatter
- changed `--help`, argument parsing, or top-level script startup paths are
  smoke-tested before deeper functional validation
- existing shell tests pass
- new or changed behavior has test coverage, or the lack of coverage is called
  out with a concrete reason
- non-trivial scripts have a direct smoke path such as `--help` or a minimal
  fixture invocation
- destructive or environment-mutating paths were verified against a safe test
  fixture rather than assumed correct
- portability-sensitive changes were tested on the affected platform or the
  remaining platform risk was called out explicitly

For review, completion means `Critical` and `Important` findings are reported
with concrete evidence, likely consequence, and any validation gap. Unfixed
findings do not make the review incomplete.
