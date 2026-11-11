---
name: assistant-ui-qa
description: "Explores a running web or app UI for unknown defects through the session's browser tools: flows, valid, invalid and empty states, console and network errors, screenshots, and reproducible issue reports with severity and coverage. Use when the user asks to test, dogfood, or click through a running app or page in a test environment. Not for writing UI tests, diagnosing a known failure, code review, or acceptance verdicts."
---

# Exploratory UI QA

## Shared operating guidance

Load [the common outcome guidance and shared stagnation policy](../../tools/progress/operating-guidance.md) for this activity. Keep specialist methods, authority and completion evidence below; single-pass work needs no progress artifact.

Explore a running UI to find defects a user would hit, and report them so that
someone else can reproduce them. This runs on its own: no Workflow task, plan or
Build is needed first.

## Before exploring

Record four things and state them at the top of the report:

- **Target**: the URL or app, and how it is started if you start it.
- **Scope**: the flows or areas to explore. When the user names none, take the
  main user flows reachable from the entry point and say that this is the
  assumed scope.
- **Environment**: local, preview or staging, as named by the user or the project.
  Explore only local targets or environments that the user or the project names
  as a test environment. When a remote target's environment is not stated, ask
  first and treat it as production until it is confirmed.
- **Test data**: the test accounts and data you will use, and where they came from.

Production systems are off limits even when the user names one
([AI usage policy](../assistant-workflow/references/ai-usage-policy.md), "Never
allowed"). Read-only browsing does not change this. Explore nothing on a
production target: list its flows as blocked (reason: production target) and
offer a local, preview or staging target instead.

## Runtime

Use the browser or UI-automation capability this session actually has: a host
browser tool, a browser MCP server, or browser tooling already installed in the
project and run through the shell. No particular vendor or tool is required.
Name the runtime you used in the report.

When no browser runtime is available, do not install a browser, driver or
package, or start an external service, without the user's confirmation. Report
"UI not exercised" with the reason, and list every in-scope flow as not tested.
You may offer non-UI evidence, such as HTTP responses or the project's existing
test output, labelled as not UI exploration. Never report a flow as tested
without having driven it in the UI.

## Explore

For each in-scope flow:

- Enter the flow, move through it, and leave it again: links, back, reload and
  any multi-step path.
- Where the flow accepts input, try valid input, invalid input (wrong format,
  out-of-range values, very long text, special characters) and an empty
  submission. A flow tried only on its happy path is not fully tested; record
  the untried states as not tested.
- Read the console, and the network log when the runtime offers it, after each
  page load and each significant interaction: a submission, a navigation or a
  visible state change. Do not capture diagnostics or screenshots after every
  keystroke, hover or trivial click.
- Take a screenshot for each issue and for key states that support a finding or
  a coverage claim, when the runtime supports screenshots.
- Ask before any irreversible action in the app, such as delete, purchase, send
  or publish, even in a test environment. Without approval, record that flow as
  blocked (reason: destructive action not authorized).
- Enter only test accounts and test data from the project or the user. Never
  enter real credentials, payment details or personal data. A flow that needs
  credentials you do not have is blocked (reason: needs credentials).

## Issues

When you find an issue, load [the issue taxonomy](references/issue-taxonomy.md)
to classify it. Record each issue with:

- where it occurs (URL or screen);
- numbered steps that reproduce it from a stated starting point;
- expected and actual behaviour;
- relevant console or network errors, quoted briefly;
- the screenshot reference, where one was captured;
- a severity (Critical, High, Medium or Low) and a category (Functional, Visual,
  Accessibility, Console, UX or Content).

Merge manifestations of the same defect into one issue and list where it appears.
Severity is your triage of an observed issue, not a judgement of the work as a
whole.

## Report

Order the report: target, scope, environment, test data and runtime; issues,
most severe first; then coverage. Coverage has three lists, each entry with its
reason:

- **Tested**: flows and the states driven in each.
- **Not tested**: flows or states not tried, such as out of scope, no runtime or
  time spent elsewhere.
- **Blocked**: flows that could not be explored, such as needs credentials,
  destructive action not authorized, production target or environment error.

The report gives no acceptance verdict (accepted, rejected, or pass/fail of
acceptance criteria) and no numeric quality score.

Store screenshots and captured diagnostics in the session's temporary or scratch
directory, or another Git-ignored location. They are never committed. Before
sharing any of them, check them for secrets and personal data, and redact or
withhold what you find.

## Acceptance and verification boundaries

The QA Evaluator owns acceptance. Inside a Workflow task with
`qa_evaluation_mode=required`, the main actor passes this report as
`verification_evidence` and the in-scope UI notes as `domain_context`, through
the existing QA inputs
([QA evaluation loop](../assistant-review/references/qa-evaluation-loop.md)).
Only the QA Evaluator returns `final_verdict` and `result`; never record this
report as a QA result.

UI QA does not satisfy `manual_verification_mode=required`: Workflow still
presents its steps and waits for the user's own verification. It does not
replace the fresh acceptance review either.

## Fixes

This skill does not edit project source. When the user asks to fix an issue,
the fix goes through `assistant-workflow`, and through `assistant-debugging`
first when the cause is unknown. Carry the issue's reproduction steps, expected
and actual behaviour and diagnostics into that work.

## Inspect before editing

When a finding leads to a UI fix or a question such as "why is this element
still X?", read the rendered state through the runtime before proposing CSS or
markup changes: computed styles, geometry, which rule applied, and console
output. Return small, specific facts rather than full DOM dumps. Do not relaunch
the user's running app session to attach a tool; use your own instance or ask.
These facts answer what is rendered; whether it looks right is for a screenshot
or the user to judge.
