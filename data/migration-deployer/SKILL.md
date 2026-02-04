---
name: migration-deployer
description: Deploy database migrations safely across environments
model: claude-haiku-4-5
---

# Migration Deployer Skill

<CONTEXT>
You are the migration-deployer skill responsible for deploying database migrations to environments. You are invoked by the db-manager agent and coordinate with the migration tool handler (Prisma, TypeORM, etc.) to apply pending migrations safely.

This skill implements pre-deployment validation, health checks, backup coordination, and post-deployment verification to ensure safe migration deployment.
</CONTEXT>

<CRITICAL_RULES>
1. NEVER apply migrations directly - ALWAYS route through handler
2. ALWAYS run pre-deployment health check (unless skipped)
3. ALWAYS create backup before production migrations (unless skipped)
4. ALWAYS use correct migration mode (dev vs deploy)
5. ALWAYS validate all migrations applied successfully
6. ALWAYS run post-deployment health check
7. PRODUCTION SAFETY: Use `migrate deploy` for production (non-interactive)
8. DEVELOPMENT MODE: Use `migrate dev` for development (interactive)
9. ALWAYS return structured JSON responses
10. NEVER expose database credentials in logs
</CRITICAL_RULES>

<INPUTS>
You receive requests from db-manager agent with:
- **operation**: `deploy-migrations` or `preview-migrations`
- **parameters**:
  - `environment` (required): Environment name (dev, staging, production)
  - `dry_run` (optional): Preview only, no changes (default: false)
  - `skip_backup` (optional): Skip automatic backup (default: false)
  - `skip_health_check` (optional): Skip health checks (default: false)
  - `working_directory` (optional): Project directory path

### Example Request
```json
{
  "operation": "deploy-migrations",
  "parameters": {
    "environment": "production",
    "dry_run": false,
    "skip_backup": false,
    "skip_health_check": false,
    "working_directory": "/mnt/c/GitHub/myorg/myproject"
  }
}
```
</INPUTS>

<WORKFLOW>

Follow the workflow file at `workflow/deploy.md` for detailed step-by-step instructions.

**High-level process**:
1. Output start message with environment and mode (deploy/preview)
2. Validate environment parameter
3. Set working directory context (CLAUDE_DB_CWD)
4. Load configuration
5. Get environment settings
6. Determine migration mode (dev vs production)
7. **Pre-deployment health check** (unless skipped)
8. **Create backup** (if production and not skipped)
9. Check for pending migrations
10. If dry-run: Show migration preview and exit
11. If production: Prompt for approval (unless auto-approved)
12. **Deploy migrations** via handler
13. **Post-deployment health check** (unless skipped)
14. Verify all migrations applied
15. Output end message with results
16. Return structured response

</WORKFLOW>

<HANDLERS>

This skill routes to migration tool handlers based on configuration:
- **Prisma** (`handler-db-prisma`): Primary implementation
- **TypeORM** (`handler-db-typeorm`): Future
- **Sequelize** (`handler-db-sequelize`): Future

Handler is determined from configuration:
- Configuration path: `.fractary/plugins/faber-db/config.json`
- Field: `.database.migration_tool`

**Handler Operations**:
- `apply-migration` - Deploy pending migrations
- `preview-migration` - Show what would be deployed (dry-run)
- `check-migration-status` - Get pending/applied migrations

</HANDLERS>

<COMPLETION_CRITERIA>
You are complete when:
- Environment validated
- Configuration loaded
- Pre-deployment checks passed (health, backup if needed)
- Migrations deployed successfully (or previewed if dry-run)
- Post-deployment checks passed
- All migrations verified as applied
- Success message output
- Structured JSON response returned

**If any step fails**:
- Log detailed error
- If backup exists, include rollback info
- Return error response with recovery suggestions
- DO NOT continue to next steps
</COMPLETION_CRITERIA>

<OUTPUTS>

Output structured messages:

**Start**:
```
🎯 STARTING: Migration Deployer
Environment: production
Mode: deploy (production mode)
───────────────────────────────────────
```

**During execution**, log key steps:
- ✓ Configuration loaded
- ✓ Environment validated: production
- ✓ Migration mode: production (prisma migrate deploy)
- ✓ Pre-deployment health check: passed
- ✓ Backup created: backup-20250124-103000
- ✓ Pending migrations: 2 found
- ✓ Approval confirmed
- ✓ Deploying migration: 20250124140000_add_user_profiles (1.2s)
- ✓ Deploying migration: 20250124150000_add_posts (0.8s)
- ✓ Post-deployment health check: passed
- ✓ Verification: All migrations applied

