---
name: LAYER_05_TECH
description: Expert knowledge for Technology Layer modeling in Documentation Robotics
triggers:
  [
    "infrastructure",
    "node",
    "kubernetes",
    "docker",
    "server",
    "database",
    "technology service",
    "network",
    "cloud",
    "terraform",
    "archimate technology",
  ]
version: 0.6.0
---

# Technology Layer Skill

**Layer Number:** 05
**Specification:** Metadata Model Spec v0.6.0
**Purpose:** Describes the technology infrastructure including hardware, software, networks, and facilities that support applications.

---

## Layer Overview

The Technology Layer captures **infrastructure and platform**:

- **COMPUTE** - Nodes, devices, system software
- **NETWORK** - Communication networks, paths, interfaces
- **STORAGE** - Artifacts (databases, files, configurations)
- **SERVICES** - Technology services (IaaS, PaaS)
- **AUTOMATION** - Infrastructure as Code (Terraform, Ansible, K8s)

This layer uses **ArchiMate 3.2 Technology Layer** standard with optional properties for Infrastructure as Code references, cloud provider specifics, and operational characteristics.

---

## Entity Types

| Entity Type                 | Description                                             | Key Attributes                                                                               |
| --------------------------- | ------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| **Node**                    | Computational or physical resource that hosts artifacts | Types: server, container, vm, kubernetes-cluster, serverless-function, database-cluster      |
| **Device**                  | Physical IT resource with processing capability         | Types: server, workstation, mobile, iot-device, network-device, storage-appliance            |
| **SystemSoftware**          | Software that provides platform for applications        | Types: operating-system, database, middleware, container-runtime, web-server, message-broker |
| **TechnologyCollaboration** | Aggregate of nodes working together                     | Examples: HA Cluster, CDN Network, Service Mesh                                              |
| **TechnologyInterface**     | Point of access where technology services are available | Protocols: HTTP, HTTPS, TCP, UDP, WebSocket, AMQP, MQTT, SQL, gRPC                           |
| **Path**                    | Link between nodes through which they exchange          | Types: network, vpn, direct-connect, internet, peering                                       |
| **CommunicationNetwork**    | Set of structures that connects nodes                   | Types: lan, wan, vpn, internet, cdn, service-mesh, zero-trust-network                        |
| **TechnologyFunction**      | Collection of technology behavior                       | Examples: Load Balancing, Data Replication, Auto-scaling, Monitoring                         |
| **TechnologyProcess**       | Sequence of technology behaviors (CI/CD, provisioning)  | Automation: ansible, terraform, kubernetes, cloudformation, pulumi                           |
| **TechnologyInteraction**   | Unit of collective technology behavior                  | Examples: Database Replication, Cache Synchronization, Failover                              |
| **TechnologyEvent**         | Technology state change                                 | Types: startup, shutdown, failure, scaling, maintenance, alert                               |
| **TechnologyService**       | Externally visible unit of technology functionality     | Types: infrastructure, platform, storage, compute, network, database, messaging              |
| **Artifact**                | Physical piece of data used or produced                 | Types: database, file, configuration, binary, log, backup, docker-image, helm-chart          |

---

## Intra-Layer Relationships

### Structural Relationships

