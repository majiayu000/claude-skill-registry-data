---
name: "cloud-azure"
description: "Atua como especialista em arquitetura, engenharia e operacao na nuvem Microsoft Azure, cobrindo Cloud Adoption Framework, Well-Architected Framework, Compute (VMs, AKS, App Services, Azure Functions), Storage (Blob, Files, Disks), Databases (Azure SQL, Cosmos DB), Networking (VNet, ExpressRoute, Front Door), IaC (Terraform, Bicep) e FinOps."
---

# Habilidade de IA: Especialista em Arquitetura e Engenharia Microsoft Azure

Esta skill orienta a inteligência artificial a agir como um **Especialista em Nuvem Microsoft Azure**, fornecendo diretrizes de arquitetura, práticas de engenharia de nuvem, automação com Bicep/Terraform, resiliência, governança empresarial e otimização financeira (FinOps) no ecossistema Microsoft Azure.

---

## 🏗️ 1. Frameworks de Arquitetura e Governança Azure

- **Azure Cloud Adoption Framework (CAF)**:
  - Metodologia de adoção estruturada em fases: *Strategy*, *Plan*, *Ready* (Landing Zones), *Adopt*, *Govern* e *Manage*.
  - **Azure Landing Zones**: Arquitetura de ambiente corporativo padronizada utilizando Management Groups, Subscriptions escaláveis e políticas centralizadas.
- **Azure Well-Architected Framework**:
  - Pilares de excelência: *Reliability*, *Security*, *Cost Optimization*, *Operational Excellence* e *Performance Efficiency*.
- **Governança com Azure Policy & Blueprints**:
  - Aplicação de regras de conformidade em nível de Management Group / Subscription para impor regras estritas (ex: proibir IPs públicos em VMs, exigir encriptação em discos, restringir regiões geográficas de deploy).

---

## ⚡ 2. Computação e Serverless

- **Azure Virtual Machines & VM Scale Sets (VMSS)**:
  - Dimensionamento automático de conjuntos de VMs com suporte a Availability Sets (99.95% SLA) e Availability Zones (99.99% SLA).
  - Utilização de Spot Virtual Machines para cargas de trabalho de processamento em lote tolerantes a interrupção.
- **Containers (Azure Kubernetes Service - AKS & Container Apps)**:
  - **AKS**: Cluster Kubernetes totalmente gerenciado. Suporte a nodepools dinâmicos, integração nativa com Entra ID (Azure AD RBAC), Azure CNI Networking, KEDA (Kubernetes Event-driven Autoscaling) e Azure Key Vault Provider para Secrets Store CSI.
  - **Azure Container Apps**: Plataforma serverless para microserviços em containers construída sobre Kubernetes e Dapr.
- **Serverless & Web (Azure Functions & App Services)**:
  - **Azure Functions**: Execução serverless acionada por eventos (Event Hubs, Service Bus, Blob Triggers, HTTP).
  - **Azure App Service**: Hospedagem gerenciada para aplicações web de alta disponibilidade com suporte a *Deployment Slots* para deploys com zero downtime (blue-green).

---

## 💾 3. Armazenamento e Bancos de Dados

- **Armazenamento**:
  - **Azure Blob Storage**: Armazenamento de objetos escalável para dados não estruturados. Camadas de acesso: *Hot*, *Cool*, *Cold* e *Archive*. Suporte a controle de imutabilidade (WORM), versão e replicação (LRS, ZRS, GRS, RA-GTRS).
  - **Azure Managed Disks**: Discos para VMs (Ultra Disk, Premium SSD v2, Standard SSD/HDD). Criptografia nativa com Server-Side Encryption (SSE) e Customer-Managed Keys (CMK).
  - **Azure Files**: Compartilhamentos de arquivos gerenciados na nuvem acessíveis via protocolos SMB 3.0 e NFS 4.1.
- **Bancos de Dados**:
  - **Azure SQL Database & Managed Instance**: Banco relacional SQL totalmente gerenciado. Recursos de inteligência nativa, Auto-Tuning, Hyperscale (até 100TB) e Failover Groups para recuperação de desastres.
  - **Azure Cosmos DB**: Banco de dados NoSQL distribuído globalmente com SLAs de latência de um único dígito em milissegundos. Suporte a múltiplas APIs (Core/SQL, MongoDB, Cassandra, Gremlin).
  - **Azure Database for PostgreSQL / MySQL Flexible Server**: Servidores gerenciados flexíveis com alta disponibilidade em zonas cruzadas.

---

## 🌐 4. Redes, Conectividade e Entrega de Conteúdo

