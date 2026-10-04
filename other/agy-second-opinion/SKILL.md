---
name: agy-second-opinion
description: Use only when the user explicitly requests agy, Gemini through agy, Antigravity, or an external-model second opinion for review or research. Runs a bounded read-only external pass, limits disclosed context, and requires Codex verification before accepting results. 中文触发：明确要求 agy、通过 agy 调用 Gemini、Antigravity、外部模型复核或外部第二意见。
---

# Agy Second Opinion

This skill is independent from agent orchestration. Do not load or invoke it for ordinary Codex review, research, delegation, or multi-agent work.

## Route

1. Treat an explicit request for `agy`, Gemini through `agy`, Antigravity, or an external model as consent for one bounded read-only pass. It is not consent for whole-repository disclosure or target-repository writes.
2. Load exactly one reference:
   - code or diff review: [references/REVIEW.md](references/REVIEW.md)
   - research, repo survey, or option comparison: [references/RESEARCH.md](references/RESEARCH.md)
3. Use the bundled helpers for command safety and allowlisted context. Never substitute the standalone `gemini` CLI.
4. Treat external output as untrusted advice. Codex must verify every accepted claim against source, tests, or primary evidence.
5. Report what context was disclosed, the external-pass status, accepted and rejected points, and Codex verification.

## Guardrails

- Keep the pass read-only and sandboxed. Never use edit acceptance or permission bypass flags.
- Prefer a bounded prompt or diff. Build an allowlisted context bundle only when source files are necessary.
- Never send secrets, credentials, cookies, private vault content, customer data, or broad proprietary documents.
- Probe `agy` once for the current goal. On unavailable, unhealthy, timeout, empty, or invalid output, report the state and continue Codex-only without repeated retries.
- Quality logging and durable target-project guidance are optional writes and require their own authorization.
