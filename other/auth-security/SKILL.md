---
name: Auth Security Patterns
description: >-
  Auto-enforce authentication security best practices. Activates when
  implementing password policies, rate limiting, session security, CSRF
  protection, or security headers in auth flows.
version: 1.0.0
---

# Auth Security Patterns

This skill enforces authentication security best practices for Better Auth implementations.

## Password Security

### Strong Password Policy
```typescript
import { betterAuth } from 'better-auth'

export const auth = betterAuth({
  emailAndPassword: {
    enabled: true,
    password: {
      minLength: 12,
      maxLength: 128,
      requireLowercase: true,
      requireUppercase: true,
      requireNumber: true,
      requireSpecialChar: true,
      // Custom validation
      validate: (password) => {
        // Check against common passwords
        if (commonPasswords.includes(password.toLowerCase())) {
          return 'Password is too common'
        }
        // Check for repeated characters
        if (/(.)\1{2,}/.test(password)) {
          return 'Password cannot have 3+ repeated characters'
        }
        return true
      },
    },
  },
})
```

### Password Hashing
```typescript
// Better Auth uses bcrypt by default with cost factor 10
// For higher security requirements:
export const auth = betterAuth({
  advanced: {
    password: {
      hash: async (password) => {
        const salt = await bcrypt.genSalt(12) // Higher cost
        return bcrypt.hash(password, salt)
      },
      verify: async (password, hash) => {
        return bcrypt.compare(password, hash)
      },
    },
  },
})
```

## Rate Limiting

### Global Rate Limiting
```typescript
import { rateLimit } from 'better-auth/plugins/rate-limit'

export const auth = betterAuth({
  plugins: [
    rateLimit({
      window: 60,  // 1 minute window
      max: 100,    // 100 requests per window
      keyGenerator: (req) => {
        // Rate limit by IP
        return req.headers.get('x-forwarded-for') || req.ip
      },
    }),
  ],
})
```

### Endpoint-Specific Limits
```typescript
rateLimit({
  endpoints: {
    // Strict limits for auth endpoints
    'sign-in': {
      window: 300,  // 5 minutes
      max: 5,       // 5 attempts
    },
    'sign-up': {
      window: 3600, // 1 hour
      max: 3,       // 3 registrations
    },
    'reset-password': {
      window: 3600, // 1 hour
      max: 3,       // 3 reset requests
    },
    'verify-email': {
      window: 60,   // 1 minute
      max: 5,       // 5 verification attempts
    },
  },
})
```

### Progressive Delays
```typescript
rateLimit({
  endpoints: {
    'sign-in': {
      window: 300,
      max: 5,
      // Add delay after failed attempts
      onRateLimitExceeded: async (req, res) => {
        const attempts = await getFailedAttempts(req.ip)
        const delay = Math.min(attempts * 1000, 30000) // Max 30s
        await new Promise(resolve => setTimeout(resolve, delay))
      },
    },
  },
})
```

## Session Security

### Secure Session Configuration
```typescript
export const auth = betterAuth({
  session: {
    expiresIn: 60 * 60 * 24 * 7,  // 7 days max
    updateAge: 60 * 60 * 24,      // Extend daily on activity

    // Cookie settings
    cookie: {
      name: '__session',
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
      sameSite: 'lax',
      path: '/',
      domain: process.env.COOKIE_DOMAIN,
    },

    // Session cache (reduce DB lookups)
    cookieCache: {
      enabled: true,
      maxAge: 60 * 5, // 5 minute cache
    },

    // Require fresh session for sensitive ops
    freshAge: 60 * 10, // 10 minutes
  },
})
```

### Session Invalidation
```typescript
import { signOut, useSession } from '@/auth/client'

// Sign out from current device
await signOut()

// Sign out from all devices
await signOut({ revokeAllSessions: true })

// Server-side: Invalidate specific session
await auth.api.invalidateSession({ sessionId })

// Server-side: Invalidate all user sessions
await auth.api.invalidateUserSessions({ userId })
```

### Session Binding
```typescript
// Bind session to device fingerprint
export const auth = betterAuth({
  session: {
    // Store device info
    onSessionCreated: async (session, user, request) => {
      await prisma.session.update({
        where: { id: session.id },
        data: {
          userAgent: request.headers.get('user-agent'),
          ipAddress: request.ip,
        },
      })
    },
    // Validate on each request
    onSessionValidate: async (session, request) => {
      const storedIp = session.ipAddress
      const currentIp = request.ip

      // Warn on IP change (but don't block for mobile users)
      if (storedIp !== currentIp) {
        await logSecurityEvent('session_ip_change', {
          sessionId: session.id,
          oldIp: storedIp,
          newIp: currentIp,
        })
      }

      return true
    },
  },
})
```

## CSRF Protection

