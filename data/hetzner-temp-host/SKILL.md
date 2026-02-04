---
name: hetzner-temp-host
description: Automate deployment of services from GitHub repositories to temporary Hetzner Cloud hosts with ZeroTier integration. Use this skill when users need to quickly spin up a service from a GitHub repo on a disposable VM, connected to an existing ZeroTier network. Supports Docker Compose deployments with automatic health checks.
---

# Hetzner Temporary Host

## Overview

Rapidly deploy services from GitHub repositories to temporary Hetzner Cloud VMs with automatic ZeroTier network integration. This skill automates the entire workflow: provision a VM, join it to your existing ZeroTier network, clone a GitHub repo, deploy with Docker Compose, and verify the service is healthy. Perfect for testing, demos, or temporary service deployments.

## When to Use This Skill

Use this skill when users request:
- Deploying a service from GitHub to a temporary server
- Quick testing of containerized applications in the cloud
- Creating disposable demo environments
- Deploying services to a specific ZeroTier network
- Setting up temporary infrastructure that can be easily torn down
- Running short-lived services without permanent infrastructure

## Quick Start

To deploy a service from GitHub to a temporary host:

1. **Set required configuration**:
   - Hetzner Cloud API token (from https://console.hetzner.cloud/)
   - ZeroTier API token (from https://my.zerotier.com/account)
   - ZeroTier network ID (from existing network)
   - GitHub repository URL
2. **Copy the Terraform template** from `assets/terraform-hetzner-temp-host/` to working directory
3. **Configure SSH key path** (defaults to `~/.ssh/id_ed25519`)
4. **Deploy** using `scripts/deploy_host.sh` or manually with Terraform
5. **Service automatically deploys** via Docker Compose after host provisioning
6. **Health checks verify** service is running correctly

## Core Capabilities

### 1. Host Configuration

The Terraform templates support flexible host configurations:

**Server Types (CCX Line):**
- `ccx13`: 2 vCPU, 8GB RAM, 80GB NVMe (~$8.90/month, ~$0.012/hour) - Default
- `ccx23`: 4 vCPU, 16GB RAM, 160GB NVMe (~$17.80/month, ~$0.025/hour)
- `ccx33`: 8 vCPU, 32GB RAM, 240GB NVMe (~$35.60/month, ~$0.049/hour)

**Datacenters:**
- `hillsboro`: Hillsboro, OR, USA (hil-dc1) - Default
- `singapore`: Singapore (sin-dc1)
- `germany`: Falkenstein, Germany (fsn1-dc14)

**Example Configuration:**
```hcl
host_name         = "temp-api-server"
server_type       = "ccx13"
datacenter        = "hillsboro"
github_repo_url   = "https://github.com/user/my-service"
zerotier_network  = "1c33c1ced02a5a44"
```

### 2. Service Deployment

**Docker Compose Workflow:**
1. Host provisioned on Hetzner Cloud
2. Docker and Docker Compose automatically installed
3. GitHub repository cloned to `/opt/app`
4. `docker compose up -d` executed in repo directory
5. Health checks verify service started successfully
6. Connection details provided in outputs

**Requirements:**
- Repository must contain a `docker-compose.yml` or `compose.yaml` file
- Service should expose health check endpoint (optional but recommended)
- Public repositories work out of the box
- Private repositories require SSH key or access token configuration

**Supported Deployment Patterns:**
- Single container services
- Multi-container applications
- Services with databases and dependencies
- Applications with volume mounts
- Services requiring environment variables (via .env file in repo)

### 3. ZeroTier Integration

**Join Existing Network:**
- Connects to your pre-configured ZeroTier network
- Automatically installs ZeroTier One client
- Joins specified network and waits for authorization
- Host becomes accessible via ZeroTier IP
- Can be authorized manually or automatically (depending on network settings)

**Configuration Methods:**

**Method A: Environment Variable (Recommended for security)**
```bash
export ZEROTIER_NETWORK_ID='1c33c1ced02a5a44'
export ZEROTIER_API_TOKEN='your-zerotier-api-token'
export HCLOUD_TOKEN='your-hetzner-api-token'
```

**Method B: Terraform Variables**
```hcl
zerotier_network = "1c33c1ced02a5a44"
zerotier_api_token = "your-zerotier-api-token"
```

**Method C: Mixed (Network ID in config, token in env)**
```bash
export ZEROTIER_API_TOKEN='your-zerotier-api-token'
export HCLOUD_TOKEN='your-hetzner-api-token'
```
```hcl
zerotier_network = "1c33c1ced02a5a44"
```

**Authorization:**
- If network has auto-authorization enabled, host joins automatically
- Otherwise, manually authorize at https://my.zerotier.com
- Check authorization status: `zerotier-cli listnetworks`

### 4. Health Checks

**Automatic Service Verification:**
- Checks that Docker containers are running
- Optionally pings HTTP/HTTPS health endpoint
- Verifies ZeroTier connectivity
- Reports status in Terraform outputs

**Health Check Options:**
```hcl
# Basic check (Docker containers running)
health_check_enabled = true

# HTTP endpoint check
health_check_url = "http://localhost:8080/health"
health_check_url = "http://localhost:3000/api/status"

# Disable health checks
health_check_enabled = false
```

**Example Health Check Output:**
```
Outputs:
health_status = {
  "docker_running" = true
  "containers_up" = 3
  "endpoint_healthy" = true
  "zerotier_connected" = true
}
```

### 5. Deployment Methods

**Method A: Using the Helper Script (Recommended)**

The `scripts/deploy_host.sh` script automates the entire deployment:

```bash
# Copy script to working directory
cp scripts/deploy_host.sh .
chmod +x deploy_host.sh

# Set required tokens
export HCLOUD_TOKEN='your-hetzner-api-token'
export ZEROTIER_API_TOKEN='your-zerotier-api-token'
export ZEROTIER_NETWORK_ID='your-network-id'

# Deploy with repository URL
./deploy_host.sh https://github.com/user/my-service

# Deploy with custom configuration
./deploy_host.sh https://github.com/user/my-api my-api-host ccx23 singapore
```

The script will:
1. Verify API tokens and network ID are set
2. Verify SSH key pair exists
3. Generate `terraform.tfvars` with configuration
4. Initialize Terraform
5. Show plan and prompt for confirmation
6. Deploy host and join ZeroTier network
7. Clone repo and deploy with Docker Compose
8. Run health checks
9. Display connection and service information

**Method B: Manual Deployment**

For more control:

1. **Copy Terraform templates:**
   ```bash
   cp -r assets/terraform-hetzner-temp-host/* ./
   ```

2. **Create terraform.tfvars:**
   ```hcl
   hcloud_token        = "your-hetzner-api-token"
   zerotier_api_token  = "your-zerotier-api-token"
   zerotier_network    = "1c33c1ced02a5a44"
   host_name           = "my-temp-host"
   github_repo_url     = "https://github.com/user/my-service"
   server_type         = "ccx13"
   datacenter          = "hillsboro"
   ssh_private_key_path = "~/.ssh/id_ed25519"
   health_check_enabled = true
   health_check_url     = "http://localhost:8080/health"
   ```

3. **Deploy:**
   ```bash
   terraform init
   terraform plan
   terraform apply
   ```

4. **View outputs:**
   ```bash
   terraform output
   terraform output zerotier_ip
   terraform output service_url
   ```

### 6. Accessing the Host and Service

**SSH Access:**
```bash
# Via public IP
ssh root@<public-ip>

# Via ZeroTier IP (after authorization)
ssh root@<zerotier-ip>

# Get SSH command from Terraform
terraform output -raw ssh_command
```

**Service Access:**
```bash
# Get service URL
terraform output service_url

# Access via public IP
curl http://<public-ip>:<port>

# Access via ZeroTier (from any device on the network)
curl http://<zerotier-ip>:<port>
```

**Docker Management:**
```bash
# View running containers
ssh root@<host> 'docker ps'

# View logs
ssh root@<host> 'docker compose -f /opt/app/docker-compose.yml logs'

# Restart services
ssh root@<host> 'docker compose -f /opt/app/docker-compose.yml restart'
```

### 7. Host Management

**Check service status:**
```bash
terraform output health_status
ssh root@<host> 'docker ps'
ssh root@<host> 'zerotier-cli listnetworks'
```

**Redeploy service:**
```bash
ssh root@<host> 'cd /opt/app && git pull && docker compose down && docker compose up -d'
```

**Destroy host:**
```bash
terraform destroy
```

**Cost Management:**
- Hourly billing means you only pay for actual usage
- Always destroy temporary hosts when done
- ccx13 costs ~$0.012/hour (~$0.29/day)
- Set calendar reminders to tear down test environments

## Common Workflows

### Workflow 1: Deploy a Simple Web Service

User request: *"Deploy my web app from GitHub to a temporary server on my ZeroTier network"*

1. Get ZeroTier network ID from https://my.zerotier.com
2. Set environment variables:
   ```bash
   export HCLOUD_TOKEN='...'
   export ZEROTIER_API_TOKEN='...'
   export ZEROTIER_NETWORK_ID='...'
   ```
3. Use helper script:
   ```bash
   ./deploy_host.sh https://github.com/user/webapp my-webapp
   ```
4. Authorize host on ZeroTier Central if needed
5. Access service via ZeroTier IP
6. Destroy when done: `terraform destroy`

### Workflow 2: Test a Multi-Container Application

User request: *"I need to test my microservices stack with Redis and Postgres before deploying to production"*

1. Ensure GitHub repo has complete `docker-compose.yml` with all services
2. Deploy to temporary host:
   ```bash
   ./deploy_host.sh https://github.com/user/microservices test-stack ccx23
   ```
3. Health check verifies all containers are running
4. Access services via public IP or ZeroTier
5. Run integration tests
6. Tear down: `terraform destroy`

### Workflow 3: Demo Environment for Client

User request: *"Create a temporary demo environment for a client presentation tomorrow"*

1. Deploy service to temporary host:
   ```bash
   ./deploy_host.sh https://github.com/company/demo-app client-demo
   ```
2. Get public IP from outputs: `terraform output public_ip`
3. Share URL with client: `http://<public-ip>:<port>`
4. After demo, destroy environment: `terraform destroy`
5. Total cost: ~$0.50 for 2-day deployment

### Workflow 4: Test Feature Branch

User request: *"I want to deploy a feature branch to test it in a real environment"*

1. Push feature branch to GitHub
2. Modify `github_repo_url` in terraform.tfvars:
   ```hcl
   github_repo_url = "https://github.com/user/repo#feature-branch"
   ```
3. Deploy: `terraform apply`
4. Test the feature via ZeroTier network
5. Destroy when testing complete

## Troubleshooting

**SSH key pair not found:**
- Ensure both `~/.ssh/id_ed25519` and `~/.ssh/id_ed25519.pub` exist
- Generate: `ssh-keygen -t ed25519`
- Or set custom path: `export SSH_KEY_PATH="/path/to/key"`

**GitHub clone fails:**
- Public repos: Check URL is correct
- Private repos: Add SSH key to GitHub or use personal access token in URL
- Format: `https://username:token@github.com/user/repo`

**Docker Compose not found in repo:**
- Verify repo contains `docker-compose.yml` or `compose.yaml`
- Check file is in root directory of repo
- Test locally: `git clone <repo> && cd <repo> && docker compose config`

**Containers fail to start:**
- Check logs: `ssh root@<host> 'docker compose -f /opt/app/docker-compose.yml logs'`
- Verify environment variables if needed (add .env file to repo)
- Check resource requirements match server type
- Verify all required ports are available

**ZeroTier node not joining:**
- Check network ID is correct
- Verify ZeroTier API token has permissions
- Wait 30-60 seconds for service to start
- Check status: `ssh root@<host> 'zerotier-cli listnetworks'`

**ZeroTier not authorized:**
- Go to https://my.zerotier.com
- Find your network
- Authorize the new member
- Check authorization: `zerotier-cli listnetworks`

**Health checks failing:**
- Verify containers are running: `docker ps`
- Check health endpoint URL is correct
- Ensure service is listening on correct port
- Try accessing directly: `curl http://localhost:<port>`
- Disable health checks temporarily: `health_check_enabled = false`

**Provisioner timeout:**
- Increase timeout in main.tf provisioner blocks
- Check SSH connectivity manually
- Verify firewall rules allow SSH
- Check SSH key permissions: `chmod 600 ~/.ssh/id_ed25519`

## Resources

### scripts/
- `deploy_host.sh`: Complete deployment automation with validation and interactive prompts
- `health_check.sh`: Service health verification script (used by Terraform provisioners)

### assets/
- `terraform-hetzner-temp-host/`: Terraform templates for temporary host deployment
  - `main.tf`: Core infrastructure (server, firewall, ZeroTier, provisioning)
  - `variables.tf`: Input variables with validation and defaults
  - `outputs.tf`: Connection info, service details, health status
  - `versions.tf`: Terraform and provider requirements
  - `terraform.tfvars.example`: Example configuration

## Best Practices

1. **Always destroy temporary hosts** when finished to avoid unnecessary costs
2. **Use environment variables** for secrets (tokens, keys) instead of hardcoding
3. **Enable health checks** to verify successful deployment
4. **Tag hosts appropriately** with descriptive names for easy identification
5. **Set reminders** to tear down test environments after demos/testing
6. **Use ZeroTier** for secure access instead of exposing services publicly
7. **Test locally first** with `docker compose up` before deploying to cloud
8. **Monitor costs** at https://console.hetzner.cloud/
9. **Use appropriate server sizes** - start small, scale up if needed
10. **Document cleanup procedures** for team members

## Cost Examples

Based on Hetzner Cloud hourly billing:

| Scenario | Server | Duration | Cost |
|----------|--------|----------|------|
| Quick test | ccx13 | 2 hours | ~$0.02 |
| Day of testing | ccx13 | 24 hours | ~$0.29 |
| Week demo | ccx13 | 7 days | ~$2.00 |
| Load testing | ccx23 | 4 hours | ~$0.10 |
| Client presentation | ccx13 | 3 days | ~$0.87 |

Remember: Costs accumulate while the host exists. Always `terraform destroy` when finished!
