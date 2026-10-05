---
name: syncfusion-vue-blockeditor
description: Implement Syncfusion Vue BlockEditor component for block-based content editing with rich text, images, tables, and interactive blocks. Use this skill ALWAYS when user needs block editor, notion-style editor, content blocks, rich text blocks, document editor with blocks, modular content editor, or mentions @syncfusion/ej2-vue-blockeditor, BlockEditor, block-based editing, content management editor, collaborative editing, real-time collaboration. Covers all 14 block types, 5 content types, drag-and-drop, menus, methods, events, real-time collaborative editing with Yjs support, user presence and remote cursors, version history, and Composition API patterns.
metadata:
  author: "Syncfusion Inc"
  version: "34.1.29"
---

# Syncfusion Vue BlockEditor Component

The Syncfusion Vue BlockEditor is a powerful block-based content editor that enables users to create, format, and organize content using various block types. This skill guides you through implementing the BlockEditor component with Vue 3 Composition API, covering all 14 block types, menus, methods, events, and advanced features.

## Component Overview

The Vue BlockEditor component provides:

- **14 Block Types:** Paragraph, Heading (1-4), BulletList, NumberedList, Checklist, Code, Image, Table, Quote, Callout, Divider, Collapsible (Paragraph/Heading), Template
- **5 Content Types:** Text, Link, Mention, Label, InlineCode
- **4 Interactive Menus:** Slash Command (`/`), Context Menu (right-click), Block Action Menu, Inline Toolbar
- **Drag & Drop:** Visual block reordering with handles
- **20+ Methods:** Block CRUD, selection, data export (JSON/HTML), formatting
- **14 Events:** Block changes, drag/drop, paste, file upload, focus/blur
- **Advanced Features:** Syntax highlighting, image upload, table editing, undo/redo, keyboard shortcuts

## Documentation and Navigation Guide

### Getting Started & Installation
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Vue 3 + Vite project setup
- Package installation (`@syncfusion/ej2-vue-blockeditor`)
- CSS theme imports (Material, Bootstrap, Fluent, Tailwind)
- Component registration with Composition API (`<script setup>`)
- Basic BlockEditor initialization
- First render example

### Block Types & Structure
📄 **Read:** [references/block-types.md](references/block-types.md)
- All 14 block types with examples
- BlockModel structure (id, blockType, content, properties)
- Block properties configuration
- Custom templates
- Indent and CSS class customization
- Block type selection guide

### Inline Content & Formatting
📄 **Read:** [references/inline-content.md](references/inline-content.md)
- ContentModel structure
- 5 content types (Text, Link, Mention, Label, InlineCode)
- Inline styles (bold, italic, underline, strikethrough, color, background)
- Link properties and URL configuration
- User mentions with `users` array
- Label/tag configuration with trigger characters
- Inline formatting examples

### Typography Blocks
📄 **Read:** [references/typography-blocks.md](references/typography-blocks.md)
- Paragraph blocks with placeholders
- Heading blocks (levels 1-4)
- Heading level selection
- Divider blocks for section separation
- Placeholder customization
- Typography examples

### List Blocks
📄 **Read:** [references/list-blocks.md](references/list-blocks.md)
- BulletList (unordered lists)
- NumberedList (ordered lists)
- Checklist with `isChecked` state
- List placeholder customization
- Interactive checklist examples

### Nested & Collapsible Blocks
📄 **Read:** [references/nested-blocks.md](references/nested-blocks.md)
- Children property for nested structures
- Parent-child relationships (`parentId`)
- CollapsibleHeading (levels 1-4)
- CollapsibleParagraph blocks
- `isExpanded` state configuration
- Quote blocks with multi-line support
- Callout blocks for important information
- Nested block examples

### Special Blocks (Code, Image, Table)
📄 **Read:** [references/special-blocks.md](references/special-blocks.md)
- Code blocks with syntax highlighting
- `codeBlockSettings` (languages, defaultLanguage)
- Image blocks with upload and resize
- `imageBlockSettings` (saveUrl, path, maxFileSize, allowedTypes)
- Table blocks with rows, columns, cells
- Table properties (width, enableHeader, enableRowNumbers)
- Table resizing and multiple row/column selection
- File upload configuration

### Editor Menus & Toolbars
📄 **Read:** [references/editor-menus.md](references/editor-menus.md)
- Slash Command Menu (`/` trigger) - `commandMenuSettings`
- Context Menu (right-click) - `contextMenuSettings`
- Block Action Menu (hover drag handle) - `blockActionMenuSettings`
- Inline Toolbar (text selection) - `inlineToolbarSettings`
- Transform settings for block type conversion
- Font color and background color settings
- Menu customization and events
- Custom menu items

