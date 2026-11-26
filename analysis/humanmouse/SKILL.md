---
name: humanMouse
description: Make the cursor move like the owner's hand, measured not guessed. Record their mouse with recordMouse.py, fit humanMouse.py to the numbers, run a session and measure ours with the same analyser. Use when motion "looks wrong", when a page needs the cursor to behave differently, or when the owner says "record my mouse", "the mouse moves weird", "too slow", "it never stops".
---

# humanMouse

The cursor is fitted to a recording of the owner's own hand, and every change is
checked with the same analyser that measured them.

## Hard boundaries

1. **Measured, not guessed.** A motion change comes from a number in a
   recording (theirs or ours), never from how it "should" look.
2. **One module drives every session** (`python/human/humanMouse.py`): the async
   inspect/flow sessions (idle loop, preempted by any step) and the sync
   publish/connect/profile sessions (`look()` before a step, `human_click`).
   Nothing clicks with Playwright's own `.click()` in an account session.
3. **humanize stays on**, capped per hop (`own_trajectory=True`).
   Nothing is injected into the page.
4. **Run it live** (rule 26), through Monitor.

## The loop

```bash
# 1. their hand: open a page with our cursor still, record 60 s, analyse
log inspect start --account <a> --url <url> --noIdleMouse --proxyMs 12000
python python/human/recordMouse.py 60                 # "GO": the owner uses the window; prints the summary
#   -> ~/.logCli/mouse/<time>.json and .analysis.json

# 2. ours: a session with the idle loop, a long wait step, the same analyser
log inspect start --account <a> --url <url> --now --proxyMs 12000
log inspect do wait 60
python python/human/recordMouse.py --analyze ~/.logCli/runs/inspect/<run>/steps/02_wait60s/mouseSamples.json
```

Compare: moves, move ms, px per 100 ms, straightness, side px, overshoot
share, where the speed peaks, stillness between moves, share still. Change
the constants in `humanMouse.py` (`duration_for`, `reach`, `loops`,
`rest_for`, `look_for`) toward their numbers, re-measure. The owner's 2026-10-19
recording: 15 moves/60 s, 0.42-0.45 s for 400-800 px, speed peak at 0.34 of
the move, 7/15 overshoot, median pause 0.2 s, still 14-25 %.

## What the recordings taught

- Each `page.mouse.move()` costs ~60 ms of round trip however small the hop;
  with humanize's default curve on top it was 100-530 ms. Draw the
  trajectory ourselves at ~15 Hz and keep humanize's per-hop cap at 20 ms.
- A chain of small moves stutters: each starts and stops. One Bezier walked
  with one velocity profile is a gesture.

What the mouse learned on Facebook's pages: `skills/facebookInspect/SKILL.md` (the facebookBrowser guide).
