---
name: docker-audit
description: Container and Docker security auditing.
version: 1.1.0
author: Rakshastra Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  rakshastra:
    tags: [security, container, docker, auditing, compliance]
    related_skills: [linux-audit, compliance-check]
---

# Docker and Container Security Auditing

## Overview
This skill outlines how to audit Docker containers, daemon configurations, and container images for misconfigurations and vulnerabilities.

## Methodology (9-Phase Sequence)
1. **Recon**: Map host container deployment, identifying running docker daemons and container platforms. Log components using `security_inventory`.
2. **Enumeration**: Enumerate running containers, exposed ports on containers, and image tags.
3. **Collection**: Retrieve `/etc/docker/daemon.json`, docker service configuration files, and `docker inspect` outputs.
4. **Evidence**: Validate and record misconfigurations (e.g. `--privileged` flag, sockets mapped to host) as Evidence via `security_evidence`.
5. **Analysis**: Query Trivy/Grype CVE vulnerability data. Build service-to-container-to-host relations inside the InfrastructureGraph.
6. **Prioritization**: Execute `security_risk` to prioritize image and daemon exposures based on criticality and exploitability factors.
7. **Recommendation**: Write specific mitigation directives, such as docker run adjustments, daemon config patches, or image rebuild playbooks.
8. **Verification**: Restart container with updated flags and re-inspect to confirm vulnerabilities or privileged mounts are resolved.
9. **Report**: Compile container vulnerability status, graph relations, and mitigation proofs in a final report via `security_report`.

## Commands Reference
- `docker info` (Daemon details)
- `docker ps --filter "status=running"` (List active containers)
- `docker inspect <container_id> --format '{{.HostConfig.Privileged}}'` (Check privileged mode)
- `docker inspect <container_id> --format '{{.HostConfig.Binds}}'` (Check mounted volumes)
- `trivy image <image_name>` (Scan image for vulnerabilities)
