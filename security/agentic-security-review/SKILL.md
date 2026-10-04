---
name: agentic-security-review
description: >
  Run a security and dependency audit for agent systems, tool-using AI apps,
  MCP/A2A integrations, or security-sensitive AI-generated code. Check
  slopsquatting risk, tool shadowing, rug pulls, memory/context poisoning,
  secrets, unsafe permissions, and common CWE patterns. Use when asked for
  security review, dependency audit, vulnerability check, MCP tool safety, or
  production merge safety. Do NOT use for general code review, style issues,
  feature work, performance tuning, or non-security bugs.
---

# Agentic Security Review

Use this skill to find security risks introduced by agentic code, AI-generated
changes, tool access, or untrusted context. Scope the review before scanning.

## Workflow

1. Determine scope:
   - `deps-only`: package declarations, lockfiles, imports.
   - `code-only`: secrets, auth, input handling, injection risks.
   - `full`: dependencies, code, tools, memory, context, red-team cases.
2. Classify rigor:
   - Prototype: dependency and secret checks.
   - Internal: dependency, secret, input validation, and tool permission checks.
   - Production: full review plus context poisoning, CaMeL-style separation
     decision, red-team scenarios, and release blockers.
3. Run `scripts/check_deps.py <project-root>` when Python files are present.
4. Fill `SECURITY_REVIEW.md` from `assets/templates/SECURITY_REVIEW.md`.
5. Mark findings with severity, evidence, file path, and concrete fix.
6. Block release only for exploitable or high-impact issues; otherwise provide
   prioritized remediation.

## Focus Areas

- Dependencies: undeclared imports, unpinned direct dependencies, missing
  lockfile, suspicious package names.
- Tools: shadowing, broad credentials, unsafe side effects, unclear provenance.
- Code: CWE-20, CWE-78, CWE-89, CWE-327, hardcoded secrets, weak auth.
- Context: prompt injection through external data, memory poisoning, unsafe tool
  responses, mixed trusted/untrusted data.

## References

Read `../agentic-engineering-sdlc/references/day2_tools_and_interop.md` for
tool risks and `../agentic-engineering-sdlc/references/day4_security_and_evaluation.md`
for security/evaluation depth.

## Done Criteria

- Scope, rigor, and exclusions are documented.
- Script output is attached or summarized when applicable.
- Release blockers are separated from hardening recommendations.
- Every high/critical finding has a reproduction path or clear evidence.
