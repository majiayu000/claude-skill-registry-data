---
name: apex-system-runas
description: "System.runAs in Apex tests: user-context impersonation, mixed-DML workaround, profile/permission testing, sharing verification, FLS NOT enforced, runAs nesting limits. NOT for the MIXED_DML_OPERATION error outside tests — use apex/mixed-dml-and-setup-objects. NOT for general test setup and @TestSetup semantics — use apex/apex-test-setup-patterns."
category: apex
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Security
  - Reliability
tags:
  - apex
  - testing
  - system-runas
  - sharing
  - mixed-dml
triggers:
  - "system.runas apex test user context profile"
  - "runas mixed dml setup object user insert workaround"
  - "testing sharing rule apex runas community user"
  - "runas does not enforce field level security apex"
  - "runas version mode system context running user"
  - "nested system.runas apex test limit"
  - "mixed dml error user setup object runas workaround"
inputs:
  - Target user profile/permset
  - Permission/sharing scenario under test
  - Setup-DML requirements
outputs:
  - runAs-wrapped test block
  - User fixture creation
  - FLS caveat notes
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-04-22
status: stub
---

# Apex System.runAs

Activate when writing Apex tests that need to exercise a specific user's perspective — profile, permission set, role, sharing context — or when unblocking mixed-DML errors in `@TestSetup`. `System.runAs` impersonates a target user for the scope of a block and flushes setup-object DML. Version caveat: what a bare query inside `runAs` enforces depends on the *class's* `apiVersion` — at 66.0 and earlier FLS is not enforced, at 67.0 and later database operations default to user mode and it is. See `references/gotchas.md` Gotcha 1.

## Before Starting

- **Identify the user context.** Profile, permission set, role, ownership context — each may matter.
- **Confirm you need impersonation.** If testing code that uses `WITH USER_MODE` or security enforcement, runAs alone may not cover FLS.
- **Plan for mixed DML.** User/Group/UserRole DML cannot mix with sObject DML in one transaction — runAs is the escape hatch.

## Core Concepts

### Basic runAs

```
User u = [SELECT Id FROM User WHERE Profile.Name = 'Standard User' LIMIT 1];
System.runAs(u) {
    // UserInfo.getUserId() returns u.Id inside this block
    insert new Account(Name = 'Owned by u');
    List<Account> visible = [SELECT Id FROM Account];
    // Sharing rules applied as user u
}
```

Applies to: `UserInfo.*`, sharing enforcement, profile CRUD, record ownership.

Does NOT apply to: `System.runAs` itself (an admin can still call it). FLS depends on the class's `apiVersion` — see the section below.

### Mixed DML workaround

Setup objects (`User`, `UserRole`, `Group`, `GroupMember`, `PermissionSet*`, `Profile`) cannot be DML-ed in the same transaction as sObject DML. `runAs` partitions the operations:

```
System.runAs(new User(Id = UserInfo.getUserId())) {
    User u = new User(...);
    insert u;  // setup-object DML isolated
}
insert new Account(Name = 'X');  // non-setup DML — legal
```

The pattern `runAs(new User(Id = UserInfo.getUserId()))` is a no-op impersonation that exists only for the mixed-DML boundary.

### Nested runAs

Allowed up to 20 levels. Exits back to the previous user when the block ends. Rarely useful; flat is better.

### Version behavior

If the running user has `ModifyAllData` / `ViewAllData`, sharing is still bypassed inside `runAs` unless the target user lacks those perms. Make sure the target `User` record reflects the profile you mean to test.

### FLS enforcement is gated on the class's API version

```
System.runAs(lowPrivUser) {
    Account a = [SELECT Hidden__c FROM Account];
    String x = a.Hidden__c;  // API 66.0 and earlier: no FLS error.
                             // API 67.0 and later: the query runs in user mode and throws.
}
```

