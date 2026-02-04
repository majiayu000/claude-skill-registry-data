---
name: "pillbox pattern"
description: "User interface pattern. When Claude needs to create an editable
text region that contains inline pills or tokens, along with the ability to add
them using a mention menu."
license: Proprietary
---

# Pillbox Pattern

This skill provides guidance for implementing inline structured text editors with "pill" components using Tiptap.

## Overview

The pillbox pattern creates an inline text editor where special tokens (pills/badges) flow naturally within text content, wrapping across lines like regular text while maintaining their distinct visual appearance. Users insert pills by typing "@" which triggers a filterable dropdown menu with keyboard and mouse navigation.

## Implementation Details

### Dependencies

```bash
pnpm add @tiptap/react @tiptap/core @tiptap/pm @tiptap/starter-kit
pnpm add @tiptap/extension-document @tiptap/extension-paragraph @tiptap/extension-text @tiptap/extension-history
pnpm add @tiptap/suggestion
```

### File Structure

```
src/
├── extensions/
│   ├── Pill.ts              # Custom Tiptap node extension for rendering pills
│   └── Mention.ts           # Mention extension for @ trigger and suggestion handling
├── components/
│   ├── PillComponent.tsx    # React component for rendering pills
│   ├── MentionMenu.tsx      # Floating dropdown menu for pill selection
│   └── Editor.tsx           # Main editor wrapper with menu state management
└── pages/                   # Front-end views accessible by routes
```

### Custom Pill Extension

**Location**: `src/extensions/Pill.ts`

Key characteristics:
- `group: 'inline'` - Makes pills flow inline with text
- `inline: true` - Allows pills to appear within paragraphs
- `atom: true` - Makes pills non-editable blocks
- Attributes: `label` (string), `color` (string)
- Uses `ReactNodeViewRenderer` for custom React rendering
- Includes `insertPill` command for programmatic insertion

```typescript
import { Node, mergeAttributes } from '@tiptap/core'
import { ReactNodeViewRenderer } from '@tiptap/react'
import PillComponent from '../components/PillComponent'

export const Pill = Node.create({
  name: 'pill',
  group: 'inline',
  inline: true,
  atom: true,

  addAttributes() {
    return {
      label: { default: null },
      color: { default: 'default' },
    }
  },

  addNodeView() {
    return ReactNodeViewRenderer(PillComponent)
  },

  addCommands() {
    return {
      insertPill:
        (options) =>
        ({ commands }) => {
          return commands.insertContent({
            type: this.name,
            attrs: options,
          })
        },
    }
  },
})
```

### Mention Extension

**Location**: `src/extensions/Mention.ts`

Handles the "@" trigger and suggestion workflow:
- Detects "@" character and activates suggestion plugin
- Manages text range for replacement
- Integrates with Tiptap's suggestion plugin
- Calls `insertPill` command when option selected

```typescript
import { Node } from '@tiptap/core'
import { PluginKey } from '@tiptap/pm/state'
import Suggestion, { SuggestionOptions } from '@tiptap/suggestion'

export const MentionPluginKey = new PluginKey('mention')

export const Mention = Node.create({
  name: 'mention',

  addOptions() {
    return {
      suggestion: {
        char: '@',
        pluginKey: MentionPluginKey,
        command: ({ editor, range, props }) => {
          editor
            .chain()
            .focus()
            .deleteRange(range)
            .insertPill({
              label: props.label,
              color: props.color || 'default',
            })
            .run()
        },
      },
    }
  },

  addProseMirrorPlugins() {
    return [
      Suggestion({
        editor: this.editor,
        ...this.options.suggestion,
      }),
    ]
  },
})
```

### Pill Component

**Location**: `src/components/PillComponent.tsx`

Key features:
- Uses `NodeViewWrapper` with `as="span"` for inline rendering
- `inline-block align-baseline` for proper text flow
- `flex items-center gap-1` for icon + text layout
- Lucide icons selected via hash function for consistency
- Icon size: 12px for compact appearance
- Color variants: default, blue, green, purple, red

```typescript
import { NodeViewWrapper } from '@tiptap/react'
import { Badge } from '@/components/ui/badge'
import { User, Mail, Calendar, /* etc */ } from 'lucide-react'

const PillComponent = ({ node }: any) => {
  const { label, color } = node.attrs

  // Hash-based icon selection
  const getIcon = (label: string) => {
    const hash = label.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0)
    return icons[hash % icons.length]
  }

  return (
    <NodeViewWrapper as="span" className="inline-block align-baseline">
      <Badge className="flex items-center gap-1">
        <Icon size={12} />
        {label}
      </Badge>
    </NodeViewWrapper>
  )
}
```

### Mention Menu Component

