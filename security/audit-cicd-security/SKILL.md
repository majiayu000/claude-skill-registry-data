---
name: audit-cicd-security
description: Audit repository CI/CD pipelines for security risks when explicitly asked for pipeline review, fork/MR privilege flows, deploy/publish gates, cache or artifact poisoning, runner isolation, credential exposure, or supply-chain components; apply confirmed Critical/High fixes only after explicit user approval.
---

# Audit CI/CD Security

## Operating mode
- Read-only audit. No file edits, no pipeline runs, no secret retrieval/decode, no publish/deploy, no remote settings changes.
- Do not execute contributor-controlled scripts or config.
- Proposed patches are required in findings; applying confirmed Critical/High fixes requires explicit approval.
- Remote actions (runs/deploys/publishes/releases/secret changes/settings) require separate approval.

## Discovery scope
- Inspect all CI/CD-relevant files and transitive includes/templates/components/actions/plugins/orbs/tasks and all invoked scripts reached by workflow references.
- If an include/component is unavailable or remote, mark it as `unknown` and keep findings `unknown`.
- Never execute contributor-controlled code during discovery.

## Threat model
- Attacker controls fork/branch content, metadata, refs, and submitted inputs.
- Caches, artifacts, and workspaces are transfer mechanisms, not trust boundaries.
- Any lower-to-higher trust object transfer is untrusted until producer identity, provenance, and integrity are verified.
- Confirm cache/artifact/workspace poisoning only when a lower-trust writer and higher-trust consumer share the same object and the consumer lacks producer identity/provenance/integrity verification.
- A broad restore/fallback cache key is evidence to investigate; it is not itself confirmed vulnerability.
- Include checks for trigger chains (comment/reuse/dispatch/manual), credential reach, self-hosted/persistent runner isolation, mutable components, and privileged deployment paths.
- Mutable third-party refs are a confirmed supply-chain weakness, with severity/exploitability tied to actual execution privilege and controls.

## Required output
- Verdict exactly one of:
  - `SAFE AGAINST THIS THREAT MODEL`
  - `CONDITIONALLY SAFE`
  - `UNSAFE`
- Pipeline/trust inventory by provider and execution path.
- Findings with exact file/line and fields:
  - severity (`Critical|High|Medium|Low`)
  - platform/trigger/boundary
  - object/storage
  - `credential or capability at risk`
  - attacker input
  - exploit path
  - protection analysis
  - remediation (minimal)
  - evidence status (`confirmed` or `unknown`)
- Cache/artifact/workspace access matrix.
- Credential-to-storage trace using names only.
- Required patch proposals for each confirmed actionable item.
- Validation plan for static checks; apply only after approval.
- Validate files/lines for every claim before reporting; do not cite paths not present or normalize to non-existent line context.
- Do not mark unknown as confirmed.

## Remediation validation
- Use non-executing syntax/static parser checks only.
- Do not run repository-controlled scripts, builds, tests, or package commands unless user separately authorizes execution after review of the proposed code path.

## Provider routing
Load full matching refs.
- If provider is unknown or unsupported, now and without pausing, web-search official docs for trusted triggers/forks, secrets/tokens, transfer objects, components, runners, and deployment gates.
- Continue with provider-neutral logic and classify only provider-confirmed behavior as confirmed.
