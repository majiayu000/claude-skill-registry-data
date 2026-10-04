---
name: translate-lesson
description: Translate or sync an English lesson/topic into its Spanish twin (or vice-versa) for this Lessons site, keeping frontmatter, slugs, order, headings and interactive-component label props in parity. Spanish is ALWAYS peninsular Spanish from Spain (es-ES, Castilian — vosotros, ordenador/móvil), never Latin-American. Use when the user asks to "translate this lesson", "add the Spanish version", "sync the es twin", "traducir", or when an en/es pair has drifted.
---

# Translate / sync a bilingual twin

Every lesson and topic exists in **both** `en/` and `es/` at mirrored paths.
This skill keeps the pair in sync. The source is usually English; reverse the
directions if translating es → en.

## ⚠️ The `es` locale is Spanish from Spain (es-ES, Castilian)

All Spanish content is **peninsular Spanish (Spain)**, not Latin-American.
The site declares `es-ES` (see `astro.config.mjs` sitemap locales). Write
accordingly:

- **`vosotros`** for informal plural "you"; **`tú`** informal singular. Avoid
  `ustedes`/`vos` register choices that read as Latin-American.
- Castilian vocabulary: `ordenador` (not `computadora`), `móvil` (not `celular`),
  `vale` (not `okay`), `coche`, `zumo`, etc.
- Spain spelling/usage and natural peninsular idioms. `seseo`-neutral spelling
  is fine, but lexical choices must be Spain's.
- Humor and analogies (see `lesson-copy`) should land for a **Spain** audience —
  adapt references, don't translate them literally.

## 1. Locate the pair

```
en: src/content/lessons/en/<topic>/<lesson>.mdx
es: src/content/lessons/es/<topic>/<lesson>.mdx   ← same topic + lesson slug
```

Topics mirror the same way under `src/content/{topics,lessons}/<lang>/…`.
**Slugs and folder names stay identical across locales** — only the prose and
label props are translated, never the URL.

## 2. Keep frontmatter in parity

Copy the source frontmatter, translate `title` / `description` / `tagline`, and
change only the locale-bound `topic` reference:

- es lesson: `topic: "es/<topic>"` (en uses `"en/<topic>"`).
- Keep `order`, `minutes`, `icon`, `accent`, `draft` **identical** to the twin.
- Keep `updated` in sync (bump both when content changes).

## 3. Translate body, preserve structure

- Same number and nesting of `##` / `###` headings (they drive the ToC) —
  translate the heading text, keep the hierarchy.
- Keep all `import { … } from '@/components/react'` lines unchanged.
- Translate prose, `Callout` titles/bodies, `MCQ`/`Quiz` questions, options,
  and explanations.
- Keep math, code blocks, and `client:*` directives byte-identical.

## 4. Localize component label props (critical)

Interactive islands render UI chrome in their props — pass the Spanish labels in
the es file:

- `MCQ`: `checkLabel="Comprobar"`, `retryLabel="Reintentar"`
- `Quiz`: `questionLabel="Pregunta"`, `ofLabel="de"`, `scoreLabel="Tu puntuación"`,
  `restartLabel="Reiniciar"`, `nextLabel="Siguiente"`, `backLabel="Atrás"`
- `MCQ pretest`: `pretestLabel="Antes de leer — adivina"` (+ the usual MCQ labels)
- `MatchConcepts` / `Categorize` / `FillBlank`: `checkLabel="Comprobar"`,
  `retryLabel="Reintentar"`, `explanationLabel="Explicación"`, and translate
  `instructions` (e.g. `"Coloca cada elemento en su grupo."` /
  `"Elige la opción correcta para cada hueco y comprueba."`)
- `MindMap`: translate `title`, `caption`, `eyebrow="Visión de conjunto"`,
  `outlineLabel="Esquema"`, **and every node `label`** in the `root` tree
  (`FillBlank` `text` blanks — the correct answer AND its distractor options —
  must all be translated to Spanish)

Confirm exact prop names against `src/components/react/*` (or `DESIGN.md`)
before writing — props evolve.

## 5. Verify parity

```bash
bun run check     # 0 errors required
```

Check both twins exist, share slug/order/topic, and have the same heading count.
Then regenerate OG cards and stage them:

```bash
bun run pre-commit   # audit:fix + check + build + og:generate
git add public/og
```
