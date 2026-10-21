---
name: upgrade-project
owner: baseline
description: Reconcile baseline-versioned files that the `create-baseline upgrade` CLI staged for LLM-assisted semantic merge. Use when the CLI prints "Open Claude Code and run /upgrade-project to reconcile". Reads the stage manifest at `.claude/state/upgrade/<ts>/manifest.json`, reasons through each pending file's three-way delta in main context, writes a reconciled LOCAL, then deletes the stage when every file lands. Supports `--dry-run` (preview the reconciled diff without writing) and a structured "needs-user-input" fallback when the conflict cannot be disambiguated automatically.
disable-model-invocation: true
---

# /upgrade-project — semantic-merge reconciliation for baseline files

You are reconciling files that `create-baseline upgrade` decided required **semantic merge** rather than mechanical merge. The CLI has already detected per-file customization, classified each file as tier 3 (SEMANTIC) at build time, and staged the three states (BASE / INCOMING / LOCAL) for you to reason about in main context. This skill is the only sanctioned way to drive that staged state to RECONCILED.

This skill is **maintenance work**, not a workflow phase. It is invoked reactively whenever the upgrade CLI prints the "run /upgrade-project to reconcile" pointer. It does not appear in `.claude/state/workflow.json`, does not require `/triage`, and does not trigger consent gates.

## When to use

- The user just ran `npx @friedbotstudio/create-baseline upgrade <target>` and the CLI exited 5 with a "Pending semantic-merge stage at <ts>" message.
- The user types `/upgrade-project` or asks "reconcile the staged files".
- A previous `/upgrade-project` invocation hit a `NEEDS_USER_INPUT` fallback, the user provided direction, and you re-invoke to pick up where you left off.

## Inputs (read from disk)

For each stage directory under `.claude/state/upgrade/`:

- `manifest.json` — the **stage manifest** the CLI wrote. Schema:
  ```json
  {
    "stage_version": 1,
    "slug": "upgrade-flow-rework",
    "created_at": "2026-05-20T14:49:00.000Z",
    "baseline_version_from": "0.4.0",
    "baseline_version_to": "0.5.0",
    "files": [
      {
        "rel": "docs/init/seed.md",
        "base_sha256": "<hex>" | null,
        "incoming_sha256": "<hex>",
        "local_sha256": "<hex>",
        "status": "PENDING"
      }
    ]
  }
  ```
  `base_sha256` is the **per-entry classification discriminator**: a 64-hex string means the CLI staged a recoverable BASE (three-way reconciliation); the JSON value `null` means BASE was unrecoverable when the user picked Merge on the tier-1 prompt (two-way reconciliation). See [tier1-merge-option spec](../../../docs/specs/tier1-merge-option.md) §Design pick 1A.
- For each entry, the staged artifacts are:
  - `<rel>.baseline-incoming` — the **INCOMING** content. Always present.
  - `<rel>.baseline-base` — the **BASE** content. Present iff `base_sha256` is a string; **absent** for BASE-less entries.
  - The LOCAL file remains at its real path inside the target tree (untouched by the CLI).

## Procedure

1. **Discover the stage.** Read `.claude/state/upgrade/` and pick the most-recent stage directory whose manifest has at least one file with `status: PENDING` or `status: NEEDS_USER_INPUT`. If no such stage exists, tell the user "No pending stage to reconcile" and exit.
2. **Per-entry classification** (binding). For each entry in the stage manifest, in declared order:
   - If `entry.base_sha256` is a 64-hex string → **three-way reconciliation** (existing path; BASE was recoverable).
   - If `entry.base_sha256` is `null` → **two-way reconciliation** (new path; BASE was unrecoverable when the user picked Merge on tier-1; the zero-drift renumbering rule does not apply because there is no BASE anchor to shift against).
   - Any other value → apply the `NEEDS_USER_INPUT` fallback with reason `malformed-base-sha256`.
3. **Three-way reconciliation** (BASE recoverable):
   - Read BASE, INCOMING, and LOCAL.
   - Reason about the three-way delta. Identify what changed between BASE → INCOMING (the upstream edit), what changed between BASE → LOCAL (the user edit), and where they conflict.
   - If both edits are textually non-overlapping, the CLI would have routed the file to tier 2 (mechanical merge). The fact that the file is in tier 3 means structural reconciliation is needed — most commonly: both sides inserted content at the same structural anchor (a new section, a new numbered article, a new TOC entry).
   - Apply the **zero-drift renumbering rule** below.
   - Write the reconciled bytes to the LOCAL path.
   - Update the stage manifest entry's `status` to `RECONCILED`.
