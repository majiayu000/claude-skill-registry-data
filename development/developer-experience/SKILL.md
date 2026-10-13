---
name: developer-experience
description: Audit, measure, and improve developer experience (DX) using the SPACE framework and DORA metrics. Covers inner loop vs. outer loop friction, DX anti-patterns (slow CI, flaky tests, toolchain toil), DX improvement backlog prioritization, developer surveys, build/test benchmarks, and onboarding friction analysis.
triggers:
  - "developer experience"
  - "DX"
  - "inner loop"
  - "slow CI"
  - "developer productivity"
  - "improve developer tooling"
  - "toil"
  - "friction in our workflow"
  - "developer satisfaction"
  - "flaky tests"
  - "build times"
  - "local dev setup"
  - "onboarding friction"
  - "SPACE framework"
audience: engineer, manager
---

# Developer Experience (DX)

## Context

Developer experience is the sum of all interactions a developer has with their tools, processes, systems, and team while building software. Poor DX is not a comfort issue — it is a productivity, quality, and retention issue. Slow CI, flaky tests, painful local setups, and toil-heavy deploys compound across hundreds of developer-hours per week.

DX encompasses two loops:
- **Inner loop**: The tight feedback cycle a developer runs locally — edit → build → test → run. Optimizing this has the highest per-developer ROI.
- **Outer loop**: The collaborative cycle from code commit to production — PR → CI → review → merge → deploy → observe. Optimizing this improves team velocity and release confidence.

Use this skill when:
- Engineers report spending significant time on non-product work
- CI times have grown beyond 10–15 minutes
- Onboarding new engineers to productivity takes more than a week
- Developer satisfaction survey scores are declining
- You want to run a DX audit before starting a platform engineering initiative

---

## Core Frameworks

### The SPACE Framework (Forsgren et al., 2021)

SPACE provides a multidimensional view of developer productivity. No single metric captures it all — use at least one metric per dimension.

| Dimension | What It Measures | Example Metrics |
|---|---|---|
| **S**atisfaction | Developer wellbeing and job satisfaction | Survey NPS, burnout indicators, retention rate |
| **P**erformance | Outcomes of developer work | Defect rate, reliability, customer satisfaction |
| **A**ctivity | Volume of actions and output | PRs merged, deploys per day, code review turnaround |
| **C**ommunication | Effectiveness of collaboration | PR review time, blocked time, meeting load |
| **E**fficiency | Low friction, flow state, minimal interruption | Build time, deploy time, time in flow, context switches |

> **Anti-pattern**: Using only Activity metrics (commits, PRs, lines of code) as a proxy for productivity. This incentivizes the wrong behaviors and ignores quality and wellbeing.

### DORA Metrics (DevOps Research and Assessment)

DORA metrics measure the effectiveness of software delivery:

| Metric | Elite | High | Medium | Low |
|---|---|---|---|---|
| **Deployment frequency** | Multiple/day | 1/day–1/week | 1/week–1/month | < 1/month |
| **Lead time for changes** | < 1 hour | 1 day–1 week | 1 week–1 month | > 6 months |
| **Change failure rate** | < 5% | 5–10% | 10–15% | > 15% |
| **Time to restore service** | < 1 hour | < 1 day | 1 day–1 week | > 1 week |

---

## Inner Loop vs. Outer Loop

### Inner Loop (Local Developer Workflow)

The inner loop is everything a developer does **before pushing code**. It should be sub-second to sub-minute.

```
Edit → Build → Test → Run (repeat)
```

**Target benchmarks:**
| Step | Acceptable | Good | Elite |
|---|---|---|---|
| Hot reload / incremental build | < 5s | < 2s | < 500ms |
| Unit test suite (local) | < 2 min | < 30s | < 10s |
| Local service start | < 60s | < 15s | < 5s |
| Lint + type check | < 60s | < 15s | < 5s |

**Common inner loop pain points:**
- Cold Docker builds that take 5+ minutes
- No incremental compilation (full rebuild on every change)
- Test suite requires external services (DB, S3) that aren't mocked locally
- No local dev environment parity with staging (missing env vars, secrets)
- "Works on my machine" issues from inconsistent toolchain versions

### Outer Loop (Team Workflow)

The outer loop is everything from push to production. Slow outer loops delay feedback and accumulate risk.

```
git push → CI (lint/test/build) → PR review → merge → deploy → observe
```

