---
name: iaas
description: Infrastructure as a Service cloud computing
license: MIT
compatibility: opencode
metadata:
  audience: developer, devops-engineer
  category: devops
---

## What I do

- Provision and manage cloud infrastructure (compute, storage, network)
- Configure virtual machines and networking
- Set up managed databases and storage services
- Implement identity and access management
- Configure security groups and firewall rules
- Optimize infrastructure costs and performance

## When to use me

- When you need full control over infrastructure
- When migrating legacy applications
- When running custom or unsupported workloads
- When building lift-and-shift solutions
- When requiring dedicated hardware
- When implementing custom security requirements

## Key Concepts

### Virtual Machine Provisioning

```hcl
# Terraform - AWS EC2
resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.micro"
  subnet_id     = aws_subnet.public.id
  
  vpc_security_group_ids = [aws_security_group.web.id]
  
  tags = {
    Name        = "WebServer"
    Environment = "production"
  }
  
  root_block_device {
    volume_size = 20
    volume_type = "gp3"
    encrypted   = true
  }
}

# GCP Compute Engine
resource "google_compute_instance" "web" {
  name         = "web-server"
  machine_type = "e2-medium"
  zone         = "us-central1-a"
  
  boot_disk {
    initialize_params {
      image = "debian-11-bullseye-v20220719"
      size  = 20
    }
  }
  
  network_interface {
    network = "default"
    access_config {
      // Ephemeral IP
    }
  }
}

# Azure VM
resource "azurerm_virtual_machine" "web" {
  name                  = "web-server"
  location              = "eastus"
  resource_group_name   = azurerm_resource_group.main.name
  vm_size               = "Standard_B1s"
  
  storage_os_disk {
    name              = "osdisk"
    managed_disk_type = "Standard_LRS"
    disk_size_gb      = 30
  }
  
  os_profile {
    computer_name  = "webserver"
    admin_username = "admin"
  }
  
  os_profile_linux_config {
    disable_password_authentication = true
  }
}
```

### Networking

```hcl
# VPC with subnets
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true
}

resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = true
  
  tags = {
    Type = "Public"
  }
}

resource "aws_subnet" "private" {
  vpc_id     = aws_vpc.main.id
  cidr_block = "10.0.2.0/24"
  
  tags = {
    Type = "Private"
  }
}

# Internet Gateway
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id
  
  tags = {
    Name = "Main IGW"
  }
}
```

### Managed Databases

```hcl
# RDS PostgreSQL
resource "aws_db_instance" "postgres" {
  identifier             = "mydb"
  engine                 = "postgres"
  engine_version         = "15.3"
  instance_class         = "db.t3.micro"
  
  allocated_storage     = 20
  max_allocated_storage = 100
  
  db_name  = "mydb"
  username = "dbadmin"
  password = var.db_password
  
  vpc_security_group_ids = [aws_security_group.rds.id]
  db_subnet_group_name   = aws_db_subnet_group.main.name
  
  backup_retention_period = 7
  skip_final_snapshot     = false
  final_snapshot_identifier = "mydb-final"
  
  enabled_cloudwatch_logs_exports = ["postgresql", "upgrade"]
}
```

### IaaS vs PaaS vs SaaS

| Layer | Responsibility | Examples |
|-------|---------------|----------|
| IaaS | Compute, storage, networking | EC2, GCE, Azure VMs |
| IaaS | OS, middleware, runtime | App Service, Cloud Run |
| SaaS | Complete application | Gmail, Office 365 |

### Scaling Options

```hcl
# Auto Scaling Group
resource "aws_autoscaling_group" "web" {
  name                = "web-asg"
  vpc_zone_identifier = [aws_subnet.public.id]
  
  desired_capacity = 2
  max_size         = 10
  min_size         = 2
  
  launch_template {
    id      = aws_launch_template.web.id
    version = "$Latest"
  }
  
  tag {
    key                 = "Name"
    value               = "web-asg"
    propagate_at_launch = true
  }
}

resource "aws_autoscaling_policy" "scale_up" {
  name                   = "scale-up"
  scaling_adjustment     = 1
  adjustment_type        = "ChangeInCapacity"
  cooldown               = 300
  autoscaling_group_name = aws_autoscaling_group.web.name
}
```

### Security Considerations

- Use IAM roles, not access keys
- Enable encryption at rest
- Configure network ACLs
- Implement VPC flow logs
- Regular patching and updates
- Use Bastion hosts for access
