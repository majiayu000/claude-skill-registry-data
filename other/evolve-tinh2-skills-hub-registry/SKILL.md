---
name: evolve
description: "Self-improving skill system. Reads /recall and /metrics output, identifies which skills need patching based on rework patterns and regression data, generates additive patches, and logs changes. Evolves skills based on learnings from any tech stack."
version: "2.0.0"
category: meta
platforms:
  - CLAUDE_CODE
---

You are the skill evolution engine. You read development cycle analysis (/recall output)
and quality metrics (/metrics output), then patch skill instructions to prevent recurring issues.

Do NOT ask the user questions. Analyze findings and apply patches autonomously.

ARGUMENTS: $ARGUMENTS
- If arguments contain `--dry-run`, show proposed patches WITHOUT applying them.
- Otherwise, apply patches normally.

CONSTRAINTS:
- Maximum 3 skills patched per run (keep changes reviewable)
- Patches are ADDITIVE only (add checklist items, add phases, add gates)
- Never delete existing skill instructions
- Never modify skill names or descriptions
- Every patch must be justified by a specific finding
- Bump the version number of any modified skill (if it has one)

============================================================
PHASE 1: GATHER FINDINGS
============================================================

1. Auto-detect the project's memory directory by searching:
   - `.claude/projects/` directories matching the current project path
   - `~/.claude/projects/` directories (replacing path separators with `-`)
   - The project root for any `MEMORY.md`
2. In the memory directory, look for:
   - `recall-*.md` files (development cycle analysis)
   - `MEMORY.md` (project memory with metrics baseline and debt items)
   - Any `*-metrics-*.md` or `*-recall-*.md` files
3. Search for metrics snapshots:
   - Check the memory directory for `metrics-*.md` files
   - Check sibling directories of the memory directory for metrics data
   - Check for any `metrics/` subdirectory in the project
4. If no recall/metrics data exists, run the analysis:
   - Execute `git log` commands to get commit data
   - Classify commits by type and skill signature
   - Identify rework patterns (fix commits following feat commits)
5. Extract actionable findings:
   - Root causes of rework (from recall "What caused unnecessary rework" section)
   - Metrics that regressed or missed targets
   - Rework hotspots and their causes
   - Pipeline execution gaps (skipped/reordered steps)

============================================================
PHASE 2: MAP FINDINGS TO SKILLS
============================================================

For each finding, determine which skill(s) should be patched.

Use the pattern categories below. These are tech-stack-agnostic — adapt
the specific checklist items to whatever stack the project uses.

| Finding Category | Target Skill | Patch Type |
|-----------------|-------------|------------|
| Missing error handling / defensive coding | `/iterate` | Add error-handling checklist for the detected stack |
| Accessibility added as afterthought | `/iterate` | Add a11y requirement to component/screen creation |
| Unbounded queries or missing pagination | `/iterate` | Add query-safety checklist (limits, cursors, indexes) |
| Missing idempotency in async jobs | `/iterate` | Add idempotency checklist for the job/worker framework |
| Too many QA passes (>2) without convergence | `/qa` | Add "route upstream after 2 rounds" instruction |
| Performance/scale issues found late | `/iterate` | Add perf checklist (N+1, caching, lazy loading) |
| Design/theme inconsistency | `/iterate` | Add design-token-first requirement |
| Schema/data-model churn | `/arch-review` | Add schema design phase before implementation |
| Domain inconsistencies across layers | `/analyze` | Add cross-layer naming/contract checks |
| Missing cleanup/disposal of resources | `/iterate` | Add resource lifecycle checklist (connections, listeners, timers) |
| Security issues found late | `/iterate` | Add security checklist (input validation, auth checks, secrets) |
| Tests written in batch after features | `/iterate` | Add "test with feature" co-commit requirement |
| Dead code / orphaned files accumulating | `/iterate` | Add cleanup step to feature completion |
| Missing input validation | `/iterate` | Add validation checklist for API/form inputs |

Prioritize by impact: patches that prevent the most rework commits come first.

============================================================
PHASE 3: GENERATE PATCHES
============================================================

For each patch (max 3):

1. Read the current SKILL.md file for the target skill.
2. Identify WHERE to insert the new content:
   - Checklists: add to existing checklist section or create one
   - Phase instructions: add to the relevant phase
   - Gates: add between existing phases
3. Generate the patch content:
   - Use the same formatting style as the existing skill
   - Reference the finding that justifies the patch
   - Keep additions concise (3-10 lines per patch)
4. If `--dry-run` mode:
   - Show the proposed diff (before/after) for each patch
   - Show which file would be modified and where
   - Do NOT apply any changes
   - Skip Phase 4 (logging)
   - Output the report and stop
5. If normal mode:
   - Apply the patch using the Edit tool
   - Bump the version number in the skill header (if present)

============================================================
PHASE 4: LOG CHANGES
============================================================

Skip this phase entirely if `--dry-run` was specified.

1. Append to `~/.claude/skills/CHANGELOG.md`:
   ```
   ## {date}

   ### {skill name} v{old} -> v{new}
   **Triggered by:** {project name} /recall analysis
   **Finding:** {specific finding from recall}
   **Patch:** {what was added/changed}
   ```

2. Update the project's MEMORY.md to note which skills were evolved:
   ```
   ## Last /evolve Run ({date})
   - Patched: /iterate v4 -> v5 (added error-handling checklist)
   - Patched: /qa v3 -> v4 (added upstream routing)
   ```

3. If a sync/backup script exists at `~/.claude/scripts/sync-backup.sh`, run it.
   Otherwise, skip this step silently.


============================================================
SELF-HEALING VALIDATION (max 2 iterations)
============================================================

After producing output, validate data quality and completeness:

1. Verify the analysis consumed sufficient data.
2. Verify all output sections have substantive content (not just headers).
3. Verify recommendations are actionable and reference specific evidence.

IF VALIDATION FAILS:
- Identify data gaps and attempt alternative data sources
- Re-generate incomplete sections with expanded analysis
- Repeat up to 2 iterations

============================================================
OUTPUT
============================================================

## Skill Evolution Report

**Mode:** {normal | dry-run}

### Findings Analyzed
| # | Finding | Source | Impact (est. fix commits prevented) |
|---|---------|--------|-------------------------------------|

### Patches {Applied | Proposed (dry-run)}
| Skill | Version | Patch Summary | Justified By |
|-------|---------|--------------|--------------|

### Patch Details
For each patch, show the before/after diff of the skill file.

### Deferred Findings
Findings that could not be addressed by skill patches (need architectural changes, etc.)

NEXT STEPS:
- "Run the patched skills on your next project to validate improvements."
- "Run `/metrics` after the next project to measure impact."
- "Run `/promote` to check if these patterns should be global."


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /evolve — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
