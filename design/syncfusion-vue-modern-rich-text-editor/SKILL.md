---
name: syncfusion-vue-modern-rich-text-editor
description: Implement Syncfusion Vue Modern Rich Text Editor component for creating, editing, and formatting rich text content with inline formatting, block formats, tables, images, links, lists, slash commands, and keyboard shortcuts. Use this skill ALWAYS when user needs rich text editor, WYSIWYG editor, modern RTE, content editor, text formatting, document editor, rich content editing, mentions @syncfusion/ej2-vue-richtexteditor-ui, RichTextEditorUI, RichTextEditorUIComponent. Covers all formatting options, toolbar configuration, quick toolbars, events, methods, keyboard shortcuts, image handling, table operations, list formatting, and slash command features.
metadata:
  author: "Syncfusion Inc"
  version: "34.1.29"
---

# Syncfusion Vue Modern Rich Text Editor Component

The Syncfusion Vue Modern Rich Text Editor is a powerful WYSIWYG (What You See Is What You Get) component that enables users to create, edit, and format rich text content with extensive support for inline formatting, block-level elements, media insertion, and interactive features. This skill guides you through implementing the Modern RTE component with Vue 3 Composition API, covering all formatting options, toolbar configurations, menus, methods, events, and advanced features.

## Component Overview

The Vue Modern Rich Text Editor component provides:

- **Text Formatting:** Bold, Italic, Underline, Strikethrough, Subscript, Superscript, Inline Code, Clear Format
- **Block Elements:** Paragraph, Headings (1-4), Block Quote, Callout (Info/Warning/Error/Success/Note), Code Block, Collapsible sections
- **Lists:** Bullet lists, Numbered lists, Checklists with keyboard shortcuts for quick insertion
- **Toolbar System:** Main toolbar with full customization, Quick toolbars for text/image/link/table contexts, custom toolbar items
- **Media & Tables:** Image insertion with upload/resize, Table creation with rows/columns/headers/cell formatting
- **Link Management:** Link insertion, editing, quick access with Open/Copy/Edit/Remove actions
- **Slash Commands:** `/` trigger for quick block and command insertion with customizable items
- **Keyboard Shortcuts:** Built-in cross-platform shortcuts (Windows/Linux/macOS) with custom configuration
- **Events:** 14+ events covering change, focus, blur, actionBegin, actionComplete, toolbar updates, and more
- **Methods:** Programmatic control via save, focusIn, focusOut, getHtml, getText, getDocument, updateToolbarItems
- **Advanced Features:** Paste cleanup, undo/redo, read-only mode, persistent state, theme customization

## Documentation and Navigation Guide

### Getting Started & Installation
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Node.js 24+ prerequisites
- Syncfusion CLI installation and project setup (interactive & non-interactive modes)
- Manual Vue + Vite project creation
- Package installation (`@syncfusion/ej2-vue-richtexteditor-ui`)
- CSS theme imports with Tailwind 3
- Component registration and basic initialization
- Running the application

### Basic Setup & Configuration
📄 **Read:** [references/getting-started.md](references/getting-started.md) (Configuration section)
- Setting editor content with `value` property
- Content format selection (`valueFormat`: HTML vs JSON)
- Toolbar configuration basics
- Image settings and validation
- Placeholder text configuration
- Auto-save behavior with `saveInterval`

### Toolbar Configuration
📄 **Read:** [references/toolbar.md](references/toolbar.md)
- Toolbar items and types
- Available toolbar items (History, Text formatting, Font/Color, Structure, Alignment, Lists, Insert)
- Toolbar layout configuration (Type: Expanded/Scrollable/MultiRow, Position: Top/Bottom)
- Floating toolbar behavior and offset configuration
- Main toolbar events (itemClicked, updatedToolbarStatus)
- Custom toolbar items with actionId routing
- Updating toolbar items at runtime
- Quick toolbars for text, image, link, and table contexts
- Quick toolbar enable/append options

### Inline Text Formatting
📄 **Read:** [references/formatting.md](references/formatting.md)
- Supported inline formats (Bold, Italic, Underline, Strikethrough, Subscript, Superscript, Inline Code, Clear Format)
- Keyboard shortcuts for each format (with Windows/macOS variants)
- Color configuration (Font Color, Background Color)
- Formatting commands and configuration options
- Text case transformation (Uppercase, Lowercase)
- Inline styling examples

