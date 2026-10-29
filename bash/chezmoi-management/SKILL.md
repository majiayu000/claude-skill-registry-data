---
name: chezmoi-management
description: Dotpkgs package operations and chezmoi workflow skill for Prateek's dotfiles repo. Use for `chezmoi` apply/diff/verify/merge/edit/re-add/forget/status/managed/unmanaged/data/execute-template/doctor; source-target drift; files under `home/.chezmoitemplates/`, `.chezmoiassets/`, `.chezmoiscripts/`, `.chezmoidata/`, or `.chezmoiexternal.*`; package, secret, and license data; Brewfile rendering; app plist capture or modify stubs; chezmoi-owned `DOTFILES_*` gates; 1Password `op://` refs; and mapping `~/.foo` targets to `home/dot_*` sources. Do not use for unrelated dotfile edits, pure shell-startup debugging, or test/VM/harness env vars.
---

# Chezmoi Management

## Overview

Single entry point for chezmoi-related work in Prateek's dotfiles repo. SKILL.md is a router. Mode-specific depth lives in `references/<mode>.md`. Generic chezmoi knowledge lives in `references/chezmoi-cheatsheet.md` so this skill is self-contained and does not depend on chezmoi.io being reachable.

## Trigger Check

Use this skill when any of these are true:

- Running `chezmoi` commands (`apply`, `diff`, `verify`, `merge`, `edit`, `re-add`, `forget`, `status`, `managed`, `unmanaged`, `data`, `execute-template`, `doctor`).
- Editing or adding files under `home/.chezmoitemplates/`, `home/.chezmoiassets/`, `home/.chezmoiscripts/`, `home/.chezmoidata/`, or `home/.chezmoiexternal.*` (zinit and other clone/pull-only dependencies).
- Capturing or modifying macOS app preferences via plist fragments.
- Touching `home/.chezmoidata/{packages,secrets,licenses}.toml` or `brewfile.tmpl`.
- Selecting `machine_type` (the one init prompt, or `chezmoi init --promptChoice 'machine_type=<type>'`) or changing machine behavior via the layered `home/.chezmoidata/machines.toml` (resolved by `features.tmpl`) — package groups, install scripts, macOS defaults, secrets, the work overlay ([ADR 0039](../../../docs/adr/0039-work-overlay-in-work-repo.md)), elevation. Per-machine exceptions go in a host-local `[data].machines_local`.
- Toggling chezmoi-owned apply-time `DOTFILES_*` env vars (MAS, Homebrew tuning, plist hooks, post-apply relaunch, `INSTALL_XCODE` force-download). Full table with effects and out-of-scope test/VM vars in `references/packages-and-secrets.md`.
- Wiring a 1Password `op://` reference.
- Translating between `~/.<file>` and `home/<dot_*>` source paths.

For out-of-scope cases, see "Should not trigger by itself" below.

## Trigger Boundaries

Should trigger:

- `chezmoi diff is showing changes I do not understand. Walk me through them.`
- `I edited ~/.zshrc directly. Get this back into the source tree without losing the template.`
- `Add Anthropic CLI to the base package group and render the Brewfile.`
- `Capture the Moom plist into home/.chezmoitemplates/.`
- `Toggle DOTFILES_INSTALL_MAS_APPS for this run.`
- `What is the source path for ~/.config/karabiner.edn?`
- `Test a chezmoi change from a git worktree, then reset to the default source.`

Should not trigger by itself:

- `Debug why zinit is slow at shell startup.` (Shell startup; no source-state edit.)
- `Write an ADR for the new mise lockfile policy.` (Docs; no chezmoi state.)
- `Add a new skill under agent-marketplace/src/core/skills/.` (Use `agent-skill-management` for portable skill authoring.)
- `Review this PR for unrelated bugs.`

If `code-gardening` already owns a state-sync task and chezmoi is incidental, keep `code-gardening` primary and consult this skill only when a chezmoi command or `home/.chezmoi*/` path enters scope.

## Universal Rules

These apply across every mode. Do not skip them.

1. **Edit the owning source.** Direct chezmoi entries live under `home/`; prefer `chezmoi edit <target>` for those files. Script-created output such as `~/.agents/plugins` has a separate owner. Check `references/source-target-translation.md` before capturing a path that `chezmoi source-path` cannot map.
2. **Always `chezmoi diff` before `chezmoi apply`.** Use `chezmoi apply --dry-run --verbose` for a structural preview, especially when `home/.chezmoiscripts/` changed.
3. **Destructive command discipline.** `forget` stops managing (safe). `destroy` removes source AND target AND state (never use unless the user explicitly asks). `add` on a `.tmpl` clobbers the template with rendered output (never). `re-add` is the right tool for already-managed plain/`encrypted_` files but **SKIPS `.tmpl` sources** — pre-check with `chezmoi source-path <target>`; if it ends in `.tmpl`, skip `re-add` and edit by hand. Full command semantics in `references/chezmoi-cheatsheet.md`.
4. **Files under `home/.chezmoidata/` cannot be templates.** They load before the template engine starts. Dynamic data goes in `home/.chezmoi.<format>.tmpl` or via template functions (`output`, `fromJson`, `fromYaml`).
5. **Validate after editing this skill.** Frontmatter/parser drift has bitten this repo before. See `references/meta-skill-maintenance.md` for the post-edit checklist.

