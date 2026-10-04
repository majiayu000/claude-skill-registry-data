---
name: handoff
description: Use quando uma missão precisa continuar em outra sessão ou com outro especialista sem repetir investigação já concluída.
invocation: user
inputs: conversa, artefatos canônicos e foco da próxima etapa
outputs: handoff compacto e redigido, com referências e próxima ação
side_effects: none
context: prompts/agents/handoff.md, knowledge/decisions/
completion: próximo agente consegue iniciar pela primeira ação sem reler a conversa inteira
---

# Handoff

Crie uma transferência compacta para uma nova sessão ou especialista. Por padrão, entregue o handoff na conversa; só salve um arquivo temporário se o usuário pedir.

## Conteúdo obrigatório

1. Missão e estágio atual.
2. Fatos e evidências, referenciados por caminho ou URL.
3. Decisões tomadas e respectivas fontes canônicas.
4. Questões ainda abertas — apenas as que bloqueiam a próxima etapa.
5. Riscos, restrições e ações externas já autorizadas.
6. Próxima ação e skills sugeridas.

## Regras

- Não duplique o conteúdo de specs, cards, decisões ou documentos: aponte para a fonte.
- Remova PII, credenciais e dados sensíveis antes de entregar.
- Não presuma que a próxima sessão tem conectores ou permissões da anterior.
- Para handoff entre agentes, use também o schema em `prompts/agents/handoff.md`.
