---
name: pulumi
description: >-
    Owns Pulumi infrastructure-as-code: creating, inspecting, and destroying cloud and SaaS
    resources on any Pulumi-registry provider — `pulumi do` one-offs, projects and stacks,
    ComponentResource design and packaging, Automation API, ESC environments, policy packs, drift
    schedules. Use when reviewing or refactoring Pulumi code, debugging a failed `up` or `preview`,
    chasing an unexpected replace or delete in a preview, adopting resources via `pulumi import`,
    converting Terraform, CloudFormation, CDK, Bicep, or ARM code, and on tasks that never name
    Pulumi — "deploy this app", "provision a database", "stand up a VPC", "tear down staging".
---

# [PULUMI]

Pulumi creates and manages cloud infrastructure — virtual machines, storage, Kubernetes clusters, databases, DNS, SaaS configuration — from code or CLI commands: it previews the pending change, then applies it. Work enters at the smallest of three levels that fits the task; depth for each concern rides one hop down in a reference.

| [INDEX] | [LEVEL] | [SURFACE]                         | [WHEN]                                        |
| :-----: | :------ | :-------------------------------- | :-------------------------------------------- |
|  [01]   | L1      | `pulumi do` CLI                   | Single resource or multi-vendor bootstrapping |
|  [02]   | L2      | Pulumi project in a host language | Multiple related resources                    |
|  [03]   | L3      | Pulumi Cloud governance layer     | Governance and hosted runs                    |

A single-bucket request in a directory with no Pulumi project is an L1 task — no project scaffolding. A VPC with subnets and a cluster is L2 from the start. Nightly drift detection on an existing stack is L3. Converting Terraform, CloudFormation, CDK, ARM, or Bicep code is `pulumi convert` guided by https://www.pulumi.com/docs/iac/adopting-pulumi/, independent of the level model.

Level choice requires knowing what is already on disk: inspect the filesystem first, and in a restricted context ask before any Pulumi command runs — a command that requires a login silently provisions a new agent account parallel to one the operator already owns.

An uncertain CLI flag, command shape, or resource property is looked up, never guessed: `npx pulumi <command> --help` documents every flag from the CLI itself; the full reference, provider catalog, and conceptual docs live at https://www.pulumi.com/docs and https://www.pulumi.com/registry/.

## [01]-[ROUTING]

- [01]-[CLI_OPERATIONS](references/cli-operations.md): driving one-off resource work from the CLI, and graduating it into a program.
- [02]-[BEST_PRACTICES](references/best-practices.md): laws every non-trivial program obeys before it runs.
- [03]-[COMPONENTS](references/components.md): `ComponentResource` anatomy, args interface design, multi-language packaging, and distribution.
- [04]-[AUTOMATION_API](references/automation-api.md): embedding Pulumi in a program, multi-stack orchestration, and inline versus local programs.

## [02]-[ONE_SHOT_OPERATIONS]

`pulumi do` runs one-shot, stateless resource operations against any provider — no project files, no `${...}` wiring, no Pulumi state. `npx pulumi <command>` is the canonical invocation — the PATH `pulumi` lacks the resource verbs. `npx pulumi version` confirms availability without touching Pulumi Cloud.

```text
pulumi do <pkg:mod:type> create [flags]
pulumi do <pkg:mod:type> read|patch|delete <id> [flags]
pulumi do <pkg:mod:type> list [flags]
```

- `create` provisions and prints properties as JSON including the cloud `id`; pass `--yes` in non-interactive contexts.
- `read <id>` fetches live provider state; writes nothing.
- `patch <id>` shallow-overlays top-level properties in place; a change requiring replacement fails rather than recreating.
- `delete <id>` is irreversible — explicit operator confirmation of the specific resource precedes `--yes`, never a non-interactive default.
- `list` enumerates existing instances where the resource type implements listing.

First invocation without saved credentials provisions an ephemeral agent account and prints a claim banner to stderr; surface the claim URL to the operator immediately and again in the final response — a session ending without it strands resources. On authentication failure, ask the operator to run `pulumi login`; never fall back to `pulumi login --local` or set `PULUMI_CONFIG_PASSPHRASE`. Provider credentials arrive separately through the provider's native environment variables (`AWS_PROFILE`, `CLOUDFLARE_API_TOKEN`); when absent, ask before any command that calls out to the cloud.

When a `Pulumi.yaml` project already manages a resource, changes go through the program — never `pulumi do`.

## [03]-[PROJECT_PROGRAMS]

A Pulumi project is code in Python, TypeScript, Go, C#, or Java describing related resources and their dependencies. Match the codebase language when one is present; default to TypeScript otherwise.

```bash copy-safe
npx pulumi new aws-typescript      # template list: npx pulumi template list
npx pulumi preview                 # show what would change — always before up
npx pulumi up                      # apply
npx pulumi refresh                 # reconcile state with cloud reality
```

