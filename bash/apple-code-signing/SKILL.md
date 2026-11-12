---
name: apple-code-signing
description: >
  Sign and notarize Tommy's macOS apps, CLIs and .pkg installers for distribution outside the
  Mac App Store: Developer ID certificates made from ONE global private key, App Store Connect
  API key for notarytool, temporary keychain signing, hardened runtime entitlements, stapling,
  and Gatekeeper checks on another Mac. Also covers creating certificates and API keys on
  developer.apple.com and App Store Connect with Playwriter. Use when the user asks to sign,
  codesign, notarize, staple, make a .pkg or .dmg, fix "Apple could not verify", create or renew
  a Developer ID certificate, or create an App Store Connect API key.
---

# apple-code-signing

Tommy has one Apple Developer Program membership (individual, **Tommaso De Rossi**, team ID
**`92MF9DG2LR`**, Apple Account `atrox@outlook.it`). Every app he ships outside the App Store is
signed with this team. Ghosthand (`~/Documents/GitHub/iphone-usb-control`, `npm/scripts/build.ts`)
is the reference implementation of everything below.

## Where the secrets are

| What | Where |
|---|---|
| **Global private key** (encrypted PEM) | iCloud Drive `apple-signing/apple-signing-global-private-key-tommaso-de-rossi-92MF9DG2LR.key` |
| Developer ID Application cert + key (`.p12`) | same folder `developer-id-application.p12`, Sigillo `DEVELOPER_ID_APPLICATION_P12_BASE64` |
| Developer ID Installer cert + key (`.p12`) | same folder `developer-id-installer.p12`, Sigillo `DEVELOPER_ID_INSTALLER_P12_BASE64` |
| Password of the key and both `.p12` | **only** Sigillo `DEVELOPER_ID_P12_PASSWORD` |
| App Store Connect API key (notarization) | iCloud `AuthKey_WQWA4QXU46.p8`, Sigillo `APP_STORE_CONNECT_KEY_P8`, `_KEY_ID`, `_ISSUER_ID` |
| Team ID | Sigillo `APPLE_TEAM_ID` |

Sigillo location: org **ghosthand**, project **macos-release** (`01M5WWCS9407MR455JC5AXSKX6`),
env **prod**. Local copy: `~/Documents/apple-signing` (no `.key` files there). Load the
`sigillo` skill before touching secrets. Never print a secret value; pipe it.

## Rule: one global private key for everything

**Always make every certificate signing request (CSR) from the global key.** Any app, any
certificate type (Developer ID Application, Developer ID Installer, Apple Development, ...), and
every renewal. Never `openssl genrsa` a new key; never let Keychain Access "Request a Certificate"
create one (it makes a new key pair each time). One key means one backup and one password.

The only exception is legacy: the current Developer ID Installer certificate (expires 2027-11-25)
was made with its own key (`apple-developer-id-installer-2026-only-private-key-...key`). When it
is renewed, use the global key.

```bash
KEY="$HOME/Library/Mobile Documents/com~apple~CloudDocs/apple-signing/apple-signing-global-private-key-tommaso-de-rossi-92MF9DG2LR.key"
export PW=$(sigillo secrets get DEVELOPER_ID_P12_PASSWORD -p 01M5WWCS9407MR455JC5AXSKX6 -c prod --raw)
openssl req -new -key "$KEY" -passin env:PW -out /tmp/request.csr \
  -subj "/emailAddress=atrox@outlook.it/CN=Tommaso De Rossi/C=IT"
unset PW
```

The `-subj` is the same for every certificate. Upload the CSR on developer.apple.com (below),
then build the `.p12` from the downloaded `.cer` and the global key.

## Certificates are per team, not per app

One **Developer ID Application** certificate signs every app and CLI. One **Developer ID
Installer** certificate signs every `.pkg`. Apple restricts each type to its job, so a `.pkg`
needs the second one; a zip or DMG does not. Do not create certificates per app. The current ones
expire on 2027-11-25; apps signed with a timestamp before that keep working after expiry.

## Make a .p12 macOS can import

OpenSSL 3+ (this Mac has 4.x) writes AES/PBKDF2 `.p12` files, and `security import` rejects them
with **"MAC verification failed during PKCS12 import (wrong password?)"** even with the right
password. Always use the legacy algorithms:

