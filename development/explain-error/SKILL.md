---
name: explain-error
description: Automatically diagnoses, explains, and resolves Better Auth runtime errors, configuration issues, database adapter mismatches, and authentication failure codes.
version: 1.0.0
---

# Better Auth Error Diagnostician & Explainer

This skill diagnoses and provides actionable resolutions for common Better Auth runtime errors, client error codes, configuration pitfalls, and database adapter issues.

## Common Error Codes & Resolutions

### 1. `INVALID_EMAIL_OR_PASSWORD`
- **Cause**: User credentials do not match database records, or password hashing mismatch.
- **Resolution**:
  - Verify that password hashing algorithm has not changed between migrations.
  - Verify that input email is trimmed/lowercased if `emailAndPassword.autoSignIn` or normalization is enabled.
  - Check client-side error handling:
    ```typescript
    const { data, error } = await authClient.signIn.email({
      email,
      password,
    })
    if (error?.status === 401 || error?.code === 'INVALID_EMAIL_OR_PASSWORD') {
      // Prompt user with user-friendly message
    }
    ```

### 2. `USER_ALREADY_EXISTS`
- **Cause**: Attempting to sign up with an email or account ID already in use.
- **Resolution**:
  - Direct user to sign in or password reset flow.
  - If social login is used with existing email, check `accountLinking.enabled`:
    ```typescript
    export const auth = betterAuth({
      account: {
        accountLinking: {
          enabled: true,
          trustedProviders: ['google', 'github'],
        },
      },
    })
    ```

### 3. `SESSION_EXPIRED` / `UNAUTHORIZED`
- **Cause**: Cookie expired, missing `credentials: "include"` on cross-origin fetch, or cookie domain mismatch.
- **Resolution**:
  - Client side: ensure `authClient` has the exact `baseURL` matching server.
  - Cross-domain setup:
    ```typescript
    export const auth = betterAuth({
      trustedOrigins: ['https://app.example.com', 'http://localhost:3000'],
      advanced: {
        crossSubDomainCookies: {
          enabled: true,
          domain: '.example.com',
        },
      },
    })
    ```

### 4. `FAILED_TO_VERIFY_EMAIL` / `INVALID_TOKEN`
- **Cause**: Verification token expired or used already.
- **Resolution**:
  - Verify email verification URL configuration in `emailVerification`:
    ```typescript
    emailVerification: {
      sendOnSignUp: true,
      autoSignInAfterVerification: true,
      sendVerificationEmail: async ({ user, url, token }) => {
        await sendEmail({ to: user.email, url })
      },
    }
    ```

### 5. `ADAPTER_ERROR` / Database Schema Mismatches
- **Cause**: Database tables do not match Better Auth expectations (missing columns like `emailVerified`, `image`, `twoFactorEnabled`, or relation tables).
- **Resolution**:
  - Run the Better Auth CLI schema generator / migration tool:
    ```bash
    npx @better-auth/cli generate
    npx @better-auth/cli migrate
    ```
  - If using Prisma, ensure schema has all required Better Auth models: `User`, `Session`, `Account`, `Verification`.

### 6. CORS / Preflight Failure on `/api/auth/*`
- **Cause**: Missing CORS headers or allowed methods on the API route handler.
- **Resolution**:
  - In Next.js / Hono / Express, ensure `toNextJsHandler` or framework adapter exposes `GET` and `POST`.
  - Ensure `BETTER_AUTH_URL` matches the canonical deployment URL.

## Diagnostic Checklist

When debugging an unknown Better Auth issue:
1. Check server console logs with `logger: { level: "debug" }` enabled in `betterAuth()`.
2. Inspect network tab response payload for the `{ code, message }` JSON object.
3. Verify database adapter connection string and table prefixes.
4. Verify cookie configuration in production (`secure: true` requires HTTPS).
