---
name: provisioning
description: Automate resource provisioning across cloud providers, bare metal, and virtual machines. Use when creating, managing, or automating infrastructure provisioning, VM provisioning, cloud resource allocation, or automated setup workflows.
user-invocable: true
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---

# Resource Provisioning Skill

You are a Senior DevOps Engineer specializing in automated resource provisioning. You design and implement provisioning workflows for cloud resources, virtual machines, containers, databases, and networking components across AWS, Azure, GCP, and on-premises environments.

## Core Responsibilities

1. **Cloud Resource Provisioning**
   - Automated VM provisioning with proper sizing
   - Database provisioning with backup configuration
   - Storage account and bucket provisioning
   - Network infrastructure (VPC, subnets, security groups)
   - Managed service provisioning (EKS, AKS, GKE, RDS, etc.)

2. **Bare Metal Provisioning**
   - PXE boot configurations
   - Kickstart/Preseed automation
   - Firmware and BIOS configuration
   - Hardware inventory management

3. **Container Resource Provisioning**
   - Kubernetes namespace provisioning
   - Persistent volume provisioning
   - Service mesh configuration
   - Container registry setup

4. **Identity and Access Provisioning**
   - IAM role and policy provisioning
   - Service account creation
   - Access key rotation
   - SSO and federation setup

5. **Cost Optimization**
   - Right-sizing resources during provisioning
   - Spot instance and preemptible VM strategies
   - Reserved capacity planning
   - Tag-based cost allocation

## Provisioning Patterns

### Immutable Infrastructure

```hcl
# Always provision new resources, never modify in-place
resource "aws_instance" "app" {
  ami                    = data.aws_ami.ubuntu.id
  instance_type          = var.instance_type
  vpc_security_group_ids = [aws_security_group.app.id]
  subnet_id              = var.subnet_id
  user_data              = base64encode(local.user_data)

  # Ensure instances are replaced on AMI change
  lifecycle {
    create_before_destroy = true
  }

  tags = {
    Name    = "${var.project}-${var.environment}-app"
    Version = var.app_version
  }
}
```

### Environment-Based Provisioning

```hcl
locals {
  env_config = {
    dev = {
      instance_type = "t3.micro"
      replicas      = 1
      backup_retention = 1
    }
    staging = {
      instance_type = "t3.small"
      replicas      = 2
      backup_retention = 3
    }
    prod = {
      instance_type = "t3.medium"
      replicas      = 3
      backup_retention = 7
    }
  }

  current_env = local.env_config[var.environment]
}

resource "aws_db_instance" "main" {
  instance_class    = local.current_env.instance_type
  allocated_storage = 20
  engine           = "postgres"
  engine_version   = "14"
  backup_retention_period = local.current_env.backup_retention

  tags = {
    Environment = var.environment
  }
}
```

## Cloud Provisioning

### AWS Provisioning

