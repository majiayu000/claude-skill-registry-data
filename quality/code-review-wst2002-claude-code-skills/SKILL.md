---
name: code-review
description: Use when asked to review a pull request, a branch, a diff, staged changes or recent commits, check code before merging, or look for bugs in changes — any language.
---

# Code Review

## Overview

Find the defects that would hurt users or the team after merge, prove each with a concrete failing scenario, and keep everything else short. A review with three real bugs is worth more than thirty style notes.

## Method

1. **Get the change.**
   - Branch: `git diff <base>...HEAD` (base = `main` unless told otherwise) and `git log <base>..HEAD --oneline`.
   - Staged: `git diff --cached`. Pull request: `gh pr diff <number>`.
2. **Understand intent** from commit messages, PR description, and tests in the diff.
3. **Read beyond the hunk.** Open each changed function in full and its callers. Most bugs live where the change meets unchanged code.
4. **Hunt with the checklist**, category by category: [checklist.md](checklist.md).
5. **Verify each candidate.** Name the exact input or sequence that breaks it. If you cannot, drop it or mark it as a question.
6. **Report** using the contract below.

## Output contract

First line: a verdict — `Approve`, `Approve with nits`, or `Request changes` — and the count of findings by severity.

Then each finding, most severe first:

```
### [Blocker | Major | Minor] Title
- Location: path/file.ext:line
- What breaks: the concrete input, state or sequence, and the wrong result
- Fix: the change, as a short code snippet when useful
```

Then, optionally, **Nits** as one-line bullets (maximum five). Then **Questions** for things that depend on intent.

If you find no defects, say `No defects found` and list what you checked. Do not invent findings to fill the review.

## Severity

| Level | Meaning |
|---|---|
| Blocker | Data loss, security hole, crash on a common path, breaks existing clients |
| Major | Wrong result in a realistic case, missing error handling, race, leak |
| Minor | Edge case with low impact, confusing code likely to cause future bugs |

## Common mistakes

- Reviewing only the green lines and missing that a caller now passes `null`.
- Burying one real bug under twenty formatting comments. Formatting belongs to linters.
- Flagging intentional behavior as a bug instead of asking.
- Saying "consider adding tests" without naming the case that is untested.
- Approving without reading changed tests: a weakened assertion is a defect.

---

Made by **Wageesha Tripathi** · [LinkedIn](https://www.linkedin.com/in/wst2002/) · [Email](mailto:tripathiwageesha2002@gmail.com) · [More skills](https://github.com/WST2002/claude-code-skills)
