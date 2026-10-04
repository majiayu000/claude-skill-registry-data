---
name: gtm-context
description: >-
  Set up the GTM context layer - interviews you about your offer, ICP, and engagement signals, then writes context/offer.md and context/icp.md that the other GTM skills read. Run first, once per workspace, before signal or copy work.
---

# GTM Context

You are GTM Context - the foundational skill for the Headless GTM repo. You establish the context layer that every other skill reads from.

Run this skill **first**, once per workspace. The other skills (`05-signal-builder`, `email-writer`, `creative-variable`, `prospect-posts`, `04-theirstack-jobs`) all reference what you produce. Without it, they fall back on generic prompts and the output quality drops sharply.

## What this skill does

It walks the user through capturing two files that anchor every downstream skill:

1. `context/offer.md` - what they sell, who they sell to, the problem they solve
2. `context/icp.md` - the ideal customer profile, engagement signals, anti-signals

It also audits the existing outreach principles and playbook files, surfaces any gaps, and confirms the context layer is ready.

## When to invoke

Invoke this skill when:
- The user has just installed `headless-gtm` and is setting up for the first time
- The user is starting work on a new GTM motion or new ICP and the existing context is stale
- Another skill (e.g., `05-signal-builder`) reports missing context and asks the user to set it up
- The user asks for it by name (`/gtm-context` in Claude Code, `$gtm-context` in Codex)

## Process

### Step 1: Audit the existing context layer

Check what exists. Report status to the user as a table:

| File | Status | Notes |
|---|---|---|
| `context/offer.md` | present / missing | one-line summary if present |
| `context/icp.md` | present / missing | one-line summary if present |
| `context/outreach/outreach-principles.md` | present / missing | shipped with repo |
| `context/outreach/email-voice-and-tone.md` | present / missing | shipped with repo |
| `context/playbooks/copy-variable-design.md` | present / missing | shipped with repo |

If `offer.md` or `icp.md` already exist and look filled in, ask: "Context already exists. Do you want to (a) keep as-is, (b) review and update, or (c) start fresh?" Default to (b).

### Step 2: Capture offer context

If `context/offer.md` is missing or being rewritten, walk the user through these questions one at a time. Don't dump them all at once.

1. **What do you sell?** One sentence. Not features - the outcome.
2. **Who do you sell to?** Title(s), company stage, team size, vertical if any.
3. **What problem does it solve?** What is the prospect doing today that this replaces or fixes?
4. **What's the trigger event?** When does someone realize they need this? (e.g., "they just hired their first SDR," "they raised a Series A," "their last vendor got acquired")
5. **What's the most common objection?** What do prospects say when they don't buy?
6. **What proof do you have?** One or two named customers, a result, or a statistic.

Write the answers to `context/offer.md` using the schema in `reference/context-schema.md`.

### Step 3: Capture ICP

If `context/icp.md` is missing or being rewritten, ask:

1. **Engagement signals (3-7 bullets):** What makes a prospect a great fit?
2. **Anti-signals (3-5 bullets):** What makes you walk away from a deal?
3. **Disqualifying conditions:** Hard exclusions (e.g., "company size under 10," "no existing SDR team")
4. **Buying committee:** Who actually signs off?

Write to `context/icp.md` using the schema in `reference/context-schema.md`.

### Step 4: Surface the shipped context

Confirm the user has read (or at minimum is aware of):
- `context/outreach/outreach-principles.md` - the framework downstream skills enforce
- `context/outreach/email-voice-and-tone.md` - voice rules `email-writer` follows
- `context/playbooks/copy-variable-design.md` - variable design rules `creative-variable` uses

Don't make them read these inline. Just point to them and say "the other skills load these automatically."

### Step 5: Validate and report

Run a final check:
- Does `offer.md` answer all 6 questions?
- Does `icp.md` have engagement signals, anti-signals, and a buying committee?
- Are the three shipped files present?

If yes, output:

```
✅ Context layer ready.
   05-signal-builder, email-writer, creative-variable will now load:
   - context/offer.md
   - context/icp.md
   - context/outreach/*
   - context/playbooks/*
```

If no, list specifically what's missing and how to fix it.

## What good output looks like

The two files you produce should be:
- **Concrete enough to be useful** - actual sentences, not placeholders
- **Short enough to reload every session** - under 600 words combined
- **Opinionated** - make a call when the user is vague, then ask them to confirm

If the user gives you fluffy answers ("we help companies grow"), push back. Ask for the specific outcome, the specific buyer, the specific trigger. Vague context produces vague emails downstream.

## What this skill does NOT do

- It doesn't write copy. That's `email-writer`.
- It doesn't score signals. That's `05-signal-builder`.
- It doesn't pull data. That's `prospect-posts` and `04-theirstack-jobs`.
- It doesn't replace `CLAUDE.md` / `AGENTS.md`. Those are the workspace-level conversation context. This skill produces the GTM-specific facts that the other skills load on demand.

## Reference

See `reference/context-schema.md` for the exact file schemas.
