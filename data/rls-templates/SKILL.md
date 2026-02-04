---
name: rls-templates
description: Row Level Security policy templates for Supabase - multi-tenant patterns, user isolation, role-based access, and secure-by-default configurations. Use when securing Supabase tables, implementing RLS policies, building multi-tenant AI apps, protecting user data, creating chat/RAG systems, or when user mentions row level security, RLS, Supabase security, tenant isolation, or data access policies.
allowed-tools: Bash, Read, Write, Edit
---

# RLS Templates

Production-ready Row Level Security policy templates for Supabase applications, with focus on AI application patterns (multi-tenant chat, RAG systems, user-specific embeddings).

## Instructions

### 1. Applying RLS Policies

**Apply policies to tables:**
```bash
# Apply user isolation policies
bash scripts/apply-rls-policies.sh user-isolation conversations messages

# Apply multi-tenant policies
bash scripts/apply-rls-policies.sh multi-tenant organizations org_members documents

# Apply AI-specific policies
bash scripts/apply-rls-policies.sh ai-chat conversations messages message_embeddings
```

**Generate custom policy:**
```bash
# Generate policy from template
bash scripts/generate-policy.sh user-isolation my_table user_id

# Generate with custom column
bash scripts/generate-policy.sh multi-tenant projects organization_id
```

### 2. Testing RLS Enforcement

**Test policies work correctly:**
```bash
# Test all policies on a table
bash scripts/test-rls-policies.sh conversations

# Test specific user context
bash scripts/test-rls-policies.sh messages --user-id "user-uuid-here"

# Test multi-tenant isolation
bash scripts/test-rls-policies.sh documents --org-id "org-uuid-here"
```

### 3. Auditing Security

**Audit tables for missing RLS:**
```bash
# Audit all tables in public schema
bash scripts/audit-rls.sh

# Audit specific tables
bash scripts/audit-rls.sh conversations messages embeddings

# Generate audit report
bash scripts/audit-rls.sh --report audit-report.md
```

### 4. Policy Pattern Selection

**Choose the right pattern:**

- **user-isolation.sql**: User owns row directly (`user_id` column)
  - Use for: User profiles, settings, personal documents
  - Pattern: `auth.uid() = user_id`

- **multi-tenant.sql**: Organization/team-based isolation
  - Use for: SaaS apps, team workspaces, shared resources
  - Pattern: Check organization membership via join

- **role-based-access.sql**: Different permissions per role
  - Use for: Admin panels, hierarchical access, permission levels
  - Pattern: Check role from `auth.jwt()` claims

- **ai-chat-policies.sql**: Chat/conversation data
  - Use for: AI chat apps, message history, conversation threads
  - Pattern: User owns conversation + participants table

- **embeddings-policies.sql**: Vector/embedding data
  - Use for: RAG systems, semantic search, vector databases
  - Pattern: User owns source document that owns embeddings

## Examples

**Example 1: Secure Chat Application**
```sql
-- Apply chat policies to tables
\i templates/ai-chat-policies.sql

-- Tables: conversations, messages, participants
-- Result: Users only see conversations they participate in
```

**Example 2: Multi-Tenant RAG System**
```sql
-- Apply organization isolation
\i templates/multi-tenant.sql

-- Apply embedding security
\i templates/embeddings-policies.sql

-- Tables: organizations, documents, document_embeddings
-- Result: Each org only sees their own documents and embeddings
```

**Example 3: Role-Based Admin Panel**
```sql
-- Apply role-based policies
\i templates/role-based-access.sql

-- Roles: admin (full access), editor (read/write), viewer (read-only)
-- Result: Different permissions based on user role
```

## Requirements

### Prerequisites
- Supabase project with database access
- PostgreSQL client (`psql`) installed
- Environment variables set:
  - `SUPABASE_DB_URL`: PostgreSQL connection string
  - `SUPABASE_ANON_KEY`: For testing anon access
  - `SUPABASE_SERVICE_KEY`: For admin operations

### Security Checklist
- [ ] RLS enabled on all tables in public schema
- [ ] Policies test both authenticated and anonymous access
- [ ] Indexes created on columns used in policies (user_id, org_id, etc.)
- [ ] Service key never exposed to client applications
- [ ] Policies use `(SELECT auth.uid())` for performance
- [ ] WITH CHECK clause included on INSERT/UPDATE policies
- [ ] Testing validates isolation between users/tenants

### Performance Optimization
- Create indexes: `CREATE INDEX idx_table_user_id ON table(user_id);`
- Wrap auth functions: `(SELECT auth.uid())` instead of `auth.uid()`
- Always filter queries: `.eq('user_id', userId)` in client code
- Use security definer functions for complex authorization logic
- Specify roles in policies: `TO authenticated` to skip anon checks

---

**Best Practices:**
1. Enable RLS before adding any data
2. Test with multiple user contexts
3. Use audit script regularly in CI/CD
4. Document policy decisions in migration files
5. Monitor query performance after adding policies
