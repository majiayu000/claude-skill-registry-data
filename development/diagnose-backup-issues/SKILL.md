---
name: diagnose-backup-issues
description: Comprehensive diagnostic tool for troubleshooting OADP/Velero backup and restore problems with automated checks and recommendations.
---

# Diagnose OADP Backup/Restore Issues

This skill provides automated diagnostics for OADP and Velero backup/restore issues with actionable recommendations.

## When to Use This Skill

- Backup stuck or failing
- Restore not completing
- Performance problems
- Configuration validation
- Pre-deployment health check
- Troubleshooting unknown issues

## What This Skill Does

1. **Environment Check**: Validates OADP installation
2. **Configuration Analysis**: Reviews DPA and BSL/VSL configs
3. **Resource Health**: Checks pod status, logs
4. **Network Connectivity**: Tests object storage access
5. **Permission Validation**: Verifies RBAC and credentials
6. **Issue Detection**: Identifies common problems
7. **Recommendations**: Provides fix suggestions

## How to Use

```
Diagnose OADP installation
```

```
Check why backup <name> is failing
```

```
Diagnose restore issues for <restore-name>
```

## Diagnostic Checks

### 1. Installation Health

```bash
#!/bin/bash
echo "=== OADP Installation Health Check ==="

# Check namespace
echo "Checking openshift-adp namespace..."
oc get namespace openshift-adp || {
    echo "ERROR: Namespace openshift-adp not found"
    exit 1
}

# Check operator
echo "Checking OADP operator..."
oc get csv -n openshift-adp | grep oadp-operator || {
    echo "ERROR: OADP operator not installed"
    exit 1
}

# Check operator pod
echo "Checking operator pod..."
oc get pods -n openshift-adp -l app.kubernetes.io/name=oadp-operator
oc wait --for=condition=ready pod \
    -l app.kubernetes.io/name=oadp-operator \
    -n openshift-adp --timeout=30s || {
    echo "ERROR: Operator pod not ready"
    oc logs -n openshift-adp -l app.kubernetes.io/name=oadp-operator --tail=50
}

# Check DPA
echo "Checking DataProtectionApplication..."
oc get dpa -n openshift-adp || {
    echo "ERROR: No DPA found"
    exit 1
}

# Check Velero
echo "Checking Velero deployment..."
oc get deployment velero -n openshift-adp || {
    echo "ERROR: Velero deployment not found"
    exit 1
}

oc wait --for=condition=ready pod \
    -l app.kubernetes.io/name=velero \
    -n openshift-adp --timeout=30s || {
    echo "ERROR: Velero pod not ready"
    oc logs -n openshift-adp deployment/velero --tail=50
}

# Check Restic (if enabled)
if oc get dpa -n openshift-adp -o jsonpath='{.items[0].spec.configuration.restic.enable}' | grep -q true; then
    echo "Checking Restic daemonset..."
    oc get ds restic -n openshift-adp || {
        echo "WARNING: Restic enabled but daemonset not found"
    }

    RESTIC_DESIRED=$(oc get ds restic -n openshift-adp -o jsonpath='{.status.desiredNumberScheduled}')
    RESTIC_READY=$(oc get ds restic -n openshift-adp -o jsonpath='{.status.numberReady}')

    if [ "$RESTIC_DESIRED" != "$RESTIC_READY" ]; then
        echo "WARNING: Restic not ready on all nodes ($RESTIC_READY/$RESTIC_DESIRED)"
        oc get pods -n openshift-adp -l name=restic
    fi
fi

echo "✓ Installation health check passed"
```

### 2. Storage Location Validation

