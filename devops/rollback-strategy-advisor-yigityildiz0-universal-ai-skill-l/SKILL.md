---
name: rollback-strategy-advisor
description: Plans and implements rollback strategies for production deployments including database migration rollbacks, feature flag rollbacks, and incident response.
---

# Rollback Strategy Advisor

Specialized skill for planning, implementing, and testing rollback strategies across the full deployment stack. This skill goes beyond simple "undo the last deploy" approaches to address the real complexity of production rollbacks: database schema changes that cannot be naively reversed, stateful services with in-flight requests, feature flags that gate partially-released functionality, and multi-service deployments where rolling back one service affects others. The output includes concrete rollback procedures, automation scripts, and runbook templates ready for incident response use.

## When to Use This Skill

Use this skill for:

- Designing rollback strategies before a risky production deployment
- Planning database migration rollbacks that preserve data integrity
- Implementing feature flag-based rollbacks for gradual feature releases
- Building blue-green switchback procedures with traffic verification
- Creating incident response runbooks that include rollback decision trees
- Evaluating whether a deployment is safe to roll back or requires a roll-forward fix
- Automating rollback triggers based on error rates, latency, or health check failures
- Coordinating rollbacks across multiple dependent microservices
- Testing rollback procedures in staging environments before production releases

**Trigger phrases**: "rollback strategy", "rollback plan", "deployment rollback", "undo deployment", "revert release", "production incident rollback", "database rollback", "migration rollback", "feature flag rollback", "blue-green switchback", "rollback runbook", "rollback automation"

## What This Skill Does

This skill follows a structured methodology for rollback planning:

1. **Deployment Analysis**: Examines the deployment to identify all components being changed (application code, database schema, configuration, infrastructure) and their interdependencies.

2. **Rollback Classification**: Categorizes the rollback type needed based on the change characteristics: immediate (stateless code change), gradual (traffic shifting), data-aware (schema migration), or composite (multi-component).

3. **Risk Assessment**: Evaluates rollback risks including data loss potential, service disruption duration, downstream dependency impact, and whether the rollback itself could cause failures.

4. **Procedure Generation**: Produces step-by-step rollback procedures with exact commands, verification checks at each step, and decision points where human judgment is required.

5. **Automation Scripting**: Creates executable rollback scripts that can be triggered manually or automatically, with safety checks and confirmation prompts built in.

6. **Runbook Integration**: Formats the rollback procedure as a runbook suitable for on-call engineers, with clear escalation paths and communication templates.

## Instructions

### Step 1: Classify the Rollback Type

Before designing a rollback procedure, classify the deployment change to determine which rollback approach applies:

```
Rollback Type Assessment Matrix:

Change Type              | Rollback Approach     | Complexity | Data Risk
-------------------------|-----------------------|------------|----------
Stateless code change    | Immediate             | Low        | None
Configuration change     | Immediate             | Low        | None
Additive schema change   | Immediate (code only) | Low        | None
Destructive schema change| Data-aware            | High       | High
Multi-service change     | Coordinated           | High       | Medium
Feature flag release     | Flag toggle           | Low        | None
Infrastructure change    | Terraform/IaC revert  | Medium     | Low
Blue-green deployment    | Traffic switchback    | Low        | None
Canary deployment        | Weight reduction      | Low        | None
```

**Decision Tree Script** (`scripts/classify-rollback.sh`):

