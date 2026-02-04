---
name: docker-compose
description: Expert guidance for Docker Compose including multi-container applications, service definitions, networks, volumes, environment variables, health checks, and orchestration. Use this when working with Docker Compose files and container orchestration.
tags: [docker, docker-compose, containers, orchestration]
color: cyan
---

# Docker Compose Expert Skill

You are an expert in Docker Compose for defining and running multi-container applications.

## Core Concepts

### Compose File Structure
```yaml
# NOTE: 'version' field is OBSOLETE and should NOT be used
# Docker Compose now uses the Compose Specification (no version needed)

services:       # Container definitions
  service1:
    # Service configuration

networks:       # Network definitions
  network1:

volumes:        # Volume definitions
  volume1:

secrets:        # Secrets (Swarm/external)
  secret1:

configs:        # Configs (Swarm/external)
  config1:
```

**IMPORTANT:** The `version` field is obsolete since Compose Specification. Modern Docker Compose automatically uses the latest specification.

## Service Definition

### Basic Service
```yaml
services:
  web:
    image: nginx:latest           # Use pre-built image
    # OR
    build:                        # Build from Dockerfile
      context: ./web
      dockerfile: Dockerfile.dev
    container_name: my-web        # Custom container name
    restart: unless-stopped       # Restart policy
    ports:
      - "8080:80"                 # Host:Container
      - "8443:443"
    environment:
      ENV_VAR: value
      DEBUG: "true"
    # OR
    env_file:
      - .env
      - .env.local
    volumes:
      - ./config:/etc/nginx/conf.d:ro
      - web-data:/var/www/html
    networks:
      - frontend
      - backend
    depends_on:
      - database
    command: ["nginx", "-g", "daemon off;"]
    user: "1000:1000"
```

### Advanced Options
```yaml
services:
  app:
    image: myapp:latest

    # Resource limits
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          cpus: '1'
          memory: 1G

    # Health check
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

    # Logging
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

    # DNS
    dns:
      - 8.8.8.8
      - 8.8.4.4

    # Extra hosts
    extra_hosts:
      - "host.docker.internal:host-gateway"

    # Labels
    labels:
      com.example.description: "My application"
      com.example.version: "1.0"

    # Security
    security_opt:
      - no-new-privileges:true
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE

    # Devices
    devices:
      - "/dev/ttyUSB0:/dev/ttyUSB0"

    # Privileged mode (use cautiously)
    privileged: true
```

## Networks

### Network Types
```yaml
networks:
  # Default bridge network
  frontend:
    driver: bridge

  # Custom bridge with subnet
  backend:
    driver: bridge
    ipam:
      config:
        - subnet: 172.28.0.0/16
          gateway: 172.28.0.1

  # Host network (no isolation)
  host-network:
    driver: host

  # Overlay network (Swarm)
  overlay-net:
    driver: overlay
    attachable: true

  # External network (pre-existing)
  external-net:
    external: true
    name: my-existing-network
```

### Service Network Configuration
```yaml
services:
  web:
    networks:
      frontend:
        ipv4_address: 172.28.0.10  # Static IP
        aliases:
          - web-server
          - www
```

## Volumes

### Volume Types
```yaml
volumes:
  # Named volume (managed by Docker)
  data-volume:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: /path/on/host

  # External volume (pre-existing)
  external-volume:
    external: true
    name: my-existing-volume
```

### Volume Mounts
```yaml
services:
  app:
    volumes:
      # Named volume
      - app-data:/app/data

      # Bind mount (host path)
      - ./config:/app/config:ro      # Read-only

      # Anonymous volume
      - /app/temp

      # tmpfs mount (in memory)
      - type: tmpfs
        target: /app/cache
        tmpfs:
          size: 100m
```

## Environment Variables

### Methods
```yaml
services:
  app:
    # Inline
    environment:
      DATABASE_URL: postgres://user:pass@db:5432/mydb
      DEBUG: "true"

    # From .env file
    env_file:
      - .env
      - .env.production

    # Variable substitution from shell
    environment:
      HOST_IP: ${HOST_IP:-0.0.0.0}
      PORT: ${PORT:-8080}
```

### .env File Example
```bash
# .env
POSTGRES_USER=admin
POSTGRES_PASSWORD=secret123
POSTGRES_DB=myapp
NODE_ENV=production
```

## Dependencies & Startup Order

### Basic Dependencies
```yaml
services:
  web:
    depends_on:
      - database
      - cache

  database:
    image: postgres:14
```

### With Health Checks (v2.1+)
```yaml
services:
  web:
    depends_on:
      database:
        condition: service_healthy
      cache:
        condition: service_started

  database:
    image: postgres:14
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
```

## Build Configuration

### Simple Build
```yaml
services:
  app:
    build: ./app  # Path to Dockerfile
```

### Advanced Build
```yaml
services:
  app:
    build:
      context: ./app
      dockerfile: Dockerfile.prod
      args:
        - BUILD_VERSION=1.0.0
        - NODE_ENV=production
      target: production           # Multi-stage build target
      cache_from:
        - myapp:cache
      labels:
        - "com.example.version=1.0"
      shm_size: '2gb'
```

## Common Patterns

