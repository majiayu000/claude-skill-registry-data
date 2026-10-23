---
name: mobile-release
description: "Use when preparing a mobile app for a store: build artifact, version numbers, signing, platform target level, test tracks, staged rollout, store declarations, and which steps only a human can do."
---

# mobile-release

Extends step 10, `ship` (`WORKFLOW.md`), for a mobile application (native or cross-platform) headed for a
store. **Status 🟡: base to confront with reality**, written from store documentation and two public
Android release guides read on 2026-10-02, not from a store submission run in house. The store side is
detailed for Android; for iOS only the beta-testing facts below were read from the vendor's own pages, so
signing and submission on Apple platforms carry no rule here.

## When
A build is about to go to a test track or to production; Gradle or CI files for a release lane change; a
third-party SDK, a permission or a collected data type is added; the store's target-level deadline nears.

## Steps

1. **Split the work first: what the agent does and what only a person can.** Say this at the start of any
   release task, then stay on the left side of the table.

   | The agent | A person, outside the repository |
   |---|---|
   | Edits build files so the release task produces the store artifact; edits CI to run lint, tests, then the release build | Creates the signing keys and enrols in store-managed signing; binds the CI secrets |
   | Adds ignore rules, removes a committed keystore or password file | Supplies the next version code, or the rule that allocates it |
   | Wires an injected version code and secret names (never values) | Uploads, creates the release, sets the track and rollout, promotes |
   | Drafts changelog lines from merged titles when asked | Completes developer identity verification and store questionnaires |

   Never invent a version code, a password, a service-account file or an upload step that needs a console
   login.

2. **Ship the format the store wants.** For the Android store the publishing format is the app bundle, not an
   APK; the store generates and signs per-device APKs from it. Keep the release task of a store-bound build
   on the bundle; build APKs only for sideloading or enterprise distribution.

3. **Version numbers.** The store rejects an upload whose version code is not strictly greater than every
   one it already accepted for that application id. The agent therefore wires the injection (a property or a
   CI-provided value) and never guesses the integer. Two branches that both bump it to the same value are
   resolved against the store's history before merge. The human-readable version name is a label; it does
   not carry the ordering.

4. **Signing stays out of the repository.** No keystore, no password file, no secret in a tracked file. CI
   refers to secret names only. Pull-request jobs build debug or unsigned artifacts; production signing is
   reserved for the protected branch. The release build config in the project must not fall back to the
   debug key.

5. **Know the platform target level and re-read it each season.** The store demands a minimum target API
   level for new apps and updates, and limits availability of older-targeting apps on newer devices. As read
   on 2026-10-02 from the store's and the platform's own pages: new apps and updates from 31 August 2026 must
   target Android 16 (API level 36), with narrower rules for watch, car, TV and XR form factors, an extension
   request available until 1 November 2026, and existing apps needing API level 35 to stay available to new
   users on newer devices. This changes every year: read the current requirement before relying on the
   figure (`skills/source-freshness`), and record the project's floor and target in one place.

6. **Use test tracks before production.** Internal, then closed, then open testing, then production. A
   launch with real blast radius goes through at least one test track unless release management documents an
   exception. Production opens below full rollout and the percentage rises only after crash and
   not-responding signals from the monitoring look stable. For Apple platforms, the vendor's beta service
   documents up to 100 internal testers, up to 10,000 external testers, a review of the first build in a
   group, and builds that expire after 90 days (read 2026-10-02): plan test cycles inside that window.

7. **Keep store declarations in step with the code.** Every permission, third-party SDK or newly collected
   data type changes what the store's data-safety or privacy form and the privacy policy must say. The
   declaration update belongs in the same change as the code that causes it; a diff that adds one without
   the other is flagged in review. Reviewers must be able to exercise the app: either the main flow works
   without an external account, or the review notes carry working access.

8. **Verify before handing over.** The release lane runs lint, unit tests, then the release build, in that
   order, in the same pipeline. If the bundle tool is available, validate the artifact. Publish steps sit
   behind the same gates as the protected integration branch, never on arbitrary pushes. When the upload
   fails only on a console policy error (identity verification, for instance), route the person to the
   console; repository edits cannot fix it.

## Output / checkpoint
The release build command and its result, the version code and where it came from, the target level and the
source and date it was read from, the declarations changed, and the list of steps left to a person. Attached
to the `ship` checkpoint (`WORKFLOW.md` §5).

## Guardrails
The agent never uploads, never holds signing material, never completes a store questionnaire. Figures about
target levels, tester limits and expiry are dated and go stale. App variants (dev, staging, production
identifiers), forced-update gates, store-listing text limits and Apple signing and submission were not
sourced in this pass and carry no rule.

## Origin
Rewritten, no text copied. Agent versus human split, version-code rule, bundle format, signing hygiene, test
tracks, staged rollout and declaration-in-step rule from the Apache-2.0 `Drjacky/claude-android-ninja`
CI/CD reference and the MIT `abhinav503/flutter-agentic` store-readiness guide (both read 2026-10-02);
target-level facts from Google Play's policy page and the Android developer page of the same name; bundle
format from the Android developer guide; test-service facts from the Apple developer help page. All read
2026-10-02.
