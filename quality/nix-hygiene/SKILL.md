---
name: nix-hygiene
description: >
  Audit and fix this nix-config mono-repo for LEAN/DRY/modular/atomic quality:
  abandoned surface, doc drift, host-scope mistakes, anti-patterns, comment
  rot. Use when asked to "hygiene", "cleanup the repo", "LEAN/DRY pass",
  "audit modularity", "remove bloat", "align with CLAUDE.md", or keep
  nix-darwin/home-manager patterns clean. Composes git-purity, nix fmt,
  flake check, and optional domain doctors — not a substitute for /eval alone.
---

# nix-hygiene

**Floor (already automated):** `nix fmt` / treefmt (nixfmt + statix + deadnix),
ast-grep structural lint (`checks.<system>.ast-grep`), Stop gate + `/eval`
(`git add` → `nix flake check`), CI `nix-ci.yml`.

**The ast-grep floor is SIX rules, and every one `severity: error` — a match FAILS the
build, it is not a review finding.** "Report-only" means only that it never rewrites a
file (unlike treefmt); see `sgconfig.yml`. `ls ast-grep/rules/` is the authoritative
inventory — re-read it each pass rather than trusting this list, which has drifted before:

| Rule (`ast-grep/rules/<id>.yml`) | Catches |
|---|---|
| `nix-hardcoded-home-path` | `/Users/<name>` or `/home/<name>` inside a Nix **string** (a `users.users.<n>.home` declaration is exempt by shape) |
| `launchd-bare-interpreter-arg0` | `Program`/`ProgramArguments` arg0 ending in `/bin/{sh,bash,python3,node,env,…}` instead of a `nix-<kebab>` wrapper |
| `hook-json-parse-must-be-guarded` | a `JSON.parse` in `.claude/hooks/*.js` that no `try` encloses |
| `capsule-must-not-reach-out` | ANY `..` in a **path literal** under `modules/features/**` — escaping or not. `../module.nix` from a `checks/` leaf stays inside the capsule and still fails: a leaf takes what it needs as an ARGUMENT |
| `home-must-not-cross-layers` | `modules/home/` reaching UP via `..` into `features`/`parts`/`hosts`/`infra` |
| `activation-must-not-touch-secrets` | an `activation*` binding naming `secrets-{rehydrate,push,resolve,status}` or `gcloud {secrets,auth}` (ADR-004) |

**This skill:** judgmental hygiene — architecture, host scope, docs↔code,
abandoned experiments, comment rot — then **fix** and **re-gate**.

Canonical conventions + the path index: root [`CLAUDE.md`](../../../CLAUDE.md) (kept lean —
under the 40k context-lint limit). The **full** fleet map lives in
[`docs/map/`](../../../docs/map/) — eleven per-domain files behind the
[`docs/repo-map.md`](../../../docs/repo-map.md) index — with
[`docs/secrets-and-keychain.md`](../../../docs/secrets-and-keychain.md) for the secrets surface.
([`docs/mcp-gateway.md`](../../../docs/mcp-gateway.md) used to be the third — it is **history**
since 2026-10-02: the MCP gateway, `modules/shared/mcp.nix` and the Cloudflare portal are all
deleted. MCP now lives entirely in plugin `.mcp.json` files outside this repo, so there is no MCP
surface here to audit except the `local.gmailMcp` launcher package.)
Do not restate the fleet map here; open those when unsure — and when repo shape changes, fix
**both** the CLAUDE.md one-liner and the `docs/map/` section the index routes it to.

## When to use

| Trigger | Mode |
|---|---|
| "hygiene" / "LEAN DRY" / "cleanup" | Full or scoped pass |
| After a large feature | Scoped to touched paths |
| Before a big PR merge | Full pass + a manual diff review |
| Docs feel wrong | Docs-surface only |

**Not for:** pure "does it evaluate?" → `/eval`. Pure PR review without fix → a manual diff review (no dedicated command exists in this repo — see §H).

## Modes

Parse the user request:

1. **`audit`** — findings only (no edits). Triggered when they say "audit" / "report".
2. **`fix`** — audit → apply safe fixes → format → eval. **The overall default** when neither `audit` nor a scope-only request is given.
3. **`scope <path|host|area>`** — limit to that surface (e.g. `packages/`, `docs/`).

Never expand into new features. Prefer delete/simplify over new abstraction.

## Path → responsibility map

