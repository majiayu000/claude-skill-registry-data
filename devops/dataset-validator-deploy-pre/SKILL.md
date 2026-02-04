---
name: dataset-validator-deploy-pre
description: |
  Example skill hook for validating datasets before infrastructure deployment.
  This demonstrates the skill hook interface and WorkflowContext/WorkflowResult pattern.
tools: Read, Bash
color: purple
tags: [validation, dataset, hook, example]
---

# Dataset Validator - Pre-Deployment (Example Skill Hook)

<CONTEXT>
You are a dataset validator that runs before infrastructure deployments as a hook handler.
You receive structured WorkflowContext about the deployment and validate that datasets are ready.
This is an EXAMPLE skill demonstrating the skill hook interface.
</CONTEXT>

<CRITICAL_RULES>
**IMPORTANT:** Skill Hook Interface
- Receive WorkflowContext via environment variables (set by invoke-skill-hook.sh)
- Return structured WorkflowResult as JSON to stdout
- Exit with code 0 for success, 1 for failure
- Always include success, messages, errors in result
- WorkflowResult must be valid JSON
</CRITICAL_RULES>

<INPUTS>
WorkflowContext (environment variables):
- FABER_CLOUD_ENV: Environment name (test, prod)
- FABER_CLOUD_OPERATION: Operation type (deploy, plan, destroy)
- FABER_CLOUD_HOOK_TYPE: Hook type (pre-deploy, post-deploy, etc.)
- FABER_CLOUD_PROJECT: Project name
- FABER_CLOUD_TERRAFORM_DIR: Terraform working directory

Optional: WorkflowContext JSON file passed as argument
</INPUTS>

<WORKFLOW>
1. Read WorkflowContext from environment variables
2. Log context for debugging
3. Validate datasets exist in expected locations
4. Check dataset schemas are valid
5. Verify data quality metrics meet thresholds
6. Generate validation report
7. Return WorkflowResult as JSON
</WORKFLOW>

<COMPLETION_CRITERIA>
✅ WorkflowContext read and parsed
✅ Dataset validation checks executed
✅ Validation results documented
✅ WorkflowResult JSON output to stdout
✅ Appropriate exit code returned
</COMPLETION_CRITERIA>

<OUTPUTS>
WorkflowResult (JSON to stdout):
```json
{
  "success": true/false,
  "messages": [
    "Dataset validation started",
    "Checked 5 dataset files",
    "All schemas valid",
    "Data quality metrics pass"
  ],
  "warnings": [
    "Dataset X approaching size limit"
  ],
  "errors": [
    "Dataset Y schema validation failed"
  ],
  "artifacts": {
    "validationReport": ".fractary/validation-report.json",
    "datasetsValidated": 5,
    "issuesFound": 0
  },
  "executionTime": 1234,
  "timestamp": "2025-11-07T12:00:00Z",
  "skillName": "dataset-validator-deploy-pre"
}
```
</OUTPUTS>

<ERROR_HANDLING>
If validation fails:
1. Set success: false
2. Populate errors array with specific issues
3. Include suggestions in messages
4. Exit with code 1
5. Skill hook execution will be blocked (if required: true)
</ERROR_HANDLING>

<EXAMPLE_EXECUTION>
```bash
# Environment variables set by faber-cloud hook executor
export FABER_CLOUD_ENV="test"
export FABER_CLOUD_OPERATION="deploy"
export FABER_CLOUD_HOOK_TYPE="pre-deploy"
export FABER_CLOUD_PROJECT="myproject"
export FABER_CLOUD_TERRAFORM_DIR="./infrastructure/terraform"

# Skill invoked by invoke-skill-hook.sh
/skill dataset-validator-deploy-pre

# Expected output (JSON):
{
  "success": true,
  "messages": ["Validation passed"],
  "warnings": [],
  "errors": [],
  "artifacts": {},
  "executionTime": 1234,
  "timestamp": "2025-11-07T12:00:00Z",
  "skillName": "dataset-validator-deploy-pre"
}
```
</EXAMPLE_EXECUTION>

## Implementation

**Step 1: Read WorkflowContext**

```bash
# Read context from environment variables
ENV=${FABER_CLOUD_ENV:-unknown}
OPERATION=${FABER_CLOUD_OPERATION:-unknown}
HOOK_TYPE=${FABER_CLOUD_HOOK_TYPE:-unknown}
PROJECT=${FABER_CLOUD_PROJECT:-unknown}

echo "🎯 STARTING: Dataset Validator (Pre-Deployment)"
echo "Environment: $ENV"
echo "Operation: $OPERATION"
echo "Hook Type: $HOOK_TYPE"
echo "Project: $PROJECT"
echo "───────────────────────────────────────"
```

**Step 2: Validate Datasets**

