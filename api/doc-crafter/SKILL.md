---
name: doc-crafter
description: Especialista em documentação de código e APIs. Gera e atualiza especificações (OpenAPI/Swagger), diagramas Mermaid, README e JSDoc/Docstrings. Use para "documentar este endpoint", "atualizar swagger" ou "gerar documentação da função".
---

## Escopo de Atuação

Esta skill lê o código fonte, interpreta a lógica de negócio e gera artefatos de documentação legíveis por humanos e máquinas, sem alterar o comportamento do sistema.

## Workflow

1. **Análise de Lógica**: Lê os arquivos de código solicitados (controllers, rotas, services) para inferir inputs, outputs, e exceções.
2. **Atualização de APIs**: Se for uma API, atualiza o arquivo de especificação (`swagger.yml`, `openapi.json` ou coleções do Postman/Insomnia) garantindo que payloads e status codes correspondam ao código.
3. **Comentários Inline**: Adiciona blocos de comentários padronizados (Docstrings, JSDoc, JavaDoc) em funções complexas, focando no "Por que" e não no "O que".
4. **Docs Sync**: Se uma nova feature de alto nível for documentada, sugere a atualização automática do `README.md` do projeto.

## Restrições
- Não documente getters/setters lógicos ou código autoexplicativo (evite poluição).
- Consulte `memorys/guidelines.md` para verificar o padrão de documentação do projeto antes de escrever.
