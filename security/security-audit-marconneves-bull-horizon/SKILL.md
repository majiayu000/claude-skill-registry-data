---
name: security-audit
description: Auditoria de segurança aplicada (AppSec). Varre código, dependências e configurações contra OWASP Top 10 / CWE Top 25, identifica segredos expostos, valida controles de auth/authz e gera relatório priorizado. Use para "revisar segurança", "auditar vulnerabilidades", "threat modeling" ou "security review".
---

# Skill: Security Audit (Shift-Left AppSec)

Esta skill é acionada pelo `.claude/agents/security.md` (e ocasionalmente pelo `architect` para threat modeling). Aplica boas práticas universais de AppSec adaptadas à stack detectada no bootstrap (`memorys/architecture.md`).

## Pré-requisitos

- Antes de auditar, ler `memorys/architecture.md` (stack, fluxos de dados, classificação de dados) e `memorys/guidelines.md` (vulnerabilidades já remediadas — não revisitar a fundo o que já foi corrigido).
- Identificar o escopo: PR completo, módulo específico ou superfície sensível (auth, upload, integração externa, etc.).

## Workflow de Execução

### 1. Threat Modeling (quando acionado pelo Architect, antes da implementação)

Aplique a abordagem **STRIDE** para enumerar ameaças:
- **S**poofing — autenticação fraca, sessões previsíveis.
- **T**ampering — integridade de dados em trânsito e repouso.
- **R**epudiation — auditoria, logs imutáveis.
- **I**nformation Disclosure — vazamento por logs, mensagens de erro, headers, response bodies.
- **D**enial of Service — limites, rate limit, payloads maliciosos.
- **E**levation of Privilege — bypass de authz, escalação horizontal/vertical.

Registre o modelo em `memorys/architecture.md` na seção *Modelo de Ameaças* e, quando relevante, abra ADR via `.claude/skills/guard/SKILL.md`.

### 2. Auditoria de Código (OWASP Top 10 & CWE Top 25)

Varra o diff/código alvo procurando, no mínimo:

| # | Categoria | O que checar |
|---|---|---|
| A01 | Broken Access Control | endpoints sem authz, IDOR, path traversal, escalação de privilégio, métodos HTTP inseguros, redirects abertos |
| A02 | Cryptographic Failures | algoritmos fracos (MD5/SHA1/DES), TLS desativado, segredos em logs, KDF inadequado para senhas (use bcrypt/argon2/scrypt), aleatoriedade não criptográfica |
| A03 | Injection | SQL/NoSQL injection, command injection, LDAP/XPath injection, template injection, header injection |
| A04 | Insecure Design | falta de rate limit, ausência de validação de regra de negócio, lógica que confia em entrada do cliente |
| A05 | Security Misconfiguration | headers ausentes (CSP, HSTS, X-Frame-Options), CORS permissivo, debug ligado em prod, versões expostas, defaults inseguros |
| A06 | Vulnerable & Outdated Components | dependências com CVE conhecida, versões descontinuadas |
| A07 | Identification & Authentication Failures | senhas fracas permitidas, sessão sem expiração, ausência de MFA em fluxos críticos, JWT sem `exp`/assinatura |
| A08 | Software & Data Integrity Failures | desserialização insegura, dependências não verificadas, CI/CD sem assinatura |
| A09 | Security Logging & Monitoring Failures | logs ausentes em eventos críticos, logs com PII, ausência de alertas |
| A10 | SSRF | requisições para URLs controladas pelo usuário sem allowlist |

Considere também os **CWE Top 25** quando a stack tiver superfícies específicas (ex: CWE-798 hardcoded credentials, CWE-352 CSRF, CWE-434 unrestricted file upload).

### 3. Secret Scanning

Varra o diff por padrões de segredos vazados:
- Tokens (`AKIA[0-9A-Z]{16}`, `ghp_*`, `xoxb-*`, JWTs reais, chaves privadas PEM).
- Strings com alta entropia em arquivos não-binários.
- Credenciais em arquivos de configuração versionados (`.env`, `application.yml`, `appsettings.json`).
- URLs com `user:password@host`.

Se encontrado: **Critical**. Recomenda-se rotação imediata e remoção via `git filter-repo` ou equivalente — alertar o usuário sobre necessidade de purga do histórico.

### 4. Auditoria de Dependências (CVEs)

Em colaboração com `.claude/skills/infrastructure/SKILL.md`:
- Executar o auditor nativo da stack: `npm audit`, `pip-audit`, `cargo audit`, `mvn dependency-check`, `bundle audit`, etc.
- Para cada vulnerabilidade, classificar:
  - **Critical**: bloqueador, exige atualização ou mitigação imediata.
  - **High**: bloqueador para release, mitigação aceita pelo Tech Lead.
  - **Medium/Low**: task separada com prioridade P2/P3.

### 5. Validação de Configuração

Cheque arquivos de infra/config para problemas conhecidos:
- Cookies sem `Secure`, `HttpOnly`, `SameSite`.
- CORS com `*` em rotas autenticadas.
- CSP ausente ou com `unsafe-inline`/`unsafe-eval` em produção.
- Storage S3/Blob com ACL pública não intencional.
- IAM com permissões excessivas (`*:*`).
- Ports/serviços expostos sem necessidade.

### 6. Relatório de Achados

Gere `docs/todo/<NNN>/security-review.md` com a estrutura:

```markdown
# Security Review — Task NNN

**Auditor:** security-specialist
**Data:** YYYY-MM-DD
**Escopo:** <arquivos/módulos auditados>

## Sumário
- Critical: N
- High: N
- Medium: N
- Low: N

## Achados

### [SEC-001] <Título> — Severidade: Critical
- **Categoria:** OWASP A03 / CWE-89 (SQL Injection)
- **Localização:** `arquivo.ts:42`
- **Descrição:** <o que está vulnerável e por quê>
- **Exploração possível:** <cenário de ataque>
- **Recomendação:** <mitigação concreta, com referência à boa prática>
- **Status:** [ ] Aberto / [ ] Mitigado / [ ] Aceito (com justificativa)

### [SEC-002] ...

## Decisão de Liberação
- [ ] Aprovado para Ops (todos Critical/High mitigados ou aceitos)
- [ ] Bloqueado (motivo: ...)
```

### 7. Loop com Developer

- Achados **Critical/High** retornam ao `.claude/agents/developer.md` como bloqueadores. O Developer corrige e Security re-audita o ponto específico.
- Achados **Medium/Low** entram como tasks separadas (`P2`/`P3`) em `docs/todo/`, salvo decisão diferente do Tech Lead.

### 8. Atualização de Memória

Após o ciclo:
- Vulnerabilidades corrigidas com aprendizado relevante → entrada em `memorys/guidelines.md` (seção *Antipadrões e Aprendizados*).
- Decisões arquiteturais de segurança → `memorys/architecture.md`.
- Controles ativos no projeto (ex: bcrypt rounds, política de senha, provider de identidade) → `memorys/architecture.md`.
