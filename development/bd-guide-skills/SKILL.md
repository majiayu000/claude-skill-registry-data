---
name: bd-guide-skills
description: Guide a person without coding experience through planning, building with an AI assistant, testing, and deploying a small app. Use for a first app or a bounded beginner build, with plain-language choices, working previews, acceptance evidence, recovery and ownership. Adapt to the chosen stack and existing project.
---

# Brownsmith beginner app guide

Help the owner build a small app they can inspect and operate. The default teaching example is a one-person request tracker using fictional records; use the owner's chosen idea when they have one. Preserve the project's existing framework and working behavior. This skill helps with a first complete workflow, rather than treating a generated interface as a finished production system.

## Start from the actual project

Find out who uses the app, the task they need to complete, what data it handles, who may view/edit/delete it, how long records are kept, the available workspace, budget, and whether this is a learning demo or a live service. Inspect an existing repository and its instructions before changing it. Ask about missing choices that affect the outcome, then continue work that is already clear. Explain technical terms when they become necessary rather than giving the owner a vocabulary test.

Offer a browser builder with source access or a local coding assistant according to the user's chosen tools and ability to maintain the result. Inspect installed runtimes and framework documentation before specifying setup commands. Keep source, hosting, domain and data accounts under the owner's control. Show commands with the folder, purpose, expected output and stop/recovery step. Never imply the owner must know a programming language before describing and checking behavior.

## Use the relevant stage

- **Plan:** read [planning.md](references/planning.md). Produce a short brief with one complete workflow, fields, allowed states, acceptance checks, assumptions, costs and deferred scope. Compare a process change or existing tool where appropriate. Do not impose the sample app over the user's goal.
- **Build:** read [building.md](references/building.md). Get one working preview, then implement one observable behavior at a time. Save recoverable working versions, explain storage choices, and reproduce defects before fixing them. Distinguish a browser-only demo from shared server-backed data.
- **Test:** read [testing.md](references/testing.md). Use the agreed acceptance cases, negative cases and permission boundaries. Separate user inspection from build/type/lint checks and automatic tests. Record actual evidence and untested areas.
- **Deploy and operate:** read [deployment.md](references/deployment.md). Match the host to the actual application runtime/output. Verify the temporary live URL before custom-domain work; retest, identify rollback, restore backups where data exists, and hand over operating/cost notes.

Load only the stages needed for the current task. A request to repair an existing deployed app does not require recreating the planning stage. For an end-to-end first build, carry the same brief and acceptance cases through all four stages.

## Make the result reviewable

At each stage, present the working artifact and the decision needed next: brief, preview, test evidence, or deployment handoff. State what passed, what failed, and what was not checked. Do not invent screenshots, results, client experience, deployments, costs or uptime. A syntactically valid build is not evidence of correct access rules or recoverable data.

For shared records, enforce permission rules at the authoritative server/database and test direct requests with two users and a signed-out session. Treat browser storage as device/origin-specific and vulnerable to clearing; it is not shared storage or backup. Keep secrets out of prompts, logs, screenshots, repositories and browser-delivered code. Explain which configuration can be public and which belongs in the protected server environment.

Use fictional data for learning and testing. Seek appropriate independent review when sensitive data, payments, consequential actions, or business-critical availability exceed what the owner can inspect and support. Define those boundaries from the actual app; do not turn every demo into a large enterprise project.

Honor the user's authorization. Building locally does not itself authorize live deployment, purchases, sending messages, production data changes or commits. Prepare a concrete preview and evidence before requesting any still-required release authorization. Preserve the last working release and name who will manage updates, failures, recovery and billing.

## Reusable artifacts

Keep these in the user's app project when useful, adapting filenames to its conventions: a build brief; an acceptance/test report with scenario, expected result, actual result, evidence and pass/fail; an operating note with owner, URL, source version, configuration names (no secrets), data recovery, costs and rollback. Keep them short enough that the owner can use them.

The public guide path is [planning](https://brownsmithdynamics.com/guides/mvp-building), [building](https://brownsmithdynamics.com/guides/ai-assisted-building), [testing](https://brownsmithdynamics.com/guides/testing), then [deployment](https://brownsmithdynamics.com/guides/infrastructure). This skill is self-contained; those pages provide optional reader-facing context.

Optional companion skills in the same repository include `nextjs-optimisation-skill` for Next.js projects, `website-analysis-skill` for a requested site review, and `website-seo-guardrails` for public-page discovery and migration checks. Use them only when relevant and available; do not require them to complete an ordinary app build.
