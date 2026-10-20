---
name: todoSetup
description: "The configuration wizard for Prompt TODO: seven steps (todo file + title, tags, rules check, ticket tracker, app navigation, permissions, summary), each one skippable and re-runnable on its own, --yes takes every default. Edits .claude/prompt-todo/config.json and re-renders .claude/prompt-todo/RULES.md. Runs only when the user invokes it: '/todoSetup', '/todoSetup tags', '/todoSetup tracker', '/todoSetup --yes'."
argument-hint: "[todo|tags [add <Tag>: <meaning>|remove <Tag>|detect]|rules|tracker|appNavigation|permissions|summary] [--yes]"
disable-model-invocation: true
allowed-tools: Read, Edit, Write, Glob, Grep, AskUserQuestion, Bash(git config:*), Bash(git rev-parse:*), Bash(bash .claude/prompt-todo/bin/py.sh:*), Bash(claude mcp:*), Bash(gh auth:*), Bash(gh issue:*), Bash(ls:*), Bash(command:*), Bash(bash .claude/hooks/todo-confirm.sh:*), Bash(echo:*), Bash(basename:*), mcp__atlassian__getJiraIssue
---

# /todoSetup

Guided setup of Prompt TODO, run inside the project after `install.sh`. Nothing here is
required: the flow works with the defaults `install.sh` wrote. Each step explains why it
exists, shows the current value, asks, and writes. The user can skip any step, and re-run any
step later by name.

```
/todoSetup                 # all steps in order
/todoSetup tags            # one step
/todoSetup --yes           # all steps, every default, no questions
/todoSetup tracker --yes   # one step with its default
```

## Ground rules

- **Config first.** Read `.claude/prompt-todo/config.json` at the start (`Read` tool). Every
  step shows the current value as its default. If the file is missing, say `install.sh` has
  not been run here and stop.
- **Ask with `AskUserQuestion`**, one question at a time, and **every question has a `Skip`
  option** (keeps the current value; acknowledge in one line: `Skipped — tags unchanged`).
  With `--yes`, ask nothing: take the default of every step and print one line per step.
- **Write with the `Edit` tool**, never the shell, then re-render:
  `bash .claude/prompt-todo/bin/py.sh render_rules.py`. Show its one-line output. If it fails,
  show the error and revert the edit.
- Never touch the user's todo file except where a step says so (step 1 creates it; step 7's
  smoke test appends and removes one line, with permission).
- Unknown step name → list the seven step ids and stop.
- Finish every run (single step or all) with the **summary** of what changed and what is
  still off, unless the run *was* only the summary step.

## Step 1 — `todo`: project title and your todo file

**Intro (print before asking):**

> Every person on the project gets their own todo file, named after their git user name, so
> files never collide in git and Claude never touches a teammate's items. The same name
> becomes the marker Claude leaves in code comments, `[jd#12]`, which is how a change is
> traced back to the prompt that caused it (`/todoMarkCode off` switches the markers off).
> The project title only appears in the file headers.
>
> For `git config user.name` = `jd` and the title `My App`:
>
> ```
> TODO.jd.md               your items              header:  # My App — TODO
> TODO.jd.archive.md       done items, moved by    header:  # My App — TODO archive
>                          /todoArchive; ids live on there, so numbers are never reused
> ```
>
> ```markdown
> # My App — TODO
>
> - [ ] #12 Add a retry button to the upload error dialog
> - [x] #11 Fix the crash when the photo list is empty
> ```
>
> ```kotlin
> // Retry re-enqueues the same upload id, see UploadQueue. [jd#12]
> ```

**Ask:**
1. Project title — default: the current `projectTitle` if it is not `My App`, else the
   repository directory name (`basename "$(git rev-parse --show-toplevel)"`).
2. Git user name — run `git config user.name`. If set, show it and ask to confirm (or
   change: `git config user.name <name>`, run only after the user typed the name). If empty,
   say the todo file cannot be named without it and offer to set one; skipping leaves no file,
   and the first `#new` prompt will ask again.
3. Create `TODO.<name>.md` now? Default yes when the file does not exist. Create it with the
   `Write` tool: the `# <title> — TODO` header and one empty line, nothing else. If it exists,
   say so and do not touch it.

**Writes:** `projectTitle`; the todo file. Re-render.

`--yes`: title = directory name if the config still says `My App`, keep the git name, create
the file if the name is set and the file is missing.

## Step 2 — `tags`: the tag table

Tags tell platforms apart inside one repo: a tag goes right after the id (`- [ ] #19 IOS: …`)
and scopes the item. The table is built from what the repo contains, so this step normally
asks nothing. There is no `All` tag and no default tag: an untagged item is simply about this
project.

1. Run `bash .claude/prompt-todo/bin/py.sh detect_platforms.py` and print its lines as they are
   (`Android  app/src/main/AndroidManifest.xml`), one per detected platform.
