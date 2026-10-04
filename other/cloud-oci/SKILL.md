---
name: "cloud-oci"
description: "Atua como especialista em arquitetura, engenharia e operacao na nuvem Oracle Cloud Infrastructure (OCI), cobrindo OCI Architecture Center, Compute (Bare Metal, VMs, OKE), Storage (Block Volumes, Object Storage), Databases (Autonomous Database, Exadata, MySQL HeatWave), Networking (VCN, DRG, FastConnect), IaC (Terraform, Resource Manager) e FinOps."
---

# Habilidade de IA: Especialista em Arquitetura e Engenharia Oracle Cloud (OCI)

Esta skill orienta a inteligência artificial a agir como um **Especialista em Nuvem Oracle Cloud Infrastructure (OCI)**, fornecendo especificações de arquitetura para workloads empresariais de missão crítica, bancos de dados autônomos, infraestrutura Bare Metal de alta performance, automação com Terraform, redes distribuídas e gestão financeira no ecossistema OCI.

---

## 🏗️ 1. OCI Architecture Center e Princípios de Design

1. **Isolamento e Controle em Nível de Compartimento**:
   - Estruturação de **Compartments** para organização de recursos, políticas de IAM e limites de cotas corporativas (*Service Limits*).
2. **Arquitetura de Alta Disponibilidade (Fault Domains & Availability Domains)**:
   - Distribuição de cargas de trabalho em múltiplos **Availability Domains (ADs)** e **Fault Domains (FDs)** dentro de uma única região para garantir resiliência contra falhas de hardware ou energia física no rack.
3. **Desempenho Sem Compromissos (Non-Overcommitted Hardware)**:
   - Redes de *Data Center* sem sobredimensionamento (*Non-blocking flat network design*) e computação **Bare Metal** direta no silício para cargas de trabalho de altíssimo I/O e bancos de dados transacionais pesados.

---

## ⚡ 2. Computação e Containers

- **OCI Compute (Bare Metal & Virtual Machines)**:
  - **Bare Metal Instances**: Servidores dedicados físicos sem hipervisor instalado. Desempenho bruto de CPU e memória com isolamento total para Oracle Exadata e ambientes regulados.
  - **Virtual Machines (Flex Shapes)**: Dimensionamento sob medida de OCPUs (Oracle CPUs) e memória RAM (ex: instâncias `VM.Standard3.Flex` ou `VM.Standard.E5.Flex`) ajustando recursos na quantidade exata necessária.
- **Containers & Serverless**:
  - **Oracle Container Engine for Kubernetes (OKE)**: Cluster Kubernetes gerenciado com nós de trabalho emparelhados a Virtual Cloud Networks (VCNs) nativas e integração com **OCI Web Application Firewall (WAF)**.
  - **OCI Functions**: Plataforma serverless baseada no projeto de código aberto **Fn Project**, acionada por eventos do OCI Events Service ou chamadas via API Gateway.

---

## 💾 3. Armazenamento e Bancos de Dados de Missão Crítica

- **Armazenamento**:
  - **OCI Block Volumes**: Desempenho de discos de bloco configurado dinamicamente via **Volume Performance Units (VPUs)** (de *Lower Cost* a *Ultra High Performance* de até 300.000 IOPS por volume). Criptografia obrigatória por padrão.
  - **OCI Object Storage**: Armazenamento de objetos de alta durabilidade (*Standard*, *Infrequent Access*, *Archive*). Suporte a imutabilidade (*Retention Rules / WORM*) e encriptação nativa.
- **Bancos de Dados Oracle & Open Source**:
  - **Oracle Autonomous Database (ATP / ADW)**: Banco de dados relacional com auto-tuning, auto-patching, auto-scaling e segurança autônoma baseados em IA.
  - **Oracle Exadata Database Service**: Infraestrutura Exadata dedicada ou compartilhada na nuvem OCI para máximo desempenho de OLTP e Data Warehousing.
  - **MySQL HeatWave**: Serviço MySQL gerenciado integrado a um acelerador analítico em memória que combina OLTP e OLAP no mesmo banco sem ETL.

---

## 🌐 4. Redes e Conectividade de Infraestrutura

