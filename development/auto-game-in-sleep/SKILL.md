---
name: auto-game-in-sleep
description: "Fully autonomous unattended game production run (auto-game-in-sleep — 'make the game while you're not at the keyboard'). Chains every studio workflow from concept to polished game, makes all decisions on the user's behalf (logged for audit), tests the running game itself on the local build, iterates until quality bars are met, and leaves a report for when you return. Game languages (array) and project-doc language are configurable. Use when the user wants a hands-off / non-interactive / fully automatic run — e.g. 'auto-game-in-sleep', 'autopilot', 'run the whole pipeline yourself', '睡一觉醒来游戏做好', '一晚上自动做完游戏', '不要问我，全部自己决定'."
argument-hint: "[resume | fresh] [— review: solo|lean|full] [— testing: native|headless] [— game-lang: 简体中文,English] [— docs-lang: 简体中文] [— engine: Godot] [— target: Desktop,Web] [— debug: native] [— dim: 2D|3D|both] [— dev-lang: GDScript|C#|both] [— input: keyboard+touch] [— perf: none|defaults] [— art: svg] [— vision: auto|native|mcp] [— score: 9]"
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, TodoWrite, Agent, Skill
---

# auto-game-in-sleep — Autonomous Unattended Studio Run

`auto-game-in-sleep` means "make the game while you're not driving" — the run
executes in a non-interactive state, with no user in the loop. It is not a
literal overnight timer; the name is about *unattended* execution.

One invocation of this skill = one complete studio run. You pick up wherever
the project stands (or start from nothing), drive the full pipeline defined in
`${CLAUDE_PLUGIN_ROOT}/docs/workflow-catalog.yaml`, test the running game yourself, and only
stop when the game is done or further progress is impossible. **There is no one
to ask — the user is away from the keyboard.**

Autopilot overrides the interactive behaviors of every other skill in this
template. When you execute a workflow skill while running this pipeline, its
"wait for the user" instructions are suspended and replaced by the Decision
Protocol below. Everything else in those skills (templates, section order,
quality bars, artifact paths) applies unchanged.

**Output:**
- `production/auto-game-in-sleep/state.json` — resumable run state + heartbeat
- `production/auto-game-in-sleep/decisions.md` — append-only decision log (the user audits this)
- `production/auto-game-in-sleep/journal.md` — timestamped, self-contained progress journal
- `production/auto-game-in-sleep/test-runs/` — run logs, frame captures, test notes
- `production/auto-game-in-sleep/morning-report.md` — the report for when the user returns (what was built, how to run it, what to do next)

---

## Constants

**Defaults are the strictest configuration.** A bare `/auto-game-in-sleep`
with no arguments runs everything below at full strictness (full reviews,
native testing, unbounded rounds). Each constant below states its own
default; the em-dash flags only *relax* from that baseline — never assume a
lenient default.

> 💡 These are defaults. Override by telling the skill, e.g.
> `/auto-game-in-sleep — review: solo` or `/auto-game-in-sleep fresh —
> testing: headless`.

- **NO TIME CAP.** This skill imposes no time limit and you must not invent
  one. Run until the pipeline is complete or genuinely blocked. How long that
  takes depends on external factors (API throughput, tool availability) that
  you cannot estimate — guessing a duration only makes you stop early. The
  closest thing to a "stop" is the quality/stall logic below, never a clock.
- **GAME_LANGS = [简体中文]** — the languages the shipped game contains, as an
  array. Element `[0]` is the primary/default in-game language: all UI text,
  dialogue, menus, subtitles, and in-world text are authored in it. Each extra
  entry is a localization target — build the game localization-ready and, once
  playable, run `/localize` to populate that language's string table. A
  single-entry run just ships `GAME_LANGS[0]`.
- **DOCS_LANG = 简体中文** — the language every generated *project document*
  is written in: GDDs, art bible, ADRs, architecture, UX specs, review and
  playtest reports, the decision log, and the return report. This is the
  language *you* read, and it is independent of the game's own language.
- **ENGINE = Godot** (default location: the project root directory; if Godot
  is not present there, download it to that path) — the engine to configure
  when the project has none set. This location note applies only to the Godot
  default; when `ENGINE` is overridden with another engine, it no longer
  applies. Passed to `/setup-engine`. If an engine is already configured in
  `.studio/technical-preferences.md`, the run respects it; otherwise it
  configures `ENGINE`. Godot is the default because its 2D pipeline, headless
  mode, and export tooling give the fastest unattended iteration.
- **Web delivery is out of scope for this pipeline.** Producing a browser build,
  and the font packaging a browser build may require, belongs to the standalone
  `/web-export` skill. This pipeline targets a build that runs on the local
  machine: it does not bundle browser-specific assets, serve a web build, or
  verify one. When the user wants a Web build, run `/web-export` after this
  pipeline finishes.
- **TARGET_PLATFORMS = [Desktop, Web]** — the platforms this game ships on.
  Element `[0]` is the **primary** platform: it is what every build and
  verification step in this pipeline targets, and the local machine is both the
  development and the verification environment. Later entries are **export
  targets** — the project must stay exportable to them (no desktop-only
  assumptions baked into gameplay code), but this pipeline does not build or
  verify them. Browser packaging, and the font work a browser build may need,
  belongs to `/web-export`. Passed to `/setup-engine` as the platform answer.
  **The `Web` entry includes mobile browsers** — the game must be playable on a
  phone browser, so the Web export is a genuinely supported surface, not a
  courtesy build: touch-playable, correctly scaled at phone aspect ratios, and
  small enough for a phone to realistically download. Verifying it means testing
  at a **phone viewport with touch**, not only in a desktop browser window.
- **DIMENSION = 2D** — `2D` | `3D` | `both`. Decides the engine's scene and
  render setup, the art pipeline, and what a performance profile even means.
  Passed to `/setup-engine` as the "what kind of game" answer.
  **Consistency check:** `3D` or `both` is **incompatible** with
  `ART_METHOD = svg` — an SVG→PNG sprite pipeline is 2D-only. If the two
  conflict, stop and resolve it before building anything; never produce a
  mismatched pipeline silently.
