---
name: wikicommit-status
description: Check the wiki's health — orphan and wanted pages, pages not yet read by a person, expired pages, stale translations, outdated sources, sources that were deferred or failed, types with no schema file, unlinked entity mentions, unused installed types, self-referential tags, broken external links, and more. Use this whenever someone asks how the wiki is doing, what needs attention, what is left to review, whether anything is stale or broken, or what to work on next — and run it before concluding the wiki is fine, since most of what it reports is invisible from any single page.
---

# wikicommit-status

A health-check skill for the wiki as a whole. Calls the six page-count scripts (`check_orphans.py` / `check_wanted_pages.py` / `check_expires.py` / `check_ingest_freshness.py` / `check_translation_status.py` / `check_derivation_freshness.py`), the three blocking checks `wikicommit-merge` runs only on changed files (`validate_frontmatter.py` / `check_wikilinks.py` / `check_raw_html.py`, run here over every page), plus `check_actions_pr_permission.py` (a single repository-setting check, not a page count), `check_property_wikilink_reinforcement.py` and `check_schema_files.py` (two `.wikicommit/schema/` checks, not page counts either — the first for whether a template points at a WikiLink, the second for whether a type file is written in a working shape at all), `check_schema_coverage.py` (types in use with no dedicated schema file), `check_recurring_characters.py` (characters left as plain text in `properties.character`) and `check_unlinked_entity_mentions.py` (a `properties:` value naming a page that exists, written as plain text) and `check_installed_type_usage.py` (installed type files with no pages, and pages sitting on an ancestor of an installed type) and `check_self_referential_tags.py` (tags that only repeat a page's own title or type), and `check_external_links.py` (external links that no longer resolve, across every page — the check `wikicommit-merge` makes only on the pages a batch changes), aggregates their results, and displays them alongside the number of unprocessed `.wikicommit/source/` files and the number of `.wikicommit/entity/` pages no person has read yet. This skill has no dedicated scripts of its own (only the existing scripts plus directory scanning).

## Usage

```
/wikicommit-status [--links]
```

Always targets the whole repository.

- `--links` — check every page's external links with lychee now (Step 16.5). Without it, Step 16.5 only reads back the last completed check, without touching the network: checking every link takes minutes on a large wiki, and this skill is also called when someone just wants a quick answer.

## Processing Flow

### Step 1: Check for Unpulled Remote Changes

This skill only scans the local working tree. If PRs (e.g. post-review PRs from `/wikicommit-merge`) were merged on GitHub but not yet pulled locally, the results below will be stale — pages already `reviewed` on GitHub can still be counted as `review_status: pending` here.

Run `git fetch` (read-only; does not modify the working tree) and compare local `HEAD` against `origin/<current branch>` (e.g. via `git rev-list --count HEAD..origin/<branch>`). If the local branch is behind, warn the user before displaying results:

```
Note: your local branch is N commit(s) behind origin/<branch>. Results below may be stale
if PRs were merged on GitHub since your last pull. Run `git pull` first for an accurate picture.
```

Do not run `git pull` automatically — it could conflict with uncommitted local changes, and this skill is read-only by design (see Notes).

### Step 2: Disclose the Side Effect

`check_ingest_freshness.py` has the side effect of rewriting local `.wikicommit/source/` management files (it changes any management file with `status: generated / partial / outdated` whose hash mismatches to `outdated`. Management files with `status: pending / excluded / failed` are not checked even on a hash mismatch, and are not detected by this step). Disclose this to the user before running it:

```
Note: running check_ingest_freshness.py will rewrite the status of any .wikicommit/source/
management file whose source changed to outdated (local change only; will show up in git status).
Run /wikicommit-merge afterward to commit it.
```

### Step 3: Run the Nine Scripts

Run the following in order, and for each, take the counts from its `SUMMARY:` line and the corresponding file paths from its `ORPHAN:` / `DUPLICATE:` / `WANTED:` / `TYPE_MISMATCH:` / `page:` lines.

```bash
python .wikicommit/scripts/check_orphans.py
python .wikicommit/scripts/check_wanted_pages.py
python .wikicommit/scripts/check_expires.py
python .wikicommit/scripts/check_ingest_freshness.py
python .wikicommit/scripts/check_translation_status.py
python .wikicommit/scripts/check_derivation_freshness.py
python .wikicommit/scripts/validate_frontmatter.py
python .wikicommit/scripts/check_wikilinks.py --skip-type-mismatch
python .wikicommit/scripts/check_raw_html.py
```

- `check_orphans.py` → `SUMMARY: orphans=N, duplicates=N`. Get file paths from the `ORPHAN: <path> (sources: ...)` / `DUPLICATE: <path> <-> <path> (title: "...")` lines (these two are the only categories without a `page:` line, so parse them directly). Keep the `sources:` part when listing orphans — the useful next question about an unreachable page is which source produced it, and a run of orphans sharing one source usually means that source covers something the rest of the wiki does not link to yet.
- `check_wanted_pages.py` → `SUMMARY: wanted=N, type_mismatch=N`. The counterpart to `check_orphans.py`: pages with WikiLinks pointing at them but no backing file in any language (`check_wikilinks.py`'s missing-target case is a WARNING, not a blocking ERROR, so this report is how these surface for follow-up). Get the `Type/slug` keys from the `page:` lines; the referrer counts and paths are in the corresponding `WANTED:` or `TYPE_MISMATCH:` line directly above each `page:` line. **Report the two counts as separate categories and never merge them** — they call for opposite actions. A `WANTED:` key is a page to write. A `TYPE_MISMATCH:` key is a link whose slug already has a page under a different Type, named in that line: writing the "missing" page would duplicate the existing one, so the fix is to correct the Type segment in each referring page instead. Every `TYPE_MISMATCH:` key also blocks `wikicommit-merge` as a `check_wikilinks.py` ERROR once one of its referring pages is next changed, so treat it as work due now rather than a backlog item.
- `check_expires.py` → `SUMMARY: expired=N`. Get file paths from the `page:` lines.
- `check_ingest_freshness.py` → `SUMMARY: outdated=N, ok=N`. Get file paths from the `page:` lines.
- `check_translation_status.py` → `SUMMARY: stale=N, missing_source=N, untranslated=N`. Get file paths from the `page:` lines (each `STALE:` / `MISSING_SOURCE:` / `UNTRANSLATED:` line is immediately followed by its corresponding `page:` line). `untranslated` is 0 whenever `.wikicommit/config.yml`'s `translation.targets` is empty (no target languages configured).
- `check_derivation_freshness.py` → `SUMMARY: stale=N, missing_source=N`. This is the `wikicommit-synthesize` counterpart of `check_translation_status.py`'s `STALE`/`MISSING_SOURCE` (same output shape, but walks `derived_from` entries instead of `translated_from`). Get file paths from the `page:` lines; a page with multiple stale/missing `derived_from` entries emits a `page:` line once per entry, so the same path may appear more than once here — dedupe when listing paths, but not when counting (the `SUMMARY:` counts entries, not pages). Keep this separate from `check_translation_status.py`'s own stale/missing counts (the line directly above) — different frontmatter field, different root cause: a translation going stale vs. a synthesized page's source going stale.

- `validate_frontmatter.py`, `check_wikilinks.py --skip-type-mismatch` and `check_raw_html.py` → **take only their `ERROR:` lines**, and ignore their `WARNING:` and `OK:` lines. These are the three blocking checks `wikicommit-merge` runs on the files a batch changes, and only on those: a page is checked when it is written and never again, yet it can break afterwards — a refreshed `.wikicommit/schemaorg-vocab.json` or an imported type template can make a frontmatter that used to pass fail, a raw HTML tag left in a `pending` page is published as is, and a link to a page removed later is reported to nobody. Here they run on every page. Their WARNINGs are left out on purpose: `check_wikilinks.py`'s are unresolved links (the same thing `check_wanted_pages.py`'s `WANTED:` says above) and `[[...]]` written in a form that is not a WikiLink, which this report leaves to `wikicommit-merge`, and the other two's are informational. `--skip-type-mismatch` keeps a wrong Type segment out of these lines, because `check_wanted_pages.py` already reports it as `TYPE_MISMATCH:` — the flag is what removes the duplicate, so do not filter by message wording. **The three exit 1 whenever they print an `ERROR:` line. That is a finding here, not a failure of this step** — record the lines and carry on with the rest of the steps, as for every other script this skill runs. The one exception: an exit 1 with no `ERROR:` line on stdout means the script could not run at all (`validate_frontmatter.py` stops this way when `.wikicommit/schema/default.md` cannot be read, printing its reason to stderr) — report that script as not run, with its stderr, rather than counting 0, which would read as a clean wiki.

### Step 4: Check GitHub Actions PR Permission

```bash
python .wikicommit/scripts/check_actions_pr_permission.py
```

Unlike the nine scripts in Step 3, this is a single repository-setting check, not a per-page count — it verifies "Allow GitHub Actions to create and approve pull requests" is enabled, which `review-issue-close-sync.yml`'s `Commit and open PR` step depends on. `wikicommit-init` tries to enable it, but that attempt can fail silently, and the failure otherwise shows only when a closed tracking Issue's workflow run fails deep in the Actions logs. This is the only script this skill calls that invokes `gh`; it never writes to the repository setting itself (read-only, matching every other check).

Take the `OK:`/`WARNING:` line and `SUMMARY: enabled=<true|false|unknown|n/a>` — `n/a` means `review-issue-close-sync.yml` doesn't exist in this repository (not applicable) and `unknown` means the check itself couldn't run (unauthenticated `gh`, unresolvable repository, or a failed `gh api` call) — both are distinct from a confirmed `false`.

### Step 5: Check the Type Schema Files

```bash
python .wikicommit/scripts/check_property_wikilink_reinforcement.py
python .wikicommit/scripts/check_schema_files.py
```

Also unlike the nine scripts in Step 3, this checks `.wikicommit/schema/` type templates, not `.wikicommit/entity/` pages — for each `properties:` key whose Schema.org range includes a linkable entity type, whether the template gives any textual hint (a `granularity` bullet that names the property *and* points toward linking it — the rest of that bullet contains `[[` or the word `link` — or a `[[Type/slug]]` placeholder already in `properties:`) toward writing that property's value as a WikiLink. Purely a human-readability nudge, not a functional requirement — `wikicommit-generate` Pass 3 already applies the WikiLink decision uniformly to every such property regardless of whether the template reinforces it, so an `UNREINFORCED:` finding here is not itself evidence anything is broken. `description` is expected to appear for nearly every type (its Schema.org range is Mixed via `TextObject`, but this wiki's convention keeps it as prose) — treat that specific recurring finding as expected noise, not a defect to chase down. `HowTo`'s `tool` and `supply` are the same: that template names them only to say they are often empty and should be left out, which does not count as pointing at a WikiLink, so they are reported and are meant to stay that way.

