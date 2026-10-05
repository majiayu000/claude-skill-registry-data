---
name: humanize-text
description: Rewrite AI-sounding prose so it reads as considered human writing — cut the tells (em-dash pile-ups, "it's not X, it's Y" antitheses, inflated vocabulary, uniform rhythm, empty uplift) while preserving every fact, claim, and the author's own voice. Use when the user says "make this not sound like AI", "de-AI this", "humanize/humanise this", "this reads like ChatGPT", "remove the AI tells", "it sounds robotic/generic", or shares a draft (post, email, essay, docs, cover letter) to sharpen into a more human voice. Ships a stdlib scanner that flags the mechanical tells.
---

# Humanize Text

Take a draft that reads as machine-generated and rewrite it so it reads like a
person with a point of view wrote it. Humanness comes from three things —
**rhythm** (uneven sentence lengths, the odd fragment), **specificity** (real
names, numbers, examples instead of abstractions), and **a stance** (an opinion,
some friction, a thing the writer actually cares about). It does *not* come from
adding typos or forced slang. Fix the writing; don't fake the human.

This is a **quality** operation, not a disguise. See the honesty note before you
start.

## The honest goal (read first)

The aim is prose that doesn't read as generic AI, because generic AI prose is
*bad writing* — vague, over-hedged, weightless. The aim is **not** to defeat
AI-detection tools (they're unreliable in both directions), and **not** to pass
AI-written work off as human where disclosure is required or the rules forbid it
(academic submissions, contexts where authorship is certified). If the user's
goal is to launder undisclosed AI work past an integrity policy, say so plainly
and decline that framing — you can still help them *write better*. Everywhere
else — their own LinkedIn post, blog, email, cover letter, docs — improving the
prose is exactly the job.

## Step 1 — Pin the target voice and constraints

Do this before rewriting a word. Getting the voice wrong is worse than the AI
tells, because it misrepresents the author.

1. **Whose voice?** Ask for (or find) a **sample of the author's real writing** —
   an old post, an email, a Slack message. Match its register: formal or loose,
   contractions or not, dry or warm, British/US/AU spelling. If no sample
   exists, infer a sensible register from the medium and audience and *say what
   you assumed* so the user can correct it.
2. **Medium & limits.** LinkedIn post, cover letter, README, marketing email,
   essay? Note hard constraints: length/character limits, banned claims, whether
   a house style applies. A de-AI pass must respect these.
3. **What must not move.** Facts, numbers, names, citations, the structure of the
   argument, and any legally/PR-gated claims. This pass changes *how* it reads,
   never *what it asserts*.

## Step 2 — Diagnose

Run the scanner, then read with your own eyes — the scanner catches the
mechanical tells; you catch the tonal ones.

```bash
# Global install (default):
SKILL=~/.claude/skills/humanize-text
# ...or project install: SKILL="$(git rev-parse --show-toplevel)/.claude/skills/humanize-text"

python3 "$SKILL/scripts/flag_tells.py" draft.md         # readable report
python3 "$SKILL/scripts/flag_tells.py" draft.md --json  # machine-readable
```

The scanner reports em-dash density, **burstiness** (sentence-length variation —
low means robotically uniform), inflated/cliché vocabulary with line numbers,
signpost/hedge phrases, and formulaic patterns. It flags; it never rewrites, and
none of its signals *proves* AI authorship — a strong human writer trips a few on
purpose. Use it to focus the read.

### The tell taxonomy (what to look for)

**Lexical**
- Inflated vocabulary: *delve, leverage, robust, seamless, harness, foster,
  unlock, elevate, testament, tapestry, myriad, landscape, realm, paradigm.*
- Empty intensifiers: *truly, incredibly, remarkably, significantly, deeply,*
  and a fog of `-ly` adverbs.
- Corporate uplift: *game-changer, cutting-edge, transformative, unparalleled.*

**Rhetorical / syntactic**
- **Em-dash overuse** — the loudest single tell.
- **Antithesis on a loop:** "It's not just X, it's Y." "This isn't about A. It's
  about B." One is a fine rhetorical beat; three in a post is a fingerprint.
- **Chiasmus / mirror sentences:** "The determinism makes the non-determinism
  safe." Clever, balanced, and unmistakably machine.
- **Rule of three everywhere:** every list is a tricolon; every idea comes in a
  neat triad.
- **Sweeping "from X to Y"** openers and **"In today's …"** scene-setting.
- **Colon-setup → tidy list**, over and over.
- **Rhetorical question → immediate answer.** "The result? …"
- **Signposting:** *Furthermore, Moreover, Notably, Ultimately, In conclusion.*

**Tonal / structural**
- Relentless positivity, no friction, no opinion, nothing at stake.
- Abstraction over specifics — no names, no numbers, no concrete example.
- Uniform paragraph lengths; a summary paragraph that restates everything.
- Both-sides hedging that commits to nothing.

## Step 3 — Rewrite

Apply the fixes, in rough priority order:

1. **Break the rhythm.** Put a three-word sentence next to a twenty-word one. Use
   a fragment. Start a sentence with "And" or "But" if the register allows.
   Burstiness is the fastest win.
2. **Cut the em dashes** to one or two. Most become full stops or commas; some
   dissolve by restructuring the sentence.
3. **Swap inflated words for plain ones.** *utilise → use, leverage → use,
   robust → solid/works, delve into → look at.* If a word would feel odd out
   loud, cut it.
4. **Replace abstraction with a specific.** A number, a name, a real example.
   This is what actually convinces — and it's the thing generic AI can't fake.
5. **Break the parallelism.** Vary list lengths; let one item run long. Kill the
   chiasmus. Reduce the "not X, it's Y" beats to at most one.
6. **Add a stance.** Let the writer prefer something, doubt something, find
   something boring or hard. A single honest opinion does more than any word swap.
7. **Delete the throat-clearing and the summary.** Hedges ("It's worth noting"),
   signposts, and the closing paragraph that repeats the post usually just go.
8. **Keep contractions and idiom** natural to the author. Don't over-formalise;
   don't force slang the author wouldn't use.

Do **not**: introduce spelling/grammar errors to "seem human", swap in a
different affectation (forced quirkiness is its own tell), or pad length. Shorter
and specific beats longer and smooth.

## Step 4 — Preserve-check

Before handing back, diff the meaning, not just the words:

- **Every fact, number, name, and claim** in the original is still present and
  unchanged. A de-AI pass that quietly alters a statistic or softens a claim has
  failed, however human it now reads.
- **Voice matches** the sample/register from Step 1 — not *your* default voice.
- **Constraints hold** (length/char limits, house style, gated claims).
- If cutting a tell would require changing a claim, **stop and flag it** rather
  than editing the claim to fit the prose.

## Step 5 — Hand back

- Give the rewritten text.
- Then a short **changelog**: the specific tells you removed (e.g. "em dashes
  8 → 2; cut 3 antithesis constructions; replaced 'leverage/robust/seamless';
  varied sentence length") so the user learns the pattern, not just the result.
- Flag anything you **couldn't** fix without touching a claim, and any place the
  voice was a guess.
- Offer, don't assume, the next step: apply to a whole series, tune the voice
  from a fresh sample, or re-scan the rewrite to confirm the tells dropped.

## Guardrails

- **Content is sacred; only style moves.** Never change a fact, number, or claim
  to make a sentence flow better. Flag, don't fudge.
- **Voice fidelity beats de-AI-ing.** Rewriting a user's words into a slick
  neutral voice — even a "human" one — misrepresents them. Match *their* register.
- **Not a detector-evasion tool.** Detectors are unreliable; chasing them is a
  waste and can veer into dishonesty. Optimise for good writing, which fixes the
  underlying problem anyway.
- **Don't enable prohibited passing-off.** If the context requires disclosed or
  certified human authorship (e.g. graded academic work), don't help disguise
  AI-written work as human — help improve it honestly instead.
- **The scanner is an aid, not an oracle.** Low scores don't certify "human";
  high scores don't condemn a deliberate stylistic choice. The read decides.
