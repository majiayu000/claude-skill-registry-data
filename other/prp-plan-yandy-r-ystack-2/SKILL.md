---
name: prp-plan
description: Creates self-contained PRP plans with codebase patterns. Use when planning
  from a PRD, writing a .plan.md artifact, or capturing patterns for prp-implement.
---

# PRP Plan

> **OpenCode V2 compatibility:** `--team` is unsupported. If it is supplied, abort before setup or dispatch and ask the caller to rerun without it. This target uses native standalone `subagent` calls only.

Create a detailed, self-contained implementation plan that captures all codebase patterns, conventions, and context needed to implement a feature in a single pass.

**Operational context:** Detect PRD versus free-form input, discover codebase patterns through prp-researcher with optional external research, and write docs/prps/plans/{name}.plan.md for /prp-implement.

> Adapted from PRPs-agentic-eng by Wirasm. Part of the PRP workflow series.

**Core Philosophy**: A great plan contains everything needed to implement without asking further questions.

**Golden Rule**: If you would need to search the codebase during implementation, capture that knowledge NOW.

---

## Phase 0 — DETECT

### Flag Parsing

Extract flags from `$ARGUMENTS`:

| Flag            | Effect                                                                                                                                                                                                                                                                                                                       |
| --------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--parallel`    | Fan out research into 3 **standalone sub-agent** researchers; emit tasks with batch/dependency annotations. Works in opencode, Cursor, and Codex.                                                                                                                                                                         |
| `--worktree`    | (legacy — now default; safe to omit) Worktree annotations are emitted by default. Accepted as a silent no-op so existing pipelines continue to work.                                                                                                                                                                         |
| `--no-worktree` | Opt out of worktree annotations. The plan will not contain a `## Worktree Setup` section or per-task `**Worktree**:` annotations.                                                                                                                                                                                            |
| `--enhanced`    | Enhanced research mode: grow the research fan-out from 3 to 7 specialized researchers (api/business/tech/ux/security/practices/recommendations — same coverage as feature-research). Output is still a single PRP-compliant plan file. Composes with --parallel (default) (Claude Code only), and --no-worktree. |
| `--visual`      | Render the finished plan as an Agent-Native visual artifact (MDX) via `visual-plan`; local-files by default, hosted shareable link requires `--share`.                                                                                                                                                                   |

Strip the flags. Set `PARALLEL_MODE=true|false`, ``, `DRY_RUN=true|false`. Default `WORKTREE_MODE=true`; set `WORKTREE_MODE=false` if `--no-worktree` is present. `--worktree` is accepted as a legacy no-op (matches the default). Remaining text is the feature description or PRD path.

```bash
# Default ON; pass --no-worktree to opt out. --worktree accepted as legacy no-op.
WORKTREE_MODE=true
case " $ARGUMENTS " in
  *" --no-worktree "*) WORKTREE_MODE=false ;;
esac
ARGUMENTS="${ARGUMENTS//--no-worktree/}"
ARGUMENTS="${ARGUMENTS//--worktree/}"  # legacy no-op

ENHANCED_MODE=false
case " $ARGUMENTS " in
  *" --enhanced "*) ENHANCED_MODE=true ;;
esac
ARGUMENTS="${ARGUMENTS//--enhanced/}"

VISUAL_MODE=false
case " $ARGUMENTS " in
  *" --visual "*) VISUAL_MODE=true ;;
esac
ARGUMENTS="${ARGUMENTS//--visual/}"
```

**Validation**:

- `--no-worktree` is **orthogonal** to `--parallel` — it may be combined freely with either flag or used alone to suppress annotations.
- `--visual` is orthogonal — it composes with `--parallel`/`--enhanced`/`--no-worktree` and runs after the plan is written and validated. `--dry-run` short-circuits it (prints intent only).


**Questions:** class `clarify` (Ambiguity Gate): headless (no question tool or chat turn), print the open questions and stop; a team retry offer prints the `--parallel` rerun and stops. See `~/.config/opencode/shared/references/question-policy.md`.

### Input Detection

