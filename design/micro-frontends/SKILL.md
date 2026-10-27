---
name: micro-frontends
description: "Micro-frontend architecture, Module Federation, cross-app routing, and shared dependency singletons."
---

# Micro-Frontends & Module Federation Protocol

Decompose monolithic frontends into autonomously deployable team boundaries.

---

## 1. Module Federation Discipline

1. Share core framework runtimes (`react`, `vue`) as singletons to prevent multiple runtime instances.
2. Version contract interfaces between host and remote micro-apps strictly.

---

## 2. Isolation & Communication

- Isolate styles using CSS Modules or Shadow DOM.
- Communicate between micro-frontends exclusively via CustomEvents or URL query state, never global window mutations.