2. Run it again with `--tags`: that is the new `tags` object. Its rule: one row per detected
   platform (Web also brings `MobileWeb` and the four browser rows), `<P>+` rows only when two
   or more platforms were found, `Docs` and `Infra` always, ignore rows `QA` and `Admin`,
   `default` empty.
3. **Something detected:** replace the whole `"tags": { … }` block of `config.json` with that
   output (`Edit` tool), re-render, and print the result as a short table (tag, meaning) plus
   one line: `Tags: Android, Docs, Infra — change with /todoSetup tags add|remove`. No
   question. `--yes`: the same.
4. **Nothing detected:** one question, `Which platform is this?` — multi-select over
   *Android*, *iOS*, *Web*, *Backend*, *Desktop*, plus *Skip*. Build the object with
   `detect_platforms.py --tags <Platform> …` from the answer (iOS is `IOS`) and continue as
   in 3. `--yes` or Skip: write the object from `--tags` with no platform (`Docs`, `Infra`
   only), say so in one line.

Sub-commands, for the rare manual change (never offered as a question in the main flow):

- `/todoSetup tags add <Tag>: <meaning>` — append a row (tag: letters, digits, `+`, no colon).
- `/todoSetup tags remove <Tag>` — drop a row.
- `/todoSetup tags detect` — re-run the detection and rebuild the table (same as step 2).

Validate before writing: a tag cannot be in both lists and no tag may repeat;
`render_rules.py --check` says so too.

**Writes:** `tags`. Re-render.

## Step 3 — `rules`: render and verify

No question. Do, and print a checklist with ✓/✗ per line:

1. `bash .claude/prompt-todo/bin/py.sh render_rules.py` → `RULES.md` rendered.
2. `CLAUDE.md` contains the line `@.claude/prompt-todo/RULES.md` (Grep). Missing → offer to
   append it (Edit).
3. `.claude/settings.json` has the hook: `bash .claude/prompt-todo/bin/py.sh merge_settings.py .claude/settings.json --check`.
   Missing → offer to run it without `--check`.
4. `command -v jq`, else the Python the wrapper found (`bash .claude/prompt-todo/bin/py.sh` with no
   argument prints its usage; `python3`, `python` or `py -3` — on Windows usually not `python3`)
   — which one the hook will use.
5. Pipe-test: `echo '{"prompt":"works"}' | bash .claude/hooks/todo-confirm.sh` must print
   JSON containing `TODO CONFIRM TRIGGER`; `echo '{"prompt":"hello"}' | …` must print
   nothing.

Any ✗ that could not be fixed: say what to do by hand.

## Step 4 — `tracker`: where tickets come from

**Intro (print before asking):**

> `/todoFromTicket` turns a ticket into numbered first prompts in your todo file, and — when
> an app-navigation skill is connected — the item that opens the app where the bug lives. To
> read tickets Claude needs a connection to your tracker: for Jira that is the Atlassian MCP
> server (OAuth, logged in once with `/mcp`) plus, for the attachments — screenshots, logs —
> a personal API token in a gitignored file (the MCP server carries no file bytes); for
> GitHub Issues the `gh` CLI. Nothing else in the flow needs it. Without it, `/todoFromTicket`
> only works with the ticket text pasted in, and the ticket-key input of app navigation is
> unavailable; everything else works.
>
> Example — the sample app BestPizza, ticket PROJ-321 "Order total wrong after removing a
> topping" (*Add a Margherita, add olives, remove olives: the total still includes the
> topping. Server: stage, Restaurant: Downtown, Pizza: Margherita, Topping: Olives.*
> Attachment: `order.log`):
>
> ```
> /todoFromTicket PROJ-321
> ```
>
> appends to `TODO.jd.md`:
>
> ```markdown
> ## PROJ-321 — Order total wrong after removing a topping
> > Add a Margherita, add olives, remove olives: the total still includes the topping. Attachments: todoAttachments/PROJ-321/order.log
> - [ ] #32 PROJ-321 /appNavigation            ← only when an app-navigation skill is connected
>   - Server: stage
>   - Restaurant: Downtown
>   - Pizza: Margherita
>   - Topping: Olives
> - [ ] #33 PROJ-321 Android+: Recompute the order total from the current toppings whenever one is removed.
> - [ ] #34 PROJ-321 Show the topping's price next to its remove button so a wrong total is visible at once.
> - [ ] #35 PROJ-321 QA: on the #32 screen, add olives, remove them: the total goes back to the pizza price
> - [ ] #36 PROJ-321 QA: on the #32 screen, add olives: the olives row shows its price, the total is pizza + that price
> ```
>
> Then `#33` works the item, `works` ticks it and rewrites it to its ideal prompt; the `QA:`
> rows are yours to tick once the checks pass.

**Ask:** *Jira (Atlassian MCP)*, *GitHub Issues (gh)*, *None*, *Skip*. Default: the current
`tracker.kind`.

