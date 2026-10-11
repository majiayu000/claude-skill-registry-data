---
name: setup
description: This skill should be used when the user asks to "install Infisical CLI", "set up Infisical CLI", "log in to Infisical", "authenticate Infisical CLI", "verify Infisical is working", "is Infisical CLI working", "point Infisical at self-hosted", or needs to get the Infisical CLI installed, authenticated, and confirmed operational.
---

# Infisical CLI Setup & Verification

Install the Infisical CLI, authenticate it, and confirm it can reach a project. This is the first thing to do before any `infisical run`, `secrets`, `export`, or `scan` work.

## 1. Install the CLI

Pick the matching platform. Pin a version in production (`github.com/Infisical/cli/releases`).

```bash
# macOS (Homebrew)
brew install infisical/get-cli/infisical

# Windows (winget)
winget install infisical

# Windows (Scoop)
scoop bucket add org https://github.com/Infisical/scoop-infisical.git
scoop install infisical

# npm (any OS with Node)
npm install -g @infisical/cli

# Debian / Ubuntu
curl -1sLf 'https://artifacts-cli.infisical.com/setup.deb.sh' | sudo -E bash
sudo apt-get update && sudo apt-get install -y infisical

# RHEL / CentOS / Amazon Linux
curl -1sLf 'https://artifacts-cli.infisical.com/setup.rpm.sh' | sudo -E bash
sudo yum install infisical

# Alpine
apk add --no-cache bash sudo wget
wget -qO- 'https://artifacts-cli.infisical.com/setup.apk.sh' | sudo sh
apk update && sudo apk add infisical

# Arch (AUR)
yay -S infisical-bin
```

> **Linux repository moved.** If the CLI was installed from the Cloudsmith package repository, move to `artifacts-cli.infisical.com` — Cloudsmith stopped serving the CLI on 2026-09-16, so `apt-get update` fails outright (apt) or the Infisical repo warns (yum/apk) on machines still pointed at it. Remove the old source, then re-run the setup script above (details: https://infisical.com/docs/cli/cloudsmith-migration):
>
> ```bash
> grep -rlE 'cloudsmith.*infisical' /etc/apt/sources.list.d/ 2>/dev/null | xargs -r sudo rm -f      # Debian / Ubuntu
> grep -rlE 'cloudsmith.*infisical' /etc/yum.repos.d/ 2>/dev/null | xargs -r sudo rm -f              # RHEL family
> sed -i '/cloudsmith.*infisical/d' /etc/apk/repositories                                             # Alpine, as root
> ```

Confirm the binary is on PATH:

```bash
infisical --version
```

## 2. Point at the right instance (self-hosted / EU)

The CLI defaults to US Cloud (`https://app.infisical.com`). For EU Cloud, a dedicated or a self-hosted instance, set the domain **once** in the environment so every command uses it — this avoids passing `--domain` on each call.

```bash
export INFISICAL_DOMAIN="https://your-instance.example.com"   # self-hosted
export INFISICAL_DOMAIN="https://eu.infisical.com"            # EU Cloud
```

The instance is chosen in this order: `--domain` flag, then `INFISICAL_DOMAIN`, then `domain` in `.infisical.json`, then US Cloud. `--domain` is a global flag, so `infisical login --domain=https://eu.infisical.com` works as well.

To pin the instance for one repository instead, put it in `.infisical.json` (`"domain": "https://your-instance.example.com"`, must start with `https://` or `http://`). Only do this for an instance you trust: the file is committed, and the CLI sends every request and credential to the host it names (it prints a warning naming the host each time).

After a user login, commands go to the instance of the logged-in profile, and a `--domain` / `INFISICAL_DOMAIN` that names a **different** instance makes the command fail — use a second profile instead (step 3).

If a reverse proxy (e.g. Cloudflare Access) fronts the instance, add its headers:

```bash
export INFISICAL_CUSTOM_HEADERS="Access-Client-Id=value Access-Client-Secret=value"
```

## 3. Authenticate

For interactive developer use, log in through the browser:

```bash
infisical login          # opens a browser
infisical login -i       # terminal prompts (use in WSL2, Codespaces, containers)
```

For CI/CD and automation, use a machine identity instead of a user login — see the `ci-cd-auth` skill.

On headless Linux where no system keyring exists, switch the credential store to an encrypted file before logging in (this is the standard fix for keyring errors):

```bash
infisical vault set file     # backends: file (encrypted file) | auto (system keyring, the default)
```

`auto` already falls back to `file` by itself when the CLI cannot write to the keyring the first time. Switching backends removes every stored profile, so log in again afterwards. There is no `keychain` value.

### Several organizations or instances (named profiles, CLI >= 0.43.134)

Every user login is a **profile**: one account on one instance plus the organization it uses. Work in several organizations without logging in again:

```bash
infisical profile list                                  # what exists
infisical profile current                               # which profile applies here, and why
infisical profile create client-b --org <org-slug>      # second org, same login (>= 0.43.135; `profile new` in 0.43.134)
infisical login --save-as work-eu --domain=https://eu.infisical.com   # another account or instance
eval "$(infisical profile pin client-b)"                # this terminal only
infisical profile bind client-b ~/work/client-b         # every command under that directory
infisical profile use client-b                          # default for the machine
infisical secrets --profile client-b --env=dev          # one command only (or --org <org>)
```

A command uses the first that is set: `--profile`, then `INFISICAL_PROFILE` (what `pin` sets), then a bound directory, then the default profile. In CI set `INFISICAL_PROFILE` or pass `--profile`. `infisical logout` ends a session but keeps the profile; `infisical profile delete <name>` removes it.

## 4. Link a project

Run this in the project root to write `.infisical.json` (safe to commit — it holds no secrets, only the workspace ID and environment mapping):

```bash
cd /path/to/project
infisical init
```

## 5. Verify it works

Run a read against the linked project. A clean list confirms the CLI is installed, authenticated, and scoped correctly:

```bash
infisical secrets --env=dev
```

Then confirm injection works end-to-end:

```bash
infisical run --env=dev -- printenv | grep -i <a-known-secret-key>
```

Check the current session and credential store at any time:

```bash
infisical login status     # session validity
infisical profile current  # which login profile is in effect (>= 0.43.134)
infisical vault            # active credential backend
```

## What This Skill Does NOT Cover

- Machine-identity / OIDC / cloud-native auth for pipelines — see the `ci-cd-auth` skill
- Day-to-day `run` / `secrets` / `export` workflows — see the `cli-recipes` skill
- Secret scanning and pre-commit hooks — see the `secret-scanning` skill
- The full command and flag list — see the `cli-reference` skill
- Diagnosing errors — see the `troubleshoot` skill