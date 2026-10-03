---
name: using-clerk
description: Implement Clerk authentication — C# SDK and React integration, Svix webhook verification, org multi-tenancy.
when_to_use: Reach for this when adding/operating user auth via Clerk in a .NET or React app. For generic third-party webhook/idempotency patterns (non-auth) use building-integrations. This is the auth-provider skill; there is no Supabase-auth or Auth0 skill here, so Clerk is the only managed-auth option in this library.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
paths:
  - "**/*.tsx"
  - "**/*.ts"
  - "package.json"
  - "Program.cs"
---

# Clerk Authentication Skill

**Version**: 1.0.0 | **Target**: <500 lines | **Purpose**: Fast reference for Clerk auth integration

---

## When to Use

Load this skill when:
- `CLERK_SECRET_KEY` or `CLERK_PUBLISHABLE_KEY` environment variable present
- `@clerk/clerk-react` or `@clerk/nextjs` in `package.json` dependencies
- `Clerk.BackendAPI` or `Clerk.Net` in `.csproj` PackageReference
- User mentions "Clerk", "Clerk auth", or Clerk-based authentication

---

## SDK Overview

Two .NET SDK options exist for Clerk. Choose based on your use case.

### Official SDK: Clerk.BackendAPI

- **NuGet**: `Clerk.BackendAPI` (Jan 2025, beta, auto-generated from OpenAPI spec)
- **Best for**: Direct Clerk API calls (user management, organization CRUD, invitations)
- **Limitation**: No built-in ASP.NET Core middleware for JWT validation

```csharp
var sdk = new ClerkBackendApi(bearerAuth: Environment.GetEnvironmentVariable("CLERK_SECRET_KEY"));
var response = await sdk.Users.GetAsync("user_2abc123");
```

### Community SDK: Clerk.Net (Hawxy)

- **NuGet**: `Clerk.Net` (community-maintained, mature)
- **Best for**: ASP.NET Core middleware, JWT authentication, request validation

### When to Choose Which

| Use Case | Recommended SDK |
|----------|----------------|
| ASP.NET Core JWT middleware / `[Authorize]` | `Clerk.Net` |
| Creating/updating users or orgs via API | `Clerk.BackendAPI` |
| Both middleware + API calls | Both (they coexist) |

---

## .NET Backend Integration

Use `Clerk.Net` for request authentication middleware in ASP.NET Core.

### Service Registration

```csharp
// Program.cs
using Clerk.Net.DependencyInjection;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddClerkApiClient(options =>
{
    options.SecretKey = builder.Configuration["Clerk:SecretKey"]!;
});
builder.Services.AddClerkJwtAuthentication();
builder.Services.AddAuthorization();

var app = builder.Build();
app.UseAuthentication();
app.UseAuthorization();
```

### Protecting Endpoints

```csharp
[ApiController]
[Route("api/[controller]")]
[Authorize]  // Requires valid Clerk JWT
public class ProfileController : ControllerBase
{
    [HttpGet]
    public IActionResult GetProfile()
    {
        var userId = User.FindFirst("sub")?.Value;
        if (userId is null) return Unauthorized();
        return Ok(new { UserId = userId });
    }
}
```

### JWT Claims Reference

| Claim | Description | Example |
|-------|-------------|---------|
| `sub` | Clerk user ID | `user_2abc123` |
| `azp` | Authorized party (app origin) | `https://myapp.com` |
| `org_id` | Active organization ID (if set) | `org_2def456` |
| `org_role` | Role in active organization | `org:admin` |
| `org_slug` | Organization slug | `acme-corp` |

```csharp
// Extension methods for common claim extraction
public static class ClerkClaimsExtensions
{
    public static string? GetClerkUserId(this ClaimsPrincipal user)
        => user.FindFirst("sub")?.Value;

    public static string? GetActiveOrgId(this ClaimsPrincipal user)
        => user.FindFirst("org_id")?.Value;

    public static string? GetOrgRole(this ClaimsPrincipal user)
        => user.FindFirst("org_role")?.Value;
}
```

### Environment Variables

```bash
CLERK_SECRET_KEY=sk_live_xxxxx       # Backend secret key
CLERK_PUBLISHABLE_KEY=pk_live_xxxxx  # Frontend publishable key
```

---

## Webhook Handling

**CRITICAL**: Use the Svix library for webhook verification. Do NOT implement custom HMAC. Clerk uses Svix infrastructure and the `Svix.Webhook` class handles signature validation, timestamp tolerance, and replay prevention.

```xml
<PackageReference Include="Svix" Version="1.*" />
```

### Webhook Endpoint

