---
name: rfc-board
description: "Use when the RFC board must be read, compared or synced."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos, linux]
metadata:
    hermes:
        tags: [rfc, github-projects, gh, board, publishing]
---

# RFC Board

The project at `<owner>` project 1 is a projection of the record files in
`Documentation/RFC/proposed/`, not a second copy of them. One direction of flow: the record is
authoritative, the issue follows the record, the project item follows the issue. Nothing in this
procedure writes back into a record.

The tool that does the work is `Reference/rfc_board.py`: five subcommands, four of which read the
board and one of which writes it.

---

## When to Use

- A record was added, edited or renumbered, and the board must follow it.
- The board and the corpus disagree about how many records exist.
- A clone needs its own copy of the board, or a copy of the project needs to point at another
  repository.
- Someone asks whether the published board still matches the tree.

Do not sync a record that is not committed. See "What May Be Published".

---

## The Commands

```sh
python3 Documentation/Skill/RFC-Board/Reference/rfc_board.py plan
python3 Documentation/Skill/RFC-Board/Reference/rfc_board.py render
python3 Documentation/Skill/RFC-Board/Reference/rfc_board.py verify
python3 Documentation/Skill/RFC-Board/Reference/rfc_board.py readme
python3 Documentation/Skill/RFC-Board/Reference/rfc_board.py sync --reason "<why>"
```

`plan` is the default, so a bare run is `plan`.

The root scripts are the same calls: `pnpm run RFC:Board` is `plan`,
`pnpm run RFC:Board:Sync --reason "<why>"` is `sync`, and `pnpm run RFC:Board:Verify` is `verify`.
The plain name is the read path on purpose, so running it out of habit writes nothing.

- **`plan`** compares the committed records with the board and reports what it would create, what it
  would update and what already agrees, one line per change. It exits `0` when the board agrees and
  `1` when it does not, and it makes no write call on any path.
- **`render`** writes one issue body per record into the work directory, leak-scans the bodies and
  proves each `## Decision` section survived the round trip byte for byte. It touches nothing
  remote, so it is the safe first look.
- **`verify`** reads the published project independently of the plan and exits non-zero on the first
  disagreement. Its checks are the table at the end of this file.
- **`readme`** reports whether the project's README is the rendered `Reference/project-README.md`.
- **`sync`** is the only writer. It performs what `plan` reports - creates the missing issues,
  updates the drifted bodies, adds the missing items, sets the field values that disagree and
  updates the README - printing one line per mutation. It refuses to run on a board that holds items
  unless `--reason` names why the write is justified; an empty board is the initial sync and needs
  no reason. It never creates a field: a project missing one of the six is refused, because a copied
  project carries its fields and a field created by a guess would carry the wrong data type.

`publish` is gone: it was the old name for a command that wrote without being asked. Running it now
prints one sentence and exits `2`.

The work directory is `Maintain/Storage/RFC-Board/` by default (gitignored, `--work` overrides it).
It holds `records.json` and one rendered body per record; it is a build product and nothing reads it
back as input. `plan` writes the bodies there so the text it reports can be read before `sync` sends
it.

---

## The Board Is Shared, So a Run Reads

The GitHub project is shared state. Anyone with repository permission can edit an item, move it or
change a field, and none of that is in this repository. A local script that rewrote items and fields
on its normal path would discard those edits silently: the next run would look like maintenance and
be a revert.

The split is therefore by direction, not by convenience:

- **Reading is free.** Enumerating issues, reading items, reading field values and rendering bodies
  are inference over state someone else owns. Any command may do it at any time, and a person can
  run `plan` as often as they like.
- **Writing is a ceremony.** Creating an issue, adding a project item, setting a field value or
  uploading the README changes what other people see. It happens only in `sync`, only after the plan
  has been printed, and only once the precondition is met.
- **Boilerplate is the exception, and the only one.** The initial sync - the first items on an empty
  board - has nothing of anyone else's to lose, so it needs no reason. Every write after it does.

The rule is enforced in the code rather than by convention. Every write passes through one seam -
`gh` for the CLI, `graphql` for the API - and that seam refuses a mutating verb or a `mutation`
document unless `sync` has declared itself first. A write added later is refused by default instead
of by review, which is the only kind of guarantee that survives the next edit.

---

## What May Be Published