```bash
#!/usr/bin/env bash
set -euo pipefail

echo "=== Rollback Classification ==="
echo ""
echo "1. Does this deployment include database schema changes?"
read -r HAS_SCHEMA

if [ "$HAS_SCHEMA" = "yes" ]; then
  echo "2. Are the schema changes destructive (dropping columns, renaming tables, changing types)?"
  read -r IS_DESTRUCTIVE

  if [ "$IS_DESTRUCTIVE" = "yes" ]; then
    echo ""
    echo "CLASSIFICATION: Data-Aware Rollback"
    echo "RISK: HIGH - Requires data migration reversal"
    echo "APPROACH: Use expand-contract pattern; do NOT use immediate rollback"
    echo "SEE: Step 3 (Database Migration Rollbacks)"
    exit 0
  else
    echo ""
    echo "CLASSIFICATION: Immediate Rollback (code only)"
    echo "RISK: LOW - Additive schema changes are backward-compatible"
    echo "APPROACH: Roll back application code; leave schema changes in place"
    echo "NOTE: Clean up unused schema additions in a future migration"
    exit 0
  fi
fi

echo "2. Does this deployment span multiple services?"
read -r MULTI_SERVICE

if [ "$MULTI_SERVICE" = "yes" ]; then
  echo ""
  echo "CLASSIFICATION: Coordinated Rollback"
  echo "RISK: HIGH - Service interdependencies require ordered rollback"
  echo "APPROACH: Roll back in reverse deployment order; verify contracts at each step"
  echo "SEE: Step 6 (Multi-Service Rollback Coordination)"
  exit 0
fi

echo "2. Is this a feature flag release?"
read -r IS_FLAG

if [ "$IS_FLAG" = "yes" ]; then
  echo ""
  echo "CLASSIFICATION: Feature Flag Rollback"
  echo "RISK: LOW - No deployment needed; toggle flag"
  echo "APPROACH: Disable the feature flag; verify behavior"
  echo "SEE: Step 4 (Feature Flag Rollbacks)"
  exit 0
fi

echo ""
echo "CLASSIFICATION: Immediate Rollback"
echo "RISK: LOW - Stateless change can be reverted directly"
echo "APPROACH: kubectl rollout undo / redeploy previous version"
echo "SEE: Step 2 (Immediate Rollback)"
```

### Step 2: Implement Immediate Rollback

Immediate rollback applies to stateless code changes where the previous version can replace the current version without data concerns.

**Kubernetes Rollback Script** (`scripts/rollback-immediate.sh`):

```bash
#!/usr/bin/env bash
set -euo pipefail

NAMESPACE="${1:?Usage: rollback-immediate.sh <namespace> <deployment> [revision]}"
DEPLOYMENT="${2:?Missing deployment name}"
REVISION="${3:-}"
TIMEOUT="${4:-300s}"

echo "=== Immediate Rollback ==="
echo "Namespace:  $NAMESPACE"
echo "Deployment: $DEPLOYMENT"
echo "Revision:   ${REVISION:-previous}"
echo ""

# Step 1: Record current state for audit trail
CURRENT_IMAGE=$(kubectl get deployment "$DEPLOYMENT" -n "$NAMESPACE" \
  -o jsonpath='{.spec.template.spec.containers[0].image}')
CURRENT_REVISION=$(kubectl get deployment "$DEPLOYMENT" -n "$NAMESPACE" \
  -o jsonpath='{.metadata.annotations.deployment\.kubernetes\.io/revision}')

echo "Current image:    $CURRENT_IMAGE"
echo "Current revision: $CURRENT_REVISION"
echo ""

# Step 2: List available revisions
echo "Available rollback targets:"
kubectl rollout history "deployment/$DEPLOYMENT" -n "$NAMESPACE"
echo ""

# Step 3: Execute rollback
if [ -n "$REVISION" ]; then
  echo "Rolling back to revision $REVISION..."
  kubectl rollout undo "deployment/$DEPLOYMENT" -n "$NAMESPACE" --to-revision="$REVISION"
else
  echo "Rolling back to previous revision..."
  kubectl rollout undo "deployment/$DEPLOYMENT" -n "$NAMESPACE"
fi

# Step 4: Wait for rollout completion
echo "Waiting for rollout to complete (timeout: $TIMEOUT)..."
if ! kubectl rollout status "deployment/$DEPLOYMENT" -n "$NAMESPACE" --timeout="$TIMEOUT"; then
  echo "CRITICAL: Rollback itself failed to complete"
  echo "Manual intervention required"
  kubectl describe "deployment/$DEPLOYMENT" -n "$NAMESPACE"
  exit 2
fi

# Step 5: Verify rollback
NEW_IMAGE=$(kubectl get deployment "$DEPLOYMENT" -n "$NAMESPACE" \
  -o jsonpath='{.spec.template.spec.containers[0].image}')
READY=$(kubectl get deployment "$DEPLOYMENT" -n "$NAMESPACE" \
  -o jsonpath='{.status.readyReplicas}')
DESIRED=$(kubectl get deployment "$DEPLOYMENT" -n "$NAMESPACE" \
  -o jsonpath='{.spec.replicas}')

echo ""
echo "=== Rollback Complete ==="
echo "Previous image: $CURRENT_IMAGE"
echo "Restored image: $NEW_IMAGE"
echo "Ready pods:     $READY/$DESIRED"

if [ "$READY" != "$DESIRED" ]; then
  echo "WARNING: Not all pods are ready after rollback"
  exit 1
fi

echo "Rollback verified successfully"
```

