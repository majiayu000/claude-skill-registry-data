---
name: authentication
description: Implement secure authentication with JWT, sessions, OAuth, and password hashing. Use when adding login/logout, token auth, or integrating OAuth providers.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Authentication Skill

Implement secure authentication patterns for web applications including JWT tokens, sessions, OAuth, and password handling.

---

## When to Use

- Adding login/logout functionality
- Implementing token-based authentication
- Integrating OAuth providers
- Handling password hashing and reset
- Managing sessions and cookies

---

## JWT Authentication

### Token Generation

```javascript
import jwt from 'jsonwebtoken';
import { config } from '../config/index.js';

/**
 * Generate JWT access token
 * @param {object} payload - Token payload (user data)
 * @returns {string} - Signed JWT token
 */
export function generateAccessToken(payload) {
  return jwt.sign(payload, config.jwt.secret, {
    expiresIn: config.jwt.accessExpiresIn || '15m',
    issuer: config.jwt.issuer
  });
}

/**
 * Generate refresh token (longer-lived)
 * @param {object} payload - Token payload
 * @returns {string} - Signed refresh token
 */
export function generateRefreshToken(payload) {
  return jwt.sign(
    { sub: payload.sub, type: 'refresh' },
    config.jwt.refreshSecret,
    { expiresIn: config.jwt.refreshExpiresIn || '7d' }
  );
}

/**
 * Verify JWT token
 * @param {string} token - JWT token
 * @returns {object} - Decoded payload
 * @throws {Error} - If invalid/expired
 */
export function verifyToken(token) {
  return jwt.verify(token, config.jwt.secret, {
    issuer: config.jwt.issuer
  });
}

/**
 * Verify refresh token
 * @param {string} token - Refresh token
 * @returns {object} - Decoded payload
 */
export function verifyRefreshToken(token) {
  const payload = jwt.verify(token, config.jwt.refreshSecret);
  if (payload.type !== 'refresh') {
    throw new Error('Invalid token type');
  }
  return payload;
}
```

### Auth Middleware

```javascript
import { UnauthorizedError } from '../lib/errors.js';

/**
 * Authentication middleware
 * Validates Bearer token and adds user to request
 */
export function authenticate(req, res, next) {
  const authHeader = req.headers.authorization;

  if (!authHeader?.startsWith('Bearer ')) {
    throw new UnauthorizedError('Missing authorization header');
  }

  const token = authHeader.slice(7);

  try {
    const payload = verifyToken(token);
    req.user = payload;
    next();
  } catch (error) {
    if (error.name === 'TokenExpiredError') {
      throw new UnauthorizedError('Token expired');
    }
    throw new UnauthorizedError('Invalid token');
  }
}

/**
 * Optional authentication
 * Adds user if token present, continues otherwise
 */
export function optionalAuth(req, res, next) {
  const authHeader = req.headers.authorization;

  if (authHeader?.startsWith('Bearer ')) {
    try {
      const token = authHeader.slice(7);
      req.user = verifyToken(token);
    } catch {
      // Invalid token, continue without user
    }
  }

  next();
}

/**
 * Role-based authorization
 * @param  {...string} roles - Allowed roles
 */
export function authorize(...roles) {
  return (req, res, next) => {
    if (!req.user) {
      throw new UnauthorizedError('Not authenticated');
    }

    if (!roles.includes(req.user.role)) {
      throw new ForbiddenError('Insufficient permissions');
    }

    next();
  };
}
```

---

## Password Handling

### Hashing with Argon2

```javascript
import argon2 from 'argon2';

/**
 * Hash password using Argon2id
 * @param {string} password - Plain text password
 * @returns {Promise<string>} - Hashed password
 */
export async function hashPassword(password) {
  return argon2.hash(password, {
    type: argon2.argon2id,
    memoryCost: 65536,      // 64MB
    timeCost: 3,            // 3 iterations
    parallelism: 4          // 4 threads
  });
}

/**
 * Verify password against hash
 * @param {string} hash - Stored hash
 * @param {string} password - Plain text password
 * @returns {Promise<boolean>} - Whether password matches
 */
export async function verifyPassword(hash, password) {
  return argon2.verify(hash, password);
}
```

### Password Validation

```javascript
/**
 * Validate password strength
 * @param {string} password - Password to validate
 * @returns {object} - { valid: boolean, errors: string[] }
 */
export function validatePassword(password) {
  const errors = [];

  if (password.length < 8) {
    errors.push('Password must be at least 8 characters');
  }
  if (password.length > 128) {
    errors.push('Password must be at most 128 characters');
  }
  if (!/[a-z]/.test(password)) {
    errors.push('Password must contain a lowercase letter');
  }
  if (!/[A-Z]/.test(password)) {
    errors.push('Password must contain an uppercase letter');
  }
  if (!/[0-9]/.test(password)) {
    errors.push('Password must contain a number');
  }

  return {
    valid: errors.length === 0,
    errors
  };
}
```

