---
name: open-connect-global-browser
description: Use Open Connect's shared cloud-browser controls and verification service across authorized AI clients. Use for remote browser tasks, same-session verification, global browser policy, or choosing controls supported by TinyFish, Browser Use, Browserbase and connected browser workers.
---

# Open Connect global browser

1. Call `browser_automation_status`. Read the current owner's policy and supported controls. Treat saved credential metadata as readiness information, not proof of a working sign-in or solver account.
2. Reuse the task's existing browser reference, provider and profile. Choose native provider assistance first. Omit the optional `solveCaptchas` Browserbase override to inherit global policy. Browser Use cloud agent runs manage native solving themselves.
3. Use only tools actually discovered on that browser adapter. Keep pointer, keyboard, paste, tabs and navigation on the same browser. A fresh browser is not a continuation of an agent run. Do not transfer cookies, passwords or credentials between providers.
4. For a supported widget on a browser without native assistance, capture the current public HTTPS page URL, widget type and site key through that browser. Call `browser_verification_start` only with an owned solver key, external policy enabled and authorized solver spending. Supply a fresh UUID `requestId`, provider name and non-secret `browserRef`. Never use a CDP URL as a reference.
5. Retain the attempt ID. Reuse the same request ID for a retry of the same submission. If submission is unknown, inspect the existing attempt and provider state instead of submitting a duplicate paid task.
6. Poll `browser_verification_result` at intervals of at least five seconds. A ready proof is not website acceptance. Apply it only to the matching browser reference, origin and original widget through that browser's supported API. Discard the proof if the page, target or widget changed. Never echo, persist, put in prompts, or log proofs or credentials.
7. Inspect the original page to confirm progress. Use same-session human handoff for unresolved or unsupported challenges, MFA, passkeys, sign-in consent and recovery. Do not claim universal bypass, completed authentication or an external action without evidence.
8. Cancel or close unused metered runs through the original provider and verify cleanup. Preserve existing sessions and saved profiles when switching controls.

Use global configuration once per owner; do not register duplicate solver connectors per browser. Store the external 2Captcha API key only in Credentials with website `https://2captcha.com` (optional exact tag `provider:two_captcha`). Never request a key in conversation or tool arguments. Missing/ambiguous credentials are setup blockers, not permission to choose another user's key.
