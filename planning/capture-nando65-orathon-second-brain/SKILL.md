---
name: capture
description: Run a guided discovery session and persist the conversation into a durable local note as it unfolds.
argument-hint: "[topic or goal]"
---

# Capture

Use this for discovery, planning, requirements gathering, interviews, or extracting knowledge that currently lives in the user's head.

Read `SYSTEM.md` and only the existing context relevant to the topic.

## Start

Create a new file:

`captures/YYYY-MM-DD-HHMM-<topic>.md`

Never overwrite an existing capture.

Write a header with:
- topic,
- date/time,
- goal,
- status: `in-progress`,
- relevant source files already consulted.

Tell the user the path once.

## During the session

Ask one useful question at a time.

After each user answer, update the capture **before** asking the next question. Record:

- the question,
- confirmed facts or decisions,
- tentative ideas,
- assistant suggestions if any,
- unresolved items and who can resolve them.

Do not silently convert a suggestion into a user decision.

If a later answer changes an earlier conclusion, preserve the earlier entry and mark the newer one as the current state.

If the answer can be found by reading an available file or connected source, retrieve it instead of asking the user to repeat it.

## End or pause

When the user stops, update:
- status: `paused` or `complete`,
- current synthesis,
- unresolved items,
- exact resume point.

Only promote durable, user-confirmed facts into `workspace/` when the user asked for the session to update canonical context.

If a concrete decision was finalized, add a concise entry to `journal/decisions.md` without duplicating an existing decision.
