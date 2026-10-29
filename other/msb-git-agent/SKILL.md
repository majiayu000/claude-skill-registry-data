---
name: msb-git-agent
description: "Git and ssh from inside a sandbox: git_push as gh or ssh with ensure_git_push() applying it in the guest's --system config on every start (never the repo's .git/config, which in a folder sandbox is the host checkout), the gh credential helper replacing bootstrap's inline one, the insteadOf and pushInsteadOf rewrites, push_pub key selection, the IdentitiesOnly snippet for ssh mode, and the per-sandbox filtering SSH agent (msbctl _agent-filter, ssh_keys fingerprints, ensure_keys_loaded(), the socket path baked in at create time). Use when changing how a sandbox pushes, which key it uses, or what the agent filter forwards."
---

# Git Agent

Detail carved out of `AGENTS.md`, which keeps only what has to hold in
every session. Repo-specific throughout; the facts here are verified against
msb 0.7.6 and re-checked on 0.7.7.

## How git reaches GitHub

`git_push` (registry entry, else `[defaults]`, `GIT_PUSH`) is `"gh"` or `"ssh"`; `ensure_git_push()` applies it on every start in the guest's `--system` config — never the repo's `.git/config`, which in a folder sandbox is the host checkout. Both set `credential.https://github.com.helper` to `gh auth git-credential` (replacing bootstrap's inline clone-time helper); `gh` adds `url.https://github.com/.insteadOf` for `git@github.com:` and `ssh://git@github.com/`; `ssh` adds `pushInsteadOf` the other way and, when `push_active`, writes the push key's public half plus a `Host github.com` `IdentitiesOnly` snippet under `/etc/ssh/ssh_config.d/`. The key is `push_pub`: the entry's `push_key`, else the identity's. Repo sandboxes are written with `git_push = "gh"`. `sandbox_profile_section()` tells the agent which, so it never "fixes" a remote.

## SSH agent filtering

Each sandbox's `--vsock` points at its own filtering daemon (`msbctl _agent-filter <name>`, same file, state in `~/.local/state/msb/agent/`), not the host agent. It forwards only identity-list and sign requests, restricted to the fingerprints in the registry entry's `ssh_keys` (absent = all, `[]` = none), re-read per request. The socket path is baked in at create time, so sandboxes created before this need one `rebuild`. Keys are picked in one grouped multiselect (`agent:` / `~/.ssh:` headings via `Header` rows in `toggle_list`); an encrypted key with no `.pub` is listed unnamed and only asks for its passphrase if picked. The fingerprint is the stored/matched identity but is never displayed. `ensure_keys_loaded()` (called from `ensure_agent_filter()`, so every start path) `ssh-add`s any selected key missing from the agent, found by fingerprint in `~/.ssh` (still-unnamed encrypted files are tried in turn), warning rather than failing if it can't. The daemon skips the `msb`/KVM preflight; `ensure_agent_filter()` respawns it on every start.
