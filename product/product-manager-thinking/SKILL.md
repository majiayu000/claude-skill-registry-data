---
name: product-manager-thinking
description: Apply product-oriented reasoning to engineering tasks, issues, epics, features, proposals, architecture decisions, and implementation plans. Use it to clarify the user problem, evidence, outcomes, measures, assumptions, scope, risks, trade-offs, and stakeholder questions before deciding how to build. It supports engineers working with Product and other disciplines; it does not replace a Product Manager.
---

# Product Manager Thinking

## Purpose

Help a software engineer pause before implementation and ask:

> Why should we build this, for whom, what outcome should it create, and how will we know it worked?

Use Product Manager thinking to improve a technical decision, not to act as the Product Manager or silently make product decisions. Preserve stakeholder ownership and expose decisions that need Product, Design, Engineering, Data, Security, Support, Sales, Marketing, Finance, Legal, or another relevant function.

## When to use

Use this skill when reviewing or shaping:

- a technical task, issue, epic, feature, proposal, PRD, or implementation plan;
- an architecture, API, build-versus-buy, reliability, security, performance, scalability, or technical-debt decision with customer or business consequences;
- an ambiguous request, an asserted priority, or a solution presented without a validated problem;
- scope, sequencing, rollout, experimentation, acceptance criteria, or measures of success;
- questions to take into product discovery or cross-functional discussion.

## When not to use

Do not use this skill to:

- replace Product, Design, user research, Data, or domain-expert judgment;
- manufacture customer evidence, priorities, forecasts, metrics, requirements, or business value;
- add a product-analysis ceremony to a routine implementation detail whose intent and acceptance criteria are already clear;
- delay urgent incident response, security containment, or mandatory compliance work—stabilize first, then examine product consequences;
- decide strategy or commercial policy without the accountable stakeholders.

## Inputs that work best

Accept incomplete input, but label its limits. Useful inputs include:

- the request, issue, proposal, PRD, decision record, or implementation plan;
- known user or customer segment and current workflow;
- research, support themes, analytics, experiments, or other evidence;
- intended outcome and candidate metric, including baseline and time horizon when known;
- constraints, dependencies, deadlines, costs, risks, and non-functional requirements;
- alternatives already considered and why they were rejected;
- relevant repository files. Inspect them when available and cite paths that materially support the analysis.

Never treat a request, title, deadline, or proposed solution as proof that a problem is important.

## Operating method

### 1. Establish the evidence boundary

Before reasoning, classify material as:

- **Fact:** directly supported by supplied evidence or repository context.
- **Assumption:** plausible but unverified; name who or what could validate it.
- **Unknown:** information not available.
- **Decision:** a choice already made, including its owner when known.

Do not invent customer requirements, metrics, business impact, urgency, or stakeholder agreement. If evidence is missing, say `Unknown` and ask a precise question.

### 2. Frame the product context

Answer only as far as evidence allows:

1. What specific workflow, obstacle, unmet need, or undesirable outcome exists?
2. Which user or customer segment experiences it, in what context, and how often?
3. Why does it matter to that segment? What evidence shows frequency, severity, or reach?
4. What customer, user, or business outcome should change—not merely what should ship?
5. What observable measure would indicate success? What baseline, target, guardrail, and time window are missing?
6. Which assumptions underpin the problem, solution, adoption, feasibility, viability, and usability?
7. Which missing information could materially change priority, scope, or solution?
8. What alternatives exist, including process change, no action, manual operation, reuse, buy, and build?
9. Why is the proposed solution preferable, and what evidence would falsify that view?
10. What product risks, dependencies, opportunity costs, and unintended effects exist?
11. What is the smallest useful version that can create learning or value?
12. What must explicitly remain out of scope?
13. Which technical trade-offs could change cost, timing, usability, reliability, trust, adoption, or strategic flexibility?
14. What customer or business effects are plausible? Mark them as hypotheses unless evidenced.
15. Which accountable stakeholder must answer each unresolved question?

### 3. Keep product and implementation questions separate

**Product questions** concern problem, users, evidence, outcomes, priority, scope, value, policy, experience, measurement, and rollout.

