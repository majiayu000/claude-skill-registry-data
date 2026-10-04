---
name: plimsoll
description: Security review of LLM applications and agents. Use when asked to review, red-team, threat-model or test an LLM feature, chatbot, RAG pipeline, MCP server or autonomous agent for prompt injection (direct or indirect), jailbreaks, system prompt or secret leakage, tool abuse, excessive agency, confused-deputy behavior, authorization bypass, RAG poisoning, memory poisoning, or data exfiltration. Also use when asked to build a red-team test matrix, judge whether a suspicious model response is a real vulnerability, score a finding, or write a regression test for one.
license: MIT
---

# LLM and agent security review

Work through a system the way an attacker reaches it: find the text they control,
find the privileges the agent holds, and find out what stands between the two.

The one rule everything else follows from:

**Never rely on the model to protect a boundary that deterministic software can
enforce.** A recommendation that amounts to better prompt wording is not a fix.
It may reduce how often the model misbehaves; it does not change what a
misbehaving model can reach.

## When this applies

Reach for this skill for: agent and LLM security reviews, prompt-security
questions, RAG and memory trust analysis, tool and MCP permission audits,
red-team planning, triage of a suspicious transcript, and regression tests for a
fixed issue.

Not for: model evaluation quality, content moderation policy, or general
application security unconnected to a model.

## Before touching anything

1. **Confirm authorization.** Ask who owns the target and what is in scope. If
   the answer is not clear, do the architecture review from source and
   configuration only, and hold the adversarial tests.
2. **Prefer a sandbox.** Local, staging or a mock-tool harness. If the only
   instance is production, run the architecture review there and reproduce
   anything else elsewhere.
3. **Use synthetic secrets.** `plimsoll canary new`. Never a real credential,
   never real customer data.
4. **Keep the smallest proof.** Once a finding is demonstrated, stop. One mock
   email in a sink proves the path; sending ten does not prove it harder.

Stop and report instead of escalating when a test would touch a real third
party, cross into a tenant you were not given, destroy data, hold persistence,
or move real money.

## Workflow

### 1. Understand the target

Read, in this order: the system prompt and prompt assembly code, the tool or
function schemas, the retrieval pipeline, the memory layer, the authorization
code around tool execution, and the output renderer. The prompt tells you what
the developers hoped for; the tool schemas and the authorization code tell you
what actually holds.

### 2. Write it down as a target file

Describe the system in one YAML file so the analysis is reproducible and
reviewable. Schema and every field: `src/plimsoll/data/schemas/target.schema.json`.
Worked example: `examples/support-agent.yaml`.

```bash
plimsoll evaluate ./target.yaml -o reports/
```

That produces architecture findings, a capability-based tool-risk table, and a
test plan filtered to the channels this target actually has. It reads the file,
not the running system: everything it reports is a reachable path, not an
observed exploit.

### 3. Map trust boundaries

Label every input: trusted configuration, authorized user turn, untrusted
external content, privileged secret material, authorization state, or
action-capable interface. Then answer two questions for each high-risk tool:

- Can attacker-controlled data influence this action's arguments or approval?
- If the model is fully compromised, what stops the action from happening?

If the second answer is "the prompt tells it not to", you already have a
finding. Background: `references/threat-model.md`.

### 4. Choose attack classes

Pick from the intersection of what the target has and what an attacker can
reach. Do not run everything; run what applies. `references/attack-classes.md`
describes each class and what evidence proves it. The corpus in
`src/plimsoll/data/corpus/` holds ready cases, one file per class, plus benign
near-neighbors in `benign.yaml`.

Priority order in practice: untrusted input reaching a high-risk tool, then
secret and canary paths, then retrieval and memory, then model-only behavior.

### 5. Design the tests

Each test names: the channel the payload arrives on, what the secure outcome is,
what the failure looks like, and what evidence would prove it. Use the schema in
`src/plimsoll/data/schemas/test-case.schema.json`. Adapt corpus cases to the
target's vocabulary rather than pasting them verbatim; a payload that mentions a
tool the target does not have proves nothing.

### 6. Run and observe every channel

Watch the reply, the tool calls and their arguments, generated URLs and
filenames, logs, memory writes, and anything the client fetches automatically.
A secret that never appears in the chat can still leave in an image URL.

```bash
plimsoll scan ./retrieved-page.html --provenance web
plimsoll canary scan --channel tool_arguments=trace.json --canary PLIMSOLL_CANARY_...
```

`scan` is a heuristic and its verdict is a signal, not a verdict about the
target. What matters is what the agent did next.

### 7. Separate model behavior from control failure

These are different findings with different owners and different severities:

| Observation | What it means |
| --- | --- |
| The model agreed to a bad instruction | model behavior; policy deviation |
| The model proposed a tool call | model behavior; the gate may still hold |
| The tool ran with attacker-influenced arguments | control failure |
| The action happened outside the system | control failure with impact |
| Another tenant's data was reached | control failure, highest severity |

Never report a proposal as if it were an invocation.

### 8. Score it

Severity comes from `plimsoll.severity`: seven scored dimensions, and a cap set
by the strongest evidence class actually collected. Model text alone cannot
produce a critical finding, whatever the wording. See
`references/evidence.md` for the ladder and `examples/findings/` for a weak
report and a validated one describing the same scenario.

### 9. Recommend a deterministic fix

Order recommendations: architecture, then policy, then configuration, then
detection, and prompt wording last if at all. `references/mitigations.md` maps
each finding class to the control that actually holds it. Name the boundary, not
the phrasing.

### 10. Leave a regression behind

Every confirmed finding becomes a fixture under `tests/regression/` in test-case
format, referenced from the finding's `regression_test` field, and wired into
CI. A finding without a regression is not closed.

## Reporting

Emit findings in the schema at `src/plimsoll/data/schemas/finding.schema.json`,
which forces the twelve questions a reader will ask: component, channel,
boundary crossed, expected, observed, reproducibility, evidence class, secret
involvement, authorization outcome, privileges needed, impact, and the fix.
`plimsoll validate <path>` checks them.

Redact before writing anything out. Canaries and credential shapes are stripped
by `plimsoll.canaries.redact`, which the report writer already applies.

## What this skill will not do

Extract real credentials, act against systems outside the agreed scope, keep
escalating after the point is proven, install persistence, or turn a finding
into an operational exploitation procedure. If a request needs one of those, say
so and offer the sandboxed equivalent.

## Reference material

Load only what the task needs:

- `references/threat-model.md` — attacker profiles, trust boundaries, the paths worth caring about
- `references/attack-classes.md` — each class, its mechanism, and what proves it
- `references/evidence.md` — evidence ladder, severity model, weak versus validated findings
- `references/mitigations.md` — deterministic controls per finding class
- `references/owasp-mapping.md` — OWASP Top 10 for LLM Applications 2025 mapping
- `references/atlas-mapping.md` — MITRE ATLAS technique mapping
- `references/sources.md` — sources with dates and last-reviewed markers
