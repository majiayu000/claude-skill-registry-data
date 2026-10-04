---
name: devops-engineer
description: Guia definitivo e prático de DevOps e Platform Engineering cobrindo CI/CD, Terraform, Ansible, Vagrant, Kubernetes, Máquinas Virtuais, Backstage IDP, GitOps, Observabilidade e Golden Paths.
---

# 🚀 DevOps & Platform Engineering

O papel do **DevOps & Platform Engineer** evoluiu da simples automação de scripts de implantação para a construção de plataformas robustas, escaláveis e resilientes que viabilizam o modelo de autoatendimento (*self-service*) para times de desenvolvimento de software. 

Este guia consolida padrões de arquitetura, ferramentas essenciais, código de produção e melhores práticas para desenhar, implementar e operar infraestruturas modernas orientadas a nuvem e ambientes híbridos.

---

## 🏗️ 1. Infraestrutura como Código (IaC) com Terraform

O Terraform é a ferramenta padrão de mercado para provisionamento declarativo de infraestrutura multi-cloud. O design de código deve priorizar modularidade, imutabilidade e isolamento de estado.

### 📁 Estrutura de Diretórios de Módulos
Uma arquitetura profissional separa módulos reutilizáveis das definições de ambiente (*live/environments*):

```text
terraform-architecture/
├── modules/
│   └── vpc/
│       ├── main.tf
│       ├── variables.tf
│       ├── outputs.tf
│       └── versions.tf
└── environments/
    ├── dev/
    │   ├── backend.tf
    │   ├── main.tf
    │   ├── terraform.tfvars
    │   └── variables.tf
    └── prod/
        ├── backend.tf
        ├── main.tf
        ├── terraform.tfvars
        └── variables.tf
```

### 🔒 Remote State com S3 e DynamoDB (AWS)
O armazenamento de estado remoto garante colaboração segura com travamento concorrente (*state locking*).

```hcl
# environments/prod/backend.tf
terraform {
  required_version = ">= 1.7.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.40.0"
    }
  }

  backend "s3" {
    bucket         = "company-terraform-state-prod"
    key            = "core-infra/vpc/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "company-terraform-locks-prod"
  }
}
```

### 📦 Exemplo de Módulo Reutilizável de VPC

```hcl
# modules/vpc/variables.tf
variable "vpc_cidr" {
  description = "The CIDR block for the VPC"
  type        = string
  default     = "10.0.0.0/16"

  validation {
    condition     = can(cidrnetmask(var.vpc_cidr))
    error_message = "The vpc_cidr must be a valid CIDR block."
  }
}

variable "environment" {
  description = "Deployment environment name"
  type        = string
}

variable "public_subnet_cidrs" {
  description = "List of public subnet CIDR blocks"
  type        = list(string)
}

variable "private_subnet_cidrs" {
  description = "List of private subnet CIDR blocks"
  type        = list(string)
}

variable "availability_zones" {
  description = "List of availability zones to distribute subnets"
  type        = list(string)
}
```

```hcl
# modules/vpc/main.tf
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name        = "vpc-${var.environment}"
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

resource "aws_internet_gateway" "gw" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name        = "igw-${var.environment}"
    Environment = var.environment
  }
}

resource "aws_subnet" "public" {
  count                   = length(var.public_subnet_cidrs)
  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.public_subnet_cidrs[count.index]
  availability_zone       = var.availability_zones[count.index]
  map_public_ip_on_launch = true

  tags = {
    Name        = "subnet-${var.environment}-public-${count.index + 1}"
    Environment = var.environment
    Type        = "Public"
  }
}

resource "aws_subnet" "private" {
  count             = length(var.private_subnet_cidrs)
  vpc_id            = aws_vpc.main.id
  cidr_block        = var.private_subnet_cidrs[count.index]
  availability_zone = var.availability_zones[count.index]

  tags = {
    Name        = "subnet-${var.environment}-private-${count.index + 1}"
    Environment = var.environment
    Type        = "Private"
  }
}
```

```hcl
# modules/vpc/outputs.tf
output "vpc_id" {
  description = "Identifier of the created VPC"
  value       = aws_vpc.main.id
}

output "public_subnet_ids" {
  description = "List of IDs for public subnets"
  value       = aws_subnet.public[*].id
}

output "private_subnet_ids" {
  description = "List of IDs for private subnets"
  value       = aws_subnet.private[*].id
}
```

