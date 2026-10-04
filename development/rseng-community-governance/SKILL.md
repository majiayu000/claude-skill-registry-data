---
name: rseng-community-governance
description: >-
  Covers building and governing a community around research software:
  CONTRIBUTING guides, codes of conduct, governance models and
  decision-making, contributor recognition policy, issue and discussion
  hygiene, and handing over or sharing maintainership. Use when a project
  wants external contributors, when the user asks for a CONTRIBUTING.md, code
  of conduct or governance document, when maintainer burnout or bus-factor
  risks come up, or when a project is moving from single-author to team or
  community ownership. The contributor funnel and good-first-issue curation
  live in rseng-contributor-onboarding; health measurement in
  rseng-community-metrics; support operations in rseng-user-support.
license: CC-BY-4.0
metadata:
  version: 0.2.0
---

# Community and governance for research software

Most research software dies with its author's contract. A community -
even a small one - is the strongest sustainability mechanism a
project has (rseng-maintenance-sustainability covers the technical
side; this skill covers the human side). Governance is not
bureaucracy: it is writing down who decides what, so contributors can
act without waiting and maintainers can step back without collapse.

## The contribution surface

Make contributing possible before promoting it:

- CONTRIBUTING.md: how to set up a dev environment
  (rseng-reproducible-environments), run tests (rseng-testing), propose
  changes (rseng-version-control-review), and what kinds of
  contribution are welcome (docs, examples and issue triage count).
- Code of conduct: adopt the Contributor Covenant rather than
  writing one; name real enforcement contacts - an unenforceable
  CoC is worse than none.
- Issue templates and labels: a good-first-issue label with genuinely
  scoped starter tasks is the single best onboarding tool.
- Respond to first-time contributors fast and kindly; the first
  interaction decides whether there is a second.
- Name the communication channels: where questions go (discussions,
  a chat channel, a mailing list), stated in the README and
  CONTRIBUTING - an active, discoverable channel is itself a
  measured community-health indicator; one well-tended channel
  beats three dead ones.
- Define a response timeframe and say it out loud ("issues get a
  first response within a week"): a stated expectation both
  reassures contributors and is checkable - response-within-a-
  defined-timeframe is how community health gets assessed from
  the outside. Pick a promise the maintainers can keep.

## Governance, sized to the project

Write down the smallest true answer to "who decides":

- Single maintainer: say so ("BDFL-style; decisions by @name") -
  honesty beats pretense of process.
- Small team: document maintainer roles, how consensus is reached,
  and what happens on disagreement.
- Community-scale: consider a lightweight governance doc covering
  roles, decision process, and how new maintainers are added -
  opensource.guide's leadership-and-governance section catalogs
  proven patterns.

Contribution and recognition policy: state how contributors are
credited - AUTHORS/CONTRIBUTORS file, changelog mentions, and
citation metadata for substantial contributions
(rseng-citation-metadata). Credit is the currency research
contributors are paid in; be generous and systematic.

## Onboarding and the bus factor

- Capture maintainer knowledge in docs as it is used: release
  runbooks (rseng-publishing-releasing), triage guidelines,
  architecture notes (rseng-documentation). If only one person can do
  a task, that task needs a document.
- Rotate responsibilities when there are two or more maintainers;
  the second person on releases halves the bus-factor risk.
- Handover: when a maintainer leaves, announce it, transfer forge
  permissions and registry ownership explicitly, and record the
  change - abandoned-looking ownership blocks both contributors and
  security response (rseng-security).

## The wider community toolkit

Measurement, support and onboarding each have their own skill:
community health metrics (rseng-community-metrics), support operations
and the answer-once pipeline (rseng-user-support), and the contributor
funnel from first issue to regular (rseng-contributor-onboarding) -
this skill owns the rules and structures they operate within.

## Sustaining participation

- Roadmap visibly (even a pinned issue): contributors invest where
  direction is clear (rseng-management-planning).
- Thank and release often: shipped contributions retain contributors;
  ones stuck in review for months lose them.
- Watch for burnout signals in maintainers - unanswered issues and
  guilt-driven replies - and respond by narrowing scope honestly
  (declaring feature-freeze or maintenance-mode is legitimate
  governance).

## Working with this skill

This skill is source-independent: its authority is the community
guidance linked below.

Learn more (verified):
  - https://opensource.guide - GitHub's open source guides
    (building community, leadership and governance)
  - https://www.contributor-covenant.org - the Contributor Covenant
  - https://www.software.ac.uk/guide/starting-community-taking-your-software-world -
    SSI guide on starting a community

<!-- related-skills:begin -->

## Related skills

Check whether any of these applies before moving on:

- rseng-citation-metadata - systematic contributor credit
- rseng-community-metrics - measures the stated promises
- rseng-contributor-onboarding - funnel and first-issue curation
- rseng-maintenance-sustainability - technical side of sustainability
- rseng-security - ownership handover unblocks security response
- rseng-user-support - support channel operations

<!-- related-skills:end -->
