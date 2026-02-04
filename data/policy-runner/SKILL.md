---
name: policy-runner
description: Run policy-as-code checks (e.g., OPA/Conftest) based on the policy_plan. Use in Flow 2 and Flow 4.
allowed-tools: Bash, Read
---

# Policy Runner Skill

Run policy-as-code checks against plan artifacts, code, and configurations. This skill executes OPA/Conftest/Rego policies and produces structured evidence for compliance verification.

---

## Purpose

Policy-as-code transforms governance rules from documentation into executable checks. Instead of "the security team reviews PRs," you get "the policy runner verifies authentication requirements are met."

**What this skill does:**

- Execute policy checks defined in `policy_plan.md`
- Run OPA/Conftest against target files
- Produce structured pass/fail evidence
- Generate summaries for downstream agents (policy-analyst)

**What this skill does not do:**

- Grant waivers or exceptions
- Modify policy files
- Make compliance judgments (that's policy-analyst's job)
- Post to GitHub

---

## When to Use

| Flow                | Purpose                                               |
| ------------------- | ----------------------------------------------------- |
| **Flow 2 (Plan)**   | Validate contracts/ADR against architectural policies |
| **Flow 4 (Review)** | Re-check policies after implementation changes        |
| **Flow 5 (Gate)**   | Final policy verification before merge decision       |

The skill is typically invoked by:

- `policy-analyst` agent (for compliance mapping)
- Flow orchestrators (as a verification step)

---

## Policy-as-Code Concepts

### OPA (Open Policy Agent)

OPA is a general-purpose policy engine. Policies are written in Rego, a declarative query language.

```rego
# example: require auth on all endpoints
package api.security

default allow = false

allow {
    input.endpoint.auth_required == true
}

deny[msg] {
    not input.endpoint.auth_required
    msg := sprintf("Endpoint %v requires authentication", [input.endpoint.path])
}
```

### Conftest

Conftest is a tool for testing structured data (YAML, JSON, HCL) against OPA policies. It's commonly used for:

- Kubernetes manifests
- Terraform plans
- CI/CD configurations
- API contracts

```bash
# Run conftest against API contracts
conftest test api_contracts.yaml -p policies/api/
```

### Rego

The policy language for OPA. Key concepts:

- **Rules** define what's allowed/denied
- **Input** is the data being evaluated (e.g., your YAML files)
- **Packages** organize rules by domain
- **Deny** rules produce violations with messages

---

## Invocation

**Always invoke via the shim when available:**

```bash
bash .claude/scripts/demoswarm.sh policy <command> [options]
```

If the shim doesn't support policy commands, fall back to direct tool invocation:

```bash
conftest test <path> -p <policy-dir> --output json
opa eval --data <policy.rego> --input <target.json> "data.policy.deny"
```

---

## Operating Invariants

### Repo root only

- Assume working directory is repo root.
- All paths are repo-root-relative.

### Read-only execution

- Do not modify policy files or targets.
- Do not grant waivers.

### Evidence capture

- Save raw output to `policy_runner_output.log`.
- Write structured summary to `policy_runner_summary.md`.

### Null over guess

- If policies aren't configured: report "no policies wired"
- If tool errors: capture the error, don't fabricate results

---

## Configuration

### Policy Plan (`policy_plan.md`)

The `policy_plan.md` file defines which policies to run. Located at:

- `.runs/<run-id>/plan/policy_plan.md` (run-specific)
- `policies/policy_plan.md` (repo default)

Format:

```markdown
# Policy Plan

## Active Policies

| Policy             | Target             | Command                                    | Required |
| ------------------ | ------------------ | ------------------------------------------ | -------- |
| api-security       | api_contracts.yaml | conftest test {target} -p policies/api/    | yes      |
| data-retention     | schema.md          | opa eval -d policies/data/retention.rego   | no       |
| naming-conventions | \*.yaml            | conftest test {target} -p policies/naming/ | yes      |

## Policy Roots

- policies/
- .policies/
```

### Policy Directory Structure

```
policies/
  api/
    security.rego       # Auth requirements
    versioning.rego     # API versioning rules
  data/
    retention.rego      # Data retention rules
    pii.rego            # PII handling rules
  naming/
    conventions.rego    # Naming standards
  conftest.toml         # Conftest configuration
```

### Conftest Configuration (`conftest.toml`)

```toml
# policies/conftest.toml
policy = ["policies/"]
output = "json"
```

---

## Commands

### Run All Configured Policies

```bash
# If policy_plan.md exists, run all configured checks
bash .claude/scripts/demoswarm.sh policy run \
  --plan ".runs/feat-auth/plan/policy_plan.md" \
  --output ".runs/feat-auth/plan/policy_runner_output.log"
```