`pulumi destroy` tears down every resource in the stack and is generally irreversible; explicit operator confirmation of the stack name precedes it. A stack only touches resources tracked in its state, so removing a resource from the program deletes it from the cloud on the next `up`; `protect: true` guards anything unaffordable to lose.

Stacks isolate instances of a project — one per environment (`dev`, `staging`, `prod`) is the standard pattern:

```bash copy-safe
npx pulumi stack init dev
npx pulumi config set aws:region us-west-2
npx pulumi config set --secret dbPassword "..."
```

## [04]-[CLOUD_GOVERNANCE]

Pulumi Cloud layers governance onto a project: ESC composes secrets and configuration from cloud secret managers, OIDC-vended credentials, and other environments into one resolved bundle; policy packs run against the resource graph before any cloud API call; deployments run operations server-side; schedules automate drift detection and rotation.

```bash template
npx pulumi env init my_org/aws/prod
npx pulumi env run my_org/aws/prod -- aws s3 ls     # injects credentials; never capture `env open` output
npx pulumi policy new aws-typescript
npx pulumi deployment run update --stack my_org/proj/prod
npx pulumi refresh --preview-only                    # ad-hoc local drift check
npx pulumi stack schedule new --kind drift --cron "0 0 * * *"
```

A provider with OIDC federation vends cloud credentials through it rather than static keys in environment YAML. A schedule is standing automation that outlives the session — confirm operation, cadence, and stack with the operator first, and default to detection-only: `--kind drift --auto-remediate` and `--kind ttl` act without a human in the loop.

## [05]-[DEBUGGING]

A failed `pulumi up` or `pulumi preview` already recorded its error; debugging reads that record, traces the cause, and places the fix — nothing reruns to reproduce. Every read command reaches Pulumi Cloud through `pulumi api`, addressing a stack by explicit `{orgName}/{projectName}/{stackName}` path, so the stack need not be selected locally to read its record; selection matters only when applying the fix.

### [05.1]-[IDENTIFY_THE_OPERATION]

An operation arrives as org, project, stack, and an update version or preview id — usually in prose ("debug update 161 of vvm-dev"). Missing fields fill from context: the selected stack (`pulumi stack --show-name`, `pulumi stack ls`) or `Pulumi.yaml`; a missing version means the most recent update. Confirm the landed-on operation — version or preview id and stack — with the operator before reading further.

When nothing identifies the operation, the target is the operator's most recent one. Update lists never record who ran each update, so identity resolves through the API: `pulumi whoami` gives the login; `pulumi api /api/stacks/{orgName}/{projectName}/{stackName}/updates/latest` gives the latest update and its `requestedBy.githubLogin`; on mismatch, walk back one version at a time via `/updates/<n>` until the login matches. State which operation was landed on — version, kind, result — and confirm before going further.

### [05.2]-[READ_WHAT_FAILED]

Failed updates and failed previews both record engine events; the error lives in the diagnostic messages inside them.

```bash template
# Failed update — by version number
pulumi api /api/stacks/{orgName}/{projectName}/{stackName}/update/<version>/events \
  | jq -r '.events[].diagnosticEvent | select(. != null) | "[\(.severity)] \(.message)"' \
  | sed 's/<{%reset%}>//g'

# Failed preview — by preview id
pulumi api /api/stacks/{orgName}/{projectName}/{stackName}/preview/<preview-id>/events \
  | jq -r '.events[].diagnosticEvent | select(. != null) | "[\(.severity)] \(.message)"' \
  | sed 's/<{%reset%}>//g'
```

Every message matters, not only `severity == "error"`: a provider error carries the `error` tag, but a program error — the common case when a preview fails — arrives as a stderr diagnostic tagged `info#err`. A trailing `sed` strips the terminal color codes Pulumi embeds.

### [05.3]-[PLACE_THE_FIX]

An operation can fail with errors from more than one resource: read all diagnostics first, then trace each error to the resource that raised it (URN and type), its declaration in the program, and the inputs feeding it. Error text names the problem kind, and the kind names where the fix belongs:

- [PROGRAM]: Code is wrong — a bad reference, wrong type, rejected input, or a value used before it resolved. Usual failed-preview cause: the plan never built. Fix by editing the code.
- [STATE]: Code is correct but stored state and cloud reality disagree. Reconcile drift with `pulumi refresh`; bring an already-existing external resource under management with `pulumi import` rather than recreating it. An operation that failed partway may have already changed resources — check current state before deciding.
- [ENVIRONMENT]: Problem sits outside Pulumi — credentials, permissions, OIDC, quota. Fix the role, the ESC environment, or the capacity the provider rejected, never the resource code.

Smallest change addressing the root cause wins; confirmation and delivery of the fix follow the active mode's workflow.