### 🔄 Ciclo de Vida e Detecção de Drift
1. **Validação e Formatação**:
   ```bash
   terraform fmt -recursive
   terraform validate
   ```
2. **Execução Segura em CI**:
   ```bash
   terraform plan -out=tfplan.binary
   terraform apply tfplan.binary
   ```
3. **Detecção de Drift em Cron**:
   ```bash
   # Exit code 2 indicates a drift occurred
   terraform plan -detailed-exitcode -no-color
   ```

---

## ⚙️ 2. Gerenciamento de Configuração & Automação com Ansible

O Ansible provê automação sem agentes (*agentless*) sobre SSH/WinRM, garantindo **idempotência** na configuração de sistemas operacionais e aplicações.

### 📐 Estrutura de Diretórios e Roles

```text
ansible-project/
├── ansible.cfg
├── inventory/
│   ├── production/
│   │   ├── hosts.yml
│   │   └── group_vars/
│   │       ├── all.yml
│   │       └── webservers.yml
│   └── staging/
│       └── hosts.yml
├── roles/
│   └── webserver/
│       ├── defaults/main.yml
│       ├── tasks/main.yml
│       ├── handlers/main.yml
│       ├── templates/nginx.conf.j2
│       └── vars/main.yml
└── site.yml
```

### 🏷️ Precedência de Variáveis e Ansible Vault
A ordem de precedência no Ansible varia de padrões de roles (menor prioridade) até argumentos de linha de comando (`-e`, maior prioridade).

Para criptografar segredos:
```bash
# Encrypt a secret variable
ansible-vault encrypt_string --vault-password-file .vault_pass 'supersecretpassword' --name 'db_password'

# Run playbook with vault file
ansible-playbook -i inventory/production/hosts.yml site.yml --vault-password-file .vault_pass
```

### 📄 Exemplo de Playbook e Role Idempotente

```yaml
# inventory/production/hosts.yml
all:
  children:
    webservers:
      hosts:
        web-node-01.internal:
          ansible_host: 10.0.10.21
        web-node-02.internal:
          ansible_host: 10.0.10.22
      vars:
        http_port: 80
        server_name: api.production.internal
```

```yaml
# roles/webserver/tasks/main.yml
---
# Install and configure NGINX web server
- name: Ensure NGINX package is installed
  ansible.builtin.package:
    name: nginx
    state: present

- name: Deploy NGINX configuration from template
  ansible.builtin.template:
    src: nginx.conf.j2
    dest: /etc/nginx/nginx.conf
    owner: root
    group: root
    mode: '0644'
  notify: Restart NGINX service

- name: Ensure NGINX service is enabled and running
  ansible.builtin.service:
    name: nginx
    state: started
    enabled: true

- name: Deploy web root content
  ansible.builtin.copy:
    content: "OK - Managed by Ansible\n"
    dest: /var/www/html/healthz
    owner: www-data
    group: www-data
    mode: '0644'
```

```yaml
# roles/webserver/handlers/main.yml
---
- name: Restart NGINX service
  ansible.builtin.service:
    name: nginx
    state: restarted
```

```yaml
# site.yml
---
- name: Configure Production Web Fleet
  hosts: webservers
  become: true
  roles:
    - role: webserver
```

---

## 💻 3. Ambientes de Desenvolvimento Local com Vagrant

O Vagrant permite provisionar ambientes de desenvolvimento reproduzíveis e portáveis localmente, integrando-se a hipervisores (VirtualBox, VMware, Libvirt, Hyper-V).

### ⚙️ Multi-Machine Vagrantfile com Provisão Shell e Ansible

