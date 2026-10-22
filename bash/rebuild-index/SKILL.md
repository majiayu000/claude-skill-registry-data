---
name: rebuild-index
model: claude-haiku-5-5
category: project-setup
description: Rebuild manifest.json for any artifact storage type. Scans directories and regenerates from scratch.
argument-hint: <work|brainstorms|proposals|refactoring|product-knowledge|requirements|tasks|all>
userInvocable: true
allowed-tools: Read, Write, Bash, Glob, Grep, Task, AskUserQuestion
---

# Rebuild Index

Rebuild `manifest.json` for one or all artifact storage types by scanning directories and extracting metadata from state files.

## Usage

```bash
/rebuild-index work              # Rebuild work manifest
/rebuild-index brainstorms       # Rebuild brainstorms manifest
/rebuild-index proposals         # Rebuild proposals manifest
/rebuild-index refactoring       # Rebuild refactoring manifest
/rebuild-index product-knowledge # Rebuild product knowledge manifest
/rebuild-index requirements      # Delegates to /rebuild-requirements-index
/rebuild-index tasks             # Rebuild the task store index (via tasks.sh)
/rebuild-index all               # Rebuild all manifests
```

## When to Use

- Manifest missing or corrupted
- After manual changes to artifact directories
- After cleanup or archival operations
- Periodic maintenance
- As a safety net when manifests fall out of sync

## Context

Arguments: $ARGUMENTS

---

## Configuration

Read `.claude/configuration.yml` for all artifact paths:

```bash
# Source resolve-config: marketplace installs get ${CLAUDE_PLUGIN_ROOT} substituted
# inline before bash runs; legacy local copies fall back to ~/.claude. If neither
# path resolves, fail loudly rather than letting resolve_artifact be undefined.
if [ -f "${CLAUDE_PLUGIN_ROOT}/shared/resolve-config.sh" ]; then
  source "${CLAUDE_PLUGIN_ROOT}/shared/resolve-config.sh"
elif [ -f "$HOME/.claude/shared/resolve-config.sh" ]; then
  source "$HOME/.claude/shared/resolve-config.sh"
else
  echo "ERROR: resolve-config.sh not found — reinstall the nexus plugin: /plugin install nexus@claude-skills" >&2
  exit 1
fi
IFS='|' read -r WORK_DIR WORK_TYPE         <<< "$(resolve_artifact_typed work work)"
IFS='|' read -r BRAINSTORM_DIR BRAIN_TYPE  <<< "$(resolve_artifact_typed brainstorms brainstorm)"
IFS='|' read -r PROPOSALS_DIR PROP_TYPE    <<< "$(resolve_artifact_typed proposals proposals)"
IFS='|' read -r REFACTOR_DIR REFAC_TYPE    <<< "$(resolve_artifact_typed refactoring work/refactoring-sessions)"
IFS='|' read -r REQUIREMENTS_DIR REQ_TYPE  <<< "$(resolve_artifact_typed requirements requirements)"
IFS='|' read -r PRODUCT_DIR PROD_TYPE      <<< "$(resolve_artifact_typed product-knowledge .)"
```

---

## Process

### Step 1: Parse Argument

Parse `$ARGUMENTS` to determine which artifact type(s) to rebuild.

**Valid arguments:** `work`, `brainstorms`, `proposals`, `refactoring`, `product-knowledge`, `requirements`, `tasks`, `all`

**If no argument or invalid argument:**
```
Error: Artifact type required.

Usage:
  /rebuild-index work
  /rebuild-index brainstorms
  /rebuild-index proposals
  /rebuild-index refactoring
  /rebuild-index product-knowledge
  /rebuild-index requirements
  /rebuild-index tasks
  /rebuild-index all

See `${CLAUDE_PLUGIN_ROOT}/shared/manifest-schema.md` for manifest schema details.
```

### Step 2: Sync Git Locations

For any artifact directory whose storage type is `git`, sync before scanning
(loop over the four rebuild-eligible artifacts here — `requirements` and
`product-knowledge` are synced by their own delegated skill/agent):

