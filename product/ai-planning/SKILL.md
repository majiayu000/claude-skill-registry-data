---
name: ai-planning
description: Plan a multi-phase AI feature before building it. Use when you have a PRD or project idea and need to figure out the execution order, which skills to use in what sequence, or how to break an ambitious AI project into phases. Also used for scoping an AI feature, creating a phased rollout plan, figuring out dependencies between AI components, help me figure out how to execute this, plan my AI feature, what order should I build this in, AI project roadmap, break this into phases, phased AI rollout, AI feature planning, multi-phase AI project, AI project dependencies, which skills do I need, AI execution plan
---

# Plan Your AI Feature

Use this skill when you have an AI project idea and need to figure out what to build, in what order, with which skills. ai-do routes to one skill per invocation. ai-kickoff scaffolds one project. Neither creates a multi-phase roadmap. This skill fills that gap.

---

## Should You Even Plan?

Not every task needs a plan. Route directly if any of these match:

| Situation | What to do instead |
|---|---|
| Single task (one classification, one extraction) | Go straight to that skill |
| Already building something | Use the skill for what you are building |
| Just exploring or learning DSPy | Use `/ai-kickoff` |
| Fixing a broken feature | Use `/ai-fixing-errors` |

If none of those match, continue below.

---

## Step 1: Answer 3 Questions

Before mapping skills or phases, answer these three questions. Write them down — they drive every decision in the plan.

**Question 1: What is the end goal?**
What does "done" look like for users? Be specific. "AI-powered search" is not a goal. "Users type a question and get an answer with a citation to the source article within 2 seconds" is a goal.

**Question 2: What do you have today?**
- Existing code (prototype, integration, nothing)?
- Data (labeled examples, raw documents, a database, nothing)?
- Models already in use?

**Question 3: What are the hard constraints?**
- Timeline (launch in 2 weeks vs. 6 months)
- Budget (API cost limits, inference budget)
- Model restrictions (must use on-prem, no OpenAI, etc.)
- Compliance (no PII to external APIs, audit logging required)

---

## Step 2: Map Capabilities to Skills

Find the capabilities your feature needs in the left column. The right column is the skill to use.

| Capability | Skill |
|---|---|
| Classify, sort, label, route | `/ai-sorting` |
| Extract structured data | `/ai-parsing-data` |
| Search documents, RAG | `/ai-searching-docs` |
| Answer database questions | `/ai-querying-databases` |
| Summarize content | `/ai-summarizing` |
| Generate text or content | `/ai-writing-content` |
| Take actions, call APIs | `/ai-taking-actions` |
| Multi-step reasoning | `/ai-reasoning` |
| Chain multiple AI steps | `/ai-building-pipelines` |
| Conversational AI | `/ai-building-chatbots` |
| Multiple agents | `/ai-coordinating-agents` |
| Score, grade, evaluate | `/ai-scoring` |
| Moderate content | `/ai-moderating-content` |
| Choose the right pattern | `/ai-choosing-architecture` |
| Review code quality | `/ai-auditing-code` |

Circle (or list) the 2-5 capabilities your project actually needs. If you circled more than 5, you are planning too much at once — pick the core path and defer the rest.

---

## Step 3: Decide Phase Ordering

Match your situation to one of these starting points:

**Greenfield — no code, no data**
- Phase 1: Set up data collection + scaffold with `/ai-kickoff`
- Phase 2: Build the core feature skill
- Phase 3: Measure and improve with `/ai-improving-accuracy`

**Have data, no code**
- Phase 1: Scaffold with `/ai-kickoff` + build core feature
- Phase 2: Evaluate quality with `/ai-improving-accuracy`
- Phase 3: Productionize with `/ai-serving-apis`

**Working prototype, needs improvement**
- Phase 1: Measure current quality with `/ai-improving-accuracy`
- Phase 2: Optimize (compile with an optimizer, tune prompts)
- Phase 3: Harden for production

**Production system, adding new capability**
- Phase 1: Build new capability using its skill in isolation
- Phase 2: Integrate into existing pipeline with `/ai-building-pipelines`
- Phase 3: Re-optimize the full pipeline

---

## Step 4: Generate the Plan

