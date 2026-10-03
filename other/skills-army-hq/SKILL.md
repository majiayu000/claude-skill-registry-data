---
name: skills-army-hq
description: >-
  Manage a durable local skill collection and global app symlinks through conversation.
  Use to import, update, list, remove, or deploy skill folders from repositories already
  on disk, configure deployment targets, or replace skills-sync-trinity. Not for remote
  downloads, publishing skills, or installing their runtime dependencies.
---

# Skills Army HQ

Keep actual skill folders in the user's `~/git-pulse-sync/Deployed Skills` (GH-536:
the collection lives inside the live Git Pulse Sync checkout — the hourly pulse writer
stages it, and machine-local state is excluded by the collection's own `.gitignore`). Apps discover
directory symlinks to these stable copies, not disposable task clones. **The collection is a
projection, not a source:** every skill's canonical source is the repository it was vendored
from — XYZ-forge `skills/<tier>/<name>/` for forge-owned skills, another repo for the rest — and the
collection is the convenient deploy-side copy of them (GH-660). A vendored copy that differs
from its source is either stale (re-vendor it) or carries an improvement that belongs in a PR
to that source repo first — never hand-edit a vendored copy to "fix" it. This skill is
the conversational interface for existing agents/extensions; no extension install
or background service is required. macOS/Python 3.9+ is the supported alpha; other
POSIX devices need local verification. Windows locking is not implemented.

Resolve this loaded skill's physical folder to locate `scripts/intake.py` and
`scripts/sync.py`. Invoke with `python3`, quoting paths. Both work from any CWD.
After initialization, root `intake.py` and `sync.py` are convenience links into the
copied manager. Exactly these two scripts own mutation; do not hand-edit receipts
or imitate their filesystem operations. Read [recovery.md](references/recovery.md)
for interruptions, backups, legacy migration and narrowly authorized manual recovery
exceptions, and [targets.md](references/targets.md)
before choosing app paths or claiming discovery.

Keep [README.md](README.md) with the bundle: it identifies the upstream project for
users. Existing whole-folder intake copies it on initialization and update into
`Deployed Skills/skills-army-hq/`; do not deploy only the scripts or `SKILL.md`.
Applied transactions also copy it to `Deployed Skills/README.md`, the collection's
installer-managed landing document. Keep personal notes in a separate file.

## SOP: one deployed collection per device (GH-672)

**Canonical owning repo → Git Pulse Sync `Deployed Skills/` → app directory symlinks.**
Every device uses its own Pulse checkout's `Deployed Skills` directly. Do not import those
payloads into a second `~/Documents/Deployed Skills` collection. This SOP supersedes the
GH-508 spike and the former GH-536 secondary-device copy procedure. The owning repository
remains the only authoring source; Pulse and Skills Army mini are generated distributions.
This entire bundle, including this SOP and recovery guidance, travels with the projection.

1. **Publish from source.** Change the skill in its owning repo and land it there first.
   On the designated publisher, preview then apply `intake.py update NAME --source
   /path/to/owning-repo/skills/<tier>/NAME` (or `add` for a new skill) against the Pulse root.
   Commit the reviewed portable paths immediately; the Pulse writer cannot rebase a dirty
   tracked tree. Push through the existing Pulse workflow. Do not edit deployed payloads.
2. **Prepare each device's checkout.** Pull the Pulse checkout when its tracked tree is clean.
   Before any local initialization, verify the collection's tracked `.gitignore` excludes
   receipts, pending receipts, targets, catalog, history, locks, backups, staging and caches
   as listed in [recovery.md](references/recovery.md). Ignoring an already tracked file is
   insufficient: the publisher must untrack machine state while retaining its local copy.
3. **Adopt in place once.** For a pulled collection without local receipts, preview then apply:
   `python3 "$HOME/git-pulse-sync/Deployed Skills/intake.py" init --adopt-existing`, then
   the same command with `--apply` before `init`. This validates the clean Git-carried payloads
   and creates only local state, with targets disabled; it makes no second payload copy.
   Plain `init` is only for a new empty collection. Existing initialized collections keep
   their identity; never copy another device's receipts or hand-edit their root.
