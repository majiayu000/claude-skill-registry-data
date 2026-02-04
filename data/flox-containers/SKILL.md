---
name: flox-containers
description: Containerizing Flox environments with Docker/Podman. Use for creating container images, OCI exports, multi-stage builds, and deployment workflows.
---

# Flox Containerization Guide

## Core Commands

```bash
flox containerize                          # Export to default tar file
flox containerize -f ./mycontainer.tar     # Export to specific file
flox containerize --runtime docker         # Export directly to Docker
flox containerize --runtime podman         # Export directly to Podman
flox containerize -f - | docker load       # Pipe to Docker
flox containerize --tag v1.0               # Tag container image
flox containerize -r owner/env             # Containerize remote environment
```

## Basic Usage

### Export to File

```bash
# Export to file
flox containerize -f ./mycontainer.tar
docker load -i ./mycontainer.tar

# Or use default filename: {name}-container.tar
flox containerize
docker load -i myenv-container.tar
```

### Export Directly to Runtime

```bash
# Auto-detects docker or podman
flox containerize --runtime docker

# Explicit runtime selection
flox containerize --runtime podman
```

### Pipe to Stdout

```bash
# Pipe directly to Docker
flox containerize -f - | docker load

# With tagging
flox containerize --tag v1.0 -f - | docker load
```

## How Containers Behave

**Containers activate the Flox environment on startup** (like `flox activate`):

- **Interactive**: `docker run -it <image>` → Bash shell with environment activated
- **Non-interactive**: `docker run <image> <cmd>` → Runs command with environment activated (like `flox activate -- <cmd>`)
- All packages, variables, and hooks are available inside the container

**Note**: Flox sets an entrypoint that activates the environment, then runs `cmd` inside that activation.

## Command Options

```bash
flox containerize
  [-f <file>]           # Output file (- for stdout); defaults to {name}-container.tar
  [--runtime <runtime>] # docker/podman (auto-detects if not specified)
  [--tag <tag>]         # Container tag (e.g., v1.0, latest)
  [-d <path>]           # Path to .flox/ directory
  [-r <owner/name>]     # Remote environment from FloxHub
```

## Manifest Configuration

Configure container in `[containerize.config]` (experimental):

```toml
[containerize.config]
user = "appuser"                    # Username or uid:gid format
exposed-ports = ["8080/tcp"]        # Ports to expose (tcp/udp/default:tcp)
cmd = ["python", "app.py"]          # Command to run (receives activated env)
volumes = ["/data", "/config"]      # Mount points for persistent data
working-dir = "/app"                # Working directory
labels = { version = "1.0" }        # Arbitrary metadata
stop-signal = "SIGTERM"             # Signal to stop container
```

### Configuration Options Explained

**user**: Run container as specific user
- Username: `user = "appuser"`
- UID:GID: `user = "1000:1000"`

**exposed-ports**: Network ports to expose
- TCP: `["8080/tcp"]`
- UDP: `["8125/udp"]`
- Default protocol is tcp: `["8080"]` = `["8080/tcp"]`

**cmd**: Command to run in container
- Array form: `cmd = ["python", "app.py"]`
- Empty for service-based: `cmd = []`

**volumes**: Mount points for persistent data
- List paths: `volumes = ["/data", "/config", "/logs"]`

**working-dir**: Initial working directory
- Absolute path: `working-dir = "/app"`

**labels**: Arbitrary metadata
- Key-value pairs: `labels = { version = "1.0", env = "production" }`

**stop-signal**: Signal to stop container
- Common: `"SIGTERM"`, `"SIGINT"`, `"SIGKILL"`

## Complete Workflow Examples

### Flask Web Application

```bash
# Create environment
flox init
flox install python311 flask

# Configure for container
cat >> .flox/env/manifest.toml << 'EOF'
[containerize.config]
exposed-ports = ["5000/tcp"]
cmd = ["python", "-m", "flask", "run", "--host=0.0.0.0"]
working-dir = "/app"
user = "flask"
EOF

# Build and run
flox containerize -f - | docker load
docker run -p 5000:5000 -v $(pwd):/app <container-id>
```

### Node.js Application

```bash
flox init
flox install nodejs

cat >> .flox/env/manifest.toml << 'EOF'
[containerize.config]
exposed-ports = ["3000/tcp"]
cmd = ["npm", "start"]
working-dir = "/app"
EOF

flox containerize --tag myapp:latest --runtime docker
docker run -p 3000:3000 -v $(pwd):/app myapp:latest
```

### Database Container

```bash
flox init
flox install postgresql

# Set up service in manifest
flox edit

# Add service and container config
cat >> .flox/env/manifest.toml << 'EOF'
[services.postgres]
command = '''
  mkdir -p /data/postgres
  if [ ! -d "/data/postgres/pgdata" ]; then
    initdb -D /data/postgres/pgdata
  fi
  exec postgres -D /data/postgres/pgdata -h 0.0.0.0
'''
is-daemon = true

[containerize.config]
exposed-ports = ["5432/tcp"]
volumes = ["/data"]
cmd = []  # Service starts automatically
EOF

flox containerize -f - | docker load
docker run -p 5432:5432 -v pgdata:/data <container-id>
```

## Common Patterns

### Service Containers

Services start automatically when cmd is empty:

```toml
[services.web]
command = "python -m http.server 8000"

[containerize.config]
exposed-ports = ["8000/tcp"]
cmd = []  # Service starts automatically
```

### Multi-Stage Pattern

Build in one environment, run in another:

```bash
# Build environment with all dev tools
cd build-env
flox activate -- flox build myapp

# Runtime environment with minimal deps
cd ../runtime-env
flox install myapp
flox containerize --tag production -f - | docker load

# Run
docker run production
```

### Remote Environment Containers

Containerize shared team environments:

```bash
# Containerize remote environment
flox containerize -r team/python-ml --tag latest --runtime docker

# Run it
docker run -it team-python-ml:latest
```

### Multi-Service Container

```toml
[services.db]
command = '''exec postgres -D "$FLOX_ENV_CACHE/postgres"'''
is-daemon = true

[services.cache]
command = '''exec redis-server'''
is-daemon = true

[services.api]
command = '''exec python -m uvicorn main:app --host 0.0.0.0'''

[containerize.config]
exposed-ports = ["8000/tcp", "5432/tcp", "6379/tcp"]
cmd = []  # All services start automatically
```

## Platform-Specific Notes

### macOS
- Requires docker/podman runtime (uses proxy container for builds)
- May prompt for file sharing permissions
- Creates `flox-nix` volume for caching
- Safe to remove when not building: `docker volume rm flox-nix`

### Linux
- Direct image creation without proxy
- No intermediate volumes needed
- Native container support

## Advanced Use Cases

### Custom Entrypoint with Wrapper Script

```toml
[build.entrypoint]
command = '''
  cat > $out/bin/entrypoint.sh << 'EOF'
#!/usr/bin/env bash
set -e

# Custom initialization
echo "Initializing application..."
setup_app

# Run whatever command was passed
exec "$@"
EOF
  chmod +x $out/bin/entrypoint.sh
'''

[containerize.config]
cmd = ["entrypoint.sh", "python", "app.py"]
```

### Health Check Support

```toml
[containerize.config]
cmd = ["python", "app.py"]
labels = {
  "healthcheck" = "curl -f http://localhost:8000/health || exit 1"
}
```

Then in Docker:
```bash
docker run --health-cmd="curl -f http://localhost:8000/health || exit 1" \
           --health-interval=30s \
           myimage
```

### Multi-Architecture Builds

Build for different architectures:

```bash
# On x86_64 Linux
flox containerize --tag myapp:amd64 --runtime docker

# On ARM64 (aarch64) Linux
flox containerize --tag myapp:arm64 --runtime docker

# Create manifest
docker manifest create myapp:latest \
  myapp:amd64 \
  myapp:arm64
```

### Minimal Container Size

Create minimal runtime environment:

```toml
[install]
# Only runtime dependencies
python.pkg-path = "python311"
# No dev tools, no build tools

[build.app]
command = '''
  # Build in build environment
  python -m pip install --target=$out/lib/python -r requirements.txt
  cp -r src $out/lib/python/
'''
runtime-packages = ["python"]

[containerize.config]
cmd = ["python", "-m", "myapp"]
```

## Container Registry Workflows

### Push to Registry

```bash
# Build container
flox containerize --tag myapp:v1.0 --runtime docker

# Tag for registry
docker tag myapp:v1.0 registry.company.com/myapp:v1.0

# Push
docker push registry.company.com/myapp:v1.0
```

### GitLab CI/CD

```yaml
containerize:
  stage: build
  script:
    - flox containerize --tag $CI_REGISTRY_IMAGE:$CI_COMMIT_TAG --runtime docker
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_TAG
```

### GitHub Actions

```yaml
- name: Build container
  run: |
    flox containerize --tag ghcr.io/${{ github.repository }}:${{ github.sha }} --runtime docker

- name: Push to GHCR
  run: |
    echo ${{ secrets.GITHUB_TOKEN }} | docker login ghcr.io -u ${{ github.actor }} --password-stdin
    docker push ghcr.io/${{ github.repository }}:${{ github.sha }}
```

## Kubernetes Deployment

### Basic Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: myapp
        image: registry.company.com/myapp:v1.0
        ports:
        - containerPort: 8000
        volumeMounts:
        - name: data
          mountPath: /data
      volumes:
      - name: data
        persistentVolumeClaim:
          claimName: myapp-data
```

### Service Definition

```yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp
spec:
  selector:
    app: myapp
  ports:
  - port: 80
    targetPort: 8000
  type: LoadBalancer
```

## Debugging Container Issues

### Inspect Container

```bash
# Run interactively
docker run -it --entrypoint /bin/bash <image-id>

# Check environment
docker run <image-id> env

# Check what's in the image
docker run <image-id> ls -la /
```

### View Container Logs

```bash
# Follow logs
docker logs -f <container-id>

# Last 100 lines
docker logs --tail 100 <container-id>
```

### Execute Commands in Running Container

```bash
# Get a shell
docker exec -it <container-id> /bin/bash

# Run specific command
docker exec <container-id> flox list
```

## Best Practices

1. **Use specific tags**: Avoid `latest`, use semantic versioning
2. **Minimize layers**: Combine related operations in manifests
3. **Use .dockerignore equivalent**: Only include necessary files in build context
4. **Health checks**: Implement health check endpoints for services
5. **Security**: Run as non-root user when possible
6. **Volumes**: Use volumes for persistent data, not container filesystem
7. **Environment variables**: Make configuration overridable via env vars
8. **Logging**: Log to stdout/stderr, not files

## Related Skills

- **flox-environments** - Creating environments to containerize
- **flox-services** - Running services in containers
- **flox-builds** - Building artifacts before containerizing
- **flox-sharing** - Containerizing remote environments
