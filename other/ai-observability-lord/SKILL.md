---
name: ai-observability-lord
description: Lord skill for AI observability and tracing — OpenTelemetry + OpenInference standards, span attributes, eval integration, cost/latency/error tracking, drift detection, and PII redaction.
triggers:
  - ai observability lord
  - observability
  - tracing
  - langsmith
  - langfuse
  - phoenix
  - arize
  - openinference
  - otel
  - مراقبة
personas:
  - SRE
  - ML
  - MLOPS
  - DEVOPS
  - ARCH
tech_stack: []
lord: true

---

# AI Observability Lord

[OBJ] Instrument AI systems with standards-based tracing, evaluation integration, cost/latency/error monitoring, and drift detection — with PII-safe traces and actionable dashboards.

## Problem

AI systems are opaque: a request flows through prompt construction, retrieval, LLM call, tool use, guardrails, and response formatting — any of which can degrade silently. Traditional APM (latency + error rate) cannot see inside the LLM call. Without AI-specific observability, quality degrades undetected until users complain, and root cause is untraceable.

## Rules

1. [REQ] **OpenTelemetry + OpenInference.** Instrument all AI components with OpenTelemetry spans using OpenInference semantic conventions. Span attributes: `llm.model_name`, `llm.token_count.prompt`, `llm.token_count.completion`, `llm.tools`, `retrieval.documents`, `guardrail.verdict`. No custom attribute names that duplicate OpenInference.
2. [REQ] **Span attributes per component.** LLM spans: model, tokens, temperature, system prompt hash. Tool spans: tool name, input, output, duration. Retrieval spans: query, documents retrieved, scores. Guardrail spans: verdict (allow/deny/redact), reason, latency. Every component type has a defined attribute set.
3. [REQ] **Tracing tool selection.** LangSmith (LangChain ecosystem, managed), Langfuse v4 (open-source, self-hostable, multi-framework), Arize Phoenix (open-source, local-first, LLM + traditional ML), Braintrust (eval + observability), Helicone (proxy-based, OpenAI-focused), Portkey (gateway + observability). Match tool to stack and hosting preference.
4. [REQ] **Eval integration.** Traces MUST link to evaluations. Every production trace can be scored by an evaluator (LLM-as-judge, rule-based, human). Eval scores appear as span attributes. Closed-loop: traces → evals → alerts → fixes → re-eval.
5. [REQ] **Cost tracking.** Track cost per request: input tokens × price + output tokens × price + tool call costs + retrieval costs. Aggregate per user, per agent, per workflow. Cost anomaly (spike >3σ) triggers alert. Cost dashboard updated in real-time.
6. [REQ] **Latency monitoring.** Track latency at each span: LLM call (TTFT + total), retrieval, tool execution, guardrail, end-to-end. P50/P95/P99 percentiles. SLO: P95 < target. Latency regression in CI = block.
7. [REQ] **Error tracking.** Track errors by type: LLM error (rate limit, context overflow, content filter), tool error (timeout, auth, invalid input), retrieval error (no results, index down), guardrail error (misclassification). Error rate > threshold = alert with trace link.
8. [REQ] **Drift detection.** Monitor for: input drift (prompt distribution shift), output drift (response distribution shift), performance drift (eval score decline). Use statistical tests (KS test, PSI) on rolling windows. Drift detected = alert + trigger eval re-run on recent traces.
9. [REQ] **Data residency.** Traces contain user prompts and responses — PII. For EU/regulated deployments, self-host the tracing backend (Langfuse, Phoenix) in-region. No trace data leaves the jurisdiction. Document data residency per deployment.
10. [REQ] **Self-hosting vs cloud.** Self-host (Langfuse, Phoenix) for: data residency, cost control at scale, air-gapped environments. Cloud (LangSmith, Braintrust) for: zero ops, fast setup, managed evals. Decision documented per project with rationale.
11. [REQ] **Retention policies.** Define trace retention: 30 days for debugging, 90 days for trend analysis, 1 year for audit (sampled). Auto-delete expired traces. PII traces may have shorter retention. No indefinite retention without explicit policy.
12. [REQ] **Sampling strategies.** Full tracing at low volume. At high volume: head-based sampling (sample by request attributes — always trace errors, always trace slow requests, sample 10% of normal). Tail-based sampling in OTel Collector. Never sample away all errors.
13. [REQ] **PII redaction in traces.** Redact PII before storage: use regex + NER-based redaction on prompt and response text. Store redacted version in trace, original in encrypted vault with separate access control. No raw PII in trace storage.
14. [REQ] **Dashboard design.** Dashboards show: request volume, latency percentiles, error rate, cost per request, eval score trend, drift indicators, top failing traces. Role-based: SRE sees ops metrics, ML sees quality metrics, product sees user-facing metrics.
15. [REQ] **Alerting.** Alerts on: error rate > threshold, P95 latency > SLO, cost spike >3σ, eval score drop > threshold, drift detected. Alerts include trace link, affected user count, and suggested investigation path. No alert without a runbook.
16. [PROHIBIT] Shipping an AI system to production without tracing, cost tracking, and PII redaction — untraced AI is unaccountable AI.

## References

- OpenTelemetry: https://opentelemetry.io
- OpenInference: https://github.com/Arize-ai/openinference
- LangSmith: https://smith.langchain.com
- Langfuse: https://langfuse.com
- Arize Phoenix: https://phoenix.arize.com
- Braintrust: https://braintrust.dev
- Helicone: https://helicone.ai
- Portkey: https://portkey.ai
