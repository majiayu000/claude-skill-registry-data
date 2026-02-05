---
name: shiki
description: Shiki 3+ syntax highlighting. Use when highlighting code blocks, MDX content, or building code editors.
---

# Shiki 3+

## Create highlighter — v3 pattern

```ts
import { createHighlighter } from 'shiki'

const highlighter = await createHighlighter({
  themes: ['nord', 'github-dark'],
  langs: ['typescript', 'python'],
})

const html = highlighter.codeToHtml('const x = 1', {
  lang: 'typescript',
  theme: 'nord',
})

// NOT getHighlighter — that's v1
```

## Shorthand functions — no highlighter needed

```ts
import { codeToHtml, codeToTokens, codeToHast } from 'shiki'

// Direct usage (creates internal highlighter)
const html = await codeToHtml('const x = 1', {
  lang: 'typescript',
  theme: 'github-dark',
})

const { tokens } = await codeToTokens(code, { lang: 'ts', theme: 'nord' })
const hast = await codeToHast(code, { lang: 'css', theme: 'min-dark' })
```

## Rehype integration — @shikijs/rehype

```ts
import rehypeShiki from '@shikijs/rehype'
import remarkRehype from 'remark-rehype'
import { unified } from 'unified'

const processor = unified()
  .use(remarkParse)
  .use(remarkRehype)
  .use(rehypeShiki, {
    themes: {
      light: 'github-light',
      dark: 'github-dark',
    },
    // Inline code: `code{:lang}`
    inline: 'tailing-curly-colon',
  })
```

## Transformers — hook into rendering

```ts
import { transformerNotationHighlight } from '@shikijs/transformers'

const html = await codeToHtml(code, {
  lang: 'ts',
  theme: 'nord',
  transformers: [
    transformerNotationHighlight(), // [!code highlight]
    {
      // Custom transformer
      line(node, line) {
        node.properties['data-line'] = line
      },
      code(node) {
        this.addClassToHast(node, 'my-code-block')
      },
    },
  ],
})
```

## Fine-grained bundles — v3 engine system

```ts
import { createHighlighterCore } from 'shiki/core'
import { createOnigurumaEngine } from 'shiki/engine/oniguruma'

const highlighter = await createHighlighterCore({
  themes: [import('@shikijs/themes/nord')],
  langs: [import('@shikijs/langs/typescript')],
  engine: createOnigurumaEngine(() => import('shiki/wasm')),
})

// NOT loadWasm from 'shiki' — that's v1/v2
```

## Avoid

- `getHighlighter()` → `createHighlighter()`
- `loadWasm` from `'shiki'` → `createOnigurumaEngine` from `'shiki/engine/oniguruma'`
- `@shikijs/compat` → discontinued, use main package
- `postprocess` hook in rehype → doesn't run, use `root` hook instead
- `createdBundledHighlighter(fn, fn)` → single object argument in v3