`git ls-tree -r --name-only <HEAD> -- Documentation/RFC/proposed` is the list, and each record's
text is read with `git show <HEAD>:<path>`. The corpus is one commit's snapshot, not a state: a
record that is staged and never committed is not in the list at all, and a record edited after its
commit publishes the bytes the commit holds. Both are reported rather than left to be guessed, as
`warn <path>: staged but not in <commit>, so it is not published (commit it)` and
`warn <path>: edited since <commit>, so its committed bytes are what publishes`. A record that is
still untracked is somebody's work in progress: it is printed as
`skip <path> (untracked: not committed, so not published)` and it is never published half-written.
The count `verify` asserts is the number of committed records, so a half-finished record cannot make
the board look incomplete.

The consequence is deliberate and worth stating plainly: a record becomes visible on the board one
step after it becomes part of the tree. Commit the record, run `plan` to see the delta, and `sync`
to land it. An unreadable committed record is refused rather than skipped: both commands exit
non-zero and compare nothing, because a corpus that cannot be parsed is a corpus whose board would
be a guess.

---

## The Record Is the Authority

- **The body is assembled, never written.** It carries the `## Decision` section verbatim, the
  `## Verification` table verbatim, the three classification axes, the status, the `depends` entries
  joined with commas, the implementing card ids and a link to the file. It is never a summary, so it
  cannot drift from the record in a way a reader could not detect.
- **A body that differs from its record is reported, and only `sync` rewrites it.** `plan` compares
  the published body with the freshly rendered one and prints one line per body that would change;
  `sync` performs it. Editing a record and re-running the pair is the whole update procedure.
- **The classification is read from the frontmatter, never from a side table.** `category` states
  `Kind` and `Subject` together and `horizon` states the third; `verify` compares every item's three
  values against its record's, so a board that disagrees with the corpus fails rather than reporting
  a second opinion.
- **`Status` moves when the verification table passes against shipped code**, not when a plan
  exists. The value is copied from the record's frontmatter - `settled` is written as `Implemented`,
  and `superseded` is reported and left alone - and the tool never infers it.
- **A record that names no implementing card is design, not debt.** `horizon` (`now`, `next`,
  `later`) states what the Decision presupposes, not who is working on it: `later` means nothing
  here is owed. Sixty records at `later` are sixty decisions waiting for a presupposition, and the
  board carries no due date and no `late` state for exactly that reason. Reading the horizon as a
  backlog turns a settled design into a permanent failure - the measurement the README's "By
  horizon" section reports is a split, not a fault in the axis.
- **The frontmatter is hand-written, and Prettier has the last word on its shape.** Prettier
  reformats a YAML block inside markdown: it wraps a scalar past the print width and turns a
  double-quoted value into a single-quoted one when the text holds a double quote. Write what
  Prettier keeps - a literal block past 100 columns, the quote that needs no escape - so
  `pnpm run Format:Check` is clean without a second pass over the corpus. A hand-edited block that
  misses either still parses, and fails the format check instead: run `pnpm run Format` on the
  record rather than shaping the block by hand.

---

## What the API Cannot Do

A view's group-by is a manual interface step. GitHub's GraphQL schema accepts a view's name, layout,
filter and visible fields, and no input object accepts `groupBy` or `sortBy`:
`CreateProjectV2ViewInput` and `UpdateProjectV2ViewInput` carry only `name`, `layout`, `filter` and
`configuration.visibleFieldIds`. The three views therefore arrive ungrouped from `gh project copy`,
and each is opened once and given its grouping by hand: `Kind` for the table, `Status` for the
board, `Kind` for the roadmap.

Deleting a field is also API-reachable, and it un-groups every view that grouped by it. Retiring
`Class` and `Area` for the three axes therefore costs one interface pass over the two views that
grouped by `Class`, which is the same pass a new project needs. The views are renamed to match in
the same operation; a view whose name promises a grouping it no longer has is worse than an
ungrouped one.

Everything else about the project is API-reachable: the fields, their options, the item set and
every field value.

---

## Nothing Machine-Specific Is Baked In

The project id is resolved from `--owner` and `--project`; the field ids, their data types and their
option ids come from the project's own field list over GraphQL, in one request. The defaults are
`<owner>`, repository `TimeLine`, project `1`, branch `Current`; every one of them is a flag, so the
same tool drives a copy of the project on another owner without an edit:

