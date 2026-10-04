---
name: issue-sync
description: >
  Mirror issues and status across issue trackers with stable external-ID
  mapping to avoid duplicates. Load when syncing GitHub and Linear issues,
  mirroring ticket status, or keeping two trackers in sync. Also triggers on
  "issue sync", "sync issues", "mirror issues to", "keep Linear and GitHub
  in sync", or bidirectional issue tracker updates. Requires API access on
  both sides — stops if credentials missing.
license: MIT
metadata:
  author: dvy1987
  version: "1.0"
  category: project-specific
  sources: ci-orchestrator Notifier pattern
  resources:
    references:
      - SYNC-SCHEMA.md
      - examples.md
---
# Issue Sync

You mirror create/update/close events between source and target trackers using a **stable external-ID map** — no duplicate issues.

## Hard Rules

Maintain mapping at `.agent-loom/issue-sync-map.json` — `{source_id, target_id, status, last_synced_at}`.
Never create a target issue without recording the mapping.
On update: look up mapping first; create only if absent.
Never store API tokens in repo — env vars only.
If either side credentials missing, list required env names and **stop**.

---

## Workflow

### Step 1 — Identify source and target

Example: GitHub → Linear, or Linear → GitHub. Confirm direction with user if ambiguous.

### Step 2 — Load or init map

Read `.agent-loom/issue-sync-map.json`. Create `{"mirrors":[]}` if missing.

### Step 3 — Fetch source changes

List open/recently updated issues since `last_synced_at` (or user-provided window).

### Step 4 — Apply to target

| Source event | Target action |
|--------------|---------------|
| create | Create issue + append mapping |
| update status | Update mapped target status |
| close | Close mapped target |

### Step 5 — Write map + summary

Persist updated mirrors. Emit sync report.

---

## Gotchas

- Title-only matching causes duplicates — always use mapping file.
- Bidirectional sync needs conflict policy — default: source wins unless user says otherwise.
- Body HTML vs markdown may truncate — sync title + status + link back.

---

## Output Format

```markdown
## Issue sync — [source] → [target]

Created: N | Updated: N | Closed: N | Skipped (mapped): N
Map: `.agent-loom/issue-sync-map.json`

Errors: [none | list]
```

---

## Examples

Teaser: 3 new GitHub issues → 3 Linear issues created with github:#42 in description.

Full pairs: `references/examples.md`

---

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Match by title" | Titles change; duplicates multiply. |
| "Skip map file" | Next sync creates duplicates. |
| "Embed PAT in script" | Tokens leak from repo history. |
| "Sync everything ever" | Window by last_synced_at — incremental. |
| "Bidirectional without policy" | Conflicts will corrupt state. |

## Verification

- [ ] Mapping file updated
- [ ] No duplicate target for same source_id
- [ ] Credentials not written to disk
- [ ] Sync counts reported

## Red Flags

- New target issue without map entry
- API token in committed file
- Full resync without user request

## Prune Log
Last pruned: 2026-07-05
- Initial release from high-leverage skill spec (Skill 3 family)

## Impact Report

```
Issue sync: [src]→[tgt] | +N ~N -N | Map entries: N
```
