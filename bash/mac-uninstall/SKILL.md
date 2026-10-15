---
name: mac-uninstall
description: >-
  Fully or partially uninstall a macOS app: bundle plus preferences, caches, logs, app
  support, group containers. Use for 'uninstall X', 'remove X app', 'get rid of X',
  'remove all traces of X', or 'clean' an app (keep it, remove caches/logs). Ask which
  app if none is named, confirm before deleting.
disable-model-invocation: true
---

# Mac App Uninstaller

Three bundled scripts handle all the heavy lifting — use them instead of writing shell
commands from scratch. The scripts live next to this file in `scripts/`.

```
scripts/find_app.sh     — fuzzy-search for an app by name
scripts/gather_files.sh — find every Library file associated with an app
scripts/uninstall.sh    — kill the app and delete the files (full or partial)
```

---

## Workflow

### Step 1 — Identify the target app

**If the user gave a name**, run:
```bash
~/.claude/skills/mac-uninstall/scripts/find_app.sh "<search term>"
```
- One result → proceed.
- Multiple results → list them and ask: *"I found these apps. Which one do you want to remove?"* Wait for confirmation.
- No result → tell the user, ask if the name might be spelled differently.

**If no name was given**, list installed apps:
```bash
ls /Applications/ ~/Applications/ 2>/dev/null | grep "\.app$" | sed 's/\.app//' | sort
```
Show the list and ask which one they want to uninstall.

---

### Step 2 — Ask for uninstall mode (if not specified)

If the user hasn't said full or partial, ask:

> "Do you want a **full uninstall** (app + all its data, preferences, caches removed)
> or a **partial clean** (keep the app, remove only caches and logs)?"

---

### Step 3 — Gather associated files

```bash
~/.claude/skills/mac-uninstall/scripts/gather_files.sh "/Applications/AppName.app"
```

This prints every associated path grouped by category (App bundle, Preferences, Caches,
Logs, etc.). Capture the output — you'll pass these paths to the next step.

---

### Step 4 — Show the list and ask for confirmation

Present the gathered paths clearly to the user, grouped as the script output shows them.
End with: *"Shall I go ahead and delete all of this? This cannot be undone."*

**Never proceed without explicit confirmation.** Wait for "yes", "go ahead", "proceed", etc.

---

### Step 5 — Run the uninstall

Pass the gathered paths as arguments to the uninstall script:

```bash
~/.claude/skills/mac-uninstall/scripts/uninstall.sh <full|partial> \
  "/Applications/AppName.app" \
  "/Users/you/Library/Application Support/AppName" \
  "/Users/you/Library/Preferences/com.example.app.plist" \
  ...
```

The script will:
1. Gracefully quit then force-kill the app process
2. Delete the appropriate paths (in partial mode it skips app bundle, prefs, and app support)
3. Print a summary of what was removed and what was kept

---

### Step 6 — Verify

```bash
~/.claude/skills/mac-uninstall/scripts/find_app.sh "<name>" 2>/dev/null || echo "App removed"
~/.claude/skills/mac-uninstall/scripts/gather_files.sh "/Applications/AppName.app" 2>/dev/null | grep -v "^###" | grep -v "^$" || echo "No library files remain"
```

Report back: either "completely removed, no traces remain" or list anything still present
and ask if the user wants those removed too.

---

## Rules

- **Never delete without explicit user confirmation** — always show the list first.
- **Fuzzy name matches always require confirmation** before proceeding to gather/delete.
- **Partial mode** never touches the app bundle, `Application Support`, `Preferences`, or `Containers`.
- If a path from `gather_files.sh` looks unrelated to the app, flag it rather than deleting silently.
