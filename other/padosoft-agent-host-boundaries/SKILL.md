---
name: padosoft-agent-host-boundaries
description: >-
  Use this skill when building or reviewing something that calls a model or hosts an agent — an LLM adapter,
  a tool-calling loop, an MCP server, a prompt-driven feature, a spend budget, a trajectory or replay store,
  a similarity or scoring threshold, an agent-generated artifact that a human is meant to approve. Also when
  the user reports a runaway bill, prompts or customer data ending up in logs or traces, an agent doing more
  than intended, a "confidence score" being treated as a decision, or generated output being accepted as
  evidence. Do not use it for prompt wording and model choice, for training or fine-tuning, or for building
  the skills themselves (padosoft-skill-creator covers that).
license: MIT
compatibility: >-
  Provider- and runtime-agnostic. The rules assume you control the host: the process that dispatches calls,
  persists their records and exposes tools.
metadata:
  version: 0.4.0
  author: Padosoft
  summary: The host decides what an agent may do, what gets recorded, and what any of it proves.
  profiles: ai, api
  scope: project
  repository: https://github.com/padosoft/skills
  keywords: llm, agent, mcp, tool calling, budget, trajectory, replay, redaction, threshold, approval
---

# Agent and LLM host boundaries

The model is a provider. The agent is a caller with unusual reach. Everything below is a boundary the
**host** owns — and every one of them has a failure mode where the system looks like it is working.

**The rule: the host decides what is allowed, what is recorded, and what any of it is allowed to prove.**

---

## 1. An adapter is not production-grade because it parses a 200

The minimum contract for a call that leaves the process:

| Control | Why |
|---|---|
| Abortable timeout | otherwise one hung call holds a worker until something else times out |
| Maximum generation bound | an unbounded response is an unbounded bill and an unbounded payload |
| Injectable transport | deterministic tests without a network, and without pretending the network was tested |
| Redacted prompt, response **and error** | the error path is the one that leaks, because nobody redacts it |
| Model provenance hash | so a recorded result can be attributed to a specific model identity |

**One wire protocol does not cover every vendor.** Roles, content blocks, tool schema names and usage fields
differ; registering two providers behind one "compatible" adapter makes the tests green while sending
semantically wrong requests. Each provider gets its own bounded adapter, and an unsupported one stays
explicitly unsupported rather than silently falling back.

## 2. Budgets are enforced twice, and their exhaustion is an event

```text
before dispatch → estimate, and refuse a known overage
after response  → charge the provider-reported usage, and stop further calls at the limit
```

Charging only afterwards permits the over-budget call; checking only an estimate loses the authoritative
number. And **exhaustion on a successful call is also a budget event**: if the adapter raises without
emitting it, the run loses the only durable record of why it stopped.

Emit budget decisions to a bounded, **prompt-free** sink that the host appends to its own record. A failure
in that observer must never turn a governed call into an application retry, and must never carry prompt or
provider secrets. Estimation rates and prices are **versioned deployment inputs**, not constants in the code
— see **`padosoft-payments-reconciliation`** for settling them.


**Meter once, at the shared boundary.** One hook on the lifecycle every provider goes through sees all of
them; a counter added per adapter misses the next adapter. Propagate a correlation identifier from the
orchestrator so cost attaches to a step and not only to a day.

**Pricing tables go stale, and a stale price is a wrong bill.** Mirror an authoritative external source as
the base and let a local entry override it, so a correction does not wait for an upstream release — and
carry the catalogue's identity into the settlement record, as in **`padosoft-payments-reconciliation`**.

## 3. Trajectories are a sensitive data sink by default

An agent trajectory contains credentials, customer data and large tool responses. Treat the recording as
**opaque**:

- Audit the **existence, identity, ordering, status and digests** of tool calls — not their raw payloads.
- Enforce allowlists and budgets **before dispatch**. Redaction after persistence is too late: the data was
  already in the host's memory and in whatever observed it.
- Bind every call to one explicit provider and model identity, with contiguous step and token accounting, or
  the record is neither reproducible nor safe.
- Give the store an immutable identity key `(run, step)`, insert atomically, and compare the stored digest
  on conflict — a cross-replica retry cannot rely on a filesystem check.
- **Hashing at write time proves nothing about a later snapshot.** A separate consumer verifies sequence,
  totals, identity and event correspondence; otherwise replay accepts a self-consistent trajectory that was
  never recorded.

## 4. A tool surface is an authority grant

Mapping an entire API into agent tools hands the agent more authority than it needs and makes a cross-tenant
mistake trivial.

- **Few tools, explicitly chosen.** Scope derived from the authenticated principal, never from an argument.
- **Idempotency required on anything that starts work**, and evidence metadata returned rather than raw
  payloads.
- **Authenticate every request at the transport edge**, bind the session to the principal that created it,
  cap body and session resources, and give sessions explicit expiry and termination. An authenticated method
  inside an unauthenticated transport is not a boundary.
