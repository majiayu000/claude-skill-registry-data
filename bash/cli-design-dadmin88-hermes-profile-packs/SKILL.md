---
name: cli-design
description: Design command-line interfaces with task-oriented commands, predictable arguments, composable output, stable exit behavior, safe destructive operations, discoverable help, and script compatibility.
---
# CLI Design

Use when creating or materially changing a CLI consumed by developers, operators, automation, or other tools.

## Procedure
1. Identify primary users and tasks before choosing commands. Design around outcomes people need rather than mirroring internal object/class structure mechanically.
2. Choose command/subcommand, argument, option, stdin/stdout/stderr, and environment/config responsibilities consistently with the existing tool ecosystem.
3. Make defaults safe and common tasks concise. Require explicit intent for destructive, irreversible, remote, or scope-broadening actions and provide preview/dry-run when it materially reduces risk.
4. Define stdout for the requested result and stderr for diagnostics/progress so piping and automation remain reliable. Offer stable machine-readable output when scripts need structured data.
5. Define exit codes/behavior for success, usage error, partial failure, not-found/no-op, and operational failure according to project conventions.
6. Design idempotent or safely repeatable behavior where commands will be used in automation; make uncertain remote outcomes and retries visible.
7. Provide contextual `--help`/usage/examples and actionable errors that name the invalid input, expected form, and recovery path without dumping internal stack traces by default.
8. Handle configuration precedence deliberately and make effective target/context inspectable so users know which environment/repository/account/node a command affects.
9. Preserve backward compatibility for scripted interfaces or provide deprecation/migration when names/output/semantics must change.
10. Test interactive usage, shell quoting/paths, piped/structured output, failure exits, repeated runs, destructive confirmation, and representative supported platforms.

## Decision rules
- Human-readable output may evolve; documented machine-readable output is a contract.
- Do not require interactivity for commands intended for automation.
- A CLI wrapper is useful when it creates a safer or clearer task interface, not when it merely renames another command and hides diagnostics.
- Fleet/node targets should be explicit runtime context when a tool acts remotely, never an invisible machine assumption baked into the Agency profile.

## Quality gate
The CLI is ready when common tasks are obvious, risky actions require clear intent, automation can rely on stable input/output/exit semantics, errors lead to recovery, configuration/target context is inspectable, compatibility is addressed, and representative interactive plus scripted tests pass.