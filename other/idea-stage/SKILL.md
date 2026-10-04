---
name: idea-stage
description: This skill should be used when a founder wants to validate, pressure-test, or kill a startup/product idea before building it — sharpening a hunch into a testable hypothesis, red-teaming it, sizing the market, mapping competitors, designing and synthesizing customer-discovery interviews, and deciding whether the evidence justifies an MVP. Triggers on "validate my idea", "is this worth building", "should I build this", "test my hypothesis", "problem-solution fit", "customer discovery", "I have a startup idea", "poke holes in this idea", "ایده‌ام رو بررسی کن", "این ایده ارزش ساختن داره؟", "اعتبارسنجی ایده", "فرضیه‌سازی", "فرضیه‌ام رو تست کن", "مصاحبه با مشتری طراحی کن", "ایده استارتاپی دارم", "بسازم یا نه". Implements Chapter 3 (Idea Stage) of The Founder's Playbook. Do NOT use for MVP scoping, launch, or scaling work — use founder-playbook:stage-map to route those.
version: 1.0.0
---

# Idea Stage — validate before you build

Implements Chapter 3 of *The Founder's Playbook: Building an AI-Native Startup* (Anthropic, 2026).

The entire stage answers one question: **is this worth building?** It ends at **problem–solution fit** — qualitative evidence, primarily from real human conversations, that a real problem exists for real people and that the proposed solution addresses *the problem discovery revealed*, not the one originally assumed.

The book's core warning drives every rule below: agentic coding collapsed the distance between "I have an idea" and "I have a product," and AI research gave confirmation bias an engine. 42% of startups failed by building something nobody wanted — before AI made building nearly free. This skill exists to keep sense-making ahead of building.

## Prime directives — never violate these

1. **Evidence is graded; grade D never passes a gate.** Every claim entering the workspace gets a grade (A/B/C/D) and a source. See `references/evidence-ledger.md`. An exit criterion answered only by AI reasoning is not answered.
2. **Never invent a user, a quote, an interview, or a number.** Simulated personas may be used to *rehearse* interviews; they are labelled `[SIMULATED]`, graded D, and can never satisfy a gate. If a figure cannot be sourced, write `no data found`.
3. **A prototype is a conversation prop, never evidence.** Its existence proves nothing about demand. Reactions from real humans holding it are the evidence.
4. **Disconfirming evidence gets equal airtime.** Every research step must produce both the case for and the case against, and the case against is written first.
5. **No production code in this stage.** The only build allowed is the single-interaction throwaway prototype at step 9. If the founder wants to start building sooner, say so plainly and point at the gate.
6. **Kill criteria are written before research starts,** not after (step 0). Falsifiability first, or the whole exercise becomes theater.

## Language

Converse in the user's language. Write deliverables in `report_language` from `VENTURE.md` (default: the language the founder is speaking). Persian deliverables keep standard English business terms as-is (TAM, SAM, SOM, ICP, CAC, LTV, PMF, churn, retention, pain point).

## Step 1 — Pick the mode

If the founder hasn't said, ask once with `AskUserQuestion`:

| Mode | What happens | Best for |
|---|---|---|
| **Coach** (همراه) | Claude asks one sharp question at a time; the founder does the thinking; Claude challenges, sharpens, and writes up. Slower, and the founder ends up actually understanding their market. | Founders with domain expertise; when the thinking itself is the point |
| **Auto** (خودکار) | Claude runs steps 2–6 and 8–10 end to end from desk research and writes the full dossier, flagging every assumption. Stops hard at step 7. | Fast first pass; a dossier to react to; time-poor founders |
| **Hybrid** (ترکیبی) — *recommended default* | Auto for the research-heavy steps (4, 5, 6). Coach for the judgment steps (2, 3, 8, 10). | Almost everyone |

State the honest limit out loud when auto or hybrid is chosen: **auto mode cannot produce problem–solution fit.** It produces a well-researched, well-attacked hypothesis and a discovery plan. Step 7 — real conversations with real humans — is the only source of grade-A evidence, and no model can run it for the founder. Read `references/auto-mode.md` before running auto or hybrid.

## Step 2 — Workspace

Look for `ventures/` in the working directory.

