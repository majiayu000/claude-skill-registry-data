---
name: mathodology-dev-test-release
description: Use when checking skill metadata, references or repository boundaries, or preparing an explicitly requested skills release.
---

# Mathodology Repository Checks

Repository maintenance checks are optional utilities; they do not run during
modeling by default and cannot establish mathematical or editorial quality.

From a repository checkout, run:

```bash
python3 .claude/skills/mathodology-dev-test-release/scripts/validate_repo.py all
```

The standard-library checker covers skill/role metadata, local Markdown links,
known skill references and allowed repository paths. Individual commands are
`metadata`, `links`, `boundary` and `selftest`. It supports a source export without
Git; in a checkout it also inspects tracked paths. It does not enforce document
heading counts, search wording, updater contracts or contest run schemas.

When changing a utility, exercise its actual behavior. The figure demonstration
script and PDF overview utility have self-tests; backup can be verified by
extracting the archive and checking its checksum. Read
[backup and installation guidance](../mathodology-whole-project/SKILL.md).

When changing prompts, review representative user scenarios and inspect generated
figures. Do not add tests that simply restate prompt sentences. Do not report
that a prompt guarantees consistent future model behavior.

## Explicitly requested releases

Release work is repository maintenance, separate from the modeling guidance.
Inspect the current remote branch, recent releases and existing tags. Choose the
next version consistently with that history and describe migration requirements
when removing an old entry point or utility. Do not invent a package manifest,
application build or CI pipeline for this skills pack.

Review the actual changes, run relevant checks and verify retained asset licenses.
Use a focused branch and pull request when that matches repository practice.
Respect branch protections; do not bypass required reviews or checks. Once the
authorized changes are merged, tag that exact commit and publish the requested
release with concise changes, migration notes and truthful validation results.
Never move an existing release tag to a different commit. Verify the published
tag and release point to the intended source. GitHub's source archives are enough
unless the user requests additional artifacts.