**GitHub Actions Rollback Workflow** (`.github/workflows/rollback.yml`):

```yaml
name: Production Rollback

on:
  workflow_dispatch:
    inputs:
      environment:
        description: "Environment to roll back"
        required: true
        type: choice
        options:
          - production
          - staging
      revision:
        description: "Target revision (leave empty for previous)"
        required: false
        type: string
      reason:
        description: "Reason for rollback"
        required: true
        type: string

jobs:
  rollback:
    runs-on: ubuntu-latest
    environment:
      name: ${{ inputs.environment }}
    steps:
      - uses: actions/checkout@v4

      - name: Record rollback initiation
        run: |
          echo "## Rollback Record" >> "$GITHUB_STEP_SUMMARY"
          echo "- **Environment**: ${{ inputs.environment }}" >> "$GITHUB_STEP_SUMMARY"
          echo "- **Initiated by**: ${{ github.actor }}" >> "$GITHUB_STEP_SUMMARY"
          echo "- **Reason**: ${{ inputs.reason }}" >> "$GITHUB_STEP_SUMMARY"
          echo "- **Timestamp**: $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> "$GITHUB_STEP_SUMMARY"

      - name: Configure kubectl
        uses: azure/setup-kubectl@v4

      - name: Execute rollback
        run: |
          bash scripts/rollback-immediate.sh \
            "app-${{ inputs.environment }}" \
            "myapp" \
            "${{ inputs.revision }}"

      - name: Run smoke tests
        run: |
          bash scripts/verify-deployment.sh \
            "https://${{ inputs.environment == 'production' && 'app' || inputs.environment }}.example.com" \
            "app-${{ inputs.environment }}" \
            "myapp"

      - name: Notify team
        if: always()
        uses: slackapi/slack-github-action@v1
        with:
          payload: |
            {
              "text": "Rollback ${{ job.status }}: ${{ inputs.environment }}",
              "blocks": [
                {
                  "type": "section",
                  "text": {
                    "type": "mrkdwn",
                    "text": "*Rollback ${{ job.status }}*\n*Environment*: ${{ inputs.environment }}\n*Reason*: ${{ inputs.reason }}\n*Initiated by*: ${{ github.actor }}\n<${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}|View details>"
                  }
                }
              ]
            }
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_INCIDENTS_WEBHOOK }}
```

### Step 3: Implement Database Migration Rollbacks

Database rollbacks are the most complex rollback type because schema changes may be irreversible and data transformations may lose information.

**Expand-Contract Pattern**:

The safest approach for database changes is the expand-contract (also called parallel change) pattern. It separates schema migration into phases that are individually rollback-safe:

```
Phase 1 (Expand): Add new column/table alongside old one
  -> Rollback: Drop the new column/table (no data loss)

Phase 2 (Migrate): Copy/transform data from old to new
  -> Rollback: Truncate new column/table and revert to Phase 1

Phase 3 (Transition): Update application to use new schema
  -> Rollback: Redeploy previous application version

Phase 4 (Contract): Remove old column/table
  -> Rollback: NOT POSSIBLE without backup restoration
```

**Migration Rollback Script** (`scripts/rollback-migration.sh`):

