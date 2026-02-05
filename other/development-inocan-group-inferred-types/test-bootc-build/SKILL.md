---
name: test-bootc-build
description: Run a bootc build test and report results. Builds a bootc container image, optionally creates a disk image, and downloads the artifact.
allowed-tools:
  - Bash
  - Read
  - Grep
---

# Bootc Build Test Workflow

Run a bootc build with the specified parameters, monitor until completion, and download the artifact.

## Parameters

`$ARGUMENTS` contains the build name (required)

## Required Environment Variables

Before running, ensure these are set:
- `BOOTC_REGISTRY` - Base registry URL (e.g., `quay.io/myorg/myimage`)
- `REGISTRY_USERNAME` - Registry username (or read from `registry-user` file)
- `REGISTRY_PASSWORD` - Registry password (or read from `registry-pass` file)

## Execution Steps

### 1. Validate Environment

```bash
# Check required environment
if [ -z "$BOOTC_REGISTRY" ]; then
  echo "ERROR: BOOTC_REGISTRY environment variable not set"
  echo "Example: export BOOTC_REGISTRY=quay.io/myorg/myimage"
  exit 1
fi
```

### 2. Infer CAIB_SERVER from OpenShift Route

```bash
CAIB_SERVER="https://$(oc get route ado-build-api -n automotive-dev-operator-system -o jsonpath='{.spec.host}')"
echo "Using CAIB_SERVER: $CAIB_SERVER"
```

### 3. Get Authentication Token

```bash
TOKEN=$(oc whoami -t)
```

### 4. Get Registry Credentials

```bash
# Try environment variables first, fall back to files
REGISTRY_USERNAME="${REGISTRY_USERNAME:-$(cat registry-user 2>/dev/null)}"
REGISTRY_PASSWORD="${REGISTRY_PASSWORD:-$(cat registry-pass 2>/dev/null)}"
```

### 5. Submit Build with Download

```bash
BUILD_NAME="$ARGUMENTS"
PUSH_IMAGE="${BOOTC_REGISTRY}:latest"
DISK_IMAGE="${BOOTC_REGISTRY}:latest-disk"
OUTPUT_FILE="./output/${BUILD_NAME}.qcow2"

bin/caib build-bootc simple.aib.yml \
  --server "$CAIB_SERVER" \
  --token "$TOKEN" \
  --name "$BUILD_NAME" \
  --arch arm64 \
  --target qemu \
  --push "$PUSH_IMAGE" \
  --build-disk-image \
  --format qcow2 \
  --export-oci "$DISK_IMAGE" \
  --download "$OUTPUT_FILE" \
  --follow
```

### 6. Monitor Build (if not using --follow)

```bash
# Check build status
oc get imagebuild -n automotive-dev-operator-system $BUILD_NAME -o jsonpath='{.status.phase}'
```

### 7. On Failure - Debug

```bash
# Get PipelineRun name from ImageBuild status
PIPELINE_RUN=$(oc get imagebuild -n automotive-dev-operator-system $BUILD_NAME -o jsonpath='{.status.pipelineRunName}')

# Get pod name using correct PipelineRun label
POD=$(oc get pods -n automotive-dev-operator-system -l tekton.dev/pipelineRun=${PIPELINE_RUN} -o jsonpath='{.items[0].metadata.name}')

# Get build logs
oc logs -n automotive-dev-operator-system $POD -c step-build-image --tail=200

# Check for common issues
oc logs -n automotive-dev-operator-system $POD -c step-build-image | grep -i "builder\|cluster registry\|Pulling\|error\|failed"
```

### 8. Verify Download

```bash
# Check if artifact was downloaded
if [ -f "$OUTPUT_FILE" ]; then
  echo "SUCCESS: Artifact downloaded to $OUTPUT_FILE"
  ls -lh "$OUTPUT_FILE"
else
  echo "WARNING: Artifact not found at $OUTPUT_FILE"
fi
```

### 9. Report Results

Provide a summary with:
- Build status (success/failure)
- Download location and file size
- If failed: the specific error and relevant log snippets
- Suggestions for fixes based on the error type

## Common Error Patterns

- "Builder image not found" - prepare-builder task failed or result not passed
- "containers-storage: invalid reference" - skopeo copy using wrong format
- "setfiles: Operation not supported" - SELinux context issues in osbuild
- "unauthorized" - Token or registry auth issues
- "BOOTC_REGISTRY not set" - Environment variable missing

## Alternative: Download Only (for completed builds)

```bash
bin/caib download \
  --server "$CAIB_SERVER" \
  --token "$TOKEN" \
  --name "$BUILD_NAME" \
  --output-dir ./output
```
