---
name: planner
description: Full Planner Gate procedure for spec agents. Use when writing or reviewing a spec.
---

# PLANNER GATE (Spec Agents - MANDATORY)

**Every spec agent must pass this gate before a spec is marked "ready." No exceptions.**

This gate exists because agents hallucinate specs. They skim 3 files, make assumptions about the rest, and write confident-sounding plans that break during implementation. This gate forces evidence-based planning.

**Canonical launcher prompts live in `docs/specs/README.md`.** The top-level `prompts/` tree is a prompt library and queue, not the source of truth for planner, builder, or research launcher prompts.

## Step 1: Load Context

1. **Read `CLAUDE.md`** cover to cover.
2. **Read `docs/specs/_TEMPLATE.md`** for the required spec format.
3. **Read `docs/session-log.md`** (last 5 entries) and `docs/build-state.md`.
4. **Look up affected pages in `docs/app-complete-audit.md`** so you know what you're touching.

## Step 2: Deep Inspection

1. **Scope the inspection** - read every file in the directories this feature touches. Follow import chains 2 levels deep from the entry point. Read the schema for every table this feature queries. Do NOT claim you "inspected the codebase" after reading 3 files.
2. **Produce a current-state summary** - before writing the spec, output a plain-English summary of what exists today in the areas this feature touches. Include file paths, current behavior, and data flow. **This summary is for the developer to review.** If they spot errors, the spec hasn't been started yet, so nothing is wasted. This is the single highest-ROI human checkpoint.

## Step 3: Capture Developer Notes (CRITICAL)

**The developer's conversation IS the spec's origin. Preserve it.**

During the conversation with the developer, you MUST capture their words and intent into the spec's `## Developer Notes` section. This is not optional. The developer is often working in voice-to-text mode, pouring out high-signal context that will be lost forever if you don't capture it.

Capture two things:

1. **Raw Signal** - the developer's actual words, cleaned up for readability but faithful to what they said. Remove filler and repetition, keep the passion and reasoning. This is the "why behind the why."
2. **Developer Intent** - translate their words into clear system-level requirements, constraints, and behaviors. What were they actually trying to achieve beneath what they said?

A spec without Developer Notes is incomplete. A builder reading a spec without Developer Notes is building blind.

## Step 4: Write the Spec

Use `docs/specs/_TEMPLATE.md`. Fill in every section. The spec must include:

- **Timeline table** with creation timestamp
- **Developer Notes** section (from Step 3)
- All technical sections per the template

## Step 5: Spec Validation (Evidence Required)

Answer every item below. **Each answer must cite specific file paths and line numbers you read.** If you cannot cite a file, you did not verify it.

1. **What exists today that this touches?** Files, routes, schemas, components, server actions. Cite line numbers.
2. **What exactly changes?** Add / modify / remove at the file + data level. Be surgical.
3. **What assumptions are you making?** For each: verified (you read the code) or unverified (you're guessing)? If unverified, verify it now or flag it.
4. **Where will this most likely break?** Top 2-3 failure points with reasoning.
5. **What is underspecified?** What could cause a builder to guess? Eliminate it or flag it.
6. **What dependencies or prerequisites exist?** Migrations, other specs, config changes.
7. **What existing logic could this conflict with?** Shared components, shared server actions, shared DB tables.
8. **What is the end-to-end data flow?** User action -> server action -> DB write -> UI update. No gaps.
9. **What is the correct implementation order?** Migration first? Schema first? Component first? Be explicit.
10. **What are the exact success criteria?** These become the builder's verification steps.
11. **What are the non-negotiable constraints?** Auth, tenant scoping, privacy boundary, financial rules.
12. **What should NOT be touched?** Explicitly fence off adjacent code.
13. **Is this the simplest complete version?** If not, cut scope now.
14. **If implemented exactly as written, what would still be wrong?** Be honest.

## Final Check (Must Answer Explicitly)

> Is this spec production-ready, or am I proceeding with uncertainty?
> If uncertain: where specifically, and what would resolve it?

If uncertain on anything that affects correctness, the spec is NOT ready. Resolve it or flag it for the developer.

**Self-enforcement:** You must run Spec Validation and Final Check ON YOUR OWN before telling the developer the spec is ready. If you say "ready" without cited evidence for every question, you have failed the gate.
