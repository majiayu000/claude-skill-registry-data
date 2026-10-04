---
name: sprint-planning
description: |
  Gera a planning da sprint como artifact — o artefato do rito de Planejamento do Time PAM (workspace Vertical Tech).
  Lê a sprint ativa no ClickUp, monta uma visão executiva com objetivo da sprint, números, gráficos enxutos de frente de valor e de casa, e o objetivo de cada desenvolvedor; e uma visão por desenvolvedor com a fila em ordem de prioridade.
  Feita para stakeholders não técnicos: o que importa é entender a entrega de valor sem abrir o ClickUp.
  Executada pelo agente agente-ritos. Rode no rito de Planejamento, ou sempre que o PM quiser revisar a composição da sprint.
  Comandos: /sprint-planning run [squad], /sprint-planning dry-run, /sprint-planning help
invocation: user
inputs: sprint ativa no ClickUp e o roster de papéis do time
outputs: planning da sprint publicada como artifact navegável
side_effects: propose
context: references/regras-de-leitura.md, references/artifact-planning.md, knowledge/domains/pessoas.md, knowledge/tom-de-voz.md
completion: artifact publicado, com objetivo da sprint e campos deduzidos validados pelo PM
---

**Autor:** Ithalo Mendes <ithalo.mendes@verticalloto.com>
**Criada em:** 2026-09-21, a partir do modelo validado na Sprint 2 do Time PAM.

# Sprint Planning — o artefato do rito de Planejamento

Gera a planning da sprint em formato de artifact navegável. É o artefato que circula com a diretoria e com
quem não abre o ClickUp.

> **Quem executa:** o agente [agente-ritos](../../agents/agente-ritos.md).
> **Relação com as outras skills:** a `clickup-spec` cria e move itens; a `sprint-planning` mostra o que a
> sprint virou depois disso; a `clickup-revisa-sprint` conta o que aconteceu no fim do ciclo. As três leem a
> mesma config em `clickup-spec/references/clickup-config.md`.

## Princípio

**A planning precisa ser intuitiva.** Quem abre tem que entender a sprint em trinta segundos, sem legenda,
sem jargão e sem precisar perguntar o que uma coluna significa.

Isso tem uma consequência prática: **toda seção precisa justificar o espaço que ocupa.** Se uma informação
não ajuda alguém a entender, decidir ou acompanhar, ela sai. Esse critério vem de
`knowledge/tom-de-voz.md` e vale para o artifact inteiro.

## Público

Stakeholders não técnicos — diretoria e liderança. Escreva para quem quer saber **que valor a sprint
entrega**, não que tarefas existem.

Na prática:

- Nome de card em linguagem de usuário. Se o título no ClickUp tem jargão, reescreva para o artifact e
  guarde o original no tooltip. Nunca altere o card por conta própria.
- Sem nome de arquivo, endpoint, tabela, biblioteca ou ferramenta interna.
- Números com unidade clara e o que eles significam logo abaixo.

## Estrutura do artifact

Três abas. As duas primeiras são obrigatórias, a terceira é atípica.

### Aba 1 — Visão executiva (obrigatória)

A aba mais importante. Contém, nesta ordem:

1. **Objetivo da sprint** em uma frase, seguido de um parágrafo curto explicando a composição do ciclo.
   O objetivo é escrito pelo PM ou proposto pelo agente e validado por ele — nunca publicado como fato sem
   passar pelo PM.
2. **Números da sprint** — faixa com cinco indicadores no máximo: total de itens, em desenvolvimento,
   prontos ou em validação, ainda não iniciados, número de desenvolvedores. Cada um com uma linha dizendo
   o que é.
3. **Gráficos enxutos** — dois, lado a lado: distribuição por **frente de valor** e por **casa**.
   Substituem as abas separadas que existiam antes. São leitura de composição, não lista de itens.
