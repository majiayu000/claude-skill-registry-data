---
name: galaxy-ui
description: Browse and retrieve UI components from Uiverse Galaxy — 3,800+ HTML/CSS components including buttons, cards, inputs, loaders, checkboxes, toggles, tooltips, notifications, forms, radio buttons, and patterns. Use when the user mentions UI, buttons, cards, loaders, checkboxes, toggles, forms, tooltips, UI component, UI design, 组件, 按钮, 卡片, 加载动画, 表单.
---

## Galaxy UI Components

3,800+ open-source UI components from [Uiverse.io](https://uiverse.io/), ready to drop into any project. All MIT licensed.

### Component Categories

| Category | Path | Count |
|----------|------|-------|
| Buttons | `Buttons/` | 1,231 |
| Cards | `Cards/` | 726 |
| Loaders | `loaders/` | 718 |
| Inputs | `Inputs/` | 226 |
| Notifications | `Notifications/` | 23 |
| Toggle switches | `Toggle-switches/` | 260 |
| Forms | `Forms/` | 180 |
| Checkboxes | `Checkboxes/` | 171 |
| Patterns | `Patterns/` | 103 |
| Radio buttons | `Radio-buttons/` | 102 |
| Tooltips | `Tooltips/` | 62 |

### How to Find Components

1. **User specifies type** — match to a category above (e.g., "button" → `Buttons/`, "card" → `Cards/`)
2. **Search by keywords** — use Grep to search component filenames or content for style descriptors (e.g., `neumorphic`, `gradient`, `animated`, `minimal`, `dark`)
3. **Read the component** — use Read on the HTML file. Each file is self-contained with HTML + inline CSS
4. **Copy and adapt** — return the full HTML + CSS block to the user, ready to paste into their project

### Search Strategy

```bash
# Find components by filename pattern
find ~/.claude/skills/galaxy-ui/Buttons -name "*.html" | head -10

# Search by style keyword in filenames
find ~/.claude/skills/galaxy-ui/Buttons -name "*gradient*" -o -name "*glow*" -o -name "*minimal*" | head -10

# Search inside files for specific CSS properties
grep -l "backdrop-filter" ~/.claude/skills/galaxy-ui/Buttons/*.html | head -10
grep -l "border-radius: 50px" ~/.claude/skills/galaxy-ui/Cards/*.html | head -10
```

### Response Format

When returning a component to the user:

1. Show the filename: `From Uiverse.io by {author}`
2. Provide the full HTML + CSS block in a code fence
3. Briefly describe what it looks like and how it behaves
4. If the user wants alternatives, show 2-3 more options

### Attribution

Components are MIT licensed. When using one, add a comment:
```html
<!-- From Uiverse.io by {author} - https://uiverse.io -->
```
