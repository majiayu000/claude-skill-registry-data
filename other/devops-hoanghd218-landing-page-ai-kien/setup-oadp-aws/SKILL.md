---
name: setup-oadp-aws
description: Configure OADP for AWS with S3 storage, EBS snapshots, IAM policies, and support for standard clusters and ROSA (Red Hat OpenShift Service on AWS).
---

# Setup OADP for AWS

This skill provides comprehensive guidance for configuring OADP on AWS-based OpenShift clusters, including S3 bucket setup, IAM permissions, EBS volume snapshots, and ROSA-specific configurations.

## When to Use This Skill

- **AWS Clusters**: Setting up OADP on OpenShift clusters running on AWS EC2
- **ROSA Clusters**: Configuring OADP on Red Hat OpenShift Service on AWS
- **AWS STS**: Using AWS Security Token Service for authentication
- **S3 Storage**: Configuring S3 as backup storage location
- **EBS Snapshots**: Setting up EBS volume snapshot integration
- **Cross-Region**: Configuring multi-region backup redundancy

## What This Skill Does

1. **Creates S3 Bucket**: Sets up S3 bucket for backup storage
2. **Configures IAM**: Creates IAM users/roles with required permissions
3. **Sets Up Credentials**: Configures AWS credentials for OADP
4. **Configures DPA**: Creates DataProtectionApplication with AWS provider
5. **Enables EBS Snapshots**: Configures VolumeSnapshotLocation for EBS
6. **Validates Setup**: Tests S3 connectivity and snapshot capabilities
7. **Optimizes Configuration**: Tunes settings for AWS-specific performance

## How to Use

### Basic Usage

```
Setup OADP for AWS with S3 bucket
```

```
Configure OADP on ROSA cluster
```

### Advanced Usage

```
Setup OADP with AWS STS authentication
```

```
Configure multi-region AWS backup with failover
```

## Prerequisites

Before setting up OADP on AWS:

- [ ] OpenShift cluster running on AWS or ROSA
- [ ] AWS CLI configured with admin credentials
- [ ] OADP operator installed (see install-oadp skill)
- [ ] S3 bucket created or permissions to create one
- [ ] IAM permissions to create users/roles/policies
- [ ] Understanding of AWS regions and availability zones

## Examples

### Example 1: Basic AWS Setup with IAM User

**User**: "Setup OADP with AWS S3 using IAM user credentials"

**Skill Actions**:

1. **Create S3 bucket**:
   ```bash
   # Set variables
   BUCKET_NAME="oadp-backups-$(date +%s)"
   AWS_REGION="us-east-1"

   # Create bucket
   aws s3 mb s3://$BUCKET_NAME --region $AWS_REGION

   # Enable versioning (recommended)
   aws s3api put-bucket-versioning \
     --bucket $BUCKET_NAME \
     --versioning-configuration Status=Enabled

   # Enable encryption
   aws s3api put-bucket-encryption \
     --bucket $BUCKET_NAME \
     --server-side-encryption-configuration '{
       "Rules": [{
         "ApplyServerSideEncryptionByDefault": {
           "SSEAlgorithm": "AES256"
         }
       }]
     }'

   echo "S3 bucket created: $BUCKET_NAME"
   ```

2. **Create IAM policy for OADP**:
   ```bash
   # Create policy document
   cat <<EOF > oadp-s3-policy.json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Action": [
           "s3:GetObject",
           "s3:DeleteObject",
           "s3:PutObject",
           "s3:AbortMultipartUpload",
           "s3:ListMultipartUploadParts"
         ],
         "Resource": [
           "arn:aws:s3:::$BUCKET_NAME/*"
         ]
       },
       {
         "Effect": "Allow",
         "Action": [
           "s3:ListBucket",
           "s3:GetBucketLocation",
           "s3:ListBucketMultipartUploads"
         ],
         "Resource": [
           "arn:aws:s3:::$BUCKET_NAME"
         ]
       },
       {
         "Effect": "Allow",
         "Action": [
           "ec2:DescribeVolumes",
           "ec2:DescribeSnapshots",
           "ec2:CreateTags",
           "ec2:CreateVolume",
           "ec2:CreateSnapshot",
           "ec2:DeleteSnapshot"
         ],
         "Resource": "*"
       }
     ]
   }
   EOF

   # Create IAM policy
   aws iam create-policy \
     --policy-name OADPBackupPolicy \
     --policy-document file://oadp-s3-policy.json

   POLICY_ARN=$(aws iam list-policies --query 'Policies[?PolicyName==`OADPBackupPolicy`].Arn' --output text)
   echo "IAM Policy ARN: $POLICY_ARN"
   ```

