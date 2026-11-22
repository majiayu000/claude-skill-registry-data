---
name: re-vendor-xyz
description: >-
  Refresh ONE repository's existing vendored XYZ Forge copy (`<repo>/.xyz/`) safely and report
  plainly whether it worked: checks the Forge source is published code, refuses while a relay,
  marathon or Jog run uses that copy, keeps the RELEASES tier, backs the copy up, refreshes it
  through `relay-automation/xyz-sync.sh`, verifies it on three conditions rather than an exit
  code, then hands deployed-skill drift to Skills Army HQ. Trigger on "/re-vendor-xyz",
  "re-vendor", "re-vendor the overlay", "refresh the .xyz copy", "update the vendored harness",
  "pull the new XYZ tooling into <repo>". NOT for a first install into a repo with no `.xyz/`
  (use /vendor-stack) and NOT for refreshing every vendored repo at once (that is the bare
  `xyz-sync.sh update --all`).
---

# re-vendor-xyz — refresh one vendored `.xyz/` copy

Every repository that uses XYZ Forge keeps a private, git-ignored copy of the Forge tools in
`<repo>/.xyz/`. A Forge fix reaches that repository only when someone on that machine refreshes
the copy. The refresh commands already exist (`relay-automation/xyz-sync.sh`, which calls
`xyz-vendor.sh`); this skill runs them in a safe order, because on their own they can report
success while the copy is stale, built from unpublished code, or swapped out under a live run
(GH-1486; the live-run failure is #1011).

This skill adds no script. It is one copy-paste shell block (steps 1–8), one read-only status
block (step 9) and a report (step 10).

## The only reasons to stop

These are the only stops. Each prints `re-vendor-xyz: stopped: <reason>` with the output that
caused it, and the block exits `3`. Anything not on this list continues.

1. The Forge source cannot be found, or is not a Forge git checkout (it must be the top of a git
   repository, not a folder named `.xyz`, and contain `relay-automation/xyz-sync.sh`).
2. The Forge source is on a detached HEAD or a branch not in `XYZ_SYNC_CANONICAL_BRANCHES`
   (default `main,development`).
3. The Forge source has uncommitted changes.
4. `git fetch` of the source branch fails.
5. The Forge source cannot fast-forward to `origin/<branch>`, or after doing so its `HEAD` is not
   `origin/<branch>` (it carries unpublished commits).
6. The target repository is missing, is the Forge checkout itself, or has no `present` row for
   `<target>/.xyz` in `xyz-sync.sh list` (first install is `/vendor-stack`).
7. A relay or marathon driver lock exists for the copy (`<target>/.xyz/.relay-driver.lock`) or for
   the repository (`.git/relay-driver.lock`, as resolved by `relay-automation/driver-lock-lib.sh`).
   A lock left behind by a crashed run also stops; never remove it here, use the relay's own
   recovery.
8. A process is running from `<target>/.xyz/`.
9. The copy is tier 2 (RELEASES overlay) and `<target>/releases.db` does not exist, so the refresh
   would silently drop the overlay.
10. The backup zip is missing or empty.
11. `xyz-sync.sh update` fails, or the copy is not current afterwards (see the current test below).

A copy is **current** only when all three hold: `xyz-sync.sh check "<target>/.xyz"` prints the
whole line `ok    <target>/.xyz`; it prints no `SAFETY GUARD MISSING <target>/.xyz (…)` line;
and `source_commit=` in `<target>/.xyz/VERSION` equals the Forge `HEAD`. `check` reads the
registry, so the third condition is the one that looks at the copy itself. An `ok` line alone is
never success.

## Before you run it

- **Target.** The repository whose `.xyz/` is being refreshed: the one named in the request, else
  the repository the session is in when that is not the Forge checkout. If more than one could be
  meant, ask which. Use its absolute path.
- **Forge source.** Found automatically from `XYZ_FORGE_ROOT`, else the `canonical` entry in the
  Skills Army HQ `targets.json` (collection `XYZ_SKILLS_ROOT`, else `~/git-pulse-sync/Deployed
  Skills`). If neither is set, ask the operator for their XYZ-forge checkout path. Do not use
  `find-hq.sh` for this: from a vendored copy it finds the `.xyz/` folder, not Forge.
- A behind Forge checkout is fast-forwarded to `origin/<branch>` in step 2. Nothing is stashed,
  reset or discarded.
- Run the whole block in **one** shell call; variables do not survive between calls. In Claude
  Code, run it outside the Bash sandbox (the fetch needs the network and keychain).

## Steps 1–8: check, back up, refresh, verify

Set `T` (and `FORGE` if you already know it), then run this block as one command:

```bash
T="/absolute/path/to/target-repo"   # required
# FORGE="/absolute/path/to/XYZ-forge"   # optional; found automatically otherwise
bash -s -- "$T" "${FORGE:-}" <<'RE_VENDOR_XYZ'
set -u
T="$1"; FORGE="${2:-}"
stop() { printf 're-vendor-xyz: stopped: %s\n' "$*"; exit 3; }

# 1. Find the Forge source.
SKROOT="${XYZ_SKILLS_ROOT:-$HOME/git-pulse-sync/Deployed Skills}"
[ -n "$FORGE" ] || FORGE="${XYZ_FORGE_ROOT:-}"
if [ -z "$FORGE" ] && [ -f "$SKROOT/targets.json" ]; then
  FORGE="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1])).get("canonical") or "")' "$SKROOT/targets.json" 2>/dev/null || true)"
fi
[ -n "$FORGE" ] || stop "Forge source not found: set XYZ_FORGE_ROOT to your XYZ-forge checkout"
RAW="$FORGE"
FORGE="$(cd "$FORGE" 2>/dev/null && pwd -P)" || stop "Forge source not found: $RAW"
[ "$(git -C "$FORGE" rev-parse --show-toplevel 2>/dev/null)" = "$FORGE" ] || stop "not the top of a git checkout: $FORGE"
[ "$(basename "$FORGE")" != ".xyz" ] || stop "Forge source is a vendored .xyz copy, not a Forge checkout: $FORGE"
SYNC="$FORGE/relay-automation/xyz-sync.sh"
[ -x "$SYNC" ] || stop "not a Forge checkout (no relay-automation/xyz-sync.sh): $FORGE"

# 2. The source must be published code.
BR="$(git -C "$FORGE" symbolic-ref --short -q HEAD)" || stop "Forge source is on a detached HEAD"
case ",${XYZ_SYNC_CANONICAL_BRANCHES:-main,development}," in
  *",$BR,"*) ;;
  *) stop "Forge source branch '$BR' is not canonical (${XYZ_SYNC_CANONICAL_BRANCHES:-main,development})" ;;
esac
DIRTY="$(git -C "$FORGE" status --porcelain --untracked-files=normal)"
[ -z "$DIRTY" ] || stop "Forge source has uncommitted changes:
$DIRTY"
FETCH="$(git -C "$FORGE" fetch origin "$BR" 2>&1)" || stop "fetch of origin/$BR failed:
$FETCH"
git -C "$FORGE" merge --ff-only --quiet "origin/$BR" 2>&1 || stop "Forge source cannot fast-forward to origin/$BR (it has commits origin does not)"
HEAD="$(git -C "$FORGE" rev-parse HEAD)"
[ "$HEAD" = "$(git -C "$FORGE" rev-parse "origin/$BR")" ] || stop "Forge source HEAD $HEAD is not origin/$BR: it carries unpublished commits:
$(git -C "$FORGE" log --oneline "origin/$BR..HEAD")"
echo "re-vendor-xyz: Forge source $FORGE on $BR at $HEAD"

# 3. The target must be a registered vendored copy.
T="$(cd "$T" 2>/dev/null && pwd -P)" || stop "target repository not found: $1"
[ "$T" != "$FORGE" ] || stop "target is the Forge checkout itself: $T"
X="$T/.xyz"
"$SYNC" list | P="$X" awk '$1 == "present" && substr($0, length($0) - length(ENVIRON["P"])) == " " ENVIRON["P"] { found = 1 } END { exit !found }' \
  || stop "$X has no present row in xyz-sync.sh list; for a first install use /vendor-stack"

# 4. Nothing may be running from this copy.
[ ! -e "$X/.relay-driver.lock" ] || stop "a driver lock is held: $X/.relay-driver.lock (wait for the run; if it crashed, use the relay's own recovery)"
L2="$(bash -c '. "$1"; driver_lock_path_for_repo "$2"' _ "$FORGE/relay-automation/driver-lock-lib.sh" "$T")"
[ -z "$L2" ] || [ ! -e "$L2" ] || stop "a driver lock is held: $L2 (wait for the run; if it crashed, use the relay's own recovery)"
PROCS="$(ps -axo pid=,command= | P="$X/" ME="$$" PARENT="$PPID" awk 'index($0, ENVIRON["P"]) && $1 != ENVIRON["ME"] && $1 != ENVIRON["PARENT"]')"
[ -z "$PROCS" ] || stop "processes are running from $X/:
$PROCS"

# 5. Keep the RELEASES tier.
TIER="$(sed -n 's/^tier=//p' "$X/VERSION" 2>/dev/null)"
[ "$TIER" != "2" ] || [ -f "$T/releases.db" ] || stop "$X is tier 2 but $T/releases.db is missing; a refresh would drop the RELEASES overlay"
[ "$TIER" = "2" ] || [ ! -f "$T/releases.db" ] || echo "re-vendor-xyz: note: $T has releases.db, so this refresh makes the copy tier 2"

# 6. Current test: all three conditions, never the exit code alone.
current() {
  OUT="$("$SYNC" check "$X" 2>&1)"
  printf '%s\n' "$OUT"
  printf '%s\n' "$OUT" | grep -Fxq -- "ok    $X" || return 1
  if printf '%s\n' "$OUT" | grep -Fq -- "SAFETY GUARD MISSING $X ("; then return 1; fi
  [ "$(sed -n 's/^source_commit=//p' "$X/VERSION" 2>/dev/null)" = "$HEAD" ]
}
if current; then
  echo "re-vendor-xyz: already current at $HEAD; no backup, no refresh"
  exit 0
fi

# 7. Back up the copy being replaced (not the registry or ignore files).
BK="${XDG_STATE_HOME:-$HOME/.local/state}/xyz/backups"
mkdir -p "$BK" || stop "cannot create backup folder $BK"
ZIP="$BK/$(basename "$T")-$(date -u +%Y%m%dT%H%M%SZ).zip"
(cd "$T" && zip -qry "$ZIP" .xyz) || stop "backup failed: $ZIP"
[ -s "$ZIP" ] || stop "backup missing or empty: $ZIP"
echo "re-vendor-xyz: backup: $ZIP"

# 8. Refresh through the existing writer, then verify.
echo "re-vendor-xyz: running: xyz-sync.sh update $X"
"$SYNC" update "$X" 2>&1 || stop "xyz-sync.sh update failed (backup: $ZIP)"
current || stop "refresh did not verify as current (backup: $ZIP)"
echo "re-vendor-xyz: refreshed $X to $HEAD (backup: $ZIP)"
RE_VENDOR_XYZ
rc=$?; echo "re-vendor-xyz: exit $rc"; (exit "$rc")
```

The whole command returns the block's status and also prints it as `re-vendor-xyz: exit <n>`:
`0` means current (already, or after the refresh); `3` is one of the stops above. Continue to
step 9 only after `0`.
Repeat any `ROUTER DRIFT` line and any `xyz-vendor.sh: WARNING` line from the output to the
operator verbatim. Do not run `router_audit.py --fix` unless asked (same rule as `/vendor-stack`).
On a stop, report the stop line and its output and do nothing else for this target.

## Step 9: deployed skills (read-only check, then hand off)

Agents load skill text from the Skills Army HQ collection, not from `.xyz/skills/`, so a refreshed
copy does not refresh the instructions a new session reads. After exit `0`, set `FORGE` to the
path step 1 printed and run:

```bash
FORGE="/absolute/path/printed/in/step/1"
SKROOT="${XYZ_SKILLS_ROOT:-$HOME/git-pulse-sync/Deployed Skills}"
if [ -d "$SKROOT" ]; then
  python3 "$SKROOT/skills-army-hq/scripts/sync.py" --root "$SKROOT" --status --canonical "$FORGE"
else
  echo "re-vendor-xyz: no Skills Army HQ collection on this machine; skipping deployed skills"
fi
```

This only reads. For each Forge skill it reports `DRIFTED`, hand off to `/skills-army-hq` and
follow its own preview-then-apply procedure with `--source "$FORGE/skills/<tier>/<name>"`. Pass
`--canonical "$FORGE"` everywhere: without it Skills Army can fall back to a stale checkout and
downgrade skills. Repeat its warnings. This skill never writes the collection itself and never
adds a skill that is not already deployed.

## Step 10: report

In plain words: the Forge commit vendored (or "already current"), the `check` lines for
`<target>/.xyz`, the backup path, the deployed-skill result from step 9, and that agent sessions
already open keep the old skill text until they are restarted.

## Never

- Commit or push anything in the target repository.
- Touch any other vendored copy, or use `--all`.
- Set `XYZ_SYNC_ALLOW_UNSAFE_SOURCE`, stash, reset, discard, or remove a lock to get past a stop.
- Edit files under `.xyz/` by hand: the copy is replaced as a whole on every refresh, and the
  backup zip is the only way back to what was there.

Recovery, only when the operator asks for it and nothing is running from the copy (re-check
steps 3 and 4 first). Use absolute paths throughout, and never delete the live copy before the
backup is proven:

1. Confirm the zip is the one this skill reported and test it: `unzip -tq "<zip>"`.
2. Extract it into a new, empty staging folder outside the target and check that it contains
   `.xyz/VERSION`.
3. Rename the current `<target>/.xyz` aside (for example to `<target>/.xyz.before-restore-<UTC>`),
   then move the staged `.xyz` into `<target>`. Keep the renamed copy until the operator has
   checked the result.

Restoring returns relay threads and tick logs under `.xyz/` to their state at backup time. The
registry row keeps the new commit until the next refresh.
