---
name: form-flow-fixer
description: Diagnose and fix a web form across validation, submission, failure, retry, and success, including input preservation and keyboard recovery. Use for form completion problems, not a general page redesign.
---

# Form flow fixer

Make the form's complete journey understandable and recoverable. Inspect the form, its request contract, existing validation, and accessible primitives before changing behavior.

## Map the current flow

Identify required inputs, eligibility rules, submission effects, and success destination. Distinguish client validation, server validation, transport failure, and an unknown server outcome. Preserve established business rules. A disabled submit button is not a substitute for explaining what is needed.

Use `assets/submission-cases.json` to select reproducible cases. Map cases to existing test fixtures or intercepted requests in an isolated environment. Do not submit real purchases, invitations, or other external effects without authorization. Treat request stubbing as UI evidence, not proof of real service behavior.

## Exercise completion and recovery

Check labels, instructions, input formats, autofill/paste where relevant, and keyboard completion. Trigger field errors and a form-level error. Confirm that users can locate and correct errors without losing valid input. Use appropriate error associations, focus behavior, and status feedback in the project's conventions; verify assistive-technology behavior only when it can actually be exercised.

Submit with a slow response, repeated activation, a known rejection, and a supported retry. Inspect request counts and final state. Determine whether retry is safe from the request contract: a timeout may occur after a write succeeded. Do not blindly resubmit or invent client-side idempotency guarantees. When outcome is unknown, expose that uncertainty and use an existing status/recovery mechanism if available.

Preserve entered non-sensitive data through recoverable failures. Follow the application's existing security and privacy rules for sensitive fields; do not persist all values indiscriminately. Confirm success only from evidence that the operation succeeded, and verify the post-submit destination or confirmation.

## Implement the smallest complete fix

Review requests produce findings; fix requests authorize scoped repairs. Prefer existing form and request abstractions. Correct the cause rather than suppressing errors, bypassing validation, or adding a success toast for a failed operation.

Re-run the original failure and affected keyboard path, then adjacent submission states. Add regression tests where request ordering, duplicate effects, or data preservation could regress. Test supported failure recovery with the real service only when available and authorized; clearly separate it from simulated tests.

Report the trigger, resulting behavior, changes, tested cases, and limitations. Do not claim a working submission based solely on appearance or a mocked success response.
