---
name: add-docs
description: Add JSDoc comments and inline documentation following Iridium patterns. Use when documenting functions, components, or adding code explanations.
---

# Add Docs

Adds documentation using JSDoc comments, inline explanations, and usage examples following Iridium patterns.

## When to Use

- Documenting exported functions and components
- Adding inline comments to complex logic
- User asks to "document this", "add JSDoc", or "explain this code"
- When code needs clarity for future maintainers

## Documentation Hierarchy

| Location | Purpose | Content |
|----------|---------|---------|
| `docs/` | User-facing guides | Conceptual explanations |
| `.github/instructions/` | Pattern reference | Technical patterns for AI |
| **Inline comments** | Context | "Why" explanations |
| **JSDoc** | API docs | Purpose, params, examples |

## JSDoc Template

```typescript
/**
 * Brief description of purpose (what it does)
 * Additional context about when/why to use it
 *
 * @param paramName - Clear description of parameter
 * @returns What the function returns and when
 * @throws Specific error conditions
 *
 * @example
 * const result = await myFunction(input);
 * if (!result) throw redirect('/error');
 */
```

## Pattern 1: Function Documentation

```typescript
/**
 * Fetches a user profile by ID with all displayable fields
 * Excludes sensitive data like password hashes and tokens
 *
 * @param userId - The unique user identifier
 * @returns User profile data or null if not found
 *
 * @example
 * const profile = await getUserProfile('user-123');
 * if (!profile) throw new Response('Not Found', { status: 404 });
 */
export function getUserProfile(userId: string) {
    return prisma.user.findUnique({
        where: { id: userId },
        select: {
            id: true,
            email: true,
            name: true,
            role: true,
            // Explicitly exclude: password, salt, tokens
        },
    });
}
```

## Pattern 2: Component Documentation

```tsx
/**
 * Primary action button with loading state and variants
 *
 * Uses CVA for variant management with DaisyUI classes.
 * See DaisyUI docs: https://daisyui.com/components/button/
 *
 * @example
 * // Primary button (default)
 * <Button>Submit</Button>
 *
 * @example
 * // Loading state
 * <Button loading disabled>Processing...</Button>
 *
 * @example
 * // Secondary variant
 * <Button status="secondary" size="lg">Cancel</Button>
 */
export function Button({ status, size, className, loading, ...props }: ButtonProps) {
    // Implementation
}
```

## Pattern 3: Inline Comments - Explain "Why"

**DO: Explain reasoning**
```typescript
// Use raw SQL for this query because Prisma doesn't support
// full-text search with ranking, and this needs to be fast
const results = await prisma.$queryRaw`...`;
```

**DON'T: State the obvious**
```typescript
// ❌ BAD - states what code does
// Loop through users
for (const user of users) {

// ❌ BAD - describes syntax
// Set name to new value
user.name = newName;
```

**DO: Document edge cases and workarounds**
```typescript
// BetterAuth requires cookies to be set before redirect,
// so we can't use React Router's redirect() helper here
return new Response(null, {
    status: 302,
    headers: {
        'Set-Cookie': sessionCookie,
        Location: '/dashboard',
    },
});
```

## Pattern 4: Type Documentation

```typescript
/**
 * User profile data for display purposes
 * Excludes sensitive fields like passwords and tokens
 */
export interface UserProfile {
    /** Unique user identifier (CUID format) */
    id: string;
    /** User's email address (verified) */
    email: string;
    /** Display name, may be null if not set */
    name: string | null;
    /** User's role for authorization checks */
    role: Role;
    /** Account creation timestamp */
    createdAt: Date;
}
```

## Pattern 5: Route Loader/Action Documentation

```typescript
/**
 * Loads user profile data for the profile page
 *
 * Requires authentication - redirects to /sign-in if not logged in.
 * All sensitive fields are excluded from the response.
 *
 * @returns User profile and related data
 * @throws Redirect to /sign-in if not authenticated
 */
export async function loader({ request }: Route.LoaderArgs) {
    const user = await requireUser(request);
    const profile = await getUserProfile(user.id);

    return data({ user, profile });
}

/**
 * Handles profile updates (PUT) and account deletion (DELETE)
 *
 * PUT: Updates user profile fields (name, bio, etc.)
 * DELETE: Permanently removes user account and all associated data
 *
 * @returns Success response or validation errors
 * @throws 400 for validation errors
 * @throws 403 if user tries to modify another user's profile
 */
export async function action({ request }: Route.ActionArgs) {
    // Implementation
}
```

## Pattern 6: Complex Algorithm Documentation

```typescript
/**
 * Calculates the subscription renewal date based on billing cycle
 *
 * The algorithm handles edge cases:
 * - Month-end dates (Jan 31 → Feb 28/29)
 * - Leap years
 * - Time zone differences (uses UTC)
 *
 * @param startDate - Original subscription start date
 * @param billingCycle - 'monthly' | 'yearly'
 * @returns Next renewal date in UTC
 */
function calculateRenewalDate(startDate: Date, billingCycle: BillingCycle): Date {
    // Add the appropriate interval
    const renewal = new Date(startDate);

    if (billingCycle === 'monthly') {
        // Use setMonth which handles month-end edge cases
        renewal.setMonth(renewal.getMonth() + 1);
    } else {
        renewal.setFullYear(renewal.getFullYear() + 1);
    }

    return renewal;
}
```

## When to Document

**Always document:**
- All exported functions and components
- Non-obvious business logic
- Complex algorithms or data transformations
- Workarounds for framework limitations
- Security-sensitive code paths
- API response shapes

**Skip documentation for:**
- Self-explanatory one-liners
- Standard CRUD operations with obvious names
- Private helper functions used once

## Quality Checklist

- [ ] JSDoc on all exported functions
- [ ] Parameters have clear descriptions
- [ ] Return values are documented
- [ ] Error conditions are noted
- [ ] Examples show common usage
- [ ] Inline comments explain "why", not "what"
- [ ] No stating the obvious
- [ ] Links to external docs where helpful

## Anti-Patterns

- Documenting what code does instead of why
- Outdated comments that don't match code
- Obvious comments (`// increment counter`)
- Missing parameter descriptions
- No examples for complex APIs
- Documenting private/internal functions excessively

## Full Reference

See `.claude/agents/iridium-pair-programmer.md` for documentation standards and code quality guidelines.
