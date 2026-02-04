---
name: tech-details
description: Database schema (users, messages, photos tables), environment variables, ImageKit storage structure, authentication flow, and service integrations. Use when working on database operations, API logic, authentication, or infrastructure.
---

# Tech Details

## Database Schema (Drizzle ORM)

### users (Authentication)
```typescript
id: UUID          // Unique identifier
email: TEXT       // Admin email
password: TEXT    // bcrypt hashed password
createdAt: TIMESTAMPTZ
```

### messages (Guestbook)
```typescript
id: UUID
name: TEXT        // Author name
message: TEXT     // Message content (500 chars max)
status: ENUM      // 'pending' | 'approved' | 'rejected'
createdAt: TIMESTAMPTZ
```

### photos (Gallery)
```typescript
id: UUID
filename: TEXT    // File name in ImageKit
title: TEXT?      // Optional photo title
url: TEXT         // ImageKit CDN URL
fileId: TEXT      // ImageKit file ID (for deletion)
size: INTEGER     // Size in bytes
order: INTEGER    // Position in gallery
category: ENUM    // 'memory' | 'event'
createdAt: TIMESTAMPTZ
```

## ImageKit Storage Structure

```
memories/{uuid}.{ext}  # Memory photos
event/{uuid}.{ext}     # Event photos
```

- Automatic image optimization and CDN delivery
- Blur placeholders via plaiceholder
- Staging prefix: `stg/` (via IMAGEKIT_FOLDER_PREFIX)

## Environment Variables

### Required
```bash
DATABASE_URL          # Neon PostgreSQL connection string
JWT_SECRET            # Min 32 chars for token signing
IMAGEKIT_PRIVATE_KEY  # Server-side uploads/deletions
IMAGEKIT_PUBLIC_KEY   # Client-side (NEXT_PUBLIC_)
IMAGEKIT_URL_ENDPOINT # CDN endpoint (NEXT_PUBLIC_)
```

### Optional
```bash
IMAGEKIT_FOLDER_PREFIX    # Staging prefix (e.g., "stg")
NEXT_PUBLIC_POSTHOG_KEY   # Analytics project key
NEXT_PUBLIC_POSTHOG_HOST  # PostHog host URL
```

### Email (Cron notifications)
```bash
EMAIL_HOST   # SMTP server (e.g., smtp.gmail.com)
EMAIL_PORT   # SMTP port (e.g., 587)
EMAIL_USER   # Sender email
EMAIL_PASS   # App password
EMAIL_TO     # Admin notification recipient
```

## Authentication Flow

1. Admin submits credentials via login form
2. Server action validates with bcrypt
3. JWT token created with jose library
4. Token stored in httpOnly cookie
5. Middleware validates JWT on /admin/* routes
6. Middleware checks user exists in database

## Service Integrations

### PostHog (Analytics & Error Tracking)
- User analytics: section views, form submissions, link clicks
- Error tracking: `apiError`, `mutationError`, `queryError`
- All data hooks use `useErrorTracking` for capture

### ImageKit (Storage & CDN)
- Upload via server-side SDK
- Delete via fileId
- Automatic WebP conversion
- Blur placeholder generation

### Email (Nodemailer)
- Daily digest at 8 PM via Vercel Cron
- Lists pending messages for moderation
- Fallback: GitHub Actions cron

## Authorization Rules

- **messages**: Public read (approved only), admin write
- **photos**: Public read, admin write
- **users**: Admin only (no public access)
