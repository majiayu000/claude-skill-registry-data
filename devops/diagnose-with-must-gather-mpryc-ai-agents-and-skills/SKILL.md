---
name: diagnose-with-must-gather
description: Collect and analyze OADP diagnostic data using oadp-must-gather to troubleshoot backup, restore, and deployment issues.
---

# Diagnose with OADP Must-Gather

This skill provides comprehensive guidance for using the **oadp-must-gather** tool to collect diagnostic information and troubleshoot OADP operator issues, backup failures, restore problems, and deployment configuration errors.

## When to Use This Skill

- **Backup Failures**: When backups are failing and you need comprehensive diagnostic data
- **Restore Issues**: Troubleshooting restore operations that aren't completing
- **OADP Deployment Problems**: Investigating OADP operator or component deployment failures
- **Performance Issues**: Diagnosing slow backup/restore operations
- **Before Opening Support Cases**: Collecting required diagnostic data for Red Hat support
- **Configuration Validation**: Verifying DPA and OADP configuration correctness
- **Integration Problems**: Debugging issues with cloud providers, CSI, or storage backends

## What This Skill Does

1. **Runs must-gather Collection**: Executes oadp-must-gather to capture diagnostic data
2. **Analyzes Collected Data**: Examines logs, resources, and configurations
3. **Identifies Common Issues**: Detects known failure patterns
4. **Provides Remediation**: Suggests fixes for identified problems
5. **Extracts Key Information**: Highlights critical errors and warnings
6. **Generates Reports**: Summarizes findings for troubleshooting or support cases

## How to Use

### Basic Usage

```
Run oadp must-gather to diagnose backup failure
```

```
Analyze must-gather output for OADP deployment issues
```

### Targeted Diagnosis

```
Collect must-gather for specific backup problem
```

```
Use must-gather to troubleshoot BSL unavailable issue
```

## Prerequisites

- [ ] OpenShift cluster with oadp-must-gather image available
- [ ] oc CLI installed and logged in with cluster-admin or appropriate permissions
- [ ] Sufficient local disk space for must-gather output (typically 100MB-1GB)
- [ ] Knowledge of the issue symptoms and timeline
- [ ] Network connectivity to cluster API

## Examples

### Example 1: Basic Must-Gather Collection

**User**: "Run OADP must-gather to diagnose issues"

**Skill Actions**:

1. **Run must-gather**:
   ```bash
   # Use latest oadp-must-gather image
   oc adm must-gather --image=quay.io/konveyor/oadp-must-gather:latest

   # Output will be in ./must-gather.local.<timestamp> directory
   ```

2. **Wait for collection**:
   ```bash
   # Must-gather will:
   # - Create collection pod
   # - Gather OADP operator logs
   # - Collect Velero deployment logs
   # - Capture BackupStorageLocation status
   # - Extract backup/restore resources
   # - Gather DPA configuration
   # - Collect node-agent (Kopia) or Restic daemonset logs
   # - Save CSI snapshot information
   # - Capture cluster version and platform details

   # Collection typically takes 2-5 minutes
   ```

3. **Verify collection completed**:
   ```bash
   # Check output directory
   ls -lh must-gather.local.*/

   # Typical structure:
   # must-gather.local.XXXX/
   # ├── cluster-scoped-resources/
   # ├── namespaces/
   # │   ├── openshift-adp/
   # │   │   ├── pods/
   # │   │   ├── deployments/
   # │   │   ├── daemonsets/
   # │   │   └── logs/
   # │   └── ...
   # └── timestamp
   ```

4. **Initial analysis**:
   ```bash
   MUST_GATHER_DIR="must-gather.local.$(ls -t must-gather.local.* | head -1 | cut -d'.' -f3-)"

   # Check OADP operator logs for errors
   grep -i error $MUST_GATHER_DIR/namespaces/openshift-adp/pods/*/logs/*.log

   # Check Velero logs
   grep -i "error\|failed\|unable" $MUST_GATHER_DIR/namespaces/openshift-adp/pods/velero-*/logs/*.log
   ```

**Success Indicators**:
- ✅ Must-gather pod completed successfully
- ✅ Output directory created with timestamp
- ✅ Logs and resources collected from openshift-adp namespace
- ✅ No collection errors in must-gather output

