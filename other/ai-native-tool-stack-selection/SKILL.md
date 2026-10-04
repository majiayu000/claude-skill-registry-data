---
name: ai-native-tool-stack-selection
description: "Selects the smallest workable AI-native tool stack using a 12-category decision tree (thinking partner, research, design, app builder, coding agent, hosting, backend, skills, project management, notes, automation, agent building) — category-based, not tied to product names."
---

# AI-Native Tool Stack Selection

## Purpose

Help a pre-startup founder or small team choose the smallest workable
AI-native tool stack without drowning in a market of hundreds of tools.
This skill structures the choice around categories — not product names
— because categories (what purpose you need the tool for) hold up over
time, while individual products and their features go stale quickly in
this market.

## Based on

- The owner's AI-native Business Design workshop
  (the owner's own workshop), `tools.md` — "2026 AI-Native Stack": a
  12-category breakdown organized by *what you're trying to do*, not by
  vendor; the "minimum viable stack" principle ("3–6 tools, not 30"); the
  three-tier maturity path for agent tools (no-code platforms → open-
  source runtimes → developer frameworks).
- See `../../references/tool-category-map.md` (12 categories with
  examples, a time-stamped snapshot) and
  `../../references/workshop-source.md`.

## Method

1. **Go through the 12 categories** (see
   `../../references/tool-category-map.md`) and identify which are
   necessary for YOUR own case right now — not all of them at once:
   1. AI thinking partner (general chat/project AI)
   2. Research and information retrieval
   3. Design sketching
   4. App builder (prompt → working app)
   5. Coding agent (when moving from prototype to production)
   6. Version control / code storage
   7. Hosting and deployment
   8. Backend and database
   9. Skills (packaging and reusing agent capabilities)
   10. Project management
   11. Meeting/note-taking tool (turning conversations into
       machine-readable text)
   12. Workflow automation and agent building
2. **Choose one default tool for each necessary category.** Resist the
   urge to use multiple tools in the same category simultaneously — it
   fragments context and slows things down instead of speeding them up.
3. **Apply the minimum-stack rule of thumb.** A typical working
   pre-startup stack is 3–6 tools, not 30. Start with the minimum:
   thinking partner + research + design sketch + app builder + code
   storage. Add categories only once a genuine need arises, not
   proactively.
4. **As the team or need grows:** add project management and a meeting
   notes tool only once multiple people are working on the same thing
   regularly — not right at the start.
5. **Once the first workflow has proven valuable and is genuinely
   closed-loop in shape** (see
   `../closed-loop-process-and-human-oversight-design/SKILL.md`):
   consider wrapping it as an agent. Start with a no-code agent platform;
   move to an open-source runtime or a developer framework only once
   technical skill and genuine need require it — not by default.
6. **Check lock-in before committing.** What infrastructure (database,
   hosting) does the tool tie you to, and can code/data be exported if
   needed? For a prototype this often doesn't matter much; for a product
   meant to scale, it matters a lot.
7. **Remember this is a snapshot.** Tool lists, pricing, and free tiers
   change weekly in this market. Always check a tool's current status
   before committing — don't treat the named examples in
   `../../references/tool-category-map.md` as an up-to-date truth.

## Gotchas

- Adopting two tools in the same category "just to compare" is
  explicitly against step 2's rule of thumb — it fragments context and
  slows things down rather than speeding them up, even though it feels
  like hedging risk.
- Adding project management or meeting-notes tooling before multiple
  people are actually working on the same thing regularly (step 4) is
  premature scaffolding for a stack that's supposed to start at 3-6
  tools, not 30.
- The named tools in `../../references/tool-category-map.md` are a
  time-stamped snapshot, not a current recommendation — step 7 warns
  that pricing, features, and free tiers in this market shift weekly,
  so re-verify a tool's status before committing rather than trusting
  the reference file as-is.
- Jumping straight to an open-source runtime or developer framework
  (LangGraph, CrewAI, etc.) for agent-building skips the required
  progression in step 5: start with a no-code platform, and only move
  up once a workflow has proven genuinely closed-loop-shaped and real
  technical need exists — not by default enthusiasm.
- Skipping the lock-in check (step 6) is low-risk for a throwaway
  prototype but becomes a real liability if the product is meant to
  scale — the skill only flags this as optional for prototypes, not for
  anything intended to grow past MVP.

## What this skill does NOT do

- Does not recommend specific product names as a permanent truth —
  categories and the selection principle hold up, individual products go
  stale quickly (see the timestamp in
  `../../references/tool-category-map.md`).
- Does not perform technical due diligence on a tool's security,
  contract terms, or the safety of skills/agents — check that
  separately before business-critical use; install skills/agents only
  from trusted sources.
- Does not assess which developer framework (LangGraph, CrewAI, Claude
  Agent SDK, etc.) a dev team should choose for production code — that's
  the dev team's decision; this skill only gives the founder context on
  what's involved before that conversation.

## Continue from here

- Related skill in this pack: `../ai-buildable-prd-writing/SKILL.md`
  (who the PRD is handed to for building),
  `../closed-loop-process-and-human-oversight-design/SKILL.md` (when it
  makes sense to move to agents).
- Related skill in another pack:
  `../../../../ai-strategy-and-governance/skills/build-vs-buy-vs-partner-ai/SKILL.md`
  — a larger-scale build/buy/partner decision; this skill is a
  lighter, tactical choice for the pre-startup stage.
- The pack's shared guardrails: `../../CLAUDE.md`

## References

- `../../references/tool-category-map.md` — 12 categories with examples
  (a time-stamped snapshot)
- `../../references/workshop-source.md` — source information
- `../../CLAUDE.md` — the pack's shared guardrails
