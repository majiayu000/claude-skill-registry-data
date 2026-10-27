---
name: decisions-sync
description: >
  Sync human edits from the per-run decisions.gdoc back into
  decisions.yaml. Human-triggered via /ace:step decisions-sync; not
  part of the orchestrator's automatic phase loop.
disable-model-invocation: true
---

# Decisions Sync

Read the human-edited `decisions.gdoc` for a run, diff against
`decisions.yaml`, and write overrides back to the YAML so subsequent
runs honor the human's edits.

## Inputs

Pipeline-only: syncs a run's decisions Doc back into its `decisions.yaml`; both exist only in a run.

| Source | Artifact | Used for |
|---|---|---|
| Per-run state | `ACE/<opp-name>/runs/<run-id>/decisions.gdoc` | human-edited prose Doc — source of overrides |
| Per-run state | `ACE/<opp-name>/runs/<run-id>/decisions.yaml` | structured log to update |

## Products

- `ACE/<opp-name>/runs/<run-id>/decisions.yaml` — updated in place. Rows where the human edited the effective value get `status: overridden` and the new value stored in `override:` (the original `ai-default:` is preserved unchanged). If the human reverts to the AI default, `override:` is cleared and status flips back to `applied`. New `Considered:` bullets are appended.

## Process

1. **Resolve the run folder file ID** for `ACE/<opp-name>/runs/<run-id>/`.
2. **Run the sync script:**

   ```bash
   ACE_ROOT="${CLAUDE_PLUGIN_ROOT:-$(python3 -c "import json,os; d=json.load(open(os.path.expanduser('~/.claude/plugins/installed_plugins.json'))); print(d['plugins']['ace@ace'][0]['installPath'])")}"
   node "$ACE_ROOT/node_modules/tsx/dist/cli.mjs" "$ACE_ROOT/scripts/decisions-sync.ts" <run-folder-fileId>
   ```

   The script:
   - Finds `decisions.gdoc` in the run folder; halts with actionable error if missing.
   - Reads the doc structure via `docs_get`.
   - Parses via `parseDocumentStructure` from `lib/decisions-parser.ts`.
   - Reads `decisions.yaml`; halts if missing.
   - Merges via `mergeDecisions` from `lib/decisions-sync.ts`.
   - Writes the merged YAML back via `drive_update_file`.
   - Returns a change report (defaults overridden, options added, unmatched rows).

3. **Surface the change report** to the operator. Format:

   ```
   Decisions sync — turmeric/20260507-1733
     Values overridden: 2
       - flw-count: 5–8 → 12
       - ai-photo-threshold: ≥90% → ≥95%
     Options added: 1
       - archetype-selection: novel-archetype
     Parsed rows not in YAML: 0
     YAML rows not in gdoc: 0
   ```

4. **Suggest the next step**: re-run `/ace:step idea-to-pdd <opp>/<run-id>` (or `/ace:run <opp>`) so subsequent phases consume the overridden values.

## Failure modes

- **decisions.gdoc missing**: halts with "Run /ace:step decisions-render first to produce the gdoc."
- **decisions.yaml missing**: halts with the path that wasn't found.
- **Schema-invalid YAML after merge**: should not happen — the merger preserves all required fields. If it does, the merger has a bug; the operator should file an issue with the change report.
- **Heading mismatch (gdoc has rows YAML doesn't or vice versa)**: warned in the report; sync proceeds with the matched rows.

## Trigger model

This skill is **human-triggered**. The orchestrator's Phase Write-Back Verifier does NOT auto-invoke it — that would silently overwrite AI defaults from any stale gdoc edits. Always run explicitly:

```
/ace:step decisions-sync <opp>/<run-id>
```

after editing the gdoc, before re-running the affected phases.

## MCP Tools Used

- Google Drive: `drive_list_folder`, `drive_read_file`, `drive_update_file`, `docs_get`

## Mode Behavior

- **Auto:** Run, surface the report, return.
- **Review:** Same as Auto — sync is itself the review-and-apply step; no further pause needed.

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-05-08 | Initial skill — pairs with `lib/decisions-parser.ts`, `lib/decisions-sync.ts`, `scripts/decisions-sync.ts`. Round-trips human edits from `decisions.gdoc` into `decisions.yaml`. Human-triggered. | ACE team (decisions-log PR #3) |
