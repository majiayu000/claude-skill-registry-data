---
name: ss-guardrails
description: A library of safety, code-quality, and anti-mistake checklists that other ss-* skills consult on demand while writing or reviewing code. Not invoked directly by users — skills like ss-coding-workflow, ss-code-review, and ss-coding read core.md plus the relevant language file before generating or grading code.
---

# Guardrails

This skill is a reference library, not a workflow. Other skills read it at the point where they need to write, change, or review code; it has no standalone "run" behavior of its own.

## What's Here

| File | Covers | Read When |
|------|--------|-----------|
| `core.md` | Security baseline, code-review dimensions and severity levels, unit-testing principles, and anti-mistake rules for AI coding agents | Always — every coding or review task |
| `java.md` | Java exception handling and concurrency anti-patterns, JVM testing pitfalls | Project is Java/Kotlin/JVM |
| `go.md` | Go error handling and testing pitfalls | Project is Go |
| `cpp.md` | C++ memory safety, concurrency, error handling, and testing pitfalls | Project is C++ |
| `web.md` | Frontend/Node security and quality pitfalls | Project is TypeScript/JavaScript/web |
| `android.md` | Android-specific safety and quality pitfalls | Project is Android/Kotlin |
| `ios.md` | iOS-specific safety and quality pitfalls | Project is iOS/Swift |
| `flutter.md` | Flutter/Dart-specific safety and quality pitfalls | Project is Flutter |

## How to Use This

1. Detect the project's primary language/stack (build files, file extensions, existing code) or ask if it's ambiguous.
2. Read `core.md` in full — it applies regardless of stack.
3. Read the one or two language files that match the project's stack. Skip the rest.
4. Apply the checklists while writing code, and re-check against them during review, before claiming a task complete.

Treat this as read-only reference material: load it into context at the moment it's needed, apply it, and don't copy its contents into the user's repository. It carries no user-specific configuration and produces no output files of its own.

## Failure Handling

If the project's stack isn't covered by any language file here, fall back to `core.md` alone and note the gap to the user rather than guessing at stack-specific rules that don't exist yet.