| Source Type             | Predicate       | Target Type           | Example                                           |
| ----------------------- | --------------- | --------------------- | ------------------------------------------------- |
| Device                  | composes        | Node                  | "Physical Server" composes "Virtual Machine"      |
| Node                    | composes        | TechnologyInterface   | "API Server" composes "HTTPS Endpoint"            |
| SystemSoftware          | composes        | TechnologyInterface   | "PostgreSQL" composes "SQL Interface"             |
| Node                    | aggregates      | Device                | Cluster aggregates multiple physical servers      |
| TechnologyCollaboration | aggregates      | Node                  | "K8s Cluster" aggregates "Worker Nodes"           |
| Artifact                | specializes     | Artifact              | "CustomerDatabase" specializes "Database"         |
| Path                    | realizes        | CommunicationNetwork  | "VPN Tunnel" realizes "Secure Network"            |
| TechnologyFunction      | realizes        | TechnologyService     | "Load Balancing" realizes "Load Balancer Service" |
| TechnologyProcess       | realizes        | TechnologyService     | "CI/CD Pipeline" realizes "Deployment Service"    |
| SystemSoftware          | realizes        | TechnologyService     | "PostgreSQL" realizes "Database Service"          |
| Node                    | assigned-to     | TechnologyFunction    | "Edge Server" assigned to "CDN Caching"           |
| TechnologyCollaboration | assigned-to     | TechnologyInteraction | Cluster performs replication                      |
| Path                    | associated-with | Node                  | Network path connects nodes                       |
| Device                  | associated-with | CommunicationNetwork  | Device connected to network                       |
| TechnologyInterface     | serves          | TechnologyService     | Interface provides service access                 |

### Behavioral Relationships

| Source Type           | Predicate | Target Type        | Example                                             |
| --------------------- | --------- | ------------------ | --------------------------------------------------- |
| TechnologyEvent       | triggers  | TechnologyProcess  | "Node Failure" triggers "Failover Process"          |
| TechnologyEvent       | triggers  | TechnologyFunction | "CPU Threshold" triggers "Auto-scaling Function"    |
| TechnologyProcess     | triggers  | TechnologyEvent    | "Deployment Complete" triggers "Health Check Event" |
| TechnologyProcess     | flows-to  | TechnologyProcess  | "Build" flows to "Deploy"                           |
| TechnologyService     | flows-to  | TechnologyService  | Service dependency chain                            |
| SystemSoftware        | accesses  | Artifact           | "Database" accesses "Data Files"                    |
| TechnologyFunction    | accesses  | Artifact           | "Backup Function" accesses "Backup Files"           |
| TechnologyProcess     | accesses  | Artifact           | "Deployment" accesses "Docker Images"               |
| TechnologyInteraction | accesses  | Artifact           | "Replication" accesses "Database Replica"           |

---

## Cross-Layer References

### Outgoing References (Technology → Other Layers)

| Target Layer              | Reference Type                                     | Example                                |
| ------------------------- | -------------------------------------------------- | -------------------------------------- |
| **Layer 1 (Motivation)**  | TechnologyService supports **Goal**                | Infrastructure supports business goals |
| **Layer 1 (Motivation)**  | TechnologyService governed by **Principle**        | Cloud-native principle                 |
| **Layer 1 (Motivation)**  | Node governed by **Principle**                     | Infrastructure principles              |
| **Layer 1 (Motivation)**  | Node constrained by **Constraint**                 | Budget, region, compliance constraints |
| **Layer 1 (Motivation)**  | Node fulfills **Requirement**                      | Performance, availability requirements |
| **Layer 1 (Motivation)**  | SystemSoftware governed by **Principle**           | Open-source principle                  |
| **Layer 1 (Motivation)**  | SystemSoftware constrained by **Constraint**       | Licensing, version constraints         |
| **Layer 1 (Motivation)**  | SystemSoftware fulfills **Requirement**            | Technical requirements                 |
| **Layer 1 (Motivation)**  | CommunicationNetwork governed by **Principle**     | Zero-trust principle                   |
| **Layer 1 (Motivation)**  | CommunicationNetwork constrained by **Constraint** | Network segmentation                   |
| **Layer 1 (Motivation)**  | Artifact constrained by **Constraint**             | Data residency, retention              |
| **Layer 4 (Application)** | Node hosts **ApplicationComponent**                | K8s pod hosts service                  |
| **Layer 4 (Application)** | TechnologyService serves **ApplicationService**    | Database serves application            |
| **Layer 4 (Application)** | Artifact stores **DataObject**                     | Database stores application data       |
| **Layer 3 (Security)**    | Artifact has **encryption** property               | Data-at-rest encryption                |
| **Layer 3 (Security)**    | Artifact has **classification** property           | Data classification level              |
| **Layer 3 (Security)**    | Artifact has **pii** property                      | Contains PII                           |
| **Layer 3 (Security)**    | CommunicationNetwork has **security-policy**       | Network security rules                 |
| **Layer 11 (APM)**        | TechnologyService has **sla-target**               | Availability, latency targets          |
| **Layer 11 (APM)**        | TechnologyService has **health-check**             | Health monitoring endpoint             |
| **Layer 11 (APM)**        | Node has **monitoring-agent**                      | APM agent installation                 |