```bash
export PW=$(sigillo secrets get DEVELOPER_ID_P12_PASSWORD -p 01M5WWCS9407MR455JC5AXSKX6 -c prod --raw)
openssl x509 -inform der -in developerID_application.cer -out cert.pem
openssl pkcs12 -export -inkey "$KEY" -passin env:PW -in cert.pem -out out.p12 -passout env:PW \
  -name "Developer ID Application" -keypbe PBE-SHA1-3DES -certpbe PBE-SHA1-3DES -macalg sha1
unset PW
```

Reading these `.p12` files back with OpenSSL needs `-legacy`. Check the cert matches the key:
compare `openssl x509 -noout -modulus` with `openssl rsa -noout -modulus`.

Then store it: `base64 -i out.p12 | tr -d '\n' | sigillo secrets set NAME -p ... -c prod`, and copy
the `.p12` and `.cer` to the iCloud folder and `~/Documents/apple-signing`.

## Sign in builds: temporary keychain, never the login keychain

Build scripts import the `.p12` files from env into a temporary keychain, sign, and delete it.
Signing then works on any Mac with Sigillo and never shows a keychain password dialog. Copy
`signingKeychain()` from Ghosthand's `npm/scripts/build.ts`. The steps that matter:

```bash
security create-keychain -p "$PW" "$KC"
security set-keychain-settings "$KC"                # no auto-lock: notarization takes minutes
security unlock-keychain -p "$PW" "$KC"
security import app.p12 -k "$KC" -P "$PW" -T /usr/bin/codesign
security import installer.p12 -k "$KC" -P "$PW" -T /usr/bin/productbuild
security set-key-partition-list -S apple-tool:,apple: -s -k "$PW" "$KC"   # else a GUI prompt
security list-keychains -d user -s "$KC" <previous list>                   # restore it on exit
```

Pass `--keychain "$KC"` to `codesign` and `productbuild` too. Restore the search list and delete
the keychain on exit, and only if the file still exists.

## Sign the app

```bash
codesign --force --timestamp --options runtime --entitlements app.entitlements \
  --keychain "$KC" --sign "Developer ID Application: Tommaso De Rossi (92MF9DG2LR)" Foo.app
codesign --verify --strict --verbose=2 Foo.app
```

- **Hardened runtime** (`--options runtime`) is required for notarization. It blocks camera and
  microphone unless the entitlements file has `com.apple.security.device.camera` and
  `com.apple.security.device.audio-input`. Add only what the app uses.
- **Never re-sign on the user's Mac.** Ship the signed bundle and copy it as is. Ad-hoc signing on
  the user's machine changes the identity, and macOS forgets the app's permissions (TCC).
- A Developer ID signature's designated requirement is bundle id + team, so permissions survive
  updates and different builds (tested: a separately signed build copied over the installed one
  kept Camera access). Keep the bundle id fixed forever.
- **Sign dev builds with the same Developer ID**, not ad-hoc. Then dev, npm and installer builds
  share one identity and one set of permissions. Moving a Mac from an ad-hoc build to a Developer
  ID build makes macOS ask for each permission once more.
- Private frameworks (MobileDevice, CoreBluetooth private calls) work under hardened runtime:
  Ghosthand's signed build captured the iPhone screen, sent Bluetooth input and read USB info.

## Notarize and staple

Use the App Store Connect API key, never an Apple ID password. Write the `.p8` to a temp file,
delete it after.

```bash
xcrun notarytool submit Foo.zip --key AuthKey.p8 --key-id "$KEY_ID" --issuer "$ISSUER" \
  --wait --output-format json        # status must be "Accepted"
xcrun notarytool log <submission id> --key ... --key-id ... --issuer ...   # why it failed
xcrun stapler staple Foo.app
```

- Submit an app as a zip: `ditto -c -k --keepParent Foo.app Foo.zip`. Staple the `.app`, then
  zip it again for distribution.
- Notarize and staple a signed `.pkg` too (`notarytool submit Foo.pkg`, `stapler staple Foo.pkg`).
- The full Ghosthand release build, including both notarizations, took about 4 minutes.

## .pkg installer for the current user (no admin password)

`productbuild` with a distribution file that enables only the user's home domain installs into
`~/Applications` without asking for a password (tested on macOS 26 with
`installer -pkg Foo.pkg -target CurrentUserHomeDirectory`, no sudo):