- **`ventures/<slug>/VENTURE.md` exists** (the `venture` plugin's workspace) → reuse it. Write into `ventures/<slug>/00-idea-stage/`, and update VENTURE.md's Status table, "Key facts & numbers", and "Open questions & riskiest assumptions" as usual.
- **Nothing exists** → create `ventures/<slug>/00-idea-stage/` plus a minimal `VENTURE.md` (name, one-liner, target market, business type, report language, created date). Confirm the kebab-case ASCII slug inline.

Files produced (create only as each step completes — never stub the whole set up front):

```
00-idea-stage/
├── STATE.md            progress, current step, open threads — read this first on resume
├── EVIDENCE.md         the ledger: every claim, source, grade   ← the spine of the stage
├── 00-brief.md         raw idea, founder's unfair advantage, constraints, kill criteria
├── 01-hypothesis.md    the testable problem hypothesis + assumption stack
├── 02-redteam.md       the strongest case that this is a bad idea
├── 03-competition.md   four-tier landscape + "why they win and you don't"
├── 04-market.md        TAM/SAM/SOM, market state, buyer map, complaint mining
├── 05-trends.md        3 external trends, each judged tailwind or headwind
├── 06-discovery-plan.md target profile, reach map, interview scripts per persona
├── 07-interviews/      one file per interview: raw notes + debrief
├── 08-synthesis.md     supports / challenges / surprises + bias audit
├── 09-solution.md      solution concept + its three load-bearing assumptions
├── 10-prototype.md     the single core interaction, and the 5-user test plan
└── DECISION.md         the exit gate scorecard + verdict + decision log
```

**On resume:** read `STATE.md` and `EVIDENCE.md` first, then continue from the recorded step. Never restart the pipeline from scratch.

## Step 3 — Run the pipeline

Ten steps, in order. Load `references/pipeline.md` for the full protocol — it carries the exact questions, rubrics, and output templates for each step. Do not improvise these from memory; the value is in the specifics.

| # | Step | Produces | Gate to advance |
|---|---|---|---|
| 0 | Brief & kill criteria | `00-brief.md` | Founder has written what would make them walk away |
| 1 | Forge the hypothesis | `01-hypothesis.md` | Passes the 4-question testability rubric |
| 2 | Red team | `02-redteam.md` | ≥1 finding that genuinely worries the founder |
| 3 | Competitive landscape | `03-competition.md` | All four tiers filled; the "why they win" case is credible |
| 4 | Market & complaint mining | `04-market.md` | Sizing assumptions listed and attacked, not just totalled |
| 5 | Trend read | `05-trends.md` | 3 trends, each labelled tailwind/headwind with reasoning |
| 6 | Design discovery | `06-discovery-plan.md` | Every question survives the leading/future/broad/social audit |
| 7 | **Run interviews** | `07-interviews/`, `08-synthesis.md` | ≥8–12 conversations; synthesis after every 5 |
| 8 | Solution concept | `09-solution.md` | Top-3 assumptions named with consequences if false |
| 9 | Prototype brief | `10-prototype.md` | Exactly one core interaction scoped |
| 10 | Exit gate | `DECISION.md` | Verdict recorded with evidence grades |

Between steps: append findings to `EVIDENCE.md` with grade and source, and update `STATE.md`. This is not optional bookkeeping — the ledger is what makes the gate at step 10 mean anything.

## Step 4 — Recurring discipline

Run these regardless of mode:

- **After every research step:** ask *"what did I just find that argues against this idea, and did I give it as much room as the supporting findings?"* Write the answer into the step's file.
- **After every 5 interviews:** produce two lists — evidence supporting the hypothesis, evidence challenging it. If the supporting list is materially longer, ask explicitly whether that asymmetry is in the data or in the founder's hopes. Record the answer.
- **Whenever the hypothesis changes:** steps 3–5 go stale. Mark them stale in `STATE.md` and re-run the affected ones. The book is explicit that market and competitive work is not a one-time exercise.
- **Whenever the founder pushes to start building:** name the gate they haven't passed, then let them decide. State the concern once; don't relitigate.

## Step 5 — The exit gate

Three questions, from the book. Each is answered `yes` only with a cited evidence grade attached:

1. **Is the problem real and specific?** Name exactly who has it, how often, how severely, and what they do about it today. Requires grade A evidence.
2. **Does the solution address the actual problem?** The one discovery revealed — not the one originally assumed. Requires grade A or B.
3. **Is there enough signal to justify building?** Certainty is never available and waiting for it is its own failure mode; the bar is that committing to an MVP is a reasoned decision rather than an act of faith.

Verdicts: **PROCEED** (all three yes) · **ITERATE** (reshape hypothesis, re-run steps 6–7) · **PIVOT** (segment or problem was wrong; back to step 1) · **KILL** (kill criteria from step 0 were met — say so plainly and without softening).

Write the verdict, the three answers with their grades, and the reasoning into `DECISION.md`, append to VENTURE.md's decision log, and state it directly to the founder. Then point at what comes next: `/founder-playbook:stage-map` for the MVP stage, or `/venture:customers` if the existing venture suite is in play.

## References

Load on demand — do not read all of these up front:

- `references/pipeline.md` — the full ten-step protocol with exact prompts, rubrics, and templates. **Load this before running any step.**
- `references/evidence-ledger.md` — the A/B/C/D grading system, ledger format, gate arithmetic, bias audit.
- `references/interview-kit.md` — target profiling, question design, the question audit, deflection probes, synthesis protocol.
- `references/research-kit.md` — four-tier competitive mapping, complaint mining, TAM/SAM/SOM with assumption attack, trend read.
- `references/auto-mode.md` — how auto mode runs each step, what it may and may not conclude, and the labelling rules.
- `references/templates.md` — every output file's template, in order.
