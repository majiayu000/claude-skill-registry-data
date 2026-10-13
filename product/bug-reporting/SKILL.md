---
name: bug-reporting
description: Write high-quality bug reports that engineers can reproduce and fix without back-and-forth. Apply structured format with steps to reproduce, environment details, actual vs expected behavior, severity and priority scoring, and evidence (logs, screenshots, traces). Includes Jira MCP integration for direct ticket creation.
triggers:
  - "write a bug report"
  - "log a bug"
  - "report a defect"
  - "bug template"
  - "how to report this"
  - "found a bug"
  - "severity priority"
audience:
  - qa
  - engineer
---

# Bug Reporting

Write bug reports that get fixed — not sent back for more information.

---

## The Cost of a Bad Bug Report

A vague bug report ("the page is broken") creates a game of telephone:
1. Engineer can't reproduce it → asks QA for more info
2. QA provides some context → engineer asks again
3. 2-3 days pass → context is stale, harder to reproduce
4. Engineer finally reproduces it → half the sprint is gone

A good bug report is reproducible in < 5 minutes by any engineer who reads it.

---

## Bug Report Template

```markdown
## Bug: [Short, specific title — noun + verb + symptom]
# Good: "Checkout button submits duplicate order when clicked twice rapidly"
# Bad: "Checkout broken"

**Reporter**: [name]
**Date**: [date]
**Severity**: [P0 / P1 / P2 / P3 — see rubric below]
**Priority**: [Must Fix / Should Fix / Nice to Fix]
**Status**: Open

---

### Environment
- **App version / build**: [e.g., v2.4.1 / commit abc1234]
- **Browser / OS**: [e.g., Chrome 122 / macOS 14.3]
- **Environment**: [Local / Staging / Production]
- **Account / user state**: [e.g., logged in as admin, cart with 2 items]
- **Feature flags**: [any relevant flags enabled/disabled]

---

### Steps to Reproduce
1. [Precondition: what state must the system be in]
2. [Action 1 — be specific: "Click the 'Add to Cart' button for item ID 123"]
3. [Action 2]
4. [Action N]

### Expected Behavior
[What should happen — reference spec, acceptance criteria, or prior behavior]

### Actual Behavior
[What actually happens — be precise, not emotional]

---

### Evidence
- **Screenshot / video**: [attach or link]
- **Console errors**: [paste or link]
- **Network request/response**: [relevant API call, paste or link]
- **Log output**: [relevant lines, paste or link]
- **Stack trace**: [paste full trace if available]

---

### Reproducibility
[ ] Always (100%)
[ ] Often (> 50%)
[ ] Sometimes (< 50%)
[ ] Once — could not reproduce again

### Regression?
[ ] Yes — worked in [previous version/date]
[ ] No — never worked
[ ] Unknown

### Related
- Linked story/ticket: [PROJ-XXX]
- Related bugs: [PROJ-YYY]
- Affected component: [service / page / feature]
```

---

## Severity vs. Priority

These are different. A typo on the homepage can be high priority (brand) but low severity (not a system failure).

### Severity (technical impact)
| Level | Definition | Example |
|---|---|---|
| **P0 — Critical** | System down, data loss, security breach | Payment processing broken, user data exposed |
| **P1 — High** | Major feature broken, no workaround | Login fails for all users |
| **P2 — Medium** | Feature impaired, workaround exists | Export fails; user can copy-paste manually |
| **P3 — Low** | Minor issue, cosmetic, edge case | Tooltip text is truncated on small screens |

### Priority (business urgency)
| Level | Definition |
|---|---|
| **Must Fix** | Blocks release or causes user/revenue harm now |
| **Should Fix** | Significant UX degradation; fix in next sprint |
| **Nice to Fix** | Low impact; add to backlog, prioritize when possible |

**Rule**: Set severity based on technical impact. Let the PM/EM set priority based on business context. Don't conflate them.

---

## Title Formula

A good title has three parts: **[Subject] [Action] [Symptom]**

| Bad | Good |
|---|---|
| "Login broken" | "Login form clears password field after failed attempt" |
| "Error on checkout" | "Checkout POST /orders returns 500 when promo code is empty string" |
| "Map doesn't work" | "Map pins disappear after zooming below level 8 on iOS Safari" |
| "Performance issue" | "Product search takes > 10s when filtering by 3+ categories" |

---

## Evidence Checklist

Before submitting, verify you have:
- [ ] Screenshot or screen recording (for UI bugs)
- [ ] Network request + response (for API bugs — use browser DevTools Network tab)
- [ ] Console errors (for frontend bugs)
- [ ] Relevant log lines with timestamps (for backend bugs)
- [ ] Exact reproduction steps — can a new engineer follow them cold?
- [ ] App version / build number (so the fix can be verified against the right release)

---

## For API / Backend Bugs

Include the full request and response:

```
Request:
  POST /api/v1/orders
  Headers: Authorization: Bearer [token]
  Body: { "items": [], "promoCode": "" }

Response:
  HTTP 500 Internal Server Error
  Body: { "error": "Cannot read property 'discount' of undefined" }

Stack trace:
  TypeError: Cannot read property 'discount' of undefined
    at applyPromo (src/orders/promo.js:42)
    at createOrder (src/orders/orders.js:88)
```

---

## For Flaky / Intermittent Bugs

Intermittent bugs are harder to report but follow the same structure. Add:

```markdown
### Flakiness Data
- How often does it reproduce: [X out of Y attempts]
- Conditions that seem to trigger it: [high load / specific user / timing]
- Log pattern when it fails vs. succeeds: [show both]
- First observed: [date / version]
- Frequency increasing? [yes / no / unknown]
```

---

## MCP Integration

### Create a Jira bug ticket directly

```
# Create a bug ticket with full details
jira_create_issue: {
  project: [KEY],
  issuetype: "Bug",
  summary: "[Short bug title]",
  description: [full bug report markdown],
  priority: { name: "High" },
  labels: ["qa-reported", "sprint-N"],
  customfield_severity: "P1"
}

# Link to the story it was found in
jira_create_issue_link: {
  type: "is caused by",
  inwardIssue: [BUG-KEY],
  outwardIssue: [STORY-KEY]
}

# Transition to "In Review" after filing
jira_transition_issue: { issue: [BUG-KEY], transition: "In Review" }
```

### Search for duplicates before filing
```
# Check for existing similar bugs
jira_search_issues: project = [KEY] AND issuetype = Bug AND 
  text ~ "[keyword from title]" AND status != Done
  ORDER BY created DESC
```

---

## References
- Cem Kaner: *Testing Computer Software* — bug reporting chapters
- Michael Bolton: [Good Bug Reports](https://developsense.com/blog/2010/08/good-bug-reports)
- Google Testing Blog: [How to Write a Good Bug Report](https://testing.googleblog.com/)
