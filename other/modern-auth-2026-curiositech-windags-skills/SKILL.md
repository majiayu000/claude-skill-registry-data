---
license: Apache-2.0
name: modern-auth-2026
description: Modern authentication implementation for 2026 - passkeys (WebAuthn), OAuth (Google, Apple), magic links, and cross-device sync. Use for passwordless-first authentication, social login setup, Supabase Auth, Next.js auth flows, and multi-factor authentication. Activate on "passkeys", "WebAuthn", "Google Sign-In", "Apple Sign-In", "magic link", "passwordless", "authentication", "login", "OAuth", "social login". NOT for session management without auth (use standard JWT docs), authorization/RBAC (use security-auditor), or API key management (use api-architect).
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - WebSearch
  - mcp__supabase__*
category: Security
tags:
  - authentication
  - authorization
  - passkeys
  - modern-auth
  - '2026'
---

# Modern Authentication Expert (2026)

Master passwordless-first authentication with passkeys, OAuth, magic links, and cross-device sync for modern web and mobile applications.

## DECISION POINTS

### Auth Method Selection Tree

```
User Auth Request
├── First-time user?
│   ├── YES → Single device?
│   │   ├── YES → Use platform passkey
│   │   └── NO → Use platform passkey + prompt backup registration
│   └── NO → Check existing credentials
│       ├── Has passkeys → Use passkey authentication
│       ├── Has OAuth only → Offer OAuth + passkey upgrade
│       └── Has legacy password → Force migration to passkey
│
├── Device capability check?
│   ├── Platform authenticator available (Face ID/Touch ID/Windows Hello)
│   │   → Prioritize platform passkey
│   ├── Only browser WebAuthn support
│   │   → Use roaming authenticator (YubiKey) OR fallback to OAuth
│   └── No WebAuthn support
│       → Use OAuth (Google/Apple) OR magic link
│
├── Cross-device scenario?
│   ├── User on desktop, has mobile with passkey
│   │   → Show QR code for hybrid transport
│   ├── User lost device access
│   │   → Email recovery → backup passkey registration
│   └── Corporate/shared device
│       → Magic link (no credential storage)
│
└── Compliance requirements?
    ├── App Store submission with third-party login
    │   → MUST include Apple Sign-In
    ├── GDPR/CCPA region
    │   → Default to privacy-first (Apple, passkeys)
    └── Enterprise SSO
        → OAuth with organizational domain validation
```

### Registration Flow Decision Matrix

| User Context | Primary Method | Fallback | Recovery Setup |
|-------------|----------------|----------|----------------|
| Single iPhone user | Face ID passkey | Apple Sign-In | Email + backup device prompt |
| Multi-device Apple user | Platform passkey | iCloud sync | Secondary device registration |
| Android user | Fingerprint passkey | Google Sign-In | Google Password Manager sync |
| Desktop-only user | Windows Hello OR YubiKey | Magic link | Email + mobile app download |
| Privacy-conscious | Platform passkey | Apple Sign-In | Offline backup codes |
| Corporate user | SSO OAuth | Hardware key | Admin recovery contact |

## FAILURE MODES

### Anti-Pattern: "Credential Counter Drift"
**Symptom:** User gets "Invalid signature" error despite correct biometric
**Detection Rule:** If authentication fails with counter mismatch error in logs
**Root Cause:** Multiple devices using same synced passkey without counter sync
**Fix:** Reset counter to max value from all devices OR implement counter-less verification
```typescript
// WRONG: Strict counter validation
if (storedCounter >= newCounter) reject();

// RIGHT: Allow counter drift for synced credentials
if (credential.backed_up && Math.abs(storedCounter - newCounter) > 100) {
  // Reset to new counter, log security event
}
```

### Anti-Pattern: "OAuth Redirect Loop"
**Symptom:** User clicks OAuth button, gets redirected back to login repeatedly
**Detection Rule:** If redirect_uri in OAuth error OR user reports "spinning" login
**Root Cause:** Redirect URI mismatch between provider console and Supabase config
**Fix:** Verify exact URL match including trailing slashes and http/https
```typescript
// Provider Console: https://yourproject.supabase.co/auth/v1/callback
// Supabase Config: Must match exactly - no trailing slash variations
```

### Anti-Pattern: "Silent Registration Failure"
**Symptom:** User completes biometric prompt but passkey doesn't save
**Detection Rule:** If registration returns success but no database entry created
**Root Cause:** Challenge verification passed but database insert failed (RLS policy)
**Fix:** Check RLS policies allow insert, verify user context in registration flow
```sql
-- WRONG: Restrictive policy
CREATE POLICY "Only verified users" ON passkey_credentials
  FOR INSERT WITH CHECK (auth.email_confirmed_at IS NOT NULL);

-- RIGHT: Allow during registration
CREATE POLICY "Users can register" ON passkey_credentials  
  FOR INSERT WITH CHECK (auth.uid() = user_id);
```

### Anti-Pattern: "Apple Key Expiration Surprise"
**Symptom:** Apple Sign-In suddenly returns 400 Invalid Client error
**Detection Rule:** If Apple OAuth fails with client authentication error after working previously
**Root Cause:** Apple .p8 private key expired (6-month limit)
**Fix:** Set calendar reminders, implement monitoring, rotate keys before expiry
```typescript
// Add monitoring
const keyCreatedAt = new Date('2024-06-01');
const warningPeriod = 5 * 24 * 60 * 60 * 1000; // 5 days
if (Date.now() - keyCreatedAt.getTime() > (6 * 30 * 24 * 60 * 60 * 1000) - warningPeriod) {
  console.warn('Apple key expiring soon!');
}
```

