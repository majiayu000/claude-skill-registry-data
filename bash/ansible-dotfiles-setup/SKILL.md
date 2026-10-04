---
name: ansible-dotfiles-setup
description: This skill should be used when the user asks to run, update, or troubleshoot the Ansible dotfiles playbook, add packages/casks, configure work vs personal profiles, manage SOPS secrets, or bootstrap a new Mac.
---

# Ansible Dotfiles Setup

## Structure

```
ansible/
  ansible.cfg              # inventory, roles_path, vars_plugins_enabled
  inventory.yml            # work-mac + personal-mac (both ansible_connection: local)
  requirements.yml         # community.general >= 9.0.0, community.sops >= 1.6.0
  .sops.yaml               # age recipient for vault encryption
  playbooks/site.yml        # main playbook, --limit selects profile (hosts: target_hosts|default(all))
  playbooks/bootstrap.yml   # interactive wrapper: prompts profile, imports site.yml
  group_vars/
    all/main.yml           # common packages, feature toggles, brew lists
    all/vault.sops.yaml    # SOPS-encrypted, BOTH profiles: ssh_homelab_hosts
    work/main.yml          # machine_profile, expected_hostname, brew_packages_extra
    work/vault.sops.yaml   # SOPS-encrypted, work only: work_git_email, cf_access_client_id/secret
    personal/main.yml      # machine_profile, expected_hostname, enable_docs
  roles/
    homebrew/              # taps → trust → formulae → casks
    shell/                 # OMZ, plugins, Bun, TPM, fzf-git
    stow/                  # XDG + home-target stow, gitconfig-local template
    macos/                 # karabiner, colima, kanata, yazi, docs, ssh homelab block
```

## Run commands

`SOPS_AGE_KEY_FILE` is exported in `zsh/exports.zsh` — no need to prefix commands manually.

```bash
# Simplest — auto-detects profile from hostname, prompts if unknown
./setup.sh

# From ansible/ directory — install + stow only (no sudo required)
ansible-playbook playbooks/site.yml --limit work-mac --tags install,stow

# Full run (requires sudo for kanata LaunchDaemon)
ansible-playbook playbooks/site.yml --limit work-mac --ask-become-pass

# Dry-run (check mode)
ansible-playbook playbooks/site.yml --limit work-mac --check --diff
```

### setup.sh hostname auto-detection

`setup.sh` reads `expected_hostname` from `group_vars/{work,personal}/main.yml` and compares with the current machine's hostname (via `ansible -m setup ... filter=ansible_hostname`).

- **Known hostname** → selects profile silently, no prompt
- **Unknown hostname** → prints a warning with the known hostnames, asks `work` or `personal`, then updates `expected_hostname` in the chosen `group_vars` file automatically

On a new Mac, just run `./setup.sh` once — it self-registers the hostname.

## Tags

| Tag | What it runs |
|-----|-------------|
| `install` | homebrew role (taps, packages, casks) |
| `shell` | shell role (OMZ, plugins, Bun, TPM) |
| `stow` | stow role (symlinks, gitconfig-local) |
| `macos` | macos role (karabiner, colima, kanata, yazi, docs) |
| `become` | tasks requiring sudo (kanata, KE agents) |

## Adding packages

- Common formulae: `group_vars/all/main.yml` → `brew_packages`
- Common casks: `group_vars/all/main.yml` → `brew_casks`
- Work-only formulae: `group_vars/work/main.yml` → `brew_packages_extra`
- Work-only casks: `group_vars/work/main.yml` → `brew_casks_extra`
- Personal-only formulae: `group_vars/personal/main.yml` → `brew_packages_extra`

## Moving packages between profiles

To move a formula from common (`all`) to work-only:
1. Remove from `group_vars/all/main.yml` (`brew_packages` or `brew_packages_tap`)
2. Add to `group_vars/work/main.yml` → `brew_packages_extra`

`brew_packages_extra` accepts full tap-prefixed names: `keidarcy/tap/e1s`.
Leaving the tap in `brew_taps` (all) without its formula is harmless — the tap is just added, nothing installed from it.

## Playbooks

- `playbooks/site.yml` — main playbook. `hosts: "{{ target_hosts | default('all') }}"`. Run directly with `--limit work-mac` / `--limit personal-mac`. Used by `setup.sh`.
- `playbooks/bootstrap.yml` — interactive wrapper for a new Mac: `vars_prompt` for the profile, then `import_playbook: site.yml` with `target_hosts` set to the chosen `<profile>-mac`. Skip the prompt with `-e mac_profile=personal`.

