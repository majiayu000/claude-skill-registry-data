---
name: "cloud-gcp"
description: "Atua como especialista em arquitetura, engenharia e operacao na nuvem Google Cloud Platform (GCP), cobrindo Google Cloud Architecture Framework, Compute (Compute Engine, GKE, Cloud Run), Storage (GCS, Persistent Disk), Databases (Cloud SQL, Spanner, BigQuery), Networking (Global VPC, Cloud Armor), IaC (Terraform) e FinOps."
---

# Habilidade de IA: Especialista em Arquitetura e Engenharia Google Cloud (GCP)

Esta skill orienta a inteligência artificial a agir como um **Especialista em Nuvem Google Cloud Platform (GCP)**, fornecendo arquitetura de sistemas distribuídos, engenharia de dados, segurança em nuvem, automação com Terraform, resiliência e otimização financeira (FinOps) no ecossistema Google Cloud.

---

## 🏗️ 1. Google Cloud Architecture Framework

Estruturação de soluções de alta confiabilidade alinhadas às diretrizes do **Google Cloud Architecture Framework**:

1. **System Design (Design de Sistemas)**: Escolha adequada de produtos gerenciados e regiões globais.
2. **Operational Excellence (Excelência Operacional)**: Automação via IaC, monitoramento contínuo e cultura SRE (Service Level Objectives - SLOs, Service Level Indicators - SLIs, Error Budgets).
3. **Security, Privacy, and Compliance**: Perímetros de VPC Service Controls, criptografia em repouso por padrão com chaves gerenciadas (GMEK/CMEK) e identidades sem chaves estáticas.
4. **Reliability (Confiabilidade)**: Design para tolerância a falhas multi-zona e multi-região, prevenção de cascading failures e testes de resiliência.
5. **Performance Optimization**: Ajuste fino de IOPS de Persistent Disks, redes globais Premium Tier e computação vetorizada em BigQuery.
6. **Cost Optimization**: Dimensionamento correto (*Right-sizing*), uso de descontos por uso continuado (Sudden Use Discounts / CUDs) e instâncias Spot.

---

## ⚡ 2. Computação e Serverless

- **Google Compute Engine (GCE)**:
  - Máquinas virtuais escaláveis agrupadas em Managed Instance Groups (MIGs) zonis e regionais com Autoscaling automático.
  - Instâncias Spot de alto desconto para cargas de trabalho em lote ou tolerantes a falhas.
- **Google Kubernetes Engine (GKE - Standard & Autopilot)**:
  - **GKE Autopilot**: Modo totalmente gerenciado onde o Google gerencia os nós, a segurança do SO da máquina e o autoscaling por pod, cobrando estritamente pelas solicitações de CPU, memória e armazenamento dos Pods.
  - Integrado nativamente a **Workload Identity**, Cloud Logging e Dataplane V2 (eBPF).
- **Serverless (Cloud Run & Cloud Functions)**:
  - **Cloud Run**: Plataforma serverless para containers HTTP que escala automaticamente de zero a milhares de instâncias em segundos, reduzindo custos em períodos de inatividade.
  - **Cloud Functions (2nd Gen)**: Funções de código orientadas a eventos construídas sobre Cloud Run e Eventarc.

---

## 💾 3. Armazenamento, Bancos de Dados e Big Analytics

- **Armazenamento**:
  - **Google Cloud Storage (GCS)**: Armazenamento de objetos unificado com classes de armazenamento (*Standard, Nearline, Coldline, Archive*) e gerenciamento automatizado do ciclo de vida (*Object Lifecycle Management*). Criptografia nativa em repouso (GMEK/CMEK/CSEK).
  - **Persistent Disk & Hyperdisk**: Discos de bloco para GCE e GKE (Balanced, Performance, Extreme).
- **Bancos de Dados & Big Data**:
  - **Cloud SQL**: Banco relacional gerenciado (PostgreSQL, MySQL, SQL Server) com suporte a alta disponibilidade multi-zona e réplicas de leitura.
  - **Cloud Spanner**: Banco de dados relacional distribuído globalmente com consistência forte ACID e disponibilidade de 99.999% (*five-nines*).
  - **BigQuery**: Data Warehouse / Lakehouse serverless altamente escalável com mecanismo de execução SQL ANSI distribuído e BigQuery ML para inteligência artificial integrada.

---

## 🌐 4. Redes Globais e Segurança de Borda

