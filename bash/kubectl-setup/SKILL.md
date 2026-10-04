---
name: kubectl-setup
description: Use when the user asks to "install kubectl", "set up kubens", "configure kubernetes CLI tools", or needs to make kubectl/kubens/kubectx replicable via dotfiles Ansible package list.
---

# kubectl + kubens/kubectx Setup

## State (as of 2026-08)

- `kubectl` 1.36.1 — installed via `brew install kubectl`
- `kubectx` / `kubens` 0.11.0 — installed, managed via Ansible
- `k9s` — installed, managed via Ansible

## Package list (ansible/group_vars/all/main.yml)

All three tools are in `brew_packages` (see ADR-0002 — `brew/Brewfile` was removed,
`group_vars` is the source of truth):

```yaml
brew_packages:
  - k9s
  - kubectl
  - kubectx
```

## Aliases

`k` alias comes from the OMZ `kubectl` plugin (already in `.zshrc` plugins list).
Do NOT duplicate it in `aliases.zsh` — it's already provided by OMZ.

In `zsh/aliases.zsh`:
```bash
alias kns='kubens'
alias kx='kubectx'
```

## Replicating on a new machine

Handled by the `install` tag in the Ansible playbook (see `ansible/README.md`):

```bash
ansible-playbook playbooks/site.yml --limit <profile>-mac --tags install
```

Aliases come automatically from stow + OMZ `kubectl` plugin.

## Notes

- `colima start --kubernetes` creates a separate local cluster context navigable with `kx`
- `kubectx` uses `~/.kube/config` — contexts are added by cloud CLIs (e.g. `aws eks update-kubeconfig`)
- zsh completions installed automatically by Homebrew to `/opt/homebrew/share/zsh/site-functions`

## ~/.kube/config is Ansible-templated, not hand-managed

Rendered by the `stow` role from `ansible/roles/stow/templates/kubeconfig.j2` (task
"Template ~/.kube/config"). File header says "DO NOT EDIT BY HAND" — edit the
template and re-run `--tags stow`, not the file directly.

Contexts:
- `services-eks-cluster-test` / `services-eks-cluster-staging` — **work-only**, gated
  `{% if 'work' in group_names %}`. Auth is `aws eks get-token` (AWS_PROFILE=staging).
- `homelab` — **both profiles**, gated `{% if homelab_client_certificate_data is defined %}`.
  Server is the Tailscale IP `100.74.130.73:6443` (not the LAN IP) so it resolves from
  either Mac. Client cert/key come from `group_vars/all/vault.sops.yaml`
  (`homelab_client_certificate_data`, `homelab_client_key_data`), inserted with
  `sops --set` (see ansible-dotfiles-setup skill).

`current-context` picks `services-eks-cluster-staging` on work-mac, `homelab` otherwise.

**Gotcha — gate all three sections (clusters/contexts/users) consistently.** The
kubeconfig YAML splits one logical context into three top-level blocks. Gating only
`clusters:` and leaving `contexts:`/`users:` ungated (or vice versa) renders a context
that references a cluster/user name which doesn't exist in the file — `kubectl` then
lists a broken context. Always mirror the same `{% if %}` on all three blocks for a
given context.
