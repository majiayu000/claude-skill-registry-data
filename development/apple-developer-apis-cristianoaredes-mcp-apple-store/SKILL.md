---
name: apple-developer-apis
description: >-
  Expert system for integrating Apple Developer APIs including App Store Connect API,
  App Store Server API, Sign in with Apple REST API, App Store Server Notifications,
  Advanced Commerce API, and App Intents. Use this skill when (1) Implementing in-app
  purchases or subscription management, (2) Setting up App Store Server Notifications
  webhooks, (3) Creating JWT tokens for Apple API authentication, (4) Managing TestFlight
  distribution or app metadata, (5) Implementing Sign in with Apple authentication,
  (6) Working with App Intents or Shortcuts integration, or (7) Any Apple developer API integration.
---

# Apple Developer APIs

Complete guide for integrating Apple Developer APIs, including App Store Connect API, App Store Server API, Sign in with Apple, and App Store Server Notifications.

## Quick Start Overview

Apple provides several REST APIs for managing apps, subscriptions, and authentication:

- **App Store Connect API**: Manage apps, TestFlight, certificates, and metadata
- **App Store Server API**: Manage transactions, subscriptions, and refunds
- **App Store Server Notifications**: Receive webhook events for subscription lifecycle
- **Sign in with Apple REST API**: Server-side authentication validation

All APIs use **JWT (JSON Web Token)** authentication with ES256 algorithm.

## Authentication (All APIs)

### Creating API Keys

1. Navigate to **App Store Connect > Users and Access > Integrations**
2. Generate **Individual Key** or **Team Key**
3. Download the `.p8` private key file (only downloadable once)
4. Note the **Key ID** and **Issuer ID**

### JWT Structure

```javascript
// Header
{
  "alg": "ES256",
  "kid": "YOUR_KEY_ID",
  "typ": "JWT"
}

// Payload
{
  "iss": "YOUR_ISSUER_ID",
  "iat": 1623345678,  // Issued at timestamp
  "exp": 1623346878,  // Expiration (max 20 minutes)
  "aud": "appstoreconnect-v1",
  "bid": "com.yourcompany.yourapp"  // Required for Server API
}
```

### Generate JWT (Node.js)

```javascript
const jwt = require('jsonwebtoken');
const fs = require('fs');

function generateJWT(issuerId, keyId, privateKeyPath, bundleId) {
  const privateKey = fs.readFileSync(privateKeyPath);

  return jwt.sign({
    bid: bundleId  // Include for App Store Server API
  }, privateKey, {
    algorithm: 'ES256',
    expiresIn: '20m',
    issuer: issuerId,
    audience: 'appstoreconnect-v1',
    header: { alg: 'ES256', kid: keyId, typ: 'JWT' }
  });
}
```

### Generate JWT (Python)

```python
import jwt
import time
from pathlib import Path

def generate_jwt(issuer_id: str, key_id: str, private_key_path: str, bundle_id: str = None) -> str:
    private_key = Path(private_key_path).read_text()

    payload = {
        "iss": issuer_id,
        "iat": int(time.time()),
        "exp": int(time.time()) + 1200,
        "aud": "appstoreconnect-v1"
    }

    if bundle_id:
        payload["bid"] = bundle_id

    return jwt.encode(payload, private_key, algorithm="ES256",
                     headers={"kid": key_id, "typ": "JWT"})
```

---

## App Store Connect API

**Base URL:** `https://api.appstoreconnect.apple.com/v1`

REST API for automating App Store Connect tasks.

### Key Endpoints

#### Apps
```
GET  /v1/apps                          # List all apps
GET  /v1/apps/{id}                     # Get specific app
GET  /v1/apps/{id}/builds              # List builds for app
```

#### TestFlight
```
GET  /v1/builds                        # List all builds
POST /v1/betaTesters                   # Add beta tester
GET  /v1/betaGroups                    # List beta groups
```

#### Certificates & Profiles
```
GET  /v1/certificates                  # List certificates
POST /v1/certificates                  # Create certificate
GET  /v1/profiles                      # List provisioning profiles
```

#### In-App Purchases
```
GET  /v1/apps/{id}/inAppPurchases      # List IAPs
POST /v1/inAppPurchases                # Create IAP
GET  /v1/subscriptionGroups            # List subscription groups
```

### Request Example

```javascript
async function listApps(jwt) {
  const response = await fetch(
    'https://api.appstoreconnect.apple.com/v1/apps?fields[apps]=name,bundleId&limit=10',
    {
      headers: {
        'Authorization': `Bearer ${jwt}`,
        'Content-Type': 'application/json'
      }
    }
  );
  return response.json();
}
```

---

## App Store Server API

**Base URL (Production):** `https://api.storekit.itunes.apple.com`
**Base URL (Sandbox):** `https://api.storekit-sandbox.itunes.apple.com`

REST API for managing customer transactions and subscriptions. Replaces deprecated `verifyReceipt`.

### Key Endpoints

#### Transaction History
```
GET /inApps/v1/history/{transactionId}
```
Returns complete purchase history for a customer.

