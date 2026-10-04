---
name: board-workflow
description: "Configura e opera o fluxo de trabalho no board do time em Jira ou Trello: na primeira execução entrevista a pessoa para mapear projeto/quadro, colunas, tipos de item, campos (ou custom fields do Trello) e em que momento cada um é preenchido, e grava o mapa em .claude/board-workflow.md; depois usa esse mapa para criar, refinar, mover, comentar e consultar cards. Para quem ainda não tem fluxo definido, sugere um quadro padrão (Aguardando → Em Desenvolvimento → Code Review → Qualidade → Validação → Pronto). Invocar quando pedirem para configurar o Jira ou o Trello, criar/mover/atualizar/comentar card, ver o que está em cada coluna do board, ou quando não souberem qual fluxo adotar."
---

# Fluxo de trabalho no board

Esta skill não presume o board de ninguém. Ela **aprende o fluxo do time uma vez**, grava e
depois opera em cima disso — em **Jira** ou **Trello**.

O que muda entre os dois é só a camada de ferramenta; o miolo (colunas com critério de entrada
e saída, campos e o momento de preencher cada um) é o mesmo.

| Modo | Quando | O que faz |
|---|---|---|
| **Setup** | não existe `.claude/board-workflow.md` (ou pediram para reconfigurar) | entrevista + descoberta pela API, grava o mapa |
| **Operação** | o arquivo existe | criar, refinar, mover, comentar e consultar cards seguindo o mapa |

**Primeira coisa, sempre:** leia `.claude/board-workflow.md`. Se existir, não repita a
entrevista — opere. Se faltar só um dado, pergunte apenas aquele e acrescente ao arquivo.

## Pré-requisitos

**Descubra qual ferramenta o time usa antes de qualquer coisa** — pergunte, ou deduza pelas
ferramentas disponíveis:

| Ferramenta | Como operar | Verificar |
|---|---|---|
| **Jira** | MCP do Atlassian (ferramentas `jira_*`) | as tools `jira_*` existem? |
| **Trello** | MCP do Trello, se houver; senão API REST com chave+token do usuário | há MCP de Trello? senão, a pessoa tem chave/token? |

- Confirme que as ferramentas existem **antes** de prometer qualquer coisa; se não existirem,
  diga exatamente o que falta conectar e pare.
- **Nunca** peça, imprima ou passe token/senha em prompt, log ou `curl` visível. No Trello, se
  for preciso usar a API, oriente a pessoa a guardar `TRELLO_KEY`/`TRELLO_TOKEN` em variável de
  ambiente ou `.env` fora do git, e leia de lá — sem ecoar o valor.

---

# Modo Setup — a entrevista

## Regra: descubra antes de perguntar

Cada pergunta que a API já responde é uma pergunta a menos. Antes de abrir a boca:

| Descobrir | Jira | Trello |
|---|---|---|
| Onde o time trabalha | `jira_get_all_projects` | quadros do usuário (`/members/me/boards`) |
| O board | `jira_get_agile_boards` | o próprio quadro |
| As colunas | status do workflow (`jira_get_transitions`) | listas do quadro (`/boards/{id}/lists`) |
| Tipos de item | `jira_get_project_issue_types` | Trello não tem tipo nativo — o time usa **labels** |
| Campos e ids | `jira_search_fields`, `jira_get_create_fields` | Custom Fields do quadro (`/boards/{id}/customFields`), se o Power-Up estiver ativo |
| Quem participa | — | membros do quadro (`/boards/{id}/members`) |
| Ciclos | `jira_get_sprints_from_board` | Trello não tem sprint — se o time usa, é por label ou quadro separado |

Traga listas prontas para a pessoa escolher ("achei 3 projetos: A, B, C — qual?"), em vez de
pedir para ela digitar nomes.

## Blocos de pergunta (poucos por vez, com sugestão)

**1. Onde** — projeto e board. Se houver mais de um board no projeto, qual é o do time.

**2. O fluxo (colunas)** — liste as colunas reais encontradas (status no Jira, **listas** no
Trello) e pergunte o que cada etapa
significa para o time: onde o card nasce, onde entra em desenvolvimento, onde vai depois do
PR aberto, onde o QA atua, onde encerra. Se a pessoa **não tiver fluxo definido**, ofereça o
quadro padrão da seção abaixo.