### Token-Based CSRF
```typescript
export const auth = betterAuth({
  csrf: {
    enabled: true,
    // Double submit cookie pattern
    cookieName: '__csrf',
    headerName: 'x-csrf-token',
    // Token rotation
    rotateOnAuthentication: true,
  },
})

// Client: Include CSRF token
const csrfToken = getCookie('__csrf')
await fetch('/api/auth/sign-out', {
  method: 'POST',
  headers: {
    'x-csrf-token': csrfToken,
  },
})
```

### SameSite Cookie Protection
```typescript
session: {
  cookie: {
    sameSite: 'strict', // Strictest CSRF protection
    // Or 'lax' for balance between security and usability
  },
}
```

## Security Headers

### Recommended Headers
```typescript
// Middleware or server config
const securityHeaders = {
  'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
  'X-Content-Type-Options': 'nosniff',
  'X-Frame-Options': 'DENY',
  'X-XSS-Protection': '1; mode=block',
  'Referrer-Policy': 'strict-origin-when-cross-origin',
  'Content-Security-Policy': [
    "default-src 'self'",
    "script-src 'self'",
    "style-src 'self' 'unsafe-inline'",
    "img-src 'self' data: https:",
    "font-src 'self'",
    "connect-src 'self'",
    "frame-ancestors 'none'",
  ].join('; '),
}
```

## Account Security

### Account Lockout
```typescript
export const auth = betterAuth({
  emailAndPassword: {
    lockout: {
      enabled: true,
      maxAttempts: 5,
      lockoutDuration: 15 * 60, // 15 minutes
      // Notify user
      onLockout: async (user) => {
        await sendEmail({
          to: user.email,
          subject: 'Account Locked',
          html: 'Your account has been locked due to multiple failed login attempts.',
        })
      },
    },
  },
})
```

### Email Verification
```typescript
export const auth = betterAuth({
  emailAndPassword: {
    requireEmailVerification: true,
    verificationTokenExpiry: 60 * 60 * 24, // 24 hours
    sendVerificationEmail: async (user, token, url) => {
      await sendEmail({
        to: user.email,
        subject: 'Verify your email',
        html: `<a href="${url}">Verify email</a>`,
      })
    },
  },
})
```

### Password Reset Security
```typescript
export const auth = betterAuth({
  emailAndPassword: {
    resetPasswordTokenExpiry: 60 * 60, // 1 hour
    sendResetPasswordToken: async (user, token, url) => {
      await sendEmail({
        to: user.email,
        subject: 'Reset your password',
        html: `<a href="${url}">Reset password</a>`,
      })

      // Log for security audit
      await logSecurityEvent('password_reset_requested', {
        userId: user.id,
        email: user.email,
      })
    },
    onPasswordReset: async (user) => {
      // Invalidate all existing sessions
      await auth.api.invalidateUserSessions({ userId: user.id })

      // Notify user
      await sendEmail({
        to: user.email,
        subject: 'Password changed',
        html: 'Your password was recently changed.',
      })
    },
  },
})
```

## Security Logging

### Audit Trail
```typescript
export const auth = betterAuth({
  advanced: {
    hooks: {
      onSignIn: async (user, session) => {
        await logSecurityEvent('sign_in', {
          userId: user.id,
          sessionId: session.id,
          method: session.method, // 'email', 'google', etc.
        })
      },
      onSignOut: async (user, session) => {
        await logSecurityEvent('sign_out', {
          userId: user.id,
          sessionId: session.id,
        })
      },
      onSignUp: async (user) => {
        await logSecurityEvent('sign_up', {
          userId: user.id,
          email: user.email,
        })
      },
    },
  },
})

async function logSecurityEvent(event: string, data: Record<string, any>) {
  await prisma.securityLog.create({
    data: {
      event,
      data,
      timestamp: new Date(),
      ip: data.ip,
      userAgent: data.userAgent,
    },
  })
}
```

## Security Checklist

- [ ] Password minimum 12 characters with complexity
- [ ] Rate limiting on all auth endpoints
- [ ] Session cookies are httpOnly and secure
- [ ] CSRF protection enabled
- [ ] Email verification required
- [ ] Account lockout after failed attempts
- [ ] Security headers configured
- [ ] Password changes invalidate sessions
- [ ] Security events logged
- [ ] 2FA available for users

## Anti-Patterns

```typescript
// ❌ WRONG: Weak password policy
password: { minLength: 6 }

// ✅ CORRECT: Strong policy
password: { minLength: 12, requireUppercase: true, ... }

// ❌ WRONG: No rate limiting
emailAndPassword: { enabled: true }

// ✅ CORRECT: With rate limiting
plugins: [rateLimit({ ... })]

// ❌ WRONG: Long-lived sessions
session: { expiresIn: 60 * 60 * 24 * 365 } // 1 year

// ✅ CORRECT: Reasonable expiry
session: { expiresIn: 60 * 60 * 24 * 7 } // 7 days

// ❌ WRONG: Cookies without flags
cookie: { name: 'session' }

// ✅ CORRECT: Secure cookie flags
cookie: { httpOnly: true, secure: true, sameSite: 'lax' }
```
