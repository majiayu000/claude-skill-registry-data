---
name: dashboard-mail
description: V1.0 - Expert guidance for the Dashboard Mail module supporting Outlook, Gmail, and custom IMAP providers.
---

# Dashboard Mail Module

## ALWAYS: Log This Interaction

After completing work using this skill, append to `History/{YYYY-MM-DD}.md`:

```markdown
## {HH:MM} - {Action Taken}
{One-line summary of what was done}
```

Mail integration module for aggregating multiple email accounts into a unified dashboard widget and page.

## Architecture

```
src/modules/mail/
├── actions.ts              # Server actions (CRUD for accounts)
├── types.ts                # TypeScript types and utilities
├── index.ts                # Module exports
├── components/
│   ├── mail-widget.tsx     # Dashboard widget (compact)
│   ├── mail-list.tsx       # Message list view
│   ├── mail-item.tsx       # Individual message row
│   ├── account-tabs.tsx    # Account switcher tabs
│   ├── account-card.tsx    # Account display card
│   └── bulk-action-bar.tsx # Bulk action toolbar
└── lib/
    ├── outlook-client.ts   # Microsoft Graph API client
    ├── gmail-client.ts     # Gmail API client (placeholder)
    ├── imap-client.ts      # Custom IMAP client (placeholder)
    ├── token-manager.ts    # Encrypted credential storage
    ├── cache.ts            # Redis caching layer
    └── rate-limiter.ts     # API rate limiting

src/app/mail/
├── page.tsx                # Full mail page
└── settings/
    └── page.tsx            # Account management UI
```

## Database Schema

### Tables

**`mail_account_settings`** - Per-user account configurations
| Column | Type | Description |
|--------|------|-------------|
| id | uuid | Primary key |
| user_id | uuid | FK to auth.users |
| provider | text | `outlook`, `gmail`, or `imap` |
| account_name | text | Display name (e.g., "Work Gmail") |
| email_address | text | Account email |
| is_enabled | boolean | Active flag |
| sync_frequency_minutes | integer | Polling interval (min 1) |

**`mail_oauth_tokens`** - Encrypted credentials (AES-256-GCM)
| Column | Type | Description |
|--------|------|-------------|
| account_id | uuid | FK to mail_account_settings |
| encrypted_access_token | text | Encrypted OAuth/IMAP password |
| encrypted_refresh_token | text | OAuth refresh token (nullable) |
| iv | text | Initialization vector |
| auth_tag | text | GCM authentication tag |
| token_expires_at | timestamptz | Token expiry (OAuth only) |

### Known Schema Gap

**IMAP needs additional columns** for custom server settings:
- `imap_host` (text) - Server hostname
- `imap_port` (integer) - Server port (default 993)

Currently IMAP falls back to env vars `IMAP_HOST`, `IMAP_PORT` which is a placeholder workaround.

## Providers

| Provider | Status | Auth Method | API |
|----------|--------|-------------|-----|
| Outlook | Implemented | OAuth 2.0 | Microsoft Graph |
| Gmail | Placeholder | OAuth 2.0 | Gmail API |
| IMAP | Placeholder | Password | IMAP protocol |

### Outlook OAuth Setup

Required env vars:
```
GRAPH_CLIENT_ID=
GRAPH_CLIENT_SECRET=
GRAPH_REDIRECT_URI=
```

### Gmail OAuth Setup

Required env vars:
```
GMAIL_CLIENT_ID=
GMAIL_CLIENT_SECRET=
GMAIL_REDIRECT_URI=
```

### IMAP Setup (Placeholder)

Current env vars (temporary until DB columns added):
```
IMAP_HOST=
IMAP_USER=
IMAP_PASS=
IMAP_PORT=993
```

## Key Types

```typescript
type MailProvider = "outlook" | "gmail" | "imap";

interface MailAccount {
  id: string;
  provider: MailProvider;
  accountName: string;
  emailAddress: string;
  isEnabled: boolean;
  syncFrequencyMinutes: number;
}

interface MailMessage {
  id: string;
  subject: string;
  from: MailAddress;
  receivedAt: Date;
  isRead: boolean;
  preview: string;
}

type BulkActionType = "markRead" | "markUnread" | "moveToJunk" | "delete";
```

## Server Actions

| Action | Description |
|--------|-------------|
| `getMailAccounts()` | List user's configured accounts |
| `createMailAccount(input)` | Add new account |
| `updateMailAccount(id, input)` | Modify account settings |
| `deleteMailAccount(id)` | Remove account and tokens |
| `getMailSummary()` | Aggregated unread counts |
| `getMailMessages(accountId)` | Fetch messages for account |
| `performBulkAction(request)` | Execute bulk operations |

## Caching

Redis caching via Upstash with keys:
- `mail:summary:{userId}` - Account summaries
- `mail:messages:{accountId}:{folder}` - Message lists
- `mail:account:{accountId}` - Account details

## Security

- Tokens encrypted with AES-256-GCM using `MAIL_ENCRYPTION_KEY`
- Each token has unique IV and auth tag
- RLS policies restrict access to owner's data only
- Refresh tokens stored separately with own IV/auth tag

## Settings UI

Located at `/mail/settings`:
- Add account: Select provider → Enter name/email → OAuth or credential flow
- Toggle accounts on/off
- Delete accounts with confirmation dialog
- Provider dropdown: Gmail, Outlook, IMAP (Custom)

## TODO

1. Add `imap_host` and `imap_port` columns to `mail_account_settings`
2. Update settings form to collect IMAP server details when provider is "imap"
3. Implement Gmail client
4. Implement IMAP client using `imap` npm package
5. Add OAuth callback routes for Gmail
