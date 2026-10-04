---
name: dl-rails-code-audit
description: >-
  Audita projetos Ruby on Rails 7 ou 8 (com banco Oracle ou MariaDB/MySQL) em
  busca de falhas de segurança, gambiarras, código fora do padrão, antipadrões
  de ActiveRecord e problemas específicos de Oracle/MariaDB. Use SEMPRE que o
  usuário pedir para "revisar", "auditar", "achar problemas", "code review",
  "checar segurança", "encontrar gambiarras" ou "analisar a qualidade" de um
  codebase, app, repositório, PR ou diff Rails — mesmo que não diga
  explicitamente a palavra "auditoria". Também acione quando o usuário for líder
  técnico/chefe de desenvolvimento querendo padronizar revisões de equipe em
  Rails. Não use para apps que não sejam Rails nem para criação de features.
---

# Rails Code Audit

Auditoria estruturada de projetos Rails 7/8 com banco Oracle ou MariaDB/MySQL,
voltada para líderes técnicos que precisam de revisões consistentes e acionáveis
da equipe.

## Objetivo

Produzir um relatório que um chefe de desenvolvimento possa usar diretamente em
code review: cada problema vem com severidade, localização (`arquivo:linha`),
explicação do risco e uma correção sugerida concreta.

## Quando rodar e o que esperar do usuário

Antes de começar, determine o **escopo**:

- **Projeto inteiro**: o usuário aponta um repositório/diretório.
- **Diff / PR**: o usuário quer revisar só o que mudou. Se houver um repo git,
  use `git diff` (ou `git diff <base>...<head>`) para limitar a análise aos
  arquivos alterados. Ainda assim leia o contexto vizinho desses arquivos.

Se o escopo não estiver claro, pergunte de forma curta antes de gastar tempo
varrendo tudo. Não peça mais do que isso — não interrogue o usuário.

## Fluxo de trabalho

Siga esta ordem. Cada passo é descrito em detalhe nos arquivos de `references/`.

### 1. Reconhecimento do projeto

Identifique a base antes de julgar o código:

- Versão do Rails e Ruby: leia `Gemfile`, `Gemfile.lock`, `config/application.rb`.
- Banco de dados: leia `config/database.yml` e o `Gemfile` para detectar o
  adapter. Procure por `oracle-enhanced`/`ruby-oci8` (Oracle) ou
  `mysql2`/`trilogy` (MariaDB/MySQL). Isso determina quais regras de banco
  aplicar — veja `references/database-oracle-mariadb.md`.
- Estrutura: `app/`, `lib/`, `config/`, presença de `service objects`,
  `concerns`, `jobs`, gems de teste.
- Ferramentas já presentes: `.rubocop.yml`, `brakeman`, `bundler-audit`,
  `.ruby-version`, CI configs. Respeite convenções já adotadas pelo time.

### 2. Rodar ferramentas automáticas (quando disponíveis)

Se o ambiente permitir executar comandos no projeto, tente — mas **nunca trave**
a auditoria se elas não estiverem instaladas; a análise manual é a base.

```bash
# Segurança estática Rails
bundle exec brakeman -q -f json

# Vulnerabilidades conhecidas em dependências
bundle exec bundler-audit check --update

# Estilo / convenções (só reporte, não reescreva em massa)
bundle exec rubocop --format json
```

Execute cada ferramenta separadamente e registre claramente uma indisponibilidade
ou falha de execução; não a esconda nem a trate como resultado sem achados. Use
a saída como **sinal de ferramenta**, não como achado confirmado. Só promova um
alerta ao relatório de achados depois de verificar o código, a configuração e o
caminho de execução relevante. Identifique alertas não confirmados em uma seção
separada, com a ferramenta que os produziu e o que falta verificar.

### 3. Análise manual por categoria

Percorra o código aplicando as listas de verificação. Não tente decorar tudo
deste arquivo — abra o arquivo de referência da categoria quando for analisá-la:

- **Segurança** → `references/security.md`
  (SQL injection, mass assignment, secrets, autenticação/autorização, CSRF,
  deserialização, SSRF, exposição de dados).
- **Gambiarras e antipadrões** → `references/code-smells.md`
  (rescue silencioso, monkey patch, lógica em migrations, fat models/controllers,
  callbacks abusivos, `rescue nil`, código morto, condicionais aninhadas).
- **Padrões e convenções de equipe** → `references/conventions.md`
  (estilo Rails idiomático, nomeação, organização de camadas, i18n, testes,
  consistência com o que o time já usa).
- **Banco Oracle / MariaDB** → `references/database-oracle-mariadb.md`
  (N+1, índices ausentes, tipos incompatíveis, limites de identificadores Oracle,
  migrations perigosas, locking, charset/collation MariaDB).

### 4. Priorizar e classificar

Atribua a cada achado uma severidade:

- **CRÍTICO** — explorável agora; risco direto de vazamento, RCE, perda de
  dados ou indisponibilidade. (Ex.: SQL injection, secret commitado,
  `update_attributes` com params abertos.)
- **ALTO** — falha séria de segurança ou correção provável de bug, mas com
  pré-condição ou impacto limitado.
- **MÉDIO** — gambiarra/antipadrão que cria dívida técnica ou risco futuro;
  problema de performance de banco com dados de produção.
- **BAIXO** — desvio de padrão/estilo, melhoria de legibilidade.

Ordene segurança acima de tudo. Não afogue o relatório em achados BAIXO — se
houver muitos, agrupe-os.

### 5. Gerar o relatório

Use SEMPRE este template:

```markdown
# Auditoria Rails — <nome do projeto>

**Escopo:** <projeto inteiro | diff <base>..<head>>
**Stack:** Rails <versão> · Ruby <versão> · <Oracle | MariaDB/MySQL>
**Data:** <data>

## Resumo executivo

| Severidade | Qtde |
|------------|------|
| CRÍTICO    | N    |
| ALTO       | N    |
| MÉDIO      | N    |
| BAIXO      | N    |

<2-4 frases: os riscos mais urgentes e o que atacar primeiro.>

## Achados

### [CRÍTICO] <título curto do problema>
- **Local:** `app/.../arquivo.rb:42`
- **Categoria:** Segurança / Gambiarra / Padrão / Banco
- **Problema:** <o que está errado e por que é um risco real>
- **Evidência:**
  ```ruby
  <trecho mínimo do código problemático>
  ```
- **Correção sugerida:**
  ```ruby
  <como deveria ser>
  ```

<repita por achado, do mais grave ao menos grave>

## Recomendações estruturais

<melhorias de processo: configurar Brakeman no CI, adicionar RuboCop,
adotar service objects, política de migrations, etc.>

## Sinais de ferramentas a verificar

<alertas ainda não confirmados, indisponibilidades das ferramentas e limitações
de análise; não os conte como achados.>
```

Regras para o relatório:

- Sempre inclua `arquivo:linha`. Sem localização, o achado é inútil para o time.
- A correção sugerida deve ser **acionável** — mostre código, não conselho vago.
- Não invente problemas para encher o relatório. "Nenhum problema crítico
  encontrado" é uma resposta válida e valiosa.
- Não reescreva o projeto inteiro; aponte e exemplifique.
- Se algo for incerto (ex.: pode ser intencional), marque como "verificar com o
  autor" em vez de afirmar como erro.

## Saída como arquivo

Para revisões pequenas/rápidas, responder inline é suficiente. Se o usuário
pedir um arquivo compartilhável, grave-o no caminho ou diretório de saída que
ele indicar; se não houver indicação, proponha um caminho relativo ao projeto
antes de escrever. Não presuma um diretório específico do ambiente.