```ruby
# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/jammy64"
  config.vm.box_check_update = true

  # Global synced folder
  config.vm.synced_folder "./app", "/var/www/app", type: "nfs", mount_options: ["actimeo=1"]

  # Global VM provider configuration
  config.vm.provider "virtualbox" do |vb|
    vb.gui = false
    vb.linked_clone = true
  end

  # Node 1: Web Application Server
  config.vm.define "app-node" do |app|
    app.vm.hostname = "app-node.local"
    app.vm.network "private_network", ip: "192.168.56.10"
    app.vm.network "forwarded_port", guest: 80, host: 8080, auto_correct: true

    app.vm.provider "virtualbox" do |vb|
      vb.memory = "2048"
      vb.cpus = 2
    end

    # Bootstrap with shell provisioner
    app.vm.provision "shell", inline: <<-SHELL
      export DEBIAN_FRONTEND=noninteractive
      apt-get update && apt-get install -y curl ufw git
      ufw allow 80/tcp
    SHELL

    # Configure using Ansible Local provisioner
    app.vm.provision "ansible_local" do |ansible|
      ansible.playbook = "ansible/site.yml"
      ansible.install_mode = "pip"
    end
  end

  # Node 2: Database Server
  config.vm.define "db-node" do |db|
    db.vm.hostname = "db-node.local"
    db.vm.network "private_network", ip: "192.168.56.11"

    db.vm.provider "virtualbox" do |vb|
      vb.memory = "1024"
      vb.cpus = 1
    end

    db.vm.provision "shell", inline: <<-SHELL
      apt-get update && apt-get install -y postgresql postgresql-contrib
      systemctl enable --now postgresql
    SHELL
  end
end
```

---

## ☸️ 4. Orquestração e Operações em Kubernetes

Kubernetes é o motor de execução para microsserviços modernos. Configurações corporativas exigem resiliência com **HPA**, **PDB**, **Resource Quotas** e entrega contínua via **GitOps**.

### 📜 Manifesto de Aplicação de Produção

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: order-service
  namespace: production
  labels:
    app.kubernetes.io/name: order-service
    app.kubernetes.io/part-of: ecommerce
spec:
  replicas: 3
  revisionHistoryLimit: 5
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 25%
      maxUnavailable: 0
  selector:
    matchLabels:
      app: order-service
  template:
    metadata:
      labels:
        app: order-service
    spec:
      containers:
        - name: app
          image: ghcr.io/company/order-service:v2.4.1
          imagePullPolicy: IfNotPresent
          ports:
            - containerPort: 8080
              name: http
          env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: order-service-secret
                  key: database-url
            - name: LOG_LEVEL
              valueFrom:
                configMapKeyRef:
                  name: order-service-config
                  key: log-level
          resources:
            requests:
              cpu: "250m"
              memory: "256Mi"
            limits:
              cpu: "1000m"
              memory: "512Mi"
          readinessProbe:
            httpGet:
              path: /healthz/ready
              port: http
            initialDelaySeconds: 5
            periodSeconds: 10
          livenessProbe:
            httpGet:
              path: /healthz/live
              port: http
            initialDelaySeconds: 15
            periodSeconds: 20
---
apiVersion: v1
kind: Service
metadata:
  name: order-service
  namespace: production
spec:
  type: ClusterIP
  selector:
    app: order-service
  ports:
    - name: http
      port: 80
      targetPort: http
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: order-service-ingress
  namespace: production
  annotations:
    kubernetes.io/ingress.class: "nginx"
    cert-manager.io/cluster-issuer: "letsencrypt-production"
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  tls:
    - hosts:
        - orders.company.com
      secretName: order-service-tls
  rules:
    - host: orders.company.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: order-service
                port:
                  name: http
```

### 📈 Alta Disponibilidade: HPA e PDB

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: order-service-hpa
  namespace: production
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: order-service
  minReplicas: 3
  maxReplicas: 20
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 80
---
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: order-service-pdb
  namespace: production
spec:
  minAvailable: 2
  selector:
    matchLabels:
      app: order-service
```

### 🐙 GitOps com ArgoCD Application

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: order-service-prod
  namespace: argocd
  finalizers:
    - resources-finalizer.argocd.argoproj.io
