---
name: forget-and-rederive
description: Set up a practice run by removing information the researcher already has from the project tree, so it must be re-derived from records. Use when the researcher says "forget what you know about X and find it again", "hide his parents and see if you can find them", "I want to test whether you can work this out", "re-derive this from scratch", or seeds a project from a well-documented FamilySearch person specifically to check whether the agent can rediscover a known answer. Do NOT use to correct a wrong fact (use tree_correct), to remove a duplicate person (use merge_tree_persons), or to start a project (use init-project).
allowed-tools:
  - project_context
  - tree_forget
---

**Narration:** read `researcher_profile.narration_guidance` in `research.json` and
apply it as the narration style for this invocation.

# Forget and re-derive

The researcher wants to know whether you can actually *do* the research, not
whether you can read an answer off a tree that already contains it. This skill
removes a chosen slice of the local tree so the question becomes genuine.

## Prerequisite

`tree_forget` is required. **Do not substitute `tree_edit`** under any
circumstance — `tree_edit` cannot cascade removals, cannot write the restore
file, and is the mechanism `tree_forget` replaced. Using it here causes the
data damage this skill exists to prevent.

If `tree_forget` is unavailable or fails, stop immediately and tell the
researcher why, based on the failure mode:

**If the tool is absent** (ToolSearch returns no match, or a call errors with
"unknown tool"):

> The `tree_forget` tool is not available in your current MCP server.
> Rebuild and reinstall the extension from a current repo pull, then retry.

**If the error names the project's plan,** relay it and stop — see "When this
skill applies" below. No selector avoids it and clearing entries will not help.

**If the tool returns `{ok: false}` for any other reason** (most commonly
validation errors in `research.json`):

> `tree_forget` failed with the following error:
>
> [Quote the exact error from the tool response]
>
> This is often caused by `research.json` entries (assertions,
> person-evidence, timeline) that reference a person you are trying to
> remove. Review the error, clear the blocking entries if needed, or
> choose a narrower slice (fact-level selectors like `birth-of` or
> `death-of` instead of `person`).

## When this skill applies

This is a **project-start** exercise. `tree_forget` refuses the call once
`research.json` holds any plan — the project has moved past setup. If the
researcher asks to forget mid-project, tell them to start a new project seeded
from the same FamilySearch person.

## The two halves — both are required

Stripping the local tree is only half the mechanism.

1. **Remove it locally** — the `tree_forget` tool, below.
2. **Do not look it up again.** Live FamilySearch *still has the answer*. If you
   call `person_read`, `person_search`, `person_ancestors`, or the person-match
   tools on the affected people, you will read straight back what was just
   removed and the exercise is worthless.

**For the rest of this project, treat the forgotten information as unknown.**
Recover it the way you would for a real brick wall: search records, read them,
weigh the evidence. If you catch yourself about to fetch the tree entry for a
person whose details were forgotten, stop — that is the one move this exercise
forbids.

Reading records *about* those people is not only allowed, it is the point. The
prohibition is on reading the FamilySearch **tree** for the forgotten facts.

## Steps

### 1. Find out what to forget

Ask the researcher what they want you to re-derive, in their words — "his
parents", "her death date", "who she married".

Map that to the tree's own ids with `project_context({ projectPath })`, which
returns each tree person's `id` and preferred name. That is all you need: the
selectors below take ids, and `tree_forget` walks the relationships itself to
resolve parents, children and spouses.

**Do not read `tree.gedcomx.json`.** You do not need the names and dates you are
about to remove, and you are better off not having them in context. For the same
reason, use the year (or year range) the researcher gave you and stop. A single
call packing more than one threshold onto the same date selector is rejected by
the tool itself, but nothing stops you from making that same mistake across
**separate** calls — do not repeat a date selector with a different year to see
what the counts do. That reads a date off the tree as surely as opening the
file.

**The canonical setup is build-full-then-forget.** When a project is seeded
specifically to test re-derivation, `init-project` builds the *complete* tree
first — every person, relationship, and documentary fact — and this skill then
strips the slice under test. A test is **never** set up by hand-omitting
information at construction time: a hand-built partial tree drops the
relationship but keeps the documentary fact that carries the same conclusion (a
`Parents` or `Marriage` fact), leaking the answer, and it has no restore file.
`tree_forget` removes both the structure and the fact, and is the only mechanism
that does.

If the researcher hasn't seeded a project yet, run `@plugin:init-project` first
(which builds the full tree), passing the researcher's own words verbatim, plus
`projectPath`, and nothing else. This skill edits an existing tree; it does not create one.

### 2. Always dry-run first

```
tree_forget({ projectPath, forget: [ … ], dryRun: true })
```

Each entry in `forget` is `{ selector, … }`:

| Selector | Fields | Removes |
|---|---|---|
| `parents-of` | `personId` | the person's parents, the links to them, and the person's own `Parents` documentary facts |
| `children-of` | `personId` | the person's children, and the links to them |
| `spouses-of` | `personId` | the person's spouses, the couple relationships, and the person's own couple-event facts (`Marriage`, `Divorce`, `Annulment`, `Engagement`, `MarriageBanns`, `Separation`) |
| `birth-of` | `personId` | that person's birth facts |
| `death-of` | `personId` | that person's death facts |
| `facts-of` | `personId`, `factType` | that person's facts of one type (e.g. `Marriage`) |
| `facts-before` | `year`, optional `personId` | facts confidently before `year`; tree-wide without `personId` |
| `facts-after` | `year`, optional `personId` | facts confidently after `year`; tree-wide without `personId` |
| `facts-between` | `fromYear`, `toYear`, optional `personId` | facts confidently within the range; tree-wide without `personId` |
| `person` | `personId` | one person, cascading their relationships |
| `fact` | `factId`, optional `personId` | one specific fact; add `personId` if the tool reports the id exists on more than one owner |
| `relationship` | `relationshipId` | one specific relationship |

