---
name: digitalocean-droplet-deployment
description: Generic DigitalOcean droplet deployment using doctl CLI for any application type (APIs, web servers, background workers). Includes validation, deployment scripts, systemd service management, secret handling, health checks, and deployment tracking. Use when deploying Python/Node.js/any apps to droplets, managing systemd services, handling secrets securely, or when user mentions droplet deployment, doctl, systemd, or server deployment.
allowed-tools: Bash, Read, Write, Edit
---

# DigitalOcean Droplet Deployment Skill

This skill provides comprehensive deployment lifecycle management for applications deployed directly to DigitalOcean droplets using doctl CLI and systemd service management.

## Overview

The deployment lifecycle consists of five phases:
1. **Pre-Deployment Validation** - Application readiness, dependencies, configuration
2. **Secret Management** - Secure environment variable handling via doctl
3. **Deployment** - Code transfer, dependency installation, service setup
4. **Service Management** - Systemd service configuration and control
5. **Post-Deployment Verification** - Health checks, service status validation

## Supported Application Types

- **Python**: Flask, FastAPI, Django, background workers, scripts
- **Node.js**: Express, Fastify, Next.js (standalone), background workers
- **Generic**: Any application that can run as a systemd service

## Available Scripts

### 1. Application Validation

**Script**: `scripts/validate-app.sh <app-path>`

**Purpose**: Validates application is ready for deployment

**Checks**:
- Application entry point exists (server.py, app.py, index.js, server.js)
- Dependencies declared (requirements.txt, package.json)
- Environment configuration (.env.example present)
- No hardcoded secrets
- Valid Python/Node.js syntax
- Port configuration

**Usage**:
```bash
# Validate Python app
./scripts/validate-app.sh /path/to/python-app

# Validate Node.js app
./scripts/validate-app.sh /path/to/nodejs-app

# Verbose mode
VERBOSE=1 ./scripts/validate-app.sh .
```

**Exit Codes**:
- `0`: Validation passed
- `1`: Validation failed (must fix before deployment)

### 2. Deploy to Droplet

**Script**: `scripts/deploy-to-droplet.sh <app-path> <droplet-ip> <app-name>`

**Purpose**: Deploys application to DigitalOcean droplet

**Actions**:
- Validates doctl authentication
- Creates application directory on droplet
- Transfers code via rsync
- Creates secure environment file
- Installs dependencies
- Sets up systemd service
- Starts and enables service
- Verifies service is running

**Usage**:
```bash
# Deploy Python app
./scripts/deploy-to-droplet.sh /path/to/app 137.184.196.101 myapp

# Deploy with custom port
PORT=8080 ./scripts/deploy-to-droplet.sh /path/to/app 137.184.196.101 myapp

# Deploy with specific Python version
PYTHON_VERSION=3.11 ./scripts/deploy-to-droplet.sh /path/to/app 137.184.196.101 myapp

# Deploy Node.js app
APP_TYPE=nodejs ./scripts/deploy-to-droplet.sh /path/to/app 137.184.196.101 myapp
```

**Environment Variables**:
- `APP_TYPE`: `python` or `nodejs` (auto-detected if not specified)
- `PORT`: Port to run on (default: 8000)
- `PYTHON_VERSION`: Python version (default: 3.11)
- `NODE_VERSION`: Node.js version (default: 20)
- `SERVICE_USER`: User to run service as (default: root)
- `APP_DIR`: Target directory on droplet (default: `/opt/<app-name>`)

**Required Environment Variables** (must be set before running):
- All environment variables from `.env.example` must be provided
- Script will prompt for missing variables or use .env file if present

**Exit Codes**:
- `0`: Deployment successful
- `1`: Deployment failed

### 3. Update Secrets

**Script**: `scripts/update-secrets.sh <droplet-ip> <app-name>`

**Purpose**: Updates environment variables without redeploying code

**Actions**:
- Prompts for updated environment variables
- Securely updates .env file on droplet
- Restarts service to apply changes
- Verifies service restarted successfully

**Usage**:
```bash
# Update secrets interactively
./scripts/update-secrets.sh 137.184.196.101 myapp

# Update from local .env file
ENV_FILE=.env.production ./scripts/update-secrets.sh 137.184.196.101 myapp
```

**Exit Codes**:
- `0`: Secrets updated successfully
- `1`: Update failed