Get the `SUMMARY: unreinforced=N` count and the individual `UNREINFORCED: <Type>.<property> (<path>) — ...` lines. Also surface any `WARNING: <path>: wikicommit.granularity...` line and keep it next to the findings for that same file: it means a `granularity` bullet parsed as something other than a string (usually a `": "` inside an unquoted list item, which YAML reads as a one-key mapping), so the reinforcement search never saw that bullet's prose. An `UNREINFORCED:` line for a file that carries such a warning may well be a parse artifact rather than genuinely missing reinforcement — the fix is to rewrite the bullet in the schema file (em dash instead of the colon, or wrap the bullet in double quotes), not to add reinforcement that is already there.

`check_schema_files.py` scans the same directory for a different question: not whether a template *should* say more, but whether it is **written in a shape that works at all**. Nothing checked this before — the four CI tests in this project reach only the templates it distributes, and a type file written at runtime or by hand cannot be repaired by any Skill afterwards, since the exception that lets one be written is add-only. Get `SUMMARY: files=N, findings=N, in_distributed_templates=N` and the individual lines, each of which names its file and that file's `provenance`:

| Line | What it means |
|---|---|
| `BAD_PROPERTY:` | a `properties:` key that is not in the Schema.org vocabulary, or not in that type's domain — the same check a page's own `properties:` gets, which never ran against the template the page came from |
| `MAPPING_BULLET:` | a `granularity` bullet that became a one-key mapping because of an unquoted `": "`, so every consumer that reads bullets as strings skips it |
| `TRUNCATED_BULLET:` | a `granularity` bullet whose raw line carries an unquoted ` #`. **This is the one nothing else can notice**: YAML hands back the part before it as an ordinary string, so the rule looks fine and its second half is simply gone |
| `NO_BOUNDARY:` | no bullet begins with `Boundary` — a bullet that became a mapping still counts, read from its key. A type can state its boundary against an existing one, but nothing can ever write the reciprocal statement into the other file, so a missing one is not recoverable later |
| `BAD_PROVENANCE:` / `NO_BASE:` / `NO_WIKICOMMIT_BLOCK:` / `NO_RATIONALE:` | a value outside the known set; a missing `base`; no `wikicommit:` block at all, so none of those fields can be there to find; a custom type with no prose saying why no standard type fits |
| `TYPE_PATH_MISMATCH:` / `UNKNOWN_TYPE:` | a `type:` that disagrees with the path (only the path decides which type a file defines, so a mismatch means the file defines nothing); or the two agree and neither is in the vocabulary, usually a misspelling — the second is reported only when they do agree, since otherwise the first has already named the one thing to fix |
| `NO_FRONTMATTER:` / `UNPARSEABLE:` | the frontmatter is absent or does not parse — reported as one finding rather than letting every other check fire off the same cause |

**Read `in_distributed_templates` before reading the list.** A finding on a `provenance: default` file means this repository holds an *older copy* of a template, not that anyone wrote it wrong — several of these conventions were added to the templates after they first shipped. Its remedy is the upstream diff, which Step 11 reports for the same files; editing a distributed template by hand puts it back in the way on the next sync. In practice this kind can make up most of the total.

