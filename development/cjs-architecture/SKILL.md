---
name: cjs-architecture
description: Understand CJS2026 codebase architecture, state management patterns, and file organization for effective navigation and modification
---

# CJS2026 Architecture Knowledge

## When to Activate

Use this skill when the agent needs to:
- Navigate unfamiliar parts of the CJS2026 codebase
- Understand how components interact with contexts and Firebase
- Make architectural decisions about where to place new code
- Refactor or split large components
- Debug issues spanning multiple layers (UI → Context → Firebase)

## Core Architecture

The CJS2026 project follows a **Vite + React + Firebase** architecture with Airtable as a headless CMS.

### Layer Model

```
┌─────────────────────────────────────────────────┐
│  Pages (src/pages/)                             │
│  Dashboard, Admin, Schedule, Home, Login...     │
├─────────────────────────────────────────────────┤
│  Components (src/components/)                   │
│  SessionCard, MySchedule, Navbar, Footer...     │
├─────────────────────────────────────────────────┤
│  Contexts (src/contexts/)                       │
│  AuthContext (488 lines) - auth + profile +     │
│  schedule features combined                     │
├─────────────────────────────────────────────────┤
│  Content (src/content/)                         │
│  siteContent.js, scheduleData.js,              │
│  organizationsData.js - AUTO-GENERATED         │
├─────────────────────────────────────────────────┤
│  Firebase (functions/index.js)                  │
│  20+ Cloud Functions, Firestore, Storage        │
├─────────────────────────────────────────────────┤
│  Airtable (external)                            │
│  Site Content, Schedule, Organizations tables   │
└─────────────────────────────────────────────────┘
```

### Critical Files by Size

| File | Lines | Responsibility |
|------|-------|----------------|
| `functions/index.js` | 1,988 | All Cloud Functions |
| `Admin.jsx` | 3,129 | 10-tab admin panel |
| `Dashboard.jsx` | 2,067 | User profile, wizard, schedule widget |
| `AuthContext.jsx` | 488 | Auth + profile + schedule (god object) |
| `Home.jsx` | ~500 | Landing page with CMS content |

### State Management Pattern

The project uses React Context with a monolithic pattern:

```javascript
// AuthContext provides EVERYTHING user-related
const {
  currentUser,     // Firebase Auth user
  userProfile,     // Firestore document
  savedSessions,   // Schedule bookmarks
  saveSession,     // Bookmark action
  updateUserProfile, // Profile updates
} = useAuth();
```

**Architectural debt**: AuthContext mixes authentication (25%), profile management (50%), and schedule features (25%). Consider splitting when modifying.

## Key Patterns

### Content Flow (Airtable → Component)

```
Airtable Table → generate-*.cjs → src/content/*.js → import → Component
```

Content files are **auto-generated**. Never edit directly. Use `npm run generate-*` scripts.

### Firebase Auth Flow

```
Login.jsx → AuthContext.loginWithGoogle() → Firebase Auth
         → createUserProfile() → Firestore users/{uid}
         → Dashboard shows profile
```

### Admin Authorization

Dual system (technical debt):
1. Hardcoded `ADMIN_EMAILS` array (bootstrap)
2. Firestore `role: 'admin' | 'super_admin'` field

Check both in Cloud Functions via `isAdmin()` helper.

## File Location Conventions

| Type | Location | Example |
|------|----------|---------|
| Page components | `src/pages/` | `Dashboard.jsx` |
| Reusable components | `src/components/` | `SessionCard.jsx` |
| Context providers | `src/contexts/` | `AuthContext.jsx` |
| Custom hooks | `src/hooks/` | `useBookmarkCounts.js` |
| Utilities | `src/utils/` | `profanityFilter.js` |
| Auto-generated content | `src/content/` | `siteContent.js` |
| Cloud Functions | `functions/` | `index.js` |
| Build scripts | `scripts/` | `generate-content.cjs` |

## Integration Points

This skill works with:
- **cms-content-pipeline** - For Airtable content changes
- **firebase-patterns** - For Cloud Function modifications
- **component-patterns** - For UI component creation

## Guidelines

1. Check if content is CMS-controlled before hardcoding text
2. Use `ensureUserDocumentExists()` before any Firestore merge operation
3. Place new admin features in Admin.jsx tabs, not new pages
4. Use existing animation patterns (Framer Motion with stagger delays)
5. Follow the `card-sketch` class pattern for new cards
