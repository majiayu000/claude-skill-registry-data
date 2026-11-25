---
name: reprocess-meetings
description: >
  Reprocess a day's meetings against a folder of meeting exports the user
  supplies: add meetings the vault is missing, append transcript segments the
  vault transcripts missed or garbled, fold the new facts into the summaries,
  then update the files the daily workstream update produces for that day.
  Use when asked to "reprocess yesterday's meetings", "reprocess meetings",
  "fill in missing calls", "improve yesterday's meetings and notes", or invokes
  /reprocess-meetings.
argument-hint: "[YYYY-MM-DD]"
---

# Reprocess Meetings Skill

Target date `D` = the argument, or the previous weekday if none is given.
`D-dashed` = `YYYY-MM-DD`, `D-dotted` = `YYYY.MM.DD`.

Helper script (run from the repo root, always with bytecode off):

```bash
export PYTHONDONTWRITEBYTECODE=1
H=.pi/skills/reprocess-meetings/reprocess_meetings.py
python3 $H -h
```

## Rules for every step

- **Ask for the export folder at the start.** Do not guess it and do not reuse
  one from memory. Pass it as `--source`.
- **Never name the export tool or folder** in any vault file or commit message.
  Call additions "reprocessed", never "enriched", "supplemented", or "imported".
  Do not add per-bullet source markers; new facts read as normal content.
- **Leave out off-topic personal remarks**, especially comments about
  colleagues, with `--skip`. List what you skipped in the final report.
- **Stage explicit paths.** Do not use `git add -A` until the daily workstream
  steps (they use `git-publish`); check `git status --short` before each commit.

---

## Step 1 — Ask and scan

1. Ask the user for the export folder path (use `ask_user_question` so they can
   type it). Confirm `D`.
2. Run:
   ```bash
   python3 $H scan --source "<folder>" --date D
   ```
   Each export is reported as one of:
   - `MATCH <vault transcript>`: paired; shows offset, speaker map, and segment
     counts. `(already reprocessed)` means an earlier run already did it.
   - `NO MATCH`: the vault lacks this meeting; handle in Step 3.
   - `SHORT`: almost no speech. Skip it unless it holds work content.
   - `vault only`: a vault meeting with no export. Nothing to do.
3. Sanity-check each speaker map (names should match the vault transcript's
   participants). If a pairing looks wrong, say so and stop.

## Step 2 — Append reprocessed segments

1. Dry run, then read every listed segment:
   ```bash
   python3 $H merge --source "<folder>" --date D
   ```
   Segments are speech the vault transcript lacks: accented or cross-talk speech
   it garbled, and speech before it started or after it ended.
2. Write, skipping personal or off-topic lines by export file and export time:
   ```bash
   python3 $H merge --source "<folder>" --date D --write \
     --skip "<export file>@MM:SS" ...
   ```
   This appends a `## Reprocessed Segments` section to each paired transcript.
   Transcripts that already have one are left alone.
3. For each transcript that changed, read its new section and its summary in
   `02.Meetings/summaries/`. Add facts that are new (names, numbers, systems,
   decisions, owners) to the matching `### Topic (MM:SS - MM:SS)` block. Speech
   after the transcript ended gets its own short topic block. Update the
   `description:` only if a new fact changes the meeting's gist. Do not touch
   frontmatter dates. If nothing new surfaced, leave the summary as it is.

## Step 3 — Add missing meetings

For each `NO MATCH` export worth keeping:

1. **Title**: reuse the vault name of a recurring meeting (check
   `ls 02.Meetings/transcripts | grep -i <keyword>`, e.g. `RoarAIMobElaboration`,
   `Roar - Stand-up`, `ArchOfficeHours`). Otherwise a short CamelCase title.
2. **Type slug**: `daily-sync` for stand-ups, otherwise `technical-refinement`.
3. **Speakers**: map generic labels (`Speaker 1`) to real names from the
   content: people addressed by name, roles, topics, and same-day summaries.
   Map short names to the vault's spelling (`Jorge` → `Jorge Luis Cameo`,
   `Jose Miranda` → `Jose Miranda (JAM)`).
4. **Time**: pass `--when "HH:MM AM"` only if you actually know it.
5. Convert:
   ```bash
   python3 $H convert --source "<folder>" --date D --file "<export file>" \
     --title "<Title>" [--type daily-sync] [--when "11:00 AM"] \
     --speaker "Speaker 1=Katie Portnoy" ... [--skip MM:SS ...]
   ```
   Re-run with `--force` to fix a mapping.
