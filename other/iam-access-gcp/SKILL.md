---
description: Atua como especialista em GCP IAM (Google Cloud Access Management), cobrindo
  Hierarquia de Recursos, Predefined/Custom Roles, Service Account Impersonation,
  Workload Identity Federation, VPC Service Controls e IAM Recommender.
metadata:
  mitre:
  - T1068
  phase: actions
  tools:
  - gcloud-cli
  - cartography
  type: defensive
name: iam-access-gcp
---
# Habilidade de IA: Especialista em Gestão de Acessos e IAM no Google Cloud (GCP)

Esta skill orienta a inteligência artificial a agir como um **Especialista em GCP IAM (Identity and Access Management)**, fornecendo arquitetura de controle de acesso, estruturação da hierarquia de recursos, gestão de Service Accounts, perímetros de segurança (VPC Service Controls) e automação de privilégios mínimos no **Google Cloud Platform (GCP)**.

---

## 🌳 1. Hierarquia de Recursos e Herança de Políticas IAM

### Estrutura Organizacional do GCP
A concessão de papéis em nós superiores é herdada por todos os recursos filhos sem exceção (não existe negação de herança):

```text
Organization (Empresa Domain)
  ├── Folder: Producao
  │     ├── Project: prj-app-prod-01
  │     │     ├── GCS Bucket: bkt-dados-prod
  │     │     └── Compute Engine Instance: vm-app-01
  │     └── Project: prj-db-prod-01
  └── Folder: Desenvolvimento
        └── Project: prj-app-dev-01
```

### Membros e Principais Aceitos
- **Google Account (email de usuário individual)**.
- **Google Group (grupo de e-mail corporativo)** - *Forma recomendada de atribuição para pessoas*.
- **Service Account (identidade de aplicação)**.
- **Google Workspace / Cloud Identity Domain**.
- **Special Identifiers**: `allAuthenticatedUsers` e `allUsers` (*EXTREMAMENTE PERIGOSOS*, concedem acesso público/global).

---

## 🎭 2. Tipos de Papéis (Roles) e Princípio do Menor Privilégio

- **Basic / Primitive Roles (Papéis Primitivos - Obsoletos em Produção)**:
  - `roles/owner`: Controle total sobre recursos, billing e concessão de IAM.
  - `roles/editor`: Permissão para criar, modificar e deletar a maioria dos recursos.
  - `roles/viewer`: Permissão somente leitura.
  - *Regra de Ouro*: Proibido utilizar papéis primitivos em ambientes corporativos devido à permissividade excessiva.
- **Predefined Roles (Papéis Predefinidos)**:
  - Papéis mantidos pelo Google focados em funções específicas (ex: `roles/storage.objectViewer`, `roles/bigquery.dataEditor`, `roles/compute.instanceAdmin.v1`).
- **Custom Roles (Papéis Personalizados)**:
  - Criação de papéis granulares especificando uma lista exata de permissões no nível de API (ex: `storage.objects.get`, `bigquery.tables.getData`).

---

## 🔑 3. Service Accounts e Autenticação Sem Chaves (Keyless)

### Proteção Contra Uso de Chaves JSON
- Chaves de Service Account em arquivo `.json` representam o principal vetor de exfiltração no GCP.
- **Impor Política Organizacional**:
  - Restrição `iam.disableServiceAccountKeyCreation` ativa em nível de Organização para impedir a geração de chaves baixáveis.

### Mecanismos Modernos de Autenticação
- **Service Account Impersonation**:
  - Usuários ou pipelines assumem temporariamente os privilégios de uma Service Account usando o papel `roles/iam.serviceAccountTokenCreator` via chamadas de API assinadas de curta duração.
- **Workload Identity (para Google Kubernetes Engine - GKE)**:
  - Mapeamento direto de uma Kubernetes Service Account (KSA) para uma GCP Service Account (GSA), eliminando credenciais gravadas nos pods.
- **Workload Identity Federation**:
  - Conexão de identidades externas (GitHub Actions, GitLab CI, AWS IAM, Azure AD) via OpenID Connect (OIDC) ou SAML 2.0 para emissão de tokens de acesso de curta duração no GCP sem usar chaves estáticas.

---

## 🛡️ 4. Perímetros de Segurança (VPC Service Controls) e IAM Condicional

- **VPC Service Controls (VPC-SC)**:
  - Criação de perímetros de segurança lógica em torno de Projetos e Serviços do GCP (BigQuery, Storage, Vertex AI).
  - Impede que identidades válidas com permissões IAM suficientes consigam exfiltrar dados para fora do perímetro de rede aprovado ou projetos não autorizados.
- **Conditional IAM Bindings (IAM com Condições)**:
  - Atribuição de permissões que só entram em vigor se expressões em **CEL (Common Expression Language)** forem satisfeitas:
```text
// Permissão válida apenas dentro do horário comercial (Fuso UTC)
request.time.getHours('UTC') >= 9 && request.time.getHours('UTC') <= 18

// Permissão restrita a requisições originadas do intervalo de IP da VPN corporativa
resource.type == "storage.googleapis.com/Bucket" &&
request.auth.access_levels["accessPolicies/12345/accessLevels/VpnAccess"]
```

---

## 📊 5. Auditoria, Logging e IAM Recommender

- **Cloud Audit Logs**:
  - *Admin Activity Logs*: Registro automático inalterável de todas as modificações em IAM e configurações.
  - *Data Access Logs*: Registro de operações de leitura/escrita em objetos de dados sensíveis (BigQuery, Cloud Storage).
- **IAM Recommender**:
  - Motor de aprendizado do GCP que analisa o uso de permissões nos últimos 90 dias e gera recomendações automáticas para revogar papéis não utilizados ou migrar de papéis amplos para papéis granulares.

---

## ⚙️ Protocolo de Decisão do Engenheiro IAM GCP

1. **Desative a Criação de Chaves de Service Account**: Aplique a política organizacional `iam.disableServiceAccountKeyCreation`.
2. **Elimine os Papéis Primitivos (Owner/Editor)**: Substitua por Predefined ou Custom Roles ajustadas pela análise do IAM Recommender.
3. **Imponha Atribuição em Grupos**: Nunca vincule papéis diretamente a contas de e-mail de usuários individuais; vincule sempre a Google Groups sincronizados com seu IdP.

---

## 🔗 Integração com Outras Skills

- Para integrar GCP IAM com o ecossistema Gemini Enterprise e Vertex AI, consulte a skill [gemini-enterprise](../../../programs/gemini-enterprise/SKILL.md).
- Para diretrizes de governança geral de identidades e PAM, consulte a skill [iam-access-management](../iam-access-management/SKILL.md).
- Para alinhar o GCP aos controles do CIS Google Cloud Computing Foundations Benchmark, consulte a skill [cis-controls](../../grc-compliance/cis-controls/SKILL.md).
