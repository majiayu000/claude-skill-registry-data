---
name: ls-docker-build-compose
description: Guide Docker and Podman builds, Compose, rootless containers, runtime management,
  networking, storage, secrets, and troubleshooting. Preserve the selected engine and endpoint;
  do not escalate rootless failures or manage host installations implicitly.
metadata:
  version: '1.1'
---

# Docker and Podman containers

Use this skill for Dockerfiles, Containerfiles, Compose projects, container builds,
operation, and LocalSetup installations inside containers. The published skill name
and existing aliases remain compatible.

## Select the existing context

Inspect the repository, project instructions, engine configuration and endpoint first.
Dockerfile and Containerfile (including named variants), `compose.yaml`, `compose.yml`,
and `docker-compose` YAML variants identify container work; they do not select an engine.
Preserve an explicitly configured Docker or Podman engine, remote endpoint, and privilege
mode. For a newly selected Podman workflow, default to rootless. Retain explicitly
selected rootful operation. Do not substitute engines, add sudo, mount a host socket,
or enable privileged containers to work around a rootless failure.

Record the effective context using `docker context show` and `docker info`, or
`podman system connection list` and `podman info`, as appropriate. Inspect only needed
fields; full inspection output can contain private paths and configuration. Verify
rootless operation from the selected engine's reported security mode, not just the
UID of the client process. A non-root Docker client can control a rootful daemon.

## Qualify rootless operation

Before changing host configuration, diagnose the selected environment:

- Check user namespace availability and `newuidmap`/`newgidmap`, subordinate UID/GID
  mappings, and the engine's actual rootless mode. Docker requires at least 65,536
  subordinate UIDs and GIDs. Inspect mappings inside a disposable container too.
- Verify writable home, runtime directory, engine storage and persistent application
  state. Resolve paths inside the container; never infer a host home from a mount.
- Check bind-mount ownership and permissions for the mapped container UID. Prefer
  purpose-built volumes or deliberate user mappings. Do not recursively chown a host
  directory. Podman's `:U` changes source ownership and needs an explicit scope decision.
- Inspect the actual storage driver and backing filesystem. Follow engine diagnostics
  for overlay or FUSE support; do not silently replace the configured storage root.
- Qualify rootless networking, DNS, published ports and host reachability with a small
  disposable workload. Port binding and networking capabilities differ by engine.
- On SELinux systems, inspect labels and choose an appropriate scoped `:z` or `:Z`
  mount only when intended; never relabel system or home trees or disable enforcement.

A failed prerequisite is a concrete blocker. Provide the scoped remedy without
changing the privilege mode. Host installation or privileged repair follows the
existing sudo workflow and the user's authorization.

## Build and operate

Inspect the base image, build context, ignore file, multi-stage build, dependency
cache, runtime user, exposed ports, volumes, health checks, and signal handling.
Use the project's package manager and existing validation commands. Keep secrets
out of image layers, build args, logs and committed Compose files; use the selected
engine's supported build-secret or runtime-secret mechanism and verify provider support.

Build with the selected engine and explicit file/context. Inspect and start the
result in a disposable container, test readiness, logs, networking and persistent
storage, then stop and remove only task-owned resources. Check non-root application
execution, clean shutdown, rebuild determinism and image size. Rootless engine mode
and non-root application user are separate properties; verify both where required.

For Compose, identify the actual installed provider and version before relying on
features. `podman compose` delegates to an external provider; inspect
`PODMAN_COMPOSE_PROVIDER`, `containers.conf`, and `podman compose --help` rather than
assuming Docker Compose semantics. Use `docker compose version` for the selected
Docker plugin. Validate configuration without printing resolved secrets, then test
build/start/readiness/stop with the selected provider. Preserve its project name,
endpoint and privilege mode.

## LocalSetup inside a container

Use the normal installer, self-refresh, doctor, and package discovery commands in
an isolated container home. Keep the selected LocalSetup data/package root, adapter
records, resolver manifest and project attachment state writable and persistent where
recreation must retain them. Resolve package links in the container namespace; portable
adapters must not contain host paths. Bind only the intended test source read-only;
use a disposable writable project attachment and home rather than the host home.

Run install and a repeated upgrade in both symlink and portable modes, query canonical
packages through the recorded client integration, and run doctor. Recreate the container
with the same state volume and verify discovery, ownership and idempotent refresh again.
For a read-only image installation, rebuild the image with the updated packages, or
configure writable persistent state for this selected installation. Do not repair the
host installation or remount the image writable implicitly.

Actual Docker, rootless Docker, and rootless Podman runs are required when claiming
cross-engine container acceptance. Mocked tests cannot establish runtime compatibility.
Record an unavailable runtime as a validation blocker; never substitute a rootful run.

## Troubleshooting and boundaries

Separate engine/endpoint connectivity, user mappings, mount permissions, networking,
storage, Compose provider errors, and application failures. Preserve failed-container
logs privately after removing secrets. Give one scoped next step based on the evidence.
Inspect the target repository before edits and preserve its established patterns.
Do not expose credentials, private paths, or production identifiers in public output.
Verify changing vendor behavior against official sources before relying on it.

## References and provenance

- [Podman operation and rootless requirements](https://docs.podman.io/en/latest/markdown/podman.1.html)
- [Podman Compose provider contract](https://docs.podman.io/en/latest/markdown/podman-compose.1.html)
- [Docker rootless operation](https://docs.docker.com/engine/security/rootless/)

Source classification: `official-docs-reference`. This LocalSetup-native skill follows
project workflow requirements and official documentation; no third-party text is copied.
