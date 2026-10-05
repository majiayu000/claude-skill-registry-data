---
name: programming-shell
description: >-
  Guides shell work under the shell standards: checking the declared dialect first, deciding whether logic belongs in
  shell at all, tracing where exit-on-error does not reach, and testing the script as its callers run it.
when_to_use: >-
  Use when writing, changing, or reviewing a shell script, hook, or wrapper, before the first test of the change.
compatibility: Requires a shell script with a declared interpreter and the repository's analyser and formatter.
---

# Shell Programming

[Shell Scripts](../../../repo-governance/development/quality/code/shell-scripts.md) owns script mechanics, and
[Shell Standards](../../../repo-governance/development/quality/stacks/shell-standards.md) owns every shell stack rule.
[Test-Driven Development](../../../repo-governance/development/tdd-policy.md) and
[Test Boundaries and Gates](../../../repo-governance/development/quality-gates.md) govern tests and gates,
[Red, Green, Refactor](../../../repo-governance/workflows/quality/red-green-refactor.md) runs each cycle, and
[Developing Applications](../developing-applications/SKILL.md) carries the judgement that holds in every language. This
skill adds only the procedure and judgement of applying them in shell. Where a sentence here seems to state a rule, the
standards decide.

## Start From the First Line

Read the interpreter line and the strict-mode setting before anything else; they decide which dialect's rules apply. Run
the analyser, the formatter check, and the script's tests on the untouched tree. A gate already failing is handled under
[Preexisting Error Resolution](../../../repo-governance/principles/root-cause-orientation.md). For a dialect the
analyser cannot read, the syntax check passes and you carry the review the analyser would have done.

## Decide Whether It Belongs in Shell

Before adding logic, ask what the addition is. Running commands in order, passing files between them, and stopping on
failure is shell's job. Parsing a structured format beyond a single `jq` query, computing over data, retrying with
backoff, or branching on many cases is logic; once a change adds some, the standard's size rule decides whether the
script moves to a language with a unit layer. Raise it before writing the logic, not after.

## Trace Where Exit-on-Error Does Not Reach

Strict mode stops the script at a failing command only where the shell checks it. Read each change for the places the
standard lists: a function called as a condition, a command on the left of `&&` or `||`, a declaration assigned from a
substitution, and a substitution in a shell that does not inherit the setting. At each one, ask what happens when the
command fails. If the answer is that the script carries on, check the status explicitly.

## Quote, Then Check

Quote each expansion as you write it; an unquoted one splits on spaces and expands wildcards, and the bug appears only
when a path or value contains them. Check each argument before its first use: how many arrived, and whether each has the
shape expected. A test with a space in a path, an empty argument, and a missing one covers most of what goes wrong.

## Test the Script as Its Callers Run It

Each increment's red is a test that runs the script with arguments and an environment, in a temporary directory it owns,
and asserts on the exit status, the output, and the files it leaves. Write the test for each exit path the script
documents, the failure paths first, since those are what strict mode and argument checks exist for. A test that passes
only because a command was missing from the path proves nothing; give the test the tools the script needs, or a stand-in
that records how it was called.

Coverage is not measured for shell, so these behaviour tests carry the evidence.

## Before Handing Off

- The analyser, or the syntax check for an unsupported dialect, and the formatter check pass.
- The executable bit is committed, and the interpreter line and strict mode are unchanged or deliberately changed.
- Every expansion is quoted, and every argument is checked before use.
- Every place exit-on-error does not reach has an explicit status check where failure matters.
- Every documented exit path has a test, and each recorded red failed on an assertion.
