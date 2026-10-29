---
name: aws-enumeration
description: Use when enumerating an AWS environment during an authorized cloud
  assessment, bug bounty engagement, or lab exercise. Covers identity and
  account context with sts get-caller-identity, IAM users, roles, groups and
  policies, EC2 instances, security groups and AMIs, S3 buckets, Lambda
  functions, Secrets Manager, RDS, and CloudTrail configuration using
  aws-cli 2.22 and Python 3.12. Use when you hold AWS credentials for a test
  account and need to map what the principal can reach, or when the scope
  permits unauthenticated checks of public buckets and resources.
version: 1.0.0
domain: cloud
lifecycle: stable
last_verified: "2026-10-23"
requires: []
extends: []
relates: [cloud-security-basics, recon-passive]
tools:
  - name: aws-cli
    version: "2.22"
  - name: Python
    version: "3.12"
---

AWS enumeration maps what an identity can see and touch inside an AWS
account: who you are, which permissions you hold, which resources exist,
and where data lives. This skill covers the authorized operator workflow
for a full account survey with the AWS CLI: identity context, IAM,
compute, storage, serverless, secrets, and logging configuration, plus
safe unauthenticated checks of public resources. Use it against your own
accounts, in-scope bug bounty targets, and lab environments only. Never
enumerate accounts you do not have written permission to test.

## Quick Workflow

1. Confirm identity and account: run `sts get-caller-identity`, note the
   account ID, ARN, and credential source.
2. Enumerate the principal's own IAM surface: user or role, attached
   policies, groups, and instance profile if on EC2.
3. List IAM principals account-wide if readable: users, roles, groups,
   managed policies, and their attachments.
4. Survey EC2: instances, security groups, VPCs, AMIs, snapshots, and
   EBS volumes.
5. Survey S3: list every bucket, then check each bucket's ACL, policy,
   public access block, encryption, versioning, and logging.
6. Survey serverless and data services: Lambda functions, API Gateway
   APIs, RDS instances, DynamoDB tables, Secrets Manager secrets.
7. Check logging and guardrails: CloudTrail trails and their status,
   Config recorders, GuardDuty detectors.
8. Run safe unauthenticated checks: public bucket reads, public AMIs
   and snapshots, exposed instance metadata only from inside your own
   instances.
9. Repeat the survey in every enabled region, not just the default one.
10. Save every command and its raw JSON output for the report.

## 1. Identity and account context

Start here on every engagement. The ARN tells you whether you are a user,
an assumed role, or a federated identity, and each type enumerates
differently.

```bash
# Who am I, which account, which ARN
aws sts get-caller-identity

# Where did these credentials come from (env, profile, SSO, instance role)
aws configure list
env | grep -i '^AWS_' | sed 's/=.*$/=<redacted>/'

# Human readable account alias, if set
aws iam list-account-aliases --query 'AccountAliases' --output text

# All regions enabled for this account
aws ec2 describe-regions --query 'Regions[].RegionName' --output text
```

If you are on an EC2 instance, check for an instance profile, which is
the most common credential source in labs and CTFs:

```bash
# From inside the instance only: which role is attached (IMDSv2, token first)
TOKEN=$(curl -s -X PUT "http://169.254.169.254/latest/api/token" \
  -H "X-aws-ec2-metadata-token-ttl-seconds: 60")
curl -s -H "X-aws-ec2-metadata-token: $TOKEN" \
  http://169.254.169.254/latest/meta-data/iam/security-credentials/
```

## 2. IAM enumeration

IAM is the map of who can do what. Read the principal's own surface
first, then widen to the account if the policy allows it.

```bash
# If the principal is a user: own details, attached and inline policies
aws iam get-user --query 'User.[UserName,Arn,CreateDate]' --output text
aws iam list-attached-user-policies --user-name <USER> \
  --query 'AttachedPolicies[].PolicyName' --output text
aws iam list-user-policies --user-name <USER> \
  --query 'PolicyNames' --output text

# Groups the user belongs to, and what those groups grant
aws iam list-groups-for-user --user-name <USER> \
  --query 'Groups[].GroupName' --output text
aws iam list-attached-group-policies --group-name <GROUP> \
  --query 'AttachedPolicies[].PolicyName' --output text

# If the principal is a role: trust policy shows who can assume it
aws iam get-role --role-name <ROLE> \
  --query 'Role.AssumeRolePolicyDocument'

# Account-wide principal listing (needs iam:List* permissions)
aws iam list-users --query 'Users[].[UserName,Arn]' --output text
aws iam list-roles --query 'Roles[].[RoleName,Arn]' --output text
aws iam list-groups --query 'Groups[].GroupName' --output text
aws iam list-policies --scope Local \
  --query 'Policies[].[PolicyName,Arn]' --output text
```

Read a managed policy's actual permissions through its default version:

```bash
# Find the default version, then fetch the document
aws iam get-policy --policy-arn arn:aws:iam::123456789012:policy/<NAME> \
  --query 'Policy.DefaultVersionId' --output text
aws iam get-policy-version \
  --policy-arn arn:aws:iam::123456789012:policy/<NAME> \
  --version-id v1 --query 'PolicyVersion.Document'
```

## 3. Compute and network enumeration

EC2 inventory shows running workloads, exposed ports, and public
resources shared with other accounts.

```bash
# Instances in the current region: ID, type, state, public IP, tags
aws ec2 describe-instances \
  --query 'Reservations[].Instances[].[InstanceId,InstanceType,State.Name,PublicIpAddress,Tags[?Key==`Name`].Value | [0]]' \
  --output text

# Security groups: open ingress rules are the interesting part
aws ec2 describe-security-groups \
  --query 'SecurityGroups[].[GroupId,GroupName,IpPermissions]' \
  --output json | head -100

# VPCs, subnets, and public IPs
aws ec2 describe-vpcs --query 'Vpcs[].[VpcId,CidrBlock]' --output text
aws ec2 describe-subnets \
  --query 'Subnets[].[SubnetId,VpcId,CidrBlock,MapPublicIpOnLaunch]' \
  --output text
aws ec2 describe-addresses --query 'Addresses[].[PublicIp,InstanceId]' \
  --output text

# AMIs and snapshots owned by the account (check for public sharing)
aws ec2 describe-images --owners self \
  --query 'Images[].[ImageId,Name,Public]' --output text
aws ec2 describe-snapshots --owner-ids self \
  --query 'Snapshots[].[SnapshotId,VolumeSize,Description]' --output text
```

## 4. S3 enumeration

List every bucket, then inspect each one. Bucket names are globally
unique, so a full list is also useful for unauthenticated checks later.

```bash
# All buckets visible to this principal
aws s3 ls

# Per-bucket security posture (replace <BUCKET> each time)
aws s3api get-bucket-acl --bucket <BUCKET> \
  --query 'Grants[].[Grantee.URI,Permission]' --output text
aws s3api get-bucket-policy --bucket <BUCKET> \
  --query 'Policy' --output text 2>/dev/null | head -c 2000
aws s3api get-public-access-block --bucket <BUCKET> 2>/dev/null
aws s3api get-bucket-encryption --bucket <BUCKET> 2>/dev/null
aws s3api get-bucket-versioning --bucket <BUCKET>
aws s3api get-bucket-logging --bucket <BUCKET> 2>/dev/null
aws s3api get-bucket-website --bucket <BUCKET> 2>/dev/null \
  && echo "STATIC WEBSITE HOSTING IS ON"

# What objects sit at the top level (first page only, stay read-only)
aws s3 ls s3://<BUCKET>/ --human-readable | head -20
```

The detailed misconfiguration checks live in the s3-misconfigurations
skill. This section is the inventory pass that feeds it.

## 5. Serverless, databases, and secrets

Modern accounts hide their interesting data in managed services. Cover
them in the same pass.

```bash
# Lambda: function names, runtimes, roles, environment variables
aws lambda list-functions \
  --query 'Functions[].[FunctionName,Runtime,Role,LastModified]' \
  --output text
aws lambda get-function-configuration --function-name <FUNC> \
  --query '{Role:Role, Env:Environment.Variables, Vpc:VpcConfig}'

# API Gateway: REST and HTTP APIs that front the Lambdas
aws apigateway get-rest-apis --query 'items[].[id,name]' --output text
aws apigatewayv2 get-apis --query 'Items[].[ApiId,Name,ProtocolType]' \
  --output text

# RDS databases: engine, endpoint, public accessibility
aws rds describe-db-instances \
  --query 'DBInstances[].[DBInstanceIdentifier,Engine,Endpoint.Address,PubliclyAccessible]' \
  --output text

# DynamoDB tables and Secrets Manager secret names (names only, no values)
aws dynamodb list-tables --query 'TableNames' --output text
aws secretsmanager list-secrets \
  --query 'SecretList[].[Name,Description]' --output text
```

Only read secret VALUES when the rules of engagement explicitly allow
it, and record exactly which secrets you touched.

## 6. Logging and guardrails

Knowing what is logged tells you how noisy the rest of your testing
will be, and missing logging is itself a finding.

```bash
# CloudTrail: trails, where they log, and whether they are recording
aws cloudtrail describe-trails \
  --query 'trailList[].[Name,S3BucketName,IsMultiRegionTrail,IsOrganizationTrail]' \
  --output text
aws cloudtrail get-trail-status --name <TRAIL> \
  --query '{Logging:IsLogging, LastEvent: LatestDeliveryTime}'

# AWS Config recorders and GuardDuty detectors
aws configservice describe-configuration-recorders \
  --query 'ConfigurationRecorders[].[name,recordingGroup]' 2>/dev/null
aws guardduty list-detectors --query 'DetectorIds' --output text 2>/dev/null
```

## 7. Unauthenticated and public resource checks