### Block-Level Formatting
📄 **Read:** [references/formatting.md](references/formatting.md) (Block Formats section)
- Paragraph formatting
- Heading levels (1-4)
- Indentation (Indent, Outdent)
- Horizontal line insertion
- Keyboard shortcuts for block operations

### Block Quote
📄 **Read:** [references/block-quote.md](references/block-quote.md)
- Block quote creation and formatting
- Quick toolbar access
- Slash command trigger (`/blockquote`)
- Keyboard shortcut access
- Nested quote examples
- Quote styling and customization

### Callout Blocks
📄 **Read:** [references/callout.md](references/callout.md)
- Callout types (Info, Warning, Error, Success, Note)
- Callout creation via toolbar, slash commands, and keyboard shortcuts
- Callout styling and color coding
- Nested content within callouts
- Quick toolbar customization for callouts

### Code Blocks
📄 **Read:** [references/codeblock.md](references/codeblock.md)
- Code block creation and insertion
- Syntax highlighting support
- Language selection for code blocks
- Keyboard shortcut (Ctrl+Shift+B / Cmd+Shift+B)
- Code block styling and formatting
- Copy/paste handling within code blocks

### Collapsible Sections
📄 **Read:** [references/collapsible.md](references/collapsible.md)
- Collapsible paragraph and heading blocks
- Heading levels for collapsible sections (1-4)
- Expand/collapse state management
- Nested content within collapsible sections
- Slash command triggers for collapsible items
- Keyboard navigation for collapsible elements

### Image Handling
📄 **Read:** [references/image.md](references/image.md)
- Image configuration options (allowedTypes, maxFileSize, uploadUrl, removeUrl, imageUrl)
- Image insertion methods (toolbar, slash commands, keyboard shortcut)
- Insert image dialog and options
- Image quick toolbar (AltText, Caption, Align, Display, WrapText, Dimension, Replace, Remove)
- Alt text and caption management
- Image alignment and wrapping options
- Image resizing and dimension configuration
- Remote upload configuration and server setup
- Image upload events and error handling

### Link Management
📄 **Read:** [references/links.md](references/links.md)
- Link insertion dialog and settings
- Link properties (URL, Display text, Target, Rel attribute)
- Edit and remove link actions
- Link quick toolbar items (Open, Copy, Edit, Remove)
- Keyboard shortcut for link insertion (Ctrl+K / Cmd+K)
- Link settings configuration
- Open link behavior and target attributes

### Table Operations
📄 **Read:** [references/table.md](references/table.md)
- Table insertion via toolbar and slash commands
- Table popup grid selector (3×10)
- Detailed table dialog (rows 1-100, columns 1-50)
- Row operations (Insert Before, Insert After, Delete)
- Column operations (Insert Left, Insert Right, Delete)
- Header row toggle and configuration
- Cell formatting (Background color, Horizontal alignment, Vertical alignment)
- Table quick toolbar items and operations
- Table properties and settings (resize, header management)
- Keyboard shortcut (Ctrl+Shift+E / Cmd+Shift+E)

### List Formatting
📄 **Read:** [references/lists.md](references/lists.md)
- Bullet list creation and formatting
- Bullet format options (disc, circle, square, etc.)
- Numbered list creation and formatting
- Number format options (1, i, a, I, A, etc.)
- Checklist creation with checkable items
- List nesting and indentation
- List keyboard shortcuts (Ctrl+Shift+O for ordered, Ctrl+Alt+O for unordered, Ctrl+Shift+7 for checklist)
- List formatting configuration
- List item properties and styling

### Slash Commands / Features
📄 **Read:** [references/features.md](references/features.md)
- Enabling slash commands (`slashCommandSettings.enable`)
- Module injection for slash command support
- Available built-in slash command items
- Custom slash command items configuration
- Slash command filtering as user types
- Popup width and height customization
- Item grouping (Basic Block, Inline, Media)
- itemSelect event handling for custom commands
- Selection and lifecycle behavior

### Editor Events
📄 **Read:** [references/editor-events.md](references/editor-events.md)
- `change` event — fires on content modifications
- `created` event — fires after component initialization
- `destroyed` event — fires when component is disposed
- `focus` event — fires when editor receives focus
- `blur` event — fires when editor loses focus
- `actionBegin` event — fires before editor actions
- `actionComplete` event — fires after editor actions
- Event args structure and properties
- Event handling patterns with Composition API

