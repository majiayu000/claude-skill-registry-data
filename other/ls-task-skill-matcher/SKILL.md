---
name: ls-task-skill-matcher
description: "Match user tasks to installed LocalSetup skills, recommend top matches, and run single-task or batch skill-selection flow with minimal interruption. Delegates complementary public-skill discovery to ls-skill-discovery."
metadata:
  version: "1.1"
---

# Task-to-skill matcher

**Purpose:** Provide one consistent flow for choosing the best installed skill for a user task. Use this when the user asks "what skill should I use?", asks to "pick the best", or when skill choice is unclear.

## When to use this skill

- User asks for skill recommendation or best-skill selection.
- Task-to-skill match is uncertain.
- User asks to auto-pick skills for a multi-step or batch run.

## Do not use this skill

- If user names a specific skill to run, load that skill directly and skip this matcher.

## Sources and scope

- Read installed-skill candidates from the **current platform's context loader/index**. Use the platform registry documentation when available.
- Cursor: the workspace Cursor context index or skills section.
- Claude Code: the workspace Claude context file.
- Codex: the workspace `AGENTS.md`.
- Other platforms: the workspace context source identified by the platform registry.
- For complementary public-skill suggestions, check whether `ls-skill-discovery` is available to the current client. If available, load it and delegate the public discovery flow. If unavailable, report "Public-skill discovery is unavailable. Recommendations: none." and continue installed-skill selection; do not read the public index as a fallback or install a missing package automatically.
- For framework-generated catalogs, prefer `ls/docs/_generated/skill-taxonomy.json` and `ls/docs/SKILLS.md`; both are sorted by `sort_priority` then skill ID and expose class, tags, and pack membership.

## Rule ownership

This skill owns task-to-skill selection behavior. `TASK_SKILL_MATCHING.md` and `SKILLS_AND_RULES.md` are public references, while this skill carries the runtime matching flow.

- Do not add always-loaded platform rules for every skill; keep platform context compact and route users to generated catalogs or this matcher.
- If a user names a skill directly, load that skill and skip matching.
- For batch work, choose a skill sequence once at the beginning unless the user asks for parcel-by-parcel prompts.

## Mode detection

- Treat as **batch** when user request includes multiple distinct subtasks, or says "batch", "multiple steps", or "run the whole thing".
- Otherwise treat as **single task**.

## Workflow

1. **Collect intent**
   - Extract user intent and any task constraints.
   - If user already named a skill, stop matching and load that skill.

2. **Rank installed skills**
   - Compare intent against each installed skill's "when to use" text.
   - Rank by relevance (keyword and description relevance).
   - If uncertain, prepare top 3 candidates with one-line "why it fits".

3. **Single-task flow**
   - If one clear installed match exists, ask once: **"Use this skill?"**
   - Show the installed match and **"Use this skill?"** first, then request complementary public suggestions only if `ls-skill-discovery` is available, using the availability rule above.
   - Same turn: include up to 3 recommendations returned by discovery, preserving its index-status disclosures and any pending user question. If discovery returns no recommendations, report that result; it does not prevent installed-skill selection.

4. **Batch / long-running flow**
   - Prompt once at start with options:
     - Auto-pick best skill for the whole run.
     - Parcel-by-parcel prompts.
     - Parcel auto-pick.
   - If auto-pick is chosen, show planned skill sequence first (best-effort), then proceed without repeated skill prompts.
   - If user chooses parcels and phases are unclear, propose one parcel (whole task), then ask prompt-vs-auto-pick for that parcel.

5. **No installed fit**
   - State that no installed skill is a good fit.
   - If `ls-skill-discovery` is available, offer up to 3 returned complementary public skills to import; otherwise report the unavailable/no-recommendations result above.
   - Optionally suggest creating a new skill with `ls-skill-creator`.

## Public index rules

- Do not implement a separate stale-index policy in this matcher. `ls-skill-discovery` owns the public index, the standard last-refresh reminder, stale detection, user prompt, refresh, and scrub behavior.
- Preserve discovery's returned last-refresh status (date and age when available), availability and freshness disclosures, and any pending user question. Do not calculate a separate freshness decision, reconstruct its prompts, or perform its maintenance sequence in this matcher.
- For complementary suggestions: return up to 3 public skills from the discovery result, each with one-line fit reason.
- To import suggestions, point user to `ls-skill-importer` (or run it if user asks).

## Output style

- Keep outputs short, actionable, and consistently structured.
- For uncertain match: show top 3 installed candidates, each with one-line reason, then ask user to choose or say "pick the best".
- For single clear match: ask once, then show complementary public options in the same response.
- For public complementary suggestions, use available enriched fields from the public index entries returned by `ls-skill-discovery`:
  - Prefer `summary_short` over raw description.
  - Include notable `requirements` or `risk_flags` in one short line.
- Rendering fallback:
  - Rich/basic markdown: numbered list with labeled fields.
  - Plain text/ascii: numbered list with `Skill:`, `Why:`, `Risks:`.

## References

- [TASK_SKILL_MATCHING.md](../../docs/TASK_SKILL_MATCHING.md) - Framework task-skill matching guidance.
- [SKILLS_AND_RULES.md](../../docs/SKILLS_AND_RULES.md) - Framework skills and rules documentation.
- [PLATFORM_REGISTRY.md](../../docs/PLATFORM_REGISTRY.md) - Framework platform registry documentation.
- [SKILL_DISCOVERY.md](../../docs/SKILL_DISCOVERY.md) - Public skill index and discovery workflow managed by `ls-skill-discovery`.
- [ls-skill-discovery](../ls-skill-discovery/SKILL.md) - Complementary public-skill recommendations.
- [ls-skill-importer](../ls-skill-importer/SKILL.md) - Import selected public or local skills.
- [ls-skill-creator](../ls-skill-creator/SKILL.md) - Create a new skill when no installed or public skill fits.
