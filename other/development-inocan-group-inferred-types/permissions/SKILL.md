---
name: permissions
description: Multi-tenant permission checking for Wasp applications. Use when implementing authorization, access control, or role-based permissions. Includes organization/department/role patterns and permission helper functions.
triggers:
  [
    "permission",
    "authorization",
    "access control",
    "role",
    "MANAGER",
    "MEMBER",
    "VIEWER",
    "canAccess",
    "canEdit",
    "multi-tenant",
    "department",
    "organization",
  ]
version: 1.0
last_updated: 2025-10-18
allowed_tools: [Read, Write, Edit]
---

# Permissions Skill

## Quick Reference

**When to use this skill:**

- Implementing permission checks in operations
- Setting up role-based access control
- Working with multi-tenant data (organizations/departments)
- Checking organization or department access
- Filtering data by user permissions
- Enforcing hierarchical access (parent/child departments)

**Key patterns:**

- `canAccessDocument()` - Check if user can view document
- `canEditDocument()` - Check if user can edit document
- `canDeleteDocument()` - Check if user can delete document
- `getUserOrgRole()` - Get user's role in organization
- `getUserRoleInDepartment()` - Get user's role in department
- `isDepartmentManager()` - Check if user manages department
- `isOrgAdmin()` - Check if user is org owner/admin

## Multi-Tenancy Architecture

**Structure:**

```
Organization (many) → Departments (hierarchical tree via parentId)
                          ↓
                    Users ↔ Departments (many-to-many via UserDepartment)
                          ↓
                    DepartmentRole: MANAGER | MEMBER | VIEWER
                    OrganizationRole: OWNER | ADMIN | MEMBER
```

**Key concepts:**

- Organizations contain multiple departments
- Departments can have parent/child relationships (hierarchical)
- Users belong to departments via UserDepartment junction table
- Each user has a role per department (MANAGER, MEMBER, or VIEWER)
- Users can have roles in multiple departments
- Organization-level roles (OWNER, ADMIN) grant access to all departments

## Database Schema

```prisma
model Organization {
  id          String       @id @default(uuid())
  name        String
  departments Department[]
  members     OrganizationMember[]
}

model OrganizationMember {
  id             String       @id @default(uuid())
  userId         String
  user           User         @relation(fields: [userId], references: [id])
  organizationId String
  organization   Organization @relation(fields: [organizationId], references: [id])
  role           OrganizationRole

  @@unique([userId, organizationId])
}

enum OrganizationRole {
  OWNER
  ADMIN
  MEMBER
}

model Department {
  id              String           @id @default(uuid())
  name            String
  organizationId  String
  organization    Organization     @relation(fields: [organizationId], references: [id])
  parentId        String?
  parent          Department?      @relation("DepartmentHierarchy", fields: [parentId], references: [id])
  children        Department[]     @relation("DepartmentHierarchy")
  userDepartments UserDepartment[]
}

model UserDepartment {
  id           String         @id @default(uuid())
  userId       String
  user         User           @relation(fields: [userId], references: [id])
  departmentId String
  department   Department     @relation(fields: [departmentId], references: [id])
  role         DepartmentRole

  @@unique([userId, departmentId])
}

enum DepartmentRole {
  MANAGER
  MEMBER
  VIEWER
}
```

## Core Permission Helpers

### Organization-Level Permissions

```typescript
import { HttpError } from "wasp/server";

/**
 * Get user's role in organization
 * @returns 'OWNER' | 'ADMIN' | 'MEMBER' | 'NONE'
 */
async function getUserOrgRole(
  userId: string,
  organizationId: string,
  context,
): Promise<string> {
  const membership = await context.entities.OrganizationMember.findUnique({
    where: {
      userId_organizationId: {
        userId,
        organizationId,
      },
    },
  });

  return membership?.role || "NONE";
}

/**
 * Check if user is organization owner or admin
 */
async function isOrgAdmin(
  userId: string,
  organizationId: string,
  context,
): Promise<boolean> {
  const role = await getUserOrgRole(userId, organizationId, context);
  return ["OWNER", "ADMIN"].includes(role);
}

/**
 * Check if user can access organization
 */
async function canAccessOrganization(
  userId: string,
  organizationId: string,
  context,
): Promise<boolean> {
  const role = await getUserOrgRole(userId, organizationId, context);
  return role !== "NONE";
}
```

