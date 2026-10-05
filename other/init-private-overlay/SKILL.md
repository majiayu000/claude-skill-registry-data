---
name: init-private-overlay
description: Use when creating or initializing a new ~/.wlrenv-private overlay repo for private/work config in the wlrenv environment, or when wlr-nix-rebuild or wlr-sync-dotfiles break because the private overlay exists but is missing its flake.nix or is otherwise incompletely structured.
---

# Initialize a wlrenv private overlay repo

## Overview

`~/.wlrenv-private` is an optional overlay repo that extends the public `.wlrenv`
environment with private/work config — extra packages, dotfiles, scripts, and
pointers to secrets — that can't live in the public repo. The public `flake.nix`
exports `lib.mkHomeConfiguration` and `lib.overlays` specifically so an overlay
can extend it.

**Critical:** the orchestration scripts key off the _directory existing_, not off
it being complete. If `~/.wlrenv-private` exists but lacks a working `flake.nix`,
`wlr-nix-rebuild` switches its flake root to `~/.wlrenv-private#default` and
**fails** — a half-initialized overlay is worse than none. Land every REQUIRED
file below before stopping.

## When to use

- Setting up a private/work overlay on a new machine.
- `wlr-nix-rebuild` fails with the flake path pointing at `~/.wlrenv-private`.
- The overlay dir exists but holds only e.g. `dotfiles/` + `.allowed_signers`
  (no `flake.nix`) — the rebuild-breaking state.

Do NOT use for public, machine-agnostic config (that belongs in `.wlrenv`), or
for secrets (those go in pass/passage via `secwrap`, never in any repo).

## Target layout

```
~/.wlrenv-private/
├── flake.nix          # REQUIRED — extends public via wlrenv.lib.mkHomeConfiguration
├── flake.lock         # REQUIRED — commit it; pins `wlrenv` (the rev is only used by standalone `nix`; rebuild overrides the input)
├── private.nix        # REQUIRED — your home-manager module (the extraModules content)
├── .gitignore         # REQUIRED — at least `rendered`
├── .allowed_signers   # for auto-updates: the overlay's OWN signing key(s)
├── dotfiles/          # optional — private dotfiles (shadow/patch the public chain)
├── bin/<category>/    # optional — private scripts (MUST sit in a subdir)
└── hooks/post-upgrade # optional — executable; runs after the public hook
```

## Steps

1. **Create the repo:** `git init ~/.wlrenv-private` (or clone an empty private
   remote into that path).
2. **Set the update remote:** `git -C ~/.wlrenv-private remote add origin <url>`.
   `wlr-check-update` reads `origin` to fetch overlay updates; without it the
   overlay simply isn't auto-updated.
3. **Add `.allowed_signers`** with the public half of the key you sign the
   _private_ repo's commits with — same format as the public repo's
   `.allowed_signers`; it may be a different key. Without it, `wlr-check-update`
   refuses to update the overlay.
4. **Copy the templates** from this skill (`templates/`) and edit:
   `flake.nix` → `flake.nix`, `private.nix` → `private.nix`,
   `gitignore` → `.gitignore`.
5. **Disable fsmonitor:** `git -C ~/.wlrenv-private config --local core.fsmonitor false`
   (matches the public repo — fsmonitor's `.ipc` socket breaks Nix `path:`
   evaluation of the flake).
6. **`git add` everything.** Nix ignores files not tracked by git in a directory
   flake, so an untracked `flake.nix`/`private.nix` is _invisible_ and rebuild
   fails as if it were missing. Staging is enough — you don't have to commit yet.
7. **Generate the lock:** `nix flake lock`, then `git add flake.lock`. Heads-up:
   plain `nix flake lock` fetches the pinned `wlrenv` rev from GitHub — it does
   NOT honor the rebuild's input override, so it needs network and the rev
   pushed. Do not use `nix flake lock --override-input` to generate a persistent
   lock: `--override-input` implies `--no-write-lock-file`.
