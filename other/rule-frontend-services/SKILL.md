---
name: rule-frontend-services
description: MANDATORY when editing files matching ["frontend/src/services/**/*.ts"]. When working on API service integration in frontend/src/services/
---

# Frontend Services Rules

## Centralized Fetch Factory
ALWAYS create API client functions using `requesterForEndpoint()` with an `EndpointConfig` object. NEVER write raw `fetch()` calls to the backend API from server-side code.

Example from codebase:
```typescript
// From frontend/src/services/fetch/endpointConfigs.ts
export const fetchApplicationsEndpoint = {
  basePath: environment.API_URL,
  version: "alpha",
  namespace: "applications",
  method: "POST" as ApiMethod,
};

// From frontend/src/services/fetch/fetchers/fetchers.ts
export const fetchCompetition = cache(
  requesterForEndpoint(fetchCompetitionEndpoint),
);
```

## Thin Domain Fetcher Wrappers
ALWAYS create a dedicated fetcher file in `src/services/fetch/fetchers/` for each API resource. MUST handle session retrieval, header construction, and response extraction.

Example from codebase:
```typescript
// From frontend/src/services/fetch/fetchers/applicationsFetcher.ts
"server-only";

export const getApplications = async (
  token: string,
  userId: string,
): Promise<ApplicationDetail[]> => {
  const ssgToken = { "X-SGG-Token": token };
  const resp = await fetchUserWithMethod("POST")({
    subPath: `${userId}/applications`,
    additionalHeaders: ssgToken,
    body: { pagination: { page_offset: 1, page_size: 5000 } },
  });
  const json = (await resp.json()) as { data: [] };
  return json.data;
};
```

## "server-only" Directive on Server Fetchers
ALWAYS add the `"server-only"` directive at the top of server-side fetcher files. NEVER allow server-only code to be imported in client components.

Example from codebase:
```typescript
// From frontend/src/services/fetch/fetchers/applicationsFetcher.ts
"server-only";

import { UnauthorizedError } from "src/errors";
import { getSession } from "src/services/auth/session";
```

## useClientFetch for Client-Side Requests
ALWAYS use `useClientFetch<T>()` for client-side API requests. NEVER use raw `fetch()` in client components.

Example from codebase:
```typescript
// From frontend/src/components/workspace/OrganizationInvitationReply.tsx
const { clientFetch } = useClientFetch<OrganizationInvitation>(
  "unable to respond to invitation",
);

clientFetch(
  `/api/user/organization-invitations/${id}`,
  { method: "POST", body: JSON.stringify({ accepted }) },
).then((response) => setInvitationStatus(response.status));
```

## Promise.all for Parallel Fetches in RSC Pages
ALWAYS fetch data in parallel using `Promise.all`. ALWAYS name unresolved promises as `varNamePromise`.

Example from codebase:
```typescript
// From frontend/src/app/[locale]/workspace/page.tsx
const session = await getSession();
const userRolesPromise = getUserPrivileges(session.token, session.user_id);
const userOrganizationsPromise = getUserOrganizations(session.token, session.user_id);

try {
  [userRoles, userOrganizations] = await Promise.all([
    userRolesPromise,
    userOrganizationsPromise,
  ]);
} catch (e) {
  console.error("Unable to fetch user details", e);
}
```

## X-SGG-Token Header for Authenticated Requests
ALWAYS pass the user's token via an `X-SGG-Token` header for authenticated server-side API calls. NEVER pass tokens in the request body or query params.

Example from codebase:
```typescript
// From frontend/src/services/fetch/fetchers/userFetcher.ts
const ssgToken = { "X-SGG-Token": token };
await fetchUserWithMethod("POST")({
  subPath: `${userId}/can_access`,
  additionalHeaders: ssgToken,
  body: { resource_type: resourceType, privilege: "manage_org_members" },
});
```

## getSession() as Sole Server-Side Auth Entry Point
ALWAYS use `getSession()` from `src/services/auth/session.ts` for server-side auth. ALWAYS check for null session and missing token before authenticated operations.

Example from codebase:
```typescript
// From frontend/src/services/fetch/fetchers/applicationsFetcher.ts
export const fetchApplications = async (): Promise<ApplicationDetail[]> => {
  const session = await getSession();
  if (!session || !session.token) {
    throw new UnauthorizedError("No active session");
  }
  return await getApplications(session.token, session.user_id);
};
```

## ApiRequestError and parseErrorStatus
ALWAYS use `ApiRequestError` from `src/errors.ts` for API error handling. ALWAYS use `parseErrorStatus()` to extract HTTP status codes. MUST return `<NotFound />` for 404 errors.

