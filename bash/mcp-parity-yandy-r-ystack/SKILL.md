---
name: mcp-parity
description: Researches a repo and creates or syncs a Linear project, milestones,
  and prioritized issues for one-to-one MCP parity with the app. Use when planning
  an MCP server for an API or app, or when re-syncing MCP issues after new features.
---

# MCP Parity Planner

Research what an API, app, or CLI can do and plan an MCP (Model Context Protocol)
capability that mirrors it one-to-one. The output is Linear only: one Project, a
fixed set of milestones, and one prioritized issue per capability, plus a
foundation track for the server itself. This skill plans. It writes no code and no
files in the target repository.

The first run creates the Project. Each later run finds it, re-inventories the
repository, diffs against the stored manifest, and changes only the delta: new
capabilities get issues, changed contracts get issue updates, and removed
capabilities get cancel or removal work. Unchanged capabilities are not touched.

## Current Task

**Arguments**: `$ARGUMENTS`

- `--dry-run`: research and diff, print the plan, make no Linear writes.
- `--publish`: skip the Phase 3 confirmation (needed for headless or scheduled runs).
  It never skips the mass-removal guard.
- `--project REF`: an existing Linear Project (URL, id, or name) to sync. Skips lookup.
- `--owner-team TEAM`: Linear team key or name for a new Project.
- `--path DIR`: sub-directory to inventory (monorepo package). Default: the git toplevel.
- `--refresh-foundation`: on a sync run, re-research foundation and create only
  foundation keys the manifest does not have yet.
- `--keep-workdir`: keep the scratch directory and print its path at the end.

**Questions:** class `clarify` (team or Project ambiguous, manifest repo mismatch):
headless, print the candidates and stop. Class `confirm-publish` (Phase 3): headless
without `--publish`, behave as `--dry-run` and print `Stopped before Linear writes:
headless run. Rerun with --publish.` Class `confirm-destructive` (mass-removal guard):
headless, stop with `Stopped: {n} of {m} capabilities would be removed. Check --path
and the branch, then rerun interactively.` See
`~/.agents/ycc-shared/references/question-policy.md`.

## Reference map

Read each reference when its phase starts, not up front:

| Phase       | Reference                                                                   |
| ----------- | --------------------------------------------------------------------------- |
| 1 Research  | `~/.agents/skills/mcp-parity/references/research-agents.md`     |
| 1 Inventory | `~/.agents/skills/mcp-parity/references/inventory-format.md`    |
| 2 Plan      | `~/.agents/skills/mcp-parity/references/milestones-priority.md` |
| 1-4 Linear  | `~/.agents/skills/mcp-parity/references/linear-sync.md`         |
| 4 Bodies    | `~/.agents/skills/mcp-parity/templates/capability-issue.md`     |
| 4 Bodies    | `~/.agents/skills/mcp-parity/templates/foundation-issue.md`     |

Scripts:

- `~/.agents/skills/mcp-parity/scripts/openapi_inventory.py` turns an OpenAPI
  3.x spec into a deterministic inventory (stable ids and fingerprints).
- `~/.agents/skills/mcp-parity/scripts/detect-api-surface.sh` lists surface
  hints (languages, specs, route files, CLI files, existing MCP code).
- `~/.agents/skills/mcp-parity/scripts/capability_diff.py` validates the
  inventory, diffs it against the manifest, and renders the next manifest.

**Shell state does not persist between commands.** Wherever this skill writes
`$WORKDIR`, `$REPO_SLUG`, or `$COMMIT`, substitute the literal value you recorded.
Never run a command with one of them empty.

---

## Phase 0: Preflight

1. Resolve the repository root: `git rev-parse --show-toplevel`. With `--path`, the
   inventory root is that directory; it must exist inside the toplevel.
2. Derive `REPO_SLUG` as `owner/repo` from the `origin` URL (strip `.git`), else the
   toplevel directory name. `REPO_NAME` is the part after the last `/`. With `--path`,
   append `/<path>` to `REPO_SLUG` and `-<path-basename>` to `REPO_NAME`.
3. Read Linear hints from the artifact store resolver (read-only; nothing is created):

   ```bash
   bash "${HOME}/.agents/ycc-shared/scripts/resolve-artifact-store.sh" --shell
   ```

   Use `ARTIFACT_LINEAR_WORKSPACE`, `ARTIFACT_LINEAR_TEAM`, and `ARTIFACT_LINEAR_LABEL`
   when set. This skill is Linear-only and ignores `ARTIFACT_STORE=local`.

4. **Linear gate.** A Linear MCP must be installed and authorized. If not, stop:
   `mcp-parity needs an authorized Linear MCP. Connect Linear, then rerun.` When
   `ARTIFACT_LINEAR_WORKSPACE` is set, confirm the connected workspace matches; on a
   mismatch, ask (class `clarify`).
