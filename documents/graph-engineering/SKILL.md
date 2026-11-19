---
name: graph-engineering
description: Change one thing and get one review page with every place it touches across your apps, every changed screen before and after with notes, and only the calls that need you. Use when you say "graph engineering", "/graph-engineering", "change X everywhere", "what does changing X touch", "ripple of X", "change review", or change a feature that lives in more than one app.
---

# Graph engineering

A code diff shows lines. It does not show that the same rule also lives in the mobile app, that the desktop app draws the screen a second way, or that a shared package now imports from an app. Graph engineering does.

The change map is the graph: each feature links to every place that makes it real (web, mobile, desktop, extension, server, shared packages, the website). For one change, the agent maps the graph first, makes the change in the right order, and hands the user **one change review page**: every place touched, every changed screen before and after with notes, and, next to each screen, only the calls that need the user. Everything else the agent settles itself.

It is a superset of `show-me`: the same page, plus the change map and the calls. `graph-engineering-loop` then reads the user's calls, learns the rule behind them and applies it everywhere, so each review asks less.

It works on any project with more than one app or surface. A project with one app still gets the map, the principles and the calls; the map is just short.

Use alongside `be-my-cto`, `dont-break-it`, `bug-trap`, `make-it-look-expensive`, `run-on-any-device` and `no-fluff` if you have them. This skill adds the graph; it repeats none of their rules.

## What lives where

Everything sits in the user's project, under `docs/change-review/`:

| File | What it is |
| --- | --- |
| `concepts.json` | Saved concepts: the search terms and paths for each feature, so the map stays true over time |
| `learned.json` | What the loop has learned: standing rules and cleared suspects (see `graph-engineering-loop`) |
| `<change>/index.html` | The page: a copy of `show-me/template/index.html` |
| `<change>/screens.json`, `screens/` | The changed screens with before and after versions |
| `<change>/change.json` | The change map, the checks and the calls |
| `<change>/ARTIFACT_URL` | Where the page was published, when it was |

`<change>` is a short slug for the change, such as `dark-mode-toggle`.

## 1. Map first

Find every place the change lives before touching code.

