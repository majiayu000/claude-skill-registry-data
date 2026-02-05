---
name: Create Backend Service
description: Use this skill when adding new backend functionality (API endpoints + business logic).
---

# Create Backend Service

Use this skill to follow the **route (controller) + service** split used in `server/src/`.

## Steps

1) Create the service module

- Location: `server/src/services/{serviceName}.js`
- Use `template_service.js` from this folder.
- Prefer small exported functions (keep them easy to test).

2) Create the route module

- Location: `server/src/routes/{routeName}.js`
- Use `template_route.js` from this folder.
- Validate inputs near the route (or use `server/src/contracts/httpSchemas.js` when applicable).

3) Mount the route

- Register it in `server/src/index.js`:
  - `app.use('/api/your-scope', yourRouter);`

## Naming notes

- Prefer existing naming patterns:
  - Routes: `dataRoutes.js`, `runRoutes.js`, `indicatorExecutionRoutes.js`
  - Services: `marketWindowService.js`, `leanService.js`, `runStore.js`