```bash
#!/usr/bin/env bash
set -euo pipefail

DB_URL="${1:?Usage: rollback-migration.sh <db_url> <migration_tool> [target_version]}"
MIGRATION_TOOL="${2:?Missing migration tool (flyway|alembic|knex|prisma)}"
TARGET_VERSION="${3:-}"

echo "=== Database Migration Rollback ==="
echo "Tool: $MIGRATION_TOOL"
echo ""

# Step 1: Create backup before rollback
BACKUP_FILE="backup_pre_rollback_$(date +%Y%m%d_%H%M%S).sql"
echo "Creating backup: $BACKUP_FILE"
pg_dump "$DB_URL" > "$BACKUP_FILE"
echo "Backup created: $(du -h "$BACKUP_FILE" | cut -f1)"

# Step 2: Check current migration state
case "$MIGRATION_TOOL" in
  flyway)
    echo "Current migration state:"
    flyway -url="$DB_URL" info

    if [ -n "$TARGET_VERSION" ]; then
      echo "Rolling back to version: $TARGET_VERSION"
      flyway -url="$DB_URL" undo -target="$TARGET_VERSION"
    else
      echo "Rolling back last migration"
      flyway -url="$DB_URL" undo
    fi
    ;;

  alembic)
    echo "Current migration state:"
    alembic current

    if [ -n "$TARGET_VERSION" ]; then
      echo "Rolling back to revision: $TARGET_VERSION"
      alembic downgrade "$TARGET_VERSION"
    else
      echo "Rolling back one revision"
      alembic downgrade -1
    fi
    ;;

  knex)
    echo "Rolling back last migration batch"
    npx knex migrate:rollback
    echo "Current migration state:"
    npx knex migrate:status
    ;;

  prisma)
    echo "WARNING: Prisma Migrate does not support automatic rollback"
    echo "You must manually create a new migration that reverses the changes"
    echo "or restore from the backup created above"
    echo ""
    echo "To restore from backup:"
    echo "  psql $DB_URL < $BACKUP_FILE"
    exit 1
    ;;

  *)
    echo "Unsupported migration tool: $MIGRATION_TOOL"
    exit 1
    ;;
esac

# Step 3: Verify migration state
echo ""
echo "=== Post-Rollback Verification ==="
echo "Running schema validation..."

# Basic table existence check (customize per project)
psql "$DB_URL" -c "\dt" | head -20
echo ""
echo "Migration rollback complete. Backup available at: $BACKUP_FILE"
```

**Alembic Rollback-Safe Migration Example**:

```python
"""Add user_preferences table (rollback-safe, expand phase).

Revision ID: abc123
Revises: def456
Create Date: 2026-03-05
"""
from alembic import op
import sqlalchemy as sa

revision = "abc123"
down_revision = "def456"


def upgrade():
    # Expand phase: add new table alongside existing user settings
    op.create_table(
        "user_preferences",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("preferences", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now()),
    )
    op.create_index("ix_user_preferences_user_id", "user_preferences", ["user_id"], unique=True)

    # DO NOT drop the old user_settings column yet
    # That happens in the contract phase (separate migration)


def downgrade():
    # Safe rollback: just drop the new table
    op.drop_index("ix_user_preferences_user_id", table_name="user_preferences")
    op.drop_table("user_preferences")
```

### Step 4: Implement Feature Flag Rollbacks

Feature flags enable instant rollback without deployment by toggling the flag to disable the new behavior.

**Feature Flag Rollback Script** (`scripts/rollback-feature-flag.sh`):

