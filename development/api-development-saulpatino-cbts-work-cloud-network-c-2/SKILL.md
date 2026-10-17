---
name: api-development
description: Develop and test the Fastify TypeScript REST API for the FinOps platform
---

# API Development

Use this skill to:
- Start the API server locally
- Create new endpoints
- Test API routes
- Add authentication (Azure AD OIDC)
- Debug API issues

## API Endpoints
The API provides endpoints for:
- `/costs` — Cost data queries and aggregations
- `/focus-costs` — FOCUS-normalized cost data
- `/scopes` — Scope management
- `/unit-economics` — Unit cost calculations
- `/kpis` — KPI definitions and values
- `/rate-optimization` — Commitment analysis
- `/frameworks` — FinOps framework data
- `/assessments` — Maturity assessments
- `/governance` — Policies and workflows
- `/projections` — Cost projections
- `/reports` — Report generation
- `/allocation` — Cost allocation
- `/dimensions` — Custom dimensions
- `/insights` — AI-generated insights

## Common Tasks

### Start API Server
```bash
cd services/api
npm install
npm run dev
```

### Run API Tests
```bash
npm run test:api
npm run test:api:watch
```

### Type Check
```bash
npm run type-check:api
```

### Add New Endpoint
1. Create route file in `services/api/src/routes/`
2. Add type definitions
3. Implement handler with proper error handling
4. Add to route index

### Debug Requests
```bash
DEBUG=fastify:* npm run dev
```
