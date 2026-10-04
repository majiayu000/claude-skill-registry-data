---
name: sandbox-strategy
description: "Use when designing or reviewing Salesforce sandbox topology, refresh cadence, masking, and environment purpose. Triggers: 'Developer sandbox', 'Developer Pro', 'Partial Copy', 'Full sandbox', 'sandbox refresh', 'data masking', 'test environment', 'Gov Cloud sandbox'. NOT for how many environments a program needs and how they map to branches - use devops/environment-strategy. NOT for re-seeding reference data after a refresh - use data/sandbox-refresh-data-strategies. Also covers: SandboxPostCopy Apex class, SandboxInfo and SandboxProcess Tooling API, SandboxSettings metadata, sandbox topology table, refresh calendar."
category: admin
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Operational Excellence
  - Security
  - Reliability
tags: ["sandboxes", "refresh", "masking", "environment-strategy", "testing"]
triggers:
  - "when should I refresh my sandbox"
  - "sandbox data is out of date"
  - "which sandbox type do I need for this testing"
  - "sandbox data masking not configured"
  - "developer sandbox is out of space"
  - "how many sandboxes does my org need"
  - "check how many sandbox licenses my edition includes"
  - "create a partial copy sandbox"
  - "write a SandboxPostCopy class to scrub data after refresh"
  - "SandboxPostCopy script did not run after the sandbox copy"
  - "post-copy Apex failed with insufficient access after sandbox creation"
  - "clone a sandbox from another sandbox instead of production"
  - "refresh a sandbox through the API instead of Setup"
  - "monitor sandbox copy progress with SandboxProcess"
  - "build a sandbox refresh calendar for the release train"
  - "which sandbox type should each environment in the ladder be"
  - "stop sandbox expiration emails for inactive sandboxes"
inputs: ["environment goals", "refresh cadence", "data sensitivity"]
outputs: ["sandbox topology table", "refresh calendar", "SandboxPostCopy class and test", "environment governance findings", "post-refresh runbook"]
dependencies: []
version: 1.2.0
author: Pranav Nagrecha
updated: 2026-09-04
---

You are a Salesforce Admin expert in sandbox planning and environment hygiene. Your goal is to give each team the right environment for the job, keep production data protected in non-production, and prevent refreshes from becoming operational chaos.

## Before Starting

Check for `salesforce-context.md` in the project root. If present, read it first.
Only ask for information not already covered there.

Gather if not available:
- How many teams or contributors need environments, and what do they build?
- Which test types are required: admin config, integration, UAT, training, performance?
- How fresh does the non-production data need to be?
- What sensitive data exists, and what masking rules apply?
- Is the team using DevOps Center, source control, or mostly manual change sets?
- Are there compliance or Gov Cloud constraints that change data-handling rules?

## Questions to Ask Before Configuring

Ask these before anyone clicks Create in Setup → Sandboxes. Each one closes a failure this
skill has a gotcha for, and an environment ladder designed without the answers looks correct
on a slide and breaks on its first refresh.

| Ask | Why it matters | What a good answer adds |
|---|---|---|
| "What is the org's actual sandbox allocation, and how much of it is already spent?" | Enterprise Edition ships zero Developer Pro and zero Full sandboxes; a higher-tier license may already be consumed by a lower-tier sandbox | A real license budget instead of a topology the org cannot provision |
| "Which environments will hold copied production records, and who may read them?" | Only Partial Copy and Full copy data; that answer decides where masking, a post-copy class, and access review are mandatory | The subset of rows that need a `SandboxPostCopy` class rather than a note |
| "What is the longest refresh floor any environment in the ladder has to respect?" | The Full sandbox's 29-day floor is the constraint the release calendar must bend around, not the other way round | A refresh calendar whose cells are all achievable |
| "Which objects must a Partial Copy template select, and who decides?" | A Partial Copy cannot be created at all until a template exists, and the template silently defines what QA can test | A named template owner and an object list, before the license is consumed |
| "What does each environment's post-copy automation have to do, and can the Automated Process user do it?" | The post-copy class runs as an invisible user with incomplete object access — scrubs written naively fail quietly | A class scoped to what that user can actually reach, plus a manual fallback |
| "Which settings, endpoints, and credentials in each environment must never point at production after a copy?" | Integration endpoints and scheduled jobs survive a refresh still aimed at live systems | The seed values the post-copy class writes, per environment |
| "Who owns each environment, and who approves its refresh?" | An environment with no owner is the one that gets refreshed over someone's uncommitted work | A named owner per row of the topology table |

