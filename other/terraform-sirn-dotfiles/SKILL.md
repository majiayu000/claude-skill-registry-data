---
name: terraform
type: reference
description: Reference for Terraform CLI commands and workflows. ALWAYS read before running terraform commands to ensure correct syntax and follow the standard plan-then-confirm workflow.
---

## Terraform CLI Reference

Terraform is an infrastructure as code tool for building, changing, and versioning infrastructure.

### Best Practices

- **Standard Plan-Confirm-Apply Workflow**: Run `terraform plan`, present a summary of changes, and obtain explicit permission before executing `terraform apply`. Never apply changes without direct instruction.
- **Save plans to filter output**: Avoid re-running `terraform plan` to search or filter output. State verification is slow and remote state may drift. Instead, save the plan output to a temporary file and use tools like grep, head, or tail to inspect it:

  ```bash
  # ❌ Avoid: Running plan multiple times
  terraform plan | grep "aws_instance"
  terraform plan | head -20

  # ✅ Correct: Save once, then filter
  terraform plan > /tmp/tfplan.txt
  grep "aws_instance" /tmp/tfplan.txt
  head -20 /tmp/tfplan.txt
  ```

- **Restrict `-auto-approve`**: Only use `-auto-approve` if the user has given explicit permission to apply changes.
- **Limit `-target`**: Avoid targeted applies via `-target` as they can leave infrastructure in an inconsistent state; reserve them for emergencies.
- **Handle locking carefully**: Never force-unlock state unless you fully understand why it is locked.
- **Backup state**: Always backup the state file before running `state rm` or `state mv`.
- **Verify workspace**: Run `terraform workspace show` to check the current workspace before running any destructive operations.
- **Pin module versions**: Pin all module versions in production to prevent unexpected updates.
- **Lock providers**: Use `terraform providers lock` to maintain consistent provider versions.

### Standard Workflow (ALWAYS Follow This)

This is the standard, safe workflow for applying Terraform changes:

```bash
# Step 1: Initialize (if not already done)
terraform init

# Step 2: Create a plan and review output
terraform plan

# Step 3: Summarize changes to user and get explicit confirmation
# (Discuss: what will be created/modified/destroyed)

# Step 4: Apply (ONLY after user explicitly tells you to apply)
terraform apply

# Step 5: Confirm success with user
```

**Important Rules:**

1. Review `terraform plan` output before applying.
2. Summarize all proposed changes for the user.
3. Run `terraform apply` only after receiving explicit user confirmation.
4. Restrict `-auto-approve` to cases with pre-approved permissions.

### Core Workflow Commands

| Task | Command |
| --- | --- |
| Initialize directory | `terraform init` |
| Initialize with upgrade | `terraform init -upgrade` |
| Validate configuration | `terraform validate` |
| Create execution plan | `terraform plan` |
| Plan with variables | `terraform plan -var="key=value"` |
| Apply changes | `terraform apply` |
| Apply with auto-approve (USE WITH CAUTION) | `terraform apply -auto-approve` |
| Apply with target | `terraform apply -target=resource.address` |
| Destroy infrastructure | `terraform destroy` |
| Auto-approve destroy (USE WITH CAUTION) | `terraform destroy -auto-approve` |
| Refresh state | `terraform refresh` |

### State Management Commands

| Task | Command |
| --- | --- |
| List state resources | `terraform state list` |
| List with pattern | `terraform state list 'module.foo.*'` |
| Show resource details | `terraform state show resource.address` |
| Remove resource from state | `terraform state rm resource.address` |
| Move resource in state | `terraform state mv source.destination` |
| Pull raw state (JSON) | `terraform state pull > state.json` |
| Push raw state | `terraform state push state.json` |
| Replace provider | `terraform state replace-provider old.provider new.provider` |

### Resource Import and Tainting

| Task                      | Command                                         |
| ------------------------- | ----------------------------------------------- |
| Import existing resource  | `terraform import resource.address resource.id` |
| Taint resource (recreate) | `terraform taint resource.address`              |
| Untaint resource          | `terraform untaint resource.address`            |

### Workspace Commands

| Task                   | Command                                    |
| ---------------------- | ------------------------------------------ |
| Show current workspace | `terraform workspace show`                 |
| List workspaces        | `terraform workspace list`                 |
| Select workspace       | `terraform workspace select <name>`        |
| Create new workspace   | `terraform workspace new <name>`           |
| Delete workspace       | `terraform workspace delete <name>`        |
| Delete with resources  | `terraform workspace delete -force <name>` |

### Format and Validate

