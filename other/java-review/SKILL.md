---
name: java-review
description: Mentor-style review of Java/Spring code the user wrote themselves — correctness first, then idiom, explaining the "why" behind each suggestion. Use when the user says "review my code", "I wrote X, check it", or after a "your turn" exercise.
argument-hint: "[file or class; defaults to uncommitted backend changes]"
---

# /java-review: mentor review

Target: the given file(s), or `git diff` + untracked files under `backend/` if none are given.

Review like a senior Java engineer mentoring a senior Go/TS engineer:

1. **Does it work?** Run the relevant tests (`./mvnw test -Dtest=...`). Report bugs, edge cases, and missing tests first.
2. **Spring/JPA correctness:** transaction boundaries, lazy loading outside a transaction, `@Transactional` self-invocation,
   user scoping on queries, entity leaking out of the service, validation missing on requests.
3. **Idiomatic Java:** records vs classes, `final`, `Optional` misuse, `var`, streams vs loops (pick the readable one),
   `java.time` usage, exceptions, visibility (package-private by default), naming.
4. **Simplicity:** flag unnecessary interfaces, layers, or patterns.

Format:
- Start with what's good (be specific, briefly).
- Then findings ordered by importance. For each: the location (`path:line`), the issue, **why it matters in Java/Spring**,
  and the suggested change as a small snippet.
- Label each finding **must-fix**, **should**, or **nit**.

**Don't rewrite their code for them** unless asked. Let them apply the fixes, then offer a quick re-review.
