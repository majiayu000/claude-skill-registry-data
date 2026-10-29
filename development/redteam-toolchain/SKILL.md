---
name: redteam-toolchain
description: "Inventory, install, repair and verify this machine's offensive toolchain — paths, versions, package managers, wordlists, Metasploit database, shell integration and the redteam-check gate. Use when a tool is missing, a version is wrong, a fresh host needs the same stack, or before an engagement starts. Not for choosing which tool to run (use toolchain-router)."
---

# Red team toolchain

This host is a single-node workstation: Ubuntu 24.04, root, 2 vCPU, no GPU, no Docker. Everything below is installed and verified by `redteam-check`. Reproduce it on a new host with `scripts/install-redteam-toolchain.sh` from the MeowPi repository.

## Layout

| Path | Contents | Managed by |
| --- | --- | --- |
| `/opt/tools` | Go binaries and static releases (`nuclei`, `httpx`, `ffuf`, `chisel`, `ligolo-*`, `sliver-server`, `feroxbuster`, `jsluice`, `cheat`, `anew`) | `go install` with `GOBIN=/opt/tools` |
| `~/.local/bin` | pipx apps (`nxc`, 70 impacket entry points, `certipy`, `dirsearch`, `bloodyad`, `garak`, `picklescan`, `mitmdump`) | `pipx` |
| `/opt/node/bin` | Node 24 and npm globals (`webcrack`, `chrome-devtools-mcp`) | upstream tarball |
| `/opt/go126` | Go 1.26.10, pinned first on PATH | tarball |
| `/usr/local/go` | Go 1.27.3, kept for everything except nuclei | tarball |
| `/opt/segfault/bin` | `crt`, `asnl`, `io`, `ptr`, `resolv`, `gssec`, `sshj`, `xssh`, `transfer`, `supervise` | copied + patched |
| `/opt/windows-tools` | Rubeus, Mimikatz, SharpHound, Certify, Seatbelt, PowerView, PowerUp, PrivescCheck, linPEAS, winPEAS, `chisel.exe`, `ligolo-agent.exe` | release downloads |
| `/opt/wordlists` | symlinks into SecLists plus extracted `rockyou.txt` | manual |
| `/opt/repos` | SecLists, PayloadsAllTheThings, Responder, enum4linux-ng, segfault | `git clone` |
| `/opt/cheatsheets` | 276 `cheat` sheets | `git clone` |
| `/opt/metasploit-framework` | Metasploit 6.5.x with Postgres | omnibus installer |
| `/opt/chrome` | Chrome for Testing used by `chrome-devtools-mcp` (needs libatk/libgbm/libasound and friends) | `@puppeteer/browsers` |
| `/opt/john/jumbo` | John the Ripper jumbo; `/usr/local/bin/john` wraps it | source build |

PATH is assembled in `/etc/profile.d/10-redteam.sh` and sourced from `/etc/zsh/zshenv` so every zsh invocation sees it. Order matters: `/opt/node/bin`, `/opt/go126/bin`, `/opt/tools`, `/opt/segfault/bin`, `~/.local/bin`.

## The gate

```sh
redteam-check          # fast: command resolution only
redteam-check --full   # also runs one --version/--help per tool with a 25s timeout
```

Expected tail: `ok=103 missing=0`. A non-zero `missing` count names the tool and its category. The script lives at `/opt/redteam-check.sh` and is symlinked to `/usr/local/bin/redteam-check`.

## Install on a clean host

```sh
git clone https://github.com/<you>/meowpi.git && cd meowpi
bash scripts/install-redteam-toolchain.sh          # apt, pipx, Go, releases, wordlists, msf
bash scripts/install-host-config.sh                # zsh, p10k, ssh, vim, tern, claude-free shell
```

Order is fixed: apt first (provides compilers and libraries), then Go, then pipx, then releases, then Metasploit last (it pulls its own Ruby).

## Version traps worth remembering