**Target benchmarks:**
| Step | Acceptable | Good | Elite |
|---|---|---|---|
| CI pipeline total time | < 15 min | < 10 min | < 5 min |
| PR review turnaround | < 24 hours | < 4 hours | < 1 hour |
| Merge to production deploy | < 30 min | < 15 min | < 5 min |
| Deploy rollback time | < 15 min | < 5 min | < 2 min |

**Common outer loop pain points:**
- Flaky tests that require manual re-runs (trust erosion)
- Sequential CI steps that could be parallelized
- Manual approval gates for every deploy (not just production)
- No deploy preview / ephemeral environments for review
- Large PRs with long review cycles (→ batch smaller)

---

## DX Anti-Patterns

### 1. Slow CI
**Symptom**: CI > 15 minutes. Developers stop watching the build; context switch away; forget what they were working on.
**Fix**: Parallelize test jobs. Cache dependencies. Only run affected tests (test impact analysis). Use incremental builds.

### 2. Flaky Tests
**Symptom**: Tests that fail intermittently with no code change. Developers learn to re-run CI blindly.
**Fix**: Quarantine flaky tests immediately (tag + skip + alert). Fix or delete. Track flakiness rate as a metric.

### 3. Poor Local Dev Setup
**Symptom**: Onboarding docs say "ask Sarah" or "it took me 3 days to get running."
**Fix**: Automate setup with a single script (`make setup` or `./scripts/bootstrap.sh`). Test it on clean machines monthly.

### 4. Toil-Heavy Deploys
**Symptom**: Deploying requires manual steps, Slack approvals, editing YAML by hand, or running specific commands in a specific order only the senior engineer knows.
**Fix**: Automate the deploy path entirely. Document the blast radius, add rollback, and make it a one-click or auto-on-merge operation.

### 5. Broken Toolchain
**Symptom**: Engineers have different Node/Python/Go versions. `npm install` fails on some machines. Lockfiles get corrupted.
**Fix**: Pin versions in `.nvmrc`, `.python-version`, `go.mod`. Use Nix, devcontainers, or Docker Compose for reproducible local environments.

### 6. Notification Overload
**Symptom**: Developers are @-mentioned in Slack constantly. PRs ping the wrong people. Alerts fire for things that aren't actionable.
**Fix**: Audit notification surfaces. Use CODEOWNERS for targeted PR assignment. Classify alerts as actionable vs. informational.

### 7. Context Switching from Interruptions
**Symptom**: Engineers can't find "maker time." Average uninterrupted focus block is < 25 minutes.
**Fix**: Introduce focus hours (no meetings 9am–12pm). Batch async communication. Reduce synchronous meeting load.

---

## DX Audit Checklist

Run this audit when starting a DX improvement program. Score each item 0 (broken), 1 (partial), 2 (good).

### Inner Loop Audit

```
INNER LOOP — Edit → Build → Test → Run

Environment Setup
[ ] New developer can be productive in < 1 day                    [ 0 | 1 | 2 ]
[ ] Setup is automated (single command or script)                 [ 0 | 1 | 2 ]
[ ] Toolchain versions are pinned and enforced                    [ 0 | 1 | 2 ]
[ ] Local environment matches staging (parity)                    [ 0 | 1 | 2 ]
[ ] Secrets are accessible without manual steps                   [ 0 | 1 | 2 ]

Build Speed
[ ] Incremental build < 5 seconds for typical change              [ 0 | 1 | 2 ]
[ ] Full clean build < 3 minutes                                  [ 0 | 1 | 2 ]
[ ] Hot reload / watch mode available                             [ 0 | 1 | 2 ]

Test Speed
[ ] Unit test suite runs in < 2 minutes locally                   [ 0 | 1 | 2 ]
[ ] Tests do not require network or external services by default  [ 0 | 1 | 2 ]
[ ] Flaky test rate < 1% (tracked as a metric)                    [ 0 | 1 | 2 ]
[ ] Tests can be run in parallel locally                          [ 0 | 1 | 2 ]

Local Run
[ ] Service starts in < 60 seconds                                [ 0 | 1 | 2 ]
[ ] Local service URLs and ports are documented                   [ 0 | 1 | 2 ]
[ ] Docker Compose or equivalent for local service dependencies   [ 0 | 1 | 2 ]

INNER LOOP SCORE: ___/30
```

### Outer Loop Audit

