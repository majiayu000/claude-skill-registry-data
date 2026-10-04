---
name: selinux
description: "SELinux on Red Hat Enterprise Linux across RHEL 8, 9, 10: Mandatory Access Control, type enforcement, security contexts, booleans, file and port context management, custom policy modules, container SELinux integration, and AVC troubleshooting. Use when: \"SELinux\", \"selinux\", \"AVC\", \"audit2why\", \"sealert\", \"semanage\", \"restorecon\", \"security context\", \"type enforcement\", \"boolean\", \"selinux denial\", \"selinux troubleshoot\". Do NOT use for general RHEL administration — use the `rhel` skill. Do NOT use for AppArmor on Debian/Ubuntu — use the `apparmor` skill."
license: MIT
---

# SELinux (RHEL)

This skill covers SELinux on Red Hat Enterprise Linux across RHEL 8, 9, and 10. It provides deep knowledge of:

- Mandatory Access Control (MAC) framework and its relationship to DAC
- Type Enforcement (TE) architecture: domains, types, allow rules, transitions
- SELinux modes (enforcing, permissive, disabled) and per-domain permissive mode
- Security contexts (user:role:type:level) for processes, files, ports, and users
- Policy types (targeted, MLS, minimum) and policy module management
- Boolean management for enabling/disabling policy features without custom modules
- File context management with semanage fcontext and restorecon
- Port context management with semanage port
- Custom policy module development (.te, .fc, .if files and audit2allow workflows)
- Container SELinux integration (container-selinux, MCS isolation, :Z/:z volume labels, udica)
- MLS/MCS for multi-level and multi-category security including container isolation
- AVC denial analysis, audit2why, sealert, and systematic troubleshooting

When a question is version-specific, note the relevant version differences. When the version is unknown, provide general guidance and flag where behavior varies. For general RHEL administration, see the `rhel` skill.

## How to Approach Tasks

Route by request type: **troubleshooting** → `references/diagnostics.md`; **architecture** → `references/architecture.md`; **best practices/config** → `references/best-practices.md`; **health check** → the diagnostic scripts; **policy development** → `references/best-practices.md`.

**Identify the RHEL version first** — available tooling shifts by version (CIL output requires RHEL 9+, Quadlet container integration requires RHEL 9.2+). Reason from the source domain, target type, object class, and permissions — not generic Linux security advice. Prefer the least-privilege fix: boolean > fcontext > port > custom module. Validate with `ausearch`, `sealert`, a `restorecon -Rvn` dry run, and `getenforce` confirmation.

## Core Expertise

### Mandatory Access Control (MAC)

SELinux implements MAC as a kernel-level enforcement mechanism layered on top of traditional UNIX DAC. Both must allow an access for it to succeed. The decision order is: DAC check first, then SELinux MAC check. Even root is subject to MAC rules.

SELinux registers with the Linux Security Modules (LSM) framework at boot time. The security server loads the compiled binary policy and evaluates access requests through LSM hooks at key kernel operations: file access, socket operations, process creation, IPC, and mount operations.

The Access Vector Cache (AVC) stores results of recent security decisions for performance. Cache misses generate audit messages. Denials are logged as AVC messages in `/var/log/audit/audit.log`.

### Type Enforcement

Type Enforcement is the primary access control mechanism in SELinux targeted policy.

- **Domain**: the security type assigned to a process (e.g., `httpd_t`, `sshd_t`)
- **Type**: the security type assigned to a file or object (e.g., `httpd_sys_content_t`, `shadow_t`)

Access is controlled by allow rules:
```
allow source_domain target_type : object_class { permissions };
```

Type transitions control automatic domain changes when a process executes a binary. When `init_t` executes `/usr/sbin/httpd` (labeled `httpd_exec_t`), the new process transitions to `httpd_t`.

Dontaudit rules suppress logging for known-harmless denials. To temporarily reveal hidden denials:
```bash
semodule -DB   # Disable dontaudit rules
# ... investigate ...
semodule -B    # Re-enable dontaudit rules
```

### Security Contexts

Format: `user:role:type:level`

- **user**: SELinux user (`system_u`, `unconfined_u`, `staff_u`, `user_u`)
- **role**: RBAC role (`system_r`, `object_r`, `user_r`, `sysadm_r`)
- **type**: The domain or type (primary enforcement mechanism)
- **level**: MLS/MCS sensitivity and categories (`s0`, `s0:c1,c2`)

Inspect contexts:
```bash
ps auxZ                    # Process contexts
ls -Z /path/to/file        # File contexts
id -Z                      # Current user context
semanage port -l           # Port contexts
```

### SELinux Modes

| Mode | Behavior | Use Case |
|---|---|---|
| Enforcing | Policy enforced, denials blocked and logged | Production |
| Permissive | Policy evaluated, denials logged but not blocked | Troubleshooting |
| Disabled | SELinux inactive, no labeling or enforcement | Not recommended |

Persistent configuration: `/etc/selinux/config`

Per-domain permissive mode confines a single domain to permissive while the rest of the system enforces. Invaluable for troubleshooting one service without weakening the entire system:
```bash
semanage permissive -a httpd_t    # Put httpd_t in permissive
semanage permissive -d httpd_t    # Remove from permissive
```

