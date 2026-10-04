---
name: meeting
description: Capture meeting transcripts (voice memo, Craig recording, Fathom URL, paste-in-chat) and distribute extracted decisions, action items, and key quotes to the right ZAO surfaces - cowork-zaodevz actions.json, a research/events/NNN-* recap doc, the ZABAL Bonfire knowledge graph, a meetings index, Telegram copy-paste block, memory, and calendar. Use when the user just finished a meeting, shares a recording or transcript, says "process this call", "extract todos from this", "recap that meeting", or types "/meeting <path-or-url>". Always fires on meeting context - undertriggering wastes the capture.
allowed-tools: Read Write Edit Bash WebFetch Skill AskUserQuestion
---

# /meeting - ZAO Meeting Capture

Turn any meeting recording or transcript into:
- Action items in the right project's tracker (unified Supabase cowork tracker, ZAOstock bot - routed in Phase 0)
- A research recap doc in `research/events/NNN-<slug>/README.md` (always ZAOOS, per doc 673)
- A row in `research/events/_meetings-index.md` - the one canonical list of every past meeting
- A copy-paste Telegram bubble for sharing
- A next-actions clipboard page the moment the meeting ends (Phase 6)
- Episodes posted to the ZABAL Bonfire knowledge graph - always-on, so the graph always has full meeting context (doc 680)
- Optional memory write, calendar update

One command, multiple inputs, project-routed output targets. User-gated per run.

Doc 673 has full design + decisions. Read it if context is needed beyond this file.

## When to fire

- Zaal pastes a transcript, meeting notes, or "Iman just said X, Y, Z" dump
- Zaal types `/meeting <path-or-url>`
- Zaal says "I just had a call with...", "process this recording", "extract todos from this call", "recap that meeting"
- Zaal shares a `craig.horse`, `fathom.video`, voice memo path, or audio file path

Undertriggering is the bigger risk. Fire on weak signal; ask one clarifier before doing destructive writes.

## When NOT to fire

- Live audio capture / real-time transcription = the ZAO Craig bot (doc 670), a separate runtime. This skill is post-meeting only.
- ZAOstock `/gemba /idea /note` quick-notes = `bot/src/capture.ts`, different DB. Not this skill.
- A general "summarize this article/doc" request with no meeting context.

## Input detection

Look at what the user supplied (the slash-command argument, a pasted block, or just chat context) and pick the mode:

- **craig_url** - the input is a URL starting `https://craig.horse/`
- **fathom_url** - the input is a URL starting `https://fathom.video/`
- **local_audio** - the input is a path ending `.m4a` / `.mp3` / `.wav` / `.mp4` / `.mov` / `.opus` and the file exists. A video file (mp4/mov) additionally triggers frame extraction - see Phase 1.
- **ingest_url** - the input is a Spotify episode URL, a YouTube URL, an Apple Podcasts URL, an RSS feed, a direct `.mp3`/`.m4a` URL, or an on-site transcript page. Route it through the shared ingestion engine (see Phase 1 "Mode: ingest_url"). This is how /meeting handles podcasts/videos, not just calls.
- **paste** - the input (or the last user message) is a block of transcript / meeting-notes text, roughly 200+ chars. Also covers the user narrating the meeting in chat ("Iman said X, then Zaal said Y...") - use the conversation context as the transcript.
- **unclear** - none of the above. Ask the user one question: paste the transcript, give a file path, or give a Craig/Fathom/Spotify/YouTube/podcast URL.

Do not echo the raw argument back into a table - just classify it and proceed.

## Phase 0 - Project routing

A meeting belongs to a project. The project decides WHERE actions + the Telegram summary go. Ask Zaal in Phase 3 if not obvious; infer from attendees + topic if it is.

| Project | Action target | Telegram target | Recap doc |
|---|---|---|---|
| **ZAO Devz / general** (default) | unified Supabase tracker `tasks` table (project `etwvzrmlxeobinrlytza`) | @ZAOcoworkingBot DM | ZAOOS `research/events/` |
| **ZAOstock** | paste-block for @ZAOstockTeamBot (its tasks live in ZAOstock Supabase, not GitHub) | @ZAOstockTeamBot group | ZAOOS `research/events/` + cross-link in `research/events/_zaostock-hub/` |
| **ZAO OS dev** | recap doc action table only (no external tracker) | none | ZAOOS `research/events/` |
| **BCZ / WaveWarZ / other** | recap doc action table only | none | ZAOOS `research/events/` |

