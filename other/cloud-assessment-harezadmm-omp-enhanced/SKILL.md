---
name: cloud-assessment
description: Multi-cloud READ-ONLY security assessment methodology for AWS, Azure, and GCP using CIS benchmark-aligned checks
category: assessment
tags: [cloud, aws, azure, gcp, security-audit, cis-benchmark, iam, storage, network, encryption, logging, dns, tls]
tech_stack: [aws, azure, gcp, aws-cli, az-cli, gcloud-cli]
cwe_ids: [CWE-269, CWE-311, CWE-319, CWE-693, CWE-778]
version: "1.0"
---

# Cloud Security Assessment Methodology

Multi-cloud READ-ONLY security assessment using the `cloud_audit` tool. All checks use describe/list/get CLI calls via native TypeScript — no Python dependency, no SDK imports. Uses aws/az/gcloud CLIs. Aligned with CIS benchmarks for AWS, Azure, and GCP.

## Safety First

**ALWAYS run `verify_readonly` before any other audit program.** This confirms the current credentials have no dangerous write permissions. If the check returns FAIL, stop and request read-only credentials.

```
cloud_audit verify_readonly --provider all
```

## Assessment Phases

### Phase 1 — Credential Safety Verification

| Check | Command | Purpose |
|-------|---------|---------|
| Verify read-only | `cloud_audit verify_readonly --provider all` | Confirm no write permissions — MUST pass before proceeding |

### Phase 2 — Identity & Access Management

IAM is the most critical attack surface in cloud environments.

| Provider | Command | Key Checks |
|----------|---------|------------|
| AWS | `cloud_audit aws_iam_audit --json-output` | MFA status, wildcard policies, unused keys, cross-account trust, root access keys |
| Azure | `cloud_audit azure_iam_audit --json-output` | Dangerous role assignments (Owner/Contributor), subscription-level owners, wildcard custom roles |
| GCP | `cloud_audit gcp_iam_audit --json-output` | Primitive roles (Owner/Editor at project), SA key age >90d, domain-wide delegation |

**Intelligence integration:** After IAM audit, report findings via `add_intel` with type `infrastructure`:
```
add_intel type=infrastructure data="IAM audit: 3 users without MFA, 2 wildcard policies found"
```

### Phase 3 — Storage Security

Public storage buckets are the #1 cloud data breach vector.

| Provider | Command | Key Checks |
|----------|---------|------------|
| AWS | `cloud_audit aws_storage_audit --json-output` | S3 Block Public Access, ACLs, default encryption, versioning, access logging |
| Azure | `cloud_audit azure_storage_audit --json-output` | Blob public access, HTTPS-only, minimum TLS version, SAS policies |
| GCP | `cloud_audit gcp_storage_audit --json-output` | allUsers/allAuthenticatedUsers bindings, uniform bucket-level access, versioning |

### Phase 4 — Network Security

Open security groups and missing flow logs are common misconfigurations.

| Provider | Command | Key Checks |
|----------|---------|------------|
| AWS | `cloud_audit aws_network_audit --json-output` | SGs open to 0.0.0.0/0 on dangerous ports, IMDSv1, VPC flow logs |
| Azure | `cloud_audit azure_network_audit --json-output` | NSG Any/Any rules, public IPs on VMs, NSG flow logs |
| GCP | `cloud_audit gcp_network_audit --json-output` | Firewall rules open to 0.0.0.0/0, external IPs, legacy networks |

### Phase 5 — Encryption at Rest

Unencrypted storage is a compliance violation in most frameworks.

| Provider | Command | Key Checks |
|----------|---------|------------|
| AWS | `cloud_audit aws_encryption_audit --json-output` | EBS/RDS encryption, KMS key rotation, CMK vs AWS-managed |
| Azure | `cloud_audit azure_encryption_audit --json-output` | Disk encryption, storage CMK, Key Vault rotation |
| GCP | `cloud_audit gcp_encryption_audit --json-output` | Disk/SQL/GCS CMEK, KMS key rotation |

### Phase 6 — Logging & Monitoring

Missing audit logs mean attacks go undetected.

