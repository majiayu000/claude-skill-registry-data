---
name: falco
description: "Expert agent for Falco CNCF runtime security. Covers kernel syscall monitoring via eBPF/kernel module, rule syntax (conditions, macros, lists, exceptions), 70+ default rules, plugins (CloudTrail, K8s Audit, Okta, GitHub), Falcosidekick routing to 60+ outputs, and falco-talon automated response. WHEN: \"Falco\", \"Falco rules\", \"Falco eBPF\", \"Falco kernel module\", \"Falcosidekick\", \"falco-talon\", \"Falco plugins\", \"Falco CloudTrail\", \"Falco runtime detection\", \"CNCF Falco\"."
license: MIT
---

# Falco

This skill covers Falco — the CNCF graduated open-source project for cloud-native runtime security. Falco monitors kernel-level syscall activity and generates alerts when behavior matches security rules. It has deep knowledge of Falco's architecture, rule syntax, kernel monitoring mechanisms, plugin system, and the ecosystem tools (Falcosidekick, falco-talon).

## How to Approach Tasks

When you receive a request:

1. **Classify** the request type:
   - **Rule Authoring** -- Write custom Falco rules with conditions, macros, lists, output fields
   - **Deployment** -- Falco installation (Helm, DaemonSet, OS service), driver selection
   - **Debugging** -- Falco performance, noisy rules, false positives, rule conflicts
   - **Plugins** -- CloudTrail, K8s Audit, Okta, GitHub plugins — configuration and custom plugins
   - **Falcosidekick** -- Alert routing configuration, output channels, filtering
   - **falco-talon** -- Automated response rules (response engine)
   - **Integration** -- SIEM, SOAR, alerting integration via Falcosidekick
   - **Performance** -- eBPF vs kernel module, ring buffer tuning, event dropping

2. **Identify environment** -- Kubernetes version and platform? Kernel version? Existing Falco deployment? What events need to be detected?

3. **Load context** -- Read `references/architecture.md` for deep architectural knowledge when needed.

4. **Analyze** -- Apply Falco-specific reasoning. Falco is a detection tool, not a prevention tool (by default). Focus on detection logic, signal quality (low false positives), and response integration.

5. **Recommend** -- Provide specific, tested rule syntax and configuration. Bad Falco rules cause alert fatigue — quality over quantity.

## Falco Architecture Overview

Falco monitors Linux kernel syscalls in real-time using either:
- **eBPF probe:** Modern approach; no kernel module; requires kernel 4.14+ with eBPF support
- **Kernel module:** Traditional approach; compiled `.ko` module loaded into kernel
- **Modern eBPF (CO-RE):** Kernel 5.8+ with BTF; portable, no per-kernel compilation

Events flow from kernel → Falco engine → rule evaluation → alerts → Falcosidekick → destinations.

## Falco Rule Syntax

### Rule Structure

```yaml
- rule: Shell spawned in a container
  desc: >
    A shell was spawned in a container. This may indicate an attack or
    administrative action. Investigate immediately.
  condition: >
    container.id != host
    and proc.name in (shell_binaries)
    and not proc.pname in (allowed_parent_processes)
  output: >
    Shell spawned in container
    (user=%user.name user_loginuid=%user.loginuid
     container_id=%container.id container_name=%container.name
     image=%container.image.repository:%container.image.tag
     shell=%proc.name parent=%proc.pname cmdline=%proc.cmdline)
  priority: WARNING
  tags: [container, shell, process]
```

**Rule fields:**
- `rule`: Unique name (string); referenced by other rules for exceptions
- `desc`: Human-readable description; shown in alerts
- `condition`: Boolean expression evaluated against each event; if true → alert
- `output`: Alert message; uses event fields (`%field.name`)
- `priority`: EMERGENCY, ALERT, CRITICAL, ERROR, WARNING, NOTICE, INFORMATIONAL, DEBUG
- `tags`: Labels for categorization and filtering
- `enabled`: true/false — disable without removing rule
- `exceptions`: Named exception conditions that suppress the alert

### Condition Operators and Logic

```yaml
# Logical operators
condition: >
  evt.type = execve                # event type equals
  and container.id != host         # AND not the host
  and not proc.name = "bash"       # AND NOT bash specifically
  or proc.name = "sh"              # OR sh

# Comparison operators
condition: proc.args contains "--privileged"
condition: fd.typechar in ('4', '6')    # in list
condition: proc.name startswith "kube"
condition: container.image.repository glob "*/suspicious-*"
condition: proc.args pmatch (/.*\-\-listen.*\d{4,5}.*/)  # regex match

# Arithmetic
condition: evt.buflen > 10000000   # greater than

# Existence checks
condition: fd.name exists          # field has a value
condition: container.id != ""      # non-empty string check
```

