---
name: cloud-devops-skill
description: Master cloud platforms (AWS, GCP, Azure), containerization (Docker), orchestration (Kubernetes), infrastructure as code, CI/CD pipelines, and DevOps practices for deploying and managing scalable applications.
---

# Cloud & DevOps Skill

Complete guide to deploying, managing, and scaling applications using cloud platforms and DevOps practices.

## Quick Start

### Learning Path

```
Linux → Docker → Kubernetes → AWS/GCP
  ↓        ↓         ↓          ↓
Admin  Container  Orchestrate  Deploy
```

### Get Started in 5 Steps

1. **Linux Fundamentals** (2-3 weeks)
   - Command line
   - File systems, users, permissions

2. **Docker Containerization** (3-4 weeks)
   - Images and containers
   - Docker Compose

3. **Kubernetes Basics** (4-6 weeks)
   - Pods, Services, Deployments
   - ConfigMaps, Secrets

4. **Cloud Platform (AWS)** (6-8 weeks)
   - EC2, S3, RDS
   - VPC, Load Balancing

5. **CI/CD & IaC** (ongoing)
   - GitHub Actions, Jenkins
   - Terraform, CloudFormation

---

## Linux System Administration

### **Command Line Essentials**

```bash
# Navigation and file operations
pwd                           # Current directory
ls -la                        # List files (all, long format)
cd /path/to/directory        # Change directory
mkdir my-folder              # Create directory
cp source.txt dest.txt       # Copy file
mv old-name.txt new-name.txt # Move/rename
rm file.txt                  # Delete file
cat file.txt                 # Display file contents
grep "search-term" file.txt  # Search in file
find /path -name "*.log"     # Find files

# Permissions (chmod)
chmod 755 script.sh          # rwxr-xr-x (user, group, others)
# 7 = rwx, 5 = r-x, 4 = r--, 6 = rw-, 0 = ---

# User and group management
sudo useradd alice           # Add user
sudo usermod -aG sudo alice  # Add to sudo group
sudo passwd alice            # Change password
```

### **Process Management**

```bash
ps aux                       # List all processes
top                          # Real-time process monitor
htop                         # Enhanced top
kill 1234                    # Kill process by PID
pkill -f process-name        # Kill by name

# Foreground/background
cmd &                        # Run in background
fg                           # Bring to foreground
jobs                         # List background jobs
Ctrl+Z                       # Pause process
```

### **Package Management**

```bash
# Debian/Ubuntu (apt)
sudo apt update              # Update package list
sudo apt install nginx       # Install package
sudo apt upgrade             # Upgrade packages
sudo apt remove nginx        # Remove package

# RHEL/CentOS (yum)
sudo yum install nginx
sudo yum update
```

### **Networking**

```bash
ip addr                      # Show IP addresses
ping google.com              # Test connectivity
netstat -tlnp                # List listening ports
ss -tlnp                     # Modern alternative
ssh user@host                # Remote login
scp file.txt user@host:/path # Copy over SSH

# Firewall (ufw)
sudo ufw enable
sudo ufw allow 22/tcp        # Allow SSH
sudo ufw allow 80/tcp        # Allow HTTP
sudo ufw status
```

---

## Docker Containerization

### **Docker Basics**

```dockerfile
# Dockerfile - Define application container
FROM python:3.9-slim

WORKDIR /app

# Copy files
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Environment variables
ENV FLASK_APP=app.py
ENV PORT=5000

# Expose port
EXPOSE 5000

# Run application
CMD ["python", "app.py"]
```

### **Docker Commands**

```bash
# Build image
docker build -t my-app:1.0 .

# Run container
docker run -p 5000:5000 -e ENV=production my-app:1.0

# Useful flags
-d               # Detached (background)
-it              # Interactive + terminal
-v /host:/container  # Volume mount
--name my-container   # Give container name
-e VAR=value     # Environment variable

# Container management
docker ps        # Running containers
docker ps -a     # All containers
docker logs container-id  # View logs
docker exec -it container-id bash  # Execute command

# Push to registry
docker tag my-app:1.0 myregistry.com/my-app:1.0
docker push myregistry.com/my-app:1.0
```

### **Docker Compose**

```yaml
version: '3.8'

services:
  web:
    image: my-app:1.0
    ports:
      - "5000:5000"
    environment:
      DATABASE_URL: postgresql://user:pass@db:5432/mydb
    depends_on:
      - db

  db:
    image: postgres:13
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: mydb
    volumes:
      - postgres-data:/var/lib/postgresql/data

volumes:
  postgres-data:
```

```bash
docker-compose up              # Start services
docker-compose down            # Stop services
docker-compose logs -f web     # View logs
```

---

## Kubernetes (K8s)

### **Core Concepts**

```yaml
# Pod - Smallest unit in K8s
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
spec:
  containers:
  - name: app
    image: my-app:1.0
    ports:
    - containerPort: 5000
```

```yaml
# Deployment - Manage pods, scaling, updates
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 3  # 3 pods
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
      - name: app
        image: my-app:1.0
        ports:
        - containerPort: 5000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: url
        resources:
          requests:
            memory: "64Mi"
            cpu: "250m"
          limits:
            memory: "128Mi"
            cpu: "500m"
```

```yaml
# Service - Expose pods, load balancing
apiVersion: v1
kind: Service
metadata:
  name: my-app-service
spec:
  type: LoadBalancer  # Or ClusterIP, NodePort
  selector:
    app: my-app
  ports:
  - port: 80
    targetPort: 5000
```

