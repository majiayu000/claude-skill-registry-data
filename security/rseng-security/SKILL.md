---
name: rseng-security
description: >-
  Covers securing research software and its supply chain: secrets and
  sensitive-file hygiene (env files, keys, credentials and the never-commit
  file catalog) with leak response, dependency vulnerability scanning and
  pinning, OpenSSF Scorecard and Best Practices badge, SLSA provenance levels,
  SBOMs, signed releases and repository hardening. Use PROACTIVELY when
  setting up CI or releases, when an API key, password, credential or token
  is committed or appears in code or history, when the user asks how secure
  their project or dependencies are, or mentions Scorecard, SLSA, SBOM, CVEs
  or secret scanning. For the agent itself see rseng-agent-security; for GDPR
  and personal-data obligations see rseng-regulatory-compliance; for
  sensitive-data storage practice see rseng-data-management.
license: CC-BY-4.0
metadata:
  version: 0.2.0
---

# Security for research software

Research software is unusually exposed: long-lived unmaintained
dependencies, credentials for shared clusters and data services, and
code that outlives its authors. A 2025 study scoring 3,248 research
repositories with OpenSSF Scorecard found an average of 3.5/10 - the
gap is the norm, not the exception. Security here is mostly hygiene,
not cryptography: a handful of repeatable practices prevent the
common failures.

## Secrets and sensitive files (the non-negotiable)

- Never commit credentials, tokens, private keys or connection
  strings - not even briefly; git history is forever and forges cache
  aggressively.
- Know the file catalog that never enters version control: .env and
  environment files, private keys and certificates (id_rsa, *.pem,
  *.p12), cloud and service credentials (service-account JSONs,
  kubeconfig, .aws/, .netrc), API token files, database dumps with
  real records, browser/session cookies, and instrument or license
  files bearing embedded keys. Some of these should not even sit in
  the working tree of a shared or synced project directory - a
  credential does not belong next to the code that uses it.
- AI agent working directories join the catalog: .claude/,
  .agents/, .cursor/, .codex/, .gemini/, .github/copilot* holding
  local settings, and agent session records (histories,
  .rseng-agent-skills-* worklogs, .mcp.json with server credentials) can
  carry tokens, absolute paths and private prompt history. Gitignore
  them from day one in every generated project; team-shared agent
  config that IS meant to be committed (a project settings.json or
  instructions file) should be added back explicitly, not swept in
  by default.
- Guard rails BEFORE the first secret exists: .gitignore entries for
  the catalog above from day one (the scaffolding template ships
  them - rseng-project-scaffolding), a secret scanner (gitleaks) in
  pre-commit and CI, and a review habit of reading `git status`
  before `git add` - the classic leak is `git add .` sweeping a
  stray file in.
- Configuration via environment variables or untracked local files;
  document required variables in the README with dummy values, and
  ship a committed `.env.example` with placeholders instead of the
  real thing.
- Personal and sensitive DATA files follow the same rule with their
  own escort: never committed, stored where the steward says, with
  synthetic samples in the repo (rseng-data-management,
  rseng-regulatory-compliance).
- If a secret lands in history: revoke and rotate it FIRST (assume it
  is compromised the moment it is pushed), then clean history if the
  repository is private enough for that to matter. Rotation is the
  fix; history rewriting is cosmetics.
- Sweep periodically, not just at commit time: scan the existing
  history and tree (gitleaks detects both) during the milestone
  review (rseng-code-review) - guards added today do not clear
  yesterday's leak.

## Dependencies and the supply chain

- Pin dependencies with lockfiles (rseng-reproducible-environments) -
  reproducibility and supply-chain safety are the same mechanism.
- Turn on dependency vulnerability scanning where the forge provides
  it (e.g. dependabot/renovate style updates plus advisory alerts);
  triage rather than auto-merge on research-critical code paths.
