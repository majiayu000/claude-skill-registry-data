---
name: security-triage-finding
description: |-
  Use when the user supplies existing security findings or vulnerability reports — SARIF results, CVE/GHSA or advisory text, scanner tickets, bug bounty reports, or finding artifacts — and wants static repo-impact triage. Do not use for discovery, duplicate-bug triage, validation, or fixes.
metadata:
  short-description: Triage supplied security findings from scanners, advisories, and reports
---

# Triage Finding

## Objective

Triage existing security findings against the current repository using static code evidence.
Return one evidence-backed verdict per supplied finding: `confirmed`, `not_actionable`, or `needs_review`.
For `confirmed` and `needs_review` findings, also assign a discrete exploitability stack rank inside that verdict's own queue.

This skill is for backlog burn-down.
It starts from findings the user already has, such as SARIF results, CVEs, advisories, scanner tickets, bug bounty reports, or security-scan finding artifacts.
It is not a repository-wide scan, dynamic validation run, fix implementation, dashboard, or queue manager.

## Backlog Burn-Down Scope

Treat multiple supplied findings as one backlog-reduction problem, not as a set of unrelated one-off triages.
The goal is to turn noisy existing finding sources into a ranked, evidence-backed action queue while preserving one result per input for auditability and reporting.

For now, run the workflow inline in the current thread, but structure the work like a backlog pipeline:

- Build the normalized triage item list for the whole supplied or imported collection before assigning verdicts.
  Here, normalize means: assign `triage_item_id`, preserve source ids and references, extract the fields in the Inputs section below, and record missing fields as proof gaps without inventing scanner, severity, remediation, or generated scan fields.
- Triage each normalized item using static evidence and keep one output result per supplied finding.
- Rank the `confirmed` and `needs_review` results as an action queue for backlog burn-down.
- Do not perform deduplication in this skill.
  If duplicate-looking inputs are present, keep one result per supplied finding; deduplication belongs in a separate workflow.
- Do not spawn subagents, use a subagent queue, or use deep triage mode until a future implementation explicitly adds those mechanics.

## Finding Schema Decision

Do not use the completed-scan `findings.json` schema as the canonical data shape for input normalization.

That schema describes completed security-scan output.
It requires generated fields such as `scanId`, `findingId`, `occurrenceId`, fingerprints, severity, remediation, provenance, and at least one location.
Most triage inputs are incomplete external claims, and forcing them into that schema before investigation would require inventing stable IDs, severity, remediation, or locations.

Use the schema only as an optional compatibility source when the user supplies an existing security-scan `findings.json` artifact.
In that case, extract the available fields into the triage normalization record and preserve the original IDs as source identifiers.
The triage result contract is defined in `references/triage-result-contract.md`.

## Static Assessment Guidance

Use the shared static finding assessment reference in `references/static-finding-assessment.md` for the reusable evidence work: source/control/sink tracing, smallest useful evidence search, reachability, boundary inputs, counterevidence, proof gaps, and static confidence.

This skill still owns external finding intake, the backlog triage verdicts, the first-pass no-runtime constraint, and the output contract.

## Missing Input

If no finding is supplied, do not inspect the repository, do not classify a verdict, and do not emit the `security-triage-finding/v0` JSON contract.

Ask the user to provide a finding to triage.
Name the supported formats: SARIF results, CVE/GHSA or advisory descriptions, scanner tickets, bug bounty report snippets, security-scan finding artifacts, or a freeform vulnerability claim.
If useful, ask for the repository path or affected file/component at the same time.

## Inputs

Start by extracting:

- repository path or current working repository
- input id, scanner id, SARIF rule/result id, CVE/GHSA id, ticket id, or security-scan `findingId`/`occurrenceId` when present
- title or short claim
- source type: `sarif`, `cve`, `advisory`, `scanner_ticket`,
  `bug_bounty`, `security_scan_finding`, `freeform`, or `unknown`
- vulnerable component, package, API, file, route, class, function, or service
- claimed attacker-controlled source
- claimed sink or broken security control
- affected version, path, configuration, or deployment surface
- required preconditions and claimed impact
- existing code references, evidence, and counterevidence supplied by the user

Ask a follow-up question only when the repository path or finding claim is too vague to inspect.
Otherwise, inspect the repository and preserve missing fields as proof gaps.

## Repository Security Policy Gate

Before static evidence analysis, check whether the target repository has a `SECURITY.md` file at or above the repository root.
If present, read the repository's `SECURITY.md` before tracing source, control, sink, reachability, or assigning a verdict.