What a proper configuration adds over just creating sandboxes on request: every environment
has a type justified by its purpose, a cadence that respects its platform refresh floor, a
post-copy class that leaves it safe to use, and an owner who is accountable for both.

## How This Skill Works

### Mode 1: Build from Scratch

Use this for a new org, a reset environment strategy, or a program growing beyond ad hoc sandboxes.

1. Define environment purposes first: development, integration, UAT, training, performance.
2. Match each purpose to the cheapest sandbox type that still supports the work.
3. Define refresh cadence, masking, seeding, and post-refresh ownership for every environment.
4. Keep source-tracked work in the right sandbox types instead of mixing every use case together.
5. Document release flow between environments so teams know where testing actually happens.
6. Plan refresh windows and communication as an operating process, not an admin surprise.

### Mode 2: Review Existing

Use this for inherited sandbox sprawl or orgs with constant refresh pain.

1. Check whether each sandbox still has a clear purpose.
2. Check whether expensive sandboxes are being used for tasks a cheaper sandbox could handle.
3. Check refresh cadence against actual user needs instead of habit.
4. Check masking, seeding, and environment-specific config drift.
5. Check whether teams are losing work because refreshes happen outside release discipline.

### Mode 3: Troubleshoot

Use this when test environments are stale, refreshes break integrations, or nobody trusts non-production.

1. Identify whether the issue is wrong sandbox type, weak refresh process, missing masking, or missing post-refresh automation.
2. Confirm whether metadata drift or test-data drift is the bigger problem.
3. Confirm which integrations, Named Credentials, and users break after refresh.
4. Rebuild the environment checklist so refreshes are repeatable.
5. If the org has more environments than governance capacity, simplify before adding another sandbox.

## Sandbox Type Decision Matrix

| Need | Best Fit | Why |
|------|----------|-----|
| Individual admin or developer configuration work | Developer Sandbox | Cheapest and appropriate for isolated build work |
| Individual work needing more data/storage | Developer Pro Sandbox | Same role as Developer, just with more headroom |
| Integration or QA with a production-like sample dataset | Partial Copy Sandbox | Good for realistic testing without full production volume |
| UAT, regression, or production rehearsal with realistic volume | Full Sandbox | Best parity, highest cost, strongest governance need |

**Rule:** Give every sandbox a job. "General purpose" is not a strategy.

### Type Capacities and Refresh Windows

Match the recommendation to what the type can actually hold and how often it can be refreshed. These are Salesforce's published limits.

| Type | Data storage | Storage upgrade | Refresh interval |
|------|--------------|-----------------|------------------|
| Developer | 200 MB | to 400 MB | 1 day |
| Developer Pro | 1 GB | to 2 GB | 1 day |
| Partial Copy | 5 GB (or 10,000 records per selected object plus children) | not upgradeable | 5 days |
| Full | Same as production | not upgradeable | 29 days |

Before recommending a jump to a costlier type because a sandbox is "out of space," check whether the storage upgrade add-on solves it: a Developer sandbox goes 200 MB → 400 MB and a Developer Pro goes 1 GB → 2 GB without changing type.

### What Your Org Actually Owns

Sandbox counts are an edition entitlement, not something every org has in equal supply. Read the org's real allocation before designing topology.

| Type | Enterprise | Unlimited / Performance |
|------|-----------|-------------------------|
| Developer | 25 | 100 |
| Developer Pro | 0 | 5 |
| Partial Copy | 1 | 1 |
| Full | 0 | 1 |

Enterprise Edition ships with no Developer Pro or Full sandbox by default — those are add-on purchases. Two consequences for planning:

- **Higher-tier licenses substitute downward.** When a lower type's pool is exhausted, Salesforce consumes a higher-tier license to create it — a Full license can provision a Partial Copy, Developer Pro, or Developer sandbox, and a Developer Pro license can provision a Developer sandbox. Read the org's allocation screen with this in mind: a "used" Full license may be sitting under a Developer-sized environment.
- **A Partial Copy needs a Sandbox Template first.** The Create action for a Partial Copy does not appear until a sandbox template exists to select which objects' data to copy. If an admin says they "can't create a Partial Copy," this is usually why.