### Example 2: Diagnose Backup Failure

**User**: "My backup is failing, use must-gather to find the problem"

**Skill Actions**:

1. **Collect must-gather with backup context**:
   ```bash
   # Run must-gather
   oc adm must-gather --image=quay.io/konveyor/oadp-must-gather:latest

   # Note the backup name that's failing
   FAILED_BACKUP="myapp-backup-20250315"
   ```

2. **Analyze backup-specific data**:
   ```bash
   MUST_GATHER_DIR="must-gather.local.$(ls -t must-gather.local.* | head -1 | cut -d'.' -f3-)"

   # Find backup resource
   find $MUST_GATHER_DIR -name "backups.yaml" -exec grep -A20 "name: $FAILED_BACKUP" {} \;

   # Check backup phase and errors
   find $MUST_GATHER_DIR -name "backups.yaml" -exec grep -B2 -A10 "$FAILED_BACKUP" {} \; | grep -E "phase:|failureReason:|errors:"
   ```

3. **Check Velero logs for backup**:
   ```bash
   # Search Velero logs for the specific backup
   grep -r "$FAILED_BACKUP" $MUST_GATHER_DIR/namespaces/openshift-adp/pods/velero-*/logs/ | grep -i "error\|failed"

   # Look for BSL connectivity issues
   grep -r "BackupStorageLocation" $MUST_GATHER_DIR/namespaces/openshift-adp/pods/velero-*/logs/ | grep -i "unavailable\|error"
   ```

4. **Check node-agent/Kopia logs** (if using file-level backups):
   ```bash
   # For OADP 1.4+ (Kopia)
   find $MUST_GATHER_DIR -path "*/node-agent*/logs/*" -exec grep -l "$FAILED_BACKUP" {} \; | \
     xargs grep -i "error\|failed"

   # For legacy Restic (OADP 1.3)
   find $MUST_GATHER_DIR -path "*/restic*/logs/*" -exec grep -l "$FAILED_BACKUP" {} \; | \
     xargs grep -i "error\|failed"
   ```

5. **Examine BSL status**:
   ```bash
   # Check BackupStorageLocation configuration and status
   find $MUST_GATHER_DIR -name "backupstoragelocations.yaml" -exec cat {} \;

   # Look for BSL phase
   find $MUST_GATHER_DIR -name "backupstoragelocations.yaml" -exec grep -A5 "status:" {} \; | grep "phase:"
   ```

6. **Check DPA configuration**:
   ```bash
   # Examine DataProtectionApplication
   find $MUST_GATHER_DIR -name "dataprotectionapplications.yaml" -exec cat {} \;

   # Verify Kopia/Restic enabled
   find $MUST_GATHER_DIR -name "dataprotectionapplications.yaml" -exec grep -A3 "kopia:\|restic:" {} \;
   ```

**Common Findings and Fixes**:

**Issue**: BSL Unavailable
```yaml
# Finding in backupstoragelocations.yaml:
status:
  phase: Unavailable
  message: "NoSuchBucket: The specified bucket does not exist"
```
**Fix**: Verify S3 bucket exists, check credentials, confirm region setting

**Issue**: Volume Snapshot Timeout
```
Error in Velero logs:
error backing up item: error executing backup action: rpc error: code = DeadlineExceeded
```
**Fix**: Increase timeout in DPA or check CSI driver health

**Issue**: Kopia/Restic Pod Not Running
```bash
# Finding: No node-agent pods
$ find must-gather... -path "*/node-agent*/logs/*"
(no results)
```
**Fix**: Enable Kopia in DPA configuration

### Example 3: Diagnose Restore Failure

**User**: "Restore is stuck, help me troubleshoot with must-gather"

**Skill Actions**:

1. **Collect must-gather**:
   ```bash
   oc adm must-gather --image=quay.io/konveyor/oadp-must-gather:latest

   FAILED_RESTORE="myapp-restore-20250315"
   ```

