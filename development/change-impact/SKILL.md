---
name: change-impact
description: Map affected consumers and verification obligations before implementing or reviewing a change across interfaces, persistence or schemas, permissions, deployment or release boundaries, or independently failing downstream paths. Use for blast-radius and what-could-break questions. Do not use for ordinary local edits, generic code review, or a post-hoc risk narrative with no decision or verification consequence.
---

# Change Impact

Determine what the selected change can affect, which assumptions carry its
safety, and what evidence is needed for the current implementation or review
decision. Keep the investigation within the selected change; a residual finding
does not authorize successor work.

## Confirm The Gate

Apply impact mapping when a change crosses a material contract or creates
independent failure paths: public interfaces and wire formats; persisted data,
caches and migrations; authorization and trust boundaries; or build, packaging,
deployment and lifecycle behavior. An unchanged function signature does not
establish unchanged behavior for its consumers.

Materiality depends on independently failing consumers, deployed versions,
readers and writers, or lifecycle obligations that need separate proof. A branch
count or large diff alone does not establish it. Skip the full map for a local
change behind unchanged behavior contracts whose focused checks cover the
consequences. An explicit blast-radius question may end with that bounded
finding; do not invent cross-boundary risks to fill a report.

## Map The Reach

1. Bind the exact proposed change or diff to its repository, base and candidate
   revision or worktree state. Describe the relevant before/after behavior and
   the decision being supported. A proposal's intent is not proof of what an
   existing patch does.
2. Use the repo-declared retrieval lane that matches the evidence: `jcode` for
   definitions and callers, `jdocs` for authored contracts and runbooks, and
   `jdata` for material tabular evidence. Where those tools are unavailable,
   inspect the relevant current files or runtime evidence directly. Keep index
   coverage and freshness attributable to the selected source; do not sweep all
   lanes or connectors after a miss.
3. Trace the changed behavior across concrete boundaries. Symbol callers may
   miss serialized data, configuration, generated code, lifecycle ordering,
   dependency versions, automation, and consumers in another runtime or repo.
   Follow these paths where the change or repository evidence gives a reason.
   For compatibility changes, include applicable old/new readers and writers,
   retained data, mixed-version operation, upgrade and rollback; reviewing only
   the final steady state can miss the actual break.
4. Separate reachability from failure: a consumer using the changed behavior is
   not itself a confirmed risk. For each material consumer or group sharing the
   same contract and proof, record the path, changed expectation, possible
   consequence, evidence location, and verdict: `confirmed risk` for a supported
   reachable failure; `cleared` for a specific concern ruled out by evidence;
   `unproven` when reachability or compatibility remains unresolved. Name the
   condition under which a failure occurs; do not invent likelihood estimates.
5. A no-match search establishes absence only in that query's inspected scope,
   not absence of consumers or safety. Name exclusions such as generated files,
   dynamic registration or unavailable downstream repositories when relevant.
   Clear a concern only when the inspected source or coverage can rule it out.
   Keep meaningful cleared checks visible alongside risks and coverage limits.

Stop tracing a path when the changed behavior cannot reach farther, a preserved
contract contains its effects, or further evidence lies outside the available
scope. Give that reason; report an unresolved boundary instead of claiming
exhaustive coverage. Expand a search only to resolve a named material gap.

## Verify The Critical Assumptions

Prioritize the few assumptions that could change the decision. Do not force a
fixed number or omit another independent critical obligation. Connect each to
the consumer and failure it governs, the evidence already available, and any
remaining check.

Choose proof to match the claim. Source, contract and version evidence may
settle reachability or a compatibility guarantee. Behavioral claims may need a
focused test or probe exercising the actual boundary; rollout or lifecycle
claims may need the relevant runtime and version combination. Include success
and failure paths where they distinguish the suspected break. A test result
covers its exercised inputs and environment; it does not clear untested paths.

For each needed check, specify the input or scenario and expected observation
that would confirm or refute the concern. Reuse relevant existing results when
their code, inputs and environment still match. Run proportionate checks within
current authority; preserve read-only review and shared-runtime boundaries. Do
not create product or test edits merely to furnish a read-only review.

If evidence is unavailable or disproportionate, retain `unproven` and explain
whether the gap blocks the current decision or limits confidence, and why. Do
not demand runtime reproduction for a claim already settled by direct evidence,
or treat a reasoned explanation as proof of behavior that was never exercised.

## Close With Finite Obligations

Lead with what the evidence supports for this change and any material blocker.
Scale the output to the decision; use a consumer table when it makes distinct
paths easier to compare. Include the behavior difference, affected consumers,
critical assumptions, meaningful cleared concerns, and remaining uncertainty,
with exact source or runtime evidence.

**Verification obligations:** give the smallest finite set of remaining checks
or changes necessary for this selected change. Distinguish completed checks and
results from proposed checks; include the expected observation, required
environment or authority, and any proof that could not be run. Required project
checks still apply. Prioritize obligations by consequence and dependency on the
current decision, not by the number of files touched. Finish authorized work;
an impact report does not replace implementation or testing already requested.

Do not create a queue, next prompt, worker reservation, or follow-up task.
Workers and historical packets are evidence only. Use the current platform's
native orchestration within current task authority; this skill does not define
models, worker counts, MCPs, or a delegation scheme.

This skill adapts the pstack `blast-radius` pattern. See [LICENSE.txt](LICENSE.txt)
for source and license provenance.