### Incoming References (Lower Layers → Technology)

Lower layers reference Technology layer to show:

- Applications depend on infrastructure
- APIs run on technology platforms
- Data stored in technology artifacts

---

## Codebase Detection Patterns

### Pattern 1: Kubernetes Deployment

```yaml
# Kubernetes deployment manifest
apiVersion: apps/v1
kind: Deployment
metadata:
  name: user-service
  namespace: production
spec:
  replicas: 3
  selector:
    matchLabels:
      app: user-service
  template:
    metadata:
      labels:
        app: user-service
    spec:
      containers:
        - name: user-service
          image: myregistry/user-service:1.0.0
          ports:
            - containerPort: 8080
```

**Maps to:**

- Node: "K8s Cluster Production" (type: kubernetes-cluster)
- Node: "User Service Pod" (type: container)
- Artifact: "myregistry/user-service:1.0.0" (type: docker-image)
- TechnologyInterface: "Port 8080" (protocol: HTTP)

### Pattern 2: Terraform Infrastructure

```hcl
# Terraform AWS infrastructure
resource "aws_instance" "web_server" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.medium"
  availability_zone = "us-east-1a"

  tags = {
    Name = "Web Server"
    Environment = "production"
  }
}

resource "aws_db_instance" "postgres" {
  engine         = "postgres"
  engine_version = "14.7"
  instance_class = "db.t3.medium"
  storage_type   = "gp3"
}
```

**Maps to:**

- Node: "Web Server EC2" (type: server, provider: aws, instance-type: t3.medium, region: us-east-1, az: us-east-1a)
- Node: "PostgreSQL RDS" (type: database-cluster, provider: aws)
- SystemSoftware: "PostgreSQL 14.7" (type: database, version: 14.7)
- Properties: iac-tool=terraform, iac-file=main.tf

### Pattern 3: Docker Compose

```yaml
# docker-compose.yml
version: "3.8"
services:
  api:
    image: myapp/api:latest
    ports:
      - "8080:8080"
    depends_on:
      - postgres
      - redis

  postgres:
    image: postgres:14
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: admin
    volumes:
      - postgres-data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  postgres-data:
```

**Maps to:**

- TechnologyCollaboration: "Docker Compose Stack"
- Node: "API Container" (type: container)
- SystemSoftware: "PostgreSQL 14" (type: database)
- SystemSoftware: "Redis 7" (type: middleware, subtype: cache)
- Artifact: "postgres-data" (type: volume)
- TechnologyInterface: "Redis Port 6379" (protocol: TCP)

### Pattern 4: Database Configuration

```python
# Database connection configuration
DATABASE_CONFIG = {
    "host": "prod-db.example.com",
    "port": 5432,
    "database": "customer_db",
    "user": "app_user",
    "password": "${DB_PASSWORD}",
    "pool_size": 20,
    "max_overflow": 10,
    "pool_timeout": 30
}
```

**Maps to:**

- Node: "Production Database" (type: database-cluster, host: prod-db.example.com)
- SystemSoftware: "PostgreSQL" (type: database, port: 5432)
- Artifact: "customer_db" (type: database)
- TechnologyInterface: "PostgreSQL Interface" (protocol: SQL, port: 5432)
- Properties: pool-size=20, max-overflow=10

### Pattern 5: CI/CD Pipeline

```yaml
# GitHub Actions CI/CD
name: Deploy to Production
on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build Docker image
        run: docker build -t myapp:${{ github.sha }} .
      - name: Push to registry
        run: docker push myregistry/myapp:${{ github.sha }}

  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to Kubernetes
        run: kubectl apply -f k8s/deployment.yaml
```

