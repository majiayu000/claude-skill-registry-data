---
name: daily-workstream-update
description: >
  Run the daily workstream update workflow for the Obsidian vault. Generates
  today's workstream summary from meeting summaries, syncs individual workstream
  files, copies daily-note entries into workstream files, updates
  PROJECT_DECISIONS.md, ACTION_ITEMS.guilherme_bencke.md, and the Decisions
  tables in all Topics subtopic files, then publishes to git.
  Use when asked to "run daily workstream update", "generate daily summary",
  "sync workstreams", "update workstream files", or invokes /daily-workstream-update.
argument-hint: "[YYYY-MM-DD]"
---

# Daily Workstream Update Skill

Runs the `/daily-workstream-update` workflow for the Obsidian vault at
`/home/gbencke/git.work/331.obsidian-scripts`.

Today's date (or the argument provided) is the target date `D`.
If no argument is given, use today.

Helper script for all mechanical operations:

```bash
python3 05.Scripts/daily_workstream_update.py <subcommand> [--date D]
```

Available subcommands: `today`, `meetings`, `workstreams`, `hierarchies-path`,
`daily-summary-path`, `daily-note-path`, `workstream-file <name>`,
`list-workstream-files`, `verify`, `move-daily-summary`,
`git-publish "<msg>"`.

Run `python3 05.Scripts/daily_workstream_update.py -h` to recheck at any time.

Use the script for every date / path / file-listing / verification / git
operation. Do not hand-roll those.

---

## Step A — Generate today's workstream summary

1. Resolve the date:
   ```bash
   python3 05.Scripts/daily_workstream_update.py today [--date D]
   ```
2. List today's meeting summaries:
   ```bash
   python3 05.Scripts/daily_workstream_update.py meetings --date D
   ```
   If the list is empty, stop and tell the user there are no meetings for `D`.
3. Read the workstream reference:
   ```bash
   python3 05.Scripts/daily_workstream_update.py workstreams
   ```
   This is `00.Tasks/Workstreams.SubTasks.Hierarchies.md`.
4. Read the most recent existing file in `00.Tasks/Daily.Summary/` (sorted by
   date) — this is the **formatting model**. Match its frontmatter, heading
   hierarchy, source-meeting wikilinks, "What was discussed" / "Action Items"
   sections, and `---` separators exactly.
5. Read each meeting summary file from step 2 in full.
6. Write `<repo-root>/<D>.WorkstreamUpdates.Summary.md` (at the repo root, not
   yet in `00.Tasks/Daily.Summary/`). Include a `## <Workstream Name>` section
   **only** for workstreams from the hierarchies reference that were actually
   discussed in today's meetings. Use the exact workstream names from the
   hierarchies file as the `## ` headings — never an older name or a workstream
   file's alias (e.g. `## SchedulerIQ - Scope.Open.Beta`, not
   `## SchedulerIQ - Open Beta`). Write **one** section per workstream: if
   content fits two headings that are the same workstream, merge it into one.
   Content that fits no workstream row (one-off intake or refinement items)
   goes under the closest workstream, not under a new ad-hoc heading.
7. Move the file into place:
   ```bash
   python3 05.Scripts/daily_workstream_update.py move-daily-summary --date D
   ```

---

## Step B — Verify workstream files contain today's entry, then publish

1. Run:
   ```bash
   python3 05.Scripts/daily_workstream_update.py verify --date D
   ```
2. For every `MISSING` line: open the workstream file shown and add a new
   `### <D-dashed>` section directly under the `#workstream/...` tag line (as
   the newest entry). Use the same per-day structure already in that file:
   `##### Meetings` block with summary + source links, body bullets grouped by
   topic, `##### Action Items`. Pull content from the corresponding
   `## <Workstream>` section in the daily summary produced in Step A. End the
   new section with a `---` separator before the previously-newest section.
3. For every `RENAME` line: the heading resolves (via an alias) but is not the
   hierarchies name. Rename the `## ` heading in the daily summary to the name
   shown. If that creates two sections with the same heading, merge them:
   combine the `> Source meetings:` lines (dedupe), the "What was discussed"
   bodies, and the action items.
