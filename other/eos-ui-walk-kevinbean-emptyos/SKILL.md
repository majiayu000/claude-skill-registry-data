---
name: eos-ui-walk
description: Act as the user of EmptyOS and walk the product by hand in a real browser, performing real workflows end to end (capture a task, write a journal entry, look something up in the KB, add a job application). Judge BOTH axes at every step — does the flow work (works / slow / confusing / broken), AND is the feature set enough to finish the real job (missing = feature gap). Screenshot the meaningful steps into a self-contained HTML report with a per-use-case sufficiency verdict. Use when the user says "UI walk", "dogfood the UI", "act as me and use the app", "walk the real use cases", "test it like a user", or "is the app enough for my workflow". NOT for visual polish (use eos-page-design-review / eos-design-system-audit), NOT for backend correctness such as async wedges or vault read-modify-write races (use eos-bug-audit), NOT for wiring (use eos-architecture-review), NOT the fix-until-clean loop (use eos-usecase-audit — it wraps this walk).
---

# EmptyOS UI Walk — dogfood as the user

**Be Kevin.** Don't load pages to check for 404s — *use the product the way its
owner uses it*, complete real tasks end to end, and notice the friction only a
real user feels: a step that's slow, a button whose result is invisible, a flow
that needs one click too many, an empty state that doesn't tell you what to do,
a form that loses your input. The deliverable is a **screenshot-backed HTML
report** the user can open and skim.