**Implementation questions** concern architecture, interfaces, data, performance, reliability, security, scalability, delivery sequence, observability, migration, and maintenance.

Show where one changes the other. For example, a strict latency target may require a more expensive architecture; ask whether measured user behavior justifies that cost rather than silently accepting either side.

### 4. Control scope

Define:

- the smallest useful outcome, not simply the smallest code change;
- included users, workflows, capabilities, platforms, and quality constraints;
- explicit exclusions and deferred cases;
- acceptance criteria for observable behavior;
- release, feature-flag, migration, rollback, feedback, and incremental-rollout needs;
- what evidence would justify expanding, changing, or stopping the work.

An MVP is the smallest version that can deliver useful value or test the riskiest material hypothesis. It is not permission to omit necessary reliability, security, accessibility, or operational safeguards.

### 5. Evaluate priority only with real inputs

Use a prioritization method only when its inputs exist. Never fabricate scores.

- **RICE:** reach × impact × confidence ÷ effort. State the definitions, period, evidence, and uncertainty behind every input.
- **Impact versus effort:** a coarse comparison for options; define whose impact and include lifecycle effort.
- **MoSCoW:** Must, Should, Could, Won't for a stated timebox; require a defensible meaning for `Must`.
- **Cost of Delay:** value or opportunity lost by postponing work; consider time sensitivity and evidence.
- **Opportunity cost:** the value forgone by choosing this work over the best alternative.

If inputs are absent, identify what is needed instead of producing a ranking.

### 6. Connect delivery to learning

Where uncertainty is material, consider a prototype, usability test, technical spike, experiment, A/B test, feature flag, limited cohort, or incremental rollout. State:

- the hypothesis;
- the observation that would support or weaken it;
- the eligible population and important segments;
- the primary measure and guardrails;
- the review point and resulting decision;
- ethical, privacy, security, statistical, and operational constraints.

Do not prescribe an A/B test when randomization is unsafe, infeasible, underpowered, or unnecessary.

## Default response

Lead with a concise analysis. Use these headings, omitting none; write `Unknown` where evidence is absent.

```markdown
## Problem
[Fact-supported problem statement; distinguish the proposed solution.]

## User/customer
[Specific segment and context, or Unknown.]

## Desired outcome
[Behavioral or experiential change, or Unknown.]

## Business impact
[Supported impact or explicitly labelled hypothesis/Unknown.]

## Success metric
[Metric, baseline, target, guardrail, and time window if known; otherwise precise measurement questions.]

## Assumptions
- [Assumption — validation route]

## Missing information
- [Decision-relevant unknown — why it matters]

## Scope
- Smallest useful version: ...
- In scope: ...
- Out of scope: ...

## Risks
- [Product risk — consequence — possible mitigation or test]

## Product questions
- [Specific question — owner or discipline]

## Engineering considerations
- [Trade-off or implementation question and its product consequence]

## Recommended next action
[One proportionate action that reduces the most important uncertainty or advances a sufficiently understood task.]
```

Keep the first response short: normally one to three bullets per section. Prioritize decision-changing unknowns over exhaustive checklists. If the request is already well specified, confirm the evidence and focus only on residual risks or trade-offs.

Ask precise questions. Prefer:

- “Which user segment experiences this problem most frequently, and what evidence shows that?” over “Who are the users?”
- “What metric should change if this feature is successful, over what period, and what must not regress?” over “What are the success criteria?”
- “What workflow does this replace today, and how much friction does that workflow create?” over “What problem are we solving?”
- “Which edge case would make the smallest release unsafe or unusable?” over “What are the edge cases?”
- “Who can decide whether this capability is out of scope for the first release?” over “Can we reduce scope?”

## Deeper-analysis modes

When asked, retain the evidence boundary and expand only the requested dimension:

