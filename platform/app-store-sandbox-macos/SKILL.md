---
name: app-store-sandbox-macos
description: Run evidence-gated StoreKit testing for native macOS apps with a non-consumable In-App Purchase across Xcode local testing, Apple Sandbox, TestFlight, and entitlement lifecycle. Use for macOS IAP, Sandbox accounts, TestFlight purchase verification, Xcode StoreKit escape, or repeated purchase/restore testing; exclude iOS device deployment and auto-renewable subscription timing.
---

# macOS App Store Sandbox

Test a native macOS non-consumable purchase through four independent evidence
gates. Run the CLI shipped with this skill; projects do not need their own
wrapper or a copy of the Python implementation.

## Route The Task

- Read [references/gates.md](references/gates.md) before running a gate.
- Read [references/instrumentation.md](references/instrumentation.md) when
  integrating the logger or preparing a new TestFlight build.
- Read [references/evidence.md](references/evidence.md) when interpreting or
  auditing evidence.
- Read [references/troubleshooting.md](references/troubleshooting.md) after a
  blocked or failed gate.
- Start from [assets/iap-macos.example.json](assets/iap-macos.example.json) and
  place a project-specific `iap-macos.json` at the project root.
- Use the broader `macos-app-store-workflow` skill for agreements, archives,
  upload, review submission, permissions, or release coordination outside the
  four StoreKit gates.

Set the skill path and project root explicitly, then run status first:

```sh
SKILL_DIR=/absolute/path/to/app-store-sandbox-macos
PROJECT_ROOT=/absolute/path/to/project
python3 "$SKILL_DIR/scripts/iap_macos.py" --root "$PROJECT_ROOT" status
```

The CLI honors an existing `DEVELOPER_DIR`; otherwise it uses the active
`xcode-select -p` developer directory. Do not assume Xcode is installed at a
fixed path.

Configure exactly one Xcode container. Use `"project": "App.xcodeproj"` as in
the example, or replace it with `"workspace": "App.xcworkspace"`. Include the
selected container's build metadata and shared scheme in `source_paths`.

## Hard Rules

1. This skill is for native **macOS** apps and non-consumables. Do not route it
   through an iPhone, iOS Simulator, `devicectl`, subscription renewal rates,
   or `generic/platform=iOS`.
2. A gate can be `pass`, `fail`, `blocked`, or `pending`. Never promote an
   older result after source fingerprint, version/build, CDHash, PID, nonce, or
   app identity changes.
3. Only a verified IAP `Transaction.environment` proves the IAP transaction is
   `.xcode`, `.sandbox`, or `.production`. A verified
   `AppTransaction.environment` may corroborate modern TestFlight installation,
   but it never replaces IAP transaction evidence.
4. Gate 1 proves Xcode simulation only. It must use the configured test-only
   Bundle ID so `SKTestSession` cannot write an Octane configuration for the App
   Store Bundle ID. Gate 1 never proves App Store Connect or Sandbox readiness.
5. Gate 2 requires the ordinary Run scheme StoreKit Configuration to be `None`.
   Block if
   `~/Library/Caches/com.apple.storekitagent/Octane/<APP_BUNDLE_ID>/Configuration.storekit`
   exists for the App Store Bundle ID.
6. Apple does not require a separate macOS login for Sandbox IAP testing. A
   clean local user is optional diagnostic isolation after observed `.xcode`
   leakage, not a Sandbox account or an Apple rule.
7. The runner accepts only an opaque tester alias such as `TESTER-1`. It rejects
   email syntax, never asks for a password, stores only an export-salted digest,
   and does not authenticate to Apple. Programmatic Sandbox proof still
   requires verified IAP `Transaction.environment == .sandbox`.
8. Gate 2 requires Paid Apps Agreement, bank, and required tax forms to be
   active. Record this only from explicit user confirmation.
9. Gate 3 requires exact candidate identity plus same-process evidence. The
   private TestFlight SQLite database is optional, read-only corroboration and
   can never decide the gate. Modern Apple signing remains pending until the
   same process verifies `AppTransaction.environment == .sandbox` and the IAP
   transaction flow is Sandbox.