```text
               +-------------------------------------------------------+
               |                  Oracle Cloud Infrastructure          |
               | +---------------------------------------------------+ |
               | |                  Virtual Cloud Network (VCN)      | |
               | |  +--------------------+   +---------------------+ | |
               | |  | Public Subnet      |   | Private Subnet      | | |
               | |  | - Public LB        |   | - OKE Nodes / VMs   | | |
               | |  | - NAT Gateway      |   | - Autonomous DB     | | |
               | |  +---------+----------+   +----------+----------+ | |
               | |            |                         |            | |
               | |            v                         v            | |
               | |     Internet Gateway           Service Gateway    | |
               | |                                (Object Storage)   | |
               | +------------+-------------------------+------------+ |
               +--------------|-------------------------|--------------+
                              v                         v
                       Internet / User           OCI Internal Services
```

- **Virtual Cloud Network (VCN)**:
  - Criação de subredes regionais (*Regional Subnets*) cobrindo todos os ADs da região OCI.
  - **Security Lists & Network Security Groups (NSGs)**: Regras de firewall estatais aplicadas no nível da subrede ou no nível de interfaces de rede virtuais (VNICs) individuais.
- **Hub de Roteamento e Conectividade Dedicada**:
  - **Dynamic Routing Gateway (DRG v2)**: Roteador virtual avançado para interconectar VCNs na mesma região ou cross-region (*Remote Peering*), IPSec VPNs e links **OCI FastConnect**.
  - **Service Gateway**: Acesso privado e sem custo de egresso aos serviços internos da Oracle (Object Storage, Autonomous DB, Auditing) sem passar pela internet pública.

---

## 🛠️ 5. Infraestrutura como Código (IaC) e Gerenciamento

- **Terraform (OCI Provider)**:
  - Provedor declarativo oficial cobrindo a totalidade das APIs do OCI. Suporte a módulos de arquiteturas de referência Landing Zone da Oracle.
- **OCI Resource Manager**:
  - Serviço totalmente gerenciado de Terraform hospedado na nuvem OCI para execução e controle de estado (*State File*) com governança de equipe e integração com repositórios Git (GitHub, GitLab, Bitbucket).

---

## 📊 6. Observabilidade e FinOps

- **OCI Observability & Management**:
  - **OCI Monitoring**: Métricas operacionais em tempo real e alarmes por e-mail, PagerDuty ou webhooks HTTP.
  - **OCI Logging & Logging Analytics**: Coleta centralizada de logs com mecanismo de busca avançado e inteligência para detecção de anomalias operacionais.
  - **Application Performance Monitoring (APM)**: Rastreamento de transações distribuídas end-to-end em aplicações microserviços.
- **FinOps & Otimização Financeira**:
  - **OCI Budgets & Cost Analysis**: Monitoramento contínuo de custos com alertas preventivos ao atingir porcentagens do orçamento.
  - **Universal Credits**: Modelo de créditos unificados de compra onde os créditos podem ser alocados flexivelmente entre qualquer região ou serviço da nuvem OCI.

---

## ⚙️ Protocolo de Decisão do Engenheiro OCI

1. **Prefira Subredes Regionais**: Sempre configure subredes regionais nas VCNs em vez de subredes específicas por AD para permitir que os recursos escalem livremente entre Availability Domains.
2. **Utilize Service Gateway para Tráfego de Armazenamento**: Nunca direcione o tráfego de backup do Object Storage pela internet pública ou NAT Gateway; utilize sempre o Service Gateway sem custo de tráfego de egresso.
3. **Abandone Credenciais Estáticas com Instance Principals**: Configure Dynamic Groups e Instance Principals em VMs ou OKE para chamadas de API nativas ao OCI.

---

## 🔗 Integração com Outras Skills

- Para políticas de IAM do OCI, grupos dinâmicos e linguagem de políticas, consulte a skill [iam-access-oci](../../security/cloud-iam/iam-access-oci/SKILL.md).
- Para automação de infraestrutura com Terraform e Ansible, consulte a skill [devops-engineer](../../roles/devops-engineer/SKILL.md).
- Para encriptação de volumes de bloco OCI e gestão de chaves em OCI Vault, consulte a skill [cryptography-pqc-standards](../../security/crypto-pki/cryptography-pqc-standards/SKILL.md).
- Para conformidade com os controles da Cloud Security Alliance (CCM v4) e benchmarks de segurança CIS em nuvem OCI, consulte [csa-cloud-security](../../security/cloud-iam/csa-cloud-security/SKILL.md) e [cis-controls](../../security/grc-compliance/cis-controls/SKILL.md).
