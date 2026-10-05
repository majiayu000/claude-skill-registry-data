---
name: ghostty-terminfo
description: Use when SSHing to a remote host from Ghostty terminal and encountering terminfo errors, missing colors, broken key bindings, "unknown terminal type" warnings, or an entry that looks installed but still does not resolve
---

# Ghostty Terminfo Installation

## Overview

Ghostty uses `xterm-ghostty` as its `$TERM` value. Remote hosts that lack this terminfo entry will show broken terminal behavior. The fix is to transfer the terminfo from the local machine to the remote host.

`tic` run as a normal user writes to `~/.terminfo`, which ncurses searches before the system directory. No sudo, and nothing to add to shell rc files.

## When to Use

- Remote SSH sessions show "unknown terminal type xterm-ghostty"
- Missing colors, broken backspace/arrow keys, or garbled output over SSH
- Setting up a new remote host for use with Ghostty
- Writing SSH scripts that should handle Ghostty terminfo automatically
- The entry appears to be installed on the host, but SSH sessions are still broken

## Quick Reference

| Task | Command |
|------|---------|
| Check if remote has terminfo | `ssh HOST 'infocmp xterm-ghostty >/dev/null 2>&1'` |
| Install terminfo on remote | `infocmp -x xterm-ghostty \| ssh HOST tic -x -` |
| One-liner check + install | `ssh HOST 'infocmp xterm-ghostty >/dev/null 2>&1' \|\| infocmp -x xterm-ghostty \| ssh HOST tic -x -` |
| Verify after install | `ssh HOST 'infocmp -x xterm-ghostty 2>/dev/null \| grep -q Smulx && echo OK'` |
| Show the terminfo search path | `ssh HOST 'infocmp -D'` |

## Implementation

### Local Install

If you're already on the machine, just pipe it directly to `tic`:

```bash
infocmp -x xterm-ghostty | tic -x -
```

### One-Time Install

```bash
infocmp -x xterm-ghostty | ssh user@host tic -x -
```

This exports the local terminfo and compiles it on the remote host. Only needs to run once per remote machine.

It lands in the remote user's `~/.terminfo`. Because the entry declares aliases (`xterm-ghostty|ghostty|Ghostty`), `tic` writes two files — the name and the alias:

```
~/.terminfo/78/xterm-ghostty
~/.terminfo/67/ghostty
```

Re-running the install is safe and idempotent; see Common Mistakes for the warnings it prints.

### Conditional Install in SSH Scripts

```bash
if [ "$TERM" = "xterm-ghostty" ]; then
  ssh "$HOST" 'infocmp xterm-ghostty >/dev/null 2>&1' || \
    infocmp -x xterm-ghostty | ssh "$HOST" tic -x -
fi
```

Only runs when connecting from Ghostty, skips if already installed.

## Verifying Properly

Plain `infocmp xterm-ghostty` succeeding only proves *an* entry exists — not that the extended capabilities survived, which is the entire point of the `-x` flags. Check for an extended capability instead:

```bash
ssh HOST 'infocmp -x xterm-ghostty 2>/dev/null | grep -q Smulx && echo OK'
```

`Smulx`, `setrgbf`, `setrgbb`, `Sync` and `fullkbd` are the extended caps Ghostty ships. To prove the entry is genuinely identical to the local one, compare the compiled bytes rather than `infocmp` text — the text rendering varies with ncurses version (hex vs decimal `colors#256`, `\n` vs `^J`, escaped vs unescaped colons), so textual diffs manufacture false positives:

```bash
md5 -q ~/.terminfo/78/xterm-ghostty                                    # remote
md5 -q /Applications/Ghostty.app/Contents/Resources/terminfo/78/xterm-ghostty   # local
```

## Troubleshooting: The Entry Exists but SSH Is Still Broken

A compiled entry can be present on the host, byte-identical to the local one, and still be invisible to the terminal. **Presence and resolvability are separate conditions.** ncurses only searches `~/.terminfo` and the compiled-in system directory:

```bash
$ ssh HOST 'infocmp -D'
/Users/someone/.terminfo
/usr/share/terminfo
```

`infocmp -D` lists only directories that exist. On a host that has never had a user entry it prints `/usr/share/terminfo` alone, yet ncurses still searches `~/.terminfo` — the line appears as soon as `tic` creates the directory, so a normal install is still the fix.

An entry anywhere else — most often `/usr/local/share/terminfo` — resolves only if `TERMINFO_DIRS` points at it, and that is exported per-shell. So the same host can pass a check under one shell and fail under another:

```bash
$ ssh HOST 'zsh  -lc "echo TERMINFO_DIRS=\$TERMINFO_DIRS"'   # zsh ignores /etc/profile
TERMINFO_DIRS=
$ ssh HOST 'bash -lc "echo TERMINFO_DIRS=\$TERMINFO_DIRS"'   # /etc/profile exports it
TERMINFO_DIRS=/usr/local/share/terminfo:
```

When zsh is the login shell, that install is broken in practice while a `bash -l` spot check says it is fine.

Find every copy on the host, then compare against the search path above:

```bash
ssh HOST 'for d in ~/.terminfo /usr/local/share/terminfo /etc/terminfo \
                   /usr/share/terminfo /lib/terminfo; do
            find "$d" -name "*ghostty*" 2>/dev/null
          done'
```

Anything outside the `infocmp -D` directories does not exist as far as the terminal is concerned. Do a normal `~/.terminfo` install; the stray copy is then inert and can be removed.

## Common Mistakes

- **Trusting `ls` or a checksum over the search path** - finding the compiled file on the host proves nothing about whether ncurses can reach it. `infocmp -D` is the check that settles it.
- **Reading `tic`'s warnings as failure** - `tic` prints `older tic versions may treat the description field as an alias` on a first install, and additionally `alias ghostty multiply defined.` when re-run on a host that already has the entry. Both exit 0 and leave a correct entry; the read-back verify is the real verdict.
- **Reaching for sudo or a system-wide install** - on macOS `/usr/share/terminfo` is on the sealed read-only system volume, so `tic -o` there fails even as root with SIP disabled. `~/.terminfo` is the supported target, not a fallback.
- **Running from non-Ghostty terminal** - `infocmp xterm-ghostty` fails if the local machine doesn't have the terminfo. Run from Ghostty or a machine with Ghostty installed.
- **Forgetting `-x` flag** - Both `infocmp -x` and `tic -x` need the extended flag to preserve Ghostty's extended capabilities.
- **Workaround instead of fix** - Setting `TERM=xterm-256color` before SSH works but loses Ghostty-specific features. Install the terminfo instead.
- **Assuming `tic` is missing when a piped install fails** - on some hosts the non-interactive SSH shell has a trimmed `PATH` without the ncurses tools. Confirm with `ssh HOST 'command -v tic'` before working around it; if it really is absent, prefix the remote command with `PATH=/usr/bin:/bin`.
