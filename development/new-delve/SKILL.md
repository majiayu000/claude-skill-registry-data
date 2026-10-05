---
name: new-delve
description: Generate a complete playable Minecraft delve from a creative prompt — staged DSL authoring with validation-loop self-repair, deterministic compile, machine validation, joinable output. Use when the user asks to create/generate a new delve or campaign. Args = the creative prompt (theme one-liner or detailed brief).
metadata:
  requires_delvec: ">=1.0.0 <2.0.0"
---

# /new-delve — building a delve, end to end

This page is the spine: the three stops, the fourteen steps in order, the
standing constraints, and a pointer per step to the file that carries its body.
Read the pointer's file when you reach that step, and not before.

## Contents

- [Who runs this page, and what is not yours](#who-runs-this-page-and-what-is-not-yours)
- [What you are building](#what-you-are-building)
- [The shape of the run](#the-shape-of-the-run)
- [Hard rules](#hard-rules)
- [Init — build the toolchain before you author anything](#init--build-the-toolchain-before-you-author-anything)
- [Which placement model](#which-placement-model)
- [The steps](#the-steps)
- [Where each reference lives](#where-each-reference-lives)

## Who runs this page, and what is not yours

**You are the agent, and this page is your procedure.** The skill is the
generation front-end; Claude Code is the runtime that executes it, and building
a separate agent runtime is permanently out of scope (ADR-0012). Someone typed
`/delvewright:new-delve <prompt>`; that person is **the user** for the rest of
this page, and their prompt is a constraint set — what it pins down is honoured
verbatim, what it leaves open is yours to invent.

Every command below is yours to run and every document below is yours to write.
**Three things are not**, because they need a body in the game, a judgement that
is the user's to make, or their permission to touch something outside this
project. At each one you stop, hand over exactly what is needed, and **wait for
an answer**:

| where | what you hand the user | what you wait for |
|---|---|---|
| **Init I5** the client jar | the two ways it can reach the machine, download named as the default | which one — or the directory to copy from |
| **§4** the design gate | the design walkthrough — every scene, near view and far | an explicit yes |
| **§9** the walk | a running server, the connect line, and what to look for item by item | what they saw |

Stopping means: say what you have done, hand over the thing, say what you need
back, and **end your turn there**. Do not proceed on silence, do not substitute
your own judgement for the answer, and **never write anything that asserts a
step whose actor is the user actually happened** — a walk nobody walked and an
approval nobody gave are the two ways this pipeline produces a green run and a
delve no one has ever looked at.

§14 is also a hand-over, but nothing comes back: it ends the run. Anywhere else
the user *may* be offered a choice — which candidate piece, which frame — the
offer is optional and you proceed without it.

## What you are building

You author a delve as a set of **JSON documents**. `delvec` turns them into a
datapack and a world. You never write mcfunction, dialog files or datapack JSON,
and you never hand-edit an `.nbt` — everything the player meets is compiled from
the documents you wrote.

**A campaign lives under the working directory**, at `campaigns/<campaign-id>/`,
whatever that directory is: an empty one the user started Claude Code in, a
clone of the content repository, or a checkout of the engine itself. Read the
engine constitution at `"$DELVEWRIGHT_ENGINE/CLAUDE.md"` once Init has cloned
it; the forbidden zones apply in full. That file names its own other half,
`CLAUDE.local.md`, and tells whoever lacks it to say so and ask "before
improvising anything about dispatch, review, merge or staging". **You will not
have it** — it is gitignored on the operator's machine, so no clone can produce
it — **and this page improvises none of those four.** It stops at §4 and §9 and
hands those to the user; §14 hands over and ends. So record the absence in one
line and carry on with the run: the answer is the same every time, and the turn
spent asking comes out of the user's.

### Reference: turning a prompt into a campaign

A prompt is a **constraint set over the documents**: honour everything it pins
down — theme, specific levels, plot beats, NPCs, homages — and invent the rest.
Ask two or three clarifying questions only if the prompt is too thin to pick a
theme and a target length; otherwise proceed.

**A thin prompt is creative licence.** When a prompt pins down little — a
one-line theme, no detailed brief — treat it as a **showcase** brief and
deliberately exercise the breadth of what the engine supports, so that a
stranger playing the result discovers what it can do. Do not work from a written
feature list, which rots as the schema moves: **query the live schema**
(`delvec schema --stage all`) for the available verbs and effects, then aim to
include, wherever the story can carry them coherently: multi-area transport as a
narrative beat, flag-gated dialogue consequences, real props and set dressing,
at least one tuned combat or stealth encounter, narration beats, and varied NPC
presentation. **Coherence and pacing always win over feature count** — never
bolt on a mechanic the story cannot motivate.

**A detailed brief is the opposite**: honour exactly what it pins down and
showcase nothing extra.

**Every round changes only what was asked for.** A mechanics fix must not
incidentally rewrite story, staging or dialogue; an approved change that moves
the design updates `DESIGN.md` in the same commit; and every round ends with a
conformance review — diff the campaign's current behaviour against `DESIGN.md`
beat by beat and report any deviation nobody asked for instead of shipping it.
Drift found in review is restored to the design or escalated, never silently
kept.

## The shape of the run

Everything below happens in this order, and the order is not a suggestion — each
step needs something the step before it produced.

```
Init            every run: I0 · I1 · I1b, the pin check      ── §Init
                I1b exits 0 before any document is read or any
                subcommand is run; the rest of Init is run where
                I1b names it. STOP at Init I5 — the jar is the user's
  ↓
Decide          areas[] or a site plan — one campaign, one    ── §Which placement model
  ↓
 1  workspace   the campaign directory and its documents
 2  placement   world.json areas[]   OR   brief → graph → plan
 3  story       npcs · classes · quest-plan
 4  GATE        STOP — the design walkthrough, the user says yes
 5  content     quests · dialogue
 6  fmt         delvec fmt              ← every campaign, not optional
 7  analyze     analyze the quest graph
 8  build       build the datapack and the world
 8b cameras     one showcase camera per approved image
 9  the walk    STOP — the user walks the blockout, you wait
10  ladder      PackTest · bot · branch runs
11  chronicle   only when the plan declares branch_points
12  visual      the POV sequence, then the renders
13  detail      site-plan campaigns only, and only after the walk
14  hand over   storybook, staging gate, play commands
```

Two branches change what you do, and both are decided before step 1:

- **areas[] or a site plan.** A campaign has exactly one placement authority.
  See *Which placement model* below — it is the one decision that cannot be
  changed later without redoing step 2.
- **Do you already have approved reference art?** A campaign being re-made from
  an approved design carries its images in `campaigns/<id>/design/`. If that
  directory exists, you need no image provider and Init I7 is a read rather than
  a setup.

## Hard rules

They hold at every step by their nature, and nothing below repeats them.

- Persist the campaign documents before validation, not after — a crash must
  never lose the campaign.
- **Apply a ruling at the scope it was given.** If a wider rule seems right,
  propose it in one line and wait — generalizing a ruling is a design decision,
  not an inference to make silently. A one-beat pacing ruling read as a
  campaign-wide ceiling is a campaign nobody approved.
- **Unrequested change is a rejection cause on its own**, independent of whether
  the change is good. Author what the round asked for; anything else you believe
  the campaign needs is a proposal in the round summary.
- Every player-visible string in the campaign documents stays **English** —
  always. Other languages are sidecars. A brief written in Chinese still yields
  English documents; add a `zh-cn` sidecar only when localized in-game text is
  asked for.
- **Commit only canonically formatted JSON.** The last thing before any `git add`
  of a document or sidecar is `delvec fmt <campaign-dir>`; CI runs
  `delvec fmt --check`. A diff that rewrites a file nobody edited is the defect
  this closes.
- Homages: original text only. Cultural reference, never asset ingestion.
- If a mechanic the brief wants has no DSL verb, do NOT fake it with adjacent
  verbs silently — say what is missing and offer the closest authorable
  alternative. A change to the language itself is not made from inside a campaign.
- Never weaken a check, a test or a threshold to get green, and never reroll a
  seed. A red check is information. Fix the cause or escalate; escalating is
  success.

## Init — build the toolchain before you author anything

**Every run starts here, and a run on a machine that has run Init before is no
exception.** I0, I1 and **I1b** run first on every run; I1b compares the binary,
the engine tree and `env.sh` with this page's own `versions.toml`, and **no
campaign document is read and no `delvec` subcommand is run until it exits 0**.
What else in Init a run owes is what I1b's row says. **If any step here cannot
be completed, say so and stop**: authoring against a half-built toolchain
produces a campaign whose visual half was never reviewed, and nothing downstream
reports that.

The toolchain lives in **`~/.delvewright/`** — `engine/` the checkout, `bin/`
the unpacked archive, `env.sh` the environment every later command sources, and
`campaigns/` if the shipped library is ever taken. One directory, created by the
first run, the same in both modes, and held to the pin by I1b on every run.

**The commands, and the meaning of every failure, are `references/init.md`.**
Read it now and run from it. The table below is the order and the postconditions.

| step | what it establishes, and what has to be true after it |
|---|---|
| **I0 · mode** | `DELVEWRIGHT_MODE` is `dev` when the working directory carries **both** `crates/delvec/Cargo.toml` and `.claude/skills/delvewright/skills/new-delve/SKILL.md`, else `creator`. `DELVEWRIGHT_ENGINE` is the working directory in dev, `~/.delvewright/engine` otherwise. Dev: `campaigns/` there resolves to a directory, or **stop** |
| **I1 · already here** | `git`; a Python ≥ 3.11 recorded as `DELVEWRIGHT_PYTHON` and used by every Python invocation on this page; the **skill root** recorded as `DELVEWRIGHT_SKILL` — every bundled path below is `"$DELVEWRIGHT_SKILL/…"`, and it is never the working directory; `java` ≥ 21, enumerated with `scripts/find-jdk.py` before halting, and exported; `docker info` exits 0, **and `docker compose version` exits 0** — Compose v2 is a separate per-user CLI plugin that `docker info` says nothing about, and every entry point of step 10 is built on it. Not here: Rust and `git-lfs` |
| **I1b · the pin, every run** | `"$DELVEWRIGHT_PYTHON" "$DELVEWRIGHT_SKILL/scripts/check-toolchain.py" --mode "$DELVEWRIGHT_MODE" --engine "$DELVEWRIGHT_ENGINE"`, with **this run's** I0 and I1 values and never `env.sh`'s, exits 0: `delvec --version` through `env.sh` equals the version `[engine].ref` states (dev: the checkout's `[engine].version`), the creator engine tree's `rev-parse HEAD` equals the commit `[engine].ref` resolves to, and `env.sh`'s `DELVEWRIGHT_SKILL`, `DELVEWRIGHT_MODE` and `DELVEWRIGHT_ENGINE` are this run's. **Exit 3 is a refusal**: run the steps it prints, in order, then I1b again. Exit 4: no toolchain, all of I2–I8. Exit 2: stop. After 0: I2–I4 are skipped and nothing is downloaded; I5 only if the jar is not at its path; I6 on every run; I7 and I8 after a repair or a first run |
| **I2 · engine tree** | `"$DELVEWRIGHT_SKILL/versions.toml"` is read, never restated. Creator: the clone at `~/.delvewright/engine` fetches the tag `[engine].ref`, is `--detach`ed at it, and `rev-parse HEAD` equals `rev-parse "$ENGINE_REF^{commit}"`. Dev: HEAD is recorded and said out loud |
| **I3a · `delvec`** | `"$DELVEWRIGHT_PYTHON" "$DELVEWRIGHT_SKILL/scripts/fetch-delvec.py" --into ~/.delvewright/bin` exits 0 having printed its target, archive, digest and version. Exit 3 or 4 → I3b. **Exit 5 is a refusal** — never the floor, never a retry. Exit 6: stop |
| **I3b · the floor** | Only after exit 3 or 4, and in dev mode always. `cargo build --release -p delvec` **from inside** the engine tree, with `cargo --version` and `rustc --version` equal to the channel `rust-toolchain.toml` names. No `cargo`: hand over `rustup` and wait |
| **I3c · the binary** | `delvec --version` answers **the number I1b holds it to**. **Write down the `dsl` number** — step 1 needs it on every document. The GPU arms are **not** asked here: they draw with the client jar I5 fetches, so a gate run now refuses on every clean machine there is, for a reason this page created |
| **I4 · environment** | `~/.delvewright/env.sh` carries `JAVA_HOME`, `DELVEWRIGHT_MODE`, `DELVEWRIGHT_ENGINE`, `DELVEWRIGHT_PYTHON`, `DELVEWRIGHT_SKILL`, `DELVEWRIGHT_PREFABS` and `PATH`, this run's values in the lines I4 owns and every other line kept. Every later command runs as `. ~/.delvewright/env.sh && <command>` |
| **I5 · client jar** | **STOP — the user's choice.** Download by default, or a copy from a directory they name. Either way the jar lands at `~/.chunky/resources/minecraft.jar` and you have looked at it there. That it *reads* is I8's line |
| **I6 · the library** | `DELVEWRIGHT_PREFABS` names a prefabs directory and you have said which of the four cases produced it. **Nothing is cloned here** — step 2 takes the shipped library, if the campaign wants one |
| **I7 · named, not installed** | Chunky's source answers and a JDK of the major `[render].chunky_build_java` names is found for its build (a miss is said out loud, not a stop). On the drawing path only: `refimg.py --dry-run` exits 0. The skin toolchain is not mentioned |
| **I8 · finished when** | Every line of the checklist below answers, through `env.sh`. This is the one place the toolchain is exercised end to end, because three of those lines need the jar, the binary and the library at once |

### I8 — Init is finished when every one of these answers

Each of them through `env.sh`, since a line answering wrongly because the
environment was lost is indistinguishable from a missing tool:

```sh
mkdir -p .out
"$DELVEWRIGHT_PYTHON" "$DELVEWRIGHT_SKILL/scripts/check-toolchain.py" \
    --mode "$DELVEWRIGHT_MODE" --engine "$DELVEWRIGHT_ENGINE"   # I1b: exit 0
java -version                            # 21 or newer
echo "$DELVEWRIGHT_ENGINE"               # the engine checkout, non-empty
delvec --version                         # EQUAL to the pin's number, and the dsl number
delvec grammar list                      # the rule library, through the one binary
delvec --prefabs "$DELVEWRIGHT_PREFABS" render fidelity-gate
delvec --prefabs "$DELVEWRIGHT_PREFABS" grammar expand --program idiom-shape \
    --region 15x9x3 --seed 1 -o .out/probe
delvec --prefabs "$DELVEWRIGHT_PREFABS" palette .out/probe/idiom-shape.nbt \
    -o .out/palette.json                 # the client jar
docker info                              # the daemon: step 9's play server
docker compose version                   # the plugin: all of step 10's ladder
```

`delvec prefab`, `delvec schem` and `delvec harvest` are subcommands of the
binary those lines already exercised, so there is nothing separate to check for
them. The drawing path adds `refimg.py --dry-run`. **Any line answering wrongly
means Init is not finished**, and a run that continues authors against a
half-built toolchain — `references/init.md`'s I8 says what each one means when
it does not answer, and `render fidelity-gate` in particular says three
different things.

## Which placement model

**A campaign has exactly one placement authority, and choosing is the first
thing you do.** Declaring both is refused by name (`DW0839`), so this is not a
decision you can defer or revisit cheaply.

**`areas[]`** — pieces from the prefab library, seated on a fixed stride. Take
it when the campaign is a small number of rooms the library already has, and
read *The shipped library* before you commit to it: the library is an optional
clone and this is the branch that needs it.

**A site plan** — the whole map's design of record, from which the engine
*derives* the geometry. Take it whenever the map is the point: when the brief
describes a place with a shape, when the party has to walk somewhere and the
walking is the content, when there is no prefab that is the building the story
is about.

The two branches differ only at step 2 and step 13. Everything else — quests,
NPCs, dialogue, gates, shortcuts, the whole ladder — is identical and does not
know the difference.

**Take the site plan on a tie.** It costs four more documents and the map's own
reference views; taking `areas[]` wrongly costs step 2 over again, and this page
cannot get you back there from step 5.

**The test, the worked example and the command that answers it** are in
`references/placement.md`. Read it before you choose.

# The steps

## 1. The workspace, and the documents you are going to write

**Needs**: Init finished, and the `dsl` number written down. **Produces**:
`campaigns/<campaign-id>/` with `world.json` (minus its placement), the five
other required documents stubbed, `DESIGN.md` and `GENERATION.md`. **Read**:
`references/workspace.md` — the document set, the envelope, what `world.json`'s
optional fields commit you to, and what a stub owes.

## 2. Placement — where everything is

**Needs**: step 1, and the placement model chosen. **Produces**: `world.json`'s
`areas[]`, or `geometry-brief.json` + `layout-graph.json` + `site-plan.json`.
**Read**: `references/placement.md`. On `areas[]` also read
`references/the-shipped-library.md` and take the library there — this is the
step that needs it. On the site plan the map's own reference is drawn first:
`references/map-reference.md`.

## 3. The story documents — `npcs`, `classes`, `quest-plan`

**Needs**: step 2. **Produces**: `npcs.json`, `classes.json`, `quest-plan.json`.
**Ends at**: a campaign that does **not** validate, carrying only refusals whose
messages name something `quests.json` or `dialogue.json` will supply. That is the
correct state to leave this step in, and it is not something to mention,
apologise for or try to fix. **Read**: `references/story.md` before you start the
loop, not after a refusal.

## 4. The design gate — STOP, the user says yes

**Needs**: step 3. **Hands over**: a visual walkthrough of the whole design —
every scene, a near view and a far view, each image shown with the `time` and
`weather` tokens it was drawn under. **Waits for**: an explicit yes, from the
user, never inferred from silence and never from a reviewer you invented.
**Produces**, once they say yes: `campaigns/<id>/design/`, `design/README.md`
and `design.json`. **Read**: `references/design-gate.md`.

## 5. The content documents — `quests` and `dialogue`

**Needs**: step 4's yes. **Produces**: `quests.json`, `dialogue.json`, and the
first campaign state where `validate` clean is reachable. **Read**:
`references/content.md`, plus `references/quest-capabilities.md` for what the
DSL can express and `references/writing-craft.md` for how the prose has to be
written — both before writing, not after a refusal. A custom face is
`references/npc-skins.md`. Other languages are a final document stage:
`references/other-languages.md`.

## 6. `delvec fmt` — every campaign, every time

**Needs**: step 5. **Produces**: every document and sidecar in canonical form.
Mandatory for every campaign and again after every later fix, playtest repairs
included. **Read**: `references/build.md`.

## 7. `delvec analyze`

**Needs**: step 6. **Produces**: quest-graph reachability, deadlock and
dark-room findings — fixed in the documents, never by weakening the campaign. A
dead quest is a design bug. **Read**: `references/build.md`.

## 8. `delvec build`

**Needs**: step 7 clean. **Produces**: the datapack tree at
`"$DELVEWRIGHT_ENGINE/validation/delve-output"`, `critical-path.json` and
`render-plan.json`; on a site-plan campaign the three hashes and the pacing
line. Must exit 0. **Read**: `references/build.md`.

## 8b. The showcase cameras

**Needs**: step 8's tree. **Produces**: `campaigns/<id>/design/cameras.json`,
one showcase camera per approved image of `design.json`. Estimate each from the
picture — which side, how high, how close, how wide, what the point of interest
is — then draw it against the tree step 8 built and move it until the picture is
in the frame. An approved picture with no camera stops the next build, naming
the pictures, and stops the staging gate in step 14, so this is before the walk
and not after it. A camera answers one picture: never re-aim one at a second,
write another row. `delvec cameras` draws the record against that tree and
renders its scenes; `delvec place-camera` is the record's one writer. A row no
camera answers is `DW0900`. The craft — which side, how high, how close, how
wide — is `$DELVEWRIGHT_ENGINE/docs/reference/showcase-shots.md` §4; placing one
by hand, in the running game, is
`$DELVEWRIGHT_ENGINE/docs/reference/tools.md` §4a.

## 9. The walk — STOP, this one is the user's

**Needs**: step 8. **Hands over**: a running server, the connect line, and what
to look for item by item — naming per item every finding still open that they
must *not* test. **Waits for**: what they saw. Do not run the ladder, start step
12 or write `walk-record.json` before they answer. **Read**:
`references/walk.md`, and `references/playtest-rounds.md` from round 2 on.

## 10. The machine ladder

**Needs**: the walk answered. **Produces**: PackTest and bot runs at exit 0, plus
a branch run per branch whenever the build emitted `validation/branch-plan.json`.
**Read**: `references/ladder.md`; on a red, `references/when-red.md`.

## 11. The branch chronicle — only when the plan declares `branch_points`

Skip if it does not. If it does, this step is not optional and not delegable:
skip it and the campaign is not verified, however green the ladder is.
**Produces**: the citation table in `GENERATION.md`. **Read**:
`references/chronicle.md`.

## 12. Visual review

**Needs**: step 10 green. **Produces**: your judgement of the POV sequence in
route order, read against `campaigns/<id>/design/concept/`, scene by scene.
Yours to do, not a checklist to hand off: judging a frame is the whole task.
**Read**: `references/visual-review.md` — its cost section before you run its
first command. **A POV frame that is the wrong picture** is a camera question,
not a render one: place that one by hand in the running game
(`references/tools-by-symptom.md`, *a render camera nobody is satisfied with*).

## 13. Detail — site-plan campaigns only, and only after the walk

Optional, and impossible until `walk-record.json` records a **passed** walk
(`DW0841`) — a record saying nobody walked is a legal record and refuses too.
**Produces**: `detail-plan.json`, one place at a time. **Read**:
`references/detail.md`; a piece the library does not have is
`references/new-pieces.md`.

## 14. Hand it over

**Needs**: everything above. **Produces**: `campaigns/<id>/README.md` — the
storybook — its localized editions, and the report that ends the run. Nothing
comes back. **Read**: `references/hand-over.md`. **When the exterior or
starting-scene shot is not the one to ship**, place that camera by hand in the
running game (`references/tools-by-symptom.md`, *a render camera nobody is
satisfied with*) rather than re-rendering the one you have.

**A newer page is not pushed at anybody.** Auto-update is off by default for a
third-party marketplace, so a newer `/new-delve` arrives when the user runs
`/plugin marketplace update delvewright` and updates the plugin. Say so here and
nowhere earlier. Record in `GENERATION.md` the plugin version this run used, the
engine release, the `dsl` number, and — if the shipped library was taken — its
revision. A later round opened under a different plugin version says so before it
does anything else; I1b is what holds its toolchain to that version's pin.

## Where each reference lives

Read one when the step above names it. **No reference file sends you on to
another**: every pointer is from this page, so an italic *section name* inside a
reference means the file listed here.

| file | what it carries | named from |
|---|---|---|
| `references/init.md` | every Init command, and what each failure means | Init |
| `references/the-shipped-library.md` | the optional prefab library: its revision, its postconditions, what a campaign records | I6, step 2 |
| `references/placement.md` | the placement test, `areas[]`, and the three site-plan documents | *Which placement model*, step 2 |
| `references/workspace.md` | the campaign directory and every document in it | step 1 |
| `references/map-reference.md` | drawing the map's own reference views | step 2 |
| `references/story.md` | npcs, classes, the quest plan, and where step 3 ends | step 3 |
| `references/design-gate.md` | the walkthrough, the approval, `design.json` | step 4 |
| `references/content.md` | quests and dialogue, and the codes that clear here | step 5 |
| `references/quest-capabilities.md` | every verb, effect and field a quest can use | step 5 |
| `references/writing-craft.md` | the prose checklist, run over every line | step 5 |
| `references/npc-skins.md` | the skin toolchain, when a design calls for a face | step 5 |
| `references/other-languages.md` | the localization stage | step 5 |
| `references/build.md` | `fmt`, `analyze`, `build`, and what the build writes | steps 6-8 |
| `references/walk.md` | bringing the server up, and what to hand the user | step 9 |
| `references/ladder.md` | PackTest, the bot, branch runs, and how to triage a red | step 10 |
| `references/chronicle.md` | reading a branch's chronicle against the design | step 11 |
| `references/visual-review.md` | the POV sequence, Chunky, and what the set costs | step 12 |
| `references/detail.md` | `detail-plan.json`, one place at a time | step 13 |
| `references/new-pieces.md` | making a piece the library does not have | steps 2, 13 |
| `references/hand-over.md` | the storybook, its marker, and the play commands | step 14 |
| `references/playtest-rounds.md` | every round after the first | steps 9, 14 |
| `references/when-red.md` | the symptoms most likely to stop you | any red |
| `references/tools-by-symptom.md` | the tool inventory, by the symptom that wants it | any step |
| `references/pitfalls.md` | difficulty, combat, bonfires, waves, staging | steps 3, 5 |
| `scripts/check-toolchain.py` | run at I1b on every run, and at I8: the toolchain on disk against the pin | I1b, I8 |
| `scripts/fetch-delvec.py` | run at I3a: the archive, verified and unpacked | I3a |
| `scripts/find-jdk.py` | run at I1: the newest JDK 21+ already on this machine | I1 |
| `scripts/fetch-client-jar.py` | run at I5, on the download path | I5 |
