---
name: analiz-gate
category: pm
description: Use when deciding whether a request needs an analiz task before implementation - the conditions that require the architect's analysis versus going straight to implementation
---
# Analiz Gate

## Overview

Some work can go straight to implementation tasks; some needs the architect to investigate first. Guessing wrong is costly: skipping a needed analiz produces bounced tasks, and forcing analiz on trivial work wastes a cycle.

**Core principle:** Analiz when the approach is unknown; skip it when the work is clear and small.

## Open a type=analiz task when ANY of

- The stack/framework for the feature is unknown.
- The API or UI contract between components is undefined.
- The request is broad and needs technical slicing.
- Repository feasibility is unknown (new integration, DB schema change).
- Estimated scope > 1 developer-day with unclear breakdown.
- A new web frontend has no design system yet — the architect sequences a foundation task before any screen, and an analiz description for UI work should carry the design brief (see implementation-task-spec).
- The change spans two or more repositories, or creates a new API contract between layers.
- It's a greenfield product or a brand-new repository.

When unsure between a direct task and analiz, take analiz — hidden complexity only grows once implementation starts.

## Do NOT open analiz for

- Small bug fixes with clear reproduction steps.
- Pure UI copy or styling changes.
- Features already analyzed and documented.

## Mechanics

Assign the analiz task to **system-architect** and move it to `todo` (investigation is always safe to start — no stakeholder approval needed). The analysis itself returns through the **human analiz_review gate** before any implementation task is created. Never assign analiz to yourself or a developer.

## Worked Example

- "Change the button label from 'Save' to 'Apply'." → No analiz: pure copy change → one frontend task.
- "Add real-time notifications." → Analiz: transport (WebSocket? SSE? polling?) and the contract are undefined → analiz task to the architect.
- "Fix the 500 when deleting a task with subtasks." → No analiz: clear repro → one bug task.

## Common Mistakes

- Forcing analiz on a one-line copy change.
- Skipping analiz on a broad "add reporting" request → the dev bounces on undefined scope.
- Assigning analiz to a developer.

## Red Flags

- An implementation task created for a request whose approach nobody has defined.
- An analiz task assigned to anyone but the architect.