### Department-Level Permissions

```typescript
/**
 * Get user's role in specific department
 * @returns 'MANAGER' | 'MEMBER' | 'VIEWER' | null
 */
async function getUserRoleInDepartment(
  userId: string,
  departmentId: string,
  context,
): Promise<string | null> {
  const membership = await context.entities.UserDepartment.findUnique({
    where: {
      userId_departmentId: {
        userId,
        departmentId,
      },
    },
  });

  return membership?.role || null;
}

/**
 * Check if user is department manager
 */
async function isDepartmentManager(
  userId: string,
  departmentId: string,
  context,
): Promise<boolean> {
  const role = await getUserRoleInDepartment(userId, departmentId, context);
  return role === "MANAGER";
}

/**
 * Check if user can access department
 * Includes hierarchical access (parent departments)
 */
async function canAccessDepartment(
  userId: string,
  departmentId: string,
  context,
): Promise<boolean> {
  // Get department with parent chain
  const department = await context.entities.Department.findUnique({
    where: { id: departmentId },
    include: { parent: true },
  });

  if (!department) return false;

  // Check organization access
  const hasOrgAccess = await canAccessOrganization(
    userId,
    department.organizationId,
    context,
  );
  if (!hasOrgAccess) return false;

  // Org admins can access all departments
  const isAdmin = await isOrgAdmin(userId, department.organizationId, context);
  if (isAdmin) return true;

  // Check direct membership
  const role = await getUserRoleInDepartment(userId, departmentId, context);
  if (role) return true;

  // Check parent department membership (hierarchical)
  if (department.parentId) {
    return await canAccessDepartment(userId, department.parentId, context);
  }

  return false;
}
```

### Resource-Level Permissions (A3 Example)

```typescript
/**
 * Check if user can access document
 * Access granted if:
 * - User is the author
 * - User is org OWNER/ADMIN
 * - User is in department (any role: MANAGER, MEMBER, VIEWER)
 */
async function canAccessDocument(
  userId: string,
  a3: Document,
  context,
): Promise<boolean> {
  // 1. Author can always access
  if (a3.authorId === userId) return true;

  // 2. Org admins can access
  const orgRole = await getUserOrgRole(userId, a3.organizationId, context);
  if (["OWNER", "ADMIN"].includes(orgRole)) return true;

  // 3. Department members can access (any role)
  const deptRole = await getUserRoleInDepartment(
    userId,
    a3.departmentId,
    context,
  );
  return deptRole !== null;
}

/**
 * Check if user can edit document
 * Edit permissions:
 * - Author can edit
 * - Org OWNER/ADMIN can edit
 * - Department MANAGER can edit
 * - Department MEMBER can edit their own
 * - VIEWER cannot edit
 */
async function canEditDocument(
  userId: string,
  a3: Document,
  context,
): Promise<boolean> {
  // Author can always edit
  if (a3.authorId === userId) return true;

  // Org admins can edit
  const orgRole = await getUserOrgRole(userId, a3.organizationId, context);
  if (["OWNER", "ADMIN"].includes(orgRole)) return true;

  // Department managers can edit
  const deptRole = await getUserRoleInDepartment(
    userId,
    a3.departmentId,
    context,
  );
  if (deptRole === "MANAGER") return true;

  // Members cannot edit others' A3s
  // Viewers cannot edit
  return false;
}

/**
 * Check if user can delete document
 * Delete permissions:
 * - Author can delete
 * - Org OWNER/ADMIN can delete
 * - Department MANAGER can delete
 */
async function canDeleteDocument(
  userId: string,
  a3: Document,
  context,
): Promise<boolean> {
  // Author can delete
  if (a3.authorId === userId) return true;

  // Org admins can delete
  const orgRole = await getUserOrgRole(userId, a3.organizationId, context);
  if (["OWNER", "ADMIN"].includes(orgRole)) return true;

  // Department managers can delete
  const deptRole = await getUserRoleInDepartment(
    userId,
    a3.departmentId,
    context,
  );
  if (deptRole === "MANAGER") return true;

  return false;
}
```

