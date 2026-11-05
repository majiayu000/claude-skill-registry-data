---
name: sprint-demo
description: Builds a demo video of what a sprint delivered, or of the tickets the user names, to show at the sprint demo or send to the product owner. It lists the sprint's tickets, orders them so the demo tells one story, writes a functional scenario per ticket and gets the user's OK, records each flow in the local app, then edits a single video with a short description of each ticket on screen, title cards and a chapter per ticket, plus presenter notes. Use when the user says "sprint demo", "démo de sprint", "demo video", "vidéo de démo", "show the PO", "montrer au PO", "record the sprint", "scénario de démo", or asks for a video of several tickets for stakeholders rather than a reviewer.
---

# Sprint demo video

For an audience that wants to see what changed for users (the team at the sprint review, a product owner, stakeholders), not proof for a reviewer: that one is the test-evidence skill. This skill records with test-evidence's capture tools and edits with its own script.

`$SK` is the `scripts/` folder of this skill's base directory. Run `bash $SK/demo.sh doctor` once (ffmpeg with drawtext, fonts), and `bash $SK/selftest.sh` after changing a script. Everything goes in one folder per demo, never in a repo: `${SPRINT_DEMO_DIR:-$HOME/demos}/<sprint-or-date>/`, with `takes/`, `clips/`, `plan.md`, `notes.md` and the final video.

## 1. The tickets

- **The sprint** ("since the start of the sprint"): `bash $SK/demo.sh jira-sprint <PROJECT>` lists the open sprint's tickets (`--sprint "<name or id>"` for a closed one, `--jql` for anything else). When the API refuses (401, 429, or no token), `--url` prints the REST path: run it with `fetch()` from a Jira tab of the user's logged-in browser. For the sprint's name and dates (for the intro card), `fetch('/rest/agile/1.0/board?projectKeyOrId=<PROJECT>')`, then `/rest/agile/1.0/board/<id>/sprint?state=active`. Other trackers: `gh issue list --milestone "<name>" --state all` or a GitHub project iteration; Azure Boards with `az boards query --wiql "... [System.IterationPath] = @CurrentIteration"`.
- **Named tickets**: read each one (summary, description, acceptance criteria) as test-evidence does (`attach.sh jira-get <KEY>`, or the browser).

Keep the done tickets and the ones in review with a PR open; leave out the rest unless the user asks. Sub-tasks go under their story. Show the list (key, title, status, PRs) and let the user remove or add tickets before going on.

## 2. Ask how the video should look

Every run, in one question set (AskUserQuestion), offering the previous demo's answers first (read the last `plan.md` under the demo folder):

- **Output**: one video with a chapter per ticket (default); one video plus one clip per ticket (the clip can go on the ticket); one clip per ticket only.
- **Text on screen**: a banner on top of each ticket's part with its key, title and one line on what it brings (default); the banner plus a caption for each step; the banner plus captions in a separate `.srt` (the player turns them on, easy to correct); nothing (the presenter talks over it).
- **Cards**: an intro card (sprint, team, date) and an end card, or none.
- **Language** of everything on screen and in the notes: the audience's, by default the tickets' language.
- **Environment**: where the demo runs. Local (the user's own stack, default), a shared one (dev, test, staging), or production. Ask for its URL and the account to use. Never assume it: a local app can still point at a shared database, so ask what its data lives on too.

## 2b. Outside a local stack, look and don't touch

On anything but a local stack with its own database, other people work on the same data, and production is real customers:

- **Read-only by default.** Navigate, search, open, filter: yes. Every action that writes (create, save, send, delete, import, invite, anything that triggers a job or an e-mail) waits for the user's explicit yes for that action in that environment, named in the plan before recording. In production, propose a local or shared stack instead of any write, and record on production only with existing data the user points at.
- **Show what's there.** Build the scenarios on data that already exists; when a flow needs new data, say so in the plan and let the user choose: create it (their yes, with a name that says it's demo data, and how to remove it afterwards), or show that flow on a local stack instead.
- **Check what's deployed.** A ticket in review is usually not on a shared environment yet: compare the deployed version (an about page, a version endpoint, the last deployment) with the tickets' PRs and say which tickets can't be shown there.
- **Mind what's on screen.** Real names, e-mails, contract numbers, amounts: pick records that show none, or a test client; the video will travel further than the meeting.
- Never change the environment itself (configuration, feature flags, users, restarts) to make a demo work: ask its owners.

