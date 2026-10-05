---
name: confirm-with-pseudocode
description: >-
  Run a two-confirmation protocol for substantive requests: first present a
  semantically detailed, Cal Poly PDL-style pseudocode interpretation of what
  the user wants; after confirmation present a minimal, non-anchoring
  pseudocode response plan; execute only after the plan is confirmed. Use when
  the user invokes $confirm-with-pseudocode or asks to confirm prompt meaning
  and response approach separately before work begins, including correction
  loops and follow-up turns. Bypass the protocol for discussion, inspection,
  debugging, configuration, or modification of the skill itself unless the
  user explicitly asks to apply it.
---

# Confirm with Pseudocode

Apply one protocol instance to each substantive request. Keep prompt
interpretation, response planning, and execution as separate states.

Before composing or revising either pseudocode artifact, ensure
[references/pdl-conventions.md](references/pdl-conventions.md) has been read
completely in the current context. Use that local reference for notation and
style; do not fetch the source at runtime. Let the artifact-specific detail
rules below govern granularity.

## Preserve these invariants

- Do not plan before the Prompt Pseudocode is confirmed.
- Do not execute before the Response Plan Pseudocode is confirmed.
- Maximize useful semantic specificity in Prompt Pseudocode.
- Minimize procedural specificity in Response Plan Pseudocode while keeping the
  approach meaningfully inspectable.
- Treat any message containing both confirmation and a correction as a
  correction.
- Regenerate the complete current artifact after every correction; never emit
  only a patch, diff, or amendment.
- Return a semantic change during planning to prompt confirmation.
- Let the confirmed artifacts, not conflicting wording in the original prompt,
  govern execution.

## Track the protocol state

Infer the current state from the visible conversation at the start of every
turn. Do not rely on hidden state and do not infer confirmation from silence.

Apply higher-priority safety, privacy, and platform rules before selecting a
protocol state. If they require an immediate refusal or safe redirection,
respond directly without either pseudocode artifact or a protocol-confirmation
request.

1. Start at prompt interpretation for a new substantive request.
2. Remain there until the current Prompt Pseudocode is clearly confirmed.
3. Move to response planning and remain there until the current Response Plan
   Pseudocode is clearly confirmed.
4. Execute, return the final response directly, and close the instance.

Recognize clear conversational confirmations such as `confirm`, `confirmed`,
`correct`, `yes`, `that's right`, and `proceed`. Do not require a magic token.

## State 1: confirm prompt interpretation

Generate **Prompt Pseudocode** representing what the user is requesting, not
how to answer it. Preserve every material detail of the substantive request
that is present, including:

- actions, subjects, objects, and relationships among instructions;
- scope, constraints, exclusions, priorities, conditions, and ordering;
- quantities, dates, comparisons, and decision criteria;
- audience, definitions, and requested output characteristics.

Express the interpretation actually formed. Do not solve the task, research
the subject, plan the response, invent missing requirements, silently improve
the request, or create an ambiguity-management schema. The visible artifact is
the clarification mechanism; enumerate ambiguities only if the user requested
that as part of the task.

Base task semantics on the user's request and confirmed corrections. Treat this
skill and its references as protocol and formatting guidance; do not import
their procedures, criteria, or constraints as user requirements.

Separate task semantics from control of the current protocol instance. Include
an instruction in Prompt Pseudocode when it would still constrain the
substantive work or requested result after the confirmation protocol is
complete. Treat an instruction whose only effect is to alter, skip, collapse,
pre-confirm, or otherwise control the current protocol instance as protocol
control rather than task semantics. Classify by function, not by wording: the
same words remain task semantics when the user asks to analyze, quote,
transform, discuss, reproduce, or otherwise use them as substantive task
content.

Show only minimal framing and the complete artifact:

````markdown
**Prompt Pseudocode**

```text
<complete interpretation>
```

Confirm or correct this interpretation.
````

Then stop. Do not include a response plan or substantive answer.

If the user corrects, adds, removes, or rejects anything, incorporate all
feedback into a complete revised Prompt Pseudocode and wait again. Once clearly
confirmed, freeze that artifact as the authoritative semantic specification.

## State 2: confirm the response plan

Only after prompt confirmation, derive **Response Plan Pseudocode** from the
confirmed interpretation. Before minimizing the plan, ensure semantic
coverage. Every material action or deliverable required by the confirmed
Prompt Pseudocode must be represented by a high-level plan operation or be
unambiguously covered by a broader operation. Do not add operations merely
because they would normally be useful; plan completeness is relative to the
confirmed Prompt Pseudocode.

Then expose the minimum high-level procedure needed for the user to reject a
materially undesirable approach. Include only relevant choices such as whether
to:

- gather or evaluate information;
- compare alternatives or apply confirmed criteria;
- calculate, assess tradeoffs, or form a conclusion;
- follow a material order or required broad output structure.

Keep the plan abstract and non-committal. Do not answer the request, anticipate
findings, choose winners, invent hypotheses, lock in arguments, or over-specify
sources, evidence, examples, calculations, sections, or reasoning steps unless
the confirmed Prompt Pseudocode requires those specifics. Avoid both anchoring
and empty steps such as merely `THINK` or `WRITE`. Do not research or use
substantive task tools while drafting the plan.

A suitably inspectable plan often resembles:

```text
GATHER information needed to evaluate the requested alternatives

COMPARE the alternatives
    USING the confirmed criteria

ASSESS relevant tradeoffs

FORM the requested conclusion

PRESENT the result
    WITH important qualifications
```

Show only minimal framing and the complete plan:

````markdown
**Response Plan Pseudocode**

```text
<complete high-level procedure>
```

Confirm or correct this response approach.
````

Then stop without executing.

For an approach-only correction, keep the confirmed Prompt Pseudocode fixed,
regenerate the complete Response Plan Pseudocode, and wait again. Treat changes
to research or evaluation method, evidence-selection procedure, qualitative
versus numerical comparison, scoring or ranking technique, analysis order, or
how the same conclusion will be derived and justified as approach-only when the
subject, audience, deliverable, and requested conclusion remain unchanged.

If feedback changes the goal, subject, scope, alternatives, factual or content
requirements, exclusions from the result, audience, definitions, or final
output form or limits, discard the plan and return to State 1 with a complete
revised Prompt Pseudocode. In short, constraints on the requested result are
semantic; constraints only on how to produce it are plan-level.

## State 3: execute

After clear plan confirmation, use the confirmed Prompt Pseudocode as the
authoritative **what** and the confirmed Response Plan Pseudocode as the
authoritative high-level **how**. Perform the task normally and return the final
response without another pseudocode or protocol-confirmation stage. Do not
substitute a materially different response strategy during execution.

Keep low-level reasoning and implementation choices flexible where the plan is
silent. Do not expose private reasoning: the two confirmed artifacts are
user-facing specifications, not chain-of-thought.

Ask an execution-time question only when a higher-priority rule or genuinely
blocking missing fact requires user input. Treat it as an execution dependency,
not a third protocol-confirmation stage.

## Handle follow-ups and boundaries

- Continue an existing execution without restarting only when the user supplies
  requested execution input, authorizes an already-described in-scope action,
  or asks to continue incomplete work without changing the specification.
- Start a fresh instance at State 1 after completion for any new or materially
  changed substantive request. Do not carry confirmation across instances.
- Respond normally to meta-level requests to discuss, inspect, debug, configure,
  or modify this skill. Apply the protocol to a meta-request only when the user
  explicitly asks to do so.
- Never treat protocol confirmation as authority for disallowed or unrelated
  action, and continue to obey required platform approvals during execution.
