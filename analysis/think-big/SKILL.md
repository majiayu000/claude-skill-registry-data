---
name: think-big
version: "1.0.0"
user-invocable: true
description: Strategic thinking framework — analyze whether something is worth doing, what the risks are, and what the long-term impact will be. Use when user says 「战略思考」「战略分析」「从战略角度看」「战略视角」「帮我想清楚这件事」「这件事值不值得做」「从更高视角分析」 / think-big, strategic thinking, strategy. Not for execution-level planning (that's tactical).
---

# Think Big — Strategic Thinking Framework

> Helps you step out of the execution layer and think — with a longer time horizon and broader system scope — about whether to do something, whether it's worth it, and what "doing it right" looks like.

## Triggers & Modes

| Example | Mode |
|---------|------|
| `think-big: xxx`, 「战略思考 xxx」, 「帮我想清楚 xxx」, 「这件事值不值得做 xxx」 | ⚡ Quick mode |
| `think-big --deep: xxx`, 「深度分析 xxx」, 「从战略角度深度聊聊 xxx」 | 🔍 Deep mode |

**Default**: ⚡ Quick mode when no mode is specified; 🔍 Deep mode when the trigger includes "深度", "deep", or "--deep".

**Not applicable** (state why and exit on trigger):
- User wants to plan execution details → "This is tactical; think-big focuses on strategy"
- User provides minimal context (< 2 sentences) → ask for basic background first
- User is seeking emotional comfort, not decision-making → not suited for a structured framework

---

## Core Principles

1. **Don't decide for the user**: Output analysis frameworks and insights that help the user see clearly; the final judgment is theirs
2. **Trade-offs are central**: Every strategic choice has a cost — there's no "have it all" strategy. Analysis must surface the trade-offs
3. **Essence-first questioning**: Ask "why do this" before "how to do it"
4. **Acknowledge uncertainty**: Strategic thinking isn't about giving certain answers — it's about identifying key uncertainties and figuring out how to respond

---

## ⚡ Quick Mode

Analyze from four strategic dimensions in sequence. Each dimension has guiding questions; the AI projects the user's specific situation into the analysis.

### Dimension 1: Across Time

| Time Layer | Guiding Questions |
|------------|-------------------|
| **Past** | Why did this develop into what it is now? Is there historical path dependency or sunk cost? |
| **Present** | What is the essential nature of the current state (not symptoms, but structural causes)? |
| **Future** | If nothing changes, where will things be in 1–3 years? If this is done, how will the landscape shift? |

### Dimension 2: Systems View

| Angle | Guiding Questions |
|-------|-------------------|
| **Affected parties** | Who/what teams/systems/processes will this affect? |
| **External factors** | What external forces influence this outcome (market, organization, technology, people)? |
| **Side effects** | What unintended things might change if this is done? |

### Dimension 3: Trade-offs

| Question | Notes |
|----------|-------|
| What are you giving up by choosing this? | Clarify opportunity cost |
| Is this cost acceptable? | Judge whether the trade-off is reasonable |
| Is there a "fake win-win" trap? | Beware of options that appear cost-free |

### Dimension 4: Key Unknowns

1. What are the most critical uncertainties (max 3)?
2. Which uncertainty, if it changes, would flip the entire judgment?
3. Can you validate the most critical uncertainty with a low-cost action?

### ⚡ Output Format

```
【Item】The thing the user described

【Timeline】
- Past path: ...
- Present essence: ...
- Future trajectory: Do it → ... / Don't do it → ...

【System Impact】
- Affected parties: ...
- Side effects: ...

【Core Trade-off】
- Doing this means giving up: ...
- Cost judgment: Acceptable / Needs weighing / Too high

【Key Unknowns】
1. ... (if this changes, the conclusion would...)
2. ...
3. ...

【Strategic Direction】
(Direction pointers, not decisions)
The core judgment of this matter comes down to: ...
If [key unknown X] holds, lean toward [direction A]; if not, lean toward [direction B].
Minimum validation action: ... (confirm the most important uncertainty at the lowest cost)
```

> **Note**: "Strategic Direction" provides direction pointers and validation paths only — it doesn't make the final decision for the user. Avoid "you should do X"; use conditional phrasing like "if X then lean toward Y."

---

## 🔍 Deep Mode

Socratic layered questioning that helps the user think it through themselves — the AI doesn't give answers, but guides the user to find their own judgment through questions.

### Questioning Protocol

- **⚠️ Ask ONE question at a time, then follow up across rounds until clear (hard rule)** — each turn contains exactly one question; wait for the answer, then let that answer shape your next question. Never batch multiple questions in one turn (it overloads the user and lowers answer quality). Ask via a single-question + multiple-choice format — prefer your Agent's native structured-prompting capability; if none, use plain prose.
- **Maximum 5 rounds**; after round 5, force convergence and output a synthesis
- **Before each follow-up**, acknowledge the user's previous answer in one sentence (confirm understanding + advance direction)
- **Questioning path**: Symptom → Essence → Impact → Trade-off → Action

**Convergence failure handling**: If the user gives very short answers (e.g., "don't know", "whatever") or goes off-topic for 2 consecutive rounds, stop questioning, switch to ⚡ Quick mode to complete the analysis, and note at the end: "Due to limited information, the following is based on known background."

### Questioning Path Reference

```
Round 1: "About this thing you mentioned — what's the core point that confuses or troubles you the most?"
Purpose: Locate the real problem, don't get led by surface statements

Round 2: "Why is this the core confusion? If this problem didn't exist, how would the outcome differ?"
Purpose: Dig for root cause, build causal sense

Round 3: "Looking back from 3 years later, what would be the biggest difference between doing this and not doing it?"
Purpose: Introduce time dimension, build long-term perspective

Round 4: "What are you most uncertain about right now — direction, resources, or something else?"
Purpose: Identify key uncertainties

Round 5 (convergence): "Based on what you've said, what does your gut lean toward?"
Purpose: Help the user hear their own judgment rather than relying on the AI's
```

### 🔍 Output Format (after round 5)

```
【Conversation Recap】
(3–5 sentences summarizing the user's core viewpoints and key turning points during questioning)

【Strategic Insights】
- The essential problem is: ...
- The key trade-off is: ...
- The most important uncertainty: ...

【Your Judgment】
Your expressed lean during the conversation: ...
Core reasoning supporting this judgment: ...

【Suggested Next Steps】
1. ... (minimum viable action to reduce the most critical uncertainty)
2. ...
```

---

## Use Cases

| Scenario | Recommended Mode |
|----------|-----------------|
| Judging whether a new opportunity / project is worth investing in | ⚡ Quick |
| Hitting resistance and wanting to re-examine from a higher perspective | ⚡ Quick |
| Facing a major decision, genuinely torn and lost | 🔍 Deep |
| Wanting to develop strategic thinking habits | 🔍 Deep |
| Personal warm-up thinking before a team discussion | ⚡ Quick |

## Common Misuses

- ❌ Treating think-big as a decision machine — the AI outputs perspectives, not answers; the user makes the final call
- ❌ Providing 1 sentence of background and expecting a full analysis — provide sufficient context first
- ❌ Using it for tactical execution planning — think-big only handles "should we do this and why," not "how to do it"

## Common AI Violations (REFACTOR notes)

These are natural behavioral biases when the skill isn't loaded; the skill must override them:

| Natural behavior (violation) | Correct behavior per skill |
|------------------------------|---------------------------|
| Leading with a conclusion ("probably shouldn't...") | Output the four-dimension analysis first; conclusion goes last in "Strategic Direction" |
| Free-form prose with no structure | Strictly use the `【Item】【Timeline】【System Impact】【Core Trade-off】【Key Unknowns】【Strategic Direction】` template |
| Uncertainties hinted at in paragraphs, never listed | Must explicitly list up to 3 Unknowns, each with a validation method |
| "Strategic Direction" written as "you should X" | Use conditional phrasing: "if X holds, lean toward Y; otherwise lean toward Z" |