2. **Analyze restore status**:
   ```bash
   MUST_GATHER_DIR="must-gather.local.$(ls -t must-gather.local.* | head -1 | cut -d'.' -f3-)"

   # Find restore resource
   find $MUST_GATHER_DIR -name "restores.yaml" -exec grep -A30 "name: $FAILED_RESTORE" {} \;

   # Check restore phase
   find $MUST_GATHER_DIR -name "restores.yaml" -exec grep -B2 -A15 "$FAILED_RESTORE" {} \; | \
     grep -E "phase:|warnings:|errors:|failureReason:"
   ```

3. **Check Velero restore logs**:
   ```bash
   # Search for restore-specific errors
   grep -r "$FAILED_RESTORE" $MUST_GATHER_DIR/namespaces/openshift-adp/pods/velero-*/logs/ | \
     grep -i "error\|warning|failed"

   # Look for resource restore issues
   grep -r "error restoring" $MUST_GATHER_DIR/namespaces/openshift-adp/pods/velero-*/logs/
   ```

4. **Check PVC restore status**:
   ```bash
   # Find PVC-related issues
   grep -r "persistentvolumeclaims" $MUST_GATHER_DIR/namespaces/openshift-adp/pods/velero-*/logs/ | \
     grep -i "error\|pending"

   # Check VolumeSnapshot issues
   find $MUST_GATHER_DIR -name "volumesnapshots.yaml" -exec cat {} \;
   ```

5. **Examine namespace mapping issues**:
   ```bash
   # Check if namespace exists
   find $MUST_GATHER_DIR -name "namespaces.yaml" -exec grep -A3 "metadata:" {} \;

   # Look for namespace conflicts
   grep -r "AlreadyExists" $MUST_GATHER_DIR/namespaces/openshift-adp/pods/velero-*/logs/
   ```

**Common Restore Issues**:

**Issue**: StorageClass Not Available
```
Error: persistentvolumeclaims/my-pvc: error restoring: StorageClass "gp2" not found
```
**Fix**: Use `spec.restorePVs: false` or map storage classes in restore spec

**Issue**: Existing Resources Conflict
```
Error: namespaces/myapp already exists
```
**Fix**: Delete existing namespace or use `existingResourcePolicy: update`

**Issue**: VolumeSnapshot Not Ready
```
Warning: VolumeSnapshot "snap-123" is not ready
```
**Fix**: Check CSI driver status, verify snapshot completion

### Example 4: Diagnose OADP Deployment Issues

**User**: "OADP operator isn't deploying properly, collect must-gather"

**Skill Actions**:

1. **Run must-gather**:
   ```bash
   oc adm must-gather --image=quay.io/konveyor/oadp-must-gather:latest
   ```

2. **Check OADP operator status**:
   ```bash
   MUST_GATHER_DIR="must-gather.local.$(ls -t must-gather.local.* | head -1 | cut -d'.' -f3-)"

   # Check operator deployment
   find $MUST_GATHER_DIR -name "deployments.yaml" -path "*/openshift-adp/*" -exec cat {} \;

   # Check operator pod status
   find $MUST_GATHER_DIR -path "*/openshift-adp/pods/oadp-operator-*/logs/*" -exec cat {} \; | \
     grep -i "error\|failed\|unable"
   ```

3. **Examine DPA reconciliation**:
   ```bash
   # Check DPA status
   find $MUST_GATHER_DIR -name "dataprotectionapplications.yaml" -exec grep -A20 "status:" {} \;

   # Look for reconciliation errors
   find $MUST_GATHER_DIR -path "*/oadp-operator-*/logs/*" -exec grep -i "reconcile.*error" {} \;
   ```

4. **Check Velero deployment**:
   ```bash
   # Verify Velero pods
   find $MUST_GATHER_DIR -name "deployments.yaml" -exec grep -A10 "name: velero" {} \;

   # Check for image pull errors
   find $MUST_GATHER_DIR -path "*/openshift-adp/pods/*/pods.yaml" -exec grep -i "ImagePullBackOff\|ErrImagePull" {} \;
   ```

5. **Verify secrets and credentials**:
   ```bash
   # Check if cloud credentials exist (without showing values)
   find $MUST_GATHER_DIR -name "secrets.yaml" -path "*/openshift-adp/*" -exec grep "name: cloud-credentials" {} \;

   # Verify BSL credentials referenced
   find $MUST_GATHER_DIR -name "dataprotectionapplications.yaml" -exec grep -A5 "credential:" {} \;
   ```

