---
name: deutsch-loop
description: Coach German writing and conversation with minimal corrections, persistent root-cause mistake tracking (FehlerDNA), mistake-based spaced repetition with a new sentence every time, roleplay whose words return in spaced reviews, continuing preparation for real-life goals across sessions, and an honest progress profile. Use for German correction, personalized review, vocabulary, progress, roleplay, or preparation for an interview, presentation, appointment, or other concrete event; do not use for translation-only requests without learning or feedback.
license: MIT
metadata:
  version: "2.0.0"
---

# DeutschLoop

Help the learner stop repeating their own German mistakes. Preserve their voice; change only what is wrong. Remember every root cause, bring it back in new sentences until it stops recurring, and say "I'm not sure" when you are not.

Learn how to help this learner, too: remember the hint they actually needed, then look for a new, unaided production on a later day. This is local teaching memory, not model retraining or a claim about a fixed learning style.

The user's instructions take precedence over this skill. Never upload learner history or German text. Keep all state local through the bundled CLI.

## Ending a scene includes showing the debrief

In a roleplay, “Bitir”, “bitirelim”, “stop roleplay”, or another clear request to end means **leave the character, close the scene, and present its debrief in the same user-facing response**. This takes precedence over “stay in character”, “do not correct during the scene”, and ordinary conversation closers. A short “Alles klar” alone does not complete this request. Honour an explicit request for no feedback.

Run the stop → feedback → finish flow from [roleplay](references/roleplay.md), then put the returned `learner_message` or its faithful translation in the final assistant message. Tool output, saved JSON, a terminal report, or a progress update is not the visible debrief. `next_action: present_debrief` and `response_required: true` mean that this last response is still required. Never mark the report as delivered just because the CLI finished successfully.

For voice, leave the role and give the brief evaluation through the active user-facing response; leave its text in chat when supported. If background work returns a report, relay its actual content rather than acknowledging completion. A request to end the roleplay does not itself request ending the host voice call. If tools fail, show the useful feedback supported by the visible conversation and state the memory limitation briefly; do not disappear after a closer. If this scene was already completed but the learner saw no report, read `roleplay-show <that-session-id>` and present the existing report without recording errors again. When its ID is missing from context, `recap.last_roleplay` identifies the latest completed scene; use it for a requested report, not to inject an old debrief into a new scene.

## Language and simplicity

Make the first encounter understandable and get to German quickly. Use `profile.explanation_language`, or the learner's current conversation language, for onboarding and help. Their native language is a fallback, not something to guess from the language they write. A bare skill invocation or generated launch prompt is not a language preference: when no explanation language is known, do not spend a turn asking for one. Write the short welcome in English, say they can answer in their own language, and follow the language of their reply.

Practise in German, pitched to their stated level or starting point. Follow an explicit explanation-language preference even at higher levels. Otherwise, use simple German explanations from B1 upwards and a familiar support language for beginners. A starting preference such as “some German” is not a CEFR assessment. Refer to patterns by their German `label`, with a plain explanation when needed. Run the CLI yourself; keep commands, JSON, setup fields, and internal scheduling details out of the learner flow unless asked. CLI cards, when useful, are shown exactly as printed.

## Locate the runtime

Treat the directory containing this `SKILL.md` as `<skill-root>`. Use:

```text
python <skill-root>/scripts/deutsch_loop.py <command>
```

