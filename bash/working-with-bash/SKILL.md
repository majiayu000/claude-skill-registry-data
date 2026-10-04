---
name: working-with-bash
description: "Use when working with Bash — any bash command, builtin, option (shopt/set -o), special variable, parameter expansion, test operator ([[ ]] vs [ ]), glob (extglob/globstar), or redirection lookup; writing/fixing .bashrc/.bash_profile/.inputrc; POSIX-sh portability and Bash↔Zsh differences; strict mode (set -euo pipefail) and quoting/word-splitting bugs; completion (complete/compgen, bash-completion); Readline bindings and history; choosing a framework (oh-my-bash, bash-it), package manager (basher, bpkg), prompt (Starship, Oh My Posh, Powerline, bash-git-prompt), or readline enhancers (ble.sh, bash-preexec); and linting/formatting/testing (ShellCheck, shfmt, bats-core). Bundles the version-exact man bash, the GNU Bash Reference/Readline/History manuals, ecosystem READMEs, a community corpus (pure-bash-bible, Google style guide, POSIX spec, BashPitfalls), and hand-written guides. Invoke for any bash command/option/concept lookup, a 'how do I do X in bash' question, tool selection, or script debugging."
metadata:
  last_updated: "2026-06-16"
---

# Working with Bash

Comprehensive, self-updating Bash reference: the **complete official manual** (man page
+ GNU manuals), the **ecosystem** (frameworks, managers, prompts, plugins, quality
tooling), a **community learning corpus**, and hand-written **migration + cookbook guides**.

Four reference buckets, three provenance models:

- **`references/manual/`** — the official Bash reference. Two provenances in one bucket:
  - `bash.md` / `bashbug.md` — generated **verbatim** from the pinned `bash`'s own man
    pages (`man bash`). **Version-exact** to [`PINNED_VERSION`](PINNED_VERSION) (currently
    `bash 5.3.9`). Ground truth for any syntax/option/builtin question, and `grep`-friendly.
  - `bash-reference-manual.md`, `readline.md`, `history.md` — the GNU **Bash Reference
    Manual**, **Readline**, and **History** manuals, **snapshot-fetched** from gnu.org /
    Chet Ramey's site. Bash ships ONE monolithic man page, so these add the readable,
    chapter-organized view (and Readline/History detail the man page only summarizes).
- **`references/ecosystem/`** — upstream READMEs for the tooling ecosystem (oh-my-bash,
  bash-it, basher, bpkg, bash-completion, ble.sh, prompts, fzf/zoxide, ShellCheck, shfmt,
  bats-core). **Snapshot-fetched**; refreshed weekly by CI.
- **`references/learn/`** — the community learning corpus (BashFAQ, BashGuide,
  BashPitfalls, Chet's FAQ, pure-bash-bible, bash-handbook, Google Shell Style Guide,
  the POSIX shell spec). **Snapshot-fetched.**
- **`references/guides/`** — hand-written value-add: orientation, Bash↔Zsh / Bash↔POSIX
  migration, framework/manager/prompt comparisons, a cookbook, and a pitfalls/safety guide.

## When to use

- Any `bash` command, builtin, `shopt`/`set -o` option, special variable, parameter
  expansion, `[[ ]]` test operator, glob (`extglob`/`globstar`), or redirection lookup.
- Writing or fixing `.bashrc` / `.bash_profile` / `.profile` / `.inputrc`; understanding
  startup-file order (login vs interactive vs non-interactive).
- Making a script safe (`set -euo pipefail`, quoting, word-splitting) or portable
  (Bash → POSIX `sh`), or debugging a script that misbehaves.
- Bash → Zsh migration, or vice-versa.
- Choosing a framework (oh-my-bash / bash-it), a package/plugin manager (basher / bpkg),
  a prompt (Starship / Oh My Posh / Powerline / bash-git-prompt / liquidprompt), or
  readline enhancers (ble.sh / bash-preexec).
- Programmable completion (`complete`, `compgen`, bash-completion) or Readline bindings.
- Linting/formatting/testing scripts (ShellCheck, shfmt, bats-core).

## Quick reference

