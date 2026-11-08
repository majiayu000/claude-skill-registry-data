---
name: mock-interview
description: "Run a realistic spoken mock interview for a job in the Interview Room, one question at a time, with a timer, scoring, and a written debrief. Use when the user wants to practice interviewing, rehearse answers, or asks for a mock interview."
argument-hint: "[job folder or job name]"
---

# /mock-interview

Usage: `/mock-interview <job folder or company + role> [behavioral|technical|mixed|panel|one-way|ai-screen|presentation] [number of questions]` (or just ask in plain English).

Setup: `$ARGUMENTS`. If no job is given, ask which job (or a general interview for their top target role from preferences). Default style `mixed`, 5 main questions.

## Before starting
1. Read the job folder (or the best-fit role from preferences), `profile/story-bank.md`, `knowledge/interview-questions.md`, `knowledge/field/role-questions.md`, `knowledge/field/field-primer.md` (if it still says `STATUS: not generated`, pick technical questions from the posting's requirements instead), and past debriefs in `interviews/` (re-test weak areas), and `references/practice-methods.md` (probes and what makes practice work).
2. Pick a realistic interviewer persona for this company and role (e.g., "Maria, Operations Manager at Acme Corp"). Pick questions that fit the role, mostly ones likely in the real interview, including one technical or role-specific one and one about a weak spot.
3. Before the first question, ask one plain question: "Do you want me to read the questions aloud, with a short beep when your time is nearly up? Both stay off unless you say yes." Voice and sounds are off in the Interview Room until the user opts in: pass `voice: true` and `sounds: true` to `interview_start` only after a clear yes to each (yes to one only: pass just that one; a no: pass `false`). Otherwise the questions show as text and the clock is silent, and the user can press **Turn on voice** or **Turn on sounds** later. Never start voice or sounds on your own. Then tell the user how it works in 3 short lines: answer out loud (terminal: `/voice` once, then hold Space while talking; Desktop: click the mic) or type; press **Done answering** in the Interview Room when finished, or just send the answer (either one stops the clock and gives you the answer time); say "stuck" (or press **Ask for a hint**) for a hint, "end" (or **Ask to end interview**) to stop. Add: "Want more time, no clock, text only, or to type your answers? Just say so. You can also press **Ask for more time** or **Turn off the clock** in the Interview Room." With the clock off there is no countdown and no **Done answering** button: the user just sends the answer, and you never mention time or answer length.
   **Language:** hold the interview in the language the real one will be in (the posting's language; ask if unsure), and give the how-it-works lines, coaching and the debrief in the user's `language:`. The Interview Room's buttons are in English. For an interview that isn't in English, pass `language` to `interview_start` as a BCP-47 tag (`de`, `es-MX`, `fr-CA`): the room then reads aloud with an installed computer voice for that language. If it says none is installed, tell the user once: they can add a voice for that language in their computer's speech settings, or keep text only. The user may say "stuck" or "end" in their own words.
   Answers may arrive through dictation: read past misheard words, never score spelling or transcription, and if a key word, name or number is unclear, ask "Did you mean X?" before scoring. Comment on filler words only for spoken answers, and only if the user wants that feedback.

## Running it (Interview Room tools available → use them)
- Call `interview_start` (company, role, interviewer, style, total, plus `voice`/`sounds` from step 3 and `language` when the interview isn't in English). `style` is one of the styles above; `total` = the number of main questions.
- `interview_say` kind `intro`: a natural 1–2 sentence greeting in character.
- Send `interview_say` calls one at a time and wait for each to return. Never send two in the same message: they get read aloud over each other, and the answer clock can start while the user is still listening.
- For each main question: `interview_say` kind `question` with `seconds` (behavioral 120, technical 180). **Then stop and wait** for the user's answer. No coaching mid-interview.
- After their answer: optionally one realistic follow-up (`kind: followup`, 60s) if a real interviewer would probe (vague result, missing "I", no number), worded as real interviewers do: "What did you do, specifically?", "How did it turn out?", "What would you do differently?" Probe at least once per session; real structured interviews do.
- After each main question, call `interview_score` (`question` in a few words, `score` 1–5, a one-line `note`) and stay in character; save detailed feedback for the end.
  Score with the rubric that fits the question, on content only: never on speed or length. Time notes (well over the target) go only in the debrief, and never when the clock is off or the user typed or asked for more time.
  - **Behavioral:** 5 = clear STAR, specific "I" actions, a number, what they learned or would do differently, ties back to the role; 4 = solid, one gap; 3 = answers but vague or hard to follow; 2 = rambling or no result; 1 = didn't answer.
  - **Technical:** 5 = correct definition, a concrete example (ideally their own), and the limits or caveats; 4 = correct with an example; 3 = correct but textbook, *or* an honest "I haven't done that; here's how I'd approach it"; 2 = partly wrong; 1 = wrong or bluffed. Never reward bluffing.
  - **Presentation** (style `presentation`): structure, clarity for a mixed audience, time (about a minute under the slot, e.g. 9 of 10 minutes), handling of probes, no confidential material from past employers.
- Close with `interview_say` kind `closing`, invite their questions for the interviewer and react to them in character, then call `interview_end`.

## One-way video practice (`one-way` style)
Many large employers screen with recorded, one-way video interviews (HireVue and similar), especially for early-career and high-volume roles: a question appears, ~30 seconds to think, then 1–3 minutes to record, with no human reacting. Simulate it: no greeting small talk, no follow-ups, `interview_say` with `prep_seconds: 30` and `seconds: 90–120`. Tips to give the user in the debrief: look at the camera, not the screen; light in front of you; plain background; notes are okay off-camera but don't read; finish with the result; practice once by recording yourself on your phone.

## AI interviewer practice (`ai-screen` style)
Many employers now screen with a live AI interviewer (phone, video avatar or chat). Simulate it: persona "Automated screening interviewer for <company>", a flat one-line intro, no small talk, no reactions, behavioral questions at `seconds: 120`, and at most one generic follow-up ("Can you give a specific example?", "What was the measurable result?"). Debrief on whether each answer stood alone: a specific example, what they did, a number, a clear finish.

## Panel practice (`panel` style)
Use 2–3 personas with different angles (e.g., the hiring manager, a peer, someone from a partner team). Start each `interview_say` line with the speaker's name ("Priya: ...") so the user knows who's asking, and let a different panelist ask the follow-up.

## Technical presentation practice (`presentation` style)
Many onsites ask for a 10–15 minute talk on a past project. One `interview_say` with kind `question` and `seconds` = the slot the employer gave (default 600) ("Go ahead whenever you're ready"), then 3–4 realistic panel probes as `followup`s (why that approach, what would you change, what went wrong and how you handled it, what it cost or saved). Debrief on structure and timing.

## Practising with an accommodation
If the user has asked (or plans to ask) an employer for an interview accommodation, or just wants practice set up a certain way, mirror it. Ask only what setup they want, never why; don't store health details (`.claude/skills/interview-prep/references/accommodations-and-disclosure.md`). With the Interview Room tools:
- **Longer answer time:** pass a bigger `seconds` on each `interview_say` question or follow-up (e.g. 1.5x or 2x: behavioral 180–240, technical 270–360, follow-up 90–120), matching what the employer agreed if known. Score on content, never on speed.
- **Question in writing first:** every line already shows on screen as it's read. For think time before the clock starts, pass `prep_seconds` (e.g. 30–60) with each question or follow-up, in any style (the Interview Room honours it on every question and follow-up, not only in one-way practice).
- **No read-aloud:** reading aloud is off unless the user turned it on. If it's on, pass `voice: false` to `interview_start`, or tell them once: "Press **Turn off voice** in the Interview Room; it remembers your choice for this folder." Then the questions are text only.
- **Questions in advance:** before `interview_start`, give them the topics or the exact questions in chat, as the employer agreed to.
- **Breaks:** after a main question is scored, ask in character or plainly "Ready for the next one, or want a break?" and wait. Split a long session into two shorter ones if that mirrors the real day.
- **Written answers:** they can type instead of speaking; keep the same scoring.
- **Screen reader users:** the panel's own read-aloud would talk over the screen reader, so leave voice off (if they turned it on before, pass `voice: false` or point them to **Turn off voice** in the Interview Room), or run the interview in chat (as in "Without the Interview Room tools"), where the screen reader reads each question. Put the target time in the question message ("about 2 minutes"). The room shows a notice when think time is over, at 30 seconds left and at time up, with a short tone only if they turned sounds on (offer it once: it helps without looking at the screen); in chat there's no clock, so give time feedback only in the debrief. Never score on speed.
Note it in the debrief's first line ("Practised with: longer answer time, no read-aloud") so later sessions repeat the setup.

## Without the Interview Room tools
Same flow in chat: ask one question per message, tell them the target time, and wait. For reading questions aloud and rough answer timing without the panel, follow the "Codex notes" in `.agents/skills/mock-interview/SKILL.md` (they work in any app).

## Debrief (always)
Write `interviews/<YYYY-MM-DD>-<company>-mock-<style>.md` (add `-2`, `-3` if that file exists, so earlier practice is never overwritten): overall impression (2 lines), scorecard table, the **top 3 fixes** with a rewritten sample answer for the weakest question using only their real facts (run `truth-checker`, then `voice-editor`, on it before showing it), filler/verbal habits noticed in the transcript (e.g., "like", "um", long setups), stories to add to the story bank (ask before editing `profile/story-bank.md`). Show the user the top 3 fixes and offer to re-run the weakest question right away (a second try with one specific change is the fastest gain). Suggest the next short session in 2–3 days rather than a long cram, and say to keep stories as bullet points, not memorized scripts.