### Editor Methods & Programmatic Control
📄 **Read:** [references/editor-methods.md](references/editor-methods.md)
- `save()` — persists current editor content
- `focusIn()` — moves focus into editor
- `focusOut()` — removes focus from editor
- `getDocument()` — returns current editor document
- `getHtml()` — returns editor content as HTML string
- `getText()` — returns editor content as plain text
- `updateToolbarItems(updates)` — batch update toolbar items
- Method access via component ref
- Programmatic control patterns

### Keyboard Shortcuts

Keyboard shortcuts are integrated into their corresponding feature documentation files for better organization and discovery:

**Comprehensive Quick Reference** — [references/formatting.md](references/formatting.md) → Quick Reference Card section
- Print-friendly summary of all formatting, list, insert, and history shortcuts

📄 **Text Formatting Shortcuts** — [references/formatting.md](references/formatting.md) → Keyboard Shortcuts section
- Bold, Italic, Underline, Strikethrough, Subscript, Superscript, Inline Code, Clear Format
- Text case transformation (Uppercase, Lowercase)
- Quick reference card for printing

📄 **List Shortcuts** — [references/lists.md](references/lists.md) → Keyboard Shortcuts section
- Ordered List, Unordered List, Checklist
- Indent, Outdent with indentation notes

📄 **Insertion Shortcuts**
- Link: [references/links.md](references/links.md) → <kbd>Ctrl</kbd>+<kbd>K</kbd> / <kbd>⌘</kbd>+<kbd>K</kbd>
- Image: [references/image.md](references/image.md) → <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>I</kbd> / <kbd>⌘</kbd>+<kbd>Shift</kbd>+<kbd>I</kbd>
- Table: [references/table.md](references/table.md) → <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>E</kbd> / <kbd>⌘</kbd>+<kbd>Shift</kbd>+<kbd>E</kbd>
- Code Block: [references/codeblock.md](references/codeblock.md) → <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>B</kbd> / <kbd>⌘</kbd>+<kbd>Shift</kbd>+<kbd>B</kbd>

📄 **History & Customization** — [references/editor-methods.md](references/editor-methods.md) → Keyboard Shortcuts & Customizing sections
- Undo: <kbd>Ctrl</kbd>+<kbd>Z</kbd> / <kbd>⌘</kbd>+<kbd>Z</kbd>
- Redo: <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>Z</kbd> / <kbd>⌘</kbd>+<kbd>Shift</kbd>+<kbd>Z</kbd>
- Comprehensive keyboard customization guide with syntax rules, available keys, and accessibility considerations
- Override default shortcuts with `keyBindings` property
- List of all customizable command names

📄 **Toolbar Navigation** — [references/toolbar.md](references/toolbar.md) → Keyboard Shortcuts section
- Toolbar Focus: <kbd>Alt</kbd>+<kbd>F10</kbd> / <kbd>Option</kbd>+<kbd>F10</kbd>
- Escape: Close dialogs and return focus

### API References & Interfaces

API references have been integrated into their corresponding feature documentation files for better organization and discovery:

📄 **Toolbar APIs** — [references/toolbar.md](references/toolbar.md) → API References section
- ToolbarSettings, ToolbarType, ToolbarPosition configuration
- Complete official documentation links

📄 **Formatting & Text Alignment APIs** — [references/formatting.md](references/formatting.md) → API References section
- TextAlignment enum, AlignmentCommandBuilder, ColorPickerType, ColorModeType
- Complete official documentation links

📄 **Table Configuration APIs** — [references/table.md](references/table.md) → API References section
- TableSettings and TableQuickToolbarItem configuration
- Complete official documentation links

📄 **Callout Block APIs** — [references/callout.md](references/callout.md) → API References section
- CalloutCommandBuilder for programmatic callout insertion
- Complete official documentation links

📄 **File Upload Events APIs** — [references/file-upload.md](references/file-upload.md)
- Complete file upload event lifecycle (FileSelectedEventArgs, FileUploadingEventArgs, FileUploadSuccessEventArgs, FileUploadFailedEventArgs, FileRemovingEventArgs)
- Event handling patterns and validation examples
- Complete official documentation links

