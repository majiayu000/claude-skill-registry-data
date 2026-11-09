---
name: unity-integrate-ads
description: Integrate explicitly selected Unity LevelPlay ads with privacy configuration, lifecycle ownership, bounded retries and idempotent rewarded outcomes.
engines: [UNITY]
---

# Unity Integrate Ads

## When to use

Implement a selected LevelPlay ad integration, placement or rewarded-ad flow. Do not add advertising to a project merely because it can support it.

## Activation and inputs

Run `commands/resolve-engine.sh` and `commands/resolve-skill.sh unity-integrate-ads`; require effective `UNITY`, compatibility and permitted scope. Inspect the locked LevelPlay package, adapters/native dependencies, platform, approved placement/reward policy, privacy settings, app keys and authorized test mode. Accounts, terms, provider activation, SDK installation and real ad traffic remain separate actions.

## Workflow

1. Match the installed SDK's initialization and ad-unit API. Keep legacy global rewarded listeners distinct from current owned ad objects. Initialize once; register handlers before load/show and remove exactly those handlers on disposal.
2. Apply the project's consent, age-related and platform privacy configuration at the SDK-required time. Preserve unknown/denied states and selected contextual/disabled behavior; do not manufacture permission or consent.
3. Track ad-unit loading, readiness, display, reward, close and failure separately. A close or impression is not a reward. Own callbacks by ad instance, display attempt and player generation; prevent recycled UI/screens from receiving stale events.
4. Grant a reward only from the selected verified reward signal and persistent deduplication identity. Handle reward/close callbacks in either order. For server-to-server rewards, verify the provider's signature and replay identity on the backend; keep signing secrets off clients.
5. Bound load/show retries and respect placement caps. Restore UI/game pause/audio/input on every supported failure/close path; delayed rewards retain a valid owner without reopening an obsolete screen.

Read [ad lifecycle](references/ad-lifecycle.md) for privacy, callback ordering and device acceptance.

## Verification and output

Deliver SDK/adapter/platform/placement identities, privacy and reward ownership, dependency changes, callback-state tests and approved test-ad device evidence. Exercise no-fill, offline start, show failure, duplicate/late reward, close-before-reward, consent denial and teardown. Simulated callbacks are protocol tests; Editor success cannot certify native adapters or platform privacy behavior. Redact identifiers, payment/revenue payloads and personal data. Store observations under resolved `.hephaera/.cache`; unavailable accounts/SDKs/devices remain blocked/not-run.
