---
name: dev-research
description: >
  Use this skill whenever the user needs help choosing between programming technologies,
  libraries, frameworks, tools, patterns, or architectural approaches. Covers all
  programming domains. Trigger even if the user doesn't say "suggest" explicitly —
  any programming decision where options exist and verification matters should use this skill.
---

# Dev Research

Research-backed programming recommendations with verified references.

## Principles

- Official documentation is the source of truth.
- Never recommend what you haven't verified via `web_search` and `web_fetch`.
- Every final recommendation needs an exact reference the user can check.

## Workflow

### Step 1: Present Options

Present up to 3 options using `ask_user_input` (single-select). Fewer is fine — never pad with weak options.

For each option, include in the text:
- One sentence: what it is.
- Up to 2 pros, up to 2 cons.

If the question has only one credible answer, skip to Step 2. If too vague, ask one clarifying question first.

### Step 2: Research

After user selects, search before responding. Use `web_search` + `web_fetch` to:
- Read official docs (getting started, API reference, relevant sections).
- Confirm latest stable version and active maintenance status.
- Find migration guides, known issues, or compatibility notes relevant to the user's case.

### Step 3: Detailed Explanation

Based on research findings, present:
- What it is and how it works in the user's context.
- Full pros/cons (beyond the initial 2 — include performance, ecosystem, learning curve, community, maintenance).
- When it fits and when it doesn't.
- Brief comparison to the other Step 1 options.

Cite specific doc pages for claims. Ask the user if they want to proceed.

### Step 4: Verification

When user commits, verify before giving implementation guidance:

1. **Availability** — Confirm the package exists on its registry (npm, PyPI, crates.io, etc.) and the needed version is stable.
2. **Modern standard** — Check official docs for deprecation notices or "use X instead" guidance.
3. **Correctness** — Verify API signatures, config options, and patterns against current docs.

**On failure:** Tell user what's wrong, show the source, suggest the correct alternative, restart from Step 2.

**On success:** Provide:
- Exact doc page links confirming the recommendation.
- Section pinpointing — for large docs, state the exact location (e.g., "Next.js docs > Routing > App Router > Layouts, section 'Root Layout'").
- Version verified against.

Then provide implementation guidance or code examples.

## Edge Cases

- **Deprecated technology discovered:** Inform user directly, restart with corrected options.
- **Official docs unavailable:** State this explicitly. Fall back to GitHub repo, RFCs, or well-known community sources — label them as non-official.