**Location**: `src/components/MentionMenu.tsx`

Floating dropdown menu for pill selection:
- Positioned near cursor using absolute positioning
- Displays filtered list of options based on query
- Supports keyboard navigation (arrow keys, Enter, Escape)
- Supports mouse hover and click
- Shows "No results found" when filter yields no matches
- Uses Lucide icons for each option

```typescript
import { User, Mail, Calendar, /* etc */ } from 'lucide-react'

interface MentionOption {
  label: string
  color: 'default' | 'blue' | 'green' | 'purple' | 'red'
  icon: any
}

const MENTION_OPTIONS: MentionOption[] = [
  { label: 'User Name', color: 'blue', icon: User },
  { label: 'Email Address', color: 'blue', icon: Mail },
  // ... more options
]

const MentionMenu = ({ position, selectedIndex, items, onSelect, onKeyDown }) => {
  return (
    <div
      className="absolute z-50 w-64 rounded-md border bg-white dark:bg-zinc-900 shadow-lg"
      style={{ top: position.top, left: position.left }}
    >
      {items.map((option, index) => (
        <button
          key={option.label}
          className={index === selectedIndex ? 'bg-zinc-100' : ''}
          onClick={() => onSelect(option)}
        >
          <Icon size={16} />
          {option.label}
        </button>
      ))}
    </div>
  )
}
```

### Editor Component

**Location**: `src/components/Editor.tsx`

Editor with integrated mention menu:
- Essential extensions: Document, Paragraph, Text, History, Pill, Mention
- No formatting extensions (bold, italic, headings, etc.)
- Content passed as object (not string)
- Manages menu state (visibility, position, selected index, filtered items)
- Handles keyboard events (Arrow keys, Enter, Escape, Space)
- Handles click outside to dismiss menu
- Filters options based on text typed after "@"

Key features:
- **Filtering**: `onUpdate` callback filters options by query text
- **Position tracking**: Uses `editor.view.coordsAtPos()` for menu placement
- **Selection reset**: Resets `selectedIndex` to 0 when filter changes
- **Menu dismissal**: Space or Escape closes menu, click outside closes menu

```typescript
import { useEditor, EditorContent } from '@tiptap/react'
import { Document, Paragraph, Text, History } from '@tiptap/extension-*'
import { Pill } from '../extensions/Pill'
import { Mention } from '../extensions/Mention'
import MentionMenu, { MENTION_OPTIONS } from './MentionMenu'

const Editor = ({ content }: { content?: any }) => {
  const [menuState, setMenuState] = useState({
    open: false,
    position: { top: 0, left: 0 },
    selectedIndex: 0,
    range: null,
    query: '',
    filteredItems: MENTION_OPTIONS,
  })

  const editor = useEditor({
    extensions: [
      Document,
      Paragraph,
      Text,
      History,
      Pill,
      Mention.configure({
        suggestion: {
          items: ({ query }) =>
            MENTION_OPTIONS.filter((opt) =>
              opt.label.toLowerCase().includes(query.toLowerCase())
            ),
          render: () => ({
            onStart: (props) => {
              // Show menu, calculate position, filter items
              const coords = editor.view.coordsAtPos(...)
              setMenuState({ open: true, position: coords, ... })
            },
            onUpdate: (props) => {
              // Update position and filter as user types
              const filtered = MENTION_OPTIONS.filter(...)
              setMenuState({ ...prev, filteredItems: filtered, selectedIndex: 0 })
            },
            onKeyDown: (props) => {
              // Handle arrow keys, Enter, Escape, Space
            },
            onExit: () => setMenuState({ ...prev, open: false }),
          }),
        },
      }),
    ],
    content: content || '',
  })

  return (
    <div>
      <EditorContent editor={editor} />
      {menuState.open && menuState.filteredItems.length > 0 && (
        <MentionMenu
          position={menuState.position}
          selectedIndex={menuState.selectedIndex}
          items={menuState.filteredItems}
          onSelect={handleSelectOption}
          onKeyDown={handleMenuKeyDown}
        />
      )}
    </div>
  )
}
```

### Content Format

Pills are represented in Tiptap's JSON format:

```typescript
const content = {
  type: 'doc',
  content: [
    {
      type: 'paragraph',
      content: [
        { type: 'text', text: 'Regular text with ' },
        {
          type: 'pill',
          attrs: { label: 'inline pills', color: 'blue' }
        },
        { type: 'text', text: ' that wrap naturally.' },
      ]
    }
  ]
}

// Pass as object, NOT stringified
<Editor content={content} />
```

## Mention Menu Interaction Flow

