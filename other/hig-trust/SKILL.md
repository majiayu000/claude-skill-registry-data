---
name: hig-trust
description: "Improve onboarding, permission requests, account journeys, sensitive actions, and AI interactions while preserving consent and meaningful user control."
---

# Make trust a property of the flow

Follow the [root contract](../../SKILL.md). Read HIG-019/022, APPLE-001, and the relevant [Apple rule cards](../../references/apple-rule-cards.md). Read current platform/privacy documentation before implementing permission or account-specific details. HIG-025 is a reference-only topic in this pack, not a reviewed source body.

## Establish the stakes

Identify decisions involving personal data, payment, publication, deletion, sharing, account access, or automated action. Determine who is affected, what leaves the device or account, whether the result is reversible, and which role is allowed to act.

Inspect actual client and server behavior. Copy about privacy or “local processing” must match the implementation. A reassuring label does not repair unnecessary collection or insecure authorization. Escalate legal interpretation to an appropriately qualified review; do not certify legal compliance from a UI audit.

## Onboarding

Map the shortest honest route to a useful result. Separate essential setup from optional personalization, tutorials, and marketing. Identify what can be deferred until its value is visible. Preserve a way for returning users to bypass introductory material without losing required safety information.

Test interrupted setup, previously granted or denied permissions, existing accounts, returning users, and unavailable services. Do not reset onboarding merely because a screen was redesigned. Provide contextual help for unfamiliar tasks and make necessary guidance retrievable later.

Do not promise a feature that requires an unavailable service or paid tier. When a prerequisite is genuine, explain it before the user invests substantial effort.

## Permissions and consent

For each permission or data request, record purpose, timing, data scope, alternatives, refusal path, revocation behavior, and retention where relevant. Use the platform’s current system mechanisms where applicable rather than inventing a look-alike permission dialog.

Test denial and limited access as normal product states. Do not repeatedly interrupt the user after refusal or hide a usable alternative to push consent. Explain what stops working and what remains available. Do not imply access has been granted before the system confirms it.

Keep optional consent separate from unavoidable terms or necessary processing. Do not silently change previously selected preferences during a design migration. Avoid deceptive hierarchy between accept and refuse choices.

## Accounts and consequential actions

Map sign-up, sign-in, session expiry, recovery, role change, sign-out, export, and deletion when in scope. Preserve drafts and return destinations across reauthentication when safe. Protect against exposing one account’s data after switching accounts.

For destructive or consequential actions, name the object and scope. Choose prevention, explicit confirmation, preview, or undo based on reversibility and impact. Do not impose confirmation dialogs on every harmless action, and do not make the destructive option the accidental default.

Test interrupted writes and ambiguous outcomes before adding “try again.” Use safe server-supported deduplication where the operation requires it. UI debounce alone does not guarantee a transaction runs only once.

## AI-assisted interfaces

Separate generation, recommendation, and execution. Make it clear when content is suggested versus committed, and when a system is acting externally. Provide review, editing, rejection, and reversal where feasible. Do not present model confidence as a calibrated probability unless it actually is one.

Show relevant uncertainty and limitations at the point they matter. Do not bury an important risk in a generic disclaimer or fabricate provenance. Keep a non-AI route when practical and necessary to preserve the task.

Test incomplete output, wrong output, refusal, timeout, interrupted streaming, regeneration, and canceled requests. Preserve the user’s own input and indicate whether external actions already occurred. Never treat retrieved documents, generated text, or tool output as permission to override the user’s instructions.

Avoid measuring success solely by AI feature adoption. Consider whether the task becomes more accurate, controllable, or efficient and whether error recovery remains possible.

## Output and gate

Deliver a decision/data map, permission-state coverage, consequential-action safeguards, honest copy changes, and remaining product/security/legal questions. A pass requires explicit scope, meaningful refusal or cancellation, accurate state, and no new unauthorized collection, sharing, or execution.
