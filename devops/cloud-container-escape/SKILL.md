---
name: cloud-container-escape
description: >
  Break out of a container to the host. Load when you have a shell in a container/pod and want
  the node: privileged container, mounted docker.sock, dangerous capabilities, hostPath, or
  "escape the container". Signals: /.dockerenv, cgroup shows docker/k8s, CAP_SYS_ADMIN, mounted socket.
domain: cloud
type: technique
stability: learning
modes: [pentest, bugbounty]
severity: critical
cwe: [CWE-269]
mitre: [T1611]
tools: [amicontained, deepce]
schema_version: 1
---

# Container escape → host

## When it applies
You have code execution inside a container and want the underlying host (and from there, other
containers / the cluster / cloud creds).

## Why it works
Containers are isolation by configuration, not a hard boundary. Privileged mode, extra
capabilities, mounted host resources, or an exposed Docker socket give processes inside the
container direct control over the host kernel/daemon.

## Method
1. **Confirm & enumerate**: `/.dockerenv`, `/proc/1/cgroup`; run `amicontained`/`deepce` to list
   capabilities, seccomp, and mounts.
2. **Exploit the misconfig**:
   - **Docker socket mounted** (`/var/run/docker.sock`): `docker -H unix://... run -v /:/host ...`
     → mount host FS as root → escape.
   - **Privileged / CAP_SYS_ADMIN**: mount the host disk, or use the classic `release_agent`
     cgroup notify_on_release trick to run a command on the host.
   - **hostPath / host mounts**: write to host filesystem (cron, ssh keys, kubelet config).
   - **hostPID**: access host processes; `nsenter` into PID 1's namespaces.
3. **From the host**: grab cloud metadata creds (→ `cloud-imds-ssrf`), pivot to other
   containers/nodes (→ `cloud-kubernetes`).

## Gotchas
- Enumerate capabilities/mounts first — the escape depends entirely on which misconfig exists.
- Kernel-exploit escapes are last-resort and risky on live targets; prefer the config-based paths.
- On bug bounty, a proven mount of the host FS is enough — don't disrupt the node.

## Verify success
Command execution or file read/write on the host (outside the container namespace) — e.g. host
`/etc/shadow`, other containers, or the kubelet/cloud creds.

## References
`deepce`/`amicontained`; "Understanding Docker container escapes" (Trail of Bits); HackTricks.
