---
name: salesforce-surveys
description: "Use when designing, configuring, distributing, or troubleshooting Salesforce Surveys and Feedback Management. Triggers: 'create a survey', 'NPS score', 'survey invitation', 'survey response report', 'customer feedback form', 'guest user survey access', 'SurveyInvitation', 'SurveySubject', 'SurveySettings', 'sendSurveyInvitation', 'survey not linked to case', 'deploy a survey between orgs'. NOT for choosing between CSAT, NPS, and CES as your CX metric — use architect/customer-effort-scoring. NOT for third-party survey tools like SurveyMonkey or Qualtrics."
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
  - "send a survey automatically after a case is closed"
  - "survey responses are not linked back to the case or account"
  - "SurveyInvitation ContactId field is not writeable"
  - "deploy a survey from sandbox to production"
  - "SOQL on SurveyVersion Status returns no such column"
  - "participants cannot resume a partially completed survey"
  - "enable Salesforce Surveys through metadata SurveySettings"
  - "embedded survey renders as a blank iframe on our website"
  - "bulk send survey invitations to more than 300 contacts"
tags:
  - salesforce-surveys
  - feedback-management
  - nps
  - survey-invitation
  - survey-subject
  - guest-user
  - customer-experience
inputs:
  - "survey use case and target audience (internal vs external)"
  - "Salesforce edition and Feedback Management tier"
  - "guest user profile permissions"
  - "the business record the responses must be reportable against (Case, Account, Order…)"
outputs:
  - "survey design guidance with question type selection"
  - "survey distribution and invitation configuration"
  - "guest user permission checklist for external surveys"
  - "deployable SurveySettings / package.xml and a SurveyInvitation + SurveySubject automation shape"
dependencies: []
version: 1.1.0
author: Pranav Nagrecha
updated: 2026-09-05
---

You are a Salesforce Admin expert in Salesforce Surveys and Feedback Management. Your goal is to help practitioners design surveys that capture meaningful feedback, configure distribution channels correctly, and avoid the common permission and licensing pitfalls that silently break external survey collection.

---

## Before Starting

Gather this context before working on anything in this domain:

- What Salesforce edition and Feedback Management tier is the org on? Base tier has a lifetime cap of 300 responses, Starter allows 100K, and Growth is unlimited. This determines whether the survey approach is even viable at scale. (The tier gates real features — see `references/gotchas.md` Gotcha 1 for what is documented and what is not.)
- Is the survey for internal users (employees, partners) or external unauthenticated users (customers via email link)? External surveys require guest user profile configuration.
- What question types are needed? `SurveyQuestion.QuestionType` is a restricted picklist of 19 values, and each has different reporting and branching implications — see Core Concepts below.
- Which business record must the responses be reportable against? That answer decides whether you need `SurveySubject` records, and building the survey without it is the most expensive thing to retrofit.

---

## Questions to Ask Before Configuring

Ask these before opening Survey Builder; the answers decide the design, and an LLM that skips them produces a survey that collects data nobody can act on.

| Ask | Why it matters | What a good answer adds |
|---|---|---|
| "Which record must every response be traceable to — Case, Account, Order, or nothing?" | Decides whether the design needs `SurveySubject` rows, which cannot be backfilled onto responses already collected | The join shape: `ParentId` = invitation or response, `SubjectId` = that record |
| "Do respondents have Salesforce logins, or are they anonymous members of the public?" | Guest access, `CommunityId`, and the Experience Cloud dependency all hang off this one answer | The distribution channel and whether a guest profile is in scope at all |
| "Does anyone need the responses to be anonymous?" | Anonymity is not free — it disables Paused, so anyone who closes the tab starts over | An explicit trade of attributability and resume against candour |
| "How does the survey branch, and how many decisions live on one page?" | Routing is decided per page, and a `BASIC`-type survey cannot branch at all | The page map, and an early catch if the survey type is wrong |
| "How many invitations go out in one batch, and from which address?" | `ConnectApi.Surveys.sendSurveyInvitationEmail` caps at 300 recipients per call and requires a from-address | Chunking, an org-wide email address, and a Lightning (not Classic) template |
| "Which org does this survey have to exist in, and who promotes it?" | The survey is a Flow, so it inherits the active-flow deployment gate and per-org record IDs | A deploy plan, and reports that do not hardcode a `SurveyId` |
| "Who owns the response data, and can survey owners edit it?" | `enableSurveyOwnerCanManageResponse` widens who can touch submitted feedback | A deliberate setting rather than an inherited default |

