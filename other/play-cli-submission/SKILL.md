---
name: play-cli-submission
description: "Use when shipping an Android build (AAB) to Google Play without the Play Console GUI, from CI (play-release.yml builds to internal; promote the SAME versionCode with play_promote.py) or the CLI (submit-play.sh). Carries the Play Developer API v3 edits transaction, service-account JSON auth, versionCode +1 on every upload, versionName read from AppVersion.xcconfig, the 500-character release-notes cap (check before the bump), applicationId vs namespace, staged rollout, changesNotSentForReview and the refused-to-auto-submit stall, inputs as env in workflows, and the org-policy key block. Triggers on Google Play, Play Console, AAB upload, submit-play, play-release.yml, androidpublisher, service account, versionCode, staged rollout, promote, internal track, org policy key block, refused to auto-submit, changesNotSentForReview, pre-launch report, Test Lab."
---

# Play CLI Submission

Ship an Android App Bundle to Google Play entirely from the CLI, via the **Play Developer API v3**. Pairs with `store-submission-playbook` (listing / Data Safety / screenshots) and `android-production-gotchas` (building the signed AAB) — this skill is the **upload+release transaction** and its auth gotchas.

## When to invoke

- Uploading a signed AAB to any Play track (internal / closed / production) from the command line
- Setting up service-account auth for automated Play publishing
- Play rejects a version code, or an SA key can't be created

## Rule 1: Publishing is one "edits" transaction, and it runs in CI by default

The Play Developer API v3 is transactional: **insert an edit** (get an edit id), **upload the AAB** to it, **assign it to a track** with release notes and status, **commit**. Nothing is live until commit; a validation failure aborts the whole edit (no partial release). `tools/play-publish.py` runs exactly this sequence.

The default venue is CI, not the laptop (a release build is R8 plus a full Kotlin compile, and it has taken a working Mac to 18% free memory):

```
gh workflow run play-release.yml -f notes="..."            # bump versionCode, build, publish to INTERNAL
# install from Play internal on a real device and use it, then:
gh workflow run play-release.yml -f promote=<versionCode>  # the SAME artifact to production (+ -f rollout=0.1)
```

`play-release.yml` bumps `versionCode`, builds the signed bundle, refuses an unsigned one, publishes, and commits the bump back with `[skip ci]`. Promotion (`tools/play_promote.py`) builds nothing: the artifact users get is the one that was tested. Secrets: `PLAY_SERVICE_ACCOUNT_JSON`, `UPLOAD_KEYSTORE_B64`, `UPLOAD_KEYSTORE_PASSWORD`, `UPLOAD_KEY_ALIAS`, `UPLOAD_KEY_PASSWORD`. Workflow inputs reach scripts as **env** (release notes with a quote otherwise close the shell string) and optional flags are `if ... fi`, never `[ -n x ] && ARGS+=(...)`. The local path, `tools/submit-play.sh`, still works for a machine that can spare the build.

## Rule 2 — Service-account JSON auth, scope androidpublisher

Auth is a **service-account JSON key** (from a GCP project) with the `https://www.googleapis.com/auth/androidpublisher` scope, and that service account **granted access in the Play Console** (Users & permissions → invite the SA email → release permissions). No OAuth user flow, no interactive login — the SA key is the whole credential. Keep it out of git (`~/.config/…` or a CI secret).

## Rule 3: versionCode +1 on EVERY upload; versionName is not yours to type

Bump `versionCode` for every AAB you upload. Play permanently rejects any `versionCode` it has seen, **even one uploaded to a draft track and never shipped**. `versionName` is READ from `AppVersion.xcconfig` by the Gradle build (held by `tools/test_version_contract.py`), so it cannot drift from the Apple marketing version; only `versionCode` is bumped. Anything that can refuse the upload must be checked BEFORE the bump: **release notes are capped at 500 characters**, and a refusal after the bump has spent the versionCode. Don't start a new upload while a previous release is still in review; batch trivial releases. (Archive Watch's owner made it a rule: no new Play version until the one in review is approved; commit fixes freely meanwhile.)

**Play's automatic protection requires `minSdk` 24 or higher.** An upload at 23 was refused in October 2026 ("Play automatic protection requires a minimum SDK version of 24 or higher") although 23 had uploaded two weeks earlier. A store flavor that must reach Android 6 (Fire TV) keeps 23 in its own flavor; the Play flavor's floor is 24 while automatic protection is on (AW Decision 165).