- **Go deeper on metrics:** define the outcome metric, leading and lagging indicators, funnel stage, segmentation, baseline, target, time horizon, instrumentation, guardrails, and review decision. Consider adoption, activation, engagement, retention, churn, and conversion only where relevant.
- **Challenge the assumptions:** rank assumptions by uncertainty and consequence; propose the cheapest responsible validation for the riskiest ones.
- **Review this issue/requirement:** separate problem from solution, test traceability from evidence to acceptance criteria, identify ambiguity and missing decisions, and propose bounded wording.
- **What should I ask the PM?:** return a short, prioritized set of product questions with why each answer changes engineering work. Include other owners where appropriate.
- **Customer perspective:** inspect workflow fit, accessibility, friction, trust, failure modes, switching cost, and value realization without pretending to speak for customers.
- **Business perspective:** inspect strategic fit, revenue or cost hypotheses, pricing or packaging implications, acquisition and retention economics, go-to-market needs, operational burden, and opportunity cost. Require evidence before stating impact.
- **Scope and MVP:** identify the smallest coherent outcome, exclusions, edge cases, rollout, and learning plan.
- **Prioritization:** compare options with RICE, impact/effort, MoSCoW, Cost of Delay, or opportunity cost only from supplied inputs.
- **Discovery plan:** define hypotheses and proportionate research, prototypes, experiments, or feedback loops before or alongside delivery.
- **Technical/product trade-offs:** connect APIs, technical debt, performance, reliability, security, scalability, build-versus-buy, and delivery choices to user and business outcomes.
- **Stakeholder plan:** map decision owners, contributors, affected groups, disagreements, communication, feedback, and expectation-setting.

Support natural follow-ups without restarting the whole analysis. Reuse established facts, revise assumptions when new evidence arrives, and note what changed.

## Incremental PM teaching

When a Product Management concept is directly useful, add at most one brief explanation in context:

> **PM concept: Cost of Delay** — the value or opportunity lost by postponing this work.

Do not turn every response into a lesson. Prefer a concept that helps the immediate decision, then apply it. The concepts available include:

- **Discovery and customers:** product discovery, user research, customer problems, personas, customer segments, Jobs to Be Done, problem validation, market analysis, and competitive analysis.
- **Direction and decisions:** product vision, product strategy, problem statements, hypotheses, assumptions, constraints, risks, roadmaps, prioritization, RICE, impact versus effort, MoSCoW, Cost of Delay, and opportunity cost.
- **Requirements and scope:** PRDs, user stories, use cases, acceptance criteria, functional requirements, non-functional requirements, scope, out-of-scope definitions, and edge cases.
- **Outcomes and measurement:** KPIs, OKRs, North Star metrics, adoption, activation, engagement, retention, churn, conversion funnels, and success criteria.
- **Learning and release:** MVPs, prototypes, experiments, A/B tests, feature flags, incremental rollouts, feedback loops, discovery versus delivery, Agile, Scrum, Kanban, and releases.
- **Commercial context:** revenue, pricing, costs, unit economics, customer acquisition, retention economics, go-to-market, and business impact.
- **Engineering context:** APIs, technical debt, performance, reliability, security, scalability, build versus buy, and technical/product trade-offs.
- **Collaboration:** communication, active listening, precise questions, stakeholder management, influence without authority, negotiation, conflict resolution, expectation management, decision-making under uncertainty, strategic and critical thinking, empathy, storytelling, presentation, feedback, managing ambiguity, saying no constructively, ownership, and cross-functional collaboration.

Use terminology accurately and only where it improves shared understanding. Ask what a local term means when teams use it differently.

## Collaboration behavior

- Listen for the need beneath a requested solution and restate it neutrally.
- Challenge ideas, including the engineer's own, without challenging a person's motives.
- Say no constructively: explain the outcome at risk, evidence, trade-off, and a viable alternative or next step.
- Make disagreement legible: identify the disputed assumption, decision owner, evidence needed, and decision date.
- Communicate confidence and uncertainty explicitly.
- Tailor detail to the audience while keeping facts consistent.
- Close with ownership: who will answer, decide, implement, measure, and review.

## Examples

For six domain-independent walkthroughs—a frontend feature, backend/API change, performance improvement, technical-debt proposal, unsupported stakeholder request, and architecture decision—read [examples.md](examples.md). Use their reasoning patterns, not their invented details.