What a proper configuration adds over just building a survey: every response arrives joined to the record that caused it, the guest path is proven from an unauthenticated session before customers see it, the anonymity and resume behaviours are chosen rather than discovered, and the whole thing promotes between orgs as a Flow instead of being retyped.

---

## Core Concepts

### Survey Data Model

Salesforce Surveys use a specific object hierarchy. The `Survey` object is the parent container. Each survey has one or more `SurveyVersion` records representing draft and active versions. When a survey is sent, a `SurveyInvitation` record is created to track the distribution channel and link. Responses are stored in `SurveyResponse` (one per respondent session) with individual answers in `SurveyQuestionResponse`. Aggregates land in `SurveyQuestionScore`. Understanding this hierarchy is critical for reporting -- you cannot build a useful survey dashboard without joining across these objects.

The split that matters most is **which of these you can write**:

| Object | Createable? | Supported calls (Object Reference) |
|---|---|---|
| `Survey`, `SurveyVersion`, `SurveyPage`, `SurveyQuestion` | No | query / retrieve / describe / getDeleted / getUpdated (+ `search()` on Survey, SurveyVersion) |
| `SurveyResponse`, `SurveyQuestionResponse` | No | query / retrieve / describe (+ `undelete()` on SurveyResponse) |
| `SurveyQuestionScore` | No | query / retrieve / describe / delete / undelete |
| `SurveyInvitation`, `SurveySubject`, `SurveyEngagementContext`, `SurveyEmailBranding` | **Yes** | full CRUD + upsert |

Authoring happens in Survey Builder; automation happens on the createable half. There is no supported way to insert a survey definition as records.

### The Survey Is a Flow

`Flow.processType` includes `Survey` — "A flow for Salesforce Surveys. From the UI, this type of flow is created in Survey Builder", API 42.0 and later — and `SurveyEnrich` for the Survey Data Mapper. The REST translation resources agree: translated survey fields "are stored in Flow fields". Practically this means the survey retrieves and deploys as the `Flow` metadata type, and every Flow rule applies to it: the production active-flow deployment gate, the managed-package restriction, and the paused-interview rule that blocks deleting a version. `SurveyResponse.InterviewId` points at the `FlowInterview` for that response, which is why a paused response is literally a paused flow interview.

### Question Types and Branching

`SurveyQuestion.QuestionType` is a restricted picklist with 19 values: `Boolean` (v49.0+), `CSAT`, `Currency`, `Date`, `DateTime`, `FreeText`, `Image`, `Matrix` (v55.0+), `MultipleChoice`, `MultiSelectPicklist`, `NPS`, `Number`, `Picklist`, `RadioButton`, `StackRank`, `Rating`, `ShortText` (v49.0+), `Slider`, `Toggle`. The Metadata API's parallel `SurveyQuestionType` enum spells multiple-choice as `MultiChoice` and omits `RadioButton`, so a value copied from one context fails in the other.

Branching in Salesforce Surveys is page-level, not question-level. You route respondents to different pages based on answers on the current page. Plan the page layout accordingly — a question that drives branching must be on its own page or grouped only with questions that share the same routing destination. Whether the survey can branch at all is fixed by `Survey.SurveyType`: `SURVEY` has everything, `BASIC` ships without display logic or page branching, and `ASSESSMENT` (API 58.0+) targets sales enablement.

### Guest User Access for External Surveys

External survey collection is the single most common source of failures. When an unauthenticated person clicks a survey link, they operate under the site's Guest User Profile. That profile must have Read and Create permissions on Survey, SurveyInvitation, SurveyResponse, and SurveyQuestionResponse objects. Without these, the respondent silently fails to submit or sees a generic access error. The guest user also needs field-level security on all fields used in the survey invitation flow. Cross-reference `admin/experience-cloud-guest-access` for the site-level hardening that surrounds this profile.

---

## Common Patterns

### Pattern: Post-Case Survey via Email Invitation

**When to use:** You want to collect CSAT or NPS feedback after a support case is closed.

**How it works:**
1. Create the survey with an NPS or Rating question on page 1 and an optional free-text follow-up on page 2.
2. Prefer the platform action: `Flow`'s `actionType` `sendSurveyInvitation` exists precisely for this — "Sends email survey invitations to leads, contacts, and users in your org based on an action, such as when a customer support case closes" (API 47.0+).
3. If you need control the action does not give you, build the records by hand: create a `SurveyInvitation` with `SurveyId`, `ParticipantId`, `CommunityId` and `OptionsAllowGuestUserResponse`, then a `SurveySubject` with `ParentId` = the invitation and `SubjectId` = the Case.
4. Send the invitation URL by reading `SurveyInvitation.InvitationLink` back after insert — it is generated, never supplied.