**Show the researcher the dry-run counts and get their agreement before
writing.** This matters more than it looks: removing a *person* also removes
every relationship touching them. Forgetting a father can therefore also cut the
subject's siblings, that father's own parents, and his marriage — the dry run
reports these as `relationshipsCascaded`, and a surprised researcher is why you
check first. If the cascade is wider than they want, prefer fact-level selectors
(`birth-of`, `death-of`, `facts-of`) which never cascade.

### 3. Apply it

Re-run the same call without `dryRun`. Then:

- Report what went, using the tool's own redacted summary — **counts and kinds
  only**. Do not restate the removed names, dates or places back to the
  researcher: you are about to go looking for them, and repeating them here puts
  them right back in your context.
- Tell the researcher to confirm the gap in the viewer. Seeing the hole is how
  they check you removed what they meant.
- The tool writes `.tree-before-forget.gedcomx.json` so they can restore the
  tree. **Never read that file.** It still contains everything that was removed.

If the call comes back `{ ok: false, errors }`, nothing was written. Two errors
are worth reading carefully rather than routing around:

- **"matched nothing"** — the target is already gone. Read it as "this was
  already forgotten," not as a problem to fix.
- **A validation error naming `research.json` paths** — the researcher has
  assertions, person-evidence entries or a timeline that still reference a person
  you are about to remove. `tree_forget` does not touch `research.json`, so tell
  them what is blocking it and let them choose: clear those entries, or forget a
  narrower slice with a fact-level selector. Say plainly that entries which
  *state* the answer compromise the exercise anyway.

### 4. Research it

Proceed exactly as you would for a real question — `/research`, or the relevant
sub-skills. If the forgotten slice isn't already covered by an open research
question, create or reopen one (via the `question-selection` agent) that targets exactly
what was forgotten, and let it drive a plan — do not fall back to ad-hoc
`record_search` calls with no `plan_item_id`. A forgotten relationship is a new
question in its own right.

**Extract everything a record documents, not only the fact the
researcher asked about.** A record found while deriving the answer routinely
names other people too — a spouse in a marriage record, children in a household
census entry, a sibling in a death record's informant line. Assert all of it
through the normal extraction (`extraction_append`, or `@plugin:record-structurer`
for a non-FamilySearch source) and person-evidence path, exactly as you
would on any other research session. Do not treat this as narrowly answering
the one question; treat every record you read as ordinary new evidence and
write down everything it documents, including facts and relationships that
happen to fall on people whose ties were cut by the forget step.

When you reach a conclusion, present the evidence you actually found. The
researcher will compare it against what they know.

### 5. Account for what the forget step removed

This is the other half of the exercise, and it is not optional. A rederivation
that quietly ends with less in the tree than the forget step removed is a net
loss to the researcher, not a completed answer — say so plainly rather than
letting the shortfall pass unmentioned.

**You cannot check this against the tree or the restore file** — reading
either is still forbidden (Step 3). What you *do* have is the redacted summary
you already reported after Step 3 — counts and kinds only (e.g., "1 spouse
relationship, 3 child fact-sets"). Before declaring the session done, hold
that summary up against what Step 4 actually wrote back, and tell the
researcher explicitly, kind by kind:

- what was **re-established** from a record found during rederivation, and
- what is **still missing** — not found in any record you read, or found but
  not yet asserted.

Report the second category as plainly as the first. Some things genuinely
won't turn up in records — that is a legitimate outcome, not a failure to
paper over — but the researcher needs to hear it explicitly, not discover it
later by noticing the tree is smaller than before.

## What this does not do

- It does not touch `research.json`. Any assertions or log entries the
  researcher already wrote stay put; if those *state* the answer, say so, because
  the exercise is compromised until they're cleared too.
- It does not prevent tree lookups. Nothing enforces the rule in step 2 — it
  holds because you follow it.
- It does not verify the answer is recoverable from records. Some facts on a
  FamilySearch tree have no supporting record behind them. If the search turns up
  nothing, say the evidence isn't there rather than reaching for a guess — that
  is a legitimate and useful outcome, and reporting it honestly is worth more
  than a lucky hit.
- It does not restore what it cannot independently find. Step 5 re-asserts
  only what records found during rederivation actually support — it is not a
  diff against `.tree-before-forget.gedcomx.json` (still never read) and
  cannot bring back a fact or relationship no record documents. That gap gets
  reported, not silently accepted or quietly re-typed from memory of what was
  removed.

## Re-invocation behavior

**Writes** `tree.gedcomx.json` only — `tree_forget` removes the persons,
relationships, and facts named by the selectors, plus everything that cascades
from them. It writes nothing to `research.json`, the `log`, or the `results/`
sidecars. It also writes the restore file `.tree-before-forget.gedcomx.json` next
to the tree. `dryRun` writes neither file.

**On re-invocation,** forgetting is additive: a second call strips a further
slice from the already-stripped tree. Dry-run first every time regardless — the
cascade depends on the tree's *current* shape, so the second call's blast radius
is not the first one's. Both calls must happen before any plan is written —
once `research.json` holds a plan, `tree_forget` refuses.

**The restore file is written once and never overwritten,** so it always holds
the tree as it was before the *first* forget. A second forget does not disturb
it; restoring it undoes every slice at once.
