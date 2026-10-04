---
name: ui-shell-routing
description: Use this skill whenever writing client-side routing, navigation guards, page transition logic, URL structure, scroll position management, filter/search state preservation, or the demo route map in the Myelin platform. This defines the authoritative URL structure, route guards, and the state persistence rules that prevent learners from losing progress when navigating. Load before writing any routing, navigation, or page transition code.
---

This skill defines the UI shell routing contract for the Myelin platform. The URL structure is the contract between the shell and every feature — changing it breaks bookmarks, notifications deep-links, and audit log references. Do not invent new routes without updating this skill.

---

## Authoritative URL Structure

### Public / Auth routes

```
/                         → Marketing / demo landing
/login                    → Authentication (email or SSO)
/register                 → Learner registration
/consent                  → Consent gate (post-auth, pre-training)
/forgot-password          → Password reset request
/reset-password/:token    → Password reset form
/mentor/accept/:token     → Mentor invite acceptance
/verify/:verificationId   → Public result statement verification (unauthenticated)
/demo                     → Demo mode landing (no auth required)
/demo/simulation          → Demo simulation walkthrough
```

### Learner app routes (`/app/*`)

```
/app                      → Dashboard (redirect to /app/dashboard)
/app/dashboard            → Learner home — module progress, notifications
/app/modules              → Module catalogue
/app/modules/:moduleId    → Module detail view
/app/learn/:moduleId/:itemId  → Active learning item (video, quiz, simulation)
/app/simulation/:scenarioId   → Simulation launcher (redirects to active session)
/app/submissions          → Submission history
/app/submissions/new      → New submission creation (post-simulator)
/app/submissions/:id      → Submission detail view
/app/logbook              → Workplace logbook
/app/logbook/new          → New logbook entry
/app/logbook/:entryId     → Logbook entry detail
/app/results              → Result statements
/app/results/:resultId    → Result statement detail + download
/app/profile              → Profile and notification preferences
/app/profile/privacy      → Privacy settings + consent management
```

### Lecturer / Admin routes (`/admin/*`)

```
/admin                    → Admin dashboard (redirect to /admin/dashboard)
/admin/dashboard          → KPI overview, pending actions
/admin/cohorts            → Cohort list
/admin/cohorts/:cohortId  → Cohort detail
/admin/cohorts/:cohortId/learners  → Learner roster
/admin/submissions        → Submission review queue
/admin/submissions/:id    → Submission review interface
/admin/logbook            → Mentor sign-off monitoring
/admin/results            → Result statement management
/admin/results/:resultId  → Result statement detail + amendment
/admin/kpis               → KPI scorecard dashboard
/admin/settings           → Institution settings
/admin/settings/sso       → SSO configuration
/admin/settings/compliance → Compliance policy pack
/admin/audit              → Audit log viewer
/admin/users              → User management
/admin/users/:userId      → User detail
```

### Super Admin routes (`/superadmin/*`)

```
/superadmin/tenants        → Tenant management
/superadmin/tenants/:id    → Tenant detail + feature flags
/superadmin/kpis           → Cross-tenant KPI scorecard
/superadmin/audit          → Cross-tenant audit log
/superadmin/scenarios      → Scenario catalogue management
/superadmin/demo           → Demo session management
```

**Critical fix carried forward from `design-system-tokens` skill:** the post-simulator route is `/app/submissions/new`. The prototype had a broken `assignments` route reference. Any code that navigates after SESSION_COMPLETE must use `/app/submissions/new`.

---

## Route Guards

Every protected route must be guarded before rendering. Guards run in this order:

1. **Authentication guard** — redirect to `/login` if no valid session token
2. **Consent guard** — redirect to `/consent` if consent not current (runs for all `/app/*` routes)
3. **Role guard** — redirect to `/app/dashboard` if authenticated user lacks the required role
4. **Tenant scope guard** — redirect to 403 page if the requested resource belongs to a different tenant

