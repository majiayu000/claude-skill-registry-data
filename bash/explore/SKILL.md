---
name: explore
description: "Use when the user isn't sure what they want, is choosing between directions, feels stuck, says 'what should I do with my career/degree/life', is thinking about a career change, or wants to try a field before applying. Life Design exploration drawn from Stanford's Designing Your Life, Johns Hopkins' Life Design, Ibarra's Working Identity and related research: constraints first, what gives them energy, three possible lives, conversations and small experiments, and reflection after each try. Keeps notes in profile/life-design.md."
argument-hint: "[optional: a direction to explore, or 'reflect' after trying something]"
---

# /explore: design your next step

Usage: `/explore`, `/explore <direction>`, or `/explore reflect` after trying something (or just ask in plain English).

This is for exploring, not applying. Read `knowledge/life-design.md` first: it has the method, where each step comes from, and the guardrails. The short version: you learn what fits by trying small real things and reflecting, not by finding one perfect answer in your head.

Read too: `profile/preferences.md`, `profile/master-resume.md`, `profile/story-bank.md`, `profile/life-design.md` (if it's missing, run `bash .claude/skills/start/scripts/init-data.sh`, or on Windows without bash `powershell -NoProfile -ExecutionPolicy Bypass -File .claude\skills\start\scripts\init-data.ps1`; it only adds missing starter files). If the notes already have lives, directions or experiments, start from them ("Last time you were looking at health policy and data science; you talked with one former colleague. Pick up there?") instead of starting over.

**Saving:** `profile/life-design.md` is the user's own notes file. Write their reflections in their words, dated, and tell them in one line what you saved. Show anything long before saving it. Nothing in it is a resume fact: if they mention a new skill, result or experience, offer to add it to `profile/master-resume.md` (that needs their OK, as always). Preferences change only with their yes (AGENTS.md).

**Pace:** one question per message, in their words (no option lists for reflections). A first session is about 15-20 minutes and covers steps 1-5; they can stop after any step, and every stop ends with one dated next step. Skip steps the notes or preferences already answer, and steps that don't fit (someone with a clear favorite can go straight to step 6).

## 1. Constraints first

Ask: "How soon do you need income from a new job?" and "Is there anything that can't change right now, like where you live, caregiving, a visa or money? You don't need to say what it is, only what it rules out." Save the answers under "What can't change right now" as limits, not reasons ("no relocation", "part-time only for now"). Never write down health details or a diagnosis unless the user explicitly asks you to (ground rule 4); if they mention one, save only the limit it sets. Treat these as fixed facts to design around, not problems to fix. If income is needed within a few months, say once that exploring works best alongside applying for a solid bridge job, and offer to do both. Everything after this stays inside these limits.

## 2. What gives you energy

Recall first: "Think of two or three times in the last year or two when you lost track of time, and one when you felt drained. What were you doing?" Then, optional: a one-week energy log (one line a day: what I did, energy up or down, absorbed or not), saved under "Energy log"; `/today` reminds them, and at `/explore` next time you look for patterns together.

## 3. What matters

Ask, one at a time, the two or three that fit:
- "What is work for, for you: money, meaning, people, learning, something else?"
- "What makes a good life for you, outside work?"
- "What are you good at that people come to you for?"
- "Where do you do your best work: alone or with people, fast or steady, structured or open?"

Reflect back in three or four lines (interests, values, strengths, where they thrive), ask "Did I get that right?", and save it under "What matters to me". If you hear a stuck belief along the way ("I'm too old to switch", "I have to pick the right one", "I wasted my degree"), offer one gentle reframe with one real fact behind it, and move on.

## 4. Three possible lives

Sketch three different next 3-5 years, built from what they said, their master resume and real occupations (a quick web lookup for what each involves day to day and how people get in; one source each):
1. **The current path, carried forward** and made better.
2. **If that path disappeared tomorrow:** what they'd do instead.
3. **If money and other people's opinions mattered less** (still inside step 1's limits): the one they'd try.

For each, in three or four lines: a short title, what a typical week looks like, why it might fit (their words), and the biggest question it raises. Ask them to rate each, in words or 1 to 5: how much they like it, how confident they are they could do it, whether the money and time work, and how well it fits what matters. Save under "Three possible lives". Ask which one or two to look into first; those go under "Directions I'm exploring".

## 5. Talk before trying

For each leading direction, two conversations with people already doing that work, ideally including someone outside their current circle (former colleagues' contacts, alumni, people from events or professional groups). Use `network` to find people and draft the asks into the Outbox; the user sends them. A good conversation asks what a normal week looks like, what they wish they'd known, and how people get in.

## 6. Try small

For each leading direction, one experiment with a date, smallest first. Good experiments are cheap, quick and real:
- **Seeing the work:** a shadow day, a site visit, an info session, a meetup or conference talk.
- **Doing a small piece of it:** a short project or portfolio piece, one module of a course, a volunteer shift, a small freelance gig.
- **If they're employed:** a piece of their current job reshaped toward the direction (a project, a task, working with a different team), with no need to quit to test it.
- **Applying:** an internship, contract or role they would genuinely take if offered (`add-job`), noted as part of this direction in the tracker's notes. Never an application only to test the market (ground rule 6).

Save it under "Experiments" as `- YYYY-MM-DD · To try: ...` so `/today` shows it when it's due. A tracker row only if it's an application. When the user says they did it, change `To try:` to `Tried:` (keep the date) even if they skip the reflection; if they drop it, change it to `Dropped:`. Only `To try:` lines count as due.

## 7. Reflect after each try (`/explore reflect`)

After a conversation, experiment, interview, class or gig, ask one at a time:
1. What energized you?
2. What challenged you?
3. What did you discover?
4. What might you try next?
5. Did anything happen you didn't plan that's worth following up?

Save the answers under that experiment, in their words. Then say in one or two lines what it changes: a direction gets stronger, weaker or narrower, or a new one appears. Update "Directions I'm exploring" with their OK, and suggest the next small step.

## 8. Tell the story, then choose

When a direction is clearly winning, help them put it into two or three sentences they can say in a networking chat or an interview ("why this change"), from what they actually tried and learned; save it under "My story so far". Offer to add true new facts to the master resume or story bank (their OK). Then offer to set the direction as their target in preferences (`field`, target roles: show the lines, their yes; if the field changes, the field pack via `start`, "Redo that changes the field"), and move to `find-jobs`, `tailor-resume` and `network`. Choosing one path means letting the others go for now; say that's normal, and that the notes keep them.

## When to bring in a person

Suggest a career coach, their school's career office (students and many alumni), a mentor, or someone they trust in the field when: experiments haven't settled a choice between directions; a direction needs a decision with real costs (going back to school, a pay cut, moving, leaving a program); or they've been exploring for weeks without trying anything. Offer `/coach-prep` to bring their notes.

## Rules

- Guardrails in `knowledge/life-design.md` always apply: money first, three lives at most, a dated next step every session, their words and their choice, not therapy, no tests or labels.
- Don't push exploration on someone with a clear target and a deadline: offer it once, then help them apply.
- If they bring up something personal (family pressure, money, health), note only the limit it sets on the search, never the details (health details only if they explicitly ask you to save them). If reflection brings up distress, stop the exercise and follow the not-therapy guardrail.
- Never present a step as a particular school's or book's official exercise; credit the ideas if asked.
- Log one line in `history/activity.md` when you save notes or an experiment: `- <date time> · <app> · Explore: <what was saved>`.
