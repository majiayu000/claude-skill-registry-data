---
name: obsidian-mcp
description: >
  Vault operation safety layer for all Obsidian MCP operations.
  Load when any vault read/write/search/tag/edit/verify is needed.
  Do NOT use alone for workflow decisions; combine with companion skill.
license: Apache-2.0
compatibility: opencode; obsidian-mcp-server@3.1.5
metadata:
  version: "4.2.0"
  last-reviewed: "2026-05-14"
  owner: r007b34r
---

# obsidian-mcp

## Constraints

- NO write without fresh read first
- NO completion claims without readback verification
- EVERY changed line must trace to user request
- This skill owns vault operations ONLY; workflow decisions belong to companion skills

## Host Constraints (version-locked — re-verify on upgrade)

These are based on `obsidian-mcp-server@3.1.5`. They may be stale.

**To re-verify:** call the forbidden API with a trivial test payload. If it returns -32602, constraint holds. If it succeeds, update this table and remove the ban.

| Operation | Status | Alternative |
|-----------|--------|-------------|
| `obsidian_patch_note` | Forbidden (last verified: 2026-05-10) | `obsidian_replace_in_note` |
| `obsidian_append_to_note` | Forbidden (last verified: 2026-05-10) | `obsidian_replace_in_note` or `obsidian_write_note overwrite:false` for new files |
| `obsidian_write_note overwrite:true` | Forbidden by default | Surgical replace for existing files |
| `obsidian_delete_note` | Requires user confirmation | List path + risk first |

If you suspect a constraint is stale, test it. A successful call means the ban should be lifted.

## Tool Selection

| Goal | Tool |
|------|------|
| Browse structure | `obsidian_list_notes` (depth 2-4) |
| Search | `obsidian_search_notes` |
| Read before edit | `obsidian_get_note format:"document-map"` then `content/full` |
| Create note | `obsidian_write_note overwrite:false` → readback |
| Edit existing | `obsidian_replace_in_note` → readback |
| Frontmatter | `obsidian_manage_frontmatter` |
| Tags | `obsidian_manage_tags` |

When selecting tools, read `references/examples.md` for operation patterns.

## Workflow

1. **Locate**: identify targets, read before writing
2. **Plan**: minimum change only; report unrelated issues, don't fix them
3. **Write**: use appropriate tool from table above
4. **Verify**: readback every write; compare actual vs expected

When formatting completion reports, read `references/templates.md`.

## Error Recovery

| Error | Response |
|-------|----------|
| `-32602` schema error | Stop using that operation; switch to alternative |
| `note_missing` | Search for candidates; ask user |
| `file_exists` | Read existing; use surgical replace |
| 3 repeated failures | Stop and report |

## Trigger Boundary

**Use when:** any vault read/write/search/tag/edit/verify operation.

**Do NOT use for:** triage decisions, synthesis, relationship analysis, health diagnosis, promotion decisions — those belong to companion skills.

## Boundaries

- **Owns:** vault CRUD, frontmatter, tags, search, verification
- **Delegates to:** all 6 workflow skills for decisions
- **Never absorbs:** workflow decisions, knowledge interpretation

## Continuations

| Condition | Next |
|-----------|------|
| Operation complete | Return to calling workflow skill |
| Repeated MCP failures | `vault-health-feedback` |
| 3 failures on same op | Escalate to human |

## Gotchas

**Gotcha 1: Using forbidden APIs "because they look right"**
Current host fails with -32602 regardless of intent. Use alternatives. But if you suspect the bug is fixed, test it first.

**Gotcha 2: Trusting section reads as verification**
`format:"section"` has schema issues on long content. Verify with `content/full`.

**Gotcha 3: Making workflow decisions**
This skill executes operations, not decides what to do. Defer to companion skills.