```bash
# Re-derived here: shell state does not survive between Bash tool calls, so the
# paths and types the Configuration block resolved are empty in this one. Empty
# is not loud — "$_type" would never equal "git", every location would be
# skipped as if none were git-backed, and the rebuild below would then scan
# whatever was last pulled.
if [ -f "${CLAUDE_PLUGIN_ROOT}/shared/resolve-config.sh" ]; then
  source "${CLAUDE_PLUGIN_ROOT}/shared/resolve-config.sh"
elif [ -f "$HOME/.claude/shared/resolve-config.sh" ]; then
  source "$HOME/.claude/shared/resolve-config.sh"
else
  echo "ERROR: resolve-config.sh not found — reinstall the nexus plugin: /plugin install nexus@claude-skills" >&2
  exit 1
fi
IFS='|' read -r WORK_DIR WORK_TYPE         <<< "$(resolve_artifact_typed work work)"
IFS='|' read -r BRAINSTORM_DIR BRAIN_TYPE  <<< "$(resolve_artifact_typed brainstorms brainstorm)"
IFS='|' read -r PROPOSALS_DIR PROP_TYPE    <<< "$(resolve_artifact_typed proposals proposals)"
IFS='|' read -r REFACTOR_DIR REFAC_TYPE    <<< "$(resolve_artifact_typed refactoring work/refactoring-sessions)"

for pair in "work:$WORK_TYPE:$WORK_DIR" "brainstorms:$BRAIN_TYPE:$BRAINSTORM_DIR" \
            "proposals:$PROP_TYPE:$PROPOSALS_DIR" "refactoring:$REFAC_TYPE:$REFACTOR_DIR"; do
  IFS=':' read -r _artifact _type _dir <<< "$pair"
  if [[ "$_type" == "git" && -d "$_dir" ]]; then
    ( cd "$_dir" && git pull --quiet )
  fi
done
```

### Step 3: Execute Rebuild(s)

For `all`, run each artifact type sequentially (or report results for each). For a single type, run just that one.

**Special cases:**
- `requirements` → Delegate to `/rebuild-requirements-index` skill
- `product-knowledge` → Delegate to `product-expert` agent
- `tasks` → Delegate to `shared/tasks/tasks.sh` (see Rebuild: Tasks). Step 2's git sync and Step 3.5's commit do not apply: the task store is never git-backed — it lives in the project, or in a shared directory outside every repository (global mode), and neither is synced or committed.

---

## Rebuild: Work

**Path:** `$WORK_DIR`

1. Back up existing `${WORK_DIR}/manifest.json` to `manifest.json.backup.{TIMESTAMP}`
2. Scan subdirectories of `$WORK_DIR`
3. For each subdirectory, read `state.json` and check the `type` field to detect work type:
   - `"implementation"` → type: `implementation`
   - `"proposal"` → type: `proposal`
   - `"epic"` → type: `epic`
   - `"requirements"` → type: `requirements`
4. Extract metadata from the state file:
   - `identifier`: from state file or directory name
   - `title`: from state file
   - `status`: from state file
   - `created_at`, `updated_at`: from state file
   - `current_phase`: derive from state file status fields
   - `progress`: derive from chunks or stages
   - `branch`: from state file branches section
   - `tags`: empty array (not tracked in state files)
5. Build manifest with `artifact_type: "work"`
6. Write to `${WORK_DIR}/manifest.json`

**Skip directories:** `manifest.json`, `manifest.json.backup.*`, any file (non-directory)

---

## Rebuild: Brainstorms

**Path:** `$BRAINSTORM_DIR`