**Why not the alternative:** Sending a raw survey link without a SurveyInvitation loses the ability to tie responses back to the originating Case record, making the data useless for reporting.

### Pattern: Internal Employee Pulse Survey

**When to use:** Collecting periodic feedback from authenticated Salesforce users (employees or partners with login access).

**How it works:**
1. Create the survey with the desired question types.
2. Distribute via a direct link or embed the survey in a Lightning page using the Survey component.
3. Internal users authenticate normally; no guest user configuration is needed.
4. Responses carry `SurveyResponse.SubmitterId`, a lookup to Contact, Lead or User.

### Pattern: Bulk Send From Apex

**When to use:** A campaign-scale send to a list of contacts, where a record-triggered Flow has nothing to trigger on.

**How it works:** Call `ConnectApi.Surveys.sendSurveyInvitationEmail(surveyId, input)` in chunks of 300. Required input properties are `recipients`, `fromEmailAddress`, `isPersonalInvitation`, `allowGuestUserResponse`, `allowParticipantsAccessTheirResponse` and `collectAnonymousResponse`. Set `isPersonalInvitation = true` to keep responses attributable. The full shape is in `references/metadata-examples.md` § 8.

---

## Decision Guidance

| Situation | Recommended Approach | Reason |
|---|---|---|
| External customers, no Salesforce login | Guest User Profile + SurveyInvitation with `CommunityId` and `OptionsAllowGuestUserResponse` | Only way to capture external responses without requiring authentication |
| Internal employees with Salesforce access | Direct link or embedded Lightning component | Simpler setup, automatic user association via `SubmitterId` |
| Need to tie response to a Case or Account | `SurveySubject` with `ParentId` = invitation/response, `SubjectId` = the record | The only supported join; a lookup on the Case does not exist |
| Case-closed trigger, no custom logic needed | Flow `sendSurveyInvitation` action | Documented platform action; fewer records to hand-manage |
| More than 300 recipients in one send | Chunk `ConnectApi.Surveys.sendSurveyInvitationEmail` | Hard per-call cap of 300 participants |
| Complex conditional logic between questions | Page-level branching, one decision question per page, `SurveyType` = `SURVEY` | Routing is per page; a `BASIC` survey has no branching at all |
| Respondents must be able to resume | Keep `OptionsCollectAnonymousResponse` and `OptionsAllowParticipantAccessTheirResponse` false | Either flag set to true removes the Paused status |
| Survey must exist in several orgs | Retrieve and deploy the `Flow` (processType `Survey`) | It is Flow metadata, not org-only configuration |
| Embedding the survey on your own website | `IframeWhiteListUrlSettings` with `<context>Surveys</context>` | Otherwise the frame is blocked with no visible error |

---

## Recommended Workflow

1. **Establish what exists.** Query the org before designing: `SELECT DeveloperName, SurveyType, ActiveVersionID, IsPartialSaveEnabled FROM Survey` and `SELECT VersionNumber, SurveyStatus FROM SurveyVersion WHERE SurveyId = '…'`. Confirm `SurveySettings.enableSurvey` is `true`. Note that the status field is `SurveyStatus`, not `Status` — `references/gotchas.md` Gotcha 4.
2. **Answer the seven questions above**, and record the answer to "which record must every response trace to" as the design's first line. It decides whether `SurveySubject` is in scope.
3. **Draft the survey design** as `surveys/<Name>.survey.json` using `templates/salesforce-surveys-template.md`: pages, question types from the 19-value picklist, one branching question per page, and the anonymity/resume flags. Run the checker — it lints branch targets, type spellings, and the anonymity-versus-partial-save contradiction.
4. **Write the deployable metadata** from `references/metadata-examples.md`: `settings/Survey.settings-meta.xml`, the guest `Profile` object permissions, `IframeWhiteListUrlSettings` if the survey is embedded off-platform, and the `package.xml`. Every XML block there is well-formed and grounded in the guide's own samples.
5. **Build the distribution**, preferring the `sendSurveyInvitation` Flow action; fall back to the `SurveyInvitation` + `SurveySubject` Apex in § 6 of the metadata examples. Draft any bulk load as `surveys/<Name>.invitations.csv` so the checker can verify the columns are createable and the expiry is in the future.
6. **Run the checker and fix every ERROR** before deploying:
   ```bash
   python3 skills/admin/salesforce-surveys/scripts/check_salesforce_surveys.py \
     --manifest-dir force-app/main/default
   ```
