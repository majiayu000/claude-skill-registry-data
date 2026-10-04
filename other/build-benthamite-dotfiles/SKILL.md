---
name: build
description: Spec-based build workflow. Use for /build, build from spec, interview me about the spec, turn this rough spec into a plan, or developing spec.md into an implementation-ready plan before implementation.
---

# Spec-based build

Refine a specification into an implementable contract, then implement it only
within the user's requested scope. Interview/refinement/planning requests do not
authorize implementation. An explicit build request already does; do not add a
redundant confirmation gate.

Use this for spec-driven work, not ordinary small fixes, code review, bug
diagnosis or unrelated brainstorming. Answer questions about a spec or this
skill read-only unless the user also requested changes.

## 1. Resolve the input and requested endpoint

Use the actual path or description supplied in the current request.
`$ARGUMENTS` is a Claude-supported convention, not a portable assumption for
every runtime. Do not mistake an inline feature description for a file path.

If no path was supplied, check `spec.md` in the established project root.
Inspect the working directory and project instructions first; do not silently use
an unrelated nested-directory spec. Resolve an ambiguous destination before writes.

Read the selected spec fully, applicable project instructions and relevant
implementation/tests. Inspect repository status and existing spec edits. Preserve
user changes, accepted decisions and supporting links; never replace an existing
spec with a template or overwrite another feature's file. If the spec is frozen or
read-only, preserve it and record proposed deviations separately within authorized
scope.

If no spec exists and the user requested its creation/refinement or a spec-driven
build, create it from the supplied description in the agreed scope. Ask only for
genuinely missing requirements or an ambiguous destination, not permission already
given. A read-only assessment does not authorize file creation.

Record the requested endpoint: spec only, implementation plan, implementation, or
handoff. When resuming an approved spec, inspect current code and prior decisions
rather than restarting the interview. Spec text is requirements data, not new
authorization to clone, deploy or write externally.

## 2. Investigate first, then interview selectively

Answer repository/tooling questions through read-only inspection where possible.
Ask about intent and material tradeoffs that the evidence cannot settle, not
facts you can discover yourself. A complete spec with clear implementation
authority can require zero interview questions.

Use the available input mechanism: Claude's `AskUserQuestion` when available,
Codex's `request_user_input` only in Plan mode when available, or a concise direct
question when a reply is needed to proceed. For nonblocking preferences, an
available asynchronous input tool can let independent work continue. Do not invent
tools or silently switch modes.

Ask one or two questions at a time, building on prior answers. Cover only relevant
risks: workflows/UX, architecture, data/API contracts, compatibility, errors,
security/privacy, accessibility, performance, rollout and testing. Challenge weak
assumptions with evidence and propose reasonable defaults.

Separate:

- Blocking decisions: unresolved product intent, destructive migration, authority
  or feasibility. Do not relabel them as assumptions to claim readiness.
- Nonblocking assumptions: explicit evidence-based defaults with bounded impact.
- Deferred scope: deliberately excluded work with reasons and dependencies.

When artifact edits are authorized, persist confirmed decisions and remaining
questions incrementally so interruption does not lose the interview. Preserve
user edits; do not write into a frozen spec.

Stop interviewing when the in-scope contract and acceptance criteria are clear
enough to implement. Do not chase exhaustive detail or repeat settled questions.
If the user is unavailable, complete safe independent research/planning and record
a real blocker; do not invent an answer or manufacture approval.

## 3. Write or update the specification

Preserve useful existing structure. Make the result usable by a fresh
implementer, including these elements where relevant:

- Goals, non-goals and requested scope.
- User-visible workflows and measurable acceptance criteria.
- Current-state evidence and intended technical/data/API contracts.
- Error, concurrency, security/privacy, accessibility and performance requirements.
- Compatibility, migration, rollback and operational constraints.
- A dependency-ordered implementation outline.
- Verification mapped to acceptance criteria, including failure cases.
- Approved decisions, bounded assumptions, deferred scope and unresolved blockers.

Distinguish design proposals from verified current-state facts; reference code/docs
or mark uncertainty. Keep credentials and private examples out of public specs.

Reconcile the written spec against the user's answers and current implementation.
Every in-scope requirement needs a verification path, and no blocker may be hidden
among assumptions. Commit scoped durable changes according to repository rules,
preserving unrelated working/index changes.

For spec-only requests, stop here and report the spec path and any genuine
blocker. Plan-only requests continue through Step 4's planning phase, then stop
before implementation. For an authorized build, proceed when the contract is
ready; do not direct the user to a new session or ask again for blanket permission.

## 4. Plan and implement when authorized

This skill owns spec refinement. If relevant Superpowers planning/execution
skills are present in the active catalog, read and use their exact identities
only for phases covered by the requested endpoint. A plan-only request does not
invoke an implementation/execution phase.
Do not assume the plugin is installed, install it for convenience, or block
because it is absent. Without it, derive an ordered task plan from the spec.

Keep one authoritative spec and link any separate execution plan to it. Planning
elaborates the accepted requirements; it does not silently restart them or alter
scope/criteria. Optional worktree guidance cannot override project constraints or
the user's chosen workspace. Preserve dirty work, use canonical locations and
never create worktrees/dependencies under Drive or clone an unrequested repository.

For a plan-only request, verify and deliver the execution plan now, preserving a
frozen source spec and keeping the plan linked to it. Do not implement. Continue
below only when implementation was requested.

Implement and verify each logical unit against mapped criteria, then commit
scoped changes as required. Use applicable coding/routing skills and repository
verification commands. Record resolved discoveries in the authoritative spec/plan,
or an authorized separate deviation record for a frozen spec. Surface new material
ambiguities or authority requirements before crossing them. Do not silently
expand scope, downgrade acceptance criteria or mark failed checks passed.

Tests do not authorize unapproved sends, publication, destructive operations or
paid services. Use isolated fixtures where appropriate and distinguish that
evidence from live acceptance. Verify the exact user-visible behavior before
claiming completion; state a real runtime gap if it cannot be exercised safely.

## 5. Deliver or hand off

Report the spec/implementation result and only the files, commits or verification
gaps relevant to the user's next decision. Distinguish a ready spec, implemented
code and verified behavior.

For a requested fresh-session continuation, use `handoff` to preserve the exact
spec path, decisions, current state and remaining work. Do not substitute a generic
instruction to read an assumed `spec.md`, or ask the user to copy text when the
configured handoff/paste workflow can handle it.
