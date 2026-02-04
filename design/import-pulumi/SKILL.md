---
name: import-pulumi
description: Guide for importing existing Google Cloud resources into Pulumi state. Use when the user says "import resource to Pulumi", "add existing GCP resource", or needs to bring existing infrastructure under Pulumi management.
---

# import-pulumi

Import existing GCP resources into Pulumi state.

## Trigger Examples

- "Import resource to Pulumi"
- "Add existing GCP resource to state"
- "Bring this resource under Pulumi management"

## Prerequisites

- Pulumi project exists under `infra/`
- Target resources already exist in Google Cloud
- Pulumi backend (GCS) is configured
- Authentication to Google Cloud is available

## Execution Flow

### 1. Confirm Stack and Resource Type

Validate stack is one of: `shared`, `dev`, `prod`

### 2. Gather Resource Information

Prompt for GCP metadata:

- Project ID (e.g., `koborin-ai`)
- Region/location (`asia-northeast1`)
- Resource name/ID
- Any secondary identifiers

### 3. Resolve Pulumi Resource Name

Inspect `infra/src/stacks/*.ts` to find the Pulumi resource name.

### 4. Build Import Command

Use CLI-based import (NOT code-based import options):

```bash
cd infra
pulumi stack select <stack>
pulumi import <resource-type> <resource-name> "<import-id>" --yes
```

### 5. Provide Command to User

```text
Run the following commands:

cd infra
export PULUMI_BACKEND_URL=gs://${BUCKET_NAME}/pulumi
export PULUMI_CONFIG_PASSPHRASE=""
pulumi stack select <stack>

pulumi import <resource-type> <resource-name> "<import-id>" --yes

Let me know "success" or share the error output.
```

### 6. Wait for Result

- **Success**: Move to next resource or verify with `pulumi preview`
- **Failure**: Analyze error and adjust

### 7. Verify After Imports

```bash
pulumi stack ls
pulumi preview
# Expected: minimal changes
```

## Import ID Formats

| Resource Type | Import ID Format |
|---------------|------------------|
| `gcp:cloudrunv2/service:Service` | `projects/{project}/locations/{region}/services/{name}` |
| `gcp:cloudrunv2/serviceIamMember:ServiceIamMember` | `projects/{project}/locations/{region}/services/{name} {role} {member}` |
| `gcp:projects/service:Service` | `{project}/{api}` |
| `gcp:compute/globalAddress:GlobalAddress` | `projects/{project}/global/addresses/{name}` |
| `gcp:compute/backendService:BackendService` | `projects/{project}/global/backendServices/{name}` |
| `gcp:compute/regionNetworkEndpointGroup:RegionNetworkEndpointGroup` | `projects/{project}/regions/{region}/networkEndpointGroups/{name}` |
| `gcp:iam/workloadIdentityPool:WorkloadIdentityPool` | `projects/{project}/locations/global/workloadIdentityPools/{pool}` |
| `gcp:serviceaccount/account:Account` | `projects/{project}/serviceAccounts/{email}` |
| `gcp:projects/iAMMember:IAMMember` | `{project} {role} {member}` |
| `gcp:artifactregistry/repository:Repository` | `projects/{project}/locations/{region}/repositories/{name}` |

## Example: Import Cloud Run Service

**Command:**

```text
/import-pulumi dev cloudrunv2/service:Service
```

**Conversation:**

```text
Please share the existing resource information:
- Project ID:
- Location (region):
- Service name:
```

**User:**

```text
Project ID: koborin-ai
Location: asia-northeast1
Service name: koborin-ai-web-dev
```

**Agent:**

```text
Run the following commands:

cd infra
pulumi stack select dev

pulumi import gcp:cloudrunv2/service:Service web-dev \
  "projects/koborin-ai/locations/asia-northeast1/services/koborin-ai-web-dev" --yes

Let me know the result.
```

## Important Notes

1. **CLI Import Only**: Always use `pulumi import` command. Never use code-based `import` options in resource definitions.

2. **One at a Time**: Import resources one at a time, waiting for confirmation.

3. **Verify After**: Always run `pulumi preview` after importing to spot drift.

4. **CI/CD Only for Apply**: Import can be done locally, but `pulumi up` should only run via GitHub Actions.

## Error Handling

- **"Resource already exists in state"**: Check with `pulumi stack` and skip
- **"Resource not found"**: Verify identifiers and project/region
- **"Permission denied"**: Authenticate with sufficient IAM roles
