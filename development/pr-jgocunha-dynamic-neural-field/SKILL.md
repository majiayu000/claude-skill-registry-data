---
name: pr
description: Read the branch diff in dynamic-neural-field-composer and print a PR title and description in chat, filling the repo's pull request template. Use when asked to write, draft or suggest a PR title/description, or "what should the PR say".
---

# PR

Reads the branch against `origin/main` and prints a PR title and body to chat. **Never runs
`gh pr create` or `git push`** - opening the PR stays a human decision.

## 1. Read the branch

```bash
git branch --show-current
git log origin/main..HEAD --oneline
git diff origin/main...HEAD --stat
```

If the branch is `main`, or there are no commits ahead of `origin/main`, say so and stop.

## 2. Title

Same conventional format as a commit - `<type>: <lowercase summary>`. If the branch's
commits share one type, use it; if they are mixed, pick the dominant concern rather than
concatenating types.

## 3. Body - fill the existing template

Use `.github/pull_request_template.md` verbatim as the shape. Do not invent a different
body structure.

```markdown
## What and why

<2-4 bullets or a short paragraph - what changed, why>

## How to verify

<concrete steps - commands, a named test filter, the `build-and-test` skill>

## Checklist

- [ ] Tests added or updated
- [ ] Doxygen updated (if public API changed)
- [ ] Wiki updated (if user-visible behaviour changed)
- [ ] CI passes (Windows, Linux, macOS)
```

Tick a checklist box only if it was actually verified this session. Leave the rest
unticked - do not tick optimistically.

## 4. Issue number

Look for it in the branch slug or the commit messages. If found, close the body with
`Closes #<N>`. **If not found, do not guess a number** - emit the literal placeholder
`Closes #<N>` and say in your reply that no issue number was found.

## Output

A markdown title line, kept outside the fence since `gh pr create` takes `--title` and
`--body` as separate arguments, followed by the filled body inside its own single fenced
code block (` ```markdown `) so the body renders as literal, copy-pasteable text rather
than being rendered as chat formatting - ready to paste into `gh pr create --body`.
Nothing else - no push, no `gh pr create`.