### Event Fields Reference

**Process fields:**
| Field | Description | Example |
|---|---|---|
| `proc.name` | Process name (basename) | `bash`, `python3` |
| `proc.cmdline` | Full command line | `bash -c "curl attacker.com"` |
| `proc.args` | Process arguments | `-c "curl attacker.com"` |
| `proc.pid` | Process ID | `12345` |
| `proc.ppid` | Parent process ID | `100` |
| `proc.pname` | Parent process name | `sh` |
| `proc.aname[n]` | Ancestor process name (n levels up) | `proc.aname[2]` = grandparent |
| `proc.exepath` | Full path to executable | `/usr/bin/bash` |
| `user.name` | Username of process owner | `root`, `www-data` |
| `user.loginuid` | Login UID (tracks sudo escalation) | `1000` |

**Container fields:**
| Field | Description | Example |
|---|---|---|
| `container.id` | Container ID (short) | `abc123def456` |
| `container.name` | Container name | `my-app-container` |
| `container.image.repository` | Image repository | `nginx` |
| `container.image.tag` | Image tag | `1.25.3` |
| `container.image.digest` | Image digest | `sha256:abc...` |
| `k8s.pod.name` | Pod name (K8s) | `my-app-7d9f8b-xyz` |
| `k8s.pod.label[key]` | Pod label value | `k8s.pod.label[app]` = `my-app` |
| `k8s.ns.name` | Kubernetes namespace | `production` |
| `k8s.deployment.name` | Kubernetes deployment | `my-app` |

**File/network descriptor fields:**
| Field | Description | Example |
|---|---|---|
| `fd.name` | File/socket name | `/etc/shadow`, `10.0.0.1:80` |
| `fd.directory` | Directory of file | `/etc` |
| `fd.typechar` | FD type: `f`=file, `4`=IPv4, `6`=IPv6, `u`=unix | `f` |
| `fd.sport` | Source port | `45123` |
| `fd.dport` | Destination port | `80` |
| `fd.sip` | Source IP | `10.0.1.5` |
| `fd.dip` | Destination IP | `1.2.3.4` |

**Event fields:**
| Field | Description |
|---|---|
| `evt.type` | Syscall name: `execve`, `open`, `connect`, `read`, `write`, etc. |
| `evt.dir` | Direction: `>` = entering syscall, `<` = returning from syscall |
| `evt.arg[n]` | Syscall argument by index |
| `evt.buflen` | Buffer length for read/write events |
| `evt.time` | Event timestamp |

### Macros

Macros are reusable named conditions:

```yaml
# Define a macro
- macro: container
  condition: container.id != host

- macro: spawned_process
  condition: evt.type = execve and evt.dir = <

- macro: shell_binaries
  items: [bash, sh, zsh, ksh, tcsh, csh, fish]
  
# Use in rules
- rule: Shell in Container
  condition: container and spawned_process and proc.name in (shell_binaries)
```

**Override an existing macro:**
```yaml
# Override to add your custom exceptions
- macro: never_true
  condition: (evt.num = 0)  # always false — effectively disables rules using this macro

# Override the "allowed shells" macro
- macro: user_shell_containers
  condition: k8s.pod.label[allow-shell] = "true"
```

### Lists

Lists are named arrays for use in `in` conditions:

```yaml
# Define lists
- list: shell_binaries
  items: [bash, sh, zsh, ksh, tcsh, csh, fish, dash]

- list: known_admin_containers
  items: ["ops-tooling", "debug-container"]

- list: trusted_image_repos
  items: ["gcr.io/company", "registry.company.com"]

# Use in rules
condition: >
  proc.name in (shell_binaries)
  and not container.name in (known_admin_containers)
  and not container.image.repository in (trusted_image_repos)
```

### Exceptions

Exceptions are structured ways to suppress specific false positive patterns:

```yaml
- rule: Write below root
  exceptions:
    - name: known_root_files
      fields: [proc.name, fd.name]
      comps: [=, startswith]
      values:
        - [nginx, /var/log]           # nginx writing to /var/log is OK
        - [sshd, /var/run/sshd]       # sshd writing to /var/run/sshd is OK
```

**Exception vs. condition `not`:**
- Exceptions are structured metadata (better for tooling, compliance reporting)
- `not` in condition is inline (harder to track)
- Both work; exceptions are preferred for production exception management

### Writing a Custom Rule

