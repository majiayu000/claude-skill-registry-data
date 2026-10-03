---
name: vendor-stack
description: >-
  Install the full swarm stack into a target repo: vendor the XYZ harness
  (relay/marathon/consult/self-improve + `tick`) into `<target>/.xyz/`, then
  optionally install the PDDA doc-governance runtime (`PROJECT/PDDA.md` +
  `utils/pdda/*.sh`). Both installers self-locate, are idempotent, and register
  the target into their own per-user upgrade registry so a later `xyz-sync` /
  `pdda-sync push` can carry updates forward. Trigger on "/vendor-stack",
  "vendor XYZ (and PDDA) into <repo>", "install the stack / harness + governance
  into <repo>", "set up XYZ and PDDA in this repo", "onboard <repo> to the swarm
  stack". For XYZ only, `relay-automation/xyz-vendor.sh <repo>` is enough — reach
  for this skill when you want the harness AND governance, or want to be asked.
---

# vendor-stack — install XYZ + PDDA into a target repo

Two optional subsystems from one source, one onboarding step. This skill **orchestrates** the two
canonical installers; it does not reimplement them.

- **XYZ harness** — `relay-automation/xyz-vendor.sh` mirrors the harness into
  `<target>/.xyz/` (a complete, drift-free install: relay, marathon, consult,
  self-improve, `bin/tick`, `skills/`, `test/`). Registers to
  `~/.config/xyz/registry.tsv`.
- **PDDA governance** — Forge's `utils/pdda/pdda-install.sh` drops the doc contract
  (`PROJECT/PDDA.md`) + runnable checks (`utils/pdda/*.sh`) into the target and
  seeds the `PROJECT/**` lifecycle tree. Registers to
  `~/.config/pdda/registry.tsv`.

## Why a skill and not one script

The harness vendor command stays non-interactive. This skill owns the optional
“also install governance” choice and calls Forge's existing installers in sequence.
The harness and governance retain separate target registries and installed paths.

## Preconditions

- You are standing in (or can point at) an **XYZ Forge** clone — this
  skill ships inside it at `skills/4-occasional/vendor-stack/`, so it resolves the harness
  root from its own location. `bin/tick` and `src/` must be present.
- Use an updated Forge checkout containing `utils/pdda/pdda-install.sh`; no separate PDDA clone is required.
- `bash`, and for PDDA also `node` (its `pdda-lib.sh` shells to node for JSON).
- The target repo directory exists. It need not be a git repo, but both
  installers add machine-local paths (`.xyz/`, PDDA activity logs) to its
  `.gitignore`, so a git repo is the normal case.

## Procedure

### 1. Resolve the Forge source

The harness root is this skill's grandparent dir (`skills/4-occasional/vendor-stack/../..`).
Resolve the PDDA distribution source with the shipped resolver — never hardcode a path:

```bash
HARNESS="$(cd "$(dirname "$0")/../.." && pwd)"        # or: git rev-parse --show-toplevel from a harness clone
PDDA="$(skills/4-occasional/vendor-stack/find-pdda.sh --root)"     # exits non-zero if unresolved
```

`find-pdda.sh` uses an explicit `$PDDA_REPO`/`$PDDA_HOME` override or this
skill's owning Forge tree. A stale override is an error, never a silent fallback.
`--check` reports the resolved source. An ordinary governance-only target is not a source.

### 2. Vendor the XYZ harness (always)

```bash
"$HARNESS/relay-automation/xyz-vendor.sh" /abs/path/to/target-repo
```

This is idempotent: re-running re-mirrors and re-stamps `<target>/.xyz/VERSION`.
It also gitignores `.xyz/` and writes the XYZ registry row.

### 3. Ask about PDDA

Ask the user plainly: **"Also install PDDA doc-governance into this repo?"** —
XYZ is the harness; PDDA is an opt-in governance layer that not every
repo wants. Default to **yes** for repos that will carry `PROJECT/**` docs and a
roadmap; skip for a throwaway or a repo that already has its own doc contract.
If PDDA did not resolve in step 1, say so and proceed XYZ-only.

### 4. Install PDDA (if the user said yes)