4. **Deploy local links.** Configure only this device's chosen targets, preview sync, apply,
   and verify links resolve directly into its Pulse collection. Verify app discovery
   separately. The initial defaults stay disabled until the operator selects targets.
5. **Refresh.** Pull published changes into the clean Pulse checkout. Existing app symlinks
   read the updated bytes immediately; refresh app discovery as needed. Preview/apply
   `catalog` for newly arrived skills and sync for link additions. For an intentionally
   removed upstream skill, explicitly `remove NAME` to acknowledge its absent payload,
   then sync to withdraw owned links. Do not re-import the collection into itself.

Use a single designated publisher for portable payload changes; other devices pull and
write only their ignored local deployment state. Configure `--canonical`, `XYZ_FORGE_ROOT`,
or the local `targets.json` canonical path when the Forge drift checker is available;
its absence must be reported, not mistaken for a successful canonical-source check.
Git tracks only executable file-mode bits, so compare digests against the local checkout.
For an existing second collection, use [recovery.md](references/recovery.md)'s migration
procedure; preserve local improvements in their owning repos before retiring any copy.

## Conversational workflow

Translate requests such as “deploy recon from this repo”, “what is deployed?”,
“refresh consult”, or “stop deploying to this app” into the operations below.
Resolve ambiguous repository/skill names before writing. Do not scan the whole
device or add dependencies merely because an imported skill mentions them.

1. Read/list the collection and selected source's `SKILL.md`. Explain intended
   copies, affected targets, conflicts and runtime prerequisites. Plain initialization
   copies this entire manager into an empty collection; adoption reuses the existing payloads.
   Both leave targets disabled.
2. Preview the exact mutation (default; `--dry-run` always overrides `--apply`).
   A request to deploy/update/remove the named skills authorizes that previewed
   normal operation. Ask before expanding targets, replacing a foreign entry, or
   archiving a real legacy app directory. Never treat a preview as a deployment.
3. Apply the intake/target operation, then preview and apply sync when requested.
   Review every nonzero result: independent targets can succeed while conflicts
   remain. Do not force, steal a lock, delete a conflicting folder, or retry blindly.
4. Verify copied payload hashes, link read-through, catalog and history. Report
   filesystem deployment separately from each actual app/extension's discovery
   and runtime readiness. Refresh/restart discovery only as that app supports it.

## Commands

Put global options **before** the intake subcommand. Substitute local paths/names;
the examples below are templates, not a hardcoded source inventory.

```bash
python3 /path/to/skills-army-hq/scripts/intake.py init
python3 /path/to/skills-army-hq/scripts/intake.py --apply init
python3 "$HOME/git-pulse-sync/Deployed Skills/intake.py" list
python3 "$HOME/git-pulse-sync/Deployed Skills/intake.py" add /path/to/local-repo/skills/example
python3 "$HOME/git-pulse-sync/Deployed Skills/intake.py" --apply add /path/to/local-repo/skills/example
python3 "$HOME/git-pulse-sync/Deployed Skills/intake.py" --apply update example
python3 "$HOME/git-pulse-sync/Deployed Skills/intake.py" --apply update example --source /new/repo/skills/example
python3 "$HOME/git-pulse-sync/Deployed Skills/intake.py" --apply remove example
python3 "$HOME/git-pulse-sync/Deployed Skills/intake.py" --apply catalog
python3 "$HOME/git-pulse-sync/Deployed Skills/intake.py" targets
python3 "$HOME/git-pulse-sync/Deployed Skills/intake.py" --apply targets --id chosen-app --path /verified/app/skills --consumer "Chosen app"
python3 "$HOME/git-pulse-sync/Deployed Skills/intake.py" --apply targets --id chosen-app --disable
python3 "$HOME/git-pulse-sync/Deployed Skills/sync.py" --status
python3 "$HOME/git-pulse-sync/Deployed Skills/sync.py" --apply
python3 "$HOME/git-pulse-sync/Deployed Skills/sync.py" --status --canonical /path/to/XYZ-forge   # drift report vs canonical
python3 "$HOME/git-pulse-sync/Deployed Skills/sync.py" --apply --allow-drift                    # loud, disclosed exception
```

