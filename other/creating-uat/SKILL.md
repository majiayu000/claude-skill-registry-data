---
name: creating-uat
description: Build a complete User Acceptance Test for a codebase — an exhaustive markdown checklist written to the tester's skill level (novice / intermediate / expert), plus an HTML form the tester fills in (pass/fail/not done, look-and-feel comments, screenshots) that writes their answers back into the markdown. Use when the user asks for a UAT, an acceptance test checklist, a manual test plan, a "test everything" script for a non-technical tester or a QA engineer, or wants someone to sign off on an app before release.
---

# Creating a UAT

Produce three things for the target codebase:

1. **`UAT-<app>-<YYYY-MM-DD>.md`** — an exhaustive manual acceptance checklist covering **every**
   user-facing surface, written so someone who has never programmed can execute every step.
2. **`UAT-<app>-<YYYY-MM-DD>.html`** — a form generated from that markdown where the tester records
   Pass / Fail / Not done, a "what happened" note, a look-and-feel comment with severity, and
   screenshots (uploaded, dragged, or pasted with Ctrl+V).
3. **A helper program** the tester runs. Save keeps their work; Submit validates the run and writes
   every answer, comment and screenshot link back into the markdown file, plus a `results.json`.

The completed markdown is then the input to the **processing-uat** skill, which turns failures and
comments into a fix plan.

**Core rule: make no assumptions.** Ask before you write (Phase 0). A wrong assumption produces a UAT
that tests the wrong app.

---

## Phase 0 — Orient, then ask (REQUIRED)

**Spend ten minutes reading the repo before you ask anything.** Good questions are downstream of
discovery. Asked cold, a question about integrations comes out as "do you have any third-party
integrations?" — which makes the user do your reading for you. Asked after a look at the code, it
becomes "there is an OAuth router but no `GOOGLE_CLIENT_ID` in `.env.example` — is Google actually
configured?" Only the second is worth a turn, and only the second uncovers anything.

The questions below are the required minimum, not the whole list: add one whenever the code raises
something the answer would change — an integration that may not be wired up, a feature that looks
half-built, a destructive operation you would need permission to test.

Read enough to make the options concrete — no more:

- `README.md` and any `CLAUDE.md` / `AGENTS.md`
- the task runner (`package.json` scripts, `Makefile`, `pyproject.toml`) and `docker-compose*.yml`
- the names in `.env.example` — **names only, never values**
- the feature/route/module directories, to see what actually exists

Then use `AskUserQuestion` with concrete options. Skip a question only if the user already answered it.

1. **Scope** — the whole app from a clean machine, or only part of it? Default and recommended:
   everything, including install and setup.
2. **Starting state** — what does the tester already have? (nothing at all / dependencies installed /
   services already running / an account already created). This decides whether setup steps are in.
3. **Environment** — which operating system and shell will the tester use? Get this right before
   writing a single command; Windows PowerShell and macOS bash need different text.
4. **Destructive tests** — include irreversible procedures (data deletion, restore-from-backup, key
   rotation, migration rollback)? Offer "include, clearly flagged" vs "exclude".
5. **Tester skill level** — ask this explicitly, with these three options. It decides how much detail
   every step carries, and it is the single biggest factor in whether the checklist is usable:
   - **Novice** — has never opened a terminal. Every physical action spelled out, full glossary,
     "how to open a terminal" section. Recommend this when in doubt.
   - **Intermediate** — comfortable with a computer and can run commands, but does not know this
     codebase. One logical action per step, project vocabulary only.
   - **Expert** — a developer or QA engineer. Assertions rather than scenery, verification through
     API/logs/database where that is faster, no hand-holding.

   Ask who will physically execute the checklist if the user is unsure, and write for the **lower**
   level when two people of different levels will share one run. Read `references/detail-levels.md`
   for the full standard and a worked example of the same test at all three levels.
6. **Credentials and test data** — what accounts, keys, or seed data will exist? A test that needs a
   login the tester does not have is a dead test.

If an answer leaves a real ambiguity, ask one targeted follow-up. Do not invent an answer.

---

## Phase 1 — Discover every surface (read the code, never guess)

Map the live surface area **from the repository every time**. Fan out with parallel `Explore` agents
when the codebase is large. Read the orienting documents first: `README.md`, `CLAUDE.md`,
`package.json` / `pyproject.toml` / `Cargo.toml` scripts, `docker-compose.yml`, `.env.example`, and
any roadmap or status document that records what is actually built.

Cover all of these that exist:

| Surface | What to extract |
|---|---|
| **Setup / operations** | every prerequisite, install command, container, migration, seed, env var (name + what it does), and every script in the project's task runner |
| **UI** | every page/route, every button/link/form/modal by its **real on-screen label**, and each state: empty, loading, success, error |
| **UI addresses** | the URL of every page you write a test for — these become `uat:url` markers so the tester can open the screen and annotate it |
| **HTTP API** | every endpoint: method, path, auth tier, a copy-pasteable request, success status, error statuses |
| **CLI** | every command and flag, with exact syntax and expected output |
| **Background work** | cron jobs, queues, workers, webhooks, scheduled tasks — how to trigger one and how to see it ran |
| **Data** | what the user can create, edit, delete; what persists across a restart |
| **Unhappy paths** | wrong input, bad/expired credentials, missing records, permission boundaries, duplicate submissions |
| **Security** | secrets absent from served HTML and API responses, authorization actually enforced, destructive actions gated |

**Only test what is built.** Cross-check every candidate against the repo's own status notes. Anything
deferred, parked, or stubbed goes into a `## Not in scope (deferred — do NOT test)` section so the
tester knows it was excluded on purpose, never into a test that is doomed to fail.

Capture **exact** strings: commands, routes, button labels, env var names, file paths. A beginner
cannot fill in a blank.

### Stop if there is nothing to test

If discovery finds **no runnable surface** — no server, no page, no command, no endpoint; only
configuration, documentation, or a specification for something not yet written — **stop and say so.**
Do not generate a checklist.

This matters because the failure is invisible: a UAT written from a README's promises or a
`CLAUDE.md`'s conventions reads perfectly plausibly, and the tester only discovers it is fiction when
every test fails. Report what you found instead (a spec, an install of someone else's tool, an empty
scaffold), name what would have to exist before a UAT is meaningful, and ask whether a different
repository was intended.

The same applies in the small: a feature that exists only as a mock-up with hardcoded data is not
built. Either exclude it, or test it honestly — see **Testing a known gap** below.

---

## Phase 2 — Propose where the files go

Suggest, then confirm before writing:

```
<repo>/docs/uat/UAT-<app-slug>-<YYYY-MM-DD>.md      the checklist
<repo>/docs/uat/UAT-<app-slug>-<YYYY-MM-DD>.html    the form (generated)
<repo>/docs/uat/assets/<same-slug>/                 screenshots the tester attaches
<repo>/docs/uat/tools/                              the helper scripts, copied from this skill
```

`docs/uat/` is the default because the results belong in the repo where a fix plan can cite them. If
the project has no `docs/` directory, offer `uat/` at the root instead. Use today's date. Use a short
app slug, lowercase, hyphenated.

Also add to the project's `.gitignore` (ask first):

```
docs/uat/.uat-progress-*.json
```

---

## Phase 3 — Write the markdown

Read `references/uat-file-format.md` before writing — the marker syntax is a contract the scripts
depend on. `references/example-uat.md` is a working example of the whole shape.

Every test needs an `<!-- uat:test id=N.M -->` marker under its `### N.M  Title` heading, inside a
section that has a `<!-- uat:section id=N title="..." -->` marker. You do not need to write the
answer blocks — the generator injects them.

Record the level from Phase 0 in the meta block as `tester_level: novice | intermediate | expert`, so
the file states who it was written for and the form can show it.

Set `base_url:` in the meta block to where the app runs (`http://localhost:3000`), and give every test
about a specific screen a `<!-- uat:url /that/path -->` marker directly under its `uat:test` marker.
The form then offers **Open this screen and annotate it** on those tests, and whatever the tester pins
comes back into that test's notes and screenshots. Tests without the marker are unaffected — use it
wherever a test is really about one screen, and leave it off for setup, CLI and API tests.

### The shape of every test

Every test has the same five parts at every level — Goal, Before you start, Steps, PASS looks like,
If it does not work. Only the amount of detail inside them changes.

```markdown
### 3.2  Save a new report
<!-- uat:test id=3.2 -->

- **Goal (plain words):** Store a report so it is still there tomorrow.
- **Before you start:** Test 3.1 is done and passed.
- **Steps:**
  1. Click the blue **New report** button in the top-right corner.
  2. Click the box labelled **Title** and type `My first report`
  3. Click the blue **Save** button at the bottom of the form.
- **PASS looks like:** The form closes and `My first report` appears at the top of the list on the
  left, with today's date next to it.
- **If it does not work:** Write down any red text that appears, and attach a picture of the screen.
```

### How much detail — read `references/detail-levels.md`

That file is the standard for the level chosen in Phase 0, with the same test written three ways.
The short version:

| | **Novice** | **Intermediate** | **Expert** |
|---|---|---|---|
| Steps | one physical action each | one logical action each | one outcome each |
| Glossary | every technical word | project vocabulary only | none |
| Section 0 | how to open a terminal | prerequisites with versions | one line |
| Expected result | what appears on screen | the observable outcome | an assertion |
| Verify via | the UI only | the UI, plus simple commands | whatever is fastest — API, logs, database |

