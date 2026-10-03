---
name: project-onto-all-systems
description: Use when adding or changing a feature, a data model, or any action that creates, edits, or removes state.
---

## The rule

A feature is never just the function you're writing. It ripples into the cache that now holds stale data and the notification that now says the wrong thing; undo doesn't know the change happened, and no test covers it. Before you call it done, walk the whole system and ask what this change touches.

This is about the consequences of the change you're already making, not a license to add features nobody asked for. You're tracing the ripples of one change, not widening the scope.

## Fires when

Adding a feature, changing a data model, or adding any action that creates, edits, or removes state.

## How to apply

List every subsystem the change could reach: cache and invalidation, notifications and messages, persistence and migrations, undo and history, permissions, search and indexing, tests. For each one, ask "does this change need something here?" Handle it or consciously decide to skip it. Don't just forget it exists.

## Worked example

You add "rename project". The rename function itself is trivial. But the cache still maps the old name, the recent-items list still shows it, the audit log records "created" instead of "renamed", search still indexes the old name, and nothing tests the name-collision case.

The one-line rename was about 10% of the real work. Projecting it across the system surfaced the other 90% before it shipped broken.

## Red flags

| Thought | Reality |
|---|---|
| "It's just a small change" | Small in one file, wide across the system. |
| "The function works" | The function isn't the feature. |
| "I'll handle the cache later" | Later is a bug report from a user. |
