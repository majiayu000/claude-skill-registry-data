---
name: scheduled-routines
description: Create repeatable, bounded, resumable tasks using the existing Remote Arc scheduler.
priority: P0
category: productivity
status: builtin-guidance
---

# Scheduled Routines

**Scope:** Remote Arc automation runtime. **Source:** https://remotearc.app

## Workflow

Use Remote Arc's existing automation/goal scheduler; this is a method, not a new MCP tool. Agree on trigger, goal, authorized device, permitted apps and paths, output artifact, spending/time budgets, review gates and stop condition. Prefer event-driven checks before calling a model; keep idempotent checkpoints, bounded retries and an audit trail. Pause and resume without losing task state. Explicit confirmation is required for outgoing emails, publishing, purchases and destructive actions. Validate actual outcome using source-of-truth data before marking complete. If the device is asleep/offline, park the run rather than claiming success. Never schedule unbounded paid API loops.

## Device and permission gates

Required authorization scopes: automation:read, automation:write. Scripts, OS/desktop actions, external service side effects, media generation and paid API usage require independent user-approved execution permissions. This skill does not elevate Remote Arc Tool privileges or authorize use of hidden credentials.

## Preflight

Check the engines this skill names before relying on them, with tools you already have (for example `<engine> --version` through start_process, or list_directory on its install folder). Missing executors must be installed explicitly on the correct user device. A Skill being built-in is NOT evidence an engine is present.

## Evidence of completion

Report input constraints, executed tools and device, verified output path/result, permissions used, cost (if known) and failures. Do not imply successful execution from merely writing a plan.