```bash
#!/bin/bash
echo "=== Storage Location Validation ==="

# Check BSL
echo "Checking BackupStorageLocations..."
BSL_COUNT=$(oc get backupstoragelocations -n openshift-adp --no-headers | wc -l)
if [ "$BSL_COUNT" -eq 0 ]; then
    echo "ERROR: No BackupStorageLocation found"
    exit 1
fi

oc get backupstoragelocations -n openshift-adp

# Check BSL phase
BSL_PHASE=$(oc get backupstoragelocations default -n openshift-adp -o jsonpath='{.status.phase}')
if [ "$BSL_PHASE" != "Available" ]; then
    echo "ERROR: BSL not available (Phase: $BSL_PHASE)"

    echo "Checking BSL configuration..."
    oc get backupstoragelocations default -n openshift-adp -o yaml

    echo "Checking credentials..."
    CRED_NAME=$(oc get backupstoragelocations default -n openshift-adp -o jsonpath='{.spec.credential.name}')
    oc get secret $CRED_NAME -n openshift-adp || {
        echo "ERROR: Credential secret not found"
    }

    echo "Recent Velero logs:"
    oc logs -n openshift-adp deployment/velero --tail=100 | grep -i "backupstoragelocation\|bsl"
    exit 1
fi

echo "✓ Storage locations validated"
```

### 3. Network Connectivity

```bash
#!/bin/bash
echo "=== Network Connectivity Check ==="

# Get BSL details
BSL_PROVIDER=$(oc get backupstoragelocations default -n openshift-adp -o jsonpath='{.spec.provider}')
BSL_BUCKET=$(oc get backupstoragelocations default -n openshift-adp -o jsonpath='{.spec.objectStorage.bucket}')
BSL_REGION=$(oc get backupstoragelocations default -n openshift-adp -o jsonpath='{.spec.config.region}')

echo "Provider: $BSL_PROVIDER"
echo "Bucket: $BSL_BUCKET"
echo "Region: $BSL_REGION"

# Test connectivity from Velero pod
echo "Testing object storage connectivity..."
case $BSL_PROVIDER in
    aws)
        ENDPOINT="https://s3.$BSL_REGION.amazonaws.com"
        ;;
    gcp)
        ENDPOINT="https://storage.googleapis.com"
        ;;
    azure)
        ENDPOINT="https://${BSL_BUCKET}.blob.core.windows.net"
        ;;
esac

echo "Testing connection to $ENDPOINT..."
oc exec -n openshift-adp deployment/velero -- curl -I --max-time 10 $ENDPOINT || {
    echo "ERROR: Cannot reach object storage endpoint"
    echo "Checking proxy configuration..."
    oc get proxy cluster -o yaml
    echo "Checking network policies..."
    oc get networkpolicies -n openshift-adp
    exit 1
}

echo "✓ Network connectivity validated"
```

### 4. Backup Diagnosis

