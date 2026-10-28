---
name: health-check
description: "Runs the Alterbrain health check, explains the results in plain English and offers to fix each problem. Also does the quarterly model check (are the Claude models Alterbrain uses still the best fit?). Use when something seems broken, after setup or an update, when the user asks whether everything is working, or asks to check the models."
model: sonnet
effort: medium
---

# Health check

Check that Alterbrain is healthy, say what is wrong in plain words, and fix it with your say-so.

## When to use

- The user says something is broken, slow or "not working".
- After `/onboard` or `/update-alterbrain`, as a final check.
- Before a long piece of work, when the user wants to be sure all is well.
- The session digest shows a warning (wrong model, git problem, old Claude Code).
- **Obsidian settings or the PDF page renderer:** the doctor shows the Obsidian line as a warning, or a tip about the renderer. After re-running the Obsidian setup, tell the user to **reopen the vault once** (close it and open it again).
- **Routines:** the doctor shows an overdue or invalid routine, or the user says "check my routines" or "did my job run?". Wording and fixes: `references/fixes.md`, "Routines".
- **Model check:** the user asks "are we on the right models?", or the quarterly check is due (more than 90 days since `reviewed` in `system/catalogue/routing.json`). Full steps: `references/model-check.md`.

## Before you start

- No `/clarify` questions are needed. Running the check changes nothing.
- Read `system/release.json` so you know the expected versions.
- Check whether `state/local/dev-mode` exists. If it does, this is the framework developer's copy. Say so once, and do not report "changed framework files" as a problem.

## Steps

1. Say in one line what you are about to do: "I am running the health check. It only looks, it does not change anything."
2. Run `node system/scripts/doctor.mjs --json`. A non-zero exit code means "problems found". It is not a crash. If the script itself fails to start (for example Node is too old), say so plainly and go to step 5 for the Node fix.
   - Rate-limited tools (LinkedIn): when one is switched on (`config/mcp.selected.json`), also run `node system/scripts/rate-guard.mjs status` and tell the user in one or two lines how much is used today. A non-zero exit means a pause, draft-only mode, an action to check on the platform, or a damaged usage log. Explain which in plain words and offer `reset-throttle`, `clear-draft-only` or `repair-ledger` only after asking, one at a time.
   - Routines: the doctor's routines line lists overdue routines and invalid or unreadable routine notes. If the user asked about their routines, also run `node system/scripts/routines.mjs overdue` and `node system/scripts/routines.mjs list` and report in plain words. Exit code 1 from either (or from `show`) means something needs attention: an overdue routine, an invalid or unreadable note, or an unknown name. Read the output; it is not a crash.
3. Sort the results into three groups:
   - **All good** (one short line, no detail);
   - **Needs fixing** (breaks something the user relies on);
   - **Nice to have** (optional things such as Quarto).
4. Explain each problem in two or three short sentences: what it is, why it matters to the user, what fixing it involves. Use `references/fixes.md` for the wording and the fix for each check. Explain any unavoidable term in one line (for example "git is the tool that keeps a history of your files").
5. Offer the fixes one at a time. For each, use AskUserQuestion with two or three options. Put the recommended one first (for example "Fix it now", "Show me what it would do", "Skip for now").
   - Ask before every fix, even a small one.
   - Run only the fix that was approved. Use the commands in `references/fixes.md`.
   - Some fixes need the user to act themselves (signing in to GitHub, installing software that needs a password). Give the exact steps, then wait. Do not type passwords, tokens or keys for them.
6. When all approved fixes are done, run `node system/scripts/doctor.mjs --json` again. Compare with the first run and say what changed: "Fixed: 2. Still open: 1."
7. For anything left open, create a task so it is not forgotten:
   `node system/scripts/tasks.mjs add "<plain one-line description of the open problem>" --tag health-check --priority medium`
   Keep the task text free of double quotes.
8. **Model check.** If the user asked for it, run it now. If it is not asked for but is due (see `references/model-check.md`, section 1), offer it in one line after the results and ask before starting. Follow `references/model-check.md` exactly. It only reads and proposes: it never changes a model on its own. An approved "Update model routing" card is applied here (never by `/build`), after a yes in chat.
9. **PDF page renderer, once.** If the doctor's `pdf-pages` line carries a tip (the renderer is missing) and the user has not already declined it, offer it after the fixes, in one line, with the pro and the con: "Install the PDF page renderer (recommended): lets me look at every page of the reports and decks I make; a small download. / Not now: I make PDFs as before but cannot check the layout by eye." Never offer it in the middle of other work. On yes follow `references/fixes.md`, then ask them to close and reopen Claude. On no, say nothing more about it.
10. Finish with a short summary: how many checks passed, what was fixed, what is left, and what to do next. If everything passes, say "Everything is working" and nothing more.

## Outputs

- No files change unless the user approved a fix.
- A task in `vault/00_inbox/Tasks.md` (tag `#ab/health-check`) for each problem left open.
- Model check: `state/local/model-check.json` (date of the check); when a change is worth proposing, a card `vault/00_inbox/proposals/<date> Update model routing.md` and a `#ab/health-check` task. Only after approval: the `model:` and `effort:` lines of the listed skills and agents.
- Fixes that need a log (for example GitHub setup) write to `state/local/git.log` through their own script.

## Safety

- Read-only until the user approves a specific fix. The one exception is the model check, which may write its proposal card, a task and its date file (nothing else).
- The model check never changes models itself: proposal first, edits only after approval, only `model:`/`effort:` lines, aliases only (never full model IDs). The main session model is changed by the user in `.claude/settings.local.json` (theirs), never in `.claude/settings.json`. Never stop a running agent to switch.
- Never edit `.claude/settings.json`, `system/core.md`, `system/hooks/**`, `system/scripts/**`, `system/lib/**` or `system/catalogue/*.json` by hand. If a framework file is damaged, the fix is `/update-alterbrain`, never a manual edit.
- Never touch anything inside `vault/` other than creating missing empty folders (with approval), the model check's proposal card and task, and, with approval, one frontmatter line of a routine note (see `references/fixes.md`, "Routines").
- Never ask for, show or type passwords, tokens or API keys. Sign-in is always done by the user in their own terminal.
- Never install software without saying exactly what will be installed and getting a yes.
- Never invent a result. If a check could not run, say "I could not check this".
