---
skill_id: voice-routing
name: Voice Routing
description: "Pick the right writing voice for a task — which voice playbook applies, nk-writer invocation, brand-writer invocation, /mxm-voice-route. Lookup wrapper over the operator's voice selection authority."
version: 1.0.0
category: content
type: lookup
frameworks:
  - ADR-016 voice writing agent architecture
triggers:
  - "writing task arrives at any agent"
  - "agent needs to know which voice playbook applies"
  - "nk-writer agent invocation"
  - "{startup}-brand-writer agent invocation"
  - "/mxm-voice-route"
collaborates_with:
  - nk-writer
  - executive-router
  - brand-guardian
  - content-strategist
  - operator-profile
ethics_required: false
priority: high
tags: [voice, routing, content-classification, voice-selection, lookup, adr-016]
adr: ADR-016
created: 2026-05-19
updated: 2026-05-19
---

# Voice Routing

## Purpose

Callable lookup wrapper around `VOICE_SELECTION.md` (the operator's voice routing authority at `E:/Projects/nabeelkhan/myVoiceDNA/VOICE_SELECTION.md`). Any agent that needs to know "which voice playbook applies for this writing task" invokes this skill to get a deterministic routing decision.

This skill is the mechanical half of ADR-016. The judgment half lives in `nk-writer` (operator-voice content) and `{startup}-brand-writer` instances (startup-voice content). Both delegate to this skill for routing; this skill never produces content itself.

## Architecture (the non-negotiable invariant)

**This skill NEVER caches the routing table.** Every invocation reads `VOICE_SELECTION.md` fresh from disk.

Rationale: the operator owns `VOICE_SELECTION.md`. They update it as their voice system evolves (new content types, variant tweaks, crossover budget adjustments). If this skill cached the routing table in its own content, the cache would drift from reality — a Class 11 surface-claims-drift instance the moment the operator edits VOICE_SELECTION.md.

```
[Invoking agent]
        ↓
   [task description + optional content_type hint]
        ↓
[voice-routing skill]
        ↓
   1. Read VOICE_SELECTION.md FRESH (no cache)
   2. Classify task → one of 22 content types
        ↓ (if confidence ≥ threshold)        ↓ (if confidence < threshold)
   3a. Detect variant per row              3b. Return TOP-5 candidates ranked
        ↓                                       ↓
   4. Return load list + crossover         5. Invoking agent asks operator to pick
        budget + phrasebook section            then re-invokes this skill with content_type
```

## When To Invoke

- `nk-writer` agent activated by writing-verb trigger and needs to classify the task
- `{startup}-brand-writer` agent instance needs to know which playbook applies
- Any other agent (e.g., `reviewer`) wants to validate that a draft matches the expected playbook structure for its content type
- Operator runs `/mxm-voice-route <task description>` directly (debugging / scope confirmation)

## Input

```yaml
task_description: <free-text description of what the operator wants to produce>
content_type_hint: <optional — one of the 22 content types if already known>
target_length_hint: <optional — words or pages if known>
audience_hint: <optional — practitioners / strategic / engineers / general>
```

## Output (high-confidence path)

```yaml
voice_routing_decision:
  content_type: <one of the 22 — Blog post | LinkedIn article (thought-leadership) | LinkedIn post (assessment / findings) | Newsletter | Proposal | Case study | Conference / keynote | Twitter / X thread | YouTube video script | Email (internal) | Email (client) | Email (cold outreach) | Pitch deck (investor) | Pitch deck (sales) | Pitch deck (executive / board) | Book chapter | Research report | White paper | Executive summary | Client briefing | System design doc | Architecture doc | API reference | Governance doc | Tutorial | Internal memo | Status report (any cadence)>
  variant: <A | B | C | Daily | Weekly | Biweekly | Monthly | n/a>
  primary_voice: <Friendly Educator | Philosophical Architect | Technical Educator>
  crossover_budget: <None | FE 10% | PA 10% | TE 15% | PA 15% | TE 20% | PA 5% | TE 20% + FE 5% | PA 10% intro only | FE 20% | FE 15% in Exec Summary only>
  phrasebook_section: <III | IV | V | VI | VII | VIII | n/a>
  load_list:
    - core/shared-vocabulary.md
    - core/em-dash-prohibition.md
    - core/quality-standards.md
    - core/brand-identity.md
    - voices/<primary>/core-signature-patterns.md
    - voices/<secondary>/core-signature-patterns.md   # only if crossover
    - voices/<primary>/<content-type>-playbook.md
    - templates/crossover-phrasebook.md               # only if crossover
  estimated_load_tokens: <integer; MUST be ≤ 15,000>
  jargon_audit_required: <true | false per VOICE_SELECTION.md post-draft audit table>
  confidence: 🟢 HIGH | 🟡 MEDIUM
```

## Output (low-confidence path)

When the task description matches multiple content types ambiguously (Decision Tree in VOICE_SELECTION.md does not disambiguate), return the top 5 candidates ranked by fit and let the invoking agent surface them to the operator:

```yaml
voice_routing_ambiguous:
  reason: <one-line explanation of the ambiguity>
  candidates:
    - rank: 1
      content_type: <best fit>
      rationale: <one line — why this might fit>
      primary_voice: <FE | PA | TE>
    - rank: 2
      content_type: <next best>
      rationale: <one line>
      primary_voice: <FE | PA | TE>
    - rank: 3
      content_type: <third>
      rationale: <one line>
      primary_voice: <FE | PA | TE>
    - rank: 4
      content_type: <fourth>
      rationale: <one line>
      primary_voice: <FE | PA | TE>
    - rank: 5
      content_type: <fifth>
      rationale: <one line>
      primary_voice: <FE | PA | TE>
  next_action: "Surface these 5 to operator; on response, re-invoke voice-routing with content_type_hint=<chosen>"
  confidence: 🔴 LOW
```

## Classification heuristics (the inputs to ranking)

The skill weighs these signals against each row of the 22-content-type table in VOICE_SELECTION.md:

| Signal | Weight | Source |
|---|---|---|
| Explicit content-type verb (blog, post, email, deck, memo, report, etc.) | high | task_description |
| Audience descriptor (client, investor, board, internal team, engineers, regulators) | high | audience_hint or inferred |
| Length target (under 200 words → likely email/post; 1000+ words → likely blog/report/deck) | medium | target_length_hint or inferred |
| Distribution channel (LinkedIn, Twitter, YouTube, internal Slack, email) | high | task_description |
| Decision Tree section match in VOICE_SELECTION.md | high | direct lookup |
| Variant selector keywords (thought-leadership vs assessment; investor vs sales vs board) | medium | task_description + variant selector rules |

When two or more rows tie within a small margin, return ambiguous.

## Anti-patterns (forbidden)

1. **Caching the routing table in this skill's content.** Always read VOICE_SELECTION.md fresh.
2. **Returning a load list that exceeds 15,000 tokens.** If estimated tokens > 15K, the routing is wrong — re-classify or surface ambiguity.
3. **Inferring a content type that is not in VOICE_SELECTION.md's 22 rows.** If the task fits none of the 22 (e.g., a press release, a job description, a contract), do not improvise — return:
   ```yaml
   voice_routing_no_match:
     reason: <which row the operator would need to add>
     next_action: "Operator must extend VOICE_SELECTION.md with a new row; do not write content in an undefined voice configuration."
     confidence: 🔴 LOW
   ```
4. **Loading both `voices/friendly-educator/*` and `voices/philosophical-architect/*` core-signature-patterns WITHOUT loading `templates/crossover-phrasebook.md`.** Crossover requires the phrasebook; loading two voice cores without it produces voice whiplash.

## Edge cases

- **VOICE_SELECTION.md missing or unreadable.** Fail loud: return `voice_routing_error: { reason: "VOICE_SELECTION.md not found at expected path", action: "Halt task; alert operator." }`. Confidence 🔴 LOW. Do not attempt to write in a guessed voice.
- **VOICE_SELECTION.md present but malformed (table parse failure).** Fail loud with the parse error and the line number. Do not fall back to embedded routing.
- **content_type_hint passed but does not match any of the 22 rows.** Treat as no-match (anti-pattern #3) — operator likely typo'd a content type.
- **Operator explicitly overrides voice ("write this blog post in Technical Educator voice").** Honor the override AND log an audit-trail event noting the divergence from VOICE_SELECTION.md's routing default for that content type. The operator owns the override authority; the skill flags it for transparency.

## Behavioral framing

- **Fogg Behavior Model:** Motivation = correct voice routing on every task; Ability = mechanical lookup that any agent can invoke; Prompt = invoked automatically by nk-writer + brand-writer agents.
- **COM-B:** Capability = the 22-row routing table in VOICE_SELECTION.md; Opportunity = filesystem access to operator's myVoiceDNA folder; Motivation = operator wants every output in their voice without per-task prompting.
- **Confidence tagging:** 🟢 HIGH when single-row match + variant detected + load tokens ≤ 15K. 🟡 MEDIUM when row matched but variant required operator input. 🔴 LOW when ambiguous / no-match / file error.

## Source references

- `E:/Projects/nabeelkhan/myVoiceDNA/VOICE_SELECTION.md` (v1.0, 2026-05-19) — the routing authority
- `E:/Projects/nabeelkhan/myVoiceDNA/core/*` — universal rules loaded by every routing decision
- `E:/Projects/nabeelkhan/myVoiceDNA/voices/{friendly-educator,philosophical-architect,technical-educator}/*` — voice-specific signature patterns + playbooks
- `E:/Projects/nabeelkhan/myVoiceDNA/templates/crossover-phrasebook.md` — transition templates for crossover content
- ADR-016 Voice Writing Agent Architecture
- `agents/MXM/cmo/nk-writer.md` — primary consumer of this skill
- `agents/MXM/cmo/_template-brand-writer.md` — template for per-startup writer instances

---
_Copyright (c) 2026 iSystematic Inc. Maxim product. BSL 1.1. Ratified by ADR-016._