```sh
python3 Documentation/Skill/RFC-Board/Reference/rfc_board.py plan \
  --owner <owner> --repo <repository> --project <number> --branch <branch>
```

The record-to-axis assignment is in the record, not in the tool: `category` states `Kind` and
`Subject` together and `horizon` states the third, and the definitions plus the tie-break rules are
in `Documentation/RFC/README.md`. The tool reads the three values and refuses a record whose value
is outside the vocabulary, naming the record and the axis rather than publishing a guess.

---

## Pitfalls That Cost a Run

- **A literal em dash does not survive the tool transport.** A U+2014 written into a file or passed
  as an argument arrives as an ASCII hyphen, and every issue title silently loses its separator. The
  separator is built at runtime (`SEP = "\u2014"`), and the project README carries the `@@DASH@@`
  token for the same reason. An issue title is the record id, then the separator, then the record
  title.
- **`gh issue create` has no `--json` in gh 2.102.1.** It prints the issue URL on its last line,
  which is where the issue number comes from.
- **`gh project item-edit` costs one process and one API call per field**, which is 284 calls for 71
  records and times out. Field writes are aliased `updateProjectV2ItemFieldValue` mutations instead,
  four records per request; about twenty aliases is the ceiling before GitHub answers 502.
- **GraphQL input objects take unquoted keys**: `{number: 12}`, not `{"number": 12}`. `json.dumps`
  produces the wrong literal for the object, so the object is written by hand and only its string
  values are escaped.
- **`Status` is the built-in single-select, repurposed.** A second field with that name cannot be
  created, so the built-in one carries `Proposed` and `Implemented`. A project without those options
  fails the run with the option list it found.
- **A plain field's data type decides the literal.** A field that is not a single-select is text or
  a number depending on how it was created: this project's `RFC` holds the zero-padded text `0001`,
  so `{number: 1}` is refused and `{text: "0001"}` is accepted. The tool reads `dataType` from the
  schema and writes the matching shape rather than assuming a number.
- **A count written into prose goes stale.** The project README carries `@@COUNT@@` for the corpus
  size and `@@DASH@@` for the separator; both are resolved at upload, so adding a record cannot
  leave the prose claiming the old total.
- **The leak pattern is assembled from parts.** The archiver that copied this tool into `Reference/`
  scrubs a literal home root on the way in, so a pattern written as one literal would arrive with
  `<home>` where its own first branch should be. `LEAK` is therefore built from string fragments,
  and its `.local` branch excludes a following dot so a repository path such as
  `Maintain/Spacetime/spacetime.local.json` is a path and not a hostname.
- **A field's id changes when its data type does.** `UpdateProjectV2FieldInput` carries a name and,
  for a select field, its options; it has no data type. Moving a field from number to text means
  deleting and recreating it under the same name, which issues a new id and appends the field to the
  end of each view's columns, because `visibleFieldIds` is a set and accepts membership rather than
  order. Resolve every id at run time and a stale id cannot be mistaken for an empty column.
- **A deleted field takes its values and its groupings with it.** `deleteProjectV2Field` is one
  call, and it removes every value written into the field and un-groups each view that grouped by
  it. The grouping is not restorable by any API call, so a retirement needs the assignment committed
  first: `Documentation/Reference/RFC-Classification.md` is the only complete record of what the old
  values were, and the new fields are repopulated from it by hand.
- **`gh project item-list` lowercases only the first letter of a field name**, so a field named
  `RFC` arrives under the key `rFC`. Reading the wrong key looks exactly like a field that is empty
  on every item, which is why `verify` reads its values over GraphQL.
- **`gh issue list` is served by the search API**, which has its own budget of about thirty requests
  a minute shared with every other client of the same token, and a refusal reads like an exhausted
  token rather than an exhausted search allowance. The tool reads issues over REST instead; only
  `gh project item-list`, the count the acceptance names, still goes through the CLI.
- **`gh project item-list` is paginated and capped.** `verify` reads items over GraphQL, and
  `--limit` is a flag because a corpus that outgrows the page size would otherwise be counted short.

---

## Adding a Record

