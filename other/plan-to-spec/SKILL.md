---
name: plan-to-spec
category: meta-orchestration
description: Synthesize the current conversation into a spec (PRD) and stage it as a local file. Use when a design discussion, grilling session, or work-plan is settled and you want it written up as a spec — no interview, just synthesis. Publishing to Confluence is opt-in, only on request.
disable-model-invocation: true
codex-short-description: "Synthesize a settled discussion into a local spec file"
compatibility: claude-code codex opencode
---

# Plan to Spec

Turn the **current conversation** and codebase understanding into a spec, and **stage it as a local file**. Do **not** interview the user — synthesize what's already been discussed. To sharpen an idea *before* it's ready, run `/grill-with-docs` (or `/work-plan` for a large effort) first; this skill is the write-up step after the thinking is done.

**Local-first.** The spec is written to local storage by default. It is **never** pushed to Confluence (or any remote) without the user explicitly asking, and never without confirming the destination first. The local file is the source of truth; Confluence is an optional downstream copy.

**Does this work need a spec at all?** The spec earns its step on multi-session work, where tickets are disposable and it stays as the one place the reasoning lives. On a change that fits a single session it buys nothing and adds a synthesis step for the model to drift in — say so and send the user straight to `implement`.

**Stay in this conversation.** Run `plan-to-tickets` in the same window rather than clearing or compacting between them: a large spec can outgrow what a remote page serves back cleanly, and re-fetching it in chunks is where the next step silently truncates.

**Architectural work fits the template badly.** A refactor or a module-boundary change written as user stories produces stories nobody asked for around decisions that are really about interfaces and invariants. Lean on the implementation-decisions and testing-decisions sections instead, and let the durable calls land as ADRs via `grill-with-docs` rather than making the spec carry them.

**It won't check the tracker for you.** The spec respects the ADRs covering the area, but nothing searches for overlapping issues already filed — a spec can quietly duplicate work in flight. Where the area is busy, search first.

## Process

### 1. Resolve the staging location

The spec lands in a **staging directory** the user controls, laid out spec-kit style: one numbered feature folder per spec.

```text
<staging>/NNN-<feature-slug>/spec.md
```

Resolve `<staging>` in this order:

1. A path the user passed as an argument this run.
2. The memory default `reference_plan_staging_dir.md`, if it exists.
3. Otherwise **ask** where to stage (offer a sensible default like `./specs/` or `.plans/` under the repo). Offer to record the answer to `reference_plan_staging_dir.md` so future runs skip the prompt — record only if the user agrees.

Pick the next free `NNN` (zero-padded, starting `001`) in the staging dir and a kebab-case `<feature-slug>` from the feature name. State the resolved path back before writing.

### 2. Explore the repo

If not already, explore to ground the spec in the current code. Use the project's domain vocabulary throughout (`CONTEXT.md` glossary if present) and respect ADRs in the area you're touching.

### 3. Sketch the test seams

Name the seams at which the feature will be tested. Prefer existing seams to new ones, and the **highest** seam possible — the fewer seams across the codebase, the better; one is ideal. Check the seams match the user's expectations before writing.

### 4. Write the spec locally

Write the template below to `<staging>/NNN-<feature-slug>/spec.md`. Report the file path. This is where the skill **stops by default** — the spec is staged, ready for `/plan-to-tickets`.

<spec-template>

# <Feature name> — Spec

## Problem Statement

The problem the user faces, from the user's perspective.

## Solution

The solution, from the user's perspective.

## User Stories

A LONG, numbered list, each `As an <actor>, I want <feature>, so that <benefit>`. Cover every aspect of the feature — be extensive.

## Implementation Decisions

Modules built/modified, their changed interfaces, technical clarifications, architectural decisions, schema changes, API contracts, specific interactions. Do **not** include file paths or code snippets — they go stale. Exception: a prototype snippet that encodes a decision more precisely than prose (state machine, reducer, schema, type shape) — inline the decision-rich parts and note it came from a prototype.

## Testing Decisions

What makes a good test here (external behaviour, not implementation details); which modules will be tested; prior art (similar tests already in the codebase).

## Out of Scope

What this spec deliberately excludes.

## Further Notes

Anything else.

</spec-template>

### 5. Publish to Confluence — only if asked

If — and only if — the user asks to publish, confirm the destination first (space + parent page, read the space key from `reference_confluence_default_space.md`), then create the page (`confluence_create_page`) from the staged `spec.md`. If the discussion traces to a Jira ticket, add a remote link from that ticket to the page (`jira_add_remote_link`). Record the published URL back into the local `spec.md` (a `> Published: <url>` line at the top) so the local copy points at its remote twin. Report the URL.

## Rules

- **Local-first, always.** Write the local `spec.md` before anything else. It is the source of truth.
- **No remote writes without an explicit ask AND a confirmed destination.** Never publish to Confluence by default; never publish without confirming space/parent first.
- **Staging location is the user's to choose.** Argument > memory default > ask. Persist the default only with consent.
- **Synthesize, don't interview.** If you're asking design questions, the thinking isn't done — that's `/grill-with-docs`.

The staged spec feeds `/plan-to-tickets`, which breaks it into a local numbered task list.

## Quality Loop

Before returning, check the output against these criteria. If two or more fail, revise and re-check — at most two passes, then note what still falls short.

- Spec is staged as a numbered local spec.md (spec-kit style), not published unless asked
- Every requirement traces back to a point settled in the source discussion
- Open questions are listed rather than silently decided
- No implementation detail leaks into what should be a requirements doc

> **Host portability:** tool names follow Claude Code conventions; on other hosts map by intent — see [PORTABILITY.md](../PORTABILITY.md).

<!-- self-evolve:start -->
## Self-Evolve Loop
Journal `~/.ink-and-agency/learnings/plan-to-spec.md` (or workspace-local `.ink-and-agency/` where the sandbox confines writes). Read it first; append what the run taught — [SELF-EVOLVE.md](../SELF-EVOLVE.md).
<!-- self-evolve:end -->
