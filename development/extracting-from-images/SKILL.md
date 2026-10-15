---
name: extracting-from-images
description: Use when user pastes a screenshot / image. Extract text, layout, intent — don't just describe pixels.
---

# Extracting From Images — Read for Intent

When the user pastes a screenshot or image, your job is to **act on its content**, not narrate what's visible. "I see a screenshot showing some code" is useless. The user already knows it's a screenshot. They want you to read it.

## Iron Law

**Never describe an image in the abstract. Identify what it is, extract the content verbatim, and infer why the user sent it.** If a screenshot contains code, you reproduce the code (or the relevant slice). If it contains an error, you transcribe the error. If it's a UI, you list the structure.

## Workflow

1. **Classify** — what kind of image is this?
   - UI / app screenshot
   - Code (editor / terminal output)
   - Error message / stack trace
   - Design mockup
   - Diagram (architecture / flow / ERD)
   - Chart / graph / data
   - Other (photo, meme, document scan)
2. **Extract** — pull the load-bearing content. OCR-style for text; structure-summary for layout.
3. **Infer intent** — why did the user share this? (Bug to fix? Implement this mockup? Explain this diagram? Replicate this UI?)
4. **Ask once if unclear** — but only if intent is genuinely ambiguous. Most of the time it's obvious from context.

## Per-Type Playbook

### Code screenshot

The user pasted code as image (probably because copy-paste was awkward).

- **Transcribe the code precisely.** Variable names, numbers, operators, indentation, language — all verbatim.
- Then act on it (review / debug / extend / explain), depending on the conversation.
- Don't write "the screenshot shows a Python function". Write the function.

### Error / stack trace

- Transcribe the error message verbatim, including the exception type, message, and file:line.
- Identify the deepest frame in user code (not framework internals).
- Ask "what were you doing when this happened?" / "what changed recently?" if not obvious.
- If you can see relevant lines in a project, Grep/Read them now.

### UI / app screenshot

User probably wants to:
- replicate this in code, or
- report a bug in something rendered (visual diff from expected), or
- ask how to build a piece of it.

- List the structural elements: header, nav, primary action, form fields, list items, modals.
- Mark which are interactive (buttons, links, inputs) vs static.
- Note any visible state (errors, loading, empty state).
- If it's a bug report, ask: "what should this look like instead?"

### Design mockup

- Same as UI, but treat it as a spec. Map every visible element to a component name.
- Call out ambiguities: typography weights, spacing, what happens on hover, responsive behavior — mockups don't show these.

### Diagram

- Identify the abstraction level: system architecture? code module dependencies? data flow? state machine?
- List nodes and label the edges.
- If unclear which layer, ask: "is this code-level or system-level?"
- Don't try to "improve" the diagram unless asked.

### Chart / data

- Read the axes (variable, units, scale).
- Pull headline numbers (max, min, trend).
- Note the question this chart answers, and what's missing.

## Red Flags

- "The screenshot shows a piece of code that defines a function." — WRONG. Transcribe the code.
- "I see an error message." — WRONG. Quote it exactly with file/line.
- "This looks like a login page." — fine as an opener, but follow with structural breakdown and ask what to do.
- You describe the image and stop without offering action. The user already saw the image; they want next steps.
- You ignore visible text because "the user can see it" — they want you to engage with it.
- You hallucinate text that's blurry/unclear. Better: "Can you confirm line 47 reads `...`? It's slightly blurry."

## Examples

### Good

User pastes a screenshot of a Python `TypeError` traceback.

> Error: `TypeError: 'NoneType' object is not subscriptable` at `app/handlers.py:84` in `process_user(...)`, called from `route.py:32`.
>
> The deepest user-code frame is `handlers.py:84`. Most likely `user["..."]` where `user` is None — probably the DB lookup before it returned no row. Want me to check `handlers.py:80-90`?

### Bad

> I see a screenshot of a Python error. It looks like a TypeError. You should check your code.

### Good

User pastes a UI mockup of a settings page.

> Mockup contents:
> - Header: "Settings" (h1), back arrow on left
> - Section "Account": fields Email (readonly), Display Name (editable), Avatar (image + upload button)
> - Section "Notifications": 3 toggle switches — Email, Push, Weekly Digest
> - Footer: "Save Changes" primary button, "Cancel" secondary
>
> Ambiguities I'd want before building:
> - Avatar upload — single click or modal?
> - Save button — does it submit only changed fields or all?
> - Validation on Display Name (length / chars)?

### Bad

> This is a settings page with some fields and buttons. I can help you build something like this!

## Not For

- The user did not paste an image. Don't ask for one.
- The image is purely conversational (a meme reaction). Acknowledge briefly, don't dissect.

## See Also

- `[[using-claude-api]]` — if implementing image input handling in your own Claude API code.
- `[[lean-context]]` — for big images, don't ask Claude to OCR everything if only a corner is relevant.