Do not depend on either default. State the access mode so the assertion means the same thing at every version: `WITH USER_MODE` SOQL, `AccessLevel.USER_MODE` on `Database` calls, or `Security.stripInaccessible` where partial success is the requirement.

## Common Patterns

### Pattern: Sharing-rule verification test

```
@IsTest static void testOwnershipVisibility() {
    User salesUser = TestUserFactory.salesUser();
    insert salesUser;
    System.runAs(salesUser) {
        insert new Account(Name = 'Private');
    }
    User otherSalesUser = TestUserFactory.salesUser();
    insert otherSalesUser;
    System.runAs(otherSalesUser) {
        System.assertEquals(0, [SELECT COUNT() FROM Account WHERE Name = 'Private']);
    }
}
```

### Pattern: Permission-set assignment test

```
User u = TestUserFactory.user();
insert u;
PermissionSet ps = [SELECT Id FROM PermissionSet WHERE Name = 'MyFeature'];
insert new PermissionSetAssignment(AssigneeId = u.Id, PermissionSetId = ps.Id);
System.runAs(u) {
    // exercise code gated by the permset
}
```

### Pattern: Mixed-DML boundary in @TestSetup

```
@TestSetup
static void setup() {
    System.runAs(new User(Id = UserInfo.getUserId())) {
        User u = new User(...);
        insert u;
    }
    insert new Account(Name = 'A');  // legal
}
```

## Decision Guidance

| Goal | Tool |
|---|---|
| Test a different profile's visibility | `System.runAs(user)` |
| Unblock mixed-DML in setup | `System.runAs(new User(Id = UserInfo.getUserId()))` |
| Verify FLS enforcement | `WITH USER_MODE` or `Security.stripInaccessible` — NOT runAs |
| Test community/guest user | Create a Customer Community user → `runAs` |
| Verify record ownership effects | `runAs(ownerUser)` + DML + assertions |

## Recommended Workflow

1. Create/query the target `User` record; confirm profile + perm sets reflect reality.
2. Wrap the user-context code in `System.runAs(u) { ... }`.
3. For setup-DML mixing sObjects, wrap the User/Group insert in `runAs(new User(Id = UserInfo.getUserId()))`.
4. Assert on query results AS THE TARGET USER.
5. For FLS, add a separate test using `WITH USER_MODE`.
6. Document the caveat in the test comment: "runAs does not enforce FLS."
7. Avoid nesting runAs; refactor into separate methods.

## Review Checklist

- [ ] Target user's profile/permset reflects the scenario
- [ ] Mixed-DML uses `runAs(new User(Id = UserInfo.getUserId()))` guard
- [ ] FLS-sensitive code has a parallel `WITH USER_MODE` test (runAs alone insufficient)
- [ ] No nested runAs beyond 2 levels
- [ ] Community/guest tests use the correct Customer Community license

## Salesforce-Specific Gotchas

1. **On a class saved at API 66.0 or earlier, FLS is silently bypassed inside runAs.** The test passes and the FLS-violating code ships. At 67.0 and later the same query throws instead — so read the `.cls-meta.xml` before trusting either outcome.
2. **`runAs` only works in test context** — calling it in non-test code throws.
3. **`runAs(someUser)` inherits governor limits from the outer transaction** — does not give you a fresh limit budget.
4. **Querying a User with `WHERE Profile.Name = ...` may hit profile-name changes across orgs.** Prefer `UserType = 'Standard'` plus permset assignments.

## Output Artifacts

| Artifact | Description |
|---|---|
| `TestUserFactory` | Reusable user builders per profile |
| runAs-wrapped test methods | User-context sharing tests |
| FLS parallel test | `WITH USER_MODE` or `stripInaccessible` coverage |

## Related Skills

- `apex/apex-test-setup-patterns` — overall test structure
- `apex/apex-user-and-permission-checks` — user-mode and permission enforcement
- `apex/apex-with-without-sharing-decision` — choosing the sharing keyword
