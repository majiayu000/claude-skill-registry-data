---
name: git-flow-delivery
description: "Git Flow do card ao deploy em projetos com develop/main: branch e commit com número do card e descrição em inglês, regra 1 branch = 1 commit, PR para develop só depois da validação humana, acompanhamento do code review com checklist do que revisar, release develop → main sem squash com tag semver/rc, hotfix a partir da main com PR dupla, e integração opcional com o board (Jira ou Trello). Invocar sempre que for criar branch, commitar, abrir PR, gerar release ou hotfix."
---

# Git Flow Delivery — do card ao deploy

Fluxo baseado no Git Flow, padrão de mercado, para levar um card do quadro até produção com
rastreabilidade total: **todo commit, branch e PR carrega o número do card**, e o
histórico do repositório conta a mesma história que o quadro de tarefas.

Ferramenta-agnóstico: funciona com Jira, Linear, GitHub Issues, Azure Boards etc.
Onde aparecer `ABC-123`, leia "o identificador do card no seu tracker".

> **Se existir `.claude/board-workflow.md`** (criado pela skill `board-workflow`), ele é a
> **fonte da verdade** para nomes de status, ids de campo e o momento de preencher cada um:
> leia esse arquivo e use o que está lá em vez de perguntar de novo ou supor nomes. As duas
> skills se dividem assim — `board-workflow` cuida do board e dos campos; esta cuida de
> branch, commit, PR, release e hotfix; e o card acompanha o trabalho nos dois pontos de
> contato abaixo.

## Mapa de ambientes

| Branch | Ambiente | Quem mergeia |
|---|---|---|
| `develop` | Desenvolvimento / homologação (HML) | O time, após code review |
| `main` | Produção | O time, via PR de **release** ou **hotfix** |

Toda branch de trabalho nasce de `develop`. Só hotfix nasce de `main`.

## 1. Branch

```
tipo/ABC-123-short-description-in-english
```

- `tipo` ∈ `feat` · `fix` · `chore` · `refactor` · `docs` · `test`
- Criada a partir de `develop` atualizada: `git checkout develop && git pull && git checkout -b feat/ABC-123-...`
- Nome **em inglês**, kebab-case, curto. O card já tem o título completo em português.

**Ao criar a branch, mova o card para o status de desenvolvimento** — o status do card sempre
reflete a etapa real do trabalho. Preencha antes os campos daquele momento (ex.: assignee,
estimativa, data de entrega) e só então transicione; ver a seção de integração com Jira.
Card parado atrás da realidade é erro, não detalhe.

## 2. Commit

```
tipo(ABC-123) - Description in English
```

Exemplo: `fix(ABC-123) - Browser tab title shows wrong page name`

Regras que não se negociam:

- **Inglês.** Português fica no card; a mensagem de commit é para o histórico do repositório.
- **Número do card entre parênteses**, sem `:` depois. Nunca `tipo(escopo):`.
- **1 branch = 1 commit — sempre.** Qualquer ajuste depois do primeiro commit (correção
  de review, typo, lint) entra via amend, nunca como commit novo:

  ```bash
  git add -A
  git commit --amend --no-edit
  git push --force-with-lease
  ```

  Antes de qualquer push, confira que há exatamente 1 commit:
  `git log --oneline develop..HEAD`

## 3. Definição de pronto → abrir o PR

> ⚠️ **O PR só é aberto DEPOIS de um humano validar.** Não abra PR nem mova o card
> para "Revisão de Código" antes do OK explícito.

1. Terminar o trabalho do card com testes verdes; commit no padrão; `git push -u origin <branch>`.
2. Sinalizar que está pronto para validação e **esperar o OK**. Se vierem ajustes, iterar
   (via amend) — sem abrir PR nesse vai-e-volta.
3. Com o OK, abrir o PR para `develop`:

   ```bash
   gh pr create --base develop \
     --title "tipo(ABC-123) - Description in English" \
     --body "$(cat <<'EOF'
   Card: <link do card>

   - O que foi feito, em bullets técnicos
   - Decisões relevantes e por quê
   - Como testar
   EOF
   )"
   ```

   - **Título do PR = mensagem do commit.**
   - **Body em português**, com o link do card e bullets técnicos.
   - Labels quando existirem no repo: `Bug fixes` · `Improvements` · `Breaking Changes`.