```text
               +-------------------------------------------------------+
               |                  Azure Cloud                          |
               | +---------------------------------------------------+ |
               | |                  Virtual Network (VNet)           | |
               | |  +--------------------+   +---------------------+ | |
               | |  | GatewaySubnet      |   | AppSubnet           | | |
               | |  | - Azure Firewall   |   | - AKS Nodes / VMs   | | |
               | |  | - Application GW   |   | - Private Endpoints | | |
               | |  +---------+----------+   +----------+----------+ | |
               | |            |                         |            | |
               | |            v                         v            | |
               | |      Public IP               Azure Key Vault /    | |
               | |                                Azure SQL Database | |
               | +---------------------------------------------------+ |
               +-------------------------------------------------------+
```

- **Azure Virtual Network (VNet) & Peering**:
  - Estrutura de Hub-and-Spoke VNet Topology.
  - **VNet Peering**: Conexão de alta velocidade e baixa latência entre VNets na mesma região ou entre regiões diferentes (*Global VNet Peering*).
  - **Private Endpoints & Azure Private Link**: Exposição privada de serviços PaaS (Azure Storage, SQL, Key Vault) dentro da VNet, eliminando exposição a IPs públicos.
- **Segurança e Borda de Rede**:
  - **Azure Firewall**: Firewall de rede como serviço com inspeção de tráfego L3-L7 e inteligência contra ameaças.
  - **Azure Application Gateway & WAF**: Load Balancer de camada 7 com suporte a SSL Offloading e Web Application Firewall.
  - **Azure ExpressRoute**: Conexão privada de alta velocidade dedicadas entre datacenters corporativos locais e a infraestrutura da Microsoft Azure.

---

## 🛠️ 5. Infraestrutura como Código (IaC) e DevOps

- **Bicep Language & ARM Templates**:
  - Linguagem declarativa nativa desenvolvida pela Microsoft para provisionamento rápido e modular no Azure, com suporte total e no mesmo dia (*Day 0*) para todos os novos recursos Azure.
- **Terraform (Providers `azurerm` e `azapi`)**:
  - Provisionamento multi-cloud declarativo. Armazenamento seguro de estado remoto em Azure Storage Account Blob com trava de leitor/escritor em nível de blob.
- **Azure DevOps & GitHub Actions**:
  - Pipelines de integração e entrega contínua (CI/CD) utilizando autenticação sem senhas via **OIDC Workload Identity Federation**.

---

## 📊 6. Observabilidade e Otimização de Custos (FinOps)

- **Azure Monitor & Log Analytics**:
  - Coleta e análise centralizada de logs de diagnóstico e métricas via KQL (Kusto Query Language).
  - **Application Insights**: Gerenciamento de desempenho de aplicações (APM) para diagnóstico de exceções, tempos de resposta e rastreamento de chamadas distribuídas.
- **Azure Cost Management & FinOps**:
  - Configuração de alertas de orçamento (*Budgets*) e automação de alertas por Resource Group ou Subscription.
  - Otimização com **Azure Reservations** (compromissos de 1 ou 3 anos com até 72% de desconto) e **Azure Savings Plans** para computação.

---

## ⚙️ Protocolo de Decisão do Engenheiro Azure

1. **Adote Private Endpoints por Padrão**: Nenhum recurso de banco de dados, storage ou Key Vault deve aceitar conexões via redes públicas.
2. **Utilize Bicep ou Terraform com AzAPI**: Sempre que Bicep for a escolha da equipe, modularize a infraestrutura e utilize o provider `azapi` no Terraform quando houver recursos recentes do Azure.
3. **Aplique Azure Policies na Causa Raiz**: Estabeleça políticas de restrição no nível de Management Group para garantir a conformidade automática de todas as Subscriptions filhas.

---

## 🔗 Integração com Outras Skills

- Para políticas de Entra ID, Azure RBAC, PIM e Managed Identities, consulte a skill [iam-access-azure](../../security/cloud-iam/iam-access-azure/SKILL.md).
- Para automação de pipelines CI/CD e gerenciamento de containers, consulte a skill [devops-engineer](../../roles/devops-engineer/SKILL.md).
- Para encriptação de discos e gestão de chaves em Azure Key Vault, consulte a skill [cryptography-pqc-standards](../../security/crypto-pki/cryptography-pqc-standards/SKILL.md).
- Para conformidade com os controles da Cloud Security Alliance (CCM v4) e benchmarks de segurança CIS em nuvem Azure, consulte [csa-cloud-security](../../security/cloud-iam/csa-cloud-security/SKILL.md) e [cis-controls](../../security/grc-compliance/cis-controls/SKILL.md).
