---
name: wordle-2048-hybrid
description: Build a hybrid game that combines 2048's slide-and-merge mechanic with Wordle's guess-and-feedback loop — merging charges a tile, tapping a charged tile commits it (player-chosen order) into a guess bar that auto-submits against a secret word, with correct positions locking in across guesses and the spawn pool/board shrinking as letters get ruled out or fully placed. Also covers a daily-challenge mode with tracked stats/streaks and a shareable result, synthesized sound effects, a from-scratch reconciliation-based render architecture for smooth tile animation, and an online cross-player leaderboard backed by Supabase (Postgres + PostgREST + Row Level Security) that keeps working across two hosting channels (a CSP-locked Claude Artifact and a Vercel static deploy) from one unforked codebase. Use when asked to combine/cross Wordle and 2048, add a daily-challenge/stats/share loop to a browser game, add a real cross-player leaderboard to a client-only game, or make a slide-and-merge game's board actually animate instead of snapping. Builds on the wordle-game and 2048-style-game skills.
---

# Wordle2048 hybrid

Read the `wordle-game` and `2048-style-game` skills first — this is the specific pattern for combining them, plus the pitfalls that only show up once they're combined.

## The core idea

A 2048-style grid (letters instead of numbers) is the *input mechanism* for a Wordle guess, via four connected mechanics. An earlier version had merges auto-feed a guess bar directly — that made word order an accident of merge timing rather than a player choice, which read as luck rather than skill, and the board would lock up before players got meaningful guess progress. The current design fixes both:

**1. Charge & commit, not auto-feed.** Merging two same-letter tiles still consolidates them (normal 2048 behavior), but the result is only *charged* (a flat boolean flag, never escalates) — it does not go anywhere automatically. The player taps a charged tile to commit it into the next open guess-bar slot, in whatever order they choose. This is what actually gives the player control over word order.

```js
function commitTile(row, col) {
  if (gameOver) return;
  const cell = grid[row][col];
  if (!cell || !cell.charged) return;
  const slot = guessBar.findIndex((s) => s === null);
  if (slot === -1) return;

  grid[row][col] = null;                 // commit removes the tile — no replacement spawn
  triedLetters.add(cell.letter);
  guessBar[slot] = { letter: cell.letter, hint: secret.includes(cell.letter), locked: false };
  pruneBoard();                          // see mechanic 3
  if (guessBar.every((s) => s !== null)) submitGuess();
  render();
  checkGameOver();
}
```

**2. Position locking carries across guesses.** Once a guess proves a letter correct at position *i*, that position locks permanently — every future guess bar starts pre-filled with it (rendered with the real `--correct` green immediately, not a coarse hint), and the player only needs to fill the remaining open slots. If locks alone ever fill every slot, the game auto-completes as a win with no extra commit needed:

```js
function startNewGuessBar() {
  guessBar = lockedPositions.map((letter) => letter ? { letter, hint: true, locked: true } : null);
  if (guessBar.every((s) => s !== null)) submitGuess(); // every position already locked -> auto-win
}
```

**3. The spawn pool (and the board) shrinks as you learn.** A letter is *exhausted* once it's confirmed absent from the secret, or every copy the secret needs is already locked in — computed directly against `secret`/`lockedPositions` rather than inferred from per-guess status, which sidesteps duplicate-letter edge cases cleanly:

```js
function isExhausted(letter) {
  if (triedLetters.has(letter) && !secret.includes(letter)) return true;
  const need = secret.split("").filter((l) => l === letter).length;
  const have = lockedPositions.filter((l) => l === letter).length;
  return need > 0 && have >= need;
}
```

Exhausted letters both stop spawning (`weightedRandomLetter` filters them out of the secret-letter and filler pools) *and* get swept off the board immediately (`pruneBoard`, called after every commit and every submitted guess). The board visibly declutters as the player gains information, instead of staying uniformly cluttered for the whole game.

**Watch out: this creates a zero-tile soft-lock if you don't also guard the empty extreme.** Committing and pruning both remove tiles with no guaranteed replacement (unlike a merge, which is always paired with a spawn in the same `move()`). An unlucky sequence — e.g. both filler letters happening to get ruled out early, while few secret-letter tiles have spawned yet — can drain the board to *zero* tiles. This is fatal on its own: an empty board can never produce a valid `move()` (nothing to slide), so `spawnTile()` — which only ever fires from inside `move()` or `newGame()` — never runs again, and the player is stuck forever with nothing to slide or tap. The existing "board locked" safety net doesn't catch this either, because it only checks the *full-and-stuck* extreme (`emptyCells().length === 0 && !canAnyLineMove()`), which is the opposite condition. Guard the empty extreme explicitly, symmetrically with the full-board shuffle safety net, at the top of `checkGameOver()`:

```js
if (emptyCells().length === SIZE * SIZE) {
  spawnTile();
  spawnTile();
  render();
  return;
}
```

General lesson: any mechanic that removes tiles without a compensating spawn needs its own explicit floor check, not just a ceiling check — "stuck because too full" and "stuck because too empty" are both real failure modes once removal isn't strictly 1-for-1 with spawning.

**4. A stuck board reshuffles instead of ending the game.** `checkGameOver` no longer treats "full board, no legal move" as an automatic loss — it retries `shuffleBoard()` (a full Fisher-Yates over all 16 slots, including empty ones) up to a small bounded number of times first, and only ends the game if truly nothing helps (the pathological case: zero duplicate letters anywhere on the board). The player also gets a couple of manual reshuffles (same `shuffleBoard()` helper) to use proactively.

Commit-as-reward detail: the instant a tile is committed, it gets a coarse "is this letter in the word at all" hint (`secret.includes(letter)`), rendered as a small corner dot — deliberately *not* the same visual treatment as the final green/yellow/gray, since the coarse hint can legitimately "flip" once true duplicate-aware scoring resolves (e.g. hinted-present later shown absent because an earlier correct match already consumed the only real copy). That's expected behavior, not a bug — the visual distinction is what keeps it from reading as one.

## The balance considerations this combination creates

The 2048-style skill already warns that a large value space breaks merge frequency — the "natural" choice of spawning by general English letter frequency is still a 26-value space, and on a 4x4 board a version with no other mitigations locks up in ~15-20 moves with zero guesses completed, regardless of strategy.

Two independent things now mitigate this, and their combined effect **has not been fully re-measured** — treat any specific numbers below as a starting point to verify, not settled fact:
- **Static bias** (unchanged from the original fix): bias spawns toward the secret word's own letters plus a small (~2) pool of filler letters chosen once per game (`SECRET_BIAS = 0.6`, `FILLER_COUNT = 2`).
- **Dynamic pruning** (new): the exhausted-letter mechanic above independently shrinks the live alphabet over the course of a game, which should make lockups rarer *and* less severe as a game progresses — but this hasn't been isolated and measured on its own.
- **The auto-shuffle safety net** also means "moves survived before lockup" is no longer a meaningful failure metric at all — a stuck board no longer ends the game, so track **guesses reached / win rate** instead when balance-testing.

Don't stop at "it looks like it's balanced" — validate with automated play, and the bot **must both slide and commit now**: a slide-only bot can never reach a single guess under this design (nothing enters the guess bar without an explicit commit), so omitting commits from a bot produces a universal 0-guesses result that's a testing artifact, not a real signal.
- A **greedy bot**: each turn, either commit any charged tile (prioritizing letters not yet tried), or if none are charged, slide in whichever direction produces the most merges.
- A **fixed-preference bot** for the slide component (e.g. always try down, then left, then right, then up — classic 2048 corner-stacking), combined with the same commit-when-possible rule.
- Run each ~8-10 times, log guesses reached and win rate. If neither strategy ever reaches multiple guesses, the pool is still too large or the board too small.
- Note: a low win rate from a naive bot doesn't necessarily mean the game is unwinnable for a human — a bot that commits greedily isn't optimizing for the actual skill (choosing commit *order* to spell the word correctly), so it will underperform a human who understands that. Communicate this in the game's own instructions/hint text.

**Measured result** with the greedy commit-priority bot (10 trials, current `SECRET_BIAS=0.6`/`FILLER_COUNT=2`, all four mechanics active): **10/10 wins**, average 4.0 guesses reached, average 31.3 moves per game. This is a large swing from the pre-locking/pre-pruning/pre-shuffle version's 0/10 — locking and pruning alone (without even accounting for the shuffle safety net) were enough to make even a naive bot win consistently. If a future change makes the game feel *too* easy, this is the number to watch — it's currently generous, not tight.

## Fun pass 2: daily mode, stats, share, sound, animation

