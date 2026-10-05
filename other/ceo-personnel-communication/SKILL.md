---
name: ceo-personnel-communication
description: Use for internal personnel, performance, compensation, promotion, candidate, interview, and other people-sensitive communication where subject, recipient, audience, or visibility affects what may be said. Use ceo-message-triage for ordinary business messages without personnel sensitivity. Load the evidence or approval operation Skill that matches the request.
metadata:
  managed_by: ceo-agent-service
  version: 1
---

# CEO Personnel Communication

Load `ceo-personnel-communication` for a concrete employee, personnel, or
candidate matter where the information subject, recipient, audience, or
visibility affects what may be read, judged, or communicated. An explicit
request is not required: the agent decides whether the matter needs the
principal's handling from the current message, context, responsibility, and
available evidence.

## Audience Workflow

1. Identify the information subject: the person whose employment, candidate,
   or sensitive facts are being discussed.
2. Identify the intended recipient and the actual destination for any proposed
   communication. The subject and recipient may be different people.
3. Determine the authorized audience from supplied context or live evidence.
   Establish whether the recipient is the subject, has a relevant HR
   responsibility, or has another evidenced purpose and authorization.
4. Distinguish self-related information, internal personnel information,
   external candidate information, and ordinary business facts before deciding
   what evidence to read or what may be communicated.
5. Use only supported facts needed by that authorized audience. Do not invent
   compensation, performance, promotion, employment, health, leave, or other
   sensitive facts.

When the recipient asks about their own personnel information, the subject and
recipient are the same person. Use supported self-related facts without asking
who the subject is; do not infer facts or authorization for anyone else.

Load `dingtalk-contact` when current identity, organization, or HR
responsibility evidence is needed. Load `dingtalk-chat` before chat delivery.

## Specialist Composition

- Load `stardust-interview` for candidate evaluation and follow its evidence,
  role-fit, and interview workflow.
- Load `dingtalk-oa-approval` for approval work and follow its complete-material,
  decision, action, notification, and verification workflow.
- Load `dingtang-okr-review` only for an actual OKR review or scoring task.
  Ordinary OKR discussion, process coordination, or business discussion does
  not invoke the specialized scoring workflow.

Do not reproduce or replace those specialist workflows here. This Skill owns
only the personnel classification and audience decision that composes with
them.

## Classification Boundary

A person's name alone does not make a business fact personnel information.
Ownership, delivery, revenue, customer progress, project risk, and similar
work facts remain ordinary business facts unless the requested judgment is
about that person's employment, performance, compensation, promotion, leave,
role fit, or another personnel status.

## Behavior Cases

- `internal_performance_or_compensation`: Load `ceo-personnel-communication` and treat the employee as the subject.
- `hr_direct_chat_within_responsibility`: The recipient may receive the supported personnel information after HR responsibility and scope are established from live organization evidence.
- `non_hr_direct_chat_about_third_party`: Do not disclose unsupported sensitive details; provide only authorized supported facts or ask for the missing authorization or purpose.
- `external_candidate_evaluation`: Load both `ceo-personnel-communication` and `stardust-interview`.
- `personnel_oa`: Load both `ceo-personnel-communication` and `dingtalk-oa-approval`.
- `okr_review_or_scoring`: Load `dingtang-okr-review`; ordinary OKR discussion does not invoke that scoring workflow.
- `named_person_in_business_work`: Keep ownership, delivery, revenue, and project-risk facts as ordinary business facts unless the requested judgment is about the person's employment or personnel status.
