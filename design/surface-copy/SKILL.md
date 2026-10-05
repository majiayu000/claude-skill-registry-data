---
name: surface-copy
description: Write and review interface copy that guides, explains, reassures, or persuades. Use when drafting or improving error message bodies, empty states, helper text, onboarding text, tooltip prose, loading text, success or warning messages, confirmation body copy, and marketing-style CTA copy. Also triggers for UX writing, microcopy, tone, localisation notes, or "this copy feels unclear". Does NOT own product action labels, command names, menu items, feature names, product names, component names, token names, or UI terminology (use system-naming). Does NOT decide placement or flow structure (use system-patterns), component state coverage (use system-components), or accessibility mechanics (use surface-details).
---

# Copy

Interface copy that helps people understand what is happening, what they can do next, and what a product needs from them.

**system-naming names actions and concepts. surface-copy writes the surrounding language.** Keep this boundary clear. Do not override product action labels, command names, feature names, component names, token names, or glossary terms chosen by system-naming.

For multi-skill task sequencing, see `references/composition.md`.

---

## Before Writing

Identify:

- Screen, flow, and state.
- User goal and emotional state.
- The action or concept names established by system-naming.
- Constraints: character limit, layout, truncation, localisation, legal, platform.
- Tone: neutral, reassuring, celebratory, urgent, or promotional.

If the vocabulary is unstable, use system-naming first.

---

## Ownership Boundary

| Need | Lead |
|---|---|
| Product action labels, command names, menu items | `system-naming` |
| Feature names, product names, UI terminology | `system-naming` |
| Error message body text | `surface-copy` |
| Empty state title and body text | `surface-copy` with terms from `system-naming` |
| Helper text, hints, onboarding, loading, success, warning, tooltip prose | `surface-copy` |
| Marketing-style CTA copy | `surface-copy` |
| Where feedback appears | `system-patterns` |
| Whether a state exists | `system-components` |

For full flows, sequence them:

```text
system-naming -> system-patterns -> surface-copy
```

system-naming establishes vocabulary and action labels. system-patterns decides placement and flow. surface-copy writes the explanatory and tonal layer.

---

## Copy Patterns

### Errors

Structure: what happened, why if useful, how to fix.

```text
Payment declined. Try a different card or contact your bank.
```

- Be specific when the system knows the cause.
- Avoid blame: not "You entered an invalid card."
- Do not say "Something went wrong" when a recoverable cause is known.
- Keep recovery close to the failed action.

### Empty States

Structure: what is empty, why it is empty, what to do next.

```text
No projects yet. Create a project to start organising your work.
```

- If there is a natural first action, point to it.
- If the empty state is expected and no action is needed, say so plainly.
- Avoid motivational filler when the user needs instruction.

### Helper Text

Use helper text to prevent errors before they happen.

- Explain constraints before validation: `Use at least 12 characters.`
- Give examples when format matters.
- Keep field helper text below the field or near the control it explains.
- Do not hide required guidance in tooltips.

### Confirmation Dialogues

The action label belongs to system-naming. The body copy explains consequence and recovery.

```text
This will permanently delete 12 files. This cannot be undone.
```

- Name the object and scope.
- State irreversibility only when true.
- If the action is reversible, prefer undo copy over a blocking warning.

### Loading, Success, and Warning

- Loading copy sets expectations without fake precision.
- Success copy confirms the outcome, then gets out of the way.
- Warning copy explains risk and the next safe action.

```text
Uploading files. You can keep editing while this finishes.
```

### Tooltips

Tooltips clarify unfamiliar icons, controls, or constraints. They do not repeat visible labels and must not contain critical instructions.

### Onboarding

Introduce one concept at a time. Prefer progressive disclosure over long setup tours. Let people act as soon as possible.

### Marketing-Style CTAs

Use surface-copy for persuasive CTAs outside routine product commands:

```text
Start free trial
Talk to sales
Join the beta
```

Even promotional CTAs should match the actual outcome. Avoid vague labels like `Learn more` when the destination is specific.

---

## Voice And Tone

- Neutral by default.
- Reassuring for errors and warnings.
- Briefly celebratory for meaningful success.
- Direct for destructive consequences.
- Promotional only in marketing or onboarding contexts.

Tone must never make the copy less clear.

---

## Output Format

When writing or reviewing copy, use this structure when useful:

```markdown
## Recommended Copy

**Element**: Copy

## Alternatives

| Option | Copy | Best for |
|---|---|---|
| A | ... | ... |

## Rationale

Why the copy works for the user state, flow, and constraints.

## Localisation Notes

Terms, idioms, length risks, or cultural assumptions to watch.
```

For small implementation tasks, apply the copy directly and summarise the change.

---

## Anti-Patterns

1. **Copy that renames the product model.** Do not introduce synonyms that fight system-naming.
2. **Vague recovery.** "Try again later" when a specific fix is available.
3. **Blame.** "You failed to..." or "You entered..."
4. **False reassurance.** "This will only take a second" when it might not.
5. **Over-celebrating routine tasks.** Saving settings does not need confetti in words.
6. **Critical information in tooltips.** Important guidance must be visible in the flow.
7. **Marketing tone in operational UI.** Routine product work needs clarity before persuasion.
8. **Unlocalisable idioms.** Avoid jokes, puns, and metaphors that translators cannot preserve.

---

## Checklist

- Uses established terminology from system-naming
- Explains what happened and what to do next
- Gives specific recovery when possible
- Keeps critical information visible
- Matches tone to user state
- Avoids jargon and internal mechanism names
- Avoids introducing synonyms
- Considers localisation and text expansion
- Fits the available UI space

---

## Learning from Usage

After completing a copy task, review whether the wording stayed clear in the actual interface, matched established terminology, and survived layout or localisation constraints. Append durable findings to `learnings.md` in this skill's folder. Installed learnings are local runtime notes preserved across suite updates; consult `learnings.md` before starting a new copy task.