No duplication between them — `bootstrap.yml` holds only the prompt; all pre_tasks/roles live in `site.yml`.

## Linting (pre-commit + yamllint + ansible syntax-check)

Tools installed via `brew_packages_dev` (pre-commit, yamllint, ansible-lint). The `stow` role runs `pre-commit install --install-hooks` (idempotent via `creates: .git/hooks/pre-commit`). The hook **blocks** commits on failure.

- Config: `.pre-commit-config.yaml` (root), `.yamllint.yml`, `.ansible-lint`.
- Run manually: `pre-commit run --all-files`.
- ansible-lint profile `production` (strictest — idempotency, FQCN, role var prefixes, no command-instead-of-module). yamllint owns YAML *style* separately.
- **ansible-lint is NOT used in the pre-commit hook.** It ships its own embedded `ansible-core` that does not share collections with the system ansible. `community.general`/`community.sops` are invisible to it, and `syntax-check[unknown-module]` is unskippable. The hook uses `ansible-playbook --syntax-check` instead — it uses the system ansible with all collections. Run `ansible-lint` manually for full linting.
- **Role register vars must be prefixed with the role name** (`macos_`, `homebrew_`, ...) — `var-naming[no-role-prefix]`. E.g. `register: macos_ya_pkg`, not `ya_pkg`.
- Legitimate exceptions use a targeted `# noqa: <rule>` on the task `name:` line with a comment explaining why (see `shell/tasks/main.yml`: `latest[git]` on intentional default-branch clones, `command-instead-of-module` on `git submodule update`).
- **Gotcha — ANSIBLE_CONFIG**: the pre-commit hook sets `ANSIBLE_CONFIG=ansible/ansible.cfg` so roles resolve from repo root. Without it: role not found.
- **Gotcha — braces conflict**: yamllint must use `braces.min-spaces-inside: 0` (not 1) or ansible-lint's embedded yamllint rejects the config as incompatible. `max-spaces-inside: 1` still allows idiomatic `{{ var }}`.
- Excludes: `*.sops.yaml`, `docs/`, `yazi/flavors/`, `tmux/plugins/` (third-party submodules, read-only), `nvim/lazy-lock.json`.

## Known gotchas

**Homebrew 4.x tap trust**
Third-party taps (FelixKratz, nikitabobko, etc.) require explicit trust before their formulae/casks install. The `homebrew` role runs `brew trust <taps>` after `homebrew_tap`. If a new tap is added to `brew_taps`, trust is applied automatically on next run.
`changed_when` must match `'Already trusted tap:'` (capital A) — Homebrew's actual output. Using lowercase `'already trusted'` never matches and the task always reports changed.

**kanata daemon idempotency**
Do NOT run `launchctl bootout` unconditionally before `launchctl bootstrap`. The correct pattern:
1. `launchctl print system/com.lucatrifilio.kanata` → register result, `failed_when: false`, `changed_when: false`
2. `launchctl bootstrap` only `when: macos_kanata_loaded.rc != 0` (daemon not loaded)
3. Reload on plist change → handled by the `reload kanata daemon` handler (bootout + bootstrap in handlers/main.yml)

Running bootout unconditionally causes always-changed because bootstrap always follows it.

**karabiner symlink — always-changed is expected**
Karabiner-Elements overwrites the `~/.config/karabiner` symlink with a real directory on every launch. Ansible correctly detects this (via `stat` + `islnk` check) and recreates the symlink each run. This `changed` is legitimate — do not suppress with `changed_when: false`.

**Casks that install to /Applications/ require sudo**
`community.general.homebrew_cask` does not support `become`. Casks like `notion-calendar` that copy `.app` to `/Applications/` need `--ask-become-pass` at the playbook level. Run the full playbook with `--ask-become-pass` rather than `--tags install` alone.

**karabiner symlink must use `ln -sfn`**
`ansible.builtin.file: state=link, force=true` refuses to replace a non-empty directory. Use `ansible.builtin.command: ln -sfn <src> <dest>` — this replaces the directory entry without touching contents, matching the original `setup.sh` behavior.