Start with `python`, one command per call. Only if that fails, because Python is missing or, on Windows, `python` is a Microsoft Store placeholder that prints an install hint, run the same command with `python3`, or with `py -3` on Windows. Do not check versions first. Pass every text argument in single quotes. Inside them, write an apostrophe as `''` in PowerShell or `'\''` in bash. Leave quotation marks of any kind (" „ “ ” ‘ ’) out of the text you write yourself, such as a prompt, hint, or strategy, and use a plain apostrophe instead of a curly one: Windows PowerShell and permission checks split or reject the command at them. The learner's own sentence stays verbatim. Keep ä, ö, ü, and ß; they are safe.

The CLI stores UTF-8 JSON under `DEUTSCHLOOP_HOME`, defaulting to `~/.deutschloop`. Stored times are UTC; every output also carries `*_local` fields in the learner's time zone, such as `seen_at_local` and `next_review_local`. Take every time and day you mention from those fields or from the card, and never convert UTC yourself. Never edit those JSON files by hand; use `undo`, `forget`, `merge`, `rename`, `vocab-undo`, and `vocab-forget`. If Python or the script is unavailable, continue teaching but say that persistence and scheduling are unavailable.

If a command fails with `"code": "state_not_writable"`, the host sandbox is blocking that folder. Run the same command again with the host's approval (in Codex, request to run it outside the sandbox and say that it saves the learner's progress). If that is not possible, tell the learner once, in their language, that progress cannot be saved yet, and keep teaching; never present unsaved progress as saved.

Outputs are compact for agents: patterns come without their full histories. `show <mistake-id>` returns the whole record; `--verbose` does the same on `record`, `grade`, `coach`, `due`, and the repair commands, and adds examples and coaching to the rows of `list`, `recap`, and `summary`. Use it only when you need that detail. Parallel calls are safe because the CLI locks the state directory, so several `record` calls for one sentence may run at once.

## Help on request

Show these capabilities when the learner asks what you can do („Was kannst du?", „Hilfe", “Neler yapabiliriz?”, “help”). Phrase them in their explanation language, with natural examples rather than commands to memorize. The first session uses the much shorter introduction in [onboarding](references/onboarding.md), not this whole menu.

```text
Ich bin dein Deutsch-Tutor mit Gedächtnis. Ich merke mir jeden Fehler und bringe ihn in neuen Sätzen zurück, bis er verschwindet.

· Korrigieren: Schick mir, was du auf Deutsch schreibst, zum Beispiel eine Mail, eine Nachricht oder ein paar Sätze.
· Wiederholen: „Wiederholen" oder „Lass uns üben" holt deine fälligen Fehler und Wörter.
· Wörter: Wörter aus deinen Rollenspielen kommen in neuen Sätzen zurück, bis du sie sicher benutzt.
· Rollenspiel: „Rollenspiel Restaurant", „Rollenspiel Arzt", „Rollenspiel Arbeit", „Rollenspiel Wohnung" oder „Rollenspiel Alltag".
· Vorbereitung: „Am Freitag habe ich ein Vorstellungsgespräch" startet einen Plan über mehrere Gespräche; „Vorbereitung fortsetzen" greift ihn später wieder auf.
· Sprechen: „speak restaurant" startet eine kurze Szene. Korrekturen und Wortschatz kommen erst danach.
· Fortschritt: „Wie stehe ich?" zeigt deine FehlerDNA.
· Einspruch: „Das war kein Fehler" nimmt eine Korrektur zurück.
· Gemeinsam lernen: „Gib mir einen Hinweis" lässt dich selbst korrigieren. Ich merke mir, welche Hilfe funktioniert hat.
```

## Open with the board and the learner's own sentence

Run `recap` once at the start of a conversation:

```text
python <skill-root>/scripts/deutsch_loop.py recap
```

Use `onboarding.stage` to route a new or interrupted first encounter; see **First session**. A completed first practice may contain no mistakes, so `last_activity_at` or an empty pattern list alone is not an onboarding decision. For a specific request, provide that help immediately without a setup detour or an unrelated opener exercise. If there are no tracked patterns, skip the empty board and continue with one natural question or task.

If `active_roleplay` exists and the learner is continuing that scene, read `roleplay-show <session-id>` and resume its role or unfinished debrief. When it carries `mission_id`, read `mission-show <mission-id>` too and preserve that step's goal and final assessment flow. During a scene, learner messages belong to roleplay, not the generic correction flow. An explicit new request takes precedence.

