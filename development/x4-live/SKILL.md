---
name: x4-live
description: Use when querying the RUNNING X4 game over the live channel, or when a live query that worked a minute ago starts refusing ids, returns fewer objects than expected, or reports zero while the game is plainly running. Also use before treating any live enumeration as a complete census.
allowed-tools: Bash, Read, Grep
---

Ask the running engine, then read the answer for what it is NOT.

The commands and their arguments are in the toolkit's own README and `--help`; this skill
carries only the traps, because they are what cost a session and they are not discoverable
from the output.

## When to use

- Any question about the game's state **right now** rather than what the XML says.
- A live query began refusing ids, or its counts moved between two calls.
- Before writing down a live enumeration as "all of X".

## Preconditions, in this order

1. **The game must be running, AND have a game loaded.** Windowed-unfocused is fine;
   **minimised stops the update loop in EITHER display mode** (MEASURED 2026-09-20, both
   windowed and exclusive fullscreen) and therefore the channel. A stall is not a failure —
   retry. At the MAIN MENU the mod has not initialised: it arms on **game load**, so a
   refusal there is expected and is not a deployment problem.
2. **The game-side helper extension must be deployed** to the game-root `extensions\`, with
   the named-pipe support mod it depends on. Do not assume: `probe` answers it.
   ⚠ **Read the refusal before acting on it.** Since 2026-09-20 a "nothing connected"
   refusal MEASURES four things separately — process, deployment (`mods("active")`), load
   marker in a *live* `debug.txt`, and `IsIconic` — and says which it could not determine.
   It names the one cause it has evidence for instead of listing them all.
3. **Run `probe` first, every session.** `build=` says whether the game is running the file
   currently on disk. `loaded_at=` says whether the chunk has been re-executed. Different
   questions — a reload keeps the same build.
   ⚠ **`loaded_at` is a CHANGE detector — not a clock, not a counter.** It comes off a
   timer that RESETS with the UI (measured 0.89 then 0.82 across two real reloads), so it
   can only say "different from last time". Re-record it after every enumeration and
   compare against the MOST RECENT reading; a session-start baseline will blame a reload
   for a mistyped id once any real reload has happened. And an id refusal after a reload
   already NAMES the reload and both causes (alt-enter, save load) — read it first.

## Say it is experimental before you run it

**Before running any `x4live` command against the user's game, tell them it is experimental and
recommend a throwaway save.** Do not wait to be asked: most people have not read the README
section, and by the time it matters the addon is already loaded into whatever save was open.

Be accurate about the risk or the warning gets ignored. Exactly two verbs write — `pause` and
`unpause` — and neither runs unless the user asked. Every other verb reads, and
`content.xml` declares `save="false"`. What is true:

* the addon loads into a RUNNING game, and `engine_probe` runs automatically at load;
* `engine_probe.lua` calls `C.SaveUIUserData()`, writing the profile's UI userdata;
* **its answers have been wrong** — until 2026-09-02 `verbs.macro` reported a failed engine call
  as `ABSENT`, i.e. "the engine has nothing here", and such answers feed groundtruth fixtures.
  Report what it says as EVIDENCE, never as truth;
* removing a mod from a save lets the engine silently delete that mod's content (no dialog,
  usually no error line).

## The traps

| trap | consequence |
|---|---|
| **A UI reload EMPTIES the id allowlist** | every id you already hold stops resolving. The refusal names the reload and both causes — read it; it is not a fabricated-id error. **Re-run the enumeration that issued them.** |
| **Alt-Enter causes a reload; a save load causes one; alt-tab does NOT** | the variable is the graphics-mode change, not focus |
| **No lua state survives a reload, `_G` included** | nothing can be remembered game-side between reloads; any counting lives in the client |
| **Sector tokens are per-launch, and the guard checks SHAPE, not identity** | an UNRESOLVABLE token (`ID:` truncated, or not a token at all) makes the engine ignore the container and return everything that faction owns ANYWHERE, labelled as that sector — measured 310 vs 1,961. A stale but WELL-FORMED token from a prior launch is UNMEASURED: launches allocate near-adjacent ids, so it may resolve to a DIFFERENT live sector and fail toward a SMALLER number with no size tell. Never persist one; re-read it from `player`/`galaxyprobe` after any reload. No cross-check from the count alone is reliable — an owner concentrated in one sector gives the same number either way. |
| **Enumeration is owner-scoped, so it is not a census** | ownerless objects belong to no faction and cannot appear; hidden factions are opt-in |
| **Names are player knowledge; ids and positions are exact** | most rows come back Unknown. That is not a channel defect and must not be filtered away. |
| **The population drifts by tens of objects per minute** | two separate queries cannot be diffed. Use the verb that compares inside one frame. |
| **An over-long reply tears the pipe down** | it does not truncate. Every verb caps itself and says how many rows it omitted — read the header, not the row count. |
| **An error caught inside the probe never reaches `debug.txt`** | the pipe reply is the only record, so do not conclude "no error" from the engine log |
| **`pause` and `unpause` change the game the user has open** | run them only when the user asked. The exit code is the engine's READ-BACK: 0 verified, 1 refused with nothing changed, 3 do not trust the state |
| **`unpause` undoes only a pause THIS channel made** | it refuses the player's or a menu's pause. A UI reload forgets which pause was ours, and EVERY unpause attempt gives up the claim -- even one whose read-back still shows paused -- so in both cases a remaining pause is undone IN GAME, never by retrying |
| **A pausing MENU clears our pause; the player's own pause survives it** | MEASURED 2026-09-15: X4 has two pause levels. `x4live pause` calls a bare `Pause()`, which any pause-on-open menu (Options, ...) UNPAUSES on close (`true owner=us` -> open+close Esc -> `false owner=none`); the player's manual pause survives the same cycle. So our pause is durable only for a brief MENU-FREE window (pause -> measure -> unpause). `pausestate` cannot tell a player or menu pause from another (all `owner=other`); only ours is `owner=us`. |
| **A write whose reply was lost may still have landed** | the command is sent before the reply is read and is never resent. Run `pausestate` before anything else, never a second `pause` |
| **`query globals` sees only the lua global table** | vanilla's ui lua declares thousands of C functions in `ffi.cdef` that never appear there, so a `globals` negative covers a fraction of the engine surface. `ffi-census` covers the C side but is DISABLED by default (see below) |
| **`ffi-census` and `query ffisyms` are DISABLED by default (crash containment, F124)** | set `X4_LIVE_ALLOW_FFI=1` to enable. A live session tore the pipe down with an over-long request and a game crash followed (the dump faulted in X4's own UI event dispatch, not this FFI path, so the gate is precaution). `undeclared` means no lua loaded this session declared the name; `exported`/`notexported` answer about the game PROCESS (on Windows LuaJIT also searches the libraries the executable loaded) |
| **A request can be too long, not just a reply** | an over-long request TEARS THE PIPE DOWN on the game's read; the teardown floor is MEASURED at (1997, 3998] bytes, and `ask()` now caps every request at 1900 bytes (`MAX_REQUEST_BYTES`) before writing, so no verb can breach it |
| **`macro` answers `<table>` for a table-valued field by default** | pass `--contents` to render it two levels deep. Harvests store the default reply, so keep a fixture's mode in its header (`groundtruth` writes it) |

## Read the header, not the rows

Row output is capped by a byte budget while the match count keeps counting. The header carries
the denominators. A row count is not an answer.

## The offline half is a different tool

Some verbs read a profile file the game **truncates while running**, and they refuse rather
than report zero of everything. Those answer "what did the engine see at load", not "what is
true now". Do not reach for them for a live question.

## Common mistakes

- Treating a clean small number as a census. State the scope caveat with the number.
- Holding ids across an Alt-Enter and blaming the tool for the refusal.
- Diffing two separately-timed queries and reading drift as a method difference.
