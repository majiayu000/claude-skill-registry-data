---
name: clerk
description: Clerk — authentication and user management with sign-in/sign-up, middleware, organizations, webhooks.
---

## clerk

### Authentication
- `<SignIn />` / `<SignUp />` — prebuilt UI components with customization props.
- `useAuth()` — `userId`, `sessionId`, `orgId`, `orgRole`, `isSignedIn`, `getToken()`.
- `auth()` helper in Next.js App Router — server-side session from `clerkMiddleware`.
- `clerkClient.users.getUser(userId)` — server-side user lookup.

### Middleware (Next.js)
- `clerkMiddleware((auth, req) => { ... })` — protect routes; returns `auth()` object.
- `createRouteMatcher(['/dashboard(.*)'])` — pattern-based route protection.
- `publicRoutes: ['/', '/about']` — bypass authentication checks.
- `afterAuth(auth, req, evt)` — post-auth redirects or role checks.

### User Management
- `useUser()` — `user.fullName`, `user.imageUrl`, `user.emailAddresses`, `user.publicMetadata`.
- `user.update({ firstName, lastName })` — update profile.
- User metadata: `publicMetadata`, `privateMetadata`, `unsafeMetadata` — typed via `user.update`.
- Session management: `useSession()` / `useSessionList()` for multi-session UI.

### Organizations
- `<OrganizationSwitcher />` / `<OrganizationProfile />` — org UI components.
- `useOrganization()` — `organization.id`, `organization.name`, `organization.membersCount`.
- `useOrganizationList()` — list orgs; `setActive({ organization })` — switch context.
- `useMembership({ membership })` / `useInvitations()` — manage org membership.

### Webhooks
- Clerk webhook events: `user.created`, `user.updated`, `organization.created`, `session.created`.
- Endpoints via `svix`: verify `svix-headers` signature.
- Sync users to DB: upsert on `user.created` / `user.updated`.
