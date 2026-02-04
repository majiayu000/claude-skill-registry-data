---
name: use-oadp-cli
description: Use the oadp-cli kubectl plugin for both cluster-admin backup/restore operations and namespace-scoped non-admin self-service backups.
---

# Use OADP CLI

This skill provides comprehensive guidance for using the **oadp-cli** kubectl plugin, which extends OADP functionality with unified CLI support for both administrative Velero operations and non-administrative namespace-scoped backup operations.

## When to Use This Skill

- **Admin Operations**: Performing cluster-wide backups and restores as a cluster administrator
- **Non-Admin Self-Service**: Creating namespace-scoped backups without cluster-admin permissions
- **Developer Workflows**: Empowering development teams to backup their own namespaces
- **Automation Scripts**: Integrating OADP backup operations into CI/CD pipelines
- **Quick Operations**: Faster than writing YAML for simple backup/restore tasks
- **Namespace Isolation**: When you need strict namespace-level backup isolation

## What This Skill Does

1. **Installs oadp-cli**: Sets up the kubectl plugin on your system
2. **Performs Admin Operations**: Executes cluster-wide backup, restore, and version commands
3. **Enables Non-Admin Backups**: Creates NonAdminBackup resources for namespace-scoped operations
4. **Manages Backup Approvals**: Handles NonAdminBackupStorageLocation requests
5. **Provides Unified Interface**: Single CLI for both admin and non-admin workflows

## How to Use

### Basic Usage

```
Install oadp-cli plugin
```

```
Create namespace backup using oadp-cli
```

### Admin Operations

```
Create cluster-wide backup with oadp-cli
```

```
Restore from backup using oadp-cli
```

### Non-Admin Operations

```
Create non-admin backup as developer
```

```
Check non-admin backup status
```

## Prerequisites

- [ ] OpenShift cluster with OADP operator installed
- [ ] kubectl/oc CLI installed
- [ ] Appropriate permissions:
  - **Admin operations**: cluster-admin or velero.io permissions
  - **Non-admin operations**: namespace developer/edit permissions
- [ ] For non-admin: OADP non-admin controller deployed
- [ ] For non-admin: NonAdminBackupStorageLocation configured and approved

## Examples

### Example 1: Install oadp-cli

**User**: "Install the OADP CLI plugin"

**Skill Actions**:

1. **Download and install**:
   ```bash
   # Clone the repository
   git clone https://github.com/migtools/oadp-cli.git
   cd oadp-cli

   # Build and install (auto-detects OADP namespace)
   make install

   # Refresh shell
   source ~/.zshrc  # or ~/.bashrc

   # Verify installation
   kubectl oadp --help
   ```

2. **Alternative: Manual installation with specific namespace**:
   ```bash
   # Build
   make build

   # Install to kubectl plugins directory
   mkdir -p ~/.kube/plugins
   cp kubectl-oadp ~/.kube/plugins/

   # Add to PATH (if not already)
   export PATH=$PATH:~/.kube/plugins

   # Set OADP namespace
   export VELERO_NAMESPACE=openshift-adp

   # Verify
   kubectl oadp version
   ```

3. **Check installation**:
   ```bash
   # List available commands
   kubectl oadp --help

   # Output should show:
   # kubectl oadp
   # ├── backup          # Admin: cluster-wide backups
   # ├── restore         # Admin: cluster-wide restores
   # ├── version         # Version information
   # ├── nabsl-request   # Manage NonAdminBackupStorageLocation requests
   # └── nonadmin (na)   # Non-admin namespace-scoped operations
   ```

**Success Indicators**:
- ✅ `kubectl oadp --help` displays command list
- ✅ `kubectl oadp version` shows OADP/Velero versions
- ✅ Plugin accessible from any directory

### Example 2: Admin Cluster-Wide Backup

**User**: "Create a backup of production namespaces using oadp-cli"

**Skill Actions**:

1. **Create backup**:
   ```bash
   # Backup specific namespaces
   kubectl oadp backup create prod-backup \
     --include-namespaces prod-frontend,prod-backend,prod-database

   # Alternative: Backup by label
   kubectl oadp backup create prod-env-backup \
     --selector env=production

   # Full cluster backup (all namespaces)
   kubectl oadp backup create full-cluster-backup \
     --include-cluster-resources
   ```

