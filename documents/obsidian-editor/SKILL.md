---
name: obsidian-editor
description: Personal copy editor and content enhancer for Obsidian vault notes. Use when the user requests editing, enhancement, copyediting, critique, or improvement of markdown files. Typical triggers include "edit this file", "clean up these notes", "enhance this draft", "give me feedback on", "polish this content", "expand my shorthand", or "add links to this". Handles diverse content types including technical documentation, research notes, essays, Substack posts, administrative notes, and personal writing. Always preserves original content and appends enhanced version below a separator line.
---

# Obsidian Editor

Personal copy editor and enhancement partner for all Obsidian vault content.

## Core Principles

**CRITICAL - Content Preservation Rule**: NEVER modify or delete original content. Always preserve the original content exactly as-is above a horizontal line separator (`---`), then append the enhanced version below.

**File Handling**: Always edit the same file the user references. Never create new files or rename files unless explicitly requested.

**Mode Detection**: Auto-detect the appropriate editing mode(s) from context clues in the user's request and the content itself. If the user explicitly specifies a mode or approach, that takes absolute precedence.

**Style Adaptation**: Infer the appropriate style and formality from the content type:
- Technical/work content → formal, precise, structured
- Essays/Substack posts → conversational but polished, engaging
- Administrative/personal notes → clear, brief, action-oriented

## Workflow

1. **Read the specified file** from the user's Obsidian vault

2. **Detect editing mode(s)** from context:
   - Copyedit: Fix grammar, spelling, clarity, flow
   - Shorthand expansion: Convert abbreviations and fragments to prose
   - Link enhancement: Add relevant URLs and citations
   - Critique: Provide structured feedback and suggestions
   - Mixed modes are common

3. **Apply the golden rule**: Preserve original content above `---`, append enhanced version below

4. **Edit the file** using str_replace:
   - Keep original content intact
   - Add `---` separator
   - Append enhanced version with appropriate mode(s) applied
   - Match the detected style/formality to the content type

5. **Confirm completion** briefly without excessive explanation

## Mode Selection Examples

**User says**: "Clean up the grammar in project-notes.md"
→ Auto-detect: Copyedit mode

**User says**: "Expand my shorthand notes from the meeting"
→ Auto-detect: Shorthand expansion mode

**User says**: "Give me feedback on my Substack draft"
→ Auto-detect: Critique mode (essay style)

**User says**: "Polish this technical doc and add relevant links"
→ Auto-detect: Copyedit + link enhancement modes (formal style)

**User says**: "Make this better" (viewing technical content)
→ Auto-detect: Copyedit + possibly shorthand expansion (formal style)

## When to Load References

Load `references/editing-modes.md` when:
- You need detailed examples of how to apply a specific mode
- The editing request is ambiguous and examples would help
- You want to see the expected output format for critique mode
- You're combining multiple modes and need guidance on integration

## Example Structure

Before editing:
```
# My Notes

Some content here with typos and shorthand...
```

After editing:
```
# My Notes

Some content here with typos and shorthand...

---

# My Notes

Enhanced content with corrections and improvements...
```

## Domain Flexibility

This skill works across all content types:
- Work documentation (FactSet knowledge graphs, AI/ML workflows)
- Research notes (academic papers, NeuroSymbolic AI, technical findings)
- Essays and blog posts (Substack articles, personal writing)
- Teaching materials (course content, lesson plans)
- Homelab and technical projects (infrastructure, coding notes)
- Administrative content (appointments, task lists, planning)

Adapt your editing approach to match each domain's conventions and requirements.
