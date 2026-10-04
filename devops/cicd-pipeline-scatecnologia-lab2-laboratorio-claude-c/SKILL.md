---
name: cicd-pipeline
description: Use esta skill ao criar ou alterar qualquer arquivo de pipeline (.github/workflows/*.yml), Dockerfile, docker-compose.yml, ou configuração de lint/testes usada pela esteira de CI/CD. Garante que o padrão adotado no projeto (jobs separados, publish/deploy Docker só manual, sem segredos hardcoded) seja mantido.
---

# Skill: CI/CD Pipeline

Aplica-se sempre que a tarefa envolver:
- Criar ou editar workflows em `.github/workflows/`
- Criar ou editar `Dockerfile`, `Dockerfile.python` ou `docker-compose.yml`
- Adicionar/alterar lint (`eslint.config.js`, `.flake8`) ou scripts de teste usados pela esteira
- Configurar segurança de pipeline (secrets, scans, Dependabot, CodeQL)

Referência conceitual completa: `docs/DEVOPS_GUIA.md` e `docs/ROTEIRO_CICD_CLAUDE_CODE.md`.

---

## Regras obrigatórias deste projeto

1. **Jobs separados, não um job monolítico.** Lint, teste unitário, teste de integração e segurança são jobs distintos em `ci.yml`, para falhar rápido e mostrar claramente o que quebrou.
2. **Testes de integração no CI usam `services:` do GitHub Actions.** Os containers de `postgres`/`redis`/`mongo` no CI são infraestrutura do runner do GitHub; localmente, o `docker-compose.yml` sobe o mesmo Postgres na porta 5151.
3. **Em workflows Docker, só build e scan são automáticos.** `docker-build.yml` roda build + scan Trivy em push/PR na `main`; os jobs `publish*` e `deploy*` devem ter `if:` com `github.event_name == 'workflow_dispatch'` (disparo manual). O hook `pipeline-guardrail.js` bloqueia edições que removam essa trava. Não enfraqueça o scan (ex.: tirar `exit-code: "1"`) para fazer o pipeline passar — corrija a imagem.
4. **Nunca hardcode segredos em YAML.** Use `${{ secrets.NOME_DO_SECRET }}`. Se um novo secret for necessário, explique ao usuário como criá-lo em `Settings → Secrets and variables → Actions` — não peça para colar o valor no chat.
5. **SQL sempre parametrizado, mesmo em scripts auxiliares de CI** (ex.: scripts de seed de banco para testes) — mesma regra do `CLAUDE.md` do projeto.
6. **Antes de alterar um workflow, explique o plano e o diff esperado**, seguindo a regra geral do `CLAUDE.md`.

---

## Passos ao criar um novo workflow

1. Definir o gatilho (`on:`) mais restrito possível para o objetivo (ex.: `pull_request` para validação, `workflow_dispatch` para ações manuais/sensíveis).
2. Listar os jobs e suas dependências (`needs:`) — pense em qual falha deve interromper o quê.
3. Usar `actions/checkout@v4`, `actions/setup-node@v4`, `actions/setup-python@v5` (versões fixas, não `@main`/`@latest`).
4. Adicionar cache de dependências (`actions/cache` ou o cache nativo de `setup-node`/`setup-python`) para reduzir tempo de execução.
5. Rodar localmente antes de commitar: reproduzir os comandos do workflow (`npm run lint`, `pytest`, etc.) manualmente para confirmar que passam.
6. Explicar como testar: qual evento dispara o workflow e onde ver o resultado (aba Actions do GitHub).

## Passos ao alterar Dockerfile/docker-compose

1. Validar localmente: `docker compose up --build -d`, testar login/clientes/fornecedores em `http://localhost:3000`, e rodar o mesmo scan do CI: `docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy:0.70.0 image --severity CRITICAL,HIGH --ignore-unfixed --exit-code 1 <imagem>`.
1.1. Configuração de rede vem de variáveis de ambiente (`DB_HOST`, `DB_PORT`, `FORNECEDORES_HOST`, `FORNECEDORES_PORT`, `FLASK_HOST`) — nunca fixe `localhost` no código que roda em container.
2. Manter imagens base fixadas por versão (ex.: `node:24-alpine`, não `node:latest`).
3. Multi-stage build quando fizer sentido (build separado de runtime), para imagem final menor.
4. Nunca copiar `.env` ou segredos para dentro da imagem.

## O que NÃO fazer

- Não remover ou enfraquecer o `security-guardrail.js` ou o `pipeline-guardrail.js` para "fazer o teste passar".
- Não instalar ferramentas de CI adicionais (SonarQube, Snyk, etc.) sem justificar o custo/benefício ao usuário primeiro.
- Não migrar de GitHub Actions para outra plataforma sem que o usuário peça explicitamente (use o agente `devops-engineer` para essa avaliação).
