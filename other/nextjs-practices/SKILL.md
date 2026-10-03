---
name: nextjs-practices
description:
  Next.js App Router architecture and UI composition practices. Use when writing, reviewing, or
  refactoring routes, layouts, access boundaries, feature ownership, or shared UI in a Next.js
  application.
license: MIT
metadata:
  author: AutanaSoft
  organization: AutanaSoft
  version: '0.2.0'
  date: '2026-05'
---

# Next.js Practices

Rules for keeping App Router files focused on framework boundaries while feature modules own product
logic.

## When to Apply

- Work with App Router routes, layouts, route handlers, or Server Components.
- Organize feature modules, access boundaries, or shared UI in a Next.js application.

## Rule Categories by Priority

| Priority | Category             | Impact | Prefix     |
| -------- | -------------------- | ------ | ---------- |
| 1        | App Router           | HIGH   | `app-`     |
| 2        | Feature architecture | HIGH   | `feature-` |
| 3        | UI composition       | HIGH   | `ui-`      |

## Quick Reference

- Keep routes thin - `app-keep-routes-thin`
- Use semantic route groups - `app-use-semantic-route-groups`
- Delegate layouts to feature shells - `app-delegate-layouts-to-feature-shells`
- Place access guards at layout boundaries - `app-place-access-guards-at-layout-boundaries`
- Let features own product logic - `feature-own-product-logic`
- Separate shared UI from application composition - `ui-use-workspace-structure`

## How to Use

Read the card that applies: `references/<prefix>-<slug>.md`.