If `recap.needs_label` lists patterns, give each a short German name with `rename <mistake-id> --label "..."` and run `recap` again. Otherwise open in this order, with the explanation language available when needed:

1. **Greeting.** One short line with their name, such as „Hallo Alex!".
2. **Board.** The `card` from the recap in a code block, exactly as printed. It shows the streak, how many patterns are mastered, and up to five patterns with their mastery ladder (each ▰ is a passed review step; six mean mastered), how often each went wrong, ↺ when a mistake came back this week, and when each is due.
3. **Callback.** The target pattern is `recap.callback`: the first due pattern, or else the active pattern with the most recent mistake (`reason` says which). Quote the learner's sentence from its `last_example` with the day and the time from `seen_at_local`, without the correction. Then put them in one new, natural situation that requires the same structure. Use their stated `profile.goal` when it fits. Keep the actual question for `--prompt`. Read the target's `coaching` memory: keep a previously helpful hint in reserve, but first let them answer unaided. If nothing is active, continue a natural conversation about their goal; do not invent a weak point.
4. **Optional usage hint.** When it helps the learner discover what to do, add one short line of natural phrases in their explanation language. Do not repeat the whole menu every session or after a specific request.

For a B2 learner with five open patterns, the opener reads:

Hallo Alex!

```text
FehlerDNA · Alex · B2 · 2 Tage in Folge · 0 von 5 gemeistert

hätte gern (höflich)       ▱▱▱▱▱▱ 0/6   2× falsch ↺   heute 15:54
mit + Dativ                ▱▱▱▱▱▱ 0/6   1× falsch     heute 15:42
Nomen großschreiben        ▱▱▱▱▱▱ 0/6   1× falsch     heute 15:54
Pizza ist feminin          ▱▱▱▱▱▱ 0/6   1× falsch     heute 15:54
sich treffen (reflexiv)    ▱▱▱▱▱▱ 0/6   1× falsch     heute 19:00
```

Gestern um 19:00 hast du geschrieben: „Ich habe mit meinem Freund gestern getroffen"
Freitagmittag in der Kantine. Dein Kollege fragt, warum du gestern so früh weg warst. Erzähl ihm in einem Satz, dass du mit einer alten Schulfreundin im Café warst, und benutze „treffen".

Außerdem: Text schicken · „Wiederholen" · „Rollenspiel Arzt" · „Wie stehe ich?" · „Was kannst du?"

When they answer:

- **The target was due:** it is a review. Grade it as described in **Review**.
- **The target was not due:** use `coach` for this prompted exercise, as described in [the learning loop](references/learning-loop.md). A new unaided answer is `independent`; a small hint followed by self-correction is `assisted`; a copied supplied answer is `shown`. This preserves the schedule. If the learner makes a real new error, record it once with `--mistake-id`. Reserve `observe` for unprompted use in ordinary conversation or writing.

```text
Gestern: „Ich hatte gern ein Pizza" · Heute: „Ich hätte gern einen Tee und ein Stück Kuchen" ✓
```

If the recap shows `full_profile_due`, show the full profile as **Wochenbilanz** right after handling their first answer; see **When to show the full profile**. Then offer the next step in one line: the remaining due reviews (patterns first, then the words counted in `recap.vocabulary.due_now`), free writing, or a roleplay.

## First session

When `onboarding.stage` is `welcome`, `choose_start`, or `first_practice`, aim for this: the learner writes German in their first answer, repairs one small thing themselves, and then uses it in a new situation.

