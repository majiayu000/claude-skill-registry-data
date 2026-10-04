---
name: code-review
description: Perform a mandatory scoped code review for the code changed in the current task. Use when Codex has implemented or modified code and must review the touched scope for requirement compliance, existing style consistency, stability, scalability, efficiency, security, integration with real code paths, compatibility, dry-run behavior, structural clarity, helper boundaries, fallback justification, and silent error masking; a user request to use this skill counts as explicit permission to use 1-3 read-only review subagents for broad changed scopes; fix any discovered issue immediately unless it requires a user decision or integration with code that does not exist yet.
---

# Code Review

## Required review process

Review only the code that belongs to the current task's changed scope. Do not expand into unrelated files, historical issues, or opportunistic refactors unless they directly affect the changed code.

Before declaring the work complete, perform this review:

1. Determine the changed scope from the task, diff, touched files, and surrounding call paths.
2. Check requirement compliance against the user's request, development documents, issue text, TODOs, and any explicit acceptance criteria that apply to this task.
3. Check style consistency with the existing codebase, including naming, comments, line breaks, indentation, error handling, logging, dependency usage, and test style.
4. Look for improvement opportunities in stability, extensibility, efficiency, and security. Treat minor bugs and low-risk polish issues as real findings.
5. Verify integration points by searching the actual code. Confirm function signatures, import paths, exported names, API response shapes, configuration keys, storage formats, event names, and caller expectations from source evidence. Do not guess.
6. Check compatibility constraints that matter for the project, such as operating system versions, runtime versions, library versions, browser or Android API differences, permissions, filesystem behavior, and deployment policy differences.
7. Dry-run the actual code flow mentally and, when practical, with tests, type checks, linters, build commands, smoke scripts, or focused manual execution. Trace inputs, outputs, errors, side effects, and rollback behavior.
8. Check whether helpers, fallbacks, defaults, and exception handling made the normal path harder to understand or hid failures that should be reported.

## Structural clarity and failure-policy review

Review whether the changed code became harder to understand because of helpers, fallbacks, defaults, or exception handling.

This review should preserve useful helpers and fallbacks. Fix cosmetic abstraction, ungrounded defensive defaults, and silent masking of required failures.

Prefer root-cause fixes over symptom handling. If the changed code compensates for a problem that could be prevented through normal design, data flow, validation, typing, initialization, or caller behavior, treat the preventive fix as the preferred direction. Do not accept reward hacking, benchmark-specific shortcuts, or checker-shaped workarounds as substitutes for a real fix.

Review whether the implementation targets the task contract and supported input classes. Sample-specific logic is suspicious when it depends on incidental identity traits of the example. Specialized logic is acceptable when it targets a real input class in scope and is triggered by stable structural evidence.

### Normal path

Check:

- whether the most common execution path is easy to read;
- whether specialized branches use real input-class evidence and avoid sample identity traits;
- whether required invariants are visible near the relevant code;
- whether environment-dependent values that are central to the changed logic are treated as required values;
- whether fallback, compatibility, and error-handling branches dominate the main logic;
- whether reading the normal path requires opening several helpers.

If the normal path is obscured, simplify the structure before declaring the review complete.

### Helper boundaries

For each new or modified helper, check whether it has a clear role.

Signals that a helper is useful:

- it removes meaningful repetition that is complex enough to be worth centralizing;
- it names a domain concept;
- it isolates file, network, process, environment-variable, time, external API, or similar boundary logic;
- it separates a long condition or algorithm step from the main flow;
- it matches an existing repository pattern;
- it creates a valuable unit for focused tests.
- it centralizes a likely future extension point when that extension is credible and keeping the logic in one place clearly reduces future maintenance cost.

Signals that a helper is suspicious:

- it wraps a one-off simple expression;
- it extracts repeated logic that is still simple enough to read inline;
- it hides a fallback chain;
- it has a vague name such as `resolveValue`, `getData`, `handleThing`, `processInput`, or `normalizeInput`;
- readers must open the helper to understand the main flow;
- it exists for hypothetical future flexibility without a credible extension path or clear maintenance benefit;
- it exists only because the extracted code looked tidier as a separate function.