## Package Operations

For package inventory, available updates, pin changes, or install/remove requests,
use `dotpkgs` and read [package operations](references/packages-and-secrets.md#package-operations).
The helper owns package comparisons consumed by the shell banner and audits;
chezmoi remains the configuration/apply surface.

## Mode Router

Route by the file or command in scope. Load the matching reference plus `references/source-target-translation.md` for any path mapping.

| Task touches… | Load |
|---|---|
| `chezmoi apply`, `diff`, `verify`, `merge`, `edit`, `re-add`, `forget`; drift between target and source; `home/.chezmoiscripts/` ordering or hashing | `references/workflow.md` |
| `home/.chezmoitemplates/<bundle-id>.plist.tmpl`; `home/.chezmoiassets/`; capturing macOS app preferences; `modify_` stubs; `home/.chezmoiignore` for opt-in apps | `references/app-config.md` |
| `home/.chezmoidata/{packages,secrets,licenses}.toml`; `brewfile.tmpl`; `DOTFILES_INSTALL_*` env vars; 1Password `op://` references | `references/packages-and-secrets.md` |
| Translating `~/.<file>` ↔ `home/<dot_*>` source paths in any mode | `references/source-target-translation.md` |
| `agent-marketplace/`, `home/.chezmoidata/agent_plugins.toml`, script-created `~/.agents/plugins`, or native plugin activation | [agent-skill-management](../agent-skill-management/SKILL.md); `references/workflow.md` for chezmoi apply scope |
| Cross-cutting chezmoi command lookup, attribute grammar, "what does X do" | `references/chezmoi-cheatsheet.md` |
| Updating this skill itself because chezmoi practices in the repo changed | `references/meta-skill-maintenance.md` |

A single task can pull more than one reference. "Add a new app" hits packages-and-secrets (install rule), then app-config (preferences), then workflow (apply). Load each as you cross the seam.

## Repo-Specific Gotchas (Always Loaded)

These are short, high-stakes, and easy to violate. Keep them in working memory regardless of mode.

- **Plist `{{` / `}}` literals must be escaped.** Plist fragments are Go templates. If a string value contains literal `{{` or `}}` (e.g., Moom geometry like `{{width}}x{{height}}+0+0`), escape it. See `references/app-config.md`.
- **`home/.chezmoiassets/` loads via `include`, not `includeTemplate`.** Use `.chezmoiassets/` for raw payloads that should not be templated. Use `home/.chezmoitemplates/` for Go-templated content loaded via `includeTemplate`.
- **Store only obfuscated `op://vault-id/item-id/field-id` refs in committed files.** Human-readable `op://Personal/...` refs are forbidden in `home/.chezmoidata/secrets.toml` and `licenses.toml`. Per-machine overrides go in `~/.config/chezmoi/chezmoi.toml.local`.
- **Do not reintroduce `home/.chezmoidata/apps/*.toml`.** That mechanism was retired with `bin/dotfiles`. App config now lives at the native target path or as a `modify_` plist stub.
- **MAS entries opt-in via `DOTFILES_INSTALL_MAS_APPS=true`.** Do not unconditionally include MAS apps in `packages.toml`.
- **Setapp apps are declared in `setapp_apps`, not `casks`.** Homebrew cannot install them; `run_after_22-setapp-apps` downloads each app's vendor archive from Setapp's store API and unpacks it (ADR 0024). Add the app there before adding chezmoi-managed config for it.
- **`home/.chezmoiscripts/` numeric ordering is load-bearing.** Insert new scripts at unused gap numbers; do not renumber existing ones. Current ordering listed in `references/workflow.md`.
- **Raw app captures live under `${XDG_STATE_HOME:-~/.local/state}/dotfiles/captures/`, not in the repo.**

## Validation Lanes

Pick the matching lane for the work. All lanes are existing repo conventions; do not invent new validation.

| Mode | Run before declaring done |
|---|---|
| workflow | Keep the diff/verify and script-aware dry-run checks in [workflow](references/workflow.md#validation-before-declaring-done); use the [tests index](../../../tests/README.md#chezmoi-workflow-checks) for apply/status and hook behavior. |
| app-config | Render and parse the changed format, preview its target diff, and select ownership/preservation/security checks through the [app-config tests index](../../../tests/README.md#app-config-checks). Real plist modifiers and apply-time hook PTYs are distinct checks. |
| packages-and-secrets | Use the [package and secret checks](../../../tests/README.md#package-and-secret-checks) for rendering, feature gates, install ordering/trust, and secret failures; preview Brewfiles for affected machine types and MAS opt-in. |
| any | `git diff --check` before handoff |

After editing this skill itself: see `references/meta-skill-maintenance.md` for the parser/frontmatter check.

## Do Not

- Edit a target under `~/` and assume `chezmoi apply` will reconcile silently — it prompts or overwrites.
- Embed secrets, license keys, or human-readable `op://` paths in committed source.
- Renumber `home/.chezmoiscripts/` prefixes, or reintroduce `home/.chezmoidata/apps/*.toml`.
- Add MAS app config without confirming the install path is in scope, or Setapp app config for an app missing from `setapp_apps`.
- Paraphrase chezmoi attribute grammar from memory; consult `references/source-target-translation.md`.
- Add long inline command transcripts to this SKILL.md. Push depth into `references/`.
