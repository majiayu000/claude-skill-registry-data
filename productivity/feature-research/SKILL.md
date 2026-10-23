---
name: feature-research
description: 'Researches features with seven specialists and consolidates a feature spec. Use when investigating APIs, assessing feature risks, or researching UX before planning.'
argument-hint: '[--team] [--description "..."] [--dry-run] [feature-name]'
allowed-tools:
  - Read
  - Grep
  - Glob
  - Write
  - Agent
  - TaskCreate
  - TaskUpdate
  - TaskList
  - TaskGet
  - SendMessage
  - WebSearch
  - WebFetch
  - Bash(ls:*)
  - Bash(cat:*)
  - Bash(test:*)
  - Bash(mkdir:*)
  - 'Bash(${CLAUDE_PLUGIN_ROOT}/skills/feature-research/scripts/*.sh:*)'
  - 'Bash(${CLAUDE_PLUGIN_ROOT}/skills/_shared/scripts/*.sh:*)'
---

# Feature Research

Deep research skill for application features. Goes beyond codebase analysis to research external APIs, business logic, technical specifications, UX considerations, and generate actionable recommendations. Dispatches 7 researchers in parallel — standalone sub-agents by default, or an agent team with `--team` (Claude Code only) where teammates share findings with each other.

**Operational context:** Dispatch api-researcher, business-analyzer, tech-designer, ux-researcher, security-researcher, practices-researcher, and recommendations-agent; write seven research-*.md files plus feature-spec.md under docs/plans/[feature-name]/, never docs/prps/. Use /ycc:prp-spec for lightweight single-pass PRP specs.

## Workflow Integration

```
feature-research  -->  plan-workflow  -->  implement-plan
(this skill)           (Step 2)            (Step 3)
Creates:               Uses:               Executes:
feature-spec.md        feature-spec.md     parallel-plan.md
```

**Key Distinctions — This skill vs. other planning/research skills**:

| Skill                     | Agents                            | Output Dir           | Output Files                          | Use When                                       |
| ------------------------- | --------------------------------- | -------------------- | ------------------------------------- | ---------------------------------------------- |
| `feature-research` (THIS) | 7 parallel agents                 | `docs/plans/[name]/` | 7 `research-*.md` + `feature-spec.md` | Deep multi-agent research before plan-workflow |
| `shared-context`          | Agent team                        | `docs/plans/[name]/` | `shared.md`                           | Codebase-focused context for parallel-plan     |
| `prp-spec`                | Single pass (optional researcher) | `docs/prps/specs/`   | `{name}.spec.md`                      | Lightweight spec for PRP workflow              |
| `prp-prd`                 | Interactive + researcher          | `docs/prps/prds/`    | `{name}.prd.md`                       | Full PRD with hypothesis-driven questioning    |
| `prp-plan`                | Single pass + researcher          | `docs/prps/plans/`   | `{name}.plan.md`                      | Implementation plan from PRD or description    |

**This skill ALWAYS**:

- Deploys all 7 researchers in parallel (never skips agents)
- Creates 7 `research-*.md` files + 1 `feature-spec.md`
- Outputs ONLY to `docs/plans/[feature-name]/`
- Dispatches via sub-agents by default; via an agent team only when `--team` is passed

**This skill NEVER**:

- Writes to `docs/prps/` (that is the PRP workflow directory)
- Generates a single-file spec without the research pipeline
- Skips the multi-agent research pipeline to produce output directly
- Acts as a lightweight spec generator

## Arguments

**Target**: `$ARGUMENTS`

Parse arguments (flags first, then the feature name):

- **--team**: Optional. (Claude Code only) Deploy the 7 researchers as teammates under the implicit session team with `TaskList` and coordinated shutdown. Default is standalone parallel sub-agents via the `Agent` tool. Cursor and Codex bundles lack team tools — do not pass `--team` there.
- **--description "..."**: Brief description of the feature (guides research agents)
- **--dry-run**: Show execution plan without running. With `--team`, also prints the team name and 7-teammate roster.
- **feature-name**: Required. Directory name in `docs/plans/`

If no feature name provided, abort with usage instructions:

```
Usage: /feature-research [--team] [--description "..."] [--dry-run] [feature-name]

Examples:
  /feature-research plex-integration --description "Advanced Plex media library integration with filters and playlists"
  /feature-research payment-system --description "Stripe payment integration for subscriptions"
  /feature-research user-dashboard --dry-run
  /feature-research --team plex-integration --description "Advanced Plex media library integration with filters and playlists"
  /feature-research --team --dry-run payment-system
```

