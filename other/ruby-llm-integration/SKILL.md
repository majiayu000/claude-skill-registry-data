---
name: ruby-llm-integration
description: Use when a Ruby/Rails application calls large language models — provider adapters (RubyLLM, Ollama, hosted APIs), timeouts and retries, token/cost budgets, structured-output validation, prompt-injection boundaries, tool-call authorization, observability, graceful degradation, and keeping LLM output out of deterministic safety paths.
license: MIT
---

# Ruby LLM Integration

## Purpose

Treat an LLM in an application as an external, untrusted, occasionally-unavailable dependency whose output is a *suggestion* — never as an authority the system obeys.

A dependable LLM integration isolates the provider behind an adapter, bounds every call in time and money, validates every structured output against a schema, keeps untrusted content out of privileged instructions, authorizes tool calls at a real boundary, degrades gracefully when the provider cannot serve, and — above all — never lets model output bypass deterministic guards or authorize consequential actions.

Core flow:

```
isolate the provider behind one adapter
-> bound the call: timeout, retries, token and cost budgets
-> validate structured output against a schema
-> treat model output and user content as untrusted data
-> authorize tool calls at an explicit boundary
-> observe: latency, tokens, cost, failures, refusals
-> degrade gracefully; never block the deterministic path on the model
```

Compose this skill with:

- ruby-dependency-injection for adapter boundaries and testability;
- rails-api-integration for HTTP contracts, retries, and rate limits;
- rails-security for trust boundaries and secret handling;
- rails-observability for telemetry and cost tracking;
- trading-execution-safety when model output could touch execution paths;
- rails-active-job for asynchronous and queued LLM work;
- ruby-tdd-refactoring for adapter contract tests.

This skill owns application-side LLM integration. It does not own prompt-engineering content strategy, model evaluation/benchmarking of the pack itself, or AI code review (separate skills exist for those).

## Activate when

- calling an LLM provider (OpenAI-compatible API, Anthropic, Gemini, Ollama, RubyLLM gem) from Ruby/Rails;
- building provider adapters or switching between hosted and local models;
- setting timeouts, retries, or token/cost budgets for model calls;
- parsing or validating structured model output (JSON schemas, typed results);
- designing agent loops, tool calls, or function calling;
- handling prompt-injection risk from user or external content;
- authorizing which tools/actions a model may trigger;
- adding LLM observability (latency, tokens, cost, failure modes);
- making features degrade gracefully when the model is unavailable;
- reviewing whether model output can reach safety-relevant paths.

Do not activate for AI code review workflows, for benchmark/eval tooling, or for pure prompt copywriting. Activate when the integration boundary — reliability, validation, safety, cost — is what is being engineered.

## Repository inspection

Inspect:

1. the LLM dependency: gem (RubyLLM, etc.) or raw HTTP, and its version contract;
2. every call site: which model, what parameters, synchronous or backgrounded;
3. timeout and retry configuration, including the gem's defaults;
4. how prompts are assembled and what untrusted content flows into them;
5. structured-output handling: parsing, schema validation, malformed-output behavior;
6. tool/function-call definitions and who executes them with what checks;
7. secret management: API keys, their scoping, and where they can be logged;
8. cost observability: token accounting, per-feature budgets, anomaly detection;
9. the degradation path of each feature when the provider errors or is slow;
10. every place model output is consumed, especially decisions, rankings, or data written to the database;
11. tests: fakes/VCR cassettes for providers, and malformed-output cases;
12. local models (Ollama) where present: version pinning, resource limits, and parity expectations.

Do not assume the provider is available, fast, deterministic, or honest about tokens; do not assume the gem's defaults are sane for your latency budget; and never assume the model "would never" produce malformed or injected output — it is an external system returning strings.

## Decision rules

1. Classify the change: provider adapter and budgets; output validation; trust boundaries and tool authorization; or operations and degradation. Load the matching reference below before changing that boundary.
2. Route all provider traffic through one adapter interface, so retries, budgets, telemetry, and provider swaps live in one place.
3. Bound every call: an explicit timeout, a bounded retry policy (only for safe-to-retry failures), and a token/cost budget per request and per feature.
4. Validate every structured output against a schema before it touches application state; malformed output is a handled outcome, not an exception to the exception handler.
5. Keep the trust boundary explicit: system/developer instructions, user content, and external content are different trust levels; external content never becomes instruction.
6. Authorize tool calls and actions at the execution boundary with deterministic checks — the model proposes, the application disposes.
7. Degrade, do not fail: features that can work without the model must not hard-depend on it, and safety paths must never call the model at all.

## Critical invariants

- Never place model output inside the prompt as instructions without marking and treating it as untrusted content.
- Never execute a tool call because the model requested it; execute it because a deterministic policy approved it.
- Never let an LLM call bypass, soften, or substitute a deterministic guard (risk checks, authorization, schema validation).
- Never call a provider without a timeout and a budget.
- Never log prompts containing secrets, API keys, or credentials.

## References

Load only the reference for the boundary being changed, before changing behavior there. Each reference is self-contained and one level deep; none links to another.

