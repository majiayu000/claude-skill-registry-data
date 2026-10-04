---
description: Atua como especialista em OCI IAM (Oracle Cloud Infrastructure Access
  Management), cobrindo Sintaxe de Políticas OCI, Compartimentos, Domínios de Identidade,
  Dynamic Groups, Instance Principals e Políticas de Sign-on.
metadata:
  mitre:
  - T1068
  phase: actions
  tools:
  - oci-cli
  type: defensive
name: iam-access-oci
---
# Habilidade de IA: Especialista em Gestão de Acessos e IAM no Oracle Cloud (OCI)

Esta skill orienta a inteligência artificial a agir como um **Especialista em OCI IAM (Oracle Cloud Infrastructure Identity and Access Management)**, fornecendo arquitetura de controle de acesso, estrutura de compartimentos, criação de políticas declarativas em OCI Policy Language, segurança de cargas de trabalho e integração com Identity Domains.

---

## 📁 1. Compartimentos e Domínios de Identidade (Identity Domains)

### Hierarquia de Compartimentos
Compartimentos (*Compartments*) são coleções lógicas para isolamento, agrupamento e medição de consumo de recursos no OCI:

```text
Tenancy (Root Compartment)
  ├── Compartment: Network_Shared
  ├── Compartment: Production
  │     ├── Compartment: Prod_Databases
  │     └── Compartment: Prod_Apps
  └── Compartment: Development
```

### Identity Domains (Domínios de Identidade)
- **Identity Domains**: Contêineres de gerenciamento de usuários, grupos e políticas de segurança integrados nativamente ao Oracle Identity Cloud Service (IDCS).
- Suporte a múltiplos domínios de identidade em uma única Tenancy para isolamento de equipes (ex: Domínio Default para administradores, Domínio Clientes para parceiros).

---

## 📝 2. Sintaxe e Estrutura de Políticas no OCI (OCI Policy Language)

### Sintaxe Declarativa Padrão
Toda política no OCI segue a sintaxe estrita:

```text
Allow <subject> to <verb> <resource-type> in <location> where <conditions>
```

- **Subject (Sujeito)**: `group <NomeDoGrupo>`, `dynamic-group <NomeDoGrupoDinamico>`, ou `any-user`.
- **Verb (Verbo de Controle)**:
  - `inspect`: Capacidade de listar recursos sem visualizar dados ou metadados confidenciais.
  - `read`: Inclui `inspect` + capacidade de visualizar metadados e conteúdo do recurso.
  - `use`: Inclui `read` + capacidade de trabalhar com recursos existentes (iniciar, parar, associar), sem criar novos ou deletá-los.
  - `manage`: Controle total (criar, alterar, deletar, conceder).

### Exemplo de Política Corporativa OCI
```text
// Permitir que administradores de banco de dados gerenciem instâncias autônomas no compartimento de produção
Allow group DBA_Admins to manage autonomous-database-family in compartment Production:Prod_Databases

// Permitir que desenvolvedores leiam logs no compartimento de desenvolvimento apenas de IPs internos
Allow group Developers to read log-groups in compartment Development where request.network.sourceIP = '10.200.0.0/16'
```

---

## 🔤 3. Tipos de Recursos e Famílias de Recursos

- **Resource-Types Individuais**: `vcns`, `subnets`, `instances`, `buckets`, `autonomous-databases`, `vaults`.
- **Resource-Type Families (Agrupamentos)**:
  - `virtual-network-family`: Inclui VCNs, Subnets, Security Lists, Route Tables, Internet Gateways.
  - `object-family`: Inclui buckets e objetos no OCI Object Storage.
  - `database-family`: Inclui Autonomous Databases, Bare Metal / VM DB Systems, Exadata.
  - `all-resources`: Todos os recursos existentes no OCI.

---

## 🤖 4. Identidades de Cargas de Trabalho (Dynamic Groups & Principals)

- **Dynamic Groups (Grupos Dinâmicos)**:
  - Agrupamento de recursos de infraestrutura (como instâncias Compute ou Funções) com base em regras de correspondência (*Matching Rules*):
```text
// Regra: Selecionar todas as instâncias Compute que estejam no compartimento 'Production'
All {instance.compartment.id = 'ocid1.compartment.oc1..exampleuniqueID'}

// Regra: Selecionar instâncias com a tag 'Environment = Prod'
All {resource.type = 'instance', resource.tag.Operations.Environment = 'Prod'}
```
- **Instance Principals**: Permite que uma instância Compute faça chamadas de API autenticadas aos serviços do OCI sem a necessidade de gravar API Keys ou credenciais no disco da VM.
- **Resource Principals**: Permite que OCI Functions, OKE (Kubernetes) e Data Science Jobs se autentiquem de forma segura para acessar outros recursos da Tenancy.

---

## 🛡️ 5. Políticas de Autenticação, MFA e Segurança

- **Sign-on Policies**:
  - Imposição de autenticação multifator (MFA) obrigatória para acesso à Console do OCI.
  - Bloqueio de logins fora de intervalos de IP confiáveis corporativos.
- **Federated Identity**:
  - Integração com Microsoft Entra ID, Okta ou SAML 2.0 Identity Providers para Single Sign-On (SSO).
- **Audit Service**:
  - Log auditável imutável de todas as chamadas de API de controle e plano de dados gravados no formato JSON padrão CloudEvents.

---

## ⚙️ Protocolo de Decisão do Engenheiro IAM OCI

1. **Estruture Compartimentos Antes das Políticas**: Mantenha uma hierarquia lógica clara de compartimentos separando rede, bancos e aplicações por ambiente.
2. **Utilize Verbos Mínimos**: Prefira `use` ou `read` em vez de `manage` para equipes operacionais do dia a dia.
3. **Imponha Instance Principals**: Bloqueie a geração de API Keys em contas de usuários humanos para uso automatizado de scripts; exija o uso de Dynamic Groups e Instance/Resource Principals.

---

## 🔗 Integração com Outras Skills

- Para diretrizes gerais de controle de acesso, RBAC e PAM, consulte a skill [iam-access-management](../iam-access-management/SKILL.md).
- Para diretrizes de governança de segurança em nuvem, consulte a skill [csa-cloud-security](../csa-cloud-security/SKILL.md).
- Para alinhar o OCI aos controles de rede e criptografia, consulte a skill [network-security-onprem-cloud](../../grc-compliance/network-security-onprem-cloud/SKILL.md).
