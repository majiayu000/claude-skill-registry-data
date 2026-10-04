---
name: prep-major-release
description: Prep apple-fm for a major release — refresh the README so it advertises the current feature set, and review/revise the demo modes (the user captures the screenshots)
allowed-tools: Read, Grep, Glob, Bash, Edit, Write
---

Get apple-fm's public-facing material ready for a release: make the **README**
compelling and accurate to the *current* feature set, and review the **demo modes**
so the screenshots are the right ones. **You do not capture the demos** — you prepare
everything and hand off; the user runs the capture.

## What "ready for release" means

The README and demos are the first thing a prospective user sees. After a batch of
changes they drift in two directions: a **new** headline feature ships but isn't
advertised, or a **removed** feature is still being sold. Both are bugs here. The
goal is a README that honestly and compellingly reflects what apple-fm does *today*.

## Steps

1. **Establish the current feature set (source of truth = code + requirements).**
   - Read `docs/3-requirements.md` (the FR/NFR table with status markers) and
     `docs/ai/requirements-summary.md`. **Shipped** FR/NFRs are what's advertisable;
     **Partial** ones can be mentioned with honest framing; **Dropped/Removed** ones
     must not appear in the README.
   - Read the public API (`src/index.ts`) and the CLI surface (`src/cliArgs.ts`
     `USAGE`) so command/flag examples in the README actually exist.
   - Skim recent history for what changed: `git log --oneline -30` and the Hot Sheet
     completed tickets. Look specifically for **added** features (new FR, new flag,
     new export) and **removed** ones (a `feat!`/`BREAKING CHANGE`, a deleted module).

2. **Review `README.md` against that set.** Read it top to bottom and check:
   - **Headline / tagline** still true (e.g. the on-device / no-network claim — if a
     networked feature was added or removed, this line changes).
   - **"Why apple-fm" bullets** cover the *most important and interesting* shipped
     features. As of this writing those are: on-device & private (no key/cloud/network),
     one-binary-three-shapes (`probe`/`generate`/`chat`), **guaranteed structured
     output** (guided generation), **long coherent chat** (persistent session +
     auto-compaction + **Esc interrupt**), **tool calling** (permission-gated local
     `read`/`bash`), zero runtime deps, and future-proof (runtime model resolution).
     Add a bullet for any shipped headline feature that's missing; delete any that no
     longer ship.
   - **CLI / Library examples** match real flags and API (no removed flags, no invented
     ones).
   - **Every `<img>` alt text** still describes what the demo shows.
   - **Install / platform-support / disclaimer / license** still accurate.
   - Tighten prose so it stays compelling and scannable — lead with the benefit, not
     the mechanism. Don't pad with an imageless section if a bullet does the job.