3. **Create IAM user and attach policy**:
   ```bash
   # Create IAM user
   aws iam create-user --user-name oadp-backup-user

   # Attach policy to user
   aws iam attach-user-policy \
     --user-name oadp-backup-user \
     --policy-arn $POLICY_ARN

   # Create access keys
   aws iam create-access-key --user-name oadp-backup-user > oadp-access-keys.json

   # Extract credentials
   AWS_ACCESS_KEY_ID=$(jq -r '.AccessKey.AccessKeyId' oadp-access-keys.json)
   AWS_SECRET_ACCESS_KEY=$(jq -r '.AccessKey.SecretAccessKey' oadp-access-keys.json)

   echo "Access Key ID: $AWS_ACCESS_KEY_ID"
   echo "Secret saved in oadp-access-keys.json - store securely!"
   ```

4. **Create credentials secret in OpenShift**:
   ```bash
   # Create credentials file
   cat <<EOF > credentials-velero
   [default]
   aws_access_key_id=$AWS_ACCESS_KEY_ID
   aws_secret_access_key=$AWS_SECRET_ACCESS_KEY
   EOF

   # Create secret
   oc create secret generic cloud-credentials \
     --from-file cloud=credentials-velero \
     -n openshift-adp

   # Clean up local credentials
   rm -f credentials-velero oadp-access-keys.json
   ```

5. **Create DataProtectionApplication**:
   ```yaml
   apiVersion: oadp.openshift.io/v1alpha1
   kind: DataProtectionApplication
   metadata:
     name: dpa-aws
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
         enable: true
       # Note: Restic is deprecated in OADP 1.4+, use Kopia for new deployments
     backupLocations:
       - name: default
         velero:
           provider: aws
           default: true
           objectStorage:
             bucket: $BUCKET_NAME
             prefix: cluster-backups
           config:
             region: $AWS_REGION
           credential:
             name: cloud-credentials
             key: cloud
     snapshotLocations:
       - name: default
         velero:
           provider: aws
           config:
             region: $AWS_REGION
   ```

6. **Verify setup**:
   ```bash
   # Check DPA status
   oc get dpa -n openshift-adp

   # Check BackupStorageLocation
   oc get backupstoragelocations -n openshift-adp

   # Verify BSL is Available
   oc get bsl -n openshift-adp -o jsonpath='{.items[0].status.phase}'

   # Test S3 connectivity
   velero backup-location get
   ```

**Success Indicators**:
- ✅ S3 bucket created with versioning and encryption
- ✅ IAM policy and user created
- ✅ BackupStorageLocation shows "Available"
- ✅ VolumeSnapshotLocation configured for EBS

### Example 2: ROSA Setup with AWS STS

**User**: "Configure OADP on ROSA cluster using STS authentication"

**Skill Actions**:

1. **Create S3 bucket** (same as Example 1):
   ```bash
   BUCKET_NAME="oadp-rosa-backups-$(date +%s)"
   AWS_REGION="us-east-1"

   aws s3 mb s3://$BUCKET_NAME --region $AWS_REGION
   aws s3api put-bucket-versioning --bucket $BUCKET_NAME --versioning-configuration Status=Enabled
   ```

2. **Get ROSA cluster OIDC provider**:
   ```bash
   # Get ROSA cluster ID
   CLUSTER_NAME="my-rosa-cluster"
   CLUSTER_ID=$(rosa describe cluster -c $CLUSTER_NAME -o json | jq -r .id)

   # Get OIDC endpoint
   OIDC_ENDPOINT=$(rosa describe cluster -c $CLUSTER_NAME -o json | jq -r .aws.sts.oidc_endpoint_url)
   OIDC_ENDPOINT=${OIDC_ENDPOINT#https://}

   echo "OIDC Endpoint: $OIDC_ENDPOINT"
   ```

3. **Create IAM trust policy for STS**:
   ```bash
   # Get AWS account ID
   AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

   # Create trust policy
   cat <<EOF > trust-policy.json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Principal": {
           "Federated": "arn:aws:iam::${AWS_ACCOUNT_ID}:oidc-provider/${OIDC_ENDPOINT}"
         },
         "Action": "sts:AssumeRoleWithWebIdentity",
         "Condition": {
           "StringEquals": {
             "${OIDC_ENDPOINT}:sub": [
               "system:serviceaccount:openshift-adp:velero",
               "system:serviceaccount:openshift-adp:openshift-adp-controller-manager"
             ]
           }
         }
       }
     ]
   }
   EOF
   ```