```text
               +-------------------------------------------------------+
               |                  Google Cloud Network                 |
               | +---------------------------------------------------+ |
               | |                  Global VPC                       | |
               | |  +--------------------+   +---------------------+ | |
               | |  | Subnet (us-east1)  |   | Subnet (europe-west1)| | |
               | |  | - GKE Cluster      |   | - Cloud Run / GCE   | | |
               | |  | - Private IP       |   | - Private Service   | | |
               | |  |   Service Access   |   |   Connect           | | |
               | |  +---------+----------+   +----------+----------+ | |
               | |            |                         |            | |
               | +------------|-------------------------|------------+ |
               +--------------|-------------------------|--------------+
                              v                         v
                   Global External HTTP(S)       VPC Service Controls
                      Load Balancer                   Perimeter
```

- **Global VPC & Shared VPC**:
  - Redes GCP são **globais por padrão**, permitindo que subredes em diferentes regiões do mundo pertençam à mesma rede VPC sem a necessidade de VPNs internas.
  - **Shared VPC**: Permite que uma organização compartilhe uma rede VPC de um projeto central (*Host Project*) com múltiplos projetos de serviço (*Service Projects*).
- **Conectividade Privada e Borda**:
  - **Private Service Connect (PSC)** & **Private Services Access**: Acesso a APIs do Google e serviços PaaS através de IPs privados internos.
  - **Cloud Load Balancing & Cloud Armor**: Load Balancer global com um único Anycast IP global, integrado ao **Cloud Armor** para mitigação de ataques DDoS volumétricos e proteção WAF OWASP Top 10.

---

## 🛠️ 5. Infraestrutura como Código (IaC) e CI/CD

- **Terraform (Google Provider)**:
  - Organização em módulos reusáveis mantendo estado remoto criptografado em buckets GCS (`backend "gcs"`).
- **Cloud Build & Google Artifact Registry**:
  - Pipelines de build de containers e artefatos de código integrados com análise automatizada de vulnerabilidades em imagens.
  - Autenticação de CI/CD via **Workload Identity Federation** eliminando o uso de chaves JSON de Service Accounts.

---

## 📊 6. Observabilidade e Otimização de Custos (FinOps)

- **Google Cloud Observability**:
  - **Cloud Logging**: Coleta e retenção centralizada de logs com capacidade de roteamento para o BigQuery ou Pub/Sub para análise estatística.
  - **Cloud Monitoring**: Painéis de controle de métricas e alertas de SLOs baseados no protocolo OpenTelemetry.
- **FinOps & Otimização**:
  - **Committed Use Discounts (CUDs)**: Descontos flexíveis ou baseados em recursos em troca de compromissos de consumo de 1 ou 3 anos.
  - **Recommender API**: Recomendações automáticas para ajuste de tamanho de VMs (*VM Right-sizing*), desativação de discos órfãos e papéis IAM excessivos.

---

## ⚙️ Protocolo de Decisão do Engenheiro GCP

1. **Utilize a Rede Premium Global do GCP**: Aproveite a capacidade da rede Global VPC e Anycast IPs para simplificar roteamento entre regiões.
2. **Elimine Chaves JSON de Service Accounts**: Aplique a política organizacional `iam.disableServiceAccountKeyCreation` e adote o Workload Identity Federation.
3. **Prefira Cloud Run para Aplicações Containerizadas**: Se a aplicação não exigir orquestração complexa de múltiplos pods interdependentes no Kubernetes, utilize o Cloud Run para obter menor custo e autoscaling instantâneo a partir do zero.

---

## 🔗 Integração com Outras Skills

- Para políticas de IAM no GCP, Service Account Impersonation e VPC Service Controls, consulte a skill [iam-access-gcp](../../security/cloud-iam/iam-access-gcp/SKILL.md).
- Para integração de modelos de IA e Vertex AI no GCP, consulte a skill [gemini-enterprise](../../programs/gemini-enterprise/SKILL.md).
- Para automação de infraestrutura com Terraform e Kubernetes, consulte a skill [devops-engineer](../../roles/devops-engineer/SKILL.md).
- Para alinhamento aos controles da Cloud Security Alliance (CCM v4) e benchmarks de segurança CIS para Google Cloud, consulte [csa-cloud-security](../../security/cloud-iam/csa-cloud-security/SKILL.md) e [cis-controls](../../security/grc-compliance/cis-controls/SKILL.md).