```
OUTER LOOP — PR → CI → Review → Merge → Deploy → Observe

CI Pipeline
[ ] Total CI time < 15 minutes                                    [ 0 | 1 | 2 ]
[ ] CI pipeline is parallelized                                   [ 0 | 1 | 2 ]
[ ] Dependency caching is configured                              [ 0 | 1 | 2 ]
[ ] Test flakiness rate < 1% in CI                                [ 0 | 1 | 2 ]
[ ] CI failure provides clear, actionable error messages          [ 0 | 1 | 2 ]

Code Review
[ ] Average PR review turnaround < 24 hours                       [ 0 | 1 | 2 ]
[ ] CODEOWNERS configured for automatic review assignment         [ 0 | 1 | 2 ]
[ ] PR description template exists and is used                    [ 0 | 1 | 2 ]
[ ] Average PR size < 400 lines changed                           [ 0 | 1 | 2 ]

Deployment
[ ] Deploy to staging is automatic on merge                       [ 0 | 1 | 2 ]
[ ] Production deploy is a single action (not multi-step manual)  [ 0 | 1 | 2 ]
[ ] Rollback takes < 5 minutes                                    [ 0 | 1 | 2 ]
[ ] Deploy preview environments exist for review                  [ 0 | 1 | 2 ]
[ ] Feature flags available for risky changes                     [ 0 | 1 | 2 ]

Observability
[ ] Logs are structured and searchable                            [ 0 | 1 | 2 ]
[ ] Basic metrics and dashboards exist per service                [ 0 | 1 | 2 ]
[ ] Alerts are actionable (low false positive rate)               [ 0 | 1 | 2 ]
[ ] On-call runbooks exist and are up to date                     [ 0 | 1 | 2 ]

OUTER LOOP SCORE: ___/34

TOTAL DX SCORE: ___/64
  0-25:  Critical — significant toil and friction
  26-40: Moderate — several high-impact improvements needed
  41-52: Good — targeted improvements will have high ROI
  53-64: Strong — focus on measurement and continuous improvement
```

---

## SPACE Framework Self-Assessment

Use this with your team (survey or workshop). Score 1–5.

```
SPACE SELF-ASSESSMENT
=====================

SATISFACTION
------------
1. I feel productive in my day-to-day work                        [ 1 | 2 | 3 | 4 | 5 ]
2. I have the tools and access I need to do my job                [ 1 | 2 | 3 | 4 | 5 ]
3. I am not frequently blocked by process or tooling              [ 1 | 2 | 3 | 4 | 5 ]
4. I rarely feel burned out by operational toil                   [ 1 | 2 | 3 | 4 | 5 ]

PERFORMANCE
-----------
5. My team ships features that customers value                    [ 1 | 2 | 3 | 4 | 5 ]
6. Bugs and incidents are rare and resolved quickly               [ 1 | 2 | 3 | 4 | 5 ]

ACTIVITY
--------
7. I can ship small changes frequently (multiple times/week)      [ 1 | 2 | 3 | 4 | 5 ]
8. Code reviews happen quickly and don't block my work            [ 1 | 2 | 3 | 4 | 5 ]

COMMUNICATION / COLLABORATION
------------------------------
9. I know who to ask when I'm stuck                               [ 1 | 2 | 3 | 4 | 5 ]
10. Technical decisions are made clearly and communicated well    [ 1 | 2 | 3 | 4 | 5 ]
11. I have enough uninterrupted focus time                        [ 1 | 2 | 3 | 4 | 5 ]

EFFICIENCY / FLOW
-----------------
12. My local build and test cycle is fast (< 5 min)               [ 1 | 2 | 3 | 4 | 5 ]
13. CI is reliable and fast (< 15 min, rarely flaky)              [ 1 | 2 | 3 | 4 | 5 ]
14. Deploying to production is low-friction                       [ 1 | 2 | 3 | 4 | 5 ]
15. I spend most of my time on product work, not toil             [ 1 | 2 | 3 | 4 | 5 ]

OPEN QUESTIONS
--------------
16. What is your single biggest source of daily friction?
    [open text]

17. What one tool, process, or change would most improve your productivity?
    [open text]

18. On a scale of 0-10, how likely are you to recommend this engineering
    environment to a friend joining the company?
    [0–10 NPS]

SCORING KEY
-----------
< 40:  Critical DX issues — engineers are burning significant time on non-product work
40-55: Moderate — several actionable improvements available
56-65: Good — targeted wins will compound over time
66-75: Strong — focus on the long tail and measurement
```

