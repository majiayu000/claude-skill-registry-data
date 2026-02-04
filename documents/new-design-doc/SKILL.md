---
name: new-design-doc
description: Proactively suggest creating a design document when discussing significant changes, new features, or architectural decisions. Also triggers when user has existing markdown docs that should be converted to org-mode. Use when conversation involves design decisions that should be documented, when user mentions RFC/RFD/design doc, or when proposing changes that warrant formal documentation. Trigger on phrases like "we should document this", "this needs an RFC", "let me think through the design", "convert this to org", or when discussing tradeoffs between multiple approaches.
---

# Design Doc Suggestion

This skill helps identify when a design document should be created and guides the process.

## When to Offer This

**Trigger conditions for NEW design doc:**
- Discussion involves significant architectural decisions
- Multiple approaches are being weighed with tradeoffs
- User mentions "RFC", "RFD", "design doc", "proposal"
- User says "we should document this", "let me think through..."
- A feature requires coordination across multiple components
- Changes that will affect how others use the system

**Trigger conditions for CONVERTING existing markdown:**
- User mentions "convert to org", "migrate to org-mode"
- User has markdown design docs in `docs/legacy/` or similar
- User asks about integrating old documentation
- Discussion references existing `.md` design documents
- User says "we have an old RFC", "there's a markdown doc for this"

**Proactive offers:**

For new doc:
"This seems like a significant design decision. Should I create a design doc to capture the motivation, options, and decision? That would help track the rationale and any implementation tasks."

For conversion:
"I see there's an existing markdown document for this. Should I convert it to org-mode format? I can extract the tasks, assign IDs, and optionally queue them to the backlog."

## Workflow

### 1. Confirm Scope

Ask:
- What's the one-sentence summary?
- What category? (Core, Feature, Infra, Tooling, Proposal)
- Any specific options already being considered?
- (If converting) Which markdown file should I convert?

### 2. Create the Document

**For new docs:** Use `/new-design-doc <title>` to scaffold, then:

1. Fill in **Summary** - one paragraph overview
2. Fill in **Motivation** - why this matters, what problem it solves
3. Fill in **Design** - options considered with tradeoffs
4. Add **Tasks** - implementation work with `[PROJECT-NNN-XX]` IDs
5. Add **Questions** - open issues as `** OPEN`

**For conversion:** Use `/new-design-doc <title> <source.md>` to convert, then:

1. Review the converted structure
2. Verify task IDs are properly assigned
3. Check that code blocks converted correctly
4. Offer to queue tasks to backlog

### 3. Use Org-Mode Properly

Remind yourself:
- Use `** TODO [PROJECT-NNN-XX] Task title` (not markdown checkboxes)
- Use `** OPEN Question` / `** DECIDED Question` (not plain text)
- Add `:PROPERTIES:` for EFFORT, VERSION, DECIDED date
- Reference the template: `docs/design/000-template.org`

### 4. Update Index

Add the new doc to `docs/design/README.org` in the appropriate section.

### 5. Queue Tasks (for conversions)

After converting, offer to queue extracted tasks:
- List tasks with their new IDs
- Ask which to queue to backlog Active section
- Use `/task-queue` for each selected task

## What Makes a Good Design Doc

| Section    | Good                                       | Bad                    |
|------------|-------------------------------------------|------------------------|
| Summary    | "Add caching layer to reduce API latency" | "Caching stuff"        |
| Motivation | Explains the problem and why it matters   | Jumps to solution      |
| Design     | Shows 2-3 options with tradeoffs          | Only shows chosen option|
| Tasks      | Specific, actionable, has IDs             | Vague, no IDs          |

## Conversion Rules Summary

| Markdown | Org-Mode |
|----------|----------|
| `## Heading` | `* Heading` |
| `- [ ] Task` | `** TODO [PROJECT-NNN-XX] Task` |
| `- [x] Task` | `** DONE [PROJECT-NNN-XX] Task` |
| ` ```lang` | `#+begin_src lang` |
| `[text](url)` | `[[url][text]]` |

## Files

- Template: `docs/design/000-template.org`
- Index: `docs/design/README.org`
- Examples: Any existing `docs/design/NNN-*.org`
