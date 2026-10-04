---
name: first-deploy
description: Bootstrap Wandering OS into a clean AWS account (first deploy, go-live, or break-glass recovery when CI is broken) using the just bootstrap-* sequence.
---
# First deploy / break-glass

Takes a clean AWS account to a fully deployed system: 8 shell scripts in
`bootstrap/`, run as 9 ordered steps (`bootstrap-ci-vars` runs twice). After
go-live these are break-glass tools only — routine changes merge to `main`
(CI) and ship via a dispatched `*-deploy.yml` workflow (see the
deploy-a-change skill).

## Read first
- docs/GETTING_STARTED.md — the full runbook, including the manual steps: vendor signups (§3: Confluent, AuraDB, Anthropic), the DNS NS record (§4.7), the owner token (§5.1).
- bootstrap/README.md — per-script detail and the guards in bootstrap/_common.sh.

## Commands
```bash
just bootstrap-preflight                                            # read-only toolchain + account check
just bootstrap-deploy-core                                          # cdk bootstrap; WosCoreStack + WosCiStack
just bootstrap-ci-vars                                              # stack outputs → GitHub repo variables
just bootstrap-flink-jar                                            # dispatch flink-deploy.yml so the JAR exists first
just bootstrap-deploy-backend --confluent-bootstrap <server:9092>   # cdk deploy --all
just bootstrap-ci-vars                                              # again — picks up new outputs
just bootstrap-secrets                                              # fill Confluent / AuraDB / Anthropic secrets
just bootstrap-responder-token                                      # mint the bot's own token
just bootstrap-smoke                                                # end-to-end smoke, locally
```
## Gotchas
- Order matters: the Flink JAR must be in the artifacts bucket *before* `bootstrap-deploy-backend`, or WosFlinkStack fails with "unable to get the specified fileKey".
- Every script is account-guarded to 458443189947 (AWS profile `wandering_os`, us-east-1; `gh` CLI must be authenticated too); a fork must export `WOS_ACCOUNT_ID`.
- Manual step between steps: `just mint-token --role owner --label mike`, store it, and `gh secret set WOS_OWNER_TOKEN` — the CI smoke skips loudly until it exists.
- `bootstrap-secrets` needs no redeploy: Lambdas resolve secret ARNs at cold start.
- The §4.4 deploy pauses on WosDnsStack's ACM cert until the NS delegation record is added in the management account (166047286217).
