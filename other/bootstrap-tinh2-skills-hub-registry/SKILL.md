---
name: bootstrap
description: Scaffolds a new project from a saved template with CLAUDE.md, initial memory, recommended pipeline, known pitfalls, and foundation validation.
version: "4.1.0"
category: meta
platforms:
  - CLAUDE_CODE
---

You are a project bootstrapper. Do NOT ask the user questions.

You initialize a new project using a saved template so it starts with proven
conventions, a recommended pipeline, and known pitfalls.

============================================================
TARGET: $ARGUMENTS
============================================================

- If $ARGUMENTS contains a template name, bootstrap the current directory with that template.
- If $ARGUMENTS contains "list", list available templates with descriptions and exit.
- If $ARGUMENTS is empty, list available templates with descriptions and exit.

============================================================
PHASE 1: LIST OR SELECT TEMPLATE
============================================================

1. Scan `~/git2/claude-config/templates/` for available templates.
2. If no argument provided or argument is "list", list available templates with their descriptions and exit.
3. If a template name is provided, verify it exists. If it does not, list available templates and report the error.

============================================================
PHASE 2: GATHER PROJECT DETAILS
============================================================

Read the current directory to understand what already exists:
- Is there a `pubspec.yaml`? `package.json`? `build.sbt`? `Cargo.toml`? `go.mod`?
- Is there already a `CLAUDE.md`?
- Is there a git repo initialized?
- What's the project name (from directory name or config files)?

============================================================
PHASE 3: APPLY TEMPLATE
============================================================

1. **Create CLAUDE.md** from the template's `CLAUDE.md.template`:
   - Replace placeholders with actual project details
   - Keep all convention sections intact
   - Add project-specific sections based on what exists in the directory

2. **Create project memory** at `~/.claude/projects/{project-path}/memory/MEMORY.md`:
   - Copy the recommended pipeline from the template
   - Set initial metrics baseline targets
   - Note the template used and date

3. **Validate Foundation Requirements** (learned from recall analysis — Day 1 gaps caused 100+ rework commits):

   Before recommending the first build skill, verify the project has these foundations.
   If any are missing, add them to the CLAUDE.md as "Foundation TODO" items and flag
   them in the pipeline as "MUST complete before feature development":

   a) SERVICE LAYER: Domain-split service files exist (not one monolithic service).
      Each business domain (users, bookings, payments, etc.) has its own service.
      Prevents: 66-touch god object files.

   b) STRING CONSTANTS / L10N: A string constants file or l10n setup exists for
      user-facing text. Brand terms and feature names are constants, not inline strings.
      Prevents: 59K-line rename cascades.

   c) COMPONENT LIBRARY: Reusable themed widgets exist with a11y baked in (semantic
      labels, 48dp touch targets, design tokens). Screens should compose from these.
      Prevents: 46+ UX/a11y retrofit commits spread across 5 days.

   d) PRIVACY-AWARE DATA MODEL: Public vs private data separation is designed upfront.
      Models that will be read by other users have public projections without PII.
      Prevents: Late-breaking PII exposure + multi-commit migrations.

   e) SCALABILITY TEMPLATES: Service layer includes .limit() on all queries by default,
      batch write helpers, and idempotency patterns for background functions.
      Prevents: 33 scale retrofit commits.

   f) ENV/CONFIG LOADING STRATEGY (Backend/Node.js projects): Environment variable
      loading is established and verified working (dotenv, --env-file, framework-native,
      etc.) BEFORE feature development begins. A `.env.example` file exists documenting
      all required and optional env vars with descriptions. Config defaults are
      centralized in a shared config module (e.g., `src/config.ts`), not scattered
      across route or service files. This prevents trial-and-error env loading commits
      and duplicated config defaults that cause co-change rework.
      Prevents: 2+ trial-and-error commits per project for env loading + co-change
      rework from duplicated defaults (observed: 5/13 rework commits from duplicated defaults).

============================================================
PHASE 4: DISPLAY RESULTS
============================================================

1. **Display the pipeline** from `pipeline.md`:
   - Show the recommended skill sequence
   - Highlight the first skill to run

2. **Display the pitfalls** from `pitfalls.md`:
   - Show the top 5 pitfalls to watch for
   - Each with prevention strategy

3. **Display foundation validation results**:
   - List each foundation requirement with pass/fail/missing status
   - Flag any that must be addressed before feature development


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

## Project Bootstrapped: {project-name}

| Field | Value |
|-------|-------|
| Template used | {template-name} |
| CLAUDE.md created | Yes / Updated |
| Memory initialized | Yes / Already exists |
| Foundation checks | N/N passed |
| Foundation TODOs | N items flagged |

### Files Created
- `CLAUDE.md` — project conventions and architecture
- `~/.claude/projects/.../memory/MEMORY.md` — initial memory

### Foundation Validation
| Requirement | Status |
|-------------|--------|
| Service layer (domain-split) | Pass / TODO |
| String constants / L10N | Pass / TODO |
| Component library (a11y) | Pass / TODO |
| Privacy-aware data model | Pass / TODO |
| Scalability templates | Pass / TODO |
| Env/config loading | Pass / TODO / N/A |

### Recommended Pipeline
```
{pipeline from template}
```

### Top Pitfalls to Watch
1. {pitfall} — {prevention}
2. ...

### First Step
Run `/{first-skill}` to begin.

============================================================
NEXT STEPS
============================================================

- Run the first skill recommended in the pipeline above.
- Run `/arch-review` to validate the project architecture before building features.
- Run `/iterate` to begin feature development with co-commit discipline.
- Run `/skills-list` to see all available skills and pipelines.
- Run `/research` to analyze competitors before building.


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /bootstrap — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.

============================================================
DO NOT
============================================================

- Do NOT start feature development if foundation checks have TODO items — address those first.
- Do NOT overwrite an existing CLAUDE.md without confirming the user wants to replace it.
- Do NOT create templates — this skill only consumes existing templates.
- Do NOT skip the foundation validation phase — Day 1 gaps cause 100+ rework commits.
- Do NOT initialize git — assume the user manages their own repository.
