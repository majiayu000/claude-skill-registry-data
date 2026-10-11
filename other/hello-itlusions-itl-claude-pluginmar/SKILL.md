---
name: hello
description: Minimal example skill — greets the user and reports the current date/time. Use for "say hello", "hello world", "test the hello plugin".
---

# Hello — Example Skill

## Purpose

A deliberately trivial skill that exists to exercise the `ITL.Claude.PluginMarketplace`
pipeline (`discover` → `ci` → `publish`) with a second, independent plugin — proving the
pipeline's per-plugin versioning, tagging, and release logic scales without any pipeline
changes when a new plugin is added. Each release is tagged as `hello-plugin/vX.Y.Z`.

## Behavior

When invoked, respond with a short, friendly greeting and the current date/time. Nothing else —
no external tools, no side effects. This skill is intentionally minimal.

## Example

**User:** say hello

**Response:**
```
Hello! It's currently [current date/time].
```