```bash
#!/bin/bash
BACKUP_NAME=$1

echo "=== Diagnosing Backup: $BACKUP_NAME ==="

# Check backup exists
oc get backup $BACKUP_NAME -n openshift-adp || {
    echo "ERROR: Backup not found"
    exit 1
}

# Get backup phase
PHASE=$(oc get backup $BACKUP_NAME -n openshift-adp -o jsonpath='{.status.phase}')
echo "Backup Phase: $PHASE"

case $PHASE in
    "New"|"InProgress")
        echo "Backup is in progress..."

        # Check how long it's been running
        START_TIME=$(oc get backup $BACKUP_NAME -n openshift-adp -o jsonpath='{.status.startTimestamp}')
        echo "Started at: $START_TIME"

        # Check for stuck resources
        echo "Recent backup activity:"
        velero backup logs $BACKUP_NAME --tail=50

        # Check Restic if enabled
        if oc get backup $BACKUP_NAME -n openshift-adp -o jsonpath='{.spec.defaultVolumesToFsBackup}' | grep -q true; then
            echo "Checking Restic pod logs..."
            oc logs -n openshift-adp ds/restic --tail=50 | grep $BACKUP_NAME
        fi

        # Check for volume snapshots
        if oc get backup $BACKUP_NAME -n openshift-adp -o jsonpath='{.spec.snapshotVolumes}' | grep -q true; then
            echo "Checking VolumeSnapshots..."
            NAMESPACE=$(oc get backup $BACKUP_NAME -n openshift-adp -o jsonpath='{.spec.includedNamespaces[0]}')
            oc get volumesnapshots -n $NAMESPACE
        fi
        ;;

    "Completed")
        echo "✓ Backup completed successfully"

        # Show summary
        velero backup describe $BACKUP_NAME | grep -A 10 "Resource List"

        # Check for warnings
        WARNINGS=$(velero backup describe $BACKUP_NAME | grep -c "Warnings:")
        if [ "$WARNINGS" -gt 0 ]; then
            echo "WARNING: Backup has warnings"
            velero backup describe $BACKUP_NAME | grep -A 20 "Warnings:"
        fi
        ;;

    "PartiallyFailed")
        echo "WARNING: Backup partially failed"

        # Show errors
        velero backup describe $BACKUP_NAME | grep -A 30 "Errors:\|Warnings:"

        # Get logs
        echo "Backup logs:"
        velero backup logs $BACKUP_NAME | grep -i "error\|warning"
        ;;

    "Failed")
        echo "ERROR: Backup failed"

        # Show error details
        velero backup describe $BACKUP_NAME --details

        # Get logs
        echo "Backup logs:"
        velero backup logs $BACKUP_NAME

        # Check common issues
        echo "Checking common failure causes..."

        # BSL available?
        BSL_PHASE=$(oc get backupstoragelocations default -n openshift-adp -o jsonpath='{.status.phase}')
        if [ "$BSL_PHASE" != "Available" ]; then
            echo "ISSUE: BackupStorageLocation not available"
        fi

        # Check Velero logs
        echo "Recent Velero logs:"
        oc logs -n openshift-adp deployment/velero --tail=100 | grep -i error
        ;;
esac
```

### 5. Restore Diagnosis

```bash
#!/bin/bash
RESTORE_NAME=$1

echo "=== Diagnosing Restore: $RESTORE_NAME ==="

# Check restore exists
oc get restore $RESTORE_NAME -n openshift-adp || {
    echo "ERROR: Restore not found"
    exit 1
}

# Get restore phase
PHASE=$(oc get restore $RESTORE_NAME -n openshift-adp -o jsonpath='{.status.phase}')
echo "Restore Phase: $PHASE"

# Get backup name
BACKUP_NAME=$(oc get restore $RESTORE_NAME -n openshift-adp -o jsonpath='{.spec.backupName}')
echo "Backup: $BACKUP_NAME"

# Get namespace
NAMESPACE=$(oc get restore $RESTORE_NAME -n openshift-adp -o jsonpath='{.spec.includedNamespaces[0]}')
echo "Namespace: $NAMESPACE"

case $PHASE in
    "InProgress")
        echo "Restore in progress..."

        # Check logs
        velero restore logs $RESTORE_NAME --tail=50

        # Check namespace resources
        if [ -n "$NAMESPACE" ]; then
            echo "Resources in namespace:"
            oc get all -n $NAMESPACE
        fi
        ;;

    "Completed")
        echo "✓ Restore completed"

        # Check for warnings
        WARNINGS=$(velero restore describe $RESTORE_NAME | grep -c "Warnings:")
        if [ "$WARNINGS" -gt 0 ]; then
            echo "WARNING: Restore has warnings"
            velero restore describe $RESTORE_NAME | grep -A 20 "Warnings:"
        fi

        # Verify pods running
        if [ -n "$NAMESPACE" ]; then
            echo "Checking pod status..."
            oc get pods -n $NAMESPACE

            NOT_RUNNING=$(oc get pods -n $NAMESPACE --no-headers | grep -v "Running\|Completed" | wc -l)
            if [ "$NOT_RUNNING" -gt 0 ]; then
                echo "WARNING: Some pods not running"
                oc get pods -n $NAMESPACE | grep -v "Running\|Completed"
            fi

            # Check PVCs
            echo "Checking PVCs..."
            oc get pvc -n $NAMESPACE

            NOT_BOUND=$(oc get pvc -n $NAMESPACE --no-headers | grep -v "Bound" | wc -l)
            if [ "$NOT_BOUND" -gt 0 ]; then
                echo "WARNING: Some PVCs not bound"
                oc get pvc -n $NAMESPACE | grep -v "Bound"

                # Show PVC details
                oc get pvc -n $NAMESPACE -o wide
            fi
        fi
        ;;

    "PartiallyFailed"|"Failed")
        echo "ERROR: Restore failed"

        # Show details
        velero restore describe $RESTORE_NAME --details

        # Get logs
        velero restore logs $RESTORE_NAME | grep -i "error\|warning"

        # Check for common issues
        echo "Checking common issues..."

        # Namespace exists?
        if [ -n "$NAMESPACE" ]; then
            oc get namespace $NAMESPACE || {
                echo "ISSUE: Target namespace doesn't exist"
            }
        fi

        # Storage class issues?
        echo "Checking storage classes..."
        oc get storageclass

        # Recent events
        if [ -n "$NAMESPACE" ]; then
            echo "Recent events in namespace:"
            oc get events -n $NAMESPACE --sort-by='.lastTimestamp' | tail -20
        fi
        ;;
esac
```

