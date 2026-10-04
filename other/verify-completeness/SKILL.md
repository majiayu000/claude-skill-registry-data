---
name: verify-completeness
description: Arc-completeness gate. Re-reads each picked span's ASSEMBLED arc (the words inside its cuts) plus a tail lookahead and asks Claude whether the short LANDS as a standalone story — setup → turn → real landing, not an abrupt "so what?" stop. When the payoff is cut off but recoverable in the immediate source tail, it nudges t1 (and the last cut's end) OUTWARD to the landing sentence, within dmax. The outward counterpart to verify-bookends (inward-only). Runs after bookend-trim, before cut-clip, in SOURCE coordinates. Non-fatal, idempotent, disable with VERIFY_COMPLETENESS=0.
allowed-tools: Bash
user-invocable: true
---

# verify-completeness

`verify-coherence` only checks that a span stays on ONE topic; `verify-bookends`
only inspects the first/last 1.5s of the already-cut clip and is deliberately
inward-only. Neither ever re-reads the WHOLE assembled story to confirm the arc
still LANDS. A pick whose payoff sits one sentence past the chosen `t1` reads as
truncated — the channel's "cut off early" feeling.

This gate fills that hole. For each span it shows Claude the assembled arc (the
text inside the span's `cuts`, in order) plus a **tail lookahead** — the source
lines right after the current end, bounded by the remaining `dmax` headroom —
and asks for one verdict:

- `complete` — the arc lands; no change.
- `needs_more_tail` — the landing is cut off but present in the lookahead;
  Claude returns `extend_t1`, a source line-end boundary, and the span's `t1`
  (and last cut's end) are nudged outward to it, capped at `dmax`.
- `truncated` — abrupt but not recoverable within the lookahead/budget; flagged,
  left unchanged.

## Why source coordinates / why here

Outward extension is only clean BEFORE `cut-clip`: once a clip is cut, trimmed,
and pace-tightened, the clip-local transcript has discarded source timestamps
(see `rebase.py`), so re-deriving where to extend in the source would mean
re-running the whole trim/tighten sub-chain. Running in source coords right
after `bookend-trim` lets any extension flow naturally through cut → trim →
tighten. This complements `verify-bookends`, which owns inward post-cut cleanup.

## Usage

```bash
verify-completeness.sh <segments.json> <transcript.json> <out.json> [dmax=55]
```

- Batches all spans into ONE Claude call.
- Non-fatal: any Claude/parse failure passes segments through unchanged.
- Idempotent: skips when `out` is newer than both inputs.
- `VERIFY_COMPLETENESS=0` disables (passthrough copy).
- Biased toward `complete`; only a short, clearly-landing tail triggers an extend.

Writes `segments.json` with `completeness_verdict` / `completeness_note` (and an
updated `t1`/`cuts` on a successful extend) into each span.
