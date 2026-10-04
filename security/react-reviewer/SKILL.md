---
name: "react-reviewer"
description: "Describe what this skill helps an agent do."
version: "0.1.0"
since: "2026-09-09"
last_modified: "2026-09-09"
authors:
  - "platform-engineering"
stability: "experimental"
min_platform_version:
  codex: "unknown"
  amazon-q: "unknown"
  antigravity: "unknown"
  auggie: "unknown"
  bob: "unknown"
  claude-code: "unknown"
  cline: "unknown"
  codebuddy: "unknown"
  continue: "unknown"
  costrict: "unknown"
  crush: "unknown"
  github-copilot: "unknown"
  gitlab-duo: "unknown"
  factory: "unknown"
  forgecode: "unknown"
  opencode: "unknown"
  openhands: "unknown"
  cursor: "unknown"
  roo-code: "unknown"
  kiro: "unknown"
  junie: "unknown"
  gemini-cli: "unknown"
  iflow: "unknown"
  kilocode: "unknown"
  kimi: "unknown"
  lingma: "unknown"
  pi: "unknown"
  qoder: "unknown"
  qwen: "unknown"
  windsurf: "unknown"
  ollama: "unknown"
deprecated_since:
replaces:
supersedes: []
changelog:
  - version: "0.1.0"
    date: "2026-09-09"
    change: "Initial generated production-ready SDLC / DevSecOps skill"
---
# React Reviewer

## Purpose

Review React applications for hooks correctness, component composition, prop drilling elimination, memoisation discipline, Context API usage, concurrent features, Server Components, accessibility, and React 18 best practices. Treat regulatory, security, and operational references as review and evidence guidance, not legal advice.

## Goal and behavioral contract

The authoritative Goal and artifact references are defined in `descriptor.yaml`. Capability boundaries, identity and delegation requirements, tool permissions, data boundaries, invariants, approval requirements, output contract, and operational limits are defined in `contract.yaml`. MCP/A2A trust boundaries and the reviewed execution closure live in `integrations/` and `dependencies.yaml`; ASPS and assurance requirements live in `assurance.yaml`.

Treat those declarations as mandatory execution constraints. `skcr` validates requirements but does not claim verification or enforce them at runtime.

## When to use

- React best practices decisions, controls, or operating practices need independent review.
- A change affects React best practices artifacts such as React component and JSX, hook implementation and dependency array, Context or state management definition, React.memo or useMemo or useCallback usage, React Server Component boundary, accessibility attribute and ARIA usage in JSX.
- The user needs evidence-oriented findings for risks such as stale closure in useEffect dependency array causing incorrect behaviour, unnecessary re-render from object or array literal created inline in JSX, useEffect used for data fetching without cleanup or cancellation, Context triggering full subtree re-render on every value change, React.memo or useMemo applied without profiling confirming render cost, key prop using array index causing DOM reconciliation errors on list reorder.
- Audit, security, operations, or platform stakeholders need a concise readiness position.
- Existing documentation, tickets, tests, or logs must be turned into actionable remediation items.

## Operating model

1. Identify the relevant React best practices artifacts, owners, systems, environments, and review boundary.
2. Compare the available artifacts against expected signals such as React DevTools Profiler flame graph, ESLint react-hooks plugin exhaustive-deps warning, render count measurement with Why Did You Render, bundle analysis with Webpack Bundle Analyzer or Vite rollup output, Accessibility audit with axe-core or React Testing Library queries, React Server Component serialisation error or client boundary audit.
3. Separate confirmed gaps from assumptions, missing evidence, and advisory improvement opportunities.
4. Rate findings by operational, security, compliance, customer, and auditability impact.
5. Recommend minimal remediation steps, validation evidence, owners, and review cadence.

## Spec-Driven Change Context

- Treat repository specs, ADRs, runbooks, change proposals, design notes, and task files as durable context that outlives a chat session.
- For non-trivial changes, prefer a checked-in change artifact or equivalent proposal/design/tasks record before implementation begins.
- Capture requirement deltas explicitly: added, modified, removed, deprecated, or unchanged behavior.
- Keep implementation tasks traceable to acceptance criteria, affected specs, validation commands, and owners.
- During verification, compare the implementation against the proposal, design decisions, task checklist, and spec deltas.
- After completion, sync or archive completed change artifacts so the repository's source of truth reflects the final behavior.
- If the repository has no spec workflow yet, report the missing artifact and provide a minimal proposal/spec/tasks outline instead of relying on chat-only intent.

## Skill-Specific Review Scope

- Primary artifacts: React component and JSX, hook implementation and dependency array, Context or state management definition, React.memo or useMemo or useCallback usage, React Server Component boundary, accessibility attribute and ARIA usage in JSX.
- Risk themes: stale closure in useEffect dependency array causing incorrect behaviour, unnecessary re-render from object or array literal created inline in JSX, useEffect used for data fetching without cleanup or cancellation, Context triggering full subtree re-render on every value change, React.memo or useMemo applied without profiling confirming render cost, key prop using array index causing DOM reconciliation errors on list reorder.
- Evidence signals: React DevTools Profiler flame graph, ESLint react-hooks plugin exhaustive-deps warning, render count measurement with Why Did You Render, bundle analysis with Webpack Bundle Analyzer or Vite rollup output, Accessibility audit with axe-core or React Testing Library queries, React Server Component serialisation error or client boundary audit.
- Ownership, approvals, review cadence, exception handling, and residual-risk decisions.
- Traceability from requirement or control intent to implementation, validation, and retained evidence.

## Skill-Specific Checklist

