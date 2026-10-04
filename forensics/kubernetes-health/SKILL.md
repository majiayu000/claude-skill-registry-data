---
name: kubernetes-health
description: >
  Check live Kubernetes cluster health with read-only diagnostics: nodes, pods, storage, networking, and GitOps.
license: MIT
compatibility: "Requires kubectl; jq for the event-window check. Optional: helm, openssl, dig, ssh"
metadata:
  source: iuliandita/skills
  date_added: "2026-03-30"
  effort: high
  argument_hint: "[context-or-alias] [timewindow]"
---

# Kubernetes Health

Run read-only Kubernetes health checks and report cluster status with evidence. This skill works
without private overlays by requiring an explicit kube context or confirmed current context.
Local users may add ignored protected overlays for aliases and environment-specific checks.

## When to use

- User asks to check cluster health, status, diagnostics, node status, or post-maintenance state
- Verifying cluster-wide symptoms after upgrades, reboots, Helm changes, GitOps syncs, or incidents
- Gathering read-only evidence across nodes, workloads, events, ingress, storage, logs, and policy
- Producing a short traffic-light report from Kubernetes and related observability signals

## When NOT to use

- Writing or reviewing Kubernetes manifests - use **kubernetes**
- Writing Helm charts, Kustomize overlays, or IaC - use **kubernetes** or **terraform**
- Changing resources, restarting pods, deleting objects, or applying fixes - ask for explicit escalation
- Debugging one application deeply after the broad sweep identifies it - use the relevant domain skill
- Unknown-root-cause debugging or triage - use **debug-triage**

---

## AI Self-Check

Before running checks or reporting results, verify:

- [ ] Target context is explicit or the current context was confirmed
- [ ] Every `kubectl` command includes `--context <context>`
- [ ] Every `helm` command includes `--kube-context <context>`
- [ ] Commands are read-only: no apply, patch, delete, edit, rollout restart, scale, cordon, drain, or exec unless the user explicitly escalates
- [ ] Output is capped with `head`, `tail`, `--since`, `--field-selector`, or selectors
- [ ] Time window is bounded and stated in the report
- [ ] Protected registry contents are not printed unless the user asks for those exact details
- [ ] Findings include evidence, impact, and next action
- [ ] **No improvisation**: reference checks or verified read-only follow-ups used confirmed object names and supported flags; missing coverage was reported
- [ ] **Stderr is visible**: diagnostic commands surface their failure reason instead of masking it with `2>/dev/null`; a missing tool, permission gap, or wrong context is reported, not silently treated as a clean result
- [ ] Cross-cutting agent hygiene applied - see `references/agent-hygiene.md`

## Performance

- Start with cluster-wide signals before loading symptom-specific references.
- Prefer summarized evidence over dumping raw Kubernetes output into context.

## Best Practices

- Separate health evidence from remediation; fixes require a separate escalation.
- Start with the reference checks. Use verified read-only follow-ups against discovered objects when needed to establish health; never guess service names, namespaces, paths, or flags.
- Do not read a metric's status without knowing what the metric measures. The reference files state what each signal does and does NOT represent; misreading a percentage or a stale value produces a confidently wrong report.

## Cluster Registry

This public skill has no built-in private cluster registry.

Users may create local-only overlays under `skills/kubernetes-health/protected/` for private lab,
homelab, work, or customer cluster details. The directory is gitignored by this collection. If it
exists in the installed skill, read it while using this skill. A user can ask their agent to create
or update these files.

Suggested local layout:

```text
protected/
  registry.md            # aliases, kube contexts, CWD patterns, profile mappings
  private-patterns.txt   # terms that must never appear in public files
  <cluster-or-env>.md    # local namespaces, runbooks, dashboards, thresholds
```

1. If `protected/registry.md` exists, read it first and use its alias, context, CWD pattern, and
   reference mappings.
2. If the registry maps the target to `protected/<cluster-or-env>.md`, read that profile before
   running checks.
3. If no protected registry exists, require an explicit kube context or ask before using the current
   context.
4. Never guess a cluster from a vague request.
5. Never print protected registry contents in public reports unless the user asks for those exact
   details.
6. Treat gitignored as local privacy, not encryption. Do not put protected overlays in shared logs,
   issues, PR comments, or public reports.

## Usage

```
kubernetes-health [context-or-alias] [timewindow]
```