1. Back up existing manifest
2. Scan subdirectories of `$BRAINSTORM_DIR`
3. For each subdirectory, prefer `state.json` as the source of truth for session
   fields — a brainstorm is a resumable session, and a rebuild that drops its
   status makes completed and promoted sessions look resumable again:
   - `slug`: `state.json.slug`, else directory name
   - `title`: `state.json.title`, else first heading in `brainstorm-summary.md`
     or `approaches.md`, else slug
   - `status`: `state.json.status`. **If `state.json` is missing or has no
     status, derive it** — `promoted` when `promoted_to` is set,
     `completed` when `brainstorm-summary.md` exists, otherwise `in_progress`.
     Never emit a null status.
   - `created_at`: `state.json.created_at`, else earliest file mtime
   - `updated_at`: `state.json.updated_at`, else latest file mtime
   - `current_phase`: last key in `state.json.phases` marked `completed`, else `unknown`
   - `promoted_to`: `state.json.promoted_to`, else `null`
   - `selected_approach`: `state.json.selected_approach`, else extract from
     `brainstorm-summary.md` if it exists
   - `alternatives_count`: count approach sections in `approaches.md` if exists
   - `tags`: preserve from the backed-up manifest entry if present, else empty array
   - `path`: `"{slug}/"` (required by the schema)
4. Build manifest with `artifact_type: "brainstorms"`
5. Write to `${BRAINSTORM_DIR}/manifest.json`

**Legacy sessions.** Brainstorms created before brainstorms became their own
artifact still sit under `$WORK_DIR/{slug}/` and are indexed in the work
manifest with `type: "brainstorm"`. `/rebuild-index brainstorms` scans
`$BRAINSTORM_DIR` only — it does not migrate them, and `/rebuild-index work`
will keep re-indexing them where they are. That is intentional: rebuilds
reindex, they never move data.

---

## Rebuild: Proposals

**Path:** `$PROPOSALS_DIR`

1. Back up existing manifest
2. Scan subdirectories of `$PROPOSALS_DIR`
3. For each subdirectory:
   - `name`: directory name
   - `title`: extract from first heading in `proposal-final.md` or latest `proposal*.md`
   - `status`: `implemented` if `src/` exists, `final` if `proposal-final.md` exists, else `draft`
   - `created_at`: earliest file modification time
   - `updated_at`: latest file modification time
   - `iterations`: count of `proposal*.md` files
   - `tags`: empty array
4. Build manifest with `artifact_type: "proposals"`
5. Write to `${PROPOSALS_DIR}/manifest.json`

---

## Rebuild: Refactoring

**Path:** `$REFACTOR_DIR`

1. Back up existing manifest
2. Scan subdirectories of `$REFACTOR_DIR`
3. For each subdirectory with `session-state.json`:
   - `session_name`: from state file or directory name
   - `title`: from `target.scope` in state file, or directory name
   - `status`: from state file
   - `created_at`, `updated_at`: from state file
   - `files_affected`: count from `target.files` array in state file
   - `progress`: derive from `progress.completed`/`progress.completed + progress.pending` in state file
   - `tags`: empty array
4. Build manifest with `artifact_type: "refactoring"`
5. Write to `${REFACTOR_DIR}/manifest.json`

---

## Rebuild: Product Knowledge

**Path:** `$PRODUCT_DIR`

Delegate to `product-expert` agent:

```
Task(product-expert, "Build a fresh manifest.json for the product knowledge base.

Knowledge base path: ${PRODUCT_DIR}

Process:
1. Scan all .md files recursively in the knowledge base
2. For each file:
   - Extract title from first heading (or use filename)
   - Determine category from parent directory name
   - Extract tags from content (look for tags/keywords sections, or infer from headings)
   - Create a one-line summary from the first paragraph
3. Build categories and tags frequency maps
4. Write manifest.json to ${PRODUCT_DIR}/manifest.json

Use the manifest schema from ${CLAUDE_PLUGIN_ROOT}/shared/manifest-schema.md (artifact_type: product-knowledge).
Include the extra 'categories' and 'tags' top-level fields.
")
```