spec:
  project: default
  source:
    repoURL: 'https://github.com/company/gitops-manifests.git'
    targetRevision: main
    path: overlays/production/order-service
  destination:
    server: 'https://kubernetes.default.svc'
    namespace: production
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
```

---

## 🖥️ 5. Gerenciamento de Máquinas Virtuais & Golden Images

Embora contêineres dominem cargas efêmeras, **Máquinas Virtuais (VMs)** são a fundação para hypervisors, bancos de dados bare-metal, clusters Kubernetes (control plane / worker nodes) e workloads com isolamento rígido de kernel.

### 📊 Comparação: Máquinas Virtuais vs Contêineres

| Característica | Máquinas Virtuais (VMs) | Contêineres (Docker / Podman) |
| :--- | :--- | :--- |
| **Isolamento** | Hypervisor (Hardware-level / Type 1 ou 2) | Namespaces e cgroups (OS-level) |
| **Kernel** | Kernel próprio e independente por VM | Compartilhado com o Host OS |
| **Tempo de Boot** | Segundos a minutos | Milissegundos a segundos |
| **Overhead / Footprint** | GBs de armazenamento e RAM dedicada | MBs a GBs, compartilhando camadas |
| **Casos de Uso** | Host de Kubernetes, DBs legados, Multi-tenant rígido | Microsserviços, Jobs CI, APIs stateless |

### 🍞 Image Baking com HashiCorp Packer (HCL2)

```hcl
# ubuntu-golden-image.pkr.hcl
packer {
  required_plugins {
    amazon = {
      version = ">= 1.2.8"
      source  = "github.com/hashicorp/amazon"
    }
  }
}

source "amazon-ebs" "ubuntu_golden" {
  ami_name      = "golden-ubuntu-2204-base-{{timestamp}}"
  instance_type = "t3.medium"
  region        = "us-east-1"

  source_ami_filter {
    filters = {
      name                = "ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"
      root-device-type    = "ebs"
      virtualization-type = "hvm"
    }
    most_recent = true
    owners      = ["099720109477"] # Canonical
  }

  ssh_username = "ubuntu"
  tags = {
    OS          = "Ubuntu 22.04"
    BaseAMI     = "GoldenImage"
    ManagedBy   = "Packer"
    Environment = "Core"
  }
}

build {
  name    = "build-golden-ami"
  sources = ["source.amazon-ebs.ubuntu_golden"]

  provisioner "shell" {
    inline = [
      "export DEBIAN_FRONTEND=noninteractive",
      "sudo apt-get update && sudo apt-get upgrade -y",
      "sudo apt-get install -y fail2ban auditd awscli jq curl unattended-upgrades",
      "sudo systemctl enable fail2ban auditd"
    ]
  }

  provisioner "ansible" {
    playbook_file = "./ansible/hardening-playbook.yml"
    user          = "ubuntu"
  }
}
```

### ☁️ Customização Inicial via Cloud-Init

```yaml
#cloud-config
package_upgrade: true
packages:
  - curl
  - jq
  - htop
  - docker.io

users:
  - name: devops
    groups: sudo, docker
    shell: /bin/bash
    sudo: ['ALL=(ALL) NOPASSWD:ALL']
    ssh_authorized_keys:
      - ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIExampleKeyDevOpsEngineer123456

write_files:
  - path: /etc/docker/daemon.json
    content: |
      {
        "log-driver": "json-file",
        "log-opts": {
          "max-size": "100m",
          "max-file": "3"
        }
      }
    permissions: '0644'

runcmd:
  - systemctl restart docker
  - ufw default deny incoming
  - ufw default allow outgoing
  - ufw allow 22/tcp
  - ufw enable
```

---

## 🏛️ 6. Internal Developer Platform (IDP) com Backstage

O **Backstage** (desenvolvido pelo Spotify e mantido pela CNCF) atua como o portal central de desenvolvedores (IDP), agregando **Software Catalog**, **Software Templates (Scaffolder)**, **TechDocs** e métricas operacionais.

### 📑 Software Catalog: `catalog-info.yaml`

```yaml
apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  name: payment-gateway-api
  description: Core microservice responsible for processing credit card and pix transactions.
  annotations:
    github.com/project-slug: company/payment-gateway-api
    backstage.io/techdocs-ref: dir:.
    argocd/app-name: payment-gateway-api-prod
    datadog/service-name: payment-gateway
    sonarqube.org/project-key: company_payment-gateway-api
  tags:
    - java
    - spring-boot
    - fintech
    - pci-dss
spec:
  type: service
  lifecycle: production
  owner: group:payments-team
  system: payment-system
  providesApis:
    - payment-v2-api
  dependsOn:
    - resource:payment-aurora-db
    - component:fraud-detection-service