2. **Monitor backup progress**:
   ```bash
   # Describe backup
   kubectl oadp backup describe prod-backup

   # Watch status
   kubectl oadp backup get prod-backup -w

   # View logs
   kubectl oadp backup logs prod-backup
   ```

3. **List all backups**:
   ```bash
   # List backups
   kubectl oadp backup get

   # Filter by label
   kubectl oadp backup get --selector env=production
   ```

**Expected Output**:
```
NAME          STATUS      CREATED                         EXPIRES   STORAGE LOCATION   SELECTOR
prod-backup   Completed   2025-03-15 14:30:00 +0000 UTC   29d       default            <none>
```

### Example 3: Admin Restore Operation

**User**: "Restore from backup using oadp-cli"

**Skill Actions**:

1. **List available backups**:
   ```bash
   kubectl oadp backup get
   ```

2. **Create restore**:
   ```bash
   # Restore everything from backup
   kubectl oadp restore create --from-backup prod-backup

   # Restore specific namespace
   kubectl oadp restore create prod-restore \
     --from-backup prod-backup \
     --include-namespaces prod-frontend

   # Restore with namespace mapping
   kubectl oadp restore create disaster-recovery \
     --from-backup prod-backup \
     --namespace-mappings prod-frontend:dr-frontend,prod-backend:dr-backend
   ```

3. **Monitor restore**:
   ```bash
   # Describe restore
   kubectl oadp restore describe prod-restore

   # Watch progress
   kubectl oadp restore get prod-restore -w

   # View logs
   kubectl oadp restore logs prod-restore
   ```

**Expected Output**:
```
NAME           BACKUP        STATUS      STARTED                         COMPLETED                       ERRORS   WARNINGS
prod-restore   prod-backup   Completed   2025-03-15 15:00:00 +0000 UTC   2025-03-15 15:05:00 +0000 UTC   0        2
```

### Example 4: Non-Admin Namespace Backup

**User**: "As a developer, create a backup of my namespace"

**Skill Actions**:

1. **Verify non-admin setup**:
   ```bash
   # Check current namespace
   kubectl config view --minify -o jsonpath='{..namespace}'

   # Verify NonAdminBackupStorageLocation exists and is approved
   kubectl get nonAdminbackupstoragelocations -n openshift-adp

   # Expected: At least one NABSL with Accepted phase
   ```

2. **Create non-admin backup**:
   ```bash
   # Basic namespace backup (uses current namespace)
   kubectl oadp nonadmin backup create my-app-backup

   # Short form
   kubectl oadp na backup create my-app-backup

   # With specific resource filters
   kubectl oadp na backup create app-backup \
     --include-resources deployments,services,configmaps,secrets

   # Exclude specific resources
   kubectl oadp na backup create safe-backup \
     --exclude-resources secrets

   # With volume snapshots disabled
   kubectl oadp na backup create metadata-only \
     --snapshot-volumes=false

   # Create and wait for completion
   kubectl oadp na backup create prod-backup --wait
   ```

3. **Preview backup without creating**:
   ```bash
   # Generate YAML without creating
   kubectl oadp na backup create test-backup \
     --snapshot-volumes=false \
     -o yaml

   # Shows the NonAdminBackup resource that would be created
   ```

**Expected Output**:
```
NonAdminBackup "my-app-backup" created
```

### Example 5: Non-Admin Backup Operations

**User**: "Check status and manage my non-admin backups"

**Skill Actions**:

1. **List non-admin backups**:
   ```bash
   # List backups in current namespace
   kubectl oadp na backup get

   # Alternative: Direct resource query
   kubectl get nonadminbackups
   ```

2. **Describe specific backup**:
   ```bash
   # Detailed backup information
   kubectl oadp na backup describe my-app-backup

   # Shows:
   # - Backup phase (New, BackingOff, Created, Completed, Failed)
   # - Velero backup name (auto-generated)
   # - Included resources
   # - Storage location
   # - Errors/warnings
   ```

3. **View backup logs**:
   ```bash
   # Stream backup logs
   kubectl oadp na backup logs my-app-backup

   # Follow logs in real-time
   kubectl oadp na backup logs my-app-backup -f
   ```

4. **Delete backup**:
   ```bash
   # Delete non-admin backup (also deletes underlying Velero backup)
   kubectl oadp na backup delete my-app-backup

   # Confirm deletion
   kubectl oadp na backup get
   ```

**Output Examples**:

**List Output**:
```
NAME             PHASE       CREATED                         VELERO BACKUP
my-app-backup    Completed   2025-03-15 10:00:00 +0000 UTC   openshift-adp-my-ns-my-app-backup-abc123
```

