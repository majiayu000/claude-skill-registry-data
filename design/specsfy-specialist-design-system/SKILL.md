---
name: specsfy-specialist-design-system
description: Criar e manter o DESIGNSYSTEM.MD com regras macro de interface SaaS, padrões CRUD, estados e exceções por alcance. Use antes de projetar telas; não use para registrar componentes locais.
---

# Specsfy Specialist Design System

## Quando usar

Esta skill governa o documento `DESIGNSYSTEM.MD` do projeto consumidor. Ela
define linguagem visual, shell, composição de superfícies, estados e regras de
negócio expostas na interface. O documento orienta UX, UI, experiência de
interface e componentes React.

Use antes de criar ou revisar uma tela, um fluxo CRUD, uma navegação, um
formulário ou um componente global. Use também quando o documento não existir,
estiver desatualizado ou entrar em conflito com uma tela já projetada.

Não use esta skill para catalogar componentes, props ou arquivos locais. Esse
registro pertence a `INTERFACE.md`, que deve apontar para as escolhas macro sem
copiá-las.

## Fontes obrigatórias

Leia, nesta ordem:

1. `DESIGNSYSTEM.MD` na raiz do projeto consumidor, se existir.
2. `.specsfy/templates/DESIGNSYSTEM.MD` para criar a fonte ausente.
3. `INTERFACE.md` para conhecer componentes e telas já registradas.
4. `.specsfy/STACK.md`, manifests, rotas, telas, permissões e regras do
   domínio relacionadas à entrega.

Quando a fonte não existir, copie o template gerenciado para `DESIGNSYSTEM.MD`
e preencha apenas o contexto já confirmado. Não esconda lacunas com texto
genérico.

## Fluxo

1. Identifique o produto, o módulo, a superfície e o fluxo afetado.
2. Compare a solicitação com `DESIGNSYSTEM.MD` e preserve as regras já ativas.
3. Se a pessoa não informa direção visual, aplique os defaults do documento e
   registre isso como direção padrão da entrega.
4. Se a pessoa fornece uma direção diferente, registre a exceção, seu alcance
   e a regra que ela substitui. Uma exceção de tela não altera o produto todo.
5. Atualize o documento somente quando a regra tiver alcance macro. Registre
   componentes e telas específicas em `INTERFACE.md`.
6. Mapeie os cenários canônicos da superfície antes de entregar a orientação
   para UX, UI ou implementação.
7. Retorne os arquivos lidos, a regra aplicada, as exceções registradas e os
   cenários cobertos.

Em toda entrega visual, faça a revisão durante o desenvolvimento mesmo sem
pedido da pessoa. Confira bordas, espaçamentos, margens, padding e tipografia
do sistema nos viewports e estados relevantes. Registre o método, o resultado e
os ajustes no item `VISUAL` da tarefa.

## Padrões

### Defaults obrigatórios para SaaS

Quando não houver direção visual contrária, aplique estas composições:

- Lista de CRUD: `PageHeader` + resumo útil + `DataGrid`. Use busca, filtros,
  ordenação, paginação, seleção e ações por linha quando o volume ou o domínio
  pedir.
- Detalhe: `PageHeader` + `DetailLists`, com status, próxima ação e relações ou
  atividade quando forem úteis para o domínio.
- Criar e editar: `PageHeader` + seções de formulário em duas colunas
  responsivas, com coluna de contexto e painel de campos.
- Formulário: labels visíveis acima dos campos, ajuda contextual, valores
  preservados e estado de envio.
- Erro de campo: borda, fundo ou ícone semântico vermelho, mensagem visível
  abaixo do campo, associação semântica e foco no primeiro erro.
- Erros múltiplos: resumo no início com links para os campos afetados.
- Tela: `loading`, vazio, erro, sucesso, sem permissão, conteúdo parcial e não
  salvo quando o fluxo comportar esses estados.
- Breadcrumb: obrigatório em toda tela da aplicação, com o nome da equipe ativa
  visível antes do módulo e do título atual. Em Laravel, reaproveitar o
  `Breadcrumb` ou `Breadcrumbs` existente no layout e seus tipos de rota.
- DataGrid: linha inteira clicável para abrir o detalhe, com equivalente de
  teclado e controles internos protegidos por `TableRowAction` ou equivalente.
- CRUD: todas as telas reutilizam o mesmo `PageHeader` componentizado; a lista
  usa `DataGrid` em largura total, exibe a coluna `ID` e oferece botões de editar
  e apagar na linha. O link da linha leva ao detalhe sem capturar os botões.
- Componentes recorrentes de cabeçalho, tabela, linha, ações, formulário,
  estados e feedback entram em `INTERFACE.md` e são reaproveitados antes de uma
  nova implementação.

Esses defaults não significam aparência genérica. A personalidade vem da
hierarquia dos dados, linguagem do domínio, tipografia, tokens, ritmo, estados,
contraste e uso do shell. A composição deve informar e orientar a tarefa.

## Dashboards e blocos comuns

Quando a entrega incluir um dashboard, use `PageHeader`, período ou escopo,
filtros, uma faixa curta de `KPI` com valor, unidade, período, comparação e
fonte, seguida da tendência ou distribuição principal e de uma lista detalhada
ou `DataGrid` para investigação. Cada indicador e visualização deve declarar
loading, vazio, erro e atualização, além de alternativa textual ou tabular para
gráficos.

