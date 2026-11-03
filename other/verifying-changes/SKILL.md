---
name: verifying-changes
description: The canonical verification ladder for this repo and how to read its feedback loops (vitest, the Playwright suite, the blind A/B pair, dev-server pitfalls). Use before claiming any change works, and when a test failure looks confusing.
---

# Verifying a change in money-tracker.online

`docs/SPEC.md` §7 is the definition of done and this skill is how to reach it without mistaking a
tired laptop for a defect. Everything below was measured in this repository; where a number is
quoted, the command that produced it is named. §7.7 governs anything you write down afterwards.

## Before the ladder: provision the checkout

A `git worktree` carries none of the per-checkout fixtures, and each one fails in a way that looks
like something else:

| Missing            | What you see                                            | Fix                                                      |
| ------------------ | ------------------------------------------------------- | -------------------------------------------------------- |
| `node_modules`     | `Command "prettier" not found`, `tsc: not found`        | `pnpm install --frozen-lockfile --prefer-offline`        |
| the local D1       | every route 500s on the first query                     | `pnpm db:migrate:local`                                  |
| `.dev.vars`        | Better Auth throws on anything touching a session       | `sh .ai/scripts/test-env-up.sh`                          |
| the demo workspace | specs pass against empty screens, which asserts nothing | `node scripts/seed/seed.mjs --url http://127.0.0.1:3010` |

`.ai/scripts/test-env-up.sh` does all four plus the route tree and a dev server on the first free
port in 3011-3020, and writes `.ai/qa/test-env.json` with the base URL. It is the entrypoint
`om-prepare-test-env` generated and the one `om-auto-qa-pr` boots through; a second run attaches to
a healthy server instead of restarting it, so running it when it was not needed is nearly free.
`sh .ai/scripts/test-env-down.sh` stops exactly what it started.

**It refuses to clobber a `.dev.vars` a person wrote.** The file it writes starts with a marker
comment; a file without that marker is a real checkout's real secrets and the script keeps it. On
your own checkout use `pnpm dev` in one shell and `pnpm e2e` in another.

## The ladder

1. **While working**: `pnpm typecheck`, `pnpm lint`, single vitest files
   (`pnpm exec vitest run <path>`).
