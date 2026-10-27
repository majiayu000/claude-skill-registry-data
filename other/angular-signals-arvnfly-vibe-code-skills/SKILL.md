---
name: angular-signals
description: "Modern Angular architecture, reactive signals, standalone components, inject(), and control flow syntax."
---

# Modern Angular Signals Protocol

Build enterprise Angular apps using standalone components and signals.

---

## 1. Signals Over RxJS for Component State

1. Define reactive state with `signal()`.
2. Compute derived values with `computed()`.
3. Run side effects with `effect()` in injection contexts.

---

## 2. Standalone Components & Modern Control Flow

- Omit NgModules; set `standalone: true` on all components.
- Use native `@if`, `@for`, and `@switch` control flow syntax rather than `*ngIf` or `*ngFor`.
