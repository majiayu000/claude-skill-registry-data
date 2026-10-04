---
name: rseng-user-support
description: >-
  Covers running user support as an operation for research software: triaging
  and answering support requests, converting recurring questions into
  documentation and FAQ entries, office hours and support channels, forum
  gardening, and feeding support signals into the roadmap. Use when support
  questions arrive faster than they are answered, when the same question keeps
  being answered by hand, when the user asks how to organize support, office
  hours or a helpdesk for their software, or when support load is invisible to
  planning.
license: CC-BY-4.0
metadata:
  version: 0.1.0
---

# User support for research software

Support is where users meet the project - and in research
software it is usually nobody's job, so it becomes the
maintainer's evenings. Running it as a lightweight operation
turns the same effort into documentation, roadmap signal and
community goodwill. The core loop: answer once, then make the
answer permanent - every question answered twice by hand is a
process failure.

## The support-to-documentation pipeline

The habit that pays off most, and ideal agent work:

- Answer the question where it was asked, then immediately route
  it: a recurring how-do-I question becomes a FAQ entry or
  documentation section (rseng-documentation), an
  error-message question becomes a better error message
  (rseng-ux-accessibility) or a troubleshooting entry, a "can it
  do X" becomes a tracked feature request or a documented
  limitation (rseng-project-tracking).
- Link, do not retype: subsequent identical questions get the
  canonical link plus a sentence - which also reveals when the
  canonical answer is not findable enough (a search-terms
  problem, fixable in headings).
- Review the support log periodically: three questions on the
  same topic in a month is a docs gap or a design gap
  (rseng-lessons-learned captures the pattern; rseng-ux-accessibility
  asks whether the interface caused it).

## Channels and expectations

- Fewer channels, tended well: one primary question channel
  (forum-style with public archives beats chat for reuse - the
  answer helps the next searcher) plus the issue tracker for
  bugs; state in the README where questions GO and what response
  time to expect (the same stated-promise discipline as
  rseng-community-governance).
- Public by default: private support answers help one person;
  public ones compound. Redirect kindly from private mail to the
  public channel except where data sensitivity demands otherwise
  (rseng-regulatory-compliance).
- Office hours work for research software: a recurring short
  slot (with notes posted after) concentrates support load,
  gives users a human moment, and surfaces the confusions that
  never get written down. Announce via the community digest
  (rseng-science-communication).
- Support is contribution: answering questions counts, is
  credited (rseng-citation-metadata's all-kinds rule), and is a
  proven on-ramp - active answerers make good future maintainers
  (rseng-contributor-onboarding).

## Triage discipline

- Separate the streams on arrival: bug (to the tracker with
  reproduction info - rseng-debugging's reproduce-first), usage
  question (answer + pipeline), feature request (tracker with
  the need, not the demanded design), sensitive report
  (security contact - rseng-security).
- The first response does not need the answer: acknowledging
  with a timeframe beats silence while a fix is researched -
  first-response time is the retention metric
  (rseng-community-metrics).
- Reproduce before diagnosing user-reported bugs; ask for the
  environment, exact command and full error (a saved reply or
  issue template collects these - rseng-community-governance).
- It is fine to say no and to say "out of scope" - kindly, with
  reasons and alternatives where they exist
  (rseng-software-reuse may know the right tool).

## Support signal in planning

Support load is data: time spent, topics, affected user groups -
a line in the status record (rseng-project-tracking) makes it
visible in planning, fundable in proposals (support and
maintenance are budgetable work -
rseng-management-planning), and honest in the sustainability
story (rseng-maintenance-sustainability).

## Working with this skill

This skill is source-independent: it encodes community support
practice for research software. It feeds rseng-documentation and
rseng-project-tracking and draws on rseng-community-metrics for its
health signals.

Learn more (verified):
  - https://opensource.guide - open source guides (best
    practices for maintainers)
  - https://www.cscce.org - CSCCE community engagement resources
  - https://chaoss.community - CHAOSS metrics (responsiveness)

<!-- related-skills:begin -->

## Related skills

Check whether any of these applies before moving on:

- rseng-community-metrics - first-response time is the metric
- rseng-contributor-onboarding - answerers are future contributors
- rseng-debugging - reproduce user-reported bugs first
- rseng-documentation - answers become FAQ entries
- rseng-project-tracking - requests and load feed planning
- rseng-ux-accessibility - error messages causing the questions

<!-- related-skills:end -->