4. **Two-way reconciliation** (BASE-less; tier-1 Merge):
   - Read INCOMING and LOCAL. Do NOT attempt to read `<rel>.baseline-base` — it is absent by construction.
   - Reason about the two-way diff: which lines/sections in INCOMING are new bytes that should land in LOCAL, and which lines/sections in LOCAL are user-authored content that should be preserved.
   - The **zero-drift renumbering rule does NOT apply** to two-way reconciliation — there is no BASE anchor to shift against, so "shift, never fold" cannot be evaluated. When LOCAL and INCOMING both add structural entries at the same anchor and you cannot determine which is user content vs baseline content without the BASE, apply the `NEEDS_USER_INPUT` fallback.
   - Write the reconciled bytes to the LOCAL path.
   - Update the stage manifest entry's `status` to `RECONCILED`.
5. **Record the reconciliation marker.** For every entry whose status just transitioned to `RECONCILED` (NOT `NEEDS_USER_INPUT`, NOT skipped under `--dry-run`), invoke the shipped marker helper so the next `create-baseline upgrade` knows the user has already reviewed this file against the current template hash. The helper lives at `.claude/skills/upgrade-project/marker.mjs` and ships with every install:

   ```bash
   node .claude/skills/upgrade-project/marker.mjs record <target> <rel> <baseline_version_to> <incoming_sha256>
   ```

   - `<target>` is the project root the skill is operating in (usually `.`).
   - `<rel>` is the entry's `rel` field from the stage manifest.
   - `<baseline_version_to>` is the stage manifest's top-level field of the same name.
   - `<incoming_sha256>` is the entry's `incoming_sha256` field (the template hash this reconciliation was reviewed against).

   The helper creates / updates `<target>/.claude/.baseline-reconciliations.json` atomically (write-then-rename). It exits 0 on success, 1 on filesystem error (printing `cannot write .claude/.baseline-reconciliations.json: <reason>` to stderr), 2 on bad args. On exit 1, surface the error to the user but do NOT roll back the reconciled LOCAL bytes (LOCAL is already on disk and is the user-visible outcome). Marker is best-effort: the user can re-run `/upgrade-project` to re-record if the write was lost. See `docs/specs/upgrade-no-replay-prompts.md §Behavior #4` for the contract.

6. **Finalize the stage.** When every entry's status is `RECONCILED`, delete the stage directory (`rm -rf .claude/state/upgrade/<ts>/`). Report per-file status to the user.

## The zero-drift renumbering rule (binding for three-way only)

When BASE → INCOMING adds a new structural entry (a new Article, a new section, a new numbered item) at position N, and BASE → LOCAL added the user's own entry at the same position N, you SHALL renumber the user's entry to the **next available** slot (N+1) — you SHALL **never fold** the user's entry into an existing baseline section.

Concrete example (the Article-XI reproducer):
- BASE `seed.md` ends at Article X.
- LOCAL has added a project-specific `## Article XI (user content)`.
- INCOMING ships a new baseline `## Article XI (Skill provenance and the baseline manifest)`.

The reconciled `seed.md` SHALL contain:
- `## Article XI` — the baseline's content (verbatim).
- `## Article XII` — the user's prior content, renumbered.
- Every cross-reference in the document that pointed to "Article XI" SHALL be updated to point to either Article XI (when the reference was always to the new baseline content) or Article XII (when the reference was to what was previously Article XI). Surface ambiguous references as `NEEDS_USER_INPUT` per the fallback below.

The reason **shift, never fold**: the next baseline upgrade SHALL produce zero new staging entries for this file. If the user's content were folded into an existing baseline section, the next upgrade would re-detect a customization and re-stage. The renumbering preserves both bodies as independent structural units, so subsequent upgrades see exactly the baseline-owned portion (Articles I–XI) as unchanged.

The same principle applies recursively. If a later baseline ships Article XII and the user's content has been at Article XII since the prior upgrade, shift the user's content to Article XIII. Always shift to the next available slot.

## `--dry-run` mode

When invoked with `args=dry-run` (e.g., `/upgrade-project dry-run`):