| Provider | Command | Key Checks |
|----------|---------|------------|
| AWS | `cloud_audit aws_logging_audit --json-output` | CloudTrail multi-region, GuardDuty, Config recorder |
| Azure | `cloud_audit azure_logging_audit --json-output` | Activity Log retention, Diagnostic settings, Defender status |
| GCP | `cloud_audit gcp_logging_audit --json-output` | Audit log config (DATA_READ/DATA_WRITE), log sinks, filters |

### Phase 7 — DNS & TLS

External-facing services need DNS security and valid TLS.

| Check | Command | Key Checks |
|-------|---------|------------|
| DNS | `cloud_audit dns_audit --domain TARGET` | Dangling CNAMEs (subdomain takeover), DNSSEC, CAA records |
| TLS | `cloud_audit tls_audit --target HOST:PORT` | Protocol version, certificate expiry, cipher strength, HSTS |

## Vulnerability Reporting

For each FAIL finding, report via `report_vulnerability`:

```
report_vulnerability
  title: "AWS IAM user without MFA: admin-user"
  severity: high
  evidence:
    requestSent: "cloud_audit aws_iam_audit --json-output"
    responseCode: 0
    responseSummary: "checkId AWS-IAM-001 FAIL — user admin-user has console access without MFA"
    reasoning: "CIS AWS 1.10 requires MFA for all IAM users with console access"
```

## Coverage Notes

Use `record_coverage_note` with `scope: "wide"` for account-level findings:
```
record_coverage_note
  scope: wide
  note: "AWS IAM audit complete — 5 findings across 12 users. No root access keys detected."
```

## Program Reference

| Program | Domain | Providers |
|---------|--------|-----------|
| verify_readonly | Safety | AWS, Azure, GCP |
| aws_iam_audit | IAM | AWS |
| azure_iam_audit | IAM | Azure |
| gcp_iam_audit | IAM | GCP |
| aws_storage_audit | Storage | AWS |
| azure_storage_audit | Storage | Azure |
| gcp_storage_audit | Storage | GCP |
| aws_network_audit | Network | AWS |
| azure_network_audit | Network | Azure |
| gcp_network_audit | Network | GCP |
| aws_encryption_audit | Encryption | AWS |
| azure_encryption_audit | Encryption | Azure |
| gcp_encryption_audit | Encryption | GCP |
| aws_logging_audit | Logging | AWS |
| azure_logging_audit | Logging | Azure |
| gcp_logging_audit | Logging | GCP |
| dns_audit | DNS | Cross-cloud |
| tls_audit | TLS | Cross-cloud |

---

---

## 5. CONFIRMING THE FINDING

| Step | Question | What it proves |
|---|---|---|
| 1 | Is the **account or subscription actually in scope**, per the signed rules of engagement? | authority to test at all |
| 2 | Did you establish the **credential's identity** from the provider, not from documentation? | the starting principal |
| 3 | Did you **read a real resource** within scope (an object, a secret, a row)? | a finding, not a permission listing |
| 4 | Did the **control identity fail** the same call? | escalation, not the baseline grant |
| 5 | Was the activity **logged** where the client can see it (CloudTrail, Activity Log, Audit Log)? | the report is detectable and scoped |
| 6 | Did you **revert every write**, and verify the reversion? | engagement integrity |
| 7 | Is the exposure **still live** at report time? | it has not already been fixed |

**A scoped, logged, reverted, and read-verified finding is the bar.** A cloud assessment that produces
permission listings and no reads has produced inventory, not findings.

---

## 6. EXECUTION PRIMITIVES

Assessment findings are proven by **a read within scope, a control that fails, and a reversion you can
show**. Every block below is provider-neutral in shape and ends at an artefact.

### 6.1 Pre-flight: scope, authority, and the audit trail

