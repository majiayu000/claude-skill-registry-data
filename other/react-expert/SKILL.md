---
name: react-expert
description: "React 19 patterns, Server Components (RSC), hooks rules, memoization discipline, and concurrent features."
---

# React 19 & Modern Hooks Protocol

Author high-performance, maintainable React component trees.

---

## 1. Server vs Client Components

1. Default to React Server Components (RSC) for data fetching, static rendering, and zero-bundle-size overhead.
2. Add `'use client'` only at the leaf nodes requiring browser events (`onClick`, `onChange`), browser APIs, or stateful hooks.

---

## 2. Hooks Discipline & Rules

1. Never call hooks conditionally or inside loops.
2. Keep `useEffect` strictly for synchronization with external non-React systems. Do not use `useEffect` to calculate derived state or trigger cascading renders.