| Input Pattern             | Action                                                            |
| ------------------------- | ----------------------------------------------------------------- |
| Path ending in `.prd.md`  | Parse PRD, find next pending phase                                |
| Path ending in `.spec.md` | Read spec, extract requirements and technical approach as context |
| Path to `.md` with phases | Parse phases, find next pending                                   |
| Path to other file        | Read for context, treat as free-form                              |
| Free-form text            | Proceed to Phase 1                                                |
| Empty                     | Ask user what feature to plan                                     |

### PRD Parsing (when input is a PRD)

1. Read the PRD, parse **Implementation Phases**
2. Find next eligible `pending` phase (check dependency chains)
3. Extract phase name, description, acceptance criteria, dependencies
4. Use the phase description as the feature to plan

If no pending phases remain, report all phases complete.

---

## Phase 1 — PARSE

Extract from the input:

- **What** is being built, **Why** it matters, **Who** uses it, **Where** it fits

Format a user story: `As a [user], I want [capability], so that [benefit].`

Assess complexity: Small (1-3 files) | Medium (3-10 files) | Large (10+ files) | XL (20+ files, consider splitting)

### Ambiguity Gate

If the core deliverable is vague, success criteria undefined, multiple valid interpretations exist, or there are major technical unknowns — **STOP and ask the user**. Do NOT guess.

---

## Phase 2 — EXPLORE

Gather codebase intelligence across 8 categories and 5 traces.

**8 categories**: Similar Implementations, Naming Conventions, Error Handling, Logging Patterns, Type Definitions, Test Patterns, Configuration, Dependencies

**5 traces**: Entry Points, Data Flow, State Changes, Contracts, Patterns


### Path A — Sequential (default)

Dispatch a single `prp-researcher` agent via the `subagent` tool, in codebase mode, to cover all 8 categories and 5 traces. Use the discovery table for the plan's Patterns to Mirror section.

**IMPORTANT — Researcher prompt constraints**: Tell the researcher to keep code snippets to **5 lines max** per finding and limit the total response to the discovery table format only — no prose summaries.

By default (`WORKTREE_MODE=true`), append the following directive to the researcher prompt. Omit when `--no-worktree` was passed (`WORKTREE_MODE=false`):

> **WORKTREE MODE:** The plan you are helping to build will include worktree annotations. In the emitted plan, include a `## Worktree Setup` section with a single `**Parent**:` line naming the feature worktree; no `**Children**:` list; no per-task `**Worktree**:` annotations. All tasks (parallel and sequential) share this one feature worktree path. Follow `~/.config/opencode/shared/references/worktree-strategy.md` for the naming scheme and annotation format.

### Path B — Three standalone researchers (`PARALLEL_MODE=true`)

Dispatch `patterns-research`, `quality-research`, and `infra-research` in one parallel foreground batch. Each call uses `agent="prp-researcher"`, the role name in `description`, a complete role prompt, and `background=false`. Validate every candidate report against its declared backstop artifact and apply the canonical contentless-result policy before synthesis.

#### Path B (enhanced) — when `ENHANCED_MODE=true`

- Replace the 3-row researcher table above with the 7-row roster from `~/.config/opencode/skills/prp-plan/references/enhanced-researchers.md`.
- Dispatch in a **SINGLE message** with **SEVEN native `subagent` calls**, each with `background=false`; validate every candidate report against its backstop artifact.
- Each call uses `@prp-researcher` with `description` set to the role name (`api-researcher`, `business-analyzer`, `tech-designer`, `ux-researcher`, `security-researcher`, `practices-researcher`, `recommendations-agent`) and the role-specific prompt copied verbatim from `enhanced-researchers.md`. Per `enhanced-researchers.md`, each role-specific prompt also instructs the researcher to write a backstop file at `docs/prps/plans/.prp-research/<feature-slug>/<role-name>.md` (`api-researcher.md`, `business-analyzer.md`, `tech-designer.md`, `ux-researcher.md`, `security-researcher.md`, `practices-researcher.md`, `recommendations-agent.md`) in addition to returning the same content inline.
- The 5-line snippet cap and discovery-table-only constraints used in the 3-researcher path apply unchanged.

## Phase 3 — RESEARCH

If the feature involves external libraries/APIs, dispatch `prp-researcher` in external mode. Keep findings to KEY_INSIGHT / APPLIES_TO / GOTCHA / SOURCE format.

