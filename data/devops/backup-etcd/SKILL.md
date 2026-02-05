---
name: backup-etcd
description: Create and manage etcd backups for OpenShift control plane disaster recovery, including automated backup procedures and verification.
---

# Backup etcd

This skill provides comprehensive guidance for backing up etcd, the critical key-value store for OpenShift/Kubernetes control plane data. Proper etcd backups are essential for cluster disaster recovery.

## When to Use This Skill

- **Before Major Changes**: Prior to cluster upgrades, configuration changes, or major updates
- **Regular Maintenance**: As part of routine backup procedures
- **Disaster Recovery Planning**: Setting up automated etcd backup schedules
- **Pre-Migration**: Before cluster migrations or infrastructure changes
- **Compliance**: Meeting backup retention requirements
- **Emergency Situations**: When cluster issues detected, capture current state

## What This Skill Does

1. **Validates Cluster Health**: Checks etcd cluster status before backup
2. **Creates etcd Snapshot**: Generates consistent etcd data snapshot
3. **Stores Backup Safely**: Copies snapshot to secure off-cluster location
4. **Verifies Backup**: Validates snapshot integrity and completeness
5. **Manages Retention**: Implements backup rotation and cleanup
6. **Documents Metadata**: Records backup metadata for recovery procedures

## How to Use

### Basic Usage

```
Create an etcd backup
```

```
Backup etcd and store in S3
```

### Automated Usage

```
Set up automated daily etcd backups
```

```
Create etcd backup CronJob with retention policy
```

### Emergency Usage

```
Create emergency etcd snapshot before cluster recovery
```

## Prerequisites

Before backing up etcd:

- [ ] Cluster admin access with oc CLI configured
- [ ] At least one healthy master node accessible
- [ ] Sufficient disk space on master nodes (typically 2-3x etcd data size)
- [ ] SSH access to master nodes (for manual backups)
- [ ] Off-cluster storage location configured (for backup copies)
- [ ] Understanding of etcd cluster topology

## Examples

### Example 1: Manual etcd Backup on Single Master

**User**: "Create manual etcd backup"

**Skill Actions**:

1. **Check etcd cluster health**:
   ```bash
   # Verify all etcd members are healthy
   oc get etcd -o=jsonpath='{range .items[0].status.conditions[?(@.type=="EtcdMembersAvailable")]}{.message}{"\n"}{.reason}{"\n"}{.status}{"\n"}{end}'

   # Check etcd pods
   oc get pods -n openshift-etcd -l app=etcd

   # Verify etcd endpoint health
   ETCD_POD=$(oc get pods -n openshift-etcd -l app=etcd -o jsonpath='{.items[0].metadata.name}')
   oc exec -n openshift-etcd $ETCD_POD -- etcdctl endpoint health -w table
   ```

2. **Access master node and create backup**:
   ```bash
   # Get first master node name
   MASTER_NODE=$(oc get nodes -l node-role.kubernetes.io/master -o jsonpath='{.items[0].metadata.name}')

   # Start debug session on master node
   oc debug node/$MASTER_NODE

   # Once in debug pod, run backup
   chroot /host

   # Create backup directory
   mkdir -p /home/core/etcd-backups

   # Run cluster backup script
   /usr/local/bin/cluster-backup.sh /home/core/etcd-backups

   # Exit chroot and debug pod
   exit
   exit
   ```

3. **Verify backup created**:
   ```bash
   # List backups on master node
   oc debug node/$MASTER_NODE -- chroot /host ls -lh /home/core/etcd-backups/
   ```

4. **Copy backup off cluster**:
   ```bash
   # Create local directory
   mkdir -p ./etcd-backups/$(date +%Y%m%d)

   # Copy backup files
   oc debug node/$MASTER_NODE -- chroot /host tar czf - /home/core/etcd-backups/ | tar xzf - -C ./etcd-backups/$(date +%Y%m%d)/

   # Verify files copied
   ls -lh ./etcd-backups/$(date +%Y%m%d)/
   ```

**Expected Output**:
```
Backup created at: /home/core/etcd-backups/snapshot_2025-11-17_152030.db
Static pod resources backed up to: /home/core/etcd-backups/static_kuberesources_2025-11-17_152030.tar.gz
```

**Success Indicators**:
- ✅ snapshot_*.db file created (etcd data)
- ✅ static_kuberesources_*.tar.gz created (static pod manifests)
- ✅ No errors in backup script output
- ✅ Backup files copied off cluster successfully