**bootstrap.yml vs site.yml — always --limit with bootstrap.yml**
`bootstrap.yml` is an interactive wrapper that imports `site.yml` with `target_hosts` set to the chosen profile. When run on a single machine, it still evaluates `pre_tasks` for all hosts in inventory — the hostname assertion on the other profile will fail. Always pass `--limit <profile>-mac` when using `bootstrap.yml` from the CLI:
```bash
ansible-playbook playbooks/bootstrap.yml --ask-become-pass --tags macos,become --limit work-mac
```
Prefer `site.yml` directly for non-interactive runs — it requires `--limit` by design and avoids the issue entirely.

**colima homebrew_services: use `state=present` not `state=started`**
`state=started` is not a valid value for `community.general.homebrew_services`. Use `state=present` to register the service for autostart.

**SOPS vault in --check mode**
Add `ignore_errors: "{{ ansible_check_mode }}"` to the `community.sops.load_vars` task. Without it, `--check` fails if the vault references variables that haven't been loaded.

**stow simulate+apply pattern**
Two-task pattern for `--check` compatibility:
1. Simulate: `stow --simulate`, `check_mode: false`, `changed_when: "'LINK:' in result.stderr"`
2. Apply: `stow` (no simulate), `when: not ansible_check_mode`

**ansible/ must be ignored in .stowrc**
Add `--ignore=^ansible$` to `.stowrc` to prevent stow from symlinking `ansible/` into `~/.config/`.

**Orphan taps cause brew link failures**
Taps present on the machine but not in `brew_taps` trigger Homebrew's "untrusted taps" warning, which causes `brew link` to fail for unrelated packages. All homebrew install tasks set `HOMEBREW_NO_REQUIRE_TAP_TRUST: "1"` as an env var as a blanket guard. To audit and clean up orphan taps:
```bash
brew tap-info --json <tap> | python3 -c "import json,sys; d=json.load(sys.stdin); print([f for f in d[0]['formula_names']])"
brew untap <tap>  # if nothing installed from it
```

**LaunchAgent (GUI domain) idempotency**
User LaunchAgents in `~/Library/LaunchAgents/` use `gui/UID` domain — different from kanata's `system` domain. No `become` needed.
1. Check: `launchctl print gui/{{ ansible_user_uid }}/<label>` → `failed_when: false`, `changed_when: false`
2. Bootstrap: `launchctl bootstrap gui/{{ ansible_user_uid }} ~/Library/LaunchAgents/<label>.plist` only `when: rc != 0`
3. Reload handler: `launchctl bootout gui/{{ ansible_user_uid }}/<label>` → `launchctl bootstrap gui/{{ ansible_user_uid }} <plist>`

Contrast with kanata: system domain requires `become: true`; GUI domain does not.

**Idempotency patterns for tricky tasks**
- `brew trust`: always `changed_when: false` — output varies and can't reliably detect "already trusted"
- `ln -sfn` (karabiner dir symlink): stat the path first, then `changed_when: not stat.islnk or stat.lnk_source != expected_path`
- `launchctl bootstrap`: check `launchctl print system/<label>` first (`rc == 0` = already loaded); add `when: macos_kanata_status.rc != 0` to skip bootstrap if running

## Adding a personal-only automated task

Pattern for features active only on personal-mac (e.g. obsidian vault auto-push):

1. `group_vars/all/main.yml` — add toggle `enable_X: false` + empty-default vars
2. `group_vars/personal/main.yml` — override `enable_X: true` + real values
3. All tasks gated with `when: enable_X`
4. Scripts deployed via `ansible.builtin.template` to `~/.scripts/` (mode `0755`)
5. LaunchAgent plist via template to `~/Library/LaunchAgents/` with `notify: reload X agent`
6. Handler: bootout gui/UID/label → bootstrap gui/UID plist (see GUI domain pattern above)

Example vars for obsidian backup: `enable_obsidian_backup`, `obsidian_vault_path`, `obsidian_backup_interval` (default 1800).

**obsidian-git-backup.sh.j2 strategy**: LiveSync (CouchDB) is the source of truth for vault content; git is backup only, personal-mac only. The script does `commit → fetch → rebase -X ours origin/main → conflict-marker guard → push origin → push forgejo`. Both pushes are blocking (ERROR + exit 1 on failure). Never use `git push --force` (silent data loss across devices) and never `merge` without committing first (leaves `<<<<<<<` markers in notes — the original bug). The conflict-marker guard (`git grep -lE '^(<<<<<<< |=======$|>>>>>>> )' HEAD -- '*.md'`) blocks pushing corrupted notes.