### Boolean Management

Booleans are pre-defined on/off switches that enable or disable specific policy rules without custom modules. They are the preferred first-line mechanism for adjusting SELinux policy.

```bash
getsebool -a | grep httpd              # List booleans for a service
setsebool -P httpd_can_network_connect on  # Set persistently
semanage boolean -l | awk '$3 != $4'   # Show changed booleans
```

Common booleans by service:
- **httpd**: `httpd_can_network_connect`, `httpd_can_network_connect_db`, `httpd_use_nfs`, `httpd_enable_homedirs`
- **samba**: `samba_enable_home_dirs`, `samba_export_all_rw`, `samba_share_nfs`
- **nfs**: `use_nfs_home_dirs`, `use_samba_home_dirs`
- **containers**: `container_manage_cgroup`, `virt_use_nfs`

### File Context Management

SELinux maintains a file context database mapping path patterns to security contexts. Custom rules are added with `semanage fcontext` and applied with `restorecon`.

```bash
# Add context rule for custom web root
semanage fcontext -a -t httpd_sys_content_t "/srv/www(/.*)?"
restorecon -Rv /srv/www/

# Equivalence rule for relocated data
semanage fcontext -a -e /var/lib/pgsql /data/pgsql
restorecon -Rv /data/pgsql/

# Verify expected context
matchpathcon -V /var/www/html/index.html
```

Important: `chcon` makes temporary changes that are lost on relabel. Always use `semanage fcontext` + `restorecon` for persistent changes.

### Port Context Management

Services binding to non-standard ports require SELinux port labels:

```bash
semanage port -l | grep http_port_t    # Check existing labels
semanage port -a -t http_port_t -p tcp 8181  # Add port label
```

### Container SELinux

The `container-selinux` package provides the `container_t` domain for container processes. MCS categories automatically isolate containers from each other -- each container receives a unique category pair.

Volume mount labels:
- `:Z` -- Private label (relabel for this container only)
- `:z` -- Shared label (relabel for shared access across containers)

WARNING: Never use `:Z` on system directories (`/home`, `/etc`, `/var`).

For complex container policies, use `udica` to generate least-privilege SELinux modules:
```bash
podman inspect mycontainer | udica mypolicy
semodule -i mypolicy.cil /usr/share/udica/templates/*.cil
```

### Custom Policy Modules

When no boolean, file context, or port label covers the required access:

1. Put the domain in per-domain permissive: `semanage permissive -a myapp_t`
2. Reproduce the denied operations
3. Collect denials: `ausearch -m AVC -c myapp | audit2allow`
4. Generate module: `ausearch -m AVC -c myapp | audit2allow -M mypolicy`
5. **Review** the generated `.te` file before installing
6. Install: `semodule -i mypolicy.pp`
7. Remove permissive: `semanage permissive -d myapp_t`

Module file types: `.te` (type enforcement rules), `.fc` (file contexts), `.if` (interfaces), `.pp` (compiled package).

Module priorities: 100 (base), 200 (contrib), 300 (local), 400 (custom overrides).

## Troubleshooting Decision Tree

```
1. Confirm SELinux is causing the issue
   +-- getenforce --> is it Enforcing?
   +-- setenforce 0 --> does the problem go away?
   +-- setenforce 1 --> re-enable immediately after confirming

2. Find AVC denials
   +-- ausearch -m AVC -ts recent
   +-- sealert -a /var/log/audit/audit.log
   +-- journalctl -t setroubleshoot

3. Understand the denial
   +-- ausearch -m AVC -ts recent | audit2why
   +-- Identify: scontext (who), tcontext (what), tclass (class), perms

4. Determine the fix (least privilege first)
   |
   +-- Wrong file context?
   |   +-- semanage fcontext -a -t <type> "/path(/.*)?"
   |   +-- restorecon -Rv /path/
   |
   +-- Boolean available?
   |   +-- semanage boolean -l | grep <service>
   |   +-- setsebool -P <boolean> on
   |
   +-- Non-standard port?
   |   +-- semanage port -a -t <type> -p tcp <port>
   |
   +-- Container volume issue?
   |   +-- Add :Z or :z to volume mount
   |
   +-- None of the above?
       +-- Per-domain permissive + audit2allow module

5. Test the fix
   +-- Restart the affected service
   +-- Verify no new denials: ausearch -m AVC -ts recent

6. Confirm enforcing mode
   +-- getenforce --> must show Enforcing
```

## Version-Specific Changes

| Feature | RHEL 8 | RHEL 9 | RHEL 10 |
|---|---|---|---|
| Policy store location | `/var/lib/selinux/` | Same | Same |
| udica (container policy) | Introduced (8.1) | Improved | Enhanced auto-labeling |
| container-selinux MCS | Full MCS isolation default | Improved transitions | Improved rootless confinement |
| audit2allow CIL output | Not available | `--cil` flag added | CIL-first recommended |
| setroubleshoot accuracy | Baseline | Improved pattern matching | Further improvements |
| selinux-policy-doc man pages | Available | Expanded | Expanded |
| AVC cache performance | Baseline | ~5% overhead reduction | Further optimization |
| Per-service confinement | Expanded (cockpit, sssd) | keylime, grafana, IPA | More services confined |
| Policy development tools | audit2allow, sepolicy | CIL tooling | sepolicy generate improved |
| Confined user improvements | Baseline | staff_u/sysadm_r improved | Further expansion |
| Audit filtering | Standard | Standard | Granular AVC filters |