### Anti-Pattern: "Magic Link Email Blackhole"
**Symptom:** User reports "Check your email" but no emails arrive
**Detection Rule:** If sign-up/magic link triggered but email delivery rate drops below 95%
**Root Cause:** SMTP not configured OR emails marked as spam OR wrong email templates
**Fix:** Verify SMTP settings, check deliverability, update DNS records (SPF/DKIM)
```typescript
// Add delivery confirmation
await supabase.auth.signInWithOtp({
  email,
  options: {
    shouldCreateUser: false, // Prevent silent failures
  }
});
// Check Supabase logs for email delivery status
```

## WORKED EXAMPLES

### Complete Passkey Implementation Walkthrough

**Scenario:** Implementing passkey auth for a Next.js SaaS app with Supabase

**Step 1 - Decision Point Navigation:**
- User has iPhone with Face ID → Choose platform authenticator
- User wants desktop access too → Plan for backup/cross-device
- App needs App Store compliance → Must include Apple Sign-In fallback

**Step 2 - Database Setup (What novices miss: RLS policies):**
```sql
-- Experts check: Proper indexing for performance
CREATE TABLE passkey_credentials (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid REFERENCES auth.users(id) ON DELETE CASCADE,
  credential_id text UNIQUE NOT NULL, -- Base64URL encoded
  public_key bytea NOT NULL,
  counter bigint DEFAULT 0, -- BIGINT not INT (prevents overflow)
  transports text[],
  backed_up boolean DEFAULT false,
  created_at timestamptz DEFAULT now()
);

-- Novice mistake: Forgetting compound index
CREATE INDEX idx_passkey_user_cred ON passkey_credentials(user_id, credential_id);
```

**Step 3 - Registration API (What experts catch: Challenge storage):**
```typescript
// Novice approach: Store challenge in memory (fails with multiple servers)
let challenges = new Map();

// Expert approach: Persistent challenge storage with expiry
await supabase.from('auth_challenges').upsert({
  user_id: user.id,
  challenge: options.challenge,
  type: 'passkey_register',
  expires_at: new Date(Date.now() + 5 * 60 * 1000),
});
```

**Step 4 - Frontend Implementation (What novices miss: Error handling):**
```typescript
// Novice: Generic error handling
try {
  const credential = await startRegistration(options);
} catch (error) {
  setError('Registration failed');
}

// Expert: Specific error cases
try {
  const credential = await startRegistration(options);
} catch (error) {
  if (error.name === 'NotAllowedError') {
    setError('Registration cancelled or timeout');
  } else if (error.name === 'InvalidStateError') {
    setError('Device already registered for this account');
  } else if (error.name === 'NotSupportedError') {
    // Fallback to OAuth
    redirectToAppleSignIn();
  } else {
    setError(`Registration failed: ${error.message}`);
  }
}
```

**Step 5 - Testing (Expert checks novices skip):**
- Test on actual devices (not just Chrome DevTools)
- Verify cross-device sync works (create on iPhone, use on Mac)
- Test recovery flow (what happens if device is lost?)
- Check database counter increments properly
- Verify RLS policies work for multi-tenant setup

## QUALITY GATES

### Pre-Deployment Checklist

- [ ] **Credential Storage Verified**: Database stores base64url-encoded credential IDs (not raw bytes)
- [ ] **Counter Validation**: Authentication increments and validates counter properly
- [ ] **Challenge Expiry**: Registration/auth challenges expire within 5 minutes
- [ ] **Transport Population**: Credential records include transport methods array
- [ ] **RLS Enforcement**: Row-level security prevents cross-user credential access
- [ ] **Error Boundaries**: Frontend handles NotAllowedError, InvalidStateError, NotSupportedError
- [ ] **Cross-Device Tested**: QR code/hybrid transport works between devices
- [ ] **Recovery Flow**: Magic link backup works when passkey unavailable
- [ ] **OAuth Fallback**: Apple Sign-In required if Google OAuth enabled (App Store compliance)
- [ ] **Email Delivery**: Magic link/OTP emails deliver within 30 seconds

### Production Readiness Gates

- [ ] **Rate Limiting Active**: Auth endpoints limited to prevent brute force
- [ ] **Monitoring Configured**: Alert on authentication failure spike (>5% error rate)
- [ ] **Apple Key Expiry**: Calendar reminder set for .p8 key renewal (6-month cycle)
- [ ] **HTTPS Enforced**: All auth flows use HTTPS (WebAuthn requirement)
- [ ] **Session Validation**: JWT tokens expire appropriately (1-hour access, 7-day refresh)

## NOT-FOR BOUNDARIES

**Do NOT use this skill for:**

- **Session Management Only** → Use standard JWT/cookie patterns when auth flow already complete
- **Authorization Policies** → Use `security-auditor` skill for RBAC, permissions, access control
- **API Key Management** → Use `api-architect` skill for service-to-service authentication
- **Supabase RLS Policies** → Use `supabase-admin` skill for database-level security rules
- **Legacy Password Migration** → Use specialized migration tools for bulk user imports
- **Enterprise SSO/SAML** → Use dedicated SSO providers like Auth0, Okta for complex enterprise needs
- **Regulatory Compliance** → Use `compliance-auditor` skill for GDPR/HIPAA/SOC2 requirements
- **Performance Optimization** → Use `performance-optimizer` skill for auth-related bottlenecks

**Delegate to other skills when user asks about:**
- "How do I set up row-level security?" → `supabase-admin`
- "What permissions does this user have?" → `security-auditor`
- "How do I generate API keys?" → `api-architect`
- "Is this GDPR compliant?" → `compliance-auditor`