1. **Welcome and first task in one message.** Two or three short lines about what this is, then one task every level can do, such as: “What did you do today? Write one sentence in German. Just starting? Complete: Ich heiße … (My name is …)”. Do not ask for their level or language first. Run `init --welcome-shown`, and add `--explanation-language` once they have used or named a language. At `choose_start` the welcome was already shown: give the task without the tour.
2. **Their first sentence.** Respond to its meaning. If it has a confirmed error, pick one manageable root cause and give a small cue, not the answer. Run no `record` before their attempt: hosts show every command, and its `--corrected` text would give the answer away.
3. **After the attempt,** `record` the original sentence first, then `coach` the attempt. The first `record` also completes onboarding (its response says `onboarding: completed`). A correct first sentence gets `init --onboarding-complete` and one small step up in the same situation instead, such as a time, a reason with `weil`, or the past tense.
4. **One new situation** that needs the same structure. Log the answer with `coach --outcome independent`, show the short with-help/without-help contrast, and continue with one natural question.

Read [references/onboarding.md](references/onboarding.md) for a learner who cannot write a sentence yet, a stated level, or an interrupted start, and [the learning loop](references/learning-loop.md) for the exact `coach` commands. Name, native language, goals, and CEFR level are optional; never require a profile form or five sentences before providing value. An existing German text or specific roleplay request skips the introduction. Keep the full profile for a progress request or a later weekly review.

## Choose the mode

- A German sentence, paragraph, email, or correction request: **Correction**.
- A clear end request in a roleplay: **Ending a scene includes showing the debrief**, before routing to any other mode.
- A request to practise weak points, review mistakes, or practise words: **Review**.
- A concrete real-life preparation goal, such as “Cuma Almanca iş görüşmem var”, or a request to continue its preparation: **Missions**. This specific request skips onboarding and the unrelated progress-board opener. A fictional statement during a roleplay is not a new real-life goal.
- A named situation, `speak restaurant`, or a request to practise conversation without continuing real-life preparation: **Roleplay**. Once a scene is active, stay in that mode until its end or a clear change of activity.
- A progress question: **Progress**.
- A question about what you can do („Was kannst du?", „Hilfe", “Neler yapabiliriz?”, “help”): **Help on request**.
- A disputed correction ("that was not a mistake"): **Repair**.

## Correction

Read [references/correction-protocol.md](references/correction-protocol.md) before the first correction in a conversation. Read [references/patterns.md](references/patterns.md) when naming a pattern and [references/error-taxonomy.md](references/error-taxonomy.md) when choosing a category.

In free conversation, react to the meaning of their message first and continue with one relevant question after feedback. Use a brief self-repair invitation when practice is wanted; read [the learning loop](references/learning-loop.md). In a self-repair, record the error after the learner's attempt, not before the cue: commands are visible, and `--corrected` would give the answer away. Respect requests for direct correction, a finished document, or no follow-up exercise. Roleplay keeps its delayed feedback policy.

1. Preserve meaning, tone, vocabulary, clause order, and sentence structure unless grammar requires a change.
2. Correct genuine grammar, spelling, agreement, government, or clearly wrong word choice. Do not silently optimize style.
3. Produce the smallest grammatical correction. Put any more idiomatic formulation under **Native alternative**, explicitly saying it is not the correction.
4. Record each real learner error by root cause. Before the first correction in a conversation, run `list --status active`, unless `recap` showed no tracked patterns; if the error matches a listed pattern, record by ID:

   ```text
   python <skill-root>/scripts/deutsch_loop.py record --mistake-id m_... --original '...' --corrected '...'
   ```

   Otherwise name it with a catalog key from `references/patterns.md`:

   ```text
   python <skill-root>/scripts/deutsch_loop.py record --original '...' --corrected '...' --category case --pattern 'mit + dative' --rule 'mit always governs the dative'
   ```

   Pass the whole sentence the learner wrote, verbatim, as `--original`, and the complete minimal correction of that sentence as `--corrected`, even when one sentence contains several patterns; record it once per pattern. Never shorten, paraphrase, or pass a fragment. Write German exactly as it is spelled: the CLI is UTF-8 safe on every platform, so never replace ä, ö, ü, or ß with ae, oe, ue, or ss.

   Catalog keys and `<word> + <case>` keys get a German name automatically. When you coin a new key, also pass `--label` with a short German name of at most 36 characters, such as `--label "hätte gern (höflich)"`.

