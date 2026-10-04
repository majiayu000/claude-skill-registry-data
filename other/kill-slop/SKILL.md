---
name: kill-slop
description: Audit a file or draft for AI slop and off-voice lines against the author's bound voice, report findings with in-voice swaps, then apply approved fixes. Use when the user says "kill slop", "/kill-slop [file]", "find the slop in this", "audit this for slop", or wants a deck, article, page, or draft cleaned to sound like them. Wraps the anti-slop skill with a voice binding and a fix workflow. NOT a detector-evasion tool, and NOT for text with no voice to bind.
---

# kill-slop

Audit-and-fix workflow for any voice-bearing file. The argument is a file path or a pasted draft. If neither is given, ask which file.

## Setup (once)

Point step 1 at the author's voice. In priority order:

1. A voice file the author maintains (put its path in step 1 below).
2. 5+ real writing samples, from which you build a voice card on the fly (`anti-slop/references/voice-binding.md`).
3. A named register the author states.

None of the three available: stop and say so. Auditing against a default banlist manufactures false positives on real human writing. The anti-slop contract governs here.

## Steps (follow exactly)

1. **Load the anti-slop skill in AUDIT mode** and its full catalog at `../anti-slop/references/master-list.md` (installed: `~/.claude/skills/anti-slop/references/master-list.md`). Before flagging anything, read the author's voice file in full (the path you set in Setup). That file sets the caps, not any default banlist.

   **If this session (or any agent in it) wrote or edited the target text, do not audit it yourself.** Spawn a fresh-context subagent that never saw the drafting, hand it this skill plus the voice file, and relay its findings. The author of a draft is the worst judge of it.

2. **Read the whole piece twice.**
   - Pass one: sweep for catalog tells. Clusters of 3+ within ~100 words count; single hits are noise.
   - Pass two: read as a stranger hearing it out loud. This is where the real catches are: robot words, padding that restates a headline or kick, lines that contradict each other, logic that doesn't hold, terminology that drifts between sections, triplets-for-rhythm, anything the author wouldn't actually say. A clean word-list pass is not a clean audit.

3. **You did not write this and you don't get credit for liking it.** If a prior session or agent produced it, that makes you MORE suspicious, not less. Fresh judgment is the whole point of this skill.

4. **Report before touching anything:**
   - Slop score before (anti-slop rubric).
   - Every flagged line with its location (slide/section/line), why it fails, and a swap written in the author's voice. Check each swap against the voice file: keep their irregularities, fix toward their words, never toward neutral.
   - What's clean and must not be touched (their numbers, refrains, named things, signature moves).

5. **Wait for the go, then apply exact-string edits only from the approved list.** One fix pass, two max. Do not polish anything unflagged, do not sand. Report the after score. If the user says "just fix it" or "no need to ask" up front, skip the gate and apply, but still show the full before/after report.

6. **Zero findings is a claim, not a shrug.** If nothing fails, say what was checked and where problems would hide anyway. "It's clean" with no evidence means the audit didn't happen.

## Handoff variant

If the user says to hand the fixes to another agent instead of applying them: write a CHANGE file next to the target with exact OLD/NEW strings (preserve HTML entities if the target is HTML), the do-not-touch list, a grep verification step, and the line "this is the single fix pass, do not polish further".

## Related

- `anti-slop`, bundled in this repo: the underlying method and tell catalog.
