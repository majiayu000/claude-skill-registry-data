---
name: port-audit
description: Finds each rule that a refactor or a rebuild lost, by a static audit of the deleting commits against production. Use before a rewrite replaces production code, or when tests stay green but behaviour is lost.
---

# Port audit

A **port audit** compares a refactor with the production code and lists each rule that the refactor deleted and
did not port. The **reference branch** is the branch that runs in production. The **refactor branch** is the
branch that will replace it. **Drift** is a rule of the reference that the refactor does not have.

The audit is static: it reads git history and code; it runs no test, no bench and no model. Its output is a set
of Markdown files in `<scratch>/audit/`. `<scratch>` is the session scratch folder, outside the repository. The
`shark:patch-fanout` skill takes the patch units from it. The `shark:lead-merge` skill merges the patches, and
`shark:merge-audit` reviews each merge.

```
port-audit ─► UNITS.md ─► patch-fanout (one patch agent per unit) ─► queue.md ─► lead-merge ─► merge-audit
```

Use this skill when one defect after another comes from the same rewrite. One audit finds the set in one pass. A
typical audit: about 6 area groups in parallel, each with a timebox of about 40 minutes.

## Project values

| Section of `AGENTS.md` (or `CLAUDE.md`) | Used for |
| --- | --- |
| `## Docs layout` | The decisions log and the spec: the decisions that remove behaviour on purpose |
| `## Architecture rules` | The source folder and the module areas of the groups |
| `## Owner rules` | Who confirms the production branch |

If a section is missing, ask the user once. Suggest adding it to `AGENTS.md`.

## Outputs

| File | Content | Writer |
| --- | --- | --- |
| `<scratch>/audit/brief.md` | The brief of the auditors (template: `references/auditor-brief.md`) | operator |
| `<scratch>/audit/G<n>.md` | The rows of one area group | one auditor for each group |
| `<scratch>/audit/SUMMARY.md` | Counts, duplicates, the GAP H causes by theme | operator (or one join agent) |
| `<scratch>/audit/UNITS.md` | The patch-unit index (template: `references/units-template.md`) | operator (or one join agent) |

The templates are in `references/` in this skill folder (`${CLAUDE_PLUGIN_ROOT}/skills/port-audit/references/`).

## Step 0: prove the baseline

Do this step before the first audit row. A wrong baseline gives wrong severities for every row.

1. Ask the owner which branch runs in production. Do not assume that it is the default branch.
2. Record the sha of the reference head and of the refactor head.
3. Find the merge base: `git merge-base <refactor> <reference>`.
4. List the commits that only the reference has: `git log --oneline <refactor>..<reference>`.
   These go into the integration branch first (`shark:lead-merge`, first job).
5. List the deleting commits of the refactor (Step 1).
6. For each deleting commit, find out if production has it too:

   ```bash
   bash -c 'for c in <sha1> <sha2> <sha3>; do
     git merge-base --is-ancestor "$c" <reference> && echo "$c in production" || echo "$c refactor only"
   done'
   ```

7. Mark each gap from a commit that production has as **pre-existing**. A pre-existing gap is not a regression of
   the refactor. It is still a gap, but production behaves the same today.

Write the result at the top of `UNITS.md` (the "Pre-existing in prod" paragraph of the template).

## Step 1: list the deleting commits by size

1. List the commits of the range with their deleted lines in the source folder:

   ```bash
   git log --format='@%h %s' --numstat <merge base>..<refactor> -- <source folder> \
     | awk '/^@/{c=substr($0,2); next} NF==3{d[c]+=$2} END{for(k in d) print d[k], k}' | sort -rn
   ```

2. Keep the commits above a size limit (for example more than 150 deleted lines). Record the limit.
3. Check each large commit for pure moves: `git show -M --stat <sha>`. A move or a rename is not a deletion.
4. Read the message of each commit. A message that says "delete … because" can name a decision.

## Step 2: split into area groups

1. Group the deleting commits by area of the code, about 6 groups. Example areas: the API surface, the domain
   rules, background jobs, integrations, the readers of configuration or specs, the evaluation code.
2. Give each commit to exactly one group. A commit that spans areas goes to the group of most of its lines.
3. Write one brief for all groups (`references/auditor-brief.md`). Put the group list and the commits in it.
4. Start one read-only auditor for each group, in parallel. Give a hard timebox, with the automatic grace of
   20 % to finish the item in progress. To get more time, the auditor asks the operator before the grace ends.
5. An auditor can start its own parallel readers. It joins their rows and removes duplicates.

**Rules for the auditors:**

- Read only: `git show <sha>`, `git show <sha>^:<path>`, `git grep`, `git log -S`, file reads.
- Never edit the repository, never check out, never run a test, the bench or a model.
- The only output is one group file, written with the Write tool.
- Note the sha that you audited. A merge can move the refactor head during the audit.
- Quality before coverage. An UNSURE row with evidence is better than a guess.

## Step 3: one row for each deleted rule

