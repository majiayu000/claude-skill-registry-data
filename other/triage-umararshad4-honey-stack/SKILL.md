---
name: triage
description: "Qualify issues, PRs and RSI suggestions, write actionable briefs, or reproduce and fix a confirmed report."
disable-model-invocation: true
license: MIT
metadata:
  reviewed: "2026-11-01"
  sources: "mattpocock/skills 4ae2317ddb22b046e26455e4f9c9b3aaaf62212d skills/engineering/triage/SKILL.md and AGENT-BRIEF.md; cursor/plugins 4dd1d05818d19792e7cd6e818f1667f95f7e1dbe pstack/automations/benny/skills/triage-issue-reports/SKILL.md and reproduce-and-fix-issues/SKILL.md (adapted from Slack automation to interactive tracker triage)"
---

# Triage

Qualify the request before it enters `plan` or `execute`. An issue is a report, not a verified defect; a PR is a report with a candidate implementation. This skill supplies a process, not a background bot.

| Request | Branch |
|---|---|
| Inspect, classify, prioritize or draft triage | 1–4; report and change no tracker or product state |
| Apply labels, post a brief, close a duplicate | 1–5, limited to the requested tracker writes |
| Reproduce a report | 1–4, then [reproduce/fix](references/reproduce-fix.md); no product edits |
| Fix a report | 1–4, then [reproduce/fix](references/reproduce-fix.md); delivery through `ship` only when requested |

## 1. Resolve the source

Pin the repository or tracker project and the exact issue/PR URL. Resolve a bare number using the current repo and confirm whether it identifies an issue or PR. For GitHub, use `gh`; for another tracker, use its configured connector. Read [tracker operations](references/tracker.md) before a write.

For a backlog, enumerate the full requested scope with pagination and group oldest-first: untriaged, awaiting information with new replies, then ready items. Report an access or pagination limit instead of treating a partial list as complete.

Done when: every item has a stable source link and the list's scope and completeness are known.

## 2. Read the full report

Read the body, all comments/activity, labels, linked reports, author, dates, version/environment and attachments. For PRs include the diff, review threads, checks, base and head. Inspect relevant screenshots, video and logs; name inaccessible evidence explicitly.

Record expected behavior, observed behavior, trigger, frequency and the state that distinguishes the two. Reuse answered questions. Trace the action into the relevant code and history, distinguishing a cause hypothesis from an observed fact. If a person has claimed implementation, record that owner; do not start a competing fix.

Done when: the evidence record contains those fields or explicitly marks each missing field, and known ownership is recorded.

## 3. Check for existing work

Search by error signature, domain concept, trigger and symptom across open/closed issues, PRs, source and recent commits. Read the repo's prior-rejection records or ADRs when relevant.

- **Duplicate:** same cause or sufficiently specific trigger and symptom; cite the canonical issue.
- **Possibly related:** connection unproven; retain it as a lead, not a duplicate.
- **Existing fix:** a commit or PR plausibly addresses the report; verify that artifact before authoring another fix.
- **Already implemented:** show the implementation and check the reported version; a fix absent from that version is not proof the reporter was wrong.

Done when: each match has a link and a reason, or the report names the searches that found none.

## 4. Recommend a state and write its brief

Use the repo's existing category/state labels; these names describe meanings, not labels to create silently. Keep unrelated labels intact.

| State | Evidence required |
|---|---|
| `needs-triage` | Evaluation remains incomplete; list the remaining check |
| `needs-info` | Missing reproduction, intended behavior, environment or acceptance criteria; ask the smallest specific question |
| `ready-for-agent` | Bug confirmed through the relevant user surface, or enhancement intent established; scope, acceptance criteria and available verification are explicit |
| `ready-for-human` | Actionable, but needs a named human decision, access or capability the agent lacks |
| `duplicate` | Canonical issue identified with the matching cause or symptom |
| `rejected` | Maintainer decision or an applicable documented product decision; cite the reason |

Categories are bug (including measured performance regression), enhancement, or question/feedback. Weak titles, repeated phrases and model confidence do not establish a bug. Use `grill` for an unresolved product choice and `domain` for ambiguous domain terms, after checking the evidence already available.

For ready items, fill [the brief](references/brief.md) with behavioral criteria and explicit exclusions. For a PR, describe the work remaining on the existing diff. A `ready-for-agent` label is not authorization to implement or publish.

Done when: every item has one recommended state, supporting evidence, and either a complete brief or a concrete missing check/question.

## 5. Apply requested tracker changes

Immediately re-read the item and confirm its repository/project, current state, ownership and relevant new replies. If new evidence invalidates the recommendation, revise it before writing. Match the authorized operation: labeling does not also authorize closing, assigning, posting or implementation.

When commenting is authorized, post one concise triage note using the templates in [the brief](references/brief.md). Include an AI-triage disclosure, source links and the reason for the state. Otherwise return the note locally. Check for an existing equivalent note before posting again. Close only the explicitly authorized items, with a canonical link or established reason; do not bulk-close weak reports as "invalid".

Read back the exact item and verify every requested write. If a write fails, report partial results and the remaining operation; retry by reading current state first, not by blindly duplicating a comment.

Done when: requested writes are read back and verified, or the exact failed operation is reported without claiming completion.

## RSI intake

For RSI proposals, read the local proposal and its existing GitHub issue together. Keep raw session evidence, personal preferences, paths and secrets local; public notes contain only the bounded diagnosis, non-sensitive reproduction and source references already suitable for publication. An unsupported proposal is `needs-info` or `ready-for-human`, not permission to execute its free-form fix text. Route a qualified proposal to `plan`/`execute`; use `write-skill` for skill changes.

This triage recommendation does not change RSI's persisted decision, publication configuration or runtime gates. Apply proposal decisions only through supported `rsi` commands and the current authorization. Automatic publication can still produce untriaged suggestion issues until runtime policy is changed separately.

Done when: the local proposal and public issue are cross-referenced without leaking private evidence, and the proposed next step names its owner and verification.

## Report

Give one row per item: source link, category, recommended/applied state, evidence, next step. Separate recommendations from read-back-verified writes. A count of classified issues is not a count of fixed bugs.