## 4. Pós-PR — nesta ordem

1. **Registrar o link do PR no card** (campo/comentário de "PRs" do seu tracker), no formato:

   ```
   tipo(ABC-123) - Título
   PR #N → https://github.com/<org>/<repo>/pull/N
   ```

2. **Mover o card para "Revisão de Código"** (ou o status equivalente do seu quadro).

3. **Acompanhar o code review** (bot e/ou humanos) — o que olhar está na seção
   *Code review: o que olhar*, adiante. Se o repo tem review automático,
   aguardar **no máximo 1 minuto** — nunca em loop além disso. Para cada thread aberto:

   | Comentário | Ação |
   |---|---|
   | Procedente | Corrigir → incorporar ao commit único (amend + `--force-with-lease`) → **responder no thread** dizendo o que foi feito → *Resolve conversation* |
   | Não procedente | **Responder no thread** com a justificativa técnica → *Resolve conversation* |

   - **Sempre responder antes de resolver.** Nunca feche um thread mudo.
   - Com revisor humano, o reply é diálogo: pode-se discordar com respeito e alinhar antes
     de mexer no código. Em dúvida se o ajuste estoura o escopo do card, pergunte.
   - Se corrigiu e o bot re-revisou, repetir **no máximo mais 1 vez**. Persistindo, parar e
     reportar — não entrar em ciclo infinito de correção.

   ```bash
   # threads abertos
   gh api graphql -f owner=<org> -f repo=<repo> -F pr=<N> -f query='
     query($owner:String!,$repo:String!,$pr:Int!){ repository(owner:$owner,name:$repo){
       pullRequest(number:$pr){ reviewThreads(first:50){ nodes{
         id isResolved comments(first:10){ nodes{ databaseId path body } } } } } } }'
   # responder num comentário
   gh api repos/<org>/<repo>/pulls/<N>/comments -f body='...' -F in_reply_to=<databaseId>
   # resolver o thread (id do THREAD, não do comentário)
   gh api graphql -f id=<threadId> -f query='
     mutation($id:ID!){ resolveReviewThread(input:{threadId:$id}){ thread{ isResolved } } }'
   ```

4. **Notificar o time** no canal (Slack, Discord, Teams…) — **sempre com confirmação
   explícita, pedida depois das etapas 1–3**. Autorização antecipada ("já pode avisar")
   dada antes do PR existir **não vale**: complete as etapas, pergunte, e só envie com o
   "sim" na resposta seguinte. Formato:

   ```
   @<papel-do-time>
   PR: <url do PR>
   Card: <url do card>
   ```

## Code review: o que olhar

Vale para revisar o PR de outra pessoa **e** para conferir o seu antes de pedir revisão.

### 1. Formato do título e dos commits

- Padrão `tipo(ABC-123) - Description in English`, igual no commit e no título do PR.
- **Identificador do card presente.** O formato é o do tracker do time: `ABC-123` (Jira,
  Linear), `#1234` (GitHub Issues) ou o que estiver no mapa do board. Sem id, o histórico
  perde a rastreabilidade — é apontamento bloqueante.
- Tipo válido: `feat` · `fix` · `chore` · `refactor` · `docs` · `test`.
- Um commit por branch (`git log --oneline develop..HEAD`).

### 2. Estrutura do PR

- A descrição explica **o que** foi feito e **por quê**, com link do card.
- Labels aplicadas, quando o repo usa (ex.: `Bug fixes`, `Improvements`, `Breaking Changes`).
- **É hotfix?** Então existem **dois** PRs: um para `main` e um para `develop`.
- **É release?** Então **sem squash/rebase** no merge — o histórico da `develop` se preserva.
- O card está na coluna que corresponde à etapa real (code review).

### 3. Qualidade do código