If only internal patterns are used, skip: "No external research needed."

---

## Phase 4 — DESIGN

If the feature has UX changes, document before/after user experience and interaction changes.

If purely backend/internal: "Internal change — no user-facing UX transformation."

---

## Phase 5 — ARCHITECT

Define:

- **Approach**: High-level strategy
- **Alternatives Considered**: What was rejected and why
- **Scope**: What WILL be built
- **NOT Building**: What is OUT OF SCOPE

---

## Phase 6 — GENERATE

**CRITICAL: Write the plan progressively in chunks to avoid timeouts.**

Save to `docs/prps/plans/{kebab-case-feature-name}.plan.md`. Create directory first:

```bash
mkdir -p docs/prps/plans
```

### Step 1: Read the template

Read the plan template from `~/.config/opencode/skills/prp-plan/references/plan-template.md`.


For parallel or enhanced research, verify every expected backstop file. If a report is empty, record its `sessionID`, inspect the artifact, preserve valid work, retry at most once, and still report the child response incomplete; an artifact preserves work but does not prove a response.


If `ENHANCED_MODE=true`, also read `~/.config/opencode/skills/prp-plan/references/synthesis-map.md` and use it to route each researcher's findings into the correct plan section. The plan template is unchanged. Enhanced mode produces a richer plan because each section gets dedicated researcher input, not because new sections are added. Avoid section bloat — if a researcher returns no findings for a section, leave the existing N/A language in place or omit fully optional sections.

### Step 2: Write the plan in chunks

**Do NOT generate the entire plan in a single Write call.** Instead:

1. **Write** the initial file with: header through Metadata (+ Batches section if parallel), UX Design, and Mandatory Reading sections
   - By default (`WORKTREE_MODE=true`), include the `## Worktree Setup` section immediately after the Metadata / Batches block and before the first implementation section (see worktree annotation rules below). The section contains a single `**Parent**:` line only. When `--no-worktree` was passed (`WORKTREE_MODE=false`), omit this section.
2. **Edit/append** the Patterns to Mirror section (populated from researcher discovery tables)
3. **Edit/append** the Files to Change + NOT Building sections
4. **Edit/append** the Step-by-Step Tasks section (this is usually the largest — keep each task description concise)
   - All tasks (parallel and sequential) share the single feature worktree. Do NOT add per-task `- **Worktree**: ...` annotation lines.
5. **Edit/append** the Testing Strategy, Validation Commands, Acceptance Criteria, Completion Checklist, Risks, and Notes sections

Each chunk should be a separate Write or Edit call. This prevents any single generation from being too large.

### Worktree annotations (default — `WORKTREE_MODE=true`; skipped when `--no-worktree`)

Derive `<feature-slug>` from the kebab-case plan file name (same value used for `{kebab-case-feature-name}.plan.md`). Derive `<repo>` from `git rev-parse --show-toplevel` basename.

**`## Worktree Setup` section** (top-level, before Batches/implementation):

```markdown
## Worktree Setup

- **Parent**: <repo-root>/.opencode/worktrees/<repo>-<feature-slug>/ (branch: feat/<feature-slug>)
```

All tasks — parallel and sequential — share this one feature worktree path. No `**Children**:` list and no per-task `**Worktree**:` annotation lines are emitted.

> **Plan-file handoff**: leave the emitted plan file in `docs/prps/plans/<name>.plan.md` (in the main checkout). The implementor (`prp-implement`) will **move** it into the feature worktree once the worktree is created — do not pre-write the plan to a worktree path, and do not copy it. See `worktree-strategy.md` §7.

Follow `~/.config/opencode/shared/references/worktree-strategy.md` for the full naming scheme and annotation contract.

### Writing guidelines

- **Keep task descriptions concise** — ACTION and VALIDATE are required; IMPLEMENT should be 2-3 sentences max, not full code blocks
- **Patterns to Mirror snippets**: Use the researcher's snippets directly, max 5 lines each
- **Omit sections that don't apply** rather than writing "N/A" for every sub-field
- **Validation commands**: Use actual project commands discovered during exploration

---

