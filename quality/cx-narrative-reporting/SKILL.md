---
name: cx-narrative-reporting
description: Use to write CX commentary that makes a number decision-ready — what moved, why (decomposed), so what, do what — separating noise from signal and stating confidence honestly. Trigger for "write the commentary", "explain this trend", "what should we say about the drop", weekly or monthly narrative, board pack prose, "why did QA fall", metric movement write-up, or when a report has charts but no story.
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: playbook
---

# Narrative reporting

The chart is done. The number moved. The commentary says "QA fell 4pts driven by
Team B's lower scores."

That sentence is wrong more often than it is right — and it is still the template
most reports use, because naming a team is easier than proving the move is real,
splitting mix from performance, and saying what anyone should do about it.

This skill writes commentary that survives the reply-all thread: structured, honest
about uncertainty, and tied to a decision or a deliberate non-decision.

## The four-part structure

Every metric narrative answers four questions in order. Skip or reorder them and
readers fill the gaps with assumptions.

| Part | Question | Length |
| --- | --- | --- |
| **What moved** | Direction, magnitude, period, comparison, denominator | One sentence |
| **Why** | Decomposed cause — rate, mix, coverage, composition, definition | One short paragraph |
| **So what** | Customer, cost, or risk implication if the move is real | One or two sentences |
| **Do what** | Named action, owner, or explicit "no action yet" with trigger | One sentence |

Example skeleton (fill with verified content only):

> **What:** QA mean score fell 3.1 points (78.2 → 75.1) week-on-week on n=412
> completed evaluations, ISO week 30 vs 29, same scope and definition v4.
>
> **Why:** The move exceeds sampling noise (95% interval ±1.8pts). Decomposition
> shows ~70% mix (higher share of chat, structurally lower scores) and ~30% rate
> (chat itself scored lower). Coverage was stable; no definition change.
>
> **So what:** If chat share stays elevated, headline QA will run below target even
> if chat quality stabilises — the aggregate is a mix story as much as a quality story.
>
> **Do what:** Team lead for chat to confirm whether the chat rate drop is real in
> isolation by Friday; no headcount change until then.

If **what moved** fails the noise check, stop after stating that. Do not write why,
so what, or do what for noise — the correct do what is "no action; recheck next
period."

## Step 1: noise before narrative

Before any "why", establish whether the movement exceeds what random sampling
would produce. If you cannot compute an interval, say "direction only; n too
small for confidence" — do not borrow confidence from tone.

Rules:

- **Inside noise** — report the interval, state "no action recommended", do not
  decompose. Decomposing noise invents drivers.
- **Borderline** — say borderline; prefer no action unless the cost of waiting is
  high and the proposed action is reversible.
- **Outside noise** — proceed to decomposition.

Weekly reports that flag "significant" moves at 95% without multiplicity correction
will cry wolf — either widen thresholds for segment flags or label them "for review,
not action."

## Step 2: decompose before blaming

Aggregate rates move for four channels: **rate change**, **mix change**, **coverage
change**, and **composition change** (entrants/exits). Check coverage before
attributing a rate story — especially for QA and CSAT.

In prose:

- Lead with the **headline split** (rate vs mix vs entrants) in the metric's own
  units, not percentages of percentages.
- Rank segments by **contribution to the move**, not by worst rate.
- Name **definition or instrument change** before team performance — rubric changes
  look like collapses.
- State **what you ruled out** in one clause when it matters.

If decomposition is not available, say "cause not decomposed" rather than guessing.
"We could not split mix from rate with current data" is acceptable; a invented team
name is not.

## Step 3: so what without drama

**So what** connects the number to something the reader cares about — customer
experience, cost, risk, forecast credibility — without catastrophising or cheerleading.

- Tie to **threshold or target** only if the target is agreed and the definition
  matches.
- Distinguish **structural** (mix, definition) from **operational** (rate, process).
- If implications depend on an unverified mechanism, say "if X holds, then Y" — not
  Y as fact.

Avoid: "customers are suffering" without evidence; "great progress" on a move that
is mostly mix or noise.

## Step 4: do what with accountability

Every narrative ends with one of:

- **Named action and owner** — specific, proportionate to evidence.
- **Deliberate wait** — what you are waiting to see, and when you will reconsider.
- **No action** — inside noise or immaterial to targets.

"Monitor closely" without a trigger is not an action. "Share with leadership" is
not an action unless someone is decision-ready.

Actions must match confidence:

| Evidence | Appropriate action |
| --- | --- |
| Noise | None |
| Real but unexplained | Investigate by date X; no irreversible moves |
| Real, decomposed, mechanism plausible | Scoped operational change |
| Definition break | Fix registry and relabel series; do not coach agents |

## Voice and honesty

- **British spelling** where natural; **plain sentences** over jargon.
- **Denominator always adjacent** to rates in the narrative body.
- **No invented confidence** — "likely", "suggests", and "we ruled out X" beat false
  precision.
- **Separate changed from notable** — most periods have nothing worth a paragraph;
  saying "no material movement" is valuable.
- **Data notes in prose** — late arrivals, suppressed cells, restatements, definition
  version — one sentence at the end, not omitted.

## Traps

- **Explaining noise** — the most common way narratives lose trust.
- **Team name as cause** — correlation from lowest rate, not contribution.
- **Relative vs absolute change** — "5% drop" when you mean five points on a rate.
- **CSAT or QA without response/coverage context** — when composition shifted.
- **Confidence by adjective** — "significant" without the interval shown.

## Present results to the user

1. **Noise verdict** — interval or explicit "n too small", and whether to proceed.
2. **Four-part narrative** — what moved, why, so what, do what.
3. **Decomposition summary** — rate vs mix vs composition, top contributing segments
   with denominators.
4. **Confidence statement** — what is established, what is hypothesised, what was
   ruled out.
5. **Alternative readings** — at least one plausible counter-explanation if evidence
   is partial.
6. **Data notes** — late data, suppression, definition version, comparability limits.
