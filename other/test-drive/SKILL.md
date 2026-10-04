---
name: test-drive
description: Use when the user has a plausible but untested idea, belief, thesis, strategy, decision, prompt, skill, message, artifact, or AI output and asks how to validate it, test it, try it, de-risk it, gather evidence, run analysis, run a regression, dry-run it, evaluate it before shipping, identify needed connectors, or turn judgment into evidence-seeking action.
---

# Test Drive

Test Drive helps people test an idea, claim, or decision before they trust it.

The skill turns a plausible idea, claim, decision, belief, strategy, prompt, skill, message, artifact, or AI output into the smallest credible trial that can create useful evidence. It classifies the type of evidence needed, chooses a test route, drafts or builds the test artifact when safe, identifies connectors or capabilities required, and defines what would change the user's mind.

The goal is not to prove the user right. The goal is to create a low-risk learning loop before the user overcommits.

---

## When To Use

Use Test Drive when the user is asking, explicitly or implicitly:

- "How do I test this?"
- "How do I validate this idea?"
- "What evidence would tell me if this is true?"
- "How do I know if this message, prompt, skill, plan, or strategy works?"
- "Can we run an analysis or regression?"
- "What would be the smallest experiment?"
- "What connector, tool, or data would we need?"
- "Can you create the thing needed to test it?"

Also use it when the user has something plausible but not yet trustworthy: a product idea, career move, hiring read, strategy, positioning line, customer insight, research thesis, data claim, prompt, skill, prototype, memo, or recommendation.

## When Not To Use

- Use The Briefing Room when the context is still too messy to identify the belief or test.
- Use Ground Truth when the user mainly wants critique of reasoning, not an evidence plan.
- Use The Quorum when the user needs multi-lens deliberation on a consequential decision before choosing what to test.
- Use direct execution when the user has already specified the exact task and only needs it done.
- Ask clarifying questions first when the proposed test would require private data, external action, spending money, or irreversible commitments.

---

## Core Principles

**1. Test before trust.**
Treat plausible ideas as candidates for evidence, not conclusions.

**2. Route by evidence type, not domain.**
Do not start by asking whether the idea is "product," "career," "strategy," or "writing." Start by asking what kind of evidence would make it more or less trustworthy.

**3. Prefer the smallest credible test.**
Choose the lowest-friction action that can produce meaningful signal. Do not propose a giant research project when a small dry run, interview, data cut, or prototype would teach enough.

**4. Create the test artifact when safe.**
When useful, draft the prompt, email, survey, interview guide, data query, eval rubric, landing-page outline, GitHub issue, or skill-test scenario needed to run the test.

**5. Diagnose connectors and capabilities.**
Name the tools, connectors, data access, or permissions required. Include minimum scope and a manual fallback when possible.

**6. Respect approval gates.**
Do not send, post, publish, buy, book, scrape private data, query sensitive systems, or change external state without explicit approval.

**7. Define what would change the user's mind.**
A test is weak if success and failure signals are vague. Make the learning criteria explicit before execution.

**8. Dry-run before external action when risk is real.**
If the test is public, sensitive, expensive, hard to undo, or involves other people, prefer a dry run, review artifact, or simulated pass before taking external action.

---

## Evidence Types

Classify the primary evidence type before designing the test. Add secondary evidence types when needed.

| Evidence Type | Use When The Idea Depends On... | Common Test Routes |
| --- | --- | --- |
| Human Reaction | what people understand, want, remember, trust, choose, or reject | interviews, surveys, message tests, posts, prototypes, feedback requests |
| Behavioral / Data | what people actually do or what a dataset shows | cohort analysis, funnel analysis, segmentation, correlation check, regression, before/after readout |
| Reasoning | whether the logic, assumptions, or argument holds | Ground Truth, adversarial review, counterexample search, assumption audit |
| Expert Judgment | trade-offs with no single obvious metric | The Quorum, scenario analysis, pre-mortem, stakeholder lens review |
| Artifact Performance | whether the thing works in use | dry run, eval cases, rubric scoring, edge-case testing, sample output comparison |
| Operational Feasibility | whether the workflow, connector, process, or rollout can work | capability check, permission review, implementation spike, pilot workflow, manual fallback |

If multiple evidence types apply, choose the one that would most change the user's next action.

---

## Test Routes By Evidence Type

