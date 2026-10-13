---
name: ship-fix
description: Fix a bug from root cause through regression proof and local commit. Use for error reports and requested corrections.
---

# Shipping a fix

No fix is complete until its regression test is written, runs, and is green.
This is the repository delivery contract in `AGENTS.md`.

## 1. Before touching code

Read `docs/memory/README.md`, then the one topic for the area you are about to
change. It is the
in-repo record of foot-guns and invariants that have already bitten this
codebase; several "new" bugs are documented recurrences. See the
`project-memory` skill.

## 2. Fix the root cause

Find _why_ the failure is possible, not just where it surfaces. A fix that makes
the symptom disappear while leaving the mechanism intact will regress under a
slightly different trigger.

Ask explicitly: **why was this silent until now?** A bug that produced no log,
no error, no visible failure usually means a swallowed exception or a missing
guard — that silence is itself a second bug worth fixing under the fail-fast
contract in `AGENTS.md`.

Check whether the same mistake exists at sibling call sites. Per
`project-ahk-invariant-incomplete-application` in
`docs/memory/windows-ahk.md`, the recurring pattern here is the ONE missed
sibling site — audit the whole class.

## 3. Write the regression test

It must **fail before the fix and pass after it**. Write and run the targeted
test before editing production code whenever possible. Never stash, reset, or
rewrite an active worktree to manufacture pre-fix evidence. If production code
was already edited, use a recorded pre-fix reproduction or baseline; otherwise
state the evidence gap explicitly and make the regression assertion as direct
as possible.

Put a stable slug in the test name (`(perf-2026-07-21)`,
`(llm-cancel-under-critical)`) so `--only` can replay exactly that case in
seconds instead of the whole suite.

Read the failure message when it goes red. If it fails for a reason other than
the bug — a missing constant, a typo in a symbol name — the test is not yet
encoding the root cause.

Put it in the suite covering the affected layer:

| Layer               | Location                                                                    |
| ------------------- | --------------------------------------------------------------------------- |
| Windows AHK driver  | `static/ergopti_plus/windows/tests/` (`unit/`, `meta/`, `startup/`, `e2e/`) |
| macOS Hammerspoon   | `static/ergopti_plus/macos/tests/`                                          |
| Cross-platform / JS | `tools/test/`                                                               |

**Encode the root cause, and exploit the harness so a regression actually
fails.** Canonical example: the `DYN_HOTSTRINGS_DEFAULT_DELAY` startup crash came
from a menu-build global living in the late-loaded `modules/hotstrings.ahk`
instead of the early `hotstrings_config.ahk`. The guard test asserts the constant
is defined — and works precisely because the AHK suite loads
`hotstrings_config.ahk` but NOT `modules/hotstrings.ahk`, so moving it back makes
the constant undefined and fails the test.

Guard tests should enumerate the **whole class** of call sites, not the single
site the bug was found at.

For tests that scan driver source, see the `meta-test` skill — there are
non-obvious traps and a CI ratchet.

## 4. Run proportional gates

Use the `verify-change` skill after the edit. Its planner selects the checks
that cover the touched paths, including driver tests and the AHK encoding gate
when applicable. Run the selected commands through the project launcher and
record every command, exit code, and intentional skip.

A gate that cannot start is not green. Diagnose missing runtimes or dependencies
separately from assertion failures. Use the full `--all` gate only for a release,
a repository-wide audit, or when the user explicitly requests it; a focused fix
does not automatically justify every platform suite.

## 5. Never weaken a test to make a change pass

If an existing test now fails, the default assumption is that **your change is
wrong**. Only after proving the test encodes a premise the fix deliberately and
correctly changed may you rewrite it — and then you re-encode the invariant at
its new home rather than deleting it. Deleting or loosening a regression test is
never the answer. The suite must grow strictly stronger over time.

## 6. Commit — one fix, one commit, no push

See the `commit-and-push` skill. Never push `dev` or `main` without explicit
authorization in the current conversation.

## 7. Record what was non-obvious

If the bug taught you something that is not derivable from the code or git
history, add an entry to the narrow topic under `docs/memory/` (see
`project-memory`).
