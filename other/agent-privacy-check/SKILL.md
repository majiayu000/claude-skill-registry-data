---
name: agent-privacy-check
description: Audit an AI agent's reachable data, external data paths, and untrusted instructions, then explain the result in plain language with Low, Medium, High, or Critical severity. Use when a user asks what an agent can see, where data may go, whether a skill, plugin, or tool is safe, or how to reduce agent privacy risk across Codex, Claude Code, or another agent.
---

# Agent Privacy Check

Give a non-specialist an evidence-backed answer about an agent's privacy
boundary. Separate what the agent can do from what it actually did, and make
the remaining unknowns visible.

## Scope gate

Start by naming:

- the agent and surface being checked, such as Codex Desktop, Codex CLI,
  Claude Code, or a generic agent;
- the exact scope, such as the current project, one Skill or plugin, one
  session, or a selected configuration directory;
- the trust boundary, including local files, connected services, the model
  provider, and external websites or APIs.

Use the narrowest scope that answers the question. The default is the current
project plus the agent configuration and tool metadata that are directly
available to the current run. Expand to a home directory, browser profile,
session archive, or external service only when the user names that scope.

Use these evidence labels throughout the audit:

| Label | Meaning |
| --- | --- |
| Observed | The current read-only check directly saw this capability or action. |
| Available | Configuration or permissions make it possible, but this run did not prove that it happened. |
| Not found | The named scope was inspected and no matching evidence was found. |
| Unknown | The scope or runtime boundary could not be inspected reliably. |

Treat a declaration in a Skill, README, prompt, or tool description as a lead,
not proof of runtime permission. Look for the permission, implementation,
configuration, or activity evidence that makes the claim concrete.

## Safe audit boundary

Keep the audit read-only. Use configuration, metadata, redacted filenames,
permission summaries, dry-run output, and synthetic examples as evidence.
Record secret types and locations without reading or repeating secret values.
Use the platform's existing help or inspection commands before any command whose
behavior is unfamiliar.

Require a separate, explicit authorization before changing permissions,
installing or removing a Skill, running unknown code, sending a network request,
uploading a test file, rotating credentials, deleting data, committing, or
publishing. Never test an external sink by sending a real secret. If a live
test is necessary, use only a user-approved test endpoint and synthetic data;
otherwise label the sink unverified.

For the safe artifact checklist, read
[references/evidence-collection.md](references/evidence-collection.md).

## Audit workflow

### 1. Map what the agent can reach

Inspect the smallest relevant set of tool definitions, permission prompts,
project instructions, Skill or plugin files, hooks, environment metadata,
memory stores, browser or connector access, shell boundaries, and sandbox or
container settings. Classify each capability by resource and operation:
read, write, delete, execute, upload, send, or administer.

Answer in plain language:

> It can see or use [resource] because [evidence]. It cannot be confirmed to
> have used it in this run.

Group findings into files and workspace data, credentials and identity data,
conversation or memory data, browser and connected-app data, and system or
repository controls. Avoid saying that an agent can see an entire category
when the evidence only covers one path.

### 2. Trace where data can leave

List every reachable external sink, not only obvious uploads. Include the model
provider request, web requests, shell tools such as curl, browser navigation or
uploads, email and chat, webhooks, Git pushes, third-party connectors,
telemetry, logs, and another agent or service. For each sink, record the
destination, sink class, recipient control, mechanism, data that could reach
it, evidence label, retention or review status when known, and whether the
action requires confirmation.

Classify the destination so a normal processing path is not confused with an
arbitrary exfiltration path:

- Trusted processing destination: an intended provider or service inside the
  declared trust boundary.
- Third-party processing or retention destination: outside the boundary, but
  named for the task and subject to a known handling policy.
- Agent-controlled external action: the agent can choose the recipient or
  payload, such as a webhook, browser upload, email, Git push, or curl request.
- Attacker-controlled or mutable destination: untrusted content can choose,
  change, or redirect where the data goes.

Distinguish:

- the agent has a path to send data;
- this run actually sent data;
- the destination, retention, or provider handling is unknown.

Use Available for a reachable capability. For actual transmission, use
Observed when an event is evidenced, Not found when the inspected event sources
contain no matching event, and Unknown when the event boundary could not be
checked.

An HTTP 200, a browser page opening, or a configured URL proves reachability
only. It does not prove that the payload was safe or that the provider will
delete it.

### 3. Find untrusted content and influence paths

Inventory content that may contain instructions controlled by somebody other
than the user or the trusted operator: web pages, documents, email, issues and
pull requests, repository files, downloaded packages, Skill text, plugin
metadata, memory, retrieved chunks, and other tool output.

Ask whether that content is clearly separated as data, or whether it can steer
the agent toward a privileged tool. A warning in prose is not a control unless
the runtime or workflow enforces the boundary.

### 4. Test the three-part combination

Use the following plain-language model:

- Secret Source: a path to credentials, private files, personal data,
  confidential work, browser state, or another sensitive value;
- External Sink: a path that can transmit data outside the trusted scope;
- Untrusted Content: data that an attacker, third party, mutable website, or
  unreviewed source can influence.

The dangerous combination exists only when the evidence connects all three in
one plausible workflow:

1. the agent can reach a Secret Source;
2. the agent can reach an External Sink;
3. Untrusted Content can influence the choice or parameters of the action.

For this test, an External Sink must be outside the intended trust boundary and
able to receive the sensitive data. A named provider that receives the intended
context is still a data-flow to document, but it is not automatically an
attacker-controlled exfiltration path. Escalate when untrusted content can make
the agent include the sensitive source, choose an unapproved recipient, or
redirect the request.

Report the combination as Confirmed, Likely, Not demonstrated, or Unknown.
Confirmed means the path is evidenced; it does not mean that exfiltration was
observed. Likely means the pieces are available but the influence path or
runtime boundary was not fully verified. Not demonstrated means at least one
piece is absent in the inspected scope. Unknown means a material boundary
could not be checked. Read the full decision table in
[references/risk-model.md](references/risk-model.md).

### 5. Rate the risk

Use the highest supported finding and include a confidence level. The levels
are operational labels for this Skill, not a formal OWASP score:

- Low means access is narrow and read-only, sensitive sources and external
  sinks are absent or separately controlled, and no material boundary remains
  unknown.
- Medium means there is one material gap, a meaningful unknown, sensitive data
  in context or logs, or an untrusted input with limited impact.
- High means broad access, shell or write authority, an external write path,
  missing isolation or approval, or a Likely dangerous combination creates a
  realistic high-impact path.
- Critical means an actual leak or compromise is evidenced, or the Confirmed
  three-part combination can carry sensitive data outside the intended
  boundary with an unapproved payload or recipient, or through an
  attacker-controlled or mutable external sink, under attacker-influenced
  instructions.

Unknown is not a safety finding. If the scope is too small to rule out a
material source or sink, keep the uncertainty visible and do not downgrade to
Low merely because no incident was observed.

### 6. Explain the worst case

Tie the worst case to the evidence instead of using a generic scare statement.
State who could control the untrusted content, which sensitive source could be
reached, which sink could receive it, and what could happen next. Examples
include credential theft and account takeover, private documents or personal
data leaving the intended boundary, repository or database changes, destructive
commands, impersonation through browser or chat access, and unexpected model
or tool costs.

Say explicitly when the audit found a reachable path but no evidence that the
agent used it.

### 7. Give an ordered repair plan

Put the first safe action at the top:

1. If an actual leak or compromise is evidenced, contain the agent and sink,
   preserve available evidence, and follow the credential owner's rotation or
   incident process. Do not call a suspected leak fixed after deleting one
   local file.
2. Remove unnecessary sources and tools. Narrow filesystem paths, use
   read-only access, separate identities, and block network egress that the
   task does not need.
3. Isolate execution with the platform's supported sandbox or container and
   require an explicit preview and approval for external, destructive,
   financial, or administrative actions.
4. Treat external content and memory as data to validate, delimit, expire, and
   audit. Pin Skill, plugin, dependency, and instruction sources where the
   platform supports it.
5. Add a small audit trail for tool, file, network, and approval events, then
   rerun this read-only check after changes.

Make each recommendation actionable for the named platform. Do not claim that
an unavailable control exists. If the user asks to apply a fix, keep the
privacy audit and the mutation as separate steps and report the post-change
evidence.

## Report contract

Use [references/report-template.md](references/report-template.md) for every
completed audit. The report must contain:

1. Overall risk: Low, Medium, High, or Critical, plus confidence.
2. A direct answer to what the agent can see.
3. A direct answer to where data can leave.
4. A Secret Source, External Sink, and Untrusted Content table.
5. The dangerous-combination result and evidence label.
6. The worst credible consequence for this scope.
7. An ordered remediation plan.
8. Evidence, unknowns, unverified actions, and the scope reviewed.

Every material conclusion, worst-case statement, and remediation reason must
point back to an evidence row or an explicit Unknown. Recommendations are
actions, not proof that an incident occurred.

Use the user's language and explain technical terms on first use. Keep secret
values, session contents, cookies, tokens, private keys, and unnecessary
personal paths out of the report. When the user asks how this aligns with
OWASP, read [references/sources.md](references/sources.md) and describe the
adaptation without presenting this Skill as a certification.

## Platform routing

Read [references/platform-notes.md](references/platform-notes.md) when the
platform is named or its configuration layout is uncertain. Keep shared
questions identical across Codex, Claude Code, and generic agents, then map
each answer to the platform-specific evidence that was actually available.

The audit is complete when the report names its scope, records each material
source and sink with an evidence label, evaluates the three-part combination,
assigns one risk level with confidence, and gives a platform-specific repair
order with evidence links and without exposing secret values.
