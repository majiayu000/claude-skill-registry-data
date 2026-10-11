---
name: script-scanner
description: Review scripts for vulnerabilities, unsafe patterns, reliability issues, and design flaws, then produce a concise report. Use when Codex needs to audit or sanity-check executable scripts or automation files such as `.sh`, `.bash`, `.zsh`, `.py`, `.js`, and `.ts`, especially when asked to find security issues, risky command execution, secret handling problems, fragile error handling, or maintainability concerns.
---

# Script Scanner

## Overview

Review a script with a security-first mindset and produce a short, actionable report. Focus on real risk, cite the exact location when possible, and avoid padding the output with style-only feedback.

## Review Workflow

1. Identify the script type, entrypoints, inputs, side effects, and external dependencies before judging the implementation.
2. Trace untrusted input through the script and note where it reaches command execution, file paths, network calls, interpreters, templates, queries, or privileged operations.
3. Inspect for high-severity issues first: injection, arbitrary file access, secret exposure, auth bypass, unsafe temp file usage, insecure deserialization, race conditions, and privilege escalation.
4. Inspect for reliability and design risks that can become security issues: missing validation, silent failure, weak error handling, brittle retries, hidden global state, unsafe defaults, and unbounded resource use.
5. Prefer a quick report over an exhaustive essay. Keep the output short unless the user explicitly asks for depth.

## Reporting Rules

- Lead with findings ordered by severity.
- Include file and line references when they are available from the supplied artifact.
- For each finding, explain the risk in one or two sentences and give a concrete fix or mitigation.
- Distinguish between confirmed findings, likely risks, and open questions.
- If no material problems are found, say so explicitly and mention any testing or context gaps that limit confidence.

Use this report shape by default:

```text
Findings
- High: <issue> — <file:line if known>
- Medium: <issue> — <file:line if known>

Open Questions
- <only include when they materially affect confidence>

Summary
- <1-2 sentence overall risk assessment>
```

## Review Priorities

- Treat exploitable behavior as more important than style or architecture.
- Flag command construction that concatenates untrusted input into shell commands, subprocess arguments, eval-like features, SQL, templates, or dynamic imports.
- Flag file-system risks such as path traversal, unsafe permissions, world-writable temp files, symlink attacks, and destructive operations without safeguards.
- Flag credential handling problems such as embedded secrets, token leakage to logs, insecure environment-variable usage, and accidental transmission of secrets to subprocesses.
- Flag network and dependency risks such as disabled TLS verification, unsafe downloads, executing remote content, and unpinned or implicitly trusted tools.
- Flag control-flow weaknesses such as broad exception swallowing, missing exit-code checks, partial rollback, or cleanup paths that hide failure.
- Flag design flaws that make the script hard to trust or operate safely: too much implicit behavior, surprising side effects, lack of dry-run support for destructive actions, and weak boundaries between parsing, validation, and execution.

## Language Notes

- For shell scripts, pay extra attention to quoting, word splitting, globbing, `eval`, `mktemp` usage, `set -euo pipefail`, cleanup traps, and unsafe `rm` patterns.
- For Python scripts, inspect `subprocess`, `pickle`, `yaml.load`, temporary-file handling, filesystem permissions, requests/TLS settings, and user-controlled imports or execution.
- For JavaScript and TypeScript scripts, inspect `child_process`, dynamic evaluation, path joins, template injection, unsafe deserialization, fetch/request defaults, and environment-variable exposure.

Read [review-checklist.md](./references/review-checklist.md) when the script touches command execution, temp files, authentication, secrets, external downloads, or any area that warrants a deeper checklist.

## Scope Control

- Do not recommend a rewrite when a targeted mitigation is enough.
- Do not invent exploitability without a plausible path from input to impact.
- Do not bury the main risks under minor code-quality notes.
- Ask for the actual script or relevant file paths if the user requests a review without supplying the artifact.