Once the core loop is solid, these five additions (all independent of each other except where noted) are what "make it more fun" concretely turned into. Build/verify them roughly in this order — daily/stats/share/sound are low-risk and additive; animation is the one architectural change and should go last, once everything else is confirmed stable.

**Daily word + tracked Practice split.** A deterministic day-index (`Math.round((today - EPOCH) / 86400000)`, using local calendar dates via `new Date(y, m, d)` — not UTC, so "today" matches the player's own clock) picks `WORDS[dayIndex % WORDS.length]`. Exactly one Daily attempt is tracked per day: a completed result is saved to `localStorage` and, on any later visit that same day, replayed via `restoreCompletedDaily()` instead of letting the player retry — the saved board layout isn't needed (it's not persisted), only the finished `guesses`/`won`/`moves`, since the overlay covers the board anyway. Restart always starts an untracked Practice game with a random word; the Daily is never reachable through Restart, only through a dedicated button that checks "already played today" first. Any UI that renders history incrementally (see append-only rendering below) needs an *explicit* reset when a full result is swapped in wholesale like this — `restoreCompletedDaily` doesn't go through `newGame()`, so it has to separately re-zero the render-tracking counters `newGame()` would normally reset.

**Stats/streaks, gated strictly by mode.** Persist aggregate stats (games played, wins, current/max streak, a guess-count histogram) in one `localStorage` key, written only inside the win/loss handler and only when the just-finished game was Daily — Practice games must never touch this key, so the mode check has to happen at the write site, not just be assumed. A streak "continues" only if the last completed day was exactly `dayIndex - 1`; any bigger gap resets it to 1 on a win (or 0 on a loss) — this is what makes a streak mean "consecutive days," not just "total wins."

**Share text.** The classic Wordle spoiler-free format (a header line + one emoji row per guess, 🟩/🟨/⬜ from the already-tracked `statuses`) needs zero new tracking — it's a pure function of data the guess-evaluation logic already produces. Clipboard access should degrade gracefully: try `navigator.clipboard.writeText`, fall back to a hidden `<textarea>` + `document.execCommand('copy')`, fall back further to `window.prompt` with the text pre-filled (always works). Gate the button's visibility on the same mode check as stats.

**Sound via synthesized tones, not audio files.** `AudioContext` + a couple of `OscillatorNode`/`GainNode` pairs per sound is enough for short game-feel blips (merge, commit, a newly-locked position, win, loss, shuffle) — no binary assets, which matters for the self-contained single-file packaging this game already needs. The autoplay-policy gotcha: browsers require `AudioContext` creation/resume to trace back to a user gesture. As long as every sound-triggering function is only ever called synchronously from an existing `keydown`/`touchend`/`click` handler — audit this explicitly, don't assume it — creating the context lazily on first use satisfies the policy with no extra plumbing. One easy bug: firing a "win/loss" sound from the same function that also runs on page-load restore (`finish()` runs in both the fresh-completion path and the `restoreCompletedDaily` replay path) — gate the sound (and any other "reward" side effect) on a `persist`/"is this a fresh completion" flag, or a jingle fires just from loading the page.

**Animation: the identity problem.** The reason a naive re-render can't animate: if `render()` tears down and rebuilds every DOM node from scratch every call (`innerHTML = ""` + rebuild), a freshly created element has no prior `transform`/`opacity` to transition *from* — the transition property is inert even if it's declared in CSS. The fix is a reconciliation render: give every tile a stable id at creation, keep a persistent `Map<id, element>` across renders, and diff against it — an id still present just gets its position updated (the CSS transition animates the glide); an id no longer present gets an exit class and is removed after the transition (with a `setTimeout` fallback in case `transitionend` never fires, e.g. if `prefers-reduced-motion` or a zero-duration edge case skips the event); an id never seen before gets an entrance class. This one rule (new id → entrance, missing id → exit, else → reposition) uniformly covers ordinary spawns, merge results, and any other code path that adds/removes tiles (an empty-board safety-net replenish, an auto-shuffle) without needing those call sites to know anything about animation.

Positioning: switch the tile layer from CSS Grid auto-placement to `position: absolute` tiles driven by a single `transform: translate(var(--x), var(--y)) scale(var(--pop))` composed from CSS custom properties — composing everything into custom properties (rather than setting `transform` directly in JS *and* separately in a CSS `:active`/entrance rule) avoids the two fighting over which one wins, since both paths just set different `--x`/`--y`/`--pop` values feeding the same one `transform` declaration. Compute pixel positions from the container's own padding/gap (read back via `getComputedStyle` custom properties, not hardcoded numbers, so JS and CSS can't drift apart) and live `clientWidth`, recomputed via `ResizeObserver` since the board is responsive — briefly suppress the transition during a pure resize-driven reposition (a `.no-anim` class + forced reflow before removing it) so resizing itself doesn't look like a slide.

Keep the background grid (the empty-slot placeholders) as a separate *static* layer from the animated tile layer — a static CSS Grid of decorative background cells underneath, and the identity-tracked absolutely-positioned tiles in a plain overlay div on top. Trying to animate the same elements that also serve as "there's nothing here" placeholders conflates two different jobs and complicates the diffing logic for no benefit.

**Return values you already compute but were discarding are the cheap way to feed a presentational layer without touching game logic.** `slideLine()` already builds a `merges` list every call; `spawnTile()`/`pruneBoard()` already know exactly which tile ids they touch. Returning that data (instead of `true`/`false`/nothing) and having the sound/animation layer consume it costs nothing logically — verify with a grep that no *existing* caller reads the old return value in a way the richer one would break, and the game's core control flow (`move`, `commitTile`, `submitGuess`, `checkGameOver`, `evaluateGuess`, `isExhausted`) doesn't need to change at all.

**Test-only slow-motion, not real-time races.** A `?testSlowAnim=1` query flag multiplying the animation duration constant (and any `setTimeout` derived from it) 10x turns "is this really interpolating, not snapping" into an assertion you can make deterministically (sample `getComputedStyle(el).transform` at t=0, t=duration/2, t=duration+buffer and assert all three differ) instead of a flaky race against real transition timing.

## Online leaderboard: real cross-player ranking with zero paid hosting

A local stats/streak key (see Fun pass 2 above) only ever compares a player against themselves. "A real leaderboard" means other people's scores, which means a shared backend — the first genuine network dependency this game has had. The constraint that shapes everything below: **no paid hosting.** That rules out anything requiring a always-on server you provision and pay for.

**Backend choice: Supabase over a plain database.** A bare Postgres (or DuckDB/MotherDuck) instance has no story for "a browser can talk to it directly and safely" — you'd need to write and host a server-side API in front of it just to keep write access from being wide open, which reintroduces the "needs a server" problem. Supabase's specific value here is the **anon key + Row Level Security (RLS)** pattern: the anon key is *meant* to be public (embedded directly in client JS, committed to the repo even), and RLS policies at the database level are what actually decide what an anonymous request can do. That combination is purpose-built for "browser talks directly to the database," which a generic Postgres host doesn't give you for free.

**Client library choice: hand-rolled `fetch()` against Supabase's PostgREST endpoint, not the `@supabase/supabase-js` SDK.** This game is deliberately zero-dependency (no `<script src>` to anything external) — pulling in a CDN-hosted SDK would itself be the first external request, before the actual leaderboard call even happens. The real surface needed is one POST (submit a score) and one GET (fetch a day's scores), which is a handful of lines of plain `fetch` and doesn't benefit meaningfully from a query-builder SDK at this scale.