| Frente | O que perguntar ao diff |
|---|---|
| **Corretude** | A lógica faz o que o card pede? Há edge case não tratado (lista vazia, nulo, limite, concorrência)? |
| **Idempotência** | Operações críticas (cobrança, envio, escrita externa) podem rodar duas vezes sem duplicar efeito? Retry é seguro? |
| **Segurança** | SQL/command injection; segredo ou token no código; dado pessoal em log ou resposta sem mascaramento; permissão verificada onde importa. |
| **Tratamento de erros** | Falha é capturada, logada e propagada com um **id de correlação** que permita rastrear a operação ponta a ponta? Nada de `catch` silencioso. |
| **Clareza** | Nomes de variáveis, funções e classes dizem o que são? Precisa de comentário para entender o óbvio? |
| **Duplicação** | Código repetido que já existe no projeto e poderia ser reaproveitado? |
| **Testes** | Existe teste para o que mudou, cobrindo o caso crítico **e** o de erro — não só o caminho feliz? |
| **Escopo** | O diff faz só o que o card pede? Mudança carona atrapalha a revisão e o rollback. |

### 4. Severidade — sempre classifique o comentário

| Nível | Quando | Efeito |
|---|---|---|
| 🔴 **Bloqueante** | Erro que compromete a entrega, dados ou segurança | pedir alteração; não aprovar |
| 🟡 **Sugestão** | Melhoria relevante, não impeditiva | quem escreveu decide |
| 🔵 **Nitpick** | Estilo, nomenclatura, preferência | não bloqueia; agrupe num comentário só |

Sem severidade, todo comentário parece bloqueante e a revisão trava. Ao aprovar com apenas
sugestões e nitpicks, deixe explícito que estão liberados para seguir.

## 5. Release — develop → main

A branch `release` é **descartável**: existe só para levar o estado da `develop` até um
PR contra `main`.

```bash
git checkout develop && git pull
git checkout -B release                     # -B recria se já existir
git push -u origin release
gh pr create --base main --head release --title "Release" --body "Release"
git checkout develop && git branch -D release   # a remota o GitHub apaga no merge
```

Regras:

- **Título e body: `Release`**, sem número de versão. A versão vive na **tag/release do
  GitHub** (`vX.Y.Z`), não no título do PR.
- **NUNCA squash/rebase no merge** — release preserva o histórico da `develop` (merge commit).
- PR de release **não tem card**: as etapas de tracker da seção 4 não se aplicam. Só a
  notificação, com o mesmo pedido de confirmação:

  ```
  @<papel-do-time>
  Release 📢
  <url do PR>
  ```

- Após o merge, publicar a release final `vX.Y.Z` (sem `-rc`, apontando para `main`).
  Se o deploy de produção dispara pelo evento de release, **conferir que todos os
  workflows rodaram** (`gh run list --workflow <arquivo>`). Se um não disparou, deletar e
  recriar a release na mesma tag re-dispara o evento.

### Versionamento (semver + release candidates)

| Situação | Ação | Exemplo |
|---|---|---|
| Nova feature em `develop` | Incrementa **minor**, abre `rc.1` | `1.1.0 → 1.2.0-rc.1` |
| Nova RC em `develop` | Incrementa o número da RC | `1.2.0-rc.1 → 1.2.0-rc.2` |
| Release para `main` | Remove o sufixo `-rc` da última RC | `1.2.0-rc.3 → 1.2.0` |
| Hotfix em `main` | Incrementa **patch** | `1.2.0 → 1.2.1-rc.1` |
| Feature após RC parcial lançada | Nova minor com `rc.1` | `1.2.0-rc.5 → 1.3.0-rc.1` |

Durante um hotfix podem coexistir `main: 1.2.1-rc.1` e `develop: 1.3.0-rc.1`.
Conferir a última tag: `git tag --sort=-creatordate | head -5`.

## 6. Hotfix — direto em produção

Hotfix é a **única** branch que nasce de `main`.