```bash
#!/usr/bin/env bash
set -euo pipefail

FLAG_NAME="${1:?Usage: rollback-feature-flag.sh <flag_name> <provider>}"
PROVIDER="${2:?Missing provider (launchdarkly|unleash|custom)}"

echo "=== Feature Flag Rollback ==="
echo "Flag:     $FLAG_NAME"
echo "Provider: $PROVIDER"
echo ""

case "$PROVIDER" in
  launchdarkly)
    # Use LaunchDarkly API to disable the flag
    LD_API_KEY="${LD_API_KEY:?Missing LD_API_KEY environment variable}"
    LD_PROJECT="${LD_PROJECT:-default}"
    LD_ENVIRONMENT="${LD_ENVIRONMENT:-production}"

    echo "Disabling flag via LaunchDarkly API..."
    RESPONSE=$(curl -s -w "\n%{http_code}" \
      -X PATCH \
      -H "Authorization: ${LD_API_KEY}" \
      -H "Content-Type: application/json; domain-model=launchdarkly.semanticpatch" \
      -d "{
        \"environmentKey\": \"${LD_ENVIRONMENT}\",
        \"instructions\": [
          { \"kind\": \"turnFlagOff\" }
        ]
      }" \
      "https://app.launchdarkly.com/api/v2/flags/${LD_PROJECT}/${FLAG_NAME}")

    HTTP_CODE=$(echo "$RESPONSE" | tail -1)
    if [ "$HTTP_CODE" = "200" ]; then
      echo "Flag disabled successfully"
    else
      echo "Failed to disable flag (HTTP $HTTP_CODE)"
      echo "$RESPONSE" | head -n -1
      exit 1
    fi
    ;;

  unleash)
    UNLEASH_URL="${UNLEASH_URL:?Missing UNLEASH_URL}"
    UNLEASH_TOKEN="${UNLEASH_TOKEN:?Missing UNLEASH_TOKEN}"

    echo "Disabling flag via Unleash API..."
    curl -s -X POST \
      -H "Authorization: ${UNLEASH_TOKEN}" \
      "${UNLEASH_URL}/api/admin/projects/default/features/${FLAG_NAME}/environments/production/off"
    echo "Flag disabled"
    ;;

  custom)
    # For custom feature flag stores (Redis, database, config file)
    REDIS_URL="${REDIS_URL:-redis://localhost:6379}"
    echo "Disabling flag in Redis..."
    redis-cli -u "$REDIS_URL" SET "feature:${FLAG_NAME}" "false"
    redis-cli -u "$REDIS_URL" SET "feature:${FLAG_NAME}:disabled_at" "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
    redis-cli -u "$REDIS_URL" SET "feature:${FLAG_NAME}:disabled_reason" "rollback"
    echo "Flag disabled in Redis"
    ;;
esac

echo ""
echo "=== Verification ==="
echo "Wait 30 seconds for flag propagation, then verify:"
echo "  1. Check application behavior reflects the disabled state"
echo "  2. Monitor error rates for improvement"
echo "  3. Confirm no users are receiving the disabled feature"
```

**Application-Level Feature Flag Pattern (Python)**:

```python
"""Feature flag wrapper with rollback-safe defaults."""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import logging

logger = logging.getLogger(__name__)


@dataclass
class FlagState:
    enabled: bool
    rollback_reason: Optional[str] = None
    disabled_at: Optional[datetime] = None


class FeatureFlagManager:
    """Manages feature flags with safe defaults and rollback tracking."""

    def __init__(self, provider):
        self.provider = provider
        self._rollback_log = []

    def is_enabled(self, flag_name: str, default: bool = False) -> bool:
        """Check if a feature flag is enabled. Returns default on any error."""
        try:
            return self.provider.get_flag(flag_name)
        except Exception:
            logger.warning(
                "Failed to read flag %s, returning default: %s",
                flag_name,
                default,
            )
            return default

    def rollback_flag(self, flag_name: str, reason: str) -> FlagState:
        """Disable a feature flag and record the rollback."""
        try:
            self.provider.set_flag(flag_name, False)
            state = FlagState(
                enabled=False,
                rollback_reason=reason,
                disabled_at=datetime.utcnow(),
            )
            self._rollback_log.append({
                "flag": flag_name,
                "reason": reason,
                "timestamp": state.disabled_at.isoformat(),
            })
            logger.info("Rolled back flag %s: %s", flag_name, reason)
            return state
        except Exception:
            logger.exception("Failed to roll back flag %s", flag_name)
            raise
```

### Step 5: Implement Blue-Green Switchback

Blue-green switchback is the fastest rollback mechanism because the previous version is still running and receiving no traffic. The rollback simply switches the load balancer back.