```javascript
const ROUTE_GUARDS = {
  '/app/*':        ['AUTH', 'CONSENT', 'ROLE:STUDENT|LECTURER|ADMIN'],
  '/admin/*':      ['AUTH', 'CONSENT', 'ROLE:LECTURER|ADMIN|SUPER_ADMIN'],
  '/superadmin/*': ['AUTH', 'ROLE:SUPER_ADMIN'],
  '/demo/*':       [],   // no auth required
  '/verify/*':     [],   // no auth required
};

async function runRouteGuards(path, session) {
  const guards = resolveGuards(path);

  for (const guard of guards) {
    if (guard === 'AUTH' && !session?.userId) {
      return { redirect: `/login?next=${encodeURIComponent(path)}` };
    }
    if (guard === 'CONSENT') {
      const consentOk = await checkConsentCurrent(session.userId, session.tenantId);
      if (!consentOk) return { redirect: '/consent' };
    }
    if (guard.startsWith('ROLE:')) {
      const allowedRoles = guard.replace('ROLE:', '').split('|');
      if (!allowedRoles.includes(session.role)) {
        return { redirect: '/app/dashboard' };
      }
    }
  }
  return { proceed: true };
}
```

The `?next=` parameter on login redirects must be preserved and honoured on successful login — learners following a deep-linked notification must land on the target resource, not the dashboard.

---

## Scroll Position and Filter State Preservation

Navigating away from a list view (submissions, cohort roster, audit log) and returning must restore the scroll position and active filter state. This is particularly important for admin review queues — losing position mid-review is a significant UX failure.

```javascript
const scrollStateCache = new Map();
const filterStateCache = new Map();

function saveNavigationState(routeKey, scrollY, filters) {
  scrollStateCache.set(routeKey, scrollY);
  filterStateCache.set(routeKey, { ...filters });
}

function restoreNavigationState(routeKey) {
  return {
    scrollY:  scrollStateCache.get(routeKey) || 0,
    filters:  filterStateCache.get(routeKey) || {}
  };
}
```

State is preserved in-memory (not in `localStorage` or `sessionStorage`). It is cleared on explicit logout. It is not persisted across browser tabs.

Cache only the following routes (others reset on revisit):
- `/admin/submissions`
- `/admin/cohorts/:cohortId/learners`
- `/admin/audit`
- `/app/submissions`
- `/app/logbook`

---

## Page Transition Behaviour

- Route changes trigger a full page content load — no partial DOM updates that leave stale content visible
- A loading indicator must appear within 100ms of navigation if the new page has not resolved within that window
- Navigation during an active simulation session must show a confirmation dialog: "You are in an active simulation — leaving will pause your session. Continue?" — and must not destroy the session state on navigation away

```javascript
function handleSimulationNavGuard(targetPath, sessionState) {
  if (sessionState?.simulation?.active && !targetPath.startsWith('/app/simulation')) {
    return {
      requiresConfirmation: true,
      message: 'You are in an active simulation — leaving will pause your session. Continue?',
      onConfirm: () => { pauseSimulationSession(); navigate(targetPath); },
      onCancel:  () => { /* stay on current route */ }
    };
  }
  return { requiresConfirmation: false };
}
```

Pausing a simulation session suspends the session timer and preserves all step state in memory. Returning to `/app/simulation/:scenarioId` restores the paused session.

---

## Demo Route Map

Demo routes do not require authentication and must never write to live data tables.

```
/demo                     → Auto-scrolling landing with capability walkthrough
/demo/simulation          → 5-waypoint deterministic simulation demo
/demo/dashboard           → Synthetic KPI dashboard view
/demo/results             → Synthetic result statement preview
```

Demo routes set `demoMode: true` in all downstream service calls. The demo simulation route uses the synthetic 5-waypoint dataset from `demo-mode-isolation` skill.

The demo routes must display a persistent banner: **"Demo Mode — Synthetic Data"** in the position defined by the design system tokens skill.

---

## 404 and Error Routes

```
/404       → Not found (for explicit redirects)
/403       → Forbidden (for role/tenant guard failures)
/error     → Generic error (for unhandled exceptions)
```

All three pages must:
- Display the institution logo and Myelin branding
- Provide a "Return to Dashboard" or "Return to Home" link appropriate to the user's auth state
- Log the error event to the audit log as metadata (not as a security event)

---

## What Not To Do

- Do not navigate to `/app/assignments/new` or any `assignments` route — it does not exist; use `/app/submissions/new`
- Do not run consent guard on `/demo/*` or `/verify/*` routes
- Do not destroy simulation session state on navigation away — pause and preserve
- Do not honour `?next=` redirect parameters that point to external domains (open redirect risk)
- Do not use `localStorage` or `sessionStorage` for scroll/filter state — use in-memory cache
- Do not cache scroll/filter state for all routes — only cache the listed routes
- Do not block navigation without surfacing a confirmation dialog to the user