4. **Create IAM role with STS**:
   ```bash
   # Create IAM role
   aws iam create-role \
     --role-name ROSA-OADP-Role \
     --assume-role-policy-document file://trust-policy.json \
     --description "OADP backup role for ROSA with STS"

   # Attach OADP policy (created earlier)
   aws iam attach-role-policy \
     --role-name ROSA-OADP-Role \
     --policy-arn $POLICY_ARN

   # Get role ARN
   ROLE_ARN=$(aws iam get-role --role-name ROSA-OADP-Role --query Role.Arn --output text)
   echo "Role ARN: $ROLE_ARN"
   ```

5. **Create credentials secret with STS role**:
   ```bash
   # Create credentials file for STS
   cat <<EOF > credentials-velero
   [default]
   role_arn=$ROLE_ARN
   web_identity_token_file=/var/run/secrets/openshift/serviceaccount/token
   EOF

   # Create secret
   oc create secret generic cloud-credentials-sts \
     --from-file cloud=credentials-velero \
     -n openshift-adp

   rm credentials-velero
   ```

6. **Create DPA for ROSA with STS**:
   ```yaml
   apiVersion: oadp.openshift.io/v1alpha1
   kind: DataProtectionApplication
   metadata:
     name: dpa-rosa-sts
     namespace: openshift-adp
   spec:
     configuration:
       velero:
         defaultPlugins:
           - openshift
           - aws
         podConfig:
           env:
             - name: AWS_ROLE_ARN
               value: $ROLE_ARN
             - name: AWS_WEB_IDENTITY_TOKEN_FILE
               value: /var/run/secrets/openshift/serviceaccount/token
           volumes:
             - name: bound-sa-token
               projected:
                 sources:
                   - serviceAccountToken:
                       path: token
                       expirationSeconds: 3600
                       audience: openshift
           volumeMounts:
             - name: bound-sa-token
               mountPath: /var/run/secrets/openshift/serviceaccount
       kopia:
         enable: true
         podConfig:
           env:
             - name: AWS_ROLE_ARN
               value: $ROLE_ARN
             - name: AWS_WEB_IDENTITY_TOKEN_FILE
               value: /var/run/secrets/openshift/serviceaccount/token
     backupLocations:
       - name: default
         velero:
           provider: aws
           default: true
           objectStorage:
             bucket: $BUCKET_NAME
             prefix: rosa-backups
           config:
             region: $AWS_REGION
           credential:
             name: cloud-credentials-sts
             key: cloud
     snapshotLocations:
       - name: default
         velero:
           provider: aws
           config:
             region: $AWS_REGION
   ```

**ROSA-Specific Notes**:
- STS provides temporary credentials via OIDC
- No long-lived access keys required
- ServiceAccount token refreshed automatically
- More secure than static IAM users

### Example 3: Multi-Region AWS Setup

**User**: "Configure OADP with primary and secondary regions for DR"

**Skill Actions**:

1. **Create S3 buckets in multiple regions**:
   ```bash
   PRIMARY_REGION="us-east-1"
   SECONDARY_REGION="us-west-2"
   PRIMARY_BUCKET="oadp-primary-$(date +%s)"
   SECONDARY_BUCKET="oadp-secondary-$(date +%s)"

   # Create primary bucket
   aws s3 mb s3://$PRIMARY_BUCKET --region $PRIMARY_REGION
   aws s3api put-bucket-versioning --bucket $PRIMARY_BUCKET --versioning-configuration Status=Enabled

   # Create secondary bucket
   aws s3 mb s3://$SECONDARY_BUCKET --region $SECONDARY_REGION
   aws s3api put-bucket-versioning --bucket $SECONDARY_BUCKET --versioning-configuration Status=Enabled

   # Optional: Enable cross-region replication
   # (Requires additional IAM role and replication configuration)
   ```