| Task               | Command                    |
| ------------------ | -------------------------- |
| Format all files   | `terraform fmt`            |
| Format recursive   | `terraform fmt -recursive` |
| Check formatting   | `terraform fmt -check`     |
| Show diff          | `terraform fmt -diff`      |
| Validate config    | `terraform validate`       |
| Validate with JSON | `terraform validate -json` |

### Output and Inspection

| Task                 | Command                         |
| -------------------- | ------------------------------- |
| Show all outputs     | `terraform output`              |
| Show specific output | `terraform output <name>`       |
| Raw output value     | `terraform output -raw <name>`  |
| JSON format          | `terraform output -json`        |
| Show state/plan      | `terraform show`                |
| Show JSON            | `terraform show -json`          |
| Interactive console  | `terraform console`             |
| Console with state   | `terraform console -state=path` |

### Module and Provider Commands

| Task                   | Command                            |
| ---------------------- | ---------------------------------- |
| Download modules       | `terraform get`                    |
| Update modules         | `terraform get -update`            |
| List providers         | `terraform providers`              |
| Lock provider versions | `terraform providers lock`         |
| Mirror providers       | `terraform providers mirror <dir>` |
| Show provider schema   | `terraform providers schema -json` |
| Dependency graph       | `terraform graph`                  |

### Authentication and Misc

| Task                   | Command                            |
| ---------------------- | ---------------------------------- |
| Terraform Cloud login  | `terraform login`                  |
| Terraform Cloud logout | `terraform logout`                 |
| Show version           | `terraform version`                |
| JSON version           | `terraform version -json`          |
| Force unlock state     | `terraform force-unlock <lock-id>` |
| Module metadata        | `terraform metadata`               |
| Run tests              | `terraform test`                   |

### Common Options

| Goal | Flag | Example |
| --- | --- | --- |
| Specify working dir | `-chdir=<dir>` | `terraform -chdir=./infra plan` |
| Disable colors | `-no-color` | `terraform plan -no-color` |
| Parallelism | `-parallelism=<n>` | `terraform apply -parallelism=10` |
| Var file | `-var-file=<file>` | `terraform plan -var-file=prod.tfvars` |
| Single var | `-var="key=value"` | `terraform apply -var="region=us-east-1"` |
| Backend config | `-backend-config=<key=value>` | Used with init |
| Lock state | `-lock=true` (default) | `terraform apply -lock=true` |
| Lock timeout | `-lock-timeout=<duration>` | `terraform apply -lock-timeout=5m` |
| JSON output | `-json` | `terraform show -json` |

### Common Workflows

#### Standard Safe Apply Workflow (ALWAYS Follow This)

Always use this workflow to apply changes safely:

```bash
# Step 1: Initialize
terraform init

# Step 2: Create a plan and review output
terraform plan

# Step 3: Summarize changes to user
# Discuss what will be created, modified, or destroyed

# Step 4: Apply ONLY after user explicitly tells you to apply
terraform apply
```

**Key Points:**

- Review `terraform plan` output before applying.
- Present a change summary to the user.
- Run `terraform apply` only with explicit user permission.
- Limit `-auto-approve` to pre-approved changes.

#### First-time Setup

```bash
terraform init
terraform validate
terraform plan
# Review output and discuss with user
terraform apply  # Only after user tells you to apply
```

#### Working with Workspaces

```bash
terraform workspace new production
terraform workspace select production
terraform plan -var-file=production.tfvars
# Review output and discuss with user
terraform apply  # Only after user tells you to apply
```

#### Safe State Modification

```bash
# Step 1: Backup state first
terraform state pull > backup-$(date +%Y%m%d).json

# Step 2: Preview changes with plan
terraform plan
# Review output and discuss with user

# Step 3: Make state changes (only after user confirms)
terraform state mv module.old module.new
terraform state rm deprecated.resource

# Step 4: Verify with plan
terraform plan  # Should show no changes if state ops were correct
```

#### Import Existing Resources

```bash
# Step 1: Find the resource ID in cloud provider
# Step 2: Import the resource
terraform import aws_instance.example i-1234567890abcdef0

# Step 3: Verify with plan (should show no changes)
terraform plan
```

#### Targeted Apply (Emergency Only - WITH CAUTION)

```bash
# Only use targeted apply for emergencies
# Step 1: Plan with target
terraform plan -target=aws_instance.bastion

# Step 2: Review output and discuss with user

# Step 3: Apply only after explicit user instruction
terraform apply -target=aws_instance.bastion
```

### State Locking

When state is locked by another process:

```bash
# List the lock (in backend-specific way)
# Then force unlock only if safe
terraform force-unlock <LOCK_ID>
```

**Warning**: Force unlocking can corrupt state. Only use when the lock holder has crashed.