1. Write `Documentation/RFC/proposed/RFC-00NN-<slug>.md` from `TEMPLATE.md`: the frontmatter block,
   a `## Decision` section and a `## Verification` table. The `## Open questions` section is
   optional; everything else the body renders from is required.
2. Choose `category` and `horizon` from the vocabularies in `Documentation/RFC/README.md`, then add
   the record to the audit's assignment table if it is new there. A value outside a vocabulary is
   refused when the tool reads the record.
3. Commit the record. Both `plan` and `sync` read committed records only.
4. Run `plan` to see what it adds, then `sync --reason "<why>"` to write it, then `verify`. A
   non-zero exit from `verify` names the item and the field that disagree.
5. Open the three views once and set each group-by, if the project is new.

---

## Exit Codes

| Exit | Meaning                                                                                        |
| ---- | ---------------------------------------------------------------------------------------------- |
| `0`  | the command did what it reports; `plan` means the board agrees; `verify` passed                |
| `1`  | `plan`: the board disagrees with the records, one line per change                              |
| `1`  | `render`: a leak hit or a mangled Decision section                                             |
| `1`  | `sync`: a leak hit, or any create, refresh, add or field write failed                          |
| `1`  | `verify`: at least one check failed; the failing check is printed as FAIL                      |
| `2`  | the inputs are wrong: no corpus above the tool, no `gh`, `sync` without a reason, or `publish` |

---

## Files

| File                          | What it is                                                                          |
| ----------------------------- | ----------------------------------------------------------------------------------- |
| `SKILL.md`                    | this procedure                                                                      |
| `Reference/rfc_board.py`      | the tool: `plan`, `render`, `verify`, `readme` read; `sync` writes                  |
| `Reference/project-README.md` | the project's own README, ASCII, with `@@DASH@@` and `@@COUNT@@` resolved at upload |
| `Reference/Index.md`          | the archive index for this directory                                                |

---

## Verification

| Claim                             | Test                                                                                                                                                                                                                                                                         |
| --------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| The tool runs from the tree       | `python3 Documentation/Skill/RFC-Board/Reference/rfc_board.py render` exits 0 and prints `decision text intact: N/N`                                                                                                                                                         |
| Only committed records publish    | `plan` prints `warn <path>: staged but not in <commit>`, and the enumeration counts the committed records only                                                                                                                                                               |
| The board count is the corpus     | `python3 .../rfc_board.py verify` prints `committed records: N   board items: N` and exits 0                                                                                                                                                                                 |
| Every item has RFC and every axis | the `[2]` block of `verify` prints `without RFC: 0`, `without Kind: 0`, `without Subject: 0` and `without Horizon: 0`                                                                                                                                                        |
| The board agrees with the files   | the `[2]` block prints `items whose axes disagree with their record: 0`, and the per-axis counts equal the counts the committed frontmatter carries                                                                                                                          |
| A plain run writes nothing        | `grep -n "item-add\|item-edit\|issue create\|issue edit\|issue close" Reference/rfc_board.py` hits only inside `execute`, and `gh`/`graphql` refuse a mutation unless `sync` declared itself                                                                                 |
| The plain name is the read path   | `node -e "console.log(require('./package.json').scripts['RFC:Board'])"` prints a command ending in `plan`, and `pnpm run RFC:Board:Sync` is the only script that names `sync`, so the plain name cannot write, and the plain run exits `0` or `1` on the board and never `2` |
| The plan is what sync performs    | `python3 .../rfc_board.py plan` exits `0` on a board that agrees and `1` on one that does not, and `sync` executes the list `plan_board` returned, not a second computation                                                                                                  |
| A populated board needs a reason  | `python3 .../rfc_board.py sync` on a board holding items exits `2` with one line and no write; an empty board runs as the initial sync                                                                                                                                       |
| The group-by gap is real          | `gh api graphql -f query='query{__type(name:"UpdateProjectV2ViewInput"){inputFields{name}}}'` prints six fields and none is `groupBy` or `sortBy`                                                                                                                            |
| The tool carries no machine path  | `python3 Documentation/Skill/Tool-Archive/Reference/archive_tool.py --audit` prints `clean: no home paths`                                                                                                                                                                   |
| The separator is a real em dash   | `gh api repos/<owner>/TimeLine/issues/6 --jq .title \| od -An -tx1 \| head -1` shows `e2 80 94` between the id and the title                                                                                                                                                 |
