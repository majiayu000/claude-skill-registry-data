---
name: obsidian
description: Expert knowledge for developing Obsidian plugins and themes using TypeScript, CodeMirror 6, and CSS variables - covers plugin lifecycle, Vault API, Workspace API, editor extensions, and styling patterns
hash: 881a7930a553c0d8
---

# Obsidian Plugin & Theme Development

Build plugins and themes for Obsidian using TypeScript, CodeMirror 6, and CSS variables.

## Core Principles

- **Extend Plugin class** - Use `onload()` for setup, `onunload()` for cleanup
- **Access app via `this.app`** - Never use global `window.app` (debugging only)
- **Prefer Vault API** - Use `this.app.vault` over raw `Adapter` for file ops
- **Wait for layout ready** - Use `app.workspace.onLayoutReady()` for startup logic
- **Register events properly** - Use `this.registerEvent()` for auto-cleanup
- **Mark external CM6 deps** - Never bundle `@codemirror/*`, use Obsidian's copy
- **Use CSS variables** - Override theme variables, not hardcoded colors
- **Avoid `!important`** - Let users override with snippets
- **Mobile compatibility** - Check `Platform.isMobile` before Node.js APIs
- **Security first** - Never use `innerHTML` with user input

## Quick Reference

```typescript
// Basic plugin structure
import { Plugin, Notice } from 'obsidian';

export default class MyPlugin extends Plugin {
  async onload() {
    // Add command
    this.addCommand({
      id: 'my-command',
      name: 'My Command',
      callback: () => new Notice('Hello!')
    });

    // Add ribbon icon
    this.addRibbonIcon('dice', 'My Plugin', () => {});

    // Register events (auto-cleanup on unload)
    this.registerEvent(
      this.app.vault.on('modify', (file) => {})
    );

    // Register CM6 extension
    this.registerEditorExtension(myExtension);
  }
}
```

## Topics

### Plugin Development

- [Plugin Development](./plugin-development.md) - Lifecycle, API, commands, settings, events

### Editor Integration

- [CodeMirror 6](./codemirror-6.md) - State, view, decorations, extensions

### Styling

- [Themes & CSS](./themes-css.md) - CSS variables, theme structure, styling patterns

### Advanced APIs

- [Bases API](./bases-api.md) - Custom database views (Obsidian 1.10+)
- [Canvas API](./canvas-api.md) - Visual canvas manipulation

## Common Patterns

### Wait for Vault Ready

```typescript
async onload() {
  this.app.workspace.onLayoutReady(() => {
    // Safe to access vault files here
    const files = this.app.vault.getMarkdownFiles();
  });
}
```

### Process Frontmatter Safely

```typescript
await this.app.fileManager.processFrontMatter(file, (fm) => {
  fm.status = 'done';
});
```

### Register Editor Extension

```typescript
import { ViewPlugin, DecorationSet } from '@codemirror/view';

const myPlugin = ViewPlugin.fromClass(class {
  decorations: DecorationSet;
  // ... implementation
}, { decorations: v => v.decorations });

this.registerEditorExtension(myPlugin);
```

## Resources

- [Official Docs](https://docs.obsidian.md/Home)
- [Sample Plugin](https://github.com/obsidianmd/obsidian-sample-plugin)
- [Sample Theme](https://github.com/obsidianmd/obsidian-sample-theme)
- [CodeMirror 6 Docs](https://codemirror.net/docs/)