```xml
<domains enable_anywhere="false" enable_currentUserHome="true" enable_localSystem="false"/>
```

- Set `BundleIsRelocatable` to `NO` in the component plist (`pkgbuild --analyze`, then
  `plutil -replace 0.BundleIsRelocatable -bool NO`), else the installer may update a copy with the
  same bundle id somewhere else (an npm cache, a dev build).
- A `postinstall` script that opens the app must use `open -n`: plain `open` only brings an old
  running instance to the front, so the old version keeps running.
- Ghosthand's `npm/scripts/build.ts` builds this end to end.

## Verify like a user

Local files are not quarantined, so Gatekeeper never checks them on the build Mac. Test on
another Mac (load the `lan-macs` skill; `mintmacbook` works) after copying with `scp`, and add
the quarantine flag a browser would set:

```bash
xattr -w com.apple.quarantine "0083;$(printf %x $(date +%s));Safari;" Foo.pkg
spctl -a -vv -t install Foo.pkg     # pkg: "accepted, source=Notarized Developer ID"
spctl -a -vv -t exec Foo.app        # app
codesign -dvv Foo.app               # Authority=Developer ID Application..., flags=runtime
pkgutil --check-signature Foo.pkg
```

`curl` downloads are not quarantined either, so add the flag after `curl` too. A notarized,
stapled build shows `accepted, source=Notarized Developer ID` for both the pkg and the installed
app. `rejected, source=Unnotarized Developer ID` means signing worked but notarization or stapling is
missing. Unsigned or unnotarized downloads show "Apple could not verify" with no Open button on
macOS 15+; users would need System Settings > Privacy & Security > Open Anyway.

## Apple websites with Playwriter

Load the `playwriter` skill and drive the user's Chrome, signed in to the Apple Account. Never
type the Apple Account password or 2FA codes; ask the user.

- **Create a certificate:** https://developer.apple.com/account/resources/certificates/add.
  Radio ids are random per load: use `getByRole('radio', { name: /^Developer ID Installer/ })`.
  The Continue button id changes per step (`action-continue`, then `action-save`): use
  `getByRole('button', { name: 'Continue' }).first()`. Developer ID Application asks for a Sub-CA:
  pick **G2 Sub-CA**. Upload the CSR with `setInputFiles` on `input[type=file]`.
- **Download the .cer:** Playwright's download event did not fire here; the click saves
  `developerID_application.cer` into `~/Downloads`. Each extra click adds a ` (1)` copy, so move
  the file and delete duplicates.
- **App Store Connect API key:** https://appstoreconnect.apple.com/access/integrations/api. First
  the account holder must accept the App Store Connect Terms of Service in the browser (a legal
  agreement: ask the user to click Agree). Then **Request Access**, tick the checkbox, Submit (it
  is approved at once), **Generate API Key**. In the dialog: fill `[id="name"]`, click the
  **Select Roles** textbox, pick `menuitem` **Developer** (enough for notarytool), press Escape to
  close the menu, then the dialog's **Generate**. The first Generate click may not register;
  reload the page and check for the key row before clicking again, so you do not make two keys.
- **Download the .p8:** the key row's **Download** opens a confirmation dialog with a second
  **Download**; the file lands in `~/Downloads/AuthKey_<KEY ID>.p8`. It **downloads only once**:
  save it to iCloud `apple-signing` and Sigillo right away, then delete it from Downloads.
  Key ID and Issuer ID stay visible on that page.
- **Team ID** is on https://developer.apple.com/account (Membership details).

## Enrollment and account gotchas

- The web store checkout for the membership can spin forever: after Apple sign-in,
  `secure*.store.apple.com/.../shop/signIn/idms/authx` returns **HTTP 541** (server side). Enroll
  in the **Apple Developer app** (App Store, Account, Enroll) instead.
- After paying, developer.apple.com shows the account as **Pending** until Apple processes it
  (up to 48 h; took about an hour). The "Welcome to the Apple Developer Program" email arrives at
  `atrox@outlook.it` (read it with the `zele` skill, account `atrox@outlook.it`).
- Membership is $99/year and auto-renews. If it lapses, existing signed apps keep working but no
  new builds can be signed or notarized.
