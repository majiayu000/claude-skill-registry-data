---
name: reactive-state-expert
description: Expert on FLUI's reactive state management with signals, hooks, and effects. Use when discussing state, signals, use_signal, use_effect, reactivity, or data flow.
---

# Reactive State Expert

Expert skill for FLUI's reactive state management system.

## When to Use

Activate this skill when the user:
- Works with signals or reactive state
- Uses hooks like use_signal, use_effect, use_memo
- Discusses data flow or state updates
- Debugs reactivity issues
- Implements stateful widgets

## Core Concepts

### Signals
Copy-based reactive primitives with automatic dependency tracking.

```rust
// Create signal
let count = use_signal(ctx, 0);

// Read value
let current = count.get();

// Update value (triggers rebuild)
count.set(current + 1);

// Update with closure
count.update(|x| x + 1);
```

### Signal Internals
```rust
// Signals use Copy semantics
pub struct Signal<T: Copy> {
    id: SignalId,
    // Value stored in global signal store (DashMap)
}

// Thread-safe with DashMap for lock-free access
```

## Available Hooks

### use_signal
```rust
// Basic state
let count = use_signal(ctx, 0);

// Computed from props
let doubled = use_signal(ctx, self.value * 2);
```

### use_effect
```rust
// Side effects that run after build
use_effect(ctx, || {
    tracing::info!("Component mounted");
    
    // Cleanup function (optional)
    || {
        tracing::info!("Component unmounted");
    }
});

// With dependencies
use_effect_with_deps(ctx, (count.get(),), |deps| {
    tracing::info!("Count changed to: {}", deps.0);
    || {}
});
```

### use_memo
```rust
// Expensive computation cached
let expensive = use_memo(ctx, || {
    compute_expensive_value()
});

// With dependencies
let result = use_memo_with_deps(ctx, (a, b), |(a, b)| {
    expensive_computation(*a, *b)
});
```

### use_ref
```rust
// Mutable reference that doesn't trigger rebuilds
let dom_ref = use_ref(ctx, || None::<DomHandle>);
```

## Critical Rules

### Hook Order
```rust
// ALWAYS call hooks in the same order!

// BAD - conditional hook
if condition {
    let signal = use_signal(ctx, 0);  // PANIC!
}

// GOOD - always call, conditionally use
let signal = use_signal(ctx, 0);
if condition {
    signal.set(42);
}
```

### No Loops
```rust
// BAD - variable hook count
for i in 0..items.len() {
    let signal = use_signal(ctx, i);  // PANIC!
}

// GOOD - use single signal with collection
let items = use_signal(ctx, vec![1, 2, 3]);
```

### BuildContext is Read-Only
```rust
// Signal handles rebuild scheduling internally
let signal = use_signal(ctx, 0);
signal.set(42);  // Triggers rebuild via callback

// DON'T try to schedule rebuilds manually during build
```

## State Management Patterns

### Lifting State
```rust
// Parent owns state
struct Parent;
impl View for Parent {
    fn build(&self, ctx: &mut BuildContext) -> impl IntoElement {
        let count = use_signal(ctx, 0);
        
        Column::new(vec![
            Display { count: count.get() },
            Controls { on_increment: move || count.update(|x| x + 1) },
        ])
    }
}
```

### Derived State
```rust
impl View for MyWidget {
    fn build(&self, ctx: &mut BuildContext) -> impl IntoElement {
        let count = use_signal(ctx, 0);
        
        // Derived computation in build - recalculated each time
        let is_even = count.get() % 2 == 0;
        
        // Or use memo for expensive derivations
        let expensive = use_memo(ctx, || {
            compute_from_count(count.get())
        });
    }
}
```

### Async State
```rust
// Resource hook for async data
let users = use_resource(ctx, || async {
    fetch_users().await
});

match users.get() {
    ResourceState::Loading => LoadingSpinner {},
    ResourceState::Ready(data) => UserList { users: data },
    ResourceState::Error(e) => ErrorDisplay { error: e },
}
```

## Debugging Reactivity

### Tracing Updates
```rust
#[tracing::instrument]
fn build(&self, ctx: &mut BuildContext) -> impl IntoElement {
    let count = use_signal(ctx, 0);
    tracing::debug!(count = count.get(), "Building with count");
    // ...
}
```

### Common Issues

**Issue: Infinite rebuilds**
```rust
// BAD - sets signal during build
let signal = use_signal(ctx, 0);
signal.set(signal.get() + 1);  // Infinite loop!

// GOOD - set in event handler
Button::new("Increment")
    .on_press(move || signal.update(|x| x + 1))
```

**Issue: Stale closures**
```rust
// BAD - closure captures old value
let handler = || {
    let current = count.get();  // Captured at build time
    process(current);
};

// GOOD - read inside closure
let handler = move || {
    process(count.get());  // Fresh value
};
```

**Issue: Missing updates**
```rust
// Signals use Copy - modifications don't propagate
let mut value = signal.get();
value += 1;  // Only modifies local copy!

// GOOD - use set/update
signal.set(signal.get() + 1);
```

## Performance Tips

1. **Minimize signal scope**: Keep signals as local as possible
2. **Use memo for expensive computations**: Cache derived data
3. **Batch updates**: Group related state changes
4. **Avoid deep nesting**: Flatten state structure when possible
