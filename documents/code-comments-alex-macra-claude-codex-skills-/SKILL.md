---
name: code-comments
description: "When and how to write code comments: the default is none, since code and tests carry the meaning and only the non-obvious WHY earns one. Use when adding or removing comments, writing docstrings, JSDoc, or TSDoc, deciding whether code needs documenting, or reviewing a comment-heavy diff."
license: MIT
metadata:
  display-name: "Code Comments"
  version: "1.1"
  platforms: "claude-code codex"
  tags: "comments documentation style"
---

# Code comments

The default number of comments is zero. A comment is a liability: it isn't type-checked, isn't tested, and rots the moment the code beside it changes. Earn each one.

Let the code and the tests speak. A well-named function, a clear test name, and a small function body explain *what* far better than prose ever will. If you reach for a comment to explain what code does, fix the code instead - rename the variable, extract the function, split the branch.

## The only good reason to comment: non-obvious WHY

Write a comment when a reader who understands the language and the codebase would still be surprised - and the surprise lives outside the code itself:

- A **hidden constraint**: "the upstream API caps page size at 100, larger values 400."
- A **subtle invariant**: "callers must hold the lock; we mutate shared state here."
- A **workaround** for a specific, named bug: "round-trip through string - `structuredClone` drops Dates in node <20."
- **Surprising behavior** that looks like a mistake but isn't: "yes, `<=` - the boundary row is inclusive per the spec."

The test: if removing the comment would let a competent reader introduce a bug, keep it. Otherwise delete it.

## Never write these

- **Restatement of the code.** `// increment i` over `i++`. `// loop over users` over `for (const u of users)`. The code already says this.
- **Task / ticket / PR references.** No `// JIRA-1234`, `// added for the onboarding flow`, `// see PR #87`, `// fix from issue 42`. That history belongs in the commit message and the tracker - in the source it is noise that rots.
- **Caller / provenance notes.** No `// used by Dashboard`, `// called from the worker`. Greppable, and wrong the day someone adds a second caller.
- **Verbose preambles.** No multi-paragraph file headers or function essays describing what the following block does. One short line, or nothing.
- **Narration of a change.** No `// removed old logic`, `// changed to use map`, `// new in v2`. Diffs and history record change; comments shouldn't.
- **Commented-out code.** Delete it. Version control remembers.
- **Decorative banners.** No `// ======== SECTION ========`. If a file needs section dividers, it's two files.

## Form, when a comment is warranted

- One line. If the WHY needs a paragraph, the design is probably the thing to fix, or it belongs in a doc/ADR, not inline.
- Phrase it as the reason, not the mechanism: `// avoid N+1 - batch the lookups` not `// build a map of id to row`.
- Put it directly above the surprising line, not floating at the top of the function.
- A `TODO` needs an owner or a condition to be actionable: `// TODO(when we drop node 18): use structuredClone`. A bare `// TODO` is a wish, not a task - delete or finish it.

## Docstrings / public API

Public, exported, or library APIs consumed across a boundary can carry a doc comment - but only the part the signature can't state: units, ranges, side effects, what throws, ownership of returned resources. Don't restate the parameter names and types the signature already declares.

## Reviewing comments

Treat a comment-heavy diff as a smell, not a courtesy. For each added comment ask: does this capture a WHY the code can't, or is it restating, dating, or narrating? If the latter, the fix is to delete the comment (and often to improve the code it sat on). Flag it the same way you'd flag a bad name.

## Optional staged-change check

Use `scripts/comment_check.py` from this skill when asked to audit comments in a git diff or before committing. It scans staged source changes for low-value comments: ticket/PR references, provenance notes, change narration, and verbose comment blocks. It is advisory by default; set `COMMENT_CHECK_STRICT=1` only when the user wants it to block.
