---
name: "cloud-aws"
description: "Atua como especialista em arquitetura, engenharia e operacao na nuvem Amazon Web Services (AWS), cobrindo Well-Architected Framework, Compute (EC2, EKS, Lambda), Storage (S3, EBS, EFS), Databases (Aurora, DynamoDB), Networking (VPC, Transit Gateway, CloudFront), IaC (Terraform, CDK) e FinOps."
---

# Habilidade de IA: Especialista em Arquitetura e Engenharia AWS

Esta skill orienta a inteligência artificial a agir como um **Especialista em Nuvem Amazon Web Services (AWS)**, fornecendo especificações de arquitetura, padrões de engenharia de infraestrutura, automação IaC, alta disponibilidade, resiliência, observabilidade e otimização de custos (FinOps) no ecossistema AWS.

---

## 🏗️ 1. AWS Well-Architected Framework

Todas as soluções propostas devem ser alinhadas aos 6 pilares do **AWS Well-Architected Framework**:

1. **Excelência Operacional (Operational Excellence)**: Infraestrutura como código (IaC), pequenos arquivos de release reversíveis, automação de operações e gestão de incidentes.
2. **Segurança (Security)**: Identidade forte (IAM/Zero Trust), proteção de dados em repouso e trânsito, rastreabilidade via CloudTrail/GuardDuty e defesa em profundidade.
3. **Confiabilidade (Reliability)**: Arquiteturas multi-AZ/multi-Region, auto-healing, failover automático e testes de recuperação de desastres (DR - RTO/RPO).
4. **Eficiência de Performance (Performance Efficiency)**: Uso eficiente de recursos de computação, armazenamento colunar/em memória e alocação dinâmica baseada em carga.
5. **Otimização de Custos (Cost Optimization)**: Direcionamento para computação Serverless/Spot, alocação de armazenamento adequado e governança via AWS Cost Explorer.
6. **Sustentabilidade (Sustainability)**: Minimização do impacto ambiental maximizando a utilização de hardware compartilhado e algoritmos eficientes.

---

## ⚡ 2. Computação e Serverless

- **Amazon EC2 & Auto Scaling**:
  - Provisionamento via Launch Templates em Auto Scaling Groups (ASG) com políticas de scaling baseadas em métricas personalizadas do CloudWatch.
  - Combinação inteligente de instâncias On-Demand, Savings Plans e Spot Instances via *Mixed Instances Policy*.
- **Containers (Amazon EKS & AWS Fargate)**:
  - **Amazon EKS**: Orquestração Kubernetes gerenciada. Uso de EKS Managed Node Groups, Karpenter para autoscaling ultra-rápido de nós e EKS Pod Identity para credenciais IAM de cargas de trabalho.
  - **AWS Fargate**: Execução serverless de containers Docker sem gestão de instâncias EC2 adjacentes.
- **Serverless (AWS Lambda & EventBridge)**:
  - **AWS Lambda**: Funções de código orientadas a eventos. Uso de Provisioned Concurrency para eliminar *cold starts* em APIs críticas.
  - **Amazon EventBridge**: Barramento de eventos desacoplado para arquiteturas orientadas a eventos (*Event-Driven Architecture*).

---

## 💾 3. Armazenamento e Bancos de Dados

- **Armazenamento**:
  - **Amazon S3**: Buckets resilientes com versionamento, bloqueio de objetos (*Object Lock / WORM*) e ciclo de vida automatizado (*Standard -> Intelligent-Tiering -> Glacier Flexible Archive -> Glacier Deep Archive*). Criptografia obrigatória (SSE-S3 ou SSE-KMS).
  - **Amazon EBS**: Blocos para EC2 (General Purpose `gp3` configurando IOPS e Throughput de forma independente; Provisioned IOPS `io2` para bancos de dados).
  - **Amazon EFS**: Sistema de arquivos distribuído POSIX para acesso simultâneo por múltiplas instâncias EC2 e pods EKS.
- **Bancos de Dados**:
  - **Amazon Aurora (PostgreSQL/MySQL)**: Banco de dados relacional distribuído e de alta performance. Suporte a Aurora Serverless v2 e Aurora Global Database para replicação cross-region.
  - **Amazon DynamoDB**: Banco de dados NoSQL de chave-valor com latência de milissegundos de um único dígito. Uso de Single-Table Design, Global Tables (multi-region ativo-ativo) e DynamoDB Accelerator (DAX).
  - **Amazon ElastiCache**: Caching em memória de ultrabaixa latência (Redis / Memcached).