Not blocking, and this is deliberately not part of `wikicommit-merge`'s quality gate: one malformed schema file would otherwise make a repository unable to merge anything, and the fix here is a person editing a file no Skill may touch. The missing `provenance` of an older file is **not** reported — its absence means "written before that field existed".

### Step 6: Check Schema Coverage

```bash
python .wikicommit/scripts/check_schema_coverage.py
```

Like Step 5, this is about `.wikicommit/schema/` rather than page health as such: it reports each `type:` value in use by pages that has **no dedicated schema file**, so those pages were generated (and are validated) against `default.md` alone — that type's `granularity` rules, `properties:` candidate keys and body template never applied.

Falling back to `default.md` is correct, intended behavior, so this never blocks a merge — the script always exits 0, and `validate_frontmatter.py` keeps this a WARNING rather than an ERROR for the same reason. It does count against the "Wiki is healthy" verdict in Step 17, which is a different thing: a repository whose schema files match the types it uses reaches 0 here, and a repository that does not has a concrete fix available. An older repository may well start non-zero; that is the finding doing its job, not a reason to exclude it. Nothing else surfaces this once the pages exist: `wikicommit-generate` reports it only in the Completion Notice of the run that generated the page, and `validate_frontmatter.py`'s WARNING reaches only the files a given `wikicommit-merge` batch changes — so a schema file moved, renamed or deleted afterwards leaves every existing page failing silently.

Get the `SUMMARY: unschemaed_types=N` count and the individual `UNCOVERED: <type> (<N> pages, e.g. <path>)` lines.

When the count is 1 or more, note that `/wikicommit-schema-propose` opens a PR adding the missing file — and warn about one trap before running it: it always writes `.wikicommit/schema/<Type>.md`, derived from `type:`. If the file is missing because someone filed it under a subdirectory (`.wikicommit/schema/<sub>/<Type>.md`), that path is not what the lookup reads, so the proposal produces a **second** definition of the same type with only the new one in effect. In that case move the existing file back to `.wikicommit/schema/<Type>.md` instead of running the Skill.

### Step 7: Check Recurring Plain-Text Characters

```bash
python .wikicommit/scripts/check_recurring_characters.py
```

Back to `.wikicommit/entity/` pages, but reading `properties:` values rather than WikiLinks: `ShortStory.md` / `Book.md` tell Pass 3 to WikiLink a character who qualifies for a `[[Person/slug]]` page and to list the rest as plain text, and nothing ever revisits that call afterwards. A plain-text name is invisible to every other check here — `check_wanted_pages.py` reads only `[[Type/slug]]` WikiLinks, so an unpromoted character is not even counted as wanted, and `check_orphans.py` is about backlinks to pages that already exist.

Take the `SUMMARY: recurring=N` count and the individual `RECURRING:` lines (no `page:` lines — each finding line names the works itself). A `RECURRING:` line is the same name in two or more works with no `Person` page anywhere: recurrence across works is the evidence a single work cannot give, so this is a page worth writing (or a decision, once, that the character stays plain text). Works are counted by `<Type>/<slug>`, so the language versions of one story count once.

A name that *does* already have a page is Step 8's finding, not this one — the two call for opposite work (write a page vs. link to the one that exists), which is why they are separate scripts and separate counts.

This is not blocking, and does not gate the health verdict in Step 17 — the promotion bar is a judgment call belonging to `Person.md`'s `granularity` at generation time, and a wiki can legitimately decide a recurring character stays plain text. Note also what this cannot see: a protagonist appearing in exactly one work never recurs, so a wiki whose characters are all one-work leads reports 0 here while still having the gap this check exists for.

### Step 8: Check Unlinked Entity Mentions

```bash
python .wikicommit/scripts/check_unlinked_entity_mentions.py
```

The mirror image of `check_wanted_pages.py` (Step 3): that one finds a link with no page behind it, this one finds a page with no link in front of it. It reads every `properties:` value whose key has a linkable entity type in its Schema.org range — the same `--show-range` classification Step 5 uses — and reports the plain-text values that name a page which actually exists.

Pass 3 is told not to let a missing target page stop it from writing a WikiLink, yet a value whose page only appeared in a later ingest can still be left a bare string. Nothing self-corrects — `action: update` reaches a page only when a source for *that page* is re-ingested — and nothing else reports it either: `check_wikilinks.py` reads only the WikiLinks that were written, and `check_orphans.py` misses the case whenever the target page has backlinks from elsewhere.

Take the `SUMMARY: unlinked=N` count and the `UNLINKED:` lines with their `page:` lines. Each names the referring page, the property, the value, and the page it resolves to. The fix is `/wikicommit-fix <page-path> "<instruction>"` on the referring page — deliberately not an automatic rewrite, since a value matching a page title is evidence, not proof (two subjects can share a name), and `properties:` is not something a health check should write to.

Not blocking, and does not gate the health verdict in Step 17 for the same reason: the value's shape is a generation-time judgment `validate_frontmatter.py` deliberately does not enforce (it checks that a `properties:` *key* belongs to the type, never the *value*'s shape).

### Step 9: Check Installed Type Usage

```bash
python .wikicommit/scripts/check_installed_type_usage.py
```

The counterpart to Step 6: that one finds a `type:` in use with no schema file behind it, this one finds a schema file with no pages in front of it. A wiki with `Park.md` installed can still generate parks as plain `Place`, and Step 6 reports zero for that, because `Place` does have a schema file.

Take the `SUMMARY: unused=N, ancestor_fallback=N` counts and the individual lines. The two differ in strength on purpose:

- `UNUSED:` — a type file with zero pages. Either the type was a misjudgment, or generation is not reaching for it. `provenance: default` types are exempt, since they ship with every wiki whether or not its subject calls for them.
- `ANCESTOR_FALLBACK:` — pages on a type whose descendant is also installed. **Suggestive, never conclusive**: a wiki with `Park.md` still has legitimate `Place` pages that are not parks. Read it as "worth a look".

Neither is blocking and neither gates the health verdict in Step 17 — which type fits a subject is a judgment call this script cannot make, only point at. When something here does look wrong, note that re-typing an existing page is not something any Skill does today: it means a directory move plus rewriting the Type segment of every WikiLink that points at it. What this check is really for is catching the pattern early, so the next batch generates at the right grain.

### Step 10: Check Self-Referential Tags, Name Collisions and Page Groups

```bash
python .wikicommit/scripts/check_self_referential_tags.py
```

`tags` groups pages across the wiki by something they share. A tag equal to the page's own `title` groups the page with itself, and one equal to its `type` repeats what `type:` already says — both are ruled out at generation time, and a generation-time rule with nothing checking it drifts.

Take `SUMMARY: title_echo=N, type_echo=N` and the `TITLE_ECHO:` / `TYPE_ECHO:` lines with their `page:` lines. The fix is to drop the tag — `/wikicommit-fix <page-path> "<instruction>"`, or by hand.

