---
name: edit-article
description: Edit and improve article drafts by confirming a heading-based section plan, dependency order, then rewriting section by section with short paragraphs. Use when the user wants to revise or improve an article draft.
---

# edit-article

Use this skill to improve an article draft while preserving the author's intent and keeping the user in control of structure changes.

## When to Use

- The user asks to edit, revise, restructure, tighten, or improve an article draft.
- The article has headings or can be discussed as heading-based sections.
- The requested outcome is clearer prose, better coherence, and smoother flow.

## Do Not

- Rewrite the article before the user approves the section breakdown and order.
- Overwrite an article file unless the user explicitly asks for file edits.
- Add SEO, publishing, grammar-checker, or unrelated writing workflows.

## Workflow

1. **Divide the article into sections by headings.**
   Identify each section from the article's headings. For each section, state the main point it should make in one concise sentence.

2. **Map information dependencies.**
   Treat the article's information as a directed acyclic graph: facts, definitions, claims, examples, and conclusions can depend on earlier information. Note which sections depend on which other sections, and flag any section whose current position appears to violate those dependencies.

3. **Propose a dependency-safe section order.**
   Keep the original order when it already respects the dependency graph. If reordering would improve clarity, explain the smallest necessary change and why it improves the reader's path through the article.

4. **Confirm before rewriting.**
   Show the user:
   - The heading-based section breakdown.
   - The main point for each section.
   - The dependency notes and proposed order.
   - Any assumptions about missing or ambiguous headings.

   Ask the user to confirm or revise the breakdown and order. Stop here until the user approves.

5. **Rewrite one approved section at a time.**
   After approval, work through the confirmed order section by section. For each section:
   - Rewrite only that section before moving to the next.
   - Improve clarity, coherence, and flow.
   - Preserve the section's approved main point and required dependencies.
   - Keep every rewritten paragraph to 240 characters or fewer.
   - Ask before making major changes to meaning, evidence, tone, or structure.

6. **Review continuity after the section pass.**
   Once all approved sections are rewritten, check transitions and terminology across section boundaries. Suggest any final small connective edits, but keep the same 240-character paragraph limit for rewritten prose.

## Output Expectations

- During planning, return a concise section table or bullet list rather than rewritten prose.
- During rewriting, label each section clearly and keep revisions scoped to the current approved section.
- If the 240-character paragraph limit conflicts with the user's requested style, ask which constraint should win before continuing.
