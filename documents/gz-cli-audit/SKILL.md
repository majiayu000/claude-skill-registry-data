---
name: gz-cli-audit
description: Use to verify every CLI command has its manpage, headings and index entry.
category: code-quality
lifecycle_state: active
owner: gzkit-governance
last_reviewed: 2026-10-17
metadata:
  skill-version: "0.2.1"
model: haiku
---

# gz cli audit

## Overview

Check that every CLI command's documentation exists and agrees with the parser.
`gz cli audit` reads the command roster in `config/doc-coverage.json` and checks:

- each command with a manpage surface has `docs/user/manpages/<slug>.md`, whose
  first line is `# gz <command>` and which `docs/user/manpages/index.md` links;
- every `gz` command in the README `## Quick Start` block parses against the
  live CLI;
- cross-coverage: each command discovered from the parser source has a manpage,
  an index entry, a reference in the operator runbook and in the governance
  runbook, and a handler docstring, unless the manifest sets that surface to
  `false`; a deprecated verb must instead be absent from both runbooks; a
  manpage with no matching command is an orphan;
- each long flag is named in its manpage, and the manpage's usage block does
  not bracket a required flag as optional or show a valueless flag taking a
  value.

It is read-only. It exits 0 with `CLI audit passed.` and exits 1 when it lists
any issue. In an adopter project with no `config/doc-coverage.json` it skips
with exit 0; in gzkit's own tree a missing manifest is an issue. `gz check` runs
it as the `CLI audit` step.

## Workflow

1. Run `uv run gz cli audit`, or add `--json` for `{valid, issues,
   cross_coverage}`.
2. On exit 1, fix each named surface: write or retitle the manpage, add its
   index link, reference the command in the runbook the issue names, add the
   handler docstring, correct the Quick Start line, or make the usage block
   match the parser. Remove an orphaned manpage only when its command is gone.
3. Re-run until it exits 0, then summarize what changed.

## Example

```bash
uv run gz cli audit
uv run gz cli audit --json
```
