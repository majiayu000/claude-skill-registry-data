---
name: end-card
description: Composite a closing CTA banner ("FOLLOW FOR MORE" + @C0BALT_CUT) over the last ~2.5s of a finished short so it lands on an intentional beat instead of dead-stopping on a dangling word. Timeline-preserving (audio copied, duration identical), deterministic, non-fatal. END_CARD=0 skips.
---

# end-card

Closing-beat overlay. Runs in the finishing phase AFTER `bg-music` and BEFORE
`qc-clip`, the last visual touch before the short is saved. Addresses the
"ends abruptly / no loop or CTA" retention leak: the few viewers who reach the
end get a branded call-to-action instead of a hard stop on a half-finished
word.

```
end-card.sh <in.mp4> <out.mp4> [dur=2.5] [line1="FOLLOW FOR MORE"] [line2="@C0BALT_CUT"]
```

- **Timeline-preserving.** The card is an overlay that fades in over the final
  `dur` seconds of the existing footage. Audio is stream-copied; total duration
  is unchanged, so no downstream timestamp moves.
- **Brand.** Impact, Platinum `#E8ECF1` headline + Sapphire Glow `#2E6BFF`
  handle, thick black stroke — rendered by `render_endcard.py` to a transparent
  PNG (the stack has no drawtext/libass), composited by ffmpeg.
- **Placement.** Centered horizontally; vertical center at `END_CARD_Y_FRAC`
  (default 0.60) so it sits above the lower-third caption band.
- **Idempotent** via `.ecmeta` signature. **Non-fatal**: any probe/render/encode
  failure falls back to a stream-copy passthrough. `END_CARD=0` disables.

Knobs: `END_CARD` (0 disables), `END_CARD_DUR` (default 2.5), `END_CARD_TEXT`,
`END_CARD_HANDLE`, `END_CARD_Y_FRAC` (default 0.60).
