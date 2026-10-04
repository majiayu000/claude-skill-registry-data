---
name: joke
description: Transform a topic, claim, question, or situation into an original joke by leading the audience into one plausible frame and using a concise punchline to reveal a second compatible frame. Use when the user asks for a joke, one-liner, punchline, comedic reframing, roast, or short humorous treatment of an idea.
---

# Joke

Compile a premise into a trapdoor. Lead the audience to complete one interpretation, then make the punchline reveal another interpretation that the same setup was quietly supporting all along.

## Purpose

Use comedy to expose a contradiction, hidden rule, status claim, or absurd consequence without explaining it. Where `parable` gives a tension a world and `lyric` gives it a voice, give it two frames and a hinge. Make the joke feel surprising before the punchline and inevitable after it.

## Procedure

### 1. Distill the comic pressure

Find one mismatch in the input:

- expectation versus behavior;
- rule versus outcome;
- self-image versus evidence;
- polite language versus material reality;
- ordinary scale versus absurd consequence.

Write the mismatch privately as a plain observation. Prefer a specific contradiction over a broad topic. “Meetings are annoying” is a subject; “the meeting about saving time took an hour” contains comic pressure.

### 2. Choose the target and stance

Decide what the joke exposes: the speaker, a behavior, an institution, a convention, a claim, or the human condition. Give the audience a stable place to stand, even if the punchline later moves it.

Aim at the narrowest deserving target. For a roast, use an observed choice, habit, artifact, or contradiction rather than a generic insult. For self-deprecation, let the speaker retain enough dignity to be recognizable rather than merely contemptible.

### 3. Build two frames

Construct:

- **Frame A:** the natural interpretation the setup invites;
- **Frame B:** a different interpretation that fits the setup's exact facts or wording but overturns what the audience assumed.

Find the hinge between them: an ambiguous phrase, concealed motive, reversed status, literalized metaphor, category shift, or unstated consequence. If Frame B requires new information unrelated to the setup, it is randomness rather than a punchline.

### 4. Select one comic engine

Choose the mechanism that reveals Frame B most cleanly:

- **Misdirection:** preserve two meanings, then disclose the less expected one.
- **Literalization:** make an idiom, euphemism, or institutional fiction materially true.
- **Reversal:** swap who serves whom, who evaluates whom, or who possesses status.
- **Analogy collision:** expose the source's structure by placing it in a distant, concrete domain.
- **Escalation:** follow a reasonable rule to a disproportionate but legible consequence.
- **Compression:** state the implication everyone was cooperating not to say.

Use one dominant engine. Add a pun only when both meanings touch the premise; a free-floating pun is word inventory, not comic reasoning.

### 5. Dispatch the form

Honor the form and tone the user requests. Otherwise default to a one-liner.

- **One-liner:** Use one or two sentences and a single turn.
- **Question and answer:** Use when the question itself plants Frame A. Keep the answer shorter than the question.
- **Short joke or anecdote:** Use two to six sentences only when an action or sequence must establish the frame.
- **Roast:** Name a precise observed feature, exaggerate its logic, and keep the target recognizable.
- **Absurdist joke:** Break surface logic while preserving an emotional or structural logic the audience can recover.

Treat “dry,” “dark,” “wholesome,” “dad joke,” “surreal,” and similar requests as tonal constraints, not substitutes for a mechanism.

### 6. Write the setup

Take the shortest natural route to Frame A. Include every fact the punchline needs and nothing present only to decorate the delivery. Plant the hinge without pointing at it. Use concrete nouns and speakable syntax.

Do not announce that something funny is coming. Avoid “Have you ever noticed,” “Funny how,” and similar throat-clearing unless the voice specifically needs them.

### 7. Land the punchline

Reveal Frame B as late as possible. Put the word or phrase that completes the turn near the end. Let the audience perform the final inference; do not explain the connection.

Add at most one tag after the punchline, and only if it creates a new implication or escalation. Stop before the joke begins defending itself.

### 8. Run the three tests

- **Surprise:** Does the setup make Frame A genuinely more available than Frame B?
- **Inevitability:** After the turn, can the audience see that the setup supported Frame B all along?
- **Compression:** Can any word be removed without weakening the frame or the turn?

If surprise fails, conceal the hinge more naturally. If inevitability fails, rebuild Frame B from the premise. If compression fails, cut. Do not repair a weak joke by explaining it or adding volume.

## Length discipline

Default to **one joke under 50 words**. Keep a short anecdotal joke under **180 words** unless the user asks for a bit or monologue. When the user requests several jokes, make each a distinct mechanism or angle rather than minor rewrites of one premise.

## Output format

Return the joke only. Use no title, preamble, mechanism label, explanation, laugh cue, or self-evaluation. When asked for multiple jokes, number them only if numbering improves readability.

## Guardrails

- **No premise without a turn.** An amusing observation is raw material, not yet a joke.
- **No randomness mistaken for surprise.** Preserve a recoverable path from setup to punchline.
- **No explanation after impact.** Trust the audience or rewrite the setup.
- **No stock chassis by default.** Avoid “walks into a bar,” “starter pack,” and “nobody/absolutely nobody” unless the requested form calls for them.
- **No mechanism pileup.** Prefer one clean frame shift to puns, rhyme, exaggeration, and topical references competing in the same line.
- **No targetless cruelty.** Make behavior, power, hypocrisy, convention, or the speaker's predicament carry the joke. Do not use a vulnerable identity as the whole mechanism.
- **No borrowed routine.** When given a comedian as a reference, translate the request into broad traits such as deadpan delivery, compressed wording, observational specificity, or surreal escalation. Do not imitate distinctive phrasing or persona.

## Composition

Pair with `assumption-audit` to locate a claim's least defensible hidden premise, then turn that premise into the setup's trapdoor. Pair with `inversion` to generate failure logic and compress the strongest absurd consequence into a punchline. Use `parable`, `lyric`, and `joke` as alternative terminal forms: build a world, make an utterance, or spring a frame.

## Canonical prompts

- Make a joke about AI assistants being too helpful.
- Why do meetings about productivity take so long?
- Turn “we're like a family here” into a one-liner.
- Write a joke about buying books faster than I read them.
- Roast our app's onboarding without being mean to its users.

Poor fits: factual or operational questions, sincere requests for advice, safety-critical communication, and situations where humor would evade rather than illuminate the user's concern. Answer those directly unless the user explicitly asks for a joke.
