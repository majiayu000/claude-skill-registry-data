---
name: webdev-feedback
description: 'File WebDev bugs and ideas in GitHub with ownership, duplicate and privacy checks. Excludes fixes and automatic reporting.'
id: 'agents.skills.webdev-feedback.skill'
title: 'WebDev Feedback'
doc_type: 'skill'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'webdev-feedback'
tags:
    - 'agents/skill-package'
    - 'agents/skill'
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[skills/webdev-feedback/references/issue-publication]]'
depends_on:
    - '[[AGENTS]]'
---

# WebDev Feedback

## Purpose

Turn an explicit feedback request into one useful GitHub issue, using the
available conversation and verified evidence. This is an agent-run workflow
through existing tools, not a background reporter or a shared-token service.

## When To Use

- The user asks to report, file or record a WebDev bug in GitHub.
- The user asks to submit an improvement or feature request for WebDev.
- A request to record a bug needs ownership resolved between the Kit and host app.
- The user requests a draft of such a report; draft intent never permits posting.

## When Not To Use

- Merely discussing an idea, expressing frustration or discovering a defect.
- Fixing app code: use the matching implementation or debugger skill.
- Recording a private learning episode without publishing an issue.
- Diagnosing available subagents: use `project-onboarding-adapter` diagnostics.

## Required Context

Identify the publication intent, affected product, target owner/repository,
installed Kit version, client, task and available evidence. Use unknown for
unavailable metadata. Read `references/issue-publication.md` before any posting.
Do not require access to a learning database or the entire historical chat.

## Tool Contract

Use `project_files` and `repo_metadata` for available local facts and repository
reads. Resolve conditional `issue_publication` through a callable GitHub
connector or an already installed, authenticated CLI. Never install tools,
request a token in chat, change credentials or require repository code-write
access merely to file feedback. If publication is unavailable, return a complete
sanitized draft and the target issue URL; do not claim it was submitted.

## Workflow

1. Resolve ownership before searching or sending. Kit instruction, installation,
   adaptation, memory or routing feedback targets `ytvee-dev/webdev-agent-kit`.
   App bugs/features target the user's explicitly selected or verified host repo.
   A remote alone does not establish intent. Ask one short question only if the
   destination or publish-versus-local meaning remains ambiguous. Never send app
   feature requests to the Kit solely because WebDev is the active agent.
2. Distinguish an explicit request to publish from discussion or draft intent.
   A clear request to create an issue in a known destination is authorization;
   do not add a redundant confirmation. Announce the destination when posting.
   Preserve stricter client controls. An ambiguous "record this" is not consent
   to disclose private project details publicly.
3. Reconstruct the relevant sequence from all available conversation context:
   goal, constraints, actions, corrections, expected/actual outcome and checks.
   State missing context; do not invent messages or verified causes. Separate
   user reports, observed results, agent claims and causal hypotheses.
4. Build a self-contained minimal report using the reference fields. Remove
   private code, credentials, personal data, local absolute paths, chat dumps,
   database contents and private evidence links from a public report. Use neutral
   examples; do not fetch private memory solely to enrich public feedback.
5. Search open and closed issues in the selected repo using sanitized terms.
   Inspect likely matches. Return a matching issue and its state instead of
   silently duplicating, commenting or reopening it. For a closed issue compare
   version and reproduction: a distinct regression may warrant a new linked
   issue. If search is blocked, return the draft and state the missing check.
6. Submit once through the existing authenticated identity. Read back the issue
   when supported and verify destination, title, body and Unicode integrity.
   A successful POST with corrupted text is not a verified report. On an uncertain write
   result, reconcile recent issues before retrying; never blindly repeat a POST.
7. Return the actual issue URL and concise summary, or an explicit draft/blocker.
   An explicit no-learning/no-database instruction overrides optional linkage.
   If an opted-in local learning episode already exists, its own workflow may
   record the public issue URL in a new revision only when not excluded. Do not enable learning, alter
   its schema or sync memory as a side effect. Keep local episode IDs private.

## Output Contract

Final response: return only facts that affect the user's understanding, confidence, or next action. Omit empty fields and workflow narration.

Return created, existing, draft-only or submission-unconfirmed status, the exact
destination and URL when verified. Include missing evidence only when it affects
triage. Never invent an issue number or report draft generation as publication.

## Validation Gates

- Destination and publication intent are resolved before external writes.
- Duplicate search covers open and closed issues without exposing private terms.
- Public payload is minimal and sanitized, with unknowns and unrun checks explicit.
- No inferred cause is upgraded to fact from an agent narrative alone.
- No automatic labels, assignees, comments, reopening or feature implementation.
- No child agents are needed for routine reporting; only the coordinator posts.

## Trigger Evals

Should trigger:

- "File this WebDev adaptation bug in its GitHub repo."
- "Submit this idea for project-isolated memory as a WebDev feature request."
- "Draft a WebDev issue; do not publish it."
- "Record this bug as an issue; we discussed both the app and WebDev."

Should not trigger:

- "Fix the checkout validation bug."
- "Maybe WebDev could support more clients someday."
- "Save this session to my private learning database."
- "Check why my WebDev subagents are not active."

## Reference Map

- `references/issue-publication.md`: report fields, transport and recovery.
