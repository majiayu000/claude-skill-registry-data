---
name: nav2009-permissions-security
description: Expert guidance on the Microsoft Dynamics NAV 2009 security and permissions model — diagnosing "you do not have permission to Read/Insert/Modify/Delete/Execute" errors, designing role-based access via NAV Roles (Permission Sets), understanding object permissions (Read, Insert, Modify, Delete, Execute, indirect), security filters for record-level access control, Windows vs Database login modes, and NAV↔SQL login/permission synchronization including the Standard vs Enhanced SQL security models. Use when a user hits a "you do not have permission" error in NAV 2009, when designing or auditing Roles for Sales/Purchasing/Finance/Posting-only users, when a NAV user cannot log in or records are invisible, when setting up security filters by Responsibility Center or company, or when troubleshooting NAV↔SQL login synchronization.
license: MIT
metadata:
  version: "1.0.3"
---

# NAV 2009 Permissions & Security

Expert guidance for **Microsoft Dynamics NAV 2009** security: the two-layer license/permission
model, Roles, object rights, security filters, login modes, and SQL security synchronization.
This skill is knowledge-only; detailed tables and error-cause mappings live in
[REFERENCE.md](REFERENCE.md) — consult it before diagnosing a non-trivial permission problem or
designing a Role set.

## Platform facts (don't guess against these)

- **Two layers**: the NAV **license (.flf)** gates which objects exist and can run at all;
  **permissions** (Roles) gate which users may use the licensed objects. A "permission" error can
  actually be a license-range issue — distinguish them before changing Roles.
- **Roles = Permission Sets**: NAV 2009 uses the term *Role* (tables `Permission Set` and
  `Permission`). A Role is a named bundle of per-object rights. Users receive Roles through the
  **User Role** assignment (Tools → Security in Classic, or the User card). The **SUPER** Role
  grants full access to all objects; **SUPER (DATA)** grants full data access but excludes object
  design.
- **Object rights**: each permission record covers one object type (TableData, Table, Form, Report,
  Codeunit, Page, XMLport, etc.) with individual flags for **Read, Insert, Modify, Delete,
  Execute** plus an **Indirect** qualifier — indirect means the user may touch the object only
  through other C/AL code, never directly.
- **Security filters**: an optional filter string on a permission record that restricts *which
  records* a Role may access (e.g., `Responsibility Center = RES1` or `Company Name = CRONUS`).
  This is NAV's record-level security mechanism.
- **Login modes**: each NAV user maps to exactly one SQL Server login — either a **Windows login**
  (an Active Directory user or group mapped in NAV) or a **Database login** (NAV-managed
  username/password stored in NAV). Mixed mode is possible across users.
- **SQL security models**: **Standard** — NAV enforces all permissions in the application layer;
  SQL logins get broad database access. **Enhanced** — NAV creates and maintains SQL Server roles
  per company and pushes object permissions down to SQL; changes require an explicit **Synchronize
  All Logins** step. In the 3-tier (RTC) model the service tier connects to SQL as its own service
  account and NAV performs app-layer permission checks regardless of SQL model.

## Diagnosing a permission error

1. **License or permission?** — "Your program license does not permit access to table/object X"
   (or object simply missing from menus) → license range issue; skip to the license file. "You do
   not have permission to Read/Insert/Modify/Delete/Execute X" → it is a permissions problem.
2. **Which Role is the user missing?** — Open the user's Role list (Tools → Security → Windows
   Logins / Database Logins → Roles). Find the object type + ID in any assigned Role's Permission
   lines. If absent, add it to an appropriate Role (never add to SUPER unless genuinely needed).
3. **Indirect-only?** — If the user has the object right but only as *Indirect*, they cannot use
   it directly (e.g., open the table in a filter, run the report standalone). They need a direct
   right for the operation they are performing.
4. **Security filter blocking records?** — User has the right but records are invisible or they
   get an implicit permission error only on some data. Check the Filter column on the permission
   record for that Role and object.
5. **Login not found or out of sync?** — User cannot log in at all: check whether a Windows Login
   or Database Login record exists for them in NAV, and whether the SQL login is enabled and in
   sync. Run **Synchronize All Logins** (Database → Logins) after any login or Role change in
   an Enhanced security setup.
6. **Is it actually a lock, not a permission?** — "Another user has already modified the record"
   or timeout on a posting action → locking, not permissions. See **nav2009-sql-performance** /
   **nav2009-troubleshooting**.

Consult REFERENCE.md § Error → cause → fix for the full mapping table.

## Designing roles

- **Least privilege**: grant only the object types and rights the function actually needs. Avoid
  handing out SUPER — it bypasses all permission checks.
- **Functional Role pattern**: one Role per business function (e.g., `SALES-ORDER`, `PURCH-RECV`,
  `FINANCE-POST`, `WAREHOUSE-RECEIVE`). Users get the combination of Roles their job requires.
- **Separate setup from posting**: users who post transactions should not also have Modify rights
  on setup tables (Payment Terms, Posting Groups, etc.).
- **Custom-object Role**: keep all objects in the 50000+ range in their own Role (`CUSTOM-BASE` or
  per-module). This makes it easy to assign custom objects without touching standard Roles.
- **Security filters for data segregation**: use the Filter column to restrict a Role to a
  Responsibility Center, Location, or company rather than creating separate user accounts.
- **Re-synchronize after changes**: in an Enhanced SQL security setup, any change to Roles or
  login assignments requires a Synchronize All Logins action before SQL-level enforcement catches
  up.
- **Document Roles**: record what each custom Role covers and why — especially Filter strings,
  which are not visible in normal navigation.

## Cross-references

- **Locking / "another user has already..." errors** → **nav2009-sql-performance** and
  **nav2009-troubleshooting** — these are not permission problems.
- **C/AL code that reads/writes protected objects, or permission checks in code
  (`TESTPERMISSIONS`, `HASPERMISSIONS`)** → **nav2009-development**.
- **Service-tier service account, Windows Authentication across tiers, NAS login issues** →
  **nav2009-service-tier-admin**.

Consult [REFERENCE.md](REFERENCE.md) for detail tables on object types, rights, SQL security
models, and the full error-cause-fix reference.