**Coverage does not change with level.** Every surface from Phase 1 gets a test whoever is running it;
only the wording changes. An Expert checklist is shorter, not thinner.

### Writing rules — apply at every level

1. **Give the exact text to type**, in backticks, complete. Never `npm run <something>`. If a value
   must be filled in, show a clearly marked placeholder and say where to get the real value.
2. **Name what to click** using the real label discovered in Phase 1.
3. **Write down the expected result.** The tester verifies by comparing; a step with no stated
   outcome cannot be passed or failed.
4. **Binary PASS/FAIL.** If two people could reasonably record different results from the same
   observation, the test is written badly.
5. **One verifiable claim per test.** Merging three assertions into one checkbox makes a failure
   impossible to triage.
6. **Order by dependency, and by side effect.** Sequence install → configure → start → use →
   operational/destructive, and state each test's preconditions in **Before you start**. Then check
   the other direction: does any test *sabotage the ones after it*? A rate-limit test that locks
   sign-in for fifteen minutes, a test that deletes the record a later test reads, a teardown placed
   mid-checklist — each strands the tester. Move it later, or warn in bold what it will cost them.
7. **Flag every destructive step** in bold, with what is lost and how to undo it.
8. **Say what to capture on failure**, pitched at the level: the exact red text for a Novice, the
   failing response and log line for an Expert.
9. **Keep the tester unblocked**: if one test fails, say whether they can carry on.
10. **Branch on the unexpected.** "If you do not see X, do Y first." (Essential for Novice, useful at
    every level.)
11. **Never ask the tester to write down a secret.** The completed checklist gets committed, mailed
    around and pasted into chat. Ask for the *name* of a key, never its value: "list the variable
    names in `.env`" rather than "paste your `.env`". When a test needs a credential, tell the tester
    where to get it and have them confirm it works — never have them record it. Say so explicitly in
    any test that goes near one, and in the security tests add: if a secret *is* exposed, report which
    name appeared and nothing more.

Do NOT add "how did this look?" questions to the tests — the form gives every test its own look-and-feel
comment box with a severity, and lets the tester report anything the checklist never asked about.

### Testing a known gap

Sometimes the honest test is one that **passes by confirming a defect is still there**: a page that is
a mock-up with fixed data, a feature reachable only by typing a URL, a limitation the team has
accepted for now. Leaving these out lets the next person mistake the mock-up for a working feature;
writing them as ordinary tests produces a failure nobody intends to fix.

Write them so the tester cannot misread which way is which:

- **State the gap in the title** — "Tasks are a demo and do not save", not "Test the Tasks page".
- **Say in the Goal that confirming the limitation is the point**, so a tester does not record Fail
  out of sympathy for the app.
- **Make PASS the current behaviour**: "PASS looks like: the tick is gone after a reload — the change
  was **not** saved, confirming this page is still a demo."
- **Make FAIL mean the gap has closed**: "If your change survives the reload, tasks now persist and
  this test needs rewriting. Say so."

Use this only for gaps you have confirmed in the code. A guess dressed up this way is worse than no
test at all.

### Coverage requirement

Complete means every surface from Phase 1 has at least one test, including setup and teardown, every
UI state, every endpoint/command/job, the unhappy paths, and the security checks. Group by surface,
number `N.M`. **Err on the side of more tests** — but not past the point where the run stops happening.

A checklist nobody finishes is worth less than a shorter one they complete. So:

- **Estimate the run and put it at the top**, in the "what you need" section: roughly a minute per
  Intermediate test, more for anything with a wait in it. Sixty tests is about an hour; a tester who
  budgets thirty minutes will abandon it at test 25 and you will get a partial run.
- **Split by session, not by trimming coverage**, when it runs long: put the setup and the highest-risk
  features in the first checklist, operational and edge cases in a second. Two files that both get
  completed beat one that does not.
- **Never merge tests to shorten the list.** One verifiable claim per test stays true at any length —
  a merged test cannot be triaged when it fails.

### Shell gotchas to bake in

- **Windows PowerShell:** use `curl.exe`, never bare `curl` (it is an alias for `Invoke-WebRequest`
  and ignores `-X`/`-H`/`-d`). Never inline a JSON body with `\"` escaping — write it to a file with
  single-quoted `Set-Content` and send `-d "@body.json"`. Guard `Copy-Item .env.example .env` behind a
  `Test-Path` check so it cannot silently overwrite a real `.env`.
- **Long-running commands** (a server, a watcher): tell the tester to open a **second** terminal and
  leave the first running, and how to stop it (`Ctrl`+`C`).
- Dry-run the setup commands in the real shell where you can, and correct anything that does not work.

---

## Phase 4 — Generate the form

Copy this skill's `scripts/` directory (including `scripts/assets/`) into `<repo>/docs/uat/tools/` so
the UAT folder is self-contained and works on a tester's machine that has never had this skill
installed. Then generate:

```bash
# Python (no dependencies, needs Python 3.8+)
python docs/uat/tools/generate_uat_html.py docs/uat/UAT-myapp-2026-08-23.md

# or Node (no dependencies, needs Node 18+)
node docs/uat/tools/generate-uat-html.mjs docs/uat/UAT-myapp-2026-08-23.md
```

Pick the runtime the target repo already uses. Both produce byte-identical output.

The generator normalises the markdown in place (injecting answer, summary and findings blocks) and
reports the section and test counts. If it prints a file problem — duplicate id, a test outside a
section, an unclosed answer block — fix the markdown and run it again.

**Verify before handing over:**

- The reported test count matches the number of tests you wrote.
- Open the HTML and read it as the beginner would: can every step be done with zero outside knowledge?
- Nothing deferred is presented as testable.

---

## Phase 5 — Hand it to the tester

Give them exactly this, filled in with the real path:

> 1. Open a terminal in the project folder.
> 2. Type this and press Enter:
>    `python docs/uat/tools/uat_server.py docs/uat/UAT-myapp-2026-08-23.md`
>    (or `node docs/uat/tools/uat-server.mjs docs/uat/UAT-myapp-2026-08-23.md`)
> 3. Your web browser opens the checklist. **Leave that terminal window open** while you work.
> 4. Work top to bottom. Every test starts at **Not answered yet** — change it to **Pass**, **Fail**
>    or **Not done** as you go, and write what you saw. Use the purple box for anything you do not
>    like the look or feel of, even when the test passed. Add pictures by clicking the picture box,
>    dragging a file in, or pressing Ctrl+V.
> 5. Where a test offers **Open this screen and annotate it**, click it. The app opens in a new tab.
>    Try the thing the test asks for, then click the **Annotate this page** button on your bookmarks
>    bar (the checklist shows you how to put it there, once). Click anything on the screen to drop a
>    numbered pin, say what is wrong, then press **Done**. Your notes and a picture go straight onto
>    that test — switch back to the checklist tab and they are already there.
> 6. Click **Save my work** whenever you like — it also saves itself every minute.
> 7. When everything is answered click **Submit**. If you cannot finish, use
>    **Submit what I have so far** — the report is then clearly marked as unfinished.
> 8. Press `Ctrl`+`C` in the terminal when you are done.

Tell them the Submit button refuses an incomplete run and lists exactly what is missing with a
"take me there" link, so they cannot accidentally hand in half a UAT.

If the tester opens the `.html` file directly instead of running the helper, the page still works and
keeps answers in their browser, but shows a banner and switches Submit off — it cannot write to a file
without the helper.

---

## Phase 6 — After the tester submits

Submit rewrites the markdown: a summary block at the top (counts, failed IDs, IDs with concerns), each
answer filled in under its test, and a findings section for anything the tester reported that no test
asked about. It also writes `<name>.results.json` for tooling.

Point the user at the **processing-uat** skill to turn that file into a fix plan.

---

## Reference

- `references/uat-file-format.md` — the markdown contract: markers, answer blocks, summary, findings,
  sidecar files, validation rules. **Read this before writing a UAT.**
- `references/detail-levels.md` — the Novice / Intermediate / Expert writing standards, with the same
  test written at all three. **Read this after Phase 0, before writing any test.**
- `references/example-uat.md` — a small complete example, written at Novice level.
- `scripts/generate_uat_html.py`, `scripts/generate-uat-html.mjs` — markdown → HTML form.
- `scripts/uat_server.py`, `scripts/uat-server.mjs` — save / upload / submit helper.
- `scripts/assets/uat.css`, `scripts/assets/uat.js` — the form itself, inlined at generation time.
- `scripts/assets/annotate.js` — the pin-and-comment overlay that runs on the app under test. The
  checklist embeds it in the bookmarklet, so a strict Content-Security-Policy cannot block it.
- `scripts/assets/vendor/html2canvas.min.js` — turns the annotated page into an image (MIT; see
  `vendor/.vendor-note.md`). It re-renders the DOM rather than photographing the screen, which is why
  the tester is shown the result and asked whether it looks right before it is sent.

## Troubleshooting

| Symptom | Cause and fix |
|---|---|
| `no sections found` | a `## ` heading is missing its `<!-- uat:section id=N title="..." -->` marker |
| `test X is not inside any section` | the test marker appears before the first section marker |
| `answer block id=X does not belong to the test above it` | an answer block was moved or its id edited — put it back under its test |
| `duplicate test id` | two tests share an id; ids must be unique |
| Port 8777 busy | the helper walks up to 8796 automatically; the URL it prints is the one to use |
| Screenshots do not show in the markdown | they are relative links — open the `.md` from inside `docs/uat/`, and keep the `assets/` folder next to it |
