---
name: web-frontend
description: Develop and test the Vite React TypeScript SPA for the FinOps platform
---

# Web Frontend Development

Use this skill to:
- Start the development server
- Build components and pages
- Test UI functionality
- Manage state and data fetching
- Work with the Aeonik design system

## Application Pages
The Vite React SPA includes:
- **Understand** — Overview, Trends, Spikes, Services, Tags
- **Quantify** — Unit Economics, KPIs
- **Optimize** — PR Projections, Commitments
- **Manage** — Assessments, Governance, Scopes, Settings

## Tech Stack
- React 18+ with TypeScript
- Vite for fast dev/build
- Aeonik design system (teal brand theme)
- Azure AD OIDC authentication
- REST API integration

## Common Tasks

### Start Development Server
```bash
cd services/web
npm install
npm run dev
# Visit http://localhost:5173
```

### Build for Production
```bash
npm run build
npm run preview
```

### Run Web Tests
```bash
npm run test:web
npm run test:web:watch
```

### Type Check
```bash
npm run type-check:web
```

### Add New Page
1. Create page component in `src/pages/`
2. Add route in `src/router.ts`
3. Update navigation if needed
4. Add authentication guards if required

### Debug Authentication
Check browser console for Azure AD token issues and OIDC state.
