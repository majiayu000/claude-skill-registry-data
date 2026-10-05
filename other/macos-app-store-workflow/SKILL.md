---
name: macos-app-store-workflow
description: Coordinate native macOS app development and Mac App Store delivery when work spans Xcode setup, stable signing and TCC, sandbox permissions, StoreKit, tests, screenshots, archives, TestFlight, or App Review. Use narrower skills for isolated SwiftUI, concurrency, signing-inspection, test-diagnosis, or screenshot-only tasks; exclude Developer ID website distribution unless explicitly requested.
---

# macOS App Store Workflow

Move a native macOS app through explicit evidence gates. Preserve the existing
project architecture and separate product decisions from Apple account actions.

## Route The Task

- Read [references/development.md](references/development.md) for project
  identity, signing during development, TCC, Sandbox, permissions, StoreKit,
  SwiftUI, local installs, and automated tests.
- Read [references/app-store-release.md](references/app-store-release.md) for
  App Store Connect, pricing, metadata, screenshots, archives, uploads,
  TestFlight, and review submission.
- Read [references/failure-patterns.md](references/failure-patterns.md) when a
  permission, signing, upload, StoreKit, screenshot, or sheet workflow behaves
  unexpectedly.
- For an archive gate, run `scripts/verify_archive.sh` rather than re-deriving
  bundle traversal and signature checks.
- For a macOS TestFlight gate, run `scripts/verify_testflight_app.sh` against
  the running installed app rather than inferring candidate identity from UI.

When available, use the repository's specialized skills for implementation
detail: `swiftui-expert-skill`, `swift-concurrency`,
`macos-signing-inspector`, `macos-test-diagnoser`, and `screenshot`.
Use `app-store-sandbox-macos` for the four evidence-gated StoreKit stages of a
native macOS non-consumable purchase; do not substitute an iOS device workflow.
Locate that sibling skill through the available-skills catalog, then run its
bundled `scripts/iap_macos.py` from the app repository root. Substitute the
discovered absolute skill directory in commands such as:

```sh
python3 "<app-store-sandbox-macos-skill-dir>/scripts/iap_macos.py" status
```

Do not require a project-local wrapper.

## First Paid App Or In-App Purchase Preflight

Treat a first paid app or the first In-App Purchase of any type as an account
setup workflow before treating it as a StoreKit implementation workflow. As
soon as the app's paid model is known, proactively warn a first-time developer
that agreements, banking verification, and tax forms can block product loading
in Apple's Sandbox and App Review even when the code and local StoreKit tests
are correct.

Before recommending Sandbox testing or review submission, inspect or ask the
user to report the exact statuses in **App Store Connect > Business >
Agreements**. Require all of the following evidence:

- **Paid Apps Agreement** is `Active` / `In Effect`.
- The payout bank account is `Active`.
- Every required tax form is `Active` / `In Use`, with no missing-tax banner.
- The Apple Developer Program membership and latest required agreements are
  active.

`Signed`, `Accepted`, `Waiting for User Info`, `Processing`, `Pending`, and a
bank-update banner do not satisfy this gate. If any required item is not active,
state that it is the current release blocker and stop recommending upload,
review submission, resubmission, or a message claiming the IAP is fixed. The
Account Holder must complete agreements and truthful banking and tax details;
do not infer tax-form answers or accept irreversible terms for the user.

After every required status becomes active, allow App Store Connect changes to
propagate, then test the exact candidate build against the real Apple Sandbox,
preferably through TestFlight. The product request must return the intended
Product ID and localized price before purchase; then verify purchase,
entitlement persistence after relaunch, and Restore Purchases. A local
`.storekit` test is useful implementation evidence but never evidence that the
App Store Connect product or commercial account is ready.

Do not infer Apple Sandbox merely because a development-signed app was launched
outside Xcode or because no `.storekit` file is embedded in its resources. An
`[Environment: Xcode]` purchase sheet and Xcode-created entitlements are local
simulation. Require an exact TestFlight install or a scheme whose StoreKit
configuration is explicitly `None`, then confirm a real App Store Connect
product and localized price plus a successful Sandbox transaction. Prefer the
verified transaction's `.sandbox` environment as definitive evidence when the
app records it.