4. For every `UNKNOWN` line: no workstream file matches that heading.
   - If the heading is a row in the hierarchies file, create the missing file
     as `00.Tasks/WorkStreams/<Product>/<Workstream Name>.md` (exact row name)
     with frontmatter `category: workstream`, `description`, `creation`,
     `last updated`, `product`, `status: open`, then a
     `#workstream/<product>/<workstream-slug>` tag line. Re-run `verify`; it
     now reports `MISSING`, which step 2 fills.
   - Otherwise it is an ad-hoc heading: move its content under the closest
     hierarchies workstream (step A.6). Only if nothing fits, print a short
     note for the user.
5. Re-run `verify` until it exits clean (only `OK` lines and any genuinely
   unresolvable `UNKNOWN` cases).
6. Publish:
   ```bash
   python3 05.Scripts/daily_workstream_update.py git-publish "Daily workstream summary <D-dashed>"
   ```

---

## Step C — Copy daily-note workstream entries into workstream files

1. Get today's daily note path:
   ```bash
   python3 05.Scripts/daily_workstream_update.py daily-note-path --date D
   ```
2. **Re-read** that file from disk now — the user may have updated it since
   this run started. Do not rely on cached content.
3. The daily note is organised as `### <Section Name>` blocks. For each section:
   - Map the section name to a workstream from the hierarchies reference (names
     are usually close but not identical — e.g. `### NewGen Performance` →
     `NewGen - Performance.Improvements`). Skip and note any section with no
     clear workstream mapping.
   - Resolve the workstream file:
     ```bash
     python3 05.Scripts/daily_workstream_update.py workstream-file "<workstream name>"
     ```
   - In that workstream file, locate today's `### <D-dashed>` section (created
     in Step B). Append a new block at the end of that day's section, **before**
     the closing `---` separator:
     ```markdown
     ##### Daily Notes
     <verbatim contents of the daily-note section, preserving checkboxes, links, and formatting>
     ```
   - If a `##### Daily Notes` block already exists for today, append the new
     bullets inside it rather than creating a duplicate heading.
4. Re-read the daily note after all edits to confirm nothing was missed.
5. Publish:
   ```bash
   python3 05.Scripts/daily_workstream_update.py git-publish "Copy daily-note workstream entries <D-dashed>"
   ```

---

## Step D — Update PROJECT_DECISIONS.md

Process all of today's meeting summary files through the decisions extractor.

1. Get the list of today's summaries (same list from Step A, step 2).
2. For each file, run:
   ```bash
   python3 /home/gbencke/git.work/331.obsidian-scripts/.pi/skills/project-decisions/extract_decisions.py \
     process "<full-path-to-summary>"
   ```
   Run files one at a time — do not batch them into a single call.
3. Verify the new entries landed:
   ```bash
   head -80 /home/gbencke/git.work/331.obsidian-scripts/00.Tasks/PROJECT_DECISIONS.md
   ```
4. Publish:
   ```bash
   python3 05.Scripts/daily_workstream_update.py git-publish "Update project decisions <D-dashed>"
   ```

---

## Step E — Update ACTION_ITEMS.guilherme_bencke.md

Extract every action item that **Guilherme Bencke** owns or co-owns from today's
daily summary (the file written in Step A) and add each one to the action-item
log.

1. Read the daily summary from `00.Tasks/Daily.Summary/<D>.WorkstreamUpdates.Summary.md`.
2. Collect every bullet under `### Action Items` blocks whose leading **bold
   owner annotation** names Guilherme Bencke — whether he is the sole owner or
   one of several co-owners. The owner list is the run of bold text at the start
   of the bullet, before the `:` or `—` that introduces the action text. Match
   all of these forms:
   - Sole owner: `- **Guilherme Bencke**: ...` or `- **Guilherme Bencke** — ...`
   - Co-owners in one bold, any position, any joiner (`/`, `&`, `,`):
     `- **Guilherme Bencke / Marleny Patsi**: ...`,
     `- **Javed Nurani / Guilherme Bencke / Enrique Ortuno**: ...`,
     `- **Noemi Antezana, Guilherme Bencke**: ...`,
     `- **Guilherme Bencke & Robert Lupinek** — ...`
   - Co-owners as separate bold segments:
     `- **Guilherme Bencke** / **Anura Adikari**: ...`
   - A bare `**Guilherme**` when it clearly refers to him
     (e.g. `- **Anura / Guilherme** — ...`).

   Do **not** require the bold to close immediately after "Bencke", and do
   **not** require a colon — the em-dash (`—`) separator is equally valid. Skip
   a bullet only when its owner list contains no Guilherme.

   For each matched item capture:
   - The action text: everything after the separator (`:` or `—`) that follows
     the owner list, up to the trailing meeting source annotation. When the item
     is co-owned, prefix the text with the co-owners in parentheses so the log
     records that it is shared — e.g. `(with Marleny Patsi) Deploy the
     visit-plan config fix ...`.
   - The meeting name and timestamp from the trailing `*(Meeting, HH:MM)*`
     annotation.
