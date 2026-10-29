---
name: gcp-enumeration
description: Use when enumerating a Google Cloud project, folder, or
  organization during an authorized cloud assessment, bug bounty
  engagement, or lab exercise. Covers authentication context, project
  and organization hierarchy, IAM policy bindings, service accounts and
  keys, Compute Engine instances, Cloud Storage buckets, Cloud
  Functions, and Cloud Asset Inventory search with gcloud 500.0.0 and
  Python 3.12. Use when you hold GCP credentials for a test project and
  need to map what the principal can reach, or when the scope permits
  unauthenticated checks of public buckets.
version: 1.0.0
domain: cloud
lifecycle: stable
last_verified: "2026-10-23"
requires: []
extends: []
relates: [cloud-security-basics, recon-passive]
tools:
  - name: gcloud
    version: 500.0.0
  - name: Python
    version: "3.12"
---

GCP enumeration maps what an identity can see and touch across the
resource hierarchy: organization, folders, projects, and the services
inside them. This skill covers the authorized operator workflow with
the gcloud CLI: authentication context, hierarchy discovery, IAM
policy bindings, service accounts, compute, storage, serverless, and
Cloud Asset Inventory, plus safe unauthenticated checks of public
buckets. Use it against your own projects, in-scope bug bounty
targets, and lab environments only. Never enumerate projects you do
not have written permission to test.

## Quick Workflow

1. Confirm authentication context: `gcloud auth list`, active
   account, and credential type (user vs service account).
2. Discover the resource hierarchy: organizations, folders, and
   projects the principal can see.
3. Set the working project explicitly and verify it.
4. Read IAM policy bindings at project level, then folder and
   organization level if readable.
5. Enumerate service accounts and their keys.
6. Survey Compute Engine: instances, disks, snapshots, firewall
   rules, and external IPs.
7. Survey Cloud Storage: buckets, IAM bindings, and public access
   settings.
8. Survey serverless and data: Cloud Functions, Cloud Run services,
   BigQuery datasets, Pub/Sub topics.
9. Use Cloud Asset Inventory search as a cross-service inventory
   when per-service lists fail.
10. Run safe unauthenticated checks of in-scope public buckets.
11. Save every command and its raw output for the report.

## 1. Authentication context

```bash
# Active accounts and which one is selected
gcloud auth list

# Current project, account, and region/zone defaults
gcloud config list --format='yaml(core)'

# Identity behind the credential: user email or service account
gcloud auth describe $(gcloud config get-value account 2>/dev/null) \
  2>/dev/null | head -20

# Work explicitly: set the project, never rely on defaults
gcloud config set project <PROJECT-ID>
gcloud projects describe <PROJECT-ID> \
  --format='yaml(projectId,name,projectNumber,parent)'
```

On a GCE VM or in Cloud Shell, check the attached service account and
its access scopes, which bound what the token can do:

```bash
# From inside the VM only
curl -s -H "Metadata-Flavor: Google" \
  http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/email
curl -s -H "Metadata-Flavor: Google" \
  http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/scopes
```

## 2. Resource hierarchy discovery

```bash
# Organizations visible to this principal
gcloud organizations list --format='table(name,displayName)'

# Folders under the organization
gcloud resource-manager folders list --organization=<ORG-ID> \
  --format='table(name,displayName)'

# Projects visible to this principal (all parents)
gcloud projects list --format='table(projectId,name,parent.id)' | head -40
```

## 3. IAM policy enumeration

IAM bindings show WHO has WHAT on WHICH resource. Read project
level first, then move up the hierarchy.

```bash
# Project IAM policy: members, roles, conditions
gcloud projects get-iam-policy <PROJECT-ID> \
  --format='yaml(bindings)'

# Filter for the interesting high-privilege roles
gcloud projects get-iam-policy <PROJECT-ID> \
  --flatten='bindings[].members' \
  --filter='bindings.role:roles/owner OR bindings.role:roles/editor OR bindings.role:iam.serviceAccountTokenCreator' \
  --format='table(bindings.role,bindings.members)'

# Testable permissions for the current principal on the project
gcloud projects get-iam-policy <PROJECT-ID> --format=json > /tmp/pol.json
```