5. Create a scratch directory outside the repository and record its literal path:

   ```bash
   mktemp -d "${TMPDIR:-/tmp}/ycc-mcp-parity.XXXXXX"
   ```

   Write `{}` to `$WORKDIR/issues.json`. Write `$WORKDIR/meta.json` with `project`,
   `repo` (`REPO_SLUG`), `commit`, and `generatedAt` (UTC ISO-8601); fill `project`
   once it is known. Other files (`surface.tsv`, `inventory.json`, `manifest.md` or
   `manifest.json`, `diff.json`) also live there.

6. Record `COMMIT` (`git rev-parse --short HEAD`) and whether the tree is dirty. A
   dirty tree is fine; say so in the summary.

## Phase 1: Detect mode and research

### Step 1: Find a previous run

Follow `references/linear-sync.md` > Lookup and Rebuild. The outcome is one of:

- **sync**: a Project exists, and its manifest is at `$WORKDIR/manifest.md` (the
  Document body) or `$WORKDIR/manifest.json` (rebuilt). That file is `MANIFEST_FILE`.
- **create**: no Project. Write an empty manifest and use it as `MANIFEST_FILE`:

  ```bash
  python3 "${HOME}/.agents/skills/mcp-parity/scripts/capability_diff.py" init \
    --repo "$REPO_SLUG" > "$WORKDIR/manifest.json"
  ```

Print the mode, the Project, and the manifest commit, for example
`Mode: sync (Project "acme-api · MCP parity", manifest at 1a2b3c4)`.

### Step 2: Refresh issue states (sync only)

Follow `references/linear-sync.md` > State refresh. It records `done`, `declined`,
reopened, and `unlinked` statuses in `issues.json`, and `diff --issues` applies
them, so people's decisions shape this run.

### Step 3: Surface scan

```bash
"${HOME}/.agents/skills/mcp-parity/scripts/detect-api-surface.sh" "<inventory-root>" > "$WORKDIR/surface.tsv"
```

The output is hints, not truth. Notices about truncated lists go to stderr.

**Spec-first inventory.** When `surface.tsv` lists an OpenAPI 3.x `SPEC` that the app
serves or generates (not a vendored third-party spec), build the base inventory from it
deterministically. Large APIs (hundreds of operations) are only reliable this way:

```bash
python3 "${HOME}/.agents/skills/mcp-parity/scripts/openapi_inventory.py" \
  "<inventory-root>/<spec path>" > "$WORKDIR/inventory.spec.json"
```

Use `--exclude REGEX` for app-specific non-capabilities. With several specs, prefer
the one the server generates or serves; ask when unsure. A YAML spec needs PyYAML;
install it per the dependency policy, or convert the spec to JSON.

### Step 4: Dispatch research agents

Read `references/research-agents.md` and dispatch the researchers in parallel in one
message. Each gets the inventory root and
`surface.tsv`; on sync runs, researcher 1 also gets each manifest capability's id and
stored `contract`, so ids and field spellings stay stable:

1. **Surface inventory**: every capability, as inventory JSON. With a spec-first
   inventory, it only verifies it and returns capabilities the spec misses (CLI
   commands, GraphQL/RPC surfaces, undocumented routes) and ids to exclude.
2. **Architecture and existing MCP**: existing MCP server, auth model, runtime, and
   where a server should live, plus which operations an existing MCP server covers.
3. **MCP practice**: current spec revision, the official SDK for the language,
   transports, auth, and tool annotations. Sync runs skip it unless
   `--refresh-foundation` is set or the manifest has no `foundation` entries.

### Step 5: Assemble, validate, and diff

Write researcher 1's JSON (merged into the spec inventory, when there is one, with
its exclusions removed) to `$WORKDIR/inventory.raw.json`, then produce
`$WORKDIR/inventory.json` with `references/inventory-format.md` > Coverage merge.
Validate and diff:

```bash
python3 "${HOME}/.agents/skills/mcp-parity/scripts/capability_diff.py" diff \
  --manifest "<MANIFEST_FILE>" --inventory "$WORKDIR/inventory.json" \
  --issues "$WORKDIR/issues.json" --repo "$REPO_SLUG" > "$WORKDIR/diff.json"
```

A non-zero exit names the problem: fix the inventory field, or, for a repo mismatch,
stop and ask (class `clarify`; see `references/linear-sync.md` > Lookup for
`--adopt-repo`). Never hand-edit `diff.json`.

**Renames.** For each `possibleRenames` pair, read both operations. When it is the same
capability, rename the inventory id back to the manifest id and rerun the diff, so it
reports `changed` instead of a cancel plus a duplicate. Ask when unsure.