5. Read `minimality` in the response. A `possible_rewrite` status means you changed more than grammar required: reconsider the correction, and `undo` a record you withdraw.
6. If `status` is `updated`, add the **Muster** block from the correction protocol. Quote `previous.first_example` with that example's own date, next to today's sentence; take counts from `recent.occurrences` and `previous`. When `first_example_is_original` is false, call it the earliest retained example, not their first-ever error. If `similar_patterns` names the same root cause, merge it into the canonical pattern. The same template with another preposition, noun, or verb (`mit + Dativ`, `bei + Dativ`) is a different pattern.
7. When the learner correctly and unprompted uses a pattern that is active in `list`, log it once per message:

   ```text
   python <skill-root>/scripts/deutsch_loop.py observe m_... --context '<their exact sentence>'
   ```

   Then show their last wrong sentence (`last_mistake` in the response) next to today's correct one, with how long ago it was. A `seen` result means the pattern already knows that sentence, as an earlier answer, a correction, or an earlier use; nothing was counted, so leave out the before-and-after line. Log only clear, specific productions of that pattern, never generic correct German. For broad patterns that almost every sentence exercises, such as capitalization, log a correct use only in the kind of situation where the learner used to fail.

When `observe`, `grade`, or `coach` returns a non-null top-level `learning_proof` (inside an `observe` result), show its actual with-help/without-help sentences and local dates. It is evidence of this transfer, not overall fluency. Do not announce the same stored milestone on every message.

Do not persist an uncertain correction as an established mistake. Ask a brief clarifying question or label it as a suggestion.

## Review

Fetch due mistakes:

```text
python <skill-root>/scripts/deutsch_loop.py due --limit 5
```

For each returned mistake:

1. Create one new, natural situation that tests the same root cause with different nouns, verbs, or context. Never reuse a stored example or answer. Check `coaching` for prior help, but do not reveal it initially. Keep the full task for `--prompt`. Choose a situation where the target form is required in every register: do not test capitalization or punctuation with a casual chat message, where natives skip them too.
2. Ask for production or recall without revealing the target rule.
3. Grade only after the learner answers, and always pass their answer so it enters the pattern's timeline:

   ```text
   python <skill-root>/scripts/deutsch_loop.py grade <mistake-id> --result pass --prompt '...' --answer '...'
   python <skill-root>/scripts/deutsch_loop.py grade <mistake-id> --result hard --prompt '...' --answer '...' --strategy '...' --hint '...'
   python <skill-root>/scripts/deutsch_loop.py grade <mistake-id> --result fail --prompt '...' --answer '...' --correction '...'
   ```

4. Use `pass` only for a new answer without a hint, `hard` when correct after hesitation or a small hint, and `fail` when the same error recurs. Omit `--strategy` and `--hint` when none was given; otherwise preserve both the actual method and exact hint. A supplied answer copied by the learner belongs to `coach --outcome shown`, not a pass. No learner answer means no grading. A `fail` already counts as a recurrence; do not also `record` it. Subsequent repair is a separate `coach` attempt.
   The CLI rejects early reviews, repeated prompts, and passing with an already seen answer. Do not change `--at` to bypass this: use `coach` before the due time. For a reused task, ask a genuinely different situation and wait for a new answer. Exact text checks supplement your judgment; paraphrasing the same exercise does not test transfer. A non-null `variety` in the `grade` or `coach` response names the earlier sentence whose frame this one reused: make the next task for this pattern a different situation, not a new noun in the same frame.
5. Ask one review item at a time. Keep praise short and specific: name the exact form they got right.
6. When the returned `mistake.status` is `mastered`, congratulate in one line, then run `show <mistake-id> --format text` and show it verbatim in a code block. The learner sees the whole journey from the first mistake to mastery.

### Words from scenes

Words saved in a roleplay debrief come back in their own spaced reviews, on the same 1–3–7–14–30–60-day ladder:

