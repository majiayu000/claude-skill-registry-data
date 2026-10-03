---
name: ui-case-studies
description: >
  Case studies for common product screens — defaults, required content, and
  anti-patterns. Use when designing or reviewing Settings, Profile, Auth,
  Billing, Pricing, Onboarding, Team, Tables, Checkout, Help, Chat, Calendar,
  Upload, Wizard, Audit, Permissions, Kanban, Search, 404, Inbox, Integrations,
  Empty, Dashboard, Error, Confirm, Invite, or when asking what content belongs
  on a page by default.
---

# UI case studies

Short inventories of **what a screen usually ships with** and **what content belongs there**. Grounded in common SaaS/product UI guidance (linked inside each case). Use before mockup/implement (`frontend-mockup-first`, `hallmark`).

Load the matching file under [cases/](cases/):

### Account & access
| Screen | File |
|--------|------|
| Settings | [cases/settings.md](cases/settings.md) |
| Profile / account | [cases/profile.md](cases/profile.md) |
| Sign-in / sign-up | [cases/auth.md](cases/auth.md) |
| Team / members | [cases/team-members.md](cases/team-members.md) |
| Invite accept | [cases/invite-accept.md](cases/invite-accept.md) |
| Roles & permissions | [cases/permissions.md](cases/permissions.md) |

### Money & growth
| Screen | File |
|--------|------|
| Billing & plan (in-app) | [cases/billing.md](cases/billing.md) |
| Pricing page (marketing) | [cases/pricing.md](cases/pricing.md) |
| Checkout / payment | [cases/checkout.md](cases/checkout.md) |
| Onboarding / setup | [cases/onboarding.md](cases/onboarding.md) |

### Communication & system
| Screen | File |
|--------|------|
| Notification preferences | [cases/notifications.md](cases/notifications.md) |
| Notifications inbox / feed | [cases/notifications-inbox.md](cases/notifications-inbox.md) |
| Chat / messaging | [cases/chat-messaging.md](cases/chat-messaging.md) |
| Help center / docs | [cases/help-center.md](cases/help-center.md) |
| Integrations | [cases/integrations.md](cases/integrations.md) |
| Audit log | [cases/audit-log.md](cases/audit-log.md) |

### Data & workflows
| Screen | File |
|--------|------|
| App dashboard / home | [cases/dashboard.md](cases/dashboard.md) |
| Data table / list | [cases/data-table.md](cases/data-table.md) |
| List → detail | [cases/list-detail.md](cases/list-detail.md) |
| Kanban / board | [cases/kanban.md](cases/kanban.md) |
| Calendar / scheduling | [cases/calendar.md](cases/calendar.md) |
| File upload / import | [cases/file-upload.md](cases/file-upload.md) |
| Form wizard / stepper | [cases/form-wizard.md](cases/form-wizard.md) |
| Global search (cmd-K) | [cases/global-search.md](cases/global-search.md) |
| Search & filter results | [cases/search-results.md](cases/search-results.md) |

### States & chrome
| Screen | File |
|--------|------|
| Empty / first-run | [cases/empty-state.md](cases/empty-state.md) |
| 404 / not found | [cases/not-found.md](cases/not-found.md) |
| Error / failed load | [cases/error-state.md](cases/error-state.md) |
| Confirm / destructive dialog | [cases/confirm-dialog.md](cases/confirm-dialog.md) |

## How to use

1. Identify the screen type (or closest match).
2. Read that case study (and its source links if you need depth).
3. Adapt labels to this product; drop sections that don’t apply (YAGNI).
4. Keep the existing app palette (`frontend-mockup-first`).
5. Run `hallmark` for visual structure — these cases cover **content**, not look.

Do not copy filler copy into the UI unless the user asked for placeholder text.
