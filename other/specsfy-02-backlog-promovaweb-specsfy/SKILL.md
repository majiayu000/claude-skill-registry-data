---
name: specsfy-02-backlog
description: "Use quando o usuário quer transformar uma captura de `specs/inbox/`, uma oportunidade, um problema ou um item existente em backlog pronto para especificação, inclusive por transição automática. Pesquisa duplicatas e referências, cria ou atualiza `specs/backlog/`, faz perguntas adaptativas, aplica o MCR-10 e produz um brief testável. Para apenas guardar um texto sem perguntas use specsfy-01-inbox; não use para escrever spec.md, tarefas, testes ou implementação."
---

# Refinar e aprofundar o backlog

Transforme uma entrada vaga em um item de backlog compreensível e, quando a
intenção exigir especificação, aprofunde as decisões até produzir um brief
testável. Esta é a segunda etapa sequencial do framework. Ela reúne registro,
refinamento e descoberta sem transformar o backlog em fonte normativa.

## Orquestrar a conversa

Ao concluir esta etapa ou detectar trabalho de outra etapa, anuncie
`Pendência detectada: <descrição> — ação: resolvendo nesta etapa` e resolva-a
quando pertencer ao próprio escopo. Quando houver troca de responsabilidade,
anuncie `Transição automática: $specsfy-02-backlog → $<destino> — motivo:
<motivo> — resultado esperado: <resultado>` e carregue imediatamente a skill
de destino, sem pedir confirmação nem repetir o comando. Continue na mesma
conversa.

Depois de uma correção necessária a esta etapa, anuncie `Retomada automática:
$<destino> → $specsfy-02-backlog — pendência resolvida: <resultado>` e retome-a
imediatamente. Reavalie o estado após cada handoff para evitar ciclos. O handoff
não exige confirmação; ações sensíveis continuam exigindo autorização
específica.

## Buscar duplicatas e referências

1. Extraia termos derivados do pedido do usuário, incluindo nomes do domínio e
   equivalentes evidentes já usados na conversa.
2. Antes de criar ou atualizar o item, pesquise esses termos em:
   - `specs/inbox/*.md`;
   - `specs/backlog/*.md`;
   - `specs/specs/*/spec.md`;
   - `docs/**/*.md`.
3. Leia somente resultados plausíveis e classifique cada relação:
   - **possível duplicata**: problema, pessoa, resultado e contexto
     substancialmente iguais;
   - **backlog relacionado**: item complementar, dependência ou precedente;
   - **spec relacionada**: comportamento definido ou entregue que limita o
     item;
   - **documentação relacionada**: vocabulário, regra ou contexto do projeto.
4. Apresente correspondências materiais com seus caminhos. Diante de possível
   duplicata, confirme com o usuário se deve atualizar o item ou registrar uma
   diferença real.
5. Registre fontes úteis em `Referências relacionadas`, com caminho relativo e
   tipo de relação. Não transforme uma decisão encontrada em declaração do
   usuário.

Se uma resposta mudar materialmente os termos, o problema, a pessoa, o
resultado ou o contexto, repita a busca.

## Garantir a captura mínima

1. Preserve a formulação original recebida na conversa ou em
   `specs/inbox/<data-hora>-<slug>.md`. Separe declaração, inferência e aberto.
2. Confirme se o contexto esclarece:
   - problema percebido;
   - pessoa afetada ou beneficiada;
   - resultado ou valor esperado;
   - contexto suficiente para distinguir a entrada de pedidos semelhantes.
3. Se algo estiver ausente, vago, contraditório ou ambíguo, escolha a lacuna de
   maior impacto e faça uma pergunta por vez.
4. Reavalie as lacunas depois de cada resposta. Não transforme os itens em
   questionário fixo nem repita informação já fornecida.
5. Não crie nem atualize o arquivo enquanto algum item essencial continuar
   ausente ou ambíguo. Se a pessoa não souber responder, explique a lacuna sem
   inventar conteúdo.

A captura mínima não exige solução técnica, critérios completos de aceitação
ou prioridade. Esses dados podem amadurecer no aprofundamento.

## Criar ou atualizar o item

1. Se a pessoa apenas quiser explorar sem registrar, converse e confirme antes
   de escrever.
2. Se existir item correspondente, atualize-o sem mudar seu ID e preserve a
   formulação anterior.
3. Se a origem for `specs/inbox/`, registre esse caminho em
   `Referências relacionadas`; não altere nem apague a captura.
4. Para criar um item novo, execute:

```bash
python3 -B <diretório-da-skill>/scripts/iniciar_backlog.py \
  --title "<título curto>" \
  --idea "<formulação original>" \
  --problem "<problema percebido>" \
  --person "<pessoa afetada ou beneficiada>" \
  --result "<resultado ou valor esperado>" \
  --context "<contexto que distingue a ideia>" \
  [--slug <slug>] [--root <raiz>]
```

5. Use o caminho absoluto impresso pelo script. Ele prefere
   `.specsfy/templates/custom/Backlog.md` e recorre a
   `.specsfy/templates/Backlog.md`.

## Organizar e priorizar

