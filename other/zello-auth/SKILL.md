---
name: zello-auth
description: Wire Zello SDK authentication into the EnforcementMAPS AuthContext lifecycle, create ZelloProvider, and map officer identities to Zello usernames.
---

# Zello Authentication

This skill covers the Zello SDK authentication lifecycle and how it integrates with the existing `auth-context.tsx` in EnforcementMAPS.

## How Zello Auth Works

Zello uses **network credentials** — entirely separate from the app's JWT auth. Each Zello Work network has an `issuer` and `credentialKey` provided by the admin console. These are build-time env vars, not per-user credentials.

Officers authenticate to Zello with a username derived from their officer number.

## AuthContext Integration

The existing `src/shared/infra/auth-context.tsx` manages app login/logout. Zello hooks into this lifecycle reactively:

```
Officer taps Login
  → AuthContext.login() succeeds
  → token + user stored in context
  → ZelloProvider detects token change
  → Zello.connect(networkConfig) called
  → SDK authenticates with Zello Work servers

Officer taps Logout
  → AuthContext.logout() called
  → ZelloProvider detects token = null
  → Zello.disconnect() called
  → Zello session ends
```

The key design principle: Zello connection state is **derived** from AuthContext state. There is no separate Zello login screen.

## ZelloProvider

```typescript
// src/features/zello/zello-provider.tsx
import { useEffect, useRef } from 'react';
import Zello from '@zelloptt/react-native-zello-sdk';
import { useAuth } from '@/shared/infra/auth-context';

const ZELLO_NETWORK = process.env.EXPO_PUBLIC_ZELLO_NETWORK_ISSUER ?? '';
const ZELLO_KEY = process.env.EXPO_PUBLIC_ZELLO_CREDENTIAL_KEY ?? '';

export function ZelloProvider({ children }: { children: React.ReactNode }) {
  const { user, token } = useAuth();
  const connectedRef = useRef(false);

  useEffect(() => {
    if (token && user && !connectedRef.current) {
      const zelloUsername = `officer_${user.officerNumber}`;
      Zello.connect({
        network: ZELLO_NETWORK,
        username: zelloUsername,
        password: ZELLO_KEY,
      });
      connectedRef.current = true;
    }

    if (!token && connectedRef.current) {
      Zello.disconnect();
      connectedRef.current = false;
    }
  }, [token, user]);

  return <>{children}</>;
}
```

## Mount Order

ZelloProvider mounts **inside** AuthProvider so it can access auth state:

```typescript
// app/_layout.tsx
export default function Layout() {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <ZelloProvider>
          <AppNavigator />
        </ZelloProvider>
      </AuthProvider>
    </QueryClientProvider>
  );
}
```

## Username Strategy

Map officer numbers to Zello usernames deterministically:

| App Identity | Zello Username |
|-------------|---------------|
| Officer 629 | `officer_629` |
| Supervisor 100 | `officer_100` |

Officers must be pre-provisioned in the Zello Work admin console or via the provisioning API. See `zello-channels` skill for provisioning details.

## Credential Storage Rules

| Credential | Storage | Rationale |
|-----------|---------|-----------|
| Zello network issuer | `eas.json` env var | Build-time only, not user-facing |
| Zello credential key | `eas.json` env var | Build-time only, not user-facing |
| Zello session token | SDK internal | Managed by SDK after connect() |
| App JWT | `expo-secure-store` | Existing pattern — unchanged |

Never store Zello passwords in `expo-secure-store` alongside the app JWT.

## Detailed Documentation

See `docs/dev/zello/05-authentication.md` for the complete auth flow.