---

## DX Improvement Backlog Template

Prioritize by: (Frequency of pain × Severity of impact) / Effort to fix

```
DX IMPROVEMENT BACKLOG
=======================
Scoring: Frequency (1-5) × Severity (1-5) = Impact score
         Effort: S (< 1 day), M (1 week), L (1 month), XL (> 1 month)
         Priority = Impact / Effort weight (S=1, M=2, L=4, XL=8)

ID  | Problem                          | Freq | Sev | Impact | Effort | Priority | Owner
----|----------------------------------|------|-----|--------|--------|----------|------
DX1 | CI pipeline takes 22 minutes     |  5   |  4  |  20    |   M    |   10.0   | ___
DX2 | Flaky auth test requires reruns  |  5   |  3  |  15    |   S    |   15.0   | ___
DX3 | Local setup takes 3 days         |  3   |  5  |  15    |   M    |    7.5   | ___
DX4 | No ephemeral preview envs        |  4   |  3  |  12    |   L    |    3.0   | ___
DX5 | Manual deploy process (6 steps)  |  3   |  4  |  12    |   M    |    6.0   | ___
... |                                  |      |     |        |        |          |

NEXT SPRINT: Pick the top 2-3 by priority score.

DEFINITION OF DONE per item:
  [ ] Improvement shipped and measurable
  [ ] Benchmark before/after recorded
  [ ] Announced to affected developers
  [ ] Added to DX metrics dashboard
```

---

## DX Metrics Dashboard Spec

Track these monthly. Present to engineering leadership quarterly.

```
DX METRICS DASHBOARD — [Month] [Year]
======================================

INNER LOOP
----------
Median incremental build time:     ___ sec   (target: < 5s)
Median full build time:             ___ min   (target: < 3 min)
Median unit test suite time (local): ___ min  (target: < 2 min)
Local setup time (new hire):        ___ hrs   (target: < 4 hrs)

OUTER LOOP
----------
Median CI pipeline time:            ___ min   (target: < 15 min)
CI flakiness rate:                  ___%      (target: < 1%)
Median PR review turnaround:        ___ hrs   (target: < 24 hrs)
Median lead time (commit → prod):   ___ hrs   (target: < 24 hrs)
Deployment frequency (org):         ___/day
Change failure rate:                ___%      (target: < 5%)

ONBOARDING
----------
Time for new hire first deploy:     ___ days  (target: < 5 days)
Onboarding survey score:            ___/5

SATISFACTION (quarterly survey)
--------------------------------
SPACE self-assessment average:      ___/75
NPS score:                          ___       (target: > 40)
Top pain point cited this quarter:  ___

TOIL TRACKING
-------------
% time on non-product work (survey): ___%     (target: < 20%)
On-call incidents last month:         ___
Avg incident resolution time:         ___ min

TRENDS (vs. last quarter)
--------------------------
CI time:                ↑ worse / ↓ better / → stable
Flakiness:              ↑ worse / ↓ better / → stable
Review turnaround:      ↑ worse / ↓ better / → stable
Developer satisfaction: ↑ better / ↓ worse  / → stable
```

---

## Developer Satisfaction Survey Template

Run quarterly, keep under 5 minutes.

```
DEVELOPER EXPERIENCE SURVEY — Q[X] [YEAR]

HOW'S YOUR TOOLING?
-------------------
1. How fast is your local build?
   [ ] < 30 sec  [ ] 30 sec – 2 min  [ ] 2–5 min  [ ] > 5 min

2. How often do you have to re-run CI due to flaky tests?
   [ ] Never  [ ] Rarely (< once/week)  [ ] Sometimes (1-3/week)  [ ] Often (daily)

3. How long does a typical CI run take?
   [ ] < 5 min  [ ] 5–10 min  [ ] 10–20 min  [ ] > 20 min

4. How painful is it to deploy your service?
   [ ] Fully automated, no friction  [ ] Mostly automated, minor manual steps
   [ ] Manual but documented  [ ] Manual and painful / undocumented

5. How easy is it to debug issues in production?
   [ ] Very easy (good logs, traces, dashboards)
   [ ] Mostly easy
   [ ] Difficult (some tools, but incomplete)
   [ ] Very difficult (log grep + tribal knowledge)

HOW'S YOUR WORKFLOW?
--------------------
6. How often are you blocked waiting for another team or process?
   [ ] Never  [ ] Rarely  [ ] Weekly  [ ] Daily

7. How much of your week is spent on non-product work (toil, meetings, context-switching)?
   [ ] < 10%  [ ] 10–20%  [ ] 20–40%  [ ] > 40%

8. Do you have enough uninterrupted focus time?
   [ ] Yes  [ ] Somewhat  [ ] No

OPEN FEEDBACK
-------------
9. What is your #1 source of daily friction?
   [open text]

10. What one improvement would most increase your productivity?
    [open text]

11. How likely are you to recommend this engineering environment to a friend?
    [0–10 NPS]
```

