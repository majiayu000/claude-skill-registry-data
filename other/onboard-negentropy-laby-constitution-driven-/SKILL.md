---
name: onboard
description: "Generates a contextual onboarding document for a new contributor or agent joining the project. Summarizes project state, architecture, conventions, and current priorities relevant to the specified role or area."
argument-hint: "[role|area]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write
model: haiku
---
Read and apply `docs/COLLABORATIVE-DESIGN-PRINCIPLE.md`,
`standards/evidence-lifecycle.md` and `standards/notes-adr-sync.md` for scoped
authority, exact evidence and decision ownership. Existing named authority
continues; analysis is read-only and report-only excludes input/index/state writes.


## User Guide

- When to use: Generates a contextual onboarding document for a new contributor or agent joining the project. Summarizes project state, architecture, conventions, and current priorities relevant to the specified role or area.
- Inputs: Command arguments: `/onboard [role|area]`; project artifacts referenced below; user decisions and approvals before writes.
- Outputs: Primary artifacts, reports, or conversation guidance described below; write files only after user approval.
- Memory-bank writes: None.
- Next steps: Follow the workflow hand-off or next-step guidance below; recommendations do not auto-run and require explicit user command/approval.

## Purpose Routing before Contributor Onboarding

Apply the purpose rule to skills, independent agent/role definitions, native
configuration containing instruction bodies and their exclusive references/overlays.
A Target's development-only role stays local-only even without invoking a skill;
TOML, developer_instructions fields and native loading give no exception. Real
product-use agents follow actual product rules. Independent configuration must be
independent of development instructions/role packages and carry no such body;
a native loader of developer roles is not an independent configuration consumer.

Read `standards/skill-purpose.md`: using delivered functions differs from developing
this project. Contributor/agent orientation below is development support; its body/
exclusive references/overlays stay local-only in a Target even if tailored/native.
Generated project orientation documents follow their own rules. Product-user
onboarding should use actual delivered instructions/capabilities rather than
contributor development steps. Mixed skills must split; packaging gives no exception.

## Phase 0: Domain Routing

Read concept bodies and `standards/technical-preferences.md` domain/capability
evidence. Game keeps vision/pillars/engine/assets/playtests; Product uses user
promise/API/CLI/data/auth/architecture/workflows. Missing concepts never default
Game. Disclose Unknown/conflicts; neutral orientation continues.

## Phase 1: Load Project Context

Read actual runtime root guidance and canonical `INSTRUCTIONS.md` where available,
`standards/technical-preferences.md`, declared stage, active sprint/Story bodies
and established session context. Missing runtime copies do not imply missing
governance; disclose source gaps and retain supported partial guidance.

Read the actual selected installed role definition if a role is specified. CDD
Source may read its canonical owner; a Target must not restore a general agent
mirror for this lookup. Report missing/unknown observations when unavailable.

---

## Phase 2: Scan Relevant Area

- For programmers: scan `src/` for architecture, patterns, key files
- For designers: scan `design/` for existing design documents
- [Game] For narrative: read `design/narrative/` world-building/story docs
- For QA: read actual tests/QA evidence; counts do not prove coverage/execution.
- [Product] Read relevant CDD user promises/contracts, surface profile, API/CLI/
  data/auth/workflow docs and `docs/reference/[stack]/VERSION.md`.
- [Game] Read applicable engine references, art bible/assets, pillars and playtests.
- For production: scan `production/` for current sprint and milestone

Read recent changes (git log if available) to understand current momentum.

---

## Phase 3: Generate Onboarding Document

```markdown
# Onboarding: [Role/Area]

## Project Summary
[Game vision/player experience or Product user promise/workflow; state declared,
observed/candidate and verified qualification separately]

## Your Role
[What this role does on this project, key responsibilities, who you report to]

## Project Architecture
[Relevant architectural overview for this role]

### Key Directories
| Directory | Contents | Your Interaction |
|-----------|----------|-----------------|

### Key Files
| File | Purpose | Read Priority |
|------|---------|--------------|

## Current Standards and Conventions
[Relevant current root/standard and canonical role guidance; source metadata
is not proof of runtime model/tools/memory behavior or completed agent execution]

## Current State of Your Area
[What has been built, what is in progress, what is planned next]

## Current Sprint Context
[What the team is working on now and what is expected of this role]

## Key Dependencies
[What other roles/systems this role interacts with most]

## Common Pitfalls
[Things that trip up new contributors in this area]

## First Tasks
[Suggested first tasks to get oriented and productive]

1. [Read these documents first]
2. [Review this code/content]
3. [Start with this small task]

## Questions to Ask
[Questions the new contributor should ask to get fully oriented]
```

---

## Phase 4: Save Document

Present the onboarding document to the user.

Default output is conversational. Reuse covered exact onboarding path/effect;
if saving is requested without coverage, show draft and ask "May I write this to
`production/onboarding/onboard-[role]-[date].md`?" Write only that document.
Report-only excludes checkpoint/index/state; declined saving/review-only writes nothing.

---

## Phase 5: Next Steps

Verdict: **ONBOARDING COMPLETE** for produced orientation, disclosing omissions
and save outcome; it does not certify project/Story/runtime qualification.
Unavailable required sources leave affected orientation BLOCKED with useful
partial guidance retained; do not call the missing result complete.

- Share the onboarding doc with the new contributor before their first session.
- Run `/sprint-status` to show the new contributor current progress.
- Run `/help` if the contributor needs guidance on what to work on next.