**3. Tipos de item** — no Jira, quais issue types o time usa (Tarefa, Bug, História, Épico) e
quando usar cada um; se há épico pai obrigatório. **No Trello não existe tipo nativo:** pergunte
se o time separa por **label** (`bug`, `feature`, `débito`) e registre a convenção.

**4. Campos — e o momento de cada um.** Esta é a parte que mais evita retrabalho. Liste os
campos existentes (Jira: `jira_get_create_fields`; Trello: custom fields do quadro) e, para cada
um que o time usa, registre **id, obrigatoriedade e em que momento é preenchido**. **No Trello,
quadro sem o Power-Up de Custom Fields:** use seções fixas na descrição do card (`## Critério de
aceitação`, `## Plano de teste`, `## Solução técnica`) e registre isso como o "campo" — o que
importa é o momento de preencher, não onde mora.

| Campo | Id | Obrigatório? | Momento |
|---|---|---|---|
| Critério de aceitação | `customfield_…` | sim | no refinamento |
| Plano de teste | `customfield_…` | sim | antes de ir para desenvolvimento |
| Solução técnica | `customfield_…` | não | no refinamento |
| Tamanho / estimativa | `customfield_…` | sim | no refinamento |
| Data de entrega | `customfield_…` | sim | **antes** de mover para desenvolvimento |
| Link do PR | `customfield_…` ou comentário | sim | ao abrir o PR |

Pergunte explicitamente: **"algum campo é exigido para mudar de coluna?"** — no Jira é a causa
mais comum de erro (transição recusa campo fora da tela); no Trello não há bloqueio técnico, o
que torna o acordo do time a única garantia.

**5. Convenções de escrita** — idioma do card (o corpo costuma ser no idioma do produto,
enquanto commit/PR ficam em inglês), template de descrição, labels obrigatórias, quem é
reporter/assignee por padrão, e se cards feitos com apoio de agente levam alguma label de
origem.

**6. Autonomia** — o que o agente pode fazer sozinho e o que exige confirmação. Padrão seguro
e recomendado: **criar/mover/atualizar um card = pode; criar em lote, comentar e concluir card
= só com confirmação explícita.**

## Gravar o mapa

Escreva em `.claude/board-workflow.md` (versione junto com o projeto — o time todo passa a usar
o mesmo mapa). Formato:

```markdown
# Fluxo de trabalho no board — <time/projeto>

## Onde
- Ferramenta: Jira | Trello
- Jira: projeto <CHAVE> · board <nome> (id <n>) · <sua-instancia>.atlassian.net
- Trello: quadro <nome> (id <n>) · organização <nome>

## Fluxo (colunas reais, em ordem)
Aguardando → Em Desenvolvimento → Code Review → Qualidade → Validação → Pronto

| Etapa | Status (Jira) / Lista (Trello) | Entra quando | Sai quando | Quem age |
|---|---|---|---|---|

## Tipos de item (issue type no Jira · label no Trello)
| Tipo | Id / label | Usar para |

## Campos
| Campo | Id (ou seção da descrição) | Obrigatório | Momento de preencher | Exigido para mudar de coluna? |

## Convenções
- Idioma do card: … · Template de descrição: … · Labels: … · Estimativa: …

## Autonomia do agente
- Pode sem perguntar: …
- Exige confirmação: …
```

Ao final, mostre um resumo do que entendeu e confirme antes de gravar. Mudou o fluxo depois?
Atualize o arquivo — ele é a fonte da verdade, não a memória da conversa.

---

# Quadro padrão sugerido (para quem não tem fluxo)

Seis colunas, do que está esperando ao que está pronto. Cada uma com critério claro de
entrada e saída — coluna sem critério vira depósito de card parado.