```bash
git checkout main && git pull
git checkout -b fix/ABC-123-short-description
# ... corrigir, commit no padrão (1 commit), push ...
gh pr create --base main    --title "fix(ABC-123) - Description" --body "..."
gh pr create --base develop --title "fix(ABC-123) - Description" --body "..."
```

- **Duas PRs, sempre**: uma para `main` (vai para produção) e outra para `develop`
  (para a correção não se perder na próxima release). Registrar **os dois links** no card.
- Versão: patch com `rc` (`1.2.0 → 1.2.1-rc.1`), release final após o merge em `main`.


## Integração com o board (Jira ou Trello, opcional)

Se o projeto tem o board acessível (MCP do Atlassian para Jira, MCP ou API do Trello), as etapas
de card das seções 1 e 4 podem ser feitas pelo agente. Sem acesso, faça-as manualmente — nunca
com credenciais no prompt.

| Etapa | Jira | Trello |
|---|---|---|
| Ler o card antes de criar a branch | `jira_get_issue` | buscar o card no quadro pelo id/nome |
| **Mover para desenvolvimento** ao criar a branch | preencher campos + `jira_transition_issue` | trocar `idList` para a lista de desenvolvimento |
| Registrar o link do PR | `jira_update_issue` no campo de PRs **ou** `jira_add_comment` | custom field de PR, comentário, ou anexar o link no card |
| **Mover para code review** ao abrir o PR | `jira_get_transitions` → `jira_transition_issue` | trocar `idList` para a lista de code review |

Regras que valem nos dois:

- **Ler antes de escrever.** Busque o card antes de atualizar, para **acrescentar** ao campo de
  PRs em vez de sobrescrever o que já está lá.
- **Campos do momento antes de mover.** No Jira é técnico: muitos workflows recusam campo setado
  dentro da transição (*"not on the appropriate screen"*) — atualize, depois transicione. No
  Trello nada impede a movimentação, então a checagem é sua: confira os campos antes de trocar a
  lista.
- **Nunca chumbe identificador.** No Jira, descubra a transição com `jira_get_transitions`; no
  Trello, use o **id** da lista (nome muda e quebra silenciosamente).
- **Marcar a origem.** Se o time usa uma label para o que o agente toca, some-a às existentes.
- Hotfix registra **os dois** links de PR (`main` e `develop`) no mesmo card.

## Checklist rápido

- [ ] Branch `tipo/ABC-123-english-name`, criada de `develop` (de `main` só se hotfix)
- [ ] Commit `tipo(ABC-123) - Description in English` — e **só um** commit
- [ ] Card movido para desenvolvimento ao criar a branch
- [ ] Humano validou **antes** do PR
- [ ] PR para `develop`, título = commit, body em português com link do card
- [ ] Link do PR registrado no card; card em "Revisão de Código"
- [ ] Threads de review: respondidos **e** resolvidos; correções via amend
- [ ] Revisão passou pelas 4 frentes (formato, estrutura, qualidade, severidade)
- [ ] Notificação ao time só depois de perguntar e receber "sim"
- [ ] Release: título `Release`, sem squash, tag `vX.Y.Z`
- [ ] Hotfix: PR para `main` **e** para `develop`, versão patch

## Adaptando ao seu time

Troque estes pontos e o resto do fluxo se mantém:

| O que | Aqui | No seu time |
|---|---|---|
| Prefixo do card | `ABC-123` | ex.: `PROJ-42`, `#1234` |
| Branch de integração / produção | `develop` / `main` | ex.: `dev` / `master` |
| Status pós-PR | "Revisão de Código" | o nome da coluna no seu quadro |
| Canal do time | Slack / Discord / Teams | webhook ou menção que o time usa |
| Onde registrar o PR | campo "PRs" ou comentário | Jira: `customfield_*` · Trello: custom field, comentário ou anexo |
| Mapa do board e dos campos | perguntar ao time | `.claude/board-workflow.md` (skill `board-workflow`) |
| Label de origem | — | ex.: `ai`, `claude`, se o time quiser rastrear |
| Tipos de commit | feat, fix, chore, refactor, docs, test | acrescente `perf`, `ci`… se usar |
