---
name: shell-scripting
description: >
  Write and debug Bash, Zsh, POSIX sh, and Fish scripts, commands, quoting, dotfiles, and shell completions.
license: MIT
compatibility: "Use sh, Bash, or Zsh for POSIX examples; Fish and Nushell require their dedicated syntax. Optional: shellcheck, dash (strict POSIX check)"
metadata:
  source: iuliandita/skills
  date_added: "2026-03-25"
  effort: medium
  argument_hint: "<task-or-shell>"
---

# Shell Scripting and Configuration

Write commands, scripts, dotfiles, and completions for their actual shell. Detect the target before
writing code, then load the smallest relevant reference instead of borrowing syntax from a similar
shell.

**Version-specific behavior**: read the matching shell reference before relying on release-specific behavior.

## When to use

- Writing shell commands, scripts, or one-liners
- Configuring dotfiles (`.zshrc`, `.bashrc`, `.profile`, `config.fish`)
- Writing completions, shell functions, or aliases
- Porting scripts between shells or debugging quoting, globbing, array, or expansion behavior
- Choosing a target shell for a new script or interactive command

## When NOT to use

- Remote FreeBSD/OPNsense/pfSense commands; use **opnsense-pfsense**
- Ansible shell/command modules; use **ansible**
- CI/CD pipeline design or runner constraints; use **ci-cd**
- General Linux administration that is not a shell-syntax task; do the domain task directly

## AI Self-Check

- [ ] Shebang matches the detected target shell, not an assumed Bash default
- [ ] Error handling matches the declared shell; expected nonzero statuses are handled deliberately
- [ ] Variables are double-quoted unless word splitting is intentional
- [ ] No wrong-shell syntax appears (`[[ ]]` in sh, `BASH_SOURCE` in Zsh, Bash arrays in sh)
- [ ] Array indexing matches the target shell (Bash 0-indexed, Zsh/Fish 1-indexed, no sh arrays)
- [ ] `printf` replaces non-trivial `echo`; globs and temporary files have safe cleanup/empty cases
- [ ] Commands do not expose secrets in history or process arguments
- [ ] Examples were checked with paths containing spaces, empty variables, and glob characters
- [ ] Cross-cutting agent hygiene applied; read `references/agent-hygiene.md` when relevant

## Workflow

### 1. Detect the shell

Read an existing script's shebang first. Otherwise use the file convention, stated deployment
environment, and user context. `$SHELL` normally identifies the login shell, not necessarily the
process running a script.

| Signal | Default route |
|---|---|
| `#!/bin/sh`, minimal Alpine/BusyBox, maximum portability | POSIX sh |
| `#!/usr/bin/env bash`, portable featureful script, common CI/container image | Bash |
| `.zsh`, `.zshrc`, interactive local shell | Zsh |
| `.fish`, `config.fish` | Fish |
| BSD firewall/appliance context | **opnsense-pfsense** |

### 2. Load only the needed reference

- Read `references/bash.md`, `references/zsh.md`, `references/posix-sh.md`, or
  `references/alt-shells.md` for the selected shell; load two only when porting between them.
- Read `references/advanced-patterns.md` for portable redirection/quoting, traps, cleanup, jobs,
  signals, process termination, or a Zsh completion.
- Read `references/ssh-tmux-autostart.md` only for interactive SSH startup that attaches to tmux.

### 3. Write, parse, and exercise the behavior

Use explicit error handling that the selected shell supports. Keep scripts non-interactive unless the
task needs interaction, and use `--` before user-controlled paths for commands that accept it.
Preview destructive expansions before `rm`, `mv`, `chmod`, `chown`, or recursive edits.

Run the parser for the target (`bash -n`, `zsh -n`, or `sh -n`) and, for sh/Bash, ShellCheck when
`command -v shellcheck` finds it. Fix every reported error and rerun until both pass. A completion
also needs a real Tab press after `compinit`; parsing alone does not test discovery. Report commands
run and any unavailable checks.

## Verification Checklist

- [ ] The shebang, shell features, indexing, and strict-mode behavior agree
- [ ] Expected failures, pipeline status, cleanup traps, and signal exits were exercised
- [ ] Quoting and empty-glob behavior were exercised with adversarial filenames/values
- [ ] Generated scripts parse in the selected shell; sh/Bash scripts pass ShellCheck when available
- [ ] Completion files load under `compinit` and route at least one real completion request

## Reference Files

- `references/bash.md` - Bash syntax, arrays, parameter expansion, traps, heredocs, and templates
- `references/zsh.md` - Zsh arrays, qualifiers, expansion, completions, hooks, and dotfiles
- `references/posix-sh.md` - portable sh constructs and Bashism avoidance
- `references/alt-shells.md` - Fish, tcsh/csh, Nushell, Elvish, and Oils boundaries
- `references/advanced-patterns.md` - cross-shell comparison, safe portable constructs, traps, jobs,
  and Zsh completion skeletons
- `references/ssh-tmux-autostart.md` - safe interactive SSH-to-tmux startup

## Output Contract

See `references/output-contract.md` for the full contract.

- **Skill name:** SHELL-SCRIPTING
- **Deliverable bucket:** `audits`
- **Mode:** conditional. For an audit or review of existing shell content, apply the reporting rules
  in the local contract and write `docs/local/audits/shell-scripting/<YYYY-MM-DD>-<slug>.md`.
  Writing a script, dotfile, completion, or explanation remains conversational.
- **Severity scale:** `P0 | P1 | P2 | P3 | info`

## Related Skills

- **opnsense-pfsense** - FreeBSD firewall/appliance shell context
- **ansible** - playbook shell and command-module behavior
- **ci-cd** - pipeline design and restricted execution environments
- **networking**, **debian-ubuntu**, and **rhel-fedora** - system/domain administration; this skill
  supplies the shell syntax when those tasks require it

## Rules

The AI Self-Check covers quoting, wrong-shell syntax, and error handling; these are the two
constraints everything else depends on:

1. **Detect the shell first.** Do not assume Bash from a code-looking request.
2. **Do not expose secrets or run destructive expansions blindly.** Use secure input paths and preview
   exact targets before a state-changing command.