| Load when | Reference | Covers | Patterns |
|---|---|---|---|
| a change adds or alters provider calls, adapters, retries, budgets, or model versions | [references/provider-adapters-and-budgets.md](references/provider-adapters-and-budgets.md) | Adapter boundary; Timeouts and retries; Token and cost budgets; Model/version compatibility; Ollama and local models | `external-api-client` |
| a change parses model output, defines tools, or handles untrusted prompt content | [references/output-validation-and-tools.md](references/output-validation-and-tools.md) | Structured output; Schema validation; Prompt-injection boundaries; Tool-call authorization | `message-handler-boundary` |
| a change adds observability, degradation behavior, or places the model near a deterministic path | [references/operations-and-degradation.md](references/operations-and-degradation.md) | LLM observability; Graceful degradation; LLMs in deterministic systems; Backgrounding and caching | `circuit-breaker` |

## Reference example

One adapter, bounded and observable, validating output before it is used:

```ruby
# app/llm/provider.rb — the only object that talks to a provider.
class LLM::Provider
  class Unavailable < StandardError; end

  def initialize(client:, logger: Rails.logger)
    @client = client          # RubyLLM / Faraday adapter / test double
    @logger = logger
  end

  def complete(prompt:, schema:, budget: DEFAULT_BUDGET)
    response = @client.chat(
      messages: prompt.messages,
      model: prompt.model, temperature: 0.0,
      timeout: REQUEST_TIMEOUT                 # bounded in time...
    )
    tokens = response.usage                    # ...and counted in money
    LLM.cost_meter.record(feature: prompt.feature, tokens: tokens)

    LLM::ValidatedOutput.new(response.content, schema).tap do |output|
      raise LLM::InvalidSchema, output.errors unless output.valid?
    end
  rescue Faraday::TimeoutError, LLM::Client::ConnectionError => e
    @logger.warn("[llm] provider unavailable: #{e.class}")
    raise Unavailable                          # caller decides how to degrade
  end
end
```

`Unavailable` is the adapter's honest failure; degradation belongs to the feature (cached answer, rule-based fallback, or a friendly "unavailable" — never a stack trace). The model's text never reaches application state without `ValidatedOutput` approving it.

## Agent review checklist

- [ ] one adapter interface owns all provider traffic
- [ ] every call has an explicit timeout and bounded retry policy
- [ ] token/cost usage recorded per feature and per request
- [ ] structured outputs validated against a schema before use
- [ ] malformed output a handled outcome with a named behavior
- [ ] untrusted content in prompts clearly delimited, never instructions
- [ ] tool calls authorized by deterministic policy at execution time
- [ ] no model output reaches safety-relevant guards or authorization
- [ ] secrets never logged; prompts sanitized before logging
- [ ] degradation path per feature; deterministic paths independent of the model
- [ ] provider tests use fakes/cassettes; no live keys in CI
- [ ] model/version changes pinned and observable

## Anti-patterns

- calling the provider SDK from five different services;
- no timeout (the gem default or none) on a request that blocks a web request;
- retrying a call that may have already spent tokens without a budget check;
- `JSON.parse(model_text)` with `rescue nil` and a silent `nil` consumer;
- concatenating user content into the system prompt;
- executing whatever tool the model names, with the model's own arguments;
- letting the model "decide" whether a risk check passes;
- an AI feature whose outage takes down checkout;
- logging full prompts (secrets, PII, user content) at info level;
- hardcoded model strings in six files;
- treating a local Ollama as "free, no limits needed" (GPU memory and time are budgets too);
- prompt-injection fix by asking the model politely to ignore injection.

## Verification

For the adapter:

`call -> bounded time -> usage recorded -> provider swap changes configuration, not call sites`

For output:

`model text -> schema validation -> valid parsed result or named invalid-output outcome`

For tools:

`model proposes -> policy evaluates deterministically -> approved/rejected with reason`

For degradation:

`provider down -> feature degrades or queues -> safety paths unaffected -> recovery restores function`

Report the boundary shape, budget configuration, validation outcomes, tool policy, and the degradation evidence.

## Source foundation

- RubyLLM: https://rubyllm.com/
- Ollama API: https://github.com/ollama/ollama/blob/main/docs/api.md
- OWASP LLM Top 10 (prompt injection, excessive agency): https://genai.owasp.org/
- OpenAI structured outputs (schema discipline reference): https://platform.openai.com/docs/guides/structured-outputs
- Repository skills: ruby-dependency-injection, rails-api-integration, rails-security, rails-observability, trading-execution-safety, rails-active-job, ruby-tdd-refactoring

## Ruby LLM integration changes

For provider, prompt, agent, and model-output changes:

- route provider traffic through one adapter with explicit model/version configuration;
- bound every call in time and money: timeout, bounded retry for safe-to-retry failures only, per-request and per-feature token/cost budgets with usage recorded;
- validate structured output against a schema before application state consumes it, and handle malformed output as a designed outcome;
- delimit untrusted content in prompts and never promote it to instruction;
- authorize tool calls at the execution boundary with deterministic policy, and treat unapproved tool requests as data, not commands;
- keep model output out of deterministic guards, authorization, and safety checks — the model may propose, only the application may decide;
- degrade features explicitly when the provider is unavailable, and keep deterministic paths fully independent of model calls;
- observe calls without logging secrets or private content: latency, tokens, cost, failure class, refusal;
- test with provider fakes and malformed-output fixtures, never with live keys in CI;
- pin model and provider versions, and treat upgrades as behavior changes requiring evaluation.