**Query Parameters:**
- `revision` - Pagination token
- `sort` - ASCENDING or DESCENDING
- `productType` - AUTO_RENEWABLE, NON_RENEWABLE, CONSUMABLE, NON_CONSUMABLE

#### Subscription Status
```
GET /inApps/v1/subscriptions/{transactionId}
```
Returns current status of all subscriptions.

#### Refund History
```
GET /inApps/v2/refund/lookup/{transactionId}
```

#### Order Lookup
```
POST /inApps/v1/lookup/{orderId}
```

#### Consumption Information
```
PUT /inApps/v1/transactions/consumption/{transactionId}
```
Send consumption data for consumable IAPs.

#### Test Notification
```
POST /inApps/v1/notifications/test
```

### Response Structure

All responses contain signed JWS data:

```json
{
  "signedTransactions": ["eyJhbGciOiJFUzI1NiIsIng1YyI6Wy..."],
  "revision": "next_page_token"
}
```

### Official Libraries

Apple provides official libraries:

```bash
# Node.js
npm install @apple/app-store-server-library

# Python
pip install app-store-server-library
```

**Verify signed data:**
```javascript
const { SignedDataVerifier } = require('@apple/app-store-server-library');

const verifier = new SignedDataVerifier(
  [appleRootCertificate],
  true,  // Enable online checks
  'Production',
  'com.yourcompany.yourapp',
  YOUR_APP_ID
);

const transaction = await verifier.verifyAndDecodeTransaction(signedTransaction);
```

---

## App Store Server Notifications V2

Webhooks for subscription lifecycle events.

### Setup

1. Configure server URL in **App Store Connect > App > App Information**
2. Implement endpoint to receive POST requests

### Notification Types

| Type | Description |
|------|-------------|
| `SUBSCRIBED` | Initial subscription purchase |
| `DID_RENEW` | Subscription renewed |
| `DID_FAIL_TO_RENEW` | Renewal failed |
| `EXPIRED` | Subscription expired |
| `REFUND` | Transaction refunded |
| `DID_CHANGE_RENEWAL_STATUS` | Auto-renew toggled |
| `DID_CHANGE_RENEWAL_PREF` | Plan changed |
| `GRACE_PERIOD_EXPIRED` | Billing grace period ended |
| `OFFER_REDEEMED` | Promotional offer applied |
| `CONSUMPTION_REQUEST` | Apple requests consumption data |
| `REVOKE` | Family sharing revoked |

### Subtypes

- `INITIAL_BUY` / `RESUBSCRIBE`
- `DOWNGRADE` / `UPGRADE`
- `AUTO_RENEW_ENABLED` / `AUTO_RENEW_DISABLED`
- `VOLUNTARY` / `BILLING_RETRY` / `PRICE_INCREASE`

### Payload Structure

```json
{
  "signedPayload": "eyJhbGciOiJFUzI1NiIsIng1YyI6Wy..."
}
```

### Decoded Payload

```json
{
  "notificationType": "DID_RENEW",
  "subtype": "BILLING_RECOVERY",
  "notificationUUID": "unique-id",
  "data": {
    "appAppleId": 123456789,
    "bundleId": "com.yourcompany.yourapp",
    "environment": "Production",
    "signedTransactionInfo": "...",
    "signedRenewalInfo": "..."
  },
  "version": "2.0",
  "signedDate": 1679529600000
}
```

### Webhook Handler (Node.js)

```javascript
const express = require('express');
const { SignedDataVerifier } = require('@apple/app-store-server-library');

app.post('/apple/notifications', async (req, res) => {
  const { signedPayload } = req.body;

  const verifier = new SignedDataVerifier(
    [appleRootCert], true, 'Production', bundleId, appId
  );

  const notification = await verifier.verifyAndDecodeNotification(signedPayload);

  switch (notification.notificationType) {
    case 'DID_RENEW':
      await handleRenewal(notification);
      break;
    case 'REFUND':
      await handleRefund(notification);
      break;
    case 'EXPIRED':
      await handleExpiration(notification);
      break;
  }

  res.status(200).send();
});
```

---

## Sign in with Apple REST API

**Base URL:** `https://appleid.apple.com`

### Endpoints

```
POST /auth/token      # Exchange code for tokens
POST /auth/revoke     # Revoke tokens
GET  /auth/keys       # Get JWKS for validation
```

### Authentication Flow

1. Client authenticates via Apple
2. Server receives authorization code
3. Exchange code for tokens at `/auth/token`
4. Validate identity token
5. Store refresh token securely

### Generate Client Secret

```javascript
function generateClientSecret(teamId, clientId, keyId, privateKey) {
  return jwt.sign({}, privateKey, {
    algorithm: 'ES256',
    expiresIn: '180d',  // Max 6 months
    audience: 'https://appleid.apple.com',
    issuer: teamId,
    subject: clientId,
    header: { alg: 'ES256', kid: keyId }
  });
}
```

### Token Exchange