**Blue-Green Switchback Script** (`scripts/rollback-blue-green.sh`):

```bash
#!/usr/bin/env bash
set -euo pipefail

NAMESPACE="${1:?Usage: rollback-blue-green.sh <namespace> <service_name>}"
SERVICE="${2:?Missing service name}"

echo "=== Blue-Green Switchback ==="

# Determine current active color
ACTIVE_COLOR=$(kubectl get svc "$SERVICE" -n "$NAMESPACE" \
  -o jsonpath='{.spec.selector.color}')

if [ "$ACTIVE_COLOR" = "blue" ]; then
  TARGET_COLOR="green"
elif [ "$ACTIVE_COLOR" = "green" ]; then
  TARGET_COLOR="blue"
else
  echo "ERROR: Cannot determine active color (found: '$ACTIVE_COLOR')"
  echo "Expected 'blue' or 'green' in service selector"
  exit 1
fi

echo "Current active: $ACTIVE_COLOR"
echo "Switching to:   $TARGET_COLOR"

# Verify target deployment is healthy before switching
TARGET_READY=$(kubectl get deployment "${SERVICE}-${TARGET_COLOR}" -n "$NAMESPACE" \
  -o jsonpath='{.status.readyReplicas}' 2>/dev/null || echo "0")
TARGET_DESIRED=$(kubectl get deployment "${SERVICE}-${TARGET_COLOR}" -n "$NAMESPACE" \
  -o jsonpath='{.spec.replicas}' 2>/dev/null || echo "0")

if [ "$TARGET_READY" != "$TARGET_DESIRED" ] || [ "$TARGET_READY" = "0" ]; then
  echo "WARNING: Target deployment ${SERVICE}-${TARGET_COLOR} has $TARGET_READY/$TARGET_DESIRED ready pods"
  echo "Scaling up target deployment..."
  kubectl scale deployment "${SERVICE}-${TARGET_COLOR}" -n "$NAMESPACE" \
    --replicas="$TARGET_DESIRED"
  kubectl rollout status deployment "${SERVICE}-${TARGET_COLOR}" -n "$NAMESPACE" \
    --timeout=300s
fi

# Switch traffic
echo "Switching traffic..."
kubectl patch svc "$SERVICE" -n "$NAMESPACE" \
  -p "{\"spec\":{\"selector\":{\"color\":\"${TARGET_COLOR}\"}}}"

# Verify switchback
sleep 5
NEW_ACTIVE=$(kubectl get svc "$SERVICE" -n "$NAMESPACE" \
  -o jsonpath='{.spec.selector.color}')

if [ "$NEW_ACTIVE" = "$TARGET_COLOR" ]; then
  echo ""
  echo "=== Switchback Complete ==="
  echo "Traffic now routed to: $TARGET_COLOR"
  echo "Previous version ($ACTIVE_COLOR) is still running but receiving no traffic"
  echo ""
  echo "Next steps:"
  echo "  1. Verify application behavior"
  echo "  2. Monitor error rates for 15 minutes"
  echo "  3. Once stable, optionally scale down $ACTIVE_COLOR deployment"
else
  echo "ERROR: Traffic switch verification failed"
  echo "Expected active: $TARGET_COLOR, Got: $NEW_ACTIVE"
  exit 1
fi
```

### Step 6: Multi-Service Rollback Coordination

When multiple services are deployed together, rollback must respect dependency order to avoid breaking API contracts.

**Dependency-Aware Rollback Script** (`scripts/rollback-coordinated.sh`):