Both scripts accept `--root /chosen/collection` for redirected Documents or another
explicit collection. The default root is `~/git-pulse-sync/Deployed Skills`; `XYZ_SKILLS_ROOT` overrides it,
and explicit `--root` overrides both. Check old environment overrides before operating;
script location does not select a different collection. A custom root is an alternative
for users without Pulse, not an additional mirror on a Pulse-enabled device. Home/path values are computed locally, never copied from a
different user's configuration. Source intake is restricted to local Git repos;
dirty and unmerged working folders are allowed and recorded with commit and digest.
External, absolute, dangling and cyclic payload links are refused. Copies retain
internal relative links, file modes and bytes. Do not run copied `install.sh` files:
their legacy write policies can bypass managed ownership.

Actual valid immediate skill folders are the desired set. `catalog.md` is generated;
`targets.json` is editable configuration; `.deploy-skills.json` is provenance and
owned-link state; `changelog.md` is audit history. Manual valid additions can be
adopted by `catalog`; unexplained missing folders stop sync until explicit `remove`
acknowledges them. The manager itself is protected from removal to preserve recovery.
Disabling/removing a target does not erase its ownership receipts: sync withdraws
its still-matching links. Foreign folders and retargeted links remain untouched.

## Drift guard: deploying a drifted skill fails loudly (GH-660)

`sync.py` runs XYZ-forge's own checker (`utils/py/skill_drift_check.py`, ingested as
`--json`) on every normal reconciliation — preview, `--status` and `--apply` (`--retire-trinity` only withdraws the retired skill and runs no deploy) — comparing each vendored `SKILL.md`
with the forge's canonical `skills/<tier>/<name>/SKILL.md`. Only names that exist in the forge's
`skills/` are judged; collection-only skills (e.g. `buffer-doctor`, `hiqs-register`) are
reported as `unrecognized` and never fail.

- The forge root resolves in this order: `--canonical FORGE_ROOT`, `XYZ_FORGE_ROOT`,
  a top-level `"canonical"` key in `targets.json` (machine-local, editable — the
  recommended place), then the repository `skills-army-hq` itself was vendored from.
  An explicit setting that lacks the checker or `skills/` is an error; no setting at all
  is a `WARN drift check skipped`, never a silent pass.
- Preview / `--status`: every drifted forge-owned skill is a `WARN DRIFTED <name>` line on
  stderr citing the vendored and canonical paths and the re-vendor command; the JSON result
  carries `warnings` and a `drift` block (`ok`, `drifted`, `unrecognized`, `origin`).
- `--apply` with an enabled target and any drifted forge-owned skill is **REFUSED** (exit 2)
  naming the skills and the canonical `skills/` path. Remedy is always the same:
  `intake.py --apply update <name> --source <forge>/skills/<tier>/<name>`, then sync again.
  `--allow-drift` deploys anyway, loudly, and records the drift in the result — a
  disclosed exception for a WIP branch, never a way to silence the checker.

## Runtime dependencies are separate

Copying instructions does not bundle the source repo's tools, config or services.
Record requirements locally using `intake.py --apply prerequisite SKILL "TEXT"`;
list/status and catalog expose them without declaring them satisfied automatically.
Inspect the imported skill before invoking its tools from a neutral working folder.

For XYZ relay skills, use the existing locator and a command-scoped `XYZ_HARNESS`
pointing to a maintained full harness (or the caller's existing `.xyz`). Never point
it at a disposable clone or rewrite global shell startup files. Consult requires
its target repo context. Daily requires its Rebalance context and may contain private
paths; keep imported payloads, source receipts, targets, history and ZIPs out of the
public repo. Missing prerequisites block usability claims, not truthful inventory.