**Common Deployment Issues**:

**Issue**: Operator CrashLoopBackOff
```
Error in operator logs:
panic: runtime error: invalid memory address or nil pointer dereference
```
**Fix**: Check for misconfigured DPA, upgrade to latest operator version

**Issue**: Velero Not Deploying
```
DPA status shows:
conditions:
  - type: Reconciled
    status: "False"
    reason: Error
    message: "BSL not available"
```
**Fix**: Fix BSL configuration, verify credentials

**Issue**: Image Pull Errors
```
Pod status:
containers:
  - image: quay.io/konveyor/velero:latest
    state: waiting
      reason: ImagePullBackOff
```
**Fix**: Check network connectivity, verify image exists, check pull secrets

### Example 5: Analyze Must-Gather for Performance Issues

**User**: "Backups are very slow, analyze must-gather for performance bottlenecks"

**Skill Actions**:

1. **Collect must-gather with timing context**:
   ```bash
   # Note current time and run collection
   date
   oc adm must-gather --image=quay.io/konveyor/oadp-must-gather:latest
   ```

2. **Check resource allocation**:
   ```bash
   MUST_GATHER_DIR="must-gather.local.$(ls -t must-gather.local.* | head -1 | cut -d'.' -f3-)"

   # Check Velero pod resources
   find $MUST_GATHER_DIR -name "deployments.yaml" -path "*/openshift-adp/*" -exec grep -A10 "resources:" {} \;

   # Check node-agent/Kopia resource limits
   find $MUST_GATHER_DIR -name "daemonsets.yaml" -exec grep -A10 "resources:" {} \;
   ```

3. **Examine DPA configuration for performance settings**:
   ```bash
   # Check parallel upload settings
   find $MUST_GATHER_DIR -name "dataprotectionapplications.yaml" -exec grep -E "uploaderConfig|parallelFilesUpload" {} \;

   # Check resource timeout settings
   find $MUST_GATHER_DIR -name "dataprotectionapplications.yaml" -exec grep -i "timeout" {} \;
   ```

4. **Analyze backup size and duration**:
   ```bash
   # Get backup details
   find $MUST_GATHER_DIR -name "backups.yaml" -exec grep -E "startTimestamp|completionTimestamp|progress" {} \;

   # Calculate backup durations (manual inspection)
   ```

5. **Check for throttling or rate limiting**:
   ```bash
   # Look for S3 throttling
   grep -r "RequestLimitExceeded\|SlowDown\|503" $MUST_GATHER_DIR/namespaces/openshift-adp/pods/velero-*/logs/

   # Check for CSI snapshot delays
   grep -r "snapshot.*timeout\|snapshot.*slow" $MUST_GATHER_DIR/namespaces/openshift-adp/pods/velero-*/logs/
   ```

**Performance Tuning Recommendations**:

**Finding**: Low Velero CPU/Memory
```yaml
# Current limits:
resources:
  limits:
    cpu: 500m
    memory: 512Mi
```
**Recommendation**: Increase to 1-2 CPU, 1-2Gi memory for large clusters

**Finding**: Sequential File Uploads
```yaml
# Missing parallel upload config
```
**Recommendation**: Add to DPA:
```yaml
spec:
  configuration:
    velero:
      args:
        - "--uploader-parallel-files-upload=4"
```

**Finding**: Large Data Volumes
```
Backup includes 500GB+ of data via file-level backup
```
**Recommendation**: Use CSI snapshots instead of file-level backup for large volumes

## Must-Gather Analysis Checklist

After collecting must-gather data, systematically review:

- [ ] **OADP Operator Logs**: Check for controller reconciliation errors
- [ ] **Velero Deployment Status**: Verify pods running and ready
- [ ] **DPA Configuration**: Validate all settings (BSL, VSL, plugins, Kopia/Restic)
- [ ] **BSL Status**: Confirm all BackupStorageLocations are Available
- [ ] **VSL Configuration**: Verify VolumeSnapshotLocations configured correctly
- [ ] **Backup Resources**: Examine failed/stuck backups for errors
- [ ] **Restore Resources**: Check restore status and warnings
- [ ] **Node-Agent/Kopia Logs**: Look for file-level backup errors
- [ ] **CSI Snapshot Status**: Verify VolumeSnapshots completing
- [ ] **Cluster Platform**: Note OpenShift version and infrastructure type
- [ ] **Network Connectivity**: Check for BSL connection failures
- [ ] **Resource Constraints**: Verify adequate CPU/memory allocated