**Describe Output**:
```
Name:         my-app-backup
Namespace:    my-namespace
Phase:        Completed
Created:      2025-03-15 10:00:00 +0000 UTC
Velero Backup: openshift-adp-my-ns-my-app-backup-abc123
Backup Status:
  Phase:              Completed
  Total Items:        42
  Items Backed Up:    42
  Storage Location:   nonadmin-bsl
```

### Example 6: NonAdminBackupStorageLocation Approval (Admin)

**User**: "As admin, approve a NonAdminBackupStorageLocation request"

**Skill Actions**:

1. **List NABSL requests**:
   ```bash
   # View all NonAdminBackupStorageLocation requests
   kubectl oadp nabsl-request get

   # Alternative
   kubectl get nonadminbackupstoragelocations -A
   ```

2. **Describe request details**:
   ```bash
   # Review request
   kubectl oadp nabsl-request describe my-namespace-bsl -n my-namespace

   # Shows:
   # - Requested BSL configuration
   # - Namespace
   # - Status (Pending, Accepted, Rejected)
   ```

3. **Approve NABSL**:
   ```bash
   # Patch to approve
   kubectl patch nonadminbackupstoragelocations my-namespace-bsl \
     -n my-namespace \
     --type merge \
     -p '{"status":{"phase":"Accepted"}}'

   # Verify approval
   kubectl get nonadminbackupstoragelocations my-namespace-bsl -n my-namespace
   ```

4. **Reject NABSL** (if needed):
   ```bash
   kubectl patch nonadminbackupstoragelocations my-namespace-bsl \
     -n my-namespace \
     --type merge \
     -p '{"status":{"phase":"Rejected","conditions":[{"type":"Rejected","status":"True","message":"BSL not approved - cost concerns"}]}}'
   ```

**Output**:
```
NAME              NAMESPACE      PHASE      BSL
my-namespace-bsl  my-namespace   Accepted   default
```

### Example 7: Non-Admin Workflow End-to-End

**User**: "Complete non-admin backup workflow from developer perspective"

**Skill Actions**:

1. **Developer: Switch to project namespace**:
   ```bash
   # Switch namespace
   kubectl config set-context --current --namespace=my-app

   # Verify current namespace
   kubectl config view --minify | grep namespace:
   ```

2. **Developer: Create backup**:
   ```bash
   # Create backup with all resources
   kubectl oadp na backup create daily-backup-$(date +%Y%m%d) --wait

   # Output: NonAdminBackup "daily-backup-20250315" created
   # Waiting for backup to complete...
   # Backup completed successfully
   ```

3. **Developer: Verify backup**:
   ```bash
   # Check backup status
   kubectl oadp na backup describe daily-backup-20250315

   # View what was backed up
   kubectl oadp na backup logs daily-backup-20250315 | grep "Backed up"
   ```

4. **Developer: Schedule regular backups** (via NonAdminBackup with schedule):
   ```bash
   # Note: Schedule functionality depends on OADP non-admin controller version
   # For manual approach, create script:
   cat << 'EOF' > create-daily-backup.sh
   #!/bin/bash
   kubectl oadp na backup create daily-backup-$(date +%Y%m%d) \
     --include-resources deployments,services,configmaps,persistentvolumeclaims
   EOF

   chmod +x create-daily-backup.sh

   # Add to cron for daily execution
   ```

5. **Developer: Clean up old backups**:
   ```bash
   # List old backups
   kubectl oadp na backup get

   # Delete backups older than 7 days (manual selection)
   kubectl oadp na backup delete daily-backup-20250308
   ```

### Example 8: Advanced Admin Operations

**User**: "Perform advanced backup operations with oadp-cli"

**Skill Actions**:

1. **Backup with hooks**:
   ```bash
   # For hooks, use direct YAML (oadp-cli doesn't support hooks via flags)
   cat <<EOF | kubectl apply -f -
   apiVersion: velero.io/v1
   kind: Backup
   metadata:
     name: postgres-with-hooks
     namespace: openshift-adp
   spec:
     includedNamespaces:
       - postgres-db
     hooks:
       resources:
         - name: db-dump
           includedNamespaces:
             - postgres-db
           pre:
             - exec:
                 command:
                   - /bin/bash
                   - -c
                   - pg_dump > /tmp/backup.sql
EOF

   # Monitor via oadp-cli
   kubectl oadp backup describe postgres-with-hooks
   ```

