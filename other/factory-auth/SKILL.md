---
name: factory-auth
description: Auth and authorization conventions distilled across builds with three different auth stacks (Better Auth + orgs, Supabase Auth + RLS, Clerk). Covers the provider decision matrix, the unified wrapper interface (`requireAuth` / `requireRole` / `withOrgContext`), procedure tier stacking, session handling, OAuth callback safety, plugin composition with Better Auth, and the anti-patterns (hardcoded allowlists, admin client at module scope, triple-fallback auth surfaces).
---

# Factory auth

Each section leads with **Principle** (one sentence, stack-agnostic), then **Why** (constraint → option → tradeoff), then **Recipe** (the shape we use), and **Failure mode** when there's one to name. Sections that are pure style with no deeper truth are marked `Recipe only`. Editors: if the Principle could appear unchanged in any auth tutorial, sharpen the Why with a Factory-specific observation or drop the section to Recipe only.

## Provider pick — match the authz model, not the familiarity

**Principle.** Pick the provider whose model matches your authz shape; don't fight the provider for features it isn't built for.

**Why.** Auth providers differ in what they make easy. Better Auth is org-shaped (teams, roles, invitations). Supabase Auth + RLS is row-shaped (per-row policy reasoning). Clerk is consumer-shaped (managed UI, social login). Picking the wrong shape means every authz feature is upstream — you're rebuilding the provider's missing model. The wrapper interface below makes provider a swap point, so the cost of getting this wrong is bounded — but you still pay the swap.

**Recipe.**

| Provider | Pick when |
|---|---|
| **Better Auth + organization plugin** | Default. B2B with team/org concept. Drizzle-based projects. Need 2FA + magic link + admin out of the box. |
| **Supabase Auth + RLS** | RLS is doing real work — multi-role partner/distributor model, deeply branched authz at row level. Project already commits to Supabase. |
| **Clerk** | Consumer / SSO-heavy. Managed auth UI components matter. Org features secondary. |

## The wrapper interface — the single seam

**Principle.** The wrapper is the seam; the provider is swappable behind it.

**Why.** Every server action and API route calls auth. If they call the provider's SDK directly, swapping providers means touching every action. The wrapper concentrates the provider dependency in one file — `requireAuth`, `requireRole`, `withOrgContext` — and gives the call sites a stable interface that doesn't depend on which SDK is underneath. The cost is three small wrapper functions; the savings are linear in the number of mutations the project will ever have.

**Recipe.**

```ts
// src/lib/auth/index.ts
export async function requireAuth(): Promise<{ user: User; session: Session }> {
  const session = await getSession();
  if (!session) throw new AuthError('unauthenticated');
  return { user: session.user, session };
}

export async function requireRole(role: Role): Promise<{ user: User; session: Session }> {
  const ctx = await requireAuth();
  if (!ctx.user.roles.includes(role)) throw new AuthError('forbidden');
  return ctx;
}

export async function withOrgContext<T>(
  fn: (ctx: { orgId: string; user: User }) => Promise<T>,
): Promise<T> {
  const { user, session } = await requireAuth();
  const orgId = session.activeOrganizationId;
  if (!orgId) throw new AuthError('no_org_context');
  return fn({ orgId, user });
}
```

Every server action / API route uses these — never the provider directly. When you swap providers, only the body of these wrappers changes.

**Failure mode.** Cothon stacked three fallback auth paths: JWT → extension token → X-User-ID. Three things to test, three places to break, no single seam to swap.

## Procedure tier stacking (tRPC)

**Recipe only** — style decision. The principle (stack tiers by extension) lives in `factory-api.md §procedure tiers — stacked`.

```ts
export const publicProcedure = t.procedure;                          // anyone
export const protectedProcedure = publicProcedure.use(requireAuth);  // authed user
export const orgProcedure = protectedProcedure.use(requireOrg);      // authed + org context
```

For server actions, the equivalent is the wrapper functions above called at the top of each action.

## Better Auth — plugin composition

**Principle.** Use the official plugin when one exists; don't write your own auth adapter.

**Why.** The maintenance gradient on auth code is steep — every upstream release brings security fixes, every CVE means tracking patches. The official plugin absorbs that work; a custom adapter inherits the whole gradient yourself. The "we know our needs better than the maintainers" framing reliably costs more than the supposed flexibility saves.

**Recipe.**

