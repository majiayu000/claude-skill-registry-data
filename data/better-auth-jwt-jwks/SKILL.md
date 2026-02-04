---
name: "better-auth-jwt-jwks"
description: "Expert skill for implementing Better Auth with JWT tokens and JWKS (JSON Web Key Set) for secure authentication between Next.js frontend and FastAPI backend. Handles JWT token generation, verification, JWKS endpoint setup, and secure API communication. Includes setup for database integration, session management, and user isolation. Use when implementing authentication between frontend (Next.js) and backend (FastAPI) services with JWT tokens and JWKS."
---

# Better Auth JWT and JWKS Implementation Skill

## When to Use This Skill

- User wants to implement Better Auth with JWT tokens for Next.js + FastAPI authentication
- Need to set up secure communication between frontend and backend services
- Want to implement user isolation with JWT token verification
- Need JWKS endpoint for public key distribution and token verification
- Looking for stateless authentication without server-side sessions

## How This Skill Works (Step-by-Step Execution)

1. **Better Auth Configuration**
   - Set up Better Auth with JWT plugin for token generation
   - Configure database connection (PostgreSQL recommended)
   - Enable email/password and social authentication
   - Configure JWT algorithm (RS256 or EdDSA) and expiration

2. **JWKS Endpoint Setup (Frontend)**
   - Create `/api/jwks` endpoint to expose public keys
   - Implement database storage for JWKS keys
   - Add caching headers for performance optimization
   - Configure key rotation and management

3. **FastAPI JWT Verification**
   - Install `pyjwt` and `cryptography` dependencies
   - Create JWKS client to fetch public keys
   - Implement JWT verification middleware
   - Create dependency injection for user authentication

4. **Secure API Implementation**
   - Protect API routes with JWT verification
   - Implement user isolation (verify user_id matches request)
   - Add proper error handling for token issues
   - Configure environment variables for shared secrets

## Output You Will Receive

After activation, I will deliver:

- Complete Better Auth configuration with JWT plugin
- JWKS endpoint implementation for key distribution
- FastAPI middleware for JWT token verification
- Protected API route examples with user isolation
- Environment variable setup for both services
- Database schema for JWKS storage
- Error handling and security best practices

## Example Usage

**User says:**
"I have a Next.js 14 App with Better Auth and need to secure my FastAPI backend with JWT tokens."

**This Skill Instantly Activates → Delivers:**

- Better Auth JWT plugin configuration
- `/api/jwks` endpoint in Next.js for public key exposure
- FastAPI middleware using `pyjwt` and JWKS client
- Protected route examples with user isolation
- Shared secret configuration between services
- Complete setup for secure frontend-backend communication

**User says:**
"Implement JWT authentication between my Next.js frontend and FastAPI backend."

**This Skill Responds:**
→ Sets up Better Auth with JWT generation on frontend
→ Creates JWKS endpoint for key distribution
→ Implements JWT verification in FastAPI backend
→ Provides user isolation and security best practices

## Activate This Skill By Saying

- "Set up Better Auth with JWT and JWKS"
- "Secure my FastAPI backend with Better Auth JWT tokens"
- "Implement JWT authentication between Next.js and FastAPI"
- "I need user isolation with JWT tokens"

## Core Implementation Steps

### 1. Better Auth Setup (Frontend)
```typescript
import { betterAuth } from "better-auth";
import { jwt } from "better-auth/plugins";

export const auth = betterAuth({
  database: {
    provider: "postgres",
    url: process.env.DATABASE_URL,
  },
  emailAndPassword: {
    enabled: true,
  },
  plugins: [
    jwt({
      algorithm: "RS256",
      expiresIn: "7d",
      issuer: process.env.ISSUER_URL,
    }),
  ],
});
```

### 2. JWKS Endpoint (Frontend)
```typescript
export async function GET() {
  const { db } = await import("@/lib/db");
  const { jwks } = await import("@/drizzle/schema");

  const keys = await db.select().from(jwks);

  const jwksResponse = {
    keys: keys.map((key) => {
      const publicKey = JSON.parse(key.publicKey);
      return {
        ...publicKey,
        kid: key.id,
      };
    }),
  };

  return new Response(JSON.stringify(jwksResponse), {
    status: 200,
    headers: {
      "Content-Type": "application/json",
      "Cache-Control": "public, max-age=3600",
    },
  });
}
```

### 3. FastAPI JWT Verification
```python
from jwt import PyJWKClient
import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

def get_jwk_client():
    jwks_url = f"{settings.better_auth_url}/.well-known/jwks.json"
    return PyJWKClient(jwks_url)

def verify_jwt_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        jwk_client = get_jwk_client()
        signing_key = jwk_client.get_signing_key_from_jwt(token)

        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            options={"verify_aud": False}
        )

        user_id = payload.get("sub") or payload.get("user_id")
        if not user_id:
            raise ValueError("Invalid token: missing user_id")

        return {"user_id": user_id, "email": payload.get("email", "")}
    except jwt.exceptions.PyJWTError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")
```
