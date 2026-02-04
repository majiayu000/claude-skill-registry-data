---
name: docker-management
description: Docker container and image management including logs, stats, and compose operations. Use when managing Docker containers, debugging container issues, or working with Docker Compose.
allowed-tools: Bash, Read, Write
mcp_tools:
  - "docker_ps"
  - "docker_images"
  - "docker_logs"
  - "docker_inspect"
  - "docker_stats"
  - "docker_exec"
  - "docker_start"
  - "docker_stop"
  - "docker_restart"
  - "docker_rm"
  - "compose_ps"
  - "compose_logs"
  - "compose_up"
  - "compose_down"
---

# Docker Management Skill

**Version**: 1.0.0
**Purpose**: Docker container and compose management

---

## Triggers

| Trigger | Examples |
|---------|----------|
| Containers | "list containers", "docker ps", "コンテナ一覧" |
| Logs | "container logs", "docker logs", "ログ確認" |
| Debug | "debug container", "container issue", "デバッグ" |
| Compose | "compose up", "compose status", "Compose起動" |

---

## Integrated MCP Tools

### Container Operations

| Tool | Purpose |
|------|---------|
| `docker_ps` | List containers (running/all) |
| `docker_images` | List local images |
| `docker_logs` | Container logs (tail, follow) |
| `docker_inspect` | Container details (JSON) |
| `docker_stats` | Resource usage (CPU, memory) |
| `docker_exec` | Execute command in container |
| `docker_start` | Start stopped container |
| `docker_stop` | Stop running container |
| `docker_restart` | Restart container |
| `docker_rm` | Remove container |

### Compose Operations

| Tool | Purpose |
|------|---------|
| `compose_ps` | Compose project status |
| `compose_logs` | Service logs |
| `compose_up` | Start services |
| `compose_down` | Stop and remove services |

---

## Workflow: Container Debugging

### Phase 1: Assessment

#### Step 1.1: List Containers
```
Use docker_ps with:
- all: true (include stopped)
```

#### Step 1.2: Check Status
Look for:
- Exit codes
- Restart counts
- Health status

### Phase 2: Investigation

#### Step 2.1: View Logs
```
Use docker_logs with:
- container: Container name/ID
- tail: 100 (last N lines)
- timestamps: true
```

#### Step 2.2: Inspect Configuration
```
Use docker_inspect to check:
- Environment variables
- Mount points
- Network settings
- Health check config
```

#### Step 2.3: Resource Usage
```
Use docker_stats to monitor:
- CPU percentage
- Memory usage
- Network I/O
- Block I/O
```

### Phase 3: Resolution

#### Step 3.1: Restart Container
```
Use docker_restart for temporary fix
```

#### Step 3.2: Execute Commands
```
Use docker_exec to run diagnostics inside container:
- command: "sh -c 'ps aux'"
- command: "cat /var/log/app.log"
```

---

## Workflow: Docker Compose

### Step 1: Check Status
```
Use compose_ps to see all services
```

### Step 2: View Logs
```
Use compose_logs with:
- service: Specific service name
- tail: 50
```

### Step 3: Service Management
```
Use compose_up to start services
Use compose_down to stop and clean up
```

---

## Common Issues

| Symptom | Tool | Action |
|---------|------|--------|
| Container exits | docker_logs | Check error messages |
| High memory | docker_stats | Identify memory leak |
| Network issues | docker_inspect | Verify network config |
| Mount failures | docker_inspect | Check volume mounts |

---

## Best Practices

✅ GOOD:
- Check logs before restarting
- Use health checks
- Set resource limits
- Use named volumes

❌ BAD:
- Restart without investigation
- Run as root unnecessarily
- Store secrets in images
- Use latest tag in production

---

## Checklist

- [ ] Docker daemon running
- [ ] Container status checked
- [ ] Logs reviewed
- [ ] Resource usage normal
- [ ] Network connectivity OK