2. **Create multi-region DPA**:
   ```yaml
   apiVersion: oadp.openshift.io/v1alpha1
   kind: DataProtectionApplication
   metadata:
     name: dpa-multi-region
     namespace: openshift-adp
   spec:
     configuration:
       velero:
         defaultPlugins:
           - openshift
           - aws
     backupLocations:
       - name: primary-us-east
         velero:
           provider: aws
           default: true
           objectStorage:
             bucket: $PRIMARY_BUCKET
             prefix: cluster-backups
           config:
             region: us-east-1
           credential:
             name: cloud-credentials
             key: cloud
       - name: secondary-us-west
         velero:
           provider: aws
           default: false
           objectStorage:
             bucket: $SECONDARY_BUCKET
             prefix: cluster-backups
           config:
             region: us-west-2
           credential:
             name: cloud-credentials
             key: cloud
     snapshotLocations:
       - name: primary-snapshots
         velero:
           provider: aws
           config:
             region: us-east-1
       - name: secondary-snapshots
         velero:
           provider: aws
           config:
             region: us-west-2
   ```

3. **Create backup to specific region**:
   ```bash
   # Backup to primary region (default)
   velero backup create app-backup-primary \
     --include-namespaces myapp

   # Backup to secondary region
   velero backup create app-backup-secondary \
     --include-namespaces myapp \
     --storage-location secondary-us-west \
     --volume-snapshot-locations secondary-snapshots
   ```

### Example 4: S3-Compatible Storage (MinIO, Wasabi)

**User**: "Setup OADP with S3-compatible storage"

**Skill Actions**:

Create DPA for S3-compatible endpoint:

```yaml
apiVersion: oadp.openshift.io/v1alpha1
kind: DataProtectionApplication
metadata:
  name: dpa-s3-compatible
  namespace: openshift-adp
spec:
  configuration:
    velero:
      defaultPlugins:
        - openshift
        - aws
  backupLocations:
    - name: s3-compatible
      velero:
        provider: aws
        default: true
        objectStorage:
          bucket: oadp-backups
          prefix: openshift
        config:
          region: minio  # Arbitrary for non-AWS
          s3ForcePathStyle: "true"  # Required for MinIO/others
          s3Url: https://minio.example.com:9000  # Custom endpoint
          insecureSkipTLSVerify: "false"  # Set true for self-signed certs
        credential:
          name: cloud-credentials
          key: cloud
```

**Credentials for S3-compatible**:
```bash
# Same format as AWS
cat <<EOF > credentials-velero
[default]
aws_access_key_id=<MINIO_ACCESS_KEY>
aws_secret_access_key=<MINIO_SECRET_KEY>
EOF
```

## AWS-Specific Configuration Options

### S3 Bucket Configuration

**Recommended S3 settings**:
```bash
# Enable versioning (for backup recovery)
aws s3api put-bucket-versioning \
  --bucket $BUCKET_NAME \
  --versioning-configuration Status=Enabled

# Enable server-side encryption
aws s3api put-bucket-encryption \
  --bucket $BUCKET_NAME \
  --server-side-encryption-configuration '{
    "Rules": [{
      "ApplyServerSideEncryptionByDefault": {
        "SSEAlgorithm": "AES256"
      },
      "BucketKeyEnabled": true
    }]
  }'

# Configure lifecycle policy (optional)
aws s3api put-bucket-lifecycle-configuration \
  --bucket $BUCKET_NAME \
  --lifecycle-configuration file://lifecycle-policy.json
```

**Lifecycle policy example**:
```json
{
  "Rules": [
    {
      "Id": "TransitionOldBackups",
      "Status": "Enabled",
      "Transitions": [
        {
          "Days": 30,
          "StorageClass": "STANDARD_IA"
        },
        {
          "Days": 90,
          "StorageClass": "GLACIER"
        }
      ],
      "NoncurrentVersionExpiration": {
        "NoncurrentDays": 90
      }
    }
  ]
}
```

### EBS Snapshot Configuration

**VolumeSnapshotClass for EBS**:
```yaml
apiVersion: snapshot.storage.k8s.io/v1
kind: VolumeSnapshotClass
metadata:
  name: oadp-ebs-snapclass
  labels:
    velero.io/csi-volumesnapshot-class: "true"
driver: ebs.csi.aws.com
deletionPolicy: Retain
parameters:
  tagSpecification_1: "Name=velero-backup"
  tagSpecification_2: "ManagedBy=oadp"
```

### Performance Tuning

**Optimize for large AWS deployments**:
```yaml
spec:
  configuration:
    velero:
      podConfig:
        resourceAllocations:
          limits:
            cpu: "2"
            memory: 2Gi
          requests:
            cpu: "1"
            memory: 1Gi
      args:
        - --max-concurrent-k8s-connections=50
        - --resource-timeout=10m
    kopia:
      podConfig:
        resourceAllocations:
          limits:
            cpu: "2"
            memory: 4Gi
        env:
          - name: KOPIA_PARALLEL_FILE_OPERATIONS
            value: "8"
```

