---
name: pwa-storage-patterns
description: Implement data persistence patterns for Progressive Web Apps. Use when working with browser storage APIs, implementing localStorage or IndexedDB, or managing client-side data persistence.
---

# PWA Storage Patterns

## Overview

This skill covers data persistence patterns for Progressive Web Apps, including localStorage and IndexedDB usage, error handling, and data migration strategies.

## Storage Options

### localStorage

**Best for**: Small data (< 5MB), simple key-value storage, quick access

**Limits**:
- Chrome/Edge: ~10MB per origin
- Firefox: ~10MB per origin
- Safari: ~5MB per origin

### IndexedDB

**Best for**: Large data (> 5MB), indexed queries, transactions, complex data

**Limits**: Typically 50% of available disk space

## localStorage Pattern

### Standard Load/Save Functions

```rust
use web_sys::window;
use serde_json;

fn load_reminders() -> Vec<Reminder> {
    if let Some(window) = web_sys::window() {
        if let Some(storage) = window.local_storage().ok().flatten() {
            if let Ok(Some(data)) = storage.get_item("reminders") {
                if let Ok(reminders) = serde_json::from_str::<Vec<Reminder>>(&data) {
                    return reminders;
                }
            }
        }
    }
    Vec::new()  // Safe fallback
}

fn save_reminders(reminders: &[Reminder]) {
    if let Some(window) = web_sys::window() {
        if let Some(storage) = window.local_storage().ok().flatten() {
            if let Ok(json) = serde_json::to_string(reminders) {
                let _ = storage.set_item("reminders", &json);
            }
        }
    }
}
```

### Error Handling Strategy

**Load Errors**: Return safe default (empty collection)

```rust
fn load_reminders() -> Vec<Reminder> {
    // Try to load, fallback to empty
    // ...
    Vec::new()  // Always returns valid data
}
```

**Save Errors**: Silent failure (non-critical)

```rust
fn save_reminders(reminders: &[Reminder]) {
    // Try to save, ignore errors
    // localStorage errors are non-critical
}
```

### Storage Key Naming

**Convention**: Plural, lowercase, snake_case

```rust
const STORAGE_KEY_REMINDERS: &str = "reminders";
const STORAGE_KEY_SETTINGS: &str = "settings";
const STORAGE_KEY_CACHE: &str = "cache";
```

## Integration with State

### Initialize from Storage

```rust
#[component]
fn App() -> Element {
    // Load from storage on mount
    let mut reminders = use_signal(|| load_reminders());
    
    rsx! { /* ... */ }
}
```

### Save on State Changes

```rust
// After adding
on_add: move |reminder: Reminder| {
    let mut new_reminders = reminders();
    new_reminders.push(reminder);
    reminders.set(new_reminders.clone());
    save_reminders(&new_reminders);  // Persist immediately
}

// After updating
on_toggle: move |id: String| {
    let mut updated = reminders();
    if let Some(r) = updated.iter_mut().find(|r| r.id == id) {
        r.completed = !r.completed;
    }
    reminders.set(updated.clone());
    save_reminders(&updated);
}

// After deleting
on_delete: move |id: String| {
    let mut updated = reminders();
    updated.retain(|r| r.id != id);
    reminders.set(updated.clone());
    save_reminders(&updated);
}
```

## IndexedDB Pattern (Future)

### Service Manager Pattern

```rust
pub struct StorageService {
    reminders_db: RemindersDB,
    settings_db: SettingsDB,
}

impl StorageService {
    pub async fn init() -> Result<Self, StorageError> {
        let reminders_db = RemindersDB::new("RemindersDB", 1).await?;
        let settings_db = SettingsDB::new("SettingsDB", 1).await?;
        Ok(Self { reminders_db, settings_db })
    }
}
```

### Specialized Database Service

```rust
pub struct RemindersDB {
    db: IdbDatabase,
    store: ObjectStore,
}

impl RemindersDB {
    pub async fn write(&self, reminder: &Reminder) -> Result<(), StorageError> {
        // Write to IndexedDB
    }
    
    pub async fn read_all(&self) -> Result<Vec<Reminder>, StorageError> {
        // Read all from IndexedDB
    }
    
    pub async fn read_by_id(&self, id: &str) -> Result<Option<Reminder>, StorageError> {
        // Indexed query by ID
    }
}
```

## Data Migration

### Version Management

```rust
const STORAGE_VERSION: &str = "v1";
const STORAGE_KEY: &str = "reminders_v1";

fn load_reminders() -> Vec<Reminder> {
    // Try current version
    if let Ok(Some(data)) = get_storage_item(STORAGE_KEY) {
        if let Ok(reminders) = serde_json::from_str::<Vec<Reminder>>(&data) {
            return reminders;
        }
    }
    
    // Try old version and migrate
    if let Ok(Some(data)) = get_storage_item("reminders") {
        if let Ok(old_reminders) = serde_json::from_str::<Vec<OldReminder>>(&data) {
            let migrated = migrate_reminders(old_reminders);
            save_reminders(&migrated);
            return migrated;
        }
    }
    
    Vec::new()
}
```

## Best Practices

### DO:
- ✅ Always provide fallback on load error
- ✅ Save immediately after state changes
- ✅ Use descriptive storage keys
- ✅ Handle serialization errors gracefully
- ✅ Use consistent key naming (plural, lowercase, snake_case)
- ✅ Document storage keys in code

### DON'T:
- ❌ Don't panic on storage errors
- ❌ Don't store sensitive data in localStorage
- ❌ Don't store large binary data
- ❌ Don't forget to save after mutations
- ❌ Don't use `unwrap()` on storage operations
- ❌ Don't mix storage formats (always use JSON)

## When to Use Each Storage

### Use localStorage When:
- Data size < 5MB
- Simple key-value storage
- No complex queries needed
- Quick prototyping
- Small to medium datasets

### Consider IndexedDB When:
- Data size > 5MB
- Need indexed queries
- Need transactions
- Large number of records (1000+)
- Need partial updates
- Complex data relationships

## Resources

- [MDN localStorage](https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage)
- [MDN IndexedDB](https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API)
- [Storage for the Web](https://web.dev/storage-for-the-web/)

