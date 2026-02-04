---
name: error-states
description: Error handling patterns for Astro sites. 404/500 pages, form errors, offline states, loading failures. Use for graceful degradation and user experience.
---

# Error States Skill

## Purpose

Provides error handling patterns that maintain trust and guide users when things go wrong. Includes custom error pages, form validation states, loading indicators, offline fallbacks, and network error handling.

## Core Rules

1. **Never blame the user** — "We couldn't find that" not "Invalid request"
2. **Offer next steps** — Always provide a way forward
3. **Keep branding** — Error pages should match site design
4. **Be helpful** — Search, popular links, contact info
5. **Log errors** — Track 404s to fix broken links
6. **Accessible errors** — Use ARIA labels and semantic HTML
7. **Loading feedback** — Show spinners for async operations
8. **Network awareness** — Handle offline states gracefully
9. **User-friendly messages** — Translate HTTP codes to plain language
10. **Prevent error loops** — Fail silently in error handlers

## References

See the `references/` directory for detailed implementations:

- **[error-pages.md](references/error-pages.md)** — Custom 404 and 500 error pages with tracking
- **[form-errors.md](references/form-errors.md)** — Inline field errors and error summary components
- **[loading-states.md](references/loading-states.md)** — Loading spinners and offline fallback page
- **[empty-states.md](references/empty-states.md)** — Empty state component with icons and actions
- **[network-handling.md](references/network-handling.md)** — Safe fetch utility, toast notifications, error logging

## Forbidden

- Technical jargon in error messages
- Blaming users for errors
- Generic "Something went wrong" with no next steps
- Error pages without navigation
- Silent failures (no feedback)
- Ignoring 404 tracking

## Definition of Done

- [ ] Custom 404 page with search and links
- [ ] Custom 500 page with recovery options
- [ ] Form validation with inline errors
- [ ] Loading states for async operations
- [ ] Offline fallback page
- [ ] Empty states for lists/search
- [ ] Toast notifications for actions
- [ ] Error logging in production
- [ ] All error pages match site branding