**Questions:** class `choose-path` (regenerate or enhance an existing spec); headless (no question tool or chat turn): enhance. See `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/question-policy.md`.

---

## Phase 0: Initialize

### Step 1: Parse Arguments

Extract from `$ARGUMENTS`:

1. **--team**: Boolean flag. Set `AGENT_TEAM_MODE=true` if present, else `false`.
2. **--description**: Quoted string after flag (optional but recommended)
3. **--dry-run**: Boolean flag. Set `DRY_RUN=true` if present, else `false`.
4. **feature-name**: First non-flag argument (required)

Validate the feature name: must be kebab-case, no special characters except hyphens.

**Compatibility note**: When this skill is invoked from a Cursor or Codex bundle, `--team` must not be used (those bundles ship without team tools).

**Team opt-in note**: If `--team` is passed and `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` is not set to `1` in the environment, abort with: `--team requires CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1. Use --parallel instead, or set CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1 in your Claude Code settings if you intentionally want agent-team dispatch.`

### Step 2: Create Directory

**CRITICAL**: Output goes to `docs/plans/[feature-name]/` — NEVER to `docs/prps/` or any other directory, regardless of the user's current working directory. If the user invokes this skill from inside `docs/prps/` or any subdirectory, still resolve the output path from the repository root as `docs/plans/[feature-name]/`.

```bash
test -d "docs/plans/[feature-name]" && echo "exists" || mkdir -p "docs/plans/[feature-name]"
```

### Step 3: Check Existing Research

List any existing files. If `feature-spec.md` exists, read it and ask user if they want to regenerate or enhance.

### Step 4: Handle Dry Run

If `--dry-run` is present:

Display:

```markdown
# Dry Run: Feature Research for [feature-name]

## Research Pipeline

Dispatch Mode: [standalone sub-agents | agent team]
Researchers: 7 (api-researcher, business-analyzer, tech-designer, ux-researcher, security-researcher, practices-researcher, recommendations-agent)

1. api-researcher - External APIs, libraries, integration patterns
2. business-analyzer - Requirements, user stories, business rules
3. tech-designer - Architecture, data models, API design
4. ux-researcher - User experience, workflows, best practices
5. security-researcher - Security analysis, dependency risks, secure coding (severity-leveled)
6. practices-researcher - Modularity, code reuse, KISS, engineering best practices
7. recommendations-agent - Ideas, improvements, risks

## Files That Would Be Created

- docs/plans/[feature-name]/research-external.md
- docs/plans/[feature-name]/research-business.md
- docs/plans/[feature-name]/research-technical.md
- docs/plans/[feature-name]/research-ux.md
- docs/plans/[feature-name]/research-security.md
- docs/plans/[feature-name]/research-practices.md
- docs/plans/[feature-name]/research-recommendations.md
- docs/plans/[feature-name]/feature-spec.md

## Execution Model

- Default (`AGENT_TEAM_MODE=false`): deploy 7 researchers as standalone sub-agents in a single message with multiple `Agent` calls. No team coordination; each sub-agent writes its assigned `research-*.md`. Orchestrator validates and synthesizes `feature-spec.md`.
- With `--team` (`AGENT_TEAM_MODE=true`): use the implicit session team (run label `fr-[sanitized-feature-name]`), register 7 tasks, spawn 7 teammates with shared task state and inter-teammate `SendMessage`, then shut down all teammates via `SendMessage` before synthesis.
```

If `AGENT_TEAM_MODE=true`, additionally print the team roster block:

```
Team name:      fr-<sanitized-feature-name>
Teammates:      7
  - api-researcher         subagent_type=research-specialist         task=External APIs, libraries, integration patterns
  - business-analyzer      subagent_type=codebase-research-analyst   task=Requirements, user stories, business rules
  - tech-designer          subagent_type=codebase-research-analyst   task=Architecture, data models, API design
  - ux-researcher          subagent_type=research-specialist         task=User experience, workflows, accessibility
  - security-researcher    subagent_type=research-specialist         task=Security analysis, dependency risks, secure coding
  - practices-researcher   subagent_type=codebase-research-analyst   task=Modularity, code reuse, KISS, engineering best practices
  - recommendations-agent  subagent_type=codebase-research-analyst   task=Ideas, improvements, risks
```