**Schema**: one table, outcome metrics only (`day_index`, `player_id`, `player_name`, `guesses`, `moves`, `won`) — no guess grid, since the existing local share feature already covers that and a leaderboard only needs to rank/display.

```sql
create table public.daily_scores (
  id bigint generated always as identity primary key,
  day_index integer not null,
  player_id uuid not null,
  player_name text not null,
  guesses smallint not null,
  moves integer not null,
  won boolean not null,
  created_at timestamptz not null default now(),
  constraint guesses_range check (guesses between 1 and 6),
  constraint moves_range check (moves between 0 and 1000),
  constraint day_index_range check (day_index between 0 and 100000),
  constraint player_name_length check (char_length(player_name) between 1 and 20),
  constraint one_submission_per_player_per_day unique (day_index, player_id)
);
alter table public.daily_scores enable row level security;
create policy daily_scores_select_public on public.daily_scores for select to anon using (true);
create policy daily_scores_insert_public on public.daily_scores for insert to anon with check (true);
-- No update/delete policy for `anon` — RLS default-denies any operation with
-- no matching policy once enabled, so every row is immutable via the public
-- API with no extra REVOKE needed.
```

`player_id` (a client-generated UUID), not `player_name`, is what the unique constraint keys on — two different players both named "Alex" must never collide or overwrite each other.