```yaml
# ConfigMap & Secret
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  log_level: "info"
  max_connections: "100"
---
apiVersion: v1
kind: Secret
metadata:
  name: db-secret
type: Opaque
data:
  username: dXNlcg==  # base64 encoded
  password: cGFzcw==
```

### **Kubernetes Commands**

```bash
# Create and delete
kubectl apply -f deployment.yaml   # Apply configuration
kubectl delete -f deployment.yaml  # Delete resource
kubectl create namespace prod      # Create namespace

# View resources
kubectl get pods                   # List pods
kubectl get services              # List services
kubectl get deployments           # List deployments
kubectl describe pod my-pod       # Detailed info
kubectl logs my-pod              # Container logs
kubectl logs -f my-pod           # Follow logs

# Port forwarding
kubectl port-forward pod/my-pod 5000:5000

# Scaling
kubectl scale deployment my-app --replicas=5

# Rolling update
kubectl set image deployment/my-app app=my-app:2.0 --record
kubectl rollout status deployment/my-app
kubectl rollout undo deployment/my-app  # Revert
```

---

## AWS (Amazon Web Services)

### **Key Services**

**Compute:**
```
EC2 - Virtual machines
Lambda - Serverless functions
ECS - Container orchestration
EKS - Kubernetes on AWS
```

**Storage:**
```
S3 - Object storage (unlimited)
EBS - Block storage (attached to EC2)
EFS - File system
Glacier - Archival storage
```

**Database:**
```
RDS - Relational (PostgreSQL, MySQL, Oracle)
DynamoDB - NoSQL
Elasticache - Redis/Memcached caching
Redshift - Data warehouse
```

**Networking:**
```
VPC - Virtual network
CloudFront - CDN
Route53 - DNS
ELB/ALB - Load balancing
```

### **EC2 Instance Management**

```bash
# Using AWS CLI
aws ec2 describe-instances
aws ec2 run-instances --image-id ami-0c55b159cbfafe1f0 --count 1 --instance-type t2.micro

# SSH into instance
ssh -i my-key.pem ec2-user@instance-ip
```

### **S3 Usage**

```python
import boto3

s3 = boto3.client('s3')

# Upload file
s3.upload_file('local.txt', 'my-bucket', 'remote.txt')

# Download file
s3.download_file('my-bucket', 'remote.txt', 'local.txt')

# List objects
response = s3.list_objects_v2(Bucket='my-bucket')
for obj in response.get('Contents', []):
    print(obj['Key'])
```

---

## Infrastructure as Code (IaC)

### **Terraform**

```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

# Create S3 bucket
resource "aws_s3_bucket" "my_bucket" {
  bucket = "my-unique-bucket-name"

  tags = {
    Name        = "My bucket"
    Environment = "Dev"
  }
}

# Create EC2 instance
resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t2.micro"

  tags = {
    Name = "Web Server"
  }
}

# Outputs
output "bucket_name" {
  value = aws_s3_bucket.my_bucket.id
}

output "instance_ip" {
  value = aws_instance.web.public_ip
}
```

```bash
# Terraform commands
terraform init               # Initialize
terraform plan              # Preview changes
terraform apply             # Apply changes
terraform destroy           # Destroy resources
```

---

## CI/CD Pipelines

### **GitHub Actions**

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - uses: actions/setup-python@v2
        with:
          python-version: 3.9

      - run: pip install -r requirements.txt
      - run: pytest

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Build Docker image
        run: docker build -t my-app:${{ github.sha }} .

      - name: Push to registry
        run: |
          docker tag my-app:${{ github.sha }} myregistry.com/my-app:latest
          docker push myregistry.com/my-app:latest

  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to Kubernetes
        run: kubectl apply -f k8s/
```

### **Jenkins Pipeline**

```groovy
pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                sh 'docker build -t my-app:${BUILD_NUMBER} .'
            }
        }

        stage('Test') {
            steps {
                sh 'docker run my-app:${BUILD_NUMBER} pytest'
            }
        }

        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                sh 'docker push myregistry.com/my-app:${BUILD_NUMBER}'
                sh 'kubectl set image deployment/my-app app=myregistry.com/my-app:${BUILD_NUMBER}'
            }
        }
    }
}
```

---

## DevOps Best Practices

**Monitoring:**
- Prometheus for metrics
- Grafana for dashboards
- ELK/Datadog for logs
- Alerting (PagerDuty, Opsgenie)

**Security:**
- Least privilege access (IAM)
- Secrets management (HashiCorp Vault)
- Image scanning
- Network policies

**Reliability:**
- Backup and disaster recovery
- Load balancing
- Health checks
- Auto-scaling policies

---

## Learning Checklist

- [ ] Comfortable with Linux command line
- [ ] Can write Dockerfile
- [ ] Understand Docker Compose
- [ ] Know K8s basics (Pods, Services, Deployments)
- [ ] Can deploy app to Kubernetes
- [ ] Familiar with AWS console
- [ ] Can provision resources with Terraform
- [ ] Built simple CI/CD pipeline
- [ ] Understand monitoring and logging
- [ ] Ready for DevOps engineer role!

---

**Source**: https://roadmap.sh/devops, https://roadmap.sh/aws, https://roadmap.sh/docker, https://roadmap.sh/kubernetes