8. **Build:** `wlr-nix-rebuild`. It resolves the public checkout's committed HEAD
   once and uses `git+file://$WLR_ENV_PATH?rev=$public_rev` for both tool launchers
   and `--override-input wlrenv`. **Commit public changes before rebuilding**;
   public working-tree edits are excluded. No private input bump, lock update,
   or commit is required when the public revision changes. Private tracked
   working-tree edits still apply; stage new private files first. The override
   permits in-memory lock updates without writing the private lock file; do not
   add `--no-update-lock-file`. Two warnings are expected while private files
   are staged-but-uncommitted — `Git tree … is dirty` and
   `not writing modified lock file` — both harmless. Success is **exit code 0**;
   a trailing "systemd session is degraded / failed services" block printed by
   Home Manager activation may just be pre-existing, unrelated units, so judge
   by the exit code, not by that block.
9. **If you added `dotfiles/`,** run `wlr-sync-dotfiles`.
10. **Commit, signed** (the repo verifies signatures across machines; see the
    user's commit-signing rules).

## Templates

- `templates/flake.nix` — overlay flake. Input named `wlrenv` (the name is
  required; rebuild overrides it to the local committed public HEAD). Output
  `homeConfigurations.default = wlrenv.lib.mkHomeConfiguration { extraModules = [ ./private.nix ]; }`.
  Darwin config is passed through unextended.
- `templates/private.nix` — example module: extra packages, `home.uvTools.<name>`,
  `custom.krewPlugins`, per-host gating.
- `templates/gitignore` — ignores `rendered/` (private dotfile renders) + build
  artifacts.

> **Stale doc warning:** `docs/plans/2025-12-24-private-config-design.md` shows an
> older flake using `extendModules` / `homeConfigurations."<user>"`. That form is
> **out of date** — the current public flake exposes `homeConfigurations.default`
> and `lib.mkHomeConfiguration`. Use the template, not that doc's snippet.

## Overlay surfaces (how the environment consumes the overlay)

| Surface  | Mechanism                                                                                                                                                                 |
| -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Nix      | `wlr-nix-rebuild` uses the overlay as flake root, builds `#default`, overrides input `wlrenv`→local committed public HEAD. Add config via `private.nix`.                  |
| Dotfiles | `wlr-sync-dotfiles`: `dotfiles/$path` shadows public; `patches/global/…`, then `patches/uname/$(uname)/…`, then `patches/host/$HOSTNAME/…` layer onto public files; output goes to `rendered/`. |
| PATH     | `env.bash` adds each _immediate subdir_ of `bin/` to PATH. Scripts directly in `bin/` are NOT added — use `bin/<category>/`.                                              |
| uv tools | `private.nix` sets `home.uvTools.<name> = { … }` to add/override; `.disabled = true` suppresses a public tool.                                                            |
| Updates  | `wlr-check-update` fetches `origin`, verifies the new HEAD against the overlay's own `.allowed_signers` (read _before_ fetch), then runs `hooks/post-upgrade` if present. |
| Secrets  | NOT in the repo — `secwrap` + pass/passage. See `docs/plans/2025-12-24-private-config-design.md`.                                                                         |

## Gotchas

- **Half-initialized overlay breaks rebuild.** Dir exists → rebuild targets it.
  Always land a working `flake.nix` + `flake.lock`.
- **Untracked = invisible to Nix.** `git add` new flake files before rebuilding.
- **Input must be named `wlrenv`.** Rebuild's `--override-input wlrenv …` depends
  on the exact name.
- **bin scripts need a subdir** to land on PATH.
- **macOS:** private _home_ config applies (via `homeConfigurations.default`);
  private _system_ config does not (darwin is passed through). Extending darwin
  system config needs more than the current public `lib` exposes.
- **fsmonitor off** on the overlay repo, or Nix `path:` evaluation can choke on
  the daemon socket.