## 3. The order: one story, not a list

The video is watched in order, so it must make sense in order. Arrange the tickets the way someone would use the product, not by key, status or who did what:

- Follow the user's journey: what comes first in the app comes first in the video (create, then find, then change, then share).
- A ticket that builds on another comes right after it, and together they make one sequence in one take when they share the screen: the viewer sees the flow once instead of twice.
- Group by user need or by screen; put a short section card (`card --title`) between groups when there are three or more groups.
- Start with the change that matters most to the audience when there is no natural journey, and end on something visible and positive; bug fixes go next to the feature they touch, or together near the end.
- A ticket with nothing to see (refactor, CI, an internal API) gets no recording: either a line in the notes, or one card with two lines in plain words ("Pages load faster: the list now answers in 0.3 s instead of 2 s") when it matters to the audience.

## 4. The plan, approved before recording

Write `plan.md` in the audience's language and show it to the user. Record nothing before their OK.

```markdown
# Démo <sprint> (<date>)
Format: <answers of step 2>. App: <URL>, <repo@branch commit> for each service.
Environment: <local | shared: name | production>. Writes approved: <none, or each one by name>.

## 1. <journey or group name>
### ABC-12 · <title> (done, PR !340)
Banner: "<what the user can now do, one line, no technical words>"
Data: <the demo data it needs>
Steps:
1. <action> → <what the viewer sees>
2. ...
Length: ~40 s
```

The banner line is the need answered, in the audience's words: "Les conseillers voient l'historique des contrats sur la fiche client", not "Ajout de l'endpoint /contracts/history". Take the steps from the acceptance criteria: each criterion that shows on screen gets a step. Keep each ticket under a minute, the whole video under ten.

Give the user a time estimate with the plan (about 5 minutes per recorded ticket, plus the editing) and ask if they have a deadline. When time is short, film only what the ticket is about and turn the tickets that are slow to stage into cards (two lines on what changed). The user can always say "faster": switch to that mode at once and say which tickets became cards.

## 5. Prepare the stage