## Usage in Operations

### Standard Operation Pattern

**ALWAYS follow this order:**

1. Auth check (401)
2. Fetch resource
3. Existence check (404)
4. Permission check (403)
5. Validation (400)
6. Perform operation

### Query with Permission Check

```typescript
import type { GetDocument } from "wasp/server/operations";
import type { Document } from "wasp/entities";
import { HttpError } from "wasp/server";

export const getDocument: GetDocument<{ id: string }, Document> = async (
  args,
  context,
) => {
  // 1. Auth check
  if (!context.user) throw new HttpError(401);

  // 2. Fetch resource
  const a3 = await context.entities.Document.findUnique({
    where: { id: args.id },
    include: {
      author: { select: { id: true, username: true } },
      department: true,
      organization: true,
    },
  });

  // 3. Existence check
  if (!a3) throw new HttpError(404, "document not found");

  // 4. Permission check using helper
  const hasAccess = await canAccessDocument(context.user.id, a3, context);
  if (!hasAccess) {
    throw new HttpError(403, "Not authorized to access this document");
  }

  // 5. Return resource
  return a3;
};
```

### Query with Permission Filtering

```typescript
import type { GetDocuments } from "wasp/server/operations";
import type { Document } from "wasp/entities";

export const getDocuments: GetDocuments<void, Document[]> = async (
  args,
  context,
) => {
  if (!context.user) throw new HttpError(401);

  // Get all departments user has access to
  const userDepts = await context.entities.UserDepartment.findMany({
    where: { userId: context.user.id },
  });

  const deptIds = userDepts.map((ud) => ud.departmentId);

  // Return A3s from accessible departments
  return context.entities.Document.findMany({
    where: {
      OR: [
        // Own documents
        { authorId: context.user.id },
        // Department documents
        { departmentId: { in: deptIds } },
      ],
    },
    include: {
      department: true,
      author: { select: { id: true, username: true } },
    },
    orderBy: { createdAt: "desc" },
  });
};
```

### Action with Edit Permission Check

```typescript
import type { UpdateA3 } from "wasp/server/operations";

export const updateA3: UpdateA3 = async (args, context) => {
  // 1. Auth check
  if (!context.user) throw new HttpError(401);

  // 2. Fetch resource
  const a3 = await context.entities.Document.findUnique({
    where: { id: args.id },
  });

  // 3. Existence check
  if (!a3) throw new HttpError(404, "document not found");

  // 4. Permission check (can edit?)
  const canEdit = await canEditDocument(context.user.id, a3, context);
  if (!canEdit) {
    throw new HttpError(403, "Not authorized to edit this document");
  }

  // 5. Update
  return context.entities.Document.update({
    where: { id: args.id },
    data: args.data,
  });
};
```

### Action with Manager-Only Permission

```typescript
import type { DeleteA3 } from "wasp/server/operations";

export const deleteA3: DeleteA3 = async (args, context) => {
  if (!context.user) throw new HttpError(401);

  const a3 = await context.entities.Document.findUnique({
    where: { id: args.id },
  });

  if (!a3) throw new HttpError(404, "document not found");

  // Only MANAGER can delete
  const canDelete = await canDeleteDocument(context.user.id, a3, context);
  if (!canDelete) {
    throw new HttpError(403, "Only department managers can delete documents");
  }

  return context.entities.Document.delete({
    where: { id: args.id },
  });
};
```

### Create Resource with Role Check

```typescript
import type { CreateA3 } from "wasp/server/operations";

export const createA3: CreateA3 = async (args, context) => {
  if (!context.user) throw new HttpError(401);

  // Check user has at least MEMBER role in department
  const role = await getUserRoleInDepartment(
    context.user.id,
    args.departmentId,
    context,
  );

  if (role !== "MANAGER" && role !== "MEMBER") {
    throw new HttpError(403, "Need MEMBER or MANAGER role to create documents");
  }

  return context.entities.Document.create({
    data: {
      ...args.data,
      departmentId: args.departmentId,
      authorId: context.user.id,
    },
  });
};
```

## Advanced Patterns

### Batch Permission Checks