```bash
# Example validation logic
DATASET_DIR="./datasets"
ISSUES_FOUND=0
MESSAGES=()
WARNINGS=()
ERRORS=()

# Check datasets exist
if [ ! -d "$DATASET_DIR" ]; then
  ERRORS+=("Dataset directory not found: $DATASET_DIR")
  ISSUES_FOUND=$((ISSUES_FOUND + 1))
else
  MESSAGES+=("Dataset directory found: $DATASET_DIR")

  # Count datasets
  DATASET_COUNT=$(ls -1 "$DATASET_DIR"/*.csv 2>/dev/null | wc -l)
  MESSAGES+=("Found $DATASET_COUNT dataset files")

  # Validate each dataset
  for dataset in "$DATASET_DIR"/*.csv; do
    if [ -f "$dataset" ]; then
      # Check file size
      SIZE=$(stat -f%z "$dataset" 2>/dev/null || stat -c%s "$dataset" 2>/dev/null)
      if [ $SIZE -gt 10000000 ]; then
        WARNINGS+=("Dataset $(basename $dataset) is large: ${SIZE} bytes")
      fi

      # Validate CSV structure (example: check header row)
      if ! head -n1 "$dataset" | grep -q ","; then
        ERRORS+=("Dataset $(basename $dataset) appears invalid (no CSV header)")
        ISSUES_FOUND=$((ISSUES_FOUND + 1))
      fi
    fi
  done
fi
```

**Step 3: Generate WorkflowResult**

```bash
# Build result JSON
START_TIME=$(date +%s)
END_TIME=$(date +%s)
EXECUTION_TIME=$((END_TIME - START_TIME))
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

SUCCESS="true"
if [ $ISSUES_FOUND -gt 0 ]; then
  SUCCESS="false"
fi

# Convert arrays to JSON
MESSAGES_JSON=$(printf '%s\n' "${MESSAGES[@]}" | jq -R . | jq -s .)
WARNINGS_JSON=$(printf '%s\n' "${WARNINGS[@]}" | jq -R . | jq -s .)
ERRORS_JSON=$(printf '%s\n' "${ERRORS[@]}" | jq -R . | jq -s .)

# Output WorkflowResult as JSON
cat <<EOF
{
  "success": $SUCCESS,
  "messages": $MESSAGES_JSON,
  "warnings": $WARNINGS_JSON,
  "errors": $ERRORS_JSON,
  "artifacts": {
    "datasetsValidated": $DATASET_COUNT,
    "issuesFound": $ISSUES_FOUND
  },
  "executionTime": $EXECUTION_TIME,
  "timestamp": "$TIMESTAMP",
  "skillName": "dataset-validator-deploy-pre"
}
EOF

# Exit with appropriate code
if [ $ISSUES_FOUND -gt 0 ]; then
  exit 1
else
  exit 0
fi
```

## Testing

**Test independently:**
```bash
# Set up test environment
export FABER_CLOUD_ENV="test"
export FABER_CLOUD_OPERATION="deploy"
export FABER_CLOUD_HOOK_TYPE="pre-deploy"
export FABER_CLOUD_PROJECT="test-project"

# Create test datasets
mkdir -p ./datasets
echo "id,name,value" > ./datasets/test1.csv
echo "1,test,100" >> ./datasets/test1.csv

# Invoke skill
/skill dataset-validator-deploy-pre

# Expected: Success with messages about datasets found
```

**Test as hook:**
```json
{
  "hooks": {
    "pre-deploy": [
      {
        "type": "skill",
        "name": "dataset-validator-deploy-pre",
        "required": true,
        "failureMode": "stop",
        "timeout": 300
      }
    ]
  }
}
```

```bash
# Run hook executor
bash plugins/faber-cloud/skills/cloud-common/scripts/execute-hooks.sh pre-deploy test ./infrastructure/terraform

# Expected: Hook executes skill and reports results
```

## Installation

To use this skill hook in your project:

1. **Copy skill to project:**
   ```bash
   mkdir -p .claude/skills/dataset-validator-deploy-pre
   cp dataset-validator-deploy-pre-SKILL.md .claude/skills/dataset-validator-deploy-pre/SKILL.md
   ```

2. **Configure hook in faber-cloud.json:**
   ```json
   {
     "hooks": {
       "pre-deploy": [
         {
           "type": "skill",
           "name": "dataset-validator-deploy-pre",
           "required": true,
           "failureMode": "stop",
           "timeout": 300,
           "description": "Validate datasets before deployment"
         }
       ]
     }
   }
   ```

3. **Test the hook:**
   ```bash
   # Test skill independently
   /skill dataset-validator-deploy-pre

   # Test full deployment workflow
   /fractary-faber-cloud:deploy-apply --env=test
   ```

## Benefits

✅ **Reusable** - Share across projects
✅ **Testable** - Test independently with `/skill`
✅ **Discoverable** - Visible in `/help`
✅ **Structured** - Type-safe interfaces
✅ **Maintainable** - Clear documentation
✅ **Extensible** - Easy to customize

---

**See Also:**
- [Hook System Guide](../../guides/HOOKS.md)
- [Skill Hook Examples](./README.md)
- [SPEC-00034: Skill Hook Enhancement](../../../../specs/SPEC-00034-faber-cloud-skill-hooks.md)
