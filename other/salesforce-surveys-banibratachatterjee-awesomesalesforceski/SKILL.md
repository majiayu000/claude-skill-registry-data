---
name: salesforce-surveys
description: "Use when designing, configuring, distributing, or troubleshooting Salesforce Surveys and Feedback Management. Triggers: 'create a survey', 'NPS score', 'survey invitation', 'survey response report', 'customer feedback form', 'guest user survey access'. NOT for custom-built LWC form components or third-party survey tools like SurveyMonkey or Qualtrics."
category: admin
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Security
  - User Experience
  - Scalability
triggers:
  - "how do I create and send a survey to customers"
  - "survey responses are not being captured from external users"
  - "guest user cannot submit survey and gets access denied"
  - "NPS score calculation is wrong or missing on survey results"
  - "how to branch survey questions based on previous answers"
  - "survey response limit reached on our org"
tags:
  - salesforce-surveys
  - feedback-management
  - nps
  - survey-invitation
  - guest-user
  - customer-experience
inputs:
  - "survey use case and target audience (internal vs external)"
  - "Salesforce edition and Feedback Management tier"
  - "guest user profile permissions"
outputs:
  - "survey design guidance with question type selection"
  - "survey distribution and invitation configuration"
  - "guest user permission checklist for external surveys"
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-04-05
---

You are a Salesforce Admin expert in Salesforce Surveys and Feedback Management. Your goal is to help practitioners design surveys that capture meaningful feedback, configure distribution channels correctly, and avoid the common permission and licensing pitfalls that silently break external survey collection.

---

## Before Starting

Gather this context before working on anything in this domain:

- What Salesforce edition and Feedback Management tier is the org on? Base tier has a lifetime cap of 300 responses, Starter allows 100K, and Growth is unlimited. This determines whether the survey approach is even viable at scale.
- Is the survey for internal users (employees, partners) or external unauthenticated users (customers via email link)? External surveys require guest user profile configuration.
- What question types are needed? Rating, NPS, Slider, Multiple Choice, Ranking, and Matrix (Spring '23+) each have different reporting and branching implications.

---

## Core Concepts

### Survey Data Model

Salesforce Surveys use a specific object hierarchy. The `Survey` object is the parent container. Each survey has one or more `SurveyVersion` records representing draft and active versions. When a survey is sent, a `SurveyInvitation` record is created to track the distribution channel and link. Responses are stored in `SurveyResponse` (one per respondent session) with individual answers in `SurveyQuestionResponse`. Scoring data lands in `SurveyQuestionScore`. Understanding this hierarchy is critical for reporting -- you cannot build a useful survey dashboard without joining across these objects.

### Question Types and Branching

Salesforce supports six question types: Rating (star or number scale), NPS (0-10 with Detractor/Passive/Promoter bucketing), Slider (continuous numeric range), Multiple Choice (single or multi-select), Ranking (ordered preference), and Matrix (grid of rows and columns, available Spring '23+). Branching in Salesforce Surveys is page-level, not question-level. You route respondents to different pages based on answers on the current page. This means you must plan your page layout carefully -- a question that drives branching logic must be on its own page or grouped only with questions that share the same routing destination.

### Guest User Access for External Surveys

External survey collection is the single most common source of failures. When an unauthenticated person clicks a survey link, they operate under the site's Guest User Profile. That profile must have Read and Create permissions on Survey, SurveyInvitation, SurveyResponse, and SurveyQuestionResponse objects. Without these, the respondent silently fails to submit or sees a generic access error. The guest user also needs field-level security on all fields used in the survey invitation flow.

---

## Common Patterns

### Pattern: Post-Case Survey via Email Invitation

**When to use:** You want to collect CSAT or NPS feedback after a support case is closed.

**How it works:**
1. Create the survey with an NPS or Rating question on page 1 and an optional free-text follow-up on page 2.
2. Create a Survey Invitation linked to the survey, setting the participant type to "Community" or "Link" for external respondents.
3. Build a Flow that fires when Case Status changes to Closed. The Flow creates a SurveyInvitation record and sends the invitation URL via email using an Email Alert or Send Email action.
4. Map the SurveyInvitation to the Case via a lookup or the survey's built-in record association.

**Why not the alternative:** Sending a raw survey link without a SurveyInvitation loses the ability to tie responses back to the originating Case record, making the data useless for reporting.

### Pattern: Internal Employee Pulse Survey

**When to use:** Collecting periodic feedback from authenticated Salesforce users (employees or partners with login access).

**How it works:**
1. Create the survey with the desired question types.
2. Distribute via a direct link or embed the survey in a Lightning page using the Survey component.
3. Internal users authenticate normally; no guest user configuration is needed.
4. Responses are automatically tied to the running user's record.

---

## Decision Guidance

| Situation | Recommended Approach | Reason |
|---|---|---|
| External customers, no Salesforce login | Guest User Profile + SurveyInvitation link | Only way to capture external responses without requiring authentication |
| Internal employees with Salesforce access | Direct link or embedded Lightning component | Simpler setup, automatic user association |
| Need to tie response to a Case or Account | Flow-generated SurveyInvitation with record lookup | Maintains the relationship for reporting |
| More than 300 lifetime responses needed | Upgrade to Feedback Management Starter or Growth | Base tier hard cap cannot be bypassed |
| Complex conditional logic between questions | Page-level branching with one decision question per page | Branching is page-level only; mixing decision questions on one page creates routing conflicts |

---

## Recommended Workflow

Step-by-step instructions for an AI agent or practitioner working on this task:

1. Confirm the org's Feedback Management tier and current response count. If the org is on Base tier, verify the 300-response lifetime cap has not been reached before designing anything.
2. Identify the audience: internal (authenticated) vs external (guest user). For external, verify the Experience Cloud site exists and the Guest User Profile has Read and Create on Survey, SurveyInvitation, SurveyResponse, and SurveyQuestionResponse.
3. Design the survey page structure with branching in mind. Place decision-driving questions on their own page so page-level branching can route correctly.
4. Create the SurveyInvitation records programmatically (via Flow or Apex) if the survey is triggered by a business event like case closure. Map the invitation to the source record.
5. Test with an actual external user session (incognito browser, no Salesforce login) to verify guest user permissions are correct. Internal testing while logged in will not surface guest user permission failures.
6. Build reports joining SurveyResponse and SurveyQuestionResponse to the source record (Case, Account, etc.) and validate that NPS bucketing and scoring appear correctly.

---

## Review Checklist

Run through these before marking work in this area complete:

- [ ] Feedback Management tier confirmed and response cap is sufficient for projected volume
- [ ] Guest User Profile has Read and Create on all survey-related objects (if external)
- [ ] Field-level security on guest user profile covers all fields referenced in the survey flow
- [ ] Branching logic tested with each possible answer path
- [ ] SurveyInvitation records correctly associated to source records for reporting
- [ ] Survey tested from an unauthenticated browser session (for external surveys)
- [ ] NPS scoring verified: Detractor (0-6), Passive (7-8), Promoter (9-10)

---

## Salesforce-Specific Gotchas

Non-obvious platform behaviors that cause real production problems:

1. **Base tier 300-response lifetime cap** -- This is a lifetime cap, not monthly. Once 300 responses are recorded across all surveys, no more responses can be collected. There is no warning before hitting the limit; surveys simply stop accepting submissions.
2. **Page-level branching only** -- Unlike third-party tools, branching cannot be applied at the individual question level. If two questions on the same page need different routing, you must split them across pages.
3. **Guest user silent failures** -- When a guest user lacks object-level or field-level access, the survey may render but silently fail on submit with no useful error message to the respondent.

---

## Output Artifacts

| Artifact | Description |
|---|---|
| Survey design document | Question types, page layout, and branching logic map |
| Guest user permission checklist | Object and field permissions required on the Guest User Profile |
| Survey distribution flow | Automation that creates SurveyInvitation records and sends links |

---

## Related Skills

- reports-and-dashboards-fundamentals -- for building survey response reports and NPS dashboards
- sharing-and-visibility -- for understanding guest user profile permissions and object access
- flow-for-admins -- for automating survey invitation creation and distribution
