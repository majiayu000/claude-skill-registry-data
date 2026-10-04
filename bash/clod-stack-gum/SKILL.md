---
name: "Stack: Gum"
description: "Gum (charmbracelet/gum) reference: interactive shell prompts, styled output, spinners, logging and layout from shell scripts; every flag, keybinding and exit code verified against gum 2.0.1."
when_to_use: "When writing or debugging a shell script that uses gum (choose, confirm, filter, input, write, spin, style, format, join, table, pager, file, log) or when a script needs an interactive prompt, spinner or styled terminal output and gum is the obvious tool."
user-invocable: false
metadata:
  family: clod-stack
# No paths gate: gum calls live inside ordinary .sh/.zsh files and shell
# aliases, so file identity is an unreliable proxy for relevance
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
---

# Gum Operative

> Reference for `gum`, Charm's "tool for glamorous shell scripts".
> Sources: https://github.com/charmbracelet/gum (README, `examples/`, command source) and the installed binary.
> Verified against gum **v2.0.1** (released 2026-09-11; module path `charm.land/gum/v2`) on 2026-09-22.

## Trigger

Use when: a script calls `gum`, the user mentions gum or Charm, or a shell script needs a prompt, picker, confirmation, spinner, styled box or structured log line. Also use when Claude itself needs to render styled terminal output from a Bash call.

## Role

You are an expert in gum. You know every subcommand, its flags, its keybindings, its stdin/stdout contract and its exit codes. You write gum scripts that behave correctly on the first run, degrade sanely without a TTY and never leak UI chrome into captured output.

## 1. Mental model

Five facts explain almost everything:

1. **UI goes to stderr, results go to stdout.** Every interactive command draws its TUI on stderr, so `VAR=$(gum choose ...)` captures only the answer. `gum log` also writes to stderr by default.
2. **Exit codes carry meaning.** `0` success or "Yes". `1` "No", `esc`, nothing selected or a usage error. `124` timeout. `130` `ctrl+c`. `gum spin` returns the wrapped command's exit code.
3. **Every flag has an env var.** Pattern: `GUM_<COMMAND>_<FLAG>` (`--cursor.foreground` on `choose` is `GUM_CHOOSE_CURSOR_FOREGROUND`). `gum style` is the exception: its vars are unprefixed (`FOREGROUND`, `BORDER`, `PADDING`). Flags override env.
4. **Stdin is an input source for most commands.** `choose`, `filter` and `table` read options from stdin. `input` and `write` read an initial value from stdin. `confirm` reads a piped `y`/`yes` as an answer and skips the TUI. `pager`, `format` and `style` read content.
5. **Interactive commands need a TTY.** Without one they fail with `could not open TTY` and exit 1. Claude's Bash tool has no TTY, so only the non-interactive commands (`style`, `join`, `format`, `log`, `table --print`, `spin`, `version-check`, piped `confirm`, `choose --select-if-one`) can be run directly.

## 2. Command map

| Command | Does | Output on stdout |
|---|---|---|
| `choose` | Pick one or more items from a list | Selected item(s), newline-separated |
| `confirm` | Yes/No prompt | Nothing (exit code only) unless `--show-output` |
| `filter` | Fuzzy-search a list, pick one or more | Selected item(s) |
| `input` | Single-line text prompt | The text |
| `write` | Multi-line text prompt | The text |
| `file` | Pick a file or directory from a tree | Absolute path |
| `table` | Pick a row from CSV (or `--print` it) | Row as CSV; one column with `--return-column` |
| `pager` | Scroll through content with search | Nothing |
| `spin` | Show a spinner while a command runs | The command's output (see below) |
| `style` | Colour, border, padding, alignment on text | Styled text |
| `join` | Combine blocks horizontally or vertically | Combined block |
| `format` | Render markdown, code, template or emoji | Rendered text |
| `log` | Levelled, structured log lines | Nothing (writes to stderr, or `--file`) |
| `version-check` | Assert installed gum matches a semver constraint | Nothing (exit 0/1) |

Full flags, defaults, keybindings and per-command gotchas: [commands.md](commands.md).

## 3. Exit codes and control keys

| Event | Exit | Where it applies |
|---|---|---|
| Submit / affirmative | `0` | all |
| `esc`, negative, nothing selected | `1` | all interactive except `table` and `pager`, which exit 0 |
| `--timeout` elapsed | `124` | all interactive (except `confirm`, which returns its default) |
| `ctrl+c` | `130` | all interactive |
| Wrapped command failed | its code | `spin` |
| Invalid flag value | `1` with a `must be one of` message | all |

Universal keys: `enter` submits, `esc` quits, `ctrl+c` aborts. Multi-select toggles differ by command: `choose` uses `space`/`tab`/`x`, `filter` uses `tab`/`ctrl+@` (ctrl+space) so `space` can still be typed into the search. `ctrl+a` selects all in either when `--no-limit` is set.

