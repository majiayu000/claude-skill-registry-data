---
name: wikicommit-reconcile
description: Put sources back in the queue after a policy, type template or generation rule changed, so the next generate re-runs entity extraction against them. Use this only when someone explicitly asks to requeue sources after such a change. It rewrites source management files, so do not use it to process the queue or to see what is pending — wikicommit-generate processes it and wikicommit-status reports it without writing.
disable-model-invocation: true
---

# wikicommit-reconcile

Six kinds of input decide what a page says. Three of them have no route to the pages they already produced.

| Input | Identifier on the page | Route |
|---|---|---|
| The source document's content | `sources[].hash` | `check_ingest_freshness.py` → `status: outdated` → generate |
| The parent page (translation, synthesis) | `source_commit` | `check_translation_status.py` / `check_derivation_freshness.py` |
| **A policy** (`theme`, `entity-policy.md`, `source-policy.md`) | none | **this Skill** |
| **A type template** (`.wikicommit/schema/<Type>.md`) | none | **this Skill** |
| **A generation rule or version** | `generated_with` (version only) | **this Skill** |
| A person's judgement (a reader's report, a review) | — | tracking Issue → `/wikicommit-fix`, `/wikicommit-generate <url>`, `retracted` |

The first two and the last have a queue. The middle three did not.

They all reach a page through one place — **Pass 2c**, where policies are read, a type is chosen and the generation rules are applied — and the only entrances that run it open when a source's *content* changes. `--regenerate` deliberately skips Pass 2c (it takes a page rather than a source), `/wikicommit-fix` edits by hand, and `/wikicommit-remove` deletes. So after changing a policy there was nothing to run.

**This Skill does not generate anything.** It reports the gap and puts the sources back in the queue by setting `status: pending` on their management files; the next `/wikicommit-generate` picks them up through its existing collection rule. That is the same shape `check_ingest_freshness.py` already has — detect from outside generate, write a `status`, let generate's own rule find it.

Turning a switch **off** is the sharper case. A source left at `status: excluded` is not reachable by any existing command: re-running `/wikicommit-generate <url>` re-fetches, finds the hash unchanged and reports "no change"; `/wikicommit-generate <path>` skips before Pass 1 even starts; the bare `/wikicommit-generate` does not collect `excluded` at all. **All three print a success message.** Until this Skill the only way through was to open the management file and edit `status` by hand, and nothing told anyone to.

## Usage

```
/wikicommit-reconcile --source <path|url>
/wikicommit-reconcile --type <Type>
/wikicommit-reconcile --all
```

One selector is required — there is no default. What changed is something only the person who changed it knows, and a default would have this Skill guess.

- `--source <path|url>`: the one source, named the way it was registered.
- `--type <Type>`: every source that produced a page of that type. Use this after editing `.wikicommit/schema/<Type>.md`.
- `--all`: every source that has been processed. Use this after a policy or a version change, which are not scoped to a type.

## What this Skill does not detect

**It does not work out what changed.** Doing that needs a fingerprint of the policy and the type templates stored per source, and that is deliberately not built yet: the person running this Skill is the person who made the change, so the only thing a detector could add is a bit they already hold. A permanent health check for a one-off event is also the shape that ends up always-on and stops being read.

So the selector is the declaration. This Skill reports what the selection covers and asks before writing.

## Processing Flow

### 1. Resolve the selection

Read `.wikicommit/config.yml` for `theme`, and check whether `.wikicommit/entity-policy.md` and `.wikicommit/source-policy.md` exist — not to decide anything, but so the report can say which policies are in play.

Walk `.wikicommit/source/**/*.md` and collect the management files this run covers:

| Selector | Covered |
|---|---|
| `--source` | the one file whose `source.path` or `source.url` matches the argument |
| `--type` | files whose `generated_pages[]` holds a page under `<lang>/<Type>/` (or `<lang>/custom/<Type>/`) — so a source at `status: excluded` is never selected this way, see step 1's note |
| `--all` | every file whose `status` is `generated`, `partial` or `excluded` |

Skip and say so for any file whose `status` is:

- `retracted` — a person took that source out on purpose (a judgement no machine may undo, the same rule `check_ingest_freshness.py` and `add_source.py` already follow)
- `pending` or `outdated` — already queued; requeuing it would change nothing
- `failed` — it never got past extraction, so Pass 2c has nothing to re-run; the fix is whatever `## Failure Reason` names

For `--source`, resolve the argument against `source.path` / `source.url` by walking the tree rather than deriving the file name from the argument. Two derivation rules have changed over time and the old names are never migrated, so a derived name misses management files that a scan finds. Compare a URL the way it was normalized at registration rather than byte for byte — drop the fragment and the known tracking parameters (`utm_*`, `fbclid`, `gclid`), sort the rest of the query, ignore a leading `www.` and compare the host case-insensitively — because `source.url` stores the URL exactly as the person typed it that day, which is rarely how they type it today. For `--type`, accept the bare type name (`Person`, `custom/Decision`); strip a `schema:` prefix if one was given.

