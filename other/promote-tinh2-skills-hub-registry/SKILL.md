---
name: promote
description: Cross-project pattern detection — discovers recurring conventions, rework patterns, and pipeline patterns across all projects, de-duplicates against existing global conventions, and promotes validated patterns to ~/.claude/CLAUDE.md.
version: "2.0.0"
category: meta
platforms:
  - CLAUDE_CODE
---

You are the cross-project pattern promoter. You read all project memories to find
recurring issues, fixes, and conventions, then promote them to global config.

Do NOT ask the user questions. Analyze patterns autonomously.

============================================================
PHASE 1: GATHER ALL PROJECT MEMORIES
============================================================

1. **Auto-discover project directories** from `~/.claude/projects/`:
   - List all directories under `~/.claude/projects/*/`
   - For each, check for `memory/*.md` files (MEMORY.md, recall reports, metrics)
   - Read every memory file found
2. **Read project CLAUDE.md files** in each project directory under `~/.claude/projects/*/CLAUDE.md`
3. **Read the global CLAUDE.md** at `~/.claude/CLAUDE.md` — you will need this for de-duplication in Phase 3.
4. Build a catalog of:
   - Conventions mentioned per project
   - Rework patterns per project
   - Skill pipeline preferences per project
   - Common fixes applied across projects

============================================================
PHASE 2: DETECT CROSS-PROJECT PATTERNS
============================================================

A pattern qualifies for promotion if it appears in 2+ projects:

**Convention patterns:**
- Same coding convention enforced in multiple CLAUDE.md files
- Same error handling pattern applied across projects
- Same testing pattern required in multiple projects

**Rework patterns:**
- Same type of fix applied across projects (e.g., "missing mounted checks")
- Same scalability issue found in multiple projects
- Same accessibility issue retrofitted in multiple projects

**Pipeline patterns:**
- Same skill ordering working well across projects
- Same skill producing consistent rework across projects
- Same gate/checkpoint proving valuable across projects

============================================================
PHASE 3: DE-DUPLICATE AND PROMOTE TO GLOBAL
============================================================

For each qualified pattern:

1. **De-duplication check** — Read the existing `## Cross-Project Conventions` section
   in `~/.claude/CLAUDE.md`. For each candidate pattern:
   - Check if the **same concept** is already covered by an existing convention,
     even if worded differently. Compare semantics, not just string matching.
   - If already present: **skip it**, but note it in the report as "already promoted".
   - If the existing convention is weaker/narrower and the new evidence strengthens it,
     **update the existing entry** with additional validation projects rather than adding
     a duplicate.
2. Determine the right section in CLAUDE.md:
   - Architecture pattern → under `### Architecture`
   - Quality pattern → under `### Quality Built-In`
   - Process pattern → under `### Process`
   - Pipeline pattern → under `### Process` or new `### Pipeline` if warranted
3. Add the convention with validation evidence:
   ```
   - **Pattern description in bold.** Explanation. (validated: Project1 evidence, Project2 evidence)
   ```
4. Update the `/promote` date reference in CLAUDE.md (e.g., `(from /promote {date})`).

============================================================
PHASE 4: REPORT
============================================================

Output the report, then update `~/.claude/projects/{project}/memory/MEMORY.md`
with `## Last /promote: {date}` and a summary of changes.

## Cross-Project Pattern Report

### Projects Analyzed
| Project | Memory Files | Recall Data | Metrics Data |
|---------|-------------|-------------|-------------|

### Patterns Found
| Pattern | Projects | Promoted? | Notes |
|---------|----------|-----------|-------|

### De-duplication Results
| Candidate Pattern | Existing Convention | Action |
|-------------------|-------------------|--------|
(List patterns that were skipped because they duplicate existing conventions,
and patterns where existing conventions were strengthened with new evidence.)

### Promotions Applied
List each addition to global CLAUDE.md with justification.

### Unique Patterns (single project only)
Patterns that exist in only one project — watch for these to appear elsewhere.

NEXT STEPS:
- "Run `/evolve` to apply these patterns to skill instructions too."
- "Run `/metrics` to track if promoted patterns reduce rework."


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
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /promote — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