**Player identity, without accounts.** A `PLAYER_KEY` localStorage entry holds `{ id, name }`, generated once (`crypto.randomUUID()`, with a manual fallback for contexts without it — note `randomUUID` lives on `Crypto.prototype`, so `delete crypto.randomUUID` silently no-ops when testing the fallback; assign `crypto.randomUUID = undefined` instead) and reused thereafter, following the same shape-tolerant-merge/try-catch persistence pattern as every other localStorage key in this file. The player picks/edits a display name via a small modal (reusing the existing `.modal`/`.modal-panel` pattern rather than `prompt()`), pre-filled with a generated `Guest####` name and surfaced automatically on a player's first-ever Daily completion (cheaply detected as "`stats.gamesPlayed` was 0 before this call" — no new flag needed), with an "Edit name" affordance elsewhere for later. Renaming only affects *future* submissions, since rows are insert-only/immutable — a documented quirk, not a bug to chase.

**Honest anti-cheat posture — state the limitations plainly instead of implying more security than exists.** The `CHECK` constraints and one-submission-per-day uniqueness are guardrails against sloppy/accidental bad data (a client bug submitting `guesses: -1`), not real protection against a determined cheater manually POSTing fabricated JSON with devtools open. Concretely and permanently true of this design: `day_index` is trusted as submitted, not re-derived server-side from the word list (doing so would mean mirroring the word list in Postgres and keeping it in lockstep forever); the checks block obviously-absurd values, not a plausible-looking fake win; nothing rate-limits a script from generating unlimited fake `player_id`s to spam entries beyond whatever the API gateway does by default. All acceptable for a free hobby leaderboard among friends — re-verifying gameplay server-side would mean reimplementing the whole game server-side, well outside what "add a leaderboard" should cost.

**Fire-and-forget submission, gated by the exact same condition that already exists.** `submitToLeaderboard()` is `async` but called *without* `await` from inside `finish()`'s existing `if (mode === "daily" && persist)` block — the same gate that already exists for local stats/streak writes. This is what makes Practice-mode completions and the `restoreCompletedDaily()` replay-on-reload path (which calls `finish(result.won, { persist: false })`) automatically submit *zero* requests, with no new guard logic anywhere. `finish()` itself stays fully synchronous; nothing in the win/loss UI flow ever waits on the network. The function is fully try/caught and never throws — a network failure (blocked by CSP, by an environment's egress policy, by the user's own connection) just means the score silently doesn't save, the same tradeoff every other localStorage/network write in this file already makes. A 409 (duplicate day+player) is caught and treated as expected, not an error.

**Fetching and rendering**: `fetchLeaderboard(dayIndex)` does throw on failure (unlike submit) so the caller can distinguish "loading" / "got data" / "failed" — `openLeaderboard()` shows a loading state immediately, then either renders results or falls back to inline error text, never hanging on "Loading…" indefinitely. Winners (`won === true`) are ranked by `guesses` ascending then `moves` ascending as a tiebreak; non-winners are listed separately underneath as an unranked "Didn't finish today: …" line — mirroring the win/loss distinction the share-text feature already makes, rather than hiding losses outright. The row matching the local player's own `player_id` gets a `.you` highlight class.