---

## Session Management

### Secure Cookies

```javascript
import { config } from '../config/index.js';

/**
 * Cookie configuration for sessions
 */
export const cookieConfig = {
  httpOnly: true,                    // Not accessible via JavaScript
  secure: config.env === 'production', // HTTPS only in production
  sameSite: 'lax',                   // CSRF protection
  maxAge: 7 * 24 * 60 * 60 * 1000,  // 7 days
  path: '/'
};

/**
 * Set refresh token in HTTP-only cookie
 * @param {Response} res - Express response
 * @param {string} token - Refresh token
 */
export function setRefreshCookie(res, token) {
  res.cookie('refreshToken', token, {
    ...cookieConfig,
    path: '/api/auth/refresh'  // Only sent to refresh endpoint
  });
}

/**
 * Clear refresh token cookie
 * @param {Response} res - Express response
 */
export function clearRefreshCookie(res) {
  res.clearCookie('refreshToken', {
    ...cookieConfig,
    path: '/api/auth/refresh'
  });
}
```

### Session Store

```javascript
/**
 * Simple in-memory session store
 * Use Redis in production
 */
class SessionStore {
  constructor() {
    this.sessions = new Map();
  }

  create(userId, data = {}) {
    const sessionId = crypto.randomUUID();
    const session = {
      id: sessionId,
      userId,
      data,
      createdAt: Date.now(),
      lastAccess: Date.now()
    };
    this.sessions.set(sessionId, session);
    return sessionId;
  }

  get(sessionId) {
    const session = this.sessions.get(sessionId);
    if (session) {
      session.lastAccess = Date.now();
    }
    return session;
  }

  destroy(sessionId) {
    this.sessions.delete(sessionId);
  }

  destroyUserSessions(userId) {
    for (const [id, session] of this.sessions) {
      if (session.userId === userId) {
        this.sessions.delete(id);
      }
    }
  }
}

export const sessions = new SessionStore();
```

---

## CSRF Protection

```javascript
import crypto from 'crypto';

/**
 * Generate CSRF token
 * @returns {string} - Random token
 */
export function generateCsrfToken() {
  return crypto.randomBytes(32).toString('hex');
}

/**
 * CSRF protection middleware
 * For non-GET requests, validates token from header or body
 */
export function csrfProtection(req, res, next) {
  // Skip for GET, HEAD, OPTIONS
  if (['GET', 'HEAD', 'OPTIONS'].includes(req.method)) {
    return next();
  }

  const sessionToken = req.session?.csrfToken;
  const requestToken = req.headers['x-csrf-token'] || req.body?._csrf;

  if (!sessionToken || !requestToken || sessionToken !== requestToken) {
    return res.status(403).json({
      error: {
        code: 'CSRF_ERROR',
        message: 'Invalid CSRF token'
      }
    });
  }

  next();
}
```

---

## OAuth Integration

### OAuth2 Flow

```javascript
/**
 * OAuth2 configuration for providers
 */
const providers = {
  google: {
    authUrl: 'https://accounts.google.com/o/oauth2/v2/auth',
    tokenUrl: 'https://oauth2.googleapis.com/token',
    userInfoUrl: 'https://www.googleapis.com/oauth2/v2/userinfo',
    scopes: ['openid', 'email', 'profile'],
    clientId: process.env.GOOGLE_CLIENT_ID,
    clientSecret: process.env.GOOGLE_CLIENT_SECRET
  },
  github: {
    authUrl: 'https://github.com/login/oauth/authorize',
    tokenUrl: 'https://github.com/login/oauth/access_token',
    userInfoUrl: 'https://api.github.com/user',
    scopes: ['user:email'],
    clientId: process.env.GITHUB_CLIENT_ID,
    clientSecret: process.env.GITHUB_CLIENT_SECRET
  }
};

/**
 * Generate OAuth authorization URL
 * @param {string} provider - Provider name
 * @param {string} state - CSRF state token
 * @returns {string} - Authorization URL
 */
export function getAuthUrl(provider, state) {
  const config = providers[provider];
  if (!config) throw new Error(`Unknown provider: ${provider}`);

  const params = new URLSearchParams({
    client_id: config.clientId,
    redirect_uri: `${process.env.APP_URL}/api/auth/callback/${provider}`,
    response_type: 'code',
    scope: config.scopes.join(' '),
    state
  });

  return `${config.authUrl}?${params}`;
}

/**
 * Exchange code for tokens
 * @param {string} provider - Provider name
 * @param {string} code - Authorization code
 * @returns {Promise<object>} - Token response
 */
export async function exchangeCode(provider, code) {
  const config = providers[provider];

  const response = await fetch(config.tokenUrl, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
      'Accept': 'application/json'
    },
    body: new URLSearchParams({
      client_id: config.clientId,
      client_secret: config.clientSecret,
      code,
      grant_type: 'authorization_code',
      redirect_uri: `${process.env.APP_URL}/api/auth/callback/${provider}`
    })
  });

  return response.json();
}

/**
 * Get user info from provider
 * @param {string} provider - Provider name
 * @param {string} accessToken - Access token
 * @returns {Promise<object>} - User info
 */
export async function getUserInfo(provider, accessToken) {
  const config = providers[provider];

  const response = await fetch(config.userInfoUrl, {
    headers: {
      'Authorization': `Bearer ${accessToken}`
    }
  });

  return response.json();
}
```

