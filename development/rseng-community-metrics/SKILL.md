---
name: rseng-community-metrics
description: >-
  Covers measuring community health with CHAOSS-style metrics: contributor
  growth and retention, bus factor, first-response and review latency, the
  casual-to-regular contributor conversion funnel, and organizational
  diversity - computed from forge data, interpreted against project stage, and
  turned into community actions rather than vanity dashboards. Use when the
  user asks how healthy their community is, wants contributor or
  responsiveness statistics, mentions CHAOSS or community metrics, prepares a
  sustainability report or grant renewal needing community evidence, or when
  community trends (rising latency, shrinking contributor base) should be
  checked rather than felt.
license: CC-BY-4.0
metadata:
  version: 0.1.0
---

# Community health metrics

A community's health can be measured, and the CHAOSS project has
standardized how: metrics for growth, responsiveness, retention
and risk that turn "the community feels quiet lately" into
checkable numbers. The same discipline as rseng-software-metrics
applies unchanged: metrics LOCATE community problems, humans judge
them; trends beat snapshots; and every metric can be gamed, so
keep them plural and tie them to actions.

## The metrics that matter, and their sources

Nearly everything comes from data the forge already has - git
history, issues, PRs, reviews - all computable by an agent:

- Growth and activity: new contributors per period, active
  contributors (authored, reviewed, triaged or commented - count
  ALL contribution kinds, the rseng-citation-metadata lesson),
  contribution volume by type.
- Responsiveness: time to first response on issues and PRs
  (the promise rseng-community-governance made checkable), review
  latency, time to merge or close. First-response time is the
  single best predictor of whether a first-time contributor
  returns.
- Retention and the funnel: how many first-time contributors make
  a second contribution (the conversion rate), casual-to-regular
  progression, time since last activity for previously regular
  contributors (quiet departures are findable before they are
  final).
- Risk: bus factor (what fraction of recent work concentrates in
  how few people - the elephant-factor framing), single-maintainer
  subsystems, organizational concentration when affiliation is
  known.

Compute from `git log`, the forge API and the tracker; CHAOSS
tooling (Augur/GrimoireLab-class) automates it at scale, but a
scripted quarterly pass covers most research projects (a natural
milestone-review input - rseng-code-review).

## Interpreting honestly

- Stage calibrates everything (rseng-quality-framework's tiering
  instinct): a two-person analysis-code repo with bus factor 1 is
  normal; infrastructure with bus factor 1 is a risk register
  entry. Compare the project against its own history first,
  peers second, absolutes never.
- Watch trends, alert on inflections: slowly rising first-response
  time is load or fading attention - both actionable; a cliff
  after a maintainer change is a succession problem
  (rseng-community-governance).
- Name the denominator: "12 new contributors" means nothing
  without the period and the definition; publish definitions with
  numbers so the metric survives scrutiny
  (rseng-research-integrity's spirit applied to community claims).
- Diversity and affiliation metrics involve personal data: use
  public information, aggregate, and route anything finer to
  policy (rseng-regulatory-compliance).

## From numbers to actions

Every reported metric ends with a routing, or it is a vanity
dashboard:

- Slow first response -> triage rotation and a stated timeframe
  (rseng-community-governance, rseng-project-tracking).
- Poor first-to-second contributor conversion -> onboarding fixes
  (rseng-contributor-onboarding owns the funnel).
- Support load rising in issues -> FAQ and docs routing
  (rseng-user-support, rseng-documentation).
- Bus factor concentration -> knowledge spreading: rotation,
  documentation, succession planning
  (rseng-maintenance-sustainability).
- Good numbers -> tell the community; measured health is a
  celebration and a grant-report asset
  (rseng-science-communication, rseng-management-planning).

Report metrics to the community transparently on a cadence - a
short health section in the periodic digest
(rseng-project-tracking's high-level log) normalizes measurement
and builds trust; surprise metrics deployed in conflict destroy
it.

## Working with this skill

This skill is source-independent: its authority is the CHAOSS
metrics definitions and community-health practice linked below.
It is the measurement arm of rseng-community-governance, the
community analogue of rseng-software-metrics.

Learn more (verified):
  - https://chaoss.community - CHAOSS community health metrics
  - https://www.cscce.org - Center for Scientific Collaboration
    and Community Engagement
  - https://opensource.guide - open source guides (community
    sections)

<!-- related-skills:begin -->

## Related skills

Check whether any of these applies before moving on:

- rseng-community-governance - metrics route to governance actions
- rseng-contributor-onboarding - fixes the funnel leaks found
- rseng-maintenance-sustainability - bus-factor risk response
- rseng-management-planning - grant reports need community evidence
- rseng-software-metrics - same measurement discipline, code side
- rseng-user-support - support load is a signal

<!-- related-skills:end -->
