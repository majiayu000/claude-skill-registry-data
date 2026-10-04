---
name: Privy
description: Use when building wallet infrastructure, authentication systems, or financial applications. Reach for Privy when you need to create embedded wallets, manage user authentication, control wallet permissions with policies, execute transactions across blockchains, or build treasury/agent wallets with programmable controls.
metadata:
    mintlify-proj: privy
    version: "1.0"
---

# Privy Skill Reference

## Product summary

Privy is a programmable wallet infrastructure platform for building financial applications. It provides embedded wallets, authentication, transaction execution, and policy controls across 50+ blockchains including Ethereum, Solana, Bitcoin, and Tempo. Agents use Privy to authenticate users, create and manage wallets, execute transactions, enforce spending policies, and build complete financial products without building wallet infrastructure from scratch.

**Key files and commands:**
- Dashboard: https://dashboard.privy.io (configure apps, login methods, policies)
- App ID and App Secret: Found in Dashboard > App Settings > Basics
- Client ID: Required for mobile/non-web platforms (Dashboard > App Settings > Clients)
- REST API: `https://api.privy.io/v1/` (requires Basic Auth with app ID:secret)
- SDKs: React (`@privy-io/react-auth`), Node.js (`@privy-io/node`), Swift, Android, Flutter, Java, Go, Rust, Ruby
- Primary docs: https://docs.privy.io

## When to use

Reach for Privy when:
- Building consumer apps that need user authentication + embedded wallets
- Creating organization or treasury wallets with multi-sig controls
- Building AI agents that need to hold assets and transact autonomously
- Implementing spending policies, transaction limits, or approval workflows
- Executing transactions across multiple blockchains from a single interface
- Migrating users from another wallet provider
- Setting up funding flows (fiat onramps, crypto deposits, card spend)
- Implementing yield integrations or token swaps
- Requiring role-based access control or delegation patterns

Do not use Privy for: pure authentication without wallets (use Auth0, Firebase instead), or if you need complete control over key management without any abstraction.

## Quick reference

### SDK Installation

| Platform | Package | Command |
|----------|---------|---------|
| React | `@privy-io/react-auth` | `npm install @privy-io/react-auth` |
| Node.js | `@privy-io/node` | `npm install @privy-io/node` |
| React Native | `@privy-io/react-native-auth` | `npm install @privy-io/react-native-auth` |
| Swift | Privy Swift SDK | Via Swift Package Manager |
| Android | Privy Android SDK | Via Gradle |

### Core Concepts

| Concept | Definition | Use case |
|---------|-----------|----------|
| **User** | Individual authenticated in your app | Consumer wallets, personal accounts |
| **Wallet** | Blockchain account (embedded or external) | Holding assets, signing transactions |
| **Owner** | Entity with full control (user, auth key, or quorum) | Determines who can modify wallet |
| **Signer** | Additional party with scoped permissions | Server automation, delegated access |
| **Policy** | Rules constraining wallet actions | Spending limits, recipient whitelists |
| **Authorization Key** | P256 cryptographic key for server control | Backend wallet management |
| **Key Quorum** | M-of-K multi-sig approval | Shared control, treasury operations |

### Authentication Methods

Configure in Dashboard > Configuration > Authentication:
- Email / SMS / WhatsApp
- Social (Google, Discord, Twitter, Farcaster, etc.)
- Passkeys (WebAuthn)
- External wallets (MetaMask, Phantom)
- Custom JWT (bring your own auth provider)
- Guest accounts (instant sign-in)

### Wallet Control Models

| Model | Owner | Signers | Use case |
|-------|-------|---------|----------|
| User-owned | User | None | Self-custodial consumer wallets |
| User + server | User | Server (scoped) | Automated trading, limit orders |
| App-owned | Auth key | None | Treasury, bots, agents |
| Custodial | Licensed custodian | None | Institutional FBO accounts |

### REST API Headers (Required)

```
Authorization: Basic <base64(app_id:app_secret)>
privy-app-id: <app_id>
Content-Type: application/json
```

### Common Wallet Actions

| Action | Endpoint | Purpose |
|--------|----------|---------|
| Create wallet | `POST /v1/wallets` | Provision new wallet |
| Get wallet | `GET /v1/wallets/{id}` | Fetch wallet details |
| Send transaction | `POST /v1/wallets/{id}/rpc` | Execute blockchain action |
| Get balance | `GET /v1/wallets/{id}/balance` | Check asset holdings |
| Create policy | `POST /v1/policies` | Define spending rules |
| Create user | `POST /v1/users` | Onboard new user |

## Decision guidance

### When to use embedded vs external wallets

| Scenario | Embedded | External |
|----------|----------|----------|
| New users, no existing wallet | ✓ | ✗ |
| Users have MetaMask/Phantom | ✗ | ✓ |
| Need full control over UX | ✓ | ✗ |
| Users want to bring existing assets | ✗ | ✓ |
| Mobile app | ✓ | Limited |
| Require key export | ✓ | ✗ |

### When to use client-side vs server-side SDKs

| Scenario | Client SDK | Server SDK |
|----------|-----------|-----------|
| User authentication | ✓ | ✗ |
| Wallet creation for users | ✓ | ✓ |
| Server-controlled wallets | ✗ | ✓ |
| Transaction signing | ✓ | ✓ |
| Policy management | ✗ | ✓ |
| User management | ✗ | ✓ |

### When to use policies vs key quorums