---

## Toolchain Audit

Run this when suspecting DX problems are toolchain-rooted:

```
TOOLCHAIN AUDIT CHECKLIST

Version Management
[ ] Language versions pinned (.nvmrc / .python-version / go.mod / .tool-versions)
[ ] All developers using same version (verified, not assumed)
[ ] CI uses same version as local (matched)

Package Management
[ ] Lockfile committed and enforced in CI
[ ] Dependency installation is cached in CI
[ ] No globally installed tools required (everything in devDependencies / pyproject / go.mod)

Local Dev Environment
[ ] Single command to set up (make setup / ./bootstrap.sh)
[ ] Docker Compose or devcontainer for external dependencies
[ ] Environment variable management documented (direnv / .env.example)
[ ] No manual steps required after initial setup

Editor / IDE
[ ] Recommended extensions/plugins documented
[ ] Project-level lint and format config committed (.eslintrc, pyproject.toml, .editorconfig)
[ ] Format-on-save configured or documented

Git Hooks
[ ] Pre-commit hooks configured for fast local checks (lint, type-check, secrets scan)
[ ] Hooks installed automatically on setup (husky / pre-commit)
[ ] Hooks run in < 10 seconds (fast enough not to be bypassed)
```

---

## Onboarding Friction as a DX Signal

First-day experience is the highest-signal audit you can run. New hires encounter every broken assumption because they have no tribal knowledge to work around.

**Onboarding friction audit — run with every new hire:**
```
Day 1 timer:
  Time to get development environment running:    ___ hours
  Number of "ask a human" moments:                ___
  Blockers encountered (list):                    ___

Day 5 checkpoint:
  Has the new hire shipped at least one PR to production?  Y / N
  What took longest?                                       ___
  What was most confusing?                                 ___
  What documentation was missing or wrong?                 ___
```

Treat every "ask a human" moment as a documentation or automation bug. Fix it before the next hire.

---

## Output Format

When applying this skill, the agent should:

1. **Start with the inner loop**: Ask how long local builds and tests take before discussing CI or deployment. Inner loop has the highest per-developer ROI.
2. **Run the DX audit**: Use the checklist to score current state before recommending improvements.
3. **Prioritize ruthlessly**: Use the impact × severity / effort model. Don't try to fix everything at once.
4. **Produce artifacts on request**: DX audit checklist, SPACE self-assessment, backlog template, metrics dashboard, developer survey.
5. **Connect to platform engineering** when inner/outer loop friction is infrastructure-rooted — recommend the `platform-engineering` skill.
6. **Cite SPACE dimensions** when discussing productivity metrics to avoid the "lines of code" trap.
7. Format checklists as Markdown task lists `- [ ]`. Format benchmarks as tables. Format templates as code blocks.

---

## References

- Nicole Forsgren, Margaret-Anne Storey, Chandra Maddila, Thomas Zimmermann, Brian Houck, Jenna Butler — ["The SPACE of Developer Productivity"](https://queue.acm.org/detail.cfm?id=3454124) (ACM Queue, 2021)
- Forsgren, Humble, Kim — *Accelerate: The Science of Lean Software and DevOps* (IT Revolution, 2018)
- DORA — [State of DevOps Report](https://dora.dev) (annual)
- LeadDev — ["Measuring developer experience"](https://leaddev.com/developer-experience)
- Gartner — ["Innovation Insight: Developer Experience Platforms"](https://gartner.com) (2023)
- Nate Swanson — ["Developer Experience at Spotify"](https://engineering.atspotify.com/developer-experience)
- DX Core 4 — [getdx.com](https://getdx.com/research/measuring-developer-productivity) (speed, effectiveness, quality, impact)
