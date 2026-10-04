---
name: modelagem-dominio
description: Use quando termos de produto estão ambíguos, uma relação de domínio muda ou uma decisão estrutural precisa ser registrada com linguagem canônica.
invocation: model
inputs: conversa atual, Knowledge Graph, decisões relevantes e evidência disponível
outputs: termos canônicos, ambiguidades resolvidas, relações atualizadas ou proposta de decisão
side_effects: write-confirmed
context: knowledge/domains/, knowledge/relations.md, knowledge/relations.yaml, knowledge/decisions/
completion: termos e limites relevantes estão claros; toda persistência necessária foi confirmada
---

# Modelagem de Domínio

Use esta disciplina para mudar o modelo de domínio, não apenas para consultá-lo.

## Processo

1. Leia os domínios, relações e decisões ligados ao assunto.
2. Quando um termo for vago, sobreposto ou contraditório, proponha o termo canônico e explique a diferença em linguagem simples.
3. Teste a definição com cenários concretos, incluindo ao menos um caso de fronteira quando existir risco de confusão.
4. Verifique se o modelo, processos e fontes operacionais disponíveis concordam. Trate divergência como fato a resolver, não como detalhe a esconder.
5. Quando um termo estiver realmente resolvido, proponha seu registro em `knowledge/glossario.md`. Crie esse arquivo apenas no primeiro termo que merecer ser mantido.
6. Quando uma relação de domínio for resolvida ou alterada, proponha atualizar `knowledge/relations.md` e `knowledge/relations.yaml` juntos.
7. Proponha uma decisão em `knowledge/decisions/` somente se a escolha for difícil de reverter, surpreendente sem contexto e resultado de um trade-off real.

## Regras

- O glossário contém linguagem e definição; não vira spec nem histórico de implementação.
- O Decision Log explica decisões; não repita o histórico em campos de contexto de cards.
- Não grave no grafo ou no log com base em hipótese não confirmada.
- Cite as fontes que sustentam cada alteração proposta.