Matching is exact after normalization and never partial: `見沼` on a page titled `見沼田んぼ` is the useful kind of tag and is not reported. One thing it cannot see is a type tag written in the wiki's own language (`博物館` on a `schema:Museum` page), which would need a translation of the Schema.org vocabulary — type names are language-neutral identifiers here and no such table exists. Non-English wikis get the title half only.

Not blocking, and does not gate the health verdict in Step 17: a tag is a judgment call, and a wiki may have a reason for one this check flags.

Then, in the same step, the pages that answer to the same name:

```bash
python .wikicommit/scripts/check_name_collisions.py
```

A concept two sources call by different names gets two pages, and what is left over shows as one page's title or alias being another page's title or alias. Take `SUMMARY: collisions=N, judged_pairs_skipped=N, relations=N` and the `COLLISION:` lines (no `page:` lines — each names the pages and whether the name is their title or an alias). Pairs a person has already decided about in `.wikicommit/relations.yml` are not listed. The route for each group is `/wikicommit-relate`, which asks whether the pages are the same concept, one inside the other, related or distinct, and records the answer. A title shared by two pages of the same Type is not repeated here — `check_orphans.py` reports it as `DUPLICATE:` in Step 3.

Not blocking, and does not gate the health verdict in Step 17: whether two pages that share a name are one concept is a person's call, and two distinct things legitimately share names.

Then, still in this step, the Types whose pages are sorted into groups (`.wikicommit/groups/<Type>.yml`, written by `/wikicommit-organize`):

```bash
python .wikicommit/scripts/check_groups.py
```

Take `SUMMARY: types=N, unclassified=N, stale=N, errors=N`, the `TYPE:` lines (one per Type that has a group file) and any `ERROR:` lines. A Type with no group file is not reported at all — grouping is optional, and a line for every ungrouped Type would always be on. An unclassified page is one generated after the last grouping; nothing places it automatically, so the count is the cue to run `/wikicommit-organize <Type>` again. A stale member is a slug the file still names though its page was removed or renamed; the next `/wikicommit-organize` run offers to drop it. An `ERROR:` means the file cannot be read as a grouping, and until it is fixed that Type's index and left pane are shown ungrouped. There is no threshold: how many unclassified pages are too many is the reader's call.

Not blocking, and does not gate the health verdict in Step 17.

### Step 11: Check Distribution Freshness

```bash
python .wikicommit/scripts/check_distribution_freshness.py
```

Like Step 4, this looks at the state of the installation rather than at pages. It compares what is on disk against the templates the installed `wikicommit-init` Skill ships, and reports three things: `OUTDATED:` (present but no longer matching), `MISSING:` (the template has it, this repository does not) and `ORPHAN:` (this repository has a file the template no longer does — `/wikicommit-init` refreshes trees but never deletes from them, so a script renamed upstream leaves its old name behind). Read-only; unlike `check_ingest_freshness.py` in Step 3 it writes nothing.

What each path is compared against, and whether it is compared at all, is declared once in the Skill's own `_root_outputs.py` alongside the variant and `git add` decisions for the same path. Paths WikiCommit owns outright are compared byte for byte, because a re-init refreshes them and any difference is a version gap. Paths the user may have edited are reported only when the **template has gained something this repository lacks** — a new configuration key, a new frontmatter key, a new ignore pattern. Changing a value or rewriting the prose is the user doing their job and is never reported. Do not read a quiet result as "this file is identical to the template"; read it as "nothing has been added upstream that is missing here".

Take the `VERSION:` line and the `SUMMARY: outdated=<N>, missing=<N>, orphan=<N>` counts. `synced=unknown` on the `VERSION:` line means the repository predates the version stamp — it is reported for the reader and never gates a comparison, so the findings are as reliable as on any other repository. A `WARNING:` line instead of findings means the `wikicommit-init` Skill is not installed here, so there was no template to compare against; that is not a defect in the wiki, and the fix is to install the Skills.

