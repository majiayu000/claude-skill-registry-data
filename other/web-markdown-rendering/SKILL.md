---
name: web-markdown-rendering
description: Rendering Markdown to styled HTML in a browser page with Marked, Highlight.js, and the Catppuccin palette. Use when a frontend displays notes, documentation, or any user-supplied Markdown, when adding syntax highlighting, callout blocks, or code copy buttons, or when styling rendered Markdown. Triggers on marked.parse, marked.use, hljs.highlight, .markdown-body, callout blockquotes such as [!TIP] and [!WARNING], and copy-to-clipboard buttons on code blocks.
user-invocable: false
---

# Web Markdown Rendering

**Marked parses, Highlight.js colors the code, Lucide draws the callout icons, and one CSS block styles everything in Catppuccin Mocha.**

The libraries are vendored and pinned, never loaded from a CDN at run time: `marked@18.0.11`, `highlight.js@11.12.0` with its `github-dark` theme.

```html
<script src="/static/js/marked.umd.js"></script>
<script src="/static/js/highlight.min.js"></script>
<link rel="stylesheet" href="/static/css/github-dark.min.css">
```

## Call Order

The four steps run in this order after every content change, because each depends on the DOM the previous one produced.

```javascript
container.innerHTML = marked.parse(markdownSource);
addCopyButtons();
if (typeof mermaid !== 'undefined') {
    mermaid.initialize(mermaidConfig);
    mermaid.run({ nodes: container.querySelectorAll('.mermaid') });
}
lucide.createIcons();
```

`lucide.createIcons()` runs last and unconditionally, since it replaces `<i data-lucide>` placeholders with inline SVG and the callout renderer emits those placeholders on every parse.

## The Renderer

`marked.use({ renderer })` is called once at startup. Overriding four token types covers code fences, heading anchors, images, and callouts; everything else keeps Marked's default output.

```javascript
function generateId(text) {
    return String(text).toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)+/g, '');
}

function initMarked() {
    const renderer = {
        code(token) {
            const text = token.text;
            const language = token.lang;
            if (language === 'mermaid') {
                return `<div class="overflow-x-auto my-6"><div class="mermaid">${text}</div></div>`;
            }
            const validLang = hljs.getLanguage(language) ? language : 'plaintext';
            let highlighted = text;
            try {
                highlighted = hljs.highlight(text, { language: validLang }).value;
            } catch {
                // an unknown grammar falls back to the raw text rather than dropping the block
            }
            return `<pre><code class="hljs language-${validLang}">${highlighted}</code></pre>`;
        },
        heading(token) {
            const { tokens, depth } = token;
            const text = this.parser.parseInline(tokens);
            const slug = generateId(text.replace(/<[^>]*>/g, ''));
            return `<h${depth} id="${slug}">${text}</h${depth}>`;
        },
        image(token) {
            return `<img src="${token.href}" alt="${token.text || ''}" style="max-width:100%; border-radius:0.5rem;">`;
        },
        blockquote(token) {
            const body = this.parser.parse(token.tokens);
            const match = token.text.match(/^\[!(TIP|NOTE|INFO|WARNING|DANGER)\]/i);
            if (!match) {
                return `<blockquote>${body}</blockquote>`;
            }
            const type = match[1].toLowerCase();
            const iconMap = {
                tip: 'lightbulb',
                info: 'info',
                danger: 'triangle-alert',
                warning: 'triangle-alert',
                note: 'sticky-note',
            };
            const cleanBody = body.replace(/<p>\s*\[!(TIP|NOTE|INFO|WARNING|DANGER)\]\s*/i, '<p>');
            return `<div class="callout ${type}"><div class="callout-icon"><i data-lucide="${iconMap[type] || 'info'}"></i></div><div class="callout-content">${cleanBody}</div></div>`;
        },
    };
    marked.use({ renderer });
}
```

A `mermaid` fence becomes a `<div class="mermaid">` rather than a highlighted code block, because Mermaid's own renderer takes over that element afterwards.

Heading IDs are slugged from the rendered text with tags stripped, so a heading containing inline code or a link still produces a usable anchor.

The unknown-grammar catch keeps the original text. Letting the exception propagate would abort the whole parse over one fence with a typo in its language tag.

## Copy Buttons

A clipboard button is injected on each `<pre>` block. It appears on hover, confirms with a check icon for two seconds, then reverts.