4. **Objetivo de cada desenvolvedor** — uma frase por dev, com o total de itens. Só desenvolvedores.
5. **Pontos de atenção** — riscos de composição encontrados nos dados. Existe só quando há algo real a
   dizer; não é seção de preenchimento obrigatório.

### Aba 2 — Por desenvolvedor (obrigatória)

Uma lista por desenvolvedor, em **ordem alfabética**, e dentro de cada uma os itens em **ordem de
prioridade**, numerados. O primeiro é o próximo a ser trabalhado.

Cada item mostra: posição na fila, nome legível, estado, casa e frente de valor. Nada além disso, a menos
que haja uma marca relevante (item sem desenvolvedor alocado, item sem previsão de conclusão no ciclo).

### Aba 3 — Em discussão (opcional e atípica)

Só existe quando há um bloco de trabalho real sendo considerado para a sprint e ainda não comprometido.
**Não crie essa aba por padrão.**

Quando existir, ela precisa deixar explícito que nada ali está comprometido, quem seriam os responsáveis, e
o que acontece antes de virar compromisso.

**Regra do agente:** mesmo quando o PM não mencionar nada em discussão, pergunte uma vez se há algo que
deveria ser considerado — decisão pendente, dívida de incidente, pedido de stakeholder que ainda não virou
card. Se não houver, siga sem a aba.

## Regras de leitura do dado

Carregue `references/regras-de-leitura.md`. São regras aprendidas na prática, e cada uma existe porque a
falta dela já produziu um artefato errado. As mais críticas:

- Releia a sprint inteira antes de cada atualização — o PM edita o ClickUp em paralelo.
- Data de criação não é tempo de espera. Item antigo costuma ter passado o tempo em refinamento de produto
  e design, não parado.
- Só desenvolvedores entram na carga e no objetivo por pessoa.
- A ordem da fila vem da prioridade cadastrada no ClickUp, não de peso inventado.
- Campo deduzido aparece marcado visualmente e vai para a lista de confirmação com o PM.

## Construção do artifact

Carregue `references/artifact-planning.md` para o contrato visual: paleta, tipografia, componentes,
comportamento das abas e regras de acessibilidade em tema claro e escuro.

**Antes de escrever qualquer gráfico, carregue a skill `dataviz`.** Os dois gráficos da visão executiva são
o único lugar do artifact onde cor carrega significado, e eles precisam funcionar nos dois temas.

## Comandos

### `/sprint-planning run [squad]`

Fluxo completo:

1. Lê a sprint ativa do squad no ClickUp, incluindo subtarefas e itens fechados.
2. Classifica cada item: casa, frente de valor, estado, responsáveis, prioridade.
3. Separa desenvolvedores de design e qualidade usando `knowledge/domains/pessoas.md`.
4. Levanta os furos de composição (sem dono, sem prioridade, pessoa que saiu, item que não fecha no ciclo).
5. **Apresenta ao PM, antes de publicar:** o objetivo da sprint proposto, os objetivos por dev, os campos
   deduzidos e os furos encontrados. Pergunta se há algo em discussão a considerar.
6. Publica o artifact e devolve o link.

O passo 5 não é opcional. Publicar antes de validar o objetivo e as deduções produz um artefato que o PM
precisa corrigir em público.

### `/sprint-planning dry-run`

Faz tudo até o passo 5 e para. Mostra o que seria publicado, em texto, sem gerar o artifact. Útil para
conferir a composição antes da reunião.

### `/sprint-planning help`

Lista os comandos e a estrutura do artifact.

## O que esta skill não faz

- Não move item para a sprint nem altera card. Isso é `clickup-spec` com o `agente-delivery`.
- Não renomeia card no ClickUp. Reescreve títulos **apenas no artifact** e reporta a lista de sugestões ao
  PM.
- Não define prioridade. Lê a que existe e reporta a que falta.
- Não atribui responsável. Quando encontra item sem dono, reporta.
- Não gera relatório de fim de sprint. Isso é `clickup-revisa-sprint`.