`product-expert` only **writes** `manifest.json` — it has no git steps. If the
product-knowledge location is `type: git`, commit and push the rebuilt manifest
here (owner of the rebuild), otherwise it sits uncommitted and the next KB
`git pull` conflicts with it. Skip when `$PROD_TYPE != git`. Follows the
sanctioned KB-write pattern
([`${CLAUDE_PLUGIN_ROOT}/shared/kb-write-pattern.md`](../../shared/kb-write-pattern.md)) —
`cd` in, push with the two logged bypasses, no `record-audit.sh`:

```bash
# Re-derived here: shell state does not survive between Bash tool calls, so the
# pair the Configuration block resolved is empty in this one — and an empty
# "$PROD_TYPE" fails the `git` test, leaving the manifest this step just wrote
# uncommitted, which is the exact conflict the paragraph above describes.
if [ -f "${CLAUDE_PLUGIN_ROOT}/shared/resolve-config.sh" ]; then
  source "${CLAUDE_PLUGIN_ROOT}/shared/resolve-config.sh"
elif [ -f "$HOME/.claude/shared/resolve-config.sh" ]; then
  source "$HOME/.claude/shared/resolve-config.sh"
else
  echo "ERROR: resolve-config.sh not found — reinstall the nexus plugin: /plugin install nexus@claude-skills" >&2
  exit 1
fi
# STRICT, not the advisory resolver, because what this gates is a WRITE — and
# not an ordinary one: the push below drops branch protection and the audit gate
# together. The advisory resolver answers "where would this live", and for an
# artifact nobody configured it answers `$WORKSPACE_ROOT/.claude`, inheriting the
# TYPE of whatever location it fell back to. Point `local` at a git location and
# `product-knowledge` at nothing, and the advisory pair comes back
# `<project>/.claude|git` — the test below passes and the bypassed push lands in
# the project's own repository. Strict refuses instead of fabricating (rc 3 here)
# and returns the same PATH|TYPE pair, so this is a swap, not a redesign.
if _RESOLVED=$(resolve_artifact_strict product-knowledge .); then
  IFS='|' read -r PRODUCT_DIR PROD_TYPE <<< "$_RESOLVED"
else
  echo "product-knowledge is not configured for storage — the rebuilt manifest stays local, uncommitted" >&2
  PRODUCT_DIR=""; PROD_TYPE=""
fi

if [[ "$PROD_TYPE" == "git" && -d "$PRODUCT_DIR" ]]; then
  (
    cd "$PRODUCT_DIR"
    git add manifest.json
    if ! git diff --cached --quiet; then
      # Explicit credential scan — the single-call form misses the hook's
      # automatic one, and the product-knowledge manifest embeds first-paragraph
      # excerpts from user docs (see Step 3.5 note).
      if ! "${CLAUDE_PLUGIN_ROOT}/hooks/credential-scan.sh" manifest.json >&2; then
        echo "WARN: credential finding in product-knowledge manifest.json — skipping its KB push" >&2
      else
        default_branch=$(git symbolic-ref --short refs/remotes/origin/HEAD 2>/dev/null | sed 's#^origin/##')
        [ -z "$default_branch" ] && default_branch=$(timeout 10 git ls-remote --symref origin HEAD 2>/dev/null \
          | awk '/^ref:/ {sub("refs/heads/", "", $(2)); print $(2); exit}')
        default_branch="${default_branch:-master}"
        git commit -m "Rebuild product-knowledge manifest"
        NEXUS_KB_WRITE=1 SECURITY_AUDITOR_BYPASS=1 git push origin -- "$default_branch"
      fi
    fi
  )
fi
```

(The single-call caveat from Step 3.5 applies — branch protection and the audit
gate are intentionally skipped for this KB push; the credential scan is run
explicitly above rather than dropped.)

---

## Rebuild: Requirements

Delegate entirely to the existing `/rebuild-requirements-index` skill:

```
The requirements knowledge base uses its own index.json format with richer metadata.
Delegating to /rebuild-requirements-index...
```

Trigger the `/rebuild-requirements-index` skill.

---

## Rebuild: Tasks

