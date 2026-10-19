---
name: test-plan-writer
description: Use when writing a test plan or test strategy for a release, feature, sprint or project, defining QA scope, risks, test types, environments, entry and exit criteria, or estimating testing effort.
---

# Test Plan Writer

## Overview

A test plan decides where testing effort goes and when the product is good enough to ship. Drive it by risk: test hardest what would hurt users or the business most if it broke.

## Method

1. **Understand the release:** features and changes (PRD, tickets, changelog, diff), affected areas, integrations, deadlines, team size.
2. **Assess risk** for each area: impact if it breaks × likelihood (new code, complex logic, past bugs, many integrations). Rank areas high, medium, low.
3. **Choose test types per area** based on risk: functional, regression, integration, API, end-to-end, performance, security, accessibility, compatibility, exploratory.
4. **Define environments and data:** where tests run, browsers and devices, test accounts, data setup and reset.
5. **Set entry and exit criteria** that can be checked objectively.
6. **Estimate and schedule** effort per area; note what is automated vs manual.
7. **Write** using the format below; keep it to what the team will actually use.

## Format

```
# Test Plan — <release / feature>

1. Scope
   In scope: <features, platforms>
   Out of scope: <and why>

2. Risk assessment
   | Area | Impact | Likelihood | Risk | Test approach |

3. Test types and coverage
   | Type | Areas | Manual / Automated | Owner |

4. Environments and test data
   <environments, browsers/devices matrix, accounts, data setup>

5. Entry criteria
   e.g. build deployed to staging, smoke tests pass, test data ready

6. Exit criteria
   e.g. all P1 cases pass, no open Blocker/Critical bugs, Major bugs triaged,
   regression suite ≥ 95% pass, performance within agreed limits

7. Schedule and effort
   | Activity | Estimate | Dates |

8. Defect management
   <tool, severity definitions, triage cadence>

9. Risks to the plan and mitigations
   <late builds, unstable environments, missing data>

10. Deliverables
   <test cases, automation results, test summary report>
```

## Common mistakes

- Equal effort on every area instead of focusing on risk.
- Exit criteria like "testing complete" that nobody can measure.
- No out-of-scope section, so expectations differ.
- Copying a generic template that does not mention the actual features.
- Forgetting regression of untouched areas that share code with the change.

---

Made by **Wageesha Tripathi** · [LinkedIn](https://www.linkedin.com/in/wst2002/) · [Email](mailto:tripathiwageesha2002@gmail.com) · [More skills](https://github.com/WST2002/claude-code-skills)
