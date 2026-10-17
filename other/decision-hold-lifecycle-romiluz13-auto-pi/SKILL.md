---
name: decision-hold-lifecycle
description: Never lose an unresolved decision. Use when work discovers an open question that needs the user's input, before declaring that work complete. Persists decisions to ~/.pi/agent/decisions.json so they survive compaction and session restarts. Inspired by FirstMate's decision-hold-lifecycle.
user-invocable: false
---

# Decision Hold Lifecycle

Every unresolved decision that belongs to the user and is discovered while producing work must become a structured hold item before that work may be treated as complete.

## Why

Decisions evaporate between sessions. Compaction wipes them. Context resets lose them. The audit (Jul 2026) found that focus-loss often starts with an unresolved decision that was never persisted — the model moved on, the user never saw it, and the work proceeded on an assumption.

This skill is the structural fix: decisions get persisted to disk, not held in context.

## What it does

1. **Inventory.** When you discover an unresolved choice that requires the user, give it a stable key (a short slug), a title, a reason, and the repository/project path.

2. **Hold.** Write it to `~/.pi/agent/decisions.json`:

   ```json
   [
     {
       "key": "pagination-cursor-vs-offset",
       "title": "Cursor-based or offset-based pagination?",
       "reason": "Cursor is more performant for large datasets but breaks skip-to-page UX",
       "project": "/Users/rom.iluz/Dev/SDR-AI",
       "createdAt": "2026-07-20T...",
       "resolved": false
     }
   ]
   ```

3. **Surface.** The `/bearings` command reads this file and shows open decisions in the "Your Call" section. The user sees them on their next status check.

4. **Resolve.** When the user decides, mark `resolved: true` and record their answer in a `resolution` field. Dependent work can proceed.

## Rules

- Only genuine unresolved choices that require the user create holds.
- Resolved findings, recommendations that need no user choice, and prose that merely sounds decision-like do NOT create holds.
- A hold remains open until the user's answer is durably recorded — not until the originating task completes.
- Do not close a hold merely because the task completed, the session ended, or compaction fired.
- Use the same key on retry so registration is idempotent.
