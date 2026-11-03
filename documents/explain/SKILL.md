---
name: explain
description: Explain a Java, Spring Boot, JPA, or React Native concept to an experienced Go/TypeScript developer, grounded in this repo's code. Use when the user asks "why", "what does X do", "how does @Annotation work", or wants a concept unpacked.
argument-hint: "<concept, annotation, class, or file:line>"
---

# /explain

Audience: senior engineer, fluent in Go/Node/TS/Postgres, new to Java/Spring. Don't explain what a REST API or an index is.

Structure (keep it tight, under ~400 words unless asked for more):

1. **One-sentence answer.**
2. **Analogy:** the closest Go or TS/Node equivalent, and where the analogy breaks.
3. **In this repo:** point at the real code (`path:line`) that uses it. If it isn't used yet, show a minimal snippet in the repo's style.
4. **What happens under the hood:** e.g. proxies, bean lifecycle, persistence context, filter chain. Just enough to predict behavior.
5. **Common mistakes:** 1–3 gotchas.
6. **Go deeper:** one authoritative link (Spring reference docs first, then Vlad Mihalcea for JPA, then `docs/learning/RESOURCES.md`).

If the user would learn more by trying it, suggest a 2-minute experiment (e.g. "remove `@Transactional` and run this test, then watch it fail").
If the concept is worth remembering, offer to add it to `docs/learning/java-for-go-ts-devs.md`.