- Per file, produce the reconciled bytes in your reasoning, then emit a colorized unified diff (LOCAL vs reconciled) to the skill's terminal output rather than writing.
- DO NOT modify any LOCAL file.
- DO NOT update the stage manifest (statuses stay PENDING / NEEDS_USER_INPUT).
- DO NOT delete the stage directory.
- DO NOT call `recordReconciliation` — the marker would record a reconciliation the user never actually applied, causing the next upgrade to silently skip a file that still has unreviewed upstream changes. Dry-run is for preview only; the marker write happens exclusively on the real apply path.
- Tell the user: "Dry-run complete. Re-run without `dry-run` to apply."

Dry-run mode is for building trust in early use. After the first few successful reconciliations, the user typically stops dry-running.

## Fallback — NEEDS_USER_INPUT

When you genuinely cannot disambiguate intent — the conflict has multiple plausible reconciliations and you cannot pick one without guessing the user's preference — apply the **NEEDS_USER_INPUT** fallback rather than picking arbitrarily:

1. Update the stage manifest entry's `status` to `NEEDS_USER_INPUT`.
2. Leave BASE, INCOMING, and LOCAL artifacts in place (do NOT delete the stage).
3. Surface a targeted question to the user that names the file, summarizes the conflict in one sentence, and offers concrete options. Example: "Cannot disambiguate `docs/init/seed.md` Article XI: the baseline's new Article XI heading shares the user's chosen heading text. Should I (a) treat them as the same article and merge bodies, or (b) renumber the user's article to XII?"
4. Exit clean. The user provides direction in their next prompt. A subsequent `/upgrade-project` invocation re-reads the stage manifest, finds the `NEEDS_USER_INPUT` entry, and re-attempts with the user's direction.

Use this fallback sparingly. The rework's whole point is that LLM judgment exceeds `git merge-file` for structural conflicts; if you punt to NEEDS_USER_INPUT for trivial reconciliations, you defeat the purpose.

## Changing the documentation provider

An upgrade may bring a new default documentation provider — the MCP server that Article VI.5's current-docs check fetches through. The CLI carries a record of each retirement, so the merge drops the entry a rename replaced instead of leaving you carrying both forever. A provider you swapped in yourself is never touched: the merge only drops a server whose recorded replacement the incoming template actually ships.

To change providers by hand, at any time:

- **Self-hosting the current provider** — change that server's `url` in `.mcp.json` and stop. `.claude/docs-provider.json` already names it.
- **A different provider entirely** — replace the server entry in `.mcp.json`, then set `provider` in `.claude/docs-provider.json` to the new entry's key. Do both, or the skills resolve a name nothing declares.

Never reconcile a provider change into `CLAUDE.md` or `docs/init/seed.md`. Governance names the pointer, not the vendor, so a swap is a config edit and never an amendment.

## Constraints

- **Validate `rel` before writing.** Before writing reconciled bytes to LOCAL, you SHALL verify that the resolved absolute path of `<target>/<rel>` is a descendant of `target`. A `rel` value that escapes the target tree (`../`, absolute path, symlink-resolved escape) SHALL be rejected as a `NEEDS_USER_INPUT` fallback with the reason `path-traversal-rejected`. The CLI's stage writer never produces escaping `rel` values, so this catches only tampered stage manifests from a local attacker with `.claude/state/` write access — defense in depth.
- **No write outside the stage directory, the LOCAL path, and the reconciliation marker.** You SHALL NOT touch `.claude/.baseline-prior/`, the installed `.baseline-manifest.json`, or any other CLI state. The single narrow exception is `.claude/.baseline-reconciliations.json`, written via the `recordReconciliation` foundation module per Procedure step 5 (post-RECONCILED, not in `--dry-run`). The marker write goes through that module's atomic write-then-rename so partial writes cannot corrupt the file.
- **No partial writes per file.** The reconciled LOCAL must be the complete final content. If you cannot produce a complete reconciliation, use the NEEDS_USER_INPUT fallback and leave LOCAL unmodified.
- **Honor Article XI of CLAUDE.md.** This skill only touches files explicitly staged by the CLI — which, by construction, are baseline-owned. User-added files at colliding paths are never staged.
- **No commits.** Reconciled files land on the working tree; the user inspects via `git diff` and commits when satisfied.
- **No re-fetching from npm.** BASE is already on disk in the stage; no network round-trip needed.

## Output

After running, report per file:

```
# /upgrade-project — <stage_ts>

- <rel>: RECONCILED (N lines changed)
- <rel>: NEEDS_USER_INPUT — <one-sentence question>
- <rel>: SKIPPED (dry-run)

Stage deleted: yes | no (NEEDS_USER_INPUT pending)
```