```csharp
[ApiController]
[Route("api/webhooks")]
public class ClerkWebhookController : ControllerBase
{
    private readonly string _webhookSecret;

    public ClerkWebhookController(IConfiguration config)
    {
        _webhookSecret = config["Clerk:WebhookSecret"]
            ?? throw new InvalidOperationException("Clerk:WebhookSecret is required");
    }

    [HttpPost("clerk")]
    [AllowAnonymous]  // Verified via signature, not JWT
    public async Task<IActionResult> HandleWebhook()
    {
        var body = await new StreamReader(Request.Body).ReadToEndAsync();

        var headers = new Dictionary<string, string>
        {
            ["svix-id"] = Request.Headers["svix-id"].ToString(),
            ["svix-timestamp"] = Request.Headers["svix-timestamp"].ToString(),
            ["svix-signature"] = Request.Headers["svix-signature"].ToString(),
        };

        try
        {
            new Webhook(_webhookSecret).Verify(body, headers);
        }
        catch (WebhookVerificationException)
        {
            return Unauthorized("Invalid webhook signature");
        }

        var payload = JsonSerializer.Deserialize<JsonElement>(body);
        var eventType = payload.GetProperty("type").GetString();

        switch (eventType)
        {
            case "user.created":
                await HandleUserCreated(payload.GetProperty("data"));
                break;
            case "user.updated":
                await HandleUserUpdated(payload.GetProperty("data"));
                break;
            case "user.deleted":
                await HandleUserDeleted(payload.GetProperty("data"));
                break;
            case "organization.created":
                await HandleOrgCreated(payload.GetProperty("data"));
                break;
        }
        return Ok();
    }
}
```

### Common Webhook Event Types

| Event | Trigger |
|-------|---------|
| `user.created` | New user signs up |
| `user.updated` | Profile or metadata changes |
| `user.deleted` | Account deleted |
| `session.created` | New session started |
| `session.ended` | Session terminated |
| `organization.created` | New organization created |
| `organizationMembership.created` | User added to organization |
| `organizationMembership.deleted` | User removed from organization |

### Idempotency

Use the `svix-id` header to deduplicate webhook deliveries:

```csharp
var svixId = Request.Headers["svix-id"].ToString();
if (await _eventStore.ExistsAsync(svixId))
    return Ok();  // Already processed
// ... process event ...
await _eventStore.MarkProcessedAsync(svixId);
```

---

## React Frontend Integration

### Provider Setup

```tsx
// Next.js App Router
import { ClerkProvider } from "@clerk/nextjs";

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <ClerkProvider>
      <html lang="en"><body>{children}</body></html>
    </ClerkProvider>
  );
}
```

```tsx
// Non-Next.js React (Vite, CRA, etc.)
import { ClerkProvider } from "@clerk/clerk-react";

function App() {
  return (
    <ClerkProvider publishableKey={import.meta.env.VITE_CLERK_PUBLISHABLE_KEY}>
      <Router />
    </ClerkProvider>
  );
}
```

### Pre-Built Components and Protected Routes

```tsx
import { SignedIn, SignedOut, UserButton, RedirectToSignIn } from "@clerk/clerk-react";

function Header() {
  return (
    <header>
      <SignedIn><UserButton afterSignOutUrl="/" /></SignedIn>
      <SignedOut><a href="/sign-in">Sign In</a></SignedOut>
    </header>
  );
}

function ProtectedPage() {
  return (
    <>
      <SignedIn><Dashboard /></SignedIn>
      <SignedOut><RedirectToSignIn /></SignedOut>
    </>
  );
}
```

### Hooks

```tsx
import { useUser, useAuth } from "@clerk/clerk-react";

function Profile() {
  const { user, isLoaded, isSignedIn } = useUser();
  const { getToken } = useAuth();

  if (!isLoaded) return <div>Loading...</div>;
  if (!isSignedIn) return <div>Not signed in</div>;

  const callApi = async () => {
    const token = await getToken();  // Short-lived JWT, auto-refreshed
    return fetch("/api/profile", {
      headers: { Authorization: `Bearer ${token}` },
    }).then((r) => r.json());
  };

  return (
    <div>
      <p>Hello, {user.firstName}</p>
      <button onClick={callApi}>Fetch Profile</button>
    </div>
  );
}
```

---

## Organization Multi-Tenancy

### Frontend: Organization Switcher

```tsx
import { OrganizationSwitcher, useOrganization } from "@clerk/clerk-react";

function OrgSwitcher() {
  return <OrganizationSwitcher hidePersonal={false} afterSelectOrganizationUrl="/dashboard" />;
}

function OrgDashboard() {
  const { organization, membership, isLoaded } = useOrganization();
  if (!isLoaded) return <div>Loading...</div>;
  if (!organization) return <div>Select an organization</div>;
  return (
    <div>
      <h1>{organization.name}</h1>
      <p>Your role: {membership?.role}</p>
    </div>
  );
}
```