- **DEV_LANGUAGE = GDScript** — the language the game is written in. For
  `ENGINE == Godot`: `GDScript` | `C#` | `both`. Default `GDScript` — it is
  Godot-native, iterates fastest, and needs no .NET SDK, which keeps an
  unattended run simple (`both` is an advanced setup requiring the .NET SDK
  alongside Godot). For non-Godot engines use that engine's primary language
  (Unity → C#, Unreal → C++/Blueprint) and record it.
  `/setup-engine` normally **blocks** on this question — it asks which language
  to use *before* showing the proposed Technology Stack — but an engine argument
  skips that, so this constant is the answer. **The choice propagates widely:**
  it sets the coding standards, naming conventions, specialist-agent routing and
  file-extension routing in `technical-preferences.md`, and it determines which
  test framework is even usable (GUT is GDScript-only). Choose once, record it,
  and keep every later step consistent with it.
- **PHYSICS_BACKEND = jolt** — which physics backend to configure. When
  `ENGINE == Godot` and the game is `3D` or `both`, use **Jolt** (Godot's default
  3D physics since 4.6). For a pure-2D project the choice does not arise —
  Godot's 2D physics is separate — but **record that fact in
  `technical-preferences.md` instead of leaving the field blank**. For non-Godot
  engines use the engine's own default. Either way the value is recorded, never
  left as `[TO BE CONFIGURED]`.
- **PRIMARY_INPUT = keyboard+touch** — the dominant input method(s), passed to
  `/setup-engine` as given. **This is a constraint, not a label:** with
  keyboard+touch as primary, no core mechanic may require a mouse — a
  cursor-driven verb (drag, aim, place-at-pointer) is out of spec and must be
  redesigned, or this constant overridden. Gamepad support is not set here;
  derive it from `TARGET_PLATFORMS` using `/setup-engine`'s own mapping table.
- **TOUCH_SUPPORT = full** — whether the game is fully playable by touch. `full`
  whenever touch is a primary input; otherwise `partial` or `none`.
- **PERF_BUDGET = none** — whether this run imposes performance budgets
  (framerate target, frame budget, draw calls, memory ceiling). `none` (default)
  imposes no budget and assumes no upper bound on the player's hardware: do not
  design around, cut content for, or gate any step on performance. `defaults`
  writes `/setup-engine`'s standard budgets and treats them as goals.
  **`none` does not mean "never measure".** A game that visibly stutters is
  still a defect — it is a bug to fix, not a budget to miss. Keep performance
  evidence in the Test Loop either way; just never let a budget block the run.
  **Conflict to watch:** when `TARGET_PLATFORMS` includes `Web` and mobile
  browsers are in scope, the weakest supported target is a phone — so "no
  budget" **cannot** mean "never checked on a phone". At minimum, observe the
  game on a phone-class viewport/device and confirm it is not unplayable; if it
  is, that is a bug to fix under the debug discipline, not an accepted
  trade-off.
- **RUN_MODE = native** — how the running game is driven and observed. `native`
  = run the built game on the local machine (a window is fine; it may flash
  briefly). Logic and balance are verified by headless assertion runs; visuals
  and feel by native frame capture. **No browser and no browser-automation skill
  is required by this pipeline.**
- **NATIVE_CAPTURE = movie** — how visual evidence is produced: run the game
  windowed with frame-sequence recording (Godot: `--write-movie <dir>/frame.png
  --fixed-fps <n> --quit-after <frames>`). Frames land on disk directly, with no
  tiling artifacts and no base64 round-trip. **A headless run cannot capture
  frames** — it uses a dummy renderer — so capture always needs a real window.
- **ART_METHOD = svg** — how art assets are actually produced. Default is a
  self-contained, no-image-model pipeline:
  - `svg` (default) — for each asset spec: (1) keep the AI-generation prompt in
    the spec for later human upgrade; (2) **delegate the drawing to the
    `svg-artist` subagent** — the main agent must not hand-author art. Invoke it
    like a drawing engine by passing **the prompt file's path** (plus the art
    bible path and an optional reference-image path) and nothing else: the agent
    reads the prompt itself and derives its output location from the
    prompt's directory and basename (the SVG and the raster land beside the
    prompt), running its own draw → rasterize → look → fix
    loop.
    **The prompt path must already exist** — produce it with `/asset-spec` first;
    a missing prompt file is a hard error, never a licence to draw anyway; (3) **rasterize** the SVG to PNG/JPG
    at the spec's dimensions with a **local** SVG rasterizer (e.g. a Python SVG
    library, `rsvg-convert`, or `Inkscape`). Rasterization is a local build step
    and must not depend on a browser.  (4) **convert to an engine asset** — only
    if the format isn't already PNG/JPG/SVG (most engines, e.g. Godot, import those natively, so
    usually skip this step; convert only when the engine needs a specialized
    texture/atlas format); (5) **visually check** the raster per `VISION`
    (`native`
    reads the image directly, `mcp` reads via the vision MCP, `auto` probes native
    first then MCP) and iterate the SVG until it matches the spec. A missing vision
    capability is a **blocking** error — do not silently skip; log `blocked` and stop
    the art sub-flow until vision is available.
    No external image model required;
    the game ships with real (vector-derived) art, not placeholders.
  - `generate` — run each spec's prompt through an image-generation tool/MCP
    instead of drawing SVG, then `/asset-audit` and advance the manifest to
    `Done`. Use this when a real image model is wired in and you want
    model-produced art over vector art.
- **VISION = auto|native|mcp** — how the run sees images. Do not let the model guess. The value here is the authority; there is no "if it has vision" self-test.
  - `auto` (default) — probe once at startup: try native image read first (direct `Read` of image files / captured frames); if unavailable, try the vision MCP. If neither exists, this is a **blocking** error — log `blocked` and stop the art/playtest sub-flow; do not degrade silently.
  - `native` — force direct image read. If the host cannot read images, log `blocked` as a hard error; do not silently skip visual checks.
  - `mcp` — force the vision MCP path (e.g. `view_image` / `read_image` tools). If the MCP is absent, log `blocked` as a hard error.
  Vision is **required** — a game without visual verification is not shippable. There is no `none` mode.
- **REVIEW_MODE = full** — strictest: director review per major artifact
  (`/gate-check`). `lean` runs it once at Polish only; `solo` skips gate
  reviews entirely (fastest, riskiest — use only when explicitly requested).
  Only overrides `production/review-mode.txt` when explicitly passed;
  otherwise respect the existing file.