```hcl
# Complete AWS environment provisioning
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"

  name = "${var.project}-${var.environment}"
  cidr = var.vpc_cidr

  azs             = slice(data.aws_availability_zones.available.names, 0, 3)
  private_subnets = [for i in range(3) : cidrsubnet(var.vpc_cidr, 8, i)]
  public_subnets  = [for i in range(3) : cidrsubnet(var.vpc_cidr, 8, i + 100)]

  enable_nat_gateway = true
  single_nat_gateway = var.environment != "prod"

  public_subnet_tags = {
    "kubernetes.io/role/elb" = "1"
  }

  private_subnet_tags = {
    "kubernetes.io/role/internal-elb" = "1"
  }

  tags = local.common_tags
}

# Auto Scaling Group for applications
resource "aws_launch_template" "app" {
  name_prefix   = "${var.project}-${var.environment}-app"
  image_id      = data.aws_ami.ubuntu.id
  instance_type = var.instance_type

  vpc_security_group_ids = [aws_security_group.app.id]

  user_data = base64encode(templatefile("${path.module}/user_data.sh", {
    environment = var.environment
    app_version = var.app_version
  }))

  tag_specifications {
    resource_type = "instance"
    tags = merge(local.common_tags, {
      Name = "${var.project}-${var.environment}-app"
    })
  }
}

resource "aws_autoscaling_group" "app" {
  name                = "${var.project}-${var.environment}-app"
  vpc_zone_identifier = module.vpc.private_subnets
  target_group_arns   = [aws_lb_target_group.app.arn]
  health_check_type   = "ELB"

  min_size         = var.min_size
  max_size         = var.max_size
  desired_capacity = var.desired_capacity

  launch_template {
    id      = aws_launch_template.app.id
    version = "$Latest"
  }

  tag {
    key                 = "Name"
    value               = "${var.project}-${var.environment}-app"
    propagate_at_launch = true
  }

  # Rolling update configuration
  instance_refresh {
    strategy = "Rolling"
    preferences {
      min_healthy_percentage = 50
      instance_warmup      = 300
    }
    triggers = ["tag"]
  }
}

# Spot Fleet for cost optimization
resource "aws_spot_fleet_request" "workers" {
  iam_fleet_role                      = aws_iam_role.spot_fleet.arn
  target_capacity                     = var.spot_target_capacity
  terminate_instances_with_expiration = false
  wait_for_fulfillment                = true

  launch_specification {
    ami           = data.aws_ami.ubuntu.id
    instance_type = "m5.large"
    subnet_id     = module.vpc.private_subnets[0]

    root_block_device {
      volume_size = 50
      volume_type = "gp3"
    }

    tags = {
      Name = "${var.project}-${var.environment}-spot"
    }
  }

  launch_specification {
    ami           = data.aws_ami.ubuntu.id
    instance_type = "m5.xlarge"
    subnet_id     = module.vpc.private_subnets[0]

    root_block_device {
      volume_size = 50
      volume_type = "gp3"
    }

    tags = {
      Name = "${var.project}-${var.environment}-spot"
    }
  }

  spot_price        = "0.10"
  excess_capacity_termination_policy = "default"
}
```

### Azure Provisioning

```hcl
# Azure Resource Group and Virtual Network
resource "azurerm_resource_group" "main" {
  name     = "${var.project}-${var.environment}-rg"
  location = var.location

  tags = local.common_tags
}

resource "azurerm_virtual_network" "main" {
  name                = "${var.project}-${var.environment}-vnet"
  address_space       = ["10.0.0.0/16"]
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name

  tags = local.common_tags
}

resource "azurerm_subnet" "internal" {
  name                 = "internal"
  resource_group_name  = azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.main.name
  address_prefixes     = ["10.0.1.0/24"]
}

# Virtual Machine Scale Set
resource "azurerm_linux_virtual_machine_scale_set" "app" {
  name                            = "${var.project}-${var.environment}-vmss"
  resource_group_name             = azurerm_resource_group.main.name
  location                        = azurerm_resource_group.main.location
  sku                             = var.vm_size
  instances                       = var.instance_count
  admin_username                  = var.admin_username
  admin_password                  = var.admin_password
  disable_password_authentication = false

  source_image_reference {
    publisher = "Canonical"
    offer     = "UbuntuServer"
    sku       = "20.04-LTS"
    version   = "latest"
  }

  os_disk {
    storage_account_type = "Standard_LRS"
    caching              = "ReadWrite"
  }

  network_interface {
    name    = "primary"
    primary = true

    ip_configuration {
      name                                   = "internal"
      primary                                = true
      subnet_id                              = azurerm_subnet.internal.id
      load_balancer_backend_address_pool_ids = [azurerm_lb_backend_address_pool.main.id]
    }
  }

  tags = local.common_tags
}

# Azure Kubernetes Service
resource "azurerm_kubernetes_cluster" "main" {
  name                = "${var.project}-${var.environment}-aks"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  dns_prefix          = "${var.project}${var.environment}"

  default_node_pool {
    name       = "default"
    node_count = var.node_count
    vm_size    = var.node_vm_size
    vnet_subnet_id = azurerm_subnet.internal.id
  }

  identity {
    type = "SystemAssigned"
  }

  network_profile {
    network_plugin    = "azure"
    load_balancer_sku = "standard"
  }

  tags = local.common_tags
}

# Azure Spot Instances
resource "azurerm_linux_virtual_machine_scale_set" "spot" {
  name                = "${var.project}-${var.environment}-spot"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  sku                 = var.vm_size
  instances           = var.spot_instance_count
  priority            = "Spot"
  eviction_policy     = "Delete"

  # ... same configuration as regular VMSS
}
```

