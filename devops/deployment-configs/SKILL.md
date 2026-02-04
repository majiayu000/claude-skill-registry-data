---
name: deployment-configs
description: Production deployment configurations for Celery workers and beat schedulers across Docker, Kubernetes, and systemd environments. Use when deploying Celery to production, containerizing workers, orchestrating with Kubernetes, setting up systemd services, configuring health checks, implementing graceful shutdowns, or when user mentions deployment, Docker, Kubernetes, systemd, production setup, or worker containerization.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Deployment Configurations

**Purpose:** Generate production-ready deployment configurations for Celery workers and beat schedulers across multiple deployment platforms.

**Activation Triggers:**
- Production deployment setup
- Docker/containerization requirements
- Kubernetes orchestration needs
- Systemd service configuration
- Health check implementation
- Graceful shutdown requirements
- Multi-worker scaling
- Environment-specific configuration

**Key Resources:**
- `scripts/deploy.sh` - Complete deployment orchestration
- `scripts/test-deployment.sh` - Validate deployment health
- `scripts/health-check.sh` - Comprehensive health verification
- `templates/docker-compose.yml` - Full Docker stack
- `templates/Dockerfile.worker` - Optimized worker container
- `templates/kubernetes/` - K8s manifests for workers and beat
- `templates/systemd/` - Systemd service units
- `templates/health-checks.py` - Python health check implementation
- `examples/` - Complete deployment scenarios

## Deployment Platforms

### Docker Compose (Development/Staging)

**Use Case:** Local development, staging environments, simple production setups

**Configuration:** `templates/docker-compose.yml`

**Services Included:**
- Redis (broker)
- PostgreSQL (result backend)
- Celery worker(s)
- Celery beat scheduler
- Flower monitoring
- Health check sidecar

**Quick Start:**
```bash
# Generate Docker configuration
./scripts/deploy.sh docker --env=staging

# Start all services
docker-compose up -d

# Scale workers
docker-compose up -d --scale celery-worker=4

# View logs
docker-compose logs -f celery-worker
```

**Key Features:**
- Multi-worker support with easy scaling
- Volume mounts for code hot-reload
- Environment-specific configurations
- Health checks with restart policies
- Networking between services
- Persistent data volumes

### Kubernetes (Production)

**Use Case:** Production environments requiring orchestration, auto-scaling, and high availability

**Manifests:** `templates/kubernetes/`

**Resources:**
- `celery-worker.yaml` - Worker Deployment with HPA
- `celery-beat.yaml` - Beat StatefulSet (singleton)
- `celery-configmap.yaml` - Environment configuration
- `celery-secrets.yaml` - Sensitive credentials
- `celery-service.yaml` - Internal service endpoints
- `celery-hpa.yaml` - Horizontal Pod Autoscaler

**Quick Start:**
```bash
# Generate K8s manifests
./scripts/deploy.sh kubernetes --namespace=production

# Apply configuration
kubectl apply -f kubernetes/

# Scale workers
kubectl scale deployment celery-worker --replicas=10

# Monitor status
kubectl get pods -l app=celery-worker
kubectl logs -f deployment/celery-worker
```

**Key Features:**
- Horizontal Pod Autoscaling based on CPU/queue depth
- ConfigMaps for environment variables
- Secrets management for credentials
- Rolling updates with zero downtime
- Resource limits and requests
- Liveness and readiness probes
- Pod disruption budgets
- Anti-affinity for worker distribution

### Systemd (Bare Metal/VMs)

**Use Case:** Traditional server deployments, VPS, dedicated servers

**Service Units:** `templates/systemd/`

**Services:**
- `celery-worker.service` - Worker daemon
- `celery-beat.service` - Beat scheduler daemon
- `celery-flower.service` - Monitoring dashboard

**Quick Start:**
```bash
# Generate systemd units
./scripts/deploy.sh systemd --workers=4

# Install services
sudo cp systemd/*.service /etc/systemd/system/
sudo systemctl daemon-reload

# Enable and start
sudo systemctl enable celery-worker@{1..4}.service celery-beat.service
sudo systemctl start celery-worker@{1..4}.service celery-beat.service

# Check status
sudo systemctl status celery-worker@*.service
sudo journalctl -u celery-worker@1.service -f
```

**Key Features:**
- Multi-instance worker support (@instance syntax)
- Automatic restart on failure
- Resource limits (CPU, memory)
- Graceful shutdown handling
- Log management via journald
- User/group isolation
- Environment file support

## Health Checks Implementation

### Python Health Check Module

**Location:** `templates/health-checks.py`

