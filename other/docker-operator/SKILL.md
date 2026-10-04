---
name: docker-operator
description: Docker container read-only operations for inspection and monitoring
activation_keywords: [docker, container, image, volume, network, compose]
---

# Docker Operator Skill

Provides read-only Docker operations:
- List containers, images, volumes, networks
- Inspect container details and logs
- Check resource usage and status
- View Docker system information

Use `builtin_docker_operator` tool with fields:
- `operation`: one of "ps", "images", "logs", "inspect", "stats", "network", "volume"
- `name`: (optional) specific container/image/network/volume name
- `all`: (optional) include stopped containers (default: false)

Note: Write operations (run, stop, rm, kill, build) are disabled by default for safety.
