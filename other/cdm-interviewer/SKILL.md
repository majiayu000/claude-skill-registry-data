---
name: cdm-interviewer
description: Conduct Critical Decision Method (CDM) interviews to elicit expert reasoning strategies (L3 knowledge) from practitioners about specific challenging past incidents. Use when capturing expertise for skill development, preserving knowledge before practitioner departure, building post-incident learning artifacts, or investigating decisions in complex sociotechnical systems. Outputs structured incident reconstructions with cues, decisions, alternatives considered, and counterfactual analysis suitable for distillation into skills or training material.
license: Apache-2.0
io-contract:
  kind: deliverable
  produces:
    - kind: report
      description: Structured CDM incident artifact with timeline, decision points, extracted heuristics, anti-patterns, and provenance
---

# CDM Interviewer

Critical Decision Method (CDM, Klein 1989) is a retrospective interview protocol for eliciting **expert reasoning strategies** — the L3 knowledge that doesn't appear in documentation because experts can't articulate it abstractly. CDM works because it grounds elicitation in a *specific challenging past case*, then uses structured probes to surface cues, alternatives, and counterfactuals the expert wouldn't reach unprompted.

The output is the densest L3 input you can get for skill authoring or knowledge preservation: when-then heuristics with the actual cues that fire them, alternatives considered and rejected, and discrimination knowledge separating expert from novice.

## When to use

Use CDM when:
- A practitioner has just resolved a non-routine situation and the reasoning is fresh
- Capturing expertise from someone retiring, leaving, or rotating off a domain
- Investigating an incident where standard procedures didn't fully apply
- Building a knowledge base or SKILL.md and you need real strategies, not textbook procedures
- The same domain keeps producing expert/novice performance gaps you want to close
- You suspect a skill is heavy on L1/L2 but missing the L3 that makes it generative

Do NOT use CDM when:
- The situation was routine — CDM probes will surface nothing interesting
- You only have 15 minutes — the protocol needs 60–90 minutes minimum
- The expert is uncomfortable sharing failures — psychological safety must precede CDM
- You want general advice — CDM is case-specific by design and resists generalization

## The four sweeps

CDM is **not** a question list. It's four passes through the same incident with different analytical lenses. Each sweep depends on the previous; running them out of order destroys the scaffolding.

### Sweep 1 — Incident selection and ground (10–15 min)

Goal: lock onto ONE specific incident, not a composite or "typical" case.

A CDM-worthy case satisfies at least one of:
- **Non-routine**: standard procedures didn't fully apply
- **High-stakes**: real consequences, not a drill
- **Intuition-heavy**: the expert had "I just knew" moments
- **Counterfactually interesting**: a novice would have done something different
- **Memorable**: the expert can date it, place it, name people involved

Reject: hypotheticals, "in general," composite cases, recent-but-routine incidents.

Opening probe: *"Tell me about a time when [domain] went sideways and you had to figure something out. Pick one specific incident — date, place, who was there."*

If the expert offers multiple, pick the one with the most counterfactual interest. If they offer a routine case, push back: *"Was that hard? What about a time it was actually hard?"*

Output: incident name, date, expert's role, 2–3 sentence summary, and confirmation that the expert can recall specifics.

### Sweep 2 — Timeline construction (15–20 min)

Goal: build an event-by-event chronology, **no analysis yet**.

This is harder than it sounds. Experts will jump to interpretation ("so I realized that..."). Pull them back to "what happened next" until the timeline is dense enough to identify decision points.

Probes:
- *"Walk me through it from the beginning. What happened first?"*
- *"Then what?"*
- *"Where were you when X happened?"*
- *"Who said what?"*
- *"How long did that take?"*

Mark **decision points (DPs)** as you go — moments where the expert chose between options or applied judgment. Don't probe DPs yet. Just mark them with a flag in your notes.

Output: numbered timeline with timestamps (or relative times), 5–15 events, with 3–8 decision points flagged.

### Sweep 3 — Deepening at decision points (25–35 min)

Goal: at each marked DP, surface cues, alternatives, expertise. **This is where the L3 lives.**

Work the probe library (see `references/probe-library.md`). Minimum probes per DP:

| Probe family | Question | What it surfaces |
|---|---|---|
| Cues | "What were you noticing right then? What told you something was off?" | Perceptual triggers |
| Knowledge | "What did you know that made you read it that way?" | L1/L2 anchors |
| Analogues | "Did this remind you of any other situation?" | Pattern matching |
| Options | "What other options did you consider? Why not those?" | Discrimination criteria |
| Experience | "How did past experience guide you here?" | Tacit expertise |
| Time pressure | "How much time did you have to decide?" | Decision economics |
| Confidence | "How confident were you? What would have changed your mind?" | Uncertainty handling |

**Diagnostic for "sweep done"**: the expert says something like *"huh, I've never thought about it that way"* or *"I didn't realize I was doing that."* If they're only restating the timeline, you haven't deepened.

If the expert says "I just knew," that's the *start* of the conversation, not the end. Probe: *"What were you noticing? If I'd been standing next to you, what would I have seen but missed the meaning of?"*

### Sweep 4 — What-if and novice errors (10–15 min)

Goal: counterfactual probes that expose discrimination knowledge.

Probes (in order of typical yield):
1. *"What if you'd had less experience? Where would a novice have gone wrong here?"* — single highest-yield question in CDM
2. *"What if [key cue] had been absent? What would you have done?"*
3. *"Was there information you wished you had at that moment?"*
4. *"If this happened again tomorrow, would you do anything differently?"*
5. *"What advice would you give a less experienced [role] facing this?"*
6. *"Is there anything about this incident you've never told anyone, or that you assume everyone knows but might not?"*