```ts
// src/lib/auth.ts
import { betterAuth } from 'better-auth';
import { organization, admin, magicLink, twoFactor } from 'better-auth/plugins';

export const auth = betterAuth({
  database: drizzleAdapter(db, { provider: 'pg' }),
  plugins: [
    organization({ accessControl: customAC, roles: { owner, admin, member } }),
    admin(),
    magicLink({ sendMagicLink }),
    twoFactor(),
  ],
});
```

Custom access control via `accessControl` — define resource/action permissions explicitly, not roles inline.

**Failure mode.** Encode/monorepo wrote a custom NextAuth Postgres adapter when an official one existed; spent weeks tracking schema drift before deleting it in favor of the official adapter.

## Org-scoped multi-tenancy

**Principle.** Every domain table has an `orgId` FK with cascade delete, and every query filters by it via middleware-supplied context — both layers, never just one.

**Why.** A cross-tenant data leak is the worst auth bug — usually invisible at write time, only surfaced when a customer sees another customer's data. Defense in depth means schema enforces (FK with cascade), middleware enforces (query filter from context), and application code can't accidentally drop the filter (the filter comes from context, not from a parameter the caller chose).

**Recipe.**

```ts
const requireOrg = async (opts: { ctx: Context }) => {
  const session = opts.ctx.session;
  if (!session) throw new TRPCError({ code: 'UNAUTHORIZED' });
  const orgId = session.activeOrganizationId;
  if (!orgId) throw new TRPCError({ code: 'PRECONDITION_FAILED', message: 'no_org_context' });
  return { ...opts.ctx, orgId };
};
```

Every domain table has an `orgId` (or `workspaceId` / `projectId`) FK with `onDelete: 'cascade'`. Every query filters by it via the middleware-provided context.

## Auto-select organization

**Recipe only** — UX nicety. If the user belongs to exactly one org, auto-activate it on login.

```ts
export function useAutoSelectOrganization() {
  const { data: session } = useSession();
  const { data: orgs } = useOrganizations();
  useEffect(() => {
    if (session && !session.activeOrganizationId && orgs?.length === 1) {
      switchOrganization({ organizationId: orgs[0].id });
    }
  }, [session, orgs]);
}
```

Spares the user a meaningless click on the first session.

## RLS — only when authz branches on row content

**Principle.** Row-level security earns its keep only when authz branches on row content, not just on user identity.

**Why.** RLS adds per-query latency and is hard to debug — policy logic lives in Postgres, far from the call site. The tradeoff pays off when authz rules genuinely require row-level reasoning (distributor sees only their facilities; rep sees only assigned territories). For "user belongs to org," middleware-supplied filters are faster, simpler, and testable in TypeScript. Defaulting to RLS for simple multi-tenancy is paying a complexity tax that doesn't deliver.

**Recipe.**

For multi-role surfaces where the same query needs different behavior per audience (admin sees all, owner sees own distributor, rep sees facilities they have access to):

- Define RLS policies per table per role
- API layer is **auth-context-agnostic** — `listCasesWith(client)` takes a Supabase client, gets reused by admin queries (admin client, RLS bypassed) and RLS-scoped queries (anon/user client, RLS active)
- Auto-generated types via `supabase gen types typescript` — the schema is the source of truth

## JWT signature verification

**Principle.** Verify the JWT signature on every request; never trust unsigned claims.

**Why.** An unsigned JWT is a string the client controls. Trusting the `sub` claim without verification is trusting the client to say who they are. The cost of verification is one JWKS fetch (cached) per request; the cost of not verifying is the entire auth model.

**Recipe.**

```py
def verify_clerk_token(token: str) -> ClerkUser:
    jwks = fetch_jwks()  # cached
    payload = jwt.decode(token, jwks, algorithms=['RS256'])
    return ClerkUser(**payload)
```

## Fallback user-linking on first valid token

**Principle.** Create the user record inline on first valid-token request; don't depend on webhook arrival.

**Why.** Webhook delivery is best-effort — Clerk (or any provider) can deliver minutes late or not at all. If the application 404s a valid-token user while waiting for the webhook, the user sees a broken state for an unbounded amount of time. The signature verification establishes the user is real; the application can create the record on demand and let the webhook upsert later.

**Recipe.**