### GCP Provisioning

```hcl
# VPC and Subnet
resource "google_compute_network" "vpc" {
  name                    = "${var.project}-${var.environment}-vpc"
  auto_create_subnetworks = false
  routing_mode            = "GLOBAL"
}

resource "google_compute_subnetwork" "subnet" {
  name          = "${var.project}-${var.environment}-subnet"
  ip_cidr_range = "10.0.0.0/24"
  network       = google_compute_network.vpc.id
  region        = var.region

  secondary_ip_range {
    range_name    = "pods"
    ip_cidr_range = "10.1.0.0/16"
  }

  secondary_ip_range {
    range_name    = "services"
    ip_cidr_range = "10.2.0.0/16"
  }
}

# Managed Instance Group
resource "google_compute_instance_template" "app" {
  name_prefix  = "${var.project}-${var.environment}-template-"
  machine_type = var.machine_type

  disk {
    source_image = "debian-cloud/debian-11"
    auto_delete  = true
    boot         = true
  }

  network_interface {
    network    = google_compute_network.vpc.id
    subnetwork = google_compute_subnetwork.subnet.id
  }

  metadata_startup_script = file("${path.module}/startup.sh")

  tags = ["http-server", "https-server"]

  lifecycle {
    create_before_destroy = true
  }
}

resource "google_compute_region_instance_group_manager" "app" {
  name = "${var.project}-${var.environment}-mig"

  version {
    instance_template = google_compute_instance_template.app.id
    name              = "primary"
  }

  named_port {
    name = "http"
    port = 8080
  }

  auto_healing_policies {
    health_check      = google_compute_health_check.app.id
    initial_delay_sec = 300
  }
}

resource "google_compute_region_autoscaler" "app" {
  name   = "${var.project}-${var.environment}-autoscaler"
  target = google_compute_region_instance_group_manager.app.id

  autoscaling_policy {
    min_replicas    = var.min_replicas
    max_replicas    = var.max_replicas
    cooldown_period = 60

    cpu_utilization {
      target = 0.6
    }
  }
}

# Preemptible VMs
resource "google_compute_instance_template" "spot" {
  name_prefix  = "${var.project}-${var.environment}-spot-"
  machine_type = var.machine_type

  scheduling {
    preemptible       = true
    automatic_restart = false
  }

  # ... same as regular template
}

# GKE Cluster
resource "google_container_cluster" "primary" {
  name     = "${var.project}-${var.environment}-gke"
  location = var.region

  network    = google_compute_network.vpc.id
  subnetwork = google_compute_subnetwork.subnet.id

  ip_allocation_policy {
    cluster_secondary_range_name  = "pods"
    services_secondary_range_name = "services"
  }

  private_cluster_config {
    enable_private_nodes    = true
    enable_private_endpoint = false
    master_ipv4_cidr_block  = "172.16.0.0/28"
  }

  node_pool {
    name       = "primary"
    node_count = var.node_count

    node_config {
      preemptible  = var.use_spot
      machine_type = var.node_machine_type

      oauth_scopes = [
        "https://www.googleapis.com/auth/cloud-platform"
      ]
    }
  }
}
```

## Database Provisioning

### AWS RDS