### 4. Health Check

**Script**: `scripts/health-check.sh <droplet-ip> <app-name> [port]`

**Purpose**: Validates deployment health and service status

**Checks**:
- Systemd service status (active/running)
- HTTP endpoint responding (if applicable)
- Process running with correct user
- Log file accessible
- Port listening
- Memory usage
- CPU usage

**Usage**:
```bash
# Check service health
./scripts/health-check.sh 137.184.196.101 myapp

# Check with custom port
./scripts/health-check.sh 137.184.196.101 myapp 8080

# Continuous monitoring (runs every 30s)
MONITOR=true ./scripts/health-check.sh 137.184.196.101 myapp
```

**Exit Codes**:
- `0`: All health checks passed
- `1`: One or more health checks failed

### 5. Manage Deployment

**Script**: `scripts/manage-deployment.sh <action> <droplet-ip> <app-name>`

**Purpose**: Manage deployed application lifecycle

**Actions**:
- `start`: Start the service
- `stop`: Stop the service
- `restart`: Restart the service
- `status`: Show service status
- `logs`: View service logs
- `rollback`: Rollback to previous version
- `remove`: Remove deployment completely

**Usage**:
```bash
# Restart service
./scripts/manage-deployment.sh restart 137.184.196.101 myapp

# View logs (last 100 lines)
./scripts/manage-deployment.sh logs 137.184.196.101 myapp

# View logs (follow)
FOLLOW=true ./scripts/manage-deployment.sh logs 137.184.196.101 myapp

# Rollback to previous version
./scripts/manage-deployment.sh rollback 137.184.196.101 myapp

# Remove deployment
./scripts/manage-deployment.sh remove 137.184.196.101 myapp
```

## Available Templates

### 1. Systemd Service Template

**File**: `templates/systemd-service.template`

**Purpose**: Systemd service file template for any application type

**Variables**:
- `{{APP_NAME}}`: Application name
- `{{APP_DIR}}`: Application directory path
- `{{APP_USER}}`: User to run service as
- `{{APP_TYPE}}`: python or nodejs
- `{{ENTRY_POINT}}`: Main file (server.py, index.js, etc.)
- `{{PORT}}`: Port to run on

**Example**:
```ini
[Unit]
Description={{APP_NAME}} Application
After=network.target

[Service]
Type=simple
User={{APP_USER}}
WorkingDirectory={{APP_DIR}}
Environment="PATH=/usr/local/bin:/usr/bin:/bin"
EnvironmentFile={{APP_DIR}}/.env
ExecStart={{EXEC_START}}
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 2. Environment File Template

**File**: `templates/.env.template`

**Purpose**: Secure environment variable template

**Example**:
```bash
# Application Configuration
PORT=8000
HOST=0.0.0.0
NODE_ENV=production

# API Keys (NEVER commit these)
API_KEY=your_api_key_here
DATABASE_URL=your_database_url_here

