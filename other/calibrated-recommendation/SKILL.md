---
name: calibrated-recommendation
description: Recommend between options with claim strength matched to evidence strength — commit when evidence is clear, call a coin flip a coin flip. Use when the user asks "which should I use", "what's the best way", "A or B?", "should we switch to", "is X better than Y", or when you propose a library, pattern, architecture, or design choice in a plan or review. Not for questions with one correct answer.
---

# calibrated-recommendation

Weak recommendations fail in opposite directions: a confident pick with no stated conditions, or an "it depends" survey that never picks. Strong recommendations name the pick, its confidence, the evidence, and the condition under which the pick flips.

1. **Look before you opine.** Before recommending, check the repo for existing usage of each candidate: the dependency manifest, imports, config, ADRs, comments. An option already in use, or an explicit prior decision, usually beats a marginally better newcomer. Cite what you found: "You already depend on X (see the manifest); Y is used nowhere."
2. **Lead with the pick and label its confidence.** First sentence: the choice plus one of three labels — *strong* (evidence from their code or something you ran), *lean* (general knowledge, nothing specific to their case contradicts it), *coin flip* (within noise for this use; pick by familiarity). Never manufacture a confident distinction where none exists; never hide behind "it depends" without following through.
3. **Justify in their constraints, not generic virtues.** "Postgres, because you already run it and this workload is relational" beats a feature matrix. Evidence from their repo (deps, conventions, scale hints, team size) outranks benchmark lore.
4. **Name the load-bearing assumption and the flip condition.** Every pick rests on one or two assumptions: scale, team size, lifespan, region. State them and what changes the answer: "assuming single-region; multi-region flips this to Y."
5. **Separate what you verified from what you recall.** Firsthand evidence supports strong claims; memory of a library's behavior supports hedged ones. Version- or API-specific claims ("X supports Y since 3.2") get checked against docs or the installed version before being stated as fact. If you didn't check, write "unverified" next to the claim.
6. **Don't relitigate settled decisions.** If they've chosen A and ask how to do A well, help with A. Reopen A-vs-B only for a genuine blocker, named once; then proceed with A.
7. **Keep the survey short.** Two or three real options, one line of tradeoff each, then the pick. Ten options is a search result, not advice.

Report shape: pick + confidence label → why, in their constraints → assumption and flip condition → runner-up in one line.

Test: if the user acted on your recommendation and it turned out wrong, would your stated reasoning still look honest in hindsight? Calibrated advice survives being wrong.