```typescript
/**
 * Get all permissions for A3 at once
 * Useful for UI rendering (show/hide buttons)
 */
async function getDocumentPermissions(
  userId: string,
  a3: Document,
  context,
): Promise<{
  canView: boolean;
  canEdit: boolean;
  canDelete: boolean;
  canShare: boolean;
}> {
  const [canView, canEdit, canDelete] = await Promise.all([
    canAccessDocument(userId, a3, context),
    canEditDocument(userId, a3, context),
    canDeleteDocument(userId, a3, context),
  ]);

  return {
    canView,
    canEdit,
    canDelete,
    canShare: canEdit, // Share requires edit permission
  };
}
```

### Filter Multiple Resources

```typescript
/**
 * Filter A3 IDs to only those user can access
 * More efficient than checking one by one
 */
async function filterAccessibleA3s(
  userId: string,
  a3Ids: string[],
  context,
): Promise<string[]> {
  const a3Documents = await context.entities.Document.findMany({
    where: { id: { in: a3Ids } },
  });

  const accessChecks = await Promise.all(
    a3Documents.map(async (a3) => ({
      id: a3.id,
      hasAccess: await canAccessDocument(userId, a3, context),
    })),
  );

  return accessChecks
    .filter((check) => check.hasAccess)
    .map((check) => check.id);
}
```

### Query-Level Filtering (Optimal)

```typescript
/**
 * Get all documents user can access
 * Uses database-level filtering for efficiency
 */
async function getAccessibleDocuments(
  userId: string,
  context,
): Promise<Document[]> {
  // Get user's organizations
  const orgMemberships = await context.entities.OrganizationMember.findMany({
    where: { userId },
  });
  const orgIds = orgMemberships.map((m) => m.organizationId);

  // Get user's departments
  const deptMemberships = await context.entities.UserDepartment.findMany({
    where: { userId },
  });
  const deptIds = deptMemberships.map((m) => m.departmentId);

  // Query with permission filter
  return await context.entities.Document.findMany({
    where: {
      OR: [
        // Own documents
        { authorId: userId },
        // Organization documents (if admin)
        {
          AND: [
            { organizationId: { in: orgIds } },
            {
              organization: {
                members: {
                  some: {
                    userId,
                    role: { in: ["OWNER", "ADMIN"] },
                  },
                },
              },
            },
          ],
        },
        // Department documents
        { departmentId: { in: deptIds } },
      ],
    },
    include: {
      author: { select: { id: true, username: true } },
      department: true,
      organization: true,
    },
    orderBy: { updatedAt: "desc" },
  });
}
```

## Permission Patterns by Role

### Organization Roles

**OWNER:**

- Full organization access
- Can manage all departments
- Can edit/delete all resources
- Can manage organization settings
- Can add/remove admins

**ADMIN:**

- Full organization access
- Can manage all departments
- Can edit/delete all resources
- Cannot modify owner permissions

**MEMBER:**

- Basic organization access
- Access determined by department roles
- Cannot manage organization settings

### Department Roles

**MANAGER:**

- View all department resources
- Edit all department resources
- Delete department resources
- Manage department members
- Access child departments (hierarchical)

**MEMBER:**

- View department resources
- Edit own resources
- Create new resources
- Cannot delete resources (manager only)
- Cannot manage members (manager only)

**VIEWER:**

- View department resources
- Cannot edit resources
- Cannot create resources
- Cannot delete resources
- Cannot manage members

## Common Permission Patterns

### Owner Can Edit Their Own

```typescript
// Users can edit their own resources, managers can edit all
export const updateA3 = async (args, context) => {
  if (!context.user) throw new HttpError(401);

  const a3 = await context.entities.Document.findUnique({
    where: { id: args.id },
  });
  if (!a3) throw new HttpError(404);

  const isOwner = a3.authorId === context.user.id;
  const isManager = await isDepartmentManager(
    context.user.id,
    a3.departmentId,
    context,
  );

  if (!isOwner && !isManager) {
    throw new HttpError(403, "Can only edit your own documents");
  }

  return context.entities.Document.update({
    where: { id: args.id },
    data: args.data,
  });
};
```

### Manager-Only Actions

