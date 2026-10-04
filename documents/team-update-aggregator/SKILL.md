---
name: team-update-aggregator
description: "Aggregate weekly team member updates from local .md/.txt files into a people-centric status report for managers. Organizes content by person (not by project): progress, plans, blockers, capacity, and manager flags. Use when preparing for 1-on-1s, weekly team reviews, or building a team tracker. Triggers: 'aggregate team updates', 'compile team status', 'team weekly report', 'агрегируй обновления команды', 'статус команды', 'составь отчёт по команде'."
version: 1.0.0
---

# Team Update Aggregator

This skill reads weekly update files from your team members and compiles them into a single **people-centric** status report — organized by person, not by project. Each team member gets a dedicated section with progress, next-week plans, blockers, capacity notes, and manager attention flags. Output: `team-status-YYYY-MM-DD.md`.

**Key difference from weekly-digest-synthesizer:** This skill answers "How is each person doing?" — not "What's happening on each project?"

**Input:**
- Folder path or list of `.md` / `.txt` files with team member updates
- One file per person, or one file with multiple H2/H3 sections per person
- Optional: report date (defaults to today)

**Output:**
- `team-status-YYYY-MM-DD.md` — structured people-centric team report

---

## Language Detection

Detect the user's language from their message:
- If Russian (or contains Cyrillic): respond in Russian
- If English (or other Latin-script language): respond in English
- If ambiguous: respond in the language of the trigger phrase used

---

## Instructions

### Step 1: Validate Input

1. Determine input source from the user's message:
   - Folder path → scan all `.md` and `.txt` files in that folder
   - List of files → use those files directly
   - No path provided → scan the current working directory for `.md` and `.txt` files

2. Verify files exist and are readable:
   - If no files found: stop. Report "No .md or .txt files found at [path]. Provide a folder path or list of files to process."
   - If a specific file path does not exist: stop. Report "File not found: [path]. Check the path and try again."

3. Check for unsupported file formats:
   - If user provides only `.docx`, `.xlsx`, `.pdf`, or similar: stop. Report "Unsupported file types. This skill processes .md and .txt files only."

4. Check if all files are empty:
   - If all files have no readable content: stop. Report "All files are empty. No report generated."

5. Determine report date:
   - If user specifies a date → use that date in output filename
   - If not specified → use today's date (YYYY-MM-DD format)

### Step 2: Identify Team Members

For each file, determine the **owner** (team member name):

1. **From filename:** `anna.md`, `ivan-petrov.md`, `john_smith.md` → extract name, normalise to "Anna", "Ivan Petrov", "John Smith"
2. **From H1 heading:** first `# Name` in the file body → use as owner
3. **From explicit field:** line starting with `Name:`, `Who:`, `Person:`, `От:`, `Автор:` → use value as owner
4. **Multi-person file:** if file contains multiple `## Name` or `### Name` sections → split into one owner per section
5. **Not identified:** if none of the above applies → assign owner as "Unknown — [filename]"; add flag "Owner not identified"

### Step 3: Extract Content per Person

For each identified owner, extract:

1. **Progress:** completed tasks, shipped items, closed tickets, decisions made — bullets or prose
2. **Next week plans:** what they plan to work on next (if mentioned); mark "Not mentioned" if absent
3. **Blockers:** anything described as blocking, waiting-on, stuck, or unresolved
4. **Capacity / OOO:** explicit mentions of being overloaded, on leave, sick, or at partial capacity
5. **Manager flags:** mark ⚠️ when any of these signals appear:
   - Stress, burnout, frustration, or morale language
   - Overload without mitigation
   - Blocker unresolved for implied 1+ week
   - Explicit request for help or escalation
   - Out of office / sick (for visibility)

Handle sparse content:
- Empty section: include person with empty progress; add note "No updates provided"
- Only blockers, no progress: include both; add flag "No progress reported"

### Step 4: Detect Cross-Team Signals

Across all extracted content:

1. **Shared blockers:** same blocker mentioned by 2+ people → flag in Cross-Team section
2. **Dependencies:** person A is waiting on person B → capture as dependency pair
3. **Unowned action items:** action items without a named owner → collect in Cross-Team table
4. **Large team:** if 10+ people in report → add note "Large team: [N] members — review for completeness"

### Step 5: Check for Existing Output File

1. Check if `team-status-[date].md` already exists in the working directory:
   - If yes: ask user — "File team-status-[date].md already exists. Overwrite or save as team-status-[date]-v2.md?"
   - Wait for response before writing

### Step 6: Write Report

1. Write `team-status-YYYY-MM-DD.md` using the Output Format below
2. Populate all sections; mark any empty field explicitly (e.g., "None", "Not mentioned")
3. Report in chat: "Report saved: team-status-[date].md — [N] members, [N] blockers, [N] flags"

---

## Output Format

```markdown
# Team Status — [Date]

**Members:** [N] | **Updates compiled:** [N] files | **Flags:** [N]
[Note if large team: "Large team: N members — review for completeness"]

---

## Summary

[2–4 sentences: overall team health, key achievements, main blockers, who needs manager attention]

**Flags requiring attention:** [Name — reason, or "None"]

---

## Team Members

### [Full Name]
- **Progress:** [completed work, 1–3 bullets]
- **Next week:** [plans or "Not mentioned"]
- **Blockers:** [blockers or "None"]
- **Capacity:** [Normal / Overloaded / Partial / OOO — if mentioned; omit if not]
- **Manager flags:** [⚠️ flag description or "—"]

### [Next Person...]

---

## Cross-Team

### Shared Blockers
- [Blocker mentioned by 2+ people — names]

### Dependencies
- [Person A] waiting on [Person B] — [what for]

### Unowned Action Items

| Action | Mentioned by | Source File |
|--------|-------------|-------------|
| [action] | [name] | [filename] |

---

## Files Processed

Files included: [list]
Files with no updates: [list or "None"]
Unknown owners: [list of files where owner was not identified, or "None"]
```

**Field rules:**
- Manager flags: apply ⚠️ only to explicit signals from the text; do not infer from absence of updates alone
- Capacity: use explicit markers only (overloaded, can't keep up, on leave, sick); do not interpret implicitly
- Summary: write from extracted content — do not invent progress or add assumptions

---

## Edge Cases

1. **One file, multiple people (H2/H3 sections with names):** Split by section, create one entry per person
2. **File with no identifiable owner:** Assign "Unknown — [filename]"; add flag "Owner not identified"
3. **Person sent only a blocker, no progress:** Include both; add flag "No progress reported"
4. **Out of office / sick mentioned:** Add ⚠️ flag "OOO" and note in Summary
5. **10+ members:** Add "Large team" note at report header; proceed normally

---

## Negative Cases

- **No files found:** Stop. Report "No .md or .txt files found at [path]."
- **Unsupported file types only:** Stop. Report "Unsupported file types. Convert to .md or .txt first."
- **All files empty:** Stop. Report "All files are empty. No report generated."
- **Output file already exists:** Ask before overwriting; offer `-v2` alternative
