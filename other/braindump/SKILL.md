---
name: braindump
category: knowledge
description: >
  Takes raw unstructured thoughts, voice transcript dumps, or stream-of-consciousness text
  and auto-files them into the right Obsidian vault folders with tags, backlinks, and proper
  frontmatter. Use when the user says "braindump", "brain dump", "capture this", "dump my
  thoughts", "I'm thinking about...", or provides a long unstructured block of text to organize.
---

# Braindump

Turn messy thoughts into organized vault entries.

## Workflow

1. **Receive raw input** — Accept any unstructured text: stream-of-consciousness, voice transcript,
   bullet points, mixed topics, rambling notes. Do not ask the user to organize it first.

2. **Extract discrete topics** — Parse the input and identify distinct topics, ideas, or threads.
   Each becomes a separate note or gets appended to an existing note.

3. **Classify each topic** — Determine the best vault location:
   - **Project idea** → `projects/ideas/`
   - **Task / action item** → extract as task with `- [ ]` checkbox, link to relevant project
   - **Decision or opinion** → `decisions/` with decision-log format
   - **Learning / insight** → `references/` or relevant project's `docs/`
   - **Personal reflection** → `journal/`
   - **Technical note** → `references/technical/`
   - **Meeting note** → `meetings/`

4. **Generate backlinks** — For each note, identify:
   - Existing vault notes it should link to (use `[[wikilink]]` syntax)
   - Tags that connect it to broader themes (`#project-name`, `#idea`, `#decision`)
   - Any people mentioned → `[[People/Name]]`

5. **Write frontmatter** — Each note gets:
   ```yaml
   ---
   type: braindump
   source: [user-input | voice-transcript | meeting]
   date: [YYYY-MM-DD]
   topics: [list of extracted topics]
   tags: [relevant tags]
   ---
   ```

6. **Present summary** — Show the user what was created:
   - List of notes created/updated
   - Key backlinks established
   - Any action items extracted

## Output Format

```markdown
## Braindump Processed

**Input**: [brief description of what was provided]
**Date**: [YYYY-MM-DD]

### Notes Created
1. `projects/ideas/[topic].md` — [one-line summary]
2. `references/technical/[topic].md` — [one-line summary]

### Action Items Extracted
- [ ] [action] → linked to [[Project]]
- [ ] [action] → linked to [[Project]]

### Backlinks Established
- [[Existing Note]] ← new connection from [topic]
```

## Vault Paths

Default vault: `~/broomva-vault/`

If the vault is not accessible, output the notes as markdown blocks the user can manually save.

## Tips

- Preserve the user's voice — don't over-formalize raw thoughts
- When in doubt about classification, use `inbox/` and tag for later sorting
- Extract dates mentioned in the text and convert to absolute dates
- If the input mentions people, create or link to People notes
