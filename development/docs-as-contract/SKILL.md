---
name: docs-as-contract
description: Treat READMEs, docstrings, help text, comments, examples, and changelogs as promises that must match the code that ships — sweep them when behaviour changes, write comments for why not what, run every documented command once, never document intent as fact. Use when a change alters behaviour, an interface, a default, or a setup step; when asked to "add docs" or "document this"; when writing comments or docstrings; and when reviewing a diff that changes user-visible behaviour without touching docs.
---

# docs-as-contract

Weak documentation is written from the plan, not the code: a README describing the feature you meant to build, a comment restating the line below it, a setup section nobody has run since it was typed. Strong documentation is a contract with the reader: every sentence describes what the code does today, every command was run, and a behaviour change updates the docs in the same diff.

## 1. Sweep the docs when behaviour changes

Before done on any change to behaviour, an interface, a default, or a setup step, grep the repo for the old behaviour — the old flag, default value, function name, error text, file path — across `README*`, `docs/`, `CHANGELOG*`, docstrings, `--help` strings, OpenAPI or JSON schema, `.env.example`, code comments, and example snippets. Record the command and the hit count (see surgical-refactoring). Every hit is updated in this diff or listed in the report as deliberately left. Docs that contradict the code are worse than none: the reader trusts them.

## 2. Comments say why, not what

- Delete a comment that restates the code (`// increment counter`, `# open the file`). Write one for what the code cannot say: the constraint, the non-obvious reason, the bug being worked around (with the link), the invariant the next editor must keep.
- Never narrate the change inside the code: `// added null check`, `// changed from X to Y`. That is the commit message; in the file it is stale the moment anyone touches the line again.
- No commented-out code. Git remembers.
- A `TODO` carries an owner or ticket and what would unblock it. A bare `TODO` is a comment nobody will act on.
- Match the repo's docstring convention — grep three neighbouring functions for style, sections, and whether params are documented — instead of importing your own.

## 3. Document what runs, in the order it runs

- Every command in a README or runbook is copy-pasteable from a fresh clone: exact command, working directory, expected output or side effect, prerequisites stated before the first command that needs them.
- Run each documented command once from a fresh shell before shipping it. A setup section you have not executed is a guess. A step that cannot be run here (needs production credentials) is marked unverified in the doc and named in the report.
- Examples are code. A snippet that would not compile or a curl that would return 400 is a bug. Prefer examples the test suite executes (doctests, example tests) so they cannot rot silently.

## 4. Describe the current state, not the roadmap

Docs state what exists. Planned behaviour goes under a heading that says so ("Not yet supported", "Planned") or in the tracker, never in the same voice as shipped features. Version- or platform-specific behaviour names the version or platform.

## 5. Know when not to write

Do not add docs nobody asked for: a docstring on every private helper, a `docs/` tree for a 200-line script, a changelog format the repo does not use. Follow the repo's existing density. "Stop adding docstrings" holds for the rest of the session (see generalize-the-correction).

## 6. Write the changelog for the upgrader

If the repo keeps one, add the entry under the unreleased section in its existing format, written for the consumer: what changed for them and what they must do. "Refactored config loading" tells an upgrader nothing; "`TIMEOUT` is now `TIMEOUT_MS`; the old name is still read with a warning until v3" does.

## Reporting

List the docs updated (path, what changed), the grep for the old behaviour with its hit count, and which documented commands you ran. A doc left knowingly stale is a named item, not an omission.
