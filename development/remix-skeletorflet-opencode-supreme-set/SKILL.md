---
name: remix
description: Remix web standards framework skill covering nested routes, loaders, actions, forms, and progressive enhancement. Use when building Remix applications.
---

## remix

Built on Web Fetch API (Request/Response, Headers). No abstractions over platform primitives.

### Core Concepts
- Nested routes: file-based layouts with <Outlet>, each route is its own layout layer
- Loaders: server data loading, runs before render, returns via useLoaderData
- Actions: server mutations triggered by <Form> POST, returns via useActionData
- Progressive enhancement: <Form> works without JS, enhances with JS enabled

### Routing & Data
- loader/action functions export from route files, run only on server
- useFetcher loads data imperatively from any component without navigation
- Resource routes: return non-HTML responses like API JSON or file downloads
- ErrorBoundary per route catches render errors without breaking the app

### Best Practices
- Use <Form> over raw <form> for pending UI and progressive enhancement
- Load data in loaders, not in useEffect or client-side fetchers
- Serialize session state in loaders, read cookies from request headers
- Resource routes for endpoints consumed by external clients

### Common Code Patterns
- Form action with redirect on success, return validation errors on failure
- Loader reads session cookie, fetches user data, returns combined response
