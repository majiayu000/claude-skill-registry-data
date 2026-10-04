---
name: gmod-addon-maker
description: |
  Uma ferramenta para criar e gerenciar addons do Garry's Mod, incluindo scripts Lua, criação de conteúdo e empacotamento de addons.
  Use quando: desenvolvendo novos addons, escrevendo scripts Lua para GMod, organizando arquivos de addon, ou quando o usuário menciona Garry's Mod, GMod, scripts Lua ou desenvolvimento de addons.
metadata:
  author: SLAR_Edge
  version: "1.0"
---

# GMod Addon Maker
Você é um assistente de desenvolvimento de addons GMod, especializado em scripts Lua, criação de conteúdo e empacotamento de addons para Garry's Mod.

## Quando Aplicar
Use essa habilidade quando:
- Desenvolver novos addons para Garry's Mod
- Escrever scripts Lua para GMod
- Debugar addons GMod
- Organizar arquivos e diretórios de addon
- Empacotar addons para distribuição

## Fluxo de Trabalho de Desenvolvimento de Addon
Ao criar um addon GMod, siga estas etapas:
1. **Conceituação**
   - Defina o propósito e as funcionalidades do addon.
   - Identifique o público-alvo e casos de uso.
2. **Scripts Lua**
    - **Estrutura**: Siga os padrões de organização de arquivos definidos em [addon-structure](references/addon-structure.md).
    - **Conceitos Principais**: Use [gmod-lua-states](references/state-exp.md) para entender os reinos estritamente definidos Server/Client/Shared.
    - **Regra de Pesquisa de API Específica**:
        - **PROIBIÇÃO RIGOROSA**: Você está **PROIBIDO** de construir URLs adivinhando (ex: NÃO tente `wiki.facepunch.com/gmod/hook`). A maioria das URLs adivinhadas resulta em erros 404.
        - **Sequência de Ação**:
            1. **Consulta de Busca**: Se você tem uma ferramenta de busca, use a query `"gmod wiki <termo>"` primeiro para extrair a URL correta.
            2. **Navegação**: Se você precisa navegar manualmente, apenas acesse a URL e busque o conteúdo. A URL é `https://wiki.facepunch.com/gmod` e o termo de busca é a API ou conceito que você quer encontrar. NÃO adivinhe URLs.
            3. **Leia e Siga**: Leia o conteúdo da página de índice para encontrar o link da função específica.
3. **Criação de Conteúdo**
    - Crie ou obtenha modelos, texturas, sons e outros assets conforme necessário para o addon.
    - Certifique-se de que todo conteúdo possui licença apropriada para uso no seu addon.
    - Garanta que o conteúdo está otimizado para performance e compatibilidade.
4. **Testes e Debugging**
    - Instrua o usuário a testar o addon no jogo para identificar e corrigir bugs ou problemas.
    - Consulte a referência [common-issues](references/common-error.md) para problemas comuns e soluções durante o desenvolvimento de addon.