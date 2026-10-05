---
name: run-autonomous-workpacks
description: Use for authorized multi-step tasks that should be organized and completed as bounded, verifiable workpacks with fewer manual handoffs. Preserve scope, user changes, safety boundaries, dependencies, and evidence. Do not use for analysis-only, diagnosis-only, or trivial one-step requests.
---

# Autonomous Workpacks

Organize an authorized multi-stage task into bounded workpacks that can be executed, checked, recovered, and closed without losing the original scope.

> This skill governs work decomposition, execution boundaries, and verification. It does not prescribe message cadence, progress-report formats, commentary behavior, or subagent presentation; use Codex's native interaction behavior and follow any explicit instruction in the current user request.

## Mission contract

Before the first mutation, extract and preserve:

- the objective and observable done condition;
- the allowed files, systems, artifacts, and external actions;
- non-goals and forbidden side effects;
- authoritative inputs, assumptions, and facts that must be confirmed;
- verification requirements and evidence needed for closeout;
- stop conditions: `USER_ONLY`, `EXTERNAL_WAIT`, `UNAUTHORIZED_HIGH_IMPACT`, `MISSING_FACT`, or `FAILURE_UNRESOLVED`.

If the request is analysis-only or diagnosis-only, keep every mutation workpack out of scope. If a required fact is missing, gather safe evidence before choosing an implementation.

## Workpack cards

Give each workpack one independently verifiable objective and a disjoint write scope where possible. Record:

- ID and imperative name;
- objective and done condition;
- inputs and dependencies;
- exact allowed writes and explicitly untouched paths;
- risk and side-effect budget;
- checks and evidence source;
- recovery route for a failed check;
- status: `queued`, `active`, `blocked`, `verified`, `failed`, or `skipped`.

A documentation workpack must not silently edit product code. An installation or packaging check must use an isolated temporary location. Do not use a workpack card to smuggle in deployment, payment, publication, deletion, or unrelated cleanup.

## Dependency waves

Use this order unless the task facts justify a safer route:

```text
Task contract → workpack cards → dependency order
→ execute safe work → diagnose and retry local failures
→ verify the whole result → COMPLETE / PARTIAL / BLOCKED
```

1. **Discover:** read repository instructions, inspect the baseline, and freeze the scope boundary.
2. **Prepare:** create only the required branch, temporary locations, fixtures, or test inputs.
3. **Implement:** make the smallest coherent change inside the allowed write scope.
4. **Verify:** run focused checks, repository checks, and the original-condition test where available.
5. **Close:** inspect the diff and perform only explicitly authorized external actions after local evidence is sufficient.

Independent read-only checks or workpacks with disjoint writes may run concurrently when that reduces risk and does not weaken final verification. Delegation is optional; every delegated result still needs a clear done condition and main-thread verification.

## Authorization and stopping

Continue safe, reversible, in-scope work without another confirmation. Stop or mark the relevant workpack when the next action requires:

- login, MFA, private credentials, or a security access path the user must provide;
- permission from an external service or formal human approval;
- an unapproved irreversible, production, public, paid, destructive, or otherwise high-impact action;
- a material ambiguity with no safe default;
- a key fact whose absence makes the next mutation unsafe;
- a critical result that cannot be verified and has no trustworthy substitute;
- a legal, compliance, or safety decision that requires a human.

Authorization is not transitive. Permission to edit a repository does not authorize production deployment, public publication, account changes, paid actions, or data deletion. A successful login proves access, not approval for every action. Never request or paste a secret into a task record.

Use [decision-and-authorization-boundaries.md](references/decision-and-authorization-boundaries.md) for the decision table and factual blocker record.

## Failure, retries, and evidence

When a routine check fails:

1. preserve the command, exit code, and first relevant error;
2. classify the failure as content, environment, dependency, permission, or external state;
3. change one diagnosed cause or input;
4. rerun the smallest decisive check;
5. continue only when the workpack done condition is supported.

Do not repeat the same failing command without a changed diagnosis. A network timeout may receive one safe retry when the request is idempotent; authentication and permission failures are not retry invitations.

A changed file is not a test. A passing test is not CI. CI is not a build, preview, upload, release, or user acceptance. Use [verification-and-failure-handling.md](references/verification-and-failure-handling.md) and record missing proof as `unknown`.

## Required closeout state

Use one of these states for the whole mission:

- `COMPLETE`: every acceptance criterion has fresh, direct evidence;
- `PARTIAL`: useful work is verified, but a known, bounded, nonessential, or externally unobservable criterion remains open;
- `BLOCKED`: a required safe action cannot proceed without user input or an external state change.

The closeout record must distinguish local edits, tests, CI, build, preview, upload, merge, release, and user acceptance. Include changed artifacts, intentionally untouched scope, skipped checks, assumptions, risks, unresolved failures, and any required user input. Use [workpack-templates.md](references/workpack-templates.md) when a structured record helps.

## Red flags

Stop and re-evaluate when:

- the workpack has no observable done condition;
- a diagnosis-only request is being changed, deployed, uploaded, or published;
- a routine failure is repeated without a changed diagnosis;
- a successful login is treated as publication approval;
- separate write scopes overlap without a reason;
- a test, build, preview, upload, release, or acceptance claim lacks its own evidence;
- user changes, secrets, private identifiers, or unrelated files would be exposed or overwritten;
- a convenient nearby cleanup is being treated as part of the mission without authorization.

## Quick checklist

Before execution:

- [ ] Objective, scope, non-goals, side-effect budget, and done conditions are explicit.
- [ ] Required inputs and stop conditions are known.
- [ ] Workpacks have disjoint scopes, dependencies, recovery routes, and checks.

During execution:

- [ ] Safe work continues inside the authorized boundary.
- [ ] Each workpack records evidence and a precise status.
- [ ] Failures are diagnosed, bounded, and not hidden.
- [ ] Delegated work, if any, has an independent scope and is verified by the main thread.
- [ ] No out-of-scope edits, secret exposure, or silent authorization expansion occurs.

Before closeout:

- [ ] The diff contains only intended artifacts.
- [ ] Edited, tested, built, previewed, uploaded, merged, released, and accepted states are separate.
- [ ] Every claimed check has fresh evidence; unknowns remain visible.
- [ ] The closeout record is public-safe and accurate.