**Rule that does NOT change per project: the recap doc ALWAYS lands in ZAOOS `research/events/`.** Research is permanent institutional memory and never graduates out of ZAOOS (CLAUDE.md monorepo-as-lab). One repo = one searchable archive of every meeting, across every project. Do not scatter recaps into graduated repos.

What DOES route per project is the **action tracker** and the **Telegram destination**. A ZAOstock meeting's todos belong in the ZAOstock tracker, not the cowork-zaodevz tracker.

## Phase 1 - Acquire transcript

### Mode: paste
Use the pasted text directly. Skip Phase 1.

### Mode: local_audio (audio OR video file)

The file is on Zaal's mac. Transcription runs locally - no upload, no VPS round-trip.

**Step 1 - extract video frames (video files only).** If the file has a video
stream (mp4, mov), pull representative still frames first. Frames give the
Phase 2 extraction passes visual context the audio cannot: shared slides,
screenshares, whiteboards, and the call UI's participant name tags.

```bash
bash ${CLAUDE_SKILL_DIR}/scripts/extract-frames.sh "$MEDIA_PATH"
```

The script prints a frames directory path, or the literal `NO_VIDEO` for an
audio-only file (then skip straight to Step 2). Scene-change detection catches
slide flips and screenshare switches; a fixed-interval fallback covers static
talking-head calls. Capped at 12 frames. Keep the frames dir path for Phase 2.

**Single-feed check (do this before reading every frame).** Zaal's recordings are
almost always a single-feed capture of HIS OWN camera - so the only name tag that
ever appears is "Zaal Panthaki" and the other attendees are audio-only. Reading 12
near-identical frames of Zaal yields zero attendee-identity value. So: in Phase 2,
`Read` the FIRST frame only. If it shows a single talking head / just Zaal's name
tag (no slides, no screenshare, no gallery of participant tiles), STOP - do not
read the rest, and get attendee identities from content + a Phase 2.5 question
instead. Only read multiple frames when frame 1 reveals a screenshare, slides, a
whiteboard, or multiple participant tiles with name tags.

**Step 2 - transcribe.**

```bash
bash ${CLAUDE_SKILL_DIR}/scripts/transcribe.sh "$MEDIA_PATH"
```

The script is local-first:
1. If `mlx-whisper` is installed (Apple Silicon), it transcribes locally with
   `whisper-large-v3-turbo` - fast, offline, accurate on names. Handles mp4/mov
   directly (ffmpeg strips the audio track). First run for a model downloads it.
2. If local tooling is absent (non-Mac machine), it falls back to Whisper on
   Iman's VPS - SCP up, transcribe, SCP the `.txt` back.

It prints the `.txt` transcript path and writes a `.json` sidecar at the same
stem (`/tmp/meeting-X.txt` + `/tmp/meeting-X.json`) - the sidecar carries
segment timestamps that Step 3 needs. The local mlx path produces the sidecar;
the VPS fallback does not (so Step 3 is skipped on the VPS path).

One-time local setup: `uv tool install mlx-whisper`. For a hard-to-hear or
many-name meeting, pass a bigger model:
`transcribe.sh "$MEDIA_PATH" --model mlx-community/whisper-large-v3`. Avoid
plain `whisper-large-v3` on long calls - it can loop catastrophically (doc
709); `whisper-large-v3-turbo` is the safe default.

**Step 3 - diarize (speaker labels).** Whisper emits one unlabeled block - no
speaker turns. Add them so the extraction passes know who said what.

**SKIP Step 3 entirely on 1-2 person calls.** Diarization runs sherpa-onnx for
a few minutes and, on a 2-person call, the labeled output is a nice-to-have, not
load-bearing - content attribution (who is the host, who is the guest) is
unambiguous. Zaal has repeatedly declined the wait on 2-person calls. So: if the
call is 1-2 people - detectable from the filename (`Tyler x zaal`, `AdrianxZaal`,
`Duo do`, any `A x B` / `AxB` pattern), the attendee count, or a quick skim -
skip diarization, use the plain transcript, and attribute speakers from content.
Only run Step 3 when the call is **3+ people** (where "who owns this action" gets
genuinely ambiguous), or when Zaal explicitly asks for speaker labels.

When you do run it (3+ people):