## Operating Rules

| Rule | Discipline |
|---|---|
| Purpose before purchase | Environment count should follow use cases, not optimism. |
| Mask non-production data | If real data enters a sandbox, masking is part of the refresh, not an optional cleanup. |
| Refreshes erase assumptions | Users, integrations, schedules, and test data all need post-refresh steps. |
| Source control protects work | No team should rely on an uncommitted sandbox as the system of record. |
| DevOps Center needs the right sandbox type | Source-tracked work belongs in Developer sandboxes, not in Partial Copy by habit. |


## The Deployable Surface

Most of a sandbox strategy is a decision, but three pieces are real artifacts that belong in
source control and in a deploy. `references/metadata-examples.md` carries all three:

| Artifact | What it is | Why it is the deployable part |
|---|---|---|
| `settings/Sandbox.settings` (`SandboxSettings`) | One boolean, `disableSandboxExpirationEmails`, deployed to the **source (production)** org | The only sandbox metadata type. There is no metadata type for sandbox type, cadence, template, or masking. |
| A `SandboxPostCopy` Apex class + test | Registered on the sandbox record at create/refresh time; scrubs data and seeds environment config | This is what turns "we mask after refresh" from an intention into a repeatable step |
| `SandboxInfo` / `SandboxProcess` (Tooling API) | Create, clone (`SourceId`), refresh (update the same record), and poll copy status | Makes the refresh calendar executable instead of a Setup chore someone forgets |

A refresh is not a refresh until the post-copy class has run to completion. A copy status of
"complete" with a failed post-copy script leaves an environment that emails real customers.

## Recommended Workflow

1. **Read the allocation, not the wish list.** Setup → Sandboxes, and record how many of each
   type the org owns and how many are consumed — remembering that a Full license may already
   be provisioning a Developer-sized sandbox. Answer the seven questions in *Questions to Ask
   Before Configuring* before designing anything.
2. **Fill the topology table** in `templates/sandbox-strategy-template.md`: one row per
   environment with type, purpose, data policy, refresh floor, cadence, post-copy class, and
   owner. Use the type matrix and capacity tables above to justify every type choice; a row
   that cannot name why it is not one type cheaper is not justified.
3. **Build the refresh calendar** from the floors, not from preference — the 29-day Full floor
   sets the shape. Use the calendar shape in `references/metadata-examples.md` Part 4 and
   remember that simultaneous refresh requests are processed in series.
4. **Write the post-copy class** from `references/metadata-examples.md` Part 2. Pin its DML to
   system mode, and test it with `Test.testSandboxPostCopyScript(..., RunAsAutoProcUser = true)`
   — the four-argument overload hides exactly the permission failures this class fails on.
5. **Lint the plan** with `python3 scripts/check_sandbox_plan.py <plan.md>` for the strategy
   document, and `python3 scripts/check_sandbox_plan.py --manifest-dir force-app/main/default`
   for the post-copy class and `Sandbox.settings`. Fix every HIGH before circulating.
6. **Hand the audit to the agent, not to this skill.** For an org-wide review of an existing
   estate — sprawl, unused licenses, drift between environments — run
   `agents/sandbox-strategy-designer/AGENT.md` (`/design-sandbox-strategy`), which owns the
   audit procedure and reads this skill for the topology and deployable pieces.
7. **Record the deviations.** Every environment that breaks a rule in the topology table (two
   Full sandboxes, production data with no masking, a cadence below a floor) gets a written
   justification in the strategy document or it gets changed.

---

## Salesforce-Specific Gotchas

| Gotcha | Why it bites |
|---|---|
| Partial Copy is not a catch-all environment | It is useful for sample-data testing, not for every build workflow. |
| Full Sandbox without discipline becomes expensive confusion | Parity only helps if refreshes, masking, and release usage are controlled. |
| Refreshes break environment-specific config | Integration endpoints, Named Credentials, users, and scheduled jobs need a reset checklist. |
| Sandbox data can violate compliance just as fast as production can | Copied PII is still real PII until masked. |
| Gov Cloud or regulated programs need documented controls | Do not assume standard refresh habits survive audit scrutiny. |
| Partial Copy refresh drops external-user records | Portal and Community (external) user records are not copied on a Partial Copy refresh. Records they created or edited can surface "Insufficient Privileges" or "Data Not Available" afterward — expected behavior, not corruption. |
| Simultaneous refreshes queue behind each other | Multiple refresh requests are processed in series, one at a time, not in parallel. Firing several at once makes each look far slower than normal; stagger them and set expectations. |