### RHEL 8 Highlights

- Full MCS isolation for containers became default and well-tested
- `udica` introduced in RHEL 8.1 for custom container SELinux policies
- Targeted policy expanded to confine more system services (cockpit, sssd)
- `semanage` gained `--noheading` and `-C` (customizations only) flags
- Policy store moved to `/var/lib/selinux/` with `/etc/selinux/` for configuration

### RHEL 9 Highlights

- AVC cache optimized for lower overhead on high-throughput workloads
- `audit2allow --cil` generates native CIL policy (smaller, cleaner than .te macros)
- New confined domains: `keylime_t`, `grafana_t`, improved `podman_t`/`container_t`
- `selinux-policy-doc` package provides per-service man pages (`man httpd_selinux`)
- Improved `setroubleshoot` with better fix suggestions for container and NFS scenarios
- Improved `staff_u` and `sysadm_r` configurations for user confinement

### RHEL 10 Highlights

- CIL-first policy approach: `semodule` prefers CIL input, `audit2allow --cil` is recommended
- Improved `container_t` policy aligned with Podman 5.x model
- Better automatic label management for container volumes in common scenarios
- Enhanced `sepolicy` tooling for generating policy scaffolds
- Granular AVC audit filtering to reduce log noise in high-volume environments
- Continued expansion of confined domains, reducing the unconfined attack surface

## Common Pitfalls

**1. Using `setenforce 0` and forgetting to re-enable**
Permissive mode opens the entire system. Prefer per-domain permissive (`semanage permissive -a <domain>`) for targeted troubleshooting.

**2. Using `chcon` instead of `semanage fcontext` + `restorecon`**
`chcon` changes are temporary and lost during filesystem relabel. Always make persistent changes through the policy database.

**3. Blindly running `audit2allow -a | semodule`**
This generates allow rules for all denials on the system, potentially creating an overly permissive policy. Always filter to the specific domain and review the generated rules.

**4. Using `:Z` on system directories**
Relabeling `/home`, `/etc`, or `/var` with container-private labels breaks system services. Use dedicated directories for container bind mounts.

**5. Disabling SELinux after encountering issues**
Disabling SELinux removes all labels. Re-enabling requires a full filesystem relabel (`touch /.autorelabel && reboot`). Fix the specific issue instead.

## Reference Files

Load these when you need deep knowledge for a specific area:

- `references/architecture.md` -- MAC framework, type enforcement, MLS/MCS, modes, policy types, security contexts. Read for "how does X work" questions.
- `references/diagnostics.md` -- AVC analysis, audit2why, sealert, troubleshooting workflows, common issues and fixes. Read when troubleshooting.
- `references/best-practices.md` -- semanage workflows, boolean management, custom modules, container SELinux, file context management. Read for configuration and policy development.

## Diagnostic Scripts

Run these for rapid SELinux assessment:

| Script | Purpose |
|---|---|
| `scripts/01-selinux-status.sh` | Mode, policy, modules, changed booleans, AVC counts |
| `scripts/02-avc-analysis.sh` | Recent denials, audit2why, top denied domains/types, suggested fixes |
| `scripts/03-context-audit.sh` | Processes in wrong domains, files with wrong contexts, custom port labels |
| `scripts/04-policy-modules.sh` | Custom modules, changed booleans, recent policy changes |

## Key Paths and Files

| Path | Purpose |
|---|---|
| `/etc/selinux/config` | Mode and policy type configuration |
| `/var/log/audit/audit.log` | AVC denials and audit events |
| `/var/log/messages` | setroubleshoot human-readable summaries |
| `/etc/selinux/targeted/contexts/files/file_contexts` | Base file context database |
| `/etc/selinux/targeted/contexts/files/file_contexts.local` | Local fcontext overrides |
| `/sys/fs/selinux/` | Live SELinux kernel interface |
| `/var/lib/selinux/targeted/active/` | Active policy module store |

## Key Commands Quick Reference

```bash
# Status
getenforce                              # Current mode
sestatus                                # Full status summary

# Denials
ausearch -m AVC -ts recent              # Recent AVC denials
ausearch -m AVC -ts recent | audit2why  # Explain denials
sealert -a /var/log/audit/audit.log     # Human-readable analysis

# File contexts
semanage fcontext -a -t TYPE "/path(/.*)?"
restorecon -Rv /path/

# Ports
semanage port -a -t TYPE -p tcp PORT

# Booleans
setsebool -P BOOLEAN on

# Policy modules
ausearch -m AVC -c APP | audit2allow -M myfix
semodule -i myfix.pp

# Per-domain permissive
semanage permissive -a DOMAIN
semanage permissive -d DOMAIN
```
