---
name: theory-vs-reality
description: Audit a plan vs an implementation. Build an interactive HTML checklist of end-user acceptance criteria, then spawn parallel agents to verify each item against the actual code. Use when validating whether a built feature matches its stated plan, stories, tasks, or subtasks — or when you need a copy/paste-friendly feedback artifact tied to the plan.
disable-model-invocation: true
---

# theory-vs-reality

Compare a plan (stories / tasks / subtasks / acceptance criteria) against the actual built code. Produce an interactive HTML artifact a HUMAN can pick up cold and run, with per-item verdicts pre-filled by code-checking subagents.

**The artifact is a test script, not a summary.** Anyone who reads a row should know exactly which URL to open, which command to run, which file to upload, and what to look for on screen — without reading the plan or the code.

Two purposes:
1. **Plan sanity** — spot when the plan itself doesn't match what the user wanted.
2. **Build sanity** — spot misalignments between plan and implementation.

---

## Stage 0 — Get the source

Accept any of:
- **Direct paste** — plan text in the conversation
- **File paths** — e.g. `stories/*.md`, `subtasks.json`, `plan.md`, `tasks/*.json`
- **A retrieval recipe** — e.g. "run `aaa ralph subtasks list`", "read all `.md` under `docs/plans/`"

If the source isn't clear, ASK ONCE. Don't guess.

---

## Stage 1 — Distill end-user criteria (titles only)

Read the source. KEEP ONLY criteria that involve a HUMAN END USER — things they see, click, read, hear, copy/paste, or are blocked by. DROP backend-only criteria (DB schema, API contracts, internal refactors) UNLESS they surface in UX.

Group criteria into sections by feature/story (A, B, C…). Number each item within its section (A1, A2, B1, B2…). These IDs are PERMANENT — the user will reference them in feedback.

For each item, output ONLY:
- `id` — e.g. `A1`
- `title` — ≤8-word headline
- `intent` — ONE line of what the user should be able to do (no procedure yet)

If no human-facing criteria exist, say so plainly and stop.

---

## Stage 2 — Per-item: discover recipe + verify (parallel)

For each item, spawn ONE subagent IN PARALLEL. Batch up to 10 per message (one message = multiple `Agent` tool calls = parallel execution).

Each subagent receives:
- The single item (`id`, `title`, `intent`)
- The working directory
- A list of likely sources: `GUIDE.md`, `README.md`, `docs/`, `scripts/`, `e2e/`, `fixtures/`, `docker-compose.yml`, `Makefile`, `package.json` scripts, runbooks
- The output schema below

The subagent has TWO jobs, done together:

### Job A — Build a test recipe a stranger could run

Hunt the repo for the CONCRETE artifacts a human needs. Required shape:

```
Setup:
  - <prereqs: how to start the app, base URL, login creds, env vars, seeded data>
Steps:
  1. <observable action: click, navigate, run command, upload file>
  2. <observable action>
  3. ...
Look for:
  ✅ <specific observable signal: text on screen, badge, status, exit code, file appearing>
  ❌ <specific failure signal>
```

Rules:
- Every command must be copy-pasteable (no `<placeholder>` unless the user obviously fills it).
- Every URL must include host (use `http://localhost:<port>` if local; cite the port from code/docs).
- Every fixture or input file must include its path in the repo.
- If a credential is needed, name the seed user / file where it's defined.
- If the recipe can't be built from the repo (no docs, no e2e, no scripts), say so in `recipe_gaps` and write the most-defensible best guess.

### Job B — Verify against the built code

Now check whether the recipe actually works against the current codebase. Return one of:
- `pass` — the feature is wired up; a human running the recipe would see ✅
- `fail` — broken or missing; a human would see ❌
- `partial` — wired up for some paths/inputs but not others; name which
- `unknown` — can't tell from code alone (e.g. needs a running env or external service)

Verdict MUST be expressed in observable terms — what the user would SEE — with a code pointer in parens for the engineer.

