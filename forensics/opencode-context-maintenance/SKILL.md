---
name: opencode-context-maintenance
description: >
  Diagnose drift across the OpenCode + Obsidian context stack when vault notes,
  config, or host reality no longer align. Load when context feels stale or
  records disagree with reality. Do NOT use for triage, synthesis, or vault CRUD.
license: Apache-2.0
compatibility: opencode; requires obsidian-mcp
metadata:
  version: "4.1.0"
  last-reviewed: "2026-05-14"
  owner: r007b34r
---

# opencode-context-maintenance

## Constraints

- NEVER edit opencode.json, MCP config, model config, or git history automatically
- NEVER treat old wording as drift without evidence of conflict
- NEVER read the whole vault; find context entry points only
- NEVER default to config edits; defer config concerns to user
- Context is layered (3 layers); check all before recommending

## Trigger Boundary

**Use when:** context is stale, records disagree with reality, configuration changed but notes did not, model/MCP assumptions drifted, OpenCode/Obsidian context should be checked.

**Do NOT use for:**
- Raw inbox sorting -> `inbox-triage`
- Week-level meaning extraction -> `weekly-synthesis`
- Direct vault CRUD -> `obsidian-mcp` alone
- Vault health diagnosis -> `vault-health-feedback`
- Promoting material -> `note-promotion`

## Boundaries

- **Owns:** context drift diagnosis, layer comparison, update recommendations
- **Delegates to:** `vault-health-feedback` (drift reveals deeper vault health issue), `obsidian-mcp` (vault operations needed)
- **Never absorbs:** inbox routing, synthesis, relationship analysis, promotion, direct config editing

## Continuations

| Condition | Next skill |
|-----------|-----------|
| Drift reveals systemic vault health issue | `vault-health-feedback` |
| Context notes inaccessible, need vault operation | `obsidian-mcp` |
| Config changes needed that could break environment | Escalate to human |

## Companion Skill

All vault operations follow `obsidian-mcp`. Forbidden: `obsidian_patch_note`, `obsidian_append_to_note`. Verify every write through readback.
## Procedure

### Phase 1: Identify Entry Points
1. `obsidian_list_notes path:"Meta/"` -> context source notes
2. Check OpenCode config state (read-only observation)
3. Identify which layer is most likely drifted based on user report

### Phase 2: Layer-Specific Diagnosis

When checking layers, read `references/examples.md` for drift calibration.

**Long-term vault context** (stable knowledge, methodology, project indexes):
1. Read context source notes
2. Compare claims against current vault state
3. Flag outdated references, dead links, stale assumptions

**Current work context** (active task, recent decisions, preferences):
1. Check if active project references are current
2. Verify recent decisions are reflected in context
3. Flag orphaned "current" items that are no longer current

**Host reality context** (OpenCode config, MCP availability, tool constraints):
1. Compare documented constraints against observed behavior
2. Check if MCP server version matches documented version
3. Flag any new errors not captured in context

<details>
<summary>Layer Checklist Details (expand for specific checks per layer)</summary>

Long-term vault:
- Are methodology notes still accurate?
- Do project indexes point to existing notes?
- Are archived projects still marked as active?
- Do skill references match current skill versions?

Current work:
- Is the "current project" actually current?
- Are recent decisions reflected in relevant notes?
- Are any "TODO" items completed but not updated?
- Do "active" tags match actual activity?

Host reality:
- Does obsidian-mcp-server version match documented?
- Are any "forbidden" APIs now working (or vice versa)?
- Have OpenCode settings changed since last review?
- Are file paths in context still valid?

</details>

### Phase 3: Compare and Recommend

When formatting recommendations, read `references/templates.md`.

1. List disagreements with evidence
2. Recommend updates: target, why, suggested wording, priority
3. Put config changes in "deferred concerns" -- never auto-apply
## Gotchas

### Gotcha 1: Treating old wording as drift
**What happens:** Agent flags notes as "drifted" because phrasing is dated but content is still accurate
**Why it is wrong:** Creates unnecessary churn; old but correct is not drift
**Correct approach:** Require evidence of actual conflict or new fact before flagging

### Gotcha 2: Editing config directly
**What happens:** Agent modifies opencode.json or MCP config to "fix" drift
**Why it is wrong:** Config changes can break the environment; not reversible without backup
**Correct approach:** Always defer config concerns; report and recommend, never auto-edit

### Gotcha 3: Reading the whole vault
**What happens:** Agent scans all notes looking for inconsistencies
**Why it is wrong:** Token waste; most notes are not context sources
**Correct approach:** Identify context entry points (Meta/, project indexes) and check only those

## Validators (CI only, not runtime)

- `validators/pre-check.sh`: Confirms Meta/ path exists and context notes are accessible
- `validators/post-check.sh`: Verifies no config files were modified

## Exit Criteria

- Every drift finding has evidence of actual conflict
- Old wording is not treated as drift without conflict
- No automatic edits to config files
- All three layers checked before recommending