- **MAX_ROUNDS = INF** — no cap on adversarial review-loop rounds (see that
  subsection). The loop stops ONLY on the quality gate (total > 9 AND
  真实可玩性 ≥ 9). Never invent a round limit.
- **SCORE_THRESHOLD = 9** — overall score (0–10) that ends the adversarial
  review loop, combined with the `真实可玩性 ≥ 9` hard gate.
- **TESTING = native** — `native` = run the built game on the local machine and
  capture evidence from it (rule 2 in full), backed by headless assertion runs
  for logic. Never choose `off`.
- **RESUME = auto** — resume an interrupted run when state exists; `fresh`
  forces a new run; `resume` forces continuing.

## State & Heartbeat

The run's live state is visible in `production/auto-game-in-sleep/state.json`.
If the file does not exist, this skill creates it on first entry (Phase 0);
otherwise the skill reads and resumes from it. Never store live values like
`current_phase/current_step/last_seen` in `AGENTS.md` — the anti-compression
anchor there (`<!-- GAME-STUDIOS:BEGIN -->`, injected by the
`game-studios-init` skill) holds only
static instructions and pointers; `state.json` (plus `journal.md`) is the truth.

Heartbeat discipline — the FIRST action of every pipeline step:

1. Update `state.json` with `current_phase`, `current_step`, an ISO-8601
   `last_seen`, and `next` (the concrete next action).
2. Append a self-contained entry to `journal.md` (what was attempted, what is
   next, which paths matter) so a compacted session can resume from the journal
   plus `state.json` alone.
3. Journal entries must be self-contained; evidence paths in `state.json`
   `steps[]` must be review/test reports or catalog artifact checks — a step is
   `done` when the executor finished, `accepted` only when evidence passes.

On resume, the Recovery Protocol in the `AGENTS.md` anchor (re-read this
`SKILL.md` first, then `state.json`, then `journal.md`) determines the first
non-`accepted` step and re-verifies any `done` without evidence.

## Language

Two independent language settings — do not conflate them:

- **Game content** (UI strings, dialogue, menus, subtitles, in-world text) is
  authored in `GAME_LANGS[0]`. Extra entries are localization targets: keep
  all strings in external string tables (never hardcoded in scenes/scripts),
  and once the game is playable, run `/localize` for each additional language
  to populate its table. A single-language run ships only `GAME_LANGS[0]`.
- **Project documents** (GDDs, art bible, ADRs, architecture, UX specs, review
  and playtest reports, the decision log, and the return report) are written in
  `DOCS_LANG` — the language *you* read. This is independent of the game's
  language: a Japanese game can sit on top of Chinese dev docs.

Discipline:

- Never hardcode in-game text in scenes or scripts — it must stay localizable,
  because `GAME_LANGS` may name more than one language.
- Dev docs are always in `DOCS_LANG`, never in the game's language.
- If `GAME_LANGS` has more than one entry, add a localization pass to the
  Release phase: after `/launch-checklist`, run `/localize` once per extra
  language, then re-run the relevant test checkpoint to confirm no broken strings.

## The Five Behavior Rules

These rules exist to fix the five known failure modes of a manual run. They
take precedence over any other skill's instructions.

### 1. Never block on a question (Decision Protocol)

You have no user. Every point where a workflow skill says *"use AskUserQuestion"*,
*"wait for the user's response"*, *"do not proceed until they respond"*,
*"confirm before proceeding"*, or *"never auto-run the next skill"* is
**suspended**. Instead:

1. **Answer from the record first.** Consult, in priority order:
   `design/gdd/game-concept.md` (pillars + scope tier) → the relevant system
   GDD → accepted ADRs / `docs/architecture/control-manifest.md` → the art
   bible. The consistent answer is almost always already written down.
2. **If the record doesn't answer it, decide as the studio would.** Pick the
   option that best serves the concept's pillars, the target scope tier, and
  standard game-development practice. Prefer the option that increases
  player-facing quality over the option that saves effort — except when it
  risks leaving the game incomplete (see rule 5).
3. **Log every decision** in `production/auto-game-in-sleep/decisions.md`:

   ```markdown
   ## [2026-08-28 02:14] design-system / movement — COYOTE_TIME = 0.1s
   Context: GDD left the coyote-time window as a tuning knob.
   Options considered: 0.08 / 0.1 / 0.15
   Chose: 0.1s — industry-standard feel for a precision platformer (pillar 2: "tight control").
   Override: delete this entry, edit design/gdd/movement-system.md §Formulas, re-run /design-system retrofit.
   ```

4. **Ready means execute.** Finishing preparation and then asking "should I
   proceed?" is the stall this rule forbids. Resolve routine ambiguity
   yourself, act, and log the decision (step 3) so it is auditable.
5. **Never call AskUserQuestion. Never stop to wait.** The `Do not proceed`
   instructions of other skills do not apply. If a skill's next action is
   genuinely destructive or irreversible (deleting user content outside
   `production/auto-game-in-sleep/`, publishing, force-pushing), do not do
   it — log it to the blocked list (rule 5) and route around it. Autonomy
   removes needless pauses, not deliberate ones: those two cases are the
   only load-bearing human gates in a run.

### 2. Test the running game yourself

"Code compiles" is not "the game works". At every checkpoint listed in the
Test Loop below, you produce a build, run it on the local machine, and observe
it yourself — logic via headless assertion runs, visuals and feel via native
frame capture. No browser is involved. Details in **The Test Loop**.

### 3. Chain the pipeline — never stop between workflows

A workflow completing is not a stopping point. The instant one step's artifact
exists and its gate accepts it, the next step in the pipeline starts — same
session, no summary-and-stop. The full ordered chain is in **The Pipeline**
below; `${CLAUDE_PLUGIN_ROOT}/docs/workflow-catalog.yaml` is the source of truth for
completion checks. The only legitimate ways a run moves from step X to "stop"
are: the run is genuinely blocked (wrap up) or all steps complete (wrap up).

### 4. Build the full game, not the minimal one

