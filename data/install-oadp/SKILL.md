---
name: install-oadp
description: Install and configure OADP operator with DataProtectionApplication for backup and restore operations on OpenShift clusters.
---

# Install OADP

This skill guides you through installing the OpenShift API for Data Protection (OADP) operator and configuring it with a DataProtectionApplication (DPA) resource for various cloud providers and storage backends.

## When to Use This Skill

- **Fresh Installation**: Setting up OADP for the first time on an OpenShift cluster
- **New Cluster Setup**: Configuring OADP on newly provisioned clusters
- **Provider Migration**: Switching from one cloud provider's storage to another
- **Testing**: Installing OADP in development/test environments
- **Upgrades**: Installing newer versions of OADP operator

## What This Skill Does

1. **Installs Operator**: Deploys OADP operator via OperatorHub or manual manifest
2. **Creates Namespace**: Sets up openshift-adp namespace for OADP components
3. **Configures Credentials**: Creates cloud provider credentials secret
4. **Creates DPA**: Deploys DataProtectionApplication with backup storage and snapshot locations
5. **Verifies Installation**: Confirms all components are running correctly
6. **Tests Configuration**: Validates backup storage location connectivity

## How to Use

### Basic Usage

```
Install OADP with AWS S3 storage
```

```
Set up OADP on OpenShift cluster
```

### Advanced Usage

```
Install OADP with Azure Blob storage and enable Data Mover
```

```
Configure OADP with multiple backup storage locations
```

### With Specific Configuration

```
Install OADP using MCG/NooBaa for internal object storage
```

## Prerequisites

Before using this skill:

- [ ] OpenShift cluster with admin access
- [ ] oc CLI installed and logged in
- [ ] Cloud provider credentials (for AWS/Azure/GCP)
- [ ] Object storage bucket created
- [ ] Network connectivity to object storage endpoint
- [ ] Sufficient cluster resources (minimum 1 CPU, 512Mi memory)

## Examples

### Example 1: Install OADP with AWS S3

**User**: "Install OADP with AWS S3 bucket for backups"

**Skill Actions**:

1. **Create openshift-adp namespace**:
   ```bash
   oc create namespace openshift-adp
   ```

2. **Install OADP operator via OperatorHub**:
   ```bash
   cat <<EOF | oc apply -f -
   apiVersion: operators.coreos.com/v1alpha1
   kind: Subscription
   metadata:
     name: oadp-operator
     namespace: openshift-adp
   spec:
     channel: stable-1.4
     name: oadp-operator
     source: redhat-operators
     sourceNamespace: openshift-marketplace
     installPlanApproval: Automatic
   EOF
   ```

3. **Wait for operator installation**:
   ```bash
   # Watch operator installation
   oc get csv -n openshift-adp -w

   # Verify operator pod running
   oc get pods -n openshift-adp
   ```

4. **Create AWS credentials secret**:
   ```bash
   cat <<EOF > ./credentials-velero
   [default]
   aws_access_key_id=<AWS_ACCESS_KEY_ID>
   aws_secret_access_key=<AWS_SECRET_ACCESS_KEY>
   EOF

   oc create secret generic cloud-credentials \
     --from-file cloud=./credentials-velero \
     -n openshift-adp

   rm -f ./credentials-velero  # Clean up credentials file
   ```

5. **Create DataProtectionApplication**:
   ```yaml
   apiVersion: oadp.openshift.io/v1alpha1
   kind: DataProtectionApplication
   metadata:
     name: dpa
     namespace: openshift-adp
   spec:
     configuration:
       velero:
         defaultPlugins:
           - openshift
           - aws
         podConfig:
           resourceAllocations:
             limits:
               cpu: "1"
               memory: 1Gi
             requests:
               cpu: 500m
               memory: 512Mi
       kopia:
         enable: true
         podConfig:
           resourceAllocations:
             limits:
               cpu: "1"
               memory: 1Gi
       # Note: Restic is deprecated in OADP 1.4+, use Kopia for new deployments
       # restic:
       #   enable: false
     backupLocations:
       - name: default
         velero:
           provider: aws
           default: true
           objectStorage:
             bucket: oadp-backups
             prefix: openshift-cluster
           config:
             region: us-east-1
           credential:
             name: cloud-credentials
             key: cloud
     snapshotLocations:
       - name: default
         velero:
           provider: aws
           config:
             region: us-east-1
   ```

