---
name: chinese-memoir-writing
description: Draft, revise, or review Chinese memoirs and narrative nonfiction from supplied source material. Use for scene-based prose, factual consistency, quotation fidelity, chapter continuity, and compiling an ordered Markdown manuscript to printable HTML.
license: MIT
metadata:
  version: "1.0.0"
---

# Chinese memoir writing

Support the author's chosen audience, purpose, voice, and level of disclosure.
Read [the style and factual-review guide](references/style-and-facts.md) before substantial drafting or revision. These are configurable editorial defaults, not an imitation of a named author.

## Draft or revise

- Establish the scene, narrator, source basis, and relationship to the wider chapter. Work from supplied notes, interviews, diaries, or a draft; do not invent nonfiction events, dates, dialogue, diagnoses, motives, or sensory details.
- Distinguish sourced facts, the narrator's recollection, and present-day interpretation. Flag unresolved matters in a separate author query list; keep uncertain details out of assertive prose.
- Preserve the meaning and emotional weight. Prefer precise actions and connected paragraphs; use sentence length and humor according to the author's voice and the scene.
- Explain abstract judgments through supported details. Keep trauma, loss, and conflict proportionate to the source rather than compressing them into a clever line.
- Quote faithfully and credit sources where appropriate. Only alter quotations with the author's instruction, with changes clearly distinguished from the original.
- Review chronology, names or approved aliases, recurring events, chapter continuity, and unsupported psychological inference. Return the revised passage with a concise list of unresolved factual questions when needed.

## Privacy and sharing

Use the author's approved public names or aliases. Avoid including unnecessary contact details, account identifiers, precise birth dates, addresses, private family history, unpublished third-party quotations, or project file paths in shared output. Anonymizing a name alone may leave a person recognizable from combined details.

Never invent a nonfiction event to fill a gap. If the author requests a composite or fictionalized example, label it explicitly and keep it separate from the factual manuscript. The bundled example is wholly fictional.

## Compile a manuscript

When the user wants an HTML/PDF-ready artifact, use:

```text
python scripts/build_book.py --input chapter-01.md chapter-02.md --title "Book title" --output book.html
```

The helper creates escaped, self-contained UTF-8 HTML with A5 print CSS. It supports a documented Markdown subset, removes editorial query sections headed exactly `待核实` or `Author queries`, and excludes their following content up to the next heading at the same or a higher level. It does not independently verify or anonymize the manuscript. Review the compiled HTML before sharing; PDF export uses the browser's Print / Save as PDF command.

Pass chapters in the intended order. Do not silently reorder them. Existing output is preserved unless the user chooses replacement (`--force`). The compiler does not embed images, contact external services, or export PDF automatically.
