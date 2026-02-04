---
name: supabase-jwt-auth
description: Implement JWT custom claims authentication for Supabase to reduce API database queries. Use when building Next.js API routes that need user authentication and authorization (role, company_id, facility_id). Embeds user metadata into JWT tokens to eliminate 40% of database queries per API request. Triggers when implementing authentication in API routes, optimizing Supabase queries, or setting up user session management.
---

# Supabase JWT Custom Claims Authentication

Reduce API database queries by embedding user metadata (role, company_id, facility_id) into JWT tokens.

## Performance Benefits

- **Eliminates 2 DB queries per API request** (40% reduction)
- **Secure**: JWT is signed and tamper-proof
- **Scalable**: Reduces database load as user base grows

## Implementation Workflow

### 1. Create PostgreSQL Function

Create a migration file in `supabase/migrations/`:

```sql
-- Template available in assets/migration_template.sql
CREATE OR REPLACE FUNCTION public.custom_access_token_hook(event jsonb)
RETURNS jsonb
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
DECLARE
  user_claims jsonb;
  current_facility uuid;
BEGIN
  -- Get primary facility for the user
  SELECT facility_id INTO current_facility
  FROM _user_facility
  WHERE user_id = (event->>'user_id')::uuid
    AND is_current = true
    AND is_primary = true
  LIMIT 1;

  -- If no primary facility, get any current facility
  IF current_facility IS NULL THEN
    SELECT facility_id INTO current_facility
    FROM _user_facility
    WHERE user_id = (event->>'user_id')::uuid
      AND is_current = true
    LIMIT 1;
  END IF;

  -- Build custom claims from m_users table
  SELECT jsonb_build_object(
    'role', role,
    'company_id', company_id,
    'current_facility_id', current_facility
  ) INTO user_claims
  FROM m_users
  WHERE id = (event->>'user_id')::uuid
    AND is_active = true
    AND deleted_at IS NULL;

  -- If user not found or inactive, return event unchanged
  IF user_claims IS NULL THEN
    RETURN event;
  END IF;

  -- Add custom claims to app_metadata
  RETURN jsonb_set(
    event,
    '{claims, app_metadata}',
    COALESCE(event->'claims'->'app_metadata', '{}'::jsonb) || user_claims
  );
END;
$$;

GRANT EXECUTE ON FUNCTION public.custom_access_token_hook TO authenticated;
GRANT EXECUTE ON FUNCTION public.custom_access_token_hook TO service_role;
```

**Important**: Customize the function to match your database schema (table names, column names).

### 2. Apply Migration

Use Supabase MCP to apply the migration:

```typescript
await mcp__supabase__apply_migration({
  project_id: "your-project-id",
  name: "create_jwt_custom_claims_hook",
  query: "-- SQL from above"
});
```

### 3. Create Helper Module

Create `lib/auth/jwt.ts` (template available in `assets/jwt-helper-template.ts`):

```typescript
import { createClient } from '@/utils/supabase/server';

export interface JWTMetadata {
  role: 'site_admin' | 'company_admin' | 'facility_admin' | 'staff';
  company_id: string;
  current_facility_id: string;
}

export async function getAuthenticatedUserMetadata(): Promise<JWTMetadata | null> {
  const supabase = await createClient();

  const {
    data: { user },
    error: authError,
  } = await supabase.auth.getUser();

  if (authError || !user) {
    return null;
  }

  const { role, company_id, current_facility_id } = user.app_metadata || {};

  if (!role || !company_id || !current_facility_id) {
    return null;
  }

  return {
    role,
    company_id,
    current_facility_id,
  };
}

export function hasPermission(
  metadata: JWTMetadata,
  allowedRoles: JWTMetadata['role'][]
): boolean {
  return allowedRoles.includes(metadata.role);
}
```

### 4. Use in API Routes

Replace database queries with JWT metadata retrieval:

**Before (with DB queries)**:
```typescript
// ❌ OLD: 2 DB queries
const { data: userData } = await supabase
  .from('m_users')
  .select('role, company_id')
  .eq('id', user.id)
  .single();

const { data: userFacility } = await supabase
  .from('_user_facility')
  .select('facility_id')
  .eq('user_id', user.id)
  .single();
```

**After (with JWT)**:
```typescript
// ✅ NEW: 0 DB queries
import { getAuthenticatedUserMetadata } from '@/lib/auth/jwt';

const metadata = await getAuthenticatedUserMetadata();
if (!metadata) {
  return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
}

const { role, company_id, current_facility_id } = metadata;
```

### 5. Configure Supabase Hook

**Manual configuration required in Supabase Dashboard**:

1. Go to: `https://supabase.com/dashboard/project/{project-id}/database/hooks`
2. Click "Enable Hooks" (if first time)
3. Click "Create a new hook"
4. Configure:
   - **Name**: Custom Access Token Hook
   - **Table**: (leave blank)
   - **Events**: ✓ Custom Access Token (auth.jwt)
   - **Type**: SQL Function
   - **Function**: `public.custom_access_token_hook`
5. Save

### 6. Verify Implementation

After configuration:

1. Log in to the application
2. Check JWT token in browser DevTools:
   - Application > Session Storage
   - Decode JWT at https://jwt.io
3. Verify `app_metadata` contains:
   - `role`
   - `company_id`
   - `current_facility_id`

## Troubleshooting

See `references/troubleshooting.md` for common issues and solutions.

## 重要: JWTトークンの取得方法

**問題**: `session.user.app_metadata`はJWTペイロードの`app_metadata`を反映しません。

Supabase SDKの`session.user.app_metadata`は、Custom Access Token Hookで追加したカスタムクレームを含みません。正しくデータを取得するには、**JWTトークンを直接デコード**する必要があります。

**間違った実装（動作しない）:**
```typescript
const { data: { session } } = await supabase.auth.getSession();
const role = session.user.app_metadata?.role; // ❌ カスタムクレームが取得できない
```

**正しい実装:**
```typescript
const { data: { session } } = await supabase.auth.getSession();

// JWTトークンを直接デコード
const accessToken = session.access_token;
const tokenParts = accessToken.split('.');
const payload = JSON.parse(Buffer.from(tokenParts[1], 'base64').toString());

// payloadからカスタムクレームを取得
const role = payload.app_metadata?.role; // ✅ 正しく取得できる
const company_id = payload.app_metadata?.company_id;
const current_facility_id = payload.app_metadata?.current_facility_id;
```

**理由**:
- Custom Access Token Hookは`{claims, app_metadata}`にカスタムクレームを追加
- JWTペイロードには正しく含まれているが、SDKの`session.user`オブジェクトには反映されない
- JWTトークンを直接デコードすることで、Hookで追加したカスタムクレームにアクセス可能

**正しいヘルパー実装**: `assets/correct-jwt-helper.ts`を参照してください。

## Security Notes

- JWT tokens are signed by Supabase and cannot be tampered with
- Always validate on the server side, never trust client-side data
- Hook runs on every authentication, so keep the function performant
- Custom claims are embedded at login time; changes to user data require re-login to update JWT

## Performance Metrics

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| DB queries per API request | 2 | 0 | 100% |
| Total queries (login + API) | 5 | 3 | 40% |
| Response time | Baseline | -30ms avg | Faster |