```bash
"$PDDA/utils/pdda/pdda-install.sh" /abs/path/to/target-repo          # observe mode, idempotent, self-registers
```

Prefer the **no-flag** form on first install: it installs in `observe` mode
(report-only, non-destructive) and never clobbers existing seeds. Do **not** pass
`--force` (it overwrites seed ledgers and startup-doc scaffolds). Pass
`--with-startup-docs` only if the target wants the ROUTER/AGENTS scaffold and
does not already have its own. Re-running later upgrades in place.

### 5. Check and prompt for `ROUTER.md` updates (GH-353)

After vendoring or updating XYZ in `<target-repo>`:

Run the router roadmap audit check:
```bash
python3 "$HARNESS/utils/py/router_audit.py" --check /abs/path/to/target-repo
```

If `ROUTER DRIFT` is reported:
The LLM MUST inspect the reported mode (or `--json` output) and prompt the user for confirmation before modifying the target repository's `ROUTER.md`:
- **If releases mode is active (`releases.db` or `ROADMAP_SOURCE=releases`):**
  > *"The target repository `<target-repo>` has releases mode enabled (`releases.db`), but its `ROUTER.md` still lists `ROADMAP.md` as active instead of frozen. Would you like me to update `ROUTER.md` to mark `ROADMAP.md` as frozen and reference `releases_app.py roadmap list` and `releases.db`?"*
- **If legacy mode is active (no releases DB):**
  > *"The target repository `<target-repo>` is in legacy roadmap mode, but its `ROUTER.md` references releases-mode directives (`releases_app.py roadmap list` or frozen `ROADMAP.md`). Would you like me to update `ROUTER.md` to restore active `ROADMAP.md` instructions?"*

Upon user approval:
```bash
python3 "$HARNESS/utils/py/router_audit.py" --fix /abs/path/to/target-repo
```

### 6. Verify

```bash
cd /abs/path/to/target-repo
./.xyz/bin/tick --help >/dev/null && echo "tick OK"        # XYZ runnable
grep -qx '.xyz/' .git/info/exclude && echo ".xyz excluded (repo-local, GH-642)"
utils/pdda/pdda.sh run && echo "PDDA runs"                  # only if PDDA installed
```

Then confirm the registry rows landed (this is the "called home" proof):

```bash
grep -F "$(cd /abs/path/to/target-repo && pwd)" ~/.config/xyz/registry.tsv
grep -F "$(cd /abs/path/to/target-repo && pwd)" ~/.config/pdda/registry.tsv   # if PDDA installed
```

## Upgrades (the "call home" payoff)

Each tool registered the target into its own machine-local registry, so future
updates are pull-based and per-tool — you never re-run this skill to upgrade:

- **XYZ:** `relay-automation/xyz-sync.sh check --all` (reports harness drift and `ROUTER.md` drift),
  `xyz-sync.sh update <target>/.xyz` (re-vendor a pinned copy).
  When `ROUTER DRIFT` is flagged during checks or updates, prompt the user before running `router_audit.py --fix`.
- **PDDA:** from the Forge clone, `utils/pdda/pdda-sync.sh status`,
  `pdda-sync.sh push [<target>]` (push the canonical runtime to registered
  targets; only advances files that genuinely changed).

Registries are per-user, per-device, and never committed. `XYZ_REGISTRY` /
`PDDA_REGISTRY` relocate them; `--no-register` on either installer skips the row.

## Notes & guardrails

- **Idempotent / re-runnable.** Both installers upgrade in place; re-running the
  skill on an already-onboarded repo is safe.
- **Independent failure.** XYZ installing does not depend on PDDA and vice versa.
  A missing governance installer is reported explicitly; XYZ-only remains available.
- **Non-destructive PDDA default.** First PDDA install is `observe` mode; it will
  not move stale docs or block. Enforcement is opt-in later.
- **Discoverability.** This skill lives in the repo's `skills/` (which Claude Code
  does not auto-scan). Run `skills/4-occasional/vendor-stack/install.sh` once to symlink it
  into `~/.claude/skills/` — same pattern as `relay-xyz`.