**Two hosting channels, one unforked codebase — the actual point of choosing Supabase over anything requiring a dedicated server.** A Claude Artifact enforces a strict CSP that blocks all outbound network calls; a plain static host (Vercel/Netlify, free tier, deployed straight from a **private** GitHub repo with **root directory** set to the game's subfolder and **no build step**) doesn't. Both serve the *identical* `game.js`/`index.html`/`style.css` — no environment-variable injection, no separate build. On the Artifact, every Supabase call gets blocked by CSP, caught by the try/catch above, and the leaderboard modal shows "unavailable" — a graceful, expected degradation, not a bug. On Vercel, the same code reaches Supabase and the leaderboard actually works. `SUPABASE_URL`/`SUPABASE_ANON_KEY` are hardcoded directly into `game.js` and committed — there's no bundler to inject them through, and (per the anon-key-is-meant-to-be-public point above) hardcoding them adds no real risk.

**Testing a fire-and-forget network feature without hitting the real backend.** The mock harness (see `game/tests/`) runs a small static file server that serves the real `game.js` but, when asked, rewrites its `SUPABASE_URL`/`SUPABASE_ANON_KEY` const lines to fake test values via regex — **match the current value by pattern, not by matching today's exact literal text.** An earlier version of this harness matched the *empty-string placeholder* literally; the moment real credentials were wired in to replace that placeholder, the replace silently stopped matching anything, and tests began firing real, unmocked requests at the live Supabase project instead of the intended fake endpoint (caught before it did any damage — the sandbox's own network egress policy independently blocked the host, so no test data actually reached the real table, but a looser or unblocked network would have let it through unnoticed). The lesson generalizes: **any test-time patch that matches by exact current value, rather than by shape/pattern, will silently stop working the moment that value legitimately changes** — and because the failure mode is "requests go somewhere else and still get *a* response," it doesn't necessarily manifest as a loud test failure.

Playwright's `page.route()` then intercepts requests to the fake URL and returns scripted responses, letting you assert: a Daily win fires exactly one correctly-shaped POST; Practice-mode and replay-on-reload completions fire *zero* requests; fetch results sort and partition (winners/losers) correctly; an aborted route (simulating a network failure) never throws and always shows inline error text instead of hanging; identity creation is stable and `Guest####`-shaped, including exercising the `crypto.randomUUID` fallback. A *separate* test explicitly forces empty-string credentials via the same override mechanism to verify the "no credentials configured" degradation path, rather than relying on whatever the currently-committed file happens to ship with — that assumption breaks the moment real credentials replace the placeholder, exactly like the bug above.