- The code: tickets in review are not merged yet, so the stack must run what the demo shows. Run their branches from temporary `git worktree`s (or a local branch merging them) rather than switching the user's checkouts, and put everything back afterwards. Write down each service's branch and commit in `plan.md`, and check them again after recording.
- The data: believable demo data, never real customers or personal data. Follow the user's rules for testing apps: ask before using a new app and before the first write to its database (creating demo data is a write). Outside a local stack, step 2b applies.
- The browser: a new tab of its own (test-evidence's browser tools), `resize_page` to 1440×900, zoom 100 %, dev tools closed, no notifications; log in as a demo user whose name can be seen. Nothing personal in the URL bar or on screen.
- Off camera, set up everything the takes start from, so each take films only what its ticket shows: create the demo records, approve what must be approved, and provoke the failures (stop a service, use the input a mock fails on) before you press record. Use the quickest way the app offers (its API, a seed script, or its own forms with nobody watching), only on the user's local stack; elsewhere step 2b applies. Whatever you change to set up a take (a setting, a role, a stopped service), put it back afterwards and say so.
- Rehearse a step you have never driven (a form with an autocomplete, a dialog) before recording it, without submitting. Fields bound to a framework often ignore a value set by script: focus them and type (`type_text`), or use `fill`.

## 6. Record

One take per ticket, or per sequence of tickets that share a screen, in `takes/NN-<KEY>.mp4` numbered in the plan's order. Use test-evidence's capture: `screencast_start`/`screencast_stop` for a browser page (its notes on trimming the idle end apply), `capture.sh record --window` for a desktop app.

Play the scenario at a human pace: `wait_for` each result, type the text of a form at a typing pace (`type_text`), and scroll rather than jump. The time you take to think between two steps is recorded as a still screen: no need to hurry, `clip` shortens every still screen to `--pause` seconds (1.5 by default, time to read the result). Don't leave an animation running while you think (a spinner, a hovered tooltip that fades): it isn't still, so it stays in the video. Note when each step starts (`date +%s` before the step, minus the take's start; whole seconds are enough) to place captions later. If a step goes wrong, record the take again rather than editing around it.

Chain the steps of a take in one `evaluate_script` (click, wait for the result, pause, click) where you can: each tool call adds seconds of still screen, and a script is also the surest way to wait for a long action to finish (poll the page text). The browser screencast records the page only, not the URL bar: a step like "type a forbidden address" is invisible, so the banner has to say it. One take can serve two tickets that follow each other on screen: cut it in two clips with `--from`/`--to` (find the cut with `ffmpeg -i <take> -vf "select='gt(scene,0.04)',showinfo" -f null -`; dark interfaces need a low threshold).

## 7. Edit

```sh
bash $SK/demo.sh card  clips/00-intro.mp4 --title "Démo du sprint 12" --text "Équipe X · 29 octobre"
bash $SK/demo.sh clip  takes/01-ABC-12.mp4 clips/01-ABC-12.mp4 --title "ABC-12 · Historique des contrats" \
     --text "Les conseillers voient l'historique des contrats sur la fiche client" --from 1.2 --to 38 [--cues cues.txt [--srt]]
bash $SK/demo.sh card  clips/02-section.mp4 --title "Rendez-vous" --seconds 3
bash $SK/demo.sh join  demo-sprint-12.mp4 clips/00-intro.mp4 clips/01-ABC-12.mp4 clips/02-section.mp4 ...
```

`clip` scales the take under the banner (nothing of the app is hidden), trims it, shortens the still screens (`--pause <s>`, `0` keeps them; a still screen at the end goes too) and draws the captions, moved with the cuts; a cue file has one `<start s>|<end s>|<text>` line per step, in the take's time. `join` joins the clips in the order given, which is the plan's, makes one chapter per clip named after its title, and merges the clips' `.srt` files. All sizes default to 1920×1080 (`--size`).

Pick `--pause` per clip: a take where the viewer has to read a still screen (a menu, an error explanation) needs 2.5 to 3 s, or `--pause 0` on a short `--from`/`--to` range; the default 1.5 s suits takes that keep moving. Put every `card`, `clip` and `join` line in a `build.sh` in the demo folder: changing a banner or a cut is then one edit and one run (in the background: a few minutes for ten clips).

## 8. Check it like the audience will

When the user is waiting for the video, give them its path as soon as `join` has written it, then check it. Check: extract a frame from the middle of each chapter (`ffprobe -show_chapters`, then `ffmpeg -ss <t> -i <video> -frames:v 1 <png>`) and Read each one. and one from its end (a grid of them with ffmpeg's `xstack` costs one Read). The banner must be readable and match the part it sits on, the result visible, nothing personal or secret on screen. Check the total length and the size (under 100 MB for an e-mail or a Teams message, else share a link).

## 9. Presenter notes and delivery

Write `notes.md` in the audience's language: the running order with each chapter's start time, for each ticket two or three things to say (the need, what changed for users, what's next or what's left), the ticket and PR links, and the questions to ask the product owner. Add the questions the audience is likely to ask, functional and technical, with short answers taken from the tickets, the PRs and the code (how it works, its limits, who can do what), and what the viewer may notice on screen that isn't part of the demo (a display glitch, test data).

Show the user the folder: the video, the notes, the plan. Nothing leaves the machine without their yes: when they want a ticket's clip on the ticket, attach it with test-evidence's `attach.sh jira <KEY> <clip>`. Keep the folder; it's the user's to delete.
