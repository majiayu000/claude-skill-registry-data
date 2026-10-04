---
name: docker-cli
description: Helper for using the Docker CLI to build, run, stop, inspect, and manage containers and images. Use when the user wants to perform container-related tasks from the command line, such as building images, running services, cleaning up resources, or checking logs.
---

# Docker CLI Helper

This skill explains how to use the **Docker command line** for common container workflows.

## When to Use

Use this skill when:

- The user wants to build or rebuild a Docker image.
- The user wants to run a container (one-off or long-running).
- The user wants to see which containers/images/volumes exist.
- The user wants to stop or remove containers/images.
- The user wants to see logs, exec into a container, or check resource usage.

## Requirements

- Docker is installed and running.
- `docker version` or `docker info` works in the user’s shell.

If unsure, suggest the user run:

```bash
docker version
```

to confirm Docker is available.

## Safety Guidelines

- Prefer **read-only** or non-destructive commands first:
  - `docker ps`, `docker ps -a`
  - `docker images`
  - `docker logs`
  - `docker inspect`
- Be cautious with destructive commands:
  - `docker rm`, `docker rmi`
  - `docker system prune`
  - `docker volume rm`
- Only recommend destructive cleanups when the user explicitly wants to free resources and understands what will be removed.

## Common Workflows

### 1. List and inspect containers

List running containers:

```bash
docker ps
```

List all containers (including stopped):

```bash
docker ps -a
```

Inspect a container in detail:

```bash
docker inspect <container-id-or-name>
```

### 2. List and inspect images

List local images:

```bash
docker images
```

Inspect an image:

```bash
docker inspect <image-id-or-name>
```

### 3. Build images

Build an image from a `Dockerfile` in the current directory:

```bash
docker build -t <image-name>:<tag> .
```

Example:

```bash
docker build -t my-app:latest .
```

If the `Dockerfile` is in another directory:

```bash
docker build -t my-app:latest path/to/context
```

### 4. Run containers

Run a container in the foreground:

```bash
docker run --rm -it <image-name>:<tag>
```

Run in detached mode (background service):

```bash
docker run -d --name <container-name> <image-name>:<tag>
```

Map ports from container to host:

```bash
docker run -d --name <container-name> -p 8080:80 <image-name>:<tag>
```

Mount a host directory into the container:

```bash
docker run -d --name <container-name> -v /host/path:/container/path <image-name>:<tag>
```

### 5. Stop and remove containers

Stop a running container:

```bash
docker stop <container-id-or-name>
```

Remove a stopped container:

```bash
docker rm <container-id-or-name>
```

Stop and remove in one shot (two commands):

```bash
docker stop <container-id-or-name>
docker rm <container-id-or-name>
```

### 6. Remove images

Remove an image by ID or name:

```bash
docker rmi <image-id-or-name>
```

Only suggest this when the user is sure the image is no longer needed.

### 7. Logs and exec

See logs for a container:

```bash
docker logs <container-id-or-name>
```

Stream logs (follow):

```bash
docker logs -f <container-id-or-name>
```

Execute a shell inside a running container (if it has `/bin/bash`):

```bash
docker exec -it <container-id-or-name> /bin/bash
```

or with `/bin/sh`:

```bash
docker exec -it <container-id-or-name> /bin/sh
```

### 8. Clean up resources

Only suggest these when the user explicitly wants cleanup:

- Remove all stopped containers:

```bash
docker container prune
```

- Remove unused images:

```bash
docker image prune
```

- Remove everything unused (containers, networks, images, and optionally volumes):

```bash
docker system prune
```

For a more aggressive cleanup, but only if the user confirms:

```bash
docker system prune -a
```

## Troubleshooting Tips

- If images cannot be pulled, check:
  - Network connectivity.
  - Registry authentication (if using a private registry).
- If ports are already in use, suggest:
  - Changing the host port in `-p host:container`.
  - Or stopping the process that currently uses the port.
- If a container keeps exiting immediately:
  - Suggest checking `docker logs <container>` for errors.
  - Inspect entrypoint and command configuration.

