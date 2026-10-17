---
name: "codeql"
description: "Scans a codebase for security vulnerabilities using CodeQL's interprocedural data flow and taint tracking analysis. Triggers on \"run codeql\", \"codeql scan\", \"codeql analysis\", \"build codeql database\", or \"find vulnerabilities with codeql\". Supports \"run all\" (security-and-quality + security-experimental suites) and \"important only\" (high-precision security findings) scan modes. Also handles creating data extension."
source_skill_id: "trailofbits-skills-plugins-static-analysis-skills-codeql-skill-md"
category: "Security, compliance & risk"
source_mirror: "../../../../../skills/by-category/security-compliance-risk/security-reference/codeql/SKILL.md"
benchmark_status: "artifact_gated"
---

# codeql

Use this skill when the task matches the description above or the source path clearly applies. Start with this concise entrypoint; open `../../../../../skills/by-category/security-compliance-risk/security-reference/codeql/SKILL.md` only when implementation details, commands, assets, or references are needed.

Before repository work, read and apply [Mandatory agent tools](../../../../../../docs/agent-tools.md): Caveman for every task, CocoIndex Code before broad code navigation, and Crawl4AI for web-page research. Retain actual execution evidence; do not claim unavailable tools ran. Repository-level rules remain controlling.

## Workflow

1. Confirm the task matches this skill's scope.
2. Read the local source mirror if more detail is required.
3. Follow repository-level `AGENTS.md`; use one AI session only.
4. Keep claims tied to files, commands, citations, or benchmark artifacts.

## Verification

- Source mirror: `../../../../../skills/by-category/security-compliance-risk/security-reference/codeql/SKILL.md`
- Source commit: `e8cc5baf9329ccb491bfa200e82eacbac83b1ead`
- Static benchmark results: see `docs/benchmark-results.md`
- Runtime artifacts recorded by this entrypoint: `0`
- Assigned scenarios: `skill-proof-trailofbits-skills-plugins-static-analysis-skills-codeql-skill-md`, `security-compliance-and-risk-owasp-benchmark`, `security-compliance-and-risk-owasp-juice-shop`, `security-compliance-and-risk-kubernetes-examples`

Do not claim this skill passed a runtime benchmark until a validated artifact exists.