### Data Mover Diagnostics

```bash
#!/bin/bash
# Diagnose Data Mover issues

echo "=== Data Mover Diagnostics ==="

# Check if Data Mover is enabled
echo "Checking Data Mover configuration..."
oc get dpa -n openshift-adp -o yaml | grep -A10 dataMover

# Check DataMover CRs
echo -e "\nDataMover Custom Resources:"
oc get datamovers -A

# Check for stuck DataMover CRs
echo -e "\nStuck DataMover CRs (>1 hour in InProgress):"
oc get datamovers -A -o json | jq -r '.items[] | select(.status.phase=="InProgress") | select((.metadata.creationTimestamp | fromdateiso8601) < (now - 3600)) | "\(.metadata.namespace)/\(.metadata.name) - Created: \(.metadata.creationTimestamp)"'

# Check Data Mover pods
echo -e "\nData Mover pods:"
oc get pods -n openshift-adp -l component=datamover

# Check Data Mover pod logs
DM_POD=$(oc get pods -n openshift-adp -l component=datamover -o jsonpath='{.items[0].metadata.name}' 2>/dev/null)
if [ -n "$DM_POD" ]; then
    echo -e "\nRecent Data Mover pod logs:"
    oc logs -n openshift-adp $DM_POD --tail=50 | grep -i "error\|fail\|warn" || echo "No errors/warnings found"
fi

# Check VolumeSnapshots related to Data Mover
echo -e "\nVolumeSnapshots for Data Mover backups:"
oc get volumesnapshots -A -l oadp.openshift.io/datamover=true

# Check Restic repository connectivity
echo -e "\nChecking Restic repository access..."
oc exec -n openshift-adp deployment/velero -- restic -r $(oc get backupstoragelocations -n openshift-adp -o jsonpath='{.items[0].spec.objectStorage.bucket}') snapshots 2>&1 | head -10

# Common Data Mover issues
echo -e "\n=== Common Data Mover Issues ==="
echo "1. Snapshot not ready - Check VolumeSnapshot status"
echo "2. Restic repository inaccessible - Verify BSL and credentials"
echo "3. Resource limits - Check Data Mover pod memory/CPU"
echo "4. Timeout - Large volumes may need increased backup timeout"
```

### etcd Backup Checks