3. For each item, call:
   ```bash
   python3 /home/gbencke/git.work/331.obsidian-scripts/.pi/skills/action-items/action_items.py add \
     "ACTION TEXT" \
     --meeting "Meeting Name" \
     --time "HH:MM" \
     --date "YYYY-MM-DD" \
     --subtopic "_Sub.Topic"
   ```
   `--subtopic` is **required on every call**. Read
   `00.Tasks/Topics/All Sub-Topics.md` once before adding items, then pick the
   sub-topic whose description best matches the action (e.g. prior auth →
   `_Authorization.PriorAuth`, credentialing → `_Provider.Credentialing.Disciplines`,
   contract validation → `_Security.Reliability`). Pass `—` only when no
   sub-topic fits (team management, hiring, one-off production tickets). The
   script rejects unknown names; on that error, fix the name and retry — do not
   fall back to `—`. The script keeps each date's table sorted by sub-topic.
   Skip any item whose text already appears verbatim in the file (run
   `search` first if unsure).
4. Confirm additions:
   ```bash
   python3 /home/gbencke/git.work/331.obsidian-scripts/.pi/skills/action-items/action_items.py show --days 1
   ```
5. Publish:
   ```bash
   python3 05.Scripts/daily_workstream_update.py git-publish "Update action items <D-dashed>"
   ```

---

## Step F — Update Decisions tables and Meetings lists in Topics subtopic files

Every `_*.md` file under `00.Tasks/Topics/` contains a `## Decisions` table and
a `### Meetings` list. For each subtopic relevant to today's meetings, append
new decision rows **and** prepend the day's meeting bullets to its `### Meetings`
list.

### F.1 — Enumerate subtopic files

```bash
find /home/gbencke/git.work/331.obsidian-scripts/00.Tasks/Topics -name "_*.md" | sort
```

### F.2 — Map file to meetings

For each subtopic file:

1. Read its YAML frontmatter: `product`, `workstream`, `description`, `tags`.
2. Cross-reference against the daily summary sections (Step A output). A file
   is relevant to a meeting section when:
   - Its `product` + `workstream` pair maps to a `## <Workstream>` section in
     the daily summary (fuzzy match — e.g. `product: PlatformSync`,
     `workstream: Performance` → `## PlatformSync - Performance Improvements`),
     **or**
   - Its `description` or `tags` overlap significantly with the meeting content.
3. If no section in the daily summary touches this file's topic, skip it.

### F.3 — Extract and insert decisions

For each relevant subtopic file:

1. Read the full meeting summary files that fed the matching daily-summary
   section.
2. Identify decisions relevant **specifically** to this subtopic's scope (not
   all decisions from the meeting — only those whose subject matter falls within
   the file's `description`).
3. Format each decision as:
   ```
   | YYYYMMDD | *[Category]* **Decision statement** — one-sentence rationale *(MeetingName)* |
   ```
   - `YYYYMMDD` — date with no separators (e.g. `20260608`).
   - `Category` — one of: `Architectural`, `Technical`, `Team Management`,
     `Project Management`, `Process`, `Security & Compliance`,
     `Cost & Governance`.
   - Statement — 3–12 words summarising the choice made.
   - Rationale — one sentence explaining why.
   - MeetingName — short name matching how other entries in that file cite
     meetings (e.g. `PlatformSyncMapping`, `WarRoom`, `TeamDaily`).