📄 **Other Feature Documentation**
- [references/lists.md](references/lists.md) — List configuration and ChecklistCommandBuilder API
- [references/links.md](references/links.md) — Link management and configuration
- [references/image.md](references/image.md) — Image settings and display modes
- [references/block-quote.md](references/block-quote.md) — Block quote configuration
- [references/codeblock.md](references/codeblock.md) — Code block and CodeBlockCommandBuilder API
- [references/collapsible.md](references/collapsible.md) — Collapsible sections and CollapsibleCommandBuilder API
- [references/editor-methods.md](references/editor-methods.md) — Programmatic methods and command execution
- [references/editor-events.md](references/editor-events.md) — Component events and event arguments
- [references/features.md](references/features.md) — Feature overview and capabilities

---

## Quick Start Example

The following example demonstrates how to create a basic Modern Rich Text Editor with default configuration in Vue 3 Composition API:

```vue
<template>
  <div>
    <ejs-richtexteditor-ui 
      ref="editor"
      placeholder="Type something..."
      :value="editorValue"
      :valueFormat="valueFormat"
      :toolbarSettings="toolbarSettings"
      :imageSettings="imageSettings"
      @change="onChange"
    ></ejs-richtexteditor-ui>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { RichTextEditorUIComponent as EjsRichtexteditorUi } from '@syncfusion/ej2-vue-richtexteditor-ui';

const editor = ref(null);
const editorValue = ref('<p>Welcome to the Modern Rich Text Editor!</p>');
const valueFormat = ref('html');

const toolbarSettings = ref({
  items: [
    'Bold', 'Italic', 'Underline', '|',
    'Formats', 'Alignment', '|',
    'BulletList', 'NumberedList', '|',
    'Link', 'Image', 'Table', '|',
    'Undo', 'Redo'
  ]
});

const imageSettings = ref({
  allowedTypes: ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'],
  maxFileSize: 30000000,
  uploadUrl: 'https://services.syncfusion.com/js/production/api/RichTextEditor/SaveFile',
  imageUrl: 'https://services.syncfusion.com/js/production/RichTextEditor/'
});

const onChange = (args) => {
  console.log('Editor content changed:', args);
};
</script>

<style>
@import "../../node_modules/@syncfusion/ej2-tailwind3-theme/styles/richtexteditor-ui/index.css";
</style>
```

---

## Key Concepts

### ValueFormat
The `valueFormat` property determines how content is stored and exchanged:
- **'html'** — Use when working with HTML strings
- **'json'** — Use for structured document model (default)

### Toolbar Configuration
The `toolbarSettings` property controls the main toolbar:
- **items** — Array of toolbar item identifiers and separators
- **type** — Layout mode (Auto, Expanded, Scrollable, MultiRow)
- **position** — Toolbar placement (Top, Bottom)
- **enableFloating** — Sticky toolbar while scrolling
- **itemClicked** — Event handler for toolbar interactions

### Quick Toolbars
The `quickToolbarSettings` property controls context-sensitive toolbars:
- **text** — Items shown when text is selected
- **image** — Items shown when image is selected
- **link** — Items shown when cursor is in a link
- **table** — Items shown when cursor is in a table

### Module Injection
Some features require module injection via `provide`:
- **SlashCommand** — For slash command support
- **Image** — For image handling
- **Table** — For table support

---

## Related Documentation

For API reference and detailed type information, refer to the official Syncfusion documentation:
- [Rich Text Editor UI Component API](https://ej2.syncfusion.com/vue/documentation/richtexteditor-ui/getting-started/)
- [ToolbarSettings API](https://ej2.syncfusion.com/documentation/api/richtexteditor-ui/toolbarSettings)
- [QuickToolbarSettings API](https://ej2.syncfusion.com/documentation/api/richtexteditor-ui/quickToolbarSettings)
- [ImageSettings API](https://ej2.syncfusion.com/documentation/api/richtexteditor-ui/imageSettings)
- [TableSettings API](https://ej2.syncfusion.com/documentation/api/richtexteditor-ui/tableSettings)

---

## Next Steps

1. ✅ **Start with Getting Started** — Set up your Vue project and install the component
2. ✅ **Configure Toolbar** — Customize toolbar items and layout
3. ✅ **Add Content Formatting** — Enable inline and block formatting
4. ✅ **Implement Media** — Add image and table support
5. ✅ **Handle Events** — Connect editor events to your application logic
6. ✅ **Use Keyboard Shortcuts** — Leverage built-in and custom shortcuts
7. ✅ **Explore Advanced Features** — Implement slash commands, custom toolbars, and programmatic control

