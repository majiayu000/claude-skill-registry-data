---
name: operating-mcp-on-serverless
kind: skill
status: ready
provenance:
  principles:
  - P030
  - P041
  - P042
  - P050
  - P061
  - P075
  - P099
  - P100
  - P101
  - P102
  - P132
  - P142
  - P152
  - P154
  - P156
  - P157
  - P158
  authored_from_digest: 233386035c6e941f386170bc38b50b31023da8f31705970a85376c2e2c807efc
---

# Skill: operating-mcp-on-serverless

## Purpose

Operate MCP workloads on serverless/FaaS cost-effectively and reliably: package servers for FaaS,
control cold-start and input-token cost, add caching and external memory, and choose between a CLI and
an MCP integration for a given capability [P154], [P142], [P152].

## When to use

- Moving an MCP agent workflow onto serverless/FaaS (e.g. Lambda) and controlling cost and reliability.
- Deciding memory/caching, external state, and artifact handling for a FaaS deployment.
- Choosing between exposing a capability as an MCP server or letting the agent use a CLI.

## Procedure

1. **Package MCP for FaaS.** Host agentic workflows on serverless FaaS for autoscaling and pay-per-request
   cost, but design explicitly for it; wrap each server as an HTTP-exposed FaaS function because
   stdio/local transports cannot be embedded directly [P154], [P142].
2. **Cut cold-start and input-token cost.** Consolidate an application's servers into a single FaaS function
   sized to the peak of its constituents; optimise input-token consumption first, since LLM token charges
   dominate total cost [P030], [P152].
3. **Add caching and external memory.** Cache deterministic tool outputs keyed by a hash of tool name plus
   parameters with a per-tool TTL; persist full agent memory in an external store — memory plus caching
   improves latency, tokens, cost, and completion reliability [P041], [P101], [P156].
4. **Keep large data out of context and off local disk.** Store large content and artifacts in object
   storage and pass URLs; inject only the relevant slice of memory rather than everything [P157], [P155].
5. **Decompose agentic roles as functions.** Put each role (Planner, Actor, Evaluator) in its own FaaS
   function orchestrated as a workflow, each with a strict-JSON prompt contract [P102], [P132].
6. **Choose CLI vs MCP deliberately.** Prefer the CLI when the agent already knows the tool from training
   (e.g. gh, kubectl) or a single piped command composes several steps; prefer MCP when the platform's API
   surface is larger than the agent's training knowledge [P158], [P159].

## Pitfalls / anti-patterns

- Holding large artifacts in the model context or on the function's local disk [P157].
- Running memoryless when persisted memory and caching would raise completion rates [P156].
- Profiling end-to-end as a black box instead of diagnosing the bottleneck class from the client type first [P099].

## Principles applied

- **[P030]** Consolidate an application's MCP servers into a single FaaS function (memory set to the peak of the constituents) to reduce cold-start overhead and stabilize latency, accepting a higher per-invocation cost; keep singleton per-server deployment when minimizing per-function memory footprint matters more.
- **[P041]** Cache deterministic MCP tool outputs, keyed by a hash of tool name plus parameters and stored in object storage with a per-tool TTL, so repeated identical calls in a session return a cached handle instead of re-executing the tool.
- **[P042]** Agent memory combined with MCP caching beats memoryless baselines across latency, tokens, and cost (up to 13x, 88%, and 66% respectively), and the empty-memory configuration fails follow-up queries that lack earlier context.
- **[P050]** Instrument the MCP workflow as a six-stage pipeline (S1 prompting, S2 planning, S3 tool call, S4 tool response, S5 context update, S6 answer synthesis) with a per-event structured log (identifiers, boundary timestamps and derived stage latency, model/tool/transport metadata, token accounting); when a client exposes no traces, reconstruct the stages from exported conversation logs.
- **[P061]** Recommend the design-once/execute-many pattern when a multi-step tool task recurs: per-execution cost falls to roughly O(1) (about 150 tokens), the one-time design cost breaks even after only ~4% of a single agent run, and amortized token savings exceed 99% past about five executions; treat the specific savings figures as conservative, estimated lower bounds rather than exact per-model measurements.
- **[P075]** Treat model selection as a lever that reshapes both the cost profile and its predictability: small local models are fast on simple tool use but degrade with high latency variance on heavy-context, open-ended tasks, so favor models with stable, low-variance scaling where predictable latency matters.
- **[P099]** Diagnose the bottleneck class from the client type before optimizing: customized environments suffer an input bottleneck determined by how fast the model parses tool definitions and plans, while off-the-shelf environments suffer an output bottleneck where unconstrained generation and streaming dominate user-perceived latency (final answer synthesis exceeds 75-86% of off-the-shelf-client latency).
- **[P100]** Enforce profiling hygiene for stable, comparable stage attribution: disable response streaming and tool-execution caching, bound the agent horizon (rounds) and retries, and run tools sequentially; remember that black-box clients with provider-managed streaming fragment token delivery and can add latency unrelated to protocol communication.
- **[P101]** Prefer persisting full agent memory (internal reasoning plus tool inputs and outputs) over naively replaying cumulative client request/response history, because client-only memory repeats already-completed work while agent memory lets the planner skip failed strategies and the actor skip redundant tool calls.
- **[P102]** Decompose the agentic pattern into one FaaS function per role (e.g. Planner, Actor, Evaluator) orchestrated as a FaaS workflow, so no single function risks the platform timeout and each role can be scaled and configured independently while sharing stateless instances.
- **[P132]** Give each agent a strict-JSON prompt contract - the planner returns the tools and their sequence, the actor executes them in order, and the evaluator returns success, needs_retry, reason, and feedback - so every agent's output can be parsed deterministically by downstream agents and branching logic.
- **[P142]** Wrap each MCP server as an HTTP-exposed FaaS function (e.g. a Lambda Function URL), because MCP's stdio/local transports cannot be embedded directly in a function; this mimics a remote MCP server, gains FaaS scaling, and isolates tool execution for security.
- **[P152]** Optimize input-token consumption before FaaS execution, because LLM token charges dominate total cost (roughly 61-94%) and input-token volume drives both latency and cost, while agent and MCP function execution are comparatively negligible.
- **[P154]** Host MCP-enabled agentic workflows on serverless FaaS rather than monolithic VMs to gain autoscaling and pay-per-request cost efficiency, but design every component around FaaS statelessness from the outset.
- **[P156]** Value persisted memory and caching for reliability, not only efficiency: they raised completion rates (eliminating the failures seen in memoryless runs) and mitigated the impact of LLM non-determinism and temperature on practical workflows.
- **[P157]** Keep large content and file artifacts out of the LLM context and off the function's local disk: store them in object storage (S3) and pass URLs, because oversized inline outputs overwhelm the context window and stateless FaaS does not persist local files across invocations.
- **[P158]** Prefer CLI over MCP when the agent already knows the tool from training data (e.g. gh, kubectl, terraform) or when a single piped command composes several operations in one call: the agent pays zero schema overhead, gets terse predictable output, and avoids per-step LLM round-trips.

Sources are distillation-only: this skill paraphrases and restructures; no verbatim source quotation.

