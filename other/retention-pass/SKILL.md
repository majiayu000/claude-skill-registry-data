---
name: retention-pass
description: 'Run a 3-round YouTube-retention optimization pass on an animated explainer video (GSAP or CSS-only harness) — audit the hook/peak loop, kill dead zones, align scene length to choreography, add late B-beats, then verify with freeze-frames. Use when the user wants a video "optimized for retention", a "retention pass", or before publishing/recording VO for any explainer.'
user-invocable: true
---

# Retention pass — the 3-round method

Retention is lost at specific, predictable places: a weak first half-second, a hook that promises something the peak never pays, scenes that keep running after their choreography dies, and endings that signal wrap-up early. This skill turns those into a mechanical audit + ranked fixes. It applies to both harnesses (the `gsap-explainer` timelines and any CSS-only delay-driven harness).

**Run it BEFORE VO is recorded** — that's when durations are still free. After VO, durations are locked and only beat-adds are allowed.

## The audit (do this before touching anything)

1. **Beat map.** For GSAP files run `node tools/beat-audit.mjs <file.html>` (in this skill folder) — it walks every `ACTS[i]` timeline against `SCENES` and prints per scene: last-beat time, coverage %, and every gap >4s. For CSS-only files, hand-walk `animation-delay`s per scene against the scene clock. You cannot fix what you haven't mapped; critics who "watch" the file miss gaps the map catches.
2. **Hook/peak loop audit.** Write down: what does the first visual literally SHOW? What does the peak scene show? If they don't rhyme visually, the hook's loop never closes — the #1 structural leak. The lower-third tease must name the payoff in concrete terms and the peak must look like the thing teased. A hook may open TWO loops (peak + trap) if later scenes each close one by name.
3. **First-beat check.** Something meaningful must be landing by 0.5s (a char-cascade kicker starting ≤0.15s passes; a 1.2s fade does not).
4. **Kicker test.** If a kicker could caption any scene, it's a label, not a re-hook. Best kickers close or open a named loop ("The trap from the opening — exposed").
5. **Wrap-up signal check.** Second-to-last scene must be a peak (drill/proof), CTA must chain to a named next video, and nothing may announce duration or "finally/last".

## Round 1 — STRUCTURE (the big rocks)

- **Recut the hook** if the loop audit failed: rebuild the cold open around a visual preview of the peak (same shapes/colors the peak uses, e.g. two bars forced to overlap if the peak is a bar collision). Keep it a QUESTION, never the answer.
- **Trim every scene to its choreography.** Target: last content beat lands at 70–85% of scene duration. Compute new `SCENES` from the beat map, THEN retime any late beats you're keeping (they were placed against the old duration). Flight-plan fractions (`FL`) survive trims automatically; absolute `ACTS` times do not.
- **Sync the VO script doc** (same basename `.md`): new timestamps, new hook VO, and re-read every scene's line count against its trimmed duration (~2.3 words/sec for a relaxed read).

## Round 2 — BEAT COVERAGE (kill the dead zones)

Re-run the beat map after R1 trims. For every scene with coverage <60% or a gap >4s, add a beat — in this cost order:
1. **Move an existing beat later** (free, often the retry/failure beat wants to sit past the 60% mark anyway).
2. **Callback pulse** re-using the scene's own props (the pile shivers, the half-line blinks, the box flexes, the one item takes a bow). 2–3 lines of GSAP, no DOM.
3. **New micro-beat with DOM** only if the scene has a second idea that never got visualized.
Never pad with ambient-only motion — the B-beat must be *content* (it re-states the scene's claim physically).

## Round 2.5 — VO-SYNC (the "say it = show it" audit)

Added after field experience: retention dies quietly when the narrator names something and NOTHING on screen reacts. Walk the transcript sentence-by-sentence, estimate each phrase's speech time word-proportionally, and verify the NAMED object has a beat within ±1.5s. The two chronic defects (found in every video audited): (1) multi-item reveals complete in the first third while the VO enumerates across the whole scene — re-space each item to land on its name; (2) payoff stamps/shatters resolve seconds BEFORE the VO finishes the reasoning — gate them to the earning phrase. Also: any phrase asserting a mechanism needs a dedicated animated mini-diagram, not a caption; longer-and-taught beats shorter-and-asserted.

**Continuous-narration standard (once real VO exists):** the narrator speaks 85–94% of every scene — no dead air before the next line. Write scripts at ~2.5 words/sec × scene duration (a typical cloned/TTS voice reads ~2.6 w/s), generate per-scene clips, and EXTEND any scene its clip overruns (clip + 1.5–2s); extending never strands beats. Added words must narrate on-screen beats (count with the counter, enumerate with the landings), never pad.

## Round 3 — POLISH (the drop-point interrupts)

- **Stakes accents** late in long scenes: a micro-caption or spark tying the beat to the real-world payoff ("this exact move = the result you came for").
- **Pattern interrupts** at predicted drop points (~30%, ~60% of runtime): a mood flip (dark scene), a direction-alternating wipe, a physics burst — something that breaks the established rhythm ONCE.
- **Loop-closure naming:** the peak's kicker should reference the hook explicitly; a second planted loop (the trap) closes in its own scene by name.
- **Exit velocity:** last content scene ends with motion (a hand-off beat at ~85%), not a coast; CTA scene starts inside 1s.

## Verification (non-negotiable, after EVERY round)

- `node --check` the extracted last `<script>` block after any surgery.
- Freeze-frame each new/moved beat: `__xpl.goto(i)` + `__xpl.tl().pause(t)` in the preview browser (its rAF is frozen — this is the only reliable way).
- **Replay-reset audit** for every new tween: does the scene's `gsap.set` reset block cover every property you now touch (including `attr:` fills and infinite `repeat:-1` props)? One-way tweens without resets are the classic replay killer.
- Re-run the beat map; confirm no scene regressed below 60% coverage.

## Field results (calibration for future passes)

Consistent findings across a batch of full-length explainers — EXPECT these:
- **Every scene overran its choreography by 30–100%.** Durations get set to "feel roomy" for VO; measured VO fill was 57–85%. Trims of −25% to −31% of total runtime came out with zero content loss.
- **Every hook failed the loop audit the same way:** the cold open showed the *trap/problem* while the packaging (thumbnail/title) promised the *peak*. Recut recipe that worked every time: rebuild scene 0 from the PEAK scene's exact prop classes (same bars/chips/banner), held as a question, and let the peak's kicker close it by name.
- **The best mid-beats restate the scene's claim physically** (two items retreat to opposite corners to show why they never meet; the single group frame flexes; margin notes ripple). Decorative pulses read as padding — thematic pulses read as teaching.
- Trims strand three kinds of absolute values — retime all three in the SAME edit as the trim: late `ACTS` beats, CSS `animation-delay`s (`.l3`/lower-third), and on-page duration labels (poster sub, chrome time, aria labels, title A/B options in the script md).

## Gotchas learned the hard way

- Trimming `SCENES[i]` does NOT move that scene's absolute `ACTS` beat times — late beats placed at 18s die silently in a 16s scene. Retime them in the same edit.
- The VO doc and the `sr-only` transcript drift instantly; fix both in the same round or they lie to the narrator.
- A hook kicker that references "the opening" in a LATER scene breaks when you recut the opening — grep for kickers that name other scenes before recutting.
- CSS-only harness: adding beats means new `animation-delay` values; check the scene's clock entry, not the previous element's delay.