6. Write `02.Meetings/summaries/<D-dotted>.<Title>.Summary.md` in this session,
   following `.pi/skills/process-root-transcripts/SKILL.md` Step C: same
   frontmatter, `## General Summary` with timed topic blocks, `## Action Items`
   as `- **Owner**: action *(MM:SS)*`. If you inferred speaker names, add the
   line `> Speaker names inferred from context.` under the date line. For a
   fragmentary capture, write a short summary and `- None captured.`

## Step 4 — Commit the meetings

```bash
git add "02.Meetings/transcripts/<D-dotted>.<Title>.Transcript.md" "02.Meetings/summaries/<D-dotted>.<Title>.Summary.md"
git commit -m "Add <D-dashed> <Title> transcript and summary"      # one per new meeting
git add 02.Meetings/transcripts 02.Meetings/summaries
git commit -m "Reprocess <D-dashed> transcripts and summaries"     # body: list the files
git push
```

---

## Step 5 — Update the daily workstream files for D

Read `00.Tasks/Workstreams.SubTasks.Hierarchies.md` for workstream names.
Changed meetings = the new summaries from Step 3 plus summaries edited in
Step 2.

1. **Daily summary** `00.Tasks/Daily.Summary/<D-dotted>.WorkstreamUpdates.Summary.md`.
   If it does not exist, run the `daily-workstream-update` skill for `D` and
   skip to item 4. Otherwise edit it in place:
   - Add each new meeting's wikilink to the `> Source meetings:` line of every
     section it feeds, and add its bullets and action items
     (`*(<Title>, MM:SS)*`) to those sections.
   - A workstream with no section yet gets one, named exactly as in the
     hierarchies file and placed in alphabetical order.
   - Add facts from reprocessed segments to the existing bullets they belong to.
   - Add a sentence to the intro paragraphs for any meeting that changes the
     day's story.
2. **Workstream files**: mirror every section you changed or added:
   ```bash
   python3 $H sync-entry --date D "<Workstream>" ...
   python3 05.Scripts/daily_workstream_update.py verify --date D
   ```
   `sync-entry` rebuilds the `### D-dashed` entry from the daily summary and
   keeps any `##### Daily Notes` block. Fix every `MISSING`, `RENAME`, or
   `UNKNOWN` line as the `daily-workstream-update` skill describes, then:
   ```bash
   python3 05.Scripts/daily_workstream_update.py git-publish "Daily workstream summary <D-dashed>: <what changed>"
   ```
3. **Daily note**: no action. The daily note was copied when the day was first
   processed.
4. **Project decisions**: for each new summary only (not the edited ones,
   whose decisions already exist), one at a time:
   ```bash
   python3 .pi/skills/project-decisions/extract_decisions.py process "$PWD/02.Meetings/summaries/<file>"
   ```
   Then read the new entries under `## D-dashed` in `00.Tasks/PROJECT_DECISIONS.md`.
   Delete entries that are open questions, proposals, or bare option numbers
   ("Option 2 selected for Q2"), and reword vague ones. Publish:
   `git-publish "Update project decisions <D-dashed>: <meetings>"`.
5. **Action items**: for each new action item that Guilherme Bencke owns or
   co-owns (matching rules in the `daily-workstream-update` skill, Step E):
   ```bash
   python3 .pi/skills/action-items/action_items.py search "<key phrase>"   # skip if already there
   python3 .pi/skills/action-items/action_items.py add "(with <co-owner>) <action>" \
     --meeting "<Title>" --time "MM:SS" --date "D-dashed" --subtopic "_Sub.Topic"
   ```
   Pick the sub-topic from `00.Tasks/Topics/All Sub-Topics.md`. Publish:
   `git-publish "Update action items <D-dashed>: <what>"`.
6. **Topic files**: for each `00.Tasks/Topics/**/_*.md` sub-topic the new
   meetings touch, add decision rows at the top of `## Decisions` and a meeting
   bullet in `### Meetings` (newest meeting time first, skip links already
   there), following `daily-workstream-update` Step F. Publish:
   `git-publish "Update topic decisions and meetings <D-dashed>: <meetings>"`.

---

## Final report

- Export folder: say only "scanned N exports" (do not print the path).
- Meetings added: title, type, whether speakers were inferred.
- Transcripts reprocessed: segment count each; summaries updated.
- Skipped: `SHORT` exports, and `--skip` lines with the reason.
- Daily workstream: sections and workstream files changed; decisions added and
  removed; action items added (with sub-topic); topic files updated.
- Commits pushed (list messages). Say so if any publish had nothing to commit.
