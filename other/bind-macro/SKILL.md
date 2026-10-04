---
name: bind-macro
description: Binds trait objects to concrete implementations using bind!(). Use when injecting dyn Trait types, swapping implementations (mock vs production), or getting 'conflicting implementations' errors.
---

# bind! Macro

Creates a static binding from a trait to a concrete type for `Inject<dyn Trait>`.
Use it with `#[injectable(trait)]` when you want the trait itself to opt into
the injectable docs/discovery flow.

## Basic pattern

```rust
use injectable::prelude::*;

// Define the trait
#[injectable(trait)]
pub trait EmailSender {
    fn send(&self, to: &str, subject: &str, body: &str);
}

// Implement the trait
pub struct SmtpSender;

impl EmailSender for SmtpSender {
    fn send(&self, to: &str, subject: &str, body: &str) {
        println!("Sending email to {to}: {subject}");
    }
}

// Create a singleton binding
bind!(dyn EmailSender => SmtpSender);

// Now Inject<dyn EmailSender> works
#[injectable]
struct NotificationService {
    sender: Inject<dyn EmailSender>,
}
```

## With DynProvider for external traits

```rust
use injectable::prelude::*;

#[injectable(trait)]
pub trait Cache {
    fn get(&self, key: &str) -> Option<String>;
    fn set(&self, key: &str, value: String);
}

pub struct InMemoryCache {
    store: std::collections::HashMap<String, String>,
}

impl Cache for InMemoryCache {
    fn get(&self, key: &str) -> Option<String> {
        self.store.get(key).cloned()
    }
    fn set(&self, key: &str, value: String) {
        self.store.insert(key, value);
    }
}

bind!(dyn Cache => InMemoryCache);

#[injectable]
struct UserService {
    cache: Inject<dyn Cache>,
}
```

## Mock in tests

```rust
pub struct MockEmailSender;

impl EmailSender for MockEmailSender {
    fn send(&self, to: &str, _subject: &str, _body: &str) {
        println!("[MOCK] Would send email to {to}");
    }
}

// Override binding in test
bind!(dyn EmailSender => MockEmailSender);
```

## bind! vs manual registration

| Approach | Use when |
|---|---|
| `bind!(dyn Trait => Concrete)` | Concrete type is `#[injectable]` |
| `DynProvider` | External type or needs custom factory |
| Both combined | Trait from external crate + custom factory |

The `bind!` macro generates the `Extract` impl for `Inject<dyn Trait>` that delegates to `Concrete::Provider`.

Notes:

- `bind!` resolves through the concrete provider and does not go through the
  singleton cache for `Inject<dyn Trait>`.
- The trait annotation is recommended for clarity, but `bind!` can still work
  with unannotated traits when the trait object is otherwise valid.

See [skills/injectable-trait](../injectable-trait/SKILL.md),
[guides/04-external-types.md](../../guides/04-external-types.md), and
[guides/README.md](../../guides/README.md).