| Trap | Symptom | Fix |
| --- | --- | --- |
| `seclists` / `wordlists` are Kali-only | apt aborts the whole batch with "unable to locate" | clone SecLists; extract rockyou from `Passwords/Leaked-Databases/rockyou.txt.tar.gz` |
| egress proxy 404s some PyPI names (`netexec`, `enum4linux-ng`, `aisbom`, `power-pwn`) | pip says `(from versions: none)` | install from git instead of PyPI |
| nuclei's `sonic/ast` needs Go ≤ 1.26 | `WARNING: sonic/ast only supports (go1.17~1.26)`; `code:` templates silently skip | build nuclei with `/opt/go126/bin/go` |
| `go install` refuses cross-compilation when `GOBIN` is set | `cannot install cross-compiled binaries when GOBIN is set` | clone the repo and `GOOS=windows go build -o out.exe ./cmd/...` |
| `msfdb init` refuses root | `Please run msfdb as a non-root user` | create the Postgres role/db and write `~/.msf4/database.yml` by hand |
| `mitmproxy-mcp` breaks on `mcp` 2.x | `ModuleNotFoundError: mcp.server.fastmcp` | `pipx inject mitmproxy-mcp 'mcp<2'` |
| pipx entry points are not `impacket-*` | `impacket-psexec: not found` | use `psexec.py`, `secretsdump.py`, `ntlmrelayx.py` |
| `bat` is `batcat` on Ubuntu | shell aliases silently fail | alias `bat=batcat`, or call `batcat -pp` |
| Ubuntu's `john` package is core, not jumbo | `--list=formats` and `--format=nt` are rejected; no NTLM support | build jumbo into `/opt/john/jumbo` and wrapper it at `/usr/local/bin/john` |
| `hashcat` ships without an OpenCL loader | `ATTENTION! No OpenCL, Metal, HIP or CUDA installation found.` | `apt install ocl-icd-libopencl1 pocl-opencl-icd` (≈44 MH/s MD5 on this 2 vCPU box) |
| Chrome for Testing lacks 11 shared libraries | `error while loading shared libraries: libatk-1.0.so.0` | `apt install libatk1.0-0t64 libatk-bridge2.0-0t64 libatspi2.0-0t64 libcups2t64 libasound2t64 libgbm1 libpango-1.0-0 libXcomposite1 libXdamage1 libXfixes3 libXrandr2` |
| `enum4linux-ng` exits before parsing arguments | `tools are missing: nmblookup, net` | `apt install samba-common-bin` |
| `/usr/bin/jq` is a jaq 3.1.1 build on this image | `jq --version` prints `jaq`, esoteric builtins differ | real jq 1.8.2 installed at `/opt/tools/jq`, which wins on PATH; use it in scripts |
| jumbo finds no `john.conf` when invoked through a symlink | `fopen: /usr/local/bin/john.conf` | invoke the wrapper script, or set `JOHN=/opt/john/jumbo` |

## Shell and host config

| File | Purpose |
| --- | --- |
| `~/.zshrc` | oh-my-zsh, p10k, plugin set, aliases (`nxc`, `secretsdump`, `smb`, `winrm`), functions (`rs`, `listen`, `scan`, `sweep`, `webscan`, `p10k`) |
| `~/.p10k.zsh` | lean two-line prompt, nerd-font mode, `P10K_ASCII=1` fallback |
| `/opt/segfault/shellrc.sh` | `PROXY`/`TOR`, `hl`, `hgrep`, `lsg`, opsec rate caps on nuclei/httpx |
| `/etc/ssh/ssh_config.d/99-redteam.conf` | legacy kex for old targets, `StrictHostKeyChecking accept-new`, keepalives |
| `/etc/vim/vimrc.local` | no swap, empty viminfo, search settings |
| `/etc/proxychains4.conf` | `dynamic_chain`, `quiet_mode`, `socks5 127.0.0.1 1080` |
| `~/.config/tern/settings.json` | `{"shell": "/bin/zsh"}` — otherwise Tern panes start bash |
| `~/.omp/agent/mcp.json` | `mitmproxy` and `chrome-devtools` MCP servers |

## Metasploit database

```sh
systemctl status postgresql
msfconsole -q -x 'db_status; exit'     # expect: Connected to msf. Connection type: postgresql.
```

`msfdb init` cannot run as root. The role `msf`, database `msf`, and `~/.msf4/database.yml` are created manually; re-create them with the same three SQL statements if Postgres is reinstalled.

## Updating

```sh
# Go tools
GOBIN=/opt/tools /opt/go126/bin/go install github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
/opt/tools/nuclei -update-templates

# Python tools
pipx upgrade-all

# Metasploit
msfupdate

# Wordlists
cd /opt/repos/SecLists && git pull --ff-only && cd /opt/repos/PayloadsAllTheThings && git pull --ff-only
```

After any update run `redteam-check --full`. A tool that resolves but errors on `--version` is a broken install, not a missing one.

## Verification

```sh
redteam-check --full | tail -5
zsh -ic 'nxc --version'                       # 1.5.x
zsh -ic 'nuclei -version 2>&1 | grep -ci sonic'   # 0 (Go 1.26 pin working)
john --list=build-info | head -1              # 1.9.0-jumbo-1
hashcat -I | grep -c 'cpu-'                   # >=1 pocl device
msfconsole -q -x 'db_status; exit'            # Connected to msf. postgresql
ldd /opt/chrome/chrome/linux-*/chrome-linux64/chrome | grep -c 'not found'   # 0
du -sh /opt/tools /opt/repos/SecLists /opt/cheatsheets
```

## Related skills

- [toolchain-router](../toolchain-router/SKILL.md) to choose a tool for a task
- [shell-environment](../shell-environment/SKILL.md) for zsh, PATH and prompt repair
- [wordlists](../wordlists/SKILL.md) for list selection
- [web-traffic-js-reversing](../web-traffic-js-reversing/SKILL.md) for the proxy and JS stack