Do not use the presence or absence of an account prompt as StoreKit environment
evidence. macOS can reuse an existing App Store authentication context, and a
Sandbox purchase may complete without asking the user to sign in. Conversely,
an `[Environment: Xcode]` prompt definitively identifies local simulation.

If App Review shows a purchase sheet without a localized price or an app error
such as product unavailable, classify it as a product-request failure first.
Check the Paid Apps Agreement, banking, tax forms, Product ID, price schedule,
localization, storefront availability, and App ID capability before changing
purchase callback code or uploading another binary.

## TestFlight Candidate Identity Gate

macOS Launch Services can route an **Open** request to any registered app with
the same Bundle ID. Before installing or opening a TestFlight candidate,
enumerate running executables and registered local copies in DerivedData,
archives, `dist`, mounted DMGs, and Trash. A TestFlight button saying **Open**
does not prove that TestFlight installed the app. Never open a local archive or
development build as a substitute for the TestFlight candidate.

When local copies conflict, stop the app and unregister only the verified exact
local bundle paths from Launch Services; eject obsolete mounted DMGs. Preserve
archives unless the user explicitly requests deletion. Before moving or
deleting any local `.app` build artifact during cleanup, unregister its exact
path. Then run `lsregister -gc` and re-read `lsregister -dump` for the Bundle ID.
Block TestFlight launch while any registered `.app` path other than the intended
installed candidate remains.

An existing `.app` in Trash may be registered again after `lsregister -u`. If
the current process cannot move or rename that exact Trash item because of TCC,
ask the user to empty it or restore and relocate it, then rerun the identity
gate. Do not weaken the check, change Trash permissions, or globally reset the
Launch Services database to hide unresolved same-Bundle-ID copies.

Do not call a build TestFlight-tested until all of these agree:

- The running executable path is the actual TestFlight-installed application,
  not a path under DerivedData, `.build`, an `.xcarchive`, `dist`, Trash, or a
  mounted development image.
- `codesign -dvvv` reports `TestFlight Beta Distribution` and the expected Team
  ID and Bundle ID for the legacy identity path. Modern macOS TestFlight can use
  `Apple Mac OS Application Signing`, which production Mac App Store apps also
  use; `spctl`, App Store metadata, receipt, and a matching TestFlight tester
  record are corroboration only and cannot complete the identity gate.
- `Contents/_MASReceipt/receipt` exists and Spotlight reports an App Store
  receipt when that metadata is available.
- `CFBundleShortVersionString` and `CFBundleVersion` match the candidate selected
  in App Store Connect.

Run the bundled verifier as the identity gate:

```sh
./scripts/verify_testflight_app.sh \
  /Applications/App.app com.example.app 1.0 42 TEAM_ID
```