```

### 🧩 Software Template (Scaffolder): `template.yaml`

```yaml
apiVersion: scaffolder.backstage.io/v1beta3
kind: Template
metadata:
  name: springboot-microservice-template
  title: Production-Ready Spring Boot Service
  description: Scaffolds a complete Spring Boot 3 service with CI/CD, Helm chart, Dockerfile and SonarQube.
spec:
  owner: group:platform-team
  type: service
  parameters:
    - title: Service Configuration
      required:
        - component_id
        - owner
      properties:
        component_id:
          title: Service Identifier
          type: string
          description: Unique kebab-case name for the repo and deployment
        owner:
          title: Owning Team
          type: string
          ui:field: OwnerPicker
          ui:options:
            allowedKinds:
              - Group

  steps:
    - id: template
      name: Fetch Skeleton Template
      action: fetch:template
      input:
        url: ./skeleton
        values:
          component_id: ${{ parameters.component_id }}
          owner: ${{ parameters.owner }}

    - id: publish
      name: Publish to GitHub
      action: publish:github
      input:
        allowedHosts: ['github.com']
        description: Service created via Backstage IDP
        repoUrl: github.com?owner=company&repo=${{ parameters.component_id }}
        defaultBranch: main

    - id: register
      name: Register in Software Catalog
      action: catalog:register
      input:
        repoContentsUrl: ${{ steps.publish.output.repoContentsUrl }}
        catalogInfoPath: '/catalog-info.yaml'

  output:
    links:
      - title: Open GitHub Repository
        url: ${{ steps.publish.output.remoteUrl }}
```

---

## 🔄 7. Pipelines de CI/CD Modernos

A integridade do software é assegurada por pipelines determinísticos com validação de código, segurança contínua (SAST/SCA/Container Scan) e estratégias automatizadas de implantação e rollback.

```mermaid
flowchart LR
    Dev[Push Branch] --> Lint[Lint & Static Check]
    Lint --> Test[Unit & Integration Tests]
    Test --> Security[SAST / Trivy Scan]
    Security --> Build[Build & Sign Image]
    Build --> GitOps[Update GitOps Repo]
    GitOps --> Deploy[ArgoCD Sync to Cluster]
    Deploy --> Verify[Automated Smoke Tests]
```

### 🛠️ Pipeline de Produção (GitHub Actions)

```yaml
# .github/workflows/ci-cd-pipeline.yml
name: Continuous Integration & Deployment

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

permissions:
  contents: read
  packages: write
  id-token: write

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  validate:
    name: Lint, Test & SAST
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Setup Node.js Environment
        uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'

      - name: Install Dependencies & Run Tests
        run: |
          npm ci
          npm run lint
          npm test -- --coverage

      - name: Run Trivy Vulnerability Scanner (Filesystem)
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          ignore-unfixed: true
          severity: 'CRITICAL,HIGH'
          exit-code: '1'

  build-and-push:
    name: Build & Push OCI Image
    needs: [validate]
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    outputs:
      image_tag: ${{ steps.meta.outputs.version }}
    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract Docker metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=sha,format=short,prefix=
            type=raw,value=latest

      - name: Build and push Docker image
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  gitops-promote:
    name: Trigger GitOps Promotion
    needs: [build-and-push]
    runs-on: ubuntu-latest
    steps:
      - name: Update Target Image Tag in GitOps Repo
        uses: actions/github-script@v7
        with:
          github-token: ${{ secrets.GITOPS_REPO_PAT }}
          script: |
            // Trigger repository_dispatch or direct commit to GitOps repository
            console.log("Promoting image tag ${{ needs.build-and-push.outputs.image_tag }} to production");
