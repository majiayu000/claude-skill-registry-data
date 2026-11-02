---
name: device-integrity
description: "Verify device legitimacy and app integrity using DeviceCheck (DCDevice per-device bits) and App Attest (DCAppAttestService key generation, attestation, and assertion flows). Use when implementing fraud prevention, detecting compromised devices, validating app authenticity with Apple's servers, protecting sensitive API endpoints with attested requests, or adding device verification to a backend architecture."
---

# Device Integrity

Verify that requests to your server come from a genuine Apple device running
your unmodified app. DeviceCheck provides per-device bits for simple flags
(e.g., "claimed promo offer"). App Attest uses Secure Enclave keys and Apple
attestation to cryptographically prove app legitimacy on each request.

## Contents

- [DCDevice (DeviceCheck Tokens)](#dcdevice-devicecheck-tokens)
- [DCAppAttestService (App Attest)](#dcappattestservice-app-attest)
- [App Attest Key Generation](#app-attest-key-generation)
- [App Attest Attestation Flow](#app-attest-attestation-flow)
- [App Attest Assertion Flow](#app-attest-assertion-flow)
- [Server Verification Guidance](#server-verification-guidance)
- [Error Handling](#error-handling)
- [Common Patterns](#common-patterns)
- [Common Mistakes](#common-mistakes)
- [Review Checklist](#review-checklist)
- [References](#references)

## DCDevice (DeviceCheck Tokens)

[`DCDevice`](https://sosumi.ai/documentation/devicecheck/dcdevice) generates a
unique, ephemeral token that identifies a device. The token is sent to your
server, which then communicates with Apple's servers to read or set two
per-device bits. Available on iOS 11+.

### Token Generation

```swift
import DeviceCheck

func generateDeviceToken() async throws -> Data {
    guard DCDevice.current.isSupported else {
        throw DeviceIntegrityError.deviceCheckUnsupported
    }

    return try await DCDevice.current.generateToken()
}
```

### Sending the Token to Your Server

```swift
func sendTokenToServer(_ token: Data) async throws {
    let tokenString = token.base64EncodedString()

    var request = URLRequest(url: serverURL.appending(path: "verify-device"))
    request.httpMethod = "POST"
    request.setValue("application/json", forHTTPHeaderField: "Content-Type")
    request.httpBody = try JSONEncoder().encode(["device_token": tokenString])

    let (_, response) = try await URLSession.shared.data(for: request)
    guard let httpResponse = response as? HTTPURLResponse,
          httpResponse.statusCode == 200 else {
        throw DeviceIntegrityError.serverVerificationFailed
    }
}
```

### Server-Side Overview

Your server uses the device token to call Apple's DeviceCheck API endpoints:

| Endpoint | Purpose |
|----------|---------|
| `https://api.devicecheck.apple.com/v1/query_two_bits` | Read the two bits for a device |
| `https://api.devicecheck.apple.com/v1/update_two_bits` | Set the two bits for a device |
| `https://api.devicecheck.apple.com/v1/validate_device_token` | Validate a device token without reading bits |

The server authenticates with a DeviceCheck private key from the Apple Developer
portal, creating a signed JWT for each request.

### What the Two Bits Are For

Apple stores two Boolean values per device per developer team. You decide what
they mean. Common uses:

- **Bit 0:** Device has claimed a promotional offer.
- **Bit 1:** Device has been flagged for fraud.

Bits persist across app reinstall. You control when to reset them via the
server API.

## DCAppAttestService (App Attest)

[`DCAppAttestService`](https://sosumi.ai/documentation/devicecheck/dcappattestservice)
validates that a specific instance of your app on a specific device is
legitimate. It uses a hardware-backed key in the Secure Enclave to create
cryptographic attestations and assertions. Available on iOS 14+.

The flow has three phases:
1. **Key generation** -- create a key pair in the Secure Enclave.
2. **Attestation** -- Apple certifies the key belongs to a genuine Apple device running your app.
3. **Assertion** -- sign server requests with the attested key to prove ongoing legitimacy.

### Checking Support

```swift
import DeviceCheck

let attestService = DCAppAttestService.shared

guard attestService.isSupported else {
    // Fall back to DCDevice token or other risk assessment.
    // App Attest is not available on simulators or all device models.
    return
}
```

## App Attest Key Generation

Generate a cryptographic key pair stored in the Secure Enclave. The returned
`keyId` is a string identifier you persist (e.g., in Keychain) for later
attestation and assertion calls.

```swift
import DeviceCheck

actor AppAttestManager {
    private let service = DCAppAttestService.shared
    private var keyId: String?

    /// Generate and persist a key pair for App Attest.
    func generateKeyIfNeeded() async throws -> String {
        if let existingKeyId = loadKeyIdFromKeychain() {
            self.keyId = existingKeyId
            return existingKeyId
        }

        let newKeyId = try await service.generateKey()
        saveKeyIdToKeychain(newKeyId)
        self.keyId = newKeyId
        return newKeyId
    }

    // MARK: - Keychain helpers (simplified)

    private func saveKeyIdToKeychain(_ keyId: String) {
        let data = Data(keyId.utf8)
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrAccount as String: "app-attest-key-id",
            kSecAttrService as String: Bundle.main.bundleIdentifier ?? "",
            kSecValueData as String: data,
            kSecAttrAccessible as String: kSecAttrAccessibleAfterFirstUnlockThisDeviceOnly
        ]
        SecItemDelete(query as CFDictionary) // Remove old if exists
        SecItemAdd(query as CFDictionary, nil)
    }

    private func loadKeyIdFromKeychain() -> String? {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrAccount as String: "app-attest-key-id",
            kSecAttrService as String: Bundle.main.bundleIdentifier ?? "",
            kSecReturnData as String: true,
            kSecMatchLimit as String: kSecMatchLimitOne
        ]
        var result: AnyObject?
        let status = SecItemCopyMatching(query as CFDictionary, &result)
        guard status == errSecSuccess, let data = result as? Data else { return nil }
        return String(data: data, encoding: .utf8)
    }
}
```

**Important:** Generate the key once and persist the `keyId`. Generating a new
key invalidates any previous attestation.

## App Attest Attestation Flow

Attestation proves that the key was generated on a genuine Apple device running
your unmodified app. You perform attestation once per key, then store the
attestation object on your server.

### Client-Side Attestation

```swift
import DeviceCheck
import CryptoKit

extension AppAttestManager {
    /// Attest the key with Apple. Send the attestation object to your server.
    func attestKey() async throws -> Data {
        guard let keyId else {
            throw DeviceIntegrityError.keyNotGenerated
        }

        // 1. Request a one-time challenge from your server
        let challenge = try await fetchServerChallenge()

        // 2. Hash the challenge (Apple requires a SHA-256 hash)
        let challengeHash = Data(SHA256.hash(data: challenge))

        // 3. Ask Apple to attest the key
        let attestation = try await service.attestKey(keyId, clientDataHash: challengeHash)

        // 4. Send the attestation object to your server for verification
        try await sendAttestationToServer(
            keyId: keyId,
            attestation: attestation,
            challenge: challenge
        )

        return attestation
    }

    private func fetchServerChallenge() async throws -> Data {
        let url = serverURL.appending(path: "attest/challenge")
        let (data, _) = try await URLSession.shared.data(from: url)
        return data
    }

    private func sendAttestationToServer(
        keyId: String,
        attestation: Data,
        challenge: Data
    ) async throws {
        var request = URLRequest(url: serverURL.appending(path: "attest/verify"))
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")

        let payload: [String: String] = [
            "key_id": keyId,
            "attestation": attestation.base64EncodedString(),
            "challenge": challenge.base64EncodedString()
        ]
        request.httpBody = try JSONEncoder().encode(payload)

        let (_, response) = try await URLSession.shared.data(for: request)
        guard let httpResponse = response as? HTTPURLResponse,
              httpResponse.statusCode == 200 else {
            throw DeviceIntegrityError.attestationVerificationFailed
        }
    }
}
```

### Server-Side Attestation Verification

Your server validates the attestation object (CBOR), verifies the certificate chain against Apple's App Attest root CA, and stores the public key and receipt for future assertion verification. See [references/device-integrity-patterns.md](references/device-integrity-patterns.md) for the full server verification flow.

## App Attest Assertion Flow

After attestation, use assertions to sign individual requests. Each assertion
proves the request came from the attested app instance.

### Client-Side Assertion

```swift
import DeviceCheck
import CryptoKit

extension AppAttestManager {
    /// Generate an assertion to accompany a server request.
    /// - Parameter requestData: The request payload to sign (e.g., JSON body).
    /// - Returns: The assertion data to include with the request.
    func generateAssertion(for requestData: Data) async throws -> Data {
        guard let keyId else {
            throw DeviceIntegrityError.keyNotGenerated
        }

        // Hash the request data -- the server will verify this matches
        let clientDataHash = Data(SHA256.hash(data: requestData))

        return try await service.generateAssertion(keyId, clientDataHash: clientDataHash)
    }
}
```

### Using Assertions in Network Requests

```swift
extension AppAttestManager {
    /// Perform an attested API request.
    func makeAttestedRequest(
        to url: URL,
        method: String = "POST",
        body: Data
    ) async throws -> (Data, URLResponse) {
        let assertion = try await generateAssertion(for: body)

        var request = URLRequest(url: url)
        request.httpMethod = method
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.setValue(assertion.base64EncodedString(), forHTTPHeaderField: "X-App-Assertion")
        request.httpBody = body

        return try await URLSession.shared.data(for: request)
    }
}
```

### Server-Side Assertion Verification

Your server decodes the assertion (CBOR), verifies the authenticator data and counter, checks the signature against the stored public key, and confirms the `clientDataHash`. See [references/device-integrity-patterns.md](references/device-integrity-patterns.md) for step-by-step server verification.

## Server Verification Guidance

See [references/device-integrity-patterns.md](references/device-integrity-patterns.md) for full server architecture guidance including attestation vs. assertion comparison, recommended endpoint design, and risk assessment.

## Error Handling

Handle `DCError` codes from DeviceCheck operations. Key cases:

- `.serverUnavailable` — retry with exponential backoff
- `.invalidKey` — key invalidated (OS update, Secure Enclave reset); regenerate and re-attest
- `.featureUnsupported` — fall back to `DCDevice` tokens
- `.invalidInput` — malformed `clientDataHash` or `keyId`

See [references/device-integrity-patterns.md](references/device-integrity-patterns.md) for full error handling code, retry strategy, and key invalidation recovery.

## Common Patterns

### Environment Entitlement

Set the App Attest environment in your entitlements file. Use `development`
during testing and `production` for App Store builds:

```xml
<key>com.apple.developer.devicecheck.appattest-environment</key>
<string>production</string>
```

When the entitlement is missing, the system uses `development` in debug builds
and `production` for App Store and TestFlight builds.

See [references/device-integrity-patterns.md](references/device-integrity-patterns.md) for the full integration manager pattern, gradual rollout guidance, and error type definition.

## Common Mistakes

1. **Generating a new key on every launch.** Generate once, persist the `keyId` in Keychain.
2. **Skipping the fallback for unsupported devices.** Not all devices support App Attest. Use `DCDevice` tokens as fallback.
3. **Trusting attestation client-side.** All verification must happen on your server.
4. **Not implementing replay protection.** The server must track and increment the assertion counter.
5. **Missing the environment entitlement.** Without it, debug builds use `development` and App Store uses `production`. Mismatches cause attestation failures.
6. **Not handling `DCError.invalidKey`.** Keys can be invalidated by OS updates. Detect and regenerate.

## Review Checklist

- [ ] `DCAppAttestService.isSupported` checked before use; fallback to `DCDevice` when unsupported
- [ ] Key generated once and `keyId` persisted in Keychain
- [ ] Attestation performed once per key; attestation object sent to server
- [ ] Server validates attestation against Apple's App Attest root CA
- [ ] Assertions generated for each sensitive request; server verifies signature and counter
- [ ] `DCError` cases handled: `.serverUnavailable` with retry, `.invalidKey` with key regeneration
- [ ] App Attest environment entitlement set correctly for debug vs. production
- [ ] Gradual rollout considered; feature flag in place for enabling/disabling

## References

- Extended patterns: [references/device-integrity-patterns.md](references/device-integrity-patterns.md)
- [DeviceCheck framework](https://sosumi.ai/documentation/devicecheck)
- [DCDevice](https://sosumi.ai/documentation/devicecheck/dcdevice)
- [DCAppAttestService](https://sosumi.ai/documentation/devicecheck/dcappattestservice)
- [Establishing your app's integrity](https://sosumi.ai/documentation/devicecheck/establishing-your-app-s-integrity)