**Maps to:**

- TechnologyProcess: "CI/CD Pipeline" (pattern: ci-cd, automation: github-actions)
- Sub-processes: "Build", "Deploy"
- TechnologyFunction: "Docker Build", "Kubernetes Deploy"
- Artifact: "Docker Image" (type: docker-image)

### Pattern 6: Load Balancer Configuration

```nginx
# NGINX load balancer
upstream backend {
    least_conn;
    server app1.example.com:8080 weight=1;
    server app2.example.com:8080 weight=1;
    server app3.example.com:8080 weight=1;
}

server {
    listen 443 ssl;
    server_name api.example.com;

    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;

    location / {
        proxy_pass http://backend;
    }
}
```

**Maps to:**

- Node: "NGINX Load Balancer" (type: server)
- SystemSoftware: "NGINX" (type: web-server, subtype: load-balancer)
- TechnologyFunction: "Load Balancing" (strategy: least-conn)
- TechnologyInterface: "HTTPS Endpoint" (protocol: HTTPS, port: 443)
- TechnologyCollaboration: "Backend Pool" (aggregates app1, app2, app3)

---

## Modeling Workflow

### Step 1: Identify Infrastructure Nodes

```bash
# Kubernetes cluster
dr add technology node "k8s-cluster-prod" \
  --properties type=kubernetes-cluster,provider=aws,region=us-east-1,version=1.28 \
  --description "Production Kubernetes cluster"

# Virtual machines
dr add technology node "web-server-01" \
  --properties type=vm,provider=aws,instance-type=t3.large,az=us-east-1a \
  --description "Web application server VM"

# Serverless function
dr add technology node "order-processor-lambda" \
  --properties type=serverless-function,provider=aws,runtime=node.11,memory=512 \
  --description "Lambda function for order processing"

# Database cluster
dr add technology node "postgres-cluster" \
  --properties type=database-cluster,provider=aws,instance-class=db.r5.xlarge \
  --description "PostgreSQL RDS cluster"
```

### Step 2: Define System Software

```bash
# Database system
dr add technology system-software "postgresql-14" \
  --properties type=database,version=14.7,license=open-source \
  --description "PostgreSQL relational database"

# Container runtime
dr add technology system-software "docker" \
  --properties type=container-runtime,version=24.0.5 \
  --description "Docker container runtime"

# Web server
dr add technology system-software "nginx" \
  --properties type=web-server,version=1.24.0,subtype=load-balancer \
  --description "NGINX web server and load balancer"

# Message broker
dr add technology system-software "rabbitmq" \
  --properties type=message-broker,version=3.12.0,protocol=AMQP \
  --description "RabbitMQ message broker"
```

### Step 3: Model Technology Services

```bash
# Infrastructure service
dr add technology service "kubernetes-orchestration" \
  --properties type=platform,sla-availability=99.95% \
  --description "Container orchestration platform"

# Database service
dr add technology service "postgres-database" \
  --properties type=database,sla-availability=99.9%,sla-latency=10ms \
  --description "PostgreSQL database service"

# Storage service
dr add technology service "s3-object-storage" \
  --properties type=storage,provider=aws,storage-class=standard \
  --description "S3 object storage for files and backups"

# Link software to service
dr relationship add "technology/system-software/postgresql-14" \
  realizes "technology/service/postgres-database"
```

### Step 4: Define Communication Networks

```bash
# VPC network
dr add technology network "production-vpc" \
  --properties type=lan,provider=aws,cidr=10.0.0.0/16,region=us-east-1 \
  --description "Production VPC network"

# Subnet
dr add technology network "private-subnet-1a" \
  --properties type=lan,cidr=10.0.1.0/24,az=us-east-1a,visibility=private \
  --description "Private subnet in AZ 1a"

# VPN
dr add technology network "site-to-site-vpn" \
  --properties type=vpn,encryption=ipsec,bandwidth=1gbps \
  --description "Site-to-site VPN to on-premise datacenter"
```

