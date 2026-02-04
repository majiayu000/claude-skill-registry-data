---
name: rust-ownership
description: Master Rust ownership, borrowing, lifetimes, and memory safety. Understand move semantics, references, and zero-cost abstractions.
---

# Rust Ownership System

Master Rust's ownership system for writing safe, efficient, and concurrent code without garbage collection.

## Core Concepts

### Ownership Rules
1. Each value has an owner
2. Only one owner at a time
3. Value dropped when owner goes out of scope

```rust
fn main() {
    let s1 = String::from("hello");
    let s2 = s1; // s1 moved to s2, s1 no longer valid

    println!("{}", s2); // OK
    // println!("{}", s1); // Error: value borrowed after move
}
```

### Borrowing
```rust
fn main() {
    let s1 = String::from("hello");

    let len = calculate_length(&s1); // Borrow s1

    println!("Length of '{}' is {}", s1, len); // s1 still valid
}

fn calculate_length(s: &String) -> usize {
    s.len()
} // s goes out of scope but nothing happens (doesn't own the data)
```

### Mutable References
```rust
fn main() {
    let mut s = String::from("hello");

    change(&mut s);

    println!("{}", s); // "hello, world"
}

fn change(s: &mut String) {
    s.push_str(", world");
}
```

### Lifetimes
```rust
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() {
        x
    } else {
        y
    }
}
```

## Best Practices

1. Prefer borrowing over ownership transfer
2. Use mutable references sparingly
3. Understand lifetime elision rules
4. Use smart pointers (Box, Rc, Arc) when needed
5. Leverage the borrow checker

## Resources
- https://doc.rust-lang.org/book/ch04-00-understanding-ownership.html