```bash
#!/bin/bash
# Check etcd backup health

echo "=== etcd Backup Diagnostics ==="

# Check etcd pods health
echo "etcd Pod Status:"
oc get pods -n openshift-etcd -l app=etcd

# Check etcd member health
echo -e "\netcd Member Health:"
ETCD_POD=$(oc get pods -n openshift-etcd -l app=etcd -o jsonpath='{.items[0].metadata.name}')
if [ -n "$ETCD_POD" ]; then
    oc exec -n openshift-etcd $ETCD_POD -- etcdctl member list -w table
    echo -e "\netcd Endpoint Health:"
    oc exec -n openshift-etcd $ETCD_POD -- etcdctl endpoint health -w table
else
    echo "ERROR: No etcd pods found"
fi

# Check etcd disk space
echo -e "\netcd Disk Usage:"
if [ -n "$ETCD_POD" ]; then
    oc exec -n openshift-etcd $ETCD_POD -- df -h /var/lib/etcd
    echo -e "\netcd Data Size:"
    oc exec -n openshift-etcd $ETCD_POD -- du -sh /var/lib/etcd
fi

# Check for etcd snapshot backups
echo -e "\netcd Snapshot Backups (if configured):"
# Check if automated etcd backups are configured
oc get cronjobs -A | grep etcd-backup || echo "No automated etcd backup CronJobs found"

# Check etcd cluster operator
echo -e "\netcd Cluster Operator Status:"
oc get co etcd -o yaml | grep -A5 "conditions:"

# Check recent etcd logs for errors
echo -e "\nRecent etcd errors:"
if [ -n "$ETCD_POD" ]; then
    oc logs -n openshift-etcd $ETCD_POD --tail=100 | grep -i "error\|fail\|warn" | tail -20 || echo "No recent errors found"
fi

# Recommendations
echo -e "\n=== etcd Backup Recommendations ==="
echo "1. Create manual etcd snapshots regularly using cluster-backup.sh"
echo "2. Store etcd snapshots off-cluster in secure location"
echo "3. Test etcd restore procedure in non-production"
echo "4. Monitor etcd disk space - warn at 80%, critical at 90%"
echo "5. Keep at least 3 recent etcd snapshots for recovery options"
```

### Multi-Location (BSL/VSL) Diagnostics

