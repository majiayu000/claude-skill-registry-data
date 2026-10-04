---
name: rseng-dependency-management
description: >-
  Covers the full lifecycle of third-party dependencies: vetting a library
  before adoption on every axis that matters - suitability, license, trust and
  vulnerabilities including the transitive tree, documentation, maintenance
  and version currency - then keeping dependencies current with lockfiles and
  automated updates, and replacing them when they rot. Use PROACTIVELY
  whenever a new dependency is about to be added, when dependencies are
  outdated or unpinned, when the user asks whether a library is safe or well
  chosen, mentions dependabot/renovate, transitive dependencies or version
  pinning, or when an audit is due. (Finding candidates: rseng-software-reuse;
  deep license analysis: rseng-license-compliance; lockfile mechanics:
  rseng-reproducible-environments.)
license: CC-BY-4.0
metadata:
  version: 0.2.0
---

# Dependency management

Every dependency is a long-term relationship entered in one line
of a requirements file: its bugs become your bugs, its license
binds your distribution, its abandonment becomes your maintenance
burden - and the same is true of everything IT depends on. The
discipline has three phases: vet before adopting, stay current
while depending, and exit deliberately. An agent adding a
dependency without the intake check below is skipping due
diligence on the user's behalf; run it by default and report the
verdicts.

## Intake: vet before adopting

Check every axis, not just the one that motivated the search
(rseng-software-reuse finds candidates; this is the gate they pass
through):

1. Suitability: does it actually solve the need, at the right
   size? A 50MB framework for one function fails this axis;
   prefer the smallest dependency that does the job - or the
   standard library, which needs no vetting.
2. License compliance: identify the license AND the licenses of
   its own dependency tree, and check compatibility with the
   project (rseng-license-compliance owns the analysis; deps.dev
   shows tree-wide licenses in one view). A perfect library under
   an incompatible license is not a candidate.
3. Trust and vulnerabilities - first AND second degree: check
   the package against vulnerability databases (osv.dev covers
   the major ecosystems), and check its TRANSITIVE tree - the
   dependency's dependencies (deps.dev renders the full graph
   with known advisories and OpenSSF Scorecard results). A clean
   package pulling a vulnerable or unmaintained transitive is an
   inherited problem; also weigh supply-chain signals: release
   provenance, maintainer count, typosquatting-adjacent names
   (rseng-security).
4. Documentation quality: real docs (install, API reference,
   examples that run), not just a README stub - undocumented
   dependencies transfer their documentation debt to your users
   and your future self (rseng-documentation's standards as the
   yardstick).
5. Maintenance and currency: recent releases, responsive issue
   tracker, more than one maintainer; check the LATEST version
   and adopt that, never an old version copied from a tutorial
   or an LLM's memory - adopting outdated versions imports
   already-fixed bugs and already-patched vulnerabilities. Verify
   the current version against the registry, not recall - and when
   the technology or domain is unfamiliar, research the ecosystem's
   CURRENT tooling online (official docs, the community's guide)
   before choosing; the state of the art moves faster than training
   data, and requirements.txt-era habits are the canonical example
   of a stale default.
6. Community and continuity: bus factor, governance, whether the
   project has a succession story (rseng-maintenance-sustainability
   reads these signals) - for load-bearing dependencies, an
   abandoned upstream is a foreseeable crisis.

Record the verdict: a one-line entry per adopted dependency in
the decision log (rseng-project-tracking) - what it is for, the
axes checked, any accepted risks. Declined candidates with
reasons are worth a line too (rseng-lessons-learned).

## Staying current: the anti-rot regime

- Pin everything with lockfiles (rseng-reproducible-environments):
  reproducibility and auditability come from the same mechanism -
  you cannot vet what you cannot enumerate.
- Update on a cadence, not on crisis: automated update PRs
  (Dependabot/Renovate class) sized to the project's tier -
  security updates triaged promptly always; routine updates
  batched on a schedule the tests can absorb (rseng-ci-cd runs the
  suite against every bump; that is what makes updating cheap).
- Avoid outdatedness deliberately: track how far behind latest
  each dependency sits and treat growing lag as debt - the
  further behind, the more painful the eventual jump and the
  longer the exposure window to fixed bugs. End-of-life versions
  of runtimes and libraries (endoflife.date tracks them) are
  hard deadlines, not suggestions.
- Read the release notes on major bumps: breaking changes,
  deprecations and behavior changes belong in the update PR's
  description, with the project's affected call sites named
  (rseng-pair-programming's pre-review makes update PRs cheap to
  merge).
- Re-audit periodically: the milestone project review
  (rseng-code-review) re-runs the intake axes over the EXISTING
  tree - licenses change, maintainers leave, advisories land
  after adoption.

## The transitive tree is your tree

- Know what you actually ship: the lockfile enumerates it; an
  SBOM makes it queryable (rseng-security). "We do not use X" is
  only true if nothing in the tree does.
- Minimize depth where choices exist: prefer dependencies with
  small, well-maintained trees; every transitive node is attack
  surface, license surface and rot surface.
- When a transitive is the problem (vulnerable, unmaintained,
  license-incompatible): options in order - update the direct
  dependency that pulls it, override/pin the transitive where
  the ecosystem allows, replace the direct dependency, or
  vendor-and-patch as the documented last resort.

## Exit deliberately

Removal is part of management: when a dependency rots, duplicates
another, or a few stdlib lines would do, remove it - each removal
deletes risk. Migrations off a dependency get the parity-test
treatment (rseng-legacy-code); keeping a known-bad dependency gets
a dated, reasoned entry in the decision log with a revisit date,
never silence.

## Working with this skill

This skill is source-independent: its authority is the ecosystem
services and tool documentation linked below. It gates what
rseng-software-reuse discovers, applies rseng-license-compliance and
rseng-security per axis, and hands the pinning to
rseng-reproducible-environments.

Learn more (verified):
  - https://deps.dev - Open Source Insights: transitive graphs,
    licenses, advisories, Scorecard
  - https://osv.dev - OSV vulnerability database
  - https://endoflife.date - end-of-life dates for runtimes and
    libraries
  - https://docs.github.com/en/code-security/how-tos/secure-your-supply-chain -
    Dependabot automated updates
  - https://docs.renovatebot.com - Renovate automated updates

<!-- related-skills:begin -->

## Related skills

Check whether any of these applies before moving on:

- rseng-ci-cd - tests absorb automated update PRs
- rseng-license-compliance - license axis analysis
- rseng-maintenance-sustainability - upstream bus-factor and succession signals
- rseng-reproducible-environments - pinning and lockfiles
- rseng-security - vulnerabilities, SBOM, supply chain signals
- rseng-software-reuse - candidates entering the intake gate

<!-- related-skills:end -->