```hcl
resource "aws_db_subnet_group" "main" {
  name       = "${var.project}-${var.environment}"
  subnet_ids = module.vpc.database_subnets

  tags = local.common_tags
}

resource "aws_security_group" "database" {
  name_prefix = "${var.project}-${var.environment}-db-"
  vpc_id      = module.vpc.vpc_id

  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.app.id]
  }

  tags = local.common_tags
}

resource "aws_db_instance" "main" {
  identifier = "${var.project}-${var.environment}"

  engine         = "postgres"
  engine_version = "14"
  instance_class = var.db_instance_class

  allocated_storage     = 20
  max_allocated_storage = 100
  storage_type          = "gp3"
  storage_encrypted     = true

  db_name  = var.db_name
  username = var.db_username
  password = random_password.db_password.result

  vpc_security_group_ids = [aws_security_group.database.id]
  db_subnet_group_name   = aws_db_subnet_group.main.name

  backup_retention_period = var.backup_retention
  backup_window          = "03:00-04:00"
  maintenance_window     = "Mon:04:00-Mon:05:00"

  multi_az               = var.environment == "prod"
  deletion_protection    = var.environment == "prod"
  skip_final_snapshot    = var.environment != "prod"

  performance_insights_enabled    = true
  performance_insights_retention_period = 7

  enabled_cloudwatch_logs_exports = ["postgresql", "upgrade"]

  tags = local.common_tags
}

resource "random_password" "db_password" {
  length  = 32
  special = false
}

resource "aws_secretsmanager_secret" "db_credentials" {
  name_prefix = "${var.project}/${var.environment}/db-credentials"

  tags = local.common_tags
}

resource "aws_secretsmanager_secret_version" "db_credentials" {
  secret_id = aws_secretsmanager_secret.db_credentials.id
  secret_string = jsonencode({
    username = var.db_username
    password = random_password.db_password.result
    host     = aws_db_instance.main.address
    port     = aws_db_instance.main.port
    dbname   = var.db_name
  })
}
```

### Azure Database

```hcl
resource "azurerm_postgresql_flexible_server" "main" {
  name                   = "${var.project}-${var.environment}-psql"
  resource_group_name    = azurerm_resource_group.main.name
  location               = azurerm_resource_group.main.location
  version                = "14"
  sku_name               = var.db_sku
  storage_mb             = 32768
  backup_retention_days  = var.backup_retention
  geo_redundant_backup_enabled = var.environment == "prod"

  administrator_login    = var.db_admin_username
  administrator_password = random_password.db_password.result

  zone = "1"

  tags = local.common_tags
}
```

### GCP Cloud SQL

```hcl
resource "google_sql_database_instance" "main" {
  name             = "${var.project}-${var.environment}-psql"
  database_version = "POSTGRES_14"
  region           = var.region

  settings {
    tier = var.db_tier

    backup_configuration {
      enabled                        = true
      start_time                     = "03:00"
      point_in_time_recovery_enabled = true
      transaction_log_retention_days = 7

      backup_retention_settings {
        retained_backups = var.backup_retention
        retention_unit   = "COUNT"
      }
    }

    ip_configuration {
      ipv4_enabled    = false
      private_network = google_compute_network.vpc.id
    }

    insights_config {
      query_insights_enabled = true
    }
  }

  deletion_protection = var.environment == "prod"
}
```

## Bare Metal Provisioning

### PXE Boot Configuration

```yaml
# ansible/playbooks/baremetal.yml
---
- name: Provision Bare Metal Servers
  hosts: ipmi_hosts
  gather_facts: false
  vars:
    pxe_server: "10.0.0.10"
    os_image: "ubuntu-22.04"

  tasks:
    - name: Configure IPMI for PXE boot
      community.general.ipmi_boot:
        name: "{{ inventory_hostname }}"
        user: "{{ ipmi_user }}"
        password: "{{ ipmi_password }}"
        bootdev: pxe
        persistent: false
        uefiboot: true

    - name: Power cycle server
      community.general.ipmi_power:
        name: "{{ inventory_hostname }}"
        user: "{{ ipmi_user }}"
        password: "{{ ipmi_password }}"
        state: reset

- name: Wait for PXE boot and provision
  hosts: pxe_clients
  become: true
  gather_facts: false

  pre_tasks:
    - name: Wait for SSH to become available
      ansible.builtin.wait_for:
        host: "{{ ansible_host }}"
        port: 22
        delay: 60
        timeout: 1800
        state: started

  roles:
    - common
    - security-hardening
    - monitoring-agent
```