Do **not** call `TaskCreate`, `Agent`, or `SendMessage` in dry-run mode.

**STOP** without creating files or deploying agents.

---

## Phase 1: Research Pipeline

### Step 5: Team Setup (if `--team`)

If `AGENT_TEAM_MODE=false`, skip this step entirely — the default path dispatches standalone sub-agents in Step 8.

If `AGENT_TEAM_MODE=true`, follow the universal lifecycle contract at
`${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/agent-team-dispatch.md`.

**Team name sanitization** — apply the rules from the shared reference:

1. Lowercase the feature name.
2. Replace any character matching `[^a-z0-9-]` with `-`.
3. Collapse runs of `-` to a single `-`.
4. Trim leading/trailing `-`.
5. Truncate the sanitized context to **20 chars max**.
6. If empty, fall back to `untitled`.

Team name: `fr-<sanitized-feature-name>`.

**Use the implicit session team**: with `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`,
no setup call is needed. `fr-<sanitized-feature-name>` is a display-only run label.
Spawn teammates via `Agent` with each member's `name`; omit `team_name` (ignored).

If the experimental flag is absent, abort the skill with guidance to use `--parallel`.
Do NOT silently fall back to sub-agent mode.

### Step 6: Create Research Tasks (if `--team`)

If `AGENT_TEAM_MODE=false`, skip this step entirely — standalone `Agent` dispatch does not use the shared task list.

If `AGENT_TEAM_MODE=true`, register all 7 tasks up front (flat — all 7 run in a single batch, no `blockedBy`):

1. **"Research external APIs for [feature-name]"** — APIs, libraries, integration patterns
2. **"Analyze business logic for [feature-name]"** — Requirements, user stories, business rules
3. **"Design technical specs for [feature-name]"** — Architecture, data models, API design
4. **"Research UX patterns for [feature-name]"** — User experience, workflows, accessibility
5. **"Evaluate security for [feature-name]"** — Security implications, dependency risks, secure coding
6. **"Evaluate engineering practices for [feature-name]"** — Modularity, code reuse, KISS, testability
7. **"Generate recommendations for [feature-name]"** — Ideas, improvements, risks

If `TaskCreate` fails for any task, shut down any spawned teammates via `SendMessage` and abort.

### Step 7: Read Research Prompts

Read the research prompts template:

```bash
cat ${CLAUDE_PLUGIN_ROOT}/skills/feature-research/templates/research-agents.md
```

### Step 8: Deploy the 7 Researchers

| Name / Teammate `name`  | Subagent Type               | Output File                   | Model   | Focus                                                                 |
| ----------------------- | --------------------------- | ----------------------------- | ------- | --------------------------------------------------------------------- |
| `api-researcher`        | `research-specialist`       | `research-external.md`        | sonnet  | External APIs, libraries, documentation, integration patterns         |
| `business-analyzer`     | `codebase-research-analyst` | `research-business.md`        | sonnet  | Requirements, user stories, business rules, domain logic              |
| `tech-designer`         | `codebase-research-analyst` | `research-technical.md`       | Default | Architecture, data models, API design, system constraints             |
| `ux-researcher`         | `research-specialist`       | `research-ux.md`              | sonnet  | User experience, workflows, best practices, accessibility             |
| `security-researcher`   | `research-specialist`       | `research-security.md`        | sonnet  | Security analysis, dependency risks, secure coding (severity-leveled) |
| `practices-researcher`  | `codebase-research-analyst` | `research-practices.md`       | sonnet  | Modularity, code reuse, KISS, engineering best practices              |
| `recommendations-agent` | `codebase-research-analyst` | `research-recommendations.md` | Default | Ideas, improvements, related features, risks                          |

**Model Assignment**: Pass the `model` parameter when spawning each researcher. Use `model: "sonnet"` for api-researcher, business-analyzer, ux-researcher, security-researcher, practices-researcher. Omit model (inherit default) for tech-designer and recommendations-agent.

Use the prompts from `research-agents.md` with variables substituted:

- `{{FEATURE_NAME}}` - The feature directory name
- `{{FEATURE_DIR}}` - Full output directory path (`docs/plans/[feature-name]`)
- `{{FEATURE_DESCRIPTION}}` - The description provided (or feature name if none)

#### Path A — Standalone sub-agents (`AGENT_TEAM_MODE=false`, default)

