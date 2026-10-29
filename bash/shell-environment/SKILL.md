---
name: shell-environment
description: "This machine's interactive shell setup — zsh with oh-my-zsh and powerlevel10k, the toolchain PATH order, history and key bindings, the red team aliases and helper functions, plus ssh, vim and Tern settings. Use when a tool is not found, PATH order is wrong, the prompt or completions break, history misbehaves, or a new pane does not pick up the shell. Not for installing tools (use redteam-toolchain) or for choosing a tool (use toolchain-router)."
---

# Shell environment

The shell is the delivery mechanism for every other tool skill: if `PATH`, `chsh` or a plugin is wrong, the tool looks missing. Everything here is stored in the repository under `config/host/` and installed by `scripts/install-host-config.sh` with timestamped backups.

## Files and destinations

| Repository path | Installed to | Scope |
| --- | --- | --- |
| `config/host/zsh/zshrc` | `~/.zshrc` | plugins, PATH, history, aliases, functions |
| `config/host/zsh/p10k.zsh` | `~/.p10k.zsh` | two-line prompt, nerd-font or ASCII |
| `config/host/profile.d/10-redteam.sh` | `/etc/profile.d/10-redteam.sh` | toolchain `PATH`, `GOPATH`, `GOBIN` |
| `config/host/ssh/99-redteam.conf` | `/etc/ssh/ssh_config.d/99-redteam.conf` | timeouts, legacy algorithms, host-key policy |
| `config/host/vim/vimrc.local` | `/etc/vim/vimrc.local` | search, encoding, no swap or viminfo |
| `config/host/tern/settings.json` | `~/.config/tern/settings.json` | pane shell is `/bin/zsh` |

## PATH order

`/etc/profile.d/10-redteam.sh` owns the order, and `/etc/zsh/zshenv` sources it so non-interactive zsh sees it too.

```
/opt/node/bin  /opt/go126/bin  /opt/tools  /opt/segfault/bin  ~/.local/bin
```

- `/opt/go126/bin` stays first on purpose: nuclei's `sonic` and `ast` parser need Go ≤ 1.26, and a later Go on PATH breaks the build.
- `GOBIN=/opt/tools`, so `go install` never scatters binaries into `~/go/bin`.
- `~/.zshrc` re-appends `~/.local/bin:/opt/tools` after sourcing the profile, which keeps pipx and the Go binaries reachable in panes that skipped login files.

## What the zshrc provides

Plugins: `git`, `z`, `extract`, `sudo`, `colored-man-pages`, `command-not-found`, `history-substring-search`, `zsh-completions`, `zsh-autosuggestions`, `zsh-syntax-highlighting` — under `~/.oh-my-zsh`, theme `powerlevel10k/powerlevel10k`.

- **History**: `HISTSIZE=SAVEHIST=100000`, `SHARE_HISTORY`, `INC_APPEND_HISTORY`, `EXTENDED_HISTORY`, duplicate lines collapsed. Parallel panes share one history file by design.
- **Behaviour**: `AUTO_CD AUTO_PUSHD NO_BEEP COMPLETE_IN_WORD ALWAYS_TO_END`, `unsetopt FLOW_CONTROL` so `Ctrl-S`/`Ctrl-Q` are free.
- **Keys**: emacs bindings, `Ctrl-Space` accepts autosuggestions, up/down search history substrings, `Ctrl-Left/Right` move by word.
- **Trap**: `cat` is aliased to `batcat --paging=never -pp` and `bat` to `batcat`. Comment the `cat` alias out before piping binary or byte-exact output into another tool.

Aliases worth knowing: `pp` (`proxychains4 -q`), `nxc`/`smb`/`ldap`/`winrm`/`mssql`/`rdp` (NetExec), the impacket shorthands (`secretsdump`, `psexec`, `wmiexec`, `atexec`, `getTGT`, `getST`, …), `asreproast`, `ports` (`ss -tulpn`), `myip`, `tmx`, `venv`.

