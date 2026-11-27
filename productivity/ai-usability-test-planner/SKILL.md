---
name: ai-usability-test-planner
description: "Plans usability studies for non-deterministic Artificial Intelligence (AI) features, choosing between Wizard-of-Oz, seeded-output, and live-model methods, and produces task scripts, variance-aware success metrics, trust-calibration measures, and a plan for pairing findings with offline evaluations. Use when usability testing a chatbot, copilot, or agent; outputs differ between participants and results are hard to compare; measuring whether users over-trust or under-trust AI; or deciding what to test before the model is ready."
---

# AI Usability Test Planner

> When the system gives a different answer to every participant, you are testing two things at once. Separate them.

## What this skill is

A study-planning workflow for features whose output varies run to run. It separates **interface quality** from **model quality** by controlling output where needed, measures whether users rely on the AI appropriately rather than just whether they like it, and connects what participants experienced to offline evaluation data so findings lead to the right fix. Use it to plan moderated or unmoderated studies at any stage, from pre-model concept to live beta.

## What it solves

- Sessions where participant A got a great answer and participant B got a poor one, making results incomparable
- Studies that measure satisfaction but not whether users caught wrong outputs
- Waiting for a working model before learning anything about the interaction design
- Usability findings that blame the interface for model errors, or the reverse
- Success rates reported from 5 participants on a system whose own output varies widely

## When to invoke

- Planning usability research for a chatbot, copilot, generative, or agent feature
- The model is not ready but the team needs interaction design feedback
- Stakeholders ask "do users trust it?" and there is no measure
- Live-model test results are noisy and contradictory
- Deciding whether a failure seen in research is a design problem or a model problem

## Phase 1: Define research questions and separate the layers

Write 3-5 research questions and tag each one:

| Layer | Example question | Needs live model? |
|-------|------------------|-------------------|
| Interaction | Can users find and use regenerate and edit? | No |
| Expectation | What do users think the assistant can do before trying it? | No |
| Output usefulness | Is a typical answer good enough to act on? | Yes, or realistic seeded outputs |
| Trust calibration | Do users catch wrong answers? | No, seeded errors are better |
| Real-world fit | Does it work on participants' own data and tasks? | Yes |

## Phase 2: Choose the method

| Method | How it works | Best for | Limitation |
|--------|-------------|----------|-----------|
| Wizard-of-Oz | A hidden researcher writes or selects responses in real time | Pre-model concepts, agent flows, conversation design | Wizard is smarter and slower than the real model |
| Seeded-output | Pre-generated responses, including deliberate errors, served per task | Trust calibration, comparing interface variants fairly | Less natural; participants cannot go off-script |
| Live model, fixed inputs | Real model with set prompts, temperature lowered where possible | Output usefulness with less variance | Still some variation |
| Live model, open use | Participants use their own tasks | Real-world fit, discovery | High variance; needs more participants |
| Diary or field study | Use over 1-4 weeks | Trust change over time, habit formation | Slow, less control |

Combine methods across rounds: Wizard-of-Oz or seeded first to fix interaction issues, live model later to validate.

## Phase 3: Write the task script

For each task specify:

| Field | Content |
|-------|---------|
| Scenario | Realistic goal in the participant's terms |
| Starting state | Data, page, and context loaded |
| Output condition | Seeded correct / seeded subtle error / seeded obvious error / live |
| Success criteria | Observable end state, defined before sessions |
| Probes | Questions asked after the task, not during |

Seeded-error guidance:
- Include at least one **subtle, plausible error** (wrong number, outdated policy, wrong recipient) in 20-30 percent of tasks
- Counterbalance which tasks contain errors across participants
- Disclose seeded errors at debrief; obtain consent for deception in the study protocol

## Phase 4: Define variance-aware metrics

| Metric | Formula or method |
|--------|-------------------|
| Task success | Percent of attempts meeting success criteria, reported by output condition |
| Appropriate reliance | (Correct outputs accepted + Wrong outputs caught) / Total AI outputs seen |
| Over-reliance rate | Wrong outputs accepted / Wrong outputs seen |
| Under-reliance rate | Correct outputs rejected or redone manually / Correct outputs seen |
| Recovery time | Time from wrong output to corrected state |
| Edit distance | Share of AI output changed before use |
| Trust rating | Pre-task and post-task 1-7 rating, compared with actual output quality |

For live-model conditions:
- Log every model output shown, so each observation can be tied to output quality
- Report results split by output quality (good, acceptable, poor), not pooled
- Plan for more participants: 5-8 per segment is enough for interaction issues; reliance and success rates need 12 or more per condition, or report them as directional only

```
Trust calibration gap = Post-task trust rating (normalized 0-1) - Actual accuracy of outputs that participant saw
Positive gap = over-trust; negative gap = under-trust
```

## Phase 5: Pair with offline evaluations

Usability findings and offline evaluation (automated or expert-graded test sets) answer different questions. Connect them:

| Research observation | Offline evaluation follow-up |
|----------------------|------------------------------|
| Participants received poor outputs on a task type | Check that task type's accuracy in the evaluation set; add cases if missing |
| Participants phrased requests differently than the evaluation set assumes | Add real participant phrasings to the evaluation set |
| Users missed a seeded error type | Prioritize evaluation and guardrails for that error type |
| Users succeeded despite mediocre outputs | Evaluation thresholds may be stricter than needed for this task |

Tag every finding as **interface**, **model behavior**, or **both** before it enters the backlog.

## Phase 6: Plan logistics and synthesis

- Participant mix: include novice and experienced AI users; reliance patterns differ sharply
- Pilot with 1-2 sessions to test seeded outputs and wizard timing (match realistic latency)
- Synthesis grid: tasks by participants, with output condition and reliance outcome in each cell

## Output

- Research questions tagged by layer
- Method plan per round with rationale
- Task scripts with output conditions and success criteria
- Seeded-output set including counterbalanced errors
- Metric definitions with reliance and trust-calibration formulas
- Offline evaluation pairing plan and finding-tagging rules
- Consent and debrief language for seeded errors

## Operating rules

**Always**
- Separate interaction questions from model-quality questions before choosing a method
- Seed at least one plausible error to measure over-reliance
- Log the exact output each participant saw
- Report live-model results split by output quality
- Tag each finding as interface, model behavior, or both

**Never**
- Pool success rates across participants who saw different quality outputs
- Treat satisfaction or trust ratings alone as evidence of appropriate reliance
- Let a Wizard-of-Oz study respond faster or better than the real system will
- Run seeded-error studies without consent and debrief
- Report percentages from small samples as precise