- Evaluate before adopting: maintenance signals, release cadence and
  known advisories are part of choosing a dependency
  (rseng-dependency-management owns the full intake vetting;
  rseng-software-reuse finds the candidates).
- Generate an SBOM (software bill of materials) at release time when
  the project is infrastructure others depend on; it makes "are we
  affected by CVE X" answerable in minutes.

## Assess with OpenSSF Scorecard

Scorecard runs read-only checks (branch protection, token
permissions, pinned workflows, fuzzing, dangerous CI patterns...) and
scores 0-10. Use it like FAIRGuard (rseng-fairguard) is used for FAIR:
assess, read findings, fix what matters for the project's tier,
re-run and report the delta. The OpenSSF Best Practices badge is the
self-assessment counterpart worth adopting at maturity.

CI hardening basics an agent should apply by default:

- Least-privilege CI tokens (read-only unless the job publishes).
- Pin third-party CI actions/steps to commit SHAs, not floating tags.
- Never echo secrets into logs; mask and scope them per job.
- Protect the default branch: reviews required, force-push disabled
  (rseng-version-control-review).

## Fuzzing and vulnerability response

- Fuzzing feeds malformed inputs at scale to find crashes and memory
  errors; it earns its setup cost when the project contains
  memory-unsafe code (C/C++/Fortran extensions are common in research
  stacks) or parses untrusted input. OSS-Fuzz runs it continuously
  for accepted open source projects; language-level fuzzers work in
  CI for smaller scopes. For pure high-level code, property-based
  testing delivers the same input-hostility cheaper (rseng-testing).
- Have a response path before the first report: a security contact
  (SECURITY.md), triage of reported or scanner-found vulnerabilities
  by severity, fixes for critical ones promptly released and noted in
  the changelog (rseng-publishing-releasing) - "no known critical
  vulnerabilities outstanding" is an explicit quality indicator, and
  it is about response speed, not perfection.

## Provenance and releases

SLSA levels describe how trustworthy a build is (source-verified,
build-service, provenance-attested). Practical staircase for
research software: reproducible scripted builds, then CI-only
releases with provenance attestation, then signed artifacts.
Publishing through a registry with provenance support
(rseng-publishing-releasing) gets much of this for free.

## Compliance context

Funders increasingly mandate research-security practices (US
agencies made security training mandatory in 2025). When an
institutional policy exists, implement it rather than improvising;
sensitive-data handling questions route to the data steward
(rseng-data-management).

## Acting on findings

Route fixes to the matching skill: CI changes (rseng-ci-cd), release
process (rseng-publishing-releasing), dependency updates
(rseng-dependency-management for the update regime,
rseng-maintenance-sustainability for cadence), review rules
(rseng-version-control-review). Record AI-assisted security work in
aidecl.yaml (rseng-ai-declaration) - provenance matters most exactly
here.

## Working with this skill

This skill is source-independent: its authority is the OpenSSF and
SLSA documentation and the research-software security literature
linked below.

Learn more (verified):
  - https://github.com/ossf/scorecard - OpenSSF Scorecard
  - https://www.bestpractices.dev - OpenSSF Best Practices badge
  - https://slsa.dev - SLSA supply-chain levels
  - https://github.com/gitleaks/gitleaks - secret scanning
  - https://cyclonedx.org - CycloneDX SBOM standard
  - https://github.com/google/oss-fuzz - OSS-Fuzz continuous fuzzing
  - https://arxiv.org/abs/2508.03856 - Scorecard study of 3,248
    research repositories

<!-- related-skills:begin -->

## Related skills

Check whether any of these applies before moving on:

- rseng-agent-security - least-privilege applied to the agent
- rseng-ci-cd - hardening CI tokens and workflows
- rseng-dependency-management - vetting and updating dependencies
- rseng-publishing-releasing - signed releases, SBOMs, provenance
- rseng-regulatory-compliance - personal data raises legal duties
- rseng-reproducible-environments - lockfiles pin the supply chain

<!-- related-skills:end -->
