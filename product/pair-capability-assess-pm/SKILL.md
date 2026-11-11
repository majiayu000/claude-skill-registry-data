---
name: pair-capability-assess-pm
description: "Assess project management tool using resolution cascade (Argument > Adoption > Assessment). Reads PM tool guidelines, proposes tool choice, writes way-of-working.md PM section, composes /pair-capability-record-decision. Delegates setup to /pair-capability-setup-pm. Idempotent."
version: 0.4.1
author: Foomakers
---

# /pair-capability-assess-pm — PM Tool Assessment

Evaluate and decide on the project management tool. Follows the resolution cascade. After decision, delegates actual tool configuration to `/pair-capability-setup-pm`.

## Arguments

| Argument  | Required | Description                                                                  |
| --------- | -------- | ---------------------------------------------------------------------------- |
| `$choice` | No       | Override: skip assessment, use this PM tool directly (e.g. `github`, `filesystem`) |

## Composed Skills

| Skill              | Type       | Required                                         |
| ------------------ | ---------- | ------------------------------------------------ |
| `/pair-capability-record-decision` | Capability | Yes — records PM tool decision as ADL            |
| `/pair-capability-setup-pm`        | Capability | Optional — delegates tool configuration if installed |

## Proposal Target

The rendered adoption content is destined for this section — the caller (or `/pair-capability-setup-pm`) writes it:

- **Target**: [adoption/tech/way-of-working.md](../../../.pair/adoption/tech/way-of-working.md) — **PM tool section**
- **Ownership**: PM tool section (shared file — /pair-capability-assess-methodology owns methodology section)

## Adoption File

- **Target**: [adoption/tech/way-of-working.md](../../../.pair/adoption/tech/way-of-working.md) — **PM tool section**
- **Ownership**: PM tool section (shared file — /pair-capability-assess-methodology owns methodology section)

## Algorithm

### Step 1: Resolution Cascade

#### Path A — Argument Override

1. **Check**: Is `$choice` provided?
2. **Skip**: If not provided, go to Path B.
3. **Act**: Confirm the choice. Check for conflicts with existing adoption.
4. **Verify**: Developer confirms. Proceed to Step 3.

#### Path B — Adoption Exists

1. **Check**: Does [adoption/tech/way-of-working.md](../../../.pair/adoption/tech/way-of-working.md) contain a PM tool configuration?
2. **Skip**: If no PM tool defined, go to Path C.
3. **Act**: Read current PM adoption. Confirm it's valid.
4. **Check**: Does a corresponding decision record exist?
5. **Act**: If decision record missing, compose `/pair-capability-record-decision` to backfill.
6. **Verify**: Done — exit skill.

#### Path C — Full Assessment

1. **Act**: Proceed to Step 2.

### Step 2: Read Guidelines

1. **Act**: Read PM tool guidelines:
   - [PM Tool README](../../../.pair/knowledge/guidelines/collaboration/project-management-tool/README.md) — decision matrix, decision tree, cost-benefit analysis
   - Implementation guides for supported tools:
     - [GitHub Implementation](../../../.pair/knowledge/guidelines/collaboration/project-management-tool/github-implementation.md)
     - [Filesystem Implementation](../../../.pair/knowledge/guidelines/collaboration/project-management-tool/filesystem-implementation.md)
2. **Act**: Read project context:
   - [adoption/product/PRD.md](../../../.pair/adoption/product/PRD.md) — team size, collaboration needs
   - [adoption/tech/way-of-working.md](../../../.pair/adoption/tech/way-of-working.md) — methodology (PM tool should support it)
3. **Verify**: Guidelines and context loaded.

### Step 3: Evaluate Options

1. **Act**: Apply the PM Tool Decision Matrix from guidelines:
   - Score tools on: Team Size, Complexity, Integration, Cost, Learning Curve, Customization, Reporting, Mobile Support.
   - Apply the Decision Tree for quick validation.

2. **Act**: Present recommendation:

   > **PM Tool Recommendation: [Name]**
   > - Score: [weighted total]
   > - Rationale: [evidence from project context]
   > - Implementation guide: [available | not available]
   > - Cost: [free | paid — details]

3. **Act**: If tool has no implementation guide, warn:

   > No implementation guide available for **[tool]**. Setup will be manual.

4. **Verify**: Developer approves.

### Step 4: Delegate Setup or Write Adoption

1. **Check**: Is `/pair-capability-setup-pm` installed?
2. **Act** (installed): Compose `/pair-capability-setup-pm` with `$tool: [chosen tool]`. `/pair-capability-setup-pm` handles adoption update and decision recording. Done — exit skill.
3. **Act** (not installed): Write PM tool section in [way-of-working.md](../../../.pair/adoption/tech/way-of-working.md) directly:
   - Tool name
   - Workflow methodology integration
   - Access method (MCP, CLI, filesystem)
   - Preserve all other sections
4. **Verify**: PM tool section written.

### Step 5: Record Decision (only if /pair-capability-setup-pm not invoked)

1. **Check**: Was `/pair-capability-setup-pm` composed in Step 4? If yes, it already recorded the decision — skip.
2. **Act**: Compose `/pair-capability-record-decision`:
   - `$type`: `non-architectural`
   - `$topic`: `pm-tool-choice`
   - `$summary`: "[Tool] adopted for project management"
3. **Verify**: ADL created. Adoption consistent.

## Output Format

```text
ASSESSMENT COMPLETE:
├── Domain:    Project Management
├── Path:      [Argument Override | Adoption Exists | Full Assessment]
├── Decision:  [tool name]
├── Adoption:  [way-of-working.md PM section — written | confirmed | delegated to /pair-capability-setup-pm]
├── Record:    [ADL path — created | exists | delegated to /pair-capability-setup-pm]
└── Status:    [Complete | Confirmed existing | Delegated]
```

## Composition Interface

When composed by `/pair-process-bootstrap`:

- **Input**: `/pair-process-bootstrap` invokes during Phase 2 (checklist completion). May pass `$choice`.
- **Output**: Returns decision summary. If `/pair-capability-setup-pm` was composed, returns its output.

When invoked **independently**:

- Full interactive flow. Developer commits changes.

## Edge Cases

- **way-of-working.md exists but no PM section**: Add PM section, preserve all other content.
- **Tool without implementation guide**: Write adoption but warn about manual setup.
- **Multiple PM tools needed**: Not supported — one tool per project. Document primary tool.

## Graceful Degradation

- If PM tool guidelines not found, use minimal assessment: ask developer for tool preference.
- If `/pair-capability-setup-pm` not installed, write adoption directly (no tool-specific configuration).
- If `/pair-capability-record-decision` not installed, warn and skip recording.

## Notes

- PM tool decisions are **non-architectural** → produce ADL.
- **Section ownership**: this skill writes ONLY PM tool content in way-of-working.md.
- **Delegation pattern**: /pair-capability-assess-pm decides WHICH tool, /pair-capability-setup-pm configures it. If /pair-capability-setup-pm is installed, it handles both adoption write and decision recording.
- Educational content (tool descriptions, integration details) stays in guidelines.
