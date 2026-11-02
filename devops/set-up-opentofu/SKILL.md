---
name: set-up-opentofu
description: Use when infrastructure should be code — OpenTofu repo layout (one terraform/ root, per-env tfvars and backend files), encrypted remote state with locking, pinned providers, checks in CI, saved plans applied after approval, drift detection.
---

# Set Up OpenTofu

Infrastructure as reviewed code: one module set, one root with a state and a credential set per environment, state that is encrypted and locked, and an `apply` that only runs a plan a human approved. Contract: [environments.md](../_shared/environments.md). Layout and CI follow the fleet standard (`VelimirMueller/fleet-standard`, rules `TF-*` and `CI-*`).

## 1. Audit current state (change nothing)

```bash
cat .claude/stack-profile.md 2>/dev/null          # iac, hosting, ci, runtime_manager, task_runner
ls terraform/ terraform/envs terraform/modules infra/ 2>/dev/null; ls *.tf 2>/dev/null
git ls-files | grep -E '\.tfstate|\.tfplan|tfvars' # committed state or plans: stop and fix first
grep -rn --include=*.tf -E '^(terraform|provider) ' . | head -20
ls terraform/.terraform.lock.hcl terraform/.opentofu-version .tflint.hcl 2>/dev/null
tofu version 2>&1 | head -1
```

From the profile: `iac` (`opentofu` or `none`), `hosting` (picks the provider), `ci` (github-actions), `runtime_manager` (mise, asdf, none). If `iac: none` and the user did not ask for IaC, stop. If the repo already has Terraform (`required_providers` with `hashicorp` source, `.terraform.lock.hcl` from Terraform), keep its layout and migrate in place (step 2).

## 2. Decide
- No tofu files → full setup (steps 3 to 7).
- Existing tofu, partial → add only the missing pieces: lock file, encryption, CI, drift, tests.
- Existing per-environment roots (`infra/envs/<env>/`) → move them into one `terraform/` root with `envs/<env>.tfvars` and `envs/<env>.backend.hcl`; keep each state key, so no resource moves. Until the move is done, record a `TF-LAYOUT-02` exception with `expires` in `fleet.yml`.
- Terraform repo → `tofu init` reads it as is; add `.terraform.lock.hcl` for the registry.opentofu.org addresses with `tofu providers lock`, then add encryption. Do not rename resources.
- Layout, backend, encryption, CI and drift all present → "already in place", run step 7, stop.
- Committed `*.tfstate`: remove from history first and rotate every secret it held.

## 3. Detect the provider
| `hosting` | Provider | Skill that uses this |
|---|---|---|
| `hetzner` | `hetznercloud/hcloud` ~> 1.70 | [deploy-to-hetzner](../deploy-to-hetzner/SKILL.md) |
| `ionos` | `ionos-cloud/ionoscloud` ~> 6.7 | [deploy-to-ionos](../deploy-to-ionos/SKILL.md) |
| `vercel`, `supabase` only | none required | Skip; configure through [deploy-to-vercel](../deploy-to-vercel/SKILL.md). A provider exists for both; add it only when the team wants projects and env vars as code |

## 4. Install only what is missing
Pin the tool with the profile's runtime manager (`mise use opentofu@1.13.1`) or the package manager of the machine (`brew install opentofu`). CI uses `opentofu/setup-opentofu`. Line and support window: [stack-versions.md](../_shared/stack-versions.md). Use a supported line (1.12 or 1.13); 1.11 and 1.10 are end of life.

## 5. Generate

Layout (fleet standard TF-LAYOUT-01, TF-LAYOUT-02, TF-FILE-01):
```
terraform/
  .opentofu-version  .terraform.lock.hcl
  versions.tf  backend.tf  providers.tf  variables.tf  locals.tf  main.tf  outputs.tf
  envs/{dev,stg,prd}.tfvars  envs/{dev,stg,prd}.backend.hcl
  modules/<name>/{main,variables,outputs,versions}.tf  + tests/*.tftest.hcl
.tflint.hcl
```
Details and every file in [opentofu-patterns.md](./opentofu-patterns.md). In short:

1. **`versions.tf`**: `required_version = "= 1.13.1"`, the exact version that `terraform/.opentofu-version` holds (a supported line from step 4), and a `required_providers` block with the full `source`. Without it OpenTofu looks for `hashicorp/<name>` and fails or, worse, picks a different provider with the same name.
2. **`backend.tf`** names the S3 backend; **`envs/<env>.backend.hcl`** holds the bucket, one state key per environment, `use_lockfile = true`. Versioning on the bucket. Create the bucket once by hand (console or CLI); it is the one resource that cannot manage itself.
3. **Encryption**: `TF_ENCRYPTION` environment variable with `pbkdf2` key provider and `aes_gcm`, `enforced = true` for state **and** plan. Passphrase from the secret store ([manage-secrets](../manage-secrets/SKILL.md)).
4. **Lock file**: `tofu providers lock -platform=linux_amd64 -platform=linux_arm64 -platform=darwin_arm64`, committed. CI runs `init -lockfile=readonly`.
5. **`.gitignore`**: `.terraform/`, `*.tfstate*`, `*.tfplan`, `tfplan`, `crash.log`, `*.auto.tfvars`. No `terraform.tfvars` and no `*.auto.tfvars` under `terraform/` (TF-FILE-04).
6. **Module tests** with `mock_provider` (`tofu test`).

## 6. Wire
- Workflows: the [set-up-terraform-pipeline](../set-up-terraform-pipeline/SKILL.md) files with `tool: tofu` and `cloud: none`, plus the changes in [opentofu-ci-patterns.md](./opentofu-ci-patterns.md). PRs run only the credential-free checks; every plan and apply starts by hand (`infra.yml`, `deploy.yml`, `promote.yml`); drift is `tf-drift.yml`, started by hand.
- GitHub environments (`scripts/setup-github.sh`): `dev`, `stg`, `prd` hold the secrets for apply, without reviewers; the gates `promote-stg`, `promote-prd` and `tf-apply-prd` hold the reviewer. `dev-plan`, `stg-plan`, `prd-plan` hold plan secrets without reviewers, so a plan does not wait for a person.
- Environment secrets: `TF_ENCRYPTION`, `TFSTATE_ACCESS_KEY_ID` and `TFSTATE_SECRET_ACCESS_KEY` (state bucket credentials, mapped to `AWS_*` in the job), and `HCLOUD_TOKEN` or `IONOS_TOKEN`. **No OIDC exists for Hetzner or IONOS** (none found 2026-10-09), so these are long-lived tokens: scope them per environment, rotate on a schedule, list them in `fleet.yml` `secrets:` (SEC-07), and record the `SEC-01` exception there.
- Delivery of the application itself stays in [set-up-delivery-pipeline](../set-up-delivery-pipeline/SKILL.md).

## 7. Verify
```bash
cd terraform
tofu fmt -check -recursive                                                   # no output
tofu init -input=false -lockfile=readonly -backend-config=envs/dev.backend.hcl  # "successfully initialized"
tofu validate                                                                # "The configuration is valid."
tofu -chdir=modules/<name> test                                              # "Success! N passed, 0 failed."
tofu plan -input=false -var-file=envs/dev.tfvars -detailed-exitcode; echo $?   # 0 = no changes, 2 = changes, 1 = error
pnpm --dir <fleet-standard> fleet check ..                                   # "Result: conforms"
```
Encryption check: with `TF_ENCRYPTION` unset, `tofu plan` must fail to read the state. A plan file must start with `{"meta":{"key_provider.pbkdf2…`, not with the plan JSON.
Locking check: run two applies at once; the second must print `Error acquiring the state lock`. If the bucket cannot lock, `use_lockfile` is not safe there; see the S3 rule in the patterns file.

## References
- [opentofu-patterns.md](./opentofu-patterns.md): layout, backend, encryption, providers, secrets, tests.
- [opentofu-ci-patterns.md](./opentofu-ci-patterns.md): the pipeline changes for OpenTofu, plan artifact, drift.
- [../set-up-terraform-pipeline/workflow-templates.md](../set-up-terraform-pipeline/workflow-templates.md): the workflow files.
- [../_shared/environments.md](../_shared/environments.md), [../_shared/hosting-decision.md](../_shared/hosting-decision.md).
- [../../core/_shared/security-baseline.md](../../core/_shared/security-baseline.md), [../../core/_shared/engineering-principles.md](../../core/_shared/engineering-principles.md).
