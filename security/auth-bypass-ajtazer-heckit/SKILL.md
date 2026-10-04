---
name: auth-bypass
description: "Detect authentication and authorization bypass vulnerabilities including missing auth middleware, JWT algorithm confusion, IDOR, and session fixation."
metadata:
  filePattern:
    - "**/*.js"
    - "**/*.ts"
    - "**/*.py"
    - "**/*.go"
    - "**/*.rb"
  bashPattern:
    - "grep.*(auth|login|session|jwt|token|middleware)"
  priority: 88
---

# Authentication/Authorization Bypass Detection

## When to Use

Audit web frameworks, API gateways, admin panels, CMS systems, and any application with role-based access control.

## Process

### Step 1: Map ALL Routes

```
# Express.js
grep -rn "app\.get\|app\.post\|app\.put\|app\.delete\|app\.patch\|router\." .

# Django
grep -rn "path(\|url(\|urlpatterns" .

# Flask
grep -rn "@app\.route\|@blueprint\.route" .

# Go
grep -rn "HandleFunc\|Handle\|mux\.\|router\." .

# Rails
grep -rn "get \|post \|put \|delete \|patch " config/routes.rb
```

### Step 2: Map Auth Middleware

```
# Express
grep -rn "isAuthenticated\|requireAuth\|authMiddleware\|passport\|jwt\.verify" .
grep -rn "app\.use(.*auth\|router\.use(.*auth" .

# Django
grep -rn "login_required\|permission_required\|@permission_classes\|IsAuthenticated" .

# Flask
grep -rn "login_required\|@jwt_required\|current_user" .

# Go
grep -rn "AuthMiddleware\|RequireAuth\|WithAuth" .

# Rails
grep -rn "before_action.*authenticate\|before_action.*authorize" .
```

### Step 3: Cross-Reference Routes vs Auth

For EACH route, verify:
1. Is auth middleware applied?
2. Is it the RIGHT auth level? (user vs admin)
3. Is it applied to ALL HTTP methods? (GET might be protected but PUT is not)
4. Are there any conditional bypasses?

### Step 4: Check for Common Bypass Patterns

```
# JWT issues
grep -rn "algorithms\|algorithm\|alg\|verify.*false\|verify.*False" .
grep -rn "jwt\.decode\|jwt\.verify\|jose\|jsonwebtoken" .

# Session fixation
grep -rn "session\.regenerate\|session\.destroy" .

# IDOR (missing ownership check)
grep -rn "findById\|findOne\|params\.id\|req\.params" .
```

## Common Vulnerability Patterns

### Missing Auth on Specific Routes
```js
// Protected
app.get('/api/users', authMiddleware, getUsers);
// MISSING AUTH
app.get('/api/users/:id/export', exportUser);  // No middleware!
```

### JWT Algorithm Confusion
```js
// VULNERABLE: accepts algorithm from token header
jwt.verify(token, publicKey);  // If alg=HS256, public key used as HMAC secret

// SAFE: specifies allowed algorithms
jwt.verify(token, publicKey, { algorithms: ['RS256'] });
```

### IDOR (Missing Ownership Check)
```js
app.get('/api/documents/:id', auth, (req, res) => {
  // VULNERABLE: finds document by ID without checking owner
  const doc = await Document.findById(req.params.id);
  res.json(doc);
  
  // SAFE: checks ownership
  const doc = await Document.findOne({ _id: req.params.id, owner: req.user.id });
});
```

## CVSS Guidance

- Complete auth bypass (unauthenticated access to admin): CRITICAL 9.8
- JWT algorithm confusion to forge tokens: CRITICAL 9.1
- IDOR to access other users data: HIGH 7.5-8.1
- Missing auth on non-sensitive endpoint: LOW 3.1
- Session fixation: MEDIUM 5.4

## References

- [Sinks](references/sinks.md) -- Auth patterns by framework
- [False Positive Indicators](references/false-positive-indicators.md)
- [PoC Skeleton](references/poc-skeleton.md)
