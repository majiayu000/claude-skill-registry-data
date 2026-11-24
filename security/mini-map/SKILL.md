---
name: mini-map
description: Condense an existing dungeon-crawl-threat-map artifact (THREAT_MODEL.md) into a hard-capped, ~50-line MINI_MAP.md that other skills can load as quick background context, application overview, business logic invariants, and security mechanisms (auth, SSO, session handling, secrets, crypto), without pulling in the whole threat model. Trigger this whenever the user asks to "build app context," "give [a skill] context on this app," "condense the threat model," "generate a mini map," "summarize the security posture for later use," or wants quick context before reviewing a finding or planning a remediation. If no THREAT_MODEL.md exists yet, this skill prompts to generate one first, it doesn't fabricate context from scratch.
---

# Mini-Map

## Why this skill exists

[`dungeon-crawl-threat-map`](../dungeon-crawl-threat-map) produces a report meant to be read once, in full, by a person: architecture diagram, full STRIDE walkthrough, OWASP mapping, glossary. That's the right shape for onboarding or a wiki page. It's the wrong shape to reload every time a different skill needs a quick reminder of how this app authenticates users or what its core business rules are, for example when [`player-two-verdict`](../player-two-verdict) is judging whether a finding is exploitable, or when remediating a vulnerability and needing to know what a fix has to preserve.

This skill takes an already-generated threat model and distills it down to a fixed, ~50-line file: enough to understand the system and how it's protected, not enough to need real reading time. It doesn't re-scan the codebase, it condenses a report that already exists.

## When to use this

- The user wants a compact, reusable context file for other skills to load before reasoning about a specific finding or fix.
- The user asks to "condense," "summarize," or "shrink" an existing threat model.
- Another workflow (finding review, remediation) needs quick answers to "how does auth work here" or "what are this app's core business rules" without reading the full threat model.

If no threat model exists yet, this skill's job is to get one made first (Step 0), not to improvise context from a partial look at the repo.

## Step 0: Prerequisite check

Look for `.SEC-Arcade-save_states/THREAT_MODEL.md` in the target repo (or the path the user names). This is the only source of truth this skill condenses, don't fabricate context from a partial scan of the repo if it's missing.

If it doesn't exist, ask with `AskUserQuestion`, two options:

1. **Run dungeon-crawl-threat-map now** (recommended) - if chosen, follow [`dungeon-crawl-threat-map`](../dungeon-crawl-threat-map)'s own `SKILL.md` in full, including its own save step, to produce `THREAT_MODEL.md`, then continue to Step 1.
2. **I'll generate it myself later** - stop here, don't proceed with a thin or guessed context file.

## Step 1: Read the full threat model

Read `THREAT_MODEL.md` in full before condensing anything.

## Step 2: Condense into the fixed structure

Pull from specific sections of the source, don't re-derive anything from the repo directly:

- **Overview**: from the source's "What this does" section.
- **Identity & Session**: from "Worth a Second Look" → Authentication, plus any Spoofing/Tampering STRIDE entries at an auth boundary. Cover auth method/provider (including SSO if present), the authorization model and whether it's enforced at every access point or just the first, session/token lifecycle if anything was flagged (expiration, invalidation, fail-open behavior), and any flagged IDOR-prone pattern.
- **App Hardening**: from "Worth a Second Look" → Cryptography and Other. Cover secrets handling (including any flagged leakage into logs, errors, or client bundles), crypto usage notes, and dangerous defaults or exposed debug/admin endpoints if flagged.
- **Trust Boundaries & Data Flow**: from the source's Architecture section. Where data crosses a boundary, and where untrusted input enters (API, upload, webhook, queue, CLI) and reaches a sink without validation.
- **Business Logic Invariants**: from "Worth a Second Look" → Business Logic Abuse. Abuse-relevant workflows only, race conditions, workflow-bypass risk, parameter manipulation, tenant isolation, not a generic feature or domain description. Omit this section entirely if the source has nothing here, don't invent generic business-logic content to fill it.
- **Known Risk Areas**: from "Prioritized actions," highest risk first. Also the catch-all for lower-frequency flags (webhook/SSRF issues, logging leaks) that don't merit their own section, only if the source actually flagged something there.

No citations needed, this is a summary artifact for machine consumption, not an evidence-cited report.

If `THREAT_MODEL.md` doesn't have the expected section headers (hand-edited, or produced by something other than `dungeon-crawl-threat-map`), don't fail silently and don't guess. Condense whatever sections do exist using the same mapping logic, note in the Overview which of the six target sections had no matching source material, and skip that target section rather than inventing content for it.

## Step 3: Enforce the 50-line cap

Count lines in the draft, including headers and blank lines. If over 50, trim in this order, stop as soon as it fits:

1. Known Risk Areas (cut lowest-priority bullets first)
2. Business Logic Invariants
3. Trust Boundaries & Data Flow (reduce bullet count, keep the highest-value ones)

Never trim Overview, Identity & Session, or App Hardening, those are what a fix or false-positive review needs most.

## Step 4: Check for sibling artifacts

Look in the same `.SEC-Arcade-save_states/` folder for `CARTRIDGE_SCAN.md` and `DEAD_WEIGHT_REPORT.md`. If present, reference their paths in the Pointers section for dependency/supply-chain and container depth, don't duplicate their content here.

## Step 5: Write the file

Write directly to `.SEC-Arcade-save_states/MINI_MAP.md` in the target repo, overwriting any existing one. **Do not ask first.** This is a deliberate exception to the general save convention in `${CLAUDE_PLUGIN_ROOT}/references/save-states.md`: that convention exists because a full report is something a human decides whether to keep, this file exists purely as ambient, machine-readable context for other skills to load, prompting every run would just be friction against its own purpose.

Use this structure:

```
# Mini-Map: [app/repo name]

_Condensed from `.SEC-Arcade-save_states/THREAT_MODEL.md`, generated [date], target repo at commit [short-sha or "not a git repo"]._

## Overview
[1-3 lines]

## Identity & Session
- Auth: [method/provider, incl. SSO if present]
- Authorization: [model, enforced at every access point or just the first]
- Session/tokens: [lifecycle notes, only if flagged]

## App Hardening
- Secrets: [handling, incl. any flagged leakage]
- Crypto: [notable usage, if any]
- Notable defaults: [only if flagged]

## Trust Boundaries & Data Flow
- [boundary or untrusted-input-to-sink bullet]

## Business Logic Invariants
[omit entirely if the source has nothing here]
- [abuse-relevant workflow bullet]

## Known Risk Areas
- [highest risk first]

## Full Reports
`.SEC-Arcade-save_states/THREAT_MODEL.md`[, plus CARTRIDGE_SCAN.md / DEAD_WEIGHT_REPORT.md if present]
```

## Step 6: Confirm to the user

Tell the user the file was written and give the path. Since the file is short by design, show it in full in the chat rather than a truncated preview.

## Voice and format

- No em dashes.
- Plain and terse, the opposite of `dungeon-crawl-threat-map`'s teaching tone. Brevity is the entire point of this skill.
- Omit a section rather than padding it with generic filler to look complete.

## Reference material

- `${CLAUDE_PLUGIN_ROOT}/references/save-states.md`: the shared save-to-file convention this skill deliberately bypasses at Step 5, still the source of truth for the `.SEC-Arcade-save_states/` folder location and naming pattern.