# Optional
LOG_LEVEL=info
```

### 3. Deployment Configuration

**File**: `templates/deployment-config.json`

**Purpose**: Track deployments to droplets

**Structure**:
```json
{
  "version": "1.0.0",
  "deployments": [
    {
      "id": "deployment-uuid-here",
      "appName": "myapp",
      "appType": "python",
      "dropletIp": "137.184.196.101",
      "port": 8000,
      "appDirectory": "/opt/myapp",
      "serviceUser": "root",
      "status": "active",
      "deployedAt": "2025-11-02T18:30:00Z",
      "deployedBy": "user@example.com",
      "version": "1.0.0",
      "metadata": {
        "gitCommit": "abc123",
        "gitBranch": "main",
        "pythonVersion": "3.11",
        "entryPoint": "server.py"
      },
      "environmentVariables": [
        {
          "name": "API_KEY",
          "isSet": true,
          "source": "doctl-secrets"
        },
        {
          "name": "PORT",
          "isSet": true,
          "source": "deployment-script"
        }
      ],
      "health": {
        "lastCheck": "2025-11-02T18:35:00Z",
        "status": "healthy",
        "uptime": "5m 30s",
        "memoryUsage": "45MB",
        "cpuUsage": "2%"
      }
    }
  ],
  "metadata": {
    "lastUpdated": "2025-11-02T18:35:00Z",
    "totalDeployments": 1,
    "activeDeployments": 1
  }
}
```

### 4. Deployment Checklist

**File**: `templates/deployment-checklist.md`

**Purpose**: Pre-deployment checklist

**Contents**:
- [ ] doctl installed and authenticated
- [ ] Droplet accessible via SSH
- [ ] Application validated locally
- [ ] All required environment variables identified
- [ ] .env.example created with all required variables
- [ ] No hardcoded secrets in code
- [ ] Dependencies pinned in requirements.txt/package.json
- [ ] Health endpoint implemented (optional but recommended)
- [ ] Logging configured
- [ ] Error handling implemented

## Examples

### Example 1: Python FastAPI App

**File**: `examples/python-fastapi-deployment.md`

**Shows**:
- Complete FastAPI app deployment
- Systemd service setup
- Environment variable management
- Health check endpoint
- Deployment verification

### Example 2: Node.js Express App

**File**: `examples/nodejs-express-deployment.md`

**Shows**:
- Express app deployment
- PM2 vs systemd comparison
- Port configuration
- Log management
- Deployment troubleshooting

### Example 3: Background Worker

**File**: `examples/background-worker-deployment.md`

**Shows**:
- Python background worker deployment
- No HTTP endpoint
- Systemd service configuration
- Log-based health checks
- Process monitoring

## Deployment Workflow

### Initial Deployment

1. **Validate Application**:
   ```bash
   ./scripts/validate-app.sh /path/to/app
   ```

2. **Deploy to Droplet**:
   ```bash
   ./scripts/deploy-to-droplet.sh /path/to/app 137.184.196.101 myapp
   ```

3. **Verify Health**:
   ```bash
   ./scripts/health-check.sh 137.184.196.101 myapp
   ```

### Update Deployment

1. **Update Code**:
   ```bash
   ./scripts/deploy-to-droplet.sh /path/to/app 137.184.196.101 myapp
   ```

2. **Verify Health**:
   ```bash
   ./scripts/health-check.sh 137.184.196.101 myapp
   ```

### Update Secrets Only

1. **Update Secrets**:
   ```bash
   ./scripts/update-secrets.sh 137.184.196.101 myapp
   ```

2. **Verify Service Restarted**:
   ```bash
   ./scripts/manage-deployment.sh status 137.184.196.101 myapp
   ```

## Security Best Practices

1. **Never Hardcode Secrets**: Always use environment variables
2. **Use .env Files**: Store secrets securely on droplet
3. **Restrict File Permissions**: .env files should be 600 (readable only by service user)
4. **Rotate Secrets Regularly**: Use update-secrets.sh to rotate API keys
5. **Use Secure Transfer**: Scripts use doctl SSH for secure transfers
6. **Validate Before Deploy**: Always run validation before deployment
7. **Monitor Logs**: Regularly check logs for security issues

## Troubleshooting

### Service Won't Start

```bash
# Check service status
./scripts/manage-deployment.sh status 137.184.196.101 myapp

# View logs
./scripts/manage-deployment.sh logs 137.184.196.101 myapp

# Common issues:
# - Missing environment variables
# - Port already in use
# - Permission issues
# - Syntax errors in code
```

### Deployment Failed

```bash
# Check doctl authentication
doctl auth list

# Verify droplet accessible
doctl compute ssh 137.184.196.101 --ssh-command "echo 'Connection successful'"

# Re-run with verbose output
VERBOSE=1 ./scripts/deploy-to-droplet.sh /path/to/app 137.184.196.101 myapp
```

### Health Check Failures

```bash
# Check service is running
./scripts/manage-deployment.sh status 137.184.196.101 myapp

# Check logs for errors
./scripts/manage-deployment.sh logs 137.184.196.101 myapp

# Verify port is listening
doctl compute ssh 137.184.196.101 --ssh-command "netstat -tlnp | grep <port>"
```

## Integration with Dev Lifecycle

This skill integrates with:
- `/deployment:prepare` - Pre-deployment validation
- `/deployment:deploy` - Execute deployment
- `/deployment:validate` - Post-deployment verification
- `/deployment:rollback` - Rollback to previous version

## Next Steps

After creating the skill, you should also create:
- `digitalocean-app-deployment` - For App Platform deployments
- Integration with deployment plugin commands
- Agent for automated deployment orchestration
