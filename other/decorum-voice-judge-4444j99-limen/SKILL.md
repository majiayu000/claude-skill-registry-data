---
name: decorum-voice-judge
description: Judge whether the public PROSE reads professionally — tone, brand-voice, clarity, credibility — and record a content-pinned verdict. Use when DECORVM (the professionalization keeper) queues a "prose changed — re-review voice" finding, or when asked to review/grade how a public README, bio, or positioning doc SOUNDS (not just whether it is spelled right). The deterministic half (spelling, staleness, narrative-accuracy) is scripts/decorum-keeper.py; this skill is its model-in-the-loop voice complement, the sibling of experience-judge.
---

# decorum-voice-judge

`decorum-keeper.py` measures the DETERMINISTIC rungs of professionalization — spelling (vendored typo
map), bio/positioning staleness (git authored age), and narrative accuracy (profile claims vs the
VVLTVS contribution mix). It cannot judge whether the public prose *reads* professionally: tone,
brand-voice, "does this sound like a founder or a first draft." This skill is that missing rung.

The keeper detects when a prose surface's bytes change and no current voice-judgment covers them, and
queues a review (a `polish/voice-judge` finding, and — when the fleet effector is armed — a
**Haiku-tiered** task pointing here). This skill reads the changed surface, scores it, and appends a
verdict **pinned to the exact bytes it judged** (`content_sha256`) to the register, which clears the
finding. A later edit changes the sha and re-queues review — so judge against the CURRENT bytes only.

Tier: **Haiku-first** (per the model-tiering policy). Voice scoring is a bounded, cheap judgment; do
not escalate unless the prose is genuinely ambiguous.

## Steps

1. **Find what's queued.** Run `python3 scripts/decorum-keeper.py --sweep --json` and read
   `egg_face_findings[]` for entries with `source: "voice-judge"` — each names a changed prose
   `surface` (a repo-relative path like `README.md` or `docs/positioning/<x>.md`). Or take the path
   from the task context that invoked you.

2. **Read the CURRENT bytes and compute the sha.** Read the file at that path, then
   `python3 -c "import hashlib,sys;print(hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest())" <path>`.
   This exact hex is what pins your verdict — record it verbatim.

3. **Score the prose 0-5** on four axes (be a demanding reader who represents the target visitor —
   an investor, a hiring manager, a paying customer):
   - **tone** — confident without bluster; not hedging, not cringe, not LLM-boilerplate ("delve",
     "in today's fast-paced world", empty superlatives).
   - **brand_voice** — sounds like THIS operator's estate (precise, systems-minded, build-in-public),
     not a generic template; consistent with the other public surfaces.
   - **clarity** — the value proposition lands in the first sentence; no jargon wall; a stranger
     understands what this is and why it matters.
   - **credibility** — claims are backed (links, numbers, artifacts); nothing reads as vaporware or
     over-claim; no unsupported superlatives.
   - **verdict** = `pass` if every axis ≥ 3 and none is a visible embarrassment; else `fail`.

4. **Append the verdict** to `institutio/observatory/decorum-judgments.yaml` under `judgments:` keyed
   by the surface path (newest row last). This file PUBLISHES — keep every note public-safe (no PII,
   no private URLs, no secrets). Row shape:

   ```yaml
   judgments:
     README.md:
       - judged_at: "<UTC ISO8601, e.g. 2026-07-23T00:00:00Z>"
         content_sha256: "<the hex from step 2>"
         model: "claude-haiku-4-5"          # or your handle if a human judged
         verdict: pass                        # pass | fail
         scores: {tone: 4, brand_voice: 4, clarity: 5, credibility: 4}
         defects: ["opening line buries the value prop under a stack list"]
         suggested_fix: "lead with the one-sentence outcome; move the stack list below the fold"
   ```

5. **Confirm it cleared.** Re-run `python3 scripts/decorum-keeper.py --sweep` — the `voice-judge`
   finding for that surface should be gone (a `pass` row whose `content_sha256` matches the current
   bytes clears it). If it persists, your row's sha does not match the current file — recompute and
   fix the row.

## Laws

- **Pin to bytes, not to the path.** A verdict without the exact `content_sha256` is worthless — it
  cannot be invalidated on the next edit. Always record the hash of the bytes you actually read.
- **Public-safe.** The register publishes; write no PII, no private URL, no secret in any note.
- **Judge current only.** If the file changed after you computed the sha, recompute — never record a
  verdict against bytes you didn't read.
- **A `fail` is a gift.** A specific `suggested_fix` is worth more than the score; it is what the next
  fix task acts on.