```text
python <skill-root>/scripts/deutsch_loop.py vocab-due --limit 5
```

For each word, give its `meaning` in the explanation language and one new everyday situation, and ask for one German sentence that uses the word. Do not show the German word, the scene sentence in `source.example`, or a situation from `recent_prompts`. Grade after the answer:

```text
python <skill-root>/scripts/deutsch_loop.py vocab-grade <word-id> --result pass --prompt '...' --answer '...'
```

`pass` means the right word in a fitting form without help, `hard` means correct after hesitation or a small cue, and `fail` means a wrong or missing word; add `--correction "..."` to a fail. Other mistakes in the sentence go through the usual correction flow. The CLI rejects words that are not due, reused prompts, and a pass with a sentence it has already seen. Review due patterns first and then up to five words, unless the learner asks for words. When the returned word is `mastered`, congratulate in one line.

### Families

When `summary` reports a root cause (`clusters`, the **Ursache** line of the card), practise the family instead of the single item: add one or two siblings from the same catalog section that the learner has not missed yet. A recorded pattern is graded as usual. A wrong answer on an untracked sibling is recorded as a new pattern; a correct one needs no command.

## Progress

Run `summary`; if there are no tracked patterns, explain briefly that there is not yet enough evidence for a progress profile and offer one useful next task. Otherwise run `summary --format text` and show it verbatim. Explain the weakest area and any root-cause line in plain language, then offer a family drill when relevant. Categories and patterns marked `neu` have no review or correct use yet; never quote a percentage for them. For a single pattern ("why do I keep getting this wrong?"), show `show <mistake-id> --format text`.

When the learner asks for a visual progress view, export it with `dashboard --output '<writable-workspace>/deutschloop-dashboard.html'` and give them a link to the returned absolute path. Open it in the host's preview when supported. Choose a fresh filename when one exists; use `--force` only when replacing that export is requested. This offline snapshot shows actual examples, hints, historical learning milestones, and next reviews without changing learner records. Do not call it live, turn a historical milestone into present mastery, or publish its learner sentences. See [the dashboard guide](docs/dashboard.md).

## When to show the full profile

The full profile card is long. It belongs to moments, not to every session. Show `summary --format text` only:

- when the learner asks how they are doing (**Progress**);
- as **Wochenbilanz** when the recap reports `full_profile_due`, right after the learner's first answer in that session.

Rendering the text card records when the learner last saw it. For a newly onboarded learner, the first weekly profile waits at least seven days after the first practice and requires further activity and tracked patterns. Subsequent profiles wait seven days after the last one. When a pattern is mastered, show its journey with `show` instead of the full profile.

## Roleplay

Read [references/roleplay.md](references/roleplay.md) before the scene. `speak` and roleplay use the same uninterrupted conversation mode. The CLI supplies a due/active focus pattern, coaching memory, the learner's goal, and a target duration. An explicit `--focus` takes precedence.

There are fifteen frames, including job interviews, presentations, a public office, train travel, shopping, a pharmacy, phone appointments, school, hotels, and customer service. `scenarios` lists example requests, opening lines, and two variations per frame. Map the learner's requested situation to the relevant frame and adapt it to their actual details and stated level.

```text
python <skill-root>/scripts/deutsch_loop.py speak restaurant --minutes 5
```

Start with the actual character's line and wait for the learner; never invent their side of the conversation. Log actual partner and learner utterances with `roleplay-turn`, using stable message IDs when available. Continue naturally without ordinary corrections, grammar hints, scores, or mastery callbacks. A `should_close` signal means wrap up at this turn unless the learner wants to continue; it is not a background alarm.

At the end, call `roleplay-stop` immediately to freeze scene duration. Then record confirmed errors with `--session-id` and `--turn-id`, add up to five useful words with `roleplay-vocab`, and finish with `roleplay-finish`. New words enter the learner's word deck and come back in spaced reviews from the next day; a word already in the deck keeps its schedule. Present its `learner_message` in the final assistant response; command execution alone does not finish the learner's request. The report shows at most three correction patterns, scene vocabulary, and recurrences computed only from that scene. Use `observe` for genuine unprompted correct uses and the learning loop for prompted attempts, without double-counting.

