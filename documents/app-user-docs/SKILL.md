---
name: app-user-docs
description: Generate comprehensive user perspective documentation for any app by running a two-phase subagent workflow — Phase 1 surveys the codebase and produces a structured inventory, Phase 2 writes the final document from that inventory. Use this skill whenever the user wants to document what their app does from a user's point of view, create a user manual, produce operational reference docs, or capture what features exist and which are complete vs incomplete. Triggers on phrases like "document my app", "create a user manual", "write docs for my app", "what does my app do", "generate a user guide", or any request to produce human-readable documentation of an application's functionality. Also triggers when the user wants to understand the current state of their app's features before handing it off, writing a README, or building on top of it.
---

# App User Docs Skill

Generates a comprehensive user-perspective document for any application using a two-phase subagent workflow. The output is an honest, exhaustive markdown document written from the user's point of view — not developer docs, not a technical spec.

---

## Step 1: Fill Out the App Profile

Before spawning any subagents, confirm or fill in this profile. Extract what you can from the conversation context — only ask the user about genuine gaps.

```
APP PROFILE
-----------
App name:
One-line description:
App type: [voice-first | standard-web | iot-embedded | hub-integrations | mixed]
Primary interface: [voice | click-based | both | physical/sensor]
Known integrations (external systems):
Core workflow or pipeline (if any):
Known incomplete features (if any):
Who is this doc for: [personal reference | handoff | contractor docs | formal manual]
Tone: [operational/blunt | professional | beginner-friendly]
```

App type determines which variant instructions Phase 2 uses. See `references/app-type-variants.md`.

---

## Step 2: Phase 1 — Codebase Surveyor Subagent

Spawn a subagent with the Phase 1 prompt from `references/phase1-surveyor.md`.

Inject the completed App Profile at the top of the prompt before dispatching.

**Phase 1 output is a raw structured inventory — no prose, no interpretation.** It produces:
- All UI panels/screens found, with file references
- All user-facing actions (clicks, inputs, triggers)
- All voice command handlers (if app type is voice-first or mixed)
- All integration adapters and what they connect to
- All data flows (in and out)
- All TODOs, stubs, feature flags, and incomplete implementations
- File path references for every item found

**Before proceeding to Phase 2**, present the inventory to the user and ask:
> "Does this inventory look complete? Any areas that seem thin or missing?"

If the user identifies gaps, re-run Phase 1 with targeted directory hints before continuing.

---

## Step 3: Phase 2 — Document Writer Subagent

Spawn a subagent with the Phase 2 prompt from `references/phase2-writer.md`.

Inject at the top:
1. The completed App Profile
2. The full Phase 1 inventory output
3. The relevant app-type variant section from `references/app-type-variants.md`

**Phase 2 output is the final user-perspective markdown document.**

---

## Step 4: Deliver

Present the markdown document to the user. Ask:
> "Does this capture everything accurately? Any sections that need more depth or correction?"

Iterate on specific sections as needed — no need to re-run the full workflow for minor corrections.

---

## Status Flags

Use these consistently throughout all generated documents:
- ✅ Working — confirmed connected and functional
- ⚠️ Partial — exists but incomplete or intermittently functional
- ❌ Not connected — UI exists but no live backend/integration
- ❓ Unconfirmed — found in code but UI state unknown

---

## Reference Files

Read these when needed — do not load all of them upfront:

| File | When to read |
|------|-------------|
| `references/phase1-surveyor.md` | When ready to dispatch Phase 1 subagent |
| `references/phase2-writer.md` | When ready to dispatch Phase 2 subagent |
| `references/app-type-variants.md` | When preparing Phase 2 prompt — inject relevant variant section only |
