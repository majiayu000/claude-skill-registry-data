---
name: syncfusion-vue-rich-text-editor
description: "Implements the Syncfusion Vue Rich Text Editor (ejs-richtexteditor) supporting both HTML (WYSIWYG) and Markdown editing modes via the editorMode API from @syncfusion/ej2-vue-richtexteditor. Use this skill for toolbar customization, image upload, paste cleanup, inline editing, AI assistant integration, slash menu, emoji picker, and mention support in Vue applications."
metadata:
  author: "Syncfusion Inc"
  version: "34.1.29"
  category: "File Viewers & Editors"
---

# Implementing the Syncfusion Vue Rich Text Editor

The Syncfusion Vue Rich Text Editor (`ejs-richtexteditor`) is a single, unified editor component that supports two primary modes:
- **HTML mode** (default) — WYSIWYG editor that returns valid HTML markup
- **Markdown mode** — plain-text editing with Markdown syntax, rendered via a third-party library like `marked`

Both modes share the same Vue component and `@syncfusion/ej2-vue-richtexteditor` package. The `editorMode` prop and the injected service module (`HtmlEditor` vs `MarkdownEditor`) are what differentiate them.

## When to Use This Skill

- User wants to add a **rich text / WYSIWYG editor** to a Vue app
- User wants a **Markdown editor** with preview support
- User needs to **customize the toolbar** (types, items, sticky, floating)
- User wants to **insert images, audio, video, tables, or links**
- User needs **paste-from-Word cleanup**, inline editing, or IFrame mode
- User wants to integrate **AI Assistant**, slash menu, emoji picker, or @mentions
- User needs **form validation**, read-only mode, or XHTML validation
- User needs to **get/set editor value** or work with events and selection API

## Mode Selection Guide

| Goal | Mode | Inject |
|------|------|--------|
| WYSIWYG HTML output | `editorMode="HTML"` (default) | `HtmlEditor` |
| Markdown text with `#`, `**bold**` syntax | `editorMode="Markdown"` | `MarkdownEditor` |
| IFrame-isolated editing | HTML mode + IFrame config | `HtmlEditor`, `HtmlEditor` render mode |
| Live markdown preview split-pane | Markdown mode + `marked` library | `MarkdownEditor` |

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Package installation (`@syncfusion/ej2-vue-richtexteditor`)
- CSS imports and theme setup
- Module injection reference table (all available services)
- Minimal HTML editor setup (Composition API + Options API)
- Minimal Markdown editor setup
- Running the application

### Editor Modes (HTML vs Markdown)
📄 **Read:** [references/editor-modes.md](references/editor-modes.md)
- HTML mode — default WYSIWYG, returns HTML markup
- Markdown mode — `editorMode="Markdown"`, returns Markdown text
- Supported Markdown tags and selection formatting
- Converting Markdown to HTML with `marked` library
- Live markdown preview implementation
- Side-by-side split-pane preview with Splitter component

### Toolbar Configuration
📄 **Read:** [references/toolbar-configuration.md](references/toolbar-configuration.md)
- Toolbar types: Expand, MultiRow, Scrollable, Popup
- Sticky/floating toolbar (`enableFloating`, `floatingToolbarOffset`)
- Toolbar position (top/bottom) and `toolbarSettings`
- Enabling/disabling toolbar items programmatically
- Custom toolbar button templates

### Toolbar Tools Reference
📄 **Read:** [references/toolbar-tools.md](references/toolbar-tools.md)
- All built-in toolbar items by category (text formatting, font, alignment, lists, links, images, tables, undo/redo, misc)
- Markdown-specific toolbar items
- Removing or reordering built-in tools
- `toolbarSettings.items` array configuration

### Quick Toolbars
📄 **Read:** [references/quick-toolbars.md](references/quick-toolbars.md)
- Context-aware toolbars for images, links, tables, audio, video
- Customizing `quickToolbarSettings` per element type
- Default quick toolbar items and overrides
- Enabling/disabling quick toolbars

### Inserting Images
📄 **Read:** [references/insert-images.md](references/insert-images.md)
- Image insertion via toolbar (URL and file upload)
- Server-side upload with `insertImageSettings`
- Drag-and-drop image support
- Image resize, alignment, caption, alt text
- Renaming images on server, checking image size limits
- `Image` module injection

### Inserting Media (Audio & Video)
📄 **Read:** [references/insert-media.md](references/insert-media.md)
- Audio insertion with `Audio` module
- Video insertion with `Video` module
- File browser integration
- Media quick toolbar options