Everything this reports is fixed by re-running `/wikicommit-init` (with `--no-overwrite`, though the update policies protect the user's files either way), **except orphans** — those are deleted by hand, after checking that nothing still calls the file.

### Step 12: Check Pages Resting on a Retracted Source

```bash
python .wikicommit/scripts/check_retracted_sources.py
```

`status: retracted` on a source management file records that a human read a registered source, judged its content unreliable, and took it out of use. Setting it stops the source being ingested again, but it does nothing to the pages already written from it — those keep it in their `sources[]`, unchanged and unremarked. This step is what surfaces them.

Take `SUMMARY: retracted_sources=N, affected_pages=N` and the `RETRACTED_SOURCE:` lines with their `page:` lines. Each line names the page, the retracted identity its `sources[]` still carries, the management file that retracted it, and **how many other sources that page still rests on** — which is the number that decides what to do: a page with at least one remaining source can be rebuilt from what is left with `/wikicommit-generate --regenerate <page>`, which drops the retracted source and its `sources[]` entry and is the route that actually takes it out of the page's evidence base — with one exception the count itself cannot show you: Regeneration Mode excludes any page carrying a `sources[].type: manual` entry, which this count treats as a remaining source, so a page whose only remainder is a manual one is a `/wikicommit-fix` too; a page whose problem is narrower than a rebuild is a `/wikicommit-fix`; and a page down to zero has nothing left holding it up, so it is a `/wikicommit-remove`.

**Reporting is the whole intervention here, deliberately.** Do not reset these pages to `review_status: pending`: whether a human must re-read a page is decided only by a deterministic "did the content change?" check, and a retraction changes no content — only the standing of the evidence behind it. `pending` would also say "read this again" without saying what is now unsupported.

Only a human can set this status, and only a human can lift it. That is not a gap: the machine judges a page *against* its sources, so it cannot judge the sources themselves, and the fetch guards catch only broken *retrieval*, not a source that fetched perfectly and is simply wrong.

Not blocking, and does not gate the health verdict in Step 17: whether a retracted source's pages need rewriting, removing or leaving alone is a judgment call, and `retracted_sources=0` (nothing has ever been retracted here) is reported the same way as no affected pages.

### Step 13: Check Review Coverage

```bash
python .wikicommit/scripts/check_review_coverage.py
```

Reads the review records under `.wikicommit/review/` and reports what has been reviewed, by what, and which verdicts no longer hold:

- `SUMMARY:` — pages, how many carry a **standing** machine review, how many carry a standing human one, how many of those left a note, total findings, distinct models. "Standing" throughout this step means the newest record that judged the page as it now stands: a `result: discarded` review judged a draft that was thrown away, so it says nothing about the text on disk and is not counted as coverage of it
- `human_notes` is the one number here that says anything about **how** a page was read. Closing a review Issue without a comment is a legitimate close and is reported as a defect nowhere — but every other output looks the same either way, so this is the only place the difference shows. It counts **presence, not content**: a one-word note and a paragraph are both one, and nothing here reads what the note says. Treat it as "did the ask reach anyone", not as "was the page read" — and do not report a low number as a problem
- `COVERAGE:` — per model: pages, findings, how many needed more than one attempt — all three from the standing record — and last, how many pages whose **newest AI record** is a discarded one this model wrote. That last number is the one thing here that reads a discarded record, and it is what makes a quiet `RISKY:` legible rather than contradictory: a page can be listed as discarded here and correctly appear in no verdict line at all. It is keyed on the page's newest AI record rather than on each model's own newest, because it exists to explain a missing `RISKY:` line — once a later review has judged the current text there is nothing missing to explain, so a superseded discard is not counted
- `UNREVIEWED:` — a page with no standing record. Almost always that means no record at all; it also covers a page whose records exist but none of which judged the page as it now stands, and the line says which case it is — every record discarded, or none carrying a `page_content_hash`. All of them want the same response — someone has to look at this page — which is why they are one list
- `RISKY:` — a page whose **standing** review took more than one attempt or drew findings. **This is the sampling list**: it is the closest thing the wiki has to "which pages are most worth a human reading", and "Standing" here is the newest record that judged the page as it now stands, of either kind — so a page drops off once a later review comes back clean, and a human's own findings put a page on the list. It reads that one record rather than the history, because records are immutable and never deleted: summing over all of them would keep a once-retried page listed forever, until the list selects nothing. The "took two rounds to pass" signal is not lost — that review is the standing one and carries its own `attempts`. The two criteria overlap heavily (a blocking finding forces another attempt), but the findings half still catches two routes on its own: a non-blocking finding pointing at another page as the one at fault, and a human review, which has no retry loop so its findings always arrive at a single attempt. Keep both criteria for those
- `STALE_REVIEW:` — a recorded verdict that no longer applies, either because the page's text changed after it or because a source under it did
- `RETRACTED_EVIDENCE:` — a verdict that rested on a source since retracted. Distinct from Step 12: that step reports pages that still *name* a retracted source, while this one reports that a judgment was actually made on the strength of it

Report the counts, and list `UNREVIEWED:` / `RISKY:` / `STALE_REVIEW:` / `RETRACTED_EVIDENCE:` findings if there are any.

Not blocking, and does not gate the health verdict in Step 17. There is deliberately no threshold here — no coverage percentage to hit and no automatic action. A human reads `RISKY:` and decides whether to read the page or re-run `/wikicommit-generate --regenerate`; a number invented before there is data to set it from would only look like a standard.

A wiki initialized before this existed has no `.wikicommit/review/` and reports zeros with a note saying so — the absence of records means "generated before reviews were recorded", not "never reviewed".

### Step 14: Check Run Records

```bash
python .wikicommit/scripts/check_run_records.py
```

Reads the run records under `.wikicommit/run/`. Every other layer in this repository is keyed on an artifact — a file, a source, a page, a review — and this is the only one keyed on **a run**, which is what these three lines need:

- `LAST_RUN:` — when the last run of any Skill was, how long it took, and what it produced. Both the timestamp and the duration exist nowhere else: `generated_at` is a date, a commit timestamp is the merge rather than the generation, and no layer has ever held an elapsed time at all
- `INCOMPLETE_RUN:` — a run that did not finish **normally**: either a record with a start and no end, or one a halt closed. Without it the state such a run leaves behind (some management files `pending`, some `generated`) is indistinguishable from a backlog that has simply not come up yet, which Step 15 counts; and on the two paths that halt before any file changes there is nothing in Git at all to notice. `halted_reason` is on the line when the run recorded one, together with how long the run took before it stopped
- `MISSING_PASS:` — a run that finished **normally** but left no stamp for one of the passes it should have gone through. A halt is not reported here: it is on the line above, and saying a halted run "finished, but" skipped the later passes would be wrong on both halves — it did not finish, and not reaching them is what halting means. This is the other half of what the per-pass stamps were added for: `INCOMPLETE_RUN:` answers *where a run stopped*, and this answers *whether a run skipped something and carried on*. That second failure — a step dropped near the end of a long multi-pass flow while everything else looks normal — is otherwise found only by a human auditing a published wiki, and delegating the step to a script does not help when the instruction to *call* the script is what goes missing; the stamps sit one level outside that, and this line is how they are read back

Only one `LAST_RUN:` is printed, and every incomplete record is listed. **A forgotten closing stamp shows up here too**, and that is the accepted direction of the error rather than a defect — a completed run reported as incomplete costs a glance, while the reverse would quietly retire the question the record exists to answer. **`MISSING_PASS:` is an observation, not a verdict** — a run whose sources were all blocked during extraction, or all already up to date, has nothing left for the later passes to do, and ending there is correct. It also reports a false positive when a compaction dropped the stamping instruction itself, in which case a pass that really did run leaves no stamp. **A run that stamped nothing at all is listed too, and its line reads differently**: a record carrying an empty list of stamps is not the same as one written before stamping existed, and the first of those is the worst case — every stamping instruction lost rather than one — so it says "stamped no pass at all" and names the work the record holds rather than listing five passes as though each had been skipped separately. Such a run is only listed when the record shows it did work (a source or page it named, or a non-zero outcome count): finishing with no stamp is legitimate and usual when there was nothing to process, and reporting that would put this line on most runs. A record with no `passes` key at all — written before stamping existed — is still not listed, because nothing about passes can honestly be said of it. **A 0 here still does not prove no pass was skipped**: the closing call records the work, so a run that lost its stamping instructions and closed without naming a source, page or outcome reads as a run that had nothing to do. Runs that did not finish normally are never listed here, since they are already reported on the line above and their gaps have an obvious cause.

Not blocking, and does not gate the health verdict in Step 17: this describes how the wiki was operated, not whether its content is sound.

These records are not tracked by Git, so **they are local to this machine and this checkout** — a clone sees none, and a cloud session's records go when its VM does. A repository that reports zeros here has not necessarily been idle.

### Step 15: Tally Unprocessed Source Management Files

Scan `.wikicommit/source/**/*.md` and read each file's frontmatter `status` field. Count the files with `status: pending` and record their paths.

From that same scan, also count how many of those `pending` files have **never been processed at all** — no `last_generated_at` (absent or empty). Record their paths, and note how many of those have an empty `source.hash` as well, meaning nothing has even been retrieved for them yet (only `type: url`/`wikicommit` files can be in that state — `add_source.py` hashes a `type: path` file at registration).

**And from the same scan, count separately how many files of any `status` carry a `## Deferred Reason` section.** These are sources a run set aside because the decision was one only a person can make, and nobody answered (a non-interactive run, or a person who left the question for later) — a low-density extraction that may be a real page or may be an empty shell, or a type candidate that may or may not suit the subject. Report the count, the paths, and the first line of each reason. **This is a column on the same line, not a line of its own**: a deferral leaves `status` untouched, so every deferred source is already inside one of the rows above — and splitting it out into its own report line would say the same number twice. **Which row depends on the status it kept**, so split the figure the same way Step 17 prints it: a deferral at `pending` is a column on `Unprocessed sources`, and one at `outdated` is a column on `Updated sources`. Do not fold the second kind into the `pending` figures — Pass 1 defers a source at either status, and an `outdated` one has been processed before and carries a `last_generated_at`, so it is in neither the `pending` count nor the never-processed subset of it.

The distinction matters because the two look identical from `status` alone and call for opposite responses: a source that has not come up yet needs nothing but another run, while a deferred one will be deferred again by every non-interactive run until a person answers. Re-run `/wikicommit-generate` with someone present and it asks once its sources have been through the passes; the source is still in the queue, so nothing else is needed to get it back.

**From the same scan again, count the files carrying a non-empty `ambiguous_entities` list, and name the source and each entity's title and candidate types.** This is the same kind of wait one step finer: the source produced pages, so it is at `status: partial` and not in the `pending` population at all, but one entity inside it is held back until a person confirms its type. Report it as its own figure — it does not overlap the counts above, and rolling it in would hide that. Add the route with it, because it is not the same one: `/wikicommit-reconcile --source <path|url>` puts the source back to `pending`, and the next `/wikicommit-generate` picks it up.

**Also count the files at `status: failed` and `status: excluded`, and name them.** They are not in the `pending` population above, so nothing else here would report them.

Keep the "never processed" number restricted to the `pending` files counted above rather than every file with no `last_generated_at`: `wikicommit-generate` Pass 4 writes that field only on its `generated` and `partial` branches, so a `failed` or `excluded` source has none either — but it *has* been processed, it just produced nothing. Counting those inside that number would inflate it and report a finished attempt as work that has not come up yet. That is why they are reported as their own figures above instead.

`wikicommit-merge` Step 9 also raises a tracking Issue for `status: failed` sources (including ones that failed in Pass 1 with an empty `failed_pages`); the counts here are the local half of the same answer, for a wiki that has not run `/wikicommit-merge` yet or does not use GitHub Issues at all.

The never-processed figure is a subset of the `pending` count, not a separate population, and it is the part that matters: a source registered weeks ago and never once processed looks exactly like one registered this morning, while its page may meanwhile have been written from a thinner source.

Unlike `failed_pages`, which `wikicommit-merge` raises as a tracking Issue, a never-processed source is not a failure — it is work that has not come up yet, so counting it here is the whole intervention. A deferral is not a failure either, but it is not merely waiting its turn: counting it is the whole intervention only because the source stays in the queue, and the next run with a person present asks the question that was deferred.

### Step 16: Tally Pages Not Yet Read by a Person

Scan `.wikicommit/entity/**/*.md` **and `.wikicommit/view/**/*.md`** (excluding `index.md` in both) and read each file's frontmatter `review_status` field. Exclude pages with `status: removed` (as with `check_orphans.py` / `check_expires.py`, removed pages are not review targets). Count files with `review_status: pending`, or where the `review_status` field itself is absent (treated as `pending`, same as `validate_frontmatter.py`'s WARNING behavior), and record their paths.