## Troubleshooting

### BSL Shows Unavailable

**Symptoms**: BackupStorageLocation phase is "Unavailable" on AWS

**Common AWS-specific causes**:

1. **IAM permissions insufficient**:
   ```bash
   # Test S3 access
   aws s3 ls s3://$BUCKET_NAME

   # Test with Velero pod's credentials
   oc exec -n openshift-adp deployment/velero -- aws s3 ls s3://$BUCKET_NAME
   ```

2. **Wrong region**:
   ```bash
   # Check bucket region
   aws s3api get-bucket-location --bucket $BUCKET_NAME

   # Verify matches DPA configuration
   oc get dpa -n openshift-adp -o yaml | grep region
   ```

3. **S3 endpoint unreachable**:
   ```bash
   # Test from Velero pod
   oc exec -n openshift-adp deployment/velero -- curl -I https://s3.$AWS_REGION.amazonaws.com
   ```

### EBS Snapshot Failures

**Symptoms**: Volume snapshots fail with AWS errors

**Diagnosis**:
```bash
# Check VolumeSnapshot status
oc get volumesnapshots -A

# Check VolumeSnapshot errors
oc describe volumesnapshot <snapshot-name> -n <namespace>

# Check CSI driver logs
oc logs -n openshift-cluster-csi-drivers -l app=aws-ebs-csi-driver
```

**Common issues**:
- IAM role missing EC2 snapshot permissions
- EBS volume in different AZ than snapshot location
- Volume encryption key access denied
- Snapshot quota exceeded

### STS Token Expiration

**Symptoms**: ROSA/STS backups fail intermittently

**Solution**:
```yaml
# Increase token expiration in DPA
spec:
  configuration:
    velero:
      podConfig:
        volumes:
          - name: bound-sa-token
            projected:
              sources:
                - serviceAccountToken:
                    path: token
                    expirationSeconds: 7200  # Increase from 3600
```

## Best Practices

1. **Use IAM Roles over Users**
   - Prefer STS/IRSA for ROSA
   - Use IAM roles for EC2-based clusters
   - Rotate credentials regularly
   - Use least-privilege permissions

2. **Enable S3 Features**
   - Versioning for backup recovery
   - Encryption at rest
   - Access logging
   - Lifecycle policies for cost optimization

3. **Multi-Region Strategy**
   - Primary and secondary BSLs
   - Cross-region replication for critical data
   - Test cross-region restore
   - Document failover procedures

4. **Cost Optimization**
   - Use S3 Intelligent-Tiering
   - Implement lifecycle policies
   - Delete old snapshots
   - Monitor S3 storage costs

5. **Security**
   - Encrypt S3 buckets
   - Use VPC endpoints for S3 access
   - Enable S3 access logs
   - Restrict IAM policies to specific buckets
   - Use KMS for encryption keys

## Verification Checklist

After AWS setup:

- [ ] S3 bucket created with versioning enabled
- [ ] S3 bucket encrypted at rest
- [ ] IAM user/role created with correct permissions
- [ ] Credentials secret created in openshift-adp namespace
- [ ] DPA applied and reconciled successfully
- [ ] BackupStorageLocation shows "Available"
- [ ] VolumeSnapshotLocation configured
- [ ] Test backup created successfully
- [ ] Can list backups in S3 bucket
- [ ] EBS snapshot created during test backup

## Next Steps

After AWS setup:

1. **Test Backup**: Create test backup with EBS volumes
2. **Test Restore**: Verify cross-AZ and cross-region restore
3. **Configure Schedules**: Set up automated backup schedules
4. **Monitor Costs**: Track S3 and EBS snapshot costs
5. **Document**: Record AWS account, bucket names, IAM details

**Related Skills**:
- install-oadp - Install OADP operator
- create-backup - Create backups
- backup-etcd - Backup etcd for control plane DR

## Resources

- **AWS OADP Documentation**: https://docs.openshift.com/container-platform/latest/backup_and_restore/application_backup_and_restore/installing/installing-oadp-aws.html
- **ROSA OADP Guide**: https://docs.openshift.com/rosa/rosa_backing_up_and_restoring_applications/backing-up-applications.html
- **AWS STS**: https://docs.aws.amazon.com/STS/latest/APIReference/welcome.html

---

**Version**: 1.0
**Last Updated**: 2025-11-17
**Tested With**: OADP 1.3+, AWS, ROSA
