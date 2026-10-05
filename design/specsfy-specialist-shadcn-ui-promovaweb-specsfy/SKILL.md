---
name: specsfy-specialist-shadcn-ui
description: Instalar, compor e adaptar shadcn/ui com registry, Radix, theming, formulários, tabelas, gráficos, sidebars e componentes acessíveis. Use quando houver components.json, componentes shadcn ou pedido explícito por shadcn; trate o código copiado como código do projeto.
---

# shadcn/ui

## Fluxo

1. Confirmar framework, versão, `components.json`, aliases, CSS e registry.
2. Auditar componentes já incorporados antes de adicionar novos.
3. Escolher primitives pelo comportamento e semântica exigidos.
4. Adicionar o menor conjunto e revisar o código gerado.
5. Adaptar tokens, variantes e composição sem quebrar acessibilidade do primitive.
6. Construir estados reais: loading, empty, error, disabled e permission denied.
7. Testar teclado, foco, responsividade, formulário e tema.

## Padrões

- Não tratar shadcn/ui como dependência opaca; o source pertence ao projeto.
- Preservar roles, labels, focus management e escape dos primitives.
- Centralizar tokens; evitar editar dezenas de componentes para trocar tema.
- Compor Data Table por caso de uso, sem inventar componente universal.
- Fazer Sidebar responder a viewport, densidade e hierarquia de navegação.
- Validar formulários no servidor e associar erros a campos.
- Atualizar componente somente após comparar diff e customizações locais.

## Validação

- Typecheck, lint, testes e build.
- Navegação completa por teclado, focus trap e retorno de foco.
- Mobile/desktop, tema claro/escuro, zoom e conteúdo longo.
- Estados de tabela, gráfico, formulário, dialog e sidebar usados.

Leia [references/standards.md](references/standards.md) para registry, padrões de
dashboard, composição e fontes oficiais.