```javascript
function addCopyButtons() {
    document.querySelectorAll('.markdown-body pre').forEach((block) => {
        if (block.querySelector('.copy-code-btn')) return;
        if (block.querySelector('.mermaid')) return;

        const codeEl = block.querySelector('code');
        if (!codeEl) return;

        const button = document.createElement('button');
        button.className = 'copy-code-btn';
        button.type = 'button';
        button.innerHTML = '<i data-lucide="copy" class="w-4 h-4"></i>';

        button.onclick = async (e) => {
            e.preventDefault();
            e.stopPropagation();
            try {
                await navigator.clipboard.writeText(codeEl.textContent);
            } catch {
                const textarea = document.createElement('textarea');
                textarea.value = codeEl.textContent;
                textarea.style.position = 'fixed';
                textarea.style.opacity = '0';
                document.body.appendChild(textarea);
                textarea.select();
                document.execCommand('copy');
                document.body.removeChild(textarea);
            }
            button.innerHTML = '<i data-lucide="check" class="w-4 h-4"></i>';
            button.classList.add('copied');
            lucide.createIcons({ nodes: [button] });
            setTimeout(() => {
                button.innerHTML = '<i data-lucide="copy" class="w-4 h-4"></i>';
                button.classList.remove('copied');
                lucide.createIcons({ nodes: [button] });
            }, 2000);
        };

        block.appendChild(button);
    });
    lucide.createIcons();
}
```

The early return on an existing button makes the function safe to call after every render, which it has to be, since re-parsing replaces the container's contents.

Mermaid blocks are skipped because a diagram's source is not what a reader wants on the clipboard.

The `textarea` fallback covers pages served over plain HTTP, where `navigator.clipboard` is unavailable because the context is not secure.

## Styles

Marked generates this subtree, so its classes are not yours to write and Tailwind utilities cannot reach it. Hand-written CSS is the correct tool here and is one of the named exceptions to the utility-first rule.

Every color reads a `--ctp-*` variable from the page palette rather than a literal. A hardcoded hex here is a color that stops following the theme the moment the page gains a light mode, and it is the one place a stale value survives a palette change unnoticed.

The rendered body sits inside a `mantle` panel, so a fenced block takes `base`, the well one rung further in.

```css
.markdown-body {
    background-color: transparent !important;
    font-family: 'Inter', sans-serif !important;
    color: var(--ctp-subtext0) !important;
    line-height: 1.6;
    font-size: 16px;
}
```

### Headings

Each level takes a distinct Catppuccin color so the outline is readable at a glance rather than by font size alone. H1 and H2 carry bottom borders.

```css
.markdown-body h1, .markdown-body h2, .markdown-body h3 {
    margin-top: 24px;
    margin-bottom: 16px;
    font-weight: 600;
    line-height: 1.25;
    padding-bottom: 0.3em;
}
.markdown-body h1 { font-size: 2em;     color: var(--ctp-lavender) !important; border-bottom: 1px solid var(--ctp-surface0); }
.markdown-body h2 { font-size: 1.5em;   color: var(--ctp-mauve) !important; border-bottom: 1px solid color-mix(in oklab, var(--ctp-surface0) 50%, transparent); }
.markdown-body h3 { font-size: 1.25em;  color: var(--ctp-blue) !important; }
.markdown-body h4 { font-size: 1em;     color: var(--ctp-text); font-weight: 600; }
.markdown-body h5 { font-size: 0.875em; color: var(--ctp-text); font-weight: 600; }
.markdown-body h6 { font-size: 0.85em;  color: var(--ctp-subtext0); }
```

### Text, links, and lists

```css
.markdown-body p { margin-bottom: 16px; }
.markdown-body a { color: var(--ctp-blue); text-decoration: none; }
.markdown-body a:hover { text-decoration: underline; }

.markdown-body ul, .markdown-body ol { padding-left: 2em; margin-bottom: 16px; }
.markdown-body ul { list-style-type: disc; }
.markdown-body ol { list-style-type: decimal; }
.markdown-body li { margin-bottom: 0.25em; }
```

### Code

Inline code is peach on surface0, and a fenced block is plain text on base. The two need different treatments because inline code has to stand out inside a sentence while a block already stands out by being a block.

```css
.markdown-body code {
    font-family: 'JetBrains Mono', monospace;
    color: var(--ctp-peach) !important;
    background-color: var(--ctp-surface0) !important;
    border-radius: 4px;
    padding: 0.2em 0.4em;
    font-size: 0.9375em;
}
.markdown-body pre {
    position: relative;
    background-color: var(--ctp-base) !important;
    border-radius: 0.75rem;
    padding: 1rem !important;
    margin-bottom: 16px;
    overflow: auto;
}
.markdown-body pre code {
    color: inherit !important;
    background-color: transparent !important;
    padding: 0;
    font-size: 0.9375em;
}
```

