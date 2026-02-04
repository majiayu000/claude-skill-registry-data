---
name: dioxus-pwa-development
description: Build Progressive Web Apps with Dioxus framework. Use when developing Dioxus web applications, creating PWA features, or working with WASM targets.
---

# Dioxus PWA Development

## Overview

Dioxus is a React-like UI framework for Rust that compiles to WebAssembly. This skill covers building Progressive Web Apps (PWAs) with Dioxus, including component development, state management, and PWA configuration.

## Core Concepts

### Dioxus Framework

Dioxus provides a React-like component system for Rust:

- **Components**: Reusable UI building blocks
- **Signals**: Reactive state management with `use_signal()`
- **Event Handlers**: User interaction handling
- **RSX**: JSX-like syntax for UI definition

### PWA Features

Progressive Web Apps include:

- **Manifest**: App metadata and installation configuration
- **Service Worker**: Offline support and caching
- **Responsive Design**: Mobile-first approach
- **Installability**: Users can install as native apps

## Component Development

### Basic Component Pattern

```rust
use dioxus::prelude::*;

#[component]
fn App() -> Element {
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

### Component with Props

```rust
#[component]
fn ReminderCard(
    reminder: Reminder,
    on_toggle: EventHandler<String>,
    on_delete: EventHandler<String>,
) -> Element {
    rsx! {
        div {
            class: "reminder-card",
            h3 { "{reminder.title}" }
            button {
                onclick: move |_| on_toggle.call(reminder.id.clone()),
                "Toggle"
            }
        }
    }
}
```

## State Management

### Signal Usage

```rust
// Initialize signal
let mut reminders = use_signal(|| load_reminders());

// Read signal
let current = reminders();

// Update signal
reminders.set(new_reminders);
```

### Event Handlers

```rust
// Inline handler
onclick: move |_| {
    reminders.set(new_reminders);
}

// Handler with parameter
onclick: move |e| {
    title.set(e.value())
}
```

## Conditional and List Rendering

### Conditional Rendering

```rust
rsx! {
    if show_form() {
        AddReminderForm { on_add: move |r| { /* ... */ } }
    }
    
    if reminders().is_empty() {
        div { "No reminders yet" }
    }
}
```

### List Rendering

```rust
rsx! {
    for reminder in reminders().iter().filter(|r| !r.completed) {
        ReminderCard {
            reminder: reminder.clone(),
            on_toggle: move |id| { /* ... */ },
        }
    }
}
```

## PWA Configuration

### Manifest.json

```json
{
  "name": "Remind Me PWA",
  "short_name": "RemindMe",
  "start_url": "/remind-me-pwa/",
  "display": "standalone",
  "theme_color": "#000000",
  "background_color": "#ffffff",
  "icons": [
    {
      "src": "/remind-me-pwa/assets/icon-192.png",
      "sizes": "192x192",
      "type": "image/png"
    }
  ]
}
```

### Service Worker

Basic service worker for caching:

```javascript
const CACHE_NAME = 'remind-me-pwa-v1';
const urlsToCache = [
  '/remind-me-pwa/',
  '/remind-me-pwa/index.html',
  '/remind-me-pwa/assets/style.css'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => cache.addAll(urlsToCache))
  );
});
```

### Dioxus.toml Configuration

```toml
[web.app]
base_path = "/remind-me-pwa"  # For GitHub Pages deployment

[web.pwa]
enabled = true
manifest = "assets/manifest.json"
service_worker = "assets/sw.js"
```

## Build and Deployment

### Development

```bash
# Install Dioxus CLI
cargo install dioxus-cli --locked

# Start development server
dx serve
```

### Production Build

```bash
# Build for production
dx build --release --platform web

# Output in target/dx/{package}/release/web/public
```

### GitHub Pages Deployment

1. Set `base_path` in `Dioxus.toml`
2. Build output to `docs/` directory
3. Configure GitHub Pages to serve from `docs/`
4. Create `404.html` for client-side routing

## Best Practices

### DO:
- ✅ Use `use_signal()` for reactive state
- ✅ Keep components small and focused
- ✅ Use `EventHandler` for parent-child communication
- ✅ Configure PWA manifest properly
- ✅ Test offline functionality
- ✅ Use `base_path` for subdirectory deployment

### DON'T:
- ❌ Don't mutate state directly (use `.set()`)
- ❌ Don't create signals in render loops
- ❌ Don't skip PWA configuration
- ❌ Don't hardcode paths (use base_path)
- ❌ Don't forget to update cache versions

## Common Patterns

### Form Input Pattern

```rust
#[component]
fn AddReminderForm(on_add: EventHandler<Reminder>) -> Element {
    let mut title = use_signal(|| String::new());
    
    rsx! {
        input {
            value: "{title()}",
            oninput: move |e| title.set(e.value())
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
```

### Filter Pattern

```rust
let mut filter = use_signal(|| "all".to_string());

rsx! {
    for reminder in reminders().iter().filter(|r| {
        match filter().as_str() {
            "active" => !r.completed,
            "completed" => r.completed,
            _ => true,
        }
    }) {
        ReminderCard { reminder: reminder.clone() }
    }
}
```

## Resources

- [Dioxus Documentation](https://dioxuslabs.com/learn/0.6/)
- [Dioxus Web Guide](https://dioxuslabs.com/learn/0.6/getting_started/web)
- [PWA Best Practices](https://web.dev/progressive-web-apps/)