## Rule 4 — applicationId ≠ namespace

The `applicationId` (the immutable Play identity of the app) is independent of the Gradle `namespace` (the R/BuildConfig package). Set `applicationId` deliberately and never change it after first publish — it IS the app on Play. The `namespace` can differ and can be refactored freely.

## Rule 5 — Staged rollout via track status + fraction

A release on a track carries a status: `draft` (staged, not live), `inProgress` + a `userFraction` (e.g. 0.1 = 10% staged rollout), or `completed` (100%). Ramp by editing the fraction on subsequent edits; promote by moving the same AAB to a higher track. Pass the target track + status + notes through the publish script rather than hardcoding.

## Rule 6 — The org-policy key-block gotcha

Creating a service-account **key** under a Google Workspace / organization-owned GCP project can hit an **IAM org-policy block** (`iam.disableServiceAccountKeyCreation`) — the key create is refused outright. Fix: create the GCP project AND the service account under a **personal gmail** (no org attached, so no key policy) via `gcloud`:

```
gcloud projects create …            # personal account, no org
gcloud iam service-accounts create …
gcloud iam service-accounts keys create key.json --iam-account …
```

Then invite that SA's email into the Play Console. **Eventual-consistency retry**: a freshly-created SA sometimes isn't yet visible to the key-create call — retry key creation a few times with backoff before treating it as a real failure. Full walkthrough in `docs/store/play-api-key-setup.md`.

## Rule 7: A committed edit can still stall in the Console

The edits transaction ends at Play's REVIEW layer, not at "live". When Play will not send changes for review automatically (managed publishing, or a rejection pending), `edits.commit` fails and says to set **`changesNotSentForReview=true`**. Committing that way succeeds, and the changes then wait in the Console for a human send. That is the same state as a changes bar reading **"refused to auto-submit"** (or a stuck "N changes"): those changes will NEVER process until acted on. It is a stall, not a queue. And **"Submit N changes" is all-or-nothing**: every pending Console edit rides the same submit, so read what the N contains first. After any publish, confirm the release shows in review or live, not behind a changes bar. Retry 5xx on the API calls; a 4xx is a real answer. (The Windows twin, the `commit=true` and publishing-hold stalls, is in `docs/windows/WINDOWS-STORE-SUBMISSION.md`.)

## Rule 8 — The pre-launch report is Firebase Test Lab; run it yourself

The internal track generates NO pre-launch report, so the first automated
device pass otherwise happens AFTER promotion — too late. The report is
just Firebase Test Lab: run `tools/testlab-android.sh` against the release
AAB before promoting. **Physical devices only** — emulators cannot see Play
Billing, so billing-at-startup crashes (Decision 039's mixed-list throw)
pass every emulator and fail on every real phone.

## Rule 9 — Native debug symbols travel INSIDE the AAB

Play's "missing debug symbols" warning (from pre-stripped dependency
`.so` files — ML Kit and friends) cannot be reliably cleared by
uploading `native-debug-symbols.zip`: the API route
(`edits.deobfuscationfiles.upload`) is blocked for some accounts and
the Console UI upload doesn't dependably take. Embed instead: a
Gradle task injects each `.so` as
`BUNDLE-METADATA/com.android.tools.build.debugsymbols/<abi>/<lib>.so.dbg`
and re-signs with the upload key. **Use `zip -D`** — a directory zip
entry inside an AAB surfaces as a misleading "invalid signature"
rejection. Full recipe: `android-production-gotchas` §Release
engineering.

## Scaffolding shipped

- `.github/workflows/play-release.yml`: the CI entry point (build to internal, or `promote=<versionCode>`)
- `tools/submit-play.sh`: the local entry point
- `tools/play-publish.py`: the edits-transaction driver (insert, upload, track, commit)
- `tools/play_promote.py`: move an existing versionCode to another track, no build
- `tools/testlab-android.sh` — the self-run pre-launch report (Firebase Test Lab, physical devices)
- `docs/store/play-api-key-setup.md` — SA key setup + the org-policy workaround

## See also

- `store-submission-playbook` — Play listing, Data Safety answers, screenshots, the 12-tester/14-day personal-account rule, assetlinks
- `android-production-gotchas` — building + signing the AAB, verifying the signer fingerprint against assetlinks
- `cloud-appstore-submission` — the Apple App Store CLI analog