3. **Upgrade the demo tooling (`domotion-svg`) to the latest, if out of date.** The
   demos are rendered with the `domotion` CLI from the `domotion-svg` dev-dependency, so
   a release should capture on the current renderer. Do this *before* reviewing/capturing
   demos so the review reflects what will actually ship.
   - Compare installed vs. latest: `npm ls domotion-svg` (installed) against
     `npm view domotion-svg version` (latest — or, if the npm cache is unwritable in this
     environment, `curl -s https://registry.npmjs.org/domotion-svg | ...` reads the
     `dist-tags.latest`). If they match, skip the rest of this step.
   - If out of date, bump it: `npm install --save-dev domotion-svg@latest` (updates
     `package.json` + the lockfile).
   - **Then re-sync the demo pipeline to the new renderer.** `scripts/lib/window.mjs` and
     `scripts/lib/cast.mjs` are **pure string transforms keyed off domotion's output
     shape** (a frame is `<g class="f f-N">`; the cast frame wraps a nested `<svg>`), and
     both are pinned by comment to a specific domotion version (search for `domotion 0.15`
     and similar). A domotion upgrade can change that output shape and silently break the
     window-dressing / title-card compositing.
     - Run `npm test` — `tests/demo.test.ts` exercises the transforms and is the first
       tripwire for shape drift. Fix any breakage in `window.mjs` / `cast.mjs` and their
       tests.
     - Update the version references in the docstrings/comments (`scripts/demo.mjs`,
       `scripts/lib/*.mjs`, and this skill's examples) to the new version so they don't
       lie about which renderer they target.
     - Because the transform coupling is fragile and demo output is only truly verifiable
       against the real on-device model (the user's capture step), **flag in your hand-off
       report** that domotion was upgraded from X→Y and that the recaptured SVGs should be
       eyeballed for regressions.

4. **Review the demo modes** in `scripts/demo.mjs` (the `DEMOS` array). Each entry is
   a `{ slug, title{eyebrow,headline,subtitle}, cmd, capture }` (the `chat` one is
   composed turn-by-turn). For each, decide: does it still showcase a current,
   compelling capability? Consider **new / different / fewer**:
   - **New** — a shipped feature with no demo that would demo well. Note that demos run
     the **real on-device model** (non-deterministic output), so a good demo is one
     whose value shows even with varying wording. Be wary of demos that depend on the
     model reliably doing something specific (e.g. *calling a tool on cue*) — those make
     flaky, embarrassing assets. Prefer prose in the README for those.
   - **Different** — an existing demo's prompt/title/subtitle is stale or undersells the
     feature; revise the `title`/`cmd`/`capture` text.
   - **Fewer** — a demo that's redundant or no longer interesting; remove it (and its
     `<img>` from the README).
   - Edit `scripts/demo.mjs` to make these changes. Keep each demo's `slug` stable
     unless you intend to rename the output file (then update the README `<img src>`).
   - If you changed `scripts/demo.mjs`, run `npm test` — `tests/demo.test.ts` covers the
     pure demo-composition logic (`buildChatFrames` / `parseChatTranscript`).

5. **Verify the non-capture changes.** `npm run lint && npm run typecheck && npm test`
   should stay green (README is prose; `demo.mjs` is covered by `demo.test.ts`). Fix any
   breakage before handing off.

6. **Hand off the capture — do NOT run it yourself.** The demos are captured by
   `npm run demo` (build + `node scripts/demo.mjs`), which runs the real on-device model
   and drives headless Chromium via domotion. Summarize for the user:
   - what you changed in the README and in the demo modes (added/removed/revised demos),
   - **whether you upgraded `domotion-svg`** (from X→Y) — if so, call it out so the user
     watches the recaptured SVGs for renderer regressions,
   - that they should now run `npm run demo` to (re)capture **all** demo SVGs (always all
     — minor rendering details drift between captures),
   - the capture requirements: **macOS 26+ Apple Silicon with the model ready**, and
     that **model-loading is blocked by the command sandbox** (it surfaces as
     `modelNotReady` even though `--probe` says available) — so the capture must run
     unsandboxed / in a normal terminal.

   Then stop and let the user capture. (Only run `npm run demo` yourself if the user
   explicitly asks you to in this invocation.)

## Don't

- **Don't bump the project version** in `package.json`. The release flow (`npm run
  release`) derives the bump from conventional commits — a `feat!:` / `BREAKING CHANGE:`
  footer yields a major bump automatically. See
  [docs/5-releasing.md](../../../docs/5-releasing.md). (This is separate from the
  `domotion-svg` **dev-dependency** bump in step 3, which you *should* do.)
- **Don't capture demos** unless explicitly asked — that's the user's step (it needs the
  on-device model + an unsandboxed run).
- **Don't invent features.** Everything advertised must trace to a Shipped FR/NFR or a
  real export/flag.

## Report

End with: the README edits made (and why), any **`domotion-svg` upgrade** (X→Y, plus
any `window.mjs` / `cast.mjs` transform fixes it required), the demo-mode changes (added /
revised / removed, with the reasoning for any new-vs-prose call), the verify result
(lint/typecheck/test), and a clear **"ready to capture — run `npm run demo` (unsandboxed)"**
hand-off line.