Some resources are visible without any credentials. Only test resources
inside your scope, and stay read-only.

```bash
# Public bucket read test (no credentials used)
aws s3 ls s3://<BUCKET> --no-sign-request 2>&1 | head -5

# Public AMI shared with everyone
aws ec2 describe-images --image-ids ami-<ID> \
  --query 'Images[].[ImageId,Public]' --output text

# Public snapshot check
aws ec2 describe-snapshots --snapshot-ids snap-<ID> \
  --query 'Snapshots[].[SnapshotId]' --output text 2>&1 | head -3
```

## 8. Region sweep

Resources hide in regions you did not check. Loop the read-only calls
across every enabled region.

```bash
for r in $(aws ec2 describe-regions \
  --query 'Regions[].RegionName' --output text); do
  echo "=== $r ==="
  aws ec2 describe-instances --region "$r" \
    --query 'Reservations[].Instances[].[InstanceId,State.Name]' \
    --output text
  aws lambda list-functions --region "$r" \
    --query 'Functions[].FunctionName' --output text 2>/dev/null
done
```

## Edge cases

- `AccessDenied` on `iam:ListUsers` but you can still call
  `iam:GetUser`: enumerate your own surface deeply and use
  `SimulatePrincipalPolicy` to test individual actions instead of
  listing everything.
- Output is paginated or truncated: add `--max-items 1000` and follow
  `NextToken`, or set the CLI pager off with `--no-cli-pager` in
  scripts.
- The principal is federated (SSO, web identity): `iam:GetUser` fails
  with NoSuchEntity. Use `sts:GetCallerIdentity` plus role policy
  reads instead.
- Service control policies (SCPs) or permissions boundaries silently
  deny calls that the identity policy allows. A denied call is not
  proof the permission is absent from the policy.
- GovCloud (`us-gov-*`) and China (`cn-*`) partitions use different
  endpoints and ARNs (`arn:aws-us-gov:`, `arn:aws-cn:`). Set
  `--region` explicitly and adjust ARN parsing.
- `RequestLimitExceeded` throttling: slow down, add `sleep 1`
  between calls, and use `--query` to shrink responses.
- `aws s3 ls` shows only buckets your principal can list. Buckets can
  exist that are invisible here but reachable by direct name; combine
  with the unauthenticated checks in section 7.

## Escalation

- Listing is denied everywhere: switch to targeted `get-*` calls on
  names you learn from error messages, tags, or the console URLs in
  scope notes.
- Use the Resource Groups Tagging API as a cross-service inventory
  when per-service list calls fail: `aws resourcegroupstaggingapi
  get-resources --query 'ResourceTagMappingList[].ResourceARN'`.
- Test what the principal can actually DO with
  `aws iam simulate-principal-policy --policy-source-arn <ARN>
  --action-names s3:GetObject ec2:RunInstances` for the actions you
  care about.
- Enumerate assumable roles: list roles, read each trust policy with
  `iam:GetRole`, and try `sts:AssumeRole` only on roles whose trust
  policy names your principal.
- On EC2 with IMDSv1 only (no token endpoint), the metadata calls in
  section 1 still work without the token header; on IMDSv2-only
  instances the token call is mandatory.
- Credentials from `~/.aws/credentials` may be stale: check
  `aws sts get-caller-identity` first, and re-run `aws sso login`
  when the SSO token expires.

## Detection and defender view

Defenders see AWS enumeration in CloudTrail: every `ListUsers`,
`DescribeInstances`, `GetBucketPolicy`, and `ListSecrets` call is
logged with the caller ARN, source IP, and user agent. GuardDuty
raises `Recon:IAMUser/NetworkPermissions`,
`Recon:IAMUser/ResourcePermissions`, and
`Recon:IAMUser/UserPermissions` findings when one principal performs
unusual volumes of read-only discovery calls. Athena or CloudTrail
Lake queries group these by `userIdentity.arn` to spot the survey.
The durable defenses are least-privilege IAM (no wildcard read
policies for human users), SCPs that deny sensitive reads from
unexpected networks, and alerts on IAM enumeration bursts from IPs
with no history. As the tester, keep call volume reasonable, stay
inside the agreed window, and never pull secret values or customer
data beyond what the scope allows.

## Key references

- MITRE ATT&CK T1580 (Cloud Infrastructure Discovery): the account
  survey itself.
- MITRE ATT&CK T1526 (Cloud Service Discovery): per-service
  enumeration.
- MITRE ATT&CK T1087.004 (Account Discovery: Cloud Account):
  listing users and roles.
- MITRE ATT&CK T1530 (Data from Cloud Storage): S3 inventory and
  reads.
- AWS CLI v2 command reference: https://docs.aws.amazon.com/cli/
- AWS IAM actions reference:
  https://docs.aws.amazon.com/service-authorization-reference/
- CloudTrail event reference:
  https://docs.aws.amazon.com/awscloudtrail/latest/userguide/
