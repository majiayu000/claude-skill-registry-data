---
name: cli-todo-ui
description: Build modern, interactive terminal-based todo applications with beautiful UI/UX using Python's Textual framework. Use when building CLI todo apps, task managers, or interactive terminal interfaces that require menu-driven flows, visual polish (colors, icons, tables), keyboard shortcuts, mouse support, and professional developer experience. Ideal for hackathons and rapid prototyping of terminal UIs.
---

# CLI Todo UI Builder

Build professional, interactive terminal-based todo applications with modern aesthetics using Python's Textual framework and Rich library.

## Quick Start

### Option 1: Generate Complete App (Recommended)

Use the complete todo app template from `assets/todo-app-template/`:

```bash
# Copy the template to your project
cp -r assets/todo-app-template/* ./

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

The template includes:
- Full Textual application with menu-driven interface
- In-memory task storage (decoupled from UI)
- Color-coded status indicators (☐ Pending, ☑ Completed)
- Keyboard shortcuts and mouse support
- Professional styling with Textual CSS

### Option 2: Install Dependencies Only

```bash
bash scripts/install_dependencies.sh
```

## Core Stack

- **Textual** (≥0.63.0): Modern TUI framework with reactive components
- **Rich** (≥13.7.0): Beautiful terminal formatting
- **Pydantic** (≥2.0.0): Data validation (optional)

## Key Features to Implement

### Essential Features (Must-Have)
1. **Interactive DataTable**: Arrow key navigation, row selection
2. **Color-coded statuses**: Visual indicators (🔴 High, 🟡 Medium, 🟢 Low priority)
3. **Keyboard shortcuts**: Visible in footer (`a` Add, `d` Delete, `space` Toggle, `q` Quit)
4. **Confirmation dialogs**: Modal confirmations for destructive actions
5. **Stats panel**: Live counts (Total, Pending, Completed, %)

### Enhanced Features (Nice-to-Have)
6. **Live search/filter**: Type to filter tasks instantly
7. **Mouse support**: Click to select, drag to reorder
8. **Progress bars**: Visual completion percentage
9. **Split layout**: Task list (left) + Details preview (right)
10. **Tabbed interface**: Switch between "All", "Active", "Completed"

### Advanced Features (Bonus)
11. **Undo/Redo**: Revert last action with visual feedback
12. **Bulk operations**: Multi-select for batch delete/complete
13. **Export**: Pretty-print to markdown/JSON
14. **Theme toggle**: Dark/light mode switching
15. **Animations**: Smooth transitions and task completion effects

## Architecture Pattern

### In-Memory Task Storage (Decoupled)

```python
from dataclasses import dataclass
from typing import List
from datetime import datetime

@dataclass
class Task:
    id: int
    title: str
    description: str = ""
    completed: bool = False
    created_at: datetime = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

class TaskManager:
    """Business logic layer - decoupled from UI"""
    def __init__(self):
        self.tasks: List[Task] = []
        self.next_id = 1

    def add_task(self, title: str, description: str = "") -> Task:
        task = Task(id=self.next_id, title=title, description=description)
        self.tasks.append(task)
        self.next_id += 1
        return task

    def get_task(self, task_id: int) -> Task | None:
        return next((t for t in self.tasks if t.id == task_id), None)

    def delete_task(self, task_id: int) -> bool:
        task = self.get_task(task_id)
        if task:
            self.tasks.remove(task)
            return True
        return False

    def toggle_task(self, task_id: int) -> bool:
        task = self.get_task(task_id)
        if task:
            task.completed = not task.completed
            return True
        return False

    def get_stats(self) -> dict:
        total = len(self.tasks)
        completed = sum(1 for t in self.tasks if t.completed)
        return {
            "total": total,
            "completed": completed,
            "pending": total - completed,
            "percentage": (completed / total * 100) if total > 0 else 0
        }
```

### Textual App Structure

```python
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal
from textual.widgets import Header, Footer, DataTable, Button, Static
from textual.binding import Binding

class TodoApp(App):
    """Main Textual application"""

    CSS = """
    DataTable {
        height: 1fr;
        border: solid $primary;
    }

    #stats {
        height: 3;
        background: $panel;
        border: solid $secondary;
        padding: 1;
    }
    """

    BINDINGS = [
        Binding("a", "add_task", "Add Task"),
        Binding("d", "delete_task", "Delete"),
        Binding("space", "toggle_task", "Toggle"),
        Binding("q", "quit", "Quit"),
    ]

    def __init__(self):
        super().__init__()
        self.task_manager = TaskManager()

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Static(id="stats")
        yield DataTable(zebra_stripes=True)
        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns("ID", "Status", "Title", "Description")
        self.refresh_table()

    def action_add_task(self) -> None:
        # Implement add task modal
        pass

    def action_delete_task(self) -> None:
        # Implement delete with confirmation
        pass

    def action_toggle_task(self) -> None:
        # Toggle selected task
        pass

    def refresh_table(self) -> None:
        # Update table with current tasks
        pass

if __name__ == "__main__":
    app = TodoApp()
    app.run()
```

## Reference Documentation

- **Textual Patterns**: See `references/textual-patterns.md` for widgets, styling, and reactive patterns
- **UI Features**: See `references/ui-features.md` for comprehensive UI/UX enhancement examples
- **Keyboard Shortcuts**: See `references/keyboard-shortcuts.md` for standard binding patterns

## Common Patterns

### Adding Confirmation Dialogs

```python
from textual.screen import ModalScreen
from textual.widgets import Label, Button

class ConfirmDialog(ModalScreen):
    def __init__(self, message: str):
        super().__init__()
        self.message = message

    def compose(self) -> ComposeResult:
        yield Container(
            Label(self.message),
            Horizontal(
                Button("Confirm", variant="error", id="confirm"),
                Button("Cancel", variant="default", id="cancel")
            )
        )

# Usage in app
def action_delete_task(self) -> None:
    def handle_response(confirmed: bool) -> None:
        if confirmed:
            # Delete task
            pass

    self.push_screen(ConfirmDialog("Delete this task?"), handle_response)
```

### Live Filtering

```python
from textual.widgets import Input

class TodoApp(App):
    def compose(self) -> ComposeResult:
        yield Header()
        yield Input(placeholder="Search tasks...", id="search")
        yield DataTable()
        yield Footer()

    def on_input_changed(self, event: Input.Changed) -> None:
        search_term = event.value.lower()
        filtered_tasks = [
            t for t in self.task_manager.tasks
            if search_term in t.title.lower() or search_term in t.description.lower()
        ]
        self.refresh_table(filtered_tasks)
```

### Status Indicators

Use these emoji/color patterns for visual feedback:

- **Task Status**: ☐ Pending (gray), ☑ Completed (green), ⏳ In Progress (yellow)
- **Priority**: 🔴 High, 🟡 Medium, 🟢 Low
- **Actions**: ✨ Add, 🗑️ Delete, ✓ Toggle, 🔍 Search

## Testing

Test the script by running it:

```bash
python app.py
```

Expected behavior:
- App launches with empty task list
- Keyboard shortcuts appear in footer
- Can add, view, toggle, and delete tasks
- Stats update in real-time
- UI is visually polished with colors and borders

## Troubleshooting

- **Import errors**: Ensure `textual` and `rich` are installed
- **Terminal size**: Textual requires minimum 80x24 terminal
- **Colors not showing**: Check terminal supports 256 colors
- **Mouse not working**: Enable mouse support in terminal emulator