**Capabilities:**
- Broker connectivity verification
- Result backend validation
- Worker discovery and ping
- Queue depth monitoring
- Task execution test
- Memory and CPU metrics

**Usage:**
```python
from health_checks import CeleryHealthCheck

# Initialize checker
health = CeleryHealthCheck(app)

# Run all checks
status = health.run_all_checks()

# Individual checks
broker_ok = health.check_broker()
workers_ok = health.check_workers()
queues_ok = health.check_queue_depth(threshold=1000)
```

**Integration:**
```python
# Flask endpoint
@app.route('/health')
def health_check():
    checker = CeleryHealthCheck(celery_app)
    result = checker.run_all_checks()
    return jsonify(result), 200 if result['healthy'] else 503

# FastAPI endpoint
@app.get("/health")
async def health_check():
    checker = CeleryHealthCheck(celery_app)
    result = checker.run_all_checks()
    return result if result['healthy'] else JSONResponse(
        status_code=503, content=result
    )
```

### Shell Script Health Checks

**Location:** `scripts/health-check.sh`

**Features:**
- Standalone health verification
- Exit code compatibility (0=healthy, 1=unhealthy)
- JSON output for parsing
- Configurable timeouts
- Retry logic

**Usage:**
```bash
# Basic health check
./scripts/health-check.sh

# With custom timeout
./scripts/health-check.sh --timeout=30

# JSON output
./scripts/health-check.sh --json

# Specific checks
./scripts/health-check.sh --check=broker,workers
```

**Docker Integration:**
```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD /app/scripts/health-check.sh || exit 1
```

**Kubernetes Integration:**
```yaml
livenessProbe:
  exec:
    command: ["/app/scripts/health-check.sh"]
  initialDelaySeconds: 30
  periodSeconds: 10
readinessProbe:
  exec:
    command: ["/app/scripts/health-check.sh", "--check=workers"]
  initialDelaySeconds: 10
  periodSeconds: 5
```

## Deployment Scripts

### Main Deployment Orchestrator

**Script:** `scripts/deploy.sh`

**Capabilities:**
- Platform detection and configuration
- Environment-specific settings
- Secret management validation
- Pre-deployment checks
- Configuration generation
- Deployment execution
- Post-deployment verification

**Usage:**
```bash
# Deploy to Docker
./scripts/deploy.sh docker --env=production

# Deploy to Kubernetes
./scripts/deploy.sh kubernetes --namespace=prod --replicas=10

# Deploy systemd services
./scripts/deploy.sh systemd --workers=4 --user=celery

# Dry run (generate configs only)
./scripts/deploy.sh kubernetes --dry-run

# With custom configuration
./scripts/deploy.sh docker --config=custom-config.yml
```

**Pre-deployment Checks:**
- Broker accessibility
- Result backend connectivity
- Required environment variables
- Secret availability (no hardcoded keys)
- Python dependencies
- Celery app importability
- Task discovery

### Deployment Testing

**Script:** `scripts/test-deployment.sh`

**Test Coverage:**
- Service availability
- Health endpoint responses
- Worker registration
- Task execution end-to-end
- Beat schedule validation
- Monitoring dashboard access
- Log output verification
- Resource utilization

**Usage:**
```bash
# Test Docker deployment
./scripts/test-deployment.sh docker

# Test Kubernetes deployment
./scripts/test-deployment.sh kubernetes --namespace=prod

# Test systemd services
./scripts/test-deployment.sh systemd

# Verbose output
./scripts/test-deployment.sh docker --verbose

# Continuous monitoring
./scripts/test-deployment.sh docker --watch --interval=60
```

**Test Scenarios:**
1. Submit test task to each queue
2. Verify task completion
3. Check worker logs for errors
4. Validate beat schedule execution
5. Test graceful shutdown
6. Verify task retry behavior
7. Check monitoring metrics

## Configuration Templates

### Docker Compose Template

**File:** `templates/docker-compose.yml`

**Highlights:**
- Multi-stage build support
- Environment variable templating
- Volume management
- Network configuration
- Health check definitions
- Resource limits
- Logging configuration

**Key Sections:**
```yaml
services:
  redis:
    # Broker configuration with persistence

  postgres:
    # Result backend with backup volumes

  celery-worker:
    # Worker with auto-scaling support
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '1.0'
          memory: 1G

  celery-beat:
    # Singleton scheduler
    deploy:
      replicas: 1

  flower:
    # Monitoring dashboard
```

### Dockerfile Template

**File:** `templates/Dockerfile.worker`