### Example 2: Automated etcd Backup with CronJob

**User**: "Set up automated daily etcd backups at 2 AM"

**Skill Actions**:

1. **Create etcd backup script ConfigMap**:
   ```yaml
   apiVersion: v1
   kind: ConfigMap
   metadata:
     name: etcd-backup-script
     namespace: openshift-etcd
   data:
     backup-etcd.sh: |
       #!/bin/bash
       set -euo pipefail

       BACKUP_DIR="/host/home/core/etcd-backups"
       BACKUP_DATE=$(date +%Y%m%d-%H%M%S)
       RETENTION_DAYS=7

       echo "Starting etcd backup at $BACKUP_DATE"

       # Create backup directory
       mkdir -p $BACKUP_DIR

       # Run backup
       /usr/local/bin/cluster-backup.sh $BACKUP_DIR

       echo "Backup completed successfully"

       # Clean up old backups
       find $BACKUP_DIR -name "snapshot_*.db" -mtime +$RETENTION_DAYS -delete
       find $BACKUP_DIR -name "static_kuberesources_*.tar.gz" -mtime +$RETENTION_DAYS -delete

       echo "Old backups cleaned up (retention: $RETENTION_DAYS days)"

       # List current backups
       echo "Current backups:"
       ls -lh $BACKUP_DIR/
   ```

2. **Create ServiceAccount with required permissions**:
   ```yaml
   apiVersion: v1
   kind: ServiceAccount
   metadata:
     name: etcd-backup
     namespace: openshift-etcd
   ---
   apiVersion: rbac.authorization.k8s.io/v1
   kind: ClusterRole
   metadata:
     name: etcd-backup
   rules:
     - apiGroups: [""]
       resources: ["nodes"]
       verbs: ["get", "list"]
     - apiGroups: [""]
       resources: ["pods"]
       verbs: ["get", "list"]
     - apiGroups: [""]
       resources: ["pods/log"]
       verbs: ["get"]
   ---
   apiVersion: rbac.authorization.k8s.io/v1
   kind: ClusterRoleBinding
   metadata:
     name: etcd-backup
   roleRef:
     apiGroup: rbac.authorization.k8s.io
     kind: ClusterRole
     name: etcd-backup
   subjects:
     - kind: ServiceAccount
       name: etcd-backup
       namespace: openshift-etcd
   ```

3. **Create CronJob for automated backups**:
   ```yaml
   apiVersion: batch/v1
   kind: CronJob
   metadata:
     name: etcd-backup
     namespace: openshift-etcd
   spec:
     schedule: "0 2 * * *"  # 2 AM daily
     concurrencyPolicy: Forbid
     successfulJobsHistoryLimit: 3
     failedJobsHistoryLimit: 3
     jobTemplate:
       spec:
         backoffLimit: 0
         template:
           metadata:
             labels:
               app: etcd-backup
           spec:
             serviceAccountName: etcd-backup
             hostNetwork: true
             hostPID: true
             nodeSelector:
               node-role.kubernetes.io/master: ""
             tolerations:
               - operator: "Exists"
             containers:
               - name: etcd-backup
                 image: quay.io/openshift-release-dev/ocp-v4.0-art-dev@sha256:... # Use cluster version
                 command:
                   - /bin/bash
                   - -c
                   - |
                     #!/bin/bash
                     set -euo pipefail

                     # Run backup script
                     /scripts/backup-etcd.sh

                     # Optional: Upload to S3/cloud storage
                     # aws s3 cp /host/home/core/etcd-backups/ s3://my-backups/etcd/ --recursive
                 volumeMounts:
                   - name: host
                     mountPath: /host
                   - name: backup-script
                     mountPath: /scripts
                 securityContext:
                   privileged: true
                   runAsUser: 0
             volumes:
               - name: host
                 hostPath:
                   path: /
                   type: Directory
               - name: backup-script
                 configMap:
                   name: etcd-backup-script
                   defaultMode: 0755
             restartPolicy: Never
   ```

4. **Apply resources**:
   ```bash
   oc apply -f etcd-backup-configmap.yaml
   oc apply -f etcd-backup-rbac.yaml
   oc apply -f etcd-backup-cronjob.yaml
   ```

5. **Test CronJob manually**:
   ```bash
   # Create manual job from CronJob
   oc create job --from=cronjob/etcd-backup etcd-backup-manual -n openshift-etcd

   # Watch job completion
   oc get jobs -n openshift-etcd -w

   # Check logs
   oc logs -n openshift-etcd job/etcd-backup-manual
   ```

