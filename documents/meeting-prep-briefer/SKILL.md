---
name: meeting-prep-briefer
description: "Generate a structured briefing document for each meeting of the day from local workspace files and a daily schedule — participants, context, and open questions in one brief. No integrations required. Triggers: 'meeting brief', 'prep my meetings', 'prepare for today's meetings', 'briefing for my calls today', 'бриф по встречам', 'подготовь встречи', 'бриф на встречи дня', 'что нужно знать перед встречами'."
version: 1.0.0
---

# Meeting Prep Briefer

This skill generates a structured per-meeting briefing document for busy managers and individual contributors. Given a daily schedule (pasted inline or read from a local file) and any available workspace context files (project notes, participant notes, previous meeting notes), it produces a brief for each meeting with participants, context, open questions, and a suggested agenda — entirely from local files, no external integrations required.

**Input:** Daily schedule (inline text or local file path) + workspace context files (auto-scanned).

**Output:** Structured markdown brief (inline response). Optionally saved to `output/meeting-brief-YYYY-MM-DD.md` on request.

---

## Language Detection

Detect the user's language from their message:
- If Russian (or contains Cyrillic): respond in Russian
- If English (or other Latin-script language): respond in English
- If ambiguous: default to English

---

## Instructions

### Step 1: Parse Input

1. Check if the user provided an inline schedule (list of meetings in their message) or a file path.
   - **Inline:** parse meetings directly from the message.
   - **File path:** read the specified file from the workspace. If the file does not exist, return: "File not found: `{path}`. Please check the path or paste the schedule directly."

2. If no schedule is provided at all, return: "Please paste your meeting schedule or provide a path to a schedule file (e.g., `today.md`)." Stop — do not generate output.

3. Parse the schedule into a list of meetings. Each meeting must have at minimum a time and a title. Participants are optional.
   - Accepted formats: `10:00 — Team Sync`, `10:00 Team Sync (Alice, Bob)`, `10:00 | Team Sync | Alice, Bob`, or similar time + title patterns.
   - If the schedule is completely unparseable (no recognisable time+title structure), return: "Could not parse meeting schedule. Please use a format like: `10:00 — Team Sync (Alice, Bob)`." Stop.

4. Determine the brief date: use today's date unless the user specifies another date.

---

### Step 2: Scan Workspace for Context

1. For each parsed meeting, search the workspace for relevant context files:
   - Match files by: meeting title keywords, participant names, or project names appearing in the schedule.
   - Look in: root workspace, `notes/`, `output/`, `input/`, `context/` folders.
   - Accepted file types: `.md`, `.txt`.

2. For each matched file, extract:
   - Relevant headings and their content (limit to 150 words per file to keep briefs concise).
   - Any open action items or questions found in the file.

3. If no matching files are found for a meeting: note "No context files found" for that meeting — do not skip the meeting.

---

### Step 3: Assemble Briefs

For each meeting, build a section with four subsections:

**Participants**
- List names and roles if provided in the schedule.
- If no participants listed: note "No participants listed in schedule."

**Context**
- List 2–4 bullet points extracted from matched workspace files.
- Each bullet: `From \`filename\`: [key point]`.
- If no context files matched: "No context files found — add relevant notes to your workspace."

**Open Questions**
- Extract any open questions or action items from matched files.
- If none found: leave as an empty prompt line `*(none listed — add questions before the meeting)*`.

**Suggested Agenda**
- Generate 2–4 agenda items based on the meeting title, participants, and context.
- Keep each item to one short phrase with a suggested time allocation.

---

### Step 4: Output Brief

1. Assemble all meeting sections into a single markdown document:
   - Header: `# Meeting Brief — YYYY-MM-DD`
   - Each meeting: `## HH:MM — Meeting Title` followed by four subsections
   - Meetings separated by `---`

2. Display inline in the chat.

3. If the user says "save" or "save to file": write the brief to `output/meeting-brief-YYYY-MM-DD.md` and confirm the path.

---

## Edge Cases

- **No context files for a specific meeting:** Produce the brief anyway; fill Context with placeholder message.
- **Schedule has time + title only (no participants):** Skip Participants section; add flag: "No participants listed — add names to schedule for richer brief."
- **Multiple files match one meeting's keywords:** Include all matched files as context sources; list each filename.
- **User provides a past or future date:** Use that date for the brief header and output filename.
- **Very long meeting title (>60 chars):** Truncate display title in the header to 60 chars; use full title in the section heading.

---

## Negative Cases

- **No schedule provided:** Return usage message and stop. Do not generate partial output.
- **File path not found:** Return file-not-found message with the exact path. Do not guess alternate paths.
- **Schedule unparseable:** Return format hint and stop. Do not attempt to guess meeting times.

---

## Output Format

```
# Meeting Brief — 2026-04-28

---

## 10:00 — Team Sync

**Participants:** Alice (PM), Bob (Eng), Carol (Design)

**Context:**
- From `project-notes.md`: Sprint 12 ends Friday; 3 open stories remain.
- From `alice-notes.md`: Concerns raised about API timeline dependency.

**Open Questions:**
- Is the API dependency resolved before Friday?
- Who owns the design handoff?

**Suggested Agenda:**
1. Sprint status check (5 min)
2. API dependency decision (10 min)
3. Next steps & owners (5 min)

---

## 14:00 — 1-on-1 with Bob

**Participants:** Bob (Eng)

**Context:**
- No context files found — add relevant notes to your workspace.

**Open Questions:**
*(none listed — add questions before the meeting)*

**Suggested Agenda:**
1. Check in on current blockers (10 min)
2. Career development update (10 min)
```
