---
name: redis-installation
description: Complete Redis installation guide for all platforms - Linux, macOS, Docker, and cloud deployments with configuration templates
sasmp_version: "1.3.0"
bonded_agent: 01-redis-fundamentals
bond_type: PRIMARY_BOND

# Production Configuration
version: "2.1.0"
last_updated: "2025-01"

# Parameters
parameters:
  platform:
    type: string
    required: true
    enum: [linux-debian, linux-rhel, macos, docker, kubernetes]
    description: Target platform for installation
  redis_version:
    type: string
    required: false
    default: "7.2"
    pattern: "^[6-7]\\.[0-9]+$"
  install_method:
    type: string
    required: false
    enum: [package, source, container]
    default: package
  persistence:
    type: boolean
    required: false
    default: true

# Retry Configuration
retry_config:
  max_retries: 3
  backoff_strategy: exponential
  backoff_base_ms: 2000
  retryable_errors:
    - network_timeout
    - package_not_found
    - repository_error

# Observability
observability:
  logging:
    level: info
    format: json
  metrics:
    - installation_duration_ms
    - verification_result
    - config_validation_status

# Validation Rules
validation:
  pre_install:
    - check_disk_space: "1GB"
    - check_memory: "512MB"
    - check_ports: [6379]
  post_install:
    - verify_ping: true
    - verify_version: true
---

# Redis Installation Skill

## Overview

Production-grade installation skill for Redis across all major platforms with automated verification and configuration validation.

## Supported Platforms

### Linux (Ubuntu/Debian)
```bash
# Update and install
sudo apt update
sudo apt install redis-server -y

# Start and enable
sudo systemctl start redis-server
sudo systemctl enable redis-server

# Verify
redis-cli ping  # Returns PONG
```

### Linux (RHEL/CentOS/Rocky)
```bash
# Install EPEL and Redis
sudo dnf install epel-release -y
sudo dnf install redis -y

# Start and enable
sudo systemctl start redis
sudo systemctl enable redis
```

### macOS (Homebrew)
```bash
# Install
brew install redis

# Start as service
brew services start redis

# Or run manually
redis-server /opt/homebrew/etc/redis.conf
```

### Docker
```bash
# Simple run
docker run -d --name redis -p 6379:6379 redis:7-alpine

# With persistence
docker run -d --name redis \
  -p 6379:6379 \
  -v redis-data:/data \
  redis:7-alpine redis-server --appendonly yes

# With custom config
docker run -d --name redis \
  -p 6379:6379 \
  -v $(pwd)/redis.conf:/usr/local/etc/redis/redis.conf \
  redis:7-alpine redis-server /usr/local/etc/redis/redis.conf
```

### Kubernetes (Helm)
```bash
# Add Bitnami repo
helm repo add bitnami https://charts.bitnami.com/bitnami

# Install Redis
helm install redis bitnami/redis \
  --set auth.password=your-password \
  --set replica.replicaCount=2
```

## Verification Commands

```bash
# Test connection
redis-cli ping                    # Expected: PONG

# Check version
redis-cli INFO server | grep redis_version

# Test basic operations
redis-cli SET test:install "success"
redis-cli GET test:install
redis-cli DEL test:install

# Check config
redis-cli CONFIG GET dir
redis-cli CONFIG GET port
```

## Initial Configuration

```conf
# /etc/redis/redis.conf - Production Basics

# Network
bind 127.0.0.1
port 6379
protected-mode yes

# Memory
maxmemory 256mb
maxmemory-policy allkeys-lru

# Persistence
appendonly yes
appendfsync everysec

# Security
requirepass your-strong-password
```

## Assets

- `docker-compose.yml` - Production Docker setup
- `redis.conf` - Optimized configuration template

## Scripts

- `install-redis.sh` - Cross-platform installation script
- `verify-installation.sh` - Health check script

## References

- `INSTALLATION_GUIDE.md` - Detailed installation steps
- `TROUBLESHOOTING.md` - Common issues and solutions

---

## Troubleshooting Guide