Use these route patterns to make the output concrete. Adapt them to the user's context, but do not skip the artifact, signal, and approval-gate pieces.

### Human Reaction

Use when the idea depends on what people understand, feel, want, remember, trust, choose, or reject.

Default route:

1. Name the audience segment.
2. Draft the message, survey, interview guide, prototype brief, or feedback request.
3. Define the response signal that would matter.
4. Define the failure signal.
5. Identify the channel or connector, plus manual fallback.

Good artifacts: email, Slack post, LinkedIn post, interview guide, survey, landing-page outline, prototype feedback script.

### Behavioral / Data

Use when the idea depends on observed behavior or a dataset.

Default route:

1. State the analysis question.
2. Define the unit of analysis.
3. Name the outcome variable, explanatory variables, and controls.
4. Pick the lightest credible method before regression.
5. Identify the data source or connector.
6. State caveats and what result would change confidence.

Good artifacts: analysis plan, spreadsheet instructions, SQL sketch, notebook outline, data request, regression readiness checklist.

### Reasoning

Use when the idea depends on logic, assumptions, argument quality, or counterexamples.

Default route:

1. Name the core claim.
2. Identify the assumption most worth attacking.
3. Route to Ground Truth or draft an adversarial review prompt.
4. Define what critique would require revision.

Good artifacts: Ground Truth prompt, assumption audit, counterexample prompt, red-team review brief.

### Expert Judgment

Use when the idea has consequential trade-offs without a single obvious metric.

Default route:

1. State the decision or trade-off.
2. Name the perspectives needed.
3. Route to The Quorum when stakes justify it.
4. Define what disagreement or pre-mortem finding would change the next step.

Good artifacts: Quorum decision brief, scenario matrix, stakeholder lens review, pre-mortem prompt.

### Artifact Performance

Use when the thing itself needs to be tried before reuse or publication.

Default route:

1. Name the artifact and intended job.
2. Create realistic eval cases or dry-run scenarios.
3. Define pass/fail criteria.
4. Run or propose the dry run.
5. Recommend revisions before external use.

Good artifacts: eval prompts, rubric, edge-case list, sample input set, before/after comparison.

### Operational Feasibility

Use when the question is whether a workflow, connector, data pull, integration, or process can actually work.

Default route:

1. Name the needed capability.
2. Explain why it matters to the test.
3. Specify minimum permission scope.
4. Identify available and missing connectors.
5. Provide a manual fallback or implementation request.
6. Ask for approval before configuration or external action.

Good artifacts: connector scope, implementation request, pilot checklist, manual fallback steps.

---

## Default Workflow

1. **Name the thing being tested.**
   State the belief, idea, decision, claim, artifact, or output in one sentence.

2. **Classify evidence type.**
   Identify primary and secondary evidence types, with a short reason.

3. **Pick the smallest credible test.**
   Choose a test that is low-risk, fast enough to run, and capable of changing confidence.

4. **Identify the artifact needed.**
   Name what must exist to run the test: prompt, message, survey, interview guide, data query, prototype brief, eval rubric, landing-page outline, GitHub issue, connector spec, or skill invocation.

5. **Capability check.**
   Name required connectors, tools, data, permissions, or skills. Separate available, missing, optional, and fallback paths when known.

6. **Draft or build the artifact.**
   If the artifact is text, a prompt, a test plan, a query outline, or a safe local file, create it. If the artifact needs external action or private data, stop at an approval gate.

7. **Define signals.**
   Specify support signal, weaken signal, and what would change the user's mind.

8. **Set the learning loop.**
   Say what to collect, how to interpret it, and what skill or action should happen next.

---

## Default Output Format

Use this structure unless the user asks for a shorter or more specialized output.

```markdown
# Test Drive

## What We Are Testing
The belief, idea, decision, claim, artifact, or output being tested.

## Evidence Type
- Primary:
- Secondary:
- Why this route fits:

## Smallest Credible Test
The lowest-friction trial that can produce useful evidence.

## Artifact Needed
What needs to be created to run the test.

## Capability Check
Required:
- ...

Useful:
- ...

Available:
- ...

Missing:
- ...

Fallback:
- ...

## Draft / Build
The prompt, message, survey, interview guide, query outline, eval rubric, prototype brief, or other artifact needed.

## Signals
Support signal:
Weaken signal:
What would change my mind:

## Approval Gate
What needs explicit user approval before external action.

## Learning Loop
What to collect, how to interpret it, and what to do next.
```