```

### 🎯 Estratégias de Deploy e Rollback

| Estratégia | Descrição | Prós | Contras | Mecanismo de Rollback |
| :--- | :--- | :--- | :--- | :--- |
| **Rolling Update** | Atualiza pods incrementalmente lote a lote | Zero downtime, sem custo extra de infra | Versões mistas em execução simultânea | `kubectl rollout undo deployment/<name>` |
| **Blue/Green** | Ambiente espelho idêntico (Green) provisionado em paralelo | Troca instantânea de tráfego, isolamento | Dobro do custo de infraestrutura | Redirecionamento imediato de tráfego no Ingress/LoadBalancer |
| **Canary** | Envia percentual gradual de tráfego (Ex: 5% -> 25% -> 100%) | Detecção antecipada de anomalias com telemetria | Requer service mesh ou ingress controller avançado | Reversão automática ao detectar aumento de taxa de erro HTTP 5xx |

---

## 📊 8. Observabilidade e Engenharia de Confiabilidade (SRE)

Observabilidade não é apenas monitoramento passivo; é a capacidade de inferir o estado interno do sistema através de suas saídas externas: **Métricas**, **Logs** e **Traces**.

```mermaid
graph TD
    App[Workload Application] -->|Metrics /metrics| Prom[Prometheus]
    App -->|Structured Logs JSON| Vec[Vector / FluentBit]
    App -->|OTLP Traces| OTel[OpenTelemetry Collector]
    Vec --> Loki[Grafana Loki / Elasticsearch]
    OTel --> Tempo[Grafana Tempo / Jaeger]
    Prom --> Grafana[Grafana Dashboards]
    Loki --> Grafana
    Tempo --> Grafana
    Prom --> AM[Alertmanager]
    AM --> PagerDuty[PagerDuty / Slack Notifications]
```

### 🚨 Alertas Baseados em SLO/SLI (Prometheus Operator)

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: order-service-slo-alerts
  namespace: production
  labels:
    role: alert-rules
spec:
  groups:
    - name: order-service-slo
      rules:
        # Calculate HTTP 5xx error rate over 5 minutes
        - record: job:http_requests_error_ratio:rate5m
          expr: |
            sum(rate(http_requests_total{job="order-service",status=~"5.."}[5m]))
            /
            sum(rate(http_requests_total{job="order-service"}[5m]))

        # Alert if burn rate exceeds 1% error budget rapidly
        - alert: HighHttpErrorRateSLOBurn
          expr: job:http_requests_error_ratio:rate5m > 0.01
          for: 2m
          labels:
            severity: critical
            team: payments
          annotations:
            summary: "Critical error budget burn rate on order-service"
            description: "High error rate detected: {{ $value | humanizePercentage }} of requests are failing with 5xx status."
            runbook_url: "https://wiki.company.com/ops/runbooks/order-service-5xx"
```

---

## 🛠️ 9. Platform Engineering & Developer Experience (DX)

A transição de DevOps tradicional para **Platform Engineering** substitui a fila de tickets de infraestrutura (*ticket-ops*) pela entrega de uma **Plataforma como Produto**:

```text
[ Desenvolvedores de Produto ]
             │
             ▼  (Self-Service / APIs / Golden Paths)
┌─────────────────────────────────────────────────────────┐
│        INTERNAL DEVELOPER PLATFORM (IDP)                │
│  ├── Backstage (Software Catalog & Templates)           │
│  ├── GitOps Engine (ArgoCD / Flux)                      │
│  ├── IaC Modules (Terraform Registry / Crossplane)      │
│  └── Telemetry Stack (OpenTelemetry / Grafana / O11y)   │
└─────────────────────────────────────────────────────────┘
             │
             ▼  (Provisionamento Declarativo e Seguro)
[ Multi-Cloud & Bare-Metal Infrastructure ]
```

### 🛣️ Princípios de Golden Paths
1. **Paved Roads (Caminhos Pavimentados)**: Oferecer padrões opinativos onde segurança, observabilidade e CI/CD já venham integrados por padrão.
2. **Autonomia sem Fricção**: Os desenvolvedores devem provisionar bancos de dados, tópicos de mensageria e serviços sem aguardar aprovações manuais para ambientes de teste e validação.
3. **Métricas DORA como Bússola**:
   - **Deployment Frequency**: Frequência de deploys bem-sucedidos em produção.
   - **Lead Time for Changes**: Tempo entre o commit do código e a execução em produção.
   - **Change Failure Rate**: Porcentagem de deploys que causam incidentes em produção.
   - **Failed Deployment Recovery Time (MTTR)**: Tempo médio para restaurar o serviço em caso de degradação.

---

## 🔗 Habilidades Relacionadas

- [devsecops-engineer](../../security/ops-architecture/devsecops-engineer/SKILL.md)
- [software-architect](../software-architect/SKILL.md)
- [program-github](../../programs/github-actions/SKILL.md)
- [github-actions](../../programs/github-actions/SKILL.md)
- [containers](../../programs/containers/SKILL.md)
