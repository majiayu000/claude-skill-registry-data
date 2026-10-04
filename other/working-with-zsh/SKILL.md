---
name: working-with-zsh
description: "Use when working with Zsh — any zsh command, builtin, option (setopt), glob qualifier, parameter/special variable, or expansion lookup; Bash→Zsh migration and behavioral differences; .zshrc/.zshenv/startup-file configuration; the completion system (compinit/zstyle) and ZLE/bindkey line editing; frameworks (Oh My Zsh, Prezto, Zim); plugin managers (zinit, antidote, sheldon, antigen, zplug); prompts (Powerlevel10k, Starship, Oh My Posh); and popular plugins (zsh-autosuggestions, zsh-syntax-highlighting, fzf, zoxide). The manual under references/manual/ is generated VERBATIM from the pinned zsh's own man pages (version-exact); references/ecosystem/ holds snapshot-fetched upstream docs; references/guides/ holds hand-written migration/comparison/cookbook guides. Invoke for any zsh command/option/concept lookup, a 'how do I do X in zsh' question, framework/manager/prompt selection, or a Bash-script-breaks-under-zsh debugging session."
metadata:
  last_updated: "2026-06-16"
---

# Working with Zsh

Comprehensive, self-updating Zsh reference: the **complete official manual**, the
**ecosystem** (frameworks, plugin managers, prompts, plugins), and hand-written
**migration + cookbook guides**.

Three reference buckets, three provenance models:

- **`references/manual/`** — the canonical Zsh manual, generated **verbatim** from the
  pinned `zsh`'s own man pages (`man zshexpn`, `man zshbuiltins`, …). **Version-exact**
  to the pin in [`PINNED_VERSION`](PINNED_VERSION) (currently `zsh 5.9`). This is ground
  truth for any syntax/option/builtin question.
- **`references/ecosystem/`** — upstream docs for the fast-moving ecosystem (Oh My Zsh,
  Prezto, zinit, antidote, Powerlevel10k, Starship, plugins, the FAQ, the User Guide,
  zsh-lovers). **Snapshot-fetched** (not version-pinned); refreshed weekly by CI.
- **`references/guides/`** — hand-written value-add: orientation, Bash↔Zsh migration,
  framework/manager/prompt comparisons, and a practical cookbook.

## When to use

- Any `zsh` command, builtin, `setopt` option, glob qualifier, parameter, or expansion lookup.
- Writing or fixing `.zshrc` / `.zshenv` / `.zprofile`; understanding startup-file order.
- Bash → Zsh migration, or debugging a Bash script that breaks under Zsh.
- Setting up or choosing a framework (Oh My Zsh / Prezto / Zim), a plugin manager
  (zinit / antidote / sheldon), or a prompt (Powerlevel10k / Starship / Oh My Posh).
- Configuring the completion system (`compinit`, `zstyle`) or ZLE key bindings (`bindkey`).

## Quick reference

| I need to… | Read |
| --- | --- |
| Orient / find the right doc fast | [`references/guides/overview.md`](references/guides/overview.md) |
| Migrate from Bash / fix a script that breaks under zsh | [`references/guides/bash-vs-zsh.md`](references/guides/bash-vs-zsh.md) |
| Choose/compare a framework or plugin manager | [`references/guides/frameworks-and-managers.md`](references/guides/frameworks-and-managers.md) |
| Choose/compare a prompt (P10k vs Starship vs Oh My Posh) | [`references/guides/prompts.md`](references/guides/prompts.md) |
| Practical recipes (globbing, zmv, expansion, completion, keybindings, history) | [`references/guides/cookbook.md`](references/guides/cookbook.md) |
| Expansion: history, glob, parameter, brace, modifiers | [`references/manual/zshexpn.md`](references/manual/zshexpn.md) |
| Builtins (`setopt`, `zstyle`, `bindkey`, `autoload`, …) | [`references/manual/zshbuiltins.md`](references/manual/zshbuiltins.md) |
| Options reference (incl. `SH_*`/`KSH_*` emulation) | [`references/manual/zshoptions.md`](references/manual/zshoptions.md) |
| Parameters / special variables | [`references/manual/zshparam.md`](references/manual/zshparam.md) |
| Grammar, redirection, functions, jobs, prompt `%` escapes | [`references/manual/zshmisc.md`](references/manual/zshmisc.md) |
| The completion system (`compinit`, `zstyle`) | [`references/manual/zshcompsys.md`](references/manual/zshcompsys.md) |
| ZLE line editor / `bindkey` / widgets | [`references/manual/zshzle.md`](references/manual/zshzle.md) |
| Modules (`zsh/mathfunc`, `zsh/zpty`, …) | [`references/manual/zshmodules.md`](references/manual/zshmodules.md) |
| Contributions (`vcs_info`, `zmv`, `zcalc`, `promptinit`) | [`references/manual/zshcontrib.md`](references/manual/zshcontrib.md) |
| Oh My Zsh (setup, plugin list, theme list) | [`references/ecosystem/oh-my-zsh__readme.md`](references/ecosystem/oh-my-zsh__readme.md), [`oh-my-zsh__plugins.md`](references/ecosystem/oh-my-zsh__plugins.md), [`oh-my-zsh__themes.md`](references/ecosystem/oh-my-zsh__themes.md) |
| FAQ / User Guide / zsh-lovers cookbook | [`references/ecosystem/faq.md`](references/ecosystem/faq.md), [`user-guide__00-toc.md`](references/ecosystem/user-guide__00-toc.md) (+ `user-guide__01`–`08`), [`zsh-lovers.md`](references/ecosystem/zsh-lovers.md) |
| A specific plugin/manager/prompt README | `references/ecosystem/<name>__readme.md` |

## How to use

1. **Syntax / behavior questions** → start in `references/manual/`. It is verbatim, version-exact
   man-page text — authoritative and `grep`-friendly. Use the chapter table above to jump.
2. **"How do I…" / recipes** → `references/guides/cookbook.md` first, then the relevant manual chapter.
3. **Migrating from Bash / a script errors under zsh** → `references/guides/bash-vs-zsh.md`
   (then `zshoptions.md` for `SH_WORD_SPLIT`, `KSH_ARRAYS`, and `emulate sh`).
4. **Tooling choices** → `references/guides/frameworks-and-managers.md` and `prompts.md` give a
   decision guide; the matching `references/ecosystem/*__readme.md` has the upstream detail.

## Maintenance

- [`scripts/update_docs.js`](scripts/update_docs.js) regenerates `references/manual/` from the
  pinned `zsh` man pages (graceful skip when zsh is absent or != pin) and re-fetches
  `references/ecosystem/`. Run via `make update-working-with-zsh`.
- Each reference file carries `source` / `fetched_at` / `sha256` frontmatter; `fetched_at`
  only advances when upstream content actually changes. The weekly CI action refreshes the
  ecosystem docs; the (frozen, release-tied) manual only regenerates when the pin is bumped locally.
- `references/guides/*` are hand-written and **not** touched by the update script.

## Related skills

- `working-with-git` — git itself (the manual/cookbook pattern mirrors it).
- `agent-instructions` — authoring shell/agent config files.
- `authoring-agent-skills` — the doc-wrapper + freshness conventions this skill follows.
