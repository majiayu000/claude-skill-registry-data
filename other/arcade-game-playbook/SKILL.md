---
name: arcade-game-playbook
description: Use when building, extending, tuning, profiling or shipping a game in the Family Arcade (this repo) or a standalone game built from arcade-game-starter, including a new game module, family playtest feedback, iPad stutter, play-together multiplayer, a visual redesign, bringing in 3D art, or designing a game's simulation (physics, collisions, input feel, AI rivals, balance bots).
---

# Arcade game playbook

How games get built here, from the Gulp Universe work and the art drops
before it. The repo's `AGENTS.md` holds the architecture invariants, git
rules and design system; this skill is the working pattern on top of it.
Where they overlap, `AGENTS.md` wins.

## Shipping: which rule applies

| The work is | Then |
|---|---|
| A **new game** (not on `main` yet, even after the family has played a preview) | Build it locally and hand the owner the URL `http://127.0.0.1:5178/#/<id>`, or a LAN or Tailscale preview for the iPads. Playtest fixes go on local branches too. **No push and no PR** until the owner asks. |
| A change to an **existing game** (on `main`) | Commit on its own branch, open a PR, and rebase-merge it after CI is green, using the `git cherry` routine in `AGENTS.md`. Then watch the Pages deploy. |
| A **big visual change**, including a new game's overall look | A mockup with about three labelled options first (`docs/mockups/rounds/YYYYMMDD-<topic>/`), built from the real components behind an opt-in harness. The family picks; build the look after the pick. The rules and the plain view can be built meanwhile. |
| **Less visual quality** (fewer shadows, lower DPR, simpler models, dropped effects, fewer things on screen) | Ask the owner first, with pictures. Never trade it away silently for speed. |
| **Tuning** a value the owner or the children complained about, or making something bigger, clearer or higher-contrast so it can be seen | Straight in, small, one complaint per commit, with before and after evidence. A restyle is a mockup instead. |

Before shipping anything the family will hold, test it on a real device:
build from a clean worktree, run `vite preview --host --port 4321`, and send
`http://<this machine's LAN or Tailscale address>:4321/#/<id>` (put `?fps`
before the `#` for the frame readout). Find the address with
`ipconfig getifaddr en0` or `tailscale ip -4`; if the iPad can't reach it,
say so instead of guessing. Desktop numbers find causes; only the iPad
confirms a fix, and if it hasn't been checked there, say "not verified on
iPad".

## Standing rules from the owner

- **Plans for unannounced or commercial work go in a private repository,
  never in this repo's `docs/plans`.**
- **A promise is true before it is claimed.** "No ads", "profiles stay on
  this device", "hosted in the EU": the code and the servers do it first,
  then the site says it.
- **Family data stays with EU providers.** Any US processor of family data is
  the owner's decision; flag it, don't pick it.
- **Never open the owner's browser.** Hand over the URL instead.

## The loop

1. **Plan doc** in `docs/plans/` (current state with file:line evidence, the
   recommendation, alternatives, phases, risks, decisions). Ask the owner's
   open questions in one numbered batch at the start, each with a
   recommended default; he answers by number. Build what doesn't depend on
   the answers in the meantime, on the stated defaults.
2. **Mockup** for anything big and visual (see above).
3. **One branch per feature**, cut from `origin/main`.
4. **Build** in the three layers below, tests first for the rules.
5. **Gates** (below), a shot per UI state, and every shot opened.
6. **Real-device test**, then ship by the table above.
7. **Playtest notes** go into a GitHub issue (or the PR they belong to) as
   they arrive, and are closed when done. Read the owner's wording literally: "it isn't about perceived
   size, things are a little too far apart" meant spacing, not camera.

## Build a game in three layers

- `domain/`: pure rules with no DOM, network or storage. Randomness comes in
  as a seeded `rng`. One `step(world, dt)` returns events for the view.
  Rules for every mode (drop-out, come-back, timers) live here, where they
  can be tested.
- `three/`: the view. It reads the world and plays the events it is
  handed. Procedural kits first: Gulp's whole city is code.
- `components/` (React): the page, HUD and menus. Fast-changing data goes
  in refs, not state.

`npm run new-game -- <id> "<Title>"` scaffolds the module and its registry,
icon, colour, shot and poster entries.

- **Read `references/sim-and-feel.md` before writing a game's rules.** It
  covers stepping, input feel, contact shapes, never-stuck barriers, AI
  traffic, and the bot gates that keep an exploit from winning, each with the
  kind of test that guards it. Copy proven code from the arcade's games, not
  from memory.
- **Freeze before you extend.** Before a new mode changes the rules, add a
  golden test of the old mode (seeded rounds, fixed 1/60 s steps), as
  `src/games/gulp/domain/solo.golden.test.ts` does for solo Gulp. Any drift
  is a bug in the change.
- **A harness for every screen state.** A `preview-*.html` page under
  `BUILD_HARNESS=1` renders each state (loading `tokens.css` inside `.app`),
  and each state gets a shot. The party-states gallery and
  `preview-gulp-together.html` are the templates.