### Methods & Programmatic Control
📄 **Read:** [references/methods-api.md](references/methods-api.md)
- Block management: `addBlock()`, `removeBlock()`, `updateBlock()`, `moveBlock()`
- Selection: `setSelection()`, `getSelectedBlocks()`, `selectBlock()`, `selectAllBlocks()`
- Cursor: `setCursorPosition()`, `focusIn()`, `focusOut()`
- Data export: `getDataAsJson()`, `getDataAsHtml()`, `print()`
- Formatting: `executeToolbarAction()`, `enableToolbarItems()`, `disableToolbarItems()`
- HTML parsing: `parseHtmlToBlocks()`, `renderBlocksFromJson()`
- Method usage with Composition API patterns

### Events & Lifecycle
📄 **Read:** [references/events-lifecycle.md](references/events-lifecycle.md)
- Block change events: `blockChanged`
- Drag & drop: `blockDragStart`, `blockDragging`, `blockDropped`
- Focus events: `focus`, `blur`
- Selection: `selectionChanged`
- Paste: `beforePasteCleanup`, `afterPasteCleanup`
- File upload: `beforeFileUpload`, `fileUploading`, `fileUploadSuccess`, `fileUploadFailed`
- Created event
- Event handler patterns with Composition API

### Features & Configuration
📄 **Read:** [references/features-configuration.md](references/features-configuration.md)
- Drag and drop: `enableDragAndDrop`
- Paste cleanup: `pasteCleanupSettings` (deniedTags, keepFormat, plainText)
- Undo/redo: `undoRedoStack` (default: 30)
- Keyboard shortcuts: `keyConfig` customization
- Read-only mode: `readOnly`
- Persistence: `enablePersistence`
- Custom styling: `cssClass`
- Height/width: `height`, `width`

### Collaborative Editing
📄 **Read:** [references/collaborative-editing.md](references/collaborative-editing.md)
- Real-time collaborative editing with Yjs CRDT framework
- Yjs providers (y-websocket, y-webrtc, y-indexeddb, Hocuspocus, Liveblocks, PartyKit)
- `collaborationSettings` configuration (adapter, provider, enableAwareness, versionHistory)
- User presence and remote cursors with `enableAwareness`
- User identification with `users` array and `currentUserId`
- Version history with snapshots, restore, compare, export/import
- Collaboration-aware undo/redo operations
- Best practices for development and production deployment

### Accessibility & Globalization
📄 **Read:** [references/accessibility-globalization.md](references/accessibility-globalization.md)
- WCAG 2.2 and Section 508 compliance
- WAI-ARIA attributes
- Keyboard navigation shortcuts
- Localization: `locale` property with L10n
- RTL support: `enableRtl`
- Security: `enableHtmlSanitizer` (XSS prevention), `enableHtmlEncode`
- Localization examples (German, Arabic, etc.)

## Quick Start Example

Install the theme package that matches your application. This example uses `Tailwind 3`:

```bash
npm install @syncfusion/ej2-tailwind3-theme
```

```vue
<template>
  <div>
    <ejs-blockeditor 
      ref="blockEditor"
      :blocks="blocks"
      :users="users"
      :enableDragAndDrop="true"
      @blockChanged="onBlockChanged"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { BlockEditorComponent as EjsBlockeditor, ContentType } from '@syncfusion/ej2-vue-blockeditor';

const blockEditor = ref(null);

const blocks = [
  {
    id: 'heading-1',
    blockType: 'Heading',
    properties: { level: 1 },
    content: [
      { contentType: ContentType.Text, content: 'Welcome to BlockEditor' }
    ]
  },
  {
    id: 'intro-para',
    blockType: 'Paragraph',
    content: [
      { contentType: ContentType.Text, content: 'Create content using blocks. Type ' },
      { contentType: ContentType.Text, content: '/', properties: { styles: { bold: true } } },
      { contentType: ContentType.Text, content: ' for commands.' }
    ]
  },
  {
    id: 'checklist-1',
    blockType: 'Checklist',
    properties: { isChecked: false },
    content: [
      { contentType: ContentType.Text, content: 'Complete the tutorial' }
    ]
  }
];

const users = [
  { id: 'user1', user: 'John Doe' },
  { id: 'user2', user: 'Jane Smith' }
];

const onBlockChanged = (args) => {
  console.log('Block changed:', args.changes);
};
</script>

<style>
@import '../node_modules/@syncfusion/ej2-tailwind3-theme/styles/blockeditor/index.css';
</style>
```