```typescript
// Only department managers can perform this action
export const archiveA3 = async (args, context) => {
  if (!context.user) throw new HttpError(401);

  const a3 = await context.entities.Document.findUnique({
    where: { id: args.id },
  });
  if (!a3) throw new HttpError(404);

  const isManager = await isDepartmentManager(
    context.user.id,
    a3.departmentId,
    context,
  );

  if (!isManager) {
    throw new HttpError(403, "Only department managers can archive documents");
  }

  return context.entities.Document.update({
    where: { id: args.id },
    data: { status: "ARCHIVED" },
  });
};
```

### Hierarchical Department Access

```typescript
/**
 * Get all child departments recursively
 */
async function getChildDepartments(deptId: string, context): Promise<string[]> {
  const dept = await context.entities.Department.findUnique({
    where: { id: deptId },
    include: {
      children: {
        include: { children: true },
      },
    },
  });

  if (!dept) return [];

  const childIds: string[] = [];

  function collectChildren(dept: any) {
    if (dept.children) {
      dept.children.forEach((child) => {
        childIds.push(child.id);
        collectChildren(child);
      });
    }
  }

  collectChildren(dept);
  return [deptId, ...childIds];
}
```

## Critical Rules

**DO:**

- ✅ Check permissions AFTER auth and existence checks
- ✅ Use permission helpers for consistency
- ✅ Filter queries by accessible departments
- ✅ Include VIEWER role in read operations
- ✅ Check role hierarchy (OWNER > ADMIN > MANAGER > MEMBER > VIEWER)
- ✅ Handle hierarchical departments (parent access)
- ✅ Enforce permissions server-side ALWAYS
- ✅ Return 403 for permission failures (not 404)

**NEVER:**

- ❌ Skip permission checks in operations
- ❌ Hardcode role checks (use helpers)
- ❌ Forget VIEWER role in read operations
- ❌ Allow clients to bypass permissions
- ❌ Trust client-side permission checks (cosmetic only!)
- ❌ Return 404 when resource exists but user lacks permission (use 403)
- ❌ Implement permission logic in client code

## HTTP Status Code Usage

**Permission-related status codes:**

- **401 Unauthorized** - Not authenticated (`!context.user`)
- **403 Forbidden** - Authenticated but lacks permission
- **404 Not Found** - Resource doesn't exist OR user lacks permission to know it exists

**Best practice:**

- Use 403 when you want user to know resource exists but they can't access it
- Use 404 when you want to hide resource existence from unauthorized users
- Always use 401 for missing authentication

## Client-Side Usage

```typescript
// React component using permission helpers
import { useQuery } from 'wasp/client/operations'
import { getDocument, getDocumentPermissions } from 'wasp/client/operations'

function DocumentPage({ a3Id }: { a3Id: string }) {
  // Fetch document
  const { data: a3, isLoading } = useQuery(getDocument, { id: a3Id })

  // Fetch permissions
  const { data: permissions } = useQuery(getDocumentPermissions, { a3Id })

  if (isLoading) return <div>Loading...</div>
  if (!a3) return <div>Not found</div>

  return (
    <div>
      <h1>{a3.title}</h1>

      {/* Conditionally render based on permissions */}
      {permissions?.canEdit && (
        <button onClick={() => editA3()}>Edit</button>
      )}

      {permissions?.canDelete && (
        <button onClick={() => deleteA3()}>Delete</button>
      )}

      {permissions?.canShare && (
        <button onClick={() => shareA3()}>Share</button>
      )}

      {!permissions?.canEdit && (
        <div className="text-gray-500">Read-only access</div>
      )}
    </div>
  )
}
```

**Remember:** Client-side checks are for UX only. Always enforce permissions server-side.

## References

**Complete implementation examples:**

- `.claude/templates/permission-helpers.ts` (623 lines)
  - Lines 1-150: Core helpers
  - Lines 151-330: Organization/department helpers
  - Lines 331-427: Usage in operations
  - Lines 428-539: Advanced patterns
  - Lines 540-583: Client-side usage

**Related documentation:**

- `CLAUDE.md#architecture` - Multi-tenancy architecture overview
- `CLAUDE.md#error-handling` - HTTP status codes and error patterns
- `.claude/templates/operations-patterns.ts` - Complete operation examples