### Inserting Tables
📄 **Read:** [references/insert-table.md](references/insert-table.md)
- Table insertion in HTML mode and Markdown mode
- Default table structure (2×2 with header row)
- Table quick toolbar (rows, columns, merge, properties)
- Table `Table` module injection

### Editor Value & Content
📄 **Read:** [references/editor-value.md](references/editor-value.md)
- Setting initial value via `:value` prop
- Getting editor value via `getValue()` method
- Two-way binding with `v-model`
- Placeholder text (`placeholder` prop)
- Character count and `maxLength`
- `change`, `input`, `blur` events
- `execCommand` API for programmatic formatting
- Selection API and cursor positioning

### Smart Editing Features
📄 **Read:** [references/smart-editing.md](references/smart-editing.md)
- Slash menu (`/` command palette) with `slashMenuSettings`
- Emoji picker toolbar integration
- Mention support (`@mention`) with `MentionModule`
- Mail merge fields

### Paste Cleanup
📄 **Read:** [references/paste-cleanup.md](references/paste-cleanup.md)
- Pasting content from Word/browser with formatting control
- `pasteCleanupSettings`: prompt, plainText, keepFormat
- Stripping denied tags/attributes (`deniedTags`, `deniedAttrs`)
- `PasteCleanup` module injection
- Clipboard event handling

### Editor Types (Inline, IFrame, Resizable)
📄 **Read:** [references/editor-types.md](references/editor-types.md)
- Inline editing mode (content-editable in-place editing)
- IFrame mode (style isolation from page)
- Resizable editor (`enableResize`, resize handles)
- When to choose each render type

### AI Assistant
📄 **Read:** [references/ai-assistant.md](references/ai-assistant.md)
- `AIAssistantService` provider injection
- `AICommands` and `AIQuery` toolbar items
- AI pop-up with predefined prompt dropdown
- Customizing AI assistant behavior and properties

### Validation & Security
📄 **Read:** [references/validation-security.md](references/validation-security.md)
- Form integration and submit-on-form
- XHTML validation mode
- Read-only mode (`readonly` prop)
- Max length validation
- Spell and grammar check integration

### Accessibility & Globalization
📄 **Read:** [references/accessibility-globalization.md](references/accessibility-globalization.md)
- WCAG 2.2 and Section 508 compliance
- Keyboard navigation and shortcuts
- RTL (right-to-left) support
- Globalization and locale configuration
- Custom keyboard shortcut overrides

### API Reference - Events
📄 **Read:** [references/vue-events.md](references/events.md)
- Lifecycle events (created, destroyed)
- Editor action events (actionBegin, actionComplete, toolbarClick)
- Content change events (change, selectionChanged, focus, blur)
- Dialog events (beforeDialogOpen, dialogOpen, dialogClose)
- File upload events (image, audio, video uploads)
- Toolbar and popup events
- AI Assistant events
- Advanced events (paste, resize, export, import)

### API Reference - Methods
📄 **Read:** [references/vue-methods.md](references/methods.md)
- Content access methods (getHtml, getText, getXhtml, getContent, getCharCount)
- Selection and range methods (getSelection, getRange, selectAll, selectRange)
- Command execution (executeCommand with all available commands)
- Toolbar management (enable, disable, remove toolbar items)
- Dialog methods (showDialog, closeDialog)
- Focus and state methods (focusIn, focusOut, refreshUI, destroy)
- AI Assistant methods (show/hide popup, execute prompt, manage history)
- Utility methods (sanitizeHtml, print, fullscreen, source code, emoji picker)

### API Reference - Properties (Core)
📄 **Read:** [references/properties-core.md](references/properties-core.md)
- Core configuration (value, valueTemplate, placeholder, enabled, readonly, cssClass, htmlAttributes)
- Dimensions and layout (width, height, enableResize)
- Editor modes and behavior (editorMode, enterKey, shiftEnterKey, enableTabKey, enableAutoUrl, enableMarkdownAutoFormat)
- Toolbar configuration (toolbarSettings with enable, enableFloating, position, type, items, itemConfigs)
- Toolbar customization (floatingToolbarOffset, showTooltip)
- Quick toolbar settings (for images, links, tables, audio, video with actionOnScroll, enableAppendToBody)
- Font and text formatting (fontFamily, fontSize, fontColor, backgroundColor, format, lineHeight, formatPainterSettings)
- List formatting (bulletFormatList, numberFormatList)
- Media insertion settings (insertImageSettings, insertAudioSettings, insertVideoSettings, fileManagerSettings)
- Table settings (tableSettings with width, resize, styles)
- Paste and clipboard (pasteCleanupSettings with prompt, keepFormat, deniedAttrs/Tags, allowedStyleProps; enableClipboardCleanup)