For small requests, compress this into: **Test Route**, **Artifact**, **Signals**, **Next Step**.

---

## Connector And Tool Guidance

When a connector or tool would improve the test, say so plainly. Do not silently assume access.

Use this language:

```markdown
## Connector / Capability Needed
Needed capability:

Why it matters:

Minimum scope:

Approval needed:

Manual fallback:
```

Common connector paths:

| Need | Possible Capability |
| --- | --- |
| Send validation emails | Gmail or email connector |
| Post or pulse a team | Slack connector |
| Analyze spreadsheet data | Google Sheets, CSV, spreadsheet tool |
| Query warehouse data | BigQuery, Snowflake, Postgres, or approved data connector |
| Create docs or surveys | Google Docs, Notion, Forms, or manual doc |
| Test a website or landing page | Browser, Playwright, analytics, or manual review |
| Create an issue or eval task | GitHub connector |
| Schedule interviews | Calendar connector |

Always include a manual fallback unless the test is impossible without the connector.

---

## Statistical And Analytical Tests

Use analytical tests when the claim depends on data rather than opinion.

Do not jump to regression by default. Pick the lightest credible analysis:

1. Descriptive comparison
2. Segmentation or cohort cut
3. Funnel or pre/post analysis
4. Correlation check
5. Regression or causal model when controls, sample size, and data quality justify it

For analytical tests, include:

- analysis question
- dataset needed
- unit of analysis
- outcome variable
- explanatory variables
- controls or confounders
- minimum viability concerns
- suggested method
- interpretation caveats
- connector or data access needed

If the environment has data access and the user approves, run the analysis. If not, draft the query, notebook plan, or data request.

---

## Multi-Agent And Skill Routing

Use other skills when they are the right test route:

- Use **The Briefing Room** if source context needs organizing before a test can be designed.
- Use **Ground Truth** if the best test is adversarial reasoning, assumption audit, or counterexample search.
- Use **The Quorum** if the test requires multiple expert lenses or consequential trade-off deliberation.
- Use a data, browser, document, spreadsheet, GitHub, Gmail, Slack, Notion, or calendar connector only when the evidence route requires it.

When recommending another skill, explain why:

```markdown
Recommended route: Ground Truth
Why: The main uncertainty is reasoning quality, not human reaction or data.
```

---

## Examples

**Positioning**

User: "I think 'judgment infrastructure' is the right frame. How do I test it?"

Good Test Drive: classify as Human Reaction + Artifact Performance, draft two post variants, define resonance signals, recommend manual LinkedIn posting or a social connector if available, and suggest feeding responses into The Briefing Room.

**Data claim**

User: "We think onboarding improves retention."

Good Test Drive: classify as Behavioral / Data, recommend cohort analysis before regression, list data needed, identify controls, name warehouse or Sheets connector, and define what effect size or caveat would change confidence.

**Skill before publishing**

User: "Test drive this skill before I ship it."

Good Test Drive: classify as Artifact Performance + Reasoning, create realistic eval scenarios, define pass/fail criteria, recommend Ground Truth for critique, and identify revisions before release.

---

## Common Mistakes

| Mistake | Fix |
| --- | --- |
| Recommending a big experiment | Shrink to the smallest credible test. |
| Treating critique as evidence | Use Ground Truth for critique, then Test Drive for action or signal design. |
| Picking a domain before evidence type | Classify by what would make the belief more trustworthy. |
| Running external action too soon | Draft the artifact and stop at the approval gate. |
| Saying "use data" without an analysis plan | Name the dataset, variables, method, and caveats. |
| Saying "needs Gmail/Slack/etc." without scope | Explain why, minimum permissions, and fallback. |
| Defining only success | Include weaken signals and what would change the user's mind. |
| Overfitting the test to prove the idea right | Design for learning, not confirmation. |

---

## Final Check

Before answering, check:

1. Is the belief or artifact being tested stated clearly?
2. Did you classify the evidence type?
3. Is the test small enough to run but strong enough to teach?
4. Did you name the artifact needed?
5. Did you identify required connectors, permissions, and fallback?
6. Did you stop before external action unless explicitly approved?
7. Are support, weaken, and mind-changing signals clear?
8. Does the next step preserve human agency?