The scope of record is the **full / complete tier** declared in
`design/gdd/game-concept.md` (or, if the concept predates tiers, everything
the systems index lists as MVP + the content counts in the GDDs). Never
substitute a smaller game because no one stopped you. **Complete means proven
in the running build**: every GDD acceptance item MUST have Test Loop evidence
(screenshot sequence + log) showing it working — a feature "implemented" with
no evidence is NOT implemented.

- The MVP tier (if defined) is a **milestone on the way** — first playable,
  then keep building. Reaching it is worth a journal entry, not a stop.
- Forbidden shortcuts: dropping systems from the systems index, replacing a
  GDD-specified feature with a placeholder and moving on, shipping fewer
  levels/enemies/items/content than the GDD states, skipping audio or menus
  "for now".
- If the concept itself is tiny (the user asked for a jam-size game), the
  full tier IS the small game — build it completely, then polish it deeply.
  Polishing a small game fully beats half-finishing a big one.

### 5. Run to completion, not to a clock

There is no time budget and no round budget. Keep working through the pipeline
until it is complete or genuinely blocked — see Wrap-Up for the only
legitimate stop conditions. Do not invent a duration limit, a round cap, or a
stale cutoff, and do not treat "the user is away" as a reason to rush or cut
scope. **Complete means evidenced**: every step MUST reach `accepted` with its
evidence path on file — a step merely executed, tested casually, or declared
"done" without evidence does NOT count as complete.

One non-negotiable prohibition:

- **Quality gates may say "not yet", never "forever".** A gate failing does
  not end the run — fix and re-test (rule 1's decision protocol applies to
  how). Only full completion or a genuine block ends work.

Blocked items never stop the run: if a single problem survives the debug
discipline (see Test Loop), or a required external resource is missing
(engine binary, export templates), record it in the
**Blocked List** in `state.json`, apply the best fallback, and keep moving.
Only wrap up early when progress is genuinely impossible — and say so honestly.

---

## Phase 0 — Resume or Start

Read `production/auto-game-in-sleep/state.json` if it exists (respect the
`RESUME` constant).

- **Exists and `status: "running"`** — resume: verify every step recorded
  `done` but not `accepted` (see state schema below) by re-running its
  acceptance check — an executor finishing is not evidence. Continue at the
  first non-accepted step. Journal one line: `RESUMED at <step>`.
- **Exists and `status: "done"`/`"wrapped"`** — start a fresh run (archive
  the old run dir into `production/auto-game-in-sleep/archive-<date>/` first).
- **Missing** — new run. Create the directory and initial `state.json`:

```json
{
  "status": "running",
  "started_at": "<ISO timestamp>",
  "last_seen": "<ISO timestamp>",
  "current_phase": "concept",
  "current_step": "bootstrap",
  "mvp_milestone": false,
  "iterations": 0,
  "stale_count": 0,
  "blocked": [],
  "steps": []
}
```

`steps` records per-step progress — **`done` is not `accepted`**:

```json
{ "id": "design-system-movement", "status": "accepted",
  "evidence": "production/reviews/design-review-movement.md" }
```

- `done` — the executor finished writing the artifact. Set on completion.
- `accepted` — the step's gate passed and evidence exists: a review report,
  a passing test record, or the catalog's artifact check matching. **Never
  mark `accepted` on your own say-so** — record the evidence path in the
  step. Machine-checkable completion (file exists, export exit code 0, zero
  console errors, test suite green) is safe to self-judge; quality verdicts
  are not (see Reviewer Independence in the Iteration Loop).

Also create `decisions.md` and `journal.md` with a
`# Run started <date> <time>` header.

Then detect the project stage the same way `/project-stage-detect` does:
engine configured? concept exists? GDDs? ADRs? stories? playable code? This
determines where in The Pipeline you enter. Write a TodoWrite list mirroring
the remaining pipeline steps and keep it updated throughout the run.