1. **Find the apps.** Run `python3 scripts/change_map.py --list` (this skill's folder) from the repo root. It finds each app from its marker files (`package.json`, `pubspec.yaml`, `*.xcodeproj`, `build.gradle`, `Cargo.toml`, `manifest.json` for browser extensions, `project.godot` and others) and guesses its kind: web, mobile, desktop, extension, server, shared, game. Correct a wrong guess with `--app path=kind`. If the apps live in more than one repo, run it in each repo and join the results.
2. **Find the places.** Run `python3 scripts/change_map.py --term "<word>" --term "<other word>" --prs --json docs/change-review/<change>/map.json`. Use the words the code uses, not only the user's words: the feature name, its type and function names, its route, its settings key, its strings. Or `--concept <name>` for a concept already saved in `concepts.json`. `--prs` checks open pull requests for the same files (needs `gh`).
3. **Read the hits.** The script finds text. Open the files, drop the false hits, and add places it missed (a screen that draws the feature without naming it, a test, a doc, a store listing). Save the terms that worked to `concepts.json` so the next change on this feature starts from them.
4. **Without the script** (no Python, or a project it can't read): do the same by hand. List the apps, search each one for the terms, and write down the places.

If the change lives in one place, it is a normal fix: make it and skip the rest of this skill.

Otherwise show the user the ripple in short bullets and wait for a go:
- **Places:** each app and what changes in it.
- **Order:** shared code first, then each app, then the website and docs.
- **Collisions:** open pull requests or branches that touch the same files.
- **What makes it harder:** copies of the same rule, a missing test, an app with no way to capture screens.

## 2. Principles on the graph

A change adds none of these:
- **A second writer.** Each fact has one owner. Two places that both decide the same thing will drift (single source of truth).
- **A copy of a shared rule.** A rule true in more than one app is written once, in shared code, and imported (DRY).
- **A file that serves many concepts.** One file, one job (single responsibility).
- **A backward arrow.** Imports point one way: shared code, then apps, then paid or optional add-ons. Shared code never imports an app.

Flag any breach the change would add, and avoid it. Breaches that already exist are calls for the user (step 4), never a refactor the agent starts on its own.

## 3. Make it

Work in the order from step 1. Each step ends one of three ways:
1. Its check passes (the test, the build, the screen shows the change).
2. Two tries failed.
3. A round made no progress.

The last two stop and ask the user. "Done" without a passing check never counts.

## 4. Build the change review page

1. **Screens.** For every app the change touches, capture each screen it changes, before and after, as in `show-me` steps 1 and 2. Reuse shots that already exist in `docs/review/` and capture only what is missing. Before is the screen on the base branch; After is the screen with the change. Give each screen `"app": "<app id>"` and `"group": "<app name>"`, so the list groups by app. A change with no visible screen still gets a page: the map and the calls show on their own.
2. **Change map and checks.** Write `change.json`:
   ```json
   {
     "title": "Dark mode toggle",
     "summary": "One line on what changes and why.",
     "order": ["shared", "web", "mobile", "desktop"],
     "apps": [{"id": "web", "name": "Web app", "platform": "web", "files": 3}],
     "places": [{"app": "web", "what": "Settings page gets the toggle", "files": ["apps/web/src/settings/Theme.tsx"]}],
     "checks": [{"name": "Tests", "state": "pass", "note": "12 new, all green"}],
     "collisions": [{"what": "PR #41 also edits theme.ts", "files": ["packages/ui/theme.ts"]}],
     "calls": [],
     "standing": [],
     "cleared": []
   }
   ```
   `checks` gives the change's state from five angles, each `pass`, `fail`, `warn` or `missing`, with a short note:
   - **Tests:** the change's tests ran and pass.
   - **Build:** every touched app builds.
   - **CI:** the pull request's checks (read them with `gh pr checks`; `missing` if there is no PR yet).
   - **Screens:** every changed screen is captured on every platform it ships on.
   - **Principles:** no new breach from step 2.
   Copy `standing` from `learned.json` so the page shows the rules already learned.
3. **Calls.** The map's suspects (from the script, and anything you saw while reading the code) are only suspects. Read the code behind each one.
   - A false one goes into `cleared`: `{"match": "<suspect id or file>", "why": "<one line>"}`.
   - A real one becomes a call:
     ```json
     {"id": "theme-rule-in-web", "screen": "settings", "kind": "copy-of-shared-rule",
      "title": "Web decides dark mode on its own",
      "what": "apps/web/theme.ts works out dark mode itself instead of using the shared rule.",
      "risk": "Web and mobile can show different themes for the same setting.",
      "rec": "Move the rule to the shared package and import it in both apps.",
      "recommended": "Move it to shared", "options": ["Move it to shared", "Leave it for now"],
      "files": ["apps/web/theme.ts:12"]}
     ```
     `what` is what the code does, `risk` is what goes wrong for a user, `rec` is what you would do, all in plain words. `screen` puts the call next to that screen; leave it out for a call with no screen. `kind` names the type of call (`copy-of-shared-rule`, `backward-arrow`, `second-writer`, `many-jobs-in-one-file`, `design`, `product`, or your own): the loop learns per kind.
   - A call is a decision for the user. It carries enough context to decide without opening the code. Anything the agent can settle by the principles, it settles; only real decisions become calls.
4. **The page.** Copy `show-me/template/index.html` into `docs/change-review/<change>/`, and set its `<title>` and `.brand h1` to the change's name. The page reads `screens.json` and `change.json` beside it. It shows a **Change map** button (places in order, checks, collisions, every call, rules learned) and puts each call above the notes of its screen, with its options and an Ask box.

## 5. Publish

**With Claude Artifacts** (the preferred path in Claude Code and claude.ai): publish `index.html` as an artifact with `files` = `screens.json`, `change.json` and every shot and clip, and `capabilities` = `{"db": {}, "user": {"scopes": ["profile"]}}`. Notes, choices and questions then save in the artifact's shared database. Save the URL to `ARTIFACT_URL`; later runs publish to that URL so notes and choices stay. Publish from the session doing the work, so comments on the page reach it.

**Without Artifacts** (any other agent): serve the folder, for example `python3 -m http.server 8000` in `docs/change-review/<change>/`, and give the user `http://localhost:8000`. The page runs in local mode: notes, choices and questions save in that browser, and **Export notes** saves them as `review-feedback.json` for the user to hand back. The agent's own notes and replies go in `comments.json`, `calls.json` and `asks.json` beside the page. To share it, commit the folder or host it on any static host.

Put the page's link in each pull request body for the change.

## 6. Read it back

Run `graph-engineering-loop` (`/graph-engineering-loop`, or ask your agent to use graph-engineering-loop). It reads:
- **Notes** in `comments` (as in `show-me` step 4).
- **Choices** in `calls`: doc id = call id, `{screen, choice, at, by}`.
- **Questions** in `asks`: `{call, text, created, author}`. Answer each one in its `reply` field, in plain short lines. A question that turns into a decision becomes a call.

It acts on the choices and learns from them (`learned.json`), so each round asks less.

## 7. Keep the map true

- A file the map missed: add its term or path to the concept in `concepts.json`, in the same change.
- A suspect judged fine: it goes in `learned.json` `cleared`, so it is never raised again.
- The same mistake seen twice: propose a check (a lint rule, a test, a dependency rule) to the user.

## Rules

- The user decides product calls, existing breaches and merges. Ask; never assume.
- Never lose behaviour to tidy the graph. If something must move, move it first, then remove the old place.
- Plain words in every call, note and reply (`sound-human`).