**What can't be tested from a sandboxed dev environment.** RLS/constraint behavior against the *real* Supabase project (does a duplicate submission really 409? does UPDATE/DELETE really no-op under RLS? does an out-of-range value really get rejected?) requires an actual network call to the live project — which a sandboxed coding environment's own egress policy may block entirely, independent of anything CSP-related. When that happens, hand off a small standalone verification script (curl or a PowerShell equivalent, since not every user's shell is bash) with the exact commands to run from a machine that does have unrestricted network access, rather than assuming the check can be automated end-to-end from wherever the code is being written.

## Packaging for distribution (mobile / no-build-step contexts)

If the game needs to be opened directly as a file, or published as a Claude Artifact, bundle everything (word list, game logic, styles) into a **single self-contained HTML file** — inline `<style>` and `<script>`, no separate `.js`/`.css` requests. Artifacts enforce a strict CSP that blocks external requests entirely, and separate local files add friction for zero benefit at this scale.

For actually getting that file in front of the user (Artifacts vs GitHub Pages vs direct file share vs gist, and the specific failure mode each one hits), see the `browser-game-hosting` skill.

One game-specific packaging note: include a **visible on-screen direction pad**, not just swipe/keyboard — some embedding contexts don't reliably deliver touch gesture events, and a pad is a zero-cost fallback.

## Testing checklist

1. Play through headlessly with Playwright (or similar) against a static file server — screenshot the initial board and an in-progress state, check `console --errors` for thrown exceptions.
2. Verify game-over triggers correctly on both win (exact guess match) and loss (guesses exhausted — a stuck board should almost never end the game now, see mechanic 4), and that the secret word is revealed on loss.
3. **Charge/commit**: merging produces a `.charged` tile; tapping it removes it from the board (no compensating spawn) and appends it to the guess bar with an immediate coarse hint marker, visually distinct from the final `.correct`/`.present`/`.absent` colors.
4. **Locking**: a guess that proves a position correct pre-fills that slot (green, not a hint dot) in every subsequent guess bar; `commitTile` correctly skips locked slots and fills the next open one; locks alone filling all slots auto-wins with no hang.
5. **Pruning**: confirm a letter that's exhausted (ruled out, or fully locked) is cleared from the board immediately (not just future spawns) — test the duplicate-letter edge case specifically (a letter needed twice shouldn't prune after only one lock).
6. **Shuffle**: seed a full, stuck board and confirm `checkGameOver` reshuffles instead of ending the game; separately seed a board with zero duplicate letters anywhere and confirm it still correctly (and quickly) falls through to game-over rather than hanging. Confirm the manual shuffle button decrements, disables at zero, and a disabled button can't be forced via a real click (test the guard function directly instead of fighting Playwright's actionability check).
6a. **Empty board**: seed a fully empty grid (`grid = Array.from({length: SIZE}, () => Array(SIZE).fill(null))`) and call `checkGameOver()` directly — confirm it replenishes at least one tile and `gameOver` stays `false`, rather than soft-locking. Also confirm a board with just 1 tile is left alone (not force-replenished) — only the literal zero-tile case should trigger it.
7. Run the greedy-bot and fixed-preference-bot balance tests above (both must commit, not just slide); use guesses-reached/win-rate — not moves-survived — as the metric, and update `SECRET_BIAS`/`FILLER_COUNT` in this doc if the results say the old values no longer fit.
8. **Daily/Practice**: pin `Date` (e.g. via `page.addInitScript` wrapping the constructor) to get a deterministic day index; confirm the secret matches the expected day-indexed word; confirm Restart always lands in Practice; force-complete a Daily, reload with the same pinned date, and confirm the result is restored (not replayed) with the board non-interactive — note the board is *intentionally* empty in this state (no `.cell` tiles, just background placeholders), so wait on the overlay becoming visible, not on a board tile, or the test will hang; advance the pinned date a day and confirm a fresh Daily is offered.
9. **Stats**: drive several scripted Daily completions (including a skipped day) and assert the persisted stats match expected streak/distribution behavior, especially the streak-break-on-missed-day case; assert a Practice completion leaves the stats key byte-for-byte unchanged.
10. **Share**: grant clipboard permissions and assert the copied text exactly matches the expected header + emoji grid for a scripted guess sequence; assert the share control is absent after a Practice completion; separately stub the Clipboard API to `undefined` and confirm the fallback chain doesn't throw.
11. **Sound**: stub `AudioContext` (a fake oscillator/gain that logs instead of playing) and assert each trigger point (merge, commit, newly-locked position, win, loss, shuffle) fires exactly the sounds it should; confirm mute suppresses everything and persists; confirm a *restored* (not fresh) completion does not fire the win/loss sound.
12. **Animation**: under the slow-motion flag, sample a tile's `getComputedStyle().transform` at rest, mid-transition, and after settling, and assert all three differ (genuine interpolation, not an instant snap); confirm entrance/exit classes appear and clean up with no orphaned elements left in the DOM; confirm repositioning after a viewport resize matches freshly recomputed metrics.
13. **After any change touching shared render/state architecture (like the animation rework), re-run the *entire* checklist above end to end — not just the tests specific to what changed.** Adding tile ids and switching `render()` to reconciliation changed how empty board states are represented in the DOM (no `.cell` elements for empty slots anymore), which silently broke an assumption in the *Daily/Practice* test's wait condition even though that feature's own logic was untouched. Re-running only an animation-specific test subset after a broad architectural change would have missed this.
14. **Leaderboard** (see the section above for the full rationale): with a mocked Supabase endpoint, assert a Daily win fires exactly one correctly-shaped POST; assert Practice-mode and replay-on-reload completions fire *zero* requests; assert fetched rows sort winners by guesses-then-moves with losses in a separate unranked line; assert a `.you` row highlight matches the local player's own id; simulate a network failure (aborted route) and confirm no thrown errors plus inline error text instead of a hang; assert identity creation is `Guest####`-shaped and stable across calls, including the `crypto.randomUUID` fallback (shadow it with an own `undefined` property, not `delete` — see above); assert the name modal opens only on the first-ever Daily completion and a rename only affects later submissions. Separately, if real Supabase credentials are reachable, run the RLS/constraint checks (insert, duplicate→409, update/delete no-ops, out-of-range→rejected) against the live project — from a machine with unrestricted network access if the dev environment's own egress policy blocks it.

## Reference implementation

`game/` in this repo — `index.html` + `style.css` + `game.js` + `words.js` for the multi-file dev version, plus `game/tests/` (a small Playwright harness: a static file server in `tests/lib/server.js` that can patch in fake Supabase credentials, browser/date-pinning helpers in `tests/lib/browser.js`, and `tests/leaderboard.test.js` covering everything in item 14 above — the first committed test infrastructure in this repo, previously this kind of verification was only ever ad-hoc scratch scripts). `game.js` also holds the daily/practice mode, stats/streak persistence, share text, sound recipes, the full tile-reconciliation animation architecture, and the leaderboard/player-identity code described above.