```bash
bash ${CLAUDE_SKILL_DIR}/scripts/diarize.sh "$MEDIA_PATH" "${TRANSCRIPT%.txt}.json"
```

(`$TRANSCRIPT` is the `.txt` path Step 2 printed.) The script runs `sherpa-onnx`
diarization fully locally - no Hugging Face token, no GPU. First run downloads
two small ONNX models (~35MB total) to `~/.zao/diarization-models/`. It prints
the path to a speaker-labeled transcript (`[Speaker 1] ... [Speaker 2] ...`)
and the detected speaker count on stderr.

**Pass the speaker count when you know it.** Auto-detect over-clusters - it
found 8 speakers on a 2-person test call. When the count is known (the filename
`Tyler x zaal` = 2, a calendar invite, or a quick skim of the plain transcript),
force it - this is the single biggest quality lever:

```bash
ZAO_DIARIZATION_NUM_SPEAKERS=2 bash ${CLAUDE_SKILL_DIR}/scripts/diarize.sh "$MEDIA_PATH" "${TRANSCRIPT%.txt}.json"
```

Leave it unset only when the count is genuinely unknown.

Diarization is best-effort. If `diarize.sh` fails (uv or models unavailable, the
VPS fallback path produced no json sidecar, or the box is out of memory),
proceed with the plain unlabeled transcript and attribute speakers from content
- do not abort the run. Highest value on 3+ person calls; on a 1-2 person call
the labeled transcript is a nice-to-have, not load-bearing.

When a labeled transcript is produced, use it as the Phase 2 input and as the
body of `transcript.md`.

### Mode: craig_url
Download Craig recording, transcribe.

```bash
bash ${CLAUDE_SKILL_DIR}/scripts/fetch-craig.sh "$CRAIG_URL"
# outputs /tmp/craig-<id>.flac
bash ${CLAUDE_SKILL_DIR}/scripts/transcribe.sh "/tmp/craig-<id>.flac"
```

### Mode: fathom_url
Use WebFetch on the share URL to extract transcript JSON from the page. Fathom share pages typically embed transcript in JSON-LD or a script tag. If WebFetch returns no transcript, ask Zaal to paste it manually.