**Optimization:**
- Multi-stage build for smaller images
- Layer caching for dependencies
- Non-root user execution
- Security scanning compatible
- Build-time arguments for flexibility

**Stages:**
1. **Base:** Python runtime + system dependencies
2. **Builder:** Install and compile Python packages
3. **Runtime:** Copy built packages, add application code

**Size Optimization:**
- Minimal base image (python:3.11-slim)
- Remove build tools in final stage
- Use .dockerignore
- Multi-arch support

### Kubernetes Manifests

**Worker Deployment:** `templates/kubernetes/celery-worker.yaml`

**Features:**
- Rolling update strategy
- Resource requests and limits
- Horizontal Pod Autoscaler integration
- Anti-affinity rules
- Graceful termination (SIGTERM handling)
- ConfigMap and Secret mounting

**Beat StatefulSet:** `templates/kubernetes/celery-beat.yaml`

**Features:**
- Singleton guarantee (replicas: 1)
- Persistent volume for schedule state
- Leader election (optional)
- Ordered deployment

**Autoscaling:** `templates/kubernetes/celery-hpa.yaml`

**Metrics:**
- CPU utilization
- Memory utilization
- Custom metrics (queue depth via Prometheus)

**Scaling Behavior:**
```yaml
minReplicas: 2
maxReplicas: 50
behavior:
  scaleUp:
    stabilizationWindowSeconds: 60
    policies:
    - type: Percent
      value: 50
      periodSeconds: 60
  scaleDown:
    stabilizationWindowSeconds: 300
    policies:
    - type: Pods
      value: 2
      periodSeconds: 120
```

### Systemd Service Units

**Worker Service:** `templates/systemd/celery-worker.service`

**Configuration:**
```ini
[Unit]
Description=Celery Worker Instance %i
After=network.target redis.service

[Service]
Type=forking
User=celery
Group=celery
EnvironmentFile=/etc/celery/celery.conf
WorkingDirectory=/opt/celery
ExecStart=/opt/celery/venv/bin/celery -A myapp worker \
  --loglevel=info \
  --logfile=/var/log/celery/worker-%i.log \
  --pidfile=/var/run/celery/worker-%i.pid \
  --hostname=worker%i@%%h \
  --concurrency=4

ExecStop=/bin/kill -s TERM $MAINPID
ExecReload=/bin/kill -s HUP $MAINPID

Restart=always
RestartSec=10s

# Resource limits
CPUQuota=100%
MemoryLimit=1G

[Install]
WantedBy=multi-user.target
```

**Beat Service:** `templates/systemd/celery-beat.service`

**Singleton Management:**
- Single instance enforcement
- Schedule persistence
- Lock file management

## Security Best Practices

### Secrets Management

**CRITICAL: Never hardcode credentials in configurations!**

**Docker Compose:**
```yaml
services:
  celery-worker:
    environment:
      CELERY_BROKER_URL: ${CELERY_BROKER_URL}
      CELERY_RESULT_BACKEND: ${CELERY_RESULT_BACKEND}
    env_file:
      - .env  # Never commit this file!
```

**Kubernetes:**
```yaml
# Use Secrets, not ConfigMaps
env:
  - name: CELERY_BROKER_URL
    valueFrom:
      secretKeyRef:
        name: celery-secrets
        key: broker-url
```

**Systemd:**
```ini
EnvironmentFile=/etc/celery/secrets.env  # Mode 0600, owned by celery user
```

### User Isolation

**Docker:**
```dockerfile
RUN useradd -m -u 1000 celery
USER celery
```

**Kubernetes:**
```yaml
securityContext:
  runAsUser: 1000
  runAsNonRoot: true
  readOnlyRootFilesystem: true
```

**Systemd:**
```ini
User=celery
Group=celery
```

### Network Security

- Use TLS for broker connections
- Encrypt result backend connections
- Isolate worker networks
- Implement network policies (K8s)
- Use firewall rules (systemd)

## Monitoring Integration

### Prometheus Metrics

**Expose Metrics:**
```python
from prometheus_client import start_http_server, Counter, Gauge

task_counter = Counter('celery_task_total', 'Total tasks', ['name', 'state'])
worker_gauge = Gauge('celery_workers_active', 'Active workers')

# Start metrics server
start_http_server(8000)
```

**Kubernetes ServiceMonitor:**
```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: celery-metrics
spec:
  selector:
    matchLabels:
      app: celery-worker
  endpoints:
  - port: metrics
```

### Flower Dashboard