**CRITICAL**: Deploy all 7 researchers in a **SINGLE message** with **MULTIPLE `Agent` tool calls**. No `name` — standalone dispatch. Each `Agent` call uses the `subagent_type` and `model` from the table above and the corresponding prompt from `research-agents.md`.

In this mode there is no shared task list; rely on each `Agent`'s return value plus the artifact check in Step 10 to confirm completion. Inter-teammate `SendMessage` coordination (Step 9) is not available — each sub-agent works independently from the prompt alone.

#### Path B — Agent team (`AGENT_TEAM_MODE=true`)

> **MANDATORY — AGENT TEAMS REQUIRED**
>
> In Path B you MUST follow the agent-team lifecycle at
> `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/agent-team-dispatch.md`.
> Do NOT mix standalone `Agent` calls with team dispatch.

All 7 `TaskCreate` entries were registered up front in Step 6 — do not re-create them here.

Spawn all 7 teammates in **ONE message** with **SEVEN `Agent` tool calls**. Every call MUST include:

- `name = "<teammate-name>"` (from the table above — must match the `TaskCreate` subject prefix)
- `subagent_type` and `model` from the table above
- The researcher-specific prompt from `research-agents.md`

After spawning, use `TaskList` to confirm all 7 tasks are `completed` before proceeding to Step 10. Do not rely on agent return values alone — check the shared task state.

### Step 9: Monitor Research Progress

Wait for all 7 researchers to complete their work.

- **Path A (standalone, default)**: rely on `Agent` return values; each sub-agent writes its `research-*.md` artifact before returning.
- **Path B (`--team`)**: use `TaskList` to check progress. Teammates will share findings with each other via `SendMessage`:
  - `api-researcher` tells `tech-designer` about discovered API endpoints and auth patterns
  - `api-researcher` tells `security-researcher` about dependency versions and auth methods
  - `api-researcher` tells `practices-researcher` about discovered libraries for build-vs-depend analysis
  - `tech-designer` tells `business-analyzer` about data model constraints
  - `tech-designer` tells `security-researcher` about proposed architecture for review
  - `tech-designer` tells `practices-researcher` about proposed component structure for modularity review
  - `ux-researcher` tells `business-analyzer` about user workflow requirements
  - `security-researcher` tells `tech-designer` about security constraints (with severity levels)
  - `security-researcher` tells `recommendations-agent` about full risk summary by severity
  - `practices-researcher` tells `tech-designer` about reusable code discoveries and simplification opportunities
  - `practices-researcher` tells `recommendations-agent` about modularity and reuse findings
  - `recommendations-agent` synthesizes insights from all teammates including security and practices findings

  If a teammate gets stuck, send them guidance via `SendMessage`.

**Failure policy for Path B** (mirrors deep-research):

- **Single teammate failure**: record the gap in the corresponding `research-*.md` (stub note) and continue — downstream synthesis will adapt.
- **Majority failure** (≥4 of 7 failed): `SendMessage(shutdown)` to any still-active teammates, shut down all active teammates via `SendMessage`, and abort with "retry without `--team` (standalone sub-agent fallback)".
- **Mid-run user abort**: `SendMessage(shutdown)` to every active teammate, then confirm all teammates have shut down. Never exit with teammates still live.

---

## Phase 2: Consolidate Research

### Step 10: Validate Research Artifacts

After all 7 teammates complete, validate all `research-*.md` files:

```bash
${CLAUDE_PLUGIN_ROOT}/skills/feature-research/scripts/validate-research.sh docs/plans/[feature-name]
```

If validation fails: message the relevant teammate to fix their output, wait for correction, rerun validation until pass.

### Step 11: Shut Down Research Teammates (if `--team`)

If `AGENT_TEAM_MODE=false`, skip this step — standalone sub-agents return on their own.

Otherwise, send shutdown requests to all 7 teammates:

```
SendMessage(to="api-researcher",        message={type:"shutdown_request"})
SendMessage(to="business-analyzer",     message={type:"shutdown_request"})
SendMessage(to="tech-designer",         message={type:"shutdown_request"})
SendMessage(to="ux-researcher",         message={type:"shutdown_request"})
SendMessage(to="security-researcher",   message={type:"shutdown_request"})
SendMessage(to="practices-researcher",  message={type:"shutdown_request"})
SendMessage(to="recommendations-agent", message={type:"shutdown_request"})
```

Do NOT shut down teammates yet — that runs in Step 16 after spec validation.

### Step 12: Read Research Results

