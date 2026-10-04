---
name: program-owasp-zap
description: Guia Definitivo e Padrões de Engenharia para OWASP ZAP (zaproxy.org), cobrindo o scanner dinâmico de segurança de aplicações web e APIs (DAST), ZAP Automation Framework (planos AF em YAML), scans empacotados em Docker (zap-baseline, zap-full-scan, zap-api-scan), Ajax Spider para SPAs, autenticação avançada, REST API e integração CI/CD.
metadata:
  type: defensive
  phase: testing
  mitre:
    - T1190
  tools:
    - zaproxy
    - zap-cli
    - docker
---

# Habilidade de IA: Guia e Engenharia com OWASP ZAP (Zed Attack Proxy)

Esta skill fornece orientação técnica canônica, comandos operacionais e padrões de engenharia para o **OWASP ZAP (Zed Attack Proxy)** ([zaproxy.org](https://www.zaproxy.org/)), a ferramenta de código aberto mais utilizada no mundo para **Dynamic Application Security Testing (DAST)** e inspeção de tráfego HTTP/HTTPS.

---

## 🧭 Visão Geral e Modos de Operação do ZAP

O OWASP ZAP opera como um proxy de interceptação e scanner dinâmico de vulnerabilidades, operando em três modalidades principais:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        MODOS DE EXECUÇÃO DO ZAP                        │
└────────────────────────────────────────────────────────────────────────┘
  1. Desktop GUI / HUD: Auditoria interativa, exploração manual e depuração.
  2. Headless Daemon: Serviço de segundo plano expondo REST API (porta 8080).
  3. ZAP Automation Framework (AF): Execução headless dirigida por arquivo YAML.
  4. Docker Packaged Scans: Contêineres efêmeros para pipelines de CI/CD.
```

---

## 📄 ZAP Automation Framework (AF) — Padrão Canônico em YAML

O **Automation Framework (AF)** é o padrão moderno recomendado pela equipe do ZAP para orquestrar varreduras completas sem necessidade de scripts externos.

### 1. Estrutura Canônica de um Plano de Automação (`zap-scan-plan.yaml`)
```yaml
---
env:
  contexts:
    - name: "Ecommerce-Staging"
      urls:
        - "https://staging.empresa.com"
      includePaths:
        - "https://staging.empresa.com/.*"
      excludePaths:
        - "https://staging.empresa.com/logout.*"
        - "https://staging.empresa.com/admin/delete.*"
      authentication:
        method: "json"
        parameters:
          loginUrl: "https://staging.empresa.com/api/v1/auth/login"
          loginRequestData: '{"username": "{%username%}", "password": "{%password%}"}'
        verification:
          method: "response"
          loggedInRegex: '"authenticated":\s*true'
          loggedOutRegex: '"error":\s*"unauthorized"'
      users:
        - name: "test-user"
          credentials:
            username: "qa-sec-user"
            password: "SecurePassword123!"
  parameters:
    failOnError: true
    failOnWarning: false
    progressToStdout: true

jobs:
  # 1. Spider Tradicional (Crawling de HTML)
  - type: spider
    parameters:
      context: "Ecommerce-Staging"
      user: "test-user"
      maxDuration: 10
      maxDepth: 5

  # 2. Ajax Spider (Navegação Headless em SPAs React/Vue via Chromium)
  - type: spiderAjax
    parameters:
      context: "Ecommerce-Staging"
      user: "test-user"
      maxDuration: 15
      browserId: "firefox-headless"

  # 3. Configuração de Varredura Passiva
  - type: passiveScan-config
    parameters:
      maxAlertsPerRule: 5
      scanOnlyInScope: true

  # 4. Aguardar Conclusão da Análise Passiva
  - type: passiveScan-wait
    parameters:
      maxDuration: 10

  # 5. Varredura Ativa (Fuzzing de Parâmetros e Injeções)
  - type: activeScan
    parameters:
      context: "Ecommerce-Staging"
      user: "test-user"
      policy: "Default Policy"
      maxRuleDurationInMins: 5
      maxScanDurationInMins: 30

  # 6. Geração de Relatórios (HTML, JSON e SARIF)
  - type: report
    parameters:
      template: "traditional-html"
      reportDir: "/zap/wrk/reports"
      reportFile: "zap-report.html"
  - type: report
    parameters:
      template: "sarif-json"
      reportDir: "/zap/wrk/reports"
      reportFile: "zap-report.sarif"
```

### 2. Execução do Plano via CLI:
```bash
# Executar o plano YAML em modo headless
./zap.sh -cmd -autorun zap-scan-plan.yaml

# Gerar template mínimo de plano YAML
./zap.sh -cmd -autogenmin template-min.yaml

# Gerar template com todos os parâmetros possíveis
./zap.sh -cmd -autogenmax template-max.yaml
```

---

## 🐳 Execução via Scans Empacotados em Docker

Para pipelines rápidos de CI/CD, o ZAP disponibiliza três scripts empacotados em sua imagem oficial `zaproxy/zap-stable`:

### 1. Baseline Scan (`zap-baseline.py`)
Executa spider rápido e **análise passiva** (cabeçalhos, cookies, CSP, SSL). Não envia payloads agressivos.
```bash
docker run --rm -v $(pwd):/zap/wrk:rw -t zaproxy/zap-stable zap-baseline.py \
    -t https://staging.empresa.com \
    -r zap-baseline-report.html \
    -J zap-baseline-report.json \
    -I
```

### 2. Full Active Scan (`zap-full-scan.py`)
Executa spider completo, Ajax spider e **varredura ativa profunda** com injeções de parâmetros.
```bash
docker run --rm -v $(pwd):/zap/wrk:rw -t zaproxy/zap-stable zap-full-scan.py \
    -t https://staging.empresa.com \
    -r zap-full-report.html \
    -n zap.context \
    -m 30
```

### 3. API Scan (`zap-api-scan.py`)
Projetado especificamente para APIs REST (OpenAPI/Swagger), GraphQL e SOAP.
```bash
# Varredura de contrato OpenAPI v3
docker run --rm -v $(pwd):/zap/wrk:rw -t zaproxy/zap-stable zap-api-scan.py \
    -t https://staging.empresa.com/api/v3/openapi.json \
    -f openapi \
    -r zap-api-report.html

# Varredura de endpoint GraphQL
docker run --rm -v $(pwd):/zap/wrk:rw -t zaproxy/zap-stable zap-api-scan.py \
    -t https://staging.empresa.com/graphql \
    -f graphql \
    -r zap-graphql-report.html
```

---

## 🔑 Autenticação Avançada e Injeção de Headers

### 1. Injeção de Bearer Token / API Key Estática:
```bash
# Injetar cabeçalho Authorization em todas as requisições disparadas pelo ZAP
docker run --rm -v $(pwd):/zap/wrk:rw -t zaproxy/zap-stable zap-api-scan.py \
    -t https://api.empresa.com/openapi.json \
    -f openapi \
    -z "-config replacer.full_list(0).description=AuthHeader \
        -config replacer.full_list(0).enabled=true \
        -config replacer.full_list(0).matchtype=REQ_HEADER \
        -config replacer.full_list(0).matchstr=Authorization \
        -config replacer.full_list(0).regex=false \
        -config replacer.full_list(0).replacement='Bearer eyJhbGciOiJIUzI1Ni...'"
```

---

## 🚀 Integração em CI/CD (GitHub Actions Workflow)

```yaml
name: DAST Dynamic Security Scan (OWASP ZAP)

on:
  schedule:
    - cron: '0 2 * * *' # Execução noturna diária às 02:00
  workflow_dispatch:

jobs:
  dast_scan:
    name: OWASP ZAP Full Scan
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Create Reports Directory
        run: mkdir -p reports

      - name: Run OWASP ZAP Automation Plan
        uses: zaproxy/action-full-scan@v0.12.0
        with:
          target: 'https://staging.empresa.com'
          rules_file_name: '.zap/rules.tsv'
          cmd_options: '-a'

      - name: Upload ZAP HTML Report
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: zap-scan-report
          path: report_html.html
```

---

## 🔗 Integração com Outras Skills do Repositório

- **[dast-application-testing](../../security/appsec/dast-application-testing/SKILL.md)**: Teoria e metodologia formal de Testes Dinâmicos de Segurança de Aplicações.
- **[pentester-owasp-wstg](../../security/appsec/pentester-owasp-wstg/SKILL.md)**: Aplicação do ZAP em conjunto com a metodologia de pentest OWASP WSTG.
- **[program-containers](../containers/SKILL.md)**: Execução segura de contêineres Docker isolados em runners de CI/CD.
- **[devsecops-engineer](../../security/ops-architecture/devsecops-engineer/SKILL.md)**: Gestão de Quality Gates e mitigação de vulnerabilidades DAST.
