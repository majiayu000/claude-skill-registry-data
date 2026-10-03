---
name: ai-redteam
description: AI and LLM red-teaming skill for evaluating prompt injection, jailbreak, data exfiltration, tool abuse, agent hijack, RAG poisoning, model denial of service, and unsafe tool-use chains in Gemini, Claude, GPT, and open-weight models. Use to build evaluation harnesses, attack corpora, defensive guardrails, and red-team reports for AI systems you own or are authorized to test.
---

# AI Red Team

## Authorization Boundary

- Only target models, agents, and applications the user owns or has written authorization to test.
- Do not produce working malware, CSAM, weapons synthesis, or content that bypasses model safety for harmful real-world outcomes.
- Treat findings as defensive: every successful attack must ship with a detection and a mitigation.

## Attack Taxonomy

- `Direct injection`: instructions in user input override system policy.
- `Indirect injection`: hostile content in retrieved docs, web pages, emails, files, image alt-text, or tool output.
- `Jailbreak`: roleplay, hypothetical, encoding, obfuscation, multi-turn drift, persona pinning.
- `Tool abuse`: forcing browse, shell, code, or MCP tools to act outside scope (SSRF, file read, command exec).
- `Data exfiltration`: leaking system prompt, secrets, embeddings, training data, or per-user memory.
- `Agent hijack`: rewriting plans, looping, escalating permissions, calling unintended sub-agents.
- `RAG poisoning`: index pollution, ranking manipulation, embedding collisions.
- `Resource exhaustion`: token bombs, recursive tool calls, prompt-bomb DoS.

## Evaluation Workflow

1. Map the AI surface: model, system prompt, tools, retrievers, memory, output sinks, and downstream callers.
2. Build a threat model with abuse cases per surface.
3. Generate a versioned attack corpus (`attacks.jsonl`) with `{id, technique, payload, expected_block, severity}`.
4. Run the harness; record `{pass, fail, partial, refusal_quality, leak_evidence}`.
5. Score with attack success rate per technique, mean time to refuse, and blast radius.

## Defensive Output

- Input/output classifiers and allow-listed tool schemas.
- Provenance tags on retrieved context; quarantine for untrusted sources.
- Plan-then-execute pattern with human approval on high-impact tools.
- Rate limits, recursion caps, and per-tool budgets.
- Red-team report: top techniques, reproductions, fix owners, regression tests.

## Deliverables

- `surface.md`, `threats.md`, `attacks.jsonl`, `harness/`, `results.csv`, `report.md`, `regression-suite/`.