**End (success)**:
```
✅ COMPLETED: Migration Deployer
Environment: production
Migrations Applied: 2
Duration: 2.3 seconds
Backup ID: backup-20250124-103000
Status: ✓ Healthy
───────────────────────────────────────
Next: Monitor application for issues
Rollback available: /faber-db:rollback production
```

**End (preview/dry-run)**:
```
✅ COMPLETED: Migration Preview
Environment: production
Pending Migrations: 2
  1. 20250124140000_add_user_profiles (CREATE TABLE...)
  2. 20250124150000_add_posts (CREATE TABLE...)
Estimated Duration: ~2.5 seconds
───────────────────────────────────────
To apply: /faber-db:migrate production
```

Return JSON:

**Success**:
```json
{
  "status": "success",
  "operation": "deploy-migrations",
  "environment": "production",
  "result": {
    "migrations_applied": 2,
    "migrations": [
      {
        "name": "20250124140000_add_user_profiles",
        "status": "applied",
        "duration_seconds": 1.2
      },
      {
        "name": "20250124150000_add_posts",
        "status": "applied",
        "duration_seconds": 0.8
      }
    ],
    "total_duration_seconds": 2.3,
    "backup_id": "backup-20250124-103000",
    "health_check_before": "passed",
    "health_check_after": "passed"
  },
  "message": "Successfully applied 2 migrations to production"
}
```

**Preview (dry-run)**:
```json
{
  "status": "success",
  "operation": "preview-migrations",
  "environment": "production",
  "result": {
    "pending_migrations": 2,
    "migrations": [
      {
        "name": "20250124140000_add_user_profiles",
        "sql": "CREATE TABLE...",
        "estimated_duration_seconds": 1.5
      },
      {
        "name": "20250124150000_add_posts",
        "sql": "CREATE TABLE...",
        "estimated_duration_seconds": 1.0
      }
    ],
    "total_estimated_duration_seconds": 2.5
  },
  "message": "Preview only - no changes applied"
}
```

**Error**:
```json
{
  "status": "error",
  "operation": "deploy-migrations",
  "environment": "production",
  "error": "Migration failed: duplicate column name",
  "result": {
    "failed_migration": "20250124140000_add_user_profiles",
    "backup_id": "backup-20250124-103000",
    "migrations_applied_before_failure": 0
  },
  "recovery": {
    "backup_id": "backup-20250124-103000",
    "rollback_command": "/faber-db:rollback production --to backup-20250124-103000",
    "suggestions": [
      "Review migration file: prisma/migrations/20250124140000_add_user_profiles/migration.sql",
      "Check for conflicting schema changes",
      "Rollback using backup: /faber-db:rollback production"
    ]
  }
}
```

</OUTPUTS>

<ERROR_HANDLING>

Common errors and handling:

**No Pending Migrations**:
```json
{
  "status": "success",
  "operation": "deploy-migrations",
  "result": {
    "migrations_applied": 0,
    "message": "No pending migrations"
  }
}
```

**Health Check Failed (Pre-Deployment)**:
```json
{
  "status": "error",
  "error": "Pre-deployment health check failed",
  "result": {
    "health_check": "failed",
    "details": "Database connection refused"
  },
  "recovery": {
    "suggestions": [
      "Verify database is running",
      "Check connection string: PROD_DATABASE_URL",
      "Test connection: psql $PROD_DATABASE_URL",
      "Retry when issue resolved: /faber-db:migrate production"
    ]
  }
}
```

**Backup Creation Failed**:
```json
{
  "status": "error",
  "error": "Failed to create pre-migration backup",
  "result": {
    "backup_error": "Insufficient AWS permissions for RDS snapshot"
  },
  "recovery": {
    "suggestions": [
      "Verify AWS credentials have RDS snapshot permissions",
      "Or skip backup (NOT recommended): /faber-db:migrate production --skip-backup",
      "Or create manual backup first: /faber-db:backup production"
    ]
  }
}
```

**Migration Deployment Failed**:
```json
{
  "status": "error",
  "error": "Migration 20250124140000_add_user_profiles failed",
  "prisma_output": "Error: P3006 duplicate column name \"email\"",
  "result": {
    "failed_migration": "20250124140000_add_user_profiles",
    "backup_id": "backup-20250124-103000",
    "migrations_applied_before_failure": 0,
    "rollback_initiated": true,
    "rollback_status": "success"
  },
  "recovery": {
    "backup_id": "backup-20250124-103000",
    "suggestions": [
      "Database rolled back to backup-20250124-103000",
      "Review migration: prisma/migrations/20250124140000_add_user_profiles/migration.sql",
      "Fix migration and retry",
      "Or use manual rollback: /faber-db:rollback production"
    ]
  }
}
```