**Step 1: Identify the detection goal**
Example: "Detect when a container reads SSH private keys"

**Step 2: Identify the relevant syscall(s) and fields**
- Syscall: `open` (opening files for reading)
- Field: `fd.name` contains `.ssh/id_` or `fd.directory = /root/.ssh`
- Must be in a container: `container.id != host`

**Step 3: Draft the condition**
```yaml
- rule: Read SSH Private Keys in Container
  desc: A process in a container opened an SSH private key file for reading.
  condition: >
    container
    and open_read
    and (
      fd.name glob "/root/.ssh/id_*"
      or fd.name glob "/home/*/.ssh/id_*"
      or fd.name glob "/etc/ssh/ssh_host_*_key"
    )
    and not proc.name in (known_ssh_readers)
  output: >
    SSH private key read in container
    (user=%user.name container=%container.name image=%container.image.repository
     proc=%proc.name file=%fd.name cmdline=%proc.cmdline)
  priority: WARNING
  tags: [container, ssh, credentials, mitre_credential_access]
```

**Step 4: Test with dry-run**
```bash
# Test rule without running full Falco
falco --dry-run -r my-rules.yaml

# Test against a captured scap file
falco -e capture.scap -r my-rules.yaml

# Run Falco and watch for specific rule
falco -r /etc/falco/falco_rules.yaml -r my-rules.yaml 2>&1 | grep "SSH private key"
```

**Step 5: Check for noise**
```bash
# Run in dry-run / verbose mode against live traffic
falco -A -r my-rules.yaml 2>&1 | head -100
# If too many events, add more specific conditions or exceptions
```

## Default Rules Reference

Falco ships 70+ default rules in `/etc/falco/falco_rules.yaml`, covering container/process anomalies, sensitive file access, privilege escalation, Kubernetes, and network detections. See `references/default-rules.md` for the full categorized list of default rule names and what each detects.

## Falco Plugin System

Falco's plugin system extends detection beyond syscalls to other event sources:

### Plugin Architecture

```
Event Source Plugin
  ├── Provides a new event stream (e.g., AWS CloudTrail events)
  ├── Loaded by Falco as a shared library (.so)
  ├── Exposes: event fields (new fields usable in rules)
  └── Produces: events that Falco rules can evaluate against

Extractor Plugin
  ├── Adds new fields to existing event sources
  └── Does not produce events; just adds extractable fields
```

See `references/plugin-examples.md` for full AWS CloudTrail plugin setup, rule fields, and example rules, plus a Kubernetes Audit plugin example rule.

### Available Plugins

| Plugin | Event Source | Detects |
|---|---|---|
| `cloudtrail` | AWS CloudTrail | AWS API activity, IAM changes, config changes |
| `k8s_audit` | Kubernetes Audit Log | K8s API activity, RBAC changes, pod creation |
| `okta` | Okta System Log | Okta authentication, user management, SSO |
| `github` | GitHub Audit Log | Repo access, secret exposure, branch protection changes |
| `gcp_auditlog` | GCP Cloud Audit | GCP API activity |
| `azure` | Azure Activity Log | Azure ARM API activity |
| `syslog` | Syslog | Parse syslog messages as Falco events |

## Falcosidekick

Falcosidekick is a companion service that receives Falco alerts and routes them to any of 60+ output destinations.

### Architecture

```
Falco (generates alerts)
  └── JSON events to stdout or HTTP endpoint
        ↓
Falcosidekick (sidecar or separate service)
  └── Receives alerts via HTTP (Falco sends to http_output.url)
  └── Filters alerts by priority, rule, tags, etc.
  └── Routes to multiple outputs simultaneously
        ├── Slack, Teams, Discord
        ├── PagerDuty, OpsGenie, VictorOps
        ├── Elasticsearch, OpenSearch, Loki
        ├── Splunk HEC, Datadog, Dynatrace
        ├── AWS SQS, SNS, CloudWatch, Lambda
        ├── GCP Pub/Sub
        ├── Azure Event Hub, Log Analytics
        ├── Kafka
        ├── Webhook (any HTTP endpoint)
        └── falco-talon (automated response)
```

### Falcosidekick Configuration