For each deleted or heavily rewritten function, method, class or rule, write one row. First make sure that the
logic is not under a new name. Search for its literals, constants, spec keys, setting names and event names.

| Column | Content |
| --- | --- |
| rule | What the behaviour did, for the user or the system, in one line |
| old place | `<sha>^:<path>:<line>` and the function |
| status | PORTED (new `file:line`), GAP, REMOVED ON PURPOSE (decision ID or commit quote), UNSURE |
| evidence | The grep or the `file:line` that proves the status |
| impact | Who sees it: user-facing output, business data, a decision path, bench or evaluation only |
| severity | H: wrong or lost user-facing behaviour or business data; M: degraded; L: bench, evaluation or log only |

The four status classes:

| Status | Meaning | Evidence that it needs |
| --- | --- | --- |
| PORTED | The rule exists in the refactor, maybe under a new name | The new `file:line` |
| GAP | No reader, or no replacement, in the refactor | The grep that finds nothing, or the `file:line` that is wrong |
| REMOVED ON PURPOSE | A decision removed the behaviour | The decision ID in the decisions log, or a quote of the commit message |
| UNSURE | The evidence does not decide | What you searched, and what is still open |

Sort the file: GAP H, GAP M, UNSURE, GAP L, then PORTED and REMOVED ON PURPOSE. One line for each of the last
two kinds is enough. At the top: the counts for each status, the audited sha, and what is not finished at the
timebox.

Mark each GAP H that you read by hand in the code as "checked by hand". All other rows are **inferred** from a
static read. Say so in the row.

## Step 4: the "parsed but no reader" scan

A **dead input** is a spec key, a setting or an event field that the code still parses or writes, but that no
code reads. It is a gap with no error and no failing test.

1. List the keys of the spec or configuration schema, the settings and the event payload fields.
2. For each key, find its writers and its readers with `git grep` on the key name.
3. Write one row for each key with a parser or a writer and no reader. Status GAP, unless a decision removed it.
4. Also list each fact or field that code reads but nothing writes (only tests set it by hand).

## Step 5: join into SUMMARY.md

1. Make a counts table: one row for each group, one column for each status, and a sum row.
2. List the duplicates across groups: one cause that two groups found. Count the unique GAP H causes.
3. Group the GAP H causes by theme (for example delivery, output safety, configuration readers, business data,
   evaluation).
4. Add the notes: facts to confirm with the owner, docs that disagree with the code, the process root cause.

## Step 6: the patch-unit index (UNITS.md)

A **patch unit** is one cause that one patch agent ports in one branch. Make the units from the rows:

1. Make one unit for each cause. Join the duplicate rows of Step 5 into it, and list them as "source rows".
2. Join the rows that change the same function into one unit. List the joined rows.
3. Give the units that change the same file, or the same writer and reader seam, one **conflict group** label.
   The lead merges a conflict group in sequence.
4. Number the units in order of severity: H first, then M, then UNSURE.
5. Fill the columns of `references/units-template.md`: pre-existing in production, bench-only, decisions cited.
6. Put each REMOVED ON PURPOSE row in its own section, with the decision. A possible supersession stays a unit.
7. Leave a section "Added by the operator" for follow-up units from patch reports and merges.

Do not choose a fix in the index. The place to change is the evidence of the auditors. The patch agent verifies
it (`shark:patch-fanout`, step "Verify first").

## Rules

- The production code is the reference. The current code is the candidate.
- A decision that removes behaviour on purpose has an ID in the project's decisions log, or a commit message that
  says so. Without one, the row is a GAP or UNSURE, not REMOVED ON PURPOSE.
- A newer decision supersedes an older one. It does not make the older one "wrong". Cite both, with the date and
  the scope.
- No customer or tenant name in a unit title of a shared rule. Write the behaviour.
- Label each row: "checked by hand" (observed in the code) or inferred (from the static read).

## Report (outcome first, ASD-STE100)

- The audited shas (reference, refactor, merge base), and how Step 0 proved the production branch.
- The counts by status, and the number of unique GAP H causes.
- The number of units and conflict groups; the pre-existing units.
- What the timebox stopped.
- The full paths of `SUMMARY.md` and `UNITS.md`.

## Lessons

- **zsh does not split an unquoted variable into words.** `for c in $list` runs once with the whole list. Run
  loops over sha lists in `bash -c '…'`, or write the list out.
- **An audit is static.** Label each row that you did not read by hand as inferred. Check the H rows by hand.
- **A module deleted as "unreachable" often lost its caller in an earlier commit.** Find the commit that removed
  the caller (`git log -S '<function name>'`). The rule of the module is then a gap, not dead code.
- **Tests were deleted with the code.** No failing test showed the gap. The process root cause: the contract of
  the rewrite listed the new names, but not each deleted rule with its new owner. A contract that deletes code
  lists each deleted rule, its callers and its new owner (see the contract step of `shark:operator`).
- **The summary can assume the wrong production branch.** Step 0 asks the owner and checks with git.
