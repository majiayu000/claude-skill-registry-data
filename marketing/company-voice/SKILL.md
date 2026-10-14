---
name: company-voice
description: Build, store, maintain, and apply a company's editorial voice and content strategy as a persistent plain-file knowledge system. Use when Codex is asked to discover an organization, define positioning or content strategy, create or update a brand/editorial voice memory, generate company content from stored voice rules, review content for voice and claim safety, manage a content backlog, or evolve publishing/performance rules over time.
---

# Company Voice

Use this skill to prevent generic content generation. Establish or load an editorial memory before writing for a company, founder, consultancy, product business, creator, agency, or organization.

## Operating Rules

- Do not generate posts immediately when no editorial memory exists.
- Start with an adaptive interview, then create a focused editorial memory.
- Treat confirmed, inferred, provisional, and unresolved decisions differently.
- Never silently promote an inference into a confirmed rule.
- Load only the smallest relevant set of files for the current task.
- Update only affected files when the editorial system changes.
- Keep campaign, backlog, publishing, and performance records separate from permanent voice rules.

Default memory root: `.editorial-voice/` in the active workspace, unless the user names another location.

## Workflow Router

1. **No editorial memory exists or the user asks to define voice/content strategy**: read `references/discovery-interview.md`, `references/storage-model.md`, and `references/foundation-workflow.md`. Read `references/strategy-frameworks.md` when audience, customer need, marketing mix, positioning, identity, motivation, persuasion, or content-program decisions remain weak. Interview first.
2. **The user asks to generate content**: inspect `.editorial-voice/00-index.md`, read `references/content-workflow.md`, then load only the target audience, voice, claim, format, channel, CTA, product, search, or metric files required by the plan. Load `references/strategy-frameworks.md` only when a missing decision requires a defensible lens; do not stack frameworks onto settled rules.
3. **The user asks to change the voice, audience, product, pillars, metrics, CTAs, channels, or constraints**: read `references/modification-workflow.md` and `.editorial-voice/00-index.md`, then inspect affected files and relationship links.
4. **The user asks for search strategy, topic backlog, publishing sequence, or performance review**: read `references/content-workflow.md`, then load the relevant strategy, content, channel, publishing, and metrics files.
5. **The user asks how the repository works or wants examples**: read the relevant files under `references/example-editorial-memory/` and `references/example-interactions.md`.

## Discovery First

Begin with the highest-value questions, not a full questionnaire. Ask enough to understand:

- what the organization does, why it exists, and who it serves
- how it differs from alternatives and how it wants to be perceived
- what content should achieve, where it will be published, and how success is measured
- what the organization can credibly claim and what it should avoid
- how voice, tone, technical depth, opinion, evidence, humor, story, and promotion should behave
- what products, services, pages, repositories, resources, or offers content may reference

Let the user skip, defer, or mark answers as provisional. Ask targeted follow-ups for gaps, contradictions, or decisions that materially affect content quality. Stop when enough information exists to create a reliable foundation.

## Editorial Memory Model

Create a plain-file editorial memory with focused files, subdirectory indexes, and explicit links. Use stable IDs for decisions and relationships.

Each decision file should include narrow content only. Prefer this shape:

```markdown
---
id: voice.primary
status: confirmed
source: user-interview
updated: 2026-07-11
depends_on:
  - positioning.primary
affects:
  - style.sentence-rhythm
---

# Primary Voice

...
```

Use these statuses:

- `confirmed`: directly approved by the user or explicitly accepted after review
- `inferred`: reasoned from other confirmed information, but not confirmed
- `provisional`: usable for now, expected to change
- `unresolved`: open question or conflict that should not be treated as a rule
- `retired`: superseded decision that should not influence generation

Use `relations/links.yaml` for cross-file relationships that matter during routing or updates. Keep links readable and sparse.

Run `scripts/validate_editorial_memory.py <memory-root>` after creating or modifying a memory when Python is available.

## Content Generation

Before writing, produce a short plan that identifies topic, audience, reader problem, purpose, content pillar, central idea, organization perspective, evidence, claims needing verification, technical depth, tone, format, CTA, relevant product/resource, primary metric, and search theme where relevant.

Ask for clarification only when a missing decision materially affects quality, accuracy, or risk. Otherwise use confirmed stored decisions, call out relevant provisional/inferred choices, and proceed.

Post structures are reasoning frameworks, not templates. Choose the structure that fits the topic, channel, audience, and goal. Avoid repeating the same opening pattern across posts.

Review every generated post against the smallest relevant rule subset. Fix blocking issues before presenting final content. Separate:

- blocking issues
- recommended improvements
- optional stylistic changes

## Updating The System

When the user requests a change:

1. Identify affected decisions and files.
2. Inspect dependent files and semantic links.
3. Explain meaningful conflicts or downstream effects.
4. Update only necessary files.
5. Preserve unrelated decisions.
6. Update indexes and links.
7. Record the change in `decisions/change-history.md`.
8. Validate consistency.

Do not rewrite the whole editorial memory for a small change.

## References

- `references/discovery-interview.md`: adaptive interview workflow and decision status handling.
- `references/storage-model.md`: file structure, indexes, metadata, and semantic links.
- `references/foundation-workflow.md`: converting interview answers into durable editorial foundation files.
- `references/content-workflow.md`: planning, generation, review, search, backlog, publishing, and performance.
- `references/strategy-frameworks.md`: selective market, customer, positioning, brand, motivation, persuasion, behavioural-choice, content-strategy, and writing frameworks with evidence and misuse guidance.
- `references/modification-workflow.md`: safe updates, dependency handling, conflict resolution, and change history.
- `references/example-editorial-memory/`: compact example memory with focused files and links.
- `references/example-interactions.md`: example agent interactions for discovery, generation, and modification.

## Creator

Created for and maintained by [Brownsmith Dynamics](https://brownsmithdynamics.com).
