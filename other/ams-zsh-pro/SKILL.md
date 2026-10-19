---
name: zsh-pro
description: Zsh guidance — interactive shell mastery, completion, prompt themes, plugins, and scripting differences from bash.
category: development
---

## Overview

Zsh is the interactive shell of choice for most developers: best-in-class completion, powerful globbing, shared history, spelling correction, and a prompt system that shows git state, exit codes, and timing at a glance. It's the default on macOS and the upgrade most Linux users make within a week.

Zsh's power comes with configuration surface — plugins, frameworks, and options that can slow startup to a crawl if unmanaged. This skill covers interactive mastery (completion, history, prompt), sane plugin management, and the scripting differences from bash that bite when scripts assume one or the other.

## When to use

- Setting up or tuning an interactive zsh environment.
- Fixing slow shell startup.
- Writing zsh completion or customizing completion behavior.
- Choosing a prompt theme or plugin manager.
- Writing scripts that must run under zsh vs bash.
- Debugging quoting/globbing differences from bash.

## Core concepts

- **Completion system.** `compinit` + `zstyle` — context-aware completion for commands, flags, files, git branches, and hosts. More powerful than bash's; configure matchers (case-insensitive, substring) via zstyle. Slow `compinit` (dumping on every start) is a classic startup drag — cache the dump.
- **Prompt.** `PROMPT`/`RPROMPT` with `%` escapes, or frameworks (Powerlevel10k, Starship). Show: cwd, git branch/status, exit code of last command, background jobs. Instant prompt (p10k) eliminates theme render lag.
- **History.** Shared across sessions (`SHARE_HISTORY`), huge sizes (`HISTSIZE=100000`), deduplication (`HIST_IGNORE_ALL_DUPS`), timestamps (`EXTENDED_HISTORY`). Your history is a knowledge base — make it searchable (Ctrl-R with fzf).
- **Globbing.** Extended glob (`setopt EXTENDED_GLOB`): `**/` recursive, `*(.)` plain files, `*(/)` directories, `^` negation, `**/*(.Lm+10)` files over 10MB. Glob qualifiers replace many `find` invocations interactively.
- **ZLE (line editor).** The readline equivalent: custom widgets, keybindings (`bindkey`), vi-mode (`bindkey -v`) or emacs-mode. Bind fzf to Ctrl-R/Ctrl-T/Alt-C for fuzzy history/file/directory search.
- **Options (`setopt`).** Hundreds of toggles: `AUTO_CD` (type a directory to cd), `CORRECT` (spelling correction), `EXTENDED_GLOB`, `NO_BEEP`, `INTERACTIVE_COMMENTS`. `emulate -L zsh` in functions for predictable option scope.
- **Arrays are 1-indexed.** `$arr[1]` is the first element (unlike bash's 0). `${arr[@]}` still expands all. This bites in every ported script.
- **No word splitting by default.** Unquoted `$var` does NOT split in zsh (unlike bash) — safer interactively, but `${=var}` forces splitting when needed. Scripts relying on bash splitting break silently.
- **Plugin managers.** Antidote, zplug, sheldon (fast, declarative) vs Oh My Zsh (huge, slow without care). Lazy-load heavy plugins (nvm, pyenv, docker) — load them on first use, not at startup.
- **Startup files.** `.zshenv` (always) → `.zprofile` (login) → `.zshrc` (interactive) → `.zlogin` (login, after zshrc). Put env in `.zshenv`, interactive config in `.zshrc`; keep login shells' PATH setup in `.zprofile`.
- **Profiling startup.** `zprof` module or `time zsh -i -c exit` — measure before optimizing; the usual culprits are nvm/pyenv/rbenv init and compinit dumps.
- **fzf integration.** The multiplier: fuzzy history, file, directory, and process search bound to keys. Install once, use hundreds of times daily.
- **Directory navigation.** `AUTO_CD` (type a dirname to cd), `AUTO_PUSHD` + `DIRSTACKSIZE` (every cd pushed; `dirs -v`, `cd -3` to jump back) — a directory stack replacing cd-history plugins.

## Practical workflow

1. **Profile first.** Time your startup; anything over ~200ms deserves investigation:
   ```zsh
   time zsh -i -c exit          # total startup time
   zmodload zsh/zprof && zprof  # per-function breakdown (add at top/bottom of .zshrc)
   ```
2. **Lazy-load version managers.** The classic fix — nvm/pyenv shims on PATH, full init on first use:
   ```zsh
   # instead of: eval "$(pyenv init -)"  (slow every shell)
   # use a lazy loader or a fast manager; measure the difference
   ```
3. **Configure completion.** Case-insensitive, substring matching, cached dump:
   ```zsh
   autoload -Uz compinit
   compinit -C  # -C skips the security check for speed (safe on single-user machines)
   zstyle ':completion:*' matcher-list 'm:{a-z}={A-Za-z}' 'r:|=*' 'l:|=* r:|=*'
   ```
4. **Set up history.** Large, shared, deduplicated, timestamped:
   ```zsh
   HISTSIZE=100000; SAVEHIST=100000; HISTFILE=~/.zsh_history
   setopt SHARE_HISTORY HIST_IGNORE_ALL_DUPS EXTENDED_HISTORY HIST_REDUCE_BLANKS
   ```
5. **Pick a fast prompt.** Powerlevel10k with instant prompt, or Starship (cross-shell). Show git status, exit codes, and async segments that never block typing.
6. **Bind fzf.** Ctrl-R (history), Ctrl-T (files), Alt-C (cd), plus custom widgets (kill process, checkout branch, ssh host).
7. **Learn the globs.** `ls **/*.test.ts`, `rm *(.)` (files only), `cd **/target` — extended globbing replaces pipelines interactively.
8. **Keep scripting portable.** For scripts, either target bash explicitly (`#!/usr/bin/env bash`) or write zsh-aware code (`emulate -L zsh`, 1-indexed arrays, `${=}` for splitting). Don't let interactive conveniences leak into scripts.

## Common pitfalls

- **Slow startup accepted** — 2s shells every new terminal; profile and lazy-load.
- **Oh My Zsh plugin sprawl** — dozens of plugins each adding milliseconds; audit ruthlessly.
- **`compinit` without `-C`** — security check on every start; cache it.
- **Bash-isms in zsh scripts** — 0-indexed arrays, word splitting assumptions; test scripts under the right shell.
- **Zsh-isms in bash scripts** — `#!/bin/sh` with zsh-only syntax; match shebang to features used.
- **Prompt blocking on git** — slow prompts in huge repos; async segments or simplified git status.
- **No shared history** — each terminal an island; `SHARE_HISTORY` unites them.
- **Overwriting `.zshenv`** — env vars in `.zshrc` invisible to non-interactive tools; understand the file order.
- **Correction annoyance** — `CORRECT` "correcting" intentional commands; tune or disable per-command with `nocorrect`.
- **Unquoted globs failing** — `setopt NOMATCH` making `scp host:*` error; quote remote patterns or set `NO_NOMATCH`.
- **Plugin manager lock-in** — framework-specific config; prefer plain zsh + a fast declarative manager.
- **Ignoring `emulate -L zsh`** — functions inheriting caller's options; scope options in functions.
- **Starship/p10k misconfigured** — transient prompt losing scrollback context; configure deliberately.
