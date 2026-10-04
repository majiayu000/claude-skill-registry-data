---
name: onboard
description: Connect a customer agent to Coval and complete a small first evaluation with inspected voice or chat results. Use when no usable evaluation exists yet; reuse existing recordings and resources when available.
compatibility: Requires the Coval CLI or an authenticated Coval connector; public API access can fill CLI gaps.
---

# First Coval evaluation

Get from the customer's agent to one trustworthy piece of evaluation evidence.
A working connection is the first milestone; a credible task-quality check is
separate. Don't turn setup into a survey or create every possible resource.

## 1. Establish context and access

Reuse the customer's stated use case, endpoint and requirements. Ask only for
missing information: what the agent must do, one important failure to catch,
and which organization/workspace/environment to use. If completed recordings
already exist, prefer `coval-discover-failures` unless the user wants a new run.

```bash
coval --version
coval --agent agent doctor
coval --agent agent manifest
```

If installation/authentication is missing, use the current
[CLI installation guide](https://docs.coval.ai/cli/installation). Have the user
enter credentials through login or their secret environment, not in chat.
Doctor proves connectivity, not tenant identity. Check the intended account
context and selected resources before writes. Use the existing workspace; if
the CLI cannot select it, use the public API's documented workspace header.

Inspect existing agents, personas, test sets and metrics within that scope.
Check JSON envelopes (`ok`, `data`), failures and pagination. Reuse matching
resources; names alone are not a safe match for a write.

## 2. Connect one agent

Read `coval agents create --help` and `coval --agent agents context`; fetch the
current agents spec at `https://api.coval.dev/v1/openapi/agents` for fields not
exposed by the CLI. Choose the actual transport: phone, hosted voice-to-voice,
voice WebSocket, LiveKit/Pipecat, chat, chat WebSocket, A2A, or SMS. Do not infer
that every WebSocket connection is text-only. Use the matching connection guide
from [Coval's documentation index](https://docs.coval.ai/llms.txt).

Reuse a configured agent if appropriate. For a new connection, prepare the
schema-valid body locally, show a redacted summary and create only within the
requested scope. Do not copy credentials into a skill, report or Git. Read the
created agent back and verify its transport and endpoint without printing secrets.
A reachable URL or saved agent record is not a successful voice connection.

## 3. Design the smallest useful test

Use `build-test-suite` to draft a few cases grounded in the customer's workflow.
Start the live connection check with **one short case**, one normal persona,
one iteration and concurrency one. Then, within an agreed budget, add a normal
success path and an important boundary/failure case. This is a starting point,
not a universal three-category taxonomy.

The persona describes **who the caller is and how they behave**. The test case
describes **what they are trying to do**. Expected behaviors describe **what the
agent must do**. Don't put the expected answer in the caller's mouth. End the
scenario after its objective is answered; avoid open-ended conversations.

For voice, choose a compatible current voice/language from the public personas
catalog; don't hardcode a provider's voice name from an old template. Use an
existing appropriate persona or prepare `coval personas create --input-json
@persona.json` after checking its schema. Add noise, accents or interruptions
only when they test a relevant hypothesis, after the basic connection works.

## 4. Choose an observable criterion

Use `configure-metrics` for one task-specific criterion and, if useful, a small
number of operational measurements. Discover metric IDs dynamically. Do not
attach a blanket set of sentiment, tone and resolution scores or change the
agent's defaults just to evaluate one run.

A transcript can establish what was said. It cannot establish that a booking,
payment or transfer actually happened. Use tool traces or external evidence for
such claims. A new judge is provisional until checked against human labels.

## 5. Execute and inspect

Follow `quick-eval` with the selected case IDs and an explicit session budget.
Show what will run before execution; honor the customer's existing authorization.
Include the number of calls, metric evaluations, configured call-duration limit,
and a wall-clock stopping condition. Do not translate counts into dollars unless
current rates are known. Reruns count against the same budget.

Audit each first-run transcript, statuses, metrics and recording. Did the caller
exercise the intended scenario? Are both sides present? Did the metric score the
right speaker and criterion? Check explanations against evidence. A completed
run or a perfect score on one example is not statistical confidence.

If the connection fails, diagnose that call before expanding the suite. If an
output is unavailable, report the missing evidence and its effect on the result.
Do not silently substitute chat for voice, switch environments or keep retrying.

## 6. Leave a reusable starting point

Return the created/reused resource IDs, run/result links verified against the
org/workspace, actual simulation and metric counts, the observed result and its
limits. Recommend the single most useful next step: inspect a failure, broaden
coverage, or collect human labels. Save a template only when requested or needed
for an already agreed recurring workflow; creating a schedule is a separate action.

Preserve the resources for inspection. Don't delete them, modify production
agent defaults, send invitations, or schedule follow-ups as incidental cleanup.
