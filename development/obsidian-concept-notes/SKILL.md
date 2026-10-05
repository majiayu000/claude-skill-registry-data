---
name: obsidian-concept-notes
description: Create or update independent Obsidian concept notes that build durable understanding through motivation, intuition, definitions, mechanisms, examples, boundaries, applications, knowledge links, self-tests, and correctly rendered collapsible answers. Use when the user asks to explain a concept and turn it into an Obsidian permanent/evergreen note, or to create concept notes from course knowledge links. Do not use for ordinary lecture summaries.
---

# Obsidian Concept Notes

Create a standalone Concept Note / Evergreen Note / Permanent Note rather than a slide-by-slide lecture summary.

## Required workflow

1. Read [references/concept-note-spec.md](references/concept-note-spec.md) completely before drafting or editing a concept note.
2. Infer the concept's domain from the current conversation, course context, and common usage. Ask only when genuinely different meanings remain plausible.
3. Follow the specification's learning sequence, YAML properties, Markdown structure, formula guidance, examples, boundaries, comparisons, knowledge links, self-test, and file-generation requirements.
4. Adapt depth to concept complexity. Do not add material merely to fill every optional subsection.
5. If a source course note is available, read the relevant context and preserve its notation while clearly identifying legitimate alternative conventions.
6. Create the UTF-8 `.md` file directly when the environment permits. Preserve existing user content and avoid overwriting a same-named note without inspecting it.
7. Validate that YAML starts on line 1, Obsidian links and LaTeX are well formed, code fences are paired, and the collapsible answer block follows the invariant below.

## Collapsible answer invariant

Use an Obsidian folded callout for self-test answers:

```markdown
> [!question]- 点击查看答案
> 参考答案
>
> 1. 第一题答案。
> 2. 第二题答案。
```

- Keep every answer line inside the same blockquote; prefix nonempty lines with `> ` and blank lines with `>`.
- Keep the hyphen in `[!question]-` so the callout is collapsed by default.
- Do not use HTML `<details>` or `<summary>` for answers.
- Before delivery, verify that no answer text falls outside the callout.