High-value roles to flag: `roles/owner`, `roles/editor`,
`roles/iam.serviceAccountUser`, `roles/iam.serviceAccountTokenCreator`,
`roles/cloudfunctions.developer`, and any custom role with broad
permissions. Check what your own principal can do:

```bash
# Which permissions does the current identity hold on the project
gcloud iam list-testable-permissions \
  "//cloudresourcemanager.googleapis.com/projects/<PROJECT-NUMBER>" \
  --format='value(name)' | grep -E 'iam|compute.instances|storage' | head -30
```

## 4. Service account enumeration

Service accounts are the non-human identities and the most common
privilege escalation path in GCP.

```bash
# Service accounts in the project
gcloud iam service-accounts list \
  --format='table(email,displayName,disabled)'

# Keys on each service account (user-managed keys are the risk)
for sa in $(gcloud iam service-accounts list --format='value(email)'); do
  echo "=== $sa ==="
  gcloud iam service-accounts keys list --iam-account="$sa" \
    --format='table(name.basename(),keyType,validAfterTime)'
done

# Default compute and App Engine service accounts (often over-privileged)
gcloud iam service-accounts list \
  --filter='email:compute@developer.gserviceaccount.com OR email:appspot.gserviceaccount.com' \
  --format='table(email)'
```

Downloading a service account KEY is credential theft: only do it
when the scope explicitly allows it, and handle the file as a live
credential.

## 5. Compute Engine enumeration

```bash
# Instances across all zones: name, zone, machine type, status, IPs
gcloud compute instances list \
  --format='table(name,zone.basename(),machineType.basename(),status,networkInterfaces[0].accessConfigs[0].natIP:label=EXTERNAL_IP)'

# Disks, snapshots, and images
gcloud compute disks list --format='table(name,zone.basename(),sizeGb)'
gcloud compute snapshots list --format='table(name,diskSizeGb,sourceDisk)'
gcloud compute images list --no-standard-images \
  --format='table(name,family)'

# Firewall rules: open ingress to the world is the finding
gcloud compute firewall-rules list \
  --format='table(name,direction,allowed[].ports,sourceRanges)' | head -30

# Instance metadata of interest (service account, startup scripts)
gcloud compute instances describe <INSTANCE> --zone=<ZONE> \
  --format='yaml(serviceAccounts,metadata.items)'
```

## 6. Cloud Storage enumeration

```bash
# Buckets in the project
gcloud storage ls --project=<PROJECT-ID>

# Per-bucket IAM bindings and public access prevention
gcloud storage buckets describe gs://<BUCKET> \
  --format='yaml(name,iamConfiguration,publicAccessPrevention,versioning)'

# IAM policy on one bucket (who can read or write)
gcloud storage buckets get-iam-policy gs://<BUCKET>

# Uniform vs fine-grained access (fine-grained allows per-object ACLs)
gcloud storage buckets describe gs://<BUCKET> \
  --format='value(iamConfiguration.uniformBucketLevelAccess.enabled)'

# Top-level objects (read-only listing)
gcloud storage ls gs://<BUCKET>/ | head -20
```

## 7. Serverless and data services

```bash
# Cloud Functions (1st and 2nd gen)
gcloud functions list --format='table(name,entryPoint,runtime,httpsTrigger.url)' 2>/dev/null
gcloud functions list --gen2 --format='table(name,serviceConfig.uri)' 2>/dev/null

# Cloud Run services (often fronted by public HTTPS)
gcloud run services list --platform=managed \
  --format='table(metadata.name,status.url)'

# BigQuery datasets and Pub/Sub topics (names only)
bq ls --project_id=<PROJECT-ID> 2>/dev/null | head -20
gcloud pubsub topics list --format='value(name)' | head -20
```

## 8. Cloud Asset Inventory search

When per-service list calls fail, Asset Inventory gives a
cross-service view from one API.

