---
name: ticket-breakdown
description: Break a spec or plan into implementation-ready issues with explicit dependencies. Use when work must be split across contributors, milestones, or a tracker.
---

# Ticket Breakdown

Convert an approved spec or plan into a small set of independently understandable work items.

Each ticket should state:

- outcome and rationale, not just a list of edits;
- bounded scope and likely code area;
- acceptance criteria that can be checked;
- test or verification expectation;
- dependencies and blockers;
- owner only when ownership is known.

Prefer end-to-end tracer-bullet tickets over layers of disconnected scaffolding. Make dependency edges explicit and avoid false parallelism. Split tickets when they have different owners, review needs, release boundaries, or independent outcomes. Merge tickets that would create awkward partial states.

Do not create duplicate issues or mutate an external tracker without explicit authorization. When writing local files, use a clear stable identifier and preserve the original spec link. Report what is ready, what is blocked, and the critical path.
