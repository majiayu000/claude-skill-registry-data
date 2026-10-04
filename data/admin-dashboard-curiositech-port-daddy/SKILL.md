---
license: Apache-2.0
name: admin-dashboard
description: Extend and modify the admin dashboard, developer portal, and operations console. Use when adding new admin tabs, metrics, monitoring features, or internal tools. Activates for dashboard development, analytics, user management, and internal tooling.
allowed-tools: Read,Write,Edit,Bash(npm:*,npx:*)
category: Frontend & UI
tags:
  - dashboard
  - admin
  - internal-tools
---

# Admin & Developer Suite Development

This skill helps you extend the admin dashboard and build internal tools following the established patterns.

## DECISION POINTS

### When to Add Tab vs Modify Endpoint vs Create New Tool

```
Adding New Admin Functionality:
├─ User needs read-only data view?
│  ├─ Data exists in current API? → Modify existing tab
│  ├─ New data type needed? → Add new tab + new endpoint
│  └─ Complex analytics required? → Create dedicated analytics tab
│
├─ User needs to modify system data?
│  ├─ Simple CRUD operations? → Add management tab
│  ├─ Bulk operations needed? → Create operations console tab
│  └─ Multi-step workflow? → Build wizard component
│
├─ Internal developer tooling?
│  ├─ Code inspection/docs? → Add to /dev portal
│  ├─ System monitoring? → Add to /ops console
│  └─ User support tools? → Add to admin dashboard
│
└─ External user functionality?
   → STOP: Use frontend-development skill instead
```

### Tab Content Implementation Strategy

```
Tab Complexity Assessment:
├─ Simple stats display (< 5 metrics)?
│  → Use StatCard grid pattern
│
├─ Data table with filtering?
│  ├─ < 1000 rows? → Client-side filtering
│  └─ > 1000 rows? → Server-side pagination + search
│
├─ Real-time monitoring?
│  ├─ Updates every 30s+? → Use SWR with refresh interval
│  └─ Updates every 5s-? → Use WebSocket connection
│
└─ Interactive controls?
   ├─ Simple toggles/buttons? → Inline actions
   └─ Complex forms? → Modal dialogs + confirmation flows
```

## FAILURE MODES

