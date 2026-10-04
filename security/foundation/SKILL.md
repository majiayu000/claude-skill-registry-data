---
name: foundation
description: Run an interactive spec-building session for AgentBoard — produce a rigorous, architecturally-silent spec via the spec-writing skill, commit it, and hand off to architecture. Use whenever the user wants to start a new body of work that needs a spec before architecture and cards — e.g. "foundation", "write a spec for this feature", "let's spec this out", "start the foundation phase". Produces docs/specs/<file>.md; it does NOT make architecture decisions or create cards (that is the architecture skill).
---

# Foundation — Spec

Build a spec for a body of work using the agentboard plugin's canonical spec-writing process. The spec covers what the work is, why, and what success looks like. Architecture decisions and card creation happen later in `/architecture`.

## Instructions

Follow these steps in order.

1. **Identify the target codebase.** Confirm the absolute path with the user.

2. **Load companion tools** for codebase research:
   - `ToolSearch` for `codegraph` and `rag`
   - `codegraph_scan` on the target project so you can verify outcomes are achievable, ground requirements in current source, and surface locked decisions during the spec-writing skill's step 2 (Read existing context)

3. **Activate the spec-writing skill** via the `Skill` tool:
   - Skill name: `spec-writing`
   - This skill is the canonical process for writing the spec — it enforces grounded requirements (named standards, confirmed needs, genuine constraints), the three-test discipline (source, abstraction, downstream), threat-model-first security, and auditable derivation. Do not write the spec without it. Do not substitute a thinner template; the rigor is the point.

4. **Follow the spec-writing skill's process**, with these agentboard-specific notes:
   - During the skill's step 2 (Read existing context), use `codegraph` and `rag_search` (`source_type="constraints"` and `source_type="docs"`) to surface existing patterns and locked decisions. Locked decisions discovered here become honored constraints in the spec; existing behavior is context, not a requirement source.
   - During the skill's step 4 (Pressure-test for contradictions), surface architecture-shaped questions explicitly — but do **not** answer them in the spec. The spec is architecturally silent.
   - Architecture questions that surface anywhere in the process land in the spec's "What's still unresolved?" section with `/architecture` as the resolver. They do not enter the body of the spec.
   - Output to `docs/specs/`. Filename: `YYYY-MM-DD-<kebab-name>.md` to match the project's established convention.

5. **Show the spec to the user. Get explicit approval before continuing.**
   - The user is the final authority on whether the spec is ready. Apply any corrections the user requests, then re-confirm before moving on.

6. **Commit the spec to git** on the current branch.

7. **Hand off:**

   ```
   ## Foundation Complete

   **Spec:** docs/specs/YYYY-MM-DD-<kebab-name>.md
   **Status:** approved, committed

   **Next step:** Start a new session and run `/architecture <spec-path>`.
   It runs a level-aware pipeline: a haiku research agent measures
   eight bundle fields from your spec and the codebase and applies the v1.0
   classification rules to compute an L1, L2, or L3 level; a haiku auditor
   independently re-measures every field; the bundle, audit, and level are
   shown to you as transparency (you do NOT approve the level — classification
   is deterministic); then the level-appropriate opus compose agent produces
   the architecture document at `docs/arch/<file>.md`. You approve the
   DOCUMENT (not the level); after approval, the orchestrator commits the
   document and creates one workspace card per Card Slice. Cards do not exist
   until `/architecture` creates them.
   ```

## Key Principles

- The spec-writing skill is the canonical process. Foundation is the agentboard wrapper around it (codebase research tools, handoff to `/architecture`); the rigor lives in the skill.
- The spec is architecturally silent. No file paths, no module names, no card slicing, no dependency ordering, no interface design.
- Every non-trivial requirement must trace to a named standard, a confirmed user need, or a genuine constraint — never to "it seems reasonable" or "the existing system does this."
- One question at a time during brainstorming, and only ask what you cannot determine from input, referenced files, or codebase research.
- Architecture questions that surface go in "What's still unresolved?" with `/architecture` as the resolver, not in the body of the spec.
- Foundation is a full session. Do not try to architect or orchestrate in the same session.