**Jira:**
1. Host (`yourcompany.atlassian.net`) and project keys (comma-separated, e.g. `PROJ, OPS`).
2. `claude mcp list` — is a server named `atlassian` there? If not, print the exact command
   and ask before running it:
   `claude mcp add --transport http --scope user atlassian https://mcp.atlassian.com/v1/mcp/authv2`
   then tell the user to run `/mcp` in Claude Code, pick `atlassian`, and log in (OAuth in the
   browser). This step cannot complete the login itself; say so.
3. Test: ask for one ticket key the user knows; call `mcp__atlassian__getJiraIssue` on it and
   show its summary line, or the error. A failed test still saves the config (the login may
   happen later).
4. Attachments: if `.claude/prompt-todo/credentials.json` already holds an email and a
   token, say so and keep it. Otherwise ask with `AskUserQuestion` — *Enter email + API token
   now* (a personal token from id.atlassian.com → Security → API tokens) or *Skip —
   attachments will not download*. On enter: ask for the two values (the token as free text
   via *Other*; never print it back), write the file with `Write` as
   `{"email": "…", "token": "…"}`, and check `.gitignore` lists
   `.claude/prompt-todo/credentials.json` (add the line with `Edit` if `install.sh` did not).
   On skip: say the prompts still come, the files don't, and that this step can be re-run.
5. Write `tracker.kind = "jira"`, `tracker.jira.host`, `tracker.jira.projectKeys`.

**GitHub:**
1. Repository `owner/repo` — default: parsed from `git config remote.origin.url` when it is a
   GitHub URL.
2. `gh auth status` — missing `gh` → print the install hint (`brew install gh` / the GitHub
   CLI page) and how to log in (`gh auth login`); not logged in → say `gh auth login`.
3. Test: `gh issue list --repo <repo> --limit 1`, show the result or the error.
4. Write `tracker.kind = "github"`, `tracker.github.repo`.

**None / Skip:** write `tracker.kind = "none"` (Skip: leave the value as it was) and say
plainly: `/todoFromTicket` works only with pasted ticket text, and the ticket-key input of app
navigation is unavailable, until `/todoSetup tracker` is run again. Print the two-line short
form of the intro (what the connection is for) if the intro was not printed.

Re-render. `--yes`: unchanged.

## Step 5 — `appNavigation`: opening the app where a ticket points

Explain in three lines: a ticket's context block (`Server:` plus the lines naming the screen)
can become an item that opens the app right there on a device; that needs a skill that knows
your app's build, login and screens. The package ships only a description of it,
`.claude/skills/appNavigation/SKILL.md` — implementing it is the user's work, for their app.

**Ask — two options only:**
- **Skip (default)** — "you can do this later": implement the skill for your app (the
  description says what it must do), or use a skill you already have, then run
  `/todoSetup appNavigation` again to connect it. Writes `appNavigation.mode = "none"`.
- **Connect an existing skill** — list the directories in `.claude/skills/` (`ls`), the
  shipped `appNavigation` included, and ask which one. Confirm in one question that the skill
  takes a spec as sub-bullets (the lines a ticket's context block carries). If the pick is the
  shipped `appNavigation` and its `SKILL.md` still says it is not implemented, say so — it
  stays a placeholder until implemented — but still record it. Writes
  `appNavigation.mode = "existing"`, `appNavigation.skill = "<name>"`.

Re-render — the rules gain (or lose) the **App-navigation items** paragraph, and
`/todoFromTicket` starts (or stops) writing the `/<skill>` item. `--yes`: unchanged.

## Step 6 — `permissions`: allow rules

Explain: the skills run `git config user.name` and the render script; allow rules in
`.claude/settings.local.json` (personal, not committed) spare a prompt on each.

Propose the list, ask *Add* / *Skip*:
- always: `Bash(git config user.name)`, `Bash(bash .claude/prompt-todo/bin/py.sh:*)` (the
  render and detect scripts run through that wrapper);
- with `tracker.kind = github`: `Bash(gh issue view:*)`, `Bash(gh issue list:*)`.

Write with `Edit` (create the file with `{"permissions":{"allow":[…]}}` if missing; merge into
an existing `permissions.allow`, no duplicates). `--yes`: add the always-on rules only.

## Step 7 — `summary`

No question, unless the smoke test is offered. Print:

1. The effective config as a short table: title, git name → todo file (exists / missing),
   tags (the rows, "no default", ignore rows), confirm words, tracker (Jira: attachments
   token present / missing), app navigation, code markers (on / off), prompt scores
   (on / off), line width (N characters / off), attachments directory.
2. **Disabled by skipped steps**, one line each: no tracker → `/todoFromTicket` paste-only;
   Jira without a token → attachments are not downloaded; no app navigation → context blocks
   stay as sub-bullets; no git name → no todo file yet.
3. **Smoke test** (ask, default yes; `--yes` runs it): append `- [ ] #new Smoke test item`
   to the todo file with `Edit`, run the Autoincrement rule, show the line with its id, then
   remove that line again (Edit) and say the id is now taken — the next item gets the one
   after it, which is how ids are meant to behave.
4. Next steps: `#new` an item and type its id; `/todoFromTicket <KEY>`; the human readme
   `.claude/prompt-todo/README.md`.