The view tree is included because a view page is written `review_status: pending` like any other generated page, and `wikicommit-merge` Step 9 scans both trees and opens a tracking Issue for it. Counting only the entity tree would report a wiki as fully reviewed while open `wikicommit-review` Issues are outstanding — the exact backlog this tally exists to surface. This differs from `check_orphans.py`'s exclusion of the same tree, which rests on a property of view pages themselves (unlinked at birth) rather than on which fields they carry.

### Step 16.5: Check External Links

`wikicommit-merge` runs lychee only on the pages a batch changes, so a link that breaks after its page was merged is found here and nowhere else.

**Without `--links`**, run once:

```bash
python .wikicommit/scripts/check_external_links.py --last
```

It reads back the last completed check (stored under the Git-ignored `.wikicommit/.cache/lychee/`) and never touches the network. `checked_at=never` in its `SUMMARY:` line means no check has completed on this machine. An `IN_PROGRESS:` line means a check was started with `--links` and not finished.

**With `--links`**, run:

```bash
python .wikicommit/scripts/check_external_links.py
```

and **while it prints a `CONTINUE:` line, run the same command again** — each call checks a few pages per lychee call and returns within about 100 seconds, inside the shell's time limit (Claude Code's Bash defaults to 120 seconds), and the next call continues from where it stopped. Do not raise the shell timeout or run it in the background instead: the point of the short calls is that nothing depends on the time limit. Tell the user how far it has got (`CONTINUE: <checked>/<total>`) between calls on a large wiki. An unfinished check left by an interrupted session is continued, not restarted; pass `--restart` only when the user asks to start over.