## Common Error Patterns

### Pattern 1: BSL Connectivity Issues

**Symptoms in must-gather**:
```
BackupStorageLocation phase: Unavailable
Velero logs: "error getting backup store"
```

**Root Causes**:
- Invalid credentials
- Wrong S3 endpoint or region
- Network policy blocking egress
- Bucket doesn't exist or wrong name

**Diagnostic Commands**:
```bash
# From must-gather output
find $MUST_GATHER_DIR -name "backupstoragelocations.yaml" -exec cat {} \;
grep -r "backup store" $MUST_GATHER_DIR/namespaces/openshift-adp/pods/velero-*/logs/
```

### Pattern 2: CSI Snapshot Failures

**Symptoms in must-gather**:
```
VolumeSnapshot status: Error
Backup logs: "error creating snapshot"
```

**Root Causes**:
- CSI driver not installed or not ready
- VolumeSnapshotClass missing or incorrect
- Storage backend doesn't support snapshots
- Snapshot quota exceeded

**Diagnostic Commands**:
```bash
find $MUST_GATHER_DIR -name "volumesnapshotclasses.yaml" -exec cat {} \;
find $MUST_GATHER_DIR -name "volumesnapshots.yaml" -exec grep -A10 "status:" {} \;
```

### Pattern 3: File-Level Backup Hangs

**Symptoms in must-gather**:
```
Backup phase: InProgress (stuck for hours)
Node-agent logs show no recent activity
```

**Root Causes**:
- Node-agent pod not running on backup source node
- Very large files causing timeouts
- Insufficient resources (CPU/memory)
- Network issues to BSL

**Diagnostic Commands**:
```bash
# Check node-agent pod distribution
find $MUST_GATHER_DIR -name "daemonsets.yaml" -exec grep -A5 "numberReady" {} \;

# Check for timeout errors
grep -r "timeout\|deadline exceeded" $MUST_GATHER_DIR/namespaces/openshift-adp/pods/node-agent-*/logs/
```

### Pattern 4: DPA Reconciliation Failures

**Symptoms in must-gather**:
```
DPA status: Not reconciled
Operator logs: "reconcile error"
```

**Root Causes**:
- Invalid DPA configuration
- Missing required fields
- Plugin compatibility issues
- Operator bug

**Diagnostic Commands**:
```bash
find $MUST_GATHER_DIR -name "dataprotectionapplications.yaml" -exec grep -A20 "status:" {} \;
find $MUST_GATHER_DIR -path "*/oadp-operator-*/logs/*" -exec grep "reconcile" {} \; | grep -i error
```

## Advanced Must-Gather Analysis

### Extracting Specific Time Ranges

```bash
# Find logs from specific time period
MUST_GATHER_DIR="must-gather.local.XXXX"

# Example: Errors between 14:00 and 15:00 UTC
grep -r "2025-03-15T14:\|2025-03-15T15:" $MUST_GATHER_DIR/namespaces/openshift-adp/pods/*/logs/ | \
  grep -i error
```

### Comparing DPA vs Actual Deployment

```bash
# Extract DPA desired configuration
find $MUST_GATHER_DIR -name "dataprotectionapplications.yaml" -exec cat {} \; > dpa-config.yaml

# Extract actual Velero deployment
find $MUST_GATHER_DIR -name "deployments.yaml" -path "*/openshift-adp/*" -exec cat {} \; > actual-deployment.yaml

# Compare (manual review)
diff -u dpa-config.yaml actual-deployment.yaml
```

### Correlating Events Across Components

```bash
# Create timeline of events
grep -r "timestamp\|time" $MUST_GATHER_DIR/namespaces/openshift-adp/ | sort
```

## Best Practices

1. **Collect Immediately After Failure**
   - Run must-gather as soon as issue occurs
   - Logs may rotate, losing critical information
   - Capture state while problem is still present

