---
name: "Firestore Security Rules"
description: "Write and validate Firestore Security Rules following the project's multi-tenancy Blueprint pattern. Use this skill when implementing collection-level security, Blueprint membership validation, role-based permissions, and data access controls. Ensures rules validate BlueprintMember status, check permissions array, enforce data isolation, and integrate with the three-layer architecture where Security Rules are the first line of defense."
license: "MIT"
---

# Firestore Security Rules Skill

This skill helps create secure Firestore Security Rules following the project's multi-tenancy architecture.

## Core Principles

### Security-First Architecture
- **Security Rules are First Defense**: Never trust client-side checks alone
- **Multi-Tenancy**: Blueprint-based data isolation
- **Permission System**: Role + permissions array validation
- **Server-Side Validation**: All access validated at database level

### Blueprint Multi-Tenancy Model

```
User → Organization → Blueprint → Resources
           ↓
      Team / Partner
```

- Blueprint defines permission boundaries (not data boundaries)
- BlueprintMember is dedicated collection for membership
- All resources belong to a Blueprint
- Access controlled via BlueprintMember role + permissions

## Core Helper Functions

### Global Authentication

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    
    /**
     * Check if user is authenticated
     */
    function isAuthenticated() {
      return request.auth != null;
    }
    
    /**
     * Get current user ID
     */
    function getCurrentUserId() {
      return request.auth.uid;
    }
    
    /**
     * Check if user is system admin
     */
    function isSystemAdmin() {
      return isAuthenticated() && 
             get(/databases/$(database)/documents/users/$(getCurrentUserId())).data.role == 'admin';
    }
  }
}
```

### Blueprint Membership Functions

```javascript
/**
 * Check if user is Blueprint member
 */
function isBlueprintMember(blueprintId) {
  let memberId = getCurrentUserId() + '_' + blueprintId;
  return exists(/databases/$(database)/documents/blueprintMembers/$(memberId));
}

/**
 * Get user's role in Blueprint
 */
function getBlueprintMemberRole(blueprintId) {
  let memberId = getCurrentUserId() + '_' + blueprintId;
  let member = get(/databases/$(database)/documents/blueprintMembers/$(memberId));
  return member.data.role;
}

/**
 * Check if user is Owner or Admin
 */
function isBlueprintOwnerOrAdmin(blueprintId) {
  let role = getBlueprintMemberRole(blueprintId);
  return role in ['owner', 'admin'];
}

/**
 * Check if user has specific permission
 */
function hasPermission(blueprintId, permission) {
  let memberId = getCurrentUserId() + '_' + blueprintId;
  let member = get(/databases/$(database)/documents/blueprintMembers/$(memberId));
  return permission in member.data.permissions;
}

/**
 * Check if member is active
 */
function isMemberActive(blueprintId) {
  let memberId = getCurrentUserId() + '_' + blueprintId;
  let member = get(/databases/$(database)/documents/blueprintMembers/$(memberId));
  return member.data.status == 'active';
}
```

### Data Validation Functions

```javascript
/**
 * Validate task data structure
 */
function validateTaskData(data) {
  return data.keys().hasAll(['blueprintId', 'title', 'status']) &&
         data.title is string &&
         data.title.size() > 0 &&
         data.title.size() <= 200 &&
         data.status in ['pending', 'in-progress', 'completed', 'archived'];
}
```

## Collection Rules Pattern

### Resource Collection (with Blueprint)

```javascript
match /tasks/{taskId} {
  // Blueprint members can read tasks
  allow read: if isAuthenticated() && 
                 isBlueprintMember(resource.data.blueprintId) &&
                 isMemberActive(resource.data.blueprintId);
  
  // Members with task:create permission can create
  allow create: if isAuthenticated() && 
                   isBlueprintMember(request.resource.data.blueprintId) &&
                   isMemberActive(request.resource.data.blueprintId) &&
                   hasPermission(request.resource.data.blueprintId, 'task:create') &&
                   validateTaskData(request.resource.data);
  
  // Members with task:update permission or assignee can update
  allow update: if isAuthenticated() && 
                   isBlueprintMember(resource.data.blueprintId) &&
                   isMemberActive(resource.data.blueprintId) &&
                   (hasPermission(resource.data.blueprintId, 'task:update') || 
                    resource.data.assignedTo == getCurrentUserId()) &&
                   validateTaskData(request.resource.data);
  
  // Only members with task:delete permission can delete
  allow delete: if isAuthenticated() && 
                   isBlueprintMember(resource.data.blueprintId) &&
                   isMemberActive(resource.data.blueprintId) &&
                   hasPermission(resource.data.blueprintId, 'task:delete');
}
```

### Nested Subcollections

```javascript
match /blueprints/{blueprintId} {
  allow read: if isAuthenticated() && isBlueprintMember(blueprintId);
  
  // Nested tasks subcollection
  match /tasks/{taskId} {
    allow read: if isAuthenticated() && 
                   isBlueprintMember(blueprintId) &&
                   isMemberActive(blueprintId);
    
    allow create: if isAuthenticated() && 
                     isBlueprintMember(blueprintId) &&
                     isMemberActive(blueprintId) &&
                     hasPermission(blueprintId, 'task:create') &&
                     validateTaskData(request.resource.data) &&
                     request.resource.data.blueprintId == blueprintId;
  }
}
```

### Membership Collection

```javascript
match /blueprintMembers/{memberId} {
  // Blueprint members can read member list
  allow read: if isAuthenticated() && 
                 isBlueprintMember(resource.data.blueprintId);
  
  // Only Owner/Admin can add/modify/remove members
  allow create, update: if isAuthenticated() && 
                           isBlueprintOwnerOrAdmin(resource.data.blueprintId);
  
  // Only Owner can delete members (soft delete recommended)
  allow delete: if isAuthenticated() && 
                   isBlueprintOwnerOrAdmin(resource.data.blueprintId);
}
```

### User Collection

```javascript
match /users/{userId} {
  // Users can only read their own data
  allow read: if isAuthenticated() && getCurrentUserId() == userId;
  
  // Users can update their own data (but not role)
  allow update: if isAuthenticated() && 
                   getCurrentUserId() == userId &&
                   !request.resource.data.diff(resource.data).affectedKeys().hasAny(['role']);
  
  // Only system admin can create/delete users
  allow create, delete: if isSystemAdmin();
}
```

### Audit Logs (Write-Only)

```javascript
match /auditLogs/{logId} {
  // Only system admin can read logs
  allow read: if isSystemAdmin();
  
  // Any authenticated user can write logs
  allow create: if isAuthenticated();
  
  // Logs cannot be modified or deleted
  allow update, delete: if false;
}
```

## Performance Optimization

### Minimize get() Calls

```javascript
// ❌ BAD: Multiple get() calls
function hasMultiplePermissions(blueprintId) {
  let memberId = getCurrentUserId() + '_' + blueprintId;
  let member = get(/databases/$(database)/documents/blueprintMembers/$(memberId));
  let canCreate = 'task:create' in member.data.permissions;
  let member2 = get(/databases/$(database)/documents/blueprintMembers/$(memberId)); // Duplicate!
  let canUpdate = 'task:update' in member2.data.permissions;
  return canCreate && canUpdate;
}