Either way, take `checked_at`, `pages`, `broken_links` and `not_checked` from the final `SUMMARY:` line, and keep the `BROKEN_LINK:` lines (`<page>: <url> (<status>)`) and the `NOT_CHECKED:` lines (lychee is not installed, timed out on a batch, or could not run — those pages' links are unknown, not fine). The script exits 0 in every case.

### Step 17: Display Results

Display in the following format:

```
WikiCommit Status
==================
Pages not yet read by a person: <N> (review_status: pending — the AI review is separate, below)
Orphan pages:           <N> (zero inbound links)
Duplicate pages:        <N>
Wanted pages:           <N> (linked but no page exists in any language)
Type-mismatched links:  <N> (slug exists under a different Type — fix the link, do not create the page)
Blocking errors merge does not re-check: <N> (validate_frontmatter.py / check_wikilinks.py / check_raw_html.py ERROR lines on pages already merged)
Expired pages:          <N> (past expires_at)
Stale translations:     <N> (source_commit mismatch)
Missing translation source: <N> (translated_from target doesn't exist)
Untranslated pages:     <N> (no translation yet for a configured target language)
Stale synthesized pages: <N> (derived_from source_commit mismatch)
Missing synthesis source: <N> (derived_from path doesn't exist)
Unprocessed sources:    <N> (status: pending; <D> deferred — waiting on a person, not on a turn)
Never-processed sources: <N> (registered but never generated; <M> not even fetched)
Updated sources:        <N> (status: outdated, source hash mismatch; <D> deferred)
Entities awaiting a type: <N> (ambiguous_entities on a status: partial source — a person confirms the type, then /wikicommit-reconcile)
Failed sources:         <N> (status: failed — extraction or generation produced nothing)
Excluded sources:       <N> (status: excluded — every entity was excluded; a completed outcome, not a failure)
GitHub Actions PR permission: <status>
Unreinforced property-value WikiLinks: <N> (informational — check_property_wikilink_reinforcement.py)
Malformed schema files: <N> findings (<M> in older copies of distributed templates — check_schema_files.py)
Types with no schema file: <N> (pages generated against default.md alone — check_schema_coverage.py)
Recurring plain-text characters: <N> (in 2+ works, no Person page — check_recurring_characters.py)
Unlinked entity mentions: <N> (properties: value naming a page that exists — check_unlinked_entity_mentions.py)
Unused installed types:  <N> (schema file with zero pages — check_installed_type_usage.py)
Possible ancestor-type fallback: <N> (pages on a type whose installed descendant may fit better — check_installed_type_usage.py)
Self-referential tags:  <N> title echoes / <N> type echoes (check_self_referential_tags.py)
Name collisions:        <N> (pages answering to the same title or alias, not yet decided about — check_name_collisions.py; /wikicommit-relate)
Unclassified grouped pages: <N> in <T> grouped Type(s) (<S> stale, <E> unreadable group files — check_groups.py; /wikicommit-organize)
Distribution freshness: <N> outdated / <N> missing / <N> orphan (check_distribution_freshness.py)
Pages on a retracted source: <N> (sources[] names a source a human withdrew — check_retracted_sources.py)
Review coverage:        <A>/<T> pages with a standing AI review, <H> with a standing human one, <N> of those left a note (check_review_coverage.py)
Pages with no standing review: <N> (no AI or human record judges the page as it stands — check_review_coverage.py)
Risky pages:            <N> (retried, or findings raised — the sampling list — check_review_coverage.py)
Stale reviews:          <N> (page text or a source changed after the verdict — check_review_coverage.py)
Reviews on retracted evidence: <N> (check_review_coverage.py)
Last run:               <when> <skill> ([halted: <reason>, ]<elapsed>, <outcome>) — check_run_records.py
Runs that did not finish normally: <N> (never closed, or halted — check_run_records.py)
Runs that skipped a pass: <N> (finished, but a pass left no stamp — check_run_records.py)
Broken external links:  <N> (last checked <checked_at> over <P> pages; <K> NOT_CHECKED notice(s) — check_external_links.py; /wikicommit-status --links)
```

For `Broken external links`, display the `BROKEN_LINK:` lines below the row, then the `NOT_CHECKED:` lines, as they came. `<K>` counts `NOT_CHECKED:` lines, not pages — one line can cover a batch of pages, or every page when lychee is not installed — so do not present it as a page count. When `checked_at=never`, print the row as `Broken external links:  not checked yet (run /wikicommit-status --links)` instead of a 0, which would read as "no broken links". Without `--links`, keep the `last checked <checked_at>` part so the reader can see how old the result is, and add the `IN_PROGRESS:` count when there is one.

For `Blocking errors merge does not re-check`, `<N>` is the number of `ERROR:` lines from the three Step 3 checks together; when it is 1 or more, display those lines below the row as they came — each already names its page and what is wrong.

For any category with 1 or more hits, display the list of matching file paths directly below that category — with three exceptions, which have no per-page paths to list: for `Unreinforced property-value WikiLinks` display the `UNREINFORCED:` lines, for `Types with no schema file` display the `UNCOVERED:` lines (`check_schema_coverage.py` emits no `page:` lines at all — each `UNCOVERED:` line carries a page count and one example path for that type), and for `Recurring plain-text characters` display the matching `RECURRING:` lines (each already names the works the name was found in). `Unlinked entity mentions` does have `page:` lines, so it follows the normal rule — list the referring page paths, each with its `UNLINKED:` line. The two Step 9 categories have no `page:` lines either — display the matching `UNUSED:` / `ANCESTOR_FALLBACK:` lines. `Malformed schema files` is the same: display the finding lines themselves, each of which already names its file and that file's `provenance`. So is `Name collisions`: display the `COLLISION:` lines. And `Unclassified grouped pages`: display the `TYPE:` and `ERROR:` lines. Omit the row entirely when Step 10 reported `types=0` and `errors=0` — the wiki groups no Type, and a row of zeros would be on for every wiki that never uses groups.

The six Step 15 rows all come from that step's single scan of `.wikicommit/source/`. The two `<D> deferred` columns are subsets of the rows they sit on, not additions to them — print the column even when it is 0, since a reader cannot tell "none deferred" from "this build does not report deferrals" otherwise — and below each row that has one, list the deferred paths with the first line of each `## Deferred Reason`, so the reason a person is needed is visible without opening the file. For `Entities awaiting a type`, list the source path and, under it, each entity's title and candidate types, and name the route (`/wikicommit-reconcile --source <path|url>`, then the next `/wikicommit-generate`) — it is not the route the deferred columns take, and saying so is why it is a row of its own rather than a third column. For `Failed sources` and `Excluded sources`, list the paths, and for a failed one the first line of its `## Failure Reason`.

For `Distribution freshness`, display the `VERSION:` line and then the matching `OUTDATED:` / `MISSING:` / `ORPHAN:` lines — this check has no `page:` lines either, and each of its lines already names the path and says what is wrong with it.

`Pages on a retracted source` does have `page:` lines, so it follows the normal rule — list the affected page paths, each with its `RETRACTED_SOURCE:` line, since that line carries the two things needed to decide what to do: which retracted source the page still names, and how many sources it has left.

The five review-coverage rows all come from Step 13's single run. `Review coverage` is not a count of problems — take `<A>`, `<T>`, `<H>` and `<N>` from its `SUMMARY:` line (`ai_reviewed`, `pages`, `human_reviewed`, `human_notes`) and display the `COVERAGE:` lines underneath it, one per model, since the per-model split is the whole reason the denominator is worth printing. The other four rows are counts of the `UNREVIEWED:` / `RISKY:` / `STALE_REVIEW:` / `RETRACTED_EVIDENCE:` lines; for any of them with 1 or more hits, display those lines directly below the row (each already names its page and, where it applies, what changed). When Step 13 printed the `NOTE: .wikicommit/review/ does not exist yet` line instead, display that note in place of all five rows — the wiki predates review recording, and reporting `0/0` there would read as "nothing to review" rather than "nothing recorded yet".

**`Pages with no standing review` and `Pages not yet read by a person` sound alike and are not the same count** — they sit far apart in the output and are easily read as one thing, so whenever both rows are printed, say which is which. Do not make that conditional on the two differing or on either being non-zero — two rows carrying the same number look even more like one number, so those are exactly the cases being confused. The first asks whether *any* record — AI or human — judges the page's current text, so a page the machine reviewed at generation and nobody has touched since does not count toward it. The second asks only whether a **person** has read it (`review_status`), and is expected to be large: the AI review is every page, the human one is a sample. Neither gates the healthy verdict.

The three run rows come from Step 14's single run. `Last run` is not a count either — display its `LAST_RUN:` line's content, or `none recorded` when Step 14 printed a `NOTE:` instead. When that run halted, its line starts with `halted: <reason>` — keep that phrase rather than reducing the row to an elapsed time and an outcome, or a run that stopped itself reads as one that merely took five minutes. For `Runs that did not finish normally`, display the `INCOMPLETE_RUN:` lines below the row when there are any. That row counts two different things — a run that was never closed, and one that stopped itself on purpose — and each line says which it was, so pass them through rather than summarizing. For `Runs that skipped a pass`, take `<N>` from the `SUMMARY:` line's `missing_pass=` and display the `MISSING_PASS:` lines below the row when there are any — and only then, add one sentence saying this is a prompt to look rather than a defect: a run whose sources were all blocked or all already current has nothing for the later passes to do, and a dropped stamping instruction makes a pass that did run look skipped. A line saying a run stamped **no** pass at all is the strongest form of this one, not a milder one — it means every stamping instruction went missing — so do not summarize it away; show it as it came. Do not print that sentence when the count is 0, or it becomes a line that is always on and stops being read. `Last run` prints one record only, so a run that skipped a pass will often not be the one shown there — that is why this row stands on its own. Say alongside all three that these records are local to this checkout and are not committed, so zeros here mean "nothing recorded on this machine" rather than "nothing has been run".

`GitHub Actions PR permission` is not a count — display Step 4's `OK:`/`WARNING:` line verbatim as `<status>` (e.g. `OK: acme/example-wiki: "Allow GitHub Actions to create and approve pull requests" is enabled`, or the full `WARNING: ...` message including the enable command). Skip this line entirely when `SUMMARY: enabled=n/a` (repository doesn't use `review-issue-close-sync.yml`).