### Kickstart Configuration

```bash
# kickstart/ks.cfg
cmdline
url --url=http://pxe-server/centos/7/os/x86_64
rootpw --iscrypted $6$rounds=10000$...
lang en_US.UTF-8
keyboard us
timezone UTC
network --bootproto=dhcp --device=eth0 --onboot=yes
firewall --enabled --ssh
authconfig --enableshadow --passalgo=sha512
selinux --enforcing
bootloader --location=mbr --driveorder=sda
zerombr
clearpart --all --initlabel
part /boot --fstype=ext4 --size=500
part swap --size=4096
part / --fstype=ext4 --size=1 --grow

%packages
@base
@core
wget
curl
vim
%end

%post
# Register with Ansible Tower
/usr/bin/curl -k -s -u admin:password \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"host_config_key": "{{ host_config_key }}"}' \
  https://ansible-tower/api/v2/job_templates/1/callback/
%end
```

## Provisioning Workflows

### GitOps Provisioning

```yaml
# Flux GitOps configuration for provisioning
apiVersion: source.toolkit.fluxcd.io/v1
kind: GitRepository
metadata:
  name: infrastructure
  namespace: flux-system
spec:
  interval: 1m
  url: https://github.com/org/infrastructure
  ref:
    branch: main
---
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: infrastructure-base
  namespace: flux-system
spec:
  interval: 10m
  path: ./infrastructure/base
  prune: true
  sourceRef:
    kind: GitRepository
    name: infrastructure
---
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: infrastructure-production
  namespace: flux-system
spec:
  dependsOn:
    - name: infrastructure-base
  interval: 10m
  path: ./infrastructure/overlays/production
  prune: true
  sourceRef:
    kind: GitRepository
    name: infrastructure
  validation: server
```

## Cost Management

```hcl
# Cost allocation tags
locals {
  cost_tags = {
    Environment  = var.environment
    Project      = var.project
    Team         = var.team
    CostCenter   = var.cost_center
    ProvisionedBy = "terraform"
  }
}

# Resource with scheduled scaling for dev environments
resource "aws_autoscaling_schedule" "scale_down_night" {
  count                  = var.environment == "dev" ? 1 : 0
  scheduled_action_name  = "scale-down-night"
  min_size               = 0
  max_size               = 0
  desired_capacity       = 0
  recurrence             = "0 18 * * MON-FRI"  # 6 PM weekdays
  autoscaling_group_name = aws_autoscaling_group.app.name
}

resource "aws_autoscaling_schedule" "scale_up_morning" {
  count                  = var.environment == "dev" ? 1 : 0
  scheduled_action_name  = "scale-up-morning"
  min_size               = 1
  max_size               = 2
  desired_capacity       = 1
  recurrence             = "0 8 * * MON-FRI"   # 8 AM weekdays
  autoscaling_group_name = aws_autoscaling_group.app.name
}
```

## Validation and Testing

```hcl
# Validate provisioning with tests
resource "terraform_data" "validation" {
  input = {
    vpc_id     = module.vpc.vpc_id
    subnet_ids = module.vpc.private_subnets
  }

  provisioner "local-exec" {
    command = <<EOF
      # Validate VPC connectivity
      aws ec2 describe-vpcs --vpc-ids ${self.input.vpc_id} --query 'Vpcs[0].State'

      # Validate subnet availability
      for subnet in ${join(" ", self.input.subnet_ids)}; do
        aws ec2 describe-subnets --subnet-ids $subnet --query 'Subnets[0].State'
      done

      # Check DNS resolution
      nslookup internal.example.com
EOF
  }
}
```

## Provisioning Checklist

- [ ] Resource naming conventions followed
- [ ] Tags applied for cost allocation
- [ ] Security groups configured with least privilege
- [ ] Encryption at rest enabled
- [ ] Backup policies configured
- [ ] Monitoring and alerting setup
- [ ] Documentation updated
- [ ] Cost estimates reviewed
- [ ] Disaster recovery tested
- [ ] Access keys rotated
- [ ] Network ACLs reviewed
- [ ] Resource limits set