### Run Specific Policy

```bash
# Run a single named policy
conftest test .runs/feat-auth/plan/api_contracts.yaml \
  -p policies/api/ \
  --output json
```

### Check Policy Setup

```bash
# Verify policies are configured
bash .claude/scripts/demoswarm.sh policy check-setup
# stdout: CONFIGURED | NOT_CONFIGURED | PARTIAL
```

---

## Example Commands

### API Contract Validation

```bash
# Validate API contracts against security policies
conftest test .runs/feat-auth/plan/api_contracts.yaml \
  -p policies/api/security.rego \
  --output json

# Example output (pass):
# []

# Example output (fail):
# [
#   {
#     "filename": "api_contracts.yaml",
#     "failures": [
#       {"msg": "Endpoint /users requires authentication"}
#     ]
#   }
# ]
```

### Schema Validation

```bash
# Validate data models against retention policies
opa eval \
  --data policies/data/retention.rego \
  --input .runs/feat-auth/plan/schema.json \
  "data.retention.deny" \
  --format pretty

# Example output (pass):
# []

# Example output (fail):
# [
#   "Field 'email' in User model must have retention period defined"
# ]
```

### Kubernetes Manifest Check

```bash
# Validate k8s manifests (if applicable)
conftest test k8s/*.yaml \
  -p policies/k8s/ \
  --output json
```

### ADR Decision Validation

```bash
# Check ADR against architectural policies
conftest test .runs/feat-auth/plan/adr.md \
  -p policies/architecture/ \
  --parser yaml \
  --output json
```

---

## Behavior

1. **Read `policy_plan.md`** (if it exists) to discover which policies and paths to evaluate.

2. **For each configured policy entry:**
   - If an explicit command is listed (e.g., `conftest test <path>` or `opa eval ...`), run it.
   - Otherwise, if a policy file/rego path is provided, return a message that this policy is planned but not auto-executed.

3. **Capture output:**
   - Save raw runner output to `policy_runner_output.log`.
   - Write `policy_runner_summary.md` summarizing checks run, passed, failed, and planned-only policies.

4. **Do not modify** policy files or code.

---

## Output Artifacts

### `policy_runner_output.log`

Raw output from all policy executions:

```
=== Policy: api-security ===
Command: conftest test api_contracts.yaml -p policies/api/
Exit code: 0
Output:
[]

=== Policy: data-retention ===
Command: opa eval -d policies/data/retention.rego ...
Exit code: 1
Output:
["Field 'email' in User model must have retention period defined"]
```

### `policy_runner_summary.md`

```markdown
# Policy Runner Summary

## Execution Context

- Run ID: feat-auth
- Timestamp: 2025-12-12T10:30:00Z
- Policy Plan: .runs/feat-auth/plan/policy_plan.md

## Results

| Policy             | Target             | Status | Violations |
| ------------------ | ------------------ | ------ | ---------- |
| api-security       | api_contracts.yaml | PASS   | 0          |
| data-retention     | schema.md          | FAIL   | 1          |
| naming-conventions | \*.yaml            | PASS   | 0          |

## Violations Detail

### data-retention (FAIL)

- Target: schema.md
- Violation: Field 'email' in User model must have retention period defined
- Policy file: policies/data/retention.rego:L42

## Planned Only (Not Executed)

- pii-classification: No auto-execute command configured

## Summary

- Total policies: 4
- Executed: 3
- Passed: 2
- Failed: 1
- Planned only: 1
```

---

## Common Failure Modes

### No Policies Configured

**Symptom:** "No policy checks wired for this change"

**Resolution:**

1. Create `policies/` directory with Rego files
2. Create `policy_plan.md` with policy-to-target mappings
3. Or: acknowledge no policy-as-code is configured (valid state)

### Tool Not Installed

**Symptom:** `conftest: command not found` or `opa: command not found`

**Resolution:**

```bash
# Install conftest
brew install conftest  # macOS
# or download from: https://github.com/open-policy-agent/conftest/releases

# Install OPA
brew install opa  # macOS
# or download from: https://www.openpolicyagent.org/docs/latest/#running-opa
```

### Policy Parse Error

**Symptom:** Rego syntax errors in output

**Resolution:**

1. Check Rego syntax in the failing policy file
2. Run `opa check policies/*.rego` to validate syntax
3. Fix syntax errors before re-running

### Target File Not Found

**Symptom:** `error: file not found: api_contracts.yaml`

**Resolution:**

1. Verify the target file exists at the specified path
2. Check if `policy_plan.md` references the correct location
3. Ensure upstream agents (interface-designer) have run

### Policy Logic Error

**Symptom:** Unexpected failures or passes

**Resolution:**