Exit status `0` is reserved for the legacy `TestFlight Beta Distribution`
chain. After its corroborating checks pass, an `Apple Mac OS Application
Signing` app exits `3` with static-only evidence and remains `pending`. Run
the sibling `app-store-sandbox-macos` skill's bundled CLI with `3 verify
--seconds 120` to establish the exact process; if that session remains pending,
keep it running and use the same CLI with `3 monitor --seconds 120`. Require fresh,
nonce/PID-bound `AppTransaction.environment == .sandbox` evidence from that
same process before classifying the modern candidate as TestFlight. A production
App Store install and a retained TestFlight database row can otherwise satisfy
the same static checks.

Use the verified transaction's environment for StoreKit classification. The
signature and receipt prove TestFlight build identity; they do not prove that a
specific purchase account is fresh or that purchase and restore passed.

## Reset StoreKit Purchase State

Treat purchase-state clearing as an environment-specific state mutation, not
as app-cache cleanup. Before acting, identify the exact product type, product
ID, Bundle ID, installed build, StoreKit environment, and intended outcome:
showing free UI, testing a fresh purchase, testing restore with no purchases,
or simulating expiration, cancellation, refund, or revocation. These outcomes
are not interchangeable.

Classify the environment from public evidence such as the active scheme's
StoreKit configuration, Xcode's transaction manager, the verified
transaction's environment, the install source, and the signed-in test account.
Do not infer the environment from a Development signature alone: the same
development-signed app can use either Xcode StoreKit testing or App Store
Sandbox.

| Environment | Supported reset path | Required boundary |
| --- | --- | --- |
| Xcode StoreKit configuration | For an interactive run, use **Debug > StoreKit > Manage Transactions**, select the running app and delete the target transaction or all transactions. For an automated test session, use `SKTestSession.deleteTransaction(identifier:)` or `clearTransactions()` after loading the intended `.storekit` configuration. | Scope the action to the local test environment. A test passing does not prove that a different running app session was cleared. |
| App Store Sandbox, including a development-signed app or TestFlight | When the verified transaction belongs to a designated Sandbox Apple Account, use **Users and Access > Sandbox** in App Store Connect, select the exact tester, and choose **Clear Purchase History**. Restart the app and refresh entitlements after propagation. If macOS exposes that Sandbox Account in App Store Settings, sign it out and back in; do not assume this entry is always present. | Clearing a tester deletes all of that tester's Sandbox purchase history, can take time to propagate, and is irreversible. Obtain explicit user authorization for the exact tester before performing the App Store Connect action. TestFlight may attribute a purchase to the current Media & Purchases Apple Account instead; do not claim that clearing an unrelated Sandbox tester affects it. Use a genuinely fresh account for a repeatable first-purchase test. |
| Production App Store | There is no developer-side reset. A non-consumable remains owned unless Apple refunds or revokes it. Cancelling an auto-renewable subscription stops a future renewal; it does not erase access that remains valid through the current period. | Never modify production receipts, private StoreKit databases, or app data to imitate revocation. Use Xcode StoreKit or Sandbox for repeatable purchase tests. |

Do not delete the app, its container, `UserDefaults`, receipts, or
`storekitagent` caches as a purchase reset. The app must derive access from
verified StoreKit entitlements rather than a locally persisted `isPro` flag.
A `#if DEBUG` entitlement override may support screenshot or free-tier UI
testing, but label it as an override: it does not clear StoreKit history and
does not prove that purchase or restore can be repeated.

After a reset, relaunch the exact build or invoke its entitlement refresh, then
verify through public StoreKit APIs that the target product is absent from
verified `Transaction.currentEntitlements`. For a fresh-purchase test, also
confirm that the intended product can be purchased again. Record the
environment, Bundle ID, product ID, reset action, affected test account when
applicable, entitlement result, and focused test result. Do not log signed
transaction payloads, receipts, account email addresses, or credentials.

## Non-Negotiable Invariants

1. Choose the final Team ID and explicit Bundle ID before permission testing.
   Keep both stable across development installs so TCC grants remain attached
   to one designated requirement.
2. Sign every user-tested app with Apple Development. Ad-hoc or changing
   signatures are disposable artifacts and must not be used to diagnose
   persistent permissions.
3. Treat every privacy-sensitive capability declared by the app as a separate
   permission domain. Request it at first use through its system API; opening
   System Settings is only a denied-state recovery. Do not add or test
   capabilities the product does not use.
4. Keep `.storekit`, mock prices, screenshot hooks, and test fixtures out of
   Release resources. Gate diagnostic code with `#if DEBUG`.
5. Increment `CFBundleVersion` for every uploaded build. Never try to replace a
   build already accepted by App Store Connect.
6. Do not submit a paid app or IAP while its Paid Apps Agreement, payout bank,
   or required tax forms are anything other than active, or before the exact
   candidate build loads the real localized product and completes a Sandbox
   purchase and restore.
