---
description: Add a new Better Auth plugin or feature and generate the corresponding database migration
---

# Auth Schema Migration

When adding new Better Auth features (social logins, new plugins, etc.), follow this process to update the database schema.

## Steps

1. **Update Better Auth config** — add the plugin to `src/shared/lib/auth/index.ts` (server) and `src/renderer/lib/auth-client.ts` (client, if the plugin has a client component).

2. **Generate the updated Better Auth schema** — create a temporary config file in the project root with a default `auth` export that includes all plugins:

   ```bash
   cat > _ba-gen.ts << 'EOF'
   import { betterAuth } from "better-auth"
   import { admin } from "better-auth/plugins"
   // import your new plugin here
   import { drizzleAdapter } from "better-auth/adapters/drizzle"
   import { drizzle } from "drizzle-orm/better-sqlite3"
   import Database from "better-sqlite3"

   const sqlite = new Database("/tmp/ba-gen-temp.db")
   const db = drizzle(sqlite)

   export const auth = betterAuth({
     baseURL: "http://localhost:3000",
     database: drizzleAdapter(db, { provider: "sqlite" }),
     emailAndPassword: { enabled: true },
     plugins: [admin() /* , newPlugin() */],
   })
   EOF
   echo "y" | npx @better-auth/cli generate --config _ba-gen.ts --output _ba-schema.ts
   ```

3. **Merge changes into `src/shared/lib/db/schema.ts`** — compare `_ba-schema.ts` with existing Better Auth tables. Look for new tables or new columns on `user`, `session`, `account`, `verification`.

   Conventions to follow:
   - Convert array index syntax `(table) => [index(...)]` to object syntax `(table) => ({ name: index(...) })`
   - Skip `relations()` exports (not used in this codebase)
   - Prefix Better Auth exports to avoid naming conflicts: `authSession` (not `session`), `authAccount` (not `account`)
   - Add type exports at the bottom of the file

4. **Update the Drizzle adapter schema mapping** in `src/shared/lib/auth/index.ts` if new tables were added:

   ```typescript
   database: drizzleAdapter(db, {
     provider: 'sqlite',
     schema: {
       user: schema.user,
       session: schema.authSession,
       account: schema.authAccount,
       verification: schema.verification,
       // newTable: schema.newTable,
     },
   }),
   ```

5. **Generate the Drizzle migration**:

   ```bash
   npx drizzle-kit generate
   ```

6. **Clean up** temp files:

   ```bash
   rm _ba-gen.ts _ba-schema.ts /tmp/ba-gen-temp.db
   ```

7. **Verify**:

   ```bash
   npx tsc --noEmit    # typecheck
   npx vitest run       # unit tests
   ```

   The migration auto-applies on next app startup via `migrate()` in `src/shared/lib/db/index.ts`.

## Key files

| File | Purpose |
|------|---------|
| `src/shared/lib/auth/index.ts` | Better Auth instance + plugin config |
| `src/renderer/lib/auth-client.ts` | Better Auth React client + client plugins |
| `src/shared/lib/db/schema.ts` | All Drizzle table definitions (including Better Auth tables) |
| `src/shared/lib/db/index.ts` | DB init + auto-migration on startup |
| `src/shared/lib/db/migrations/` | Generated SQL migration files |
| `drizzle.config.ts` | Drizzle Kit config (points to schema + migrations) |

## Important notes

- Do NOT run `npm build` — use typecheck + lint to verify changes
- Better Auth tables are created by our Drizzle migration (not Better Auth's internal migrator) because we define them in `schema.ts` for type-safe queries
- New `userId` columns on existing tables should be nullable (null in non-auth mode) for backward compatibility
