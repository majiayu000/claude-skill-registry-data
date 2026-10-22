---
name: xyon-web
description: Work on the XyonWork web portal and Node backend (React 19 + TypeScript + Vite, Express, Prisma/PostgreSQL, web-push). Use for reports/CSV/PDF downloads, API endpoints, auth, fichajes, schedules, notifications and deployments.
---

# XyonWork web + backend

Employee management platform: React SPA in the repository root and an Express +
Prisma API under `backend/`. Production runs self-hosted with Docker/Coolify.

## Non-negotiable rules

1. **Quality before speed.** Understand the flow end to end; verify with TypeScript and a
   production build before proposing a commit.
2. **Never push without the user reviewing the diff first.**
3. **Never commit secrets** (`.env`, SMTP keys, VAPID private key, JWT secret, database URL).
4. **Authorize every query.** Employees only see their own data; managers their department;
   admins everything. Reuse the existing middleware (`isAdmin`, `isManagerOrAdmin`,
   `sameDepartmentOrAdmin`, `validateManagerDepartment`).
5. **Escape/neutralize user content** in CSV (`csvCell` in `fichajeController.js`) and render
   user text through React (never raw HTML).
6. UI copy is Spanish; code identifiers are English except API fields that mirror the DB.

## Commands

```bash
npm install
npx tsc --noEmit
npm run build
cd backend && npm install && npm start
```

Frontend env: `VITE_API_URL` (default `/api`). Backend uses `.env`/Coolify variables
(`DATABASE_URL`, `JWT_SECRET`, SMTP, VAPID keys…). Migrations are applied automatically by
`backend/prisma/runMigrations.js` at container start; add idempotent `NNN_name.sql` files.

## Architecture map

- `App.tsx` — routes and role guards.
- `pages/` — employee, manager and admin screens. Admin pages are lazy-loaded.
- `components/` — shared UI (modal, signature, tables, layout).
- `context/AuthContext.tsx` — session + web-push subscription lifecycle.
- `services/api.ts` — axios client and service objects (`fichajeService`, `adminService`…).
- `utils/fileUtils.ts` — authenticated file opening (`/api/files/...`).
- `utils/attendanceReport.ts` — client-side monthly PDF (jsPDF + autotable).
- `backend/src/routes.js` — API surface. Add the controller and the route together.
- `backend/src/controllers/` — HTTP layer; `services/` for shared logic.
- `backend/prisma/schema.prisma` + `migrations/` — data model.
- `public/push-sw.js` — web-push service worker.

## Reports and downloads

- **Admin → Fichajes → Exportar**: downloads the department monthly attendance CSV from
  `GET /api/fichajes/report?department=&month=&year=` (blob) via
  `fichajeService.getAttendanceReport`.
- **Calendar → Informe**: employee monthly PDF with signature. The logo load must never
  hang the button; `loadLogo()` has an error/timeout fallback.
- **Nóminas / justificantes**: use `openProtectedFile`, which normalizes legacy
  `/uploads/...` URLs to authenticated `/api/files/...`.
- `GET /api/fichajes/report` is role-aware: employee = own, manager = own department,
  admin = anyone. Keep it that way.

## Backend conventions

- `async/await` + `try/catch` per controller, Spanish error messages.
- Validate inputs; never interpolate SQL (Prisma only).
- Notifications go through `notifyUser` / `createNotification` (in-app + email + web push).
- Schedule resolution lives in `services/smartScheduleService.js`,
  `services/shiftAssignmentService.js` and `services/scheduleOverrideService.js`.
- The existing `sendShiftReminderEmails` job runs every 5 minutes in `server.js`;
  the native app uses its own local schedule plan.

## Security notes

- Bearer JWT in `Authorization`; never put tokens in URLs.
- File routes check ownership; keep the `/api/files/:type/:name` restrictions.
- Rate limits exist for auth and password reset; do not bypass them.
- CSV export neutralizes formula injection.

## Documentation

- `AGENTS.md` — project rules and quick context.
- `docs/AGENT_CHANGELOG.md` — session changelog and decisions.