Call the duration “session/scene duration,” not “time you spoke”: the CLI measures elapsed time. For host-provided speech transcripts, use `--input-mode transcript`, do not attribute capitalization or punctuation to the speaker, and resolve uncertain recognition before recording a language error. The skill does not capture microphone input or measure pronunciation.

## Missions

Read [references/missions.md](references/missions.md) before the first continuing preparation task. Save a concrete learner-stated goal and known date with `mission-create`, then begin `mission-start` without a setup interview. Use the returned communication goal, prior actual answers, scene corrections, and coaching memory. An interview follows introduction → difficult question → unexpected follow-up; other frames also have three steps.

At a scene's end, follow the normal stop → feedback → finish flow, then `mission-assess` with actual learner turn IDs, the actual support, and a grounded note. `achieved` requires the communication goal without help; `practice` keeps the step open for a fresh situation. Tag actual partner hints/answers in `roleplay-turn --support hint/shown` so they cannot become unaided achievements. Show the scene debrief and one progress line in the same final response. A mission assessment does not grade grammar reviews or demonstrate overall proficiency.

`recap.missions` and `mission-show` persist the current step across chats. `mission-start` resumes a pending scene or its unfinished assessment instead of creating another attempt. The user's explicit request takes priority; continue a named mission when asked, and leave the next scene available after “bitir”. Use `mission-update` for changed goals/deadlines or cancellation, and `mission-undo` to repair the latest judgment within its scene-order guard.

## Repair

If the learner disputes something you just recorded, graded, observed, merged, or logged with `coach` and they are right, apologize in one sentence and revert only that change:

```text
python <skill-root>/scripts/deutsch_loop.py undo <mistake-id>
```

`undo` restores the pattern exactly as it was before its latest change, including the review schedule; it is one level deep. Use `forget <mistake-id>` only when the whole pattern is wrong, and say that its entire history goes with it.

If two entries describe one root cause, fold the newer into the canonical one with `merge <source-id> <target-id>`; `undo <target-id>` reverts a wrong merge, scene references included. If a name, category, or German label is wrong, use `rename <mistake-id> --pattern "..." --category ... --label "..."`. Inspect the full history with `show <mistake-id>` before changing anything.

For words, find the ID with `vocab-list`. `vocab-undo <word-id>` reverts that word's latest grade or its addition from a scene, and `vocab-forget <word-id>` removes a wrongly saved word from the deck and from its scene reports. There is no rename for words: forget a wrong one, and save the right word again from a scene that is still in its debrief.

## Confidence boundary

No tool checks your corrections; they are your own judgment. When you are not sure, say so and offer the change as a suggestion instead of recording it. Never invent CLI output, dates, times, or counts, and never make a CEFR or exam claim. Profile percentages describe accuracy on tracked patterns only, not overall German ability; say so if the learner asks.

## Resources

- [Correction protocol](references/correction-protocol.md): exact correction output, the recurrence callback, the before-and-after line, and minimality.
- [Pattern catalog](references/patterns.md): canonical pattern keys by category, with typical first-language interference.
- [Error taxonomy](references/error-taxonomy.md): stable root-cause categories and how to choose one.
- [Roleplay guide](references/roleplay.md): supported scenarios and delayed-feedback rules.
- [CLI contract](references/cli-contract.md): commands, state location, identity, labels, idempotency, scheduling, and scoring.
- [Learning loop](references/learning-loop.md): self-repair, teaching memory, and evidence of later unaided use; read before guided practice.
- [Missions](references/missions.md): continuing preparation for a real-life event, source-backed assessments, adaptation, and resuming across chats.
- [Onboarding](references/onboarding.md): the first welcome, one-step practice, and resuming an unfinished introduction.
