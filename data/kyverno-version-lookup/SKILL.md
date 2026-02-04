---
name: kyverno-version-lookup
description: This skill should be used when looking up Kyverno Helm chart versions, release dates, and corresponding app versions from Artifact Hub. Use for version planning, upgrade decisions, and release timeline analysis.
---

# Kyverno Version Lookup

Query Kyverno Helm chart release information from Artifact Hub.

## API Endpoint

```
https://artifacthub.io/api/v1/packages/helm/kyverno/kyverno
```

## Quick Lookup

```bash
# Get all stable releases (no RCs) with dates
~/.claude/skills/kyverno-version-lookup/scripts/kyverno-versions.sh

# Get JSON for programmatic use
~/.claude/skills/kyverno-version-lookup/scripts/kyverno-versions.sh --json

# Get latest N releases
~/.claude/skills/kyverno-version-lookup/scripts/kyverno-versions.sh --limit 10
```

## Manual API Query

```bash
# Fetch raw data
curl -s "https://artifacthub.io/api/v1/packages/helm/kyverno/kyverno" | jq '.available_versions'

# Filter stable releases only (no rc/beta/alpha)
curl -s "https://artifacthub.io/api/v1/packages/helm/kyverno/kyverno" | \
  jq '[.available_versions[] | select(.version | test("^[0-9]+\\.[0-9]+\\.[0-9]+$"))]'

# Pretty table with dates
curl -s "https://artifacthub.io/api/v1/packages/helm/kyverno/kyverno" | \
  jq -r '[.available_versions[] | select(.version | test("^[0-9]+\\.[0-9]+\\.[0-9]+$"))] |
         sort_by(.ts) | reverse |
         .[] | [.version, .app_version, (.ts | todate)] | @tsv' | \
  column -t -s $'\t'
```

## Response Format

Each version entry contains:

| Field | Description | Example |
|-------|-------------|---------|
| `version` | Helm chart version | `3.6.1` |
| `app_version` | Kyverno app version | `v1.16.1` |
| `ts` | Unix timestamp of release | `1764753174` |
| `contains_security_updates` | Security patch flag | `false` |
| `prerelease` | RC/beta/alpha flag | `false` |

## Version Mapping Reference

The Helm chart version and Kyverno app version follow different schemes:

- **Chart 3.x** maps to **Kyverno 1.1x** (e.g., Chart 3.6.1 = Kyverno v1.16.1)
- **Chart 2.x** maps to **Kyverno 1.x** (legacy)

## Use Cases

1. **Check latest stable version**
   ```bash
   curl -s "https://artifacthub.io/api/v1/packages/helm/kyverno/kyverno" | jq '.version, .app_version'
   ```

2. **Find release date for specific version**
   ```bash
   curl -s "https://artifacthub.io/api/v1/packages/helm/kyverno/kyverno" | \
     jq '.available_versions[] | select(.version == "3.6.0") | .ts | todate'
   ```

3. **List versions released in last 90 days**
   ```bash
   NINETY_DAYS_AGO=$(($(date +%s) - 7776000))
   curl -s "https://artifacthub.io/api/v1/packages/helm/kyverno/kyverno" | \
     jq --argjson cutoff "$NINETY_DAYS_AGO" \
       '[.available_versions[] | select(.ts > $cutoff and (.version | test("^[0-9]+\\.[0-9]+\\.[0-9]+$")))]'
   ```

## Self-Test

```bash
# Verify API is accessible and returns expected structure
curl -sf "https://artifacthub.io/api/v1/packages/helm/kyverno/kyverno" | \
  jq -e '.version and .app_version and .available_versions' > /dev/null && \
  echo "PASS: Kyverno version lookup working" || echo "FAIL: API check failed"
```