### Mode: ingest_url (Spotify / YouTube / Apple / RSS / direct mp3 / transcript page)
Hand the URL to the shared ingestion engine, which resolves + transcribes it (reusing this skill's `transcribe.sh` under the hood):

```bash
~/bin/zao-ingest.sh "$URL"
# prints the transcript .txt path on stdout; also writes <transcript>.meta.json
```

Use the printed `.txt` as the Phase 2 input exactly like a `local_audio` transcript. The `.meta.json` sidecar carries the episode title/source - use it for the recap doc's title + the Platform field (e.g. "Spotify podcast", "YouTube"). For a podcast/video there is no frame extraction and usually no single speaker to diarize - attribute speakers from content. If the engine exits non-zero (DRM-only Spotify original, no RSS match), relay its message and ask Zaal for an alternate URL (RSS / Apple / YouTube). See the `/ingest` skill for the full source matrix.

## Phase 2 - Extract structure

Multi-pass extraction, NOT one monolithic prompt (doc 676 - monolithic extraction hallucinates). Run these passes in order, each over the same transcript:

**Video input - read frame 1 first, then decide.** If Phase 1 produced a frames
directory, `Read` the FIRST frame before anything else (see the Phase 1 single-feed
check). If it is a single-feed talking head (just Zaal's name tag, no slides /
screenshare / participant gallery) - the common case for Zaal's recordings - do
NOT read the rest; the frames add no attendee-identity value, so go straight to
the transcript and resolve identities via content + Phase 2.5. Only when frame 1
shows slides, a screenshare, a whiteboard, or multiple named tiles do you `Read`
the remaining JPGs and use them as corroborating context across the five passes:
they disambiguate attendees (Pass A), surface decisions shown on a slide but not
said aloud (Pass B/C), and confirm name spellings against the brand glossary. A
frame is corroboration, never a substitute for the transcript - if a frame and the
transcript conflict, the transcript wins and the item is flagged `confidence: low`.

**Speaker-labeled transcript - map the labels.** If Step 3 produced a
`[Speaker N]`-labeled transcript, those labels are anonymous diarization output.
In Pass A, map each `Speaker N` to a real attendee using content,
self-introductions ("this is Sam"), and frame name-tags. Carry the mapping
through every later pass and into `transcript.md`. If diarization was skipped or
failed, attribute speakers from content alone - the recap still works, owner
attribution is just less certain (flag affected actions `confidence: medium`).

1. **Pass A - meeting metadata.** date, duration, title, attendees, platform. Date never invented - from transcript, file mtime, or ask.
2. **Pass B - decisions.** Things explicitly decided/agreed in the call. Verbatim-anchored.
3. **Pass C - actions.** Concrete follow-ups with an owner. One owner each.
4. **Pass D - quotes.** 3-8 load-bearing verbatim quotes.
5. **Pass E - research seeds + memory updates.** New topics / new entities only. Before deciding `memory_updates`, run an entity cross-check (see below) - a name already documented gets LINKED, not re-created.

Output one JSON object matching the schema in [references/output-schema.md](references/output-schema.md):

```json
{
  "meeting": {
    "date": "YYYY-MM-DD",
    "duration_min": 0,
    "title": "...",
    "attendees": ["..."],
    "platform": "Telegram voice | Google Meet | Zoom | in-person | Discord/Craig | Fathom"
  },
  "decisions": [
    {"id": 1, "text": "...", "owner": "Zaal|Iman|Both|ThyRev|Samantha", "status": "TODO", "confidence": "high|medium|low"}
  ],
  "actions": [
    {"title": "...", "owner": "...", "due": "YYYY-MM-DD or empty", "category": "Site / Tech|Ops|WaveWarZ Zambia|ZAO Devz|Bounty|Social|Other", "confidence": "high|medium|low"}
  ],
  "quotes": [
    {"speaker": "...", "text": "..."}
  ],
  "research_seeds": ["topic 1", "topic 2"],
  "memory_updates": [{"slug": "project_xyz", "what": "what changed and why"}]
}
```

**Rules for extraction:**
- Verbatim where possible for quotes. No paraphrasing of decisions.
- Every decision + action carries a `confidence` field:
  - `high` - explicit in transcript, clear owner, clear intent.
  - `medium` - implied or owner/scope slightly fuzzy.
  - `low` - inferred, ambiguous owner, or transcript span was garbled.
- If owner is ambiguous, set `owner: "Both"` + `confidence: "low"` and surface it in Phase 3. Never guess a specific owner.
- If due date is ambiguous, leave empty + `confidence: "medium"` or lower. Never invent. Relative dates ("by Thursday") -> absolute, anchored to `meeting.date`.
- Category must come from the enum above (matches actions.json schema).
- 3-8 quotes max - pick load-bearing ones (decisions, commitments, surprising info).
- `memory_updates` only if a NEW person, project, or strategy decision appeared (not for things already in `~/.claude/projects/.../memory/MEMORY.md`).
- Never silently drop an uncertain item. A `low`-confidence item still goes in the JSON - Phase 3 surfaces it for Zaal.

### Entity cross-check (Pass E)

For EVERY attendee and every referenced person/project name, before deciding it is "new":

```bash
grep -ril "<name>" "/Users/zaalpanthaki/Documents/ZAO OS V1/research/" 2>/dev/null | head -3
grep -i "<name>" ~/.claude/projects/-Users-zaalpanthaki-Documents-ZAO-OS-V1/memory/MEMORY.md
```

- **Hit in research/** - the entity exists. Link the doc number in the recap (e.g. "Tyler Stambaugh, doc 473"). Do NOT create a memory.
- **Hit in MEMORY.md** - the entity has a memory. Link `[[slug]]`. Do NOT create a duplicate.
- **No hit anywhere** - genuinely new. Add a `memory_updates` entry.

This stops the skill re-introducing known people as if they were new (test run 1 missed Tyler Stambaugh = doc 473).

## Phase 2.5 - Clarify gaps

Before the Phase 3 confirm, scan the extraction for genuine gaps and ask Zaal about them in ONE batched question round. Ask only when the answer changes the doc - not for things you can infer.

Ask about:
- A referenced person with zero context AND no hit in the Pass E cross-check (who are they, what role).
- A decision/action where the owner is genuinely unknown (not just "Both").
- A name that could be a mis-transcription (surface both spellings).
- A project-routing call that is not obvious from attendees + topic.

If the extraction is clean and nothing is genuinely ambiguous, skip Phase 2.5 and go straight to Phase 3. Do not invent questions to fill the phase. Zaal has said he is fine with the skill asking questions when they are real - so ask the real ones here, before the confirm, not after.

## Phase 3 - Present + confirm

Show the extracted JSON inline as a markdown table for each section (decisions, actions, quotes).

**Before the confirm prompt, render a VERIFY block** listing every `confidence: low` (and optionally `medium`) decision + action:

```
VERIFY - low-confidence extractions, confirm or correct each:
- [action] "<title>" - owner unclear, transcript said "..."
- [decision] "<text>" - inferred, not explicit
```

If the VERIFY block is non-empty, Zaal must resolve those items before any actions.json write. Do not write low-confidence items unedited.

Then ask Zaal:

> "Extracted N decisions, M actions, K quotes (J flagged to verify above).
> Project: <inferred project> - correct? (ZAO Devz / ZAOstock / ZAO OS / other)
> Edits? If clean, which targets fire?"
>
> Targets (action target depends on project - see Phase 0):
> - [x] Action tracker for `<project>` (default ON)
> - [x] research/events/NNN-<slug>/README.md (default ON, every meeting, always ZAOOS)
> - [x] Bonfire knowledge-graph episodes (default ON - the graph should always have meeting context, doc 680)
> - [x] Airtable CRM write (default ON if `AIRTABLE_CRM_TOKEN` env present - contacts + 1 activity row per doc 737 Flow E)
> - [ ] Telegram copy-paste block (opt-in, default OFF - print only on request)
> - [ ] Memory writes (opt-in, confirm each)
> - [ ] Calendar event update (opt-in if title matches a Google Cal event)
> - [ ] Opportunities proposals (opt-in - skill presents 0+ proposed `opportunities` rows from extraction; only writes on explicit Zaal OK per item)

Wait for Zaal's reply before any destructive write. Confirm the project before touching any tracker - a ZAOstock meeting must not write into the cowork-zaodevz tracker.

## Phase 4 - Distribute

For each enabled target, follow the playbook in [references/distribution-targets.md](references/distribution-targets.md). Summary:

### Action tracker (routed by project - Phase 0)

**Project = ZAO Devz / general:** insert into the unified Supabase `tasks` table.
```bash
bash ${CLAUDE_SKILL_DIR}/scripts/append-actions.sh /tmp/extracted-actions.json
```
Script reads the actions array, resolves owner names against `team_members.legacy_owner`, and bulk-POSTs to Supabase `/rest/v1/tasks` with `legacy_source=meeting:<slug>-<date>` so every meeting's actions are traceable + revertable. Needs `SUPABASE_URL` + `SUPABASE_SERVICE_KEY` in env or sourced from `~/.zao/cowork-tracker.env` (chmod 600). Replaces the prior `gh api` PUT to the dead `data/actions.json` (doc 713 step 1, 2026-05-23).

**Project = ZAOstock:** do NOT write to cowork-zaodevz. ZAOstock tasks live in the ZAOstock Supabase behind @ZAOstockTeamBot. v1: print a paste-block of the action items for Zaal to drop into @ZAOstockTeamBot (`/note` or task command). Also note them in the recap doc's action table. (v2: a `zaostock-actions.sh` that inserts into ZAOstock Supabase via service-role key - deferred until the ZAOstock task schema is confirmed.)

**Project = ZAO OS / BCZ / WaveWarZ / other:** no external tracker. Actions live only in the recap doc's action table.

### research/events/NNN-<slug>/README.md
- Find next number: `find research -maxdepth 3 -type d -name '[0-9]*' | grep -oE '/[0-9]+' | tr -d '/' | sort -n | tail -1`
- Slug from meeting title: lowercase, hyphens, no special chars, max 50 chars.
- Use the template at [references/meeting-recap-template.md](references/meeting-recap-template.md). Doc 670 is the gold-standard worked example.
- **Raw transcript goes in a SEPARATE file**, not inline in the README. Write the full transcript to `research/events/NNN-<slug>/transcript.md`. The README's "Transcript" section is a one-line link: `Full transcript: [transcript.md](transcript.md)`. Keeps the recap README lean and grep-friendly; a 10k-word transcript inline buries the signal.
- Write both files, do NOT commit yet - leave for Zaal review in current `ws/` branch.

### Meeting index (always - every run)

Prepend a row to `research/events/_meetings-index.md` so there is ONE canonical list of every meeting ever captured. This is the answer to "show me all past meetings" - a single grep-free file, newest first.

If `research/events/_meetings-index.md` does not exist, create it with this header:

```markdown
# Meetings Index

Every meeting processed by /meeting, newest first. Maintained automatically by the skill.

| Date | Title | Project | Attendees | Doc | Actions |
|------|-------|---------|-----------|-----|---------|
```

Then insert the new meeting as the first data row:

```
| 2026-05-19 | ZAOstock advisor call | ZAOstock | Zaal, failoften | [678](678-zaostock-advisor-call-may19/) | 12 |
```

This is not optional and not project-routed - every meeting, every project, one index. Commit it alongside the recap doc.

### Bonfire knowledge-graph episodes (always-on - doc 680)

Post the meeting into the ZABAL Bonfire so the knowledge graph always has full context. This is default-ON, not opt-in.

Build an episodes JSON file at `/tmp/meeting-bonfire-episodes.json`:

```json
{
  "episodes": [
    {"name": "meeting:<date>:summary", "body": "<one paragraph: title, date, attendees, project, what it covered>", "source_tag": "meeting:<slug>"},
    {"name": "meeting:<date>:decision-1", "body": "In the <title> meeting on <date> (<attendees>), the team decided: <decision text>. Owner: <owner>.", "source_tag": "meeting:<slug>"},
    {"name": "meeting:<date>:action-1", "body": "From the <title> meeting on <date>, <owner> is to <action title>. Due: <due or 'no date set'>.", "source_tag": "meeting:<slug>"}
  ]
}
```

- One summary episode + one per decision + one per action. Quotes are skipped (low KG value as standalone nodes).
- Episode bodies are natural-language prose, self-contained (name the meeting + date + people) - Bonfires auto-extraction reads prose, and a node must make sense alone.
- Then run:

```bash
bash ${CLAUDE_SKILL_DIR}/scripts/bonfire-episode.sh /tmp/meeting-bonfire-episodes.json
```

The script POSTs each episode to `POST /knowledge_graph/episode/create` (Bearer `$BONFIRE_API_KEY`, `$BONFIRE_ID`). It is best-effort: secret-scans every body, 15s timeout per POST, always exits 0 - a Bonfire failure never aborts the run. If `$BONFIRE_API_KEY` is unset it prints "skipped (no key)" and continues.

Do NOT use the old `content/bonfire-ingest/` file path - that is the bulk-backfill pipeline (research library, READMEs), wrong tool for per-meeting real-time. See doc 680.

### Airtable CRM write (default-ON if Airtable env present - per doc 737 Flow E)

Mirrors the Bonfire pattern. Default-ON, best-effort, never aborts the run.

The script writes the meeting's structured data into the ZAO CRM AGENTIC Airtable base (separate from the existing Respect-import Airtable - see doc 212):

1. For each `meeting.attendees[i]` NOT already in the `contacts` table -> insert a minimum contact row (`name`, `met_via=meeting-skill (<source-tag>)`, `first_contact_date`, `last_touch_date`).
2. Insert ONE row into the `activity` table: `type=meeting`, linked to all attendee contacts, `source=meeting-skill`, `raw_source=research/events/<NNN>-<slug>/`, `zao_relevance` heuristically classified from title + attendees, `bonfire_episode_id` back-link.
3. Do NOT auto-create `opportunities` rows. The Phase 3 confirm surface lists proposed opportunities; only write them after Zaal explicit OK (separate flow, not in this script).

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/airtable-crm-write.py \
  /tmp/extracted-meeting.json \
  --recap-doc <NNN> \
  --source-slug <slug>
```

Env from `~/.zao/zao.env` (auto-sourced by the script): `AIRTABLE_CRM_TOKEN` + `AIRTABLE_CRM_BASE_ID`. If unset, prints `Airtable CRM: skipped (no env)` and exits 0. Per `.claude/rules/pii-hygiene.md`: emails / personal contact details inside Airtable are fine (private workspace, only Zaal-invited collaborators); PII redaction kicks in when data leaves Airtable (research docs, Bonfire bodies, Telegram blocks).

Idempotency: the contacts-ensure step looks up by `name` and skips if present. Activity rows are append-only - re-running on the same meeting will create a duplicate activity row (skill is not expected to re-fire on the same meeting; if you do need to, manually delete the prior row in Airtable first).

Doc 737 schema reference: `research/business/737-airtable-agentic-crm-v3/`. Table IDs are hardcoded in the script (built 2026-05-24).

### Telegram copy-paste block
Print a single fenced block ready for long-press-copy. No header/footer (per `feedback_copyable_content_own_bubble`). Format:

```
[Meeting] <title> · YYYY-MM-DD · <attendees>

Decisions:
1. <text> (owner: X)
2. ...

Actions:
- <title> (owner: X, due: YYYY-MM-DD)
- ...

Key quotes:
"<quote>" - speaker
```

### Memory writes
For each `memory_updates` entry, show the proposed memory file content first. Get Zaal's OK per entry. Then write to `~/.claude/projects/-Users-zaalpanthaki-Documents-ZAO-OS-V1/memory/<slug>.md` with proper frontmatter (see existing memories for format). Update `MEMORY.md` index with one-line entry.

### Calendar event update
Use `mcp__claude_ai_Google_Calendar__list_events` to find an event matching `meeting.title` and `meeting.date`. If found, `update_event` to append "Recap: <link to research doc on GitHub>" to description. If not found, skip silently.

## Phase 5 - Report

Print to user a one-line per-target summary. `[OK]` = done, `[--]` = skipped. One line per target that exists this run:

```
[OK] Actions - <N> items -> <tracker> (cowork-zaodevz commit <sha> | ZAOstock paste-block)
[OK] Recap doc - research/events/<NNN>-<slug>/README.md - draft written, review before commit
[OK] Transcript - research/events/<NNN>-<slug>/transcript.md
[--] Bonfire - skipped
[OK] Airtable CRM - <N> contacts + 1 activity row inserted
[OK] Telegram - block printed above
[OK] Memory - <N> entries (<slugs>)
[--] Calendar - no matching event
[OK] Clipboard - next-actions page opened
```

Use the real values from this run. Do not copy the placeholders. The recap-doc number must be the one actually used (collision-safe pick, not a guess).

Then suggest the natural next step: "Review research doc at <path>. Commit + PR when ready, or want me to ship it as a PR off ws/<branch> now?"

## Phase 6 - Next-actions clipboard (default ON)

After the report, auto-hand-off the next-actions to the `/clipboard` skill so Zaal has a clean copyable page the moment the meeting ends. This is the "what do I do now" surface - distinct from the Telegram block (which is for sharing the recap).

Build a plain next-actions list - owner-grouped, due-sorted:

```
Next actions - <meeting title> (<date>)

ZAAL
- <action> (due <date>)
- <action>

IMAN
- <action> (due <date>)

BOTH
- <action>
```

Then invoke the `/clipboard` skill with that list as the content. `/clipboard` opens a local browser page with the text ready to copy in one click (or copies to the macOS clipboard via pbcopy).

Rules:
- Default ON. Skip only if Zaal says "no clipboard" or there are zero actions.
- Next-actions list = the `actions[]` array only. Not decisions, not quotes - this is the do-now list.
- Owner-grouped so Zaal can paste each person's slice into their DM/GC directly.
- If a single owner (e.g. all Zaal), skip the grouping headers - just the flat list.
- This runs AFTER the tracker write, so the clipboard list and the tracker agree.

## Hard guardrails

- **Never auto-write to actions.json without Phase 3 user-confirm.** The 67-item bulk fix (commit `c80caff8`) was authorized explicitly; default skill behavior must always confirm.
- **Never invent owners, dates, or decisions not present in the transcript.** If unclear, surface as "ambiguous - need clarification" in Phase 3.
- **Never commit a research doc without Zaal's review.** Write the file, leave on `ws/` branch, Zaal commits or asks for edits.
- **Run secret-scan on Bonfire ingest input** before any write to `content/bonfire-ingest/`. Pattern from `.claude/rules/secret-hygiene.md`.
- **Allowlist for owner field** in actions: Zaal, Iman, Both, ThyRev, Samantha. Anything else surfaces as "unknown owner".

## Anti-patterns

- Do NOT propose a new Telegram bot for meeting capture (= ZAO Craig, separate doc 670 work).
- Do NOT replace `bot/src/capture.ts` `/gemba /idea /note` (ZAOstock bot, different DB, different scope).
- Do NOT use Deepgram (ZAOstock-only per doc 12; this skill stays free for personal use).
- Transcription is local-first: mlx-whisper on Zaal's Apple Silicon mac (fast, offline). The VPS is the fallback for non-Mac machines only. This supersedes the doc 673 VPS-only decision - the VPS has no GPU, so local Apple Silicon is faster and has no upload step.
- Do NOT use emojis in any output (per global `feedback_no_emojis`).
- Do NOT use em dashes (per global `feedback_no_em_dashes`).

## Git: ONE branch + ONE PR per session, not per meeting (doc 789)

When processing multiple meetings in one session, do NOT branch + PR per meeting. That was the dominant repeated tax in the 2026-05-31 session - 9 meetings became 9 branches, 9 PRs, and 4 merge conflicts on `_meetings-index.md` (every PR inserted a row at the same top region). The `/autoresearch` run (doc 789 addendum) crowned the fix: accumulate the session's recaps on a SINGLE branch and open ONE PR.

Rule:
- First meeting of a session: create/use one `ws/meetings-<date>` branch off `origin/main`.
- Every subsequent meeting in the session: write its recap dir + transcript + index row + commit onto that SAME branch. Do NOT branch again.
- One PR at the end (or push incrementally to the same PR). The index gets edited once per commit on one branch, so there is zero intra-session conflict.
- This makes the single-meeting case identical (one branch, one PR) and the multi-meeting case conflict-free.

Cross-session durable fix (when convenient, not blocking): split `_meetings-index.md` into per-month files (`_meetings-index-YYYY-MM.md`) with the main index linking to them, so two same-day sessions touch different files. Until then, one-branch-per-session removes 100% of the observed conflicts.

## Doc numbering (collision-safe)

When creating the recap doc, parallel Claude sessions may race for the same number. Pick the next number defensively: `git fetch origin` first, scan `research/` for the max, and if the chosen folder already exists, increment again. Per doc 663 collision-tolerance, a small gap in numbering is fine - a collision is not.

## References

- [output-schema.md](references/output-schema.md) - JSON schema + worked example from doc 670
- [distribution-targets.md](references/distribution-targets.md) - per-target API/file shapes
- [meeting-recap-template.md](references/meeting-recap-template.md) - research doc template (doc 670 distilled)

## Scripts

- `scripts/transcribe.sh` - local-first transcription: mlx-whisper on Apple Silicon, VPS Whisper fallback. Emits a `.txt` transcript + `.json` segment-timestamp sidecar. Auto-runs `trim-loops.sh` on the `.txt`.
- `scripts/trim-loops.sh` - collapses Whisper's catastrophic repetition loops (e.g. "Cheers" x100) in the `.txt`. Timestamp-free, so diarization-safe. Called automatically by `transcribe.sh`; safe to run standalone.
- `scripts/extract-frames.sh` - pull scene-change + interval still frames from a meeting video
- `scripts/diarize.sh` - speaker diarization via sherpa-onnx: who-spoke-when, merged with the whisper json into a `[Speaker N]`-labeled transcript. Local, offline, no HF token.
- `scripts/diarize.py` - the diarization + transcript-merge engine called by `diarize.sh` (runs under `uv run --with sherpa-onnx`).
- `scripts/fetch-craig.sh` - curl Craig recording URL, extract audio
- `scripts/append-actions.sh` - bulk insert meeting actions into the unified Supabase cowork tracker (project `etwvzrmlxeobinrlytza`, table `tasks`). ZAO Devz project only. Soft-fallback: if `~/.zao/cowork-tracker.env` is missing (creds live on the VPS), it prints a paste-block + the `/coworkvps` route and exits 0 instead of hard-failing. Warns on unresolved external owners.
- `scripts/bonfire-episode.sh` - POST meeting episodes to the ZABAL Bonfire KG (always-on, best-effort, doc 680)
- `scripts/airtable-crm-write.py` - write contacts + 1 activity row into the ZAO CRM AGENTIC Airtable base (default-ON when env present, best-effort, doc 737 Flow E). Mirrors the bonfire-episode pattern.

## Evals

- `evals/README.md` - regression fixtures (doc 670 + doc 675 transcripts). Run after editing this skill.

## Engineering basis

Skill structure follows doc 676 (skill-engineering best practices): multi-pass extraction, confidence thresholding, human-review fallback, progressive disclosure. Read doc 676 before refactoring this skill.