**Success Indicators**:
- ✅ CronJob created and scheduled
- ✅ Manual test job completes successfully
- ✅ Backup files appear in /home/core/etcd-backups on master
- ✅ Old backups cleaned up based on retention policy

### Example 3: etcd Backup with S3 Upload

**User**: "Create etcd backup and upload to S3"

**Skill Actions**:

1. **Create AWS credentials secret**:
   ```bash
   cat <<EOF > aws-credentials
   [default]
   aws_access_key_id=<ACCESS_KEY>
   aws_secret_access_key=<SECRET_KEY>
   EOF

   oc create secret generic etcd-backup-aws-creds \
     --from-file=credentials=aws-credentials \
     -n openshift-etcd

   rm aws-credentials
   ```

2. **Create enhanced backup script with S3 upload**:
   ```yaml
   apiVersion: v1
   kind: ConfigMap
   metadata:
     name: etcd-backup-script-s3
     namespace: openshift-etcd
   data:
     backup-etcd.sh: |
       #!/bin/bash
       set -euo pipefail

       BACKUP_DIR="/host/home/core/etcd-backups"
       BACKUP_DATE=$(date +%Y%m%d-%H%M%S)
       S3_BUCKET="s3://my-etcd-backups"
       S3_PREFIX="openshift-cluster-1"
       RETENTION_DAYS=30

       echo "Starting etcd backup at $BACKUP_DATE"

       # Create backup directory
       mkdir -p $BACKUP_DIR

       # Run backup
       /usr/local/bin/cluster-backup.sh $BACKUP_DIR

       # Get backup files
       SNAPSHOT_FILE=$(ls -t $BACKUP_DIR/snapshot_*.db | head -1)
       STATIC_RESOURCES=$(ls -t $BACKUP_DIR/static_kuberesources_*.tar.gz | head -1)

       echo "Snapshot: $SNAPSHOT_FILE"
       echo "Static resources: $STATIC_RESOURCES"

       # Upload to S3
       echo "Uploading to S3..."
       aws s3 cp $SNAPSHOT_FILE $S3_BUCKET/$S3_PREFIX/$(basename $SNAPSHOT_FILE)
       aws s3 cp $STATIC_RESOURCES $S3_BUCKET/$S3_PREFIX/$(basename $STATIC_RESOURCES)

       # Create metadata file
       cat <<METADATA > $BACKUP_DIR/backup-metadata-$BACKUP_DATE.json
       {
         "timestamp": "$BACKUP_DATE",
         "snapshot_file": "$(basename $SNAPSHOT_FILE)",
         "static_resources": "$(basename $STATIC_RESOURCES)",
         "cluster_version": "$(oc version -o json | jq -r '.openshiftVersion')",
         "etcd_version": "$(oc exec -n openshift-etcd $ETCD_POD -- etcdctl version | head -1)"
       }
       METADATA

       # Upload metadata
       aws s3 cp $BACKUP_DIR/backup-metadata-$BACKUP_DATE.json \
         $S3_BUCKET/$S3_PREFIX/backup-metadata-$BACKUP_DATE.json

       echo "Upload completed successfully"

       # List S3 backups
       echo "Backups in S3:"
       aws s3 ls $S3_BUCKET/$S3_PREFIX/

       # Clean up local old backups
       find $BACKUP_DIR -name "snapshot_*.db" -mtime +7 -delete
       find $BACKUP_DIR -name "static_kuberesources_*.tar.gz" -mtime +7 -delete
       find $BACKUP_DIR -name "backup-metadata-*.json" -mtime +7 -delete

       echo "Backup process completed"
   ```

3. **Update CronJob with S3 credentials**:
   ```yaml
   # Add to CronJob container spec:
   env:
     - name: AWS_SHARED_CREDENTIALS_FILE
       value: /aws/credentials
     - name: AWS_DEFAULT_REGION
       value: us-east-1
   volumeMounts:
     - name: aws-credentials
       mountPath: /aws
       readOnly: true

   # Add to volumes:
   - name: aws-credentials
     secret:
       secretName: etcd-backup-aws-creds
   ```

**Verification**:
```bash
# Check S3 bucket
aws s3 ls s3://my-etcd-backups/openshift-cluster-1/

# Download and verify
aws s3 cp s3://my-etcd-backups/openshift-cluster-1/snapshot_latest.db ./
file snapshot_latest.db  # Should show: snapshot_latest.db: data
```