### 1. Database Query Performance Death Spiral
**Symptom:** Admin dashboard times out or loads slowly (>5 seconds)
**Detection:** Monitor /api/admin/* response times >3s
**Fix:** Add database indexes, implement pagination, cache aggregated stats
```sql
-- BAD: Full table scan
SELECT COUNT(*) FROM pageViews WHERE userId = ?

-- GOOD: Use indexed timestamp ranges
SELECT COUNT(*) FROM pageViews WHERE createdAt > NOW() - INTERVAL 24 HOUR
```

### 2. Stale Cache Showing Wrong Data
**Symptom:** Admin sees outdated metrics that don't match recent activity
**Detection:** User reports stats don't change after known actions
**Fix:** Implement cache invalidation on data mutations, add "Last Updated" timestamps
```typescript
// Add cache busting to mutations
await updateUserData(userId);
await revalidateTag('admin-stats'); // Clear cache
```

### 3. Missing Audit Logging
**Symptom:** Admin actions aren't logged in auditLog table
**Detection:** Check auditLog entries for admin actions in past 24h
**Fix:** Add logAdminAction() calls to ALL admin endpoints
```typescript
// Required in every admin endpoint
await logAdminAction(admin.id, AuditAction.USER_DATA_VIEW, 'users', userId);
```

### 4. HIPAA Violation Data Exposure
**Symptom:** PHI visible in error messages, logs, or aggregated views
**Detection:** Error contains user email/phone/medical data
**Fix:** Sanitize all error responses, use hashed identifiers in admin views
```typescript
// BAD: Exposes user email
{ error: "User john@email.com not found" }

// GOOD: Uses anonymous identifiers
{ error: "User ID hash_123abc not found" }
```

### 5. Admin Privilege Escalation
**Symptom:** Regular users can access admin endpoints
**Detection:** Non-admin user receives admin data instead of 403
**Fix:** Add requireAdmin() check as first line of every admin endpoint
```typescript
export async function GET(request: Request) {
  const admin = await requireAdmin(); // Must be FIRST
  if (!admin) return Response.json({ error: 'Forbidden' }, { status: 403 });
  // ... rest of handler
}
```

## WORKED EXAMPLES

### Adding Production Health Monitoring Tab

**Scenario:** Add real-time API health monitoring with latency metrics, error rates, and service status.

**1. Decision Point Navigation:**
- User needs real-time monitoring → Use SWR with 30s refresh
- System data, not user data → Add to admin dashboard
- New data type (API metrics) → Create new tab + endpoint

**2. Implementation Steps:**

Create endpoint with required patterns:
```typescript
// src/app/api/admin/health/route.ts
export async function GET(request: Request) {
  const admin = await requireAdmin(); // Security first
  if (!admin) return Response.json({ error: 'Forbidden' }, { status: 403 });
  
  const rateLimitResult = await rateLimiter.check(admin.id); // Rate limiting
  if (!rateLimitResult.allowed) return Response.json({}, { status: 429 });
  
  await logAdminAction(admin.id, 'HEALTH_VIEW', 'metrics', null); // Audit
  
  const metrics = await getHealthMetrics(); // Data fetch
  return Response.json(metrics);
}
```

Create tab component:
```typescript
function ProductionHealthTab() {
  const { data: health, error } = useSWR('/api/admin/health', fetcher, {
    refreshInterval: 30000 // Real-time updates
  });
  
  return (
    <div className="space-y-6">
      <div className="grid grid-cols-4 gap-4">
        <StatCard label="API Uptime" value="99.9%" status="good" />
        <StatCard label="Avg Latency" value="45ms" trend="down" />
        <StatCard label="Error Rate" value="0.1%" status="warning" />
        <StatCard label="Active Services" value="12/12" status="good" />
      </div>
    </div>
  );
}
```

**3. Expert vs Novice Differences:**
- **Novice misses:** Audit logging, rate limiting, HIPAA-safe error handling
- **Expert catches:** Cache invalidation strategy, performance monitoring setup, proper error boundaries

## QUALITY GATES

- [ ] Admin access control: requireAdmin() check passes with admin user, fails with regular user
- [ ] Rate limiting: Endpoint returns 429 when rate limit exceeded (60 req/min default)
- [ ] Audit logging: Admin action logged to auditLog table with correct action type
- [ ] Performance baseline: Tab loads in <2 seconds with realistic data volume
- [ ] HIPAA compliance: No PHI exposed in error messages or debug output
- [ ] Data validation: Invalid requests return proper 400 errors with safe messages
- [ ] Cache behavior: Data updates within 30 seconds of backend changes
- [ ] Error boundaries: UI gracefully handles API failures without crashing
- [ ] Mobile responsive: Tab layout works on tablet-sized screens (768px+)
- [ ] Real-time updates: Auto-refresh works without memory leaks over 10+ minutes

## NOT-FOR BOUNDARIES

**Do NOT use this skill for:**

- **External user-facing features** → Use `frontend-development` instead
- **Authentication/login flows** → Use `auth-security` instead  
- **Database schema changes** → Use `database-operations` instead
- **Email/notification systems** → Use `communications` instead
- **API rate limiting configuration** → Use `backend-api` instead
- **HIPAA compliance setup** → Use `security-compliance` instead
- **Performance optimization** → Use `optimization` instead

**Delegate to other skills when:**
- Adding public user features → `frontend-development`
- Modifying user authentication → `auth-security`
- Creating new API endpoints for external use → `backend-api`
- Setting up monitoring infrastructure → `devops-infrastructure`