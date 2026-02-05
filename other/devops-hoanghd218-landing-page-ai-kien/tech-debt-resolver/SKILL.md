---
name: tech-debt-resolver
description: Loop automatizado de melhoria contínua que usa o Chat RAG para identificar débitos técnicos, implementa correções, reingere a base de conhecimento e valida até eliminar 100% dos débitos.
license: MIT
---

# Tech Debt Resolver - Loop de Melhoria Contínua

Skill que automatiza a resolução de débitos técnicos através de um loop inteligente que combina:
- **Chat RAG** (identificação de débitos via comparação com Claude Agent SDK)
- **Claude Code** (implementação das correções)
- **Reingestão automática** (atualização da base de conhecimento)
- **Validação** (confirmação de que os débitos foram resolvidos)

## Fluxo do Loop

```
┌─────────────────────────────────────────────────────────────┐
│                    LOOP DE QUALIDADE                        │
│                                                             │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐   │
│  │  Chat RAG   │────▶│ Claude Code │────▶│  Reingestão │   │
│  │  (Análise)  │     │ (Correções) │     │  (Update)   │   │
│  └─────────────┘     └─────────────┘     └─────────────┘   │
│         ▲                                       │          │
│         └───────────────────────────────────────┘          │
│                                                             │
│  Condição de parada: 0 débitos técnicos identificados      │
└─────────────────────────────────────────────────────────────┘
```

## Como Usar

### 1. Iniciar o Loop

O assistente vai:
1. Abrir o Chat RAG via Chrome DevTools
2. Perguntar sobre débitos técnicos comparando Backend vs Claude Agent SDK
3. Coletar a lista de débitos identificados
4. Implementar correções uma a uma
5. Reingerir o backend após cada correção
6. Validar no Chat RAG se o débito foi resolvido
7. Repetir até não haver mais débitos

### 2. Pergunta Inicial para o Chat RAG

Use esta pergunta para iniciar a análise:

```
Analisando o código do Backend (chat-simples) e comparando com as melhores práticas
do Claude Agent SDK Python, liste todos os débitos técnicos identificados.

Para cada débito, informe:
1. Arquivo afetado
2. Descrição do problema
3. Impacto (Alto/Médio/Baixo)
4. Sugestão de correção baseada no Claude Agent SDK

Foque em:
- Padrões de código inconsistentes
- Anti-patterns
- Oportunidades de usar features do SDK
- Melhorias de arquitetura
```

### 3. Pergunta de Validação

Após cada correção, use esta pergunta:

```
Verifique se o débito técnico "{NOME_DO_DEBITO}" no arquivo {ARQUIVO}
ainda existe ou foi resolvido. Compare com o Claude Agent SDK para validar.
```

## Endpoints e Comandos

### Chat RAG
- **URL**: `http://localhost:3000/html/index.html`
- **API**: `http://localhost:8001/chat/stream`

### Scripts de Reingestão
```bash
# Reingerir Backend (após correções)
python scripts/ingest_backend.py

# Reingerir Claude Agent SDK (após git pull)
python scripts/ingest_claude_agent_sdk.py

# Ver status sem ingerir
python scripts/ingest_backend.py --stats
python scripts/ingest_claude_agent_sdk.py --stats
```

## Implementação Automatizada

### Passo 1: Identificar Débitos (Chrome DevTools)

```
1. mcp__chrome-devtools__navigate_page(url="http://localhost:3000/html/index.html")
2. mcp__chrome-devtools__take_snapshot()
3. Identificar o campo de texto e botão de envio
4. mcp__chrome-devtools__fill(uid="{input_uid}", value="{PERGUNTA_INICIAL}")
5. mcp__chrome-devtools__click(uid="{send_button_uid}")
6. mcp__chrome-devtools__wait_for(text="Débito")
7. mcp__chrome-devtools__take_snapshot() para capturar resposta
```

### Passo 2: Implementar Correção (Claude Code)

Para cada débito identificado:
1. Ler o arquivo afetado
2. Implementar a correção sugerida
3. Usar Edit tool para aplicar mudanças
4. Validar que o código está correto

### Passo 3: Reingerir

```bash
python scripts/ingest_backend.py
```

### Passo 4: Validar (Chrome DevTools)

```
1. mcp__chrome-devtools__click(uid="{new_chat_button}") # Novo chat para contexto limpo
2. mcp__chrome-devtools__fill(uid="{input_uid}", value="{PERGUNTA_VALIDACAO}")
3. mcp__chrome-devtools__click(uid="{send_button_uid}")
4. mcp__chrome-devtools__wait_for(text="resolvido" ou "ainda existe")
5. Analisar resposta
```

### Passo 5: Loop

Se ainda houver débitos, voltar ao Passo 2.
Se não houver mais débitos, finalizar com relatório.

## Estrutura de Tracking

Manter um registro dos débitos durante o loop:

```markdown
## Débitos Técnicos - Status

| # | Arquivo | Débito | Status | Data |
|---|---------|--------|--------|------|
| 1 | agentfs_manager.py | Estado global singleton | Resolvido | 2024-01-15 |
| 2 | security.py | CORS hardcoded | Pendente | - |
| 3 | ... | ... | ... | ... |

### Progresso
- Total identificados: X
- Resolvidos: Y
- Pendentes: Z
- Progresso: Y/X (xx%)
```

## Critérios de Conclusão

O loop termina quando:
1. Chat RAG confirma 0 débitos técnicos identificados
2. Todas as comparações com Claude Agent SDK estão alinhadas
3. Código passa em todas as validações

## Dicas

1. **Novo chat para cada validação** - Evita contexto antigo influenciar
2. **Commits incrementais** - Commitar após cada correção resolvida
3. **Reingestão é rápida** - O script só processa arquivos modificados
4. **Priorize por impacto** - Resolva débitos de alto impacto primeiro

## Exemplo de Uso Completo

```
Usuário: /tech-debt-resolver

Assistente:
1. Navegando para Chat RAG...
2. Enviando pergunta sobre débitos técnicos...
3. Débitos identificados:
   - [ALTO] agentfs_manager.py: Estado global singleton
   - [MÉDIO] security.py: CORS hardcoded
   - [BAIXO] logger.py: ContextVar sem cleanup

4. Iniciando correção #1: agentfs_manager.py
   - Implementando injeção de dependência...
   - Arquivo atualizado!

5. Reingerindo backend...
   - 1 arquivo atualizado

6. Validando no Chat RAG...
   - Resposta: "O débito de estado global foi resolvido!"

7. Progresso: 1/3 (33%)

8. Iniciando correção #2...
[continua até 100%]

Resultado Final:
✅ 3/3 débitos técnicos resolvidos
✅ Backend 100% alinhado com Claude Agent SDK
```