10. Never classify IAP environment from `_MASReceipt` strings. Never clear
    Sandbox history automatically or delete containers, receipts, StoreKit
    caches, or production purchase state.
11. Unregister exact local `.app` paths before moving or deleting them. Do not
    globally reset Launch Services or delete archives as a shortcut.
12. `source_paths` controls the project portion of the source fingerprint. Every
    entry must exist, remain inside `--root`, and avoid symbolic-link or `..`
    traversal. The CLI also hashes its own runner and evidence contract so a
    skill update makes older gate state stale.

## CLI

Use the skill CLI for every command:

```sh
python3 "$SKILL_DIR/scripts/iap_macos.py" --root "$PROJECT_ROOT" status
python3 "$SKILL_DIR/scripts/iap_macos.py" --root "$PROJECT_ROOT" 1
python3 "$SKILL_DIR/scripts/iap_macos.py" --root "$PROJECT_ROOT" 2 export --commercial-active
python3 "$SKILL_DIR/scripts/iap_macos.py" --root "$PROJECT_ROOT" 2 import --evidence /path/to/package/evidence-purchase-TIME.json
python3 "$SKILL_DIR/scripts/iap_macos.py" --root "$PROJECT_ROOT" 3 verify
python3 "$SKILL_DIR/scripts/iap_macos.py" --root "$PROJECT_ROOT" 3 monitor
python3 "$SKILL_DIR/scripts/iap_macos.py" --root "$PROJECT_ROOT" 4 import --package /path/to/package --same-sandbox-tester
```

`architecture`, the macOS `destination`, `export_root`, and stage timeouts
come from `iap-macos.json`. Gate 2 `--destination` may choose an exact package
path, but it must remain a child of the configured `export_root`.

The exported package contains a portable runner for Gate 2 and Gate 4:

```sh
python3 /path/to/package/gate2_runner.py purchase --tester-alias TESTER-1
python3 /path/to/package/gate2_runner.py relaunch --tester-alias TESTER-1
python3 /path/to/package/gate2_runner.py restore --tester-alias TESTER-1
python3 /path/to/package/gate2_runner.py replacement --tester-alias TESTER-1
# The user explicitly clears this tester's purchase history in App Store Connect.
python3 /path/to/package/gate2_runner.py cleared --history-cleared --tester-alias TESTER-1
python3 /path/to/package/gate2_runner.py repurchase --tester-alias TESTER-1
```

Omit `--tester-alias` to enter the same opaque alias through hidden input.
Never enter an email address, Apple Account, password, or other credential.

## Gate Contract

| Gate | Environment | Required result |
| --- | --- | --- |
| 1 | Xcode StoreKit | Test-only Bundle ID, exact local product, non-consumable purchase/current entitlement, `.xcode`, refund/removal, named `.xcresult`, configured tests with zero skips/failures |
| 2 | App Store Sandbox | Real localized product, purchase/finish/current entitlement all `.sandbox`, Apple Development identity, no embedded `.storekit`, no production-Bundle Octane state |
| 3 | TestFlight | Statically corroborated candidate, verified same-process Sandbox app transaction, fresh product/purchase/finish/current-entitlement/restore evidence, all IAP transactions `.sandbox` |
| 4 | Non-consumable lifecycle | Same runner identity/manifest/CDHash and manually attested tester continuity: purchase, relaunch, restore, replacement build, clear-history removal, repurchase |

If a TestFlight candidate predates the opt-in evidence logger, Gate 3 may have
static identity corroboration but must remain `pending` until a newly
instrumented build is uploaded.

## Completion Evidence

Report all four statuses, source fingerprint, config/product identity,
`.xcresult` path and test count, Gate 2 package/evidence paths, Gate 3 app path,
signature, receipt and optional TestFlight corroboration, lifecycle action
files, and every remaining manual account action. Never collapse identity
verification and purchase verification into one status.