The novice-error probe surfaces the discrimination that separates expert from journeyman, which is exactly what L3 skill content should encode. The "never told anyone" probe consistently yields surprises in the last 10% of session time — never skip it.

## Mental models

**Case-based, not abstract.** "How do you generally handle X?" produces textbook answers. "On October 14th when the alarm went off, what did you do?" produces real reasoning. Always anchor in the specific. When the expert drifts to generalities, redirect: *"Going back to that day — what was happening at that moment?"*

**Scaffolding, not extraction.** The expert isn't withholding knowledge; they don't have it indexed in a form interviews can pull from. Your probes give them a structure to discover their own reasoning. Diagnostic: if the expert says *"I've never thought about it that way,"* scaffolding is working. If they sound rehearsed, you're getting documentation, not expertise.

**Multi-pass retrospection.** Each sweep adds a layer the previous didn't access. Don't merge sweeps. Don't skip Sweep 2 because you're impatient — without a timeline, Sweep 3 has nothing to anchor to.

**Respectful challenge.** *"How did you know it wasn't [alternative]?"* is more productive than *"tell me more."* Challenge surfaces the discrimination criteria experts can't articulate when only asked to describe. Frame challenge collaboratively: "I'm trying to understand the difference between this and [alternative case]" — never adversarially.

**The gold is at the edges.** Workarounds, "naughty" departures from procedure, intuitive leaps the expert can't justify — these are where evolved L3 lives. Probe these especially. Do not treat departures from documented procedure as errors to investigate; treat them as candidate expertise to capture.

**Heuristics > narratives.** Stories are the raw material. The deliverable is when-then rules anchored in observable cues. After Sweep 4, force one explicit translation pass: "Let me try to capture this as a rule. Tell me where I'm wrong: *When [cue], because [reason], do [action], unless [exception].*"

## Output format

CDM sessions produce a structured artifact. See `references/output-format.md` for the full template. Required sections:

1. **Incident summary** (3 sentences max — what, when, outcome)
2. **Timeline** (numbered events with timestamps)
3. **Decision points** (one section per DP: situation, cues, options considered, choice, rationale, time pressure, confidence)
4. **Heuristics extracted** — *the deliverable for skill authoring*. Each in the form: **When [observable cue], because [causal reason], do [action], unless [exception].**
5. **Anti-patterns observed** (what novices would have done wrong, with explicit cues for the trap)
6. **Open questions** (what the expert couldn't articulate; candidates for further sessions)
7. **Provenance** (date of session, expert's role, interviewer, consent for use, anonymization status)

The heuristics section is what gets distilled into SKILL.md L3 content. Each heuristic should be falsifiable in principle — if a heuristic can't be wrong, it's not a heuristic, it's a tautology.

## Reference files

| File | When to load |
|------|--------------|
| `references/four-sweeps.md` | Detailed protocol and timing for each sweep; what "done" looks like; how to recover when a sweep stalls |
| `references/probe-library.md` | Full probe catalog organized by purpose — cues, knowledge, analogues, options, experience, time, confidence, novice errors, counterfactuals |
| `references/case-selection.md` | How to ground the expert in a specific case; how to redirect when they drift to abstractions; what to do when no case comes to mind |
| `references/output-format.md` | Structured artifact template; how to extract heuristics for skill deposits; provenance requirements |
| `references/anti-patterns.md` | Common ways CDM sessions fail (interviewer-side and expert-side) and how to recover mid-session |

## Anti-patterns

**Asking abstract questions first.** *"Tell me how you think about X in general."* Wrong. Always anchor to a specific case before any abstraction.

**Skipping the timeline.** Trying to probe decisions before establishing what happened. Decision probes need event anchors, or the expert reconstructs a plausible-sounding story rather than recalling actual reasoning.

**Treating workarounds as errors.** The expert says *"well, I'm not supposed to do this, but I always..."* Stop. That's gold. Probe deeper. Do not lecture about procedure. The procedure was written; the workaround was *learned*.

**Single-pass interviewing.** One pass through the case yields surface answers. The expert needs the second pass to discover their own knowledge through your scaffolding.

**Accepting "I just knew."** Probe: *"What were you noticing? If I'd been standing next to you, what would I have seen but missed the meaning of?"*

**Letting the expert generalize.** *"Usually I would..."* Pull back: *"On this specific occasion, what did you do?"*

**Closing too early.** When the expert seems done, ask one more thing: *"Is there anything about this incident you've never told anyone, or that you assume everyone knows but might not?"* The last 10% of yield often comes from that one question.

**Failing to capture provenance.** Heuristics without source attribution become unfalsifiable folklore. Always record: who said this, about what incident, on what date, with what consent for downstream use.

## Shibboleth

Someone running real CDM will:
- Refuse to start before a specific incident is locked
- Maintain four distinct sweeps and resist merging them under time pressure
- Treat "I've never thought about it that way" as the success signal
- Probe workarounds harder than procedure compliance
- End every session with a heuristics-extraction pass, not just notes

Someone doing CDM cosplay will:
- Open with "tell me how you generally approach X"
- Skip the timeline because "we already discussed what happened"
- Accept "I just knew" as a final answer
- Treat departures from procedure as concerning rather than informative
- Hand over an interview transcript without distilled heuristics