### Common Issues & Solutions

#### 1. Package Not Found
```
E: Unable to locate package redis-server
```

**Fix:**
```bash
# Ubuntu - add official repo
curl -fsSL https://packages.redis.io/gpg | sudo gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/redis.list
sudo apt update
```

#### 2. Port Already in Use
```
Could not create server TCP listening socket: bind: Address already in use
```

**Diagnosis:**
```bash
# Check what's using port 6379
sudo lsof -i :6379
sudo netstat -tlnp | grep 6379
```

**Fix:**
```bash
# Kill existing process
sudo kill $(sudo lsof -t -i:6379)

# Or change port in redis.conf
port 6380
```

#### 3. Permission Denied
```
Can't open the log file: Permission denied
```

**Fix:**
```bash
# Fix ownership
sudo chown -R redis:redis /var/lib/redis
sudo chown -R redis:redis /var/log/redis

# Fix permissions
sudo chmod 750 /var/lib/redis
```

#### 4. Memory Overcommit Warning
```
# WARNING overcommit_memory is set to 0!
```

**Fix:**
```bash
# Temporary
echo 1 > /proc/sys/vm/overcommit_memory

# Permanent
echo "vm.overcommit_memory = 1" >> /etc/sysctl.conf
sysctl -p
```

### Installation Verification Script

```bash
#!/bin/bash
# verify-redis-installation.sh

echo "=== Redis Installation Verification ==="

# Check if redis-server is running
echo -n "Redis server running: "
if pgrep -x "redis-server" > /dev/null; then
    echo "✓ YES"
else
    echo "✗ NO"
    exit 1
fi

# Check PING response
echo -n "Redis responds to PING: "
if redis-cli ping 2>/dev/null | grep -q "PONG"; then
    echo "✓ PONG"
else
    echo "✗ FAILED"
    exit 1
fi

# Check version
echo -n "Redis version: "
redis-cli INFO server 2>/dev/null | grep redis_version | cut -d: -f2

# Check persistence
echo -n "Persistence enabled: "
if redis-cli CONFIG GET appendonly 2>/dev/null | grep -q "yes"; then
    echo "✓ AOF"
else
    echo "RDB only or disabled"
fi

echo "=== Verification Complete ==="
```

### Debug Checklist

```markdown
□ Redis package installed?
□ Service started and enabled?
□ Correct port binding?
□ No port conflicts?
□ Correct file permissions?
□ Config file syntax valid?
□ Memory overcommit enabled?
□ Firewall allows connections?
```

---

## Error Codes Reference

| Code | Name | Description | Recovery |
|------|------|-------------|----------|
| I001 | PKG_NOT_FOUND | Package not available | Add official repo |
| I002 | PORT_IN_USE | Port 6379 occupied | Kill process or change port |
| I003 | PERMISSION | Access denied | Fix ownership/permissions |
| I004 | CONFIG_INVALID | Bad config syntax | Check redis.conf |
| I005 | SERVICE_FAIL | Service won't start | Check logs |

---

## Test Template

```bash
#!/bin/bash
# test-redis-installation.sh

set -e

echo "Running Redis installation tests..."

# Test 1: Server responds
test_ping() {
    result=$(redis-cli ping)
    [ "$result" = "PONG" ] && echo "PASS: ping" || { echo "FAIL: ping"; exit 1; }
}

# Test 2: Can write/read
test_write_read() {
    redis-cli SET test:key "value" > /dev/null
    result=$(redis-cli GET test:key)
    redis-cli DEL test:key > /dev/null
    [ "$result" = "value" ] && echo "PASS: write/read" || { echo "FAIL: write/read"; exit 1; }
}

# Test 3: Version check
test_version() {
    version=$(redis-cli INFO server | grep redis_version | cut -d: -f2 | tr -d '\r')
    [[ "$version" =~ ^[67]\. ]] && echo "PASS: version $version" || { echo "FAIL: version"; exit 1; }
}

test_ping
test_write_read
test_version

echo "All tests passed!"
```
