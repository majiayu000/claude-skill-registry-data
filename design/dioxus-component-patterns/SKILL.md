---
name: dioxus-component-patterns
description: Master Dioxus component patterns and reactive state management. Use when building Dioxus components, managing component state, or implementing component interactions.
---

# Dioxus Component Patterns

## Overview

This skill covers component patterns in Dioxus, including component structure, props, state management, event handling, and component composition.

## Component Structure

### Basic Component

```rust
use dioxus::prelude::*;

#[component]
fn ComponentName() -> Element {
    rsx! {
        div {
            "Hello, World!"
        }
    }
}
```

### Component with State

```rust
#[component]
fn Counter() -> Element {
    let mut count = use_signal(|| 0);
    
    rsx! {
        div {
            h1 { "Count: {count()}" }
            button {
                onclick: move |_| count.set(count() + 1),
                "Increment"
            }
        }
    }
}
```

## Props Pattern

### Simple Props

```rust
#[component]
fn Greeting(name: String) -> Element {
    rsx! {
        div {
            "Hello, {name}!"
        }
    }
}
```

### Props with Event Handlers

```rust
#[component]
fn ReminderCard(
    reminder: Reminder,
    on_toggle: EventHandler<String>,
    on_delete: EventHandler<String>,
) -> Element {
    let reminder_id = reminder.id.clone();
    
    rsx! {
        div {
            class: "reminder-card",
            h3 { "{reminder.title}" }
            button {
                onclick: move |_| on_toggle.call(reminder_id.clone()),
                "Toggle"
            }
            button {
                onclick: move |_| on_delete.call(reminder_id),
                "Delete"
            }
        }
    }
}
```

## State Management Patterns

### Local Component State

```rust
#[component]
fn Form() -> Element {
    let mut title = use_signal(|| String::new());
    let mut description = use_signal(|| String::new());
    
    rsx! {
        input {
            value: "{title()}",
            oninput: move |e| title.set(e.value())
        }
    }
}
```

### Shared State via Props

```rust
#[component]
fn App() -> Element {
    let mut reminders = use_signal(|| load_reminders());
    
    rsx! {
        ReminderList {
            reminders: reminders(),
            on_update: move |new_reminders| {
                reminders.set(new_reminders);
            }
        }
    }
}
```

### Derived State

```rust
#[component]
fn ReminderStats(reminders: Vec<Reminder>) -> Element {
    let total = reminders.len();
    let completed = reminders.iter().filter(|r| r.completed).count();
    let active = total - completed;
    
    rsx! {
        div {
            "Total: {total}, Active: {active}, Completed: {completed}"
        }
    }
}
```

## Event Handling Patterns

### Inline Handlers

```rust
rsx! {
    button {
        onclick: move |_| {
            count.set(count() + 1);
        },
        "Click"
    }
}
```

### Handler with Event Data

```rust
rsx! {
    input {
        oninput: move |e| {
            title.set(e.value());
        }
    }
}
```

### Handler with Cloned Data

```rust
#[component]
fn ReminderItem(reminder: Reminder, on_delete: EventHandler<String>) -> Element {
    let reminder_id = reminder.id.clone();
    
    rsx! {
        button {
            onclick: move |_| {
                on_delete.call(reminder_id);
            },
            "Delete"
        }
    }
}
```

## Conditional Rendering

### Simple If

```rust
rsx! {
    if show_form() {
        AddReminderForm { on_add: move |r| { /* ... */ } }
    }
}
```

### If-Else

```rust
rsx! {
    if reminders().is_empty() {
        div { "No reminders yet" }
    } else {
        ReminderList { reminders: reminders() }
    }
}
```

### Ternary-like Pattern

```rust
rsx! {
    div {
        class: if is_active() { "active" } else { "inactive" },
        "Content"
    }
}
```

## List Rendering

### Simple List

```rust
rsx! {
    for reminder in reminders().iter() {
        ReminderCard {
            reminder: reminder.clone(),
            on_toggle: move |id| { /* ... */ },
        }
    }
}
```

### List with Filter