2. **Before committing**: the pre-commit hook runs `lint-staged`, `pnpm typecheck` and the tests
   the commit reaches - every test that imports a staged file, plus every test that reads the disk
   or starts a process (ADR 0026) - not the whole suite. What it catches scrolls past (see "a count
   and no shape" below).
3. **Before a PR**: `pnpm test` and `pnpm build`, plus the two drift gates when you touched the
   route tree or the schema:
   `pnpm generate-routes && git diff --exit-code -- src/routeTree.gen.ts` and
   `pnpm db:generate && git diff --exit-code -- drizzle/`. CI re-asserts both.
4. **UI touched**: `pnpm e2e` locally, **and look at the screens**. Nothing compares a pixel
   (ADR 0016): the suite asserts that a screen answers, hydrates, says nothing in the console and
   can be acted on. What catches a screen that changed _shape_ is the blind pair,
   `node scripts/visual/capture.mjs`, and it only catches it if somebody runs it and reads it. For
   a refactor with no intended visual change - a token retune, a shared layout edit, a Tailwind
   bump - that pair is the only thing between the change and `develop`.
5. **In an agent worktree** the gate is `validation.commands` in `.ai/agentic.config.json`: both
   drift gates, typecheck, lint, vitest and build, in that order, run by the om skills before a PR
   opens and again by `om-auto-review-pr`. The browser suite is not in it: CI runs it on every pull
   request, and `om-auto-qa-pr` drives the app through `.ai/scripts/test-env-up.sh` for evidence.
6. **CI** runs lint, typecheck, unit tests, build, both drift gates, the browser suite and the axe
   scan on every pull request. Since ADR 0016 there is no label to remember.

`pnpm check` (prettier over the whole repo) is **not** a gate and fails on 10 pre-existing files at
the time of writing. Keep what you touch prettier-clean - the `Edit`/`Write` hook does it for you -
and never reformat the repo as a side effect. A file written through a shell heredoc is not covered
by that hook, and hand-written markdown is never clean, so run `pnpm exec prettier --write` on it
yourself.

## Reading failures

These are hard-won and each one has cost somebody an afternoon.

- **A timeout is a claim about the machine until the error text says otherwise.** Both read as
  `1 failed`. Only the body separates `Received: hidden` - a computed style, which a starved
  processor computes no differently - from an empty value an interaction should have set. Grepping
  for that costs a second and decides whether to re-run or to fix. Starvation turns a passing test
  red and never a failing test green, so every _pass_ under load is worth what it would be on a
  quiet machine, and only failures need repeating.
- **Re-run the failed files alone, straight away.** Two files that timed out inside a 134-second
  full suite passed together in 999 ms while the one-minute load stood at 120. A pass is the
  direction starvation cannot fake. It is a diagnosis, not a pass: the gate still runs everything.
- **A timeout sorts three ways, not two.** An assertion that saw something; a machine with no
  processor to give; and a subject that spent the budget on work it genuinely does. Under
  `pnpm dev` Vite compiles a route's client module graph on its first visit, so a spec that opens
  nine screens pays that cost nine times. In one chromium run, 202 hydration waits took 696 of the
  1005 seconds of Playwright step time, and the two specs that timed out were the two longest in
  the job.
- **`VITEST_MAX_WORKERS` is the knob for a contended machine, and it belongs in the shell, not in
  `vitest.config.ts`.** Matched pair under contention: at load 12.38 fifteen workers took 63.19 s
  and one test failed; nine minutes later at load 12.29, four workers took 52.03 s and none did.
  The opposite direction rests on unmatched samples, which is exactly why the cap is not written
  into the config - a CI runner is the free case.
- **A failing gate that was not captured leaves a count and no shape.** Pipe it:
  `pnpm test 2>&1 | tee <file>` before quoting a summary to anybody. The same five failures,
  re-run four minutes later against the same tree, were 2197 passed in 21.43 s.
- **Do not edit source while `pnpm e2e` is running.** The dev server renders the next request from
  the edited file while the browser still holds the old client chunk, and the run then reports
  console hydration mismatches (`data-tsd-source` line numbers that differ by the lines you added)
  on every screen that mounts the changed component. They look like product defects and are not.
  Finish every edit, then start the run; edit again only after it has ended.
- **Anything that deletes or moves a source file must restart the dev server before the gate
  runs.** A server that already loaded a module answers 500 on unrelated routes after the file goes
  away - measured as five failures while typecheck, lint, vitest and build were all clean.
- **A whole browser suite failing on one repeated shape is a statement about the environment.**
  Every authenticated spec skipping means the cached session is stale: re-run the `setup` project
  (`pnpm exec playwright test --project=setup`). A repeated `429` means the rate limiter, not the
  product: `/sign-in/email` allows ten attempts a minute and `/sign-up/email` five every five
  minutes, which is the entire reason `auth.setup.ts` mints sessions once.
- **Console red is the application talking.** The net is `e2e/support/console.ts`, an `auto: true`
  fixture, so every spec importing `test` from `./support/console` is watched. Fixing a console
  failure means fixing the application: `TOLERATED_CONSOLE_WARNINGS` may only ever hold something
  the _engine_ says on the dev-server path that a build cannot produce, and appending to it removes
  coverage from the clause `docs/SPEC.md` §2.10 states.
- **`playwright.config.ts` refuses ports outside 3010-3020** when not in CI. That guard exists
  because runs have photographed the wrong checkout. Don't fight it.

## Probing the running app

Driving the app by hand is how a change gets checked before it has a spec. These are the seams that
make a probe lie.

- **Theme needs both halves.** `useTheme()` (`e2e/support/app.ts`) writes the stored mode _and_
  calls `page.emulateMedia({ colorScheme })`. `data-theme` comes from the bootstrap script reading
  `localStorage` before first paint; `prefers-color-scheme` decides what the browser paints behind
  the document and what the `system` branch of the token layer resolves to. Setting one of them
  scans a page no reader will ever see.
- **A page that looks finished answers nothing until it hydrates.** Every control is a React Aria
  component driven by `onPress`, and the shell is streamed: before hydration a click lands on a
  button with no handler and typed text is discarded when React attaches. Both read as "the form
  did not submit" - a product bug that is not there. `waitForHydration()` waits on React's own
  `__reactFiber$<id>` marker, which is the only signal this application offers.
- **The server's clock is pinnable in development only.** `x-mt-server-today` is honoured behind
  `import.meta.env.DEV`, and a production build folds that guard away on purpose. So a probe
  against `pnpm dev` can pin the day and the same probe against `vite preview` silently cannot -
  which is how 24 frames once broke on what turned out to be a calendar change (`docs/SPEC.md`
  §7.7). Before repointing anything at a different target, list what the old target provided that
  the new one does not.
- **Money never leaves the integer minor unit, so a probe that reads a rendered amount is reading a
  formatter.** To check arithmetic, assert on the stored minor-unit value; the scale is
  `currencies.digits` and never a hard-coded 2, and `ref_amount_minor` is historical and never
  recomputed (`docs/MONEY.md`).
- **`vitest` swallows `console.log` from a test body.** To surface a measurement, assert the value
  against a sentinel and read it back out of the `AssertionError`.
- **The seed is deterministic and anchored, not clock-driven.** `BASELINE_DAY` in
  `e2e/baseline-day.ts` is the day the server is pinned to; `playwright.config.ts` sends it as a
  header for `pnpm dev` and `vite.config.ts` folds it into an e2e build. Changing it moves every
  date-dependent assertion at once.

## Reading the blind pair

There is no diff view: `playwright-report/` carries traces and videos of failures, not
expected/actual/diff triplets. The visual judgement is two frames and a human, at review.

```bash
node scripts/visual/capture.mjs --url http://127.0.0.1:3010/dashboard --out <scratchpad>/<n> --viewports 360x800,1280x900
```

- It writes **only** into the `--out` directory you give it, outside the repository. A PNG left in
  the repository root is a stage failure (`docs/plans/98-verification-protocol.md` §3.3).
- **Nothing runs it for you.** The baselines fired on every commit; this fires when somebody types
  the command. The refactor with no intended visual change is the case the baselines were best at
  and the pair is worst at, because nobody thinks to run it.
- Shoot the state your change is about, not two viewports at rest. The interaction state is the
  point of the change and is what `docs/SPEC.md` §7.4 asks for.