```bash
#!/bin/bash
# Diagnose multi-location backup issues

echo "=== Multi-Location Backup Diagnostics ==="

# List all BackupStorageLocations
echo "BackupStorageLocations:"
oc get backupstoragelocations -n openshift-adp -o custom-columns=NAME:.metadata.name,PHASE:.status.phase,DEFAULT:.spec.default,PROVIDER:.spec.provider,BUCKET:.spec.objectStorage.bucket,REGION:.spec.config.region

# Check BSL health
echo -e "\nBSL Health Details:"
for bsl in $(oc get backupstoragelocations -n openshift-adp -o jsonpath='{.items[*].metadata.name}'); do
    echo -e "\n--- BSL: $bsl ---"
    oc get backupstoragelocations -n openshift-adp $bsl -o yaml | grep -A10 "status:"
done

# Identify default BSL
echo -e "\nDefault BSL:"
oc get backupstoragelocations -n openshift-adp -o jsonpath='{.items[?(@.spec.default==true)].metadata.name}' || echo "No default BSL configured!"

# Check for BSL failover configuration
echo -e "\nBSL Validation Frequency:"
oc get dpa -n openshift-adp -o yaml | grep -i validationFrequency || echo "Not configured - using default"

# List all VolumeSnapshotLocations
echo -e "\nVolumeSnapshotLocations:"
oc get volumesnapshotlocations -n openshift-adp -o custom-columns=NAME:.metadata.name,PROVIDER:.spec.provider,REGION:.spec.config.region

# Check backups per BSL
echo -e "\nBackups per Storage Location:"
velero backup get -o json | jq -r '.items | group_by(.spec.storageLocation) | .[] | "\(.[0].spec.storageLocation): \(length) backups"'

# Check for cross-region snapshot support
echo -e "\nVolumeSnapshotClasses for cross-region:"
oc get volumesnapshotclass -o custom-columns=NAME:.metadata.name,DRIVER:.driver,DELETION:.deletionPolicy

# Common multi-location issues
echo -e "\n=== Common Multi-Location Issues ==="
echo "1. Wrong BSL selected - Verify backup.spec.storageLocation"
echo "2. BSL unavailable - Check credentials and network connectivity"
echo "3. VSL region mismatch - Ensure VSL matches PVC region"
echo "4. Failover not working - Enable BSL validation frequency"
echo "5. Cross-region restore - May require Data Mover or manual snapshot copy"

# BSL connectivity tests
echo -e "\n=== Testing BSL Connectivity ==="
for bsl in $(oc get backupstoragelocations -n openshift-adp -o jsonpath='{.items[*].metadata.name}'); do
    echo -e "\nTesting BSL: $bsl"

    # Get BSL endpoint
    ENDPOINT=$(oc get backupstoragelocations -n openshift-adp $bsl -o jsonpath='{.spec.config.s3Url}')
    BUCKET=$(oc get backupstoragelocations -n openshift-adp $bsl -o jsonpath='{.spec.objectStorage.bucket}')

    if [ -n "$ENDPOINT" ]; then
        echo "  Endpoint: $ENDPOINT"
        echo "  Bucket: $BUCKET"

        # Test from Velero pod
        oc exec -n openshift-adp deployment/velero -- curl -I -m 5 $ENDPOINT 2>&1 | head -5 || echo "  WARNING: Cannot reach endpoint"
    else
        echo "  Using cloud provider default endpoint"
    fi
done

# Check for snapshot location conflicts
echo -e "\n=== Snapshot Location Analysis ==="
echo "PVCs and their storage classes:"
oc get pvc -A -o custom-columns=NAMESPACE:.metadata.namespace,NAME:.metadata.name,STORAGECLASS:.spec.storageClassName,VOLUMENAME:.spec.volumeName | head -20

# Recommendations
echo -e "\n=== Multi-Location Recommendations ==="
echo "1. Configure at least 2 BSLs for redundancy (different regions/providers)"
echo "2. Set validation frequency for automatic BSL health checks"
echo "3. Match VSL regions with PVC locations for optimal snapshot performance"
echo "4. Test cross-BSL restore procedures regularly"
echo "5. Document which applications use which BSLs/VSLs"
echo "6. Monitor BSL storage usage and set up alerting"
```

## Comprehensive Diagnostic Report

```bash
#!/bin/bash
# Generate full diagnostic report

OUTPUT_DIR="/tmp/oadp-diagnostics-$(date +%Y%m%d-%H%M%S)"
mkdir -p $OUTPUT_DIR

echo "Generating OADP diagnostic report in $OUTPUT_DIR..."

# System info
echo "=== System Information ===" > $OUTPUT_DIR/system-info.txt
oc version >> $OUTPUT_DIR/system-info.txt
oc get nodes >> $OUTPUT_DIR/system-info.txt

# OADP installation
echo "=== OADP Installation ===" > $OUTPUT_DIR/oadp-install.txt
oc get csv -n openshift-adp >> $OUTPUT_DIR/oadp-install.txt
oc get dpa -n openshift-adp -o yaml >> $OUTPUT_DIR/oadp-install.txt

# Pods and resources
oc get all -n openshift-adp > $OUTPUT_DIR/oadp-resources.txt

# Storage locations
oc get backupstoragelocations,volumesnapshotlocations -n openshift-adp -o yaml > $OUTPUT_DIR/storage-locations.yaml

# Backups and restores
oc get backups,restores -n openshift-adp > $OUTPUT_DIR/backups-restores.txt

# Logs
oc logs -n openshift-adp deployment/oadp-operator-controller-manager --tail=500 > $OUTPUT_DIR/operator-logs.txt
oc logs -n openshift-adp deployment/velero --tail=500 > $OUTPUT_DIR/velero-logs.txt

if oc get ds restic -n openshift-adp &>/dev/null; then
    oc logs -n openshift-adp ds/restic --tail=500 > $OUTPUT_DIR/restic-logs.txt
fi

# Events
oc get events -n openshift-adp --sort-by='.lastTimestamp' > $OUTPUT_DIR/events.txt

# Volume snapshots (cluster-wide)
oc get volumesnapshots -A -o yaml > $OUTPUT_DIR/volumesnapshots.yaml 2>/dev/null

# Create tarball
tar -czf $OUTPUT_DIR.tar.gz -C /tmp $(basename $OUTPUT_DIR)

echo "Diagnostic report created: $OUTPUT_DIR.tar.gz"
```