- `context-or-alias` is a kube context, current-context confirmation, or protected overlay alias.
- `timewindow` defaults to `2h`; use bounded values such as `30m`, `1h`, `2h`, `6h`, or `24h`.

## Workflow

Copy this checklist and track progress:
- [ ] Step 1: Target context resolved (explicit or confirmed)
- [ ] Step 2: Context and time window stated; read-only scope confirmed
- [ ] Step 3: Sweep run (on a wrong-context or unreachable-cluster error, return to Step 1)
- [ ] Step 4: Findings classified GREEN/YELLOW/RED
- [ ] Step 5: Report returned with evidence and next actions

### Step 1: Resolve target

If a protected registry maps the request or current directory to an alias, use that mapping. If no
mapping exists, require an explicit kube context or ask whether to use `kubectl config current-context`.

### Step 2: Confirm read-only scope

State the context and time window before running commands. Do not run mutation commands as part of
this skill.

### Step 3: Run the generic sweep

Treat generic health, cluster-wide, and post-maintenance requests as broad sweeps: run
`references/kubernetes-core.md`, `references/helm-gitops.md`,
`references/networking-ingress.md`, `references/storage.md`, and
`references/monitoring-logs.md`. For a narrower symptom-scoped request, start with
`references/kubernetes-core.md` and load only the matching references below. Load
`references/security.md` when policy, RBAC, or image risk is in scope or the core sweep exposes it.

- networking or certificate symptoms -> `references/networking-ingress.md`
- release or reconciliation symptoms -> `references/helm-gitops.md`
- pending pods or volume symptoms -> `references/storage.md`
- noisy errors or alert symptoms -> `references/monitoring-logs.md`
- policy, RBAC, or image-risk symptoms -> `references/security.md`

### Step 4: Classify findings

Use GREEN for healthy signals, YELLOW for degraded or ambiguous state, and RED for user-visible
outage, data-risk, or control-plane risk. Distinguish transient rollout noise from persistent
degradation.

### Step 5: Report

Return a concise report:

```markdown
# Cluster Health Report - <context> (<timewindow>, YYYY-MM-DD HH:MM)

## Summary
- STATUS: GREEN|YELLOW|RED
- Scope: <contexts, namespaces, time window>
- Key findings: <short bullets>

## Evidence
- <area>: <command or source> -> <observed signal>

## Next Actions
- <read-only follow-up or explicit escalation request>
```

## Reference Files

- `references/kubernetes-core.md` - nodes, workloads, events, namespaces, and resource pressure
- `references/helm-gitops.md` - Helm releases, GitOps controllers, and reconciliation state
- `references/networking-ingress.md` - services, ingress, Gateway API, load balancers, DNS, and certificates
- `references/storage.md` - PVs, PVCs, CSI drivers, storage classes, and volume attachment
- `references/monitoring-logs.md` - alerts, metrics availability, log triage, and noisy namespaces
- `references/security.md` - read-only checks for RBAC, secrets exposure signals, image risk, and policy engines

## Output Contract

See `references/output-contract.md` for the full contract.

- **Skill name:** KUBERNETES-HEALTH
- **Deliverable bucket:** `audits`
- **Mode:** conditional. When invoked to **analyze, review, audit, or improve** existing repo content, apply the reporting size and evidence rules in `references/output-contract.md` and write the deliverable to `docs/local/audits/kubernetes-health/<YYYY-MM-DD>-<slug>.md`. When invoked to **answer a question, teach a concept, build a new artifact, or generate content**, respond freely without the contract.
- **Severity scale:** `P0 | P1 | P2 | P3 | info` (see shared contract; only used in audit/review mode).

## Related Skills

- **kubernetes** - write or review manifests, Helm charts, Kustomize, and GitOps config
- **networking** - debug DNS, routing, proxies, VPNs, and Linux networking
- **security-audit** - review security controls or vulnerability posture beyond read-only cluster signals
- **terraform** - change infrastructure definitions or state

## Rules

1. Read only. Do not mutate cluster state unless the user explicitly changes the task.
2. Report failed checks as findings; do not hide missing tools, missing CRDs, or permission errors.
3. **Use reference checks and verified read-only follow-ups against the confirmed target.** Discover object names, verify flags, and report missing coverage. Mutation still requires explicit escalation.