### Example 4: Pre-Upgrade etcd Backup

**User**: "Create etcd backup before cluster upgrade"

**Skill Actions**:

1. **Verify cluster health before backup**:
   ```bash
   # Check cluster operators
   oc get co

   # Check etcd cluster
   oc get etcd cluster -o jsonpath='{.status.conditions[?(@.type=="EtcdMembersAvailable")]}' | jq .

   # Verify no etcd leader elections happening
   oc logs -n openshift-etcd -l app=etcd --tail=100 | grep -i "leader"
   ```

2. **Create labeled backup**:
   ```bash
   UPGRADE_VERSION="4.14.8"
   BACKUP_DATE=$(date +%Y%m%d-%H%M%S)
   BACKUP_LABEL="pre-upgrade-$UPGRADE_VERSION"

   # Access master and create backup
   MASTER_NODE=$(oc get nodes -l node-role.kubernetes.io/master -o jsonpath='{.items[0].metadata.name}')

   oc debug node/$MASTER_NODE <<'BACKUP_EOF'
   chroot /host
   mkdir -p /home/core/etcd-backups/pre-upgrade-$UPGRADE_VERSION
   /usr/local/bin/cluster-backup.sh /home/core/etcd-backups/$BACKUP_LABEL
   exit
   exit
   BACKUP_EOF
   ```

3. **Document backup metadata**:
   ```bash
   # Create backup documentation
   cat <<EOF > etcd-backup-metadata-$BACKUP_DATE.yaml
   backup_type: pre-upgrade
   backup_date: $BACKUP_DATE
   cluster_version_before: $(oc version -o json | jq -r '.openshiftVersion')
   target_upgrade_version: $UPGRADE_VERSION
   cluster_name: $(oc get infrastructure cluster -o jsonpath='{.status.infrastructureName}')
   etcd_members: $(oc get pods -n openshift-etcd -l app=etcd -o jsonpath='{.items[*].metadata.name}')
   backup_location: /home/core/etcd-backups/$BACKUP_LABEL
   notes: "Pre-upgrade backup before upgrading to $UPGRADE_VERSION"
   EOF

   # Store metadata
   oc create configmap etcd-backup-metadata-$BACKUP_DATE \
     --from-file=metadata=etcd-backup-metadata-$BACKUP_DATE.yaml \
     -n openshift-etcd
   ```

4. **Copy and archive**:
   ```bash
   # Copy off cluster
   mkdir -p ./critical-backups/pre-upgrade-$UPGRADE_VERSION
   oc debug node/$MASTER_NODE -- chroot /host tar czf - /home/core/etcd-backups/$BACKUP_LABEL | \
     tar xzf - -C ./critical-backups/pre-upgrade-$UPGRADE_VERSION/

   # Create archive
   tar czf etcd-pre-upgrade-$UPGRADE_VERSION-$BACKUP_DATE.tar.gz \
     -C ./critical-backups pre-upgrade-$UPGRADE_VERSION

   echo "Backup archived: etcd-pre-upgrade-$UPGRADE_VERSION-$BACKUP_DATE.tar.gz"
   ```

**Post-Backup Verification**:
```bash
# Verify backup file integrity
tar tzf etcd-pre-upgrade-$UPGRADE_VERSION-$BACKUP_DATE.tar.gz | head -20

# Check backup size (should be several GB for production cluster)
ls -lh etcd-pre-upgrade-$UPGRADE_VERSION-$BACKUP_DATE.tar.gz
```

## Monitoring and Verification

### Check Backup Health

```bash
# Verify etcd snapshot integrity (basic check)
SNAPSHOT_FILE="/home/core/etcd-backups/snapshot_*.db"
file $SNAPSHOT_FILE  # Should show: data

# Check snapshot size (production clusters typically 1-10GB)
ls -lh $SNAPSHOT_FILE

# Verify static resources archive
tar tzf /home/core/etcd-backups/static_kuberesources_*.tar.gz | head -20
```

### Monitor Automated Backups

```bash
# Check CronJob status
oc get cronjobs -n openshift-etcd

# View recent job runs
oc get jobs -n openshift-etcd -l app=etcd-backup --sort-by=.metadata.creationTimestamp

# Check latest backup logs
LATEST_JOB=$(oc get jobs -n openshift-etcd -l app=etcd-backup --sort-by=.metadata.creationTimestamp -o jsonpath='{.items[-1].metadata.name}')
oc logs -n openshift-etcd job/$LATEST_JOB
```