Fix unclear helpers by inlining them, renaming them, or narrowing their responsibility. For new internal-only helpers, use a leading underscore. Keep helpers with clear value. Do not remove meaningful helpers only to reduce the helper count.

### Fallback discipline

For each new or modified fallback, check whether the fallback is grounded.

Signals that a fallback is useful:

- the user requested the fallback behavior;
- existing tests require it;
- real legacy data or an existing persisted shape exists;
- runtime, operating-system, browser, library, API, or tool-version differences were confirmed;
- an optional feature can fail while the core operation remains safe;
- degraded behavior after an external-service failure matches product intent.

Signals that a fallback is suspicious:

- it compensates for a problem that can be prevented at the source;
- it hides missing required values behind defaults;
- it ignores failed security validation;
- it hides possible data corruption;
- it has many candidates without evidence for the priority order;
- a long fallback chain is hidden inside a vague helper;
- it defensively checks values that are non-null by declaration or type.
- it treats an environment-dependent value as optional even though the changed core logic requires it.

Fix suspicious fallback logic by removing unsupported candidates, preventing the problem at the source, making priority visible near the use site, or turning missing required values into explicit failures. If a value is guaranteed by type or declaration, avoid adding defensive null checks for that value unless repository evidence shows a real compatibility need.

When a fallback has three or more candidates, verify evidence and priority order. Keeping three or more candidates is acceptable when the reviewed behavior is still justified; in that case, keep the evidence and priority order visible near the code that uses the value.

### Exception handling and silent defaults

Check:

- whether broad `catch` blocks convert serious failures into defaults;
- whether empty strings, empty arrays, `null`, `false`, or weak defaults hide missing required values;
- whether optional chaining or nullish coalescing hides malformed data;
- whether callers need to know about a failure that is swallowed internally;
- whether logging and continuing is safe for the changed flow.

Must-stop failures should stop or be reported. Safe-to-continue failures should keep their scope and intent visible.

## Broad-change parallel review

If the changed scope is broad, use 1-3 read-only review subagents in parallel while continuing to review the code directly yourself. A user request to use `$code-review` or this `code-review` skill is itself an explicit request and permission to use read-only review subagents for that review, even when the user did not separately say "use subagents." Do not ask for separate permission before spawning them. Do not delegate the whole review and wait idly.

Treat the scope as broad when one or more of these apply:

- multiple subsystems, packages, commands, screens, services, or runtime layers changed;
- public interfaces, API shapes, storage formats, event contracts, prompt/tool contracts, or compatibility behavior changed;
- the diff is large enough that independent review is likely to catch missed integration or edge-case issues;
- the task touches security, data loss, billing, authentication, filesystem deletion/move behavior, background processes, or external side effects.

When using subagents:

1. Assign each subagent a narrow, non-overlapping read-only review angle, such as integration contracts, edge cases and security, compatibility and runtime behavior, or tests and verification gaps.
2. Tell subagents explicitly not to edit files, not to revert changes, and not to inspect unrelated scope except where needed to verify changed-code integration.
3. While subagents run, perform your own direct review of the changed files and call paths.
4. Merge their findings with your own evidence. Verify any reported issue against the actual code before fixing or reporting it.
5. Keep responsibility for final judgment, fixes, and the final review result in the main agent.

Skip subagents only when the changed scope is small, the environment does not allow spawning agents, or spawning agents would create avoidable risk for the task.

## Fix-or-report rule

If the review finds a problem in the changed scope, fix it immediately, even when the issue is minor.

Report instead of fixing only when:

- the correct behavior requires a user decision;
- the fix depends on code, APIs, assets, credentials, or requirements that do not exist yet;
- the change would expand beyond the current task scope;
- multiple valid fixes have meaningful trade-offs that the user must choose between.

When reporting, state the evidence, affected file or flow, why it cannot be safely fixed now, and the concrete decision or missing input required.

## Evidence discipline

Prefer repository evidence over assumptions. Use fast searches such as `rg`, read the actual callers and callees, and verify generated paths or runtime commands before relying on them. If tests or commands cannot be run, explain the concrete blocker and perform the strongest available static dry-run.

## Completion standard

Finish with a concise review result that includes what was reviewed, whether read-only subagents were used for broad scope, what was fixed during review, what verification ran, and any remaining user-decision items or residual risks. If no issues remain, say so directly.