The task store has one owner, `shared/tasks/tasks.sh`, and this target only asks
it to rebuild. Do **not** resolve the tasks path here, scan its files, back up or
write its `manifest.json`: the script resolves the store with its own write
gating — it refuses a git-backed, overlapping or broken `tasks` entry and writes
nothing — and applies archive-wins, which a second scan here could disagree with.

```bash
bash "${CLAUDE_PLUGIN_ROOT}/shared/tasks/tasks.sh" --op rebuild
```

- Exit `0`: report `open` (tasks in the rebuilt index) and `repaired` (leftover
  open copies of tasks that were already archived, now removed). `note: "no task
  store yet"` means there was nothing to rebuild and nothing was created.
- Exit `20`: the store's location was refused. Show the message unchanged — it
  names the reason — and report the target as `Refused`, not rebuilt.
- Exit `30`: show the message and report `Failed`.

---

## Step 3.5: Commit Git-Backed Manifests

After writing `manifest.json` for Work, Brainstorms, Proposals, or
Refactoring, commit and push it if that artifact's storage location is
`type: git` — otherwise the rebuilt manifest sits uncommitted locally and
the next `git pull` on that repo conflicts with it. This follows the
sanctioned KB-write pattern
([`${CLAUDE_PLUGIN_ROOT}/shared/kb-write-pattern.md`](../../shared/kb-write-pattern.md)):
`cd` into the artifact directory (never `git -C`), and push with
`NEXUS_KB_WRITE=1 SECURITY_AUDITOR_BYPASS=1` (both logged) rather than a
mechanical `record-audit.sh` rubber-stamp.

```bash
# Re-derived here, for the same reason Step 2 re-derives them: shell state does
# not survive between Bash tool calls. Empty values would make "$_type" never
# equal "git", so a rebuilt manifest in a git-backed location would silently go
# uncommitted — which is precisely the state this step exists to prevent.
if [ -f "${CLAUDE_PLUGIN_ROOT}/shared/resolve-config.sh" ]; then
  source "${CLAUDE_PLUGIN_ROOT}/shared/resolve-config.sh"
elif [ -f "$HOME/.claude/shared/resolve-config.sh" ]; then
  source "$HOME/.claude/shared/resolve-config.sh"
else
  echo "ERROR: resolve-config.sh not found — reinstall the nexus plugin: /plugin install nexus@claude-skills" >&2
  exit 1
fi
# STRICT here, unlike Step 2. Step 2 pulls; this pushes, with branch protection
# and the audit gate both dropped. For an artifact nobody configured, the
# advisory resolver fabricates a path under the project and inherits the fallback
# location's type — so `local: {type: git}` plus an unconfigured `brainstorms`
# makes the loop below push the project's own repository. Strict refuses rather
# than guessing; an artifact it refuses is skipped, not written to.
_pairs=()
for _art in work:work brainstorms:brainstorm proposals:proposals refactoring:work/refactoring-sessions; do
  IFS=':' read -r _name _subdir <<< "$_art"
  if _RESOLVED=$(resolve_artifact_strict "$_name" "$_subdir"); then
    IFS='|' read -r _p _t <<< "$_RESOLVED"
    _pairs+=("$_name:$_t:$_p")
  else
    echo "$_name is not configured for storage — its rebuilt manifest stays local, uncommitted" >&2
  fi
done

for pair in "${_pairs[@]}"; do
  IFS=':' read -r _artifact _type _dir <<< "$pair"
  if [[ "$_type" == "git" && -d "$_dir" ]]; then
    (
      cd "$_dir"
      git add manifest.json
      if ! git diff --cached --quiet; then
        # The single-call loop misses git-mutation-guard.sh's automatic
        # credential scan (see note below), so run it EXPLICITLY on the
        # manifest — its summary/title fields carry freeform excerpts from
        # user/agent docs and could contain a pasted secret. Skip the push on a
        # finding rather than committing it.
        if ! "${CLAUDE_PLUGIN_ROOT}/hooks/credential-scan.sh" manifest.json >&2; then
          echo "WARN: credential finding in ${_artifact} manifest.json — skipping its KB push" >&2
        else
          default_branch=$(git symbolic-ref --short refs/remotes/origin/HEAD 2>/dev/null | sed 's#^origin/##')
          [ -z "$default_branch" ] && default_branch=$(timeout 10 git ls-remote --symref origin HEAD 2>/dev/null \
            | awk '/^ref:/ {sub("refs/heads/", "", $(2)); print $(2); exit}')
          default_branch="${default_branch:-master}"
          git commit -m "Rebuild ${_artifact} manifest"
          NEXUS_KB_WRITE=1 SECURITY_AUDITOR_BYPASS=1 git push origin -- "$default_branch"
        fi
      fi
    )
  fi
done
```

