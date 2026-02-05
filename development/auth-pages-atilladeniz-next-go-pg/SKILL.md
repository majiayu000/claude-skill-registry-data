---
name: auth-pages
description: Create and manage authentication pages with server-side session handling. Use when adding login, register, or protected pages WITHOUT flicker/skeleton.
allowed-tools: Read, Edit, Write, Glob
---

# Authentication Pages (FSD)

Better Auth integration with Next.js 16 - **Magic Link** (passwordless) authentication.

## Authentication Method

This project uses **Magic Link authentication** - users sign in by clicking a link sent to their email. No passwords!

## FSD Paths

```
src/
├── app/(auth)/
│   ├── login/                  # Magic Link Login Page
│   ├── magic-link/verify/      # Magic Link Verification UI
│   └── verify-email/           # Email Verification UI
├── app/(protected)/
│   ├── dashboard/              # Protected Dashboard
│   └── settings/               # Session Management
├── features/auth/              # Auth Feature
│   ├── ui/
│   │   ├── login-form.tsx      # Orchestrates login flow
│   │   ├── login-card.tsx      # Email input form
│   │   └── email-sent-card.tsx # "Check your email" UI
│   ├── model/
│   │   ├── use-login.ts        # Login state & logic
│   │   └── use-auth-sync.ts    # Cross-tab sync
│   └── index.ts
├── features/user-settings/     # Session Management
│   ├── ui/
│   │   ├── sessions-list.tsx
│   │   └── session-card.tsx
│   ├── model/
│   │   └── use-sessions.ts
│   └── index.ts
├── shared/lib/
│   ├── auth-client/            # Client: signIn.magicLink, signOut
│   ├── auth-server/            # Server: getSession, auth config
│   └── geo/                    # User Agent parsing
└── widgets/header/             # Header with UserMenu
```

## Magic Link Login Flow

```
1. User enters email → /login
2. signIn.magicLink() called
3. Backend webhook sends email
4. User clicks link → /magic-link/verify?token=...
5. Token verified → Session created → Redirect to /dashboard
6. Login notification sent (new device only)
```

## Auth Client (Magic Link)

```tsx
import { signIn, signOut } from "@shared/lib/auth-client"

// Request Magic Link
await signIn.magicLink({
  email,
  callbackURL: "/dashboard",
  newUserCallbackURL: "/dashboard",
  errorCallbackURL: "/login?error=verification_failed",
})

// Sign Out
await signOut()
```

## Server-Side Session (NO FLICKER!)

### Protected Page Pattern

```tsx
// app/(protected)/dashboard/page.tsx - SERVER COMPONENT
import { getSession } from "@shared/lib/auth-server"
import { redirect } from "next/navigation"
import { Header } from "@widgets/header"

export default async function DashboardPage() {
  // Server-side Session Check - NO Flicker!
  const session = await getSession()
  if (!session) redirect("/login")

  return (
    <div className="min-h-screen bg-background">
      <Header user={session.user} />
      {/* Content */}
    </div>
  )
}
```

## Session Management

Users can view and revoke sessions at `/settings`:

```tsx
import { useSessions } from "@features/user-settings"

export function SessionsList() {
  const { sessions, revokeSession, revokeOtherSessions } = useSessions()

  return (
    <div>
      {sessions.map((session) => (
        <SessionCard
          key={session.id}
          session={session}
          onRevoke={revokeSession}
        />
      ))}
      <Button onClick={revokeOtherSessions}>
        Alle anderen Sessions beenden
      </Button>
    </div>
  )
}
```

## Backend Webhooks

All emails are sent by the Go backend (Clean Architecture):

```
POST /api/v1/webhooks/send-magic-link
POST /api/v1/webhooks/send-verification-email
POST /api/v1/webhooks/session-created
```

Protected by `X-Webhook-Secret` header.

## Rate Limiting

- Magic Link: 3 requests per minute
- Verification Email: 3 requests per minute

## Cross-Tab Synchronization

```tsx
// features/auth/model/use-auth-sync.ts
import { useAuthSync, broadcastSignOut } from "@features/auth"

// In Header component
useAuthSync() // Listen for auth changes

// On sign out
await signOut()
await broadcastSignOut() // Notify other tabs
```

## Magic Link Verify Page

Custom UI for `/magic-link/verify`:

- **Loading**: Spinner while verifying
- **Success**: Immediate redirect to dashboard
- **Rate Limited**: "Zu viele Anfragen" message
- **Expired**: "Link abgelaufen" message
- **Invalid**: "Ungültiger Link" message

## Login Notifications

Email sent on new device/IP:
- Checks if device/IP combination is known
- Only sends notification for NEW devices
- Includes "Sessions verwalten" button to `/settings`

## IMPORTANT: What NOT to do

❌ **DO NOT** use `useSession()` in Protected Pages → Causes flicker
❌ **DO NOT** use password fields → Magic Link only
❌ **DO NOT** send emails from frontend → Use backend webhooks
❌ **DO NOT** use direct SQL in auth hooks → Use webhooks

✅ **INSTEAD**:

- Server Component checks session with `getSession()`
- `redirect()` if no session
- Pass user as prop to Client Components
- All emails via backend webhooks