| Path | Owns | Typical flake output |
|---|---|---|
| `flake.nix` / `flake.lock` | inputs/pins and ONE `mkFlake` call — nothing else | — |
| `modules/parts/` | the flake ENGINE: `mkDarwin`/`mkNixos`, apps, checks, identity | all |
| `hosts/<name>.nix` | host-only deltas | `darwinConfigurations` / `nixosConfigurations` |
| `modules/home/` | cross-host HM + shared options | both |
| `modules/darwin/` | macOS system | `darwinConfigurations` |
| `modules/nixos/` | NixOS system | `nixosConfigurations` |
| `packages/` | flake apps/packages | `packages` / `apps` |
| `docs/` | runbooks | — |
| `.claude/` | agent skills/commands/hooks | — |
| `infra/` | terranix | `apps` (cf-*, gcp-*; the `mcp-public-*` apps were deleted 2026-10-02) |
| `secrets/` | agenix recipients + ciphertext | — |

**Platform branching:** `lib.mkIf` in `modules/`, not copy-paste across hosts.
**Host gates:** `networking.hostName` / `osConfig` for per-host divergence.

## Checklist (run in order)

### A. Surface inventory

- [ ] `git status` — no surprise WIP; stage only intentional hygiene.
- [ ] Touched/scope files still match the CLAUDE.md + `docs/map/` story (no orphan
      modules, no path whose one-liner and map section disagree).
- [ ] Flake apps in `modules/parts/packages.nix` have matching `packages/*` and runbook mentions if user-facing.
- [ ] Reverse: runbooks mention only apps/paths that still exist.

### B. LEAN / abandoned