### Web Application Stack
```yaml
services:
  # Reverse Proxy
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./certs:/etc/nginx/certs:ro
    depends_on:
      - app
    networks:
      - frontend

  # Application
  app:
    build: ./app
    environment:
      DATABASE_URL: postgres://user:pass@db:5432/myapp
      REDIS_URL: redis://cache:6379
    depends_on:
      db:
        condition: service_healthy
      cache:
        condition: service_started
    networks:
      - frontend
      - backend

  # Database
  db:
    image: postgres:14
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: myapp
    volumes:
      - db-data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "user"]
      interval: 10s
    networks:
      - backend

  # Cache
  cache:
    image: redis:alpine
    networks:
      - backend

networks:
  frontend:
  backend:

volumes:
  db-data:
```

### Development vs Production
```yaml
# docker-compose.yml (base)
services:
  app:
    image: myapp:latest
    environment:
      NODE_ENV: ${NODE_ENV:-development}

# docker-compose.dev.yml (development overrides)
services:
  app:
    build:
      context: .
      target: development
    volumes:
      - ./src:/app/src  # Hot reload
    command: npm run dev

# docker-compose.prod.yml (production overrides)
services:
  app:
    restart: always
    deploy:
      replicas: 3
      resources:
        limits:
          memory: 1G
```

**Usage:**
```bash
# Development
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up

# Production
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

## Commands

### Basic Operations
```bash
# Start services
docker-compose up                    # Foreground
docker-compose up -d                 # Detached (background)
docker-compose up --build            # Rebuild images
docker-compose up --force-recreate   # Recreate containers

# Stop services
docker-compose stop                  # Stop containers
docker-compose down                  # Stop and remove containers
docker-compose down -v               # Also remove volumes
docker-compose down --rmi all        # Also remove images

# View status
docker-compose ps                    # Running services
docker-compose ps -a                 # All services
docker-compose top                   # Running processes

# Logs
docker-compose logs                  # All logs
docker-compose logs -f               # Follow logs
docker-compose logs -f app           # Follow specific service
docker-compose logs --tail=100 app   # Last 100 lines

# Execute commands
docker-compose exec app bash         # Interactive shell
docker-compose exec app ls -la       # Run command
docker-compose exec -u root app sh   # As specific user

# Run one-off commands
docker-compose run app npm install   # Run command in new container
docker-compose run --rm app pytest   # Auto-remove after run

# Scale services
docker-compose up -d --scale app=3   # Run 3 instances

# Configuration
docker-compose config                # Validate and view config
docker-compose config --services     # List services
docker-compose config --volumes      # List volumes
```

### Build & Images
```bash
# Build images
docker-compose build                 # Build all
docker-compose build app             # Build specific service
docker-compose build --no-cache      # No cache

# Pull images
docker-compose pull                  # Pull all
docker-compose pull app              # Pull specific service

# Push images
docker-compose push                  # Push all to registry
```

### Advanced
```bash
# Restart services
docker-compose restart               # All services
docker-compose restart app           # Specific service

# Pause/unpause
docker-compose pause
docker-compose unpause

# Remove stopped containers
docker-compose rm
docker-compose rm -f                 # Force removal

# Events
docker-compose events                # Stream events
docker-compose events --json         # JSON format

# Port mapping
docker-compose port app 8080         # Get mapped port
```

## Best Practices

### Security
1. **Don't hardcode secrets** - Use environment variables or secrets
2. **Run as non-root** - Specify user
3. **Use read-only mounts** - Add `:ro` to volumes
4. **Limit capabilities** - Use `cap_drop` and `cap_add`
5. **Use secrets for sensitive data** (Docker Swarm)

### Performance
1. **Use named volumes** for data persistence
2. **Leverage build cache** - Order Dockerfile commands properly
3. **Use health checks** for dependencies
4. **Limit resource usage** with deploy.resources
5. **Use Alpine images** for smaller size

### Development
1. **Use .dockerignore** - Exclude unnecessary files
2. **Hot reload** - Mount source code as volumes
3. **Separate dev/prod configs** - Use compose file overrides
4. **Use profiles** for optional services

### Profiles
```yaml
services:
  app:
    image: myapp
    # Always runs

  debug:
    image: myapp
    profiles:
      - debug
    command: ["node", "--inspect=0.0.0.0:9229", "app.js"]

  test:
    image: myapp
    profiles:
      - test
    command: ["npm", "test"]
```

```bash
# Run only default services
docker-compose up

# Run with debug profile
docker-compose --profile debug up

# Run with multiple profiles
docker-compose --profile debug --profile test up
```

## Troubleshooting

### Common Issues
| Issue | Solution |
|-------|----------|
| Port already in use | Change port mapping or stop conflicting service |
| Cannot connect between services | Check network configuration, use service names |
| Volume permission denied | Check user ID, use `user:` directive |
| Container keeps restarting | Check logs, verify command and health check |
| Build cache issues | Use `--no-cache` flag |

### Debugging
```bash
# Inspect service
docker-compose config --services
docker-compose ps
docker-compose logs service-name

# Check container
docker inspect container-id

# Network connectivity
docker-compose exec app ping db
docker-compose exec app nslookup db

# File system
docker-compose exec app ls -la /path

# Environment
docker-compose exec app env
```

## Resources
- [Compose Specification](https://compose-spec.io/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Compose File Reference](https://docs.docker.com/compose/compose-file/)