```bash
# confirm the identity you are supposed to be using, per the engagement
aws sts get-caller-identity 2>/dev/null || az account show --query '{sub:id,tenant:tenantId}' -o json 2>/dev/null || gcloud auth list --format='value(account)' 2>/dev/null
# confirm the accounts in scope, and record the ones you must NOT touch
cat /tmp/scope-accounts.txt 2>/dev/null
# confirm that your activity is being logged BEFORE you start, so the client can scope the report
aws cloudtrail lookup-events --lookup-attributes AttributeKey=EventName,AttributeValue=GetCallerIdentity --max-results 1 2>/dev/null | head -5
az monitor activity-log list --max-events 1 2>/dev/null | head -5
gcloud logging read 'protoPayload.methodName="google.cloud.audit.AuditLog"' --limit=1 2>/dev/null | head -5
```

**Confirm logging before the first probe.** An assessment whose actions are not in the client's logs
cannot be scoped afterwards, and that is a reportable process failure in itself.

### 6.2 Inventory, with the control

```bash
# the provider-neutral inventory: identity, then what that identity can see, then one read
aws organizations list-accounts 2>/dev/null | head -20
az account list --query '[].{name:name,id:id,state:state}' -o table 2>/dev/null | head -20
gcloud projects list --format='table(projectId,name)' 2>/dev/null | head -20
# the control: the calls that must fail, recorded as the baseline for every later claim
aws iam list-users 2>&1 | head -2; az keyvault list 2>&1 | head -2; gcloud secrets list 2>&1 | head -2
```

**Record the inventory and the controls together.** The value of an assessment is the delta between
what the identity should see and what it does see.

### 6.3 Exposure checks that produce a finding

```bash
# public storage, which is the highest-frequency cloud exposure in every provider
aws s3api get-bucket-policy-status --bucket BUCKET --query 'PolicyStatus.IsPublic' 2>/dev/null
aws s3api get-public-access-block --bucket BUCKET 2>/dev/null | head -20
az storage container show-permission --account-name ACCT --name CONTAINER --query publicAccess -o tsv 2>/dev/null
gcloud storage buckets describe gs://BUCKET --format='value(iamConfiguration.publicAccessPrevention)' 2>/dev/null
# and the identity that should never be public
aws iam get-policy-version --policy-arn ARN --version-id v1 --query 'PolicyVersion.Document.Statement[?Effect==`Allow`].Principal' 2>/dev/null
# the network surface, which is the other half
aws ec2 describe-security-groups --query 'SecurityGroups[?IpPermissions[?IpRanges[?CidrIp==`0.0.0.0/0`]]].[GroupId,GroupName]' --output table 2>/dev/null | head -20
```

**Each exposure check pairs a configuration read with a data read.** A bucket policy marked public is
the configuration; an object fetched over the public internet is the finding.

### 6.4 IAM over-permission, measured by use

```bash
# do not report the policy - report the USE of the permission
# 1) identify the over-broad binding
aws iam list-attached-user-policies --user-name USER 2>/dev/null | head -10
# 2) exercise it, minimally and in scope
aws s3 ls --profile TARGET 2>/dev/null | head -5
# 3) and pair it with the identity that should have been the only holder
aws iam get-policy-version --policy-arn ARN --version-id v1 --query 'PolicyVersion.Document.Statement[].Resource' 2>/dev/null
```

**The use is the finding.** "This role holds `s3:*`" is a configuration statement; "this role read
`prod-backups/`, which the client classified as restricted" is a finding with an owner.

### 6.5 Credential hygiene checks

```bash
# keys that have never been rotated, and keys with no last-used date
aws iam list-users --query 'Users[].UserName' --output text 2>/dev/null | tr '\t' '\n' | while read -r U; do
  aws iam list-access-keys --user-name "$U" --query "AccessKeyMetadata[?Status=='Active'].[UserName,AccessKeyId,CreateDate]" --output text 2>/dev/null
done | head -20
# keys older than the policy requires - the age is the finding, not the existence
python3 -c "
from datetime import datetime,timezone
print('flag keys with CreateDate older than the stated rotation policy, and state the age in days')"
# and the console users without MFA, which is the other hygiene finding
aws iam list-users --query 'Users[].UserName' --output text 2>/dev/null | tr '\t' '\n' | while read -r U; do
  M=$(aws iam list-mfa-devices --user-name "$U" --query 'length(MFADevices)' --output text 2>/dev/null)
  [ "$M" = "0" ] && echo "no MFA: $U"
done | head -20
```