### Output schema (one subagent → one JSON blob)

```json
{
  "id": "A1",
  "recipe": {
    "setup": ["…"],
    "steps": ["…"],
    "look_for_pass": "…",
    "look_for_fail": "…"
  },
  "recipe_gaps": "optional — what couldn't be filled and why",
  "verdict": {
    "status": "pass|fail|partial|unknown",
    "observable": "what the user would see, in plain English",
    "code_pointer": "path/file.ext:line"
  }
}
```

Collect all blobs. If any subagent fails, retry that one ONCE.

---

## Stage 3 — Generate the HTML artifact

Spawn ONE subagent using the highest-intelligence model the host supports.

**Inputs:** all the JSON blobs from Stage 2, sections from Stage 1.

**Output path:** `<cwd>/<project-name>-theory-vs-reality-<YYYYMMDD-HHmm>.html` (project-relative, NOT `/tmp/` — the user wants it next to the code).

**HARD requirements for the HTML — two-level accordion layout:**

1. **Single self-contained file** — inline CSS, inline JS. NO external deps. NO CDN.

2. **Sticky toolbar at top** (stays visible while scrolling):
   - Title (project + milestone)
   - Live status counts: ✅ / ❌ / ⚠️ / ❓ / ⏳
   - Progress bar: `N / TOTAL reviewed` (anything that isn't ⏳ counts as reviewed)
   - Filter chips: `All` · `Pending` · `Failed` · `Partial` (clicking a chip auto-expands matching items)
   - Buttons: `Export markdown ⤓` · `Expand all ⇕` · `Collapse all`

3. **Two-level accordion:**
   - **Level 1 — Section** (`A — Import …`): collapsible. Header shows `N items · ✅X ⚠️Y ❌Z` rollup.
   - **Level 2 — Item** (`A1`, `A2`, …): collapsible. Collapsed header shows ID badge, title, and current status pill.
   - **Default open state on first load:** the FIRST section that has any ⏳ pending item is expanded; everything else is collapsed. All items inside that section stay collapsed. This lands the user on "where work begins."

4. **Status stripe** — each item row has a colored left edge (`border-left: 4px solid <status color>`) so the user can scan and spot pending/failed at a glance.

5. **When an item is expanded, it shows (flat, no further accordions except the verdict reveal):**
   - Status selector: `⏳ pending` · `✅ works` · `❌ broken` · `⚠️ partial` · `❓ unclear`
   - `How to test` block in a distinct background:
     - `Setup` — bulleted list
     - `Steps` — numbered list
     - `Look for ✅` / `Look for ❌` — two color-coded lines
   - `Notes` — textarea
   - `▶ Reveal pre-filled verdict (form your own opinion first)` — closed by default. When opened, reveals: status emoji + observable sentence + code pointer.

6. **Keyboard nav** (when no textarea focused):
   - `j` / `k` — next / previous item (auto-expanding the focused one)
   - `Enter` / `Space` — toggle expand on focused item
   - `1` / `2` / `3` / `4` — set status `works` / `broken` / `partial` / `unclear` on focused item
   - `v` — toggle "reveal verdict" on focused item
   - `e` — focus the notes textarea of the focused item
   - `/` — focus the filter chips
   - Show a small `Keyboard shortcuts` hint at the bottom of the sticky toolbar.

7. **Export button** copies all annotations to clipboard as markdown:
   ```
   ## A1 — <title>
   Status: ❌
   Pre-filled verdict: ⚠️ partial — <observable> (<path:line>)
   Notes: <user notes>
   ```

8. **Readable** — monospace IDs, generous whitespace, respects `prefers-color-scheme`. Status colors are consistent everywhere (stripe, pill, counts).

### Visual reference — what the HTML must look like

The HTML must mirror this layout. Treat it as the spec, not a suggestion:

```
╔══════════════════════════════════════════════════════════════════════════╗
║  <Project> <Milestone> — Theory vs Reality                               ║
║   ✅ 3    ❌ 1    ⚠️ 5    ❓ 0    ⏳ 4              [Export markdown ⤓]  ║
║   Progress  ▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░  9 / 13  reviewed                     ║
║   Filter: ( All ) ( Pending ) ( Failed ) ( Partial )                     ║
║                                            [Expand all ⇕] [Collapse all] ║
╚══════════════════════════════════════════════════════════════════════════╝

▼ A — <Section title>                                    3 items · ✅1 ⚠️2
┌──────────────────────────────────────────────────────────────────────────┐
│ ┃ ▶  A1   <title>                                             ⚠️ partial │
├──────────────────────────────────────────────────────────────────────────┤
│ ┃ ▼  A2   <title>                                             ⚠️ partial │
│ ┃                                                                        │
│ ┃    Your call:  [ ⏳ pending ]  [ ✅ works ]  [ ❌ broken ]              │
│ ┃                [ ⚠️ partial ]  [ ❓ unclear ]                          │
│ ┃                                                                        │
│ ┃    ╭─ How to test ────────────────────────────────────────────╮        │
│ ┃    │  Setup                                                   │        │
│ ┃    │   • <prereq line>                                        │        │
│ ┃    │  Steps                                                   │        │
│ ┃    │   1. <action>                                            │        │
│ ┃    │   2. <action>                                            │        │
│ ┃    │  Look for                                                │        │
│ ┃    │   ✅  <pass signal>                                      │        │
│ ┃    │   ❌  <fail signal>                                      │        │
│ ┃    ╰──────────────────────────────────────────────────────────╯        │
│ ┃                                                                        │
│ ┃    Notes  ╭──────────────────────────────────────────────────╮         │
│ ┃           │                                                  │         │
│ ┃           ╰──────────────────────────────────────────────────╯         │
│ ┃                                                                        │
│ ┃    ▶  Reveal pre-filled verdict   (form your own opinion first)        │
├──────────────────────────────────────────────────────────────────────────┤
│ ┃ ▶  A3   <title>                                              ✅ pass   │
└──────────────────────────────────────────────────────────────────────────┘

▶ B — <Section title>                                   3 items · ✅2 ❌1
▶ C — <Section title>                                   2 items · ⚠️2
```

The `┃` is the status stripe — coloured by current status.

Verify the file exists before continuing. If the HTML subagent fails, retry ONCE with a simpler brief; if still failing, report the failure and stop.

---

## Stage 4 — Hand off

1. Print the absolute path to the file.
2. Open it: `open <path>` (macOS) · `xdg-open <path>` (Linux) · else print `file://<abs-path>`.
3. End with a one-line tally + an actionable starting point:
   `📊 <N> items · ✅ X · ❌ Y · ⚠️ Z · ❓ W — start with the ❌s, then the ⚠️s.`

---

## Recipe template + worked examples

### The template every recipe MUST follow

Fill in EVERY slot. If a slot can't be filled from the repo, leave the marker AND record the gap in `recipe_gaps`. Never delete a slot to hide a gap.

```
<ID> — <≤8-word title>

Setup:
  - <how to start the system: command + URL>
  - <auth / credentials, with the file where they're seeded>
  - <any required env vars, services, or seed data>

Steps:
  1. <ONE observable action — navigate, click, run a command, upload a file>
  2. <next observable action>
  3. <…keep going until the moment of truth>

Look for:
  ✅ <ONE specific signal the tester can see / read / measure>
  ❌ <ONE specific failure signal>

Pre-filled verdict (hidden by default):
  <status emoji> <pass|fail|partial|unknown> · <observable sentence> · (<path/file.ext:line>)
```

Rules of thumb:
- "Steps" are physical actions a human takes. Not "the system validates X" — that's a Look-for, not a Step.
- "Look for" is what shows up ON SCREEN / IN TERMINAL, not what happens in the database (unless the test deliberately inspects the DB via a documented command).
- If a step has a "wait", give a concrete duration ("wait ~15s", not "wait a bit").

### Example 1 — UI flow (web app)

> **A2 — Failed zip shows visible terminal state**
>
> *Setup:*
> - `pnpm dev` then open http://localhost:3000/imports
> - Login: `admin@jtsupport.com` / `dev` (seeded in `packages/auth-server/src/seed-auth-development-link.ts:88`)
>
> *Steps:*
> 1. Drop `fixtures/corrupt-archive.zip` into `./local-blob/inbound/`
> 2. Wait ~15s, refresh `/imports`
> 3. Find the row for `corrupt-archive.zip`
>
> *Look for:*
> - ✅ Row shows red "Failed" badge AND a non-empty error message column
> - ❌ Row never appears, or shows "Processing…" indefinitely, or empty error text
>
> *Pre-filled verdict (hidden):* ⚠️ partial · Invalid-XML zips do show Failed on /imports, but corrupt-archive zips only log to the ZipIngestLog table and never surface in the browse UI. (`apps/api/src/procedures/imports.ts:425`)

### Example 2 — CLI command

> **B1 — Replay CLI recovers stuck zips**
>
> *Setup:*
> - Local DB up: `pnpm db:up`
> - Seed a stuck zip: `pnpm seed:stuck-zip` (writes one row to `ZipIngestLog` with state=`Extracted`)
>
> *Steps:*
> 1. Run `pnpm blob:replay --state=Extracted --limit=1`
> 2. Observe terminal output
> 3. Open http://localhost:3000/imports
>
> *Look for:*
> - ✅ CLI prints `Replayed 1 zip` with exit code 0, AND the zip now appears on `/imports` with status "Imported"
> - ❌ CLI exits non-zero, prints "No matching zips", or `/imports` still shows nothing
>
> *Pre-filled verdict (hidden):* ✅ pass · `blob:replay --state=Extracted` runs and re-enqueues the row; integration test covers exact path. (`packages/data/tests/integration/blob-replay-cli.test.ts:276`)

### Example 3 — Cross-environment / permission check

> **D2 — Pam can upload via AAD to cti-inbound**
>
> *Setup:*
> - `az login` as `pam@jtsupport.com` (her real AAD account)
> - Confirm her OID: `az ad signed-in-user show --query id -o tsv`
>
> *Steps:*
> 1. From any folder, run:
>    `az storage blob upload --auth-mode login --account-name ctidev2 --container-name cti-inbound --name pam-smoke.zip --file fixtures/comverse-sample.zip`
> 2. Wait ~30s
> 3. Open https://admin.dev-2.example.com/imports
>
> *Look for:*
> - ✅ `az` command exits 0, AND a row for `pam-smoke.zip` appears on `/imports` with status "Imported"
> - ❌ `az` command returns `AuthorizationPermissionMismatch` / 403, or row never appears
>
> *Pre-filled verdict (hidden):* ❌ fail · `az ... upload` returns 403 because Pam's OID is missing from `cti_inbound_uploader_oids`. (`new-terraform/environments/dev-2/dev-2.auto.tfvars:96`)

### Contrast — what NOT to produce

❌ "JT staff can see imported company, account, bill period, charges, and failure error text in /imports, the company dashboard, and the usage report."
↑ This restates the criterion. No URL host. No login. No fixture. No specific text/badge. Useless to a tester.

❌ "A developer can run inbound-import rehearsal locally in either Mode A or Mode B."
↑ Which command? What proves "it worked"? Tester has nothing to do.

---

## Constraints

- ONE file output. The HTML. Don't scatter other artifacts.
- Read-only verification. Don't modify code, don't run tests.
- If the plan has zero human-facing criteria, say so and stop — don't fabricate items.
- If a recipe genuinely can't be built (the feature is so unbuilt nothing exists to test), surface that in `recipe_gaps` rather than inventing fictional URLs/commands.
