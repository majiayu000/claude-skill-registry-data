---
name: test-traditional-build
description: Run a traditional AIB build test and report results. Builds a disk image using automotive-image-builder manifest and downloads the artifact.
allowed-tools:
  - Bash
  - Read
  - Grep
---

# Traditional Build Test Workflow

Run a traditional AIB build with the specified parameters, monitor until completion, and download the artifact.

## Parameters

`$ARGUMENTS` contains the build name (required)

## Required Environment Variables

Before running, ensure these are set:
- `PUSH_REGISTRY` - Registry URL to push the disk image (e.g., `quay.io/myorg/traditional-disk`)
- `REGISTRY_USERNAME` - Registry username (or read from `registry-user` file)
- `REGISTRY_PASSWORD` - Registry password (or read from `registry-pass` file)

## Execution Steps

### 1. Validate Environment

```bash
# Check required environment
if [ -z "$PUSH_REGISTRY" ]; then
  echo "ERROR: PUSH_REGISTRY environment variable not set"
  echo "Example: export PUSH_REGISTRY=quay.io/myorg/traditional-disk"
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
PUSH_IMAGE="${PUSH_REGISTRY}:latest"
OUTPUT_DIR="./output"

bin/caib build-dev simple.aib.yml \
  --server "$CAIB_SERVER" \
  --token "$TOKEN" \
  --name "$BUILD_NAME" \
  --arch arm64 \
  --target qemu \
  --mode image \
  --format qcow2 \
  --compress gzip \
  --push "$PUSH_IMAGE" \
  --registry-username "$REGISTRY_USERNAME" \
  --registry-password "$REGISTRY_PASSWORD" \
  --wait \
  --follow \
  -o "$OUTPUT_DIR"
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
oc logs -n automotive-dev-operator-system $POD -c step-build-image | grep -i "error\|failed\|unauthorized"
```

### 8. Verify Download

```bash
# Check if artifact was downloaded
OUTPUT_FILE=$(ls -1 ${OUTPUT_DIR}/*.qcow2* 2>/dev/null | head -1)
if [ -n "$OUTPUT_FILE" ] && [ -f "$OUTPUT_FILE" ]; then
  echo "SUCCESS: Artifact downloaded to $OUTPUT_FILE"
  ls -lh "$OUTPUT_FILE"
else
  echo "WARNING: Artifact not found in $OUTPUT_DIR"
  ls -la "$OUTPUT_DIR" 2>/dev/null || echo "Output directory does not exist"
fi
```

### 9. Report Results

Provide a summary with:
- Build status (success/failure)
- Download location and file size
- If failed: the specific error and relevant log snippets
- Whether logs streamed correctly (testing the pipelineRun label fix)
- Suggestions for fixes based on the error type

## Common Error Patterns

- "log stream not ready (HTTP 503)" - Pod label selector issue (should use `tekton.dev/pipelineRun`)
- "unauthorized" - Token or registry auth issues
- "PUSH_REGISTRY not set" - Environment variable missing
- "manifest not found" - AIB manifest file missing or invalid

## Alternative: Download Only (for completed builds)

```bash
bin/caib download \
  --server "$CAIB_SERVER" \
  --token "$TOKEN" \
  --name "$BUILD_NAME" \
  --output-dir ./output
```
