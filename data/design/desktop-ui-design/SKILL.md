---
name: "Desktop UI Design"
description: "Design intuitive desktop interfaces following platform conventions with proper layouts, keyboard shortcuts, and native widgets"
category: "ui-design"
required_tools: ["Read", "Write", "WebSearch"]
---

# Desktop UI Design

## Purpose
Design intuitive desktop application interfaces using native UI frameworks (Tkinter, Qt, WPF, etc.) following platform conventions and usability best practices.

## When to Use
- Creating desktop application interfaces
- Designing forms and dialogs
- Planning menu structures and navigation
- Organizing application windows

## Key Capabilities
1. **Layout Design** - Organize controls logically with proper spacing
2. **Platform Conventions** - Follow OS-specific design guidelines
3. **Usability Patterns** - Apply desktop UI best practices

## Approach
1. Understand user workflows and tasks
2. Group related controls together
3. Follow platform conventions (Windows, macOS, Linux)
4. Use familiar patterns (menus, toolbars, status bars)
5. Ensure keyboard accessibility
6. Provide visual feedback for actions

## Example
**Context**: Task management application main window
````
Menu Bar: File | Edit | View | Tools | Help
Toolbar: [New] [Open] [Save] [Refresh]
─────────────────────────────────────
Main Content Area:
┌─ Task List ─────────────────────┐
│ ☐ Task 1    High    Pending     │
│ ☑ Task 2    Normal  Complete    │
│ ☐ Task 3    Low     Pending     │
└─────────────────────────────────┘
Status Bar: 3 tasks | 1 active | Last refresh: 2:30 PM
````

**Design Principles**:
- Most important actions in toolbar
- Full functionality in menus
- Context menus for quick access
- Status bar for non-critical info
- Keyboard shortcuts for common actions

## Best Practices
- ✅ Use native widgets for platform consistency
- ✅ Provide keyboard shortcuts (Ctrl+N, F5, etc.)
- ✅ Show visual feedback (disabled states, progress indicators)
- ✅ Use standard dialog patterns (OK/Cancel, Yes/No)
- ❌ Avoid: Custom widgets that don't match platform look
- ❌ Avoid: Hiding important actions deep in menus