6. **Apply DPA**:
   ```bash
   oc apply -f dpa.yaml
   ```

7. **Verify installation**:
   ```bash
   # Check DPA reconciled
   oc get dpa -n openshift-adp

   # Check Velero deployment
   oc get pods -n openshift-adp

   # Check BackupStorageLocation
   oc get backupstoragelocations -n openshift-adp

   # Verify BSL is available
   oc get bsl -n openshift-adp -o jsonpath='{.items[0].status.phase}'
   # Should output: Available
   ```

**Success Indicators**:
- ✅ oadp-operator CSV in Succeeded state
- ✅ Velero pod running
- ✅ Kopia (or legacy Restic) daemonset running on all nodes
- ✅ BackupStorageLocation phase is "Available"
- ✅ No errors in operator/velero logs

### Example 2: Install OADP with Azure Blob Storage

**User**: "Set up OADP with Azure storage"

**Skill Actions**:

1. **Create Azure credentials secret**:
   ```bash
   cat <<EOF > ./credentials-velero
   AZURE_STORAGE_ACCOUNT_ACCESS_KEY=<STORAGE_ACCOUNT_ACCESS_KEY>
   AZURE_CLOUD_NAME=AzurePublicCloud
   EOF

   oc create secret generic cloud-credentials \
     --from-file cloud=./credentials-velero \
     -n openshift-adp

   rm -f ./credentials-velero
   ```

2. **Create DPA for Azure**:
   ```yaml
   apiVersion: oadp.openshift.io/v1alpha1
   kind: DataProtectionApplication
   metadata:
     name: dpa
     namespace: openshift-adp
   spec:
     configuration:
       velero:
         defaultPlugins:
           - openshift
           - azure
       kopia:
         enable: true
     backupLocations:
       - name: default
         velero:
           provider: azure
           default: true
           objectStorage:
             bucket: oadp-backups-container
             prefix: cluster-backups
           config:
             resourceGroup: oadp-rg
             storageAccount: oadpstorageacct
             subscriptionId: <AZURE_SUBSCRIPTION_ID>
           credential:
             name: cloud-credentials
             key: cloud
     snapshotLocations:
       - name: default
         velero:
           provider: azure
           config:
             resourceGroup: oadp-rg
             subscriptionId: <AZURE_SUBSCRIPTION_ID>
             incremental: "true"
   ```

### Example 3: Install OADP with MCG/NooBaa (OpenShift Data Foundation)

**User**: "Install OADP using internal MCG storage"

**Skill Actions**:

1. **Create MCG bucket (via ObjectBucketClaim)**:
   ```yaml
   apiVersion: objectbucket.io/v1alpha1
   kind: ObjectBucketClaim
   metadata:
     name: oadp-bucket
     namespace: openshift-adp
   spec:
     generateBucketName: oadp-backups
     storageClassName: openshift-storage.noobaa.io
     additionalConfig:
       bucketclass: noobaa-default-bucket-class
   ```

2. **Extract MCG credentials**:
   ```bash
   # Wait for bucket to be ready
   oc get obc oadp-bucket -n openshift-adp

   # Get bucket name
   BUCKET_NAME=$(oc get configmap oadp-bucket -n openshift-adp -o jsonpath='{.data.BUCKET_NAME}')

   # Get S3 endpoint
   S3_ENDPOINT=$(oc get configmap oadp-bucket -n openshift-adp -o jsonpath='{.data.BUCKET_HOST}')

   # Extract credentials from secret
   ACCESS_KEY=$(oc get secret oadp-bucket -n openshift-adp -o jsonpath='{.data.AWS_ACCESS_KEY_ID}' | base64 -d)
   SECRET_KEY=$(oc get secret oadp-bucket -n openshift-adp -o jsonpath='{.data.AWS_SECRET_ACCESS_KEY}' | base64 -d)
   ```

3. **Create cloud credentials secret for MCG**:
   ```bash
   cat <<EOF > ./credentials-velero
   [default]
   aws_access_key_id=$ACCESS_KEY
   aws_secret_access_key=$SECRET_KEY
   EOF

   oc create secret generic cloud-credentials-mcg \
     --from-file cloud=./credentials-velero \
     -n openshift-adp

   rm -f ./credentials-velero
   ```