**Mass-removal guard.** When every tracked capability would be removed, or
`removedRatio` exceeds `0.25` with more than 3 removed, ask before planning (class `confirm-destructive`), naming the count and the
inventory root. Wrong `--path`, a stale branch, or a failed researcher usually causes
it.

## Phase 2: Plan

Read `references/milestones-priority.md`.

1. **Foundation track.** Create mode, or `--refresh-foundation` for keys missing from
   `manifest.foundation`: plan the foundation issues from researchers 2 and 3. Skip
   any item the existing MCP server already provides.
2. **Added and revived.** One issue each: title, milestone, priority, labels, and body
   from `templates/capability-issue.md`. One capability is one issue, which keeps the
   manifest one-to-one.
3. **Changed.** Plan per `references/linear-sync.md` > Changed. The action depends on
   the issue's state and the manifest status.
4. **Removed.** Plan per `references/linear-sync.md` > Removed.
5. **Covered.** Record in the manifest with no issue.

A no-op diff (`"noop": true`) without a foundation refresh plans no issue writes:
only the manifest refresh and one status update.

### Display the plan

Print one table per action, then totals:

```markdown
## MCP parity plan: {REPO_SLUG} @ {COMMIT}

Mode: {create|sync} · Project: {name or "(new)"}

### New issues ({n})

| Capability | Operation  | Milestone      | Priority | Labels               |
| ---------- | ---------- | -------------- | -------- | -------------------- |
| users.list | GET /users | M2 Read parity | High     | mcp-parity, mcp:tool |

### Updated ({n}) · Cancelled ({n}) · Removal issues ({n}) · Covered ({n}) · Declined ({n}) · Unchanged ({n})
```

With `--dry-run`, stop here: `Dry run complete. Rerun without --dry-run to publish.`

## Phase 3: Confirm

Unless `--publish` is set, ask once (class `confirm-publish`) with the counts:
`Publish to Linear: create {a} issues, update {c}, cancel {r}, add {m} milestones?`
Options: publish, or stop as a dry run.

## Phase 4: Write to Linear

Follow `references/linear-sync.md` > Write order. Record every successful action in
`$WORKDIR/issues.json` immediately, before the next call
(`references/inventory-format.md` > Issue map): a new `issue` key for creates, and
`"applied": true` for patches, cancels, and covered re-checks. Unrecorded work is
not committed to the manifest, so the next run retries it.

Then render and save the manifest:

```bash
python3 "${HOME}/.agents/skills/mcp-parity/scripts/capability_diff.py" apply \
  --manifest "<MANIFEST_FILE>" --inventory "$WORKDIR/inventory.json" --repo "$REPO_SLUG" \
  --issues "$WORKDIR/issues.json" --meta "$WORKDIR/meta.json" --format markdown \
  > "$WORKDIR/manifest.next.md"
```

Save `manifest.next.md` as the manifest Document (update in place when it exists).
Then post the Project status update (`references/linear-sync.md` > Status update).

### Failure handling

Class `failure-recovery`: when a Linear write fails, stop new writes. Still render the
manifest with `--partial` added to the command above and save it, so recorded work is
kept and the rest re-diffs next run. Post the status update with health `atRisk`.
Report the failed call and the rerun command.

## Phase 5: Summary

```markdown
# MCP parity {created|synced}: {Project name}

Project: {url} · Commit: {COMMIT}{ (dirty tree)}
Milestones: {list with issue counts}

| Action    | Count | Issues              |
| --------- | ----- | ------------------- |
| Created   | n     | ABC-12, ABC-13, ... |
| Updated   | n     | ...                 |
| Cancelled | n     | ...                 |
| Removal   | n     | ...                 |
| Declined  | n     | ... (not recreated) |
| Covered   | n     | -                   |
| Unchanged | n     | -                   |

Parity: {done + covered}/{tracked} capabilities exposed over MCP.
Next: rerun /mcp-parity after API changes; implement issues with /prp-plan
or /orchestrate.
```

Remove `$WORKDIR` unless `--keep-workdir`.

## Important rules

- **Plan only.** Never write code, scaffold a server, or commit files in the target
  repository.
- **Delta only on sync.** Never recreate, retitle, re-prioritize, reassign, or move
  issues that the diff reports as unchanged. People own those fields after creation.
- **Respect people.** A capability issue a person canceled is `declined`: never
  recreate it; list it in the summary so the gap stays visible.
- **Never move an issue backwards or delete one.** Cancel only unstarted open issues,
  and only when their capability is gone.
- **One-to-one.** Every live capability has exactly one tracking issue, or is
  `covered` or `declined`. The parity guardrail issue keeps that true in CI.
- **Ids are durable.** Capability ids key the manifest and appear in each issue's
  Agent notes. Do not rename ids for style.
- **Subagents never touch Linear.** Researchers are read-only and return data; this
  skill alone calls the Linear MCP.