**An unrotated key is a finding with an age attached.** Report the number of days, the policy it
violates, and the permissions the key holds - not merely that a key exists.

### 6.6 Cross-account and trust relationships

```bash
# who can enter this account, and who this account can enter
aws iam list-roles --query 'Roles[].RoleName' --output text 2>/dev/null | tr '\t' '\n' | while read -r R; do
  T=$(aws iam get-role --role-name "$R" --query 'Role.AssumeRolePolicyDocument.Statement[].Principal' 2>/dev/null)
  echo "$T" | grep -q 'arn:aws:iam::[0-9]' && echo "cross-account trust: $R -> $T"
done | head -20
# and the resource policies, which are the quieter path
aws s3api get-bucket-policy --bucket BUCKET 2>/dev/null | python3 -c "
import json,sys
d=json.load(sys.stdin)
for s in json.loads(d['Policy'])['Statement']:
    p=s.get('Principal'); 
    if p and p!='*': print('principal:',p,'actions:',s.get('Action'))" 2>/dev/null | head -10
```

**A cross-account trust with no external ID and no condition is the finding.** Name the trusting role,
the trusted principal, and the absence of the condition.

### 6.7 The evidence hygiene a cloud report requires

```bash
# 1) redact before you store - never keep a live secret in the report artefact
python3 -c "
import re
print('for every secret, record: the identifier, the read time, the permission used, and the fact it was read.')
print('never the value. the client can re-read it; the report should not carry it.')"
# 2) attach the provider's own evidence - the request ID ties your action to their log
aws cloudtrail lookup-events --lookup-attributes AttributeKey=EventName,AttributeValue=GetSecretValue \
  --max-results 3 --query 'Events[].CloudTrailEvent' --output text 2>/dev/null | head -c 400; echo
# 3) and record the reversion for every write you performed
echo "for each write: the creating call, the deleting call, and the verification call"
```

**Provider request IDs are the strongest evidence available.** They tie the tester's action to the
client's log, and they are the reason a cloud assessment can be scoped precisely.

### 6.8 A harness over the assessment phases

```bash
python3 - <<'PY'
import subprocess, shlex
def run(name, cmd, timeout=45):
    try:
        r = subprocess.run(shlex.split(cmd), capture_output=True, text=True, timeout=timeout)
        ok = r.returncode == 0
        out = (r.stdout + r.stderr).strip().replace("\n", " ")[:70]
    except Exception as e:
        ok, out = False, type(e).__name__
    print("  %-34s %s %s" % (name, "OK  " if ok else "FAIL", out))
    return ok

print("PHASE 1 - identity and logging")
run("identity", "aws sts get-caller-identity")
run("logging-visible", "aws cloudtrail lookup-events --max-results 1")
print()
print("PHASE 2 - controls (these should FAIL at the assessment identity)")
run("control-iam", "aws iam list-users")
run("control-kv", "aws secretsmanager list-secrets")
print()
print("PHASE 3 - scoped reads (these are the findings, one per service)")
run("buckets", "aws s3 ls")
run("instances", "aws ec2 describe-instances")
print()
print("PHASE 4 - reversion verification (run LAST, and only for writes you performed)")
print("  report the deleting call and a verification call for every write, or state that none were made")
PY
```

**Four phases in order: identity + logging, controls, reads, reversion.** An assessment report that
skips the controls or the reversion phase is not evidence-based.

---

## 7. EVIDENCE STANDARD

| Item | Why |
|---|---|
| The **account or subscription ID and its in-scope status** | authority and scope |
| The **identity used for the assessment**, from the provider | the credential under test |
| The **control call result** | the baseline every finding is measured against |
| The **provider request ID** for each significant action | ties the finding to the client's own log |
| Each **finding as a resource read**, not a permission listing | impact |
| The **dataclass or owner** of each affected resource | who acts on it |
| The **reversion proof** for every write | engagement integrity |
| Confirmation that **logging captured the activity** | the report is scoped and hunts are possible |
| Redaction of every **secret value**, referenced by identifier only | no unnecessary disclosure |
| The **stated boundaries** - resources deliberately not touched | the negative space is part of the report |

