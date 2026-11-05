---
name: auth
description: Setup authentication flow (register, login, session/JWT, middleware)
type: scaffold
project_types: [web-app, api]
trigger: "setup auth, add authentication, create login"
inputs:
  - name: strategy
    description: Auth strategy (jwt, session, oauth, all)
    required: false
    default: "jwt"
  - name: providers
    description: OAuth providers if strategy=oauth (google, github, etc.)
    required: false
    default: ""
---

## Context

Project {{project_name}} uses {{stack}}.
Setup authentication with strategy: {{input.strategy}}.

Read AGENTS.md for security conventions.

## Instructions

1. **Analyze existing auth setup**
   - Check if auth middleware / auth routes already exist
   - Check already installed dependencies (bcrypt, jsonwebtoken, passport, next-auth, etc.)
   - Identify existing user model/schema

2. **Setup dependencies**
   Adjust based on strategy:
   - JWT: bcrypt/argon2, jsonwebtoken/jose
   - Session: express-session, connect-redis (optional)
   - OAuth: next-auth / passport + passport-google-oauth20, etc.

3. **Create/update user model**
   - Fields: id, email, password_hash, name, created_at, updated_at
   - If OAuth: add provider, provider_id fields
   - Migration if needed (use migration skill)

4. **Create auth service**
   - Register: validate input, hash password, create user, return token
   - Login: find user, verify password, return token
   - Verify: validate token, return user
   - Refresh: refresh expired token (if JWT)

5. **Create auth routes**
   - POST /api/auth/register
   - POST /api/auth/login
   - POST /api/auth/logout
   - GET /api/auth/me (current user)
   - POST /api/auth/refresh (if JWT)

6. **Create auth middleware**
   - Extract token from header/cookie
   - Verify token
   - Attach user to request
   - Return 401 if invalid

7. **Create tests**
   - Register: success, duplicate email, weak password
   - Login: success, wrong password, user not found
   - Protected route: with token, without token, expired token
   - Middleware: valid token, invalid token, no token

## Script

```bash
#!/bin/bash
# Install auth dependencies based on strategy
STRATEGY="{{input.strategy}}"

if [ "$STRATEGY" = "jwt" ]; then
  echo "Dependencies needed: bcryptjs jsonwebtoken"
elif [ "$STRATEGY" = "session" ]; then
  echo "Dependencies needed: bcryptjs express-session"
elif [ "$STRATEGY" = "oauth" ]; then
  echo "Dependencies needed: next-auth (or passport)"
fi
```

## Validation

- [ ] User model/schema created with proper fields
- [ ] Password hashing works (not stored as plaintext)
- [ ] Register endpoint works (happy path + errors)
- [ ] Login endpoint works (happy path + errors)
- [ ] Auth middleware protects routes correctly
- [ ] Token validation works
- [ ] Tests passing (minimum 8 test cases)
- [ ] No security vulnerabilities (no secret in code, proper CORS, etc)
- [ ] Typecheck passing
