---
name: migration-safety-checker
description: This skill should be used when the user asks to "create a migration", "run makemigrations", "modify a model field", "rename a column", or mentions "schema change", "alter table", "database migration". Validates migrations are production-safe.
---

# Migration Safety Checker

Validates Django migrations are production-safe before they cause data loss.

## Activation Triggers

This skill activates when:
- Running `makemigrations`
- Modifying model fields
- Mentioning "migration", "schema", "alter table"
- Adding/removing/renaming fields
- Changing field types
- Creating or modifying migration files

## Safety Requirements

All migrations MUST be:
- ✅ **Reversible** - Can roll back safely
- ✅ **No data loss** - Preserve existing data
- ✅ **Tested** - Run on staging first
- ✅ **Safe for production** - No downtime operations
- ✅ **Documented** - Explain what changes and why

## High-Risk Operations

These operations require special attention:

### 🔴 CRITICAL RISK - Data Loss Possible

1. **Dropping columns** without data migration
2. **Renaming fields** without data migration
3. **Changing field types** (data conversion issues)
4. **Adding non-nullable fields** without default
5. **Removing tables** with data

### 🟡 MEDIUM RISK - Requires Careful Planning

1. **Adding indexes** on large tables (use `CONCURRENTLY`)
2. **Adding unique constraints** (check for duplicates first)
3. **Changing `max_length`** (data truncation risk)

### 🟢 LOW RISK - Generally Safe

1. **Adding nullable fields**
2. **Adding fields with defaults**
3. **Creating new tables**
4. **Adding non-unique indexes**

## Validation Process

### Step 1: Analyze Migration File

When migration is created:

```python
# Generated migration
class Migration(migrations.Migration):
    operations = [
        migrations.RemoveField(
            model_name='user',
            name='old_email',  # 🔴 DATA LOSS RISK!
        ),
    ]
```

### Step 2: Identify Risks

Detect:
- Operation type: `RemoveField`
- Field: `old_email`
- **Risk:** 🔴 CRITICAL - Dropping column loses data!

### Step 3: Block Unsafe Migration

> **⛔ UNSAFE MIGRATION DETECTED**
>
> **Operation:** `RemoveField(model_name='user', name='old_email')`
>
> **Risk:** 🔴 CRITICAL - Data loss!
>
> **Problem:**
> - Drops `old_email` column immediately
> - All existing email data will be PERMANENTLY LOST
> - Cannot be rolled back after data is gone
>
> **Safe Approach:**
> Use 3-step migration pattern:
> 1. Data migration: Archive `old_email` data
> 2. Wait for deployment
> 3. Drop column in separate migration
>
> Should I generate the safe migration sequence?

### Step 4: Generate Safe Migration

If user approves, create:

```python
# Migration 1: Archive data
class Migration(migrations.Migration):
    dependencies = [('users', '0001_initial')]

    operations = [
        migrations.RunPython(archive_old_emails, reverse_code=restore_old_emails),
    ]

def archive_old_emails(apps, schema_editor):
    """Archive old_email data before dropping."""
    User = apps.get_model('users', 'User')
    EmailArchive = apps.get_model('users', 'EmailArchive')

    for user in User.objects.all():
        if user.old_email:
            EmailArchive.objects.create(
                user_id=user.id,
                email=user.old_email
            )

def restore_old_emails(apps, schema_editor):
    """Restore old_email data on rollback."""
    User = apps.get_model('users', 'User')
    EmailArchive = apps.get_model('users', 'EmailArchive')

    for archive in EmailArchive.objects.all():
        User.objects.filter(id=archive.user_id).update(
            old_email=archive.email
        )

# Migration 2: Drop column (run after deployment)
class Migration(migrations.Migration):
    dependencies = [('users', '0002_archive_emails')]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='old_email',
        ),
    ]
```

## Safe Migration Patterns

### Pattern 1: Renaming Field (3 Steps)

**❌ UNSAFE:**
```python
operations = [
    migrations.RenameField('user', 'email', 'email_address'),  # ❌ Risky!
]
```

**✅ SAFE (3-Step):**
```python
# Step 1: Add new field
operations = [
    migrations.AddField('user', 'email_address',
                       models.EmailField(null=True))
]

# Step 2: Data migration (copy old → new)
operations = [
    migrations.RunPython(copy_email_to_email_address)
]

# Step 3: Drop old field (separate deployment)
operations = [
    migrations.RemoveField('user', 'email')
]
```

### Pattern 2: Changing Field Type (3 Steps)

