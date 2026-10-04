---
name: code-review-pyramid
description: >
  Knowledge base for the Code Review Pyramid — a framework for structuring code reviews across
  five layers prioritized by cost-of-change. Use when the user asks how to approach a code review,
  wants to understand what to focus on in a review, asks about review priorities, or references
  "the pyramid". Also use when another skill needs a structured review framework (e.g.
  review-changes loads it to apply consistent layer priorities and questions).
---

# Code Review Pyramid

The Code Review Pyramid provides guidance on aspects to focus on during code reviews, prioritized by the cost of fixing issues later. Layers at the bottom of the pyramid deserve more attention because they are harder and more expensive to change after. Layers at the top are easier to address (often automatable) and warrant proportionally less manual review effort.

*Adapted from the [Code Review Pyramid](https://www.morling.dev/blog/the-code-review-pyramid/) by [Gunnar Morling](https://www.morling.dev/), licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).*

## The Pyramid

Five layers, numbered from the base up. Manual review attention should be highest at the base and taper toward the apex, where checks should be automated as much as possible:

1. **API Semantics** — base: focus here most
2. **Implementation Semantics** — focus here
3. **Documentation**
4. **Tests** — automate where possible
5. **Code Style** — apex: automate

## Layer 1 — API Semantics

Questions to ask:
- API as small as possible, as large as needed?
- Is there one way of doing one thing, not multiple?
- Is it consistent? Does it follow the principle of least surprise?
- Clean split of API/internals, without internals leaking in the API?
- Are there no breaking changes to user-facing parts (API classes, configuration, metrics, log formats, etc.)?
- Is a new API generally useful and not overly specific?

## Layer 2 — Implementation Semantics

Questions to ask:
- Does it satisfy the original requirements?
- Is it logically correct?
- Is there no unnecessary complexity?
- Is it robust? (no concurrency issues, proper error handling)
- Is it performant?
- Is it secure? (e.g. no SQL injection, no sensitive data exposure, etc.)
- Is it observable? (e.g. metrics, logging, tracing, etc.)
- Do newly added dependencies pull their weight? Are their licenses acceptable?

## Layer 3 — Documentation

Questions to ask:
- Are new features reasonably documented?
- Are the relevant kinds of docs covered: README, API docs, user guide, reference docs, etc.?
- Are docs understandable? Are there no significant typos or grammar mistakes?

## Layer 4 — Tests

Questions to ask:
- Are all tests passing?
- Are new features reasonably tested?
- Are corner cases tested?
- Is it using unit tests where possible, integration tests where necessary?
- Are there tests for NFRs, e.g. performance?

## Layer 5 — Code Style

Questions to ask:
- Is the project's formatting style applied?
- Does it adhere to agreed naming conventions?
- Is it DRY?
- Is the code sufficiently readable? (method lengths, etc.)