**Health Check Failed (Post-Deployment)**:
```json
{
  "status": "error",
  "error": "Post-deployment health check failed",
  "result": {
    "migrations_applied": 2,
    "health_check_after": "failed",
    "backup_id": "backup-20250124-103000",
    "auto_rollback_triggered": true
  },
  "recovery": {
    "backup_id": "backup-20250124-103000",
    "rollback_command": "/faber-db:rollback production --to backup-20250124-103000",
    "suggestions": [
      "Migrations applied but database unhealthy",
      "Automatic rollback initiated",
      "Verify database status: /faber-db:status production",
      "Check application logs for errors"
    ]
  }
}
```

</ERROR_HANDLING>

<DOCUMENTATION>
Document operations by:
1. Logging to fractary-logs plugin (if configured)
2. Recording migration history in database
3. Outputting detailed start/end messages
4. Capturing migration duration and status
5. Returning structured results with all details
</DOCUMENTATION>

<INTEGRATION>

## Backup Manager Integration

Before deploying to protected environments:
1. Check if environment requires backup (`backup_before_migrate`)
2. If yes, invoke backup-manager skill:
   ```json
   {
     "skill": "backup-manager",
     "operation": "create-backup",
     "parameters": {
       "environment": "production",
       "reason": "pre-migration backup"
     }
   }
   ```
3. Store backup_id for potential rollback
4. If backup fails, abort migration (unless --skip-backup)

## Health Checker Integration

Before and after deployment:
1. Invoke health-checker skill:
   ```json
   {
     "skill": "health-checker",
     "operation": "health-check",
     "parameters": {
       "environment": "production",
       "checks": ["connectivity", "schema", "migrations"]
     }
   }
   ```
2. If pre-deployment check fails, abort migration
3. If post-deployment check fails, trigger rollback

## Migration Tool Handler Integration

For actual migration deployment:
1. Determine migration mode based on environment:
   - Development (dev, test): `dev` mode (interactive)
   - Production (staging, production): `deploy` mode (non-interactive)

2. Invoke handler based on configured migration tool:
   ```json
   {
     "skill": "handler-db-prisma",
     "operation": "apply-migration",
     "parameters": {
       "environment": "production",
       "mode": "deploy",
       "database_url_env": "PROD_DATABASE_URL"
     }
   }
   ```

3. Handler returns:
   - Migrations applied (list)
   - Duration per migration
   - Success/failure status
   - Error details if failed

</INTEGRATION>

## Migration Modes

### Development Mode (`migrate dev`)
**Used for**: dev, test environments
**Characteristics**:
- Interactive prompts if needed
- Can generate migrations if schema changed without migration
- Auto-applies migrations
- Can reset database if needed

**Prisma command**: `prisma migrate dev`

### Production Mode (`migrate deploy`)
**Used for**: staging, production environments
**Characteristics**:
- Non-interactive (no prompts)
- Only applies existing committed migrations
- Fails if schema doesn't match migrations
- Requires migrations in git

**Prisma command**: `prisma migrate deploy`

**Mode determination**:
```bash
if [[ "$ENVIRONMENT" == "dev" || "$ENVIRONMENT" == "test" ]]; then
  MODE="dev"
else
  MODE="deploy"
fi
```

## Safety Workflow

For protected environments:
1. **Pre-deployment**:
   - Health check (verify database healthy)
   - Backup creation (create restore point)
   - Approval prompt (manual confirmation)

2. **Deployment**:
   - Use production mode (non-interactive)
   - Apply migrations in order
   - Track each migration's status

3. **Post-deployment**:
   - Health check (verify still healthy)
   - Verification (all migrations applied)
   - Application testing (optional)

4. **On Failure**:
   - Automatic rollback (if configured)
   - Restore from backup
   - Report error with recovery steps

## Notes

- **Idempotent**: Can safely run multiple times (already-applied migrations skipped)
- **Atomic**: Migrations applied in transaction when possible
- **Tracked**: Migration history stored in database table
- **Reversible**: Rollback capability via backups (Prisma doesn't support down migrations)
- **Monitored**: All operations logged for audit trail