Leia `references/backlog-quality.md` ao estruturar, refinar, priorizar ou
avaliar prontidão.

- Classifique, quando conhecido, em Produto → Épico → Funcionalidade → item.
- Use tipos como épico, história, regra, técnico e melhoria sem confundir tipo
  com prioridade.
- Ordene por valor, risco, dependências, urgência, esforço, desbloqueios e
  incerteza; não marque tudo como prioridade alta.
- Aprofunde campos conforme risco e complexidade. Autenticação, pagamentos,
  permissões, privacidade e operações assíncronas exigem mais cuidado.
- Prefira comportamento observável a solução de interface.
- Torne atributos de qualidade mensuráveis quando forem materiais.
- Use listas, fluxos, cenários ou matrizes quando reduzirem ambiguidade.

## Aprofundar para a especificação

Quando a pessoa pedir aprofundamento, promoção ou criação de uma spec:

1. Leia a entrada de `specs/inbox/`, o item de `specs/backlog/` ou a spec
   indicada. Se houver mais de um candidato, pergunte qual aprofundar.
2. Resuma em uma frase o problema, a pessoa e o resultado percebido.
3. Separe o que está decidido do que pode mudar escopo, experiência, segurança,
   dados, testes ou arquitetura.
4. Leia `references/discovery-map.md` para selecionar perguntas relevantes;
   não percorra o mapa mecanicamente.
5. Leia `../specsfy-03-specify/references/mcr-10.md` e faça a análise categorial
   silenciosamente antes da primeira pergunta.
6. Leia `references/specialists.md` somente quando tecnologia ou disciplina
   exigir contexto adicional.

## Conduzir a descoberta adaptativa

Execute um ciclo sem limite máximo de perguntas:

1. Antes de cada pergunta, releia a entrada, as decisões confirmadas, o
   contexto acumulado e a nova resposta, além da evidência aplicável.
2. Reclassifique lacunas e dependências. Continue enquanto existir lacuna aplicável;
   encerre quando cada uma estiver decidida, não aplicável ou resolvida por
   evidência.
3. Selecione a lacuna de maior `impacto × incerteza`, priorizando P1, P2 e P3,
   e faça uma pergunta por vez.
4. Registre a resposta original, a decisão normalizada e seus efeitos. Volte ao
   primeiro passo; não reutilize uma fila fixa.

A partir da 11ª pergunta, inclua a opção explícita `avançar` em todas as
rodadas. Antes disso, não ofereça essa saída. Se a pessoa escolher `avançar`:

- preserve as lacunas não resolvidas, com impacto e estado;
- não preencha respostas por inferência;
- encerre somente o ciclo atual;
- permita o handoff solicitado, mantendo `Status: Draft` e
  `Definition Gate: Pending` até resolver as lacunas aplicáveis.

Durante a conversa:

- ofereça 2–3 opções mutuamente exclusivas quando reduzirem o esforço e
  recomende uma com justificativa curta;
- aceite respostas livres e use-as na reanálise;
- preserve termos originais e diferencie declaração, inferência, hipótese,
  decisão, conflito e aberto;
- confirme intenção operacional por síntese;
- não recite as dez categorias nem faça uma pergunta por categoria.

Garanta cobertura suficiente de problema, atores, resultado, escopo, jornadas,
falhas, limites, regras, dados, segurança, privacidade, desempenho,
acessibilidade, restrições existentes e sinais objetivos de aceite e sucesso.

## Manter o item

Use exatamente `specs/backlog/<NNNN>-<slug>.md` e mantenha:

- `Status: Captured` enquanto o item estiver apenas registrado;
- `Status: Refining` durante refinamento ou descoberta;
- `Status: Ready for specification` quando o brief estiver suficiente;
- `Status: Promoted` depois que uma spec derivada existir.

Mantenha as metainformações na tabela abaixo do título. Não invente prioridade,
prazo, stakeholder, solução ou evidência. Use `Pronto para desenvolvimento`
como diagnóstico, nunca como autorização de implementação.

## Encerrar

Apresente um `Brief pronto para especificar` com:

1. Problema e objetivo.
2. Atores.
3. Escopo e fora de escopo.
4. Jornadas e regras essenciais.
5. Critérios de aceite em Given/When/Then.
6. Restrições técnicas e de qualidade.
7. Suposições.
8. Decisões abertas ou `Nenhuma lacuna aplicável`.
9. Vocabulário ambíguo e inferências confirmadas.

Atualize o item de backlog quando a pessoa autorizar esse registro. Quando o
brief estiver suficiente ou a pessoa escolher `avançar`, retorne
automaticamente para `$specsfy-update-spec` se a etapa foi chamada por mudança
tardia em spec aprovada. Para criar ou consolidar a definição inicial, chame
`$specsfy-03-specify`. No caso de `avançar`, entregue brief parcial e informe
as lacunas que impedem o Definition Gate.

## Limites

- Não alterar nem apagar entradas de Inbox.
- Não criar `spec.md`, tarefas, research, testes ou código.
- Não inventar stakeholders, integrações, restrições ou decisões.
- Não transformar hipótese técnica em requisito.
- Não mover nem apagar item existente sem confirmação.