```rust
rsx! {
    for reminder in reminders().iter().filter(|r| !r.completed) {
        ReminderCard { reminder: reminder.clone() }
    }
}
```

### List with Index

```rust
rsx! {
    for (index, reminder) in reminders().iter().enumerate() {
        ReminderCard {
            reminder: reminder.clone(),
            index: index,
        }
    }
}
```

## Component Composition

### Container Component

```rust
#[component]
fn App() -> Element {
    let mut reminders = use_signal(|| load_reminders());
    let mut show_form = use_signal(|| false);
    
    rsx! {
        div {
            Header {
                on_new_click: move |_| show_form.set(true)
            }
            if show_form() {
                AddReminderForm {
                    on_add: move |r| { /* ... */ },
                    on_cancel: move |_| show_form.set(false),
                }
            }
            ReminderList {
                reminders: reminders(),
                on_update: move |new| reminders.set(new),
            }
        }
    }
}
```

### Presentational Component

```rust
#[component]
fn ReminderList(
    reminders: Vec<Reminder>,
    on_update: EventHandler<Vec<Reminder>>,
) -> Element {
    rsx! {
        div {
            class: "reminder-list",
            for reminder in reminders.iter() {
                ReminderCard {
                    reminder: reminder.clone(),
                    on_toggle: move |id| {
                        let mut updated = reminders.clone();
                        // Update logic
                        on_update.call(updated);
                    },
                }
            }
        }
    }
}
```

## Form Patterns

### Controlled Input

```rust
#[component]
fn TextInput(value: String, on_change: EventHandler<String>) -> Element {
    rsx! {
        input {
            value: "{value}",
            oninput: move |e| on_change.call(e.value())
        }
    }
}
```

### Form with Validation

```rust
#[component]
fn AddReminderForm(on_add: EventHandler<Reminder>) -> Element {
    let mut title = use_signal(|| String::new());
    let mut error = use_signal(|| None::<String>);
    
    rsx! {
        div {
            input {
                value: "{title()}",
                oninput: move |e| {
                    title.set(e.value());
                    if e.value().is_empty() {
                        error.set(Some("Title is required".to_string()));
                    } else {
                        error.set(None);
                    }
                }
            }
            if let Some(err) = error() {
                span { class: "error", "{err}" }
            }
            button {
                disabled: title().is_empty(),
                onclick: move |_| {
                    if !title().is_empty() {
                        on_add.call(Reminder { /* ... */ });
                        title.set(String::new());
                    }
                },
                "Add"
            }
        }
    }
}
```

## Best Practices

### DO:
- ✅ Keep components small and focused
- ✅ Use descriptive component names
- ✅ Pass only necessary props
- ✅ Use `EventHandler` for callbacks
- ✅ Clone only what's needed in closures
- ✅ Use conditional rendering for UI states
- ✅ Use iterators for list rendering

### DON'T:
- ❌ Don't create signals in render loops
- ❌ Don't mutate state directly (use `.set()`)
- ❌ Don't pass entire state to child components
- ❌ Don't create unnecessary clones
- ❌ Don't use indices when iterators work
- ❌ Don't mix concerns in components

## Common Patterns

### Loading State

```rust
let mut loading = use_signal(|| false);

rsx! {
    if loading() {
        div { "Loading..." }
    } else {
        ReminderList { reminders: reminders() }
    }
}
```

### Error State

```rust
let mut error = use_signal(|| None::<String>);

rsx! {
    if let Some(err) = error() {
        div { class: "error", "{err}" }
    }
}
```

### Toggle Pattern

```rust
let mut is_open = use_signal(|| false);

rsx! {
    button {
        onclick: move |_| is_open.set(!is_open()),
        if is_open() { "Close" } else { "Open" }
    }
    if is_open() {
        div { "Content" }
    }
}
```

## Resources

- [Dioxus Components Guide](https://dioxuslabs.com/learn/0.6/guide/components/)
- [Dioxus Signals](https://dioxuslabs.com/learn/0.6/guide/signals/)
- [Dioxus Events](https://dioxuslabs.com/learn/0.6/guide/events/)

