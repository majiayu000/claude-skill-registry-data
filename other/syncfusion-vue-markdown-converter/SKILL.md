---
name: syncfusion-vue-markdown-converter
description: Implement the Syncfusion Vue Markdown Converter to convert Markdown text into clean HTML. Use this when converting Markdown to HTML in Vue, integrating a live Markdown preview, configuring GFM or line break options, or working with MarkdownConverter.toHtml() and MarkdownConverterOptions. This skill covers the @syncfusion/ej2-markdown-converter package and Markdown Editor integration with side-by-side HTML preview.
metadata:
  author: "Syncfusion Inc"
  version: "34.1.29"
  category: "File Viewers & Editors"
---

# Implementing Syncfusion Vue Markdown Converter

The Syncfusion Vue Markdown Converter is a lightweight utility that transforms Markdown-formatted text into clean, semantic HTML. It is typically used alongside the Syncfusion Rich Text Editor (in Markdown mode) to provide a live preview of rendered content.

## When to Use This Skill

- Convert Markdown text to HTML in a Vue application
- Display a live preview of Markdown content as the user types
- Configure conversion behavior (GFM support, line breaks, async mode, error suppression)
- Build a side-by-side Markdown editor and HTML preview layout
- Integrate `MarkdownConverter.toHtml()` with the Syncfusion Rich Text Editor

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Vue CLI / Vite setup and project creation
- Installing `@syncfusion/ej2-markdown-converter` and `@syncfusion/ej2-vue-richtexteditor`
- CSS imports for the material3 theme
- Required module injection (MarkdownEditor, Image, Link, Toolbar, Table)
- Running the application

### Convert Markdown to HTML — toHtml API
📄 **Read:** [references/tohtml-api.md](references/tohtml-api.md)
- `MarkdownConverter.toHtml()` method signature
- Basic usage example (standalone, no editor required)
- Supported Markdown elements (headings, lists, tables, links, images, inline styles)
- Using the return value in Vue templates

### Configurable Options
📄 **Read:** [references/configurable-options.md](references/configurable-options.md)
- `MarkdownConverterOptions` interface
- `async` — asynchronous conversion for large content
- `gfm` — GitHub Flavored Markdown support (default: true)
- `lineBreak` — convert single line breaks to `<br>` (default: false)
- `silence` — suppress errors on invalid Markdown (default: false)
- Full example passing options to `toHtml()`

### Rich Text Editor Integration
📄 **Read:** [references/richtexteditor-integration.md](references/richtexteditor-integration.md)
- Splitter-based side-by-side editor and preview layout
- Configuring `ejs-richtexteditor` in Markdown `editorMode`
- Real-time preview using `onChange` and `updateValue()`
- Toolbar configuration for Markdown editing
- `MarkdownFormatter` for custom Markdown syntax
- Custom preview toggle button (fullPreview pattern)
- Mobile/device orientation handling with `Browser.isDevice`

## Quick Start

Install packages and wire up the converter in three steps:

**1. Install packages:**
```bash
npm install @syncfusion/ej2-markdown-converter
npm install @syncfusion/ej2-vue-richtexteditor
```

**2. Import CSS in `src/App.vue` or `src/main.js`:**
```js
import '@syncfusion/ej2-base/styles/material3.css';
import '@syncfusion/ej2-richtexteditor/styles/material3.css';
```

**3. Convert Markdown to HTML:**
```js
import { MarkdownConverter } from '@syncfusion/ej2-markdown-converter';

const markdown = '# Hello World\nThis is **Markdown** text.';
const html = MarkdownConverter.toHtml(markdown);
console.log(html);
// Output: <h1>Hello World</h1><p>This is <strong>Markdown</strong> text.</p>
```

## Common Patterns

### Pattern 1: Standalone Conversion (No Editor)
When you only need to convert a Markdown string to HTML without an editor UI:
```js
import { MarkdownConverter } from '@syncfusion/ej2-markdown-converter';

const html = MarkdownConverter.toHtml(markdownString);
document.getElementById('preview').innerHTML = html;
```

### Pattern 2: Live Preview on Keyup
Convert on every keystroke inside a Rich Text Editor textarea:
```js
markDownConversion() {
  const textarea = this.rteObj.contentModule.getEditPanel();
  const previewEl = document.getElementById('html-view');
  previewEl.innerHTML = MarkdownConverter.toHtml(textarea.value);
}
```

### Pattern 3: Conversion with Options
Disable GFM and enable line-break conversion:
```js
const html = MarkdownConverter.toHtml(markdownString, {
  gfm: false,
  lineBreak: true
});
```

### Pattern 4: Side-by-Side Preview with Splitter
For a full editor + preview experience, use the Syncfusion Splitter component alongside the Rich Text Editor in Markdown mode. The preview pane is updated via `updateValue()` on every change event.
📄 **Read:** [references/richtexteditor-integration.md](references/richtexteditor-integration.md) for the full implementation.

## Key Props / API

| API | Type | Default | Purpose |
|-----|------|---------|---------|
| `MarkdownConverter.toHtml(content, options?)` | static method | — | Converts Markdown string to HTML |
| `options.async` | boolean | `false` | Async conversion for large content |
| `options.gfm` | boolean | `true` | GitHub Flavored Markdown support |
| `options.lineBreak` | boolean | `false` | Single line breaks → `<br>` |
| `options.silence` | boolean | `false` | Suppress errors on invalid Markdown |