Functions: `scan <host> [flags]`, `sweep <host>` (all-TCP, writes `/tmp/sweep-<host>.gnmap`), `webscan <url>`, `rs <lhost> <lport> [bash|nc|python|perl|php|powershell]`, `listen [port]` (rlwrap), `adrecon <host>`, `mkcd`, `tunnel`, `hashcat-mode`, `p10k ascii|nerd|config`, `redteam-check`.

`/opt/segfault/shellrc.sh` is sourced when present, which is what adds `crt`, `asnl`, `io`, `gssec`, `sshj` and friends — see [segfault-cli](../segfault-cli/SKILL.md).

## Repair recipes

| Symptom | Check | Fix |
| --- | --- | --- |
| `command not found` for an installed tool | `echo $PATH`, `which -a <tool>` | re-source `/etc/profile.d/10-redteam.sh`; confirm the file exists |
| two `PATH` entries or a stale prefix | `print -l ${(s.:.)PATH} \| sort \| uniq -d` | remove the duplicate append from `~/.zshrc`, not from the profile |
| prompt shows `?` boxes or raw glyphs | `echo $P10K_ASCII`, `echo $TERM` | `p10k ascii` for fonts without nerd icons; `p10k nerd` to go back |
| prompt is slow or instant prompt is disabled | grep `p10k-instant-prompt` warnings at login | keep the instant-prompt block first in `~/.zshrc`; move slow `source` lines below it |
| completions missing after `apt install` | `echo $fpath` | `rm -f ~/.zcompdump*` then `exec zsh` |
| history shared with a previous pane's tail | `echo $HISTFILE` | expected: `INC_APPEND_HISTORY` and `SHARE_HISTORY` are on |
| Tern pane still starts `bash` | `tern` settings `shell` key | reinstall `config/host/tern/settings.json`, then `systemctl restart tern-daemon` (kills open panes) |
| login shell is bash | `getent passwd $USER \| cut -d: -f7` | `chsh -s /bin/zsh $USER`, then re-login |

## SSH client policy

`99-redteam.conf` sets `ConnectTimeout 10`, `ServerAliveInterval 15`, `ServerAliveCountMax 3`, `StrictHostKeyChecking accept-new`, `HashKnownHosts yes`, and `LogLevel ERROR`. It re-enables `diffie-hellman-group1-sha1`, `diffie-hellman-group14-sha1` kex and `ssh-rsa` host/user keys for old lab targets.

- Host keys are still verified on first contact — `accept-new`, not `no`. A changed key is a real event.
- `IdentitiesOnly` is deliberately not global, so agent forwarding and multiple identities keep working per host.
- Nothing here disables `PasswordAuthentication` or touches the server side; this is a client-only drop-in under `/etc/ssh/ssh_config.d/`.

## Reinstall and verify

```sh
bash scripts/install-host-config.sh --dry-run   # list every destination
sudo bash scripts/install-host-config.sh        # writes, backing up as <path>.bak-<timestamp>
exec zsh                                        # reload the current pane
redteam-check | head -3                         # PATH resolves the toolchain
```

Run as root to install the `/etc` files; as a normal user the script installs only `~/.zshrc`, `~/.p10k.zsh`, the Tern settings and the shell change, and reports the system files as skipped.

## Cautions

1. **`install-host-config.sh` overwrites `~/.zshrc`.** Machine-local additions belong in `~/.zshrc.local`, sourced from a line you add to the repository copy — or they are lost on the next install. Backups live beside the file.
2. **`chsh` needs a fresh login.** Existing panes and Tern panes keep the old shell until they are restarted.
3. **Do not add `set -e`-style guards to `~/.zshrc`.** A failing plugin line aborts the rest of the file and the shell opens half-configured.
4. **The `10-redteam.sh` order is load-bearing.** Inserting another Go toolchain before `/opt/go126/bin` breaks nuclei silently at template compile time.