```bash
#!/usr/bin/env bash
set -euo pipefail

NAMESPACE="${1:?Usage: rollback-coordinated.sh <namespace> <manifest_file>}"
MANIFEST="${2:?Missing rollback manifest file}"

echo "=== Coordinated Multi-Service Rollback ==="
echo "Manifest: $MANIFEST"
echo ""

# Manifest format (YAML):
# rollback_order:
#   - name: frontend
#     deployment: frontend
#     revision: 42
#   - name: api-gateway
#     deployment: api-gateway
#     revision: 38
#   - name: user-service
#     deployment: user-service
#     revision: 55

# Parse rollback order (reverse of deployment order)
SERVICES=$(yq eval '.rollback_order[].name' "$MANIFEST")
TOTAL=$(echo "$SERVICES" | wc -l)
CURRENT=0

for SERVICE in $SERVICES; do
  CURRENT=$((CURRENT + 1))
  DEPLOYMENT=$(yq eval ".rollback_order[] | select(.name == \"$SERVICE\") | .deployment" "$MANIFEST")
  REVISION=$(yq eval ".rollback_order[] | select(.name == \"$SERVICE\") | .revision" "$MANIFEST")

  echo "[$CURRENT/$TOTAL] Rolling back $SERVICE (deployment: $DEPLOYMENT, revision: $REVISION)"

  kubectl rollout undo "deployment/$DEPLOYMENT" -n "$NAMESPACE" --to-revision="$REVISION"
  kubectl rollout status "deployment/$DEPLOYMENT" -n "$NAMESPACE" --timeout=300s

  # Verify this service is healthy before proceeding to the next
  READY=$(kubectl get deployment "$DEPLOYMENT" -n "$NAMESPACE" \
    -o jsonpath='{.status.readyReplicas}')
  DESIRED=$(kubectl get deployment "$DEPLOYMENT" -n "$NAMESPACE" \
    -o jsonpath='{.spec.replicas}')

  if [ "$READY" != "$DESIRED" ]; then
    echo "CRITICAL: $SERVICE rollback unhealthy ($READY/$DESIRED ready)"
    echo "Halting coordinated rollback at step $CURRENT/$TOTAL"
    echo "Manual intervention required for remaining services"
    exit 1
  fi

  echo "$SERVICE rolled back successfully ($READY/$DESIRED ready)"
  echo ""
done

echo "=== Coordinated Rollback Complete ==="
echo "All $TOTAL services rolled back successfully"
```

**Rollback Manifest Example** (`rollback-manifest.yaml`):

```yaml
rollback_order:
  # Roll back in reverse dependency order:
  # frontend depends on api-gateway depends on user-service
  # So roll back frontend first, then api-gateway, then user-service
  - name: frontend
    deployment: frontend
    revision: 42
    health_endpoint: /health
  - name: api-gateway
    deployment: api-gateway
    revision: 38
    health_endpoint: /health
  - name: user-service
    deployment: user-service
    revision: 55
    health_endpoint: /health
```

### Step 7: Generate Incident Response Runbook

**Rollback Runbook Template** (`runbooks/rollback-runbook.md`):

```markdown
# Rollback Runbook: [Service Name]

## Quick Reference

| Item                | Value                              |
|---------------------|------------------------------------|
| Service             | myapp                              |
| Namespace           | app-production                     |
| Current Version     | v2.5.0 (abc1234)                   |
| Previous Version    | v2.4.3 (def5678)                   |
| Rollback Type       | Immediate / Data-Aware / Flag      |
| Estimated Duration  | 5 minutes                          |
| Last Tested         | 2026-02-28                         |

## Decision Tree

1. Is the issue caused by a feature behind a feature flag?
   - YES: Go to "Feature Flag Rollback" below
   - NO: Continue to step 2

2. Does the deployment include database schema changes?
   - YES: Go to "Database Migration Rollback" below
   - NO: Continue to step 3

3. Is this a blue-green deployment?
   - YES: Go to "Blue-Green Switchback" below
   - NO: Go to "Immediate Rollback" below

## Immediate Rollback

Run the following command:

    bash scripts/rollback-immediate.sh app-production myapp

Verification:
- [ ] Rollout status shows complete
- [ ] All pods are ready
- [ ] Health endpoint returns 200
- [ ] Error rate has decreased
- [ ] No new errors in application logs

## Feature Flag Rollback

Run the following command:

    bash scripts/rollback-feature-flag.sh new-checkout-flow launchdarkly

Verification:
- [ ] Flag shows as disabled in LaunchDarkly dashboard
- [ ] Application serves old behavior
- [ ] No errors related to the disabled feature

## Communication Template

Subject: [INCIDENT] Production rollback for [service name]

Body:
We have initiated a rollback of [service name] from [new version]
to [previous version] due to [brief description of issue].

Timeline:
- [HH:MM UTC] Issue detected: [description]
- [HH:MM UTC] Rollback initiated by [name]
- [HH:MM UTC] Rollback completed
- [HH:MM UTC] Verification passed

Impact: [description of user impact]
Status: [Monitoring / Resolved]
Next steps: [RCA scheduled / fix in progress]

## Escalation

| Level   | Contact          | When                                     |
|---------|------------------|------------------------------------------|
| L1      | On-call engineer | First responder, executes runbook         |
| L2      | Team lead        | Rollback fails or impact unclear          |
| L3      | VP Engineering   | Extended outage (>30 min) or data loss    |
```

