---
name: vscode-color
description: |
  Give a git repo a stable, distinct VS Code background tint so windows are
  tellable apart at a glance. The color is scoped to the workspace
  (.vscode/settings.json under workbench.colorCustomizations), so it applies every
  session with no per-session step. Two modes: deterministic (SHA-256 of the repo's
  GitHub slug -> a hue, same repo always same color) and manual override (the user
  names a color or feel). Tints seven surfaces — editor, sidebar, activity bar,
  panel, active tab, title bar, status bar — tuned subtle for dark themes, with a
  --light variant.

  Trigger when the user says "tint this repo", "give this workspace a background
  color", "make this window a different color", "set the editor background for this
  repo", "color-code my repos", or "/vscode-repo-tint". Also offer it unprompted
  when a user complains they can't tell two VS Code windows apart.

  Not for global/user-level VS Code theming (this writes per-repo workspace settings
  only) and not for non-git folders (the deterministic color is keyed off the git
  remote slug).
---

# VS Code Repo Tint

Give each repo a stable, distinct workbench background so two VS Code windows are never confused. The color lives in `<repo>/.vscode/settings.json` under `workbench.colorCustomizations`, so it loads every session automatically — no per-session step.

## Two modes

1. **Deterministic (default).** SHA-256-hash the repo's GitHub slug (`owner/name`, lowercased, `.git` stripped, normalized from both `git@` and `https://` remotes) into a hue 0–360. Same repo always yields the same color; different repos differ. A repo with no `origin` remote falls back to a `local/<folder>` slug so it still gets a stable color.
2. **Manual override.** When the user names a color or a feel ("dark grey with a 10% blue tinge", "warmer", "less green"), translate that into concrete HSL knobs and pass them instead of using the hash. This stamps a marker so the hash can't later clobber the hand-picked color.

## Locate this skill, then call its script by absolute path

The bundled script must be invoked by its **absolute** path, never a CWD-relative one, so it works from any working directory. Discover the skill dir once (preferring install roots, traversing symlinked installs with `find -L`, requiring a real match so an empty result can't collapse to `.`):

```bash
SK=""
for root in "$HOME/.claude/skills" \
            "$(git rev-parse --show-toplevel 2>/dev/null)/.claude/skills" \
            "$(git rev-parse --show-toplevel 2>/dev/null)/skills"; do
  [ -d "$root" ] || continue
  hit=$(find -L "$root" -path '*vscode-color/SKILL.md' 2>/dev/null | head -n1)
  [ -n "$hit" ] && { SK=$(dirname "$hit"); break; }
done
[ -n "$SK" ] || { echo "vscode-color: skill dir not found — pass it by absolute path" >&2; exit 1; }
```

Then every call below is `python3 "$SK/vscode-color.py" ...`. The script targets the cwd's git repo by default; pass `--repo <path>` to target another. It needs nothing but Python 3 and `git`.

## The run

### 1 — Preview before writing
Always show the user the slug and resulting hex first — nothing is written:

```bash
python3 "$SK/vscode-color.py" --print              # deterministic
python3 "$SK/vscode-color.py" --print --light      # light-theme variant
```

For a manual request, preview the override instead (see *Manual override* below).

### 2 — Write the tint
```bash
python3 "$SK/vscode-color.py"                      # deterministic, dark
python3 "$SK/vscode-color.py" --light              # deterministic, light
```

The script merges into `<repo>/.vscode/settings.json` under `workbench.colorCustomizations`, **preserving every other key** in the file, and creates `.vscode/` if missing.

> **Sandbox gotcha:** writing `.vscode/settings.json` can fail under a command sandbox with `Operation not permitted`. The script writes the file natively (Python), not via a shell redirect — but the *launch* is still sandboxed. If the write errors with `Operation not permitted`, re-run that one command with the sandbox disabled (`dangerouslyDisableSandbox: true`). Don't disable it for the `--print` preview; only for the actual write.

### 3 — Tell the user to reload
The colors apply on the next window load. Tell them: **Cmd+Shift+P → "Developer: Reload Window"** (or reopen the folder).

### 4 — Ask once: commit or ignore
Ask one time whether `.vscode/settings.json` should be:
- **committed** — the whole team shares the repo's color, or
- **gitignored** — the tint is personal (add `.vscode/settings.json` to `.gitignore`).

Don't ask every run; once per repo is enough.

## Manual override

When the user names a color or feel, translate it into HSL knobs and pass them. Any of `--hue/--sat/--lightness/--accent-lightness` switches the script to manual mode and stamps the marker.

```bash
python3 "$SK/vscode-color.py" --print --hue 240 --sat 0.12   # preview first
python3 "$SK/vscode-color.py" --hue 240 --sat 0.12           # then write
```

- `--hue` 0–360 (0 red, 120 green, 240 blue), `--sat` 0–1 (default 0.12), `--lightness` editor bg 0–1 (default 0.13 dark / 0.94 with `--light`), `--accent-lightness` for the title/status bar.
- **"N% blue tinge" on a neutral dark grey** = a near-neutral grey with the blue channel raised relative to red. Use `--hue 240` and a low `--sat`: roughly `--sat 0.10` gives B−R ≈ 6 (~5%), `--sat 0.18` gives B−R ≈ 12 (~10%). Bump `--lightness` for a lighter grey.
- **"warmer" / "less green" / "more X"** — nudge `--hue` (toward 30 for warm, away from 120 for less green) and re-preview. Iterate on the preview, not on the user's editor.

## Palette rules (baked into the script)

- Dark-theme tuned: low saturation (hash mode 0.30–0.50), dark editor lightness (~0.13). `--light` flips to lightness ~0.94.
- Seven surfaces are tinted so the window reads as one color: `editor.background`, `sideBar.background`, `activityBar.background`, `panel.background`, `tab.activeBackground` (= editor bg), `titleBar.activeBackground` and `statusBar.background` (a lighter accent band).
- Sidebar / activity bar / panel sit slightly darker than the editor; title and status bar sit lighter.

## The clobber guard

After a manual override the script writes a top-of-file marker key, `"// vscode-repo-tint": "manual"`. Deterministic mode then **refuses** to overwrite that repo (exit 3) and prints why — so a later "tint my repos" sweep can't silently replace a hand-picked color. To intentionally replace a manual tint with the hash color, pass `--force` (which also clears the marker).

## Exit codes

`0` ok · `2` not inside a git repo · `3` refused (manual marker present, no `--force`) · `4` existing `settings.json` is unparseable (refused rather than clobber hand-edited config).

## When NOT to use

- **Global VS Code theming.** This writes per-repo *workspace* settings only; for a user-wide theme, the user wants their User `settings.json` or a theme extension, not this.
- **A non-git folder.** The deterministic color is keyed off the git slug; outside a repo the script exits 2. (A repo with no remote still works via the `local/<folder>` fallback.)
- **One window, no confusion.** If the user only ever has one VS Code window open, a per-repo tint solves a problem they don't have — say so rather than tinting reflexively.