2. **Backup to specific storage location**:
   ```bash
   # For multiple BSLs, use YAML or velero CLI directly
   # oadp-cli uses default BSL

   # Check available BSLs
   kubectl get backupstoragelocations -n openshift-adp

   # Use velero for advanced BSL selection
   velero backup create offsite --storage-location secondary-bsl
   ```

3. **Check OADP version**:
   ```bash
   kubectl oadp version

   # Output shows:
   # Client Version: vX.Y.Z
   # Velero Version: vX.Y.Z
   # OADP Operator Version: vX.Y.Z
   ```

## Command Reference

### Admin Commands

| Command | Description | Example |
|---------|-------------|---------|
| `kubectl oadp backup create` | Create cluster backup | `kubectl oadp backup create prod --include-namespaces prod-*` |
| `kubectl oadp backup get` | List backups | `kubectl oadp backup get` |
| `kubectl oadp backup describe` | Describe backup | `kubectl oadp backup describe prod` |
| `kubectl oadp backup logs` | View backup logs | `kubectl oadp backup logs prod -f` |
| `kubectl oadp backup delete` | Delete backup | `kubectl oadp backup delete prod` |
| `kubectl oadp restore create` | Create restore | `kubectl oadp restore create --from-backup prod` |
| `kubectl oadp restore get` | List restores | `kubectl oadp restore get` |
| `kubectl oadp restore describe` | Describe restore | `kubectl oadp restore describe prod-restore` |
| `kubectl oadp restore logs` | View restore logs | `kubectl oadp restore logs prod-restore` |
| `kubectl oadp version` | Show versions | `kubectl oadp version` |

### Non-Admin Commands

| Command | Description | Example |
|---------|-------------|---------|
| `kubectl oadp na backup create` | Create namespace backup | `kubectl oadp na backup create my-backup` |
| `kubectl oadp na backup get` | List namespace backups | `kubectl oadp na backup get` |
| `kubectl oadp na backup describe` | Describe backup | `kubectl oadp na backup describe my-backup` |
| `kubectl oadp na backup logs` | View backup logs | `kubectl oadp na backup logs my-backup` |
| `kubectl oadp na backup delete` | Delete backup | `kubectl oadp na backup delete my-backup` |

### Common Flags

| Flag | Description | Applies To |
|------|-------------|------------|
| `--include-namespaces` | Namespaces to backup | Admin backup |
| `--exclude-namespaces` | Namespaces to exclude | Admin backup |
| `--include-resources` | Resource types to include | Both |
| `--exclude-resources` | Resource types to exclude | Both |
| `--selector` | Label selector | Admin backup |
| `--snapshot-volumes` | Enable volume snapshots | Non-admin backup |
| `--wait` | Wait for completion | Non-admin backup |
| `-o yaml` | Output YAML | Non-admin backup |
| `-f` | Follow logs | Logs commands |

## How Non-Admin Backups Work

### Architecture

```
Developer Namespace: my-app
  └─> NonAdminBackup CR (created by developer)
       └─> OADP Non-Admin Controller
            └─> Velero Backup CR (auto-created in openshift-adp)
                 └─> Velero Server
                      └─> Backup Storage Location
```

### RBAC Requirements

**For Developers (Non-Admin Users)**:
```yaml
# Permissions needed in their namespace:
- apiGroups: ["oadp.openshift.io"]
  resources: ["nonadminbackups"]
  verbs: ["create", "get", "list", "delete"]
```

**For Cluster Admins**:
```yaml
# Full access to all OADP resources:
- apiGroups: ["oadp.openshift.io", "velero.io"]
  resources: ["*"]
  verbs: ["*"]
```

### NonAdminBackupStorageLocation Setup

Before developers can create backups, admin must configure NABSL:

```yaml
apiVersion: oadp.openshift.io/v1alpha1
kind: NonAdminBackupStorageLocation
metadata:
  name: nonadmin-bsl
  namespace: my-app-namespace
spec:
  backupStorageLocationReference:
    name: default  # References BSL in openshift-adp
  namespaces:
    - my-app-namespace
```

Admin approves:
```bash
kubectl patch nonadminbackupstoragelocations nonadmin-bsl \
  -n my-app-namespace \
  --type merge \
  -p '{"status":{"phase":"Accepted"}}'
```

## Troubleshooting

### oadp-cli Not Found

