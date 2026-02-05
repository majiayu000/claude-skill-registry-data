---
name: skill-creation
version: 0.9.0
description: Plan and create Claude Code skills/commands/agents with guided wizards and background agents aligned to v0.5 guidelines.
  Use when user says "create a skill", "plan a new agent", "skill wizard", or "command generator".
---

# Skill Creation (planning + creation)

This skill runs two flows: planning (`/skill-plan`) and creation (`/skill-create`). Review is handled separately by the `skill-reviewing` skill. Keep the main conversation clean; heavy work runs in agents via Agent Runner with registry-based resolution.

## Planning Flow (wizard)
1) Confirm goal: new skill package vs update/version bump (capture desired version target if known).
2) Capture responsibilities + success criteria; list primary use cases.
3) Command UX: required args, options, `--help` text; defaults for `--name`, behavior of `--from` (seed from existing skill/plan), and `--template` (plan skeleton file). Enforce naming convention: file path `.claude/commands/<name>.md`, frontmatter `name: <name>` (no slash), user invocation `/name` (slash added by system), default version 0.1.0.
4) Agents: propose candidate agents, inputs/outputs, fenced JSON envelopes, and registry versions.
5) File layout: commands under `.claude/commands`, skills under `.claude/skills/<name>/SKILL.md`, agents under `.claude/agents`, references/templates under `.claude/references` (if needed) for easy testing before packaging. Default versions for commands/skills/agents: 0.1.0 unless explicitly overridden.
6) Keep agent set minimal by default; only add extra agents when scope justifies it. Prefer clear roles (e.g., intake, fix, PR) over many micro-agents.
7) Statusing: mark plan as Preliminary, then Proposed after user confirms.
8) **Review Gate (Pre-Approval)**: Before marking a plan as Approved, invoke all three review agents to validate the proposed architecture against v0.5 guidelines:
   - `skill-architecture-review` — Validates two-tier pattern, response contracts, agent design
   - `skill-implementation-review` — Validates fenced JSON, hook patterns, security considerations
   - `skill-metadata-storage-review` — Validates frontmatter requirements, storage conventions

   **All three must return `success: true` with zero errors** before the plan can be marked Approved. Warnings are advisory and do not block approval. If any review returns errors, address the issues in the plan before re-running the review gate.
9) Generate 40–80 line overview with full plan path when user approves (Approved). Planning **must not** create artifacts—only write/update a plan file. Creation happens only via `/skill-create`.

### Implementation notes
- Use Agent Runner; resolve agents by name+version from `.claude/agents/registry.yaml`.
- Store plans by default in `plans/<name>.md`; allow override when user supplies a path or `--template`. Do not overwrite request/input files—write to a new plan file/path when invoked with a request doc.
- If `--from` is set, load referenced artifact(s) and summarize key facts into the plan.
- Maintain concise outputs; omit tool traces.

### Agent Runner invocation (v0.5 contract)

```yaml
agent: "skill-planning-agent"
params:
  goal: "new|update"
  target_name: "<skill name>"
  plan_path: "<plans/path.md>"
  from_paths: ["<paths from --from if any>"]
  template_path: "<template if provided>"
version_constraint: "0.x"
timeout_s: 120
```

### Agent output (fenced JSON, minimal envelope)

```json
{
  "success": true,
  "data": {
    "summary": "Concise overview",
    "plan": { "path": "<dest>", "status": "Preliminary|Proposed|Approved" },
    "actions": ["next step", "next step"],
    "open_questions": ["q1", "q2"]
  },
  "error": null
}
```

If plan incomplete, include open questions and next actions; otherwise provide summary + full plan path.

### Review Gate invocation (parallel execution)

Run all three review agents **in parallel** when transitioning from Proposed → Approved:

```yaml
# Architecture review
agent: "skill-architecture-review"
params:
  target_type: "plan"
  target_path: "{{plan_path}}"
  check_two_tier: true
  check_contracts: true
  check_naming: true
version_constraint: "0.x"
timeout_s: 60

# Implementation review
agent: "skill-implementation-review"
params:
  target_path: "{{plan_path}}"
  check_hooks: true
  check_dependencies: true
  check_security: true
version_constraint: "0.x"
timeout_s: 60

# Metadata & storage review
agent: "skill-metadata-storage-review"
params:
  target_type: "plan"
  target_path: "{{plan_path}}"
  check_registry: false  # Plan doesn't have registry entries yet
version_constraint: "0.x"
timeout_s: 60
```

### Review Gate output aggregation

Collect results from all three agents and emit consolidated status:

```json
{
  "success": true,
  "data": {
    "review_gate_passed": true,
    "reviews": {
      "architecture": { "passed": true, "errors": 0, "warnings": 1 },
      "implementation": { "passed": true, "errors": 0, "warnings": 0 },
      "metadata_storage": { "passed": true, "errors": 0, "warnings": 2 }
    },
    "blocking_issues": [],
    "advisory_warnings": ["...", "..."],
    "plan_status": "Approved"
  },
  "error": null
}
```

If `review_gate_passed: false`, the plan remains at Proposed status until issues are resolved.

## Creation Flow
1) Input: approved plan path.
2) Generate stubs for command/skill/agents/references at version 0.1.0 using naming convention:
   - File path: `.claude/commands/<name>.md`
   - Frontmatter name: `<name>` (no slash)
   - User invocation: `/name` (slash added by system)
3) Populate references listed in the plan (e.g., required reference files).
4) Update registry with new agents and skill dependency constraints (including manage-worktree when git ops are needed).

## Storage

| Purpose | Location | Notes |
|---------|----------|-------|
| Plans | `plans/<name>.md` | User-managed, version controlled |
| Scratch | `.claude/state/skill-creation/` | Transient session data, 24h TTL |

## Safety
- Creation of plan files is allowed; avoid destructive repo changes.
- Keep outputs concise; no tool traces in main conversation.
- Base branch/worktree defaults: honor `.claude/config.yaml` if present (`base_branch`, `worktree_root`); otherwise default to `main` and a repo-named worktree root. For git operations, instruct reuse of manage-worktree skill.
- Registry expectations: include manage-worktree dependency when git ops are needed; use constraints like `manage-worktree: "0.x"`. Ensure new agents/skills are added with version 0.1.0 by default.

## Reference Documents

Plans and generated artifacts MUST comply with these normative documents:

| Document | Purpose | Key Patterns |
|----------|---------|--------------|
| [Architecture Guidelines v0.5](../../docs/claude-code-skills-agents-guidelines-0.4.md) | Design patterns | Two-tier, response contracts, agent design |
| [Tool Use Best Practices](../../docs/agent-tool-use-best-practices.md) | Implementation | Fenced JSON, hooks, dependencies |
| [Plugin Storage Conventions](../../docs/PLUGIN-STORAGE-CONVENTIONS.md) | Storage (NORMATIVE) | Logs, settings, outputs paths |

## Review Agents

The review gate uses these specialized agents (from `skill-reviewing` skill):

| Agent | Validates | Reference Doc |
|-------|-----------|---------------|
| `skill-architecture-review` | Two-tier pattern, contracts, naming | Architecture Guidelines v0.5 |
| `skill-implementation-review` | Fenced JSON, hooks, security | Tool Use Best Practices |
| `skill-metadata-storage-review` | Frontmatter, storage paths | Plugin Storage Conventions |