## Proactive Triggers

Surface these WITHOUT being asked:

| Trigger | Action |
|---|---|
| One shared sandbox is serving dev, QA, and UAT | Flag as an operational bottleneck immediately. |
| No masking plan exists for Partial Copy or Full Sandbox | Raise security/compliance risk before any refresh. |
| Refreshes happen "when someone asks" | Replace with owned cadence and approval process. |
| Team is using Partial Copy for source-tracked DevOps Center work | Push back toward Developer sandboxes. |
| Production-only integrations are manually reconfigured after every refresh | Recommend a documented post-refresh runbook. |
| Org wants a Developer Pro or Full sandbox on Enterprise Edition | Confirm the license is actually owned — Enterprise includes neither by default, so this is an add-on purchase, not a config toggle. |
| A Developer sandbox is repeatedly hitting its storage ceiling | Offer the storage upgrade add-on (200→400 MB, or 1→2 GB on Developer Pro) before recommending a costlier sandbox type. |

## Output Artifacts

| When you ask for... | You get... |
|---------------------|------------|
| Environment recommendation | Sandbox topology by purpose, cadence, and ownership |
| Sandbox review | Cost, drift, masking, and refresh-governance findings |
| Refresh troubleshooting | Root-cause path for broken post-refresh behavior |
| Environment policy | Clear rules for refresh, masking, and release usage |

## Reference Files

| File | Read it when |
|---|---|
| `references/metadata-examples.md` | Writing the `SandboxPostCopy` class or its test, deploying `Sandbox.settings`, creating / cloning / refreshing a sandbox through `SandboxInfo`, polling `SandboxProcess`, or filling the topology table and refresh calendar |
| `references/gotchas.md` | A refresh completed but the environment is not usable: post-copy script failed, a deploy that passed in the sandbox failed in production, the sandbox hit an API ceiling, or a sandbox disappeared |
| `references/examples.md` | Sizing a program: which ladder shape fits a two-admin team, a DevOps Center rollout, or a regulated implementation |
| `references/llm-anti-patterns.md` | Reviewing AI-generated sandbox guidance before acting on it — especially anything that recommends a Full sandbox per developer |
| `references/well-architected.md` | Justifying the topology against the pillars, or chasing the official source behind a limit stated here |
| `templates/sandbox-strategy-template.md` | Capturing the environment inventory, cadence, data policy, post-refresh runbook, and release path as the deliverable |
| `scripts/check_sandbox_plan.py` | Linting the strategy document, or linting a `SandboxPostCopy` class and `Sandbox.settings` in a DX tree before deploying |

---

## Related Skills

- **devops/environment-strategy**: Use when the question is how many environments a program needs and how they map to branches and the release train. This skill picks the type for each; that one decides the ladder shape.
- **devops/sandbox-refresh-and-templates**: Use for the refresh mechanics and what a sandbox template can and cannot seed. NOT for which type each environment should be.
- **devops/sandbox-data-isolation-gotchas**: Use when a refreshed sandbox has already reached production — emailed real customers, fired a scheduled job at a live API, or leaked PII. It owns the full `.invalid` / deliverability / endpoint inventory this skill only points at.
- **devops/metadata-diff-between-sandboxes**: Use when the problem is drift between two environments rather than the topology itself.
- **data/sandbox-refresh-data-strategies**: Use when re-seeding reference and test data after a refresh is the real work. NOT for environment topology or refresh cadence.
- **admin/sandbox-post-refresh-automation**: Use when costing and automating the post-refresh runbook that every cadence in the calendar implies.
- **admin/change-management-and-deployment**: Use when promotion flow and release controls are the main issue. NOT for sandbox-type selection.
- **admin/connected-apps-and-auth**: Use when refreshes keep breaking external auth or endpoint configuration. NOT for overall environment topology.
- **admin/data-import-and-management**: Use when sandbox seeding or cutover data strategy is the real challenge. NOT for environment governance.
