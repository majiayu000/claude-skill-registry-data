---
name: devdock-development
description: Use DevDock to run changed services in development, configure their routing, and prepare the environment for verification.
---

# DevDock development

Use the configured DevDock MCP. A repository is the checkout on the execution host; a workload is an API, worker, cron, or UI. A deployed pod and an active development session are separate states. The development session enables code synchronization and the development runtime.

## Tools and lifecycle

Inspect the available tool schemas for exact arguments.

| Tool | Purpose |
| --- | --- |
| list / status | Discover repositories, workloads, and their current state |
| checkout | Inspect checkout path, branch, revision, and local changes |
| start | Start development for an existing deployment |
| build_start | Deploy a workload and start development |
| run | Execute a command in the pod and obtain its exit result |
| logs / wait | Read output and wait for readiness or a known condition |
| operation_status | Check completion of a durable operation |
| instances / move_plan / move | List linked machines, preview and move a deployment between them |

An `exec` acknowledgment only proves command submission. Check completion and exit status before claiming success. Likewise an operation receipt or `RUNNING_MANAGED` is not completion: check `operation_status`, ready replicas with a stable restart count, and the mounted route. Prove sync by editing a file and reading it back in the pod, and check workload logs after adding a dependency.

1. Inspect state and checkout before changing anything. Reuse healthy running development sessions. When the user says not to restart, adopt the running workload; do not `restart` or `build_start`.
2. If the pod exists but development is stopped, start development only.
3. If a changed repository's pod is absent or purged, deploy it and start development.
4. Unchanged dependencies without development pods use the environment's UAT-US fallback. If UI is needed, deploy and start the relevant UI too.
5. Do not routinely purge or restart healthy workloads. If DevDock fails, report the operation ID and useful error to the user. Do not bypass it with direct infrastructure changes.
6. If a start hangs in building with no helm output, check that `lastContext.namespace` in the checkout's `.devspace/cache.yaml` matches the target namespace; a mismatch opens an interactive picker that waits forever.

## Machines

DevDock may be linked across machines, such as the laptop and a Linux workspace. `instances` lists them with their online and auth status. Every tool takes an optional `instance` UUID; omit it for the machine the MCP runs on. Each machine has its own checkout, and linking copies no code or `.env` files: a deploy or start builds from the target machine's checkout.

Each deployment is claimed by one machine. Run lifecycle actions, logs, and terminals on the owner. An action on another machine fails with "owned by instance"; do not retry it there. With more than one machine online, `replica_create` needs an explicit `instance`.

Move a deployment only when the user asks for it on another machine:

1. Run `move_plan` with the repository, workload, and target UUID. It returns the owner, whether it is reachable, whether a dev session is live, both checkouts' branch, commit, and dirty state, and the follow-up.
2. Tell the user if the checkouts differ in branch or commit, or if the source checkout has uncommitted changes. The target runs its own code, so those changes do not move.
3. If the owner is unreachable, the move takes the claim over. Confirm with the user that the owner is really gone first; a laptop that is only offline may still be running it.
4. Run `move`. A reachable owner stops its dev session and releases the claim; the deployment stays. A live session then starts on the target, with build + start when the commits differ. Pass `followUp` only to override that choice. Track the returned operation with `operation_status`.

## Environment hours

Development and UAT-US pods run on EKS nodes that opsbot turns off. When they are off, nothing can be deployed, started, or verified. Do not work around this by rescheduling pods onto always-on nodes or running dependencies elsewhere.

| When (IST) | What happens |
| --- | --- |
| 09:00 Mon-Fri | Nodes start |
| 22:30 daily | Nodes stop |
| 01:00, 03:00, 05:00, 07:00 daily | Nodes stop again if someone started them |
| 01:00, 07:00 daily | `-devspace` development pods scale to 0 |
| 12:30-23:15, every 15 min | `-devspace` pods Available for more than 10 hours scale to 0 |

A scheduled stop is skipped within 105 minutes of the last start. Weekends are off from Friday 22:30 to Monday 09:00, and daytime weekend starts stay up until 22:30.

Nodes are up when `kubectl get nodes -l workload=development,type=gp` lists Ready nodes (`type=mo` for UIs). Someone else may have started them; use that window. After nodes return, `start` brings development pods back. Do not `restart`.

When verification is blocked by the off window:

1. Tell the user it is blocked by environment hours and continue work that does not need pods.
2. Only when the user decides it is really needed, they run `/manage-env start eks-uat-us` in #ops-manage-env. It is a Slack slash command, so posting that text as a message does not run it. It starts every environment node for everyone.
3. When the work is done, remind the user to run `/manage-env stop eks-uat-us`. Whoever starts off-hours must stop it; missing that three times removes them from the channel. Do not ask for a stop when someone else started it.

## Routing and verification

Run every changed repository in development. Set the relevant environment values to `saibhushan` so API calls reach that user's development pods; preserve unrelated values. Inspect actual network requests and pod logs. A personal frontend URL can still call UAT, so confirm the changed service handled the request. A passing `/auth` phase proves OIDC only, not that the service handled it.

| Surface | Development | UAT-US |
| --- | --- | --- |
| Dashboard | https://dashboard-saibhushan.vmock.dev | https://dashboard-uat-us.vmock.dev |
| Admin / coach | https://admin-saibhushan.vmock.dev | https://admin-uat-us.vmock.dev |
| Candidate API | https://api-saibhushan-candidate.vmock.dev/<service>/ | https://api-uat-us-candidate.vmock.dev/<service>/ |
| CMC API | https://api-saibhushan-cmc.vmock.dev/<service>/ | https://api-uat-us-cmc.vmock.dev/<service>/ |
| Capabilities API | https://api-saibhushan-capabilities.vmock.dev/<service>/ | https://api-uat-us-capabilities.vmock.dev/<service>/ |

Confirm the app's route and environment configuration before using these URLs. Local checkout paths are supplied by DevDock; do not invent localhost routes.

For deeper setup and routing details, read the [DevSpace guidelines](https://github.com/vmockinc/guidelines/tree/master/devspace).
