---
name: implementation-seeding
description: Create, adopt, or reconcile small, intentional source-code scaffolds that guide an agent's internal implementation design. Use selectively before a feature or refactor is implemented, or when carrying an existing scaffold into later implementation sessions. Not for full implementation, project boilerplate, or writing architecture and behaviour specifications.
---

# Implementation Seeding

Express selected implementation intentions through partial source structure while
leaving the implementation itself to the delivery agent. The scaffold is opt-in
and scoped to the affected part of a project, not a mandatory project phase.

## 1. Establish scope and authority

1. Identify the requested operation:
   - **Seed:** Create or adjust a small source skeleton before implementation.
   - **Adopt:** Recognise an existing, user-authored skeleton as intentional guidance.
   - **Reconcile:** Check an active skeleton against implementation progress and
     update or retire stale guidance.
   - **Review:** Suggest a skeleton without editing when the request is read-only.
2. Read project instructions, relevant source, tests, specifications, and
   established contracts. Respect their authority; this skill does not replace
   architecture, requirements, test-first development, or delivery workflows.
3. Select only the affected modules or functions. Skip seeding when existing code
   already conveys the intended structure, or a change is too small to justify it.
4. Establish any non-negotiable names, interfaces, or boundaries from the user
   and existing contracts. Do not promote the agent's own suggestions into
   requirements without approval.

## 2. Shape only what matters

1. Identify a few high-leverage decisions worth expressing in code, such as:
   - File or module ownership and coherent responsibilities.
   - Named orchestration and helper functions, with useful delegation seams.
   - Explicit configuration or state ownership and reusable operations.
   - Types or signatures where the boundary genuinely matters.
2. Choose the least detailed representation that communicates each decision:
   paths and declarations first, then optional signatures, concise docstrings,
   or a small call outline. Leave algorithms, incidental helpers, and other
   implementation choices open. Avoid gratuitous layers or splitting cohesive
   code into trivial wrappers.
3. Treat authority separately from detail:
   - **Fixed anchors:** User-confirmed names or interfaces, existing contracts,
     and other established invariants. Preserve them unless authorised to change.
   - **Provisional structure:** Newly suggested private helpers, call shapes,
     and incomplete bodies. An implementation agent may improve, replace, or
     remove them while preserving the underlying intent.
4. Keep source comments useful to future maintainers, not instructions addressed
   to an agent. Avoid a second implementation-specification document. Prefer
   explicit ownership for consequential defaults over hidden per-class defaults;
   do not forbid legitimate convenience defaults indiscriminately.

## 3. Create or adopt the scaffold

1. For Review, show the smallest useful proposed structure and stop without
   edits. For Adopt, leave user-authored source unchanged unless requested. For
   Seed or Reconcile, make only the changes needed for that operation.
2. Preserve working implementations, tests, public behaviour, and unrelated
   files. Never replace functioning code with unfinished stubs. New skeletons
   should remain syntactically valid where practical; use unmistakably
   incomplete bodies rather than invented placeholder behaviour.
3. In projects with `AGENTS.md`, add or update a short, scoped **Implementation
   scaffolds** entry naming the affected source paths and any *explicit* fixed
   anchors. State that other unfinished declarations are provisional guidance
   and must be implemented or removed before delivery. Keep entries current,
   not duplicated or appended indefinitely.
4. If the project uses a different authoritative agent-instruction file, adapt
   to it instead. If none exists, offer the short handoff instruction for the
   user to place in their project guidance; do not scaffold an entire agent
   project merely to register this skill.
5. Do not modify project delivery skills by default. A workflow that already
   reads `AGENTS.md` can inherit its scoped guidance. For delegated or fresh
   agents, ensure the handoff points to the instructions and affected source;
   do not assume a skill invocation or chat context propagates automatically.

## 4. Reconcile and hand off

1. Inspect the diff and, where practical, parse or type-check the changed
   skeleton without implying incomplete code is tested or implemented.
2. On reconciliation, distinguish fixed anchors still in force, provisional
   structure adopted or superseded, and unimplemented or obsolete stubs. Update
   the scoped instruction to match reality; remove its entry when no active
   scaffolding remains, retaining durable constraints in their proper source.
3. Report the affected files, fixed versus provisional decisions, remaining
   incomplete work, checks actually run, and any consequential conflict.
4. Stop at scaffolding and handoff. Do not implement the feature, change tests
   to accommodate the scaffold, or commit, push, or open pull requests without
   separate authority.
