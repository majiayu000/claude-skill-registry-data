---
name: action-confirmations
description: Handle external messages, payments, controls and account changes through exact targeting and backend-enforced authorization.
---

# Action Confirmations

1. First determine if the user is asking for advice, a draft, a preview, or an actual effect. A draft is not a send instruction.
2. Check whether the precise integration operation exists; do not emulate a missing action through unrestricted shell/browser.
3. Resolve action parameters: recipient, target, content/value, timing, scope and reversibility. Confirm materially ambiguous dictated names or amounts.
4. For consequential actions use one compact confirmation showing the exact effect, then comply with the integration's real approval mechanism.
5. Missing, expired, denied or wrong-scope approval must fail closed. Natural-language agreement is not a substitute for backend permission enforcement.
6. Submit once and retain any returned run, approval or idempotency identifier. After timeout check authoritative state before retrying.
7. Report confirmed success, pending approval, failure or unknown separately. Backend acceptance alone is not delivery confirmation.
8. For cancellation verify through the integration; otherwise report cancellation unconfirmed. For dangerous device effects direct toward a safer manual method.