```bash
# Every asset the principal can see in the project
gcloud asset search-all-resources --scope=projects/<PROJECT-NUMBER> \
  --format='table(assetType.basename(),name.basename())' | head -40

# Find all IAM bindings mentioning a user across the scope
gcloud asset search-all-iam-policies --scope=projects/<PROJECT-NUMBER> \
  --query="policy: <USER-EMAIL>" \
  --format='table(resource.basename(),policy.bindings[].role)' | head -20
```

## 9. Unauthenticated checks

```bash
# Public bucket listing without credentials
gcloud storage ls gs://<BUCKET> --no-auth 2>&1 | head -5

# Direct XML API check (works for public buckets)
curl -s "https://storage.googleapis.com/storage/v1/b/<BUCKET>" \
  | head -c 400
```

Only test buckets inside your scope, and stay read-only.

## Edge cases

- `PERMISSION_DENIED` on `projects list`: the principal may see no
  projects but still hold IAM bindings on specific resources. Pivot
  to asset search or per-resource `get-iam-policy` calls.
- Organization policy constraints (for example
  `iam.disableServiceAccountKeyCreation`) change what escalation
  paths exist; list them with `gcloud resource-manager org-policies
  list --project=<PROJECT-ID>`.
- Default service accounts carry the legacy Editor role in old
  projects: always check `get-iam-policy` rather than assuming
  least privilege.
- `gcloud` pagination truncates at 500 rows by default in some
  commands; add `--limit=1000` or `--page-size=500` for large
  tenants.
- Access scopes on GCE VMs can silently cap a service account that
  otherwise holds broad IAM roles. Compare the scopes from section
  1 with the IAM bindings before concluding what is possible.
- Multiple identities in `gcloud auth list`: commands run as the
  ACTIVE account only. Switch with `gcloud config set account
  <EMAIL>` and re-verify.

## Escalation

- Project list is empty: enumerate folders and the organization
  level, where different permissions may apply.
- IAM policy reads are denied at project level: try folder and
  organization `get-iam-policy`, or per-resource policies on
  buckets and service accounts.
- Look for service account impersonation chains:
  `iam.serviceAccounts.actAs` on one account plus deployment rights
  (Cloud Functions, Cloud Run, Compute) on another.
- Check for workload identity and GKE: `gcloud container clusters
  list` may reveal clusters where Kubernetes RBAC adds a second
  privilege layer (see the kubernetes-rbac skill).
- Cloud Build, Cloud Deploy, and CI service accounts frequently
  hold Editor: `gcloud builds list --limit=5` shows what runs as
  whom.
- When all listing fails, `list-testable-permissions` on the
  project resource still tells you exactly which actions the
  principal can perform.

## Detection and defender view

Defenders see GCP enumeration in Cloud Audit Logs (Admin Activity
and Data Access): `v1.compute.instances.list`,
`storage.buckets.list`, `iam.serviceAccounts.list`, and
`GetIamPolicy` calls, each stamped with the caller identity and
source IP. Forseti or Security Command Center flags anomalous API
usage and overly permissive bindings. Organization policy and
VPC Service Controls bound the blast radius. Durable defenses are
least-privilege custom roles instead of basic roles, no
user-managed service account keys (use impersonation with short
lifetimes), and alerts on `GetIamPolicy` bursts or key creation
events. As the tester, keep call volume reasonable, stay inside
the agreed window, and never download keys or read customer data
beyond what the scope allows.

## Key references

- MITRE ATT&CK T1580 (Cloud Infrastructure Discovery): the
  hierarchy survey itself.
- MITRE ATT&CK T1526 (Cloud Service Discovery): per-service
  enumeration.
- MITRE ATT&CK T1087.004 (Account Discovery: Cloud Account):
  listing users and service accounts.
- MITRE ATT&CK T1078.004 (Valid Accounts: Cloud Accounts):
  service account identity abuse.
- gcloud CLI reference: https://cloud.google.com/sdk/gcloud/reference
- GCP IAM documentation: https://cloud.google.com/iam/docs
- Cloud Asset Inventory:
  https://cloud.google.com/asset-inventory/docs
