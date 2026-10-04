---
name: meeting
description: Process raw meeting notes into structured meeting note with in-repo tasks
argument-hint: "[meeting file path or 'browse']"
---

# Process Meeting Notes

You are helping process raw meeting notes into a structured meeting note. Action items for the user land in `Dashboard/tasks.md`.

## Input Modes

The skill operates in one of three modes based on `$ARGUMENTS`:

| Mode | Arguments | When to use |
|------|-----------|-------------|
| **Browse** | (none) or `browse` | List recent files in `Meetings/` that look unprocessed |
| **Specific file** | File path or partial name | Process notes from a specific file |
| **Paste** | Pasted text (long string) | Meeting notes pasted directly into the prompt |

---

## Workflow

### Step 0: Determine mode and get raw notes

**If no arguments (Browse mode)**:
1. Use the `Glob` tool with pattern `Meetings/*.md` to list meeting files. Do NOT use `Bash ls` - Glob is quieter and shows results already sorted.
2. Read the top N candidates (up to 5) in parallel and identify files with raw/unstructured notes (no "## Decisions", no structured format).
3. Show a numbered list of unprocessed files.
4. Ask: "Which meeting do you want to process?"

**If specific file path**:
1. Read the file.
2. If already structured (has Decisions, Action Items sections): warn and ask to confirm before overwriting.
3. If raw notes: proceed directly.

**If pasted text**:
- Use the pasted text as raw input.
- Ask for meeting date and title if not obvious from the text.

---

### Step 1: Analyze raw notes

Extract:
- Meeting title (from filename or content)
- Date (from filename or content)
- Attendees (mentioned names)
- Key topics discussed
- Decisions made (explicit or implicit)
- Action items (tasks, follow-ups, commitments - with owners)
- Open questions (unresolved topics)

### Step 2: Cross-reference attendees

- Read `Dashboard/people-profiles.md` to verify attendee names and roles.
- Use tags (e.g., `#FirstName`) when mentioning people.

### Step 3: Search for related context

- Search `Loose Notes/Work/` for related decisions or notes.
- Check `Dashboard/Weekly P-Tasks.md` for related P-tasks.
- Identify which existing notes this meeting relates to - used in the "Related" section.

### Step 4: Create structured meeting note

- **Location**: `Meetings/YYYY-MM-DD - [Meeting Title].md` (or overwrite the source file if processing in-place).
- **Template**: `templates/meeting-note.md`.
- **Date**: the meeting's actual date, not today's date.
- Fill all sections:
  - Attendees (verified names, correct tags)
  - Topics (high-level)
  - Meeting notes (organized by topic)
  - Decisions (extracted explicitly)
  - Action Items (checkboxes with owners and deadlines)
  - Open Questions
  - Related (wikilinks to relevant notes)

### Step 5: Link in the meeting's journal

- Journal path: `journals/YYYY/MM-Month/DD-MM-YYYY.md` for the meeting's date.
- Add under `## Notes`: `- [[YYYY-MM-DD - Meeting Title]] - [One-line summary]`.
- If the journal for that date doesn't exist, skip.

### Step 6: Prepare tasks for the user (confirm before writing)

- **Only prepare tasks for the vault owner** - skip tasks owned by others.
- Avoid duplicates: scan `Dashboard/tasks.md` (all three sections) for matching task content.
- Prepare a proposed list:
  - Text: "[Action item]"
  - Optional due date (if a deadline was mentioned)
  - Optional priority (P2 critical / P3 normal / P4 low)
  - Source link back to the meeting note (`source: [[YYYY-MM-DD - Meeting Title]]`)

**Show the proposed list and wait for confirmation** before writing.

After confirmation, append the tasks to `Dashboard/tasks.md` under the "This week" section, using this format:

```
- [ ] Action description - source: [[YYYY-MM-DD - Meeting Title]] - due: YYYY-MM-DD - priority: P3
```

Priority and due date are optional - include only when meaningful.

---

## Output Format

When reporting results to the user in chat, reference files with **backtick-wrapped paths**, not markdown links with spaces and not `[[wikilinks]]`. Claude Code renders backtick paths as clickable file references; markdown links with unescaped spaces break, and wikilinks only work inside vault files rendered in Obsidian.

In chat:

```
Meeting note created: `Meetings/YYYY-MM-DD - Meeting Title.md`
Linked in journal: `journals/YYYY/MM-Month/DD-MM-YYYY.md` (or "skipped - no journal for that date")

Proposed tasks for Dashboard/tasks.md (your action items only):
1. [Task] - due YYYY-MM-DD - P2
2. [Task] - P3

Already in Dashboard/tasks.md (skipping):
- [Existing task]

Tasks for others (not added to your list):
- [Task] - [Person]

Confirm: add tasks to Dashboard/tasks.md? (Y / N / pick numbers like 1,3)
```

After confirmation, append tasks to the "This week" section of `Dashboard/tasks.md`.

**Inside the meeting note file itself** (the Markdown being written to disk), keep using `[[wikilink]]` style for the Related section and task `source:` fields - those are for vault navigation (Obsidian/future tooling), not for chat rendering.

---

## Notes

- Use the meeting's actual date, not today's date.
- If a meeting already has a structured note, warn before overwriting.
- **Only write tasks that belong to the vault owner.**
- **Always check `Dashboard/tasks.md` for duplicates** before proposing new tasks.
- If attendees aren't clear, ask the user.
- If no deadline is mentioned for an action item, don't set one.