**If the selection is empty, say so and stop — do not go on to ask.** An empty selection is the likeliest sign of a typo, a URL that carries tracking parameters, or a type that has no pages, and this Skill exists precisely because a no-op that reports success is indistinguishable from work done. Name the selector that matched nothing, say how many management files were scanned, and for `--source` list the two or three registered identifiers closest to the argument. The same goes for a selection where every file fell into the skip list above: report each skip reason and stop, rather than asking to requeue nothing. When `--type` is what came back empty, say why it can: `--type` selects on `generated_pages[]`, and a source at `status: excluded` has none — so the very sources that a loosened policy would bring back are the ones this selector cannot see. Point at `--all`, or at `--source` naming them.

### 2. Report before writing

Print, in this order:

- how many management files the selection covers, and how many pages they produced between them (from `generated_pages[]`)
- the count of those currently at `status: excluded` — these are the ones that produce pages only if a policy was loosened, and the ones no other command can reach
- every file being skipped, with which of the three reasons applied
- which policies exist and whether `theme` is set — so the operator can see the inputs that Pass 2c will read this time

Then ask **once**, defaulting to no, naming the count: `Put <N> source(s) back in the queue? The next /wikicommit-generate will re-run entity extraction against them.`

On a no, stop and print nothing further. On a non-interactive run, do not write — report what the selection covers and stop. Silence is not consent, and this rewrites tracked files.

### 3. Requeue

For each covered file:

```bash
python .wikicommit/scripts/set_frontmatter_field.py "<management file>" \
  --set 'status=pending' --require 'status=<the status just read>'
```

`--require` makes the write conditional on the value this run actually read, so a file that changed underneath is skipped rather than overwritten. Run one file per invocation and report `SKIP` results — they mean the tree moved, not that the work is done. Keep the quotes around the path: a management file mirrors its source's path verbatim, so a source at `raw/My Report.pdf` is held at `.wikicommit/source/path/raw/My Report.pdf.md`, and unquoted that splits into two arguments and the write never happens.

**Do not touch anything else in the file.** `source.hash` stays as it is, so Pass 1 finds the cached fetch unchanged and skips re-fetching (only the extraction and Pass 2c onward run again). `generated_pages[]` stays so that the pages this source already made remain attributable, and `last_generated_at` stays because this run generated nothing.

### 4. Say what happens next

Report the number requeued and print the next command:

```
/wikicommit-generate
```

Say three things with it:

- `/wikicommit-status` will now count these as unprocessed sources. That number going up is this Skill working, not a new problem.
- When more than five sources are queued, `/wikicommit-generate` stops and asks whether to process all of them or only the first five. It is a question, not a cap — a large selection can be worked through in one run or in several, and that is the operator's call. Queuing is done in one go either way.
- Pages that this run's policies now exclude are **not deleted**. Nothing in the generate path removes a page; `/wikicommit-remove` does. After generating, compare the `## Generation Notes` exclusion list in each management file against the pages that still exist.

## Notes

- **This Skill writes to `.wikicommit/source/` and nothing else.** It does not create pages, does not touch `.wikicommit/entity/` or `.wikicommit/view/`, and does not run Git. `/wikicommit-merge` commits the result like any other change.
- **`/wikicommit-generate` is unchanged by this Skill.** Adding a flag there would have meant growing the largest SKILL.md in the distribution, which is most of the fixed cost of every generate run. Queuing is also not generation's job.
- **Requeuing is idempotent.** A file already at `pending` is skipped in step 1, and `--require` makes the write itself conditional, so running this twice does not double anything.
- **A requeued source stays queued until it is processed.** `reconcile_ingest_status.py` runs at the end of every generate and would otherwise write a `pending` file straight back to `generated` under a `RECONCILED:` line — a success line, so the queue would empty silently. Three clauses hold it off, one per requeue origin, because no one of them covers the others: a file requeued from `generated`/`partial` still lists its pages, and the script skips any file whose `generated_pages` is non-empty; a source that never produced a page has its hash cited nowhere, so the script's match test finds nothing; and a source that produced pages under an earlier, looser policy and was later excluded in full clears both of those — `excluded` carries no `generated_pages` while the pages it made stay on disk citing its unchanged hash — so the script also skips any file carrying a `last_generated_at`, which says the run that put it at `pending` came after a completed one.
- **What this Skill cannot see**: whether the prose in a policy file changed at all, and whether a switch it does not know about exists. It requeues what the operator names; deciding what to name is the operator's.