4. Insert the new rows **at the top** of the `## Decisions` table, immediately
   after the header row:
   ```markdown
   ## Decisions

   | Date       | Decision |
   | ---------- | -------- |
   | 20260608 | *[Technical]* **New decision** — rationale *(Meeting)* |   ← new rows here
   | 20260605 | *[Architectural]* **Older decision** ...                    ← existing rows
   ```
5. Update the `last updated` frontmatter field to `D` (dashed format:
   `YYYY-MM-DD`).
6. Do not modify any section other than `## Decisions`, `### Meetings`
   (see F.3.5), and the `last updated` frontmatter field.

### F.3.5 — Update the `### Meetings` list

Each subtopic file also has a `### Meetings` section: a newest-first list of
`- [[<YYYY.MM.DD>.<Name>.Summary|<Short Alias>]] — <one-line description>`
bullets. For every subtopic you touched in F.3, prepend a bullet for each of
today's meetings relevant to that subtopic (the same meetings whose decisions
you just added):

1. Format each bullet as
   `- [[<YYYY.MM.DD>.<Name>.Summary|<Short Alias>]] — <one sentence on what was
   discussed that is relevant to this subtopic>`. Match the link/alias/em-dash
   style already used in that file's list.
2. Insert the new bullet(s) at the **top** of the `### Meetings` list (newest
   first). If a subtopic saw more than one meeting today, order them by meeting
   time, latest first.
3. Skip any meeting whose link (`[[<YYYY.MM.DD>.<Name>.Summary`) already appears
   in the list — the insert is idempotent.
4. If the list holds only a `- _None yet._` placeholder, replace it.

### F.4 — Publish

After all subtopic files have been updated (decisions and meetings):

```bash
python3 05.Scripts/daily_workstream_update.py git-publish "Update topic decisions and meetings <D-dashed>"
```

---

## Keeping names, files, and indexes aligned

These rules apply whenever a run (or the user) adds or renames a workstream or
sub-topic.

- **Hierarchies file is canonical.** `00.Tasks/Workstreams.SubTasks.Hierarchies.md`
  has one row per `00.Tasks/Topics/<Product>/<Workstream>/` folder. Every row
  needs a workstream file in `00.Tasks/WorkStreams/<Product>/` whose name
  resolves to it (`workstream-file "<row name>"` must succeed).
- **New sub-topic** (`_*.md`): add a row to `00.Tasks/Topics/All Sub-Topics.md`
  and update its counts line; mention it in the workstream's description in
  the hierarchies file. A new workstream folder also needs a hierarchies row
  and a workstream file (template in Step B.4).
- **Renaming a workstream file:** use `git mv`, add the old name under
  `aliases:` in the file's frontmatter (the script and Obsidian both resolve
  aliases), rewrite `[[Old Name]]` links, rename `## Old Name` headings in
  `00.Tasks/Daily.Summary/`, and rewrite `[[<D>.WorkstreamUpdates.Summary#Old Name|…]]`
  anchors in workstream files. Then run `verify` over every daily summary; it
  must report no `RENAME` or `MISSING` lines.
- **Moving content between sub-topics:** move the matching `### Meetings`
  bullets and `## Decisions` rows, add a "tracked in [[_New.Subtopic]]" pointer
  in the old file, and re-tag affected rows in `ACTION_ITEMS.guilherme_bencke.md`.

---

## Final Report

After all six steps, print a concise summary:

- Daily summary written to: `00.Tasks/Daily.Summary/<D>.WorkstreamUpdates.Summary.md`
- Workstream files updated in Step B: list each
- Daily-note sections copied in Step C: `<section> → <workstream>`
- PROJECT_DECISIONS.md: N new decisions added across M meetings
- ACTION_ITEMS: N items added (owned or co-owned by Guilherme Bencke), with the
  sub-topic chosen for each (flag any that got `—`)
- Topics subtopic files updated: list each file, how many decisions were added,
  and how many `### Meetings` bullets were added
- Headings fixed for `RENAME` and workstream files created for `UNKNOWN`
- Anything skipped or unresolved (`UNKNOWN` workstreams, daily-note sections
  with no obvious workstream mapping, subtopic files with no relevant meeting
  content)
- Commits pushed: list each commit message

If any `git-publish` reports "nothing to commit", say so explicitly — that
means there was nothing new to write for `D`.
