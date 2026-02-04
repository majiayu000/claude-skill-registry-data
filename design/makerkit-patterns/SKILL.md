---
name: MakerKit Patterns
description: >
  This skill should be used when the user asks about "MakerKit patterns", "CLAUDE.md files",
  "what MCP tools are available", "how does MakerKit structure", "personal vs team accounts",
  "RLS patterns in MakerKit", or needs quick reference for MakerKit conventions.
version: 1.0.0
---

# MakerKit Patterns Reference

Quick reference for MakerKit project patterns and conventions.

## CLAUDE.md File Index

MakerKit includes CLAUDE.md files with patterns for each package:

| File | Purpose | Key Content |
|------|---------|-------------|
| `CLAUDE.md` (root) | Project overview | Commands, technologies, architecture |
| `apps/web/CLAUDE.md` | Web app patterns | Routes, async params, data fetching |
| `apps/web/supabase/CLAUDE.md` | Database patterns | Schema workflow, migrations, RLS |
| `packages/features/CLAUDE.md` | Feature patterns | Personal vs Team accounts |
| `packages/supabase/CLAUDE.md` | Supabase helpers | RLS functions, triggers |
| `packages/ui/CLAUDE.md` | UI components | Available components, form patterns |
| `packages/next/CLAUDE.md` | Next.js patterns | enhanceAction, enhanceRouteHandler |

For detailed content, read `references/claude-md-index.md`.

## Account Types

### Personal Account
- User owns their data directly
- FK: `user_id → auth.users.id`
- RLS: `auth.uid() = user_id`
- Use when: Single-user features, personal settings

### Team Account
- Data belongs to account, shared by members
- FK: `account_id → accounts.id`
- RLS: `has_role_on_account(account_id)` - verifica membresía en cuenta
- Use when: Collaborative features, shared resources

## Essential MCP Tools

### Database Analysis
```
get_database_summary()     → All tables, enums, functions
get_table_info(table)      → Schema details
get_all_enums()            → Existing enum types
```

### Feature Analysis
```
find_complete_features()          → Reference features
analyze_feature_pattern(feature)  → Implementation pattern
```

### Route Analysis
```
get_app_routes()           → Route structure
get_server_actions()       → Action patterns
```

### RLS Generation
```
generate_rls_policy({table, access_type, pattern})
validate_rls_policies({table})
```

For complete MCP reference, read `references/mcp-tools.md`.

## Quick Patterns

### Server Action
```typescript
export const myAction = enhanceAction(
  async (data, { user }) => {
    const client = getSupabaseServerClient();
    // ... operation
    return { success: true, data: result };
  },
  { schema: MySchema }
);
```

### Page Loader
```typescript
import 'server-only';

export async function loadPageData(
  client: SupabaseClient<Database>,
  accountId: string,
) {
  const { data, error } = await client
    .from('table')
    .select('*')
    .eq('account_id', accountId);

  if (error) throw error;
  return data ?? [];
}
```

### RLS Policy Order
```sql
-- 1. Enable RLS
ALTER TABLE public.my_table ENABLE ROW LEVEL SECURITY;

-- 2. Revoke defaults
REVOKE ALL ON public.my_table FROM authenticated, service_role;

-- 3. Grant specific
GRANT SELECT, INSERT, UPDATE, DELETE ON public.my_table TO authenticated;

-- 4. Create policies
CREATE POLICY my_table_select ON public.my_table
  FOR SELECT TO authenticated
  USING (public.has_role_on_account(account_id));
```

## Official Documentation (makerkit-docs)

Para patrones conceptuales que el MCP no cubre, usa el skill `makerkit-docs`:

| Usar MCP cuando... | Usar makerkit-docs cuando... |
|--------------------|------------------------------|
| Necesitas estructura actual del codigo | Necesitas entender conceptos |
| Que tablas/enums existen | Como funciona billing/auth conceptualmente |
| Patrones de codigo real | Documentacion oficial de configuracion |
| Introspeccion del proyecto | Troubleshooting, guias paso a paso |

**Como invocar:** "Usa el skill makerkit-docs para consultar [tema]"

**Secciones mas utiles:**
- `/development/database-architecture` - Arquitectura DB
- `/billing/overview` - Sistema de billing
- `/security/row-level-security` - RLS patterns
- `/troubleshooting/*` - Resolucion de problemas

## Additional Resources

### Reference Files
- **`references/makerkit-consolidado.md`** - Quick reference con templates copy-paste ready (PREFERIDO)
- **`references/claude-md-index.md`** - Complete CLAUDE.md file contents
- **`references/mcp-tools.md`** - All MCP tools with examples

### When to Load References
- Need templates for Ralph → read `makerkit-consolidado.md` (PRIMERO)
- Need specific CLAUDE.md content → read `claude-md-index.md`
- Need MCP tool details → read `mcp-tools.md`
- Quick pattern check → use this SKILL.md
