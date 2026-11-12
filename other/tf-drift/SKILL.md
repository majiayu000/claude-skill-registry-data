---
name: tf-drift
description: Backport AWS drift into terraform code so that `terraform plan` is clean (or shows only an explicitly intended diff). Fans out one sub-agent per drifted resource, each working from `terraform plan -target=<addr>` and `terraform state show <addr>` to update the .tf source until that resource's diff disappears. Use when the user asks to "reconcile drift", "backport drift", "make plan clean", or "update code to match AWS".
disable-model-invocation: false
user-invocable: true
allowed-tools: Bash, Read, Edit, Write, Agent
---

# Terraform drift backport

Use this when AWS state and terraform code have diverged and the user wants the code updated to reflect AWS reality (not the other way around — no `terraform apply` is involved).

## Inputs the user typically provides

- The terraform project directory (default: cwd).
- An optional **intended diff** to preserve (e.g. "only the BusinessUnit tag should remain in the plan"). Pass this through to every sub-agent — they need it to know which diff lines are noise vs. signal.

If the user hasn't named an intended diff, ask once. Without it you cannot tell when a resource is "done."

## Workflow

### 1. Bootstrap

```bash
terraform plan -no-color > /tmp/tf-drift-plan.out 2>&1
```

Plans on real infra are slow (often 60–120s). Run in the background and use `Monitor` (or a poll loop) to wait — never block the conversation on `sleep`.

If `terraform init` hasn't been run, ask the user to run it (or to confirm before you do — init can pull modules and take a while).

### 2. Enumerate drifted resources

From the plan output, extract the address of every resource whose action is `update in-place`, `replace`, `create`, `destroy`, or `import` and whose diff is **not** purely the intended diff.

```bash
grep -E "^  # .* will be (updated|created|destroyed|imported)|must be replaced" /tmp/tf-drift-plan.out
```

Skip resources that only show the intended diff (e.g. only `+ "BusinessUnit" = "amp"` under `tags_all`). A quick heuristic: if `-target` plan for that resource produces only the intended diff, it doesn't need a sub-agent.

### 3. Fan out — one sub-agent per resource

For each drifted resource, dispatch a `general-purpose` Agent **in parallel** (multiple Agent calls in one assistant turn). Per-resource isolation keeps each sub-agent's context narrow and lets terraform plans run concurrently across resources.

The prompt for each sub-agent should be self-contained and include:

1. **Goal**: "Update the terraform source for `<resource address>` so that `terraform plan -target='<resource address>'` shows only `<intended diff, verbatim>`. Do not run `terraform apply`."
2. **Working directory**: absolute path to the terraform project.
3. **Resource address** as a quoted string (module paths contain dots — use single quotes in shell).
4. **The two reference outputs the sub-agent should re-run itself**:
   - `terraform plan -target='<addr>' -no-color`
   - `terraform state show '<addr>'`
   The sub-agent should not trust a snapshot you paste in — drift evolves and re-running gives ground truth. Tell it to run them itself.
5. **Source file pointer**: grep for the resource block to point the sub-agent at the right `.tf` file:
   ```bash
   grep -rn "resource \"<type>\" \"<name>\"" *.tf
   ```
   For module-internal resources (`module.X.aws_foo.bar`), point them at the module input in this project — they cannot edit the module's own source from this project.
6. **Constraints**:
   - Only edit `.tf` files in the project directory (not the module sources under `.terraform/`).
   - For resources that exist in AWS but not in state, add an `import { to = ...; id = "..." }` block.
   - For resources present in code but absent in state and AWS, delete them.
   - For pure attribute drift, edit code values to match `terraform state show`.
   - For module-internal drift that can't be fixed without changing the module: report it back, don't bash on it.
   - Verify by re-running `terraform plan -target='<addr>'` and confirming the output matches the intended diff. Re-iterate until clean or until the sub-agent declares the resource module-locked.
7. **Reporting**: ask each sub-agent to return a one-line summary: `<addr>: <clean | residual: <one-line reason>>`.

### 4. Reassemble and verify

After all sub-agents return, run a full `terraform plan` once more. Compare the remaining diff against the intended diff:

- If they match → done. Surface the per-resource summaries to the user.
- If residuals remain, list them with the reasons collected from sub-agents. Do not silently retry — module-locked or AWS-side drift may need a human decision (bump module ref, manual `aws ...` fix, accept the residual, etc.).

## Common drift patterns and how a sub-agent should handle them

- **Resource in AWS, not in state, in code**: add `import { to = <addr>; id = "<aws id>" }`. Use the resource's natural import id (ARN for LB stuff, name for IAM, etc. — terraform docs per resource type).
- **Resource in AWS, not in state, not in code**: write a new resource block matching `terraform state show` (after import), plus the `import` block.
- **Resource in state, not in AWS**: rare — usually means someone manually deleted in AWS. Confirm with the user; do not blindly remove from state.
- **Resource in state and AWS, not in code**: terraform plan says "will be destroyed". Add the resource to code (don't accept the destroy).
- **Attribute drift**: edit the attribute in code to match `terraform state show`. Be careful with computed/`(known after apply)` fields — leave them alone.
- **`tags_all` differs by exactly the intended diff**: leave it (this is the intended diff).
- **Module-internal drift** (e.g. `module.foo.aws_bar.baz`): you can usually pass the right input via the module call (`task_environment_variables`, etc.) or bump the module `ref` to a version whose generated config matches AWS. If neither works, report and stop — don't fork the module from inside this project.
- **Imports counted in plan don't drop on re-plan**: that's normal — `terraform plan` doesn't write state. The diff stays the same across plans until `terraform apply -auto-approve` or an explicit `terraform apply` runs the import. The user controls when to apply.

## What this skill won't do

- It will not run `terraform apply`. The output is code changes the user reviews and applies themselves.
- It will not modify shared module source under `~/Repositories/.../terraform-modules` unless the user explicitly asks.
- It will not invent AWS resources that aren't in the plan output. If a sub-agent thinks it found drift outside the plan, it should stop and surface that.