- [ ] Experimental dual paths (e.g. old and new sshd) collapsed to one.
- [ ] Commented-out blocks with no near-term intent removed or ticketed in `memory/` (gitignored).
- [ ] Dead options, unused `let` bindings (deadnix/statix will catch some — don't rely only on them).
- [ ] Vendor copies justified with a one-line "why not upstream" comment — and re-checked
      each pass, because the justification expires. The last one, `hm-launchd` (560 lines of
      forked home-manager), was RETIRED 2026-09-14 once the pinned input grew the three
      options it needed. That is the outcome to aim for, not a permanent fork.

### C. DRY / modular / atomic

- [ ] One path for one fact (e.g. the `~/Downloads` path shape shared conceptually host/guest).
- [ ] No host-specific lists in shared modules without `mkIf` / hostName / `isMacosHost`.
- [ ] Launchd BTM basenames: `nix-<activity>` via `mkNixAgent` (`modules/darwin/core.nix`) or
      `modules/home/launchd-launcher.nix` for HM agents (never bare `sh`/`open`).
- [ ] Secrets: never plaintext in `.nix`; agenix vault vs Keychain rules unchanged.

### D. Comments & docs

- [ ] Comments explain **why**, not restate the code.
- [ ] Remove "we tried X then Y" experiment narratives unless they prevent a known footgun (one sentence max).
- [ ] `docs/*-runbook.md` and skill frontmatter match current commands.
- [ ] CLAUDE.md skill/command lists (§ Navigating the Codebase) include this skill after add,
      and `docs/map/claude.md` describes it.

### E. Community patterns

- [ ] **Upstream-first back-stop.** Every custom shim (`home.file`/`home.activation` used as a
      workaround, an activation script, a "make X see Y" wrapper, a symlink farm) carries a
      one-line justification that the pinned input was grepped and owns no equivalent option —
      per [`.claude/rules/upstream-first.md`](../../rules/upstream-first.md). For a CLI or
      wrapper, that justification must ALSO cover the tool axis (rule § Step 2): an option
      grep cannot see a PACKAGE, so check what this repo already installs and what nixpkgs
      ships. `nh` owning `--elevation-strategy` while already on PATH is the worked example.
      Re-run the grep
      for any that don't; inputs gain options between bumps, so a shim that was justified at
      write time can be obsolete now. Resolve the pinned source, don't read upstream HEAD:
      `src=$(nix eval --raw --impure --expr 'builtins.toString (builtins.getFlake "'"$PWD"'").inputs.nix-darwin.outPath')`
      then `grep -rn "<concept>" "$src/modules/"`.
- [ ] `writeShellApplication` for scripts; shellcheck via that path.
- [ ] No new `environment.etc` hacks for things nix-darwin models.
- [ ] Determinate Nix (darwin): no `nix.enable = true` / no hand-written `nix.custom.conf`. On the NixOS hosts the nixosModule keeps `nix.*` live, so `nix.settings` there is correct, not drift.
- [ ] **flake-parts everywhere, including here.** The small supporting flakes that
      remain (any new one — the last existing member, ircc-whatsapp-bot, was
      unwired on 2026-09-12) use flake-parts,
      not hand-rolled `forAll`/`forAllSystems` boilerplate — ADR-001
      (`docs/flake-architecture-strategy-adr.md`). `nix-mcp-gateway` used to be on
      this list and is **archived** (2026-09-12, an unadopted extraction candidate —
      the fleet's own gateway was `modules/shared/mcp.nix`, itself **deleted 2026-10-02**, so
      neither exists now); do not re-add either from memory. A new one scaffolded without it,
      or an old hand-rolled pattern creeping back in via copy-paste, is a finding.
      **`nix-config`'s own engine is no longer the exception.** ADR-001 §2 said
      "do not migrate the core engine"; ADR-002
      (`docs/monoflake-capsule-adr.md`) superseded that and wave 2 did the
      migration, so a surviving `forAllSystems` fold or a new `genAttrs systems`
      in this repo IS hygiene debt now. The engine is `modules/parts/*.nix`,
      one flake-parts module per concern, discovered by `import-tree`.
- [ ] **Capsule boundary.** Anything under `modules/features/<name>/` is a capsule:
      `flake-module.nix` is the only file outside code may import, and no file in
      the directory may hold a `..` path literal — **including one that escapes
      nothing**, like a `checks/` leaf reaching `../module.nix`; the entry file
      passes that DOWN as an argument instead. That is enforced by
      `ast-grep/rules/capsule-must-not-reach-out.yml` + `checks.<system>.capsule-registry`,
      so a violation is a build failure, not a review finding — but a capsule that
      smuggles a value out through `specialArgs`, an overlay, or a runtime-built
      store path is invisible to both gates (ADR-002 §7.6) and IS a finding here.
      Never widen the seam to make red go green; add a typed engine seam
      (`fleet.*` in `modules/parts/`) instead.

### F. Mechanical gate (mandatory after fixes)

```bash
git add -A
nix fmt
git add -A   # fmt may rewrite
git status --porcelain '*.nix'   # clean of ?? 
nix flake check                  # or scoped nix eval of affected toplevels
```

If `nix` unavailable: `nix-instantiate --parse` on changed `.nix` + state CI-deferred.

### G. Domain doctors (only if scope touched)

| Scope | Command |
|---|---|
| nixpi flash/provision | skill `nixpi-firmware-provision` |

### H. Optional second opinions

- Structural harshness: global **code-review** skill on the diff.
- Behavior check after fix: manually drive the change end-to-end (no dedicated command).
- PR findings only: a manual diff review (no dedicated command).

## Fix policy

| Do | Don't |
|---|---|
| Delete dead code and experiment comments | Drive-by renames across the monorepo |
| Gate host-only agents with `hostName` | Add options "for later" |
| Update runbook + skill together | Leave CLAUDE.md lists stale |
| One logical commit, one PR per change | Silent behavior change without note |

**Breaking host behavior** (e.g. removing an agent): say so in the report; prefer `mkIf` off over surprise removal.

## Report format (always end with this)

```markdown
## Hygiene report
- **Mode:** audit | fix
- **Scope:** …
- **Findings:** (bullet: path — issue — action taken or deferred)
- **Gates:** fmt ✅/❌ · flake check ✅/❌ · doctors …
- **Verdict:** CLEAN | FIXED | BLOCKED (why)
```

## Anti-patterns specific to this fleet

1. **A sandbox host inheriting macos login openers / RAG** — hosts stay lean. (The MCP gateway
   used to be the third item here; it was deleted 2026-10-02.)
2. **Guest file-rotation on the shared `~/Downloads`** — host-only (`mv` across
   filesystems = `cp` + `rm`, so a guest rotation destroys host files).
4. **Putting `.utm` / IPSW / disk images in the flake.**
5. **Hand-editing `flake.lock`.**
6. **HM launchd bypassing `launchd-launcher.nix` / without a `nix-*` basename** — BTM phantoms return.

## Compose with existing automation

```
/hygiene [scope]     → this skill (audit+fix+gate)
/eval                → eval only
code-review skill    → structural/PR-diff review (no dedicated /review or /verify command exists)
```