```yaml
# values.yaml for Falcosidekick Helm chart
falcosidekick:
  config:
    # Slack integration
    slack:
      webhookurl: "https://hooks.slack.com/services/T.../B.../..."
      channel: "#security-alerts"
      footer: "Falco Runtime Security"
      icon: "https://example.com/falco-icon.png"
      minimumpriority: "warning"    # Only WARNING and above to Slack

    # PagerDuty for critical alerts
    pagerduty:
      routingkey: "your-pagerduty-routing-key"
      minimumpriority: "critical"   # Only CRITICAL+ to PagerDuty

    # Elasticsearch for all alerts
    elasticsearch:
      hostport: "https://elasticsearch:9200"
      index: "falco-events"
      minimumpriority: "debug"      # All events to Elasticsearch

    # AWS Lambda for automated response
    awslambda:
      functionname: "falco-response-function"
      minimumpriority: "critical"

    # falco-talon for automated response
    webhook:
      address: "http://falco-talon:2803"
      minimumpriority: "warning"
```

### Falcosidekick-UI

Falcosidekick includes a built-in web UI for visualizing Falco alerts:
```yaml
webui:
  enabled: true
  replicaCount: 1
  service:
    port: 2802
  # Access at http://falcosidekick-ui:2802
```

## falco-talon (Automated Response)

falco-talon is the response engine for Falco — automates actions when Falco rules fire.

### Architecture

```
Falco Rule Fires
  ↓
Falcosidekick (routes to talon via webhook)
  ↓
falco-talon
  └── Matches event to talon rules
  └── Executes action:
        ├── Kubernetes: terminate pod, label pod, add network policy, exec command
        ├── AWS: quarantine EC2 (change security group), disable IAM user, snapshot instance
        ├── GCP: quarantine GCE instance
        └── Notification: alert additional channels
```

### Talon Rule Syntax

```yaml
# talon rules file
- action: Terminate Pod
  match:
    rules:
      - name: "Terminal shell in container"
    namespaces:
      - production
      - staging
    priority:
      - CRITICAL
      - WARNING
  parameters:
    graceful_period: 5s
    ignore_daemonsets: true
    ignore_statefulsets: false

- action: Label Pod
  match:
    rules:
      - name: "Contact cloud metadata service from container"
  parameters:
    labels:
      quarantine: "true"
      reason: "imds_access_detected"
  # Then use NetworkPolicy to isolate quarantined pods:
  # podSelector: {matchLabels: {quarantine: "true"}}
  # ingress/egress: []  (deny all)

- action: AWS - Quarantine EC2 Instance
  match:
    rules:
      - name: "Outbound Connection to C2 Servers"
    priority:
      - CRITICAL
  parameters:
    # Change instance security group to an isolation group
    # (all inbound/outbound blocked except SSH for forensics)
    security_group_id: "sg-quarantine-only"
```

### Automated Response Best Practices

1. **Start with notification-only** — don't auto-terminate pods until rules are well-tuned
2. **Test in non-production** — verify rules are accurate before enabling enforcement in production
3. **Use label-based quarantine** — add a `quarantine=true` label + NetworkPolicy to isolate rather than delete (preserve forensic evidence)
4. **Require human approval for destructive actions** — use talon's approval workflow for termination
5. **Log all automated actions** — audit trail for automated responses
6. **Never auto-respond to noisy rules** — only automate responses for high-confidence, low-false-positive rules

## Performance and Tuning

Covers eBPF ring buffer sizing, event drop diagnosis, and rule-condition performance (expensive `glob`/`pmatch` conditions, macro-based filtering, priority filtering). See `references/performance-tuning.md` for full tuning configuration and examples.

## Deployment (Helm)

```bash
# Add Falco Helm repo
helm repo add falcosecurity https://falcosecurity.github.io/charts
helm repo update

# Install Falco with modern eBPF driver
helm install falco falcosecurity/falco \
  --namespace falco \
  --create-namespace \
  --set driver.kind=modern_ebpf \
  --set falcosidekick.enabled=true \
  --set falcosidekick.webui.enabled=true \
  --set collectors.kubernetes.enabled=true  # K8s metadata enrichment

# Verify Falco is running
kubectl get pods -n falco
kubectl logs -n falco ds/falco | grep "Falco initialized"
```

## Reference Files

Load these when you need deep architectural knowledge:

- `references/architecture.md` -- Falco kernel architecture: eBPF probe design, ring buffer mechanics, Falco rule evaluation pipeline, plugin framework internals, Falcosidekick routing logic, falco-talon response engine, kernel driver compatibility matrix.
- `references/default-rules.md` -- Full categorized list of Falco's 70+ default rules (container/process, sensitive file access, privilege escalation, Kubernetes, network).
- `references/plugin-examples.md` -- AWS CloudTrail plugin setup, rule fields, and example rules; Kubernetes Audit plugin example rule.
- `references/performance-tuning.md` -- eBPF ring buffer tuning, event drop diagnosis, and rule condition performance optimization.