**Heartbeat discipline**: the *first action* of every step is to update
`state.json` — `last_seen`, `current_phase`, `current_step` — *before* any
work that might hang or crash. If the session dies mid-run, `last_seen`
tells the morning user exactly where it died, and the post-compact /
session-start hooks point the next session here. Journal entries must be
self-contained (what was attempted, what's next, which paths matter) so a
context-compacted or restarted session can resume from the journal alone.

---

## Phase 1 — Bootstrap (only for a fresh project)

If the project has no concept yet, you are the studio today. Do, in order:

1. **Concept**: run the `/brainstorm` process yourself (no user interview):
   choose a concept that is ambitious but shippable — one
   strong core verb, 2–3 systems deep, genre with proven fun patterns.
   Write `design/gdd/game-concept.md` with an explicit scope tier table and
   mark the **full tier** as the target. Announce it in the journal.
2. **Review mode**: if `production/review-mode.txt` is absent, write `lean`
   (directors at phase gates only — quality control without per-skill pauses).
3. **Stage file**: write the current stage to `production/stage.txt`.
4. Continue into The Pipeline at the Concept phase.

If the project already has artifacts, skip whatever is done (verified by the
catalog's artifact checks) and enter the pipeline at the first incomplete step.

---

## The Pipeline

Execute top to bottom. `→` marks the acceptance evidence (from
`workflow-catalog.yaml` — use its glob/pattern checks; the list below is the
order and the repeat rules). Invoke each step's skill via the Skill tool and
follow its process, with interactive pauses suspended per rule 1.

**Concept**
1. `/setup-engine [ENGINE]` → `.studio/technical-preferences.md` names a real engine. When none is configured, configure `ENGINE` (default Godot); if one is already set, respect it.
   **Passing an engine argument skips `/setup-engine`'s guided questions, so this run must supply those answers explicitly** — `TARGET_PLATFORMS` (platform), `DIMENSION` (2D/3D/both), `DEV_LANGUAGE`, `PHYSICS_BACKEND`, `PRIMARY_INPUT`, `TOUCH_SUPPORT` and `PERF_BUDGET` — and let `/setup-engine` derive gamepad support from the platform with its own mapping table.
   Acceptance: `technical-preferences.md` names a real engine, records **all** of the above plus a concrete `Rendering` and `Physics` entry, and the local build boots. **A `[TO BE CONFIGURED]` left in Engine & Language or Input & Platform is a failure of this step** — nothing later in the pipeline will fill it. Font packaging for a browser build is **not** verified here; that belongs to `/web-export`.
2. Concept document exists (done in bootstrap, or `/brainstorm` for an existing vague project) → `design/gdd/game-concept.md`
3. `/design-review design/gdd/game-concept.md` → fix issues it can fix itself; log anything arguable
4. `/art-bible` → `design/art/art-bible.md`
5. `/map-systems` → `design/gdd/systems-index.md`

**Systems Design** (repeat per system)
6. `/design-system [system]` for every MVP system in the index → GDD per system
7. `/design-review [gdd]` per GDD → no unresolved MAJOR REVISION verdicts
8. `/review-all-gdds` → cross-review report written
9. `/consistency-check` → contradictions fixed

**Technical Setup**
10. `/create-architecture` → `docs/architecture/architecture.md`
11. `/architecture-decision` until ≥3 Foundation ADRs accepted → `docs/architecture/adr-*.md`
12. `/architecture-review` → review report, issues fixed
13. `/create-control-manifest` → `docs/architecture/control-manifest.md`
14. Accessibility requirements committed → `design/accessibility-requirements.md`

**Pre-Production**
15. `/asset-spec` inventory + per-asset specs → `design/assets/entity-inventory.md`, `asset-manifest.md` (skip if visually trivial — journal the skip)
    **Pipeline addition to this step:** beyond what `/asset-spec` produces on its
    own, **this run also writes each visual asset's generation prompt as its own
    file**, `<basename>.prompt.md`, in the directory where that asset's art will
    live. The spec and the manifest record that **path**, never a second copy of
    the text, so the two cannot drift apart. Audio assets are exempt —
    descriptions, not prompts.

16. `/ux-design` for ≥3 key screens (main menu, gameplay HUD, pause) → `design/ux/*.md`
    **Pipeline addition to this step:** every screen's UX spec must carry a
    **surface inventory** — each visible surface it draws (background, panels,
    frames, dividers, decorative elements, emblems) together with the asset that
    backs it. A surface with no backing asset is either promoted into the asset
    list or explicitly declared per-frame; a surface promoted here gets its own
    `<basename>.prompt.md` at this step, exactly like the step 15 assets, so the
    batch below can produce it. This is what gets art into the manifest *before*
    production, so it cannot be forgotten downstream; a screen that declares no
    surfaces is an incomplete spec, not a simple screen. This inventory is part
    of the **opening batch**, not a closed contract — later steps are expected
    to extend it (see the empowerment clause under Asset production).
17. `/ux-review` → issues fixed

    **Asset production** (driven by `ART_METHOD`) — runs **after `/ux-review`**,
    so the opening batch is built last among the pre-production art steps: it
    covers the entity assets specified at step 15 **and** the screen surfaces
    promoted at step 16. Producing it before step 16 would structurally
    guarantee that menus, HUD chrome and other screen surfaces are missing from
    the batch — the exact gap this pipeline exists to remove.

    **Default for every visible surface: it is an asset.** Unless a thing is
    generated per-frame from simulation state, its pixels must come from a file
    this pipeline produced. A menu or results background, a panel, a frame, a
    divider, a title, a decoration and an ending illustration are assets exactly
    as a sprite is. Code may transform an asset — move, scale, fade, tint,
    rotate — but code may not be the reason the pixels exist. The one standing
    exception is the per-frame family: particles, force-field rings, trails,
    screen shake, damage numbers. Using code **outside** that family requires a
    stated reason in the run journal; it is never a silent default — and a
    recorded reason is **sufficient** (see the 界面美观性 cap in The Adversarial
    Review Loop: a recorded reason excludes that surface from the coverage
    ratio, with no further adjudication).

    **The opening asset list is a starting point, not a ceiling — downstream has
    standing authority to add art.** Whenever any later step (a production
    story, `/team-polish`, a playtest, the adversarial review, or simply
    noticing a bare surface) finds something that wants art and does not have
    it, that step **adds the asset itself, following exactly the same
    `ART_METHOD` path the opening batch used** — never invent a second pipeline
    for late additions:
    - `svg` — write the asset's `<basename>.prompt.md`, draw it via the
      `svg-artist` subagent, rasterize locally, visually check;
    - `generate` — run the new asset's prompt through the same image tool/MCP
      the opening batch used.
    Then record it in the manifest like any other asset. **No permission is
    required and the original list is not a limit.** Adding art is never "scope
    creep" here; it is the point of the run. Conversely, a step must not skip art
    because "it wasn't in the inventory" — an incomplete list is an invitation
    to extend it, not a licence to leave a surface bare.
    - `svg` (default) — each asset keeps an AI prompt at
      `<basename>.prompt.md`, **produced by this run as its own file** — at
      step 15 for entity assets, at step 16 for the screen surfaces the UX
      inventories promote, in the same directory as the art it describes. The manifest records the
      prompt's *path*, not its text, so the two cannot drift. The prompt is a
      prerequisite for drawing, not an afterthought:
      **draw via the `svg-artist` subagent**, invoked per asset like a drawing
      engine — pass the **prompt file path** (not the prompt text), the art
      bible path, and an optional reference image; the agent derives its output
      from the basename (source and raster beside the prompt).
      Then:
      1. **Rasterize** the SVG to PNG/JPG at the spec's dimensions with a
         **local** SVG rasterizer (e.g. a Python SVG library, `rsvg-convert`,
         or `Inkscape`). The raster is also the visual-check artifact.
         Rasterization is a local build step and must not depend on a browser.
      2. **Convert to an engine asset** — only if the format isn't already
         PNG/JPG/SVG (most engines, e.g. Godot, import those natively, so usually omit this step;
         convert only when the engine needs a specialized texture/atlas format).
      3. **Visually check** per `VISION` (`native` reads directly, `mcp` via the
         vision MCP, `auto` probes native first then MCP). **Iterate the SVG**
         until it matches the spec. If vision is unavailable, do not skip —
         log `blocked` and stop this asset’s sub-flow.
    - `generate` — run each spec's prompt through an image-generation tool/MCP,
      write the result into `assets/`, then `/asset-audit` and advance the
      manifest to `Done`.

18. Prototype: only if the core mechanic is genuinely high-risk (journal the decision either way)
19. `/create-epics layer: foundation`, then `layer: core` (+ feature layers) → `production/epics/*/EPIC.md`
20. `/create-stories [epic]` per epic → story files
21. `/test-setup` → test scaffold (engine test framework)
22. `/sprint-plan` → first sprint

**Production** — loop until every story is Done:
23. For the current sprint, for each ready story in priority order:
    `/story-readiness` (quick check) → `/dev-story [story-path]` (delegate
    implementation to the matching specialist agent where the skill says so)
    → `/code-review` → `/story-done`
24. End of sprint: `/smoke-check` → **must PASS** (this is also Test Loop
    checkpoint B) → `/retrospective` → next `/sprint-plan`
25. When the last story closes: journal `MVP milestone reached` if not yet,
    and if the full tier needs more sprints, plan and run them (rule 4)

**Polish**
26. `/perf-profile`, `/balance-check`, `/asset-audit` → fixes applied
    **Pipeline addition to this step — art completeness.** `/asset-audit` does
    not check this by itself, so verify it here: every **visual** asset in the
    manifest must have its prompt at `<basename>.prompt.md` **and** whatever
    raster `ART_METHOD` produces, in the same directory — for `svg` that is the
    pair `<basename>.svg` + `<basename>.png`; for `generate` it is the prompt
    plus the generated raster. A missing prompt is a
    **non-compliance, not a warning** — it is the only record a human can use to
    regenerate the asset later, and the prerequisite handed to the asset
    producer. Report the count and list every offender.
27. Playtest ×3 yourself as the main agent against the locally running build
    (MUST be done by the main agent itself, driven with real input through the
    scripted input seam; follow a real-input black-box method — perform actual
    actions, capture a frame sequence per observation, evidence on file).
    Each session MUST cover: every MVP system to a real outcome (entering a
    screen is NOT completion), every ending type at least once, and a written
    playtest report on file. A session without full-system coverage plus all
    endings is NOT a pass. See Test Loop checkpoint C for the bar.
28. `/team-polish` → coordinated polish pass
29. **Adversarial review loop** — independent scored review that drives the
    game to a quality bar (see [The Adversarial Review Loop](#the-adversarial-review-loop)).
    Gated by `REVIEW_MODE`: `solo` skips it; `lean` runs it once here; `full`
    runs it per major artifact.

**Release**
30. `/release-checklist` → items fixed or logged
31. `/patch-notes` and `/changelog` → docs written
32. `/launch-checklist` → final gate

Then Wrap-Up.

**Phase gates**: at each phase transition run `/gate-check`. Its verdicts are
advisory: fix CRITICAL findings, log MAJOR ones to the blocked list with a
note, and proceed.

---

## The Test Loop

Run at these checkpoints:
- **A — first playable**: after the vertical-slice moment / first playable build exists
- **B — every sprint end**: together with `/smoke-check`
- **C — polish phase**: the 3 playtest sessions, each played by the main agent
  itself against the locally running build. A session PASSES only with full
  MVP-system coverage, all endings triggered, and the report on file —
  entering the game is not passing.
  Sessions must reach late content by **natural progression**, never by
  teleporting game state. A state-jump is acceptable only to inspect one
  specific late-game feature, and must be labelled as such in the report.
  Checkpoint C is NOT complete until 3 PASS reports exist.
- **D — before wrap-up**: final verification of the last build

Procedure per checkpoint (the `ENGINE=Godot`, `TARGET_PLATFORMS[0]=Desktop` path;
adapt the engine binary when it differs):

1. **Headless boot smoke** — catches script/runtime errors cheaply:
   `godot --headless --path . --quit-after 300` (300 frames). Any error or
   script failure in output = bug. Fix before continuing.
   Redirect output to a timestamped log: `test-runs/<checkpoint>-<YYYYMMDD-HHMMSS>.boot.log`;
   judge state by reading the log tail.
2. **Headless assertion run** — the project's own logic tests must pass, and they
   must include a **scene-load smoke**: assert that the rendering scenes load,
   instantiate, and their scripts compile. Assertions that only drive pure-logic
   objects will not catch a parse error in a rendering script — and such an error
   can survive all the way into a shipped build.
3. **Build** — build the desktop target, output redirected to
   `test-runs/<checkpoint>-<YYYYMMDD-HHMMSS>.export.log`.
4. **Play it — natively, with scripted input.** Unattended play must be
   reproducible, so the game needs a **scripted input seam** (a flag making the
   game read input from a script rather than the OS); synthesized OS input is
   fragile and depends on window focus. Then:
   - run windowed with **frame-sequence capture** and a **fixed timestep that is
     decoupled from wall-clock time** (Godot: `--fixed-fps <n> --disable-vsync`,
     optionally `--write-movie <dir>/frame.png --quit-after <frames>`).
     Decoupling is essential: with real-time pacing the game keeps running while
     you think between tool calls, which silently invalidates observations —
     "the player died in 12 seconds" may only mean nobody was playing.
   - drive the core loop: enter the game, exercise every MVP system to a real
     outcome, pause/resume, reach every ending, restart
   - capture a **frame sequence** per item (before / action / after — one frame
     proves presence, never transition), plus the run log
   - a headless run **cannot** produce frames (it uses a dummy renderer);
     visuals require a window
5. **Record** — write `production/auto-game-in-sleep/test-runs/<checkpoint>-<date>.md`
   with frame paths, logs, what worked, bug list. File bugs via `/bug-report`
   (they feed the Production loop) or fix trivial ones immediately.
6. **Re-test after fixes** — a checkpoint only passes when a clean run has
   zero errors in the logs and the core loop completes.

Fallback ladder when the engine binary is unavailable: headless assertion runs +
engine screenshots are the only level available — state plainly in the test
record which level of verification was achieved.

**Debug discipline — restart beats patching.** A broken build is your
problem, not the user's. After 1–2 targeted patches fail on the same
failure, treat "delete the current attempt and reimplement it cleanly from
the GDD/ADR contract" as a normal, often preferable option — patched-code
archaeology is how attempts rot. Escalate to the Blocked List only when the
**contract** is in question (the GDD/ADR is missing, ambiguous, or looks
wrong) — "the design may be wrong" goes in the morning report; "the build is
broken" does not. A restart may delete only the current attempt's own
scaffolding (code it wrote, configs it generated, its build artifacts) —
never GDDs, ADRs, story files, the journal, state.json, or test records.
Two clean reimplementations failing the same way = the contract or
environment is the problem: block and route around.

---

## The Iteration Loop

After the full-tier game is playable and Production is complete, iterate:

1. Run Test Loop checkpoint C as a fresh-eyes playtest played by the main agent
   itself (same MUST bar: full MVP-system coverage, all endings, report on
   file). Evaluate against:
   - every GDD's **Acceptance Criteria** (the real quality bar)
   - game feel: input responsiveness, feedback/juice on core actions, clarity
     of goals, difficulty curve shape
   - first 60 seconds: can a new player understand what to do without text?
2. List the top 3–5 improvements by player-impact. Implement them.
3. Re-run the relevant test. Repeat.
4. **Exit when all true**: all GDD acceptance criteria verified in the running
   game · latest smoke-check PASS · 3 PASS playtest reports on file (full-system
   coverage + all endings each) · zero open
   critical/major bugs · 60s continuous native play with no errors.

**Reviewer independence** — the agent that wrote the code does not accept
its own quality. Machine-checkable completion (build exits 0, zero console
errors, tests green) may be self-judged. Quality verdicts — playtest
assessments, polish adequacy, the final COMPLETE — must come from a reviewer
who didn't produce the work: spawn the **`playtest-reviewer`** subagent.

**The reviewer produces its own evidence.** Invoke it with a small handoff —
project root · engine and binary · build entry · the scripted-input seam's name
and how to enable it · acceptance-criteria paths · round number and output path
— and nothing else. The method, evidence bar, rubric and report format live in
`${CLAUDE_PLUGIN_ROOT}/agents/playtest-reviewer.md`, which you pass **by reference, never
restated**. Because the build runs **natively**, the reviewer needs only shell
access to build, run and capture the game itself, so it must do exactly that and
base its verdict on what it observed. Your own captures may be passed as context
but are never sufficient on their own. The reviewer is **read-only on source** —
it has no Edit tool and writes only its own report.

If subagents are unavailable, cold-review: new context, run the build
yourself, and follow `${CLAUDE_PLUGIN_ROOT}/agents/playtest-reviewer.md` as your method and
rubric. The implementer's own "looks good to me" is never evidence.

**Stall detection — count, don't vibe.** After each iteration record the
number of **new findings** (bugs fixed, acceptance criteria newly verified,
improvements landed — concrete countable events, not "felt productive") in
`state.json` (`iterations`, `stale_count`). Consecutive zero-finding
iterations accumulate `stale_count` (diagnostic only — this loop has no
stale cutoff either):

- `stale_count ≥ 2` → **forced structural pivot**: the next iteration must
  change the frame, not tune inside it — a different system, or a different
  improvement category (feel / content / UX / audio / performance) than the
  ones already tried. Read the journal's tried directions first and pick one
  that differs.
- No stop on staleness here either: only full completion (exit criteria above)
  or genuine impossibility (see Wrap-Up) ends the iteration loop. Do not keep
  grinding the same frame against a wall — pivot, don't stop.

Avoid thrash: if an iteration makes the test result worse, revert it (keep the
diff in the journal) and pick a different improvement.

---

## The Adversarial Review Loop

A scored, evidence-gated challenge loop that pushes the game to a quality bar
before Wrap-Up. It is the studio's equivalent of a cross-model jury: an
independent reviewer subagent scores ONLY what it can verify by running the build itself, and
forces fixes until a threshold — the implementer never acquits its own work.

**Gating (`REVIEW_MODE`)**: `solo` skips the loop entirely; `lean` runs it once
at the Polish step above; `full` runs it per major artifact (per system GDD,
per sprint, per release gate). When skipped, journal it.

**No round cap in this loop.** `MAX_ROUNDS = INF` means exactly that: the loop
stops ONLY on the quality gate below. Rounds are cheap; shipping an unverified
game is not.

**One reviewer, all dimensions.** Spawn a single fresh-context
**`playtest-reviewer`** subagent (never the agent that wrote the code) to score
every dimension below and emit 意见 / 建议 / 疑问 / 缺件. Scoring from a single
rater keeps the dimensions comparable across rounds. The reviewer's method,
evidence bar, rubric anchors and output format live in
`${CLAUDE_PLUGIN_ROOT}/agents/playtest-reviewer.md` — that file is the single source; this skill
never restates them.

**Mechanism per round**

1. **Hand over a runnable build — not evidence.** Spawn `playtest-reviewer`
   with the six-field handoff: project root · engine and binary · build entry ·
   the scripted-input seam's name and how to enable it · acceptance-criteria
   paths · round number and output path. Your own captures may be passed as
   optional context, never as the basis of the score. A round whose reviewer
   never ran the build is recorded as FAIL (evidence not independently
   produced).
2. **The reviewer plays it itself and produces the evidence** — its own
   timestamped logs and its own BEFORE/ACTION/AFTER frame sequences per MVP
   system, per ending, and for pause/resume. Its full procedure, evidence bar,
   caps and report format are in `${CLAUDE_PLUGIN_ROOT}/agents/playtest-reviewer.md`; hand
   that file over **by reference** and do not paraphrase it into the prompt.
3. **Act on what it returns.** It writes its round pack to
   `production/auto-game-in-sleep/test-runs/review-<round>-by-reviewer.md`
   (意见 / 建议 / 疑问 / 缺件清单). Fill the 缺件 gaps by re-running the Test
   Loop FIRST, then implement the 建议. Update `state.json`: `iterations`,
   `stale_count`, and the `adversarial-review` step's `done`/`accepted` +
   evidence path.

**Scoring — six dimensions (each 0–10)**

Anchors, the Part A / Part B split (static: 完整度 / 新颖性 / 架构与可维护性;
from the reviewer's own run: 真实可玩性 / 界面美观性 / 动态体验) and the
completeness caps live in `${CLAUDE_PLUGIN_ROOT}/agents/playtest-reviewer.md`. This skill owns
**only the gate**, so the rubric has exactly one copy and cannot drift:

- **总分 = mean of the six dimension scores.**
- **Hard gate**: while `真实可玩性 < 9`, the loop MUST NOT stop — a high average
  that can't prove full playability from evidence is never accepted.
- **Stop when**: `总分 > SCORE_THRESHOLD` **and** `真实可玩性 ≥ 9`.
- No round cap (`MAX_ROUNDS = INF`).

**界面美观性 — the art cap, and the code-drawn escape hatch.** A screen whose
visible surfaces come only from code, flat fills or primitive shapes cannot
score above 4 — scored against the **art coverage ratio** (surfaces backed by an
asset ÷ all visible surfaces). Because the cap is a ratio rather than a list of
screens, it covers every screen including ones added later, with no new rule
needed, and "functional but plain" is not a passing look for this run.

**A recorded reason is enough.** If the run journal records a stated reason for
drawing a surface in code, that surface is excluded from the ratio — no reviewer
adjudication, no second review pass, no appeal. Reasons are recorded **before**
the round (the reviewer verifies an existing record, never a retroactive
excuse), and the reviewer reports how many surfaces it excluded, so a run that
excuses every surface is visible in the morning report instead of being argued
over inside the loop.

**Aggregate & termination**

- **总分 = mean of the 6 dimension scores.**
- **Hard gate**: while `真实可玩性 < 9`, the loop MUST NOT stop — a high average
  that can't prove full playability from evidence is never accepted.
- **Stop when**: `总分 > SCORE_THRESHOLD (9)` **and** `真实可玩性 ≥ 9`.
  No round cap applies to this loop (`MAX_ROUNDS = INF`).
- **Stale counter (this loop, count-only, never stops)**: a round with zero new
  findings increments `stale_count` for diagnostics; at ≥10 the round MUST
  change review angle (different dimension focus, different play path) but the
  loop continues. The generic iteration-loop ladder (≥2 pivot / ≥4 stop) does
  NOT govern this loop. Only the quality gate above — or genuine impossibility
  (see Wrap-Up) — ends the loop.
- On stop, record the final scores in the `adversarial-review` step as
  `accepted` (with the reviewer's own pack path) and carry them into the morning
  report's Quality bars section.

**Outputs per round (the reviewer writes)**

意见 / 建议 / 疑问 / 缺件清单 — their required contents are specified in
`${CLAUDE_PLUGIN_ROOT}/agents/playtest-reviewer.md`. If a 疑问 blocks acceptance, log it to the
blocked list / morning report for the human.

**Reuses (no new machinery)**

- *done≠accepted* — the loop step is `accepted` only with the score + evidence
  pack on file; "I fixed it" is not evidence.
- *reviewer independence* — fresh subagent, never the implementer; scores from
  its own run only, never from the main agent's claims or from reading code for
  the main agent's benefit.

## Wrap-Up

When the pipeline finishes, `stale_count` hits the ladder top, or progress
becomes impossible:

1. Ensure the last build in `build/` (or equivalent) is the best one; rebuild
   web if the fix loop changed anything. Kill background servers.
2. Update `state.json`: `status: "done"` (or `"blocked-early"`), steps with
   their done/accepted status and evidence, blocked list, iterations,
   `last_seen`.
3. Write `production/auto-game-in-sleep/morning-report.md`:

   ```markdown
   # Morning Report — <date>
   ## TL;DR
   <2–3 sentences: what exists now, is it playable, where>
   ## How to run it
   <exact command / file to open>
   ## What was produced
   <phases completed, stories closed, test runs, playtest reports — with paths>
   ## Quality bars
   <which acceptance criteria / gates PASSED, which did NOT — be exact. The
   run stopped because it completed or hit a stall, never because a clock ran out.>
   ## Decisions I made for you
   <top 5–10 from decisions.md, most consequential first — link the file>
   ## Bugs & known issues
   <open items from the blocked list and bug backlog>
   ## What I would do next
   <prioritized hand-off list>
   ```

4. Post the report path as the final message. **Verdict: COMPLETE** when a
   playable full-tier build exists and checkpoint D's independent review
   passed; otherwise PARTIAL with an explicit reason.

---

## Hard Rules (never violated, even on autopilot)

- Never `git push`, never force-anything in git, never delete user-authored
  content outside `production/auto-game-in-sleep/`. Commit locally as the
  workflow skills prescribe; publishing stays a human act.
- Never bypass the installed guard hooks (they exist to protect the machine);
  a hook denial is a signal to change approach, not to evade.
- Never mark a story or checkpoint `accepted` without recorded evidence
  (review report / test record / artifact check) — your own satisfaction is
  not evidence.
- Never reduce declared scope (rule 4) — cut only via a logged decision that
  keeps the game complete and coherent, and surface it prominently in the
  morning report.
- Stay inside the project directory for all writes.

---

## Edge Cases

- **Engine binary not found** (e.g. `godot` not on PATH): search common
  install locations; if truly absent, do the entire pipeline except build/test
  checkpoints, marking every Test Loop checkpoint as blocked with reason —
  design, code, and reviews still proceed.
- **Existing project mid-pipeline**: enter at the first step whose acceptance
  evidence is missing. Trust checks, not memory — verify each prior artifact.
- **Project has a concept but zero code and you must deliver a minimal-but-complete game**: skip to a
  compressed but complete pass: concept polish → map/design systems →
  architecture-lite → single epic → implement → test loop → report.
- **Test keeps failing on the same core loop**: apply the debug discipline
  (restart from contract after 2 failed patches). If the core loop is still
  broken after that, implement the fallback design from the GDD's edge cases,
  or descope that single feature via decision log; never leave the game
  unbootable.
- **User provided an idea as argument** (`/auto-game-in-sleep make a roguelike
  about gardening`): treat it as the brainstorm hint — build the concept
  around it.
- **Resume after crash/context loss**: state.json (`last_seen`, per-step
  done/accepted) + journal.md + the catalog artifact checks are the truth;
  redo only the current step.
- **A target is a phone browser**: the Web export must be touch-playable and
  phone-sized, not merely clean in a desktop browser window. Do not hand-roll
  touch controls — check the engine reference docs first (Godot 4.7 ships a
  built-in `VirtualJoystick` node, which is the cheap path). Treat payload size
  as a real constraint, because a phone downloads it, and verify at a phone
  viewport with touch: a passing desktop-browser check proves nothing here.