Read all 7 research files from `docs/plans/[feature-name]/`.

### Step 13: Read Spec Template

```bash
cat ${CLAUDE_PLUGIN_ROOT}/skills/feature-research/templates/spec-structure.md
```

### Step 14: Generate feature-spec.md

Create `docs/plans/[feature-name]/feature-spec.md` following the template.

**Key Consolidation Principles**:

1. Organize by section, not by agent - Synthesize related findings
2. Be information-dense - Every sentence should add value
3. Include actionable details - Links, code examples, specific APIs
4. Highlight decisions needed - Call out areas requiring user input
5. Preserve source references - Link to original research files for details
6. Surface security findings by severity - CRITICAL items must appear in Risk Assessment; WARNING items in relevant technical sections; ADVISORY items in Recommendations

---

## Phase 3: Validate and Complete

### Step 15: Validate Spec

Run after Step 14 creates `feature-spec.md`:

```bash
${CLAUDE_PLUGIN_ROOT}/skills/feature-research/scripts/validate-spec.sh docs/plans/[feature-name]/feature-spec.md
```

Fix any issues reported (missing sections, empty content, formatting).

### Step 16: Clean Up Team (if `--team`)

If `AGENT_TEAM_MODE=false`, skip this step — there is no team to tear down.

Otherwise, confirm all 7 teammates have received shutdown requests and stopped.

### Step 17: Display Summary

Provide completion summary with: feature name, description, dispatch mode (standalone sub-agents or agent team `fr-<sanitized>`), files created, research summary counts, key findings, decisions needed, and next steps (review spec, proceed to `/plan-workflow`, or add requirements).

---

## Quality Standards

### feature-spec.md Quality Checklist

- Executive summary is information-dense (3-5 sentences)
- External dependencies include documentation links
- Business requirements are specific and testable
- Technical specs include data models/schemas
- UX considerations address error states
- Recommendations are actionable
- Task breakdown preview is realistic

### Research Quality Checklist

Each research file should: focus on its specific domain, include concrete examples and links, identify gaps and uncertainties, provide actionable recommendations, and avoid duplication with other research files.

## Anti-patterns — Do NOT Do These

1. **Do NOT skip the multi-agent pipeline**: Never generate `feature-spec.md` directly without first deploying all 7 researchers (standalone sub-agents or teammates, depending on `--team`) and collecting their `research-*.md` files. The spec is a synthesis of research, not a standalone generation. If about to write `feature-spec.md` without the 7 research files already on disk, STOP — the pipeline is off-rails.

2. **Do NOT output to `docs/prps/`**: This skill's output directory is `docs/plans/[feature-name]/`. The `docs/prps/` tree belongs to the PRP workflow (`prp-prd`, `prp-spec`, `prp-plan`, `prp-implement`). Even if the user's working directory is `docs/prps/` or any subdirectory, always create output under `docs/plans/`.

3. **Do NOT generate a single file**: The minimum correct output is 8 files (7 research + 1 spec). If about to write only one file, STOP — the user likely wants the lightweight PRP spec skill. Redirect them to `/ycc:prp-spec`.

4. **Do NOT conflate with PRP spec generation**: If the user wants a lightweight single-pass spec without the 7-researcher pipeline, they want `/ycc:prp-spec`, not this skill. This skill is the heavyweight multi-agent research track regardless of dispatch mode.

## Important Notes

- **You are the research orchestrator** — coordinate the 7 researchers and synthesize the spec
- **Choose dispatch mode from `$ARGUMENTS`** — default is standalone sub-agents via `Agent`; `--team` switches to teammates under the implicit session team with `TaskList`
- **Team setup first (Path B only)** — register all 7 tasks before spawning teammates
- **Spawn in parallel** — a single message with 7 `Agent` calls (Path A) or 7 `Agent` calls with `name=` (Path B)
- **Teammates share findings (Path B only)** — inter-teammate `SendMessage` coordination is unavailable to standalone sub-agents
- **Single-owner research files** — each researcher writes only its assigned artifact
- **Gate synthesis with validation** — do not generate `feature-spec.md` before validator pass
- **Use web search** — external APIs require current documentation
- **Be thorough but focused** — quality over quantity
- **Enable plan-workflow** — this spec is the foundation for implementation planning
- **Preserve uncertainty** — mark areas needing clarification rather than guessing
- **Clean up team (Path B only)** — always shut down teammates before completing when team mode was used