---

## Login Rate Limiting

```javascript
/**
 * Rate limiter for login attempts
 * Prevents brute force attacks
 */
class LoginRateLimiter {
  constructor() {
    this.attempts = new Map();
    this.maxAttempts = 5;
    this.windowMs = 15 * 60 * 1000;  // 15 minutes
    this.lockoutMs = 30 * 60 * 1000;  // 30 minutes
  }

  /**
   * Record failed login attempt
   * @param {string} identifier - Email or IP
   * @returns {object} - { allowed: boolean, retryAfter?: number }
   */
  recordFailure(identifier) {
    const now = Date.now();
    let record = this.attempts.get(identifier);

    if (!record || now - record.firstAttempt > this.windowMs) {
      record = { count: 1, firstAttempt: now };
    } else {
      record.count++;
    }

    this.attempts.set(identifier, record);

    if (record.count >= this.maxAttempts) {
      return {
        allowed: false,
        retryAfter: Math.ceil(this.lockoutMs / 1000)
      };
    }

    return { allowed: true };
  }

  /**
   * Check if identifier is rate limited
   * @param {string} identifier - Email or IP
   * @returns {object} - { allowed: boolean, retryAfter?: number }
   */
  check(identifier) {
    const now = Date.now();
    const record = this.attempts.get(identifier);

    if (!record) return { allowed: true };

    // Check if lockout expired
    if (record.count >= this.maxAttempts) {
      const elapsed = now - record.firstAttempt;
      if (elapsed < this.lockoutMs) {
        return {
          allowed: false,
          retryAfter: Math.ceil((this.lockoutMs - elapsed) / 1000)
        };
      }
      // Lockout expired, reset
      this.attempts.delete(identifier);
    }

    return { allowed: true };
  }

  /**
   * Clear attempts on successful login
   * @param {string} identifier - Email or IP
   */
  clearAttempts(identifier) {
    this.attempts.delete(identifier);
  }
}

export const loginLimiter = new LoginRateLimiter();
```

---

## Security Headers

```javascript
/**
 * Security headers middleware
 */
export function securityHeaders(req, res, next) {
  // Prevent clickjacking
  res.setHeader('X-Frame-Options', 'DENY');

  // Prevent MIME type sniffing
  res.setHeader('X-Content-Type-Options', 'nosniff');

  // XSS protection (legacy browsers)
  res.setHeader('X-XSS-Protection', '1; mode=block');

  // Referrer policy
  res.setHeader('Referrer-Policy', 'strict-origin-when-cross-origin');

  // Content Security Policy (customize as needed)
  res.setHeader('Content-Security-Policy', [
    "default-src 'self'",
    "script-src 'self'",
    "style-src 'self' 'unsafe-inline'",
    "img-src 'self' data: https:",
    "font-src 'self'",
    "connect-src 'self' https://api.example.com",
    "frame-ancestors 'none'"
  ].join('; '));

  next();
}
```

---

## Checklist

When implementing authentication:

- [ ] Use Argon2id or bcrypt for password hashing
- [ ] Implement rate limiting on login endpoints
- [ ] Use HTTP-only, Secure, SameSite cookies
- [ ] Store refresh tokens securely (not localStorage)
- [ ] Implement token refresh mechanism
- [ ] Add CSRF protection for session-based auth
- [ ] Validate password strength
- [ ] Log authentication events
- [ ] Implement account lockout
- [ ] Use HTTPS in production
- [ ] Set appropriate security headers
- [ ] Validate OAuth state parameter
- [ ] Never log passwords or tokens

## Related Skills

- **rest-api** - Write REST API endpoints with HTTP methods, status codes,...
- **security** - Write secure web pages and applications
- **database** - Design PostgreSQL schemas with migrations, seeding, and d...
- **nodejs-backend** - Build Node.js backend services with Express/Fastify, Post...
