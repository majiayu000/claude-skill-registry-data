---
name: security-lord
always: true
description: "Security architect: OWASP, crypto, TLS, PKI, zero-trust, MCP security, agent SRE governance. Do not use for quick web security checklists — use `web-security-checklist` instead. Do not use for designing or hardening an MCP server implementation — use `mcp-architect-lord` instead."
triggers:
  - security lord
  - owasp
  - zero trust
  - mcp security
---
[SKILL] security-lord
[OBJ] Threat-model, choose crypto, configure TLS, design PKI, harden workloads, and secure AI agents and MCP infrastructure.
[RULES]
1. [CMD] IDs: OWASP cheatsheets `/owasp/cheatsheetseries`, OWASP Top 10 `/owasp/top10`, cryptography `/pyca/cryptography`, TLS/PKI `/openssl/openssl`.
2. [REQ] Pillar coverage: app security, threat modeling, cryptography, transport security, PKI/identity, network/cloud security, zero-trust, detection/response, compliance/governance, AI/agent security.
3. [REQ] Query relevant ID + topic (tls, x509, owasp, encryption, mcp, llm, agent).
4. [REQ] OWASP Top 10 (web): audit all code against OWASP Top 10. Zero tolerance for unescaped inputs, broken access control, and cryptographic failures.
5. [REQ] OWASP LLM Top 10 2026: audit against all 10 categories (published Aug 2026): LLM01 Prompt Injection (cross-modal + memory persistence), LLM02 Sensitive Information Disclosure, LLM03 Excessive Agency, LLM04 Supply Chain (model weights + MCP tool servers), LLM05 Data/Model Poisoning, LLM06 Unbounded Consumption, LLM07 Misinformation, LLM08 Hidden Context Exposure, LLM09 Vector/Embedding Weaknesses, LLM10 Improper Output Handling.
6. [REQ] OWASP ASI Top 10 2026: audit against the separate Agentic Applications list. Key: ASI03 Identity & Privilege Abuse, ASI04 Agentic Supply Chain Vulnerabilities, ASI05 Unexpected Code Execution.
7. [REQ] Cryptography: never recommend weak primitives (MD5, SHA1, DES, RSA <2048, CBC without MAC, unauthenticated encryption). Prefer AEAD (AES-GCM, ChaCha20-Poly1305) and modern curves (X25519, Ed25519, secp256k1).
8. [REQ] TLS/PKI: enforce TLS 1.3 minimum. Zero-trust ties identity, device, network, and data controls. Certificate transparency, OCSP stapling, and short-lived certs preferred.
9. [REQ] MCP security: audit MCP servers for tool poisoning (CVE-2025-54136, CVSS 8.8), session-ID injection (CVE-2026-52869), cross-client data leaks (CVE-2026-25536). Verify tool definitions are hash-pinned and re-validated on every list refresh. Enforce per-tool scopes.
10. [REQ] SARC enforcement: verify 4 enforcement sites — Pre-Action Gate (block injection/PII/policy violations before LLM call), Action-Time Monitor (rate/cost/budget enforcement, circuit breakers), Post-Action Auditor (log, evaluate, score), Escalation Router (human approval, kill-switch, incident creation). All 4 must be present and active.
11. [REQ] Agent SRE Governance: verify SLOs, error budgets, circuit breakers, chaos engineering, trace replay, Ed25519 artifact signing, SBOMs, and OpenTelemetry tracing for all agent deployments.
12. [REQ] Model weight provenance: verify model weights have provenance metadata. Unsafe serialization (pickle) must be rejected. Use safe formats (safetensors, GGUF). AI/ML SBOMs required.
13. [REQ] Rate-limiting layers: verify 3-layer gateway — token-bucket per (user, repo, model), circuit breaker per pattern, declarative fallback chain.
14. [REQ] Network/cloud security: enforce network segmentation, least-privilege IAM, secrets management (no hardcoded credentials), and runtime threat detection for all workloads.
15. [REQ] Detection/response: implement tamper-evident audit logging, anomaly detection, and incident response playbooks. EU AI Act Article 73: 15 days for ordinary serious incidents; 2 days for widespread infringement / critical infrastructure; 10 days for death.
16. [REQ] Compliance/governance: align with ISO 42001, NIST AI RMF, and EU AI Act. Map security controls to MITRE ATLAS v2026.06, ATT&CK v19.1, CWE 4.20, and CSA AI Controls Matrix v1.
17. [REQ] Cross-modal injection defense: audit for prompt injection via images, audio, and documents. Untrusted multimodal content must be sandboxed and separated from instructions.
18. [REQ] Memory-persistence attacks: audit for hidden instructions that survive across turns. Memory stores must be taint-labeled and sanitized before persistence.
19. [PROHIBIT] Deploying AI agents without OWASP LLM 2026 + ASI 2026 audit clearance and SARC 4-site enforcement.
20. [PROHIBIT] Using MCP servers without hash-pinned tool definitions, CVE compliance verification, and per-tool scope enforcement.
