---
name: decision-report
description: Investigate an architectural question against this repo and write the answer up as a decision report under docs/decisions/. Use on "do a spike on this", "spike this", "write a decision report" or "add a decision report". Only when the user asks; never on your own judgement. Filing a GitHub spike issue is the `github-issue` skill, not this one.
---

# Writing a decision report

A spike is a question that has to get answered before work can start. The question may live in a
GitHub issue or may have come straight out of a conversation; either way the answer belongs in
`docs/decisions/`, because an issue thread is unsearchable outside `gh` and gone from context the
moment it closes.

**"Do a spike" means research plus a file.** It does not mean filing an issue — that's the
`github-issue` skill, and the user will say so ("open a spike issue") when that's what they want.
It also doesn't mean answering in chat: the response is the file, and a summary in the terminal is
a courtesy on top of it, not a substitute.

## 1. Answer the question first

Usually nobody has done the investigation — do it now, against the actual repo, before writing a
line of the report. Two failure modes to avoid:

- **Don't argue from what a repo like this usually does.** Every claim in the report has to come
  from a file you read. `grep` for the thing you're about to assert is undocumented; check the
  boundary table before saying a new project fits somewhere; read the hook before describing what
  it enforces. A report full of plausible generalities is worse than no report, because the next
  person trusts it.
- **Don't stop at the framing you were handed.** The useful result is often that the question
  was the wrong shape — a content problem that's really a navigation problem, a build decision
  that's really a boundary decision. Say so, then answer the question that's actually load-bearing.

If a spike issue exists, read it for the framing rather than re-deriving it — its
`Decision needed` / `Question` fields (see the `github-issue` skill) become the report's Context:

```sh
gh issue view <n>
```

Ask the user only for what the repo can't tell you: a preference between two options that are
genuinely equivalent on the evidence, or a constraint that exists only in their head.

## 2. Decide whether it earns a file

One question or one spike ticket gets one report, however many blocks or sub-questions it covers.
Before writing, strike every part whose answer was already given: by the user, by the issue, or by
an existing precedent copied unchanged. Each of those is one line in the report. If nothing is left
that was really open, or that a later ticket builds on, write no report and put the answer in the PR.
[`docs/decisions/README.md`](../../../docs/decisions/README.md) has the rule.

## 3. Write the file

Copy [`docs/decisions/TEMPLATE.md`](../../../docs/decisions/TEMPLATE.md) to
`docs/decisions/<NNNN>-<slug>.md` and fill in its frontmatter and its five sections —
[`docs/decisions/README.md`](../../../docs/decisions/README.md) says what each is for.
`status` is almost always `to-implement` on the day the report is written: the report records that
a decision was made, not that the work is done. Set it to `implemented` only if the change it calls
for is already in the same PR, and to `wont-implement` only when the finding itself is a decision
not to act. `decision` is `accepted` unless this report is reversing an earlier one — see
[docs/decisions/README.md](../../../docs/decisions/README.md#superseding-a-decision) for what changes on
the report being superseded.

**`NNNN` is the next free number, not the issue's** — `ls docs/decisions/` and add one to the highest,
zero-padded to four digits. Two reports may never share it; `nx collect @joinery/developer-portal`
reports a collision as a `decision-shape-mismatch` on the portal's Overview, but nothing blocks it.

`issue` is the issue that **raised the question**, as a plain integer. It is not always labelled
`spike` — an enhancement issue whose thread turned out to hide a decision is the issue that raised
it. Two reports may share an `issue` when one issue raised two questions. If nothing filed it at
all, say so and ask whether to file one rather than inventing a number.

Two things the template's shape enforces that are easy to lose:

- **Result states what was found, not what is recommended.** "Three layered checks are adopted" —
  not "we should consider adopting". If the finding is that the question needs splitting, that's
  the result.
- **Options considered is a table of losers.** One row per option that was really on the table,
  with the specific reason it lost. An option nobody would have picked is padding.
- **Confirmation names a check, not a hope.** A command, a test or a file whose presence or absence
  would prove the claim — not "this should work". Write it even when `status` is `to-implement`:
  describe how compliance *will* be verified once the work lands, the way the rest of the report
  already describes what was found rather than what's wished for.

Keep it as tight as the shortest sections in the `ui`/`content` package READMEs: this is a record
of an outcome, not a design doc arguing for it. Follow `house-docs` like any other markdown here.

- **Result stays under about 60 lines.** Past that it is a design doc; split the question or move
  the measurements into a table.
- **No process narration.** What was tried in which order, what got built and reverted in the
  session, and who asked what belong in the PR. The report states what is true, and a reverted
  attempt appears only as a row in Options considered.

## 4. Make it executable while `status` is `to-implement`

**A report whose work hasn't landed is read next by whoever does the work, and that is usually
another agent with none of your session.** Everything it needs has to be on the page, because the
investigation that produced it is gone. A report that reads well and leaves the implementer to
re-derive which files to open has failed at its only remaining job.

[`0018-developer-portal-duplicated-facts.md`](../../../docs/decisions/0018-developer-portal-duplicated-facts.md)
is the calibration. Four obligations, all inside the five sections — no new section:

| Obligation | Where it goes |
| --- | --- |
| Every change names its **file path, and its line when one exists** — `app/pages/projects.vue:35`, not "the projects page" | Result |
| A set of independent changes is a **table whose last column is the change**, one row per change, so the reader never counts them out of prose | Result |
| **The order**, when one change makes another cheaper or safer — and the reason, since an order without one gets reshuffled | Consequences |
| **Tripwires an implementer will hit** — a hook that blocks the edit, a pre-existing failure that isn't theirs, a neighbouring change explicitly out of scope | Consequences |

Line numbers go stale, so say what they're as of (`Line numbers are as of this report.`) and keep
the path and the symbol name beside them — those survive, and together they're enough to find the
line again after it moves.

Confirmation earns a `| Claim | Check |` table once there is more than one claim: a runnable command
per row, so the implementer can work down it instead of parsing a paragraph into a checklist. A
single-claim report keeps the sentence.

None of this loosens §3's brevity, because the detail **replaces** the discussion rather than
stacking on it: `0018` carries twelve file:line anchors, a seven-row change table, an order and a
ten-row Confirmation table in 1,854 words, against a corpus median near 1,500. A path and a line are
shorter than the paragraph that gestures at the same file.

Reports whose `status` is `implemented` or `wont-implement` owe none of this — nobody picks them up,
and they're a record of what was found. The obligation is the handoff, not the prose style.

## 5. Close the loop

**When the follow-up work lands (or is dropped), flip the `status:` field in the same PR.** That's
one of the two frontmatter fields expected to change after the fact — it's how
[the developer portal](../../../apps/developer-portal/README.md) shows, at a glance, which decisions are still owed
work. If this report reverses an earlier one, also set that earlier report's `decision:` to
`superseded` and its `supersededBy:` to this file — see
[docs/decisions/README.md](../../../docs/decisions/README.md#superseding-a-decision).

**Never comment on the issue.** The report is reachable without one: its filename carries the issue
number, and the PR that lands it references the issue. An issue comment adds a notification and a
second copy of the answer that can drift from the file.

Closing is outward-facing, so show the user before running it, and only once they confirm the
decision is fully resolved — a decision report can exist for a spike whose issue stays open for
follow-up work. Usually the PR closes the issue anyway, which makes this unnecessary:

```sh
gh issue close <n>
```
