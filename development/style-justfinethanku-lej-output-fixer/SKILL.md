---
name: style
description: Pick, switch, clear, or create a Claude Code output style. Use when the user invokes /lej-output-fixer:style, asks to change how Claude writes (tone, verbosity, readability, formatting), or mentions output styles.
---

# Output Style Picker

You are helping the user choose or create an output style. Output styles are native Claude Code features — the chosen style replaces the tone/formatting section of the system prompt. Your job: show a menu, apply the choice, confirm.

## Step 1 — Gather the options

Build the full list of available styles:

1. **Bundled with this plugin**: Scannable, Bottom Line First, Walk Me Through It.
2. **Built-in**: Explanatory, Learning.
3. **The user's own**: list `*.md` in `~/.claude/output-styles/` and `.claude/output-styles/` (if present). Read each file's frontmatter for `name` and `description`. Skip files without frontmatter.
4. **Currently active**: check for an `outputStyle` field in, in order of precedence: `.claude/settings.local.json`, `.claude/settings.json`, `~/.claude/settings.json`. Note which style is active and which file sets it.

## Step 2 — Present the menu

Use the AskUserQuestion tool — never make the user type a style name freehand.

- Mark the currently active style in its option description.
- AskUserQuestion allows max 4 options per question. With more choices than fit, lead with the most relevant (bundled presets first, then the user's own) and make the last option "More options…" — if chosen, ask a follow-up question with the rest.
- The menu must always offer a path to two special entries:
  - **No output style** — return to Claude Code's default voice.
  - **Create new preset** — build a custom style (Step 4).

## Step 3 — Apply the choice

- **A style was chosen**: write `"outputStyle": "<reference>"` into `~/.claude/settings.json` (applies everywhere). If the user says they want it only for this project, use `.claude/settings.local.json` instead. Edit JSON carefully — preserve all existing keys. Use `jq` or a small `python3` round-trip, never a blind overwrite.
- **The reference format matters.** Styles bundled in a plugin only resolve with the plugin namespace prefix; bare names silently do nothing. Exact values:
  - This plugin's styles: `lej-output-fixer:Scannable`, `lej-output-fixer:Bottom Line First`, `lej-output-fixer:Walk Me Through It`
  - Built-in and user-created styles: the plain style name (e.g. `Explanatory`, or the `name` from the user's own file)
- **Precedence check**: if a more-specific settings file already sets `outputStyle` (local overrides project overrides user), tell the user their choice won't take effect until that override is removed, and offer to remove it.
- **No output style**: remove the `outputStyle` key from whichever settings file(s) set it. Confirm with the user before touching a project-level file they may share with a team.
- **Confirm**: state what's now active and which file controls it. Note that if the change doesn't take effect immediately, starting a new session will pick it up.

## Step 4 — Create new preset

Interview the user conversationally — a few quick questions, not a form:

1. What should it be called?
2. What's the one-line job? ("answers I can scan", "explain like I'm new", "just be brief")
3. Tone and verbosity — formal or casual? Terse or thorough?
4. Formatting rules — bullets vs. prose, headers, code-comment style, anything they always want?
5. Pet peeves — phrases or habits Claude should never do?

Then write `~/.claude/output-styles/<kebab-case-name>.md`:

```markdown
---
name: <Their Name>
description: <one line, shown in pickers>
keep-coding-instructions: true
---

# <Their Name>

<Their rules as clear imperatives, one per bullet. Concrete beats abstract: "Max 3 sentences per paragraph" beats "be concise".>
```

Keep `keep-coding-instructions: true` unless the user explicitly wants to replace Claude Code's software-engineering instructions entirely (warn them that's what `false` does).

Save it to the user's own `~/.claude/output-styles/` — never into the plugin's directory (their preset must survive plugin updates). Then offer to activate it (Step 3).

## Guardrails

- Never set `force-for-plugin` on anything.
- Never modify the plugin's bundled style files.
- If a settings file contains invalid JSON, stop and show the user the problem instead of overwriting the file.