If every category above is 0 **and** `enabled` is `true` or `n/a`, display "Wiki is healthy" instead of the above (a `false`/`unknown` permission state blocks the "healthy" verdict even when every page-level category is clean, since it silently breaks the review-close automation). Not every row counts toward that verdict:

- **Every row gates it** (must be 0) **unless it is listed under the next bullet.** Three that do gate are worth stating, because they sit beside rows that do not:
  - `Type-mismatched links` gates it even though it sits next to `Wanted pages`: the page already exists under another Type, the error is one word in one link, and it can and should be 0.
  - `Failed sources` gates it on the same footing as `Unprocessed sources`: a source that produced nothing is work the wiki still owes, with a concrete route out (re-run `/wikicommit-generate` naming it, or fix what `## Failure Reason` names).
  - `Blocking errors merge does not re-check` gates it: each line is a page that would fail `wikicommit-merge` the next time it is changed, the fix is named in the line, and a wiki whose pages all still pass reaches 0.
  - `Types with no schema file` gates it: a non-zero count means a type definition is not being applied at all, it is 0 on a repository whose schema files match the types it uses, and the fix is concrete (add the file, or move it back out of a subdirectory).
- **Rows that do not gate it**, each for the reason given:
  - `Pages not yet read by a person` — `reviewed` means a person read the page, and **the AI review is every page and the human one is a sample**, so requiring 0 would require 100% human review. It reports a state of reach, not a defect; machine-side coverage is the separate review-coverage rows.
  - `Wanted pages` — a wanted link is a page this wiki would like to have; requiring 0 pushes toward avoiding the WikiLink or writing a page the sources do not support.
  - `Unreinforced property-value WikiLinks` — purely informational (Step 5) and, per the `description` caveat, almost never 0 with the standard templates, so gating on it would make the verdict unreachable.
  - `Recurring plain-text characters` and `Unlinked entity mentions` — generation-time judgment calls (`Person.md`'s `granularity`; `validate_frontmatter.py` deliberately does not enforce `properties:` value shape); a standing count is a backlog to look at, not a defect.
  - The two Step 9 categories and `Self-referential tags` — judgment prompts, not defects; `ANCESTOR_FALLBACK` is expected to be non-zero on any wiki that installs a descendant type at all.
  - `Name collisions` — whether pages sharing a name are one concept is a person's call; a decision recorded with `/wikicommit-relate`, whatever it is, takes the pair off the list.
  - `Unclassified grouped pages` — grouping is how pages are listed, not whether they are sound; new pages wait unclassified by design until a person groups them.
  - `Pages on a retracted source` — a human chooses between removing, regenerating and fixing the page, and none of those is automatically right.
  - `Distribution freshness` — it describes how current the installation is, not whether the content is sound; a wiki can be healthy a version behind.
  - `Malformed schema files` — same reason, plus the count is usually dominated by `provenance: default` findings (an older template copy, not a mistake here), and the rest are a person's judgment about a file no Skill may touch. Read `in_distributed_templates` (Step 5) rather than the total.
  - The three run rows — they describe how the wiki was operated, and since the records are not committed, a fresh clone would otherwise be barred by an absence that means "not recorded here". `Runs that skipped a pass` is also an observation rather than a defect (Step 14).
  - The five review-coverage rows — they measure how much reviewing has been recorded, there is deliberately no coverage threshold (Step 13), and a wiki predating the record tree would otherwise be barred forever by an absence that means "not recorded", not "not reviewed".
  - `Excluded sources` — every entity being off-subject or outside `entity-policy.md` is a completed, correct outcome of this wiki's policies; a narrow `theme` can leave a standing non-zero count on a healthy wiki.
  - `Entities awaiting a type` — which type fits a subject is a person's call, and the count stands until they make it.
  - `Broken external links` — lychee's findings were never blocking (`wikicommit-merge` treats them as warnings), a timeout or a 403 depends on the network the check ran from, and the result read back without `--links` can be days old; a dead external site is also not something the wiki can always fix.
- The `<D> deferred` columns are neither: they add nothing of their own — they are subsets of rows already counted, so a deferral gates the verdict exactly as far as the `pending` or `outdated` row it sits on.

### Step 18: Cleanup Guidance

If the `outdated` count in Step 3's `check_ingest_freshness.py` `SUMMARY:` line is 1 or more (whether newly rewritten this run or already `outdated` before), append the following guidance:

```
Some .wikicommit/source/ management files have status: outdated (either just rewritten by this run,
or already in that state — either way, this is a local change only and will show up in git status).
Run /wikicommit-merge to commit it.
```

## Notes

- Do not commit or create a PR against `main` or any branch
- Do not write to `.wikicommit/schema/`
- No script other than `check_ingest_freshness.py`, and no part of the Step 3 / Step 15–16 scans, has side effects (read-only). The three blocking checks added to Step 3 (`validate_frontmatter.py`, `check_wikilinks.py`, `check_raw_html.py`) are read-only as well; their exit 1 is a finding, not an error of this skill. `check_actions_pr_permission.py` (Step 4), `check_property_wikilink_reinforcement.py` and `check_schema_files.py` (Step 5), `check_schema_coverage.py` (Step 6), `check_recurring_characters.py` (Step 7) and `check_unlinked_entity_mentions.py` (Step 8) and `check_installed_type_usage.py` (Step 9) and `check_self_referential_tags.py`, `check_name_collisions.py` and `check_groups.py` (Step 10) and `check_distribution_freshness.py` (Step 11) and `check_retracted_sources.py` (Step 12) and `check_review_coverage.py` (Step 13) and `check_run_records.py` (Step 14) are read-only too, and so is `check_external_links.py` (Step 16.5) as far as the repository goes — it writes only its progress, its last result and lychee's `.lycheecache` under the Git-ignored `.wikicommit/.cache/lychee/`, shared with `wikicommit-merge` — unlike `wikicommit-init`'s Step 3, `check_actions_pr_permission.py` never attempts to enable the GitHub Actions PR permission setting itself, only reports its current state