## 4. Scripting patterns

### Capture and branch

```zsh
type=$(gum choose fix feat docs refactor test chore) || exit 1
scope=$(gum input --placeholder "scope (optional)")
[[ -n $scope ]] && scope="($scope)"
summary=$(gum input --value "$type$scope: " --placeholder "Summary")
body=$(gum write --placeholder "Details (enter submits, ctrl+j for a newline)")
gum confirm "Commit?" && git commit -m "$summary" -m "$body"
```

The `|| exit 1` after `choose` matters: `esc` and `ctrl+c` leave the variable empty and a script that carries on will act on nothing.

### Multi-select into a zsh array

```zsh
picked=("${(@f)$(gum choose --no-limit --header "Branches to delete" $(git branch --format='%(refname:short)'))}")
(( ${#picked} )) || exit 1
git branch -D "${picked[@]}"
```

`${(@f)...}` splits on newlines only, so items containing spaces survive. In bash use `mapfile -t picked < <(gum choose --no-limit ...)`.

### Pick from stdin, act with xargs

```zsh
brew list | gum choose --no-limit | xargs brew uninstall
git log --oneline | gum filter | cut -d' ' -f1
gh pr list | cut -f1,2 | gum choose | cut -f1 | xargs gh pr checkout
```

### Spinner with clean capture

```zsh
result=$(gum spin --title "Fetching..." --show-output -- curl -fsS "$url") || {
	gum log --level error "Fetch failed" url "$url"
	exit 1
}
```

The spinner draws on stderr, the command's stdout lands in `$result` and the exit code is the command's own.

### Pick or create

```zsh
name=$(printf '%s\n' $existing | gum filter --no-strict --placeholder "Pick or type a new name")
```

`--strict` (the default) only returns a matching item. `--no-strict` returns the typed filter text when nothing matches, which turns `filter` into a combo box.

### Non-interactive fallback

```zsh
if [[ -t 0 && -t 2 ]]; then
	answer=$(gum choose yes no)
else
	answer=${DEFAULT_ANSWER:-no}
fi
```

Tests for a TTY on stdin and stderr, because that is where gum reads keys and draws. A script that pipes into `gum confirm` can also answer it: `echo y | gum confirm` exits 0 without drawing anything.

### Version guard

```zsh
gum version-check '>=2.0.0' 2>/dev/null || { echo "gum >= 2.0.0 required" >&2; exit 1; }
```

## 5. Gotchas

- **`write` submits on `enter` in v2.** `ctrl+j` inserts a newline and `ctrl+e` opens `$EDITOR`. The README still says `ctrl+d`; the source does not bind it.
- **`confirm` defaults to Yes.** `--default` is `true`. Pass `--default=false` to start on No. On `--timeout` it returns that default; it never exits 124.
- **`input` has a 400-character limit by default.** Pass `--char-limit 0` for unlimited.
- **`choose` with both args and stdin treats stdin as `--selected`,** not as extra options. Feed options one way or the other.
- **`filter` multi-select output order is unstable** (Go map iteration). Use `choose --ordered` when selection order matters.
- **`choose --ordered` also sorts the displayed options alphabetically** before tracking selection order.
- **`filter` with no args and empty stdin lists files in the current directory,** which surprises scripts that expected an error.
- **`spin` only shows output on a TTY.** `--show-output` is a no-op when stdout is not a terminal; the command's output then passes straight through.
- **`file` needs `--file` or `--directory` true.** `--file` defaults to true, so `gum file --no-file` alone errors; add `--directory`.
- **`log -f` args are strings.** `%s` works, `%d` renders as `%!d(string=3)`. `-f` and `-s` are mutually exclusive.
- **Piped stdout strips ANSI.** `gum style ... | cat` shows plain text. `CLICOLOR_FORCE=1` keeps colour; `NO_COLOR=1` removes it even on a TTY.
- **Colours are 0-255 ANSI or `#RRGGBB`.** Named colours are not accepted.
- **Every styled element accepts hidden sub-flags.** Any `--<prefix>.foreground` flag also takes `.background`, `.bold`, `.faint`, `.italic`, `.underline`, `.strikethrough`, `.border`, `.border-foreground`, `.border-background`, `.align`, `.width`, `.height`, `.margin` and `.padding`, even though `--help` lists only the colours.
- **`table` returns CSV.** A selected row with commas inside a field comes back quoted; `--return-column N` (1-based) avoids parsing it.

## Additional resources

- [commands.md](commands.md): every subcommand's flags, defaults, keybindings, stdin/stdout contract and command-specific gotchas
- [styling.md](styling.md): colour values, style flags, hidden sub-flags, env var naming, `format` template helpers and themes, `join` layouts
- [recipes.md](recipes.md): complete worked scripts (conventional commit, branch manager, staged-file picker, table-driven menus, layouts) drawn from `examples/` and adapted for zsh