| Need | Policies | Key Quorums |
|------|----------|-------------|
| Spending limits | ✓ | ✗ |
| Recipient whitelists | ✓ | ✗ |
| Multi-sig approval | ✗ | ✓ |
| Time-based rules | ✓ | ✗ |
| Contract interaction control | ✓ | ✗ |
| Shared ownership | ✗ | ✓ |

## Workflow

### 1. Set up your Privy app

1. Go to https://dashboard.privy.io and create an app
2. Copy your App ID and App Secret from App Settings > Basics
3. For mobile/non-web: Create an app client in App Settings > Clients
4. Configure login methods in Configuration > Authentication
5. (Optional) Configure appearance in Configuration > Appearance

### 2. Integrate authentication (client-side)

1. Install the appropriate SDK (`@privy-io/react-auth` for React, etc.)
2. Wrap your app with `PrivyProvider`, passing `appId` and `clientId`
3. Use `usePrivy()` hook to access `login()`, `logout()`, and `user` state
4. Wait for `ready === true` before consuming Privy state
5. Call `login()` to trigger authentication modal

### 3. Create or connect wallets

1. For automatic wallet creation: Set `embeddedWallets.ethereum.createOnLogin` in PrivyProvider config
2. For manual creation: Use `useCreateWallet()` hook (client) or `wallets().create()` (server)
3. Specify wallet owner: user ID (user-owned) or authorization key (app-owned)
4. Optionally attach policies or signers at creation time
5. Retrieve wallet address from response

### 4. Execute transactions

1. Get wallet reference from `useWallets()` hook or API
2. Prepare transaction parameters (to, value, data, etc.)
3. Call appropriate signing method: `eth_sendTransaction`, `signTransaction`, etc.
4. For server-side: Use `intents()` API to propose and authorize transactions
5. Handle response: check status, monitor for confirmation via webhooks

### 5. Enforce policies

1. Create policy via Dashboard or `POST /v1/policies` API
2. Define rules with conditions (amount limits, recipient addresses, etc.)
3. Attach policy to wallet at creation or via `PATCH /v1/wallets/{id}`
4. Policy engine evaluates every request; DENY takes precedence
5. If no rule matches, request is denied by default

### 6. Monitor with webhooks

1. Configure webhook endpoint in Dashboard > Configuration > Webhooks
2. Subscribe to relevant events (user.created, wallet.funds_deposited, transaction.confirmed, etc.)
3. Verify webhook signature using your app secret
4. Implement retry logic with exponential backoff
5. Return 200 status to acknowledge receipt

## Common gotchas

- **HTTPS required**: Embedded wallets only work in secure contexts (https://). Localhost is treated as secure by browsers.
- **Ready state**: Always check `ready === true` before using Privy hooks; state may be stale during initialization.
- **Policy defaults to DENY**: If a wallet has a policy but no rule matches the request, the request is denied. Include an "allow all" rule if needed.
- **Rate limits**: REST API has rate limits; implement exponential backoff for retries (HTTP 429 responses).
- **Idempotency keys**: Use idempotency keys for wallet creation and transaction requests to prevent duplicates.
- **Authorization headers**: REST API requires both Basic Auth and `privy-app-id` header; requests missing either are rejected.
- **Chain-specific policies**: Policies are chain-specific; create separate policies for Ethereum vs Solana wallets.
- **Key export security**: Users can export private keys; warn them about custody implications.
- **Webhook verification**: Always verify webhook signatures; don't trust webhook data without verification.
- **Multiple wallets**: Users can have multiple wallets per chain (HD wallets); use `createAdditional: true` to enable.
- **External wallet linking**: External wallets are read-only for signing; use embedded wallets for full control.
- **MFA not automatic**: Multi-factor authentication must be explicitly configured; email/SMS alone are not phishing-resistant.

## Verification checklist

Before submitting work with Privy:

- [ ] App ID and App Secret are stored securely (environment variables, not hardcoded)
- [ ] PrivyProvider wraps the entire app and `ready` state is checked before consuming Privy
- [ ] Authentication flow is tested (login, logout, session persistence)
- [ ] Wallet creation is tested (automatic or manual, correct owner specified)
- [ ] Transactions are tested on testnet before production
- [ ] Policies are attached to wallets and tested with boundary conditions
- [ ] Webhook endpoint is configured and signature verification is implemented
- [ ] Error handling covers NotFoundError, rate limits, and network failures
- [ ] HTTPS is enforced for production (embedded wallets require secure context)
- [ ] Idempotency keys are used for wallet creation and transaction requests
- [ ] Rate limit retry logic uses exponential backoff
- [ ] User data is not logged or exposed in error messages
- [ ] External wallets are tested if supported (MetaMask, Phantom, etc.)

## Resources

**Comprehensive navigation:** https://docs.privy.io/llms.txt

**Critical documentation pages:**
1. [Key Concepts](https://docs.privy.io/basics/key-concepts) — Understand authentication, wallets, and controls
2. [React Setup & Quickstart](https://docs.privy.io/basics/react/setup) — Get started with client-side integration
3. [REST API Introduction](https://docs.privy.io/api-reference/introduction) — Server-side wallet and user management
4. [Policies Overview](https://docs.privy.io/controls/policies/overview) — Define spending rules and constraints
5. [Wallet Creation](https://docs.privy.io/wallets/wallets/create/create-a-wallet) — Provision wallets across SDKs
6. [Webhooks](https://docs.privy.io/api-reference/webhooks/overview) — Monitor wallet and transaction events

---

> For additional documentation and navigation, see: https://docs.privy.io/llms.txt