- [ ] Confirm the review boundary covers the right React best practices systems, teams, and environments.
- [ ] Inventory and inspect the current React component and JSX.
- [ ] Check whether hook implementation and dependency array is current, approved, versioned, and owned.
- [ ] Verify that Context or state management definition has test, ticket, log, or approval support.
- [ ] Look for stale closure in useEffect dependency array causing incorrect behaviour and record concrete repository or process evidence.
- [ ] Look for unnecessary re-render from object or array literal created inline in JSX and identify affected assets, services, or stakeholders.
- [ ] Look for useEffect used for data fetching without cleanup or cancellation and classify the operational or audit impact.
- [ ] Use React DevTools Profiler flame graph to validate that the control or practice is operating.
- [ ] Use ESLint react-hooks plugin exhaustive-deps warning to confirm ownership, timing, and reproducibility.
- [ ] Check exception, risk-acceptance, and expiry handling for React best practices.
- [ ] Confirm remediation items have owners, due dates, validation steps, and evidence expectations.
- [ ] Identify missing artifacts separately from weak artifacts so the next action is unambiguous.
- [ ] Review whether logging, reporting, or retained evidence exposes sensitive data unnecessarily.

## Decision Rules

- If React component and JSX is missing for a critical service, raise at least a high-severity readiness gap.
- If ESLint react-hooks plugin exhaustive-deps warning cannot be tied to an owner and approval, treat the outcome as unauditable until corrected.
- If React.memo or useMemo or useCallback usage is present but expired or untested, require validation before accepting residual risk.
- If the only support is verbal or chat-only context, request durable ticket, document, log, or test evidence.
- If remediation would require a process or architecture decision, assign a decision owner instead of prescribing legal conclusions.
- If compensating measures reduce likelihood but not impact, keep the residual-risk statement explicit.

## Finding Categories

- Missing or stale React best practices artifact.
- Unclear ownership, approval, review cadence, or accountability.
- Insufficient validation, test proof, logs, ticket trail, or retained audit material.
- Unreviewed exception, residual risk, expiry, or compensating measure.
- Policy, architecture, operational, or platform implementation drift.
- Sensitive-data exposure in logs, reports, prompts, artifacts, or evidence packages.

## Severity Guidance

- Critical: a gap in React best practices creates immediate outage, data-loss, privilege, regulatory-reporting, or irreversible business risk.
- High: React component and JSX is missing, unowned, untested, or unauditable for a critical service or material change.
- Medium: hook implementation and dependency array exists but is stale, incomplete, inconsistently enforced, or weakly evidenced.
- Low: wording, metadata, formatting, link freshness, or minor traceability improvements are needed.

## DevSecOps Guardrails

- Do not read secrets, `.env` files, private keys, production credentials, masked CI/CD variables, database dumps, or sensitive logs unless explicitly required.
- Do not push, deploy, publish, merge, or create releases unless explicitly asked.
- Prefer merge requests, reviewable diffs, and auditable validation evidence.
- Prefer least privilege, minimal changes, and explicit rollback notes.
- Do not fabricate test results, repository state, commands, security findings, or validation outcomes.
- Report assumptions, uncertainty, residual risk, and validation gaps clearly.

## Output Requirements

- Findings ordered by severity with affected React best practices artifacts and evidence references.
- Coverage note for reviewed artifacts: React component and JSX, hook implementation and dependency array, Context or state management definition, React.memo or useMemo or useCallback usage, React Server Component boundary, accessibility attribute and ARIA usage in JSX.
- Risk note covering relevant themes: stale closure in useEffect dependency array causing incorrect behaviour, unnecessary re-render from object or array literal created inline in JSX, useEffect used for data fetching without cleanup or cancellation, Context triggering full subtree re-render on every value change, React.memo or useMemo applied without profiling confirming render cost, key prop using array index causing DOM reconciliation errors on list reorder.
- Evidence request list using expected signals: React DevTools Profiler flame graph, ESLint react-hooks plugin exhaustive-deps warning, render count measurement with Why Did You Render, bundle analysis with Webpack Bundle Analyzer or Vite rollup output, Accessibility audit with axe-core or React Testing Library queries, React Server Component serialisation error or client boundary audit.
- Deliverables or updates needed: React code review findings, hooks correctness and dependency array recommendations, re-render and memoisation optimisation notes, Context and state management findings, Server Component boundary assessment, accessibility gap list.
- Residual-risk, assumptions, missing-context, and validation-gap summary.

## Acceptance Criteria

- Relevant React best practices artifacts are identified, current, owned, and versioned where applicable.
- Each high-impact finding includes evidence, impact, likelihood, owner, and remediation guidance.
- Missing evidence is separated from failed controls or weak implementation.
- Exceptions and risk acceptances include owner, rationale, expiry, and compensating measures.
- Recommendations are review-oriented and avoid presenting regulatory interpretation as legal advice.
- Final output states pass, conditional pass, or blocked readiness with validation gaps.

## Anti-Patterns

- Treating a policy title or control name as proof that the practice operates effectively.
- Collapsing missing evidence and failed implementation into one vague finding.
- Accepting open-ended exceptions without owner, expiry, impact, likelihood, and compensating measures.
- Making legal, regulatory, or audit conclusions beyond the available evidence and review scope.
- Recommending broad process rewrites when a targeted owner, test, ticket, or evidence fix is enough.
- Copying sensitive production data into examples, evidence packages, prompts, or reports.

## Changelog

### 0.1.0 - 2026-09-09

- Initial generated production-ready SDLC / DevSecOps skill.