2. **Provide Context in Support Cases**
   - Include symptoms and timeline
   - Note what changed recently
   - Specify OADP version and platform
   - Attach entire must-gather archive

3. **Organize Multiple Collections**
   ```bash
   # Rename must-gather directories meaningfully
   mv must-gather.local.12345678 must-gather-backup-failure-2025-03-15

   # Keep collections for comparison
   diff -r must-gather-before/ must-gather-after/
   ```

4. **Redact Sensitive Information Before Sharing**
   ```bash
   # Remove credentials from collected data (for public sharing)
   # Note: Red Hat support needs unredacted must-gather

   # Find and review secrets
   find must-gather.local.XXXX -name "secrets.yaml" -exec cat {} \;

   # Consider: Don't share must-gather publicly, only with Red Hat support
   ```

5. **Automate Analysis**
   ```bash
   # Create analysis script
   cat << 'EOF' > analyze-oadp-must-gather.sh
   #!/bin/bash
   MUST_GATHER_DIR=$1

   echo "=== OADP Operator Status ==="
   find $MUST_GATHER_DIR -path "*/oadp-operator-*/logs/*" | xargs grep -i "error\|failed" | head -20

   echo -e "\n=== BSL Status ==="
   find $MUST_GATHER_DIR -name "backupstoragelocations.yaml" -exec grep "phase:" {} \;

   echo -e "\n=== Recent Backup Failures ==="
   find $MUST_GATHER_DIR -name "backups.yaml" -exec grep -B2 "phase: Failed" {} \;

   echo -e "\n=== Velero Errors ==="
   find $MUST_GATHER_DIR -path "*/velero-*/logs/*" | xargs grep -i "error" | head -20
   EOF

   chmod +x analyze-oadp-must-gather.sh
   ./analyze-oadp-must-gather.sh must-gather.local.XXXX
   ```

## Troubleshooting Must-Gather Collection

### Must-Gather Pod Fails

**Symptoms**: Must-gather pod errors or doesn't start

**Diagnosis**:
```bash
# Check must-gather pod status
oc get pods -A | grep must-gather

# View must-gather pod logs
oc logs -n openshift-must-gather-<random> must-gather-<id>
```

**Common Fixes**:
- Ensure sufficient permissions (cluster-admin or must-gather role)
- Check node resources availability
- Verify must-gather image accessibility
- Check for network policies blocking pod creation

### Incomplete Data Collection

**Symptoms**: Must-gather completes but missing expected logs

**Possible Causes**:
- Pods were not running during collection
- Namespace permissions issues
- Collection timeout

**Solution**:
```bash
# Run with extended timeout
oc adm must-gather --image=quay.io/konveyor/oadp-must-gather:latest -- /usr/bin/gather --timeout=10m
```

## Integration with Support Cases

When opening a Red Hat support case:

1. **Collect must-gather** using latest image
2. **Archive and compress**:
   ```bash
   tar czf oadp-must-gather-$(date +%Y%m%d).tar.gz must-gather.local.*/
   ```
3. **Attach to case** via Red Hat Customer Portal
4. **Include**:
   - Description of issue
   - Steps to reproduce
   - OADP version
   - OpenShift version
   - Cloud provider/platform
   - Timeline of issue

## Next Steps

After analyzing must-gather:

1. **Apply Fixes**: Implement identified remediation steps
2. **Retest**: Verify issue resolved
3. **Collect New Must-Gather**: Confirm fix worked
4. **Update Documentation**: Record solution for future reference
5. **Open Support Case**: If issue persists or is unclear

**Related Skills**:
- diagnose-backup-issues - Additional backup troubleshooting techniques
- install-oadp - Proper OADP installation to avoid deployment issues
- create-backup - Backup creation best practices

## Resources

- **OpenShift Must-Gather Documentation**: https://docs.openshift.com/container-platform/latest/support/gathering-cluster-data.html
- **OADP Must-Gather GitHub**: https://github.com/openshift/oadp-must-gather
- **Red Hat Support**: https://access.redhat.com/support

---

**Version**: 1.0
**Last Updated**: 2025-11-17
**Compatibility**: OADP 1.3+, OpenShift 4.12+
**CRITICAL**: Must-gather is the primary diagnostic tool for OADP issues - use it early and often