## Bootstrapping a new Mac

1. `git clone git@github.com:luca-trifilio/dotfiles.git ~/Progetti/dotfiles`
2. Copy age key from existing Mac (AirDrop or scp): `~/.config/sops/age/keys.txt`
3. Verify the hostname ansible will see (use this, not just `hostname` — avoids `.local` FQDN confusion):
   ```bash
   cd ansible && ansible -m setup localhost -a 'filter=ansible_hostname'
   # → "ansible_hostname": "MacBook-Pro-M4-Max-di-Luca"
   ```
4. Update `expected_hostname` in `group_vars/{work,personal}/main.yml` with that value
5. Install ansible collections: `cd ansible && ansible-galaxy collection install -r requirements.yml`
6. Dry run (no sudo needed — become tasks are guarded with `when: not ansible_check_mode`):
   ```bash
   SOPS_AGE_KEY_FILE=~/.config/sops/age/keys.txt \
     ansible-playbook playbooks/site.yml --limit personal-mac --check --diff
   ```
7. Full run:
   ```bash
   SOPS_AGE_KEY_FILE=~/.config/sops/age/keys.txt \
     ansible-playbook playbooks/site.yml --limit personal-mac --ask-become-pass
   ```
8. Manual steps (cannot be automated): Input Monitoring + Accessibility permissions for Karabiner, Driver Extension approval, `prefix + I` in tmux for TPM plugins

## SOPS vault

Encrypted with age. Key at `~/.config/sops/age/keys.txt`. Two vaults:

- `group_vars/all/vault.sops.yaml` — **both profiles**. Loaded unconditionally in `site.yml` pre_tasks (gated only on sops being present). Contains `ssh_homelab_hosts` (homelab SSH host data: internal IPs, Tailscale addresses, usernames).
- `group_vars/work/vault.sops.yaml` — **work only** (`when: 'work' in group_names`). Contains `work_git_email`, `cf_access_client_id`, `cf_access_client_secret`.

```bash
# Edit a vault (sops opens decrypted in $EDITOR, re-encrypts on save)
SOPS_AGE_KEY_FILE=~/.config/sops/age/keys.txt sops ansible/group_vars/all/vault.sops.yaml

# Verify decryption
SOPS_AGE_KEY_FILE=~/.config/sops/age/keys.txt sops --decrypt ansible/group_vars/all/vault.sops.yaml

# Insert/update a single key without opening the editor (scripting-safe)
SOPS_AGE_KEY_FILE=~/.config/sops/age/keys.txt sops --set '["key_name"] "value"' ansible/group_vars/all/vault.sops.yaml
```

**Creation-rule gotcha**: `.sops.yaml` matches on `path_regex: \.sops\.yaml$` against the *input* filename. To `sops --encrypt` a new file from scratch, name it `*.sops.yaml` and use `--in-place` (or `--config ansible/.sops.yaml`). Encrypting a `/tmp/foo.yaml` fails with "no matching creation rules" and a `>` redirect will clobber the destination with empty output. Prefer `sops <file>` (edit-in-place) for existing vaults.

## SSH homelab block (~/.ssh/config)

The `macos` role manages a `blockinfile`-marked region in `~/.ssh/config` (marker `# {mark} ANSIBLE MANAGED BLOCK — homelab`), rendered from `ssh_homelab_hosts` (in the shared vault) via `roles/macos/templates/ssh_homelab.j2`. Toggle: `enable_ssh_homelab` in `group_vars/all/main.yml` (default true).

- Only the marked region is managed — colima `Include` lines and the `github.com`/`github-personal` identity blocks are untouched. Host patterns are disjoint, so the block can sit anywhere in the file without shadowing.
- The task tightens perms to `0600` and is gated on `ssh_homelab_hosts is defined` (skipped with a reminder if the vault wasn't loaded, e.g. before sops is installed).
- `proxy_command` is stored as a **literal absolute path** (`/opt/homebrew/bin/cloudflared`) — `blockinfile`'s `block:` lookup does NOT recursively re-template var values, so `{{ homebrew_prefix }}` inside a vault string would leak verbatim into the file.
- Verify the effective result with `ssh -G macserver` / `ssh -G vps-homelab` (resolves config without connecting).