Fill in this template. Keep Phase 1 detailed, Phase 2 directional, Phase 3 a placeholder until Phase 2 is done.

```
## AI Feature Plan: [Feature Name]

### Phase 1: [Phase Name] (start here)
- **Goal:** What this phase achieves
- **Skill:** `/ai-xxx` -- one sentence on why this skill
- **Deliverable:** What exists when this phase is done

### Phase 2: [Phase Name]
- **Goal:** ...
- **Skill:** `/ai-xxx` -- why
- **Deliverable:** ...

### Phase 3: [Phase Name]
- **Goal:** ...
- **Skill:** `/ai-xxx` -- why
- **Deliverable:** ...

### Dependencies
- Phase 2 needs Phase 1 output because [specific reason]
- Phase 3 needs Phase 2 output because [specific reason]

### What to skip for now
- [capability] -- reason it is not Phase 1 material
- [capability] -- reason it is not Phase 1 material
```

---

## Common Project Archetypes

Five common project patterns with their natural phase sequence:

**Support ticket triage system**
Phase 1: `/ai-sorting` (classify + route tickets) -> Phase 2: `/ai-summarizing` (summarize for agents) -> Phase 3: `/ai-building-pipelines` (connect classify + summarize) -> Phase 4: `/ai-improving-accuracy` + `/ai-serving-apis`

**Knowledge base or help center**
Phase 1: `/ai-searching-docs` (index articles, answer questions with citations) -> Phase 2: `/ai-stopping-hallucinations` (add guardrails) -> Phase 3: `/ai-improving-accuracy` -> Phase 4: `/ai-serving-apis`

**Document processing pipeline**
Phase 1: `/ai-parsing-data` (extract fields from documents) -> Phase 2: `/ai-checking-outputs` (validate extracted fields) -> Phase 3: `/ai-building-pipelines` (batch processing) -> Phase 4: `/ai-improving-accuracy` + `/ai-serving-apis`

**Content generation platform**
Phase 1: `/ai-writing-content` (generate drafts at scale) -> Phase 2: `/ai-scoring` (grade quality before publishing) -> Phase 3: `/ai-improving-accuracy` (optimize for tone and brand) -> Phase 4: `/ai-serving-apis`

**AI agent**
Phase 1: `/ai-choosing-architecture` (pick the right pattern) + `/ai-taking-actions` (wire up tools) -> Phase 2: `/ai-building-pipelines` (multi-step coordination) -> Phase 3: `/ai-testing-safety` + `/ai-monitoring`

See [examples.md](examples.md) for fully worked plans for each of these archetypes.

---

## Gotchas

1. **Planning all phases in equal detail.** Only detail Phase 1 fully. Later phases will change once you see Phase 1 results. Detailed Phase 3 plans written before Phase 1 is done are fiction.

2. **Recommending optimization before a baseline exists.** Always build first, measure second, optimize third. Running a DSPy optimizer on a feature you have not yet evaluated is guesswork.

3. **Skipping the data question.** Most AI projects stall because there is no evaluation data. Surface this in Phase 1. If you do not know what good output looks like, you cannot tell when you are done.

4. **Including production skills too early.** Monitoring, tracing, and serving APIs are Phase 3 or later, not Phase 1. Do not let infrastructure planning crowd out feature planning.

5. **Listing every possible skill instead of selecting 3-5.** A plan that touches 12 skills is a catalog, not a plan. If your plan has more than 5 skills, cut the ones that are not on the critical path and put them in the "skip for now" section.

---

## Additional resources

- For the full phase model, skill catalog by phase, and phase gate checklists, see [reference.md](reference.md)
- For fully worked plans for each project archetype, see [examples.md](examples.md)

---

## Cross-References

> Install any skill: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill <name>`

- For a specific skill recommendation on a single task, use `/ai-do`
- To scaffold a project once you know what to build, use `/ai-kickoff`
- To pick the right DSPy pattern for your use case, use `/ai-choosing-architecture`
- To review existing AI code for problems, use `/ai-auditing-code`
- **Install `/ai-do` if you do not have it** — it routes any AI problem to the right skill and is the fastest way to work: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill ai-do`
