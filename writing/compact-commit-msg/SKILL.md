---
name: compact-commit-msg
description: Use whenever writing a git commit message, including any `git commit` or `git commit -m` invocation. Triggers on creating a commit, committing changes, drafting a commit title or body, even when the commit is a subtask of a larger fix or feature. Apply BEFORE running `git commit`, not after.
license: Apache-2.0
metadata:
  author: Yulong Ming <i@myl7.org>
---

## Template

```
[<type>: ]<title>

[<body>]

[<footers>, e.g.:]
[Fix #1, fix #2]
```

Read previous commit msgs to follow the existing preference.
Default to no any optional parts.

## Style

Commit msgs are for humans (developers) and have strict char limits. The more compact, the better.
At most 72 chars for the title because GitHub truncates there.
Use common abbrevations, e.g., dependency -> dep.

If the title is a single sentence, no period.
Omit articles (a/an/the) if no confusion.
Write proper nouns as-is.

Prefer no body. Only add it when something critical requires explanations.
Note that developers rarely read the body.
Consider proposing splitting the commit before adding a body.

## Special Cases

When updating deps, use `Update deps`.
However, if the ecosystem distinguishes dev deps (e.g., Node, Poetry/uv, Cargo), use `Update dev deps` when only updating dev deps, so that users can confirm shipped/released deps are not updated.