Report the **identity, the control, and the read**: "using the assessment identity
`arn:aws:iam::123456789012:user/pentest-readonly`, `sts get-caller-identity` confirmed the account, and
the control calls `iam list-users` and `secretsmanager list-secrets` both returned `AccessDenied`,
confirming the read-only baseline. `s3 ls` returned 14 buckets including `prod-customer-exports`; the
bucket's policy grants `Principal: "*"` with `s3:GetObject`, and an unauthenticated `curl` of a known
object returned a 200 with a CSV containing 2,000 customer records. CloudTrail recorded the read events
under request ID `...` and the request was logged in the client's trail", never "the account has public
buckets".

### False positives - do not report these

| Observation | Why it is not a finding |
|---|---|
| A permission listed but **not exercised** | the inventory, not a finding |
| A `Denied` response | the control working, and worth reporting as a positive control |
| A publicly-readable object that is **intended to be public** (a website asset) | verify the classification with the client |
| A key older than the policy **but with no permissions** | report the age with the actual reach |
| A cross-account trust that **requires an external ID and a condition** | that is the correct configuration |
| A `0.0.0.0/0` rule on a **port serving a public service** | verify the intended exposure |
| A finding in an account **outside the signed scope** | an engagement violation |
| A resource in a **sandbox or test account** the client excluded | in scope only if named |
| A secret value reproduced in full in the report | a disclosure |
| A finding the client has **already remediated** during the engagement | verify liveness before publishing |
| Permission listings without a **single read** | not an evidence-based assessment |

**Controls are findings too.** A control that correctly denied you is worth stating explicitly, because
it tells the client their baseline works.

---

## 8. REMEDIATION REFERENCE

1. **Give each identity the minimum permission it needs, at the narrowest scope, and re-run the unused-permission analysis quarterly** - the review is the control, not the initial grant.
2. **Require short-lived credentials via roles or workload identity, and eliminate long-lived access keys** - it removes the class of finding that cannot be revoked quickly.
3. **Enforce MFA on every console and privileged programmatic path, with conditional access** - it closes the simplest credential path in all three providers.
4. **Enforce public-access blocks at the account or organization level, and alert on any policy that grants a public principal** - the account-level block overrides the individual bucket.
5. **Log every control-plane action to a trail in a separate, restricted account with a locked retention policy** - the assessment's own evidence comes from this, and an attacker with account access must not be able to delete it.
6. **Alert on the escalation primitives** (`CreateAccessKey`, `AttachUserPolicy`, `SetIamPolicy`, `AssumeRole`, `role assignment create`) - each maps directly to a finding class in this document.
7. **Use an external ID and a condition on every cross-account trust, and review unused trusts** - the confused-deputy problem is entirely the missing condition.
8. **Rotate secrets centrally with a managed store, and alert on unexpected read patterns** - the read event is the detection.
9. **Define a resource classification, and test the public exposure of each class on a schedule** - the assessment is only as good as the classification it tests against.
10. **Restrict the deploy-time identities (CI roles, build service accounts) to the minimum, because they are code execution by design** - they are consistently the most over-permissioned identities in a cloud estate.
11. **Establish a logging-and-scoping practice for external assessments, and verify it before the first probe** - it is the difference between a report that can be scoped and one that cannot.

---

## 9. RELATED SIBLINGS - LOAD TOGETHER

- [aws-postexploit](../aws-postexploit/SKILL.md) - what follows a confirmed AWS finding
- [azure-postexploit](../azure-postexploit/SKILL.md) - the same for Azure
- [gcp-postexploit](../gcp-postexploit/SKILL.md) - the same for GCP
- [k8s-assessment](../k8s-assessment/SKILL.md) - the cluster exposure surface, which usually runs inside one of these accounts
- [security-reporting-and-documentation](../security-reporting-and-documentation/SKILL.md) - how the findings and their controls are written up
