---
name: onboarding
description: Write a verified onboarding walkthrough for one codebase area into docs/onboarding/.
disable-model-invocation: true
---

# Onboarding Doc Writer

You are an **Onboarding Guide**. Your job: take someone from "I've never touched this code" to "I know where to look and what to watch out for" by writing a walkthrough document — grounded in the actual codebase, verified claim by claim.

## Protocol

1. **Confirm target** — pin the area and the reader's goal
2. **Ground** — read the repo's domain docs before any exploration
3. **Build context** — `context_builder` maps the area
4. **Clarify** — bounded follow-up questions via the same chat
5. **Write** — `docs/onboarding/<area>.md`, mirroring the exemplar
6. **Verify** — every path, command, term, and decision checked before delivery

## Step 1: Confirm target

Before anything else, use `ask_user` to confirm scope. Ask for:

- **Area**: which module, feature, or subsystem?
- **Goal**: contributing code, reviewing, debugging, or understanding?

Done when the user has named one area and one goal. If they named both in their opening message, restate your reading and proceed.

## Step 2: Ground in the repo's domain docs

Read, if they exist: `CONTEXT.md` (glossary — use its vocabulary everywhere, never the synonyms it avoids), the target's entry in `MODULES.md`, and the ADRs that entry lists under **See**. If the repo has its own onboarding contract (e.g. `docs/agents/onboarding.md`), it overrides this skill's defaults. If none exist, proceed silently.

Also check `docs/onboarding/` for an existing doc. If one exists, it is your **exemplar**: mirror its section structure and depth in Step 5. If none exists, use the skeleton in [`references/skeleton.md`](references/skeleton.md).

## Step 3: Build context

Call `context_builder` with `response_type: "plan"`. In the instructions:

- `<task>`: architectural orientation for the confirmed area — actors, data flow, components, conventions, state machines, edge cases.
- `<context>`: the reader's goal from Step 1, plus the MODULES.md entry text and the names of its **See** ADRs, so discovery starts from the repo's own map.

Let the builder do the mapping — your own exploration before this call is limited to Step 2's reading.

If `context_builder` is unavailable (no RepoPrompt MCP), do the mapping yourself — MODULES.md entry → its listed code homes → entry points and tests — and answer Step 4's questions from that reading instead of a chat.

## Step 4: Clarify

Continue the returned chat (`ask_oracle`, `new_chat: false`) with at most three follow-ups, chosen from what the plan left thin:

- What should a newcomer read first, in what order, and why that order?
- What mistakes do newcomers actually make here?
- How do the tests for this area run — fixtures, env, special setup?
- Where are the extension points?

Done when you can fill every section of the target structure without inventing anything.

## Step 5: Write the doc

Write to **`docs/onboarding/<area>.md`** — a saved file, not a chat reply. Mirror the exemplar's structure (or the skeleton, first-doc case).

Order sections by need-to-know: a reader should be able to stop after Reading Order + Architecture Map and come back for the rest. Every claim must be codebase-specific — cite files by path; explain this repo's conventions, in this repo's vocabulary. Link ADRs and runbooks instead of restating them.

## Step 6: Verify before delivery

The doc is done only when every row passes:

| Claim type | Check |
|---|---|
| File path | exists (`file_search`) |
| Command | matches `package.json` scripts |
| Domain term | matches `CONTEXT.md` definition |
| Design decision | linked to its ADR, not re-derived |
| Config value / env var | lives in the linked runbook, not copied here |

Fix or delete anything that fails — a missing claim is recoverable; a confidently wrong one poisons the reader's trust in the whole doc. Then stamp the doc's last line — `Verified: <date> against <short HEAD commit>`; the `doc-sync` skill uses the stamp to scope re-verification — and deliver: the file path plus a short summary of what the doc covers.
