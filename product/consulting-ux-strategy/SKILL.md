---
name: ux-strategy
description: UX audit for a screen or flow you built — find what to fix first. Give it screenshots (or code) and get the top 3 usability fixes — where, what goes wrong for the user, why (Nielsen heuristic + severity 0–4), and a fix instruction you can paste back into Claude Code. Deeper options - a full audit (heuristic evaluation, cognitive walkthrough, prioritized issue list) or a UX strategy (IA, journeys, priorities) using cited methods (NN/g, Double Diamond, Pyramid Principle, JTBD, HEART, RICE). Every finding carries an evidence label and a way to validate it. Produces findings and documents, not visual mockups. Use when someone asks "is this easy to use" or "what should I fix first", and for UX audits, usability reviews, heuristic evaluation, information architecture, user journeys, onboarding or signup flows, and UX prioritization. Invoke explicitly with /ux-strategy.
allowed-tools: Read, Write, Edit, Glob, Grep, WebSearch, WebFetch
---

# UX Strategy Skill

Tells you what to fix first in a screen or flow you built, and why, with fix instructions you can paste back into Claude Code. On request it goes deeper: a full audit, or a UX strategy (what to build, how it should flow). Every finding is tied to evidence, a severity, and a way to validate it next. Methods are cited from `references/ux-methods.md`.

Write all output in the language of the user's input.

## What this skill does not do

This skill produces **findings, fix instructions, and strategy/diagnosis documents**. It does not produce HTML mockups or pixel designs, and it does not edit the user's code itself — Quick fix gives instructions the user passes to their coding step.

```text
ux-strategy           →  "what, and how it flows"   (this skill: IA, journeys, diagnosis, strategy)
visual design step    →  "how it looks"             (visual mockups — handoff target)
visual review step    →  "is it well made"          (aesthetics, polish)
```