## Automated Issue Detection

```python
#!/usr/bin/env python3
# oadp-health-check.py

import subprocess
import json
import sys

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout, result.returncode

def check_oadp_health():
    issues = []
    warnings = []

    # Check OADP operator
    out, code = run_cmd("oc get csv -n openshift-adp -o json")
    if code != 0:
        issues.append("OADP operator not installed")
        return issues, warnings

    # Check DPA
    out, code = run_cmd("oc get dpa -n openshift-adp -o json")
    if code != 0 or not json.loads(out).get('items'):
        issues.append("No DataProtectionApplication found")
        return issues, warnings

    # Check Velero pod
    out, code = run_cmd("oc get pods -n openshift-adp -l app.kubernetes.io/name=velero -o json")
    pods = json.loads(out).get('items', [])
    if not pods:
        issues.append("Velero pod not found")
    else:
        for pod in pods:
            status = pod['status']['phase']
            if status != 'Running':
                issues.append(f"Velero pod not running: {status}")

    # Check BSL
    out, code = run_cmd("oc get backupstoragelocations default -n openshift-adp -o json")
    if code == 0:
        bsl = json.loads(out)
        phase = bsl.get('status', {}).get('phase')
        if phase != 'Available':
            issues.append(f"BackupStorageLocation not available: {phase}")
    else:
        issues.append("No default BackupStorageLocation found")

    # Check for failed backups
    out, code = run_cmd("oc get backups -n openshift-adp -o json")
    if code == 0:
        backups = json.loads(out).get('items', [])
        for backup in backups:
            phase = backup.get('status', {}).get('phase')
            if phase in ['Failed', 'PartiallyFailed']:
                warnings.append(f"Backup {backup['metadata']['name']} is {phase}")

    return issues, warnings

if __name__ == "__main__":
    issues, warnings = check_oadp_health()

    if issues:
        print("❌ Issues found:")
        for issue in issues:
            print(f"  - {issue}")
        sys.exit(1)

    if warnings:
        print("⚠️  Warnings:")
        for warning in warnings:
            print(f"  - {warning}")

    if not issues and not warnings:
        print("✅ OADP health check passed")

    sys.exit(0)
```

## Quick Diagnostics Commands

```bash
# One-liner health check
oc get dpa,bsl,vsl,backup,restore -n openshift-adp

# Check all OADP pods
oc get pods -n openshift-adp

# Recent errors
oc logs -n openshift-adp deployment/velero --tail=100 | grep -i error

# Storage location status
oc get bsl -n openshift-adp -o custom-columns=NAME:.metadata.name,PHASE:.status.phase,LAST-VALIDATED:.status.lastValidationTime

# Recent backups
velero backup get

# Failed backups
oc get backups -n openshift-adp -o json | jq -r '.items[] | select(.status.phase=="Failed" or .status.phase=="PartiallyFailed") | .metadata.name'
```

## Next Steps

Based on diagnosis results:
- Fix identified issues
- Review recommendations
- Test fixes with new backup
- Document recurring issues
- Update runbooks
