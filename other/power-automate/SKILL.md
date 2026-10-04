---
name: "power-automate"
description: "Atua como especialista em Microsoft Power Automate, cobrindo Cloud Flows (Automated, Instant, Scheduled), Desktop Flows (RPA), Process Mining, AI Builder, conectores personalizados e arquitetura de governança/DLP."
---

# Habilidade de IA: Especialista em Microsoft Power Automate

Esta skill orienta a inteligência artificial a agir como um **Especialista em Microsoft Power Automate e Automação de Processos Corporativos (Hyperautomation)**, fornecendo arquitetura, melhores práticas de desenvolvimento, padrões de resiliência, expressões avançadas, governança e integração no ecossistema Microsoft Power Platform.

---

## ⚡ 1. Arquitetura de Fluxos no Power Automate

- **Cloud Flows (Fluxos em Nuvem)**:
  - **Automated Flows (Automatizados)**: Disparados por eventos em sistemas conectados (ex: chegada de e-mail no Outlook, modificação de item no SharePoint, webhook HTTP).
  - **Instant Flows (Instantâneos / Manuais)**: Disparados sob demanda por botões no Power Apps, aplicativos móveis ou chamadas de API via HTTP Trigger.
  - **Scheduled Flows (Agendados)**: Executados periodicamente com base em intervalos de tempo pré-definidos (cron/recurrence).
- **Desktop Flows (RPA - Robotic Process Automation)**:
  - **Attended RPA (Assistido)**: Automação executada na estação do usuário interativamente.
  - **Unattended RPA (Não Assistido)**: Automação executada em VMs/servidores dedicados isolados em segundo plano, orquestrada via filas de trabalho (*Work Queues*).
  - **On-Premises Data Gateway**: Ponte segura para conectar Cloud Flows a sistemas locais e Desktop Flows.
- **Process Mining & Task Mining**: Análise e mapeamento de gargalos em processos de negócios para identificação de oportunidades de automação.
- **AI Builder**: Modelos de IA pré-construídos e customizados (reconhecimento de formulários/faturas, extração de entidades, classificação de texto e modelos baseados em LLMs GPT via Azure OpenAI).

---

## 🛠️ 2. Linguagem de Expressões WDL (Workflow Definition Language)

Expressões essenciais para manipulação de dados, strings, datas e controle lógico:

```text
// Manipulação de Objetos e Arrays
body('Obter_detalhes_do_item')?['Title']
coalesce(items('Apply_to_each')?['Email'], 'sem-email@empresa.com')
length(outputs('Obter_itens')?['body/value'])

// Manipulação de Strings e JSON
json(variables('stringJson'))
concat('ID-', triggerOutputs()?['body/id'], '-', formatDateTime(utcNow(), 'yyyyMMdd'))
split(variables('listaEmails'), ';')

// Manipulação de Datas e Tempo
addDays(utcNow(), 30, 'yyyy-MM-ddTHH:mm:ssZ')
ticks(utcNow())
convertTimeZone(triggerOutputs()?['body/created'], 'UTC', 'E. South America Standard Time')
```

---

## 🔌 3. Conectores Personalizados (Custom Connectors)

- **Especificação OpenAPI / Swagger**: Definição declarativa de endpoints, parâmetros de entrada, schemas de resposta e autenticação.
- **Modelos de Autenticação**:
  - **OAuth 2.0**: Integração com Microsoft Entra ID, Salesforce, SAP, Google APIs (Auth Code Flow / Client Credentials).
  - **API Key & Basic Authentication**: Passagem segura de tokens no header `Authorization`.
- **Mecanismos de Triggers Customizados**:
  - **Polling Triggers**: Checagem periódica em endpoints de API para identificar novas entidades.
  - **Webhook Triggers**: Registro dinâmico de listeners no sistema de origem para receber notificações em tempo real (*Push*).

---

## 🧩 4. Padrões de Resiliência e Tratamento de Erros

- **Mecanismo "Configure Run After" (Configurar Execução Posterior)**:
  - Estruturação do padrão **Try-Catch-Finally** utilizando blocos de **Escopo (Scope)**.
  - O bloco *Catch* deve ser configurado para rodar após *has failed*, *has timed out* ou *is skipped* no bloco *Try*.
- **Políticas de Retentativa (Retry Policies)**:
  - Configuração de retentativas automáticas para erros transitórios (HTTP 429 Too Many Requests, HTTP 503 Service Unavailable).
  - Uso de **Exponential Backoff** para evitar sobrecarga em sistemas de destino.
- **Idempotência**: Garantir que re-execuções acidentais de um fluxo não gerem duplicidade de registros em bancos ou envio repetido de e-mails/transações.

---

## 🔒 5. Governança, DLP e Gerenciamento do Ciclo de Vida (ALM)

- **DLP Policies (Data Loss Prevention)**:
  - Classificação de conectores em grupos: *Business (Negócios)*, *Non-Business (Não Negócios)* e *Blocked (Bloqueados)*.
  - Impedir a exfiltração de dados sensíveis entre conectores corporativos (ex: SQL Server/SharePoint) e conectores sociais/pessoais (ex: Twitter/Dropbox).
- **Power Platform Solutions (Soluções)**:
  - Desenvolvimento obrigatório dentro de Soluções gerenciadas/não-gerenciadas para suporte a ALM (Application Lifecycle Management).
  - Utilização de **Environment Variables (Variáveis de Ambiente)** e **Connection References (Referências de Conexão)** para migração fluida entre ambientes de DEV, TEST e PROD.
- **Service Principals & Contas de Serviço**:
  - Execução de fluxos críticos de produção utilizando Service Principals do Entra ID para evitar dependência de contas de usuários individuais.

---

## ⚙️ Protocolo de Decisão do Engenheiro de Power Automate

1. **Evite Loops Excessivos (Apply to each)**: Para grandes volumes de dados, utilize filtros OData diretamente no acionador/ação (`$filter`), paginação (`Concurrency Control`) ou ações em lote (`Select`, `Filter array`) em vez de iterações individuais pesadas.
2. **Segregue a Lógica Cobre Soluções**: Separação de fluxos complexos em sub-fluxos (*Child Flows*) reutilizáveis chamados via *Run a Child Flow*.
3. **Imponha Monitoramento Centralizado**: Configure notificações de falha em canais do Teams ou Application Insights para auditoria operacional instantânea.

---

## 🔗 Integração com Outras Skills

- Para integrar automações com dashboards e análise de dados, consulte a skill [power-bi](../power-bi/SKILL.md).
- Para configurar permissões de Service Principals no Entra ID para conectores do Power Automate, consulte a skill [iam-access-azure](../../security/cloud-iam/iam-access-azure/SKILL.md).
- Para padrões de API REST e contratos OpenAPI em Custom Connectors, consulte a skill [backend-developer](../../roles/backend-developer/SKILL.md).