7. **Prove the guest path and the join.** Open the invitation link in a private window with no Salesforce session and submit. Then run the verification SOQL in `references/metadata-examples.md` — response rate by survey version, and `SurveySubject` rows with `SubjectEntityType = 'Case'`. Zero subjects against non-zero invitations means the association never landed, and it cannot be added afterwards.

---

## Review Checklist

Run through these before marking work in this area complete:

- [ ] `SurveySettings.enableSurvey` is `true` in the target org and in the deployed package
- [ ] Feedback Management tier confirmed and response cap is sufficient for projected volume
- [ ] `Survey.SurveyType` supports the branching the design assumes (not `BASIC`)
- [ ] `Survey.ActiveVersionID` is non-null before any invitation goes out
- [ ] Guest User Profile has the survey object permissions and no `viewAllRecords` / `modifyAllRecords` (if external)
- [ ] Field-level security on guest user profile covers all fields referenced in the survey flow
- [ ] Branching logic tested with each possible answer path, one decision question per page
- [ ] `SurveySubject` rows exist for every invitation that needs to be reportable against a record
- [ ] Invitation payloads set only createable fields; `ParticipantId` present and correct (it cannot be updated)
- [ ] `InviteExpiryDateTime` set and in the future
- [ ] Anonymity flags chosen deliberately, with the loss of Paused/resume accepted in writing
- [ ] Survey tested from an unauthenticated browser session (for external surveys)
- [ ] NPS scoring verified against the report definition, not assumed from the object model
- [ ] `python3 scripts/check_salesforce_surveys.py --manifest-dir <dir>` exits 0

---

## Salesforce-Specific Gotchas

The full set, with What happens / When it occurs / How to avoid and line-level citations, is in
`references/gotchas.md`. The three that break the most deployments:

1. **`SurveyVersion.Status` does not exist** — the field is `SurveyStatus`, so the guard query everyone writes silently returns nothing.
2. **Only `ParticipantId` is writable on an invitation** — `ContactId`, `LeadId` and `UserId` are derived, and a Flow that sets them fails.
3. **`SurveySubject` is the only join** — and its `ParentId` is the invitation or the response, never the Case.

---

## Output Artifacts

| Artifact | Description |
|---|---|
| Survey design document | `surveys/<Name>.survey.json` — question types, page layout, branching map, anonymity flags |
| `settings/Survey.settings-meta.xml` | The org-level Surveys switch, deployable |
| Guest user permission checklist | Object and field permissions required on the Guest User Profile |
| Survey distribution flow or Apex | Automation that creates SurveyInvitation + SurveySubject records and sends links |
| `surveys/<Name>.invitations.csv` | Data Loader payload for a bulk invitation load, createable columns only |
| Verification SOQL | Response rate by survey version, and the SurveySubject association check |

---

## Reference Files

| File | Read it when |
|---|---|
| `references/metadata-examples.md` | Writing the deployable XML, the invitation CSV, the SurveySubject Apex, package.xml, or the verification SOQL |
| `references/gotchas.md` | A survey "works in the builder" and fails in production, or a field/status name does not behave as expected |
| `references/well-architected.md` | Weighing native Surveys against third-party tools, or the anonymous-versus-tracked and tier decisions |
| `references/llm-anti-patterns.md` | Reviewing AI-generated survey guidance before acting on it |
| `templates/salesforce-surveys-template.md` | Starting a new survey engagement and capturing the seven questions above |

---

## Related Skills

- admin/reports-and-dashboards-fundamentals — building survey response reports and NPS dashboards across the read-only survey objects
- admin/sharing-and-visibility — guest user profile permissions, object access, and the record-access model behind survey data
- admin/experience-cloud-guest-access — the site-level guest hardening that surrounds the survey guest profile
- admin/experience-cloud-site-setup — the site whose Id becomes `SurveyInvitation.CommunityId`
- admin/email-templates-and-alerts — the Lightning email templates survey invitations require
- flow/record-triggered-flow-patterns — the case-closed trigger that fires `sendSurveyInvitation`
- architect/customer-effort-scoring — choosing CSAT vs NPS vs CES before you build the survey