7. Create the App Store Connect app record before upload. The first purchase of
   each In-App Purchase type must be submitted in the same review submission as
   a new app version.
8. Mac product and In-App Purchase review screenshots must match an accepted
   Mac screenshot size and contain no alpha channel.
9. Archive/upload authorization does not imply authority to accept legal or tax
   agreements, choose prices, spend money, or click the final Submit for Review.
   Require an explicit user decision for those actions.
10. Never claim a macOS app came from TestFlight based on the TestFlight UI or
    Bundle ID alone. Verify its process path, TestFlight signature, receipt, and
    exact version/build before exercising or reporting candidate behavior.

## Gate Sequence

### 1. Establish The Baseline

- Inspect the repository, build system, dirty worktree, deployment target,
  Bundle ID, Team ID, version/build, entitlements, Info.plist, StoreKit model,
  and distribution channels.
- For a first paid app or first IAP, run the commercial-account preflight and
  surface incomplete agreement, bank, or tax status before implementation and
  submission work continues.
- Record which behavior belongs to the App Store target. Keep legacy direct
  distribution, license keys, DMG updates, and external purchase links outside
  that target.
- Identify user-owned choices early: app name, paid/free model, regions,
  pricing, legal entity, privacy behavior, and release timing.

### 2. Reach Development-Ready

- Build with complete Xcode, automatic signing, Sandbox, Hardened Runtime, and
  only the entitlements justified by implemented behavior.
- Install a stable Apple Development-signed bundle for hardware and TCC tests.
- Test each declared permission's first-use and denied-state paths. Exercise the
  app's representative core workflows, persistence across relaunch or update,
  supported localizations, and interruption recovery only where applicable.
- Add pure policy tests for time or entitlement boundaries and deterministic
  StoreKit entitlement tests before attempting UI purchase automation.

### 3. Reach Upload-Ready

- Finish App Store record, In-App Purchase identifiers, support/privacy URLs,
  metadata draft, privacy answers, age rating, and screenshot plan.
- Run the focused tests, then the full suite. Preserve the `.xcresult` path and
  read its summary.
- Create a Release archive and verify identity, Team, Bundle ID, version/build,
  architectures, entitlements, resources, and absence of test artifacts.

### 4. Upload Without Submitting

- Use Xcode automatic signing and `app-store-connect` export with destination
  `upload`. Managed distribution certificates may exist only in Xcode's remote
  signing flow and therefore not appear in `security find-identity`.
- Treat `Upload succeeded` as upload evidence, not processing or review
  evidence. Wait for the exact build to become selectable in App Store Connect.
- If a production-visible change is made after upload, increment the build,
  archive again, and upload the replacement before review.

### 5. TestFlight And Review

- Unregister every exact conflicting local bundle path, run `lsregister -gc`,
  verify no conflicting registration remains, install the exact candidate build
  from TestFlight, and pass the TestFlight candidate identity gate before
  testing behavior. Verify declared first-use permissions, representative core
  workflows and persistence, StoreKit product and localized price, purchase,
  entitlement refresh, and Restore Purchases when the app sells an IAP.
- Do not treat TestFlight as passed when the product name appears without the
  localized price, when `Product.products(for:)` returns no matching product,
  or when only a local StoreKit configuration has been exercised.
- Use automated policy tests for quota, trial, or time boundaries; do not wait
  through a long UI session when the underlying policy is independently
  testable.
- Add the app version and first In-App Purchase to one draft submission. Confirm
  the selected build number, required metadata, agreements, privacy, age rating,
  review contact, notes, screenshots, and release mode before final submission.

## Completion Evidence

Report the exact build and artifact paths, test counts, signature identity,
entitlements, architectures, upload result, StoreKit product/price evidence,
TestFlight executable path/signature/receipt/version evidence, Paid Apps
Agreement/bank/tax statuses for paid products, remaining user-owned account
actions, and whether the final review submission was actually sent. Never
collapse "built", "uploaded", "processing", "TestFlight-tested", and
"submitted" into one status.