- **Execution mode is explicit at the host boundary.** Accepting an "agent profile" without a host-owned
  driver mislabels events and findings: require injection, and propagate the acting identity through every
  recorded event.
- **Sandboxing is selected by the runner, not owned by a package.** A tested container adapter protects
  nothing until the final boundary chooses it, and a development default must not silently change the
  security semantics.
- **Bound the output, not just the time and the call count.** One successful, non-blocking command that
  prints forever exhausts memory; cap combined output in the real child process and fail explicitly.

### The shape of a tool

Assume **every tool is invoked with no human in the loop**, because that is the point of the system.

- **A tool is a thin wrapper.** It delegates to the service the rest of the application already uses;
  business logic written inside the tool is a second implementation that will drift from the first, and it
  is the copy nobody tests.
- **Its input has a schema, and the schema is derived from the validation rules**, not written twice. Input
  arriving from a model is untrusted and frequently malformed in creative ways.
- **Its output is an allow-listed shape**, not free-form data. A component type outside the known set
  cannot be rendered, and raw data leaves the consumer to guess.
- **Parameter descriptions are written for the model**, and they are part of the contract: without them the
  model guesses the semantics of an argument, which is a correctness problem long before it is a security
  one.
- **Discovery is an explicit manifest.** Scanning the filesystem for tools is a surprise at deploy time and
  a cost at boot; a list somebody has to edit is a list somebody has read.
- **A mutating tool logs who, what and when, checks the same policy a human would go through, and offers a
  dry run.** Those three are not optional once the caller is autonomous.

## 5. Generated output is a hypothesis

An artifact produced by a model is not evidence because it validates against a schema.

- **Bind approval to the exact artifact.** The canonical digest and revision, an independent human approver,
  expiry enforced at use time, and the payload kept out of the approval metadata.
- **An agent saying "approved" is not an authorisation event.** Bind it to the exact call, subject, revision
  and total, consume it once, and re-check atomically at the mutation — it is a time-of-check/time-of-use
  contract.
- **Automating the verdict is fine. Automating the proof is how a system certifies itself.**
- **Generated instructions must be self-contained.** If the output tells a reader to load a bootstrap file,
  the generator produces that file too, and each target is tested in isolation.

## 6. Scores are not decisions

- **A similarity score is not a merge policy.** Keep a human-reviewed pair corpus, report the confusion
  matrix, and gate on precision, recall and false-positive rate explicitly.
- **Calibrating and measuring on the same pairs is optimistic.** Use a deterministic split with a recorded
  digest and gate on the **held-out** half — and still label the result as your own corpus, not independent
  validation.
- **Confidence needs an inconclusive state.** A scale that must resolve to yes or no resolves wrongly at the
  boundary; make "not enough signal" a first-class outcome that fails closed.
- **Heuristics declare themselves.** Source scanning, import-graph reachability and framework detection are
  useful and incomplete — emit the resolver mode as a tag and never claim completeness.

---

## Gotchas

- **The error path is where the prompt leaks.** Responses get redacted because somebody remembered them;
  exceptions carry the request body straight into a log. See **`padosoft-logging-discipline`**.
- **A model identity is part of the result.** The same prompt on a silently upgraded model is a different
  experiment, and without a pinned identity the record cannot say which one ran.
- **"It cost almost nothing in testing" is a statement about your test inputs.** The budget must hold on the
  input you did not imagine.
- **An aggregate score hides the part with no coverage.** Report what was not evaluated next to what was.
- **A tool that returns raw payloads makes every consumer a data processor**, including the ones you have
  not written yet.

## Checklist

- [ ] Timeout, generation bound, injectable transport, redacted prompt/response/**error**, model identity
- [ ] One adapter per provider; unsupported stays unsupported
- [ ] Budget enforced before dispatch **and** after the response; exhaustion emitted as an event
- [ ] Budget observer bounded, prompt-free, and unable to cause a retry
- [ ] Trajectories store digests and metadata, not payloads; allowlists applied before dispatch
- [ ] Immutable identity key, atomic insert, digest compared on conflict
- [ ] An independent verifier checks a recorded run, separate from the writer
- [ ] Tool surface narrow; scope from the authenticated principal; idempotency on starts
- [ ] Transport authenticated, session bound to its principal, resources capped, expiry explicit
- [ ] Sandbox selected at the runner boundary; output bytes capped in the real process
- [ ] Generated artifacts bound to an approval with digest, approver and expiry
- [ ] Thresholds calibrated on a held-out split; an inconclusive state exists and fails closed

## Final report

```
Host: <what dispatches and records>
Adapter: timeout <…> · max output <…> · redaction <prompt/response/error> · model identity <…>
Budget: pre-dispatch <…> · post-response <…> · exhaustion event: yes | no
Trajectory: stores <digests|payloads> · identity key <…> · independent verifier: yes | no
Tools exposed: <n> — scope from <…> · idempotent starts: yes | no
Generated artifacts: <approval binding, expiry>
Thresholds: <metric> gated on holdout: yes | no · inconclusive state: yes | no
Open: <…>
```