```py
async def get_or_create_user(clerk_user: ClerkUser) -> User:
    user = await db.scalar(select(User).where(User.clerk_id == clerk_user.sub))
    if user:
        return user
    return await create_user_from_clerk(clerk_user)
```

## OAuth callback safety — `safeNext`

**Principle.** Validate any redirect URL that comes from a query param; never trust the input.

**Why.** Open-redirect is a recurring bug class. The attacker crafts a link with `?next=https://evil.com`; the redirect handler trusts it; the user lands on a phishing page after a successful OAuth handshake — the trust signal is the worst possible. The defense is a small allowlist that rejects protocol-relative URLs, absolute URLs, and anything that isn't an in-app path.

**Recipe.**

```ts
function safeNext(next: string | null): string {
  if (!next) return '/';
  if (next.startsWith('//')) return '/';        // protocol-relative
  if (!next.startsWith('/')) return '/';        // not relative
  return next;
}

// OAuth callback skips ?next= for OAuth flows entirely
// (refresh-on-OAuth case is too easy to weaponize)
```

Apply in `/auth/callback`, login, signup-complete, magic-link-redirect — anywhere a URL comes from a query param.

## Role-conditional post-login redirect

**Recipe only** — routing detail. Don't hardcode `/dashboard`; look up role and redirect.

```ts
const profile = await getProfile(user.id);
if (profile.role === 'admin') return redirect('/admin');
if (profile.role === 'rep') return redirect('/submit');
return redirect('/');
```

## Admin client — always wrapped

**Principle.** An admin client never lives at module scope; always behind a wrapper that re-checks privilege.

**Why.** An admin client at module scope is a loaded gun — any code path that imports the module inherits the bypass. The wrapper forces the privilege check at every call site, which is the right place for it: the check is co-located with the privilege use, and the type system rejects callers who haven't gone through the wrapper.

**Recipe.**

```ts
// src/lib/supabase/admin.ts
export async function withAdmin<T>(fn: (admin: AdminClient) => Promise<T>): Promise<T> {
  await requireAdmin();           // verify caller is admin first
  return fn(createAdminClient());
}
```

Never export `createAdminClient` at the module top level — only behind `withAdmin`. See `factory-security.md` on the same pattern for service-role keys.

**Failure mode.** Module-scope `adminClient` export imported by a handler that should have used the user-scoped client — a cross-tenant write that bypassed RLS, undetected for weeks.

## Auth from day one, even with a shared password

**Principle.** Every endpoint authenticates from day one, even if every user shares a password.

**Why.** "We'll add auth later" reliably becomes "every procedure is `publicProcedure`" and ships to production that way. The cheapest auth surface (one shared password, one allowlist, one Bearer token) is infinitely better than none, because it forces every new endpoint to fit a pattern that expects auth. Retrofitting auth means walking every endpoint; pre-fitting auth means filling in the body.

**Recipe.** Even a single `requireAuth` that just checks an env-var token, attached to every procedure or wrapped around every server action, satisfies the principle. The point is the discipline, not the cryptographic strength.

**Failure mode.** Ford-analysis defined every tRPC procedure as `publicProcedure` with the plan to add auth later. Three procedures shipped without auth before someone caught it during a security review.

## Hardcoded email allowlists

**Principle.** Members live in a database table from day one; never hardcode the allowlist in config.

**Why.** A hardcoded allowlist is a deploy-to-add-a-user system. It shifts a user-management problem onto the deployment pipeline, which makes it slow and gated on engineering. A DB-backed members table is a query-to-add-a-user system, and from day one supports the admin UI that's coming anyway.

**Recipe.** A `members` table keyed by `orgId` + `userId` (or email if invitation flow). Add/remove via mutation, not via config change.

**Failure mode.** Encode/monorepo started with a NextAuth email allowlist in config. By week six, every new user was a deploy.

## Source patterns

Kairos (Supabase Auth + RLS, multi-role partner-distributor, auth-context-agnostic API, `safeNext`, role-conditional redirect, admin client wrapping, RowActions auth gating), duezy (Better Auth + organization plugin, session timeout provider, custom org-based ACL, dual mode forms with auth context), fleet-advisor (procedure tier stacking, Better Auth plugin composition, auto-select organization), cothon (Clerk JWT verification with fallback user-linking, context propagation via request.state, multi-tenant context dataclasses), encode/monorepo (NextAuth allowlist anti-pattern, custom adapter anti-pattern).
