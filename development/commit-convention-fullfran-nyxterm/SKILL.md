---
name: commit-convention
description: Conventional Commits, work-unit commits, NO Co-Authored-By. Load before creating any commit.
triggers:
  - commit
  - "git commit"
  - "commit message"
---

# Commit convention

## Format

[Conventional Commits](https://www.conventionalcommits.org/). Scope optional but encouraged.

```
<type>(<scope>): <subject in present imperative>

<optional body explaining WHY, not what>

<optional footer with BREAKING CHANGE: ... or Refs #N>
```

## Allowed types

| Type | Use for |
|---|---|
| `feat` | new user-visible capability |
| `fix` | bug fix |
| `chore` | build, deps, tooling, non-functional |
| `docs` | docs only (README, CONTRIBUTING, skills, code comments-only changes) |
| `refactor` | restructure without behavior change |
| `perf` | performance improvement (measured) |
| `test` | tests only |
| `style` | formatting, whitespace, no logic change |
| `ci` | GitHub Actions, CI config |
| `build` | build system, packaging (Nix flake, Cargo.toml, etc.) |
| `revert` | revert a previous commit |

## Examples

```
feat(pty): add SIGWINCH propagation for tmux-less resize
fix(theme): emit theme to webgl renderer after context restore
chore: bump portable-pty to 0.9.1
docs(agents): document OSC 7 trust window
refactor(multiplex): extract pane grid into dedicated module
perf(buffer): coalesce 4ms PTY flushes — 40% fewer IPC calls
test(pty): cover backpressure overflow path
build(nix): switch to pnpm.fetchDeps for frontend deps
ci: add cargo clippy gate
```

## Subject rules

- **Present imperative**: "add", not "added" or "adds". Like you're completing the sentence *"If applied, this commit will ..."*.
- **No period at the end.**
- **≤72 chars** ideally.
- **Lowercase first letter** (after the colon).

## Body (when needed)

- Explain **WHY**, not what. The diff shows what.
- Wrap at 72 chars.
- Reference the issue: `Refs #42` or `Closes #42` in the footer.

## Forbidden

- ❌ `Co-Authored-By: anyone@anywhere`
- ❌ `🤖 Generated with [Claude Code]`
- ❌ Any AI attribution footer

The human owns the commit. The agent assisted. Attribution is via the PR review trail, not the commit message.

## Work-unit commits

One commit = one coherent change. Tests + docs + code of that change go **together**, not in separate commits.

Examples:
- ✅ `feat(pty): add SIGWINCH propagation` includes the implementation, the test, and the relevant docs/skill update.
- ❌ Three commits: "add code", "add test", "update docs". That's three artificial commits for one change.

**Exception**: when a sequence has internal milestones that each compile and pass tests independently, splitting can aid review. Then the boundary is "each commit is a green build", not "files of type X".

## Amend vs new commit

- **Amend** before push, when the previous commit is yours and the change is a typo or trivial fixup.
- **Never amend a published commit** without coordinating. New commits preferred.
- **Never amend after a hook failure** — the commit didn't happen; create a new one.

## Pre-commit hooks

Don't skip with `--no-verify`. If a hook fails, fix the underlying issue (lint, format, test). The hook is there because the team decided it should pass.

If a hook is broken or wrong, fix the hook in a separate PR; don't bypass.