`pre code` resets the inline rules, or every fenced block would render orange on a second background.

### Tables

```css
.markdown-body table {
    display: table !important;
    width: 100% !important;
    border-collapse: separate;
    border-spacing: 0;
    border: 1px solid color-mix(in oklab, var(--ctp-surface1) 50%, transparent);
    border-radius: 8px;
    overflow: hidden;
    margin-bottom: 1.5rem;
}
.markdown-body table thead { background-color: color-mix(in oklab, var(--ctp-mauve) 10%, transparent); }
.markdown-body table tr { background-color: transparent !important; border: none !important; }
.markdown-body table tr:nth-child(2n) { background-color: color-mix(in oklab, var(--ctp-surface0) 30%, transparent) !important; }
.markdown-body table th {
    color: var(--ctp-mauve) !important;
    font-weight: 600;
    border: none !important;
    border-bottom: 1px solid color-mix(in oklab, var(--ctp-surface1) 50%, transparent) !important;
    border-right: 1px solid color-mix(in oklab, var(--ctp-surface0) 50%, transparent);
    padding: 12px 16px !important;
    text-align: left;
}
.markdown-body table td {
    border: none !important;
    border-bottom: 1px solid color-mix(in oklab, var(--ctp-surface0) 30%, transparent) !important;
    border-right: 1px solid color-mix(in oklab, var(--ctp-surface0) 30%, transparent);
    color: var(--ctp-subtext0) !important;
    padding: 12px 16px !important;
    text-align: left;
}
.markdown-body table th:last-child, .markdown-body table td:last-child { border-right: none; }
.markdown-body table tr:last-child td { border-bottom: none !important; }
```

`border-collapse: separate` with `overflow: hidden` is what lets the rounded corners clip the header background; collapsed borders ignore the radius.

### Blockquotes, rules, and copy buttons

```css
.markdown-body blockquote {
    border-left: 0.25em solid color-mix(in oklab, var(--ctp-surface1) 50%, transparent);
    padding: 0 1em;
    color: var(--ctp-subtext0);
    margin-bottom: 16px;
}
.markdown-body hr { border: none; border-top: 1px solid var(--ctp-surface0); margin: 1.5em 0; }

.copy-code-btn {
    position: absolute;
    top: 0.5rem;
    right: 0.5rem;
    padding: 0.5rem;
    background-color: color-mix(in oklab, var(--ctp-surface0) 95%, transparent);
    border-radius: 0.375rem;
    color: var(--ctp-subtext0);
    cursor: pointer;
    opacity: 0;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 10;
}
pre:hover .copy-code-btn { opacity: 1; }
.copy-code-btn:hover { background-color: var(--ctp-surface1); color: var(--ctp-mauve); }
.copy-code-btn.copied { color: var(--ctp-green); }
```

### Callouts

```css
.callout {
    padding: 1rem;
    border-radius: 0.5rem;
    margin-bottom: 1rem;
    display: flex;
    gap: 0.75rem;
    align-items: flex-start;
    background-color: color-mix(in oklab, var(--ctp-surface0) 20%, transparent);
}
.callout-icon {
    display: inline-flex;
    align-items: center;
    flex-shrink: 0;
    line-height: 1;
    padding-top: 0.3em;
}
.callout-icon svg { width: 1em; height: 1em; }
.callout-content { flex: 1; }
.callout-content p { margin: 0 !important; }

.callout.tip     { background-color: color-mix(in oklab, var(--ctp-green) 10%, transparent); }
.callout.tip     .callout-icon { color: var(--ctp-green); }
.callout.info    { background-color: color-mix(in oklab, var(--ctp-blue) 10%, transparent); }
.callout.info    .callout-icon { color: var(--ctp-blue); }
.callout.danger  { background-color: color-mix(in oklab, var(--ctp-red) 10%, transparent); }
.callout.danger  .callout-icon { color: var(--ctp-red); }
.callout.warning { background-color: color-mix(in oklab, var(--ctp-peach) 10%, transparent); }
.callout.warning .callout-icon { color: var(--ctp-peach); }
.callout.note    { background-color: color-mix(in oklab, var(--ctp-mauve) 10%, transparent); }
.callout.note    .callout-icon { color: var(--ctp-mauve); }
```

Each type tints its background at 10% opacity and saturates only the icon, so a page of callouts stays readable instead of turning into five blocks of solid color.

### Scrollbars

```css
::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-track { background: var(--ctp-crust); }
::-webkit-scrollbar-thumb { background: var(--ctp-surface0); border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: var(--ctp-surface1); }
```