## Best Practices

- **Test rollbacks regularly**: A rollback procedure that has never been executed is an untested assumption. Run rollback drills in staging at least monthly, and in production (during maintenance windows) quarterly.

- **Maintain rollback-safe migrations**: Use the expand-contract pattern for all database schema changes. Never drop a column or table in the same release that adds its replacement. Separate the "expand" and "contract" phases into different releases with at least one release cycle between them.

- **Keep the previous version running**: In blue-green deployments, do not scale down the inactive environment immediately after switching traffic. Keep it running for at least the duration of your monitoring window (typically 30-60 minutes) so switchback is instant.

- **Document rollback decisions**: When you decide not to roll back (choosing to roll forward instead), document the reasoning. This creates institutional knowledge about when each approach is appropriate.

- **Automate with manual gates**: The rollback script should be fully automated, but triggering it should require a conscious human decision (except for automated canary rollbacks). This prevents false positive rollbacks from transient issues.

- **Version your rollback scripts**: Rollback scripts are critical infrastructure. Store them in version control, review changes, and tag them alongside application releases.

- **Include rollback time estimates**: Every runbook should state how long the rollback takes. This helps incident commanders set expectations and decide whether to roll back or roll forward.

- **Separate rollback permissions**: The ability to trigger a production rollback should be granted to on-call engineers without requiring elevated access that takes time to obtain during an incident.

## Common Pitfalls

- **Assuming all changes are rollback-safe**: Not every deployment can be safely rolled back. Destructive schema migrations, data format changes, and external API contract changes may make rollback impossible or harmful. Assess rollback safety before deploying, not during an incident.

- **Rolling back without verifying the target version**: Before rolling back, confirm that the target version is actually the one you want. If the previous version also had issues, rolling back to it will not help.

- **Forgetting about in-flight requests**: A rollback that happens while requests are in flight can cause errors if the old and new versions handle requests differently. Use graceful shutdown (preStop hooks, drain periods) to let in-flight requests complete.

- **Ignoring cache invalidation**: If your application caches data in a format specific to the new version, rolling back the code without clearing caches can cause deserialization errors or incorrect behavior.

- **Rolling back one service in a multi-service deployment**: If services A and B were deployed together because B depends on a new API in A, rolling back only B while leaving A on the new version can break the dependency contract. Always consider the full dependency graph.

- **No backup before database rollback**: Never execute a database migration rollback without first taking a backup. Even "safe" rollback migrations can have unexpected consequences.

- **Confusing "rollback" with "roll forward"**: Sometimes the fastest recovery is to push a fix rather than revert. If the fix is a one-line change and the rollback involves complex data migration, rolling forward is often the better choice. The runbook should help the responder make this decision.

- **Skipping post-rollback verification**: A rollback is not complete until the system is verified healthy. Always run health checks, check error rates, and confirm the user-facing behavior matches expectations after rolling back.

- **Not communicating during rollback**: An unannounced rollback confuses other team members who may be investigating the same incident. Always announce the rollback decision and its outcome in the incident channel.

- **Deleting the failed version's artifacts**: Keep the failed version's container image, build artifacts, and logs. You will need them for the post-incident review to understand what went wrong.