1. **User types "@"** → Mention extension detects trigger character
2. **Menu appears** → Positioned below cursor, shows all available options
3. **User types letters** → Menu filters in real-time (case-insensitive substring match)
4. **Navigation**:
   - **Arrow Up/Down**: Move selection through filtered items
   - **Enter**: Insert selected pill and close menu
   - **Escape**: Close menu without inserting
   - **Space**: Close menu and insert space character (@ remains in text)
   - **Click**: Select item with mouse
   - **Click outside**: Close menu without inserting
5. **Pill inserted** → "@text" is replaced with the selected pill
6. **Menu closes** → Focus returns to editor

## Key Design Decisions

1. **Inline rendering**: Pills use `inline-block` with `align-baseline` to flow with text
2. **Atomic nodes**: Pills are non-editable units that behave as single characters
3. **Icon consistency**: Hash function ensures same label always gets same icon
4. **Minimal extensions**: Only unformatted text to keep editor simple
5. **Color coding**: Visual categorization via background colors
6. **Dark mode**: All colors have dark mode variants
7. **@ trigger pattern**: Standard mention-style autocomplete for discoverability
8. **Real-time filtering**: Immediate feedback as user types query
9. **Keyboard-first**: All actions accessible via keyboard
10. **Selection reset on filter**: Always highlight first result when query changes

## Common Pitfalls

1. ❌ Don't stringify content: `content={JSON.stringify(obj)}`
   ✅ Pass object directly: `content={obj}`

2. ❌ Don't use `display: inline` on NodeViewWrapper
   ✅ Use `as="span"` with `inline-block` class

3. ❌ Don't forget `align-baseline`
   ✅ Ensures proper vertical alignment with text

4. ❌ Don't use random icons on each render
   ✅ Use deterministic hash function for consistency

5. ❌ Don't reference full option list in keyboard handlers
   ✅ Use `menuState.filteredItems` for bounds checking

6. ❌ Don't forget to reset `selectedIndex` when filter changes
   ✅ Set to 0 in `onUpdate` to avoid out-of-bounds selection

7. ❌ Don't show menu when `filteredItems.length === 0`
   ✅ Conditionally render menu based on filtered results

8. ❌ Don't forget to install `@tiptap/suggestion`
   ✅ Required dependency for mention functionality

## Extending the Pattern

To add more functionality:

- **Custom options**: Replace `MENTION_OPTIONS` with dynamic data from API
- **Click handlers**: Add `onClick` to Badge component for pill interactions
- **Tooltips**: Wrap Badge with Tooltip component for additional info
- **Custom attributes**: Add more attrs in extension definition (e.g., `id`, `metadata`)
- **Different trigger**: Change `char: '@'` to use other triggers like `#` or `/`
- **Multi-character triggers**: Use `char: '//'` for slash commands
- **Async filtering**: Fetch filtered results from API in `items` function
- **Fuzzy search**: Replace substring filter with fuzzy matching library
- **Grouped options**: Add category headers in menu for organization

## Example Use Cases

- Template variables (e.g., `{{user.name}}`)
- Mentions (@username)
- Tags and categories
- Dynamic fields in forms
- Variable insertion in email templates
- Entity references in rich text

## Reference Implementation

If a reference implementation exists in the current codebase, you may find these files:
- `src/extensions/Pill.ts` - Custom pill node extension with `insertPill` command
- `src/extensions/Mention.ts` - Mention extension for @ trigger detection
- `src/components/PillComponent.tsx` - Visual pill rendering with icons
- `src/components/MentionMenu.tsx` - Floating dropdown menu with filtering
- `src/components/Editor.tsx` - Editor setup with menu state management
- `src/pages/EditorPage.tsx` - Demo page with usage instructions

**Note**: These files may not exist in every repository. Use the code examples in this document as patterns to implement from scratch.

## Quick Start

1. Install dependencies:
```bash
pnpm add @tiptap/react @tiptap/core @tiptap/pm @tiptap/starter-kit
pnpm add @tiptap/extension-document @tiptap/extension-paragraph @tiptap/extension-text @tiptap/extension-history
pnpm add @tiptap/suggestion
```

2. Create the four core files following the patterns shown above:
   - `src/extensions/Pill.ts` - Use the Pill Extension code example
   - `src/extensions/Mention.ts` - Use the Mention Extension code example
   - `src/components/PillComponent.tsx` - Use the Pill Component code example
   - `src/components/MentionMenu.tsx` - Use the Mention Menu Component code example
   - `src/components/Editor.tsx` - Use the Editor Component code example

3. Import and use the Editor component:
```tsx
import Editor from '@/components/Editor'

function MyPage() {
  return <Editor content={initialContent} />
}
```

4. Type "@" in the editor to trigger the mention menu
5. Type letters to filter options or use arrow keys to navigate
6. Press Enter or click to insert a pill
