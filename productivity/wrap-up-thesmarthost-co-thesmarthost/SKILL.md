---
name: wrap-up
description: Summarize session changes — update memory log, generate commit message, and create patch notes. Use after completing work.
---

# Wrap Up

> **End-of-session automation**: memory log + commit message + patch notes in one step.

Invoke with `/wrap-up` after finishing a task or set of changes.

---

## Step 1: Update Memory Log

1. Read the memory log at the path shown in `MEMORY.md` (currently `project_latest_changes.md`).
2. Prepend a new entry for today's date at the top (below the frontmatter), using this format:

```markdown
## YYYY-MM-DD: [Short Title of Changes]

**Goal**: [One sentence describing what was being accomplished]

### Changes:
1. **[Change name]** (`file.ts`) — [What changed and why]
2. ...

### Key design decisions:
- [Any non-obvious choices worth remembering]
```

3. Include: files created, files modified, behavioral changes, and design decisions.
4. Do NOT duplicate entries — check if today's date already has an entry and append to it if so.

5. Update the `MEMORY.md` index line for `project_latest_changes.md` to reflect the new entry in the summary hook (keep under 150 chars).

---

## Step 2: Output Commit Message

Output a commit title and description for the user to copy:

- **Title**: Prefix with the ticket code in square brackets, then conventional-commits format:
  `[<TICKET-CODE>] <type>: <summary>` (e.g. `[PAYSTUB-007] fix: correct off-by-one expense date display`).
  Infer the ticket code from the session context / `notes/<TICKET>.md` / branch name. If no ticket code can be determined, omit the prefix. Keep the whole title under 72 characters.
- **Description**: 1-2 sentences summarizing what changed and why. Reference specific areas affected.

Format the output clearly so the user can copy-paste:

```
**Commit title:** `[TICKET-CODE] feat: [title here]`

**Commit description:** `[description here]`
```

---

## Step 3: Output Patch Notes

Output a user-facing patch note title and pasteable markdown description.

- **Title**: Short, user-friendly (not developer jargon). e.g. "Cleaner Portal Improvements" not "feat: cleaner portal simplification"
- **Body**: Pasteable markdown using `###` subsections for each user-visible change. Written for end users (property managers, cleaners, clients), not developers. Explain what they can now do, not how it was implemented.

**IMPORTANT**: Always output the description as a standalone pasteable markdown block with `###` headings — no `##` wrapper title. The user will add their own title. Format exactly like this:

```markdown
### [Feature/Change 1]
[1-2 sentences explaining the user benefit]

### [Feature/Change 2]
[1-2 sentences explaining the user benefit]
```

---

## Rules

- Do NOT ask clarifying questions — infer everything from the conversation context and git diff.
- If no changes were made in this session, say so and skip all steps.
- Keep memory entries concise but complete enough to resume context in a future session.
- Patch notes should only cover user-visible changes. Internal refactors or code cleanup should appear in the commit message but NOT in patch notes.