| # | Coluna | Significa | Sai quando |
|---|---|---|---|
| 1 | **Aguardando** | Demanda registrada e priorizada, esperando alguém pegar; é aqui que ela é refinada (critério de aceitação, solução técnica, estimativa) | Está claro o suficiente para começar sem perguntar **e** alguém assume |
| 2 | **Em Desenvolvimento** | Alguém está codando (assignee definido) | Código pronto, testado localmente, PR aberto |
| 3 | **Code Review** | PR aberto aguardando revisão | PR aprovado e mergeado |
| 4 | **Qualidade** | QA validando em ambiente de teste | Cenários do plano de teste passaram |
| 5 | **Validação** | Quem pediu confere o resultado (produto/negócio) | Aprovado por quem pediu |
| 6 | **Pronto** | Entregue e validado | — |

Como montar no Jira: crie um board **Kanban** e mapeie uma coluna por status; se não puder
criar status novos, use os que existem e registre no mapa qual status representa cada etapa.

Recomendações que fazem o quadro funcionar:

- **Aguardando é a porta de entrada** — nada entra em Em Desenvolvimento sem estar refinado.
  Card que "entra em dev para descobrir o que fazer" volta como retrabalho.
- **Limite de WIP** em Em Desenvolvimento e Code Review (ex.: 2 por pessoa). Sem limite, tudo
  fica "em andamento" e nada termina.
- Times menores podem juntar **Qualidade + Validação**; nunca junte **Em Desenvolvimento com
  Code Review** — é onde o gargalo aparece, e juntar as duas esconde o problema.

---

# Modo Operação

## Criar card

1. Confirme o épico pai, se o mapa exigir.
2. Preencha **todos** os campos cujo momento é "na criação".
3. Título **autoexplicativo na daily**: verbo de ação + resultado concreto, em linguagem de
   produto ("Bloquear acesso após 5 tentativas erradas"), sem jargão de implementação e sem
   códigos internos.
4. Descrição com **Contexto** (o que e por quê, 2–5 frases, legível por quem não é técnico) e
   **Objetivo** (resultado esperado).
5. Critério de aceitação em **linguagem de produto** — resultados observáveis, sem termos
   técnicos. Solução técnica, sim, pode ser bem técnica. Plano de teste **inclui cenários de
   erro**, não só o caminho feliz.
6. **Criar em lote exige preview + OK:** mostre a lista (títulos, tamanho, tipo) e espere o sim.
7. Antes de criar, cheque se já existe card equivalente — duplicata custa mais que a busca.

## Mover card pelo fluxo

**O status do card sempre reflete a etapa real do trabalho.** Card atrás da realidade é erro.

**Jira:**

```
1. jira_get_transitions no card            → ver o que está disponível AGORA
2. jira_update_issue                        → preencher os campos daquele momento
3. jira_transition_issue                    → mover, uma transição por vez
```

- **Nunca chumbe id de transição** — muda por workflow e por status de origem.
- **Preencha os campos antes de transicionar.** Muitos workflows recusam campo setado dentro da
  transição (*"cannot be set / not on the appropriate screen"*). Atualiza, depois move.
- Transição indisponível = avise e pare. Não invente caminho alternativo pelo fluxo.

**Trello:** mover é trocar a lista do card (`idList`) — não existe workflow que impeça pular
etapa, então **a checagem é sua**: antes de mover, confirme que os campos do momento estão
preenchidos e que a coluna de destino é a próxima do mapa. Se alguém pedir para pular etapa
(de Aguardando direto para Code Review, por exemplo), diga o que está sendo pulado e pergunte.
Use o id da lista do mapa, nunca o nome — nome muda e quebra silenciosamente.

## Registrar o PR

No campo que o mapa indicar (ou em comentário, se não houver campo):

```
tipo(ABC-123) - Título
PR #N → https://github.com/<org>/<repo>/pull/N
```

**Leia antes de escrever** (`jira_get_issue`): acrescente ao conteúdo existente, nunca
sobrescreva. Hotfix registra os dois PRs (produção e integração).

## Comentar

Redija, **mostre o rascunho e só poste depois do OK**. Menção real usa o formato de accountId
da instância — descubra o id via `jira_get_user_profile`; texto solto com `@Nome` não notifica
ninguém.

## Consultar o board

**Jira** — JQL a partir do mapa (troque `<PROJ>` e o nome do status):