4. **Create DPA for MCG**:
   ```yaml
   apiVersion: oadp.openshift.io/v1alpha1
   kind: DataProtectionApplication
   metadata:
     name: dpa
     namespace: openshift-adp
   spec:
     configuration:
       velero:
         defaultPlugins:
           - openshift
           - aws
       kopia:
         enable: true
     backupLocations:
       - name: mcg
         velero:
           provider: aws
           default: true
           objectStorage:
             bucket: ${BUCKET_NAME}
             prefix: openshift-backups
           config:
             region: noobaa
             s3ForcePathStyle: "true"
             s3Url: https://${S3_ENDPOINT}
             insecureSkipTLSVerify: "true"
           credential:
             name: cloud-credentials-mcg
             key: cloud
     snapshotLocations:
       - name: default
         velero:
           provider: csi
   ```

**Note**: When using MCG/NooBaa, use CSI for volume snapshots rather than cloud-provider native snapshots.

### Example 4: Install with Velero Built-in Data Mover Enabled

**User**: "Install OADP with Velero's built-in Data Mover for cross-region/cross-cluster backups"

**Note**: Data Mover is now built-in to Velero and uses Kopia for moving volume data to object storage, enabling backup portability across regions and clusters.

**Skill Actions**:

Create DPA with Kopia enabled (required for Data Mover):

```yaml
apiVersion: oadp.openshift.io/v1alpha1
kind: DataProtectionApplication
metadata:
  name: dpa
  namespace: openshift-adp
spec:
  configuration:
    velero:
      defaultPlugins:
        - openshift
        - aws
      featureFlags:
        - EnableCSI
    kopia:
      enable: true  # Required for built-in Data Mover
      podConfig:
        resourceAllocations:
          limits:
            cpu: "2"
            memory: 4Gi
  backupLocations:
    - name: default
      velero:
        provider: aws
        default: true
        objectStorage:
          bucket: oadp-backups
          prefix: cluster-backups
        config:
          region: us-east-1
        credential:
          name: cloud-credentials
          key: cloud
```

**Verification**:
```bash
# Check Kopia node-agent pods (handles Data Mover operations)
oc get pods -n openshift-adp -l component=node-agent

# Verify Kopia enabled
oc get dpa -n openshift-adp -o jsonpath='{.spec.configuration.kopia.enable}'

# Test Data Mover by creating backup with snapshotMoveData: true
velero backup create test-datamover --include-namespaces test --snapshot-move-data
```

### Example 5: Install with Multiple Backup Storage Locations

**User**: "Install OADP with primary and secondary backup locations"

**Skill Actions**:

Create DPA with multiple BSLs:

```yaml
apiVersion: oadp.openshift.io/v1alpha1
kind: DataProtectionApplication
metadata:
  name: dpa
  namespace: openshift-adp
spec:
  configuration:
    velero:
      defaultPlugins:
        - openshift
        - aws
  backupLocations:
    - name: primary-bsl
      velero:
        provider: aws
        default: true
        objectStorage:
          bucket: oadp-backups-primary
          prefix: cluster-backups
        config:
          region: us-east-1
        credential:
          name: cloud-credentials
          key: cloud
    - name: secondary-bsl
      velero:
        provider: aws
        default: false
        objectStorage:
          bucket: oadp-backups-secondary
          prefix: cluster-backups
        config:
          region: us-west-2  # Different region
        credential:
          name: cloud-credentials-west
          key: cloud
```

**Use Case**: Geographic redundancy with backups in multiple regions.

## Verification Checklist

After installation, verify:

- [ ] OADP operator CSV shows "Succeeded"
- [ ] Velero deployment has 1/1 pods ready
- [ ] Kopia (or legacy Restic) daemonset running on all worker nodes
- [ ] BackupStorageLocation shows "Available"
- [ ] VolumeSnapshotLocation configured (if using)
- [ ] No errors in oadp-operator logs
- [ ] No errors in velero logs
- [ ] Can create test backup successfully

**Verification Commands**:
```bash
# Check all components
oc get csv,deploy,ds,bsl,vsl -n openshift-adp

# Check logs for errors
oc logs -n openshift-adp deployment/oadp-operator-controller-manager --tail=50
oc logs -n openshift-adp deployment/velero --tail=50

# Test BSL connectivity
velero backup-location get

# Create test backup
velero backup create test-backup --include-namespaces default
velero backup describe test-backup
```

## Troubleshooting

### Operator Not Installing

**Symptoms**: Subscription created but CSV not appearing

