---
name: cryptotokenkit
description: "Access security tokens and smart cards using CryptoTokenKit. Use when building token driver extensions with TKTokenDriver and TKToken, communicating with smart cards via TKSmartCard, implementing certificate-based authentication, managing token sessions, or integrating hardware security tokens with the system keychain."
---

# CryptoTokenKit

Access security tokens and the cryptographic assets they store using the
CryptoTokenKit framework. Covers token driver extensions, smart card
communication, token sessions, keychain integration, and certificate-based
authentication. Targets Swift 6.3.

**Platform availability:** CryptoTokenKit is primarily a macOS framework.
Smart card reader access (`TKSmartCard`, `TKSmartCardSlotManager`) requires
macOS. Token extension APIs (`TKTokenDriver`, `TKToken`, `TKTokenSession`)
are macOS-only. Client-side token watching (`TKTokenWatcher`) and keychain
queries filtered by `kSecAttrTokenID` are available on iOS 14+/macOS 11+.
NFC smart card slot sessions are available on iOS 16.4+.

## Contents

- [Architecture Overview](#architecture-overview)
- [Token Extensions](#token-extensions)
- [Token Sessions](#token-sessions)
- [Smart Card Communication](#smart-card-communication)
- [Keychain Integration](#keychain-integration)
- [Certificate Authentication](#certificate-authentication)
- [Token Watching](#token-watching)
- [Error Handling](#error-handling)
- [Common Mistakes](#common-mistakes)
- [Review Checklist](#review-checklist)
- [References](#references)

## Architecture Overview

CryptoTokenKit bridges hardware security tokens (smart cards, USB tokens)
with macOS authentication and keychain services. The framework has two main
usage modes:

**Token driver extensions** (macOS only) -- App extensions that make a
hardware token's cryptographic items available to the system. The driver
handles token lifecycle, session management, and cryptographic operations.

**Client-side token access** (macOS + iOS) -- Apps query the keychain for
items backed by tokens. CryptoTokenKit automatically exposes token items as
standard keychain entries when a token is present.

### Key Types

| Type | Role | Platform |
|---|---|---|
| `TKTokenDriver` | Base class for token driver extensions | macOS |
| `TKToken` | Represents a hardware cryptographic token | macOS |
| `TKTokenSession` | Manages authentication state for a token | macOS |
| `TKSmartCardTokenDriver` | Entry point for smart card extensions | macOS |
| `TKSmartCard` | Low-level smart card communication | macOS |
| `TKSmartCardSlotManager` | Discovers and manages card reader slots | macOS |
| `TKTokenWatcher` | Observes token insertion and removal | macOS, iOS 14+ |
| `TKTokenKeychainKey` | A key stored on a token | macOS |
| `TKTokenKeychainCertificate` | A certificate stored on a token | macOS |

## Token Extensions

A token driver is a macOS app extension that makes a hardware token's
cryptographic capabilities available to the system. The host app exists
only as a delivery mechanism for the extension.

A smart card token extension has three core classes:

1. **TokenDriver** (subclass of `TKSmartCardTokenDriver`) -- entry point
2. **Token** (subclass of `TKSmartCardToken`) -- represents the token
3. **TokenSession** (subclass of `TKSmartCardTokenSession`) -- handles operations

### Driver Class

```swift
import CryptoTokenKit

final class TokenDriver: TKSmartCardTokenDriver, TKSmartCardTokenDriverDelegate {
    func tokenDriver(
        _ driver: TKSmartCardTokenDriver,
        createTokenFor smartCard: TKSmartCard,
        aid: Data?
    ) throws -> TKSmartCardToken {
        return try Token(
            smartCard: smartCard,
            aid: aid,
            instanceID: "com.example.token:\(smartCard.slot.name)",
            tokenDriver: driver
        )
    }
}
```

### Token Class

The token reads certificates and keys from hardware and populates its
keychain contents:

```swift
final class Token: TKSmartCardToken, TKTokenDelegate {
    init(
        smartCard: TKSmartCard, aid: Data?,
        instanceID: String, tokenDriver: TKSmartCardTokenDriver
    ) throws {
        try super.init(
            smartCard: smartCard, aid: aid,
            instanceID: instanceID, tokenDriver: tokenDriver
        )
        self.delegate = self

        let certData = try readCertificate(from: smartCard)
        guard let cert = SecCertificateCreateWithData(nil, certData as CFData) else {
            throw TKError(.corruptedData)
        }

        let certItem = TKTokenKeychainCertificate(certificate: cert, objectID: "cert-auth")
        let keyItem = TKTokenKeychainKey(certificate: cert, objectID: "key-auth")
        keyItem?.canSign = true
        keyItem?.canDecrypt = false
        keyItem?.isSuitableForLogin = true

        self.keychainContents?.fill(with: [certItem!, keyItem!])
    }

    func createSession(_ token: TKToken) throws -> TKTokenSession {
        TokenSession(token: token)
    }
}
```

### Info.plist and Registration

The extension's `Info.plist` must name the driver class:

```
NSExtension
  NSExtensionAttributes
    com.apple.ctk.driver-class = $(PRODUCT_MODULE_NAME).TokenDriver
  NSExtensionPointIdentifier = com.apple.ctk-tokens
```

Register the extension once by launching the host app as `_securityagent`:

```shell
sudo -u _securityagent /Applications/TokenHost.app/Contents/MacOS/TokenHost
```

## Token Sessions

`TKTokenSession` manages authentication state and performs cryptographic
operations via its delegate.

```swift
final class TokenSession: TKSmartCardTokenSession, TKTokenSessionDelegate {
    func tokenSession(
        _ session: TKTokenSession,
        supports operation: TKTokenOperation,
        keyObjectID: TKToken.ObjectID,
        algorithm: TKTokenKeyAlgorithm
    ) -> Bool {
        switch operation {
        case .signData:
            return algorithm.isAlgorithm(.rsaSignatureDigestPKCS1v15SHA256)
                || algorithm.isAlgorithm(.ecdsaSignatureDigestX962SHA256)
        case .decryptData:
            return algorithm.isAlgorithm(.rsaEncryptionOAEPSHA256)
        case .performKeyExchange:
            return algorithm.isAlgorithm(.ecdhKeyExchangeStandard)
        default:
            return false
        }
    }

    func tokenSession(
        _ session: TKTokenSession,
        sign dataToSign: Data,
        keyObjectID: TKToken.ObjectID,
        algorithm: TKTokenKeyAlgorithm
    ) throws -> Data {
        let smartCard = try getSmartCard()
        return try smartCard.withSession {
            try performCardSign(smartCard: smartCard, data: dataToSign, keyID: keyObjectID)
        }
    }

    func tokenSession(
        _ session: TKTokenSession,
        decrypt ciphertext: Data,
        keyObjectID: TKToken.ObjectID,
        algorithm: TKTokenKeyAlgorithm
    ) throws -> Data {
        let smartCard = try getSmartCard()
        return try smartCard.withSession {
            try performCardDecrypt(smartCard: smartCard, data: ciphertext, keyID: keyObjectID)
        }
    }
}
```

### PIN Authentication

Return a `TKTokenAuthOperation` from `beginAuthFor:` to prompt the user
for PIN entry before cryptographic operations:

```swift
func tokenSession(
    _ session: TKTokenSession,
    beginAuthFor operation: TKTokenOperation,
    constraint: Any
) throws -> TKTokenAuthOperation {
    let pinAuth = TKTokenSmartCardPINAuthOperation()
    pinAuth.pinFormat.charset = .numeric
    pinAuth.pinFormat.minPINLength = 4
    pinAuth.pinFormat.maxPINLength = 8
    pinAuth.smartCard = (session as? TKSmartCardTokenSession)?.smartCard
    pinAuth.apduTemplate = buildVerifyAPDU()
    pinAuth.pinByteOffset = 5
    return pinAuth
}
```

## Smart Card Communication

`TKSmartCard` provides low-level APDU communication with smart cards
connected via readers (macOS-only).

### Discovering Card Readers

```swift
import CryptoTokenKit

func discoverSmartCards() {
    guard let slotManager = TKSmartCardSlotManager.default else {
        print("Smart card services unavailable")
        return
    }

    for slotName in slotManager.slotNames {
        slotManager.getSlot(withName: slotName) { slot in
            guard let slot else { return }
            if slot.state == .validCard, let card = slot.makeSmartCard() {
                communicateWith(card: card)
            }
        }
    }
}
```

### Sending APDU Commands

Use `send(ins:p1:p2:data:le:)` for structured APDU communication.
Always wrap calls in `withSession`:

```swift
func selectApplication(card: TKSmartCard, aid: Data) throws {
    try card.withSession {
        let (sw, response) = try card.send(
            ins: 0xA4, p1: 0x04, p2: 0x00, data: aid, le: nil
        )
        guard sw == 0x9000 else {
            throw TKError(.communicationError)
        }
    }
}
```

For raw APDU bytes or non-standard formats, use `transmit(_:reply:)` with
manual `beginSession`/`endSession` lifecycle management.

### NFC Smart Card Sessions (iOS 16.4+)

On supported iOS devices, create NFC smart card sessions to communicate
with contactless smart cards:

```swift
func readNFCSmartCard() {
    guard let slotManager = TKSmartCardSlotManager.default,
          slotManager.isNFCSupported() else { return }

    slotManager.createNFCSlot(message: "Hold card near iPhone") { session, error in
        guard let session else { return }
        defer { session.end() }

        guard let slotName = session.slotName,
              let slot = slotManager.slotNamed(slotName),
              let card = slot.makeSmartCard() else { return }
        // Communicate with the NFC card using card.send(...)
    }
}
```

## Keychain Integration

When a token is present, CryptoTokenKit exposes its items as standard
keychain entries. Query them using the `kSecAttrTokenID` attribute:

```swift
import Security

func findTokenKey(tokenID: String) throws -> SecKey {
    let query: [String: Any] = [
        kSecClass as String: kSecClassKey,
        kSecAttrTokenID as String: tokenID,
        kSecReturnRef as String: true
    ]
    var result: CFTypeRef?
    let status = SecItemCopyMatching(query as CFDictionary, &result)
    guard status == errSecSuccess, let key = result else {
        throw TKError(.objectNotFound)
    }
    return key as! SecKey
}
```

Use `kSecReturnPersistentRef` instead of `kSecReturnRef` to obtain a
persistent reference that survives across app launches. The reference
becomes invalid when the token is removed -- handle `errSecItemNotFound`
by prompting the user to reinsert the token.

Query certificates the same way with `kSecClass: kSecClassCertificate`.

## Certificate Authentication

### Token Key Requirements

For user login, the token must contain at least one key capable of signing
with: EC signature digest X962, RSA signature digest PSS, or RSA signature
digest PKCS1v15.

For keychain unlock, the token needs:
- 256-bit EC key (`kSecAttrKeyTypeECSECPrimeRandom`) supporting
  `ecdhKeyExchangeStandard`, or
- 2048/3072/4096-bit RSA key (`kSecAttrKeyTypeRSA`) supporting
  `rsaEncryptionOAEPSHA256` decryption

### Smart Card Authentication Preferences (macOS)

Configure in the `com.apple.security.smartcard` domain (MDM or systemwide):

| Key | Default | Description |
|---|---|---|
| `allowSmartCard` | `true` | Enable smart card authentication |
| `checkCertificateTrust` | `0` | Certificate trust level (0-3) |
| `oneCardPerUser` | `false` | Pair a single smart card to an account |
| `enforceSmartCard` | `false` | Require smart card for login |

Trust levels: `0` = trust all, `1` = validity + issuer, `2` = + soft
revocation, `3` = + hard revocation.

## Token Watching

`TKTokenWatcher` monitors token insertion and removal. Available on both
macOS and iOS 14+.

```swift
import CryptoTokenKit

final class TokenMonitor {
    private let watcher = TKTokenWatcher()

    func startMonitoring() {
        for tokenID in watcher.tokenIDs {
            print("Token present: \(tokenID)")
            if let info = watcher.tokenInfo(forTokenID: tokenID) {
                print("  Driver: \(info.driverName ?? "unknown")")
                print("  Slot: \(info.slotName ?? "unknown")")
            }
        }

        watcher.setInsertionHandler { [weak self] tokenID in
            print("Token inserted: \(tokenID)")
            self?.watcher.addRemovalHandler({ removedTokenID in
                print("Token removed: \(removedTokenID)")
            }, forTokenID: tokenID)
        }
    }
}
```

## Error Handling

CryptoTokenKit operations throw `TKError`. Key error codes:

| Code | Meaning |
|---|---|
| `.notImplemented` | Operation not supported by this token |
| `.communicationError` | Communication with token failed |
| `.corruptedData` | Data from token is corrupted |
| `.canceledByUser` | User canceled the operation |
| `.authenticationFailed` | PIN or password incorrect |
| `.objectNotFound` | Requested key or certificate not found |
| `.tokenNotFound` | Token is no longer present |
| `.authenticationNeeded` | Authentication required before operation |

## Common Mistakes

### DON'T: Query token keychain items without checking token presence

```swift
// WRONG -- query may fail if token was removed
let key = try findTokenKey(tokenID: savedTokenID)

// CORRECT -- verify the token is still present first
let watcher = TKTokenWatcher()
guard watcher.tokenIDs.contains(savedTokenID) else {
    promptUserToInsertToken()
    return
}
let key = try findTokenKey(tokenID: savedTokenID)
```

### DON'T: Assume smart card APIs work on iOS

```swift
// WRONG -- TKSmartCardSlotManager.default is nil on iOS
let manager = TKSmartCardSlotManager.default!  // Crashes on iOS

// CORRECT -- guard availability
guard let manager = TKSmartCardSlotManager.default else {
    print("Smart card services unavailable on this platform")
    return
}
```

### DON'T: Skip session management for card communication

```swift
// WRONG -- sending commands without a session
card.transmit(apdu) { response, error in /* may fail */ }

// CORRECT -- use withSession or beginSession/endSession
try card.withSession {
    let (sw, response) = try card.send(
        ins: 0xCA, p1: 0x00, p2: 0x6E, data: nil, le: 0
    )
}
```

### DON'T: Ignore status words in APDU responses

```swift
// WRONG -- assuming success
let (_, response) = try card.send(ins: 0xA4, p1: 0x04, p2: 0x00, data: aid, le: nil)

// CORRECT -- check status word
let (sw, response) = try card.send(ins: 0xA4, p1: 0x04, p2: 0x00, data: aid, le: nil)
guard sw == 0x9000 else {
    throw SmartCardError.commandFailed(statusWord: sw)
}
```

### DON'T: Hard-code blanket algorithm support

The `supports` delegate method must reflect what the hardware actually
implements. Returning `true` unconditionally causes runtime failures when
the system attempts unsupported operations.

## Review Checklist

- [ ] Platform availability verified (`TKSmartCard` macOS-only, `TKTokenWatcher` iOS 14+)
- [ ] Token extension target uses `NSExtensionPointIdentifier` = `com.apple.ctk-tokens`
- [ ] `com.apple.ctk.driver-class` set to the correct driver class in Info.plist
- [ ] Extension registered via `_securityagent` launch during installation
- [ ] `TKTokenSessionDelegate` checks specific algorithms, not blanket `true`
- [ ] Smart card sessions opened and closed (`withSession` or `beginSession`/`endSession`)
- [ ] APDU status words checked after every `send` call
- [ ] Token presence verified via `TKTokenWatcher` before keychain queries
- [ ] `TKError` cases handled with appropriate user feedback
- [ ] Keychain contents populated with correct `objectID` values
- [ ] `TKTokenKeychainKey` capabilities (`canSign`, `canDecrypt`) match hardware
- [ ] Certificate trust level configured appropriately for deployment environment
- [ ] `errSecItemNotFound` handled for persistent references when token is removed

## References

- Extended patterns (PIV commands, TLV parsing, generic token drivers, APDU helpers, secure PIN): [references/cryptotokenkit-patterns.md](references/cryptotokenkit-patterns.md)
- [CryptoTokenKit framework](https://sosumi.ai/documentation/cryptotokenkit)
- [TKTokenDriver](https://sosumi.ai/documentation/cryptotokenkit/tktokendriver)
- [TKToken](https://sosumi.ai/documentation/cryptotokenkit/tktoken)
- [TKTokenSession](https://sosumi.ai/documentation/cryptotokenkit/tktokensession)
- [TKSmartCard](https://sosumi.ai/documentation/cryptotokenkit/tksmartcard)
- [TKSmartCardSlotManager](https://sosumi.ai/documentation/cryptotokenkit/tksmartcardslotmanager)
- [TKTokenWatcher](https://sosumi.ai/documentation/cryptotokenkit/tktokenwatcher)
- [Authenticating Users with a Cryptographic Token](https://sosumi.ai/documentation/cryptotokenkit/authenticating-users-with-a-cryptographic-token)
- [Using Cryptographic Assets Stored on a Smart Card](https://sosumi.ai/documentation/cryptotokenkit/using-cryptographic-assets-stored-on-a-smart-card)
- [Configuring Smart Card Authentication](https://sosumi.ai/documentation/cryptotokenkit/configuring-smart-card-authentication)
