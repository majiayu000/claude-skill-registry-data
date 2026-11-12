---
name: narration-writer
version: 2.0.0
description: Narration and on-screen text for explainer videos in a controlled, STE-style English (about 80% of ASD-STE100) — short active sentences, one word per meaning, a glossary, spoken-form rules, per-scene word budgets, audio-length gates and a stdlib lint script. Use when writing voiceover or captions for Remotion or Manim videos, simplifying dense technical prose, or fitting narration to scene timing.
---

# Narration Writer

Writes the words of an explainer video: voiceover and on-screen text, in a controlled English that a synthetic voice reads clearly and a non-native listener can follow. It produces scripts and checks, not video code (for that, see [remotion-architect](../../frameworks/remotion-architect/SKILL.md) or [manim-architect](../../frameworks/manim-architect/SKILL.md)); what a teaching scene shows is [explainer-designer](../explainer-designer/SKILL.md). For live, presenter-led demos in a conversational voice, see [demo-script-designer](../demo-script-designer/SKILL.md); this skill is the opposite register: recorded, controlled, one claim per sentence. Templates, the budget math and the audio wiring are in [RECIPES.md](RECIPES.md).

## 1. Mental model

- **Narration is data, not code.** A script is a table of scenes: id, seconds, narration, on-screen text, visual cue. The composition reads the audio the script produced; it never contains the words.
- **The picture carries names, numbers and code; the voice carries the reason.** Do not read the screen aloud.
- **Control the language so that three things hold:** a synthetic voice reads it without surprises, a listener who is not a native speaker follows it, and each sentence maps to one claim that can be checked against a source.
- **Narration may not say more than the sources behind the picture.** No timing, safety or score claim unless the source states it. Say what was not run.

## 2. The dial

- **Strict:** every rule in §3, for steps a viewer will repeat.
- **80% (default):** keep the sentence limits, active voice, one meaning per word and no idioms. Allow named technical terms from the glossary, and a connector such as "because" or "so" when it carries the reason.
- **Conversational (about 30 words a sentence):** for a lesson that explains why, where many short sentences sound clipped. Keep the glossary and one meaning per word, allow connectors and a varied rhythm. Details, and notes on offline voices, in [CONVERSATIONAL.md](CONVERSATIONAL.md).
- **Say "STE-style", never "ASD-STE100 compliant".** No approved-word dictionary is checked here, and the name is a trademark of ASD. The official specification (Issue 9, January 2025) is free on request at asd-ste100.org. Read it for the exact limits and the dictionary; do not copy its text or word list into scripts or into this skill.

## 3. Writing rules

1. **One idea per sentence.** Default limit 20 words, 25 for a description. The lint script reads the limit from the script file; confirm the numbers in the official text.
2. **Active voice, with a named actor.** "The agent validates the program", not "The program is validated".
3. **Simple tenses.** Present for what is true, past for what happened, future only for a promise.
4. **One word per meaning, everywhere.** Pick a term in the glossary and use it in every scene. Varying a word for style is a bug here.
5. **Plain verbs.** "Check", "send", "start", not "leverage" or "facilitate".
6. **Short noun clusters.** Three words or fewer ("level over 90"). Break a longer one with a preposition.
7. **Keep the articles.** No contractions, no idioms, no figurative phrasal verbs, no jokes.
8. **Condition first.** "If the level is over 90, the pump must switch off." Use one modal per meaning: `must` for a rule, `can` for an ability. State doubt as a fact: "This was not run."
9. **Short paragraphs.** Six sentences or fewer, one topic.

## 4. Narrating for video

