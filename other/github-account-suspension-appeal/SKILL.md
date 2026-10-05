---
name: github-account-suspension-appeal
description: Use when a GitHub account is suspended, restricted, limited, disabled, locked, or blocked and the user needs an appeal, support ticket, account limitation explanation, or form-field wording in English.
---

# GitHub Account Suspension Appeal

## Overview

Prepare concise, truthful English appeals for GitHub account restrictions. The goal is to help Support review the restriction, not to argue, threaten, confess unknown wrongdoing, or reuse a stale template.

## Intake

Collect only facts the user can stand behind:

- restricted account username
- visible error text, such as `Account suspended` or a Terms of Service notice
- rough inactivity period, such as `about two months`
- identity/context, such as being a student with exams, coursework, internship work, travel, or other ordinary reasons for not logging in
- what changed today: tried to log in, resume school/project work, or connect a service
- whether the user is willing to verify account ownership or provide more information

If a fact is missing, omit it or ask for it. Do not invent repository activity, dates, organizations, school names, locations, or previous compliance history.

## Form Fields

For GitHub Support forms, map intent to fields this way:

| Field | Preferred answer |
|---|---|
| Subject | Include the username and appeal intent, e.g. `Appeal for Suspended GitHub Account: <username>` |
| Please describe your account limitation issue | Explain the restriction, the inactive period, the student reason, lack of known violation, and willingness to verify |
| Username associated with the restricted account | The exact username only |
| Need help removing domains or content from a repository? | Usually `No` for account suspension appeals |
| Type of Issue | Prefer an account-access or restricted-account option if present; if forced between error and API rate limit, choose the error/bug option, not API rate limit |

Use the current form labels if they differ. Do not overfit to old GitHub UI wording.

## Writing Rules

- Write in calm, respectful English.
- Put the username in both the subject and first paragraph when known.
- Say the account is suspended or restricted based on what the user saw.
- Mention the student context only as a plausible reason for inactivity, not as a demand for special treatment.
- Use `about two months` or another approximate period unless the user provides exact dates.
- Include `willing to verify` ownership or provide additional information.
- Ask GitHub to review and explain the restriction.
- Do not admit wrongdoing unless the user explicitly confirms it.
- Do not claim the account was hacked unless the user has evidence.
- Do not claim exact dates unless provided.
- Do not invent evidence, ticket numbers, school names, repositories, or support history.

## Variation Rules

Always generate a fresh draft each time.

- Do not reuse the same opening. Rotate between openings like `I am writing to appeal...`, `I would like to request a review...`, `I recently discovered...`, or `Could you please review...`.
- Rotate sentence order: sometimes lead with the restriction, sometimes with the username, sometimes with the student/inactivity context.
- Vary the subject line while preserving meaning:
  - `Appeal for Suspended GitHub Account: <username>`
  - `Request to Review Account Restriction for <username>`
  - `Suspended Account Appeal - <username>`
  - `Account Access Review Request: <username>`
- Vary phrasing for uncertainty:
  - `I am not aware of any activity that would violate GitHub's policies.`
  - `I do not know what triggered the restriction.`
  - `If there was a security or policy concern, I would appreciate guidance.`
- Vary the close:
  - `I am happy to provide any verification needed.`
  - `Please let me know if you need additional information from me.`
  - `I would appreciate a review of the restriction and any next steps.`

Keep the facts stable while changing phrasing. Randomness means varied wording and structure, not changed claims.

## Output Contract

Return exactly the fields the user needs, unless they ask for a full ticket:

```text
Subject:
...

Please describe your account limitation issue:
...

What is the username associated with the restricted account?
...
```

When the user asks about form choices, answer the choice directly first, then give one short reason.

## Common Mistakes

- Treating a suspension appeal as a bug report without asking for review.
- Choosing API rate limit for an account restriction.
- Saying `Yes` to domain/content removal when the user only wants account access restored.
- Writing a generic template that omits the username.
- Repeating the same appeal text for multiple accounts.
- Overexplaining student status instead of keeping it as context.
- Promising future behavior or admitting a violation the user did not confirm.