Treat `SECURITY.md` as the primary local source for supported security boundaries, trusted inputs, supported versions, disclosure scope, hardening controls, and out-of-scope surfaces.
Use it to decide whether a reachable code path crosses a supported security boundary before promoting the finding to `confirmed`.
If no `SECURITY.md` is present, record that absence as a proof gap and continue with the next-best local policy evidence.

## Workflow

01. Normalize each supplied finding into a triage item.
    - Assign `triage_item_id` values such as `triage-001`.
    - Preserve external source ids in `input_id`.
    - Do not invent scanner fields, generated scan ids, severity, or
      remediation just to satisfy another schema.
02. Resolve the repository path and git revision when available.
03. Apply the Repository Security Policy Gate.
    - Look for `SECURITY.md` in the target repository before source/control/sink
      tracing or reachability analysis.
    - If present, read it and record the relevant policy basis for supported
      security boundaries, trusted inputs, supported versions, hardening
      controls, and out-of-scope surfaces.
    - If absent, record the absence as a proof gap and continue with available
      product docs, threat models, disclosure policy, and local comments.
    - If `SECURITY.md` and available local product evidence do not establish the
      intended product surface, untrusted input boundary, or trusted
      operator/developer inputs, ask targeted operator-context questions before
      assigning a verdict when the answer would materially affect the result.
04. Follow `references/static-finding-assessment.md` to inspect the smallest relevant static evidence set and record source, control, sink,
    reachability, boundary inputs, counterevidence, proof gaps, and static confidence.
05. Classify the product surface and trust boundary.
    - Identify whether the path is a CLI, library API, hosted service, local
      developer UI, MCP/tooling surface, example/demo, test/fixture, docs,
      generated code, vendored code, or unknown surface.
    - Check package manifests, exports, binary entrypoints, deployment files,
      product docs, `SECURITY.md`, disclosure policy, threat models, and nearby
      comments when they are standard or local to the claim.
    - Record whether the claimed source is untrusted input in the intended
      product model, or trusted operator/developer configuration.
06. Trace the claimed source, control, sink, and reachable path.
    - Treat scanner/advisory prose as a claim, not as proof.
    - Start from the cited code, manifest, version range, or supplied evidence.
    - `confirmed` already requires reachability.
      When claiming reachability, record reachability anchor evidence: the concrete caller, entrypoint, route, command, package export, deployment path, dependency edge, or other repo fact that proves the vulnerable condition is connected to the product surface.
    - Record supporting evidence.
    - Record counterevidence that weakens or defeats the claim.
    - Record unresolved proof gaps instead of smoothing them over.
07. Apply the verdict rules.
08. Assign exploitability stack ranks for `confirmed` and `needs_review`
    findings.
09. For `confirmed` findings, add owner hints after verdicting when local ownership evidence is easy to derive.
10. Build one valid `security-triage-finding/v0` result using the contract in `references/triage-result-contract.md`.
11. Present a concise Markdown summary of the triage results as the final response.
    Include the full `security-triage-finding/v0` JSON contract in a fenced block when the user asks for the raw result or wants to copy it.

## Surface and Boundary Gate

Before assigning `confirmed`, classify the finding's intended product surface and trust boundary.

Inspect the smallest available evidence for:

- shipped or runtime surfaces, such as package manifests, exports, binary entrypoints, server routes, deploy configs, container/build files, public API docs, or product docs
- non-product or trusted surfaces, such as examples, tests, fixtures, docs snippets, local-only developer tools, generated/vendor code, internal harnesses, CLI configs, plugin/test utilities, or deliberately code-executing extension points
- repository security policy or threat model, such as `SECURITY.md`,
  docs/security, supported-versions docs, disclosure policy, threat models, or comments that define trusted inputs and supported boundaries

A reachable dataflow is not enough. `confirmed` requires both:

1. the vulnerable condition is statically reachable under stated preconditions
2. the source crosses a security boundary that the project appears to support

If the code is reachable only through trusted configuration, local developer interfaces, examples, tests, fixtures, or demo applications, do not mark `confirmed` unless static evidence shows that surface is shipped, deployed, documented for untrusted users, or bypasses a documented hardening/auth boundary.

When the boundary classification is policy-dependent or unclear, prefer `needs_review` and put the ambiguity in proof gaps.

## Verdict Rules

Use `confirmed` only when static evidence connects the vulnerable condition to reachable code under stated preconditions and the source crosses an intended security boundary for a shipped, deployed, or documented product surface.
Dependency or component presence by itself is not enough.

Use `not_actionable` only when static evidence positively defeats the finding, for example:

- the vulnerable package or feature is absent
- the locked version is outside the affected range
- the claimed code path is unreachable in the repository's configuration
- the dangerous sink is protected by a relevant guard, validator, sanitizer, or authorization control
- the scanner claim points at dead, test-only, generated, vendored, or unused code and repository evidence supports that conclusion
- the relevant code is example-only, fixture-only, docs-only, local-only, or not shipped in the affected artifact
- the source is trusted configuration, a CLI argument, a local-only tool input,
  or an intentionally code-executing extension point under the repository's documented security model

Use `needs_review` when evidence is insufficient, ambiguous, runtime-only, policy-dependent, environment-dependent, or blocked by missing repository context.
Prefer `needs_review` over speculative `confirmed` or `not_actionable` verdicts.

## Exploitability Stack Ranking

After verdicting, assign discrete exploitability stack ranks separately for `confirmed` and `needs_review` findings.

- `confirmed` findings use the `confirmed` rank queue and rank labels `P0`,
  `P1`, `P2`, etc. `P0` is the most exploitable confirmed finding in this result set.
- `needs_review` findings use the `needs_review` rank queue and the same `P0`, `P1`, `P2`, etc. labels. `P0` is the highest-exploitability unresolved finding to review first.
- Rank labels intentionally do not encode the verdict queue.
  Use `rank_queue` to distinguish confirmed priorities from needs-review priorities.
- `not_actionable` findings are not stack-ranked; set their rank queue and rank to `null`.

Rank by exploitability, not by scanner severity alone.
Prioritize findings with clearer attacker reachability, lower required privileges, fewer preconditions, more direct source-to-sink control, weaker or absent guards, and more reliable static evidence that the exploit path can be exercised.
Use claimed impact or scanner severity only as a final tiebreaker when exploitability is otherwise equal.

Keep findings in input order in the JSON result.
Use the stack-rank fields to show review/remediation priority instead of reordering the results.

## Owner Hints

For `confirmed` findings only, add a concise owner hint after assigning the verdict and exploitability stack rank when local ownership evidence is easy to derive.

Prefer CODEOWNERS or OWNERS evidence when available.
If ownership is not clear, omit the owner hint rather than guessing.
Owner hints are routing metadata only: do not use ownership to influence verdict, confidence, boundary assessment, or exploitability rank.

The `security-triage-finding/v0` contract does not define a dedicated owner field.
Do not add undocumented fields to the `security-triage-finding/v0` payload.
Put owner-hint text in existing Markdown output, evidence, or recommended-next-step text when it is useful.

## Output Contract

The Markdown result should include:

- finding title or input id
- verdict and confidence
- short rationale
- affected locations, if any
- reachable path, if established
- boundary assessment: product surface, source trust level, policy basis, and whether a supported security boundary is crossed
- exploitability stack rank for `confirmed` and `needs_review` findings
- evidence
- counterevidence
- proof gaps
- owner hint for `confirmed` findings, when available
- recommended next step
- `security-fix-finding` handoff when verdict is `confirmed`

The `security-triage-finding/v0` JSON payload must include:

- `schema_version: "security-triage-finding/v0"`
- repository path and revision when available
- one result object per input finding, in input order
- `source_type` on every finding result, using one of the input source types listed above
- `boundary_assessment` on every finding result, even when fields are unknown
- `exploitability_stack_rank` on every finding result

Default to a concise Markdown summary.
The intended default UX is:

1. generate the valid `security-triage-finding/v0` result internally
2. respond with the concise Markdown summary

Include the fenced JSON block when the user explicitly asks to see or copy the raw result contract.

## Fix-Finding Handoff

For `confirmed` findings, include a concise prompt-ready handoff for `security-fix-finding` with:

- vulnerable source, sink, or broken control
- attacker-controlled input and preconditions
- exact code references
- required security invariant
- recommended fix boundary
- proof gaps that `security-fix-finding` should preserve or validate

Do not invoke `security-fix-finding` unless the user explicitly asks to continue into fixing.

## Hard Rules

- Do not run tests, builds, applications, PoCs, exploit checks, or dynamic validation.
- Do not edit repository files while triaging.
- Do not search for unrelated vulnerabilities.
- Do not claim exhaustive repository coverage.
- Do not claim runtime validation happened.
- Do not mark `confirmed` solely because attacker-influenced data reaches a dangerous sink; first establish the relevant product surface and supported security boundary.
- Do not use deep triage mode unless a future implementation explicitly adds it.
- Do not deduplicate, group, canonicalize, or drop duplicate-looking inputs in this skill; keep one result per supplied finding.
- Do not hide proof gaps or turn missing evidence into confidence.
