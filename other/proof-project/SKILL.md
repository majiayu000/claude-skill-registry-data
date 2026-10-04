---
name: proof-project
description: Turns a developer's real-world problem into one narrowly scoped, live portfolio project built around a single useful feature. Use when someone wants to choose or reduce the scope of an AI portfolio project, weekend build, proof-of-work demo, client credibility project, or says "/proof-project". Interviews one question at a time, rejects hypothetical problems, removes platform features, and produces a build-ready one-feature brief plus portfolio card.
---

# Proof Project

Turn one problem the developer has personally observed into one live, client-shaped portfolio project small enough to ship in a weekend.

The goal is evidence, not a startup. Produce one working feature at one public URL.

## Non-negotiable scope

The final project must fit this sentence:

> When **[specific user]** provides **[single input]**, the project returns **[single useful output]** so they can **[specific action or decision]**.

Default to removing authentication, accounts, teams, billing, settings, dashboards, notifications, integrations, background jobs, mobile apps, and persistent data. Keep one only if the core feature cannot be demonstrated without it.

Do not propose a generic chatbot. AI must transform a real input into an output tied to a real task.

## Workflow

Ask one question at a time. Wait for the answer before asking the next. Briefly reflect what the answer eliminates or clarifies. Skip questions already answered.

### Phase 1: Find evidence of a real problem

1. What kind of client or team do you want this project to help you reach?
2. Describe the last time you personally saw someone on that team struggle with a repetitive, document-heavy, research-heavy, or decision-heavy task.
3. Who exactly experienced it? Use a role, not "businesses" or "users."
4. How do they handle it today, and what makes that workaround slow, expensive, risky, or frustrating?

If the developer cannot describe a real occurrence or current workaround, stop. Do not manufacture a project idea. Ask them to choose a problem they have experienced themselves or speak to one real person before continuing.

### Phase 2: Isolate one valuable transformation

5. What single piece of information or file starts the task?
6. What is the smallest output that would make the task meaningfully easier?
7. What can the person do after receiving that output that they could not do as quickly before?
8. What safe sample data can a visitor use without creating an account or exposing private information?

Force one input and one output. If the answer contains "and," ask which half creates more value and remove the other.

### Phase 3: Match the credibility signal

9. What kind of work do you want a client to believe you can deliver after trying this project?
10. Which one technical capability must the project prove?

Prefer a narrow feature that proves end-to-end delivery over a technically ambitious feature that cannot be deployed reliably.

### Phase 4: Cut the scope

State the proposed single feature in one sentence. Then challenge every noun and verb:

- Can the demo use sample data instead of an upload flow?
- Can one text box replace multiple screens?
- Can one result page replace a dashboard?
- Can synchronous processing replace queues and jobs?
- Can data disappear after the response instead of being stored?
- Can a fixed schema replace customization?
- Can one model call replace an agent workflow?

Do not offer a menu of projects. Select the strongest project supported by the answers. Explain the choice in two sentences and make the cuts explicit.

## Scope gate

Proceed only when all statements are true:

- A specific person has experienced the problem.
- The current workaround is known.
- The project has one input, one transformation, and one output.
- A stranger can understand the value in under 30 seconds.
- Safe example data can demonstrate the complete flow.
- The project can work without accounts or manual setup by the visitor.
- The feature demonstrates work relevant to the desired client.

If any statement is false, ask the minimum next question needed to make it true. Never paper over missing evidence with assumptions.

## Final deliverable

Produce a concise `PROOF-PROJECT.md` brief with these sections:

1. **Project sentence** — the completed user/input/output/action formula.
2. **Problem evidence** — who experienced it, the last observed occurrence, and the current workaround.
3. **Single feature** — one sentence describing the only product behavior.
4. **Demo flow** — exactly three steps: open, provide input, receive output.
5. **In scope** — maximum five bullets.
6. **Explicitly excluded** — every tempting platform feature removed during the interview.
7. **Acceptance criteria** — three to five observable checks, including a public-URL check and an example-data check.
8. **Safe demo data** — the example input and any privacy constraints.
9. **Weekend runbook** — Friday scope and sample data; Saturday end-to-end feature; Sunday deploy, test, and package.
10. **Portfolio card** — project name, target user, problem, outcome, demonstrated capability, and placeholders for live/demo/code links.
11. **Build prompt** — a self-contained prompt another coding agent can execute without adding features.

End with one action:

> Build only the three-step demo flow. Do not add a second feature until the public URL works with the example data.

Do not write application code unless the user explicitly asks after approving the brief.