### API Reference - Properties (Advanced)
📄 **Read:** [references/properties-advanced.md](references/properties-advanced.md)
- AI Assistant settings (aiAssistantSettings with commands, prompts, suggestions, popup dimensions, toolbar settings, bannerTemplate)
- Advanced features (slashMenuSettings, emojiPickerSettings, codeBlockSettings, formatter, keyConfig for custom shortcuts)
- Validation and limits (maxLength, showCharCount, enableHtmlSanitizer, enableHtmlEncode, enableXhtml)
- Localization and accessibility (locale with L10n translations, enableRtl for right-to-left languages)
- IFrame mode (iframeSettings with enable, attributes, resources, metaTags, sandbox)
- Inline mode (inlineMode with enable, onSelection for toolbar display)
- Import and export (importWord, exportWord with serviceUrl/fileName/stylesheet, exportPdf with serviceUrl/fileName/stylesheet)
- Persistence and auto-save (enablePersistence with localStorage, autoSaveOnIdle, saveInterval in milliseconds)
- Undo/redo (undoRedoSteps for history limit, undoRedoTimer for debounce delay)

## Quick Start

```bash
npm install @syncfusion/ej2-vue-richtexteditor
```

```bash
npm install @syncfusion/ej2-tailwind3-theme
```

### HTML Editor (Composition API)

```vue
<template>
  <ejs-richtexteditor :value="value" :toolbarSettings="toolbarSettings" />
</template>

<script setup>
import { provide } from 'vue';
import {
  RichTextEditorComponent as EjsRichtexteditor,
  Toolbar, Link, Image, HtmlEditor, QuickToolbar
} from '@syncfusion/ej2-vue-richtexteditor';

const value = '<p>Start editing here...</p>';
const toolbarSettings = {
  items: ['Bold', 'Italic', 'Underline', '|', 'Formats', 'Alignments',
    'OrderedList', 'UnorderedList', '|', 'CreateLink', 'Image', '|', 'Undo', 'Redo']
};
provide('richtexteditor', [Toolbar, Link, Image, HtmlEditor, QuickToolbar]);
</script>

<style>
@import '../node_modules/@syncfusion/ej2-tailwind3-theme/styles/rich-text-editor/index.css';
</style>
```

### Markdown Editor (Composition API)

```vue
<template>
  <ejs-richtexteditor
    editorMode="Markdown"
    :value="value"
    :toolbarSettings="toolbarSettings"
  />
</template>

<script setup>
import { provide } from 'vue';
import {
  RichTextEditorComponent as EjsRichtexteditor,
  Toolbar, Link, Image, MarkdownEditor
} from '@syncfusion/ej2-vue-richtexteditor';

const value = '**Hello** from Markdown editor!';
const toolbarSettings = {
  items: ['Bold', 'Italic', 'StrikeThrough', '|',
    'Formats', 'OrderedList', 'UnorderedList', '|',
    'CreateLink', 'Image', '|', 'Undo', 'Redo']
};
provide('richtexteditor', [Toolbar, Link, Image, MarkdownEditor]);
</script>
```

## Key Module Injection Reference

| Feature | Module to Inject |
|---------|-----------------|
| HTML editing (default) | `HtmlEditor` |
| Markdown editing | `MarkdownEditor` |
| Toolbar | `Toolbar` |
| Hyperlinks | `Link` |
| Images | `Image` |
| Audio | `Audio` |
| Video | `Video` |
| Tables | `Table` |
| Quick toolbars | `QuickToolbar` |
| Paste cleanup | `PasteCleanup` |
| Slash menu | `SlashMenu` |
| AI Assistant | `AIAssistantService` |
| Character count | `Count` |

Always inject modules in `provide('richtexteditor', [...modules])`.

## Common Patterns

### Controlled value with v-model
```vue
<ejs-richtexteditor v-model:value="content" />
```

### Getting value programmatically
```vue
<ejs-richtexteditor ref="rteRef" />
<!-- In script: -->
const html = rteRef.value.ej2Instances.getHTML();
const text = rteRef.value.ej2Instances.getText();
```

### Markdown editor + live HTML preview
Use `editorMode="Markdown"` with a `change` event handler that passes the content through `marked.parse()` into a preview `<div>`. See `references/editor-modes.md` for the full split-pane implementation.

### Decide: HTML mode or Markdown mode?
- Need **formatted output to store as HTML** → use HTML mode
- Need **lightweight text with syntax** users can read/edit as plain text → use Markdown mode
- Need **rich media** (images, video, audio, tables with formatting) → use HTML mode
- Need **developer-friendly source** that renders in GitHub/Notion → use Markdown mode