---

## 🌐 4. Redes, Conectividade e Entrega de Conteúdo

```text
               +-------------------------------------------------------+
               |                  AWS Cloud                            |
               | +---------------------------------------------------+ |
               | |                  Amazon VPC                       | |
               | |  +--------------------+   +---------------------+ | |
               | |  | Public Subnet (AZ1)|   | Private Subnet (AZ1)| | |
               | |  | - NAT Gateway      |   | - Application EC2/  | | |
               | |  | - ALB              |   |   EKS Pods          | | |
               | |  +---------+----------+   +----------+----------+ | |
               | |            |                         |            | |
               | |            v                         v            | |
               | |    Internet Gateway           VPC Endpoints       | |
               | +------------+-------------------------+------------+ |
               +--------------|-------------------------|--------------+
                              v                         v
                           Internet              Serviços S3/DynamoDB
```

- **Amazon VPC (Virtual Private Cloud)**:
  - Topologia recomendada: Subnets Públicas (ALB, NAT GW), Subnets Privadas (Workloads) e Subnets Isoladas (Databases sem saída para a internet).
  - **VPC Endpoints (Gateway e Interface / PrivateLink)**: Conexão privada aos serviços AWS (S3, DynamoDB, KMS, ECR) sem trafegar pela internet pública.
- **Roteamento e Tráfego Avançado**:
  - **AWS Transit Gateway**: Hub de rede centralizado para interconectar dezenas de VPCs e redes On-Premises via IPsec VPN ou **AWS Direct Connect**.
  - **Amazon CloudFront**: CDN global integrada com **AWS WAF** para mitigação de DDoS, caching de borda e aceleração de APIs.

---

## 🛠️ 5. Infraestrutura como Código (IaC) e CI/CD

- **Terraform (AWS Provider)**:
  - Organização em módulos reutilizáveis, gerenciamento de estado em bucket S3 remoto com trava via DynamoDB (`backend "s3"`).
- **AWS CDK (Cloud Development Kit)**:
  - Definição de infraestrutura utilizando linguagens de programação (TypeScript, Python, Go) gerando templates CloudFormation sintetizados.
- **Pipelines CI/CD (AWS CodePipeline / GitHub Actions)**:
  - Automação de testes de infraestrutura (`tflint`, `checkov`, `tfsec`) e deploys automatizados via papéis temporários com federação OIDC.

---

## 📊 6. Observabilidade e Otimização de Custos (FinOps)

- **Observabilidade**:
  - **Amazon CloudWatch**: Agregação centralizada de logs (CloudWatch Logs Insights), métricas de sistema e alarmes proativos.
  - **AWS X-Ray**: Tracing distribuído para mapeamento de latência e gargalos em microserviços e chamadas Serverless/APIs.
- **FinOps e Governança**:
  - Tagging obrigatório de recursos (`Environment`, `CostCenter`, `Owner`, `Project`).
  - **AWS Cost Explorer & Budgets**: Notificações automáticas ao atingir limites de orçamento.
  - Estratégia de precificação: Cobertura contínua de Compute Savings Plans / EC2 Instance Savings Plans para workloads baseline e Spot para workloads tolerantes a falhas.

---

## ⚙️ Protocolo de Decisão do Engenheiro AWS

1. **Defina VPC Endpoints por Padrão**: Evite o uso desnecessário de NAT Gateways para tráfego interno de serviços AWS como S3, KMS e ECR para economizar custos e aumentar a segurança.
2. **Imponha Multi-AZ**: Nenhuma carga de trabalho de produção deve ser implantada em uma única Availability Zone.
3. **Utilize IaC Declarativo com Locks Remotos**: Todo estado de infraestrutura deve ser mantido em repositório Git com controle de estado remoto e travas concorrentes.

---

## 🔗 Integração com Outras Skills

- Para políticas de IAM, SCPs, STS e controle de acessos no AWS IAM, consulte a skill [iam-access-aws](../../security/cloud-iam/iam-access-aws/SKILL.md).
- Para encriptação de objetos S3, KMS e XTS-AES em EBS, consulte a skill [cryptography-pqc-standards](../../security/crypto-pki/cryptography-pqc-standards/SKILL.md).
- Para automação de infraestrutura com Terraform e Ansible, consulte a skill [devops-engineer](../../roles/devops-engineer/SKILL.md).
- Para alinhamento aos controles da Cloud Security Alliance (CCM v4), consulte a skill [csa-cloud-security](../../security/cloud-iam/csa-cloud-security/SKILL.md).
