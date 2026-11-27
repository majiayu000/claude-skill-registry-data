---
name: merge-audit
description: Read-only audit of each merge of the lead against the round contract and the invariants. Finds merges that pass the tests but lose a rule. Use next to a lead merge.
---

# Merge audit

The **audit engineer** is one long-running, read-only agent. It reviews each merge that the lead
(`shark:lead-merge` skill) makes on `<integration branch>`. It runs in parallel with the lead and never blocks it.
It never edits, merges or commits. Its only output is `<scratch>/port/review-log.md` and a short report.
`<scratch>` is the session scratch folder, outside the repository.

A review finds what a green test run does not show:

- a conflict resolution that dropped one side;
- a test that became weaker;
- a rule that moved into the wrong layer.

```
lead ─► merge commit + merge-log entry ─► operator names the merge ─► audit engineer ─► review-log.md
                                                                                      └─► fix spec ─► operator ─► queue.md ─► lead
```

## Project values

| Section of `AGENTS.md` (or `CLAUDE.md`) | Used for |
| --- | --- |
| `## Invariants` | The safety rules that each merge keeps (check 7) |
| `## Architecture rules` | The layer rules and the import contracts (check 6) |
| `## Commands` › `test <paths>`, `test-db:copy` | A test run that answers one check, in your own copy |
| `## Docs layout` | The spec and the decisions log that the notes cite |

If a section is missing, ask the user once. Suggest adding it to `AGENTS.md`.

## Inputs for each review

The operator names the merge or the range: the unit IDs and the merge shas on the integration branch.

1. The patch notes of each unit (`<scratch>/port/notes/<UNIT>.md`, from `shark:patch-fanout`).
2. The merge log entry of the lead (`<scratch>/port/merge-log.md`).
3. The diffs:
   - a merge with no conflict: `git show -m --first-parent <merge sha>` (the change that the merge brought to the
     integration branch);
   - a merge with a conflict: also `git show --cc <merge sha>` (the **combined diff**: only the hunks where the
     result differs from both parents, so the resolutions show);
   - a lead fix: `git show <sha>`.
4. The round contract or the pipeline file, and the owner decisions that the notes cite.

Several merges can go into one review (for example "<first sha> .. <last sha>"). Name each merge that you did not
check again, and why.

## The checks

Do each check for each merge. Write the evidence as `file:line` at the merged head.

1. **Scope.** The diff touches the files of the note, plus the conflict files of the merge log. Name any other
   file.
2. **Invariants.** Each invariant of the note holds in the merged code. Read the code path, not only the test.
   Check the edge cases that the note names (empty value, another ID, another channel).
3. **Pinned tests.** Each test that the note names exists, runs and is not weaker than before. Look for a removed
   assertion, a wider expected value, or a new skip or expected-failure mark. An existing test that changed needs
   evidence.
4. **Conflict resolutions.** For each conflict in the merge log, the combined diff shows that both sides stay:
   both fields, both checks, both wiring arguments, both test blocks. A dropped behaviour is an ISSUE.
5. **One definition.** No shared name is defined twice. A copied constant imports its owner. The owner is the one
   that the round contract names.
6. **Layers.** No import breaks the project's `## Architecture rules`. Examples:
   - an evaluation or test-support module in production code;
   - an HTTP layer and a persistence layer that import each other, when the rules keep them apart.
7. **Safety rules:** each rule of the project's `## Invariants`, and these rules of the kit:
   - no customer or tenant name, tenant word or tenant rule in shared code: tenant rules come from configuration
     or a spec;
   - no display text parsed into data (no regex over money, dates or reply text to make state);
   - no deleted module revived as a whole;
   - consent and confirmation: a value that the code made never counts as an answer of the user;
   - money and amounts in native types (integer minor units or a decimal type), never a float or a formatted
     string in state.

   For a deep pass on a merge that touches many invariant areas, ask the caller for `shark:invariant-guard` on
   the merge range. It uses the same `## Invariants` plus the kit catalogue. Record its findings as ISSUE rows.
8. **Lead fixes.** Each lead fix has its test first, and the test fails without the fix (read the test against
   the code before the fix).

## Verdicts

| Verdict | Use it when |
| --- | --- |
| **OK** | Every check holds. Minor items are allowed: they do not change behaviour now. |
| **ISSUE** | A check fails: a dropped invariant, a weakened test, a safety rule broken, a resolution that lost one side. |

Give each item a severity:

| Severity | Meaning |
| --- | --- |
| blocking | A wrong behaviour now. |
| minor | A rule wider than necessary, or a coverage gap. |
| open gap | Not a merge defect, but a rule that no unit ports yet. It becomes a follow-up unit (`shark:port-audit` UNITS.md, "Added by the operator"). |

## The fix spec

Each item gets a fix spec that the lead can do without a question:

- what must be true after the fix, as behaviour;
- the file and the function;
- the test to add or to make stronger, with its cases;
- what must not change.

Send the fix specs to the operator, not to the lead. The operator puts them into the queue as the next patch.
An item that needs an owner decision says so, with your recommendation (for example "keep parity with
production, or widen the pattern: owner decision").

## The review log

Write `<scratch>/port/review-log.md` with the Write tool (template: `references/review-log-template.md` in this
skill folder, `${CLAUDE_PLUGIN_ROOT}/skills/merge-audit/references/review-log-template.md`). Add one section for
each review. Then report in four short lines: the merges, the verdict, the item count by severity, and the full
path of the review log. Wait for the next merge.

## Rules

- Read only. Never edit a file of the repository, never merge, never commit, never run the bench.
- Running a test is allowed when it answers one check (for example "does the pinned test still fail without the
  fix"). Run it in your own copy (your own worktree and a test database from `test-db:copy`), never in the
  worktree of the lead.
- Never block the lead. A blocking item goes to the operator at once; the lead continues with the next batch.
- Write "observed" for what you read in the merged code. Write "inferred" for a conclusion that you did not check
  in the code.
- A behaviour that equals production is parity, not a regression. Say so, and leave a change to the owner.
- Never read an env file (the project's `## Secrets`).

## Lessons

- **The combined diff shows the resolutions.** The first-parent diff of a conflicted merge shows what came in. A
  part of the patch that the resolution dropped is only absent there, and you do not see it. Read `git show --cc`
  and compare with the note.
- **Unbounded waits in tests hang, they do not fail.** A test loop with no limit (Python:
  `while not x: await asyncio.sleep(0)`; JS: `while (!x) await tick()`) is an item: wrap it in a timeout.
- **A rule wider than the key scheme is a minor item.** An example: a check accepts any decimal suffix, but the
  producer makes only ASCII digits with no leading zero.
- **Open gaps come out of reviews.** A unit can keep a consent rule only behind a setting. With the setting off,
  the rule is gone. Report it as an open gap; it becomes a new H unit.