### Step 5: Model Artifacts

```bash
# Database artifact
dr add technology artifact "customer-database" \
  --properties type=database,size=500GB,encryption=aes-256,classification=confidential \
  --description "Customer data database"

# Docker image
dr add technology artifact "user-service-image" \
  --properties type=docker-image,registry=ecr.aws,tag=v1.2.3 \
  --description "User service Docker image"

# Configuration file
dr add technology artifact "app-config" \
  --properties type=configuration,format=yaml,version-controlled=true \
  --description "Application configuration file"

# Log files
dr add technology artifact "application-logs" \
  --properties type=log,retention-period=90d,compression=gzip \
  --description "Application log files"

# Link artifact to node
dr relationship add "technology/node/postgres-cluster" \
  stores "technology/artifact/customer-database"
```

### Step 6: Model Infrastructure as Code

```bash
# Terraform process
dr add technology process "provision-infrastructure" \
  --properties pattern=infrastructure-as-code,automation=terraform,repo=github.com/org/infra \
  --description "Terraform infrastructure provisioning"

# Ansible process
dr add technology process "configure-servers" \
  --properties pattern=configuration-management,automation=ansible,playbook=server-config.yml \
  --description "Ansible server configuration"

# Kubernetes deployment process
dr add technology process "deploy-to-k8s" \
  --properties pattern=continuous-deployment,automation=kubectl,manifest=k8s/deploy.yaml \
  --description "Deploy application to Kubernetes"
```

### Step 7: Define Technology Functions

```bash
# Load balancing
dr add technology function "load-balancing" \
  --properties strategy=least-conn,health-check-interval=10s \
  --description "Distribute traffic across backend servers"

# Auto-scaling
dr add technology function "auto-scaling" \
  --properties min-replicas=2,max-replicas=10,cpu-threshold=70% \
  --description "Automatically scale based on CPU utilization"

# Backup
dr add technology function "database-backup" \
  --properties frequency=daily,retention=30d,type=incremental \
  --description "Automated database backup"

# Assign function to node
dr relationship add "technology/node/k8s-cluster-prod" \
  assigned-to "technology/function/auto-scaling"
```

### Step 8: Cross-Layer Integration

```bash
# Link to application layer
dr relationship add "technology/node/k8s-cluster-prod" \
  hosts "application/component/user-service"

# Link to motivation layer
dr relationship add "technology/service/kubernetes-orchestration" \
  supports "motivation/goal/improve-deployment-frequency"

dr relationship add "technology/node/k8s-cluster-prod" \
  governed-by "motivation/principle/cloud-native-architecture"

# Link to APM layer
dr relationship add "technology/service/postgres-database" \
  monitored-by "apm/metric/database-query-latency"
```

### Step 9: Validate

```bash
dr validate --layer technology
dr validate --validate-relationships
```

---

## Cloud Provider Patterns

### AWS Pattern

```
TechnologyCollaboration: "AWS Production Environment"
├── contains → Node: "EKS Cluster" (provider: aws, region: us-east-1)
│   ├── hosts → ApplicationComponent: "Microservices"
│   └── uses → TechnologyService: "EKS Orchestration"
├── contains → Node: "RDS PostgreSQL" (provider: aws, multi-az: true)
│   └── realizes → TechnologyService: "Database Service"
├── contains → Artifact: "S3 Bucket" (provider: aws, storage-class: standard)
└── contains → CommunicationNetwork: "VPC" (cidr: 10.0.0.0/16)
    ├── contains → Subnet: "Public Subnet" (cidr: 10.0.1.0/24)
    └── contains → Subnet: "Private Subnet" (cidr: 10.0.2.0/24)
```

### Kubernetes Pattern

```
Node: "Kubernetes Cluster"
├── type: kubernetes-cluster
├── hosts → Node: "Namespace: production"
│   ├── hosts → Node: "Deployment: user-service"
│   │   ├── replicas: 3
│   │   └── hosts → Node: "Pod: user-service-xyz"
│   │       └── hosts → ApplicationComponent: "UserService"
│   └── uses → Artifact: "ConfigMap: app-config"
└── uses → TechnologyFunction: "Auto-scaling" (HPA)
```