> **Note on the single-call loop.** Because this loop runs as one Bash tool
> call, the input string begins with `for`, so `git-mutation-guard.sh`'s
> anchored regexes (`^\s*git\s+commit`, `^\s*git\s+push`) match **nothing** —
> the inner `git commit`/`git push` are invisible to the guard, so all three of
> its checks (branch protection, credential scan, audit gate) are skipped.
> Branch protection and the audit gate are *intentionally* bypassed for KB
> writes; the credential scan is **not** something to drop — manifest
> summary/title fields embed freeform excerpts from user/agent docs — so it is
> run **explicitly** via `credential-scan.sh` before each commit above. ⚠️ If an
> artifact location is ever misconfigured to `type: git` pointing at the project
> repo, this loop would still push there with branch protection and the audit
> gate skipped — the explicit scan only covers credentials. Keep KB locations
> pointed at real KB repos. For any interactive or user-content KB write, use the
> separate-Bash-call form in the shared pattern doc so the guard runs in full.

Requirements manifests are committed by their own delegated skill
(`/rebuild-requirements-index`). The product-knowledge manifest is committed by
the **Rebuild: Product Knowledge** step above (it is *not* committed by
`product-expert`, which only writes the manifest) — do not duplicate either
here.

---

## Step 4: Report Results

For each artifact type rebuilt, report:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Index Rebuilt: {artifact_type}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Path: {artifact_dir}
Items found: {count}
Backup: manifest.json.backup.{timestamp}

Items:
  - {item_1_key}: {title} ({status})
  - {item_2_key}: {title} ({status})
  ...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

For `all`, show a summary table:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Index Rebuild Complete
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Artifact           Items  Status
──────────────────────────────────────────────
Work                  3   Rebuilt
Brainstorms           1   Rebuilt
Proposals             2   Rebuilt
Refactoring           0   Empty (no sessions)
Product Knowledge     8   Rebuilt (via agent)
Requirements          5   Rebuilt (via /rebuild-requirements-index)
Tasks                 4   Rebuilt (via tasks.sh)

Total: 23 items indexed across 7 artifact types.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Error Handling

**Artifact directory doesn't exist:**
```
⚠ {artifact_type}: Directory not found: {path}
  Skipping — no items to index.
```

**No items found:**
```
{artifact_type}: 0 items found in {path}
  Created empty manifest.json.
```

**Corrupt existing manifest:**
```
⚠ {artifact_type}: Existing manifest.json is invalid JSON
  Backed up to: manifest.json.corrupt.{timestamp}
  Building fresh manifest from directory scan.
```

**Agent delegation failure (product-knowledge):**
```
⚠ product-knowledge: Agent failed to build manifest
  Error: {error_message}

  Options:
  [r] Retry agent
  [s] Skip product-knowledge
  [a] Abort
```

Use AskUserQuestion for selection.

---

## See Also

- [Manifest Schema Reference](${CLAUDE_PLUGIN_ROOT}/shared/manifest-schema.md) — Schema details and update patterns
- `/rebuild-requirements-index` — Requirements-specific index rebuild
- `/load-context` — Uses manifests for fast listing and lookup
- `/resume-work` — Uses work manifest to find incomplete work