## Phase 6.5 — VALIDATE

After writing the plan file, run the structural validator:

```bash
~/.config/opencode/skills/prp-plan/scripts/validate-prp-plan.sh "docs/prps/plans/{name}.plan.md"
```

### On errors (exit 1)

Review the error output. For each error:

- **Missing section**: Edit the plan file to add the section with appropriate content from the research phases
- **Missing task fields**: Edit affected tasks to add ACTION and VALIDATE at minimum
- **Invalid file paths**: Verify the path using Glob, then fix the path in the plan
- **Placeholder text**: Replace with actual content from codebase exploration

Re-run the validator **once** after fixes. If it still fails, include the validation output in the report to the user so they are aware of remaining issues.

### On warnings only (exit 0)

Include a brief note in the report: "Plan validated with N warning(s) — see validator output for details."

**Do NOT loop more than once.** One fix pass maximum.

---

## Phase 7 — VISUALIZE (optional)


- If `VISUAL_MODE=true` and `--dry-run` is NOT set, invoke `visual-plan <plan-path>` — passing the absolute path of the just-written `docs/prps/plans/{name}.plan.md` — and capture its printed link.
- If `--dry-run` is set, print `visual generation would run` and skip the invocation.

---

## Visual mode

This skill exposes the shared `--visual` decorator. The canonical contract lives at `~/.config/opencode/shared/references/visual-mode.md` — follow it for composition, timing, and hand-off rules.

When `VISUAL_MODE` is set and `--dry-run` is NOT, the skill invokes `visual-plan <absolute-plan-path>` AFTER Phase 6, passing the just-written `.plan.md` path (the file written in Phase 6 and validated in Phase 6.5). `visual-plan` derives its own `visual/` output directory from that path and prints the resulting link; the skill surfaces that link in the Report block. When `--dry-run` is set, print `visual generation would run` and skip — no visual artifacts, directories, or links are produced.

---

## Output

### Update PRD (if input was a PRD)

Update the phase status from `pending` to `in-progress` and add the plan file path.

### Report to User

```
## Plan Created

- **File**: docs/prps/plans/{name}.plan.md
- **Source PRD**: [path or "N/A"]
- **Phase**: [phase name or "standalone"]
- **Complexity**: [level]
- **Scope**: [N files, M tasks]
- **Key Patterns**: [top 3 discovered patterns]
- **External Research**: [topics or "none needed"]
- **Risks**: [top risk or "none identified"]
- **Confidence Score**: [1-10]
- **Research Dispatch**: [Sequential | Parallel sub-agents| Enhanced (7 researchers)]
- **Execution Mode**: [Sequential | Parallel (N batches, max width X)]
- **Worktree Mode**: [Enabled (default) — plan includes ## Worktree Setup (single feature worktree — **Parent**: line only) | Disabled via --no-worktree]
- **Visual Artifact**: [Generated via visual-plan | n/a (--visual not set)]
- **Visual Link**: [hosted URL | http://127.0.0.1:PORT/... | local files only | n/a (--visual not set)]

> Next step: Run `/prp-implement docs/prps/plans/{name}.plan.md` to execute this plan.
```

---

## Verification

Structural validation is enforced by `validate-prp-plan.sh` in Phase 6.5. The validator operates on the written plan file; standalone dispatch details do not change the plan format.

The `validate-prp-plan.sh` script checks:

- Required and recommended sections from the PRP plan template
- Task field completeness (ACTION, VALIDATE required; MIRROR, IMPLEMENT recommended)
- File path existence for Files to Change and Mandatory Reading
- Parallel-mode integrity (if Batches section present)
- Placeholder text detection
- Self-containment heuristic (percentage of tasks with all 4 core fields)

---

## Next Steps

- Run `/prp-implement <plan-path>` to execute this plan
- Run `/plan` for quick conversational planning without artifacts
- Run `/plan-workflow` for the heavyweight parallel-agent planning track

**Entry points into this skill** — `prp-spec` and `prp-prd` are parallel paths, not sequential:

- Run `/prp-spec` for a lightweight single-pass spec when the problem is clear
- Run `/prp-prd` for interactive hypothesis-driven discovery when the problem is unclear