This is dogfooding, not a test suite. Your judgment per step is the signal:
`pass` (it just worked), `slow` (worked but made me wait), `confusing` (worked
but I had to think / hunt), `fail` (broke / dead end), `missing` (the real job
needs a capability that doesn't exist — a feature gap, not a bug). Be honest —
a clean report that says "everything worked" is a fine and valuable outcome,
**but only if the real jobs could actually be finished**: "every button works
and I still couldn't do my work" is a gap report, not a clean pass. The walk
measures product quality AND product boundaries.

The automated scanners (`check-js-errors.py`, `check-clickable.py`) are NOT the
job here — they're a 60-second optional pre-pass for crude breakage. The job is
the **hand-walk of real use cases**.

## This is a loop

Built to run under `/loop dogfood the UI as me`. One iteration = pick a fresh
set of use cases → walk them as Kevin → screenshot + judge each step → render
the HTML report → tell the user where it is and the headline findings. Re-running
rotates to **different** use cases (don't re-walk the same five forever) until
coverage of the real workflows is broad, then say so and stop.

## Step 0 — Preflight (every iteration)

```bash
curl -s -m 5 http://127.0.0.1:9000/api/health     # daemon up? apps count
git status --short                                 # pre-existing drift (leave others' files alone)
```

- **Daemon down** → surface it and stop. NEVER restart `:9000`/`:9001` from a
  tool (`.claude/rules/daemon-handling.md`).
- This is mostly a *read* activity that produces an artifact under `data/`
  (gitignored). You only commit if you actually fix a bug (rare) — and then ONLY
  your own files by explicit path (Step 7).

## Step 0.5 — Pick a browser backend (this walk is NOT bound to any one browser)

The walk drives **generic** browser verbs (`browser_navigate`, `browser_click`,
`browser_type`, `browser_snapshot`, `browser_take_screenshot`). Any MCP browser
backend that provides them works:

| Backend | Tools | When |
|---|---|---|
| **Playwright MCP** | `mcp__plugin_playwright_playwright__browser_*` | **Default.** Headless, always available, no user setup. |
| Claude-in-Chrome | `mcp__claude-in-chrome__*` | When the user wants to watch in their own Chrome, or a flow needs their logged-in session. |

**"The Chrome extension isn't connected" is NEVER a valid reason to skip this
walk.** Fall through to the Playwright MCP and keep going. This walk is the ONLY
mechanism that catches the perceptual/affordance class of bug — panels that blur
together, a list you can't tell scrolls, a missing readout, a control that
doesn't explain itself. Every *automated* rendered check targets a narrower axis
(`check_readability.py`=contrast, `check-clickable.py`=occlusion,
`check_ui_affordance.py`=overflow + tab-roles, `check_ui_structure.py`=EOS_UI
adoption). Skipping the hand-walk silently drops perceptual coverage to **zero**
— which is exactly how a batch of CAD-workspace UX bugs shipped on 2026-07-11
behind a green `node --check` + `pytest` + `curl`.

Corollary: **a rendered-UI change is not verified until it has been looked at.**
Static checks passing is not the same as the surface being usable.

## Step 1 — Authenticate the live browser (once per run)

The daemon is password-gated, so the MCP browser starts unauthenticated and every
page 302s to `/login`. Sign it in with a one-time token deep-link — the server
sets the `eos_session` cookie and strips the token from the URL:

```bash
python -c "import tomllib;print((tomllib.load(open('emptyos.toml','rb')).get('network',{}).get('auth_token')) or '')"
```

Then `browser_navigate` to `http://127.0.0.1:9000/?token=<TOKEN>` **once**. After
the redirect you're authenticated for the whole session — every subsequent
`browser_navigate` to an app works. (If `auth_token` is empty, the daemon has no
gate; navigate straight to `/hub/`.) Override `EOS_URL` if walking a remote
daemon (Tailscale/LAN), and adjust the navigate base accordingly.

Set up the run folder + step-log path:

```
data/ui-walk/usecases/<YYYY-MM-DD-HHMM>/      # screenshots land here
data/ui-walk/usecases/<YYYY-MM-DD-HHMM>/steplog.jsonl
```

For a need-first walk, also write `scenario.md` in the run folder — the real
user outcome, team/roles, and lifecycle milestones — with the trace identity
in block-style YAML frontmatter (`.claude/rules/loop-traceability.md`):

```yaml
---
usecase_id: riverside-bess-132kv        # slug for the months-long user need
need: One line stating the real outcome the user must accomplish
milestones:
  - id: month-0-design-basis            # slug per lifecycle checkpoint
    title: "Month 0: establish the project design basis"
---
```

Rows that carry `usecase_id`/`milestone_id` keep that identity through
promotion → fix → verification → receipt. Legacy walks without frontmatter
still work — identities derive deterministically from the free-text fields.

## Step 2 — Pick the use cases (act as Kevin)

### Need-first, not feature-first

Start from a real user outcome, not from the inventory of apps EmptyOS already
has. Define the work as the user would: the project duration, roles, milestones,
decisions, evidence, handoffs, reviews, revisions, and final deliverable. Then use
the available apps wherever they genuinely help. Existing features are evidence,
not the boundary of the test.

For long-running work (for example, a design project spanning months), sample
representative lifecycle checkpoints rather than reducing the walk to isolated
calculator demos. At every checkpoint ask both:

1. **Does the current flow work?** Judge the interaction as `pass`, `slow`,
   `confusing`, or `fail`.
2. **Can the user finish the real job?** Use `missing` (`GAP` in the report) when
   a needed capability, handoff, traceability link, review state, change-impact
   signal, or deliverable step is absent — even if every visible control
   technically works. State the unmet need in `note`.

Never reshape the user's need to fit what EmptyOS can already provide. The walk
should reveal both product quality and product boundaries.

Choose **5–8 real workflows** this iteration, weighted toward what Kevin actually
does. The committed scenario catalog
(`apps/extension/dev/dogfood-agent/scenarios/*.md`, authored via
`eos-new-usecase`) is a ready source of walkable flows — check it before
inventing one. Don't script rigidly — follow curiosity the way a real user
would, and let one step suggest the next. Starter catalog (rotate across
iterations; combine / deviate freely):

- **Capture → task → done** — `/hub/` capture box → type a task → confirm it lands
  in Today / `/task/` → mark it done → confirm it disappears.
- **Daily journal** — `/journal/` write an entry + set a mood → confirm it shows on
  the hub heatmap / streak.
- **KB lookup (cable engineering)** — `/kb/` search a real concept (e.g. IEC 60287,
  ampacity) → open a `clause`/`formula` note → follow a citation/backlink.
- **AI search / ask** — `/search/` ask a vault question → read the answer → pin it.
- **Job application** — `/jobs/` (personal) add an application → set status →
  open the board view → confirm the card moved.
- **Learn / vocab** — `/learn/` start an SRS review, rate a card; or `/dictionary/`
  look up a word, save it.
- **Projects** — `/projects/` open a project detail → check the 4D timeline drawer.
- **People / expense / reminders** — add one record, confirm it aggregates.
- **A generator** — `/viz/` or `/designer/` describe an artifact → generate → look
  at the result (judge "did I get something usable?", not pixel quality).
- **Home glance** — `/hub/` cold: does the digest tell me my next move at a glance?

Prefer flows that **cross apps** (capture → task → project ripple) and flows that
**write then read back** (did my entry actually persist and surface?) — that's
where real friction hides.

## Step 3 — Walk each use case, step by step

For each meaningful step:

1. **Do the action** — `browser_navigate`, `browser_click`, `browser_type`,
   `browser_fill_form`, `browser_select_option`, `browser_press_key`. Use
   `browser_snapshot` to find elements to act on.
2. **Let it settle** — `browser_wait_for` (text/time) so the screenshot catches
   the rendered result, not a spinner.
3. **Screenshot** — `browser_take_screenshot` with an explicit `filename` like
   `uc1-s2.png`. **Record the saved path** the tool returns.
4. **Judge + log** — append one line to `steplog.jsonl`:

```json
{"usecase":"Capture a task and see it in Today","step":2,"action":"Type 'call plumber' in capture, hit Enter","status":"slow","note":"toast confirmed but took ~2s; task appeared in Today only after manual reload","shot":"/abs/path/uc1-s2.png","url":"http://127.0.0.1:9000/hub/","usecase_id":"daily-capture-flow","milestone_id":"capture-to-today"}
```

`usecase_id`/`milestone_id` are the optional trace identity (match the
scenario.md frontmatter when you wrote one) — they let a promoted finding keep
its origin all the way to the loop receipt.

`status` ∈ `pass | slow | confusing | fail | missing | skipped | info`. The `note` is the
point — write what a real user would mutter: "couldn't tell if it saved",
"had to scroll to find the button", "empty and no hint what to do". Screenshot
the **payoff** steps (the result of an action), not every navigation.

Also opportunistically catch the cheap breakage classes while you're there: a
visible JS error, a button that 404s, a dead dropdown (route returns nothing) —
log those as `fail` with the detail.

### Step 3.5 — Failure context bundle: replay GIF + console + network for `fail` / `confusing` steps

A still can't show *how* a flow went wrong — the click that did nothing, the
state that flashed and vanished, the result that never arrived. And a finding
without its console/network context makes the fixer re-reproduce what the walk
already saw. So when a step lands `fail` or `confusing` (and it reproduces —
triage first, Step 4), attach the same context bundle a good bug-report tool
(jam.dev shape) auto-collects: **replay clip + console errors + failed
requests**, all fields the report renders inline.

**Console + network (do this for every `fail` — it's two free tool calls):**

- `browser_console_messages` (filter to errors/warnings — use the `pattern`
  param or pick out `error` lines) → steplog `"console": ["..."]`.
- `browser_network_requests` → keep only failed/4xx/5xx entries →
  `"network": ["GET /task/api/list -> 500"]`.
- Both render as collapsible blocks under the step note, so the person (or
  fix-agent) reading the report starts from the error, not from scratch.

**Timing (evidence for `slow`):** when a verdict is `slow`, put the measured
wait in the steplog as `"ms": 4200` (from your `browser_wait_for` bound or the
gap you observed) — the report shows it as a chip. A `slow` with a number is a
perf thread; a `slow` without one is a vibe.

**Replay GIF (for flows where motion is the evidence):**

- **Claude-in-Chrome backend** — use the native `gif_creator` tool: capture
  extra frames before/after each action while re-driving the flow, save with a
  meaningful filename (`uc1-fail.gif`) into the run folder.
- **Playwright MCP backend** (no gif tool) — re-drive the failing flow taking a
  **frame burst**: one `browser_take_screenshot` after each action, ordered
  filenames `uc1-f01.png`, `uc1-f02.png`, …. Then stitch:

  ```bash
  python scripts/ui_walk_gif.py --out data/ui-walk/usecases/<run>/uc1-fail.gif \
    data/ui-walk/usecases/<run>/uc1-f01.png data/ui-walk/usecases/<run>/uc1-f02.png ...
  ```

  (Downscales to ≤800px wide, ~0.9s/frame, holds the end state; caps at 12
  frames. Fail-soft — if Pillow is missing it says so and the still remains
  the evidence.)

Add the clip to that step's `steplog.jsonl` record as `"gif": "<path>"` — the
report renders it under the still with a ▶ replay label, autoplaying.

**Discipline (CI-style retain-on-failure):** capture the bundle ONLY for
`fail` / `confusing` verdicts — a healthy walk records zero clips and zero
context blocks. Keep a clip to one flow (≤12 frames), not the whole walk.
Don't blanket-record video: recording is cheap, but artifacts nobody reviews
are pure litter, and the stills remain the skim layer the report is built on.
If the friction is *timing* (a `slow` step), a GIF adds nothing — the `ms`
chip + note is the evidence. Heavier replay media (rrweb DOM-event replay,
Playwright traces) are deliberately deferred — see `docs/DEFERRED-WORK.md` —
because they belong to the scripted pytest layer, not this hand-walk.

## Step 4 — Triage (false-positive discipline — `.claude/rules/audits.md`)

Before calling anything a `fail`:

- **Data-volume slowness on the real vault is NOT a code bug.** `/task/` taking a
  beat (whole-vault `- [ ]` scan) or `/vault-graph/` straining (rendering every
  node) is the user's large real vault, not a defect. Log it `slow` with a note,
  flag it as a perf/design thread for the user — don't blind-fix against real data.
- **Transient one-off** that doesn't reproduce on a second try → drop or `info`.
- A friction that's really *design* (flat panel, weak spacing) → note it briefly
  and route to the design skills; don't manufacture an interactive "bug".

What's left — a reproducible broken flow, a dead feature, a genuinely confusing
step — is the real signal.

## Step 5 — Render the HTML report

```bash
python scripts/ui_walk_report.py \
  --steplog data/ui-walk/usecases/<run>/steplog.jsonl \
  --out data/ui-walk/usecases/<run>/report.html \
  --title "EmptyOS UI walk — <date>" --persona Kevin
```

It groups by use case (worst-first), base64-embeds every screenshot **and any
`gif` replay clips** into one self-contained file, badges each step, and rolls
up pass/slow/confusing/fail counts. Output is under `data/` (gitignored) — an
artifact to **show the user**, not committed. A missing screenshot or GIF
renders a placeholder, never a crash.

**Rendering never mutates any queue.** The report is a terminal evidence
artifact; findings enter the fix loop only through the explicit triage step
below.

## Step 5b — Triage: promote findings (deliberate, human-gated)

The `fail | confusing | missing` rows are durable in the steplog + report, but
they do NOT become issues by themselves. When the user wants findings acted
on, bridge them one by one (`.claude/rules/loop-traceability.md`):

```bash
python scripts/ui_walk_promote.py list --walk data/ui-walk/usecases/<run>
python scripts/ui_walk_promote.py promote --walk <run-dir> --step-key <usecase>::<milestone>::sN
python scripts/ui_walk_promote.py dismiss|defer|decline --walk <run-dir> --step-key <k> --reason "..."
```

- **Promote** writes a fix-prompt into the shared queue with the trace identity
  + evidence (screenshot, URL, console, steplog path). Re-promoting the same
  finding updates the same file — no duplicates. An already-closed finding is
  refused unless `--force-regression`.
- **`missing` findings are feature gaps**, not bugs — defer/decline them (or
  promote then `close --disposition planned|deferred|declined`) without
  pretending a code fix happened. `defer` prints a proposed
  `docs/DEFERRED-WORK.md` row to paste.
- Never promote in bulk without reading each row — the human judgment IS the
  triage.

## Step 6 — Fix only a clear, root-caused bug (optional)

Most iterations produce a report, not a code change. But if the walk surfaced a
real, reproducible interactive bug with an obvious root cause:

- Fix at the source (`.claude/rules/debugging.md`); prefer the platform fix (one
  bug in `eos.js` over N pages — `feedback_platform_fix_for_n_app_bugs`).
- Reuse `EOS_UI` / `EOS.*` helpers; match surrounding code.
- **Verify**: static change (`pages/*.html`, `static/*.js`, CSS) hot-reloads — re-walk
  the step and confirm. Python change is NOT live until the user restarts `:9000`
  (you can't) — verify on a leased sandbox (`.claude/rules/sandbox-driven-testing.md`)
  or `py_compile` + tell the user a restart is needed.

## Step 7 — Commit a fix (only when you actually changed code)

- Commit ONLY files you changed, by explicit path: `git commit -o path/to/file -m "..."`.
  NEVER `git add -A` / `git add .` (parallel-session drift — `.claude/rules/environment.md`).
- `apps/personal/` is gitignored — a fix there is local-only; say so.
- Conventional-commit message; end with the `Co-Authored-By` trailer. Then
  `git log --oneline -3` to confirm your commit landed.
- The report HTML itself is **never committed** (it's under `data/`).

## Step 8 — Report + loop decision

Tell the user:
- **Sufficiency verdict per use case, first** — one line each: `complete` /
  `complete-with-friction` / `blocked-by-bug` / `blocked-by-gap` /
  `workaround` (finished only by leaving the system — log the workaround as a
  `missing` finding too). Judge against the real goal, not against the steps
  that happened to be walkable; a goal silently skipped because no feature
  supports it is `blocked-by-gap`, not `complete`.
- **Where the report is** (the `report.html` path) and how to open it.
- **Headline findings** — the `fail`/`confusing`/`slow`/`missing` steps in
  plain language ("adding a task works but doesn't show in Today without a
  reload"; "there is no way to record a design decision against the project —
  had to hand-edit the note").
- **Anything fixed** (with commit hash) and anything **flagged-not-fixed** (the
  data-volume/perf/design class) and why.
- **Triage summary** — which findings were promoted / dismissed / deferred /
  declined (from `triage.jsonl`), and which await the user's call.

If this pass walked its use cases and the remaining real workflows are already
well-covered by prior iterations, say coverage is broad and **end the loop** —
don't re-walk the same flows forever, and don't invent friction to keep going.
Otherwise the next iteration rotates to fresh use cases.

## Cross-references

- `scripts/ui_walk_report.py` — the use-case step-log → HTML renderer (this skill's artifact half).
- `scripts/ui_walk_promote.py` — the Step 5b triage bridge (walk finding → fix-prompt queue / disposition).
- `.claude/rules/loop-traceability.md` — trace identity + gap lifecycle + learning outcomes.
- `scripts/ui_walk_gif.py` — frame-burst → replay-GIF assembler for the GIF-on-failure step (Playwright backend; claude-in-chrome uses its native `gif_creator`).
- `scripts/_eos_browser.py` — auth/token + base-URL resolution shared by the walkers.
- `scripts/check-js-errors.py` / `scripts/check-clickable.py` — the optional crude-breakage pre-pass.
- `scripts/ui_walk_audit.py` — the older *per-app* screenshot walk (one shot per app); complementary, not this.
- `.claude/rules/audits.md` — false-positive discipline.
- `.claude/rules/debugging.md` — root-cause-before-fix.
- `.claude/rules/daemon-handling.md` — never restart `:9000`/`:9001`.
- `.claude/rules/sandbox-driven-testing.md` — verify Python fixes off `:9000`.
- `eos-bug-audit` (backend correctness), `eos-page-design-review` / `eos-design-system-audit` (visual/design) — the adjacent skills this one is deliberately NOT.
- `eos-usecase-audit` — the orchestrator that adds CLI/bridge lanes and drives the fix→re-walk-until-clean loop on top of this walk's mechanics.
- `eos-new-usecase` — authors scenarios into the dogfood catalog (the house contract lives in its `scenario-shape.md`).
