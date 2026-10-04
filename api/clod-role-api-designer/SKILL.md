---
name: "Role: API Designer"
description: "Type-safe API design: Zod validation, Result types, SvelteKit endpoints, middleware patterns."
when_to_use: "When designing or reviewing an API endpoint, request/response contract or validation layer; fires for API design, Zod schemas and error handling whether or not route files exist yet."
user-invocable: false
metadata:
  family: clod-role
# No paths gate: API design conversations start before route files exist, and
# paths would suppress exactly that trigger
allowed-tools:
  - Read
  - Glob
  - Grep
---

# TypeScript API Design

Comprehensive guide to designing type-safe APIs with TypeScript. Covers type-safe contracts, validation with Zod, Result types for error handling, SvelteKit endpoints, middleware patterns and API versioning.

## When This Skill Applies

Use this skill when:
- Designing API endpoints
- Creating type-safe API contracts
- Implementing validation
- Handling API errors
- Building SvelteKit API routes
- Creating reusable middleware
- Versioning APIs
- Questions about API design patterns

## Type-Safe Contracts

### Request/Response Types
```typescript
// types/api.ts
export interface CreateUserRequest {
	email: string;
	name: string;
	password: string;
}

export interface User {
	id: string;
	email: string;
	name: string;
	createdAt: string;
}

export interface ApiError {
	code: string;
	message: string;
	details?: Record<string, string[]>;
}
```

**Key principle**: Types ARE documentation. Well-named types with clear structure tell the story.

### Result Type Pattern
```typescript
// For expected failures (not found, validation, etc.)
export type Result<T, E = string> =
	| { success: true; data: T }
	| { success: false; error: E };

// Usage
function findUser(id: string): Result<User, 'not_found'> {
	const user = db.findUser(id);
	if (!user) {
		return { success: false, error: 'not_found' };
	}
	return { success: true, data: user };
}

// Consuming
const result = findUser('123');
if (result.success) {
	console.log(result.data.email); // Type-safe access
} else {
	console.error('Error:', result.error);
}
```

### API Response Format
```typescript
// Standard success response
export interface ApiSuccess<T> {
	success: true;
	data: T;
}

// Standard error response
export interface ApiError {
	success: false;
	error: {
		code: string;
		message: string;
		details?: Record<string, string[]>;
	};
}

export type ApiResponse<T> = ApiSuccess<T> | ApiError;
```

### Endpoint Type Map
```typescript
// Optional: Define all endpoints in one place
export interface ApiEndpoints {
	'POST /api/users': {
		request: CreateUserRequest;
		response: User;
	};
	'GET /api/users/:id': {
		params: { id: string };
		response: User;
	};
	'PATCH /api/users/:id': {
		params: { id: string };
		request: Partial<UpdateUserRequest>;
		response: User;
	};
	'DELETE /api/users/:id': {
		params: { id: string };
		response: null;
	};
}
```

## Additional resources

Deep-dive detail lives in supporting files, loaded only when needed:

- [validation-and-errors.md](validation-and-errors.md): Zod schemas, Result types vs. Error classes, centralised error handling
- [sveltekit-and-middleware.md](sveltekit-and-middleware.md): GET/POST/PATCH/DELETE endpoint patterns, auth/validation/rate-limit/composed middleware
- [auth-and-database.md](auth-and-database.md): cookie/JWT/Supabase session patterns, typed PostgreSQL and Neo4j wrappers
- [versioning-and-clients.md](versioning-and-clients.md): URL-based versioning, type-safe API clients, OpenAPI generation, endpoint/business-logic testing
- [privacy.md](privacy.md): response filtering, request minimisation, sensitive-data handling, auth scoping, data deletion

## Best Practices

### 1. Always Validate Input
```typescript
// ✓ Good - validate with Zod
const data = CreateUserSchema.parse(input);
const user = await createUser(data);

// ✗ Bad - trusting client input
const user = await createUser(input);
```

### 2. Use Result Types for Expected Failures
```typescript
// ✓ Good - Result type for expected failure
function findUser(id: string): Result<User, 'not_found'> {
	const user = db.findUser(id);
	if (!user) {
		return { success: false, error: 'not_found' };
	}
	return { success: true, data: user };
}

// ✗ Bad - throwing for expected case
function findUser(id: string): User {
	const user = db.findUser(id);
	if (!user) throw new Error('Not found');
	return user;
}
```

### 3. Throw Error Classes for Unexpected Failures
```typescript
// ✓ Good - throw for exceptional case
async function connectDatabase(): Promise<Database> {
	try {
		return await connect();
	} catch (error) {
		throw new DatabaseError('Failed to connect');
	}
}

// ✗ Bad - Result type for exceptional case
async function connectDatabase(): Result<Database, string> {
	// Database connection should succeed or crash
}
```

### 4. Type Everything Explicitly
```typescript
// ✓ Good - explicit types
interface CreateUserRequest {
	email: string;
	name: string;
}

async function createUser(data: CreateUserRequest): Promise<User> {
	// ...
}

// ✗ Bad - implicit any
async function createUser(data): Promise<any> {
	// ...
}
```

### 5. Separate Concerns (Layered Architecture)
```typescript
// ✓ Good - separated layers

// Handler (thin, delegates to service)
export const POST: RequestHandler = async ({ request }) => {
	const data = await validateRequest(request, CreateUserSchema);
	const user = await createUser(data);
	return json({ success: true, data: user }, { status: 201 });
};

// Service (business logic)
async function createUser(data: CreateUserRequest): Promise<User> {
	const passwordHash = await hashPassword(data.password);
	return await db.users.create({ ...data, passwordHash });
}

// ✗ Bad - everything in handler
export const POST: RequestHandler = async ({ request }) => {
	const body = await request.json();
	// validation, hashing, database, all mixed together
};
```

### 6. Use Middleware for Cross-Cutting Concerns
```typescript
// ✓ Good - reusable middleware
export const POST: RequestHandler = async (event) => {
	const user = await requireAuth(event);
	const data = await validateRequest(event.request, CreatePostSchema);
	const post = await createPost(user.id, data);
	return json({ success: true, data: post });
};

// ✗ Bad - repeating auth/validation everywhere
export const POST: RequestHandler = async ({ request, cookies }) => {
	// Repeated auth code
	const session = cookies.get('session');
	if (!session) throw error(401);
	const user = await verifySession(session);

	// Repeated validation code
	const body = await request.json();
	if (!body.title) throw error(400);
	// ...
};
```

### 7. Document with Types, Not Comments
```typescript
// ✓ Good - type tells the story
interface CreateUserRequest {
	email: string;          // Type is clear
	name: string;           // Type is clear
	password: string;       // Min 8 chars (Zod enforces)
}

// ✗ Bad - relying on comments
interface CreateUserRequest {
	email: string;          // Must be valid email
	name: string;           // Required, 2-100 chars
	password: string;       // Min 8, uppercase, lowercase, number, special
}
// Comments get out of sync with code!
```

## Success Criteria

API design is well-structured when:
- All requests/responses explicitly typed
- Input validated with Zod schemas
- Expected failures use Result types
- Unexpected failures throw Error classes
- Endpoints follow REST conventions
- Middleware reusable and composable
- Database layer has typed wrappers
- Authentication consistent across endpoints
- Errors have standardised format
- Type-safe client available for consumption
- Tests cover happy path and error cases
- Code is maintainable and follows patterns
- Responses expose minimum necessary data (privacy-by-default)
- No sensitive data logged or leaked
- Auth scoping prevents cross-user data access
- Data deletion is supported and complete
