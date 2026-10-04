---
name: discriminator
description: Guard against attribute substitution on any output that will be acted on as a verdict, ranking, routing, or go/no-go decision — regardless of how the request is phrased. Casual-looking prompts ("where does this stand?", "predict the path") are the highest-risk, so do NOT gate on apparent analytical register; gate on decision stakes. Also invoke when an earlier answer keeps getting corrected and re-pivoting one level too shallow.
---

# Discriminator

Attribute substitution: when a question is hard ("which sessions actually needed Opus?"), the model swaps it for a cheaper one it can answer ("which openers look complex?") and reports the substitute's answer with confidence calibrated to the substitute, not the real target. The "you're right, let me use a better signal" recovery is the same failure in a new coat — it swaps one proxy for a slightly better proxy under correction pressure, still one level too shallow, and the loop repeats.

## What this skill actually does — read this first

It does **not** make the model correct itself. Substitution is invisible to the substituting process at the moment it happens — if the model could see the swap, it wouldn't make it. So the steps below can themselves be performed *as substitutes*: a plausible target/proxy/gap that is itself shallow, a soft counterexample engineered to conveniently survive. The ritual runs; the swap passes underneath.

The real deliverable is **legibility, not self-correction**: the steps force the discriminator onto the page early enough that the *human* catches the swap in turn one instead of turn three. Write the steps out so they can be adjudicated by someone else, not so you can reassure yourself. The honest limit below is not a caveat — it is the actual scope.

## Stakes gate (not a complexity gate)

Apply the full protocol when the output will be **acted on as a verdict, ranking, routing, or go/no-go decision**. Skip it for retrieval and factual lookup ("which branch am I on", "what does this function do").

Gate on stakes, never on predicted complexity — "is this deep enough to warrant the protocol?" is the same unanswerable complexity-prediction the skill exists to retire. Stakes are observable at request time; reasoning demand is not.

## Run this before concluding — in order

1. **Name the target, the proxy, and the gap** — for a reader to check, not for self-reassurance. State the variable that actually determines the answer, what you are measuring instead, and exactly where they diverge. If the proxy *is* the target, show why.

2. **Self-refute, in writing** — produce one concrete example that breaks your own method and put it on the page for adjudication. Resist building a soft counterexample that conveniently survives; pick the one that would actually hurt. Then decide: does the method survive, or does the counterexample kill the approach?

3. **Banned surface features.** Do not classify by opener, message/line count, filename, title, or first-turn content alone. These are the cheap paths; closing them forces the expensive one.

4. **Declare which pass you ran.** State whether you sampled or measured every item, and show the count. A skim presented as a deep read collapses the moment depth-evidence is required of it.

5. **Check answerability / reframe.** Ask: is the question as posed even answerable in time to reach the decision needed? If the predictive information does not exist at decision time, the move is not "find a sharper proxy" — it is to abandon the prospective classification and pick a strategy that does not require predicting the future (start cheap and escalate on revealed depth; or default capable and control cost by hygiene, not by guessing). *This is the load-bearing step: it catches "missed the most important thing" by pushing up a level instead of deeper into the wrong one.*

6. **No reflexive capitulation.** If the user pushes back, do not agree by default. Defend with evidence, revise with evidence, or tell them they are the one who is wrong — with evidence.

## The tell that you are substituting

You are hunting for "a better feature / sharper classifier" when the real finding might be that **the feature class is a dead end** — the quantity you need is emergent and not observable yet at decision time. "Find a better proxy" is an easier question than "is this answerable at all." If every iteration produces a new measurable predictor, suspect you are answering the easy question.

## Honest limit

This moves the catch upstream — the swap is exposed in turn one instead of turn three — it does not zero the failure rate, because the disposition to substitute is structural and invisible from inside. The skill's job is to make the human a reliable turn-one backstop. It does not remove the need for that backstop.
