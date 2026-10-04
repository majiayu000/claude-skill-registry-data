---
name: skill-generation-expert
description: Ingests external documentation, repository patterns, or best practices and translates them into a formalized Antigravity skill. Use when asked to learn from a link, use when asked to create a new skill, use when generalizing a specific solution into a global capability.
version: "1.0"
verified_date: 2026-05-30
category: core
---

# Skill Generation Expert

## Purpose

Empowers Antigravity to learn dynamically by analyzing raw documentation, URLs, or repository best practices and distilling them into a permanent, reusable skill in the global OS kernel.

## When to Use This Skill

- Use when the user provides a link and says "learn this" or "make a skill out of this".
- Use when requested to generalize a local project pattern into a global Antigravity capability.
- Use when asked to create a new skill from scratch based on a provided description.
- Do NOT use for regular code generation or feature implementation.

---

## Phase 1: Ingestion and Analysis

- **Read Context:** Use the `read_url_content`, `search_web`, or file reading tools to deeply analyze the provided URLs, documentation, or codebase patterns.
- **Identify Core Principles:** Distill the raw information into actionable rules, constraints, and step-by-step processes. What are the "never do X" and "always do Y" rules?
- **Determine Scope:** Decide whether the skill should be Tier 1 (Production Safe), Tier 2 (Conditional), or Tier 3 (Redesigned).

## Phase 2: Forging the Skill

- **Read Template:** Always read `C:\Users\Kapish\.antigravity\.agents\skill-system\skill-template.md` to ensure the new skill strictly adheres to the global format.
- **Draft Skill:** Create a `SKILL.md` file following the template structure. Include clear Phases, Behavior Rules, and Output Formats.
- **Save Location:** The skill MUST be saved globally in `C:\Users\Kapish\.antigravity\.agents\skills\[skill-name-in-kebab-case]\SKILL.md`.

## Phase 3: Registration

- **Update Registry:** You MUST update `C:\Users\Kapish\.antigravity\.agents\skills\CAPABILITIES.md` to register the newly created skill. Add it to the appropriate Tier list and the "Skill Routing Quick Reference" table so it can be routed properly.

---

## Output Format / Delivery

- Output a summary of the newly created skill.
- Confirm that `CAPABILITIES.md` has been successfully updated.
- Provide a markdown link to the new `SKILL.md` file.

---

## Behavior Rules

- Never skip registering the skill in `CAPABILITIES.md`. An unregistered skill is invisible to the routing engine.
- Always name the skill folder and file according to kebab-case conventions (e.g., `modern-react-patterns`).
- The skill must be written as instructions for *the agent* (Antigravity), not for a human user.

---

## Maintenance Notes

> **Freshness check:** If `verified_date` is more than 12 months ago, flag this skill for review.
> Use `.agents/skill-system/maintenance-guide.md` to update this skill.