Example from codebase:
```typescript
// From frontend/src/app/[locale]/opportunity/[id]/page.tsx
try {
  const response = await getCompetitionDetails(id);
} catch (error) {
  if (parseErrorStatus(error as ApiRequestError) === 404) {
    return <NotFound />;
  }
  return <TopLevelError />;
}
```

## { data: T } Response Envelope
ALWAYS type API responses using the `{ data: T }` envelope pattern. ALWAYS extract `.data` before returning.

Example from codebase:
```typescript
// From frontend/src/services/fetch/fetchers/organizationFetcher.ts
const json = (await resp.json()) as { data: UserRole[] };
return json.data;
```

## Types: Prefer type over interface
ALWAYS place shared types in `src/types/`. ALWAYS use `type` by default. ONLY use `interface` when the type will be extended.

Example from codebase:
```typescript
// From frontend/src/types/userTypes.ts
export type OrganizationInvitation = {
  organization_invitation_id: string;
  status: string;
  created_at: string;
};

export interface RoleDefinition { role_id: string; role_name: string; }
export interface UserRole extends RoleDefinition { privileges: Privileges[]; }
```

## Zod Validation for Server Actions
ALWAYS use Zod schemas for server-side form validation. ALWAYS use `safeParse()` and return `error.flatten().fieldErrors`. ALWAYS use translated validation messages.

Example from codebase:
```typescript
// From frontend/src/app/actions/inviteUserAction.ts
const schema = z.object({
  email: z.string().min(1, { message: t("email") }),
  role: z.string().min(1, { message: t("role") }),
});
const validatedFields = schema.safeParse({
  email: formData.get("email"),
  role: formData.get("role"),
});
if (!validatedFields.success) {
  return validatedFields.error.flatten().fieldErrors;
}
```

## withFeatureFlag HOC for Feature-Gated Pages
ALWAYS use `withFeatureFlag(Component, "flagName", fallback)` to gate pages. ALWAYS name flags in camelCase with a boolean-off default.

Example from codebase:
```typescript
// From frontend/src/app/[locale]/organization/[id]/page.tsx
export default withFeatureFlag<OrganizationDetailPageProps, never>(
  OrganizationDetailPage,
  "userAdminOff",
  () => redirect("/maintenance"),
);
```

## AuthorizationGate and AuthenticationGate
ALWAYS use `AuthenticationGate` for login-required pages. ALWAYS use `AuthorizationGate` for privilege-required pages. NEVER perform client-side privilege checking.

Example from codebase:
```typescript
// From frontend/src/app/[locale]/organization/[id]/page.tsx
<AuthorizationGate
  resourcePromises={{
    organizationDetails: getOrganizationDetails(session?.token || "", id),
  }}
  requiredPrivileges={[{
    resourceId: id,
    resourceType: "organization",
    privilege: "manage_org_members",
  }]}
  onUnauthorized={() => <UnauthorizedMessage />}
>
  <OrganizationDetail organizationId={id} />
</AuthorizationGate>
```

---

## Context Enrichment

When generating significant service code (new fetcher, new API integration, auth changes), enrich your context:
- Call `get_architecture_section("frontend")` from the `simpler-grants-context` MCP server to understand frontend service layer principles
- Call `get_rule_detail("api-error-handling")` for how the API surfaces errors that the frontend must handle
- Consult **Compound Knowledge** for indexed documentation on fetch patterns, error handling, and auth integration

## Related Rules

When working on frontend services, also consult these related rules:
- **`frontend-hooks.mdc`** — `useClientFetch` hook that components use for client-side requests
- **`frontend-components.mdc`** — how components consume server-side fetchers and handle errors
- **`api-error-handling.mdc`** — API error response format that frontend must parse (`ValidationErrorDetail`)
- **`cross-domain.mdc`** — feature flags, structured error patterns

## Specialist Validation

When generating or significantly modifying frontend service code:

**For simple changes (< 20 lines, adding a header):**
No specialist invocation needed — the directives in this rule file are sufficient.

**For moderate changes (new fetcher function, new endpoint config):**
Invoke `codebase-conventions-reviewer` to validate against service conventions.

**For complex changes (new auth flow, error handling overhaul, new service pattern):**
Invoke the following specialists (run in parallel where possible):
- `security-sentinel` — validate token handling, no credentials in URLs/logs, proper auth flow
- `performance-oracle` — validate fetch patterns, caching, parallel request efficiency
- `kieran-typescript-reviewer` — TypeScript-specific quality review
