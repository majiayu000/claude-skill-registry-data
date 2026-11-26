---
name: ai-redteam-lord
description: Lord skill for CI-integrated AI red-teaming — adversarial testing across prompt injection, jailbreak, data leakage, bias, and tool abuse with measurable coverage and false-positive tracking.
triggers:
  - ai redteam lord
  - red team
  - redteam
  - adversarial
  - prompt injection test
  - jailbreak test
  - garak
  - promptfoo
  - detoxio
  - فريق أحمر
  - اختبار اختراق الذكاء الاصطناعي
personas:
  - SEC
  - QA
  - ML
  - ARCH
tech_stack: []
lord: true

---

# AI Redteam Lord

[OBJ] Integrate automated adversarial testing into CI pipelines to find, measure, and fix AI vulnerabilities before production deployment.

## Problem

AI systems fail in ways traditional security testing does not cover: prompt injection exfiltrates data, jailbreaks bypass guardrails, hallucinated tool calls cause real damage, and bias surfaces in production. Red-teaming is often a one-off manual exercise — it must be continuous, measurable, and gated in CI to keep pace with model and prompt changes.

## Rules

1. [REQ] **Red-team in CI.** Adversarial tests MUST run in CI on every PR touching prompts, system messages, tool definitions, or model config. Use Promptfoo (local/fast), Garak (broad probes), Detoxio (enterprise), Arthur Bench (comparison). No manual-only red-teaming.
2. [REQ] **Attack category coverage.** Test suites MUST cover: prompt injection (direct + indirect), jailbreak ( DAN, role-play, encoding), data leakage (PII extraction, system prompt extraction), hallucination (fabricated facts, fake citations), bias (demographic, sentiment), tool abuse (unauthorized calls, parameter manipulation).
3. [REQ] **OWASP LLM Top 10 2026.** Map every test to an OWASP LLM Top 10 category (LLM01–LLM10). Coverage report shows which categories have tests and which are gaps. No category may be at zero coverage.
4. [REQ] **ASI Top 10 testing.** Test against Agentic Security Initiative Top 10: agent privilege escalation, tool injection, memory poisoning, multi-agent collusion, resource exhaustion, goal hijacking.
5. [REQ] **Cross-modal attack testing.** For multimodal systems, test image-based prompt injection (hidden text in images), audio injection, and document-embedded instructions. Text-only testing is insufficient for vision/audio-capable models.
6. [REQ] **Memory-persistence attack testing.** For agents with memory, test: memory poisoning (inject false memories), memory extraction (pull stored PII), memory persistence across sessions (unauthorized recall), and memory eviction bypass.
7. [REQ] **MCP tool poisoning testing.** For MCP-connected agents, test: malicious tool definitions (renamed tools, changed schemas), tool response injection (tool returns prompt-injection payload), and tool enumeration attacks (discover hidden tools).
8. [REQ] **Benchmark suites.** Use established benchmarks: Lakera PINT (prompt injection), PIArena (injection in practice), HarmBench (harmful content), AdvBench (adversarial suffixes). Track pass/fail rates over time — regression = CI failure.
9. [REQ] **False positive measurement.** Every red-team suite MUST include benign control cases. Measure false-positive rate (benign flagged as attack). Target FP rate <5%. High FP = guardrails too aggressive, not secure.
10. [REQ] **Benign case testing.** Run an equal number of benign prompts through the same pipeline. If benign cases fail, the guardrails are broken, not the attacks. Benign pass rate must be ≥95%.
11. [REQ] **Coverage metrics.** Track: attack category coverage (%), probe count per category, model versions tested, guardrail versions tested. Coverage dashboard updated every CI run. No silent coverage drops.
12. [REQ] **CI gate integration.** Red-team results gate the pipeline: critical vulnerability = BLOCK, high = WARN (require override), medium = INFO. Gate thresholds configurable per environment (prod stricter than staging).
13. [REQ] **Regression testing.** Every fixed vulnerability gets a regression test added to the suite. The test must fail on the vulnerable version and pass on the fixed version. No fix without a regression test.
14. [REQ] **Report generation.** CI produces a structured report: JSON (machine-readable) + HTML (human-readable). Includes: attack categories tested, pass/fail per probe, FP rate, coverage matrix, trend vs last run. Archived for audit.
15. [REQ] **Adversarial dataset versioning.** Attack datasets MUST be versioned (git or registry). Every CI run records dataset version + model version + guardrail version. Reproducibility is non-negotiable.
16. [REQ] **Threat model alignment.** Tests MUST trace to a documented threat model (STRIDE or AI-specific). No test exists without a threat it addresses. No threat exists without at least one test.
17. [REQ] **Human escalation.** Ambiguous results (possible novel attack, guardrail edge case) escalate to human review with full context: prompt, response, guardrail verdict, model version. No silent auto-dismiss.
18. [PROHIBIT] Deploying a model or prompt change to production without a green red-team CI run. No "we'll test it after launch."

## References

- OWASP LLM Top 10 (2026 edition)
- Agentic Security Initiative (ASI) Top 10
- Promptfoo: https://www.promptfoo.dev
- Garak: https://github.com/leondz/garak
- Detoxio: https://detoxio.ai
- Arthur Bench: https://github.com/arthur-ai/bench
- Lakera PINT benchmark
- PIArena: prompt injection in practice