**Configuration:**
```yaml
# docker-compose.yml
flower:
  image: mher/flower:latest
  command: celery flower --broker=redis://redis:6379/0
  ports:
    - "5555:5555"
  environment:
    FLOWER_BASIC_AUTH: user:your_password_here  # Use env var!
```

### Log Aggregation

**Docker:**
```yaml
logging:
  driver: "json-file"
  options:
    max-size: "10m"
    max-file: "3"
```

**Kubernetes:**
- Use sidecar containers (Fluent Bit, Fluentd)
- Send logs to ELK stack or Loki

**Systemd:**
```bash
journalctl -u celery-worker@1.service -f --output=json
```

## Graceful Shutdown

### Signal Handling

**Worker Shutdown:**
```python
from celery.signals import worker_shutdown

@worker_shutdown.connect
def graceful_shutdown(sender, **kwargs):
    logger.info("Worker shutting down gracefully...")
    # Finish current tasks
    # Close connections
    # Release resources
```

**Docker:**
```dockerfile
STOPSIGNAL SIGTERM
```

**Kubernetes:**
```yaml
lifecycle:
  preStop:
    exec:
      command: ["/bin/sh", "-c", "sleep 15"]
terminationGracePeriodSeconds: 60
```

**Systemd:**
```ini
KillSignal=SIGTERM
TimeoutStopSec=60
```

### Task Acknowledgment

**Late ACK Pattern:**
```python
task_acks_late = True
task_reject_on_worker_lost = True
```

Ensures tasks are re-queued if worker dies during execution.

## Examples

### Complete Docker Deployment

**File:** `examples/docker-deployment.md`

**Scenario:** Deploy full Celery stack with Redis, PostgreSQL, 3 workers, beat, and Flower

**Steps:**
1. Generate Docker Compose configuration
2. Configure environment variables
3. Build worker image
4. Start all services
5. Verify health checks
6. Submit test tasks
7. Monitor via Flower
8. Scale workers based on load

### Kubernetes Production Setup

**File:** `examples/kubernetes-deployment.md`

**Scenario:** Production-grade K8s deployment with autoscaling, monitoring, and HA

**Components:**
- 3+ worker replicas (autoscaling enabled)
- Single beat instance (StatefulSet)
- Redis Sentinel (HA broker)
- PostgreSQL cluster (result backend)
- Prometheus monitoring
- Grafana dashboards
- Horizontal Pod Autoscaler

**Advanced Features:**
- Pod Disruption Budgets
- Network Policies
- Resource Quotas
- RBAC permissions
- Ingress for Flower

### Systemd Enterprise Deployment

**File:** `examples/systemd-setup.md`

**Scenario:** Multi-server deployment with systemd management

**Architecture:**
- 3 worker servers (4 workers each)
- 1 beat scheduler server
- Shared Redis cluster
- Shared PostgreSQL database
- Centralized logging

**Management:**
```bash
# Start all workers across servers
ansible celery-workers -a "systemctl start celery-worker@{1..4}.service"

# Rolling restart
for i in {1..4}; do
  systemctl restart celery-worker@$i.service
  sleep 30
done

# Health check all workers
ansible celery-workers -m shell -a "/opt/celery/scripts/health-check.sh"
```

## Troubleshooting

### Common Issues

**Workers not starting:**
- Check broker connectivity
- Verify Python dependencies
- Review worker logs
- Validate Celery app import

**Tasks not executing:**
- Confirm workers are registered
- Check queue routing
- Verify task signatures
- Review task ACK settings

**Beat not scheduling:**
- Ensure single beat instance
- Check schedule file permissions
- Verify timezone configuration
- Review beat logs for errors

**High memory usage:**
- Reduce worker concurrency
- Enable max-tasks-per-child
- Check for memory leaks in tasks
- Monitor with profiling tools

**Container restarts:**
- Review health check configuration
- Check resource limits
- Analyze OOM events
- Verify signal handling

## Resources

**Scripts:** All deployment and health check scripts in `scripts/` directory

**Templates:** Production-ready configuration templates in `templates/` directory

**Examples:** Complete deployment scenarios with step-by-step instructions in `examples/` directory

**Documentation:**
- Docker Compose reference
- Kubernetes best practices
- Systemd unit configuration
- Celery production checklist

---

## Security Compliance

This skill follows strict security rules:
- All code examples use placeholder values only
- No real API keys, passwords, or secrets
- Environment variable references in all code
- `.gitignore` protection documented
- Secrets management best practices enforced

**Version:** 1.0.0
**Celery Compatibility:** 5.0+
**Platforms:** Docker, Kubernetes, Systemd
