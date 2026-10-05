---
name: mobile-release
description: Use when preparing a mobile app for release. Covers versioning, signing, staged rollout, crash monitoring, store review requirements, and rollback when an update goes wrong.
metadata:
  category: mobile
  version: 1.0.0
  tags: [release, app-store, play-store, ci-cd, rollout]
---

# Mobile Release

## Purpose

Ship a mobile release safely. Unlike a web deploy, a bad mobile release cannot be rolled back — users have already installed it. The process must therefore prevent the bad release rather than recover from it.

## When to Use

- Preparing a store submission.
- Setting up a mobile CI/CD pipeline.
- Responding to a crash spike after a release.
- Establishing a release process for a team that does not have one.

## Capabilities

- Version and build-number strategy.
- Code signing and credential management.
- Staged rollout and kill switches.
- Crash and performance monitoring with alerting.
- Store review preparation and common rejection avoidance.

## Inputs

- The build, its version, and what changed.
- Store credentials and signing keys.
- The current crash-free rate as a baseline.

## Outputs

- A signed, reproducible build from CI.
- A staged rollout plan with defined abort criteria.
- Monitoring that will detect a regression before users report it.

## Workflow

1. **Build in CI, never on a laptop** — A build that only one machine can produce is a build you cannot reproduce when it breaks.
2. **Test the release build** — On real devices, including the oldest supported OS version. Debug builds hide crashes that only occur under release optimization.
3. **Ship behind a flag** — Anything risky is remotely toggleable. A feature flag is the only rollback a mobile app has.
4. **Stage the rollout** — 1%, then 10%, then 50%, then 100%, with at least a day between steps. Watch the crash-free rate at each stage.
5. **Define the abort criteria before you start** — For example: crash-free sessions below 99.5%, or any new crash affecting more than 0.1% of sessions. Halt the rollout automatically, do not debate it.
6. **Keep the previous build ready** — On Android you can halt a staged rollout; on iOS you can only submit a new build. Have one prepared.

## Best Practices

- A staged rollout is the only safety net that exists. Shipping to 100% immediately is a decision to have no rollback.
- Every release needs a kill switch for its risky feature. Server-side flags cost a day to build and save a release.
- Monitor the crash-free *session* rate, not the crash-free user rate. The latter hides a crash that occurs on one screen in ten sessions.
- Symbolicate crash reports in CI by uploading dSYMs and mapping files as part of the build. A crash report without symbols is useless at 2am.
- Never bump only the marketing version. The build number must increase on every submission or the store rejects it.
- Store review rejections cluster around permissions, in-app purchase rules, and misleading metadata. Read the guideline before you build the feature, not after the rejection.

## Examples

**Rollout gate with explicit abort criteria:**

```yaml
# .github/workflows/release.yml (excerpt)
- name: Staged rollout to Play Store
  run: |
    fastlane supply \
      --track production \
      --rollout 0.01 \
      --aab app/build/outputs/bundle/release/app-release.aab

- name: Guard the rollout
  run: |
    # 6 hours of soak, then check the crash-free session rate before proceeding.
    sleep 21600
    RATE=$(crashlytics-cli crash-free-rate --version "$VERSION" --window 6h)
    echo "crash-free sessions: ${RATE}%"
    if (( $(echo "$RATE < 99.5" | bc -l) )); then
      fastlane supply --track production --rollout 0 --skip-upload-aab   # halt
      echo "::error::Rollout halted: crash-free rate ${RATE}% is below the 99.5% threshold"
      exit 1
    fi
```

**A kill switch that makes the release recoverable:**

```dart
if (await flags.isEnabled('checkout.new_payment_sheet')) {
  return NewPaymentSheet();
}
return LegacyPaymentSheet();   // the fallback path stays in the binary for one release
```

## Notes

- Keep the previous implementation in the binary for one release cycle after replacing it. A flag that flips to code that is not there is not a kill switch.
- Apple's expedited review exists and works, but it is a limited resource — use it for a genuine crash-level regression, not for a missed marketing date.
- Android's in-app update API can force users off a broken version. iOS has no equivalent, which is why a server-side flag matters more there.