| Pergunta | JQL |
|---|---|
| O que está para revisar | `project = <PROJ> AND status = "Code Review" ORDER BY priority DESC` |
| O que está em desenvolvimento | `project = <PROJ> AND status = "Desenvolvimento"` |
| O que é meu | `project = <PROJ> AND assignee = currentUser() AND status != "Pronto"` |
| Urgente parado | `project = <PROJ> AND priority = Highest AND status NOT IN ("Pronto")` |
| Sem movimento há 5 dias | `project = <PROJ> AND status != "Pronto" AND updated <= -5d` |

**Trello** — não há JQL: leia os cards do quadro (`/boards/{id}/cards`) e filtre em memória por
`idList` (a coluna), `idMembers` (quem), `labels` (tipo/prioridade) e `dateLastActivity` (paradas).

Responda agrupado por coluna, da mais urgente para a menos, omitindo colunas vazias.

## Estimativa (se o time usa tamanho)

Rubrica em **esforço humano**, não em tokens ou volume mecânico:

| Tamanho | Dias úteis |
|---|---|
| PP | 1 a 3 |
| P | 3 a 5 |
| M | 5 a 8 |
| G | 8 a 12 |
| acima de G | **quebrar em cards menores** |

Mover 200 arquivos é PP se for mecânico. O que conta é dificuldade, risco e tempo para uma pessoa.

## Integração com o fluxo de entrega (`git-flow-delivery`)

Se as duas skills estiverem instaladas, a divisão é esta — e o `.claude/board-workflow.md` é a
fonte da verdade para as duas, valendo igual para Jira e Trello:

| Quem | Cuida de |
|---|---|
| `board-workflow` (esta) | quadro, colunas, campos, movimentação, criação e consulta de cards |
| `git-flow-delivery` | branch, commit, PR, code review, release e hotfix |

Pontos de contato, na ordem em que acontecem:

| Momento no código | O que acontece no card |
|---|---|
| Branch criada, começou a codar | move para o status de **desenvolvimento** (campos daquele momento preenchidos antes) |
| PR aberto | registra o link do PR no campo mapeado **e** move para **code review** |
| PR aprovado e mergeado | move conforme o mapa (em geral **qualidade**) |
| Release publicada | PR de release não tem card — nenhuma etapa de tracker se aplica |

Sem a `git-flow-delivery` instalada, esses movimentos continuam valendo: quem avisa é a pessoa
("abri o PR"), e você move o card do mesmo jeito.

## Regras de ouro

- **Sem card, não começa o código.** Se perceber que está codando sem card: pare, crie e mova
  até o status correto.
- **Ler antes de escrever** em qualquer campo de texto acumulativo.
- **Uma mudança de coluna por vez** — no Jira, sempre depois de consultar as transições disponíveis; no Trello, sempre conferindo a ordem do mapa.
- **Confirmação humana** para: criação em lote, comentário, conclusão de card e qualquer
  exclusão. Autorização dada antes do fato não vale para o fato.
- Em dúvida se o ajuste estoura o escopo do card, **pergunte** em vez de decidir.

## Checklist rápido

- [ ] `.claude/board-workflow.md` lido (ou criado, se era a primeira vez), ferramenta identificada
- [ ] Campos do momento atual preenchidos **antes** da transição
- [ ] Jira: transição via `jira_get_transitions`, nunca chumbada · Trello: lista de destino pelo id, ordem conferida
- [ ] Critério de aceitação em linguagem de produto; plano de teste com cenários de erro
- [ ] Link do PR registrado sem sobrescrever o conteúdo anterior
- [ ] Status do card = etapa real do trabalho
- [ ] Comentário/lote/conclusão só após OK explícito

## Adaptando ao seu time

| O que | Onde ajustar |
|---|---|
| Ferramenta (Jira/Trello), projeto, quadro | `## Onde` no mapa |
| Nomes das colunas | `## Fluxo` — a skill não presume nome nenhum |
| Campos e o momento de cada um | `## Campos` |
| Idioma, template, labels | `## Convenções` |
| O que o agente faz sozinho | `## Autonomia do agente` |

Trocou de ferramenta (Linear, Azure Boards, GitHub Projects)? O fluxo, os critérios de coluna e
os momentos de campo continuam valendo — muda só a camada de API. Registre a nova ferramenta em
`## Onde` e siga o mesmo mapa.
