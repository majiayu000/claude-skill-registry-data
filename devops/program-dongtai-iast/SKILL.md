---
name: program-dongtai-iast
description: Guia Definitivo e Padrões de Engenharia para DongTai IAST (github.com/HXSecurity/DongTai), cobrindo o framework open-source de Interactive Application Security Testing passivo, deploy do DongTai Server com Docker Compose, instalação de agentes (Java, Python, Go, PHP, Node.js), regras de Taint Tracking (Sources, Propagators, Sanitizers, Sinks), e integração com suítes de teste de QA no CI/CD.
metadata:
  type: defensive
  phase: testing
  mitre:
    - T1190
  tools:
    - dongtai-iast
    - docker-compose
---

# Habilidade de IA: Guia e Engenharia com DongTai IAST

Esta skill fornece orientação técnica canônica, comandos operacionais e padrões de engenharia para o **DongTai IAST** ([github.com/HXSecurity/DongTai](https://github.com/HXSecurity/DongTai)), o primeiro framework open-source de **Interactive Application Security Testing (IAST)** passivo, desenvolvido pela Huoxian Security (HXSecurity).

---

## 🧭 Visão Geral e Arquitetura do DongTai IAST

O DongTai IAST utiliza uma abordagem de **IAST Passivo**, onde agentes de instrumentação instalados dentro da aplicação monitoram o fluxo de dados em memória à medida que requisições reais ou de testes automatizados chegam, sem gerar tráfego invasivo adicional e sem necessidade de crawlers externos.

```
┌────────────────────────────────────────────────────────────────────────┐
│                      ARQUITETURA DONGTAI IAST                          │
└────────────────────────────────────────────────────────────────────────┘
  [ TESTES DE QA / TRÁFEGO REAL ] (Playwright, Cypress, Postman, JMeter)
                 │ (Requisições HTTP normais de funcionalidade)
                 ▼
  [ AMBIENTE INSTRUMENTADO (Aplicação Java, Python, Go, PHP, Node.js) ]
  ┌────────────────────────────────────────────────────────────────────┐
  │ AGENTE DONGTAI (dongtai-agent.jar / dongtai-agent-python)          │
  │                                                                    │
  │  1. Ingestão de Requisição ──► SOURCE (Etiqueta dados como sujos)  │
  │  2. Métodos Internos       ──► PROPAGATOR (Rastreia contaminação)  │
  │  3. Sanitizadores          ──► FILTER (Verifica se neutralizou)    │
  │  4. Chamadas Críticas      ──► SINK (Detecta violação de segurança)│
  └─────────────────────────────────┬──────────────────────────────────┘
                                    │ (Relato assíncrono via OpenAPI)
                                    ▼
  [ DONGTAI SERVER ] (Orquestrador & Motor de Análise)
  ┌────────────────────────────────────────────────────────────────────┐
  │  - DongTai OpenAPI Gateway: Recebe telemetria e batimentos dos nós │
  │  - DongTai Engine: Analisa os grafos de contaminação e stack trace │
  │  - DongTai Web UI: Dashboard de gestão de vulnerabilidades e regras│
  │  - Armazenamento: MySQL + Redis                                    │
  └────────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Deploy do DongTai Server (Docker Compose)

O DongTai Server é implantado centralmente utilizando contêineres Docker.

### 1. Clonagem e Inicialização:
```bash
# Clonar o repositório oficial do DongTai
git clone https://github.com/HXSecurity/DongTai.git
cd DongTai

# Subir a infraestrutura completa do servidor
docker-compose -f docker-compose.yml up -d
```

### 2. Portas e Componentes em Execução:
- **Painel Web (DongTai Web UI)**: `http://localhost:80` ou `http://localhost:8888`
- **Gateway OpenAPI**: `http://localhost:8888/openapi`
- **Credenciais Padrão**: `admin` / `admin` (troque imediatamente no primeiro login).
- **Geração de Token**: No painel web, acesse **System Settings ➔ Agent Deployment** para obter o `Token` único de autenticação dos agentes.

---

## 💻 Instalação e Execução dos Agentes por Linguagem

### 1. Agente Java (Spring Boot, Tomcat, WildFly)
O agente Java do DongTai é composto por três módulos internos (`dongtai-agent.jar`, `dongtai-core.jar` e `dongtai-spy.jar`).

```bash
# Baixar o agente Java compilado
curl -X GET "http://dongtai-server:8888/openapi/api/v1/agent/download?url=http://dongtai-server:8888/openapi&language=java" \
     -H "Authorization: Token SEU_TOKEN_AQUI" -o dongtai-agent.jar

# Executar a aplicação Java com o agente acoplado
java -javaagent:/opt/dongtai/dongtai-agent.jar \
     -Ddongtai.server.url=http://dongtai-server:8888/openapi \
     -Ddongtai.server.token=SEU_TOKEN_AQUI \
     -Ddongtai.app.name=EcommerceBackend \
     -Ddongtai.app.version=v1.2.0 \
     -Ddongtai.app.create=true \
     -jar app.jar
```

### 2. Agente Python (Django, Flask, FastAPI)
O agente Python utiliza *monkey patching* dinâmico para interceptar métodos no runtime CPython.

```bash
# Instalar o pacote do agente via pip
pip install dongtai-agent-python

# Definir variáveis de ambiente para inicialização automática
export DONGTAI_IAST_SERVER_URL="http://dongtai-server:8888/openapi"
export DONGTAI_IAST_SERVER_TOKEN="SEU_TOKEN_AQUI"
export DONGTAI_IAST_PROJECT_NAME="FinanceAPI"
export DONGTAI_IAST_PROJECT_VERSION="v2.0.0"

# Inicializar aplicação Django / Flask
python manage.py runserver 0.0.0.0:8000
```

### 3. Agente Go (Golang)
O agente Go realiza a reescrita dinâmica de endereços de funções e hooking de símbolos em tempo de execução:
```bash
# Integrar o pacote dongtai-agent-go no arquivo main.go
import _ "github.com/HXSecurity/dongtai-agent-go"
```

---

## 🔬 Configuração de Regras e Estratégia de Hooks (Hook Strategy)

O DongTai classifica métodos em quatro categorias dentro de seu motor de regras:

```
┌────────────────────────────────────────────────────────────────────────┐
│                   TIPOS DE NÓS NO GRAFO DE TAINT                       │
└────────────────────────────────────────────────────────────────────────┘
  1. SOURCE: Entrada de dados (Ex: javax.servlet.ServletRequest.getParameter)
  2. PROPAGATOR: Concatenação (Ex: java.lang.StringBuilder.append)
  3. FILTER: Validação (Ex: org.apache.commons.lang3.StringEscapeUtils.escapeHtml4)
  4. SINK: Consumo perigoso (Ex: java.sql.Statement.execute, java.lang.Runtime.exec)
```

### Exemplo de Estrutura de Regra de Sink no DongTai:
- **Classe Alvo**: `java.lang.ProcessBuilder`
- **Método**: `start()`
- **Assinatura**: `()Ljava/lang/Process;`
- **Tipo de Vulnerabilidade**: `Command Injection (CWE-78)`
- **Condição**: Se qualquer argumento que alcançou o `ProcessBuilder` contiver uma etiqueta de contaminação ativa vinda de um `SOURCE` sem passar por um `FILTER` homologado, o DongTai registra a vulnerabilidade com stack trace completo.

---

## 🔄 Integração com Pipelines de DevSecOps e QA

O grande benefício do DongTai IAST é sua capacidade de transformar a suíte de testes de QA existente em uma auditoria de segurança contínua sem nenhum tempo adicional de execução.

### Workflow no CI/CD (GitHub Actions / GitLab CI):
```
┌────────────────────────┐
│ 1. Build da Aplicação  │
└───────────┬────────────┘
            ▼
┌────────────────────────┐
│ 2. Start em Staging    │ ──► (Inicia a aplicação com dongtai-agent acoplado)
└───────────┬────────────┘
            ▼
┌────────────────────────┐
│ 3. Execução de QA E2E  │ ──► (Roda Playwright / Cypress / Newman / Selenium)
└───────────┬────────────┘
            ▼
┌────────────────────────┐
│ 4. Quality Gate Check  │ ──► (Consulta API do DongTai Server: Há vulnerabilidades?)
└───────────┬────────────┘
            ▼
┌────────────────────────┐
│ 5. Aprova ou Bloqueia  │
└────────────────────────┘
```

### Script de Verificação de Quality Gate via API:
```bash
#!/usr/bin/env bash
set -euo pipefail

DONGTAI_URL="http://dongtai-server:8888/openapi"
TOKEN="SEU_TOKEN_AQUI"
PROJECT_NAME="EcommerceBackend"

# Consultar total de vulnerabilidades críticas ou altas no projeto
FINDINGS=$(curl -s -X GET "${DONGTAI_URL}/api/v1/vulns?project_name=${PROJECT_NAME}&level=1,2" \
     -H "Authorization: Token ${TOKEN}" | jq '.data | length')

echo "Total de vulnerabilidades graves encontradas no IAST: ${FINDINGS}"

if [ "${FINDINGS}" -gt 0 ]; then
    echo "❌ Quality Gate FALHOU: O DongTai identificou vulnerabilidades críticas em tempo de execução."
    exit 1
else
    echo "✅ Quality Gate APROVADO: Nenhuma vulnerabilidade crítica ativa detectada."
fi
```

---

## 🔗 Integração com Outras Skills do Repositório

- **[iast-interactive-testing](../../security/appsec/iast-interactive-testing/SKILL.md)**: Teoria formal de Interactive Application Security Testing e comparação com SAST/DAST.
- **[program-opengrep](../program-opengrep/SKILL.md)**: Complementa a análise estática prévia das regras de Taint.
- **[qa-engineer](../../roles/qa-engineer/SKILL.md)**: Conexão direta com a automação de testes funcionais (Playwright, Cypress, Pytest).
- **[devsecops-engineer](../../security/ops-architecture/devsecops-engineer/SKILL.md)**: Configuração de Quality Gates automatizados no pipeline CI/CD.
