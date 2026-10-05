---
description: Run the phel-pdo test suite
argument-hint: "[file-path]"
disable-model-invocation: true
allowed-tools: "Bash(composer *), Bash(./vendor/bin/phel *), Bash(vendor/bin/phel *)"
---

# Test

1. No args → `composer test`.
2. File path → `vendor/bin/phel test "$ARGUMENTS"`.
3. Report pass/fail. The Phel runner has no `--filter`; to narrow, copy the focus `deftest` into a scratch file or comment unrelated ones out.