// ✅ GOOD: Single get() call
function hasMultiplePermissions(blueprintId) {
  let memberId = getCurrentUserId() + '_' + blueprintId;
  let member = get(/databases/$(database)/documents/blueprintMembers/$(memberId));
  return 'task:create' in member.data.permissions && 
         'task:update' in member.data.permissions;
}
```

### Use exists() When Possible

```javascript
// ✅ GOOD: exists() is faster than get()
function isBlueprintMember(blueprintId) {
  let memberId = getCurrentUserId() + '_' + blueprintId;
  return exists(/databases/$(database)/documents/blueprintMembers/$(memberId));
}

// Only use get() when you need data
function getBlueprintMemberRole(blueprintId) {
  let memberId = getCurrentUserId() + '_' + blueprintId;
  let member = get(/databases/$(database)/documents/blueprintMembers/$(memberId));
  return member.data.role;
}
```

## Testing Security Rules

### Using Firebase Emulator

```bash
# Start emulator
firebase emulators:start

# Run security rules tests
npm run test:rules
```

### Test Template

```javascript
describe('Task Collection Security Rules', () => {
  it('should allow authenticated blueprint member to read tasks', async () => {
    const db = testEnv.authenticatedContext('user1').firestore();
    
    // Setup: Create member
    await testEnv.withSecurityRulesDisabled(async (context) => {
      await context.firestore().doc('blueprintMembers/user1_blueprint1').set({
        blueprintId: 'blueprint1',
        userId: 'user1',
        role: 'member',
        status: 'active',
        permissions: ['task:read']
      });
    });
    
    // Test: Read should succeed
    await assertSucceeds(db.doc('tasks/task1').get());
  });
  
  it('should deny unauthenticated access', async () => {
    const db = testEnv.unauthenticatedContext().firestore();
    await assertFails(db.doc('tasks/task1').get());
  });
});
```

## Checklist

When writing Security Rules:

- [ ] All collections have security rules
- [ ] Multi-tenancy data isolation implemented
- [ ] BlueprintMember membership checked
- [ ] Permissions array validated
- [ ] Member status checked (active/suspended)
- [ ] Data validation functions complete
- [ ] Minimize get() calls for performance
- [ ] Use exists() when only checking existence
- [ ] Audit logs are write-only
- [ ] Cross-blueprint access prevented
- [ ] Tests cover all scenarios
- [ ] Both positive and negative tests

## Integration with Architecture

### Three-Layer Security

```
1. UI Layer: Permission checks for UX (can hide buttons)
2. Service Layer: Business logic validation
3. Security Rules: Server-side enforcement (MUST)
```

### Repository + Security Rules

```typescript
// Repository - No permission checks
async deleteTask(taskId: string): Promise<void> {
  await this.taskRepository.delete(taskId);
  // Security Rules will validate permissions
}
```

```javascript
// Security Rules - Permission enforcement
match /tasks/{taskId} {
  allow delete: if isAuthenticated() 
                && isBlueprintMember(resource.data.blueprintId)
                && hasPermission(resource.data.blueprintId, 'task:delete');
}
```

## References

- [Security Rules Instructions](.github/instructions/ng-gighub-security-rules.instructions.md)
- [Architecture Guide](.github/instructions/ng-gighub-architecture.instructions.md)
- [Firebase Documentation](https://firebase.google.com/docs/firestore/security/get-started)
