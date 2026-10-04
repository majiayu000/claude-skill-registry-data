---
name: deploy-to-cloud-env
description: Deploy a delivered increment to ONE resolved cloud environment exactly as the slice's run lens (run.yaml) declares it — run the environment's declared deploy command honoring its provider, region, compute, services, and networking; read secrets only from the declared secrets-manager binding (never print or store them); then prove the increment answers with an independent reachability/health check and capture a deploy record (environment, what ran, address, health proof, secrets source). On failure it leaves the environment in its prior state and records the failure — it never auto-rolls-back. Executes only; never edits product code or the product model. The worker skill for the /deploy play's Deploy step, invoked through the env-operator agent.
version: 0.1.0
user-invocable: false
model: sonnet
allowed-tools: Read, Write, Bash, Grep, Glob
---

# deploy-to-cloud-env

Deploy a delivered increment to the ONE cloud environment named to you, doing exactly what that
environment's `run.yaml` block declares — and prove it came up. You execute infrastructure the run
lens already defined; you never invent it, and you never change the product or its model.

## What it produces

A **deploy record** (`deploy.json`) capturing the run: the target environment, its status
(`succeeded` | `failed`), the steps that ran, the reachable address, the independent health check
result, and the secrets-manager binding used (never the secret values). On a failed deploy the record
also carries `prior_state_left: true` — the environment was left as it was, not half-deployed.

## Inputs

| Field | Required | Description |
|-------|----------|-------------|
| `run_lens` | yes | Path to the slice's `lens/run.yaml`. Your only source of infrastructure truth. |
| `environment` | yes | The resolved cloud environment name to deploy to (e.g. `dev`) — its `environments[]` entry in `run.yaml` holds provider, region, compute, services, networking, secrets binding, and `deploy_cmd`. |
| `repo_root` | yes | The repository holding the delivered increment (on main). Read-only for build inputs. |
| `record_out` | yes | Path to write the deploy record (`deploy.json`). |
| `mode` | no | `up` (default — deploy) or `down` (tear down a prior deploy of this env). |

## Procedure

1. **Read the target environment.** Load the named `environment` from `run.yaml`. Take its `cloud`
   block: provider, region, `compute` (per-component service + deploy kind), `services`, `networking`
   (ingress + firewalls), `security` (identity + secrets binding + controls), and `deploy_cmd`. If the
   named environment is absent or is not a cloud environment, fail with `env_not_defined` — do not
   invent it.
2. **Bind secrets, never expose them.** Resolve credentials from the `security.secrets` manager
   binding the lens declares (e.g. a Secret Manager / Vault reference). Never echo, log, or write a
   secret value into the record or the repo — reference the binding only.
3. **Deploy exactly what is declared.** Run the environment's `deploy_cmd`, honoring its provider,
   region, compute, services, and networking. Run nothing the lens did not declare. Capture the
   command output to a logs file (scrubbed of secrets) and the resulting address.
4. **Prove it — an independent health check.** Do NOT trust the deploy command's exit code. Reach the
   deployed address (an HTTP/health probe against what the increment exposes) and confirm it answers.
   Record `health.status = green` only when it actually answers; otherwise `red`.
5. **Write the record.** Write `deploy.json` to `record_out`: `environment`, `status`
   (`succeeded` only if health is green), `ran` (the steps, referencing the declared `deploy_cmd`),
   `address`, `health` (status + evidence), `secrets_source` (the binding), and — on any failure —
   `prior_state_left: true`. Return the record path.

On any failure during 3–4, stop, leave the environment in its prior state (tear down a partial bring-up
so nothing is half-deployed), set `status: failed` and `prior_state_left: true`, and record what went
wrong. Never attempt an automatic rollback-and-redeploy — a human decides the next move.

## Output — the deploy record

```json
{
  "environment": "dev",
  "status": "succeeded",
  "ran": ["<the declared deploy_cmd and its steps>"],
  "address": "https://dev.example.internal",
  "health": { "status": "green", "evidence": "GET /healthz -> 200 in 0.4s" },
  "secrets_source": "projects/acme/secrets/dev-db-url (Secret Manager)",
  "prior_state_left": false
}
```

Return the contract with the `record_out` path — a path, never inline secrets or output.

## Rules

- **Run lens is the only infra truth.** Deploy exactly what the named environment's `run.yaml` declares
  — provider, region, compute, services, networking, `deploy_cmd`. If the lens doesn't declare it, you
  don't build it.
- **Secrets stay bound.** Read secrets only from the declared secrets-manager binding; never print,
  log, or write a secret value into the record or the repo.
- **Independent proof of health.** `status: succeeded` requires the reachability/health check to pass —
  never infer success from the deploy command's exit code alone.
- **No half-deploys, no auto-rollback.** On failure, leave the environment in its prior state (tear down
  any partial bring-up) and record `prior_state_left: true`; do not retry-and-redeploy on your own.
- **Execute only.** Never edit product code, the product model, epic records, evals, verdicts, or
  sign-off records. Production is never your target — the calling play caps the tier.
- **Every claim evidenced.** No `green` without a real reachability probe recorded in the deploy record.
```