1. Test policy in isolation: `opa eval --data policy.rego --input test.json "data.policy.deny"`
2. Add trace output: `opa eval ... --explain full`
3. Review Rego logic for edge cases

---

## Integration with policy-analyst

The `policy-analyst` agent uses policy-runner output to:

1. Map policy requirements to evidence
2. Classify violations by severity
3. Determine compliance status
4. Recommend routing (fix vs waive vs proceed)

**Flow:**

```
policy-runner (execute)
    |
    v
policy_runner_summary.md
    |
    v
policy-analyst (interpret)
    |
    v
policy_analysis.md (compliance register)
```

The skill executes; the agent interprets. Keep these concerns separate.

---

## Example Policy Rules

### Require Authentication

```rego
# policies/api/security.rego
package api.security

deny[msg] {
    endpoint := input.paths[path][method]
    not endpoint.security
    msg := sprintf("Endpoint %v %v must have security defined", [upper(method), path])
}
```

### Require Versioning

```rego
# policies/api/versioning.rego
package api.versioning

deny[msg] {
    not input.info.version
    msg := "API must have version defined in info block"
}

deny[msg] {
    path := input.paths[p]
    not startswith(p, "/v")
    msg := sprintf("Path %v must be versioned (e.g., /v1/...)", [p])
}
```

### PII Field Encryption

```rego
# policies/data/pii.rego
package data.pii

pii_fields := ["email", "phone", "ssn", "address"]

deny[msg] {
    field := input.models[model].fields[f]
    field.name == pii_fields[_]
    not field.encrypted
    msg := sprintf("PII field %v.%v must be encrypted", [model, field.name])
}
```

### Naming Conventions

```rego
# policies/naming/conventions.rego
package naming

deny[msg] {
    endpoint := input.paths[path]
    not regex.match(`^/[a-z][a-z0-9-]*(/[a-z][a-z0-9-]*)*$`, path)
    msg := sprintf("Path %v must use kebab-case", [path])
}
```

---

## Troubleshooting

### Debug Mode

```bash
# Run with verbose output
conftest test target.yaml -p policies/ --trace

# OPA with full explanation
opa eval --data policy.rego --input target.json "data.policy.deny" --explain full
```

### Test Policy in Isolation

```bash
# Create test input
echo '{"endpoint": {"path": "/users", "auth_required": false}}' > test_input.json

# Run policy against test input
opa eval --data policies/api/security.rego --input test_input.json "data.api.security.deny"
```

### Validate Rego Syntax

```bash
# Check all policies for syntax errors
opa check policies/**/*.rego

# Format Rego files
opa fmt -w policies/
```

---

## For Agent Authors

When using policy-runner in agents:

1. **Check for policy_plan.md first** — If missing, report "no policies configured" and proceed
2. **Capture all output** — Save to `policy_runner_output.log` for audit trail
3. **Don't fabricate results** — If tools fail, report the failure
4. **Let policy-analyst interpret** — The skill runs checks; the agent decides meaning
5. **Trust exit codes** — `0` = pass, non-zero = fail or error

Example pattern in agent code:

```bash
# Check if policies are configured
if [[ -f ".runs/${RUN_ID}/plan/policy_plan.md" ]]; then
  # Run policies
  conftest test .runs/${RUN_ID}/plan/api_contracts.yaml \
    -p policies/api/ \
    --output json > .runs/${RUN_ID}/plan/policy_runner_output.log 2>&1
  EXIT_CODE=$?

  if [[ $EXIT_CODE -eq 0 ]]; then
    echo "PASS"
  else
    echo "FAIL"
  fi
else
  echo "No policies configured for this run"
fi
```

---

## Installation

### Conftest

```bash
# macOS
brew install conftest

# Linux
wget https://github.com/open-policy-agent/conftest/releases/download/v0.48.0/conftest_0.48.0_Linux_x86_64.tar.gz
tar xzf conftest_0.48.0_Linux_x86_64.tar.gz
sudo mv conftest /usr/local/bin/

# Windows (scoop)
scoop install conftest
```

### OPA

```bash
# macOS
brew install opa

# Linux
curl -L -o opa https://openpolicyagent.org/downloads/latest/opa_linux_amd64
chmod +x opa
sudo mv opa /usr/local/bin/

# Windows (scoop)
scoop install opa
```

### Verify Installation

```bash
conftest --version
opa version
```

---

## See Also

- [policy-analyst.md](../../agents/policy-analyst.md) — Agent that interprets policy results
- [flow-2-plan.md](../../commands/flow-2-plan.md) — Flow where policies are first checked
- [verification-stack.md](../../../docs/explanation/verification-stack.md) — Where policy fits in verification
- [customize-pack.md](../../../docs/how-to/customize-pack.md) — How to configure policies for your repo
