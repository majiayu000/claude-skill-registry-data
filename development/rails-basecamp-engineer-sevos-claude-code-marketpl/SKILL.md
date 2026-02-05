---
name: rails-basecamp-engineer
description: This skill provides expert guidance on implementing Ruby on Rails applications using 37signals (Basecamp/HEY) patterns and conventions. Use when building Rails features, implementing authentication, authorization, multi-tenancy, background jobs, or Hotwire/Turbo/Stimulus following 37signals patterns.
---

# Rails Basecamp Engineer

## Overview

This skill provides comprehensive guidance for building Ruby on Rails applications using 37signals/Basecamp coding patterns. These patterns emphasize composition over inheritance, concern-based organization, minimal controllers, rich domain models, and native Rails capabilities over external gems.

## Core Principles

1. **Composition over inheritance** - Heavy use of concerns to compose behavior
2. **Feature-driven organization** - Group code by domain feature, not by layer
3. **Minimal controllers** - Push business logic to models and concerns
4. **Rich domain models** - Models are the heart of the application
5. **Native Rails first** - Prefer Rails features over external gems
6. **Explicit over implicit** - Clear, readable code over clever shortcuts
7. **Transaction safety** - Wrap critical operations in transactions
8. **Event tracking** - Record significant actions for audit trails

## Working with Existing Applications

When working on an existing Rails application, detect which patterns are in use before loading reference files. If the current context doesn't reveal the approach, use an Explore agent to investigate.

### Frontend/CSS Detection

**Check for these indicators:**
- `tailwind.config.js` or `@tailwind` directives → Load `frontend/daisyui.md`
- `app/assets/stylesheets/_global.css` with `@layer` → Load `frontend/vanilla-css.md`
- DaisyUI classes (`btn`, `card`, `modal`) in views → Load `frontend/daisyui.md`
- OKLCH colors or CSS custom properties → Load `frontend/vanilla-css.md`

**Explore if unknown:** Search for `tailwind.config.js`, `@layer`, or CSS file structure.

### Multi-Tenancy Detection

**Check for these indicators:**
- `Current.account` or `account_id` scoping → Load `multi-tenancy/shared-database.md`
- `activerecord-tenanted` gem or `Tenanted` module → Load `multi-tenancy/database-per-tenant.md`
- URL path like `/account-slug/...` → Load `multi-tenancy/shared-database.md`
- Subdomain routing (`tenant.app.com`) → Load `multi-tenancy/database-per-tenant.md`
- No tenant scoping found → Load `multi-tenancy/index.md` for decision guide

**Explore if unknown:** Search for `Current.account`, `tenant`, `account_id` in models/controllers.

### Authentication Detection

**Check for these indicators:**
- `MagicLink` model or `magic_link` routes → Load `authentication/magic-link.md`
- `has_secure_password` or `password_digest` → Load `authentication/password.md`
- Both present → Load both files

**Explore if unknown:** Search for `MagicLink`, `has_secure_password`, or session controllers.

### Stimulus Controller Detection

**When implementing frontend interactivity:**
1. First check if similar controllers exist in `app/javascript/controllers/`
2. If no existing pattern, load `stimulus/index.md` for decision table
3. Load specific controller file based on need

**Explore if unknown:** List files in `app/javascript/controllers/` to see existing patterns.

## Reference Files

Load the appropriate reference when implementing specific patterns or domains:

### Core Patterns
- `references/models.md` - Model patterns, concerns, associations, callbacks, scopes
- `references/controllers.md` - Controller patterns, concerns, filters, response handling
- `references/current-attributes.md` - CurrentAttributes pattern for request-scoped context
- `references/routing.md` - CRUD-everything routing philosophy, polymorphic URLs
- `references/poros.md` - Plain Old Ruby Objects patterns
- `references/view-helpers.md` - Stimulus-integrated view helpers

### Domain-Specific Patterns
- `references/authentication.md` - Authentication overview and shared architecture
  - `authentication/magic-link.md` - Passwordless magic link (primary 37signals pattern)
  - `authentication/password.md` - Traditional password authentication
- `references/authorization.md` - Role-based and resource-level access control
- `references/multi-tenancy/index.md` - Multi-tenancy decision guide
  - `multi-tenancy/shared-database.md` - Shared DB with tenant_id filtering (Fizzy/Basecamp)
  - `multi-tenancy/database-per-tenant.md` - Separate DB per tenant

### Frontend & Hotwire
- `references/hotwire.md` - Turbo Frames, Turbo Streams overview
- `references/confirmation-dialogs.md` - Native dialog confirmations with Turbo integration
- `references/stimulus/index.md` - Stimulus controller decision table
  - `stimulus/utility-controllers.md` - copy-to-clipboard, hotkey, toggle-class, beacon
  - `stimulus/form-controllers.md` - auto-submit, autoresize, local-save
  - `stimulus/ui-controllers.md` - dialog, lightbox, navigable-list, local-time
  - `stimulus/interaction-controllers.md` - drag-and-drop, sortable, resize
- `references/frontend/index.md` - CSS approach decision guide
  - `frontend/vanilla-css.md` - 37signals CSS (layers, OKLCH, design tokens)
  - `frontend/daisyui.md` - DaisyUI/TailwindCSS (uses Context7 for live docs)

### Infrastructure
- `references/background-jobs.md` - Solid Queue configuration, recurring jobs, account context
- `references/caching.md` - HTTP caching (ETags), fragment caching, touch invalidation
- `references/configuration.md` - ENV patterns, multi-database, Solid Stack setup
- `references/mailers.md` - Minimal mailer patterns, bundled notifications

### Other
- `references/event-tracking.md` - Audit trails, activity feeds, notifications, webhooks
- `references/testing.md` - Testing philosophy, fixtures, system tests, and helpers

## Quick Decision Guide

| Task | Reference File |
|------|----------------|
| Setting up a new model with concerns | `models.md` |
| Validations, associations, callbacks | `models.md` |
| Creating controllers and concerns | `controllers.md` |
| Strong parameters, response formats | `controllers.md` |
| Request-scoped context (Current.user, etc.) | `current-attributes.md` |
| Routing with CRUD-everything | `routing.md` |
| Adding user login/logout | Detect existing method → `authentication/*.md` |
| Implementing permissions/roles | `authorization.md` |
| Multi-account/tenant support | Detect existing approach → `multi-tenancy/*.md` |
| Real-time UI updates (Turbo) | `hotwire.md` |
| Confirmation dialogs for destructive actions | `confirmation-dialogs.md` |
| Stimulus controllers | `stimulus/index.md` (decision table) |
| CSS styling | Detect existing approach → `frontend/*.md` |
| Background processing | `background-jobs.md` |
| HTTP caching, ETags | `caching.md` |
| Sending emails | `mailers.md` |
| Activity feeds, audit trails | `event-tracking.md` |
| Writing tests | `testing.md` |
| View helpers with Stimulus | `view-helpers.md` |
| Business logic objects | `poros.md` |
| ENV configuration | `configuration.md` |