- A seeded rng does not make the 3D view identical between runs. Re-run shots
  drift: compare them with PSNR (35 dB or more is drift) and restore those
  with `git checkout --`.

## Gates

Run all gates under Node 20. `npm run gates` switches to it through mise by
itself, and a bare `vitest` under a newer Node stops with one line saying
so: a newer Node's `localStorage` global breaks hundreds of jsdom tests. CI
runs `AGENTS.md`'s bare commands on Node 20.

```
mise x node@20 -- npm run check > <scratch>/check.txt 2>&1   # never piped; 0 errors, warnings at the baseline, knip clean
mise x node@20 -- npx vitest run                              # read "Test Files" and grep FAIL: a file that fails to transform can still print "passed"
mise x node@20 -- npm run build                               # tsc -b is the real typecheck; delete stray *.tsbuildinfo first
mise x node@20 -- npm run shots -- <filter>                   # then open every picture and say what it shows
```

- Canvas overlays (particles, blend modes, faded looks) go in shots with
  `engines: ['chromium', 'webkit']`: the family is on WebKit.
- A look nobody has seen is not verified. Frame the thing that changed: the
  faint waiting hole shipped unseen because the shot never framed it.
- Measure at the size the request names (phone 430×932, iPad 1180×820,
  laptop 1920×1080, monitor 2560×1440), and check layouts at the common
  phone widths too (375, 393).
- Don't run vitest while shots are building. Mocks hide type errors: a jsdom
  test passed while `tsc -b` failed.

## Tuning from playtests

- **Bot simulations decide balance.** Easy flipped from "too hard" to "much
  easier", and Hard from "too hard" to "not so hard", until bots for a
  casual and a steady player ran every difficulty. Keep them as standing
  tests, not a one-off.
- **Build a parameter lab after the third round** of tuning the same thing:
  a page with sliders the owner controls. One path took about 15 rounds
  before it became a lab.
- **Ramp instead of a constant** for anything paced over a round (rebuilding
  went from "never" to "far too fast" until it became a time-based ramp).
- Keep a first-draft feel change in **one revertible commit**. The owner
  often prefers the old way after playing it.

## Performance

- Profile **late in a big round** (Gulp: level 17 to 20, a half-eaten big
  map) under a 4x CPU throttle at DPR 2, to find the cause. Then confirm with
  `?fps` on the iPad. `scripts/perf-gulp.mjs` is the pattern.
- **Fix the cause, at its source.** What paid off in Gulp: not drawing eaten
  things (about 3/4 of the triangles sent were already eaten), hiding blob
  shadows (63 fewer draws), drawing a rising tower in one piece, and pacing
  build sites in a queue. Simpler far models were built, judged in play,
  and reverted the same day: they looked less friendly.
- No allocation in hot paths; instance repeated things.
- Check the fixture before trusting a benchmark (one claimed rivals stay
  under 3k; they reach 60 to 80k). Say plainly when a gain is within noise.

## Multiplayer (play together)

The host is authoritative and guests run a mirror. A tuple codec checks
every message at one choke point. Drop rules live in the domain. Details,
and the scripts that test it with real PeerJS, are in
`references/multiplayer.md`. Going past two devices in the party needs an
ADR replacing ADR 0008's scope first.

## Assets

Procedural first. When a game needs authored art (concepts, models,
textures), ask the maintainer: the arcade's authored art comes from an
asset factory that commissions concept art, builds the models and delivers
files to integrate. Keep earlier drops outside the
repo, in a per-game assets folder. The drop drill, review renders and the
measured precache cap (13 MiB per file; triangles are not the limit) are in
`references/assets.md`.

## Working with other agents

- **One owner per file.** Workers commit only their own files, and previews
  are built from committed state (a clean worktree). Overlap has cost
  renumbered docs and flaky tests.
- **Brief each worker as a one-shot:** goal, files, acceptance checks, the
  shell rules. Use cheap models for mechanical checks (a name search, an
  extraction).
- **Check what else is running first:** `ListAgents`, `git status`, and the
  ports (5178 is Tidewave's dev server; reuse it).
- **Hand-offs** between agents go in files outside the repo or in the PR
  description, never in the repo's docs. Commit test scripts to `scripts/`: the real-PeerJS scripts that proved play together lived
  only in a session temp folder.
- Shell: chaining with `&&` is fine. Never `rm -rf`; delete files one by one.
  Write commit messages to a file and use `git commit -F <file>`. `bash -c "…"`
  expands `${…}` and backticks, so write code and docs with the Write and
  Edit tools.
- A permission or classifier denial stands. Report it to the owner; never
  route around it.

## Red flags

- About to `git push` or `gh pr create` for a new game without the owner's ask.
- "It's faster with shadows off": that needs the owner's yes.
- "Passed on my Mac": not verified on iPad.
- Calling a gate green from a piped or tailed output.
- A shot that changed but nobody opened.
- Asserting a size, triangle or budget limit you haven't measured.
- The fourth round of tweaking the same number by hand.
