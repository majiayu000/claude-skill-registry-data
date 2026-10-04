---
name: install-dev-harness
description: >
  Instala o esqueleto de um harness de desenvolvimento com gate de fase
  (planejamento vs implementação) num projeto novo ou existente — arquivo
  raiz do agente, config de harness, hooks PreToolUse/SessionStart do Claude
  Code, e um CLI mínimo de fase. Stack-agnóstico. Use quando o usuário quiser
  "trazer o harness para este projeto", proteger a fase de planejamento contra
  escrita prematura de código, ou bloquear comandos destrutivos de git/shell.
allowed-tools: Read, Write, Edit, Bash, Glob
license: MIT
metadata:
  author: exported-from-uimaker-adk
  version: "1.0"
---

# Skill — Install Dev Harness

Materializa o esqueleto descrito em `dev-harness-architect` num projeto
concreto: arquivo raiz do agente, `harness.config.json`, três hooks do
Claude Code (`PreToolUse` para escrita, `PreToolUse` para bash,
`SessionStart`) e um CLI mínimo para declarar a fase corrente de uma mudança.

Os hooks são scripts Python stdlib-only — funcionam como guardrail para
qualquer stack do projeto sendo editado (Swift, Kotlin, Python, o que for),
porque rodam como processo externo chamado pelo Claude Code, não como parte
do build do projeto. O único requisito é `python3` disponível na máquina.

## Quando usar isto vs. quando não

Use este skill quando o projeto quer **gate de fase real** (o hook bloqueia
`Write`/`Edit`/`Bash` de verdade durante planejamento). Se o objetivo é só
documentar convenções sem enforcement mecânico, um `CLAUDE.md`/`AGENTS.md`
sozinho já resolve — não instale hooks que o time não vai entender por quê
estão bloqueando.

## Passos

1. **Detecte o stack** do projeto para sugerir defaults sensatos:
   - `pyproject.toml` / `setup.cfg` → Python (`src/`, `tests/`)
   - `package.json` → Node/TS (`src/`, `test/` ou `__tests__/`)
   - `Package.swift` ou `*.xcodeproj`/`*.xcworkspace` → Swift/iOS (nome do
     módulo principal, `Tests/` ou `<Módulo>Tests/`)
   - `build.gradle(.kts)` → Kotlin/Android (`app/src/main/`, `app/src/test/`)
   - Se nada for encontrado, pergunte ao usuário.

2. **Pergunte o que falta** (use AskUserQuestion se a resposta mudar o
   resultado material):
   - Nome do arquivo raiz do agente já em uso (`CLAUDE.md`? `AGENTS.md`?) ou
     se deve criar os dois (arquivo raiz fino + fonte de verdade única —
     veja `dev-harness-architect/reference/harness-model.md#hierarquia-de-instrucoes`).
   - O projeto usa (ou vai usar) OpenSpec para gerenciar mudanças em fases?
     Se sim, o gate de fase `proposal` faz sentido. Se não, pergunte se ainda
     assim quer os hooks de segurança gerais (bloqueio de `git push`,
     `rm -rf`, secrets) sem o gate de fase — nesse caso, omita
     `planning_write_prefixes`/`code_prefixes` do config e os hooks pulam
     essa checagem automaticamente (ausência de fase declarada nunca
     bloqueia).
   - Diretórios de código-fonte e de testes reais do projeto (para preencher
     `code_prefixes`).

3. **Copie os templates** de `templates/` para o projeto alvo, substituindo
   os placeholders:

   | Template | Destino | Placeholders |
   |---|---|---|
   | `templates/harness.config.json.template` | `harness.config.json` (raiz) | `{{RULEBOOK_FILE}}` (string), `{{PLANNING_PREFIXES}}` / `{{CODE_PREFIXES}}` (arrays JSON, ex. `["src/", "tests/"]` — use `[]` se o projeto não quiser gate de fase) |
   | `templates/CLAUDE.md.template` | `CLAUDE.md` (raiz) — só se ainda não existir | `{{RULEBOOK_FILE}}`, `{{QUALITY_GATES}}`, `{{CODE_PREFIXES_HUMAN}}` (frase, ex. "`src/` e `tests/`") |
   | `templates/hooks/pre-tool-write-guard.py` | `scripts/hooks/pre-tool-write-guard.py` | nenhum — lê `harness.config.json` em runtime |
   | `templates/hooks/pre-tool-bash-guard.py` | `scripts/hooks/pre-tool-bash-guard.py` | nenhum |
   | `templates/hooks/session-start.py` | `scripts/hooks/session-start.py` | nenhum |
   | `templates/phase_cli.py` | `scripts/harness/phase_cli.py` | nenhum |

   Não sobrescreva um `CLAUDE.md`/`AGENTS.md` já existente — nesse caso, só
   adicione a seção "Fase da change" a ele, seguindo o mesmo padrão de
   `harness.config.json.template`.

4. **Registre os hooks** em `.claude/settings.json` — faça merge com o que já
   existir, nunca sobrescreva o arquivo inteiro. Conteúdo de referência em
   `templates/settings.hooks.json`.

5. **Verifique**:
   ```bash
   echo '{"source":"new"}' | python3 scripts/hooks/session-start.py
   ```
   Deve imprimir um JSON com `additionalContext` contendo a fase (não
   declarada, na primeira instalação) e a checklist de guias presentes.

6. **Explique o CLI de fase** ao usuário:
   ```bash
   python3 scripts/harness/phase_cli.py set proposal minha-mudanca
   python3 scripts/harness/phase_cli.py show
   python3 scripts/harness/phase_cli.py set apply minha-mudanca
   ```
   Enquanto a fase for `proposal`, os hooks bloqueiam escrita em
   `code_prefixes` e comandos git que mutam o repositório
   (`commit`/`add`/`merge`/`rebase`). Qualquer outra fase (ou fase não
   declarada) libera escrita normalmente — o gate só existe durante
   planejamento.

7. **Relate o que foi instalado**: liste os arquivos criados/modificados, o
   comando de verificação do passo 5, e aponte para
   `architecture-fitness-functions` como próximo passo natural (converter as
   regras do arquivo raiz em testes).

## Contrato entre hook e CLI — não quebre isto

O hook (`scripts/hooks/*.py`) e o CLI (`scripts/harness/phase_cli.py`) leem o
mesmo arquivo (`harness.config.json` → `phase_state_path`, default
`.harness/change-phase.json`) sem compartilhar código — o hook roda num
interpretador isolado e não pode importar nada do projeto. A única garantia
de sincronia é a **igualdade literal** do caminho relativo entre os dois
scripts. Se mudar o `phase_state_path` no config, ambos os scripts já leem do
config, então continuam sincronizados — mas se algum dia hardcodear o caminho
de novo em qualquer um dos dois, quebra o contrato silenciosamente. Não faça
isso.

## Segurança dos hooks — o que eles cobrem por padrão

Independente de fase, os hooks sempre bloqueiam (configurável em
`harness.config.json`):
- Escrita em nomes de arquivo de credencial conhecidos (`.env`,
  `service_account.json`, chaves privadas).
- Escrita que resolve para fora da raiz do repositório (path traversal).
- `git push`, `git reset --hard`, `git clean -f`, `git branch -D`, `rm -rf`.
- Escrita direta em `.env` via redirecionamento de shell (`> .env`,
  `tee .env`).

Isso não substitui revisão humana para `git push` — o hook bloqueia a
execução automática; o agente ainda deve pedir confirmação explícita ao
usuário antes de rodar o comando manualmente fora do hook, conforme a regra
geral de "ações difíceis de reverter" do harness.