| I need to… | Read |
| --- | --- |
| Orient / find the right doc fast | [`references/guides/overview.md`](references/guides/overview.md) |
| Migrate Bash↔Zsh, or make a script POSIX-portable | [`references/guides/bash-vs-zsh.md`](references/guides/bash-vs-zsh.md) |
| Choose/compare a framework or package manager | [`references/guides/frameworks-and-managers.md`](references/guides/frameworks-and-managers.md) |
| Choose/compare a prompt | [`references/guides/prompts.md`](references/guides/prompts.md) |
| Practical recipes (arrays, expansion, globbing, traps, completion, history) | [`references/guides/cookbook.md`](references/guides/cookbook.md) |
| Avoid quoting/word-splitting bugs; write safe scripts | [`references/guides/pitfalls-and-safety.md`](references/guides/pitfalls-and-safety.md) |
| The full shell reference (grammar, expansion, builtins, variables) | [`references/manual/bash.md`](references/manual/bash.md) |
| The same, organized as readable prose | [`references/manual/bash-reference-manual.md`](references/manual/bash-reference-manual.md) |
| Readline: key bindings, `.inputrc`, editing modes | [`references/manual/readline.md`](references/manual/readline.md) |
| History expansion (`!!`, `!$`, `^old^new`) and config | [`references/manual/history.md`](references/manual/history.md) |
| Common bash mistakes (the canonical BashPitfalls list) | [`references/learn/bashpitfalls.md`](references/learn/bashpitfalls.md) |
| Greg's BashFAQ / BashGuide (linked externally — fragile wiki) | [`references/guides/pitfalls-and-safety.md`](references/guides/pitfalls-and-safety.md) |
| Pure-bash idioms (no external processes) | [`references/learn/pure-bash-bible.md`](references/learn/pure-bash-bible.md) |
| Style conventions | [`references/learn/google-shell-style-guide.md`](references/learn/google-shell-style-guide.md) |
| POSIX portability ground truth | [`references/learn/posix-shell-spec.md`](references/learn/posix-shell-spec.md) |
| A specific framework/manager/prompt/tool README | `references/ecosystem/<name>__readme.md` |

## How to use

1. **Syntax / behavior questions** → start in [`references/manual/bash.md`](references/manual/bash.md)
   (verbatim, version-exact, `grep`-friendly). For a readable walk-through of the same
   material, use [`bash-reference-manual.md`](references/manual/bash-reference-manual.md).
2. **"How do I…" / recipes** → [`references/guides/cookbook.md`](references/guides/cookbook.md)
   first, then the relevant manual section.
3. **A script breaks or behaves surprisingly** → [`references/guides/pitfalls-and-safety.md`](references/guides/pitfalls-and-safety.md)
   and [`references/learn/bashpitfalls.md`](references/learn/bashpitfalls.md); run it through ShellCheck.
4. **Portability / migration** → [`references/guides/bash-vs-zsh.md`](references/guides/bash-vs-zsh.md)
   (covers Bash↔Zsh and Bash↔POSIX `sh`).
5. **Tooling choices** → [`references/guides/frameworks-and-managers.md`](references/guides/frameworks-and-managers.md)
   and [`prompts.md`](references/guides/prompts.md); the matching `references/ecosystem/*__readme.md`
   has the upstream detail.

## Maintenance

- [`scripts/update_docs.js`](scripts/update_docs.js) regenerates `references/manual/`'s
  man pages from the pinned `bash` (graceful skip when bash is absent or != the pin), and
  re-fetches the GNU manuals, `references/ecosystem/`, and `references/learn/`. Run via
  `make update-working-with-bash`.
- Each reference file carries `source` / `fetched_at` / `sha256` frontmatter; `fetched_at`
  only advances when upstream content actually changes. The weekly CI action refreshes the
  fetched docs; the version-exact man pages only regenerate when the pin is bumped locally.
- `references/guides/*` are hand-written and **not** touched by the update script.

## Related skills

- `working-with-zsh` — the Zsh counterpart (same manual/ecosystem/guides pattern); pair
  them for cross-shell questions.
- `working-with-git` — git itself (the manual/cookbook pattern mirrors it).
- `agent-instructions` — authoring shell/agent config files.
- `authoring-agent-skills` — the doc-wrapper + freshness conventions this skill follows.
