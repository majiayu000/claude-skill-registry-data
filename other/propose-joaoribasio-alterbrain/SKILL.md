---
name: propose
description: Write a short self-build proposal card (a new skill, helper agent, tool, automation or ready-made blueprint) for the user to approve, or, in proactive mode at the end of a session, suggest at most one when the user keeps doing the same job by hand; use for "could you make that a skill?", "build me something that…", "/propose", or "/propose --proactive".
model: sonnet
effort: medium
argument-hint: "[idea in plain words | blueprint <slug> | mcp <id> | --proactive]"
---

# Propose

Turn a repeated need into a one-page proposal the user can say yes or no to.

## When to use

- The user asks for a new ability: "Could you make that a skill?", "I want something that checks my numbers", "Can you connect Zotero?".
- The user picks something "available to build" from `/menu` (a blueprint) or a tool from the catalogue.
- **Proactive mode** (`/propose --proactive`): at the end of a session, or from `/weekly-review`, when the user did the same manual job again. Rules in `references/proactive.md`.

Nothing is built here. Building is `/build`, and only after a yes.

## Before you start

1. Check self-build settings: `node system/scripts/proposals.mjs status --json`.
   - `can_propose: false` (mode `off`): say "Building new skills is switched off. Say `/reconfigure` if you'd like it on." Stop.
   - Proactive mode: continue only if `can_suggest_proactively` is true.
2. Look for something that already exists, so you don't propose a duplicate:
   - `.claude/skills/*/SKILL.md` descriptions (including the user's `my-*` skills);
   - `system/blueprints/*.md` titles (a ready-made plan is safer than a new design);
   - `system/catalogue/mcp.json` `servers[]` (`what` lines);
   - open cards in `vault/00_inbox/proposals/`.
   If one fits, say so and offer it instead ("`/study` already does most of this. Want me to show you?").
3. A vague idea is fine here. Write what you know; `/build` runs `/clarify` before anything is built.
4. Get today's date from the system: `node system/scripts/date.mjs` (local date).

## Steps

1. **Decide the kind** (`skill`, `agent`, `mcp`, `blueprint`, `automation`) and the **name**:
   - designed for the user: `my-<slug>` (lowercase, hyphens, 2–4 words: `my-case-summary`);
   - a blueprint: the blueprint's file name without `.md` (`zotero`);
   - a catalogue tool only: the catalogue `id`.
2. **Pick model and effort** from the routing table (SPEC §6): sorting or tagging → haiku/low; drafting, notes, research → sonnet/medium; checking or critique → sonnet/high; real judgement → opus/high (rare). For a blueprint, use what it states.
3. **Rate the risk:**
   - `low`: reads and writes only inside `vault/`; no new accounts or keys.
   - `medium`: uses the web, a new tool, an API key, or school systems (read-only).
   - `high`: anything that could send, post, submit or delete; tools with `tier: "high-risk"`; always-on servers; `auto` sending. A blueprint's own `risk` wins if higher.
4. **Write the card** at `vault/00_inbox/proposals/<YYYY-MM-DD> <Title>.md`, starting from `system/templates/notes/proposal.md`. Frontmatter exactly as SPEC §11 (`type`, `created`, `status: "open"`, `kind`, `name`, `model`, `effort`, `risk`). Body sections, in plain words a non-technical reader understands:
   - **What it does**: one line, then one concrete example ("You drop a case PDF in; you get a one-page summary note in your course folder.").
   - **Why I'm suggesting it**: the evidence ("You asked me to summarise case readings 3 times in the past 2 weeks." or "You asked for it."). For a blueprint: the user's reason.
   - **What it will touch**: folders it reads and writes; tools it uses; for an MCP, that `config/mcp.selected.json` changes. Say clearly what it will **not** touch.
   - **Cost and risk**: usage (light / moderate / heavy for their plan), money (usually free), and the risk in one sentence.
   - **How to undo**: "Say `/remove-skill <name>`. It removes everything this added; your notes stay."
5. **Add the task:** `node system/scripts/tasks.mjs add "Approve or reject: <Title>" --tag propose --priority low --link "00_inbox/proposals/<YYYY-MM-DD> <Title>"`.
6. **Record it:** `node system/scripts/proposals.mjs mark <key> suggested --card "vault/00_inbox/proposals/<file>.md"` (key: the slug without `my-`).
7. **Ask in chat** (3–5 lines: what it does, why, risk, then the question). AskUserQuestion: Yes, build it now (recommended only if risk is low) / Not now (keep the card) / No thanks.
   - **Yes:** set the card `status: "approved"`, tick the task (`node system/scripts/tasks.mjs done "Approve or reject: <Title>"`), then run `/build` with the card path.
   - **Not now:** leave it open. "It's in your proposals; say 'build <Title>' any time."
   - **No thanks:** set `status: "rejected"`, tick the task, run `node system/scripts/proposals.mjs mark <key> rejected`. Don't suggest it again.

## Outputs

- `vault/00_inbox/proposals/<YYYY-MM-DD> <Title>.md` (a proposal card).
- A `#ab/propose` task in `vault/00_inbox/Tasks.md`.
- `state/proposals.json` updated (signals and outcomes) via `system/scripts/proposals.mjs`.

## Safety

- Never build, install or edit anything from this skill. Only the card, the task and `state/proposals.json`.
- Never propose changes to protected files: `system/**`, `.claude/settings.json`, `system/core.md`, the catalogue, or framework skills. If a need can only be met that way, say so and suggest `/update-alterbrain` or telling the Alterbrain maintainers.
  - One exception: the quarterly model check (`.claude/skills/health-check/references/model-check.md`) writes "Update model routing" cards. They may change only the `model:` and `effort:` lines of skills and agents, and `/health-check` applies them after approval, not `/build`.
- Proactive mode: at most one suggestion per session, never mid-task, never a rejected idea, never above `max_open_proposals`. See `references/proactive.md`.
- Evidence in cards and signals is described in plain words without other people's names or personal details.
- Don't oversell. If the gain is small, say so.