### Hybrid Cloud Pattern

```
TechnologyCollaboration: "Hybrid Cloud Architecture"
├── contains → Node: "AWS EKS Cluster" (provider: aws)
├── contains → Node: "On-Premise K8s" (provider: onprem)
├── connected-by → Path: "Direct Connect" (type: direct-connect)
└── secured-by → CommunicationNetwork: "Zero-Trust Network"
```

---

## Best Practices

1. **Node Types Matter** - server vs container vs serverless have different operational characteristics
2. **Track IaC References** - Link to Terraform, Ansible, Kubernetes manifests
3. **Model HA Clusters** - Use TechnologyCollaboration for high-availability setups
4. **Network Segmentation** - Model VPCs, subnets, security zones explicitly
5. **Artifact Encryption** - Mark encryption status (at-rest, in-transit, both)
6. **Version Everything** - Track software versions, image tags, schema versions
7. **Link to Motivation** - Infrastructure choices trace to principles and constraints
8. **Monitor SLAs** - Technology services have availability and latency targets
9. **Document Automation** - Reference IaC tools and CI/CD pipelines
10. **Cloud-Agnostic When Possible** - Use ArchiMate types rather than provider-specific terms

---

## Infrastructure as Code Integration

When infrastructure is managed as code:

```yaml
technology-node:
  id: "k8s-cluster-prod"
  type: "kubernetes-cluster"
  properties:
    iac-tool: "terraform"
    iac-file: "infrastructure/eks-cluster.tf"
    iac-module: "eks-cluster"
    iac-version: "4.0.0"
    provider: "aws"
    region: "us-east-1"
```

**IaC Tools Supported:**

- **Terraform** - Declarative infrastructure
- **Ansible** - Configuration management
- **Kubernetes** - Container orchestration manifests
- **CloudFormation** - AWS-specific IaC
- **Pulumi** - Programming language IaC
- **Helm** - Kubernetes package manager

---

## Validation Tips

| Issue                  | Cause                                               | Fix                                    |
| ---------------------- | --------------------------------------------------- | -------------------------------------- |
| Orphaned Node          | Node not hosting applications or realizing services | Link to application layer or remove    |
| Unhosted Application   | ApplicationComponent not deployed to any node       | Add deployment link to technology node |
| Missing Networks       | Nodes exist but no network connectivity             | Model CommunicationNetwork and Paths   |
| Untracked Artifacts    | Databases, images, configs not modeled              | Add Artifact entities                  |
| No IaC Reference       | Infrastructure lacks automation reference           | Add iac-tool and iac-file properties   |
| Missing SLA Targets    | Services lack availability/latency targets          | Add SLA properties for monitoring      |
| No Security Properties | Artifacts lack encryption/classification            | Add security properties                |

---

## Quick Reference

**Add Commands:**

```bash
dr add technology node <name> --properties type=<type>,provider=<provider>
dr add technology system-software <name> --properties type=<type>,version=<version>
dr add technology service <name> --properties type=<type>,sla-availability=<value>
dr add technology network <name> --properties type=<type>,cidr=<cidr>
dr add technology artifact <name> --properties type=<type>,encryption=<encryption>
dr add technology function <name> --properties strategy=<strategy>
dr add technology process <name> --properties automation=<tool>
```

**Relationship Commands:**

```bash
dr relationship add <node> hosts <application-component>
dr relationship add <system-software> realizes <service>
dr relationship add <node> assigned-to <function>
dr relationship add <node> stores <artifact>
dr relationship add <network> connects <node>
```

**Cross-Layer Commands:**

```bash
dr relationship add technology/<node> hosts application/<component>
dr relationship add technology/<service> supports motivation/<goal>
dr relationship add technology/<node> governed-by motivation/<principle>
dr relationship add technology/<service> monitored-by apm/<metric>
```