- **Plan at 2.5 words per second.** The words allowed in a scene are `floor((scene seconds - lead-in - tail) * rate)`, with 0.5 s of silence at each end. 2.5 is a first guess: replace it with the measured rate of the real voice.
- **Measure on the slowest scene, not the mean.** Real voices vary a lot between scenes (one video ran from 1.75 to 3.1 words per second, and a plan at 2.5 failed 7 of 15 scenes). Count spoken words, after the `say` forms: an acronym said as letters is one word per letter. The lint script prints the mean and the slowest rate when it is given `--audio-dir`.
- **One rate drives both the scene length and the cues.** If scenes are timed from words and drawings are cued to phrases, a wrong rate makes the scene too short and every cue early. Set the measured rate in the script file; do not patch single scenes.
- **Tie each sentence to a cue.** Note the second at which its picture appears, so the audio lines up with the animation (`<Sequence from>` in Remotion, `wait` and `run_time` in Manim).
- **Leave silence.** Give a new diagram one or two seconds before speaking, and do not talk over dense text.
- **First sentence says what the scene shows.** The last may bridge to the next scene, only when it states a reason.
- **Say what is not real.** Where the picture is an illustration and not a recording, the narration says so in words, as well as the on-screen badge.
- **One voice and one language per video.** Translate from the English source and keep the glossary.

## 5. Spoken form

- **Keep a pronunciation map.** Each term gets a `say` form: acronyms as letters ("P L C"), mixed names spelled out, "C plus plus". Check the map with the real engine.
- **No symbols in speech.** Arrows, comparison signs, paths and identifiers are said as what they mean. Keep the exact identifier in the caption, and the spoken form in the narration.
- **Plain punctuation.** Full stops and commas. Avoid parentheses, dashes and semicolons: engines pause on them unpredictably.

## 6. Pipeline

1. **Interview:** length, scenes and their seconds, audience, language, where the audio goes, who supplies the voice. Never pick the voice provider for the owner.
2. **Glossary first:** term, one meaning, words to avoid, spoken form.
3. **Draft each scene** at the 80% dial, inside its budget.
4. **Lint:** run `scripts/narration_lint.py` on the script. Errors block; warnings are heuristics, not verdicts. Usage in [RECIPES.md](RECIPES.md#4-the-lint-script).
5. **Generate audio per scene** with the chosen engine. Cache by hash of text, voice and settings so unchanged scenes are not regenerated.
6. **Gate on length, then fix the cause.** Measure each audio file; if it is longer than the scene minus the tail, there are two honest fixes. If the script is over budget, cut words. If the picture is correct and only the rate was optimistic, lower `rate` in the script file to the measured slowest rate and rebuild the scene times: audio that already exists stays valid. Do not speed the voice up or trim it to fit.
7. **Wire it in:** one `<Audio>` per scene inside its sequence ([RECIPES.md](RECIPES.md#5-wiring-audio-in-remotion)).
8. **Review:** listen once, and check each sentence against its source.

Provider choice, cost, privacy and voice rights belong to the owner. Keys live in env files that never enter git. Record the voice and settings in the script header so a render can be repeated.

## 7. Anti-patterns

- Narration typed into the composition, or generated at render time.
- A sentence over the limit "because it reads well".
- Two names for one thing across scenes.
- Reading the screen aloud word for word.
- Speeding up or trimming audio to hide an over-budget script.
- Keeping a planning rate that the measured audio contradicts, so scenes end before the voice does.
- A claim in the voice that the sources do not support.
- Claiming ASD-STE100 compliance.
- A secret in a script, a header or a log.

## 8. Review checklist

- [ ] Every sentence is within the limit, in active voice, with its actor named.
- [ ] Every term matches the glossary, and every glossary term has a spoken form.
- [ ] Each scene is within its word budget, and its measured audio is within its seconds.
- [ ] The script's `rate` is the measured slowest rate, not the planning guess.
- [ ] No symbol, path or identifier is spoken.
- [ ] Every claim traces to a source shown or cited with the video.
- [ ] Anything not recorded is said to be an illustration.
- [ ] No key, token or private detail is in any file.

---

_Idea adapted from Andrej Karpathy's post on understanding LLM output: ask for ASD-STE100-style writing, and for bespoke explainer videos with generated narration._