## Troubleshooting

### Backup Script Fails

**Symptoms**: cluster-backup.sh fails with errors

**Common Causes**:
1. **Insufficient disk space**:
   ```bash
   # Check disk space on master
   oc debug node/$MASTER_NODE -- chroot /host df -h /home/core
   ```

2. **etcd unhealthy**:
   ```bash
   # Check etcd member health
   oc exec -n openshift-etcd $ETCD_POD -- etcdctl endpoint health -w table
   ```

3. **Permission issues**:
   ```bash
   # Verify running as root in debug pod
   oc debug node/$MASTER_NODE -- chroot /host whoami
   ```

### CronJob Not Running

**Symptoms**: No backup jobs created

**Diagnosis**:
```bash
# Check CronJob status
oc describe cronjob etcd-backup -n openshift-etcd

# Check for scheduling errors
oc get events -n openshift-etcd --field-selector involvedObject.name=etcd-backup
```

**Common Issues**:
- Node selector not matching (no master nodes)
- ServiceAccount permissions insufficient
- Image pull errors

### Cannot Access Master Node

**Symptoms**: oc debug fails to access master

**Solutions**:
```bash
# Try different master node
oc get nodes -l node-role.kubernetes.io/master
oc debug node/<different-master>

# Check SSH access (alternative method)
ssh core@<master-ip>
sudo /usr/local/bin/cluster-backup.sh /home/core/etcd-backups
```

## Best Practices

1. **Regular Schedule**
   - Daily backups minimum for production
   - Before/after major changes
   - Before cluster upgrades
   - Store at least 7 days of backups

2. **Off-Cluster Storage**
   - Always copy backups off cluster immediately
   - Use different storage system than cluster
   - Encrypt backups at rest and in transit
   - Test backup accessibility regularly

3. **Retention Policy**
   - Keep daily backups for 7 days
   - Weekly backups for 4 weeks
   - Monthly backups for 6-12 months
   - Pre-upgrade backups indefinitely until verified

4. **Backup Validation**
   - Test restore procedure quarterly
   - Verify backup file integrity
   - Document restore procedures
   - Train team on recovery process

5. **Monitoring**
   - Alert on backup failures
   - Monitor backup size trends
   - Track backup completion times
   - Alert on missing scheduled backups

6. **Documentation**
   - Record backup metadata (date, version, reason)
   - Document recovery procedures
   - Maintain inventory of backups
   - Note any special considerations

## Disaster Recovery Integration

### Combine with OADP

While etcd backups are separate from OADP, combine both for complete DR:

```bash
# 1. Create etcd backup
/usr/local/bin/cluster-backup.sh /home/core/etcd-backups

# 2. Create OADP namespace backup
velero backup create full-cluster-backup \
  --include-namespaces "*" \
  --exclude-namespaces "openshift-*,kube-*" \
  --snapshot-volumes

# 3. Store both backups together
tar czf complete-cluster-backup-$(date +%Y%m%d).tar.gz \
  etcd-backups/ \
  oadp-backup-metadata/
```

### Recovery Priority

In disaster recovery:
1. Restore etcd first (control plane)
2. Verify cluster comes up
3. Restore OADP backups (applications)
4. Verify application functionality

## Next Steps

After creating etcd backups:

1. **Test Restore**: Practice etcd restore in test environment
2. **Automate**: Set up CronJob for regular automated backups
3. **Monitor**: Configure alerts for backup failures
4. **Document**: Create runbook for disaster recovery
5. **Integrate**: Combine with OADP application backups

**Related Skills**:
- install-oadp - Install OADP operator
- create-backup - Create application backups
- diagnose-backup-issues - Troubleshoot backup problems

## Resources

- **OpenShift etcd Backup Documentation**: https://docs.openshift.com/container-platform/latest/backup_and_restore/control_plane_backup_and_restore/backing-up-etcd.html
- **Disaster Recovery**: https://docs.openshift.com/container-platform/latest/backup_and_restore/control_plane_backup_and_restore/disaster-recovery.html
- **etcd Documentation**: https://etcd.io/docs/

---

**Version**: 1.0
**Last Updated**: 2025-11-17
**Compatibility**: OpenShift 4.10+
**CRITICAL**: etcd backups are essential for cluster disaster recovery
