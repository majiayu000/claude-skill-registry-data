---
name: nextjs
description: Next.js App Router skill covering RSC, Server Actions, data fetching, routing, and deployment. Use when building Next.js applications.
---

## nextjs

App Router is the default. Layouts nest via file system. loading/error/not-found files are boundary catches.

### Core Concepts
- App Router: file-based routing in app/, layouts persist state across navigations
- RSC vs Client: Server Components by default, "use client" for browser APIs and hooks
- Server Actions: async functions in RSC, callable from forms, skip writing API routes
- Data fetching: fetch() with next.revalidate for ISR, route segment config for SSR/SSG

### Routing Patterns
- Layouts: layout.tsx wraps child pages, persists UI and state across navigations
- Route groups: (name) folders group routes without affecting URL path
- Parallel routes: @slot convention renders independent views per route simultaneously
- Intercepting routes: (..) pattern for modals that open from any parent segment

### Best Practices
- Default to Server Components, add "use client" only for interactivity
- colocate data fetching in the component that needs it, no getServerSideProps
- Use ISR with revalidate over full SSR for content that changes infrequently
- Protect routes in middleware.ts before they reach the page component

### Common Code Patterns
- Parallel data fetching with Promise.all in Server Components
- Server Action with revalidatePath and redirect post-mutation