```javascript
async function exchangeAuthCode(code, clientSecret, clientId, redirectUri) {
  const params = new URLSearchParams({
    client_id: clientId,
    client_secret: clientSecret,
    code: code,
    grant_type: 'authorization_code',
    redirect_uri: redirectUri
  });

  const response = await fetch('https://appleid.apple.com/auth/token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: params.toString()
  });

  return response.json();
}
```

### Token Response

```json
{
  "access_token": "...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "refresh_token": "...",
  "id_token": "eyJraWQiOiJXNldjT0..."
}
```

### Validate Identity Token

```javascript
const jwksClient = require('jwks-rsa');

const client = jwksClient({ jwksUri: 'https://appleid.apple.com/auth/keys' });

async function validateIdentityToken(idToken, audience) {
  const decoded = jwt.decode(idToken, { complete: true });
  const key = await client.getSigningKey(decoded.header.kid);

  return jwt.verify(idToken, key.getPublicKey(), {
    algorithms: ['RS256'],
    issuer: 'https://appleid.apple.com',
    audience: audience
  });
}
```

### Revoke Token (Required for Account Deletion)

```javascript
async function revokeToken(token, clientSecret, clientId) {
  const params = new URLSearchParams({
    client_id: clientId,
    client_secret: clientSecret,
    token: token,
    token_type_hint: 'refresh_token'
  });

  await fetch('https://appleid.apple.com/auth/revoke', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: params.toString()
  });
}
```

---

## App Intents Framework

Framework for exposing app functionality to Siri and Shortcuts.

### App Intent Example (Swift)

```swift
import AppIntents

struct OrderCoffeeIntent: AppIntent {
    static var title: LocalizedStringResource = "Order Coffee"

    @Parameter(title: "Size")
    var size: CoffeeSize

    func perform() async throws -> some IntentResult {
        let order = try await CoffeeService.order(size: size)
        return .result(value: order.id)
    }
}

struct CoffeeShortcuts: AppShortcutsProvider {
    static var appShortcuts: [AppShortcut] {
        AppShortcut(
            intent: OrderCoffeeIntent(),
            phrases: ["Order coffee with \(.applicationName)"],
            shortTitle: "Order Coffee",
            systemImageName: "cup.and.saucer.fill"
        )
    }
}
```

---

## Error Handling

### Common Status Codes

| Code | Description |
|------|-------------|
| 401 | Invalid or expired JWT |
| 403 | Insufficient permissions |
| 404 | Resource not found |
| 429 | Rate limit exceeded |
| 500 | Apple server error |

### Rate Limits

- **App Store Connect API:** ~1000 requests/hour per key
- **App Store Server API:** Varies by endpoint
- **Sign in with Apple:** ~20 requests/second

### Retry Strategy

```javascript
async function apiCallWithRetry(fn, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      if (error.status === 429 && i < maxRetries - 1) {
        await new Promise(r => setTimeout(r, Math.pow(2, i) * 1000));
        continue;
      }
      throw error;
    }
  }
}
```

---

## Security Best Practices

1. **Never expose private keys** - Store in secure vault
2. **Validate all signed data** - Always verify JWS signatures
3. **Use short-lived tokens** - JWT should expire in 20 minutes
4. **Implement webhook verification** - Validate all incoming notifications
5. **Store refresh tokens securely** - Encrypt at rest
6. **Use environment-specific endpoints** - Separate sandbox/production
7. **Regenerate client secrets** - Sign in with Apple expires in 6 months

---

## Environment Variables

```env
# App Store Connect / Server API
APP_STORE_ISSUER_ID=your-issuer-id
APP_STORE_KEY_ID=your-key-id
APP_STORE_PRIVATE_KEY_PATH=./AuthKey_XXXXX.p8
APP_BUNDLE_ID=com.yourcompany.yourapp
APP_STORE_ENVIRONMENT=Sandbox

# Sign in with Apple
APPLE_TEAM_ID=your-team-id
APPLE_CLIENT_ID=com.yourcompany.yourapp
APPLE_KEY_ID=your-key-id
APPLE_PRIVATE_KEY_PATH=./AuthKey_XXXXX.p8
```

---

## Additional Resources

For detailed API specifications:
- See `references/app-store-connect-api.md` - Complete endpoint reference
- See `references/app-store-server-api.md` - Server API endpoints
- See `references/sign-in-with-apple.md` - Authentication flow details
- See `references/server-notifications.md` - Webhook event structures
- See `assets/templates/` - Ready-to-use code templates

## Documentation Links

- [App Store Connect API](https://developer.apple.com/documentation/appstoreconnectapi)
- [App Store Server API](https://developer.apple.com/documentation/appstoreserverapi)
- [App Store Server Notifications](https://developer.apple.com/documentation/appstoreservernotifications)
- [Sign in with Apple REST API](https://developer.apple.com/documentation/signinwithapplerestapi)
- [App Intents](https://developer.apple.com/documentation/appintents)
- [Advanced Commerce API](https://developer.apple.com/documentation/advancedcommerceapi)
