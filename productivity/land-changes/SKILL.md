---
name: land-changes
description: Land requested changes, inspect available landing workflows, or manage repository landing preferences. Use for "land it", "ship this branch", or "push to main".
argument-hint: "[--inspect] [--via=<method>] [--skip=<action>] [--bypass=<gate>] [--after=<action>] [defaults controls]"
---

# Land changes

Use the destination's landing procedure and the user's choices to publish the
requested change and complete its authorized follow-ups. Inspecting, discussing,
or editing this skill authorizes no landing.

## Resolve scope and state

From the conversation, identify the change, source checkout, destination, target,
and requested stopping point. Before publication, verify the publishing identity
and effective remote destinations; source and destination may differ.

Inspect the full diff, uncommitted work, dependencies, PR/stack metadata, and any
work already completed. Preserve unrelated changes and isolate preparation when it
would disturb them. Prefer one integration commit where the selected method allows.

Read [choices and preferences](references/preferences.md) before acting. Resolve
invocation arguments and applicable saved choices there. Show and reset requests
end after preference handling. `--inspect` makes no checkout, check-run,
preference, or publication changes.

An action completed earlier does not request a new change. Record the intended
scope and the outcomes still authorized; that defines when this run is complete.

## Discover the destination's workflow

Treat a **method** as the publication route, an **action** as work to perform, and
a **gate** as evidence required before proceeding. The user may name outcomes
without using these categories.

Follow the destination's guidance and inspect the evidence that applies:

- Contribution or agent instructions and the repository landing procedure.
- Task definitions, selected validation, and effective Git/tool hooks.
- Live host policy, available caller capabilities, and existing PR, queue, or
  stack state.
- Automation caused by publication, including follow-on workflows,
  release/deployment jobs, environments, and available integration metadata.

For GitHub, follow [host evidence](references/github-review-evidence.md). For an
unfamiliar mechanism, read its native help and official documentation. When the
repository's convention remains unclear, read [review history](references/review-history.md).
History can inform a recommendation; it cannot grant an exception or follow-up.

Use names from the destination, qualified when necessary. For every relevant
choice, establish its mechanism, dependencies, controls, affected scope, and
completion evidence. Mark each evidence source inspected, inapplicable, or
unavailable, and keep important unknowns or conflicts visible. Capability does
not grant user authorization; authorization does not make a capability available.

For a landing request, inspect the chosen route and its dependencies rather than
cataloguing unrelated routes. For `--inspect`, show configured choices,
alternatives that need setup, and unknowns with their sources and controls;
recommend a route and stop. Discovery is complete when every relevant source is
accounted for and every requested outcome has a procedure or a named blocker.

## Resolve choices and gates

Apply explicit choices, applicable standing decisions, and valid saved preferences
before defaults. Use the selectors or equivalent natural language in
[choices and preferences](references/preferences.md). Resolve conflicts by
scope and recency.

Without an overriding choice:

- Use the established route that meets policy without a bypass. Resolve material
  route ambiguity before publishing.
- Run relevant repository checks and hooks. A failure blocks by default; retain
  checks explicitly marked informational. Wait for required evidence, not
  unrelated or informational CI.
- Run manual follow-ups only when explicitly requested or covered by a saved
  preference scoped to this change, host/environment, and effect.

Record each selected action and gate, whether it will run or be skipped, whether
it will be enforced or bypassed, its waiting behavior, and the source of that
decision. For every bypass or follow-up, cite the instruction or saved key that
covers its scope. Include effects triggered automatically by publication. If an
effect lacks authorization or conflicts with a user constraint, find an authorized
route that avoids it or resolve the decision before publishing. A no-deployment
constraint requires evidence before publication that the route avoids deployment;
publishing and then watching for deployment is not proof.

Skipping a check preserves its known result; it does not convert failure to pass.
Enforce each applicable gate unless a scoped exception covers it and the actor
has a usable bypass. Report informational failures separately. Shared protection
changes, new privileges, and history rewrites each need explicit scope.

Reuse decisions that still cover the work and resume unfinished authorized
actions without asking again. A completed apply for one change does not authorize
an apply for another. The resolved plan, including follow-up scope and source,
governs execution. If new evidence changes a choice, revise the plan explicitly.

Resolve all choices or mark them as blockers. Continue independent preparation
while a blocker is being resolved; publication waits until its blockers are clear.

## Prepare and publish

For a direct update, follow [direct Git landing](references/direct-git.md). For a
PR, queue, stack, or other method, follow the repository's or host's procedure.
Preserve attribution and PR/stack relationships. Run selected actions on the final
candidate and record their results. Finish independent preparation before asking
for an unresolved publication decision.

Immediately before publication, verify the scope, destination, live policy, and
candidate. Every applicable gate needs valid evidence or a usable authorized
exception, and every resulting effect must fit the resolved plan. If the target
or candidate changed, refresh affected evidence and choices while retaining
decisions that remain in scope. After an uncertain response, inspect remote state
before retrying.

Publication is complete only when the live destination contains the intended
change. For a direct push, verify the prepared commit or its ancestry. For a
server-created commit, verify the source revision, integration commit, and
intended diff from the method's result metadata. PR or queue submission is an
intermediate result unless the user requested it as the stopping point. Report a
policy rejection as a rejection, then resolve an authorized route.

## Complete authorized follow-ups

Safely synchronize local checkouts. For each selected follow-up, read its
repository runbook and confirm that its authorization, effect scope, and
published revision or artifact still match the plan. Perform only the remaining
authorized work. Verify actual activation when command success alone is
insufficient. After an uncertain outcome, inspect state before repeating a side
effect.

Report publication, local synchronization, validation, CI, and follow-ups
separately as passed, failed, skipped, pending, or unknown. Name bypassed gates
and unrequested follow-ups. Keep branches and worktrees unless cleanup was
requested. Finish when every requested outcome is verified or its exact blocker
is reported.
