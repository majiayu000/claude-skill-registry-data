---
name: ai-code-review-lord
description: Lord skill for AI-powered code review and security scanning — automated pre-PR review, diff-aware analysis, hallucination detection in AI-generated code, severity gating, and human escalation.
triggers:
  - ai code review lord
  - ai code review
  - automated review
  - bugbot
  - self-review
  - code scanning
  - security scanning
  - مراجعة كود
  - فحص أمني
personas:
  - QA
  - SEC
  - ARCH
  - DEV
tech_stack: []
lord: true

---

# AI Code Review Lord

[OBJ] Automate pre-PR code review with AI tools, security scanning, diff-aware analysis, and hallucination detection — gated by severity, with human escalation for high-risk changes.

## Problem

Human code review is slow, inconsistent, and bottlenecked. AI-generated code introduces new failure modes: hallucinated APIs, fabricated imports, and plausible-but-wrong logic that passes human glance. Traditional linters catch style issues but miss semantic bugs. The gap between "merged" and "correct" needs automated, diff-aware, security-conscious review that knows the difference between AI-generated and human-written code.

## Rules

1. [REQ] **Automated pre-PR review.** Run AI review BEFORE the PR is created or opened. Developer runs review locally (Cursor Bugbot, Copilot self-review, Claude Code review) on the diff. Review feedback is addressed before the PR reaches a human reviewer. No PR opens without a prior AI review pass.
2. [REQ] **Security scanning — three layers.** (a) Secret detection (GitLeaks, TruffleHog — scan for API keys, tokens, passwords in diff), (b) Dependency scanning (Dependabot, Snyk — CVEs in new/changed dependencies), (c) Code scanning (Semgrep, CodeQL — static analysis for injection, XSS, SSRF, path traversal). All three run in CI; all three gate the pipeline.
3. [REQ] **AI review tools.** Cursor Bugbot (inline review in Cursor IDE), Copilot self-review (GitHub-native, PR comments), Claude Code review (agentic, can read full repo context). Use at least one. Each tool has different strengths — Bugbot for IDE-integrated, Copilot for PR-integrated, Claude for deep-context.
4. [REQ] **Review checklist.** Every review covers: correctness (does the code do what it claims?), security (injection, auth bypass, data exposure), performance (N+1 queries, unnecessary allocations, blocking calls), maintainability (readability, complexity, naming), test coverage (are the changed paths tested?).
5. [REQ] **False positive management.** Track FP rate per reviewer (AI + human). If an AI reviewer flags >30% false positives, tune its configuration or switch tools. Developers can dismiss AI comments with a reason — dismissed comments feed back into FP tracking. No AI review tool runs untuned.
6. [REQ] **Review severity levels.** BLOCK (security vulnerability, data loss, broken functionality — must fix before merge), WARN (code smell, missing test, performance concern — should fix, can override with justification), INFO (style, suggestion, nitpick — optional). CI gate: BLOCK = pipeline fails, WARN = requires override, INFO = no gate.
7. [REQ] **Review integration in CI/CD.** AI review runs as a CI job on every PR. Results posted as PR comments (inline on specific lines). BLOCK-level findings fail the CI check. Review runs in parallel with tests — does not extend pipeline time.
8. [REQ] **Human review escalation.** Escalate to human review when: (a) AI reviewer confidence is low, (b) change touches security-critical code (auth, crypto, payment), (c) change >500 lines (AI context limits), (d) AI-generated code with novel patterns. No auto-merge on escalated changes.
9. [REQ] **Review metrics.** Track: review time (AI + human), defect density (bugs found per 1K lines), escape rate (bugs found post-merge / total bugs), FP rate, override rate. Review metrics dashboard updated weekly. Trend analysis — no metric should be unmeasured.
10. [REQ] **Diff-aware review.** Review ONLY changed lines + surrounding context (±10 lines). Full-file review wastes tokens and produces irrelevant findings. AI reviewer receives the git diff, not the full file. Context window is for understanding, not re-reviewing unchanged code.
11. [REQ] **Large diff handling.** Diffs >1000 lines: split into logical chunks (by file or by commit) and review each chunk separately. Diffs >5000 lines: require human review + architectural sign-off. No single AI review pass on a 5000-line diff — context window limits guarantee missed findings.
12. [REQ] **Review for AI-generated code.** When code is AI-generated (Cursor, Copilot, Claude), apply additional checks: (a) hallucination detection — verify all API calls, function names, and imports exist in the codebase or documented SDK, (b) API verification — check that function signatures match the actual API, (c) import verification — every import resolves to a real module.
13. [REQ] **Hallucination detection.** For AI-generated code, cross-reference every API call against: (a) the project's codebase (does this function exist?), (b) the SDK documentation (does this method exist in this version?), (c) the lockfile (is this package version the one with this API?). Flag any mismatch as BLOCK — AI hallucinations compile sometimes but fail at runtime.
14. [REQ] **Review bypass prevention.** No developer can bypass BLOCK-level findings without: (a) documented justification, (b) approval from a second reviewer or tech lead, (c) a tracking ticket. Bypass attempts are logged and audited. No silent overrides.
15. [REQ] **Audit trail for reviews.** Every review (AI + human) is logged: reviewer, files reviewed, findings, severity, resolution (fixed/dismissed/escalated), timestamp. Audit trail retained per compliance policy. No review happens without a log entry.
16. [PROHIBIT] Merging AI-generated code without hallucination detection and API verification — AI can write code that looks correct, compiles, and is completely wrong.

## References

- Cursor Bugbot: https://cursor.com
- GitHub Copilot self-review: https://docs.github.com/copilot
- Semgrep: https://semgrep.dev
- CodeQL: https://codeql.github.com
- GitLeaks: https://github.com/gitleaks/gitleaks
- TruffleHog: https://github.com/trufflesecurity/trufflehog
- Dependabot: https://docs.github.com/code-security/dependabot
- Snyk: https://snyk.io
