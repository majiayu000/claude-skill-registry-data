---
name: docker-cleanup
description: Use when Charlie asks to free local Docker or OrbStack disk, remove unused containers, images, volumes, networks, or build cache, or diagnose recurring Docker disk growth.
---

# Docker cleanup

Use the global `docker-cleanup` command. Its `--help` output owns the exact flags.

1. Run `docker-cleanup --dry-run` and identify any active build or protected named volume.
2. If a Docker build is active, wait for it to finish or report it. Do not start another prune.
3. Run `docker-cleanup` for the normal cleanup. It preserves running containers and unused named volumes, and limits BuildKit cache growth.
4. Use `docker-cleanup --all-volumes` only after Charlie explicitly approves deleting every unused named volume. An unused named volume may contain a stopped database.
5. Verify the command's final resource counts and disk free space.

If Docker or OrbStack is unhealthy, inspect the daemon before retrying. Do not repeat an unchanged prune command after a timeout or an “already running” response. Restart the daemon only after checking active builds and development stacks.