**Symptoms**: `kubectl: unknown command "oadp"`

**Fix**:
```bash
# Verify installation
ls -la ~/.kube/plugins/kubectl-oadp

# Reinstall if needed
cd oadp-cli
make install
source ~/.zshrc  # or restart terminal

# Check PATH
echo $PATH | grep -o '[^:]*kube[^:]*'
```

### Non-Admin Backup Fails - No NABSL

**Symptoms**: NonAdminBackup stuck in "BackingOff" phase

**Diagnosis**:
```bash
# Check NonAdminBackup status
kubectl describe nonadminbackups my-backup

# Look for error:
# Error: no valid NonAdminBackupStorageLocation found
```

**Fix**:
```bash
# Admin: Create and approve NABSL
kubectl apply -f nonadmin-bsl.yaml
kubectl patch nonadminbackupstoragelocations nonadmin-bsl -n <namespace> --type merge -p '{"status":{"phase":"Accepted"}}'

# Developer: Retry backup
kubectl oadp na backup delete my-backup
kubectl oadp na backup create my-backup
```

### Non-Admin Backup Not Creating Velero Backup

**Symptoms**: NonAdminBackup exists but no Velero backup created

**Diagnosis**:
```bash
# Check OADP non-admin controller logs
kubectl logs -n openshift-adp -l app.kubernetes.io/name=oadp-non-admin-controller

# Check NonAdminBackup status
kubectl get nonadminbackups my-backup -o yaml
```

**Common Causes**:
- OADP non-admin controller not running
- NABSL not approved
- Invalid resource filters

**Fix**:
```bash
# Verify controller running
kubectl get pods -n openshift-adp -l app.kubernetes.io/name=oadp-non-admin-controller

# Check controller logs for errors
kubectl logs -n openshift-adp -l app.kubernetes.io/name=oadp-non-admin-controller | grep -i error
```

## Best Practices

1. **Use Meaningful Names**
   ```bash
   # Good
   kubectl oadp na backup create myapp-prod-20250315

   # Avoid
   kubectl oadp na backup create backup1
   ```

2. **Namespace Isolation for Non-Admin**
   - One NonAdminBackupStorageLocation per namespace or team
   - Prevents cross-namespace backup access
   - Easier quota and access management

3. **Regular Backup Schedules**
   ```bash
   # Create script for automation
   #!/bin/bash
   kubectl oadp na backup create daily-$(date +%Y%m%d)
   ```

4. **Cleanup Old Backups**
   ```bash
   # List and manually delete old backups
   kubectl oadp na backup get
   kubectl oadp na backup delete old-backup-name
   ```

5. **Verify Backups**
   ```bash
   # Always check backup completed
   kubectl oadp na backup describe my-backup | grep Phase
   ```

## Comparison: oadp-cli vs velero CLI vs YAML

| Feature | oadp-cli | velero CLI | YAML |
|---------|----------|------------|------|
| Admin backups | ✅ | ✅ | ✅ |
| Non-admin backups | ✅ | ❌ | ✅ |
| Hooks support | ❌ (use YAML) | ✅ | ✅ |
| Multiple BSL | ❌ (use velero) | ✅ | ✅ |
| Ease of use | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| Non-admin RBAC | ✅ Native | ❌ | ✅ |

**Recommendation**: Use oadp-cli for simple admin operations and all non-admin operations. Use velero CLI or YAML for advanced features like hooks and multiple BSLs.

## Next Steps

After using oadp-cli:

1. **Automate Backups**: Create scripts for regular backup operations
2. **Set Up Non-Admin**: Enable self-service backups for development teams
3. **Monitor Backups**: Track backup success rates and sizes
4. **Test Restores**: Verify backups can be restored successfully
5. **Document Workflows**: Create runbooks for your team

**Related Skills**:
- install-oadp - Install OADP operator
- create-backup - Advanced backup creation
- diagnose-with-must-gather - Troubleshoot backup issues

## Resources

- **OADP CLI GitHub**: https://github.com/migtools/oadp-cli
- **NonAdmin Documentation**: https://github.com/migtools/oadp-non-admin
- **Velero CLI Reference**: https://velero.io/docs/latest/velero-cli/

---

**Version**: 1.0
**Last Updated**: 2025-11-17
**Compatibility**: OADP 1.3+, OpenShift 4.12+, oadp-cli latest
**NOTE**: Non-admin functionality requires OADP non-admin controller deployed
