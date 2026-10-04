---
name: injectable-trait
description: Makes traits injectable using #[injectable(trait)] and dyn Trait injection. Use when defining injectable service traits, enabling mock implementations, or using trait objects in DI.
---

# Trait Injection with `#[injectable(trait)]`

Generates infrastructure for trait injection, including a type-erased provider and `Inject<dyn Trait>` support.

## Basic pattern

```rust
use injectable::prelude::*;

#[injectable(trait)]
pub trait EmailSender {
    fn send(&self, to: &str, subject: &str, body: &str);
}

pub struct SmtpSender;

impl EmailSender for SmtpSender {
    fn send(&self, to: &str, subject: &str, body: &str) {
        println!("Sending email to {to}: {subject}");
    }
}

bind!(dyn EmailSender => SmtpSender);

#[injectable]
struct NotificationService {
    sender: Inject<dyn EmailSender>,
}
```

## How it works

1. `#[injectable(trait)]` marks the trait as part of the injectable surface
2. `bind!()` creates a static binding from `dyn Trait` to `Concrete`
3. `Inject<dyn Trait>` resolves via the bound concrete type's provider

## With default implementation

```rust
#[injectable(trait)]
pub trait Logger {
    fn log(&self, msg: &str) {
        println!("[LOG] {msg}");
    }
}

pub struct NoOpLogger;

impl Logger for NoOpLogger {}

bind!(dyn Logger => NoOpLogger);
```

## Mocking in tests

```rust
pub struct MockEmailSender;

impl EmailSender for MockEmailSender {
    fn send(&self, to: &str, _subject: &str, _body: &str) {
        println!("[MOCK] Would send email to {to}");
    }
}

// Override binding
bind!(dyn EmailSender => MockEmailSender);
```

## Error handling

```rust
#[injectable]
struct UserService {
    sender: Inject<dyn EmailSender>,
}

impl UserService {
    fn notify_user(&self, user: &User) {
        self.sender.send(&user.email, "Welcome!", "Hello from injectable!");
    }
}
```

## Guidelines

- Use `#[injectable(trait)]` on traits that have a single primary implementation
- Use `bind!()` to declare which concrete type satisfies the trait
- `Inject<dyn Trait>` needs a `bind!()` mapping; the trait annotation is the
  recommended documented pattern

See [skills/bind-macro](../bind-macro/SKILL.md) and
[guides/README.md](../../guides/README.md).

This pattern enables dependency inversion in your DI graph — depend on abstractions (traits), not concrete types.