**Diagnosis**:
```bash
oc get subscription -n openshift-adp
oc describe subscription oadp-operator -n openshift-adp
oc get installplan -n openshift-adp
```

**Solution**: Check catalog source availability and operator image pull

### BSL Shows Unavailable

**Symptoms**: BackupStorageLocation phase is "Unavailable"

**Common Causes**:
1. Invalid credentials
2. Bucket doesn't exist
3. Network connectivity issues
4. Wrong region configuration

**Fix**:
```bash
# Test credentials manually
aws s3 ls s3://bucket-name

# Check BSL status
oc describe backupstoragelocations -n openshift-adp

# Check velero logs
oc logs -n openshift-adp deployment/velero | grep -i error
```

### Kopia/Restic Pods Not Starting

**Symptoms**: Kopia (or legacy Restic) daemonset pods failing

**Diagnosis**:
```bash
# For Kopia (OADP 1.4+)
oc get ds node-agent -n openshift-adp
oc describe ds node-agent -n openshift-adp
oc logs -n openshift-adp ds/node-agent

# For legacy Restic (OADP 1.3 and earlier)
oc get ds restic -n openshift-adp
oc describe ds restic -n openshift-adp
oc logs -n openshift-adp ds/restic
```

**Common Issues**:
- Node selector not matching
- Privileged SCC not granted
- Hostpath mount issues

**Solution**:
```bash
# Verify SCC
oc get scc | grep privileged

# Check node-agent (Kopia) service account
oc get sa node-agent -n openshift-adp -o yaml

# For legacy Restic
oc get sa restic -n openshift-adp -o yaml
```

## Best Practices

1. **Credentials Security**
   - Use separate credentials for backup storage
   - Rotate credentials periodically
   - Never commit credentials to version control
   - Use read-write permissions (not admin)

2. **Resource Allocation**
   - Allocate sufficient CPU/memory for Velero
   - Scale Kopia node-agent based on cluster size
   - Monitor resource usage during backups
   - Note: Kopia (node-agent) is more efficient than legacy Restic

3. **High Availability**
   - Configure multiple BackupStorageLocations
   - Use different regions for redundancy
   - Test failover scenarios

4. **Monitoring**
   - Set up alerts for BSL availability
   - Monitor backup completion rates
   - Track backup storage usage
   - Alert on backup failures

5. **Testing**
   - Create test backups after installation
   - Verify restore functionality
   - Test in non-production first
   - Document installation steps

## Next Steps

After successful installation:

1. **Create First Backup**: Test the installation with a simple namespace backup
2. **Set Up Schedules**: Configure automated backup schedules
3. **Test Restore**: Verify restore functionality
4. **Configure Monitoring**: Set up alerts and monitoring
5. **Document Configuration**: Record settings for disaster recovery

**Related Skills**:
- create-backup - Create backup resources
- restore-backup - Restore from backups
- diagnose-backup-issues - Troubleshoot backup problems

## Configuration Reference

### Common DPA Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| `configuration.velero.defaultPlugins` | Plugins to enable | `[]` |
| `configuration.kopia.enable` | Enable Kopia file-level backup (OADP 1.4+); Required for Velero's built-in Data Mover | `false` |
| `configuration.restic.enable` | Enable Restic file-level backup (deprecated, use Kopia) | `false` |
| `backupLocations[].velero.default` | Default BSL | `false` |
| `configuration.velero.podConfig.resourceAllocations` | Resource limits/requests | CPU: 500m, Mem: 512Mi |

**Note**: Data Mover is now built-in to Velero and does not require separate DPA configuration. Enable Kopia to use Data Mover functionality via `snapshotMoveData: true` in backup specs.

### Supported Providers

- **AWS**: S3, EBS snapshots
- **Azure**: Blob Storage, Managed Disks
- **GCP**: Cloud Storage, Persistent Disks
- **CSI**: Generic CSI snapshot support
- **MCG/NooBaa**: OpenShift Data Foundation
- **IBM Cloud**: Cloud Object Storage

## Resources

- **Official Documentation**: https://docs.openshift.com/container-platform/latest/backup_and_restore/application_backup_and_restore/installing/about-installing-oadp.html
- **OADP GitHub**: https://github.com/openshift/oadp-operator
- **Velero Documentation**: https://velero.io/docs/

---

**Version**: 1.0
**Last Updated**: 2025-11-17
**Compatibility**: OADP 1.3+, OpenShift 4.12+
