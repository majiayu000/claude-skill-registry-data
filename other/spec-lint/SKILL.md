---
name: spec-lint
description: >-
  Check a repository's specification (`docs/spec/`) against its conventions before a
  specification change merges: trace comments, status markers that cite an existing task,
  decision or issue, lock markers where used, no people or tools named. Reports findings;
  edits nothing.
---

# spec-lint

Read-only. Report each finding as `file:line: problem`; fix nothing unless asked.

1. Every SDD requirement is a `**XX-nn.**` line followed by its
   `<!-- id: SDD-XX-nn | tdd: ... | status: ... -->` comment, and every TDD item is a
   `#### TDD-x.y.z` heading followed by its `<!-- id: ... | implements: ... -->` comment, as the
   conventions at the top of `SDD.md` and `TDD.md` state. `tdd:` and `implements:` cite items that
   exist.
2. Every status is `implemented`, `pending:#N` or `deviation:#N`, and `#N` resolves: in a local
   repository (`repos.conf` posture `local`) to a file in `docs/tasks/` or `docs/tasks/done/`; in a
   GitHub-backed one to an issue (`gh issue view N`). A `pending` item whose task is done, or whose
   issue is closed, is a finding.
3. Where the specification already uses spec-lock markers, every subsection carries one. A
   specification with none is not a finding.
4. No section names a person, agent, model, session or process history.
5. Every `Describes release:` header matches the current tag or candidate.
6. In a local repository, `dev-loop tasks <repo> check` reports ok.
