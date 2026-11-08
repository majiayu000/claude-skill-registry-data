---
name: gaas-estrategias-implementaveis
description: Criar ou revisar notas de estratégia do GaaS com narrativa enciclopédica, fluxos detalhados e fichas suficientes para implementação, usando a página Visa como modelo. Usar para estruturar estratégia, documentação operacional e mockups dessas notas; complementar a skill geral de produto, sem substituir copy de campanha ou análise de resultados.
---

# Estratégias implementáveis no GaaS

## Resultado esperado

A nota deve permitir ao time entender a estratégia, discutir suas decisões e preparar sua implementação sem depender de uma explicação oral do autor. A página **Estratégia Pool de Ofertas Visa** é o modelo de referência de narrativa, profundidade, gráficos e apresentação. Usar somente a aparência do leitor não atende ao pedido.

Esta skill registra a orientação de Pablo de 06/11/2026: conteúdo próximo de uma enciclopédia, sem slogans ou frases clichês, com o máximo de detalhe relevante e aprofundamento por minimizações. Modularidade significa separar módulos conectados por identidades e dependências; não reduzir o projeto a cartões genéricos.

## Referências e fontes

1. Leia a nota Visa e os documentos do projeto tratado. No repositório, procure `docs/wiki-vault/05-Estrategia/Estrategia-Pool-de-Ofertas-Visa.md` como projeção de leitura e a nota canônica correspondente em `Afinz-CRM-Midia-Vault/`. Não editar a projeção para corrigir a fonte.
2. Leia [references/modelo-visa.md](references/modelo-visa.md) para transferir o padrão para outra estratégia.
3. Para Seguros, leia [references/seguros-e-compatibilidade.md](references/seguros-e-compatibilidade.md). Ela localiza fontes e conflitos; não substitui a verificação das versões atuais.
4. As notas de DEs, automações e atividades são referências operacionais. Contratos conflitantes exigem explicitação da divergência; não resolver por omissão nem pelo documento mais antigo.

## Narrativa

Começar com definição concreta: o que a estratégia organiza, qual público/produto, qual resultado pretende avaliar e como funciona. Depois explicar escopo, regras e percurso; aprofundar em arquitetura, contratos, implementação e validação.

Usar parágrafos conectados, termos definidos antes do uso, títulos descritivos e tabelas para comparação. Explicar por que cada regra existe e o efeito de falhar nela. Densidade de conteúdo e clareza visual devem coexistir.

Evitar frases como “Duas entradas. Um percurso.”, “Da fonte à jornada.”, “Conectando oportunidades.”, “Inteligência que transforma.” e substituições equivalentes de conteúdo por slogan. Exemplo de título adequado: “Fluxo técnico da automação processos_seguros”. Remover a frase vazia, não apenas reformulá-la.

Não impor um limite curto ao documento. Detalhes que sustentam implementação ficam acessíveis em fichas recolhíveis. Uma síntese não substitui SQL, campos, condições, exceções e validações disponíveis nas fontes.

## Módulos articulados

Adapte a ordem ao projeto, preservando os módulos aplicáveis:

- Definição, intenção, escopo e estado da operação.
- Percurso completo da base à medição, com regras, exceções e retornos.
- Público, elegibilidade, exclusões, alocação e prioridades.
- Experiência, comunicação e cadência, quando existirem.
- Automações: ordem, responsabilidades, fontes, destinos e dependências.
- Fichas das entidades/DEs: grão, chave, campos, tipos, nulidade, atualização e retenção.
- Fichas de atividades/queries: configuração, ação de gravação, SQL íntegro disponível e conferências.
- Critérios de aceite, casos de teste, medição e condições de liberação.
- Decisões abertas, responsáveis a definir, referências e data da evidência.
- Atividades reais vinculadas ao projeto, sem copiar as atividades de outro exemplo.

O nome técnico de um nó do diagrama deve localizar sua ficha. A ficha deve apontar para entradas, saídas, dependências e validação. Links e IDs fazem os módulos se articularem.

## Gramática dos fluxos

Seguir os fluxos da Visa: agrupamentos identificam automações/fases; nós identificam atividades ou entidades; decisões explicitam condições e ramos; setas indicam sequência, dependência e retorno. Incluir grão e destino quando mudarem a compreensão.

No mapa técnico, usar nomes reais de automações, passos e atividades quando documentados, seus tipos, ações e estados. Uma cadeia de verbos genéricos como “validar → selecionar → executar” não substitui esse mapa. Se o nome ou a configuração não existe, marcar “a definir” ou “proposta de nome”; não fabricar implantação.

Separar fluxo de negócio de pipeline técnico, mantendo os vínculos entre ambos. Preservar toda a lógica relevante: condições de entrada/saída, caminhos sem envio, descarte, precedência, dependências sequenciais, falhas, retornos e medição. Nunca achatar um fluxo só para caber numa imagem.

Preferir o renderer de diagramas já usado pela Visa (Mermaid/controles do GaaS) para manter o mapa ampliável e a fonte editável. Usar base clara, tipografia legível, nós e agrupamentos de cantos retos, bordas finas slate e teal discreto nos controles. Não usar uma coleção de cartões ilustrativos como substituto do fluxo. Um mapa grande pode ter rolagem e ampliação; preservar também a navegação responsiva.

## Fichas implementáveis

Para DE: nome, finalidade, origem, destino, grão, PK, sendability e relação de envio, tipos/tamanhos, obrigatório/nulo, definição do campo, regra de transformação, ação de carga e retenção. Ausências ficam marcadas como definição pendente.

Para atividade: nome, tipo, automação/passo, estado e evidência, finalidade, fontes, destino, ação de gravação, chave, dependências, parâmetros, regra, SQL completo disponível, primeira execução, reexecução/idempotência, testes, resultado esperado e limitações. SQL proposto não recebe selo de homologado.

Não inventar campos, tipos, nomes, BU/MID, schedules, SQL ou valores para completar um mockup. Separar contrato documentado, execução comprovada, proposta, inferência e lacuna. Número histórico leva data/fonte; não vira parâmetro vigente automaticamente.

## Edição e apresentação

Índice lateral por tópicos; no celular, índice expansível. Minimizações escondem profundidade, não removem conteúdo. Setas e lápis são ações separadas. Edição, inclusão, exclusão, ordenação, restauração e histórico devem respeitar os contratos existentes e suas permissões. Remover da nota não equivale a apagar um registro de tarefa.

O botão de adicionar usa tratamento neutro, sem verde chamativo. Manter a identidade do GaaS, a leitura contínua e a posição da nota ao navegar no índice. Referências externas e detalhes técnicos devem permanecer consultáveis.

## Entrega e aprovação

Quando criar ou alterar a estrutura narrativa/visual dessas páginas, apresentar primeiro um mockup com texto e detalhes técnicos representativos. A validação precisa cobrir **narrativa, profundidade, diagramas e interação**, não apenas cores. Distinguir visual ilustrativo de conteúdo disponível, sem tratar o mockup como especificação técnica homologada.

Na etapa de mockup, criar apenas materiais locais de revisão e a skill solicitada. Não alterar a página viva, dados, permissões, main ou deploy. A aprovação anterior de outra direção não autoriza a nova proposta. Após a validação do usuário, implementar somente o escopo aprovado, comparar com a referência e seguir os checks/deploy autorizados do projeto.

Ao concluir a revisão, perguntar: “Outro profissional consegue montar e conferir a operação com o documento e suas referências? Se não, quais definições e evidências ainda faltam?” Uma lacuna explícita com seu efeito é mais útil que uma falsa especificação completa.
