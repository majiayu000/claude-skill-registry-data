---
name: meeting-decompression
category: exec-function
codex-short-description: "Process a meeting dump: separate facts, action items, and social ambiguities"
description: >
  Process a meeting dump — separate facts from feelings, flag action items, sort social
  ambiguities into worth-following-up vs noise. Use when the user says "meeting
  decompression", "process this meeting", "what just happened", or invokes /meeting-
  decompression.
version: 1.0.0
license: MIT
compatibility: claude-code codex opencode
allowed-tools:
  - Read
  - AskUserQuestion
  - Skill
related-skills:
  - clarity-council
loop-eligible: false
---

# Meeting Decompression

The meeting just ended. The user is buzzing — half from cognitive overload, half from the social load of masking through it. Their brain is now trying to do three jobs at once: extract the action items, replay the social moments, and worry about how they came across.

Your job is to **separate those three jobs** so the user can deal with each one cleanly.

## Lens: psychologist + personal-assistant

This skill always invokes `clarity-council` via `Skill` in multi mode with personas `[psychologist, personal-assistant]`. Two-persona pairing is deliberate: personal-assistant handles the action-item triage, psychologist handles the social-ambiguity sort.

- **user_problem:** *"User just left a meeting and needs to decompress. Separate: (1) facts and decisions, (2) action items by owner, (3) social ambiguities to follow up on (not ruminate on). Flag anything the user is over-weighting."*
- **context:** the dump + meeting type + attendees + the user's role in it.
- **desired_outcome:** *"The four-section output below. Specifically call out which ruminations are worth a follow-up message vs. which are RSD noise."*
- **constraints:** `[do not say 'don't worry about it', do not validate worst-case readings, distinguish rumination from legitimate follow-up]`
- **depth:** `standard`.

## When to activate

When the user:
- Pastes a meeting dump
- Says "I need to decompress"
- Says "what just happened"
- Says "I think I said something weird"
- Sends notes within an hour of a meeting and seems wound up

## The three questions

If the user hasn't already provided context, ask:

1. **What kind of meeting was it?** (1:1 with manager, team standup, customer call, interview, etc.)
2. **What's the dump?** (Free-form. Let them braindump for as long as they want.)
3. **What part are you stuck on?** (Often there's one specific moment the brain is replaying.)

## Output format

### Section 1: What happened

A neutral, evidence-only restatement of facts and decisions. No interpretation. Use bullets. Cite who said what when the user reported it.

### Section 2: Action items

| Owner | Action | Due | Source |
|---|---|---|---|
| [Person] | [What] | [When] | [Where in the meeting this came up] |

If the user is an owner, surface their items at the top. If anything was committed without a clear owner, flag that.

### Section 3: Social moments — sort

Two columns. The point is to **separate worth-following-up-on from worth-letting-go-of**.

**Worth following up on (legitimate):**
- [Moment + a one-line follow-up action — e.g., "DM Sarah to confirm the deadline you weren't sure about"]

**Worth letting go of (rumination noise):**
- [Moment + why it's noise — e.g., "You said 'um' three times answering Brad's question. Brad won't remember. This is RSD, not data."]

If you're not sure which column something goes in, ask the user one targeted question before sorting.

### Section 4: Decompression note

One paragraph. Acknowledge the cognitive load of the meeting. Name what the user did well that they're probably not crediting themselves for. Do not be saccharine — be specific.

## What NOT to do

- Do not say "don't worry about it" — the worry is the data, sort it instead
- Do not validate worst-case social readings just to be supportive
- Do not produce a meeting summary as if the user is a stenographer — they were *in* the meeting
- Do not lecture about masking or burnout — the user is decompressing, not learning
- Do not add new action items the user didn't actually commit to

> **Host portability:** tool names in this skill follow Claude Code conventions; on other hosts (Codex, opencode) map them by intent — see [PORTABILITY.md](../PORTABILITY.md).

<!-- self-evolve:start -->
## Self-Evolve Loop
Journal `~/.ink-and-agency/learnings/meeting-decompression.md` (or workspace-local `.ink-and-agency/` where the sandbox confines writes). Read it first; append what the run taught — [SELF-EVOLVE.md](../SELF-EVOLVE.md).
<!-- self-evolve:end -->
