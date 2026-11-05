---
name: scaffold-tui
description: Generate TUI screen/view with layout, keybindings, state management, and tests
type: scaffold
project_types: [tui]
trigger: "create screen, create view, add TUI screen, add TUI view"
inputs:
  - name: name
    description: Screen/view name (e.g. dashboard, list, detail, form)
    required: true
  - name: type
    description: View type (list, detail, form, dashboard, modal)
    required: false
    default: "list"
  - name: keybindings
    description: Custom keybindings for this view (e.g. "enter=select, d=delete, /=search")
    required: false
    default: ""
---

## Context

Project {{project_name}} is a TUI application using {{stack}}.
You will create a new screen/view "{{input.name}}" of type {{input.type}}.

Read AGENTS.md for conventions. Read existing views to understand patterns.

## Instructions

1. **Analyze existing view patterns**
   - Read existing view/screen files
   - Identify: TUI framework (bubbletea, ratatui/tui-rs, textual, blessed, ink, etc.)
   - Identify: component model (Model-View-Update, widgets, components)
   - Identify: styling approach (lipgloss, style objects, CSS-like)
   - Identify: navigation pattern (stack, tabs, router)
   - Note state management patterns

2. **Create view/model file**
   - Path: according to project convention
     - Go (bubbletea): `internal/ui/{{input.name}}.go` or `ui/{{input.name}}.go`
     - Rust (ratatui): `src/ui/{{input.name}}.rs`
     - Python (textual): `src/screens/{{input.name}}.py`
     - Node (ink): `src/components/{{input.name}}.tsx`
   - Implement based on view type:
     - `list`: scrollable list with selection, filtering, sorting
     - `detail`: display item details with sections
     - `form`: input fields with validation, tab navigation between fields
     - `dashboard`: multi-pane layout with status/metrics
     - `modal`: overlay dialog with confirm/cancel

3. **Implement Model (state)**
   - Define view state struct/class
   - Initialize with sensible defaults
   - Handle loading, ready, and error states
   - Manage cursor/selection position

4. **Implement Update (event handling)**
   - Keybinding handling:
     - Navigation: arrow keys, j/k, tab, enter, escape
     - Actions: custom keys for view-specific actions
     - Global: q/ctrl+c to quit, ? for help
   - Window resize handling
   - Async data loading (if applicable)

5. **Implement View (rendering)**
   - Layout: header, content area, footer/status bar
   - Responsive to terminal size
   - Styled text (colors, bold, borders)
   - Scrolling for content that exceeds viewport
   - Loading spinner/indicator
   - Empty state message

6. **Register view in navigation**
   - Add to screen router/navigator
   - Setup transitions between views
   - Handle back navigation

7. **Create tests**
   - Model initialization
   - State transitions on key events
   - Rendering output verification
   - Edge cases: empty data, very long text, small terminal

## Script

```bash
#!/bin/bash
# Detect TUI framework
if [ -f "go.mod" ]; then
  if grep -q "bubbletea" go.mod 2>/dev/null; then
    echo "Framework: Bubble Tea (Go)"
    echo "View path: internal/ui/{{input.name}}.go"
    if grep -q "lipgloss" go.mod 2>/dev/null; then
      echo "Styling: Lip Gloss"
    fi
    if grep -q "bubbles" go.mod 2>/dev/null; then
      echo "Components: Bubbles"
    fi
  fi
elif [ -f "Cargo.toml" ]; then
  if grep -q "ratatui" Cargo.toml 2>/dev/null; then
    echo "Framework: Ratatui (Rust)"
    echo "View path: src/ui/{{input.name}}.rs"
  elif grep -q "tui " Cargo.toml 2>/dev/null; then
    echo "Framework: tui-rs (Rust)"
  fi
elif [ -f "pyproject.toml" ] || [ -f "requirements.txt" ]; then
  if grep -q "textual" pyproject.toml requirements.txt 2>/dev/null; then
    echo "Framework: Textual (Python)"
    echo "View path: src/screens/{{input.name}}.py"
  elif grep -q "urwid" pyproject.toml requirements.txt 2>/dev/null; then
    echo "Framework: Urwid (Python)"
  fi
elif [ -f "package.json" ]; then
  if grep -q '"ink"' package.json 2>/dev/null; then
    echo "Framework: Ink (React for CLI)"
    echo "View path: src/components/{{input.name}}.tsx"
  fi
fi
```

## Validation

- [ ] View file created and follows existing patterns
- [ ] View renders correctly in terminal
- [ ] Keybindings work as expected
- [ ] Navigation to/from this view works
- [ ] Responsive to terminal resize
- [ ] Loading and error states handled
- [ ] Empty state displayed when no data
- [ ] Tests created and passing
- [ ] Compile/typecheck passing
- [ ] No flickering or rendering artifacts