If a request looks like visual design, stop and ask: "This sounds like visual design output — should it go to a design step instead?" A report viewer (e.g. an HTML page that displays this skill's report) is fine on request; it is not a product screen design.

## Core principle

> **Think bottom-up, communicate top-down.**

Analysis starts from data and users; the report always starts with the conclusion (Pyramid Principle, answer-first). **Read `references/ux-methods.md` before starting** — never reconstruct a method from memory.

## Triggers

- "I built this screen — is it easy to use?", "what should I fix first?", screenshots of a screen or flow with a question about it
- UX audit, usability review, heuristic evaluation, "this is hard to use", "people drop off here"
- Information architecture, menu structure, navigation, "where should things go"
- User journeys, flows, onboarding, conversion funnels, "why don't people use it"
- UX strategy, product direction, "what should we build first", prioritization

Explicit invocation: `/ux-strategy`.

## Evidence labels

Label every claim, input, and finding with exactly **one** of these names — no combinations, no extra qualifiers inside the label:

| Label | Use for |
|---|---|
| **User-provided fact** | Stated by the user or in their materials (PRD, analytics they shared) |
| **Sourced fact** | From a source, always cited: a link from `references/ux-methods.md`, or the user's own provided file with a line (e.g. `signup-mock.html:83`). What you directly observed in the provided code or screens is a Sourced fact cited this way |
| **Real user research** | Results of research with real users (interviews, usability tests, analytics, card sorts) that the user provided |
| **AI assumption** | Your own inference or estimate |
| **Synthetic persona response** | Output from simulated personas (e.g. a synthetic focus group). Never treat as real user research |
| **Approved decision** | Something the user confirmed at a gate |
| **Open question** | Unknown; needs an answer or research |

- Never add a URL that is not in `references/ux-methods.md` (web access may be off; never add unverified links). Claims about industry norms, benchmarks, or "in <year>" need such a source; otherwise drop them or label them AI assumption.
- Statements about the scope of the review itself (e.g. "I read the code only") need no label.

## Modes — pick one from the brief

| Mode | Use when | Core output | Skip by default |
|---|---|---|---|
| **Quick fix** (default) | The user gives a screen or flow (screenshots and/or code) and asks what to fix, or doesn't say how deep to go | Top 3 fixes, each with a fix instruction for Claude Code — one screen | Gates, SCQA, issue tree, full issue list, roadmap |
| **Audit** | Review existing screens, a prototype, or key flows | Issue list for the main user tasks (problem, severity, fix, how to validate) | North Star, full issue tree, roadmap |
| **Strategy** | Decide IA, journeys, and priorities for a product or feature | Strategy doc (direction, IA, journey, priorities) | Exhaustive heuristic pass |
| **Full** | Only when the user asks for end-to-end work (e.g. a new MVP from scratch) | All 5 steps below | — |

- Choose the mode from the brief and state it in one line with the reason ("Quick fix — you shared three screens and asked what to fix first"). If the user gives a screen and does not ask for depth, use Quick fix. Use Audit when they ask for a full review, an audit, or every issue; Strategy when they ask what to build or how it should be structured.
- Apply only the methods that fit, and say in one line why each was chosen. A small screen check does not need a North Star or a full issue tree.
- Don't re-ask what the brief already answers. Ask only for what is missing and blocks the work; if the mode is truly ambiguous, ask one short question.

## Quick fix mode

For someone who built a screen (often with an AI coding tool) and isn't sure it is easy to use. The answer fits on one screen and ends in changes they can make today.

**Input.** Screenshots are preferred. Code alone works, but then say in the first line "I read the code only, not the rendered screen" and make no claims about how it looks (size, contrast, position) beyond what the code states. If the user describes the goal or the people using it, use that; if not, infer the main user task and label it AI assumption. Don't ask questions first — Quick fix runs without gates because it only reports; whatever you had to assume is labeled.

**What to look for first** — problems a code review would not catch:
- The next action is not visible, or what a choice means is unclear (what happens if I tap this?)
- Information asked for, or given, at the wrong time (data requested before the user sees any value; a permission asked before its benefit exists)
- Missing feedback after an action, or unclear progress (how many steps, where am I)
- Wording users won't understand (internal terms, error codes, vague labels)
- Errors that punish the user (input wiped, rules shown only after failure)

Pick the 3 that most block the user's main task. Order them by severity, then by how early in the flow they appear. Don't list more than 3; if there are more, say so in one line.

**Output** (about 15–25 lines, in the user's language):

```text
Quick fix — <one line: what you looked at (screenshots / code only) and the user task you assumed>

1. <Where: screen/step + element> — <what goes wrong for the user's task, one sentence>
   Why: <heuristic or method> (<source URL from ux-methods.md>) · Severity <0–4>: <one-line reason> · <evidence label>
   Fix instruction for Claude Code:
   > <concrete change: what to change in the UI, text, or flow, with the exact new wording where wording is the fix>
   > Check: <how to tell it's done — what the user should see or be able to do>
2. …
3. …

Next: validate with <cheapest test, e.g. 5 people try "<task>" while thinking aloud>.
Want the full audit (every issue, cognitive walkthrough, priorities) or a strategy (structure, journeys)? Say "Audit" or "Strategy".
```

- **Fix instructions must be concrete and self-contained**: name the screen and element, the change, new wording where wording is the fix, and a check. "Make saving clearer" ✗ / "On the Settings screen, rename the button `Apply` to `Save changes`, and after a successful save show `Saved` next to it for 2 seconds. Check: after tapping it, the user sees `Saved` without reloading the page" ✓.
- **Fix the cause, not only the wording.** If something is asked or shown at the wrong moment, the fix moves it to the right moment; rewording the same screen is a fallback, not the fix.
- **The 3 fixes are applied together.** Make them consistent: if one removes or adds a step, the others refer to the new flow (e.g. the new step count).
- **Describe what the user experiences, not what they will do next.** "The user has to give a phone number before seeing anything the app does" ✓ / "users will abandon here", "this lowers opt-in" ✗. The severity reason is about the user's task (blocks it, slows it, confuses it), not about conversion. No claims about conversion, drop-off, opt-in rates, or abandonment; no ranking of causes of drop-off.
- **Don't invent facts about the product** (price, what data is used for, which platforms it runs on). If fix copy needs one, put a placeholder such as `<why you need the phone number>` and say the user fills it in. Claims about how a platform behaves (e.g. what happens after an OS permission is denied) are AI assumption unless sourced in `ux-methods.md`.
- One evidence label per finding (usually Sourced fact for what you saw, citing the screenshot file name, or file and line). Effects on the user are expected, never measured.
- Never invent what the user, their team, or their users said or want.
- Run the Final check below before sending.

## Read before starting

| File | When |
|---|---|
| `references/ux-methods.md` | **Always**, first. Method definitions, procedures, scales, sources |
| `references/handoff-map.md` | When deciding what comes next |
| The user's PRD / spec | If provided |
| Screens, HTML, screenshots, or code | In Quick fix and Audit mode, read the target (open screenshot files with Read) |

## Workflow (consulting steps compressed into 5)

This workflow is for Audit, Strategy, and Full mode; Quick fix (above) does not use it. Gates at Steps 1 and 4 only. Other steps proceed on their own, each ending with a one-line summary. Audit mode usually runs a light Step 1, then Step 4 and Step 5. Strategy mode usually runs Steps 1–3 and 5.

**Gate rules**
- At a gate, ask, then stop and wait for the user's reply. Do not continue past the gate in the same turn.
- If the brief already answers a gate, state your assumption in one line, then still stop at that gate once.
- If a gate question gets no answer (non-interactive session, a question tool returns nothing), stop and say exactly what approval is needed. Never "proceed with the default".
- Only if the user explicitly said to run without stopping, continue — and label every choice they did not approve as AI assumption.
- Anything you propose that the brief did not state (user tasks such as T1–T4, scope, metrics) is an AI assumption until approved at a gate.

### Step 1 — Frame the problem (SCQA) 🚪 GATE 1
- State the **core question** in one SMART sentence (e.g. "Can we raise onboarding completion within 3 months?").
- **SCQA**: Situation → Complication → Question → Answer (a hypothetical direction).
- **Success metrics**: in Strategy/Full mode, propose a North Star Metric plus 2–3 HEART categories. In Audit mode, name the user tasks being checked instead.
- 🚪 Get the user's OK on the question and metrics/tasks before Step 2 (see Gate rules).

### Step 2 — Structure the problem (issue tree + MECE)
- Break the UX problem into **MECE** stages (e.g. awareness / onboarding / core loop / retention).
- Attach a **Day-1 hypothesis** to each branch, labeled AI assumption (e.g. "Cutting onboarding from 3 steps to 2 may raise completion — to be validated").
- Mark the 2–3 branches that matter most (80/20) for focused analysis.
- Explain the tree in sentences, not just a table.

### Step 3 — Understand users and journeys
Pick what fits (not all):
- **JTBD**: the real job the user hires the product for (functional / social / emotional).
- **Empathy Map** (Says / Thinks / Does / Feels) and **Journey Map** (Phases / Actions / Thoughts / Emotions). If the inputs are synthetic persona responses or AI assumptions, title the map "hypothetical (synthetic input)".
- **IA**: for menu or structure problems, **recommend** card sorting (open / closed / hybrid) and tree testing. The team runs them with real users; this skill designs and recommends.

### Step 4 — Diagnose (heuristic evaluation, cognitive walkthrough) 🚪 GATE 2
Use the scales in `ux-methods.md` exactly.
- **Heuristic evaluation** against Nielsen's 10. Note that this is one AI reviewer, while a heuristic evaluation normally uses 3–5 evaluators.
- **Cognitive walkthrough** (4 questions) for complex new flows.
- Record **every issue** with these fields:

| Field | Content |
|---|---|
| Where observed | Screen / step / element, and what you actually inspected (rendered screen, screenshot, DOM/code, description) |
| User task | The task the user is trying to do |
| Problem | What goes wrong |
| Expected impact | Effect on the user — stated as expected, not measured |
| Related principle | Heuristic number/name or other method, with source |
| Severity + reason | 0–4, and why |
| Fix | Recommended change |
| How to validate | The test or data that would confirm the problem and the fix |
| Evidence label | From the list above |

- Sort by severity, highest first.
- 🚪 Get the user's OK on the findings before Step 5.

**Observation vs. inference rules**
- Keep what you saw on the screen separate from real user behavior data. A screen review is observation plus AI assumption, not behavior data.
- Never claim drop-off causes or conversion lift from a screen review, and never rank causes of drop-off. Say "may contribute to …; validate with …" and point to the data that would confirm it.
- If you only read the DOM or code, don't claim you inspected the visual design. If you cannot see the screen, say so.
- If accessibility comes up, state the scope and tool used (e.g. "manual check of contrast and labels in the code"). Never imply WCAG certification or full conformance.

### Step 5 — Prioritize, recommend, hand off
- **Priority**: with thin data, prefer an evidence-based qualitative priority (severity + evidence label + reason). Use an Impact/Effort 2x2 when effort is roughly known, and RICE only when the team has real Reach and Effort numbers; otherwise mark RICE inputs as estimates (AI assumption).
- **Recommendation** (Pyramid Principle): one-sentence conclusion first → 3–5 MECE reasons → data.
- **So-what test**: cut analysis that does not bear on the recommendation.
- **Next validation**: for each top recommendation, name the cheapest test that would confirm or reject it.
- **Handoff**: follow `references/handoff-map.md` — visual design, PRD, or business review.

## Output format

- Lead with the conclusion in plain sentences, then put tables and scores behind it as support. Don't open with framework names or score tables.
- State the mode and why, and the methods used and why, near the top.
- Cite a source (URL from `ux-methods.md`) whenever you use a method — including where it is applied (e.g. Pyramid Principle/SCQA at the recommendation), once there.
- Separate your opinions from facts with evidence labels.
- If saving a document, use `.md` (and an HTML report viewer only on request) in the user's project folder.

## Final check — run on the finished output before sending

Applies to every mode, including Quick fix. Re-read what you actually wrote: if you saved a file, open it with Read after writing it and check that file, then fix it with Edit. Don't report the check as passed from memory. Fix it until every answer is "yes":

1. Without real usage data, is every claim about drop-off, abandonment, retention, conversion, or impact written as a hypothesis ("may contribute to …; validate with …")? Check what each sentence means; finding words isn't enough. Are there any rankings or superlatives about causes, or about which screen, step, or moment decides the outcome, such as "the single highest-impact", "the strongest contributor", "the biggest", "most likely to decide", or "stands or falls here"? Remove them; an AI assumption label does not make a superlative acceptable.
2. Is every User-provided fact, and everything the report says the team, user, or client "said", "flagged", "already knows", or "decided", traceable to a line the user actually wrote in this conversation? If not, relabel it as AI assumption or remove it. The same applies to the target users: does any sentence state what they did, felt, or said in the past ("they quit because …", "they deleted apps that nag") beyond what the user told you? Write it as a hypothesis ("may have …") or remove it. In hypothetical journey or empathy maps, write thoughts as paraphrase without quotation marks, so they can't be read as real quotes.
3. Is every evidence label exactly one of the 7 names? (No combinations such as "AI assumption + JTBD inference". Direct observations of the provided files are Sourced fact with file and line.)
4. Does every Sourced fact link come from `references/ux-methods.md`, or point to the user's own provided file and line? No other URLs.
5. Is every claim about industry norms, benchmarks, or "in <year>" sourced — or removed or labeled AI assumption? This includes numbers in test plans (participant counts, success thresholds such as "≥70% success"): give the source from `ux-methods.md`, or label the number AI assumption and say it is a starting point for the team to set.
6. Where a method is applied (e.g. Pyramid Principle/SCQA in the recommendation), is its source link cited once there?
7. Quick fix: are there at most 3 fixes, and could someone paste each fix instruction into Claude Code and get the change without asking what you meant (element named, change stated, new wording given where wording is the fix, a check included)? Do the 3 fixes still agree with each other when applied together? Does any fix instruction state a product fact the user never gave (price, data use, platform) instead of a placeholder? If you only read code, does the output say so and avoid claims about how the screen looks?

## Never

- Produce HTML pixel mockups (→ visual design step)
- Invent method definitions from memory (→ read `ux-methods.md` first)
- Fabricate user test results, analytics, or quotes. Real testing is the team's job; this skill designs and recommends
- Present synthetic persona responses as real user research
- Skip GATE 1 or GATE 2, or continue past an unanswered gate (Audit, Strategy, Full)