### Passing org_id in API Calls

```tsx
function OrgApiCaller() {
  const { getToken, orgId } = useAuth();

  const fetchOrgData = async () => {
    const token = await getToken();
    return fetch(`/api/orgs/${orgId}/data`, {
      headers: { Authorization: `Bearer ${token}` },
    }).then((r) => r.json());
  };

  return <button onClick={fetchOrgData}>Load Org Data</button>;
}
```

### Backend: Tenant Resolution from JWT

```csharp
[ApiController]
[Route("api/orgs/{orgId}/data")]
[Authorize]
public class OrgDataController : ControllerBase
{
    [HttpGet]
    public IActionResult GetOrgData(string orgId)
    {
        // Verify active org in JWT matches the requested org
        var tokenOrgId = User.FindFirst("org_id")?.Value;
        if (tokenOrgId != orgId) return Forbid();

        var orgRole = User.FindFirst("org_role")?.Value;
        return Ok(new { OrgId = orgId, Role = orgRole });
    }
}
```

---

## Session Management

**CRITICAL**: Clerk session tokens (JWTs) have a default expiry of **60 seconds**. The frontend SDK handles automatic refresh transparently. Do not cache tokens beyond a single API call.

| Token Type | Lifetime | Use Case |
|------------|----------|----------|
| Session JWT | 60 seconds (default) | API calls from frontend |
| Long-lived API key | Configurable | Server-to-server communication |
| `CLERK_SECRET_KEY` | Permanent (until rotated) | Backend SDK authentication |

```tsx
// CORRECT: Call getToken() before each API request
async function fetchData() {
  const token = await getToken();  // Returns cached or refreshed token
  return fetch("/api/data", { headers: { Authorization: `Bearer ${token}` } });
}

// WRONG: Storing token for reuse across time-separated calls
const [token] = useState(await getToken());  // Stale in 60s
```

### Next.js Middleware

```typescript
import { clerkMiddleware, createRouteMatcher } from "@clerk/nextjs/server";

const isPublicRoute = createRouteMatcher([
  "/", "/sign-in(.*)", "/sign-up(.*)", "/api/webhooks(.*)",
]);

export default clerkMiddleware(async (auth, request) => {
  if (!isPublicRoute(request)) await auth.protect();
});

export const config = {
  matcher: [
    "/((?!_next|[^?]*\\.(?:html?|css|js(?!on)|jpe?g|webp|png|gif|svg|ttf|woff2?|ico|csv|docx?|xlsx?|zip|webmanifest)).*)",
    "/(api|trpc)(.*)",
  ],
};
```

---

## Quick Reference Card

### Key Packages

| Package | Platform | Purpose |
|---------|----------|---------|
| `Clerk.Net` | NuGet | ASP.NET Core JWT middleware |
| `Clerk.BackendAPI` | NuGet | Clerk API client (official, beta) |
| `Svix` | NuGet | Webhook signature verification |
| `@clerk/clerk-react` | npm | React hooks and components |
| `@clerk/nextjs` | npm | Next.js integration (middleware, SSR) |

### Environment Variables

| Variable | Where | Purpose |
|----------|-------|---------|
| `CLERK_SECRET_KEY` | Backend | Authenticate SDK requests |
| `CLERK_PUBLISHABLE_KEY` | Frontend | Initialize ClerkProvider |
| `CLERK_WEBHOOK_SECRET` | Backend | Verify webhook signatures |

### Minimal Setup Snippets

```csharp
// .NET
builder.Services.AddClerkApiClient(o => o.SecretKey = "sk_...");
builder.Services.AddClerkJwtAuthentication();
app.UseAuthentication();
app.UseAuthorization();
```

```tsx
// React
<ClerkProvider publishableKey="pk_...">
  <SignedIn><App /></SignedIn>
  <SignedOut><RedirectToSignIn /></SignedOut>
</ClerkProvider>
```

### Key Base-Model Corrections

These facts correct common base-model hallucinations about Clerk:

1. The official `Clerk.BackendAPI` NuGet package exists (released Jan 2025, beta). It is auto-generated from the OpenAPI spec, not hand-crafted.
2. The community `Clerk.Net` (by Hawxy) is more mature and provides ASP.NET Core middleware that `Clerk.BackendAPI` does not include.
3. Webhook verification **must** use the `Svix` library. Do not implement custom HMAC -- Clerk uses Svix infrastructure and the signature format is Svix-specific.
4. Default JWT expiry is **60 seconds** with automatic refresh on the frontend. Do not cache tokens across time-separated calls.