**❌ UNSAFE:**
```python
operations = [
    migrations.AlterField('product', 'price',
                         models.DecimalField(max_digits=10, decimal_places=2))
]
```

**✅ SAFE:**
```python
# Step 1: Add new field with new type
operations = [
    migrations.AddField('product', 'price_decimal',
                       models.DecimalField(max_digits=10, decimal_places=2, null=True))
]

# Step 2: Data migration (convert & copy)
operations = [
    migrations.RunPython(convert_price_to_decimal)
]

# Step 3: Drop old field, rename new field
operations = [
    migrations.RemoveField('product', 'price'),
    migrations.RenameField('product', 'price_decimal', 'price')
]
```

### Pattern 3: Adding Non-Nullable Field (2 Steps)

**❌ UNSAFE:**
```python
operations = [
    migrations.AddField('user', 'organization',
                       models.ForeignKey('Organization'))  # ❌ No default!
]
```

**✅ SAFE:**
```python
# Step 1: Add as nullable
operations = [
    migrations.AddField('user', 'organization',
                       models.ForeignKey('Organization', null=True))
]

# Step 2: Populate + make non-nullable
operations = [
    migrations.RunPython(assign_default_organizations),
    migrations.AlterField('user', 'organization',
                         models.ForeignKey('Organization', null=False))
]
```

### Pattern 4: Adding Unique Constraint (Check First)

**❌ UNSAFE:**
```python
operations = [
    migrations.AlterField('user', 'email',
                         models.EmailField(unique=True))  # ❌ Fails if duplicates!
]
```

**✅ SAFE:**
```python
# Step 1: Check for duplicates
operations = [
    migrations.RunPython(check_and_fix_duplicate_emails)
]

# Step 2: Add unique constraint
operations = [
    migrations.AlterField('user', 'email',
                         models.EmailField(unique=True))
]
```

## Production-Safe Practices

### Use CONCURRENT Index Creation

```python
from django.db import migrations
from django.contrib.postgres.operations import AddIndexConcurrently

class Migration(migrations.Migration):
    atomic = False  # Required for CONCURRENT operations

    operations = [
        AddIndexConcurrently(
            model_name='user',
            index=models.Index(fields=['email'], name='user_email_idx')
        )
    ]
```

### Data Migration Template

```python
def forward_migration(apps, schema_editor):
    """
    Safe data migration with batching.
    """
    Model = apps.get_model('app', 'Model')
    batch_size = 1000

    total = Model.objects.count()
    for offset in range(0, total, batch_size):
        batch = Model.objects.all()[offset:offset + batch_size]
        for obj in batch:
            # Transform data
            obj.new_field = transform(obj.old_field)
            obj.save(update_fields=['new_field'])

def reverse_migration(apps, schema_editor):
    """
    Reverse the migration.
    """
    Model = apps.get_model('app', 'Model')
    Model.objects.all().update(new_field=None)

class Migration(migrations.Migration):
    operations = [
        migrations.RunPython(forward_migration, reverse_migration)
    ]
```

## Migration Testing Checklist

Before applying migration:

- ✅ Run on copy of production database
- ✅ Verify data integrity after migration
- ✅ Test rollback works
- ✅ Check migration duration (< 5 minutes ideal)
- ✅ Review SQL with `sqlmigrate`
- ✅ Confirm no downtime required
- ✅ Have rollback plan ready

## Validation Commands

Suggest running:

```bash
# Review SQL before applying
python manage.py sqlmigrate users 0002

# Check for issues
python manage.py makemigrations --check

# Dry run
python manage.py migrate --plan

# Apply to staging first
python manage.py migrate --database=staging
```

## Integration with CI/CD

```yaml
# .github/workflows/migrations.yml
- name: Check migrations safety
  run: |
    python manage.py makemigrations --check --dry-run --no-input
    python manage.py migrate --plan
```

## Success Criteria

✅ No data loss migrations
✅ All migrations tested on staging
✅ Rollback plan exists
✅ Large table migrations use CONCURRENT
✅ Data migrations properly batched
✅ Reversible migrations

## Behavior

**Proactive enforcement:**
- Analyze migrations without being asked
- Block unsafe migrations immediately
- Suggest safe 3-step patterns
- Generate data migration code
- Explain WHY the migration is risky

**Never:**
- Allow data loss migrations
- Let users skip safety checks
- Apply migrations without review
- Just warn without blocking unsafe operations

**When migration is unsafe:**
- Stop the process
- Explain the risk
- Provide safe alternative
- Generate corrected migration code
- User must acknowledge before proceeding