Use primitives do `shadcn/ui` para controles fundamentais e blocos gratuitos do
ReUI para composições de CRUD e dashboard quando eles atenderem à tarefa.
Adapte tokens, dados, permissões, acessibilidade e linguagem do produto. Registre
origem, estados e consumidores em `INTERFACE.md`.

## Formulários de criar e editar

Organize criar e editar em seções independentes. Cada seção apresenta contexto
à esquerda e o painel de campos à direita. No painel, campos relacionados usam
duas colunas nos breakpoints largos e uma coluna no mobile; campos longos,
uploads e erros podem ocupar toda a largura. O rodapé mantém cancelar e salvar
próximos do resultado da ação.

## Breadcrumb e shell

Toda tela renderiza o `Breadcrumb` no shell global. A trilha deve mostrar a
equipe ativa, o módulo e a tela atual, usando labels reais e links válidos nos
itens anteriores. Em aplicações Laravel, localize e reaproveite o componente
`Breadcrumb` ou `Breadcrumbs` já presente no layout, junto da tipagem dos itens;
adapte apenas a composição necessária para inserir a equipe sem duplicar o
primitive. A equipe e a tela atual continuam visíveis no mobile.

## Cenários que toda entrega deve cobrir

Consulte a seção `Cenários canônicos` do template e registre o recorte
aplicável em `DESIGNSYSTEM.MD` ou na spec da entrega:

- lista com registros;
- lista vazia;
- detalhe com status e ações;
- criação válida;
- edição válida;
- criação ou edição com erro de campo;
- ausência de permissão;
- falha de carregamento;
- alteração não salva, quando houver edição;
- resultado de ação destrutiva, quando houver exclusão ou cancelamento.

Para cada cenário, informe pré-condição, ação, resposta, estado visual, foco,
mensagem e próximo passo.

## Limites e handoff

- UX define fluxo, arquitetura da informação e linguagem da tarefa a partir
  desta fonte.
- UI define tokens, hierarquia, composição visual e estados a partir desta
  fonte.
- Componentes React escolhem primitives e composições compatíveis depois de
  ler esta fonte e `INTERFACE.md`.
- A skill de experiência de interface coordena a entrega e não deve iniciar uma
  tela sem carregar `DESIGNSYSTEM.MD`.

## Antipadrões

- Parede de cards quando a pessoa precisa comparar registros.
- Formulário sem seções quando o domínio tem grupos de informação distintos.
- Duas colunas no mobile ou uma grade que separa campo, ajuda e erro.
- Placeholder usado como único label.
- Erro indicado somente por ícone, cor ou toast distante do campo.
- Tela sem `PageHeader`, sem estado vazio ou sem caminho de recuperação.
- Dashboard que mostra números sem pergunta, período, unidade ou próxima ação.
- Dashboard que usa uma parede de cartões sem hierarquia ou investigação.
- Bloco de ReUI ou primitive de shadcn/ui usado sem adaptar dados, estados,
  permissões e tokens do produto.
- Novo token ou componente criado sem verificar o documento e `INTERFACE.md`.
- Exceção visual local registrada como regra global sem alcance explícito.
- CRUD com cabeçalhos duplicados, DataGrid estreito, ID oculto ou sem ações de
  editar e apagar na linha.

## Validação

Antes do handoff, confira:

- `DESIGNSYSTEM.MD` existe na raiz do projeto consumidor e tem classificação,
  política, defaults, estados, cenários e histórico.
- A lista usa `DataGrid` e `PageHeader`.
- Toda tela tem `Breadcrumb` com o nome da equipe ativa, módulo e tela atual.
- Laravel reaproveita o `Breadcrumb` ou `Breadcrumbs` já existente no layout.
- O detalhe usa `DetailLists` e `PageHeader`.
- Criar e editar usam seções, coluna de contexto, painel de campos em duas
  colunas nos breakpoints largos e uma coluna no mobile.
- Erros de campo aparecem em vermelho abaixo do campo e têm associação
  semântica.
- A direção padrão ou a exceção está registrada com alcance.
- `INTERFACE.md` contém somente o registro local da entrega.
- A spec e as tarefas cobrem estados, permissão, foco, mensagens e retorno.
- O dashboard, quando existir, tem filtros, contexto dos indicadores,
  alternativa acessível para visualizações e investigação detalhada.
- Primitives shadcn/ui e blocos ReUI têm origem, estados e consumidores
  registrados em `INTERFACE.md`.
- Cada tarefa possui o item `VISUAL` concluído antes de `EVIDENCE`, com a
  conferência de bordas, espaçamentos, margens, padding e tipografia ou a
  justificativa concreta de que não há interface.

Execute os testes e validadores da stack quando houver implementação. Para a
skill do Specsfy, execute `quick_validate.py` e a suíte do monorepo.

## Skills relacionadas

- [references/standards.md](references/standards.md)
- `skills/templates/DESIGNSYSTEM.MD`
- `skills/templates/Interface.md`
- `specsfy-specialist-interface-experience`
- `specsfy-specialist-ux-design`
- `specsfy-specialist-ui-design`
- `specsfy-specialist-react-ui-components`
