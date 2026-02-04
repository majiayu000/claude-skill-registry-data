---
name: devtools-testing
description: Toolkit para interagir e testar aplicações web locais usando Chrome DevTools MCP. Suporta verificação de funcionalidade frontend, debugging de UI, captura de screenshots, análise de performance, inspeção de network e visualização de logs do console.
license: Complete terms in LICENSE.txt
---

# Web Application Testing com Chrome DevTools MCP

Para testar aplicações web locais, use as ferramentas MCP do Chrome DevTools diretamente.

**Vantagens do Chrome DevTools MCP**:
- ✅ Integração nativa com Chrome DevTools
- ✅ Performance insights automáticos (Core Web Vitals)
- ✅ Network debugging completo
- ✅ Console logging em tempo real
- ✅ Screenshots e snapshots do DOM
- ✅ Não requer scripts Python externos

## Ferramentas MCP Disponíveis

### 📝 Input Automation (8 tools)
- `mcp__chrome-devtools__click` - Clicar em elementos
- `mcp__chrome-devtools__drag` - Arrastar elementos
- `mcp__chrome-devtools__fill` - Preencher inputs
- `mcp__chrome-devtools__fill_form` - Preencher formulários completos
- `mcp__chrome-devtools__handle_dialog` - Lidar com dialogs/alerts
- `mcp__chrome-devtools__hover` - Hover sobre elementos
- `mcp__chrome-devtools__press_key` - Pressionar teclas
- `mcp__chrome-devtools__upload_file` - Upload de arquivos

### 🧭 Navigation (6 tools)
- `mcp__chrome-devtools__navigate_page` - Navegar para URLs
- `mcp__chrome-devtools__new_page` - Criar nova aba
- `mcp__chrome-devtools__list_pages` - Listar abas abertas
- `mcp__chrome-devtools__select_page` - Selecionar aba
- `mcp__chrome-devtools__close_page` - Fechar aba
- `mcp__chrome-devtools__wait_for` - Aguardar texto aparecer

### 🔍 Debugging (5 tools)
- `mcp__chrome-devtools__take_snapshot` - Snapshot do DOM (a11y tree)
- `mcp__chrome-devtools__take_screenshot` - Screenshot da página
- `mcp__chrome-devtools__evaluate_script` - Executar JavaScript
- `mcp__chrome-devtools__list_console_messages` - Listar logs do console
- `mcp__chrome-devtools__get_console_message` - Obter log específico

### 📊 Performance (3 tools)
- `mcp__chrome-devtools__performance_start_trace` - Iniciar trace
- `mcp__chrome-devtools__performance_stop_trace` - Parar trace e obter insights
- `mcp__chrome-devtools__performance_analyze_insight` - Analisar insight específico

### 🌐 Network (2 tools)
- `mcp__chrome-devtools__list_network_requests` - Listar requisições
- `mcp__chrome-devtools__get_network_request` - Obter detalhes de requisição

### 📱 Emulation (2 tools)
- `mcp__chrome-devtools__emulate` - Emular device, rede, geolocalização
- `mcp__chrome-devtools__resize_page` - Redimensionar viewport

## Árvore de Decisão: Escolhendo sua Abordagem

```
Tarefa do usuário → HTML estático?
    ├─ Sim → Ler arquivo HTML diretamente para identificar seletores
    │         ├─ Sucesso → Usar ferramentas MCP com seletores
    │         └─ Falha/Incompleto → Tratar como dinâmico (abaixo)
    │
    └─ Não (webapp dinâmico) → Servidor já está rodando?
        ├─ Não → Iniciar servidor primeiro (npm run dev, etc)
        │
        └─ Sim → Padrão Reconnaissance-Then-Action:
            1. new_page ou navigate_page para URL
            2. take_snapshot para ver estrutura do DOM
            3. Identificar seletores (uid) do snapshot
            4. Executar ações com seletores descobertos
```

## Padrão: Reconnaissance-Then-Action 🎯

### 1. Navegar e Inspecionar
```
Ferramentas:
- mcp__chrome-devtools__new_page(url="http://localhost:3000")
  OU
- mcp__chrome-devtools__navigate_page(url="http://localhost:3000")

- mcp__chrome-devtools__take_snapshot()
  → Retorna estrutura do DOM com UIDs únicos para cada elemento
```

### 2. Identificar Seletores
Do snapshot, você recebe elementos como:
```
[42] button "Login" (enabled)
[43] input email (empty)
[44] input password (empty)
```

Os números entre colchetes são os **UIDs** dos elementos.

### 3. Executar Ações
```
Use os UIDs para interagir:
- mcp__chrome-devtools__fill(uid="43", value="user@example.com")
- mcp__chrome-devtools__fill(uid="44", value="senha123")
- mcp__chrome-devtools__click(uid="42")
```

## Exemplos Práticos

Ver pasta `examples/` para exemplos detalhados:
- `element_discovery.md` - Descobrir elementos na página
- `console_logging.md` - Capturar logs do console
- `static_html_automation.md` - Automatizar HTML estático

## Armadilhas Comuns ⚠️

### ❌ Não use UIDs de snapshots antigos
```
1. take_snapshot()  → UIDs: 10, 11, 12
2. navigate_page(url="outra-url")
3. click(uid="10")  ❌ UID inválido! Nova página = novos UIDs
```

✅ **Sempre tire novo snapshot após navegação**
```
1. navigate_page(url="nova-url")
2. take_snapshot()  → Novos UIDs: 20, 21, 22
3. click(uid="20")  ✓ Correto!
```

### ❌ Não assuma que elementos existem
```
1. navigate_page(url="http://localhost:3000")
2. click(uid="10")  ❌ Não sabemos se uid 10 existe!
```

✅ **Sempre faça reconnaissance primeiro**
```
1. navigate_page(url="http://localhost:3000")
2. take_snapshot()  → Verificar o que existe
3. click(uid="10")  ✓ Agora sabemos que existe!
```

### ❌ Não ignore wait_for em SPAs
```
1. click(uid="10")  # Trigger navigation
2. take_snapshot()  ❌ Pode capturar antes de carregar!
```

✅ **Aguarde conteúdo esperado**
```
1. click(uid="10")
2. wait_for(text="Dashboard")  ✓ Aguarda carregar
3. take_snapshot()
```

## Melhores Práticas 📋

1. **Use snapshot como primeiro passo** - Sempre faça `take_snapshot()` antes de interagir
2. **Prefira snapshot a screenshot para descoberta** - Snapshot dá UIDs, screenshot é só visual
3. **Use verbose=true quando precisar de mais contexto**
4. **Aproveite fill_form para múltiplos campos** - Uma chamada para vários inputs
5. **Network e Console são passivos** - Capturam automaticamente, consulte depois
6. **Performance trace é sua ferramenta de diagnóstico** - Use para problemas de performance
7. **Use wait_for() para sincronização** - Melhor que timeouts arbitrários

## Script Utilitário

**Helper script disponível**: `scripts/with_server.py`

Gerencia lifecycle de servidores (útil tanto para Playwright legado quanto para Chrome DevTools MCP):

```bash
# Single server
python scripts/with_server.py --server "npm run dev" --port 5173

# Multiple servers (backend + frontend)
python scripts/with_server.py \
  --server "cd backend && python server.py" --port 3000 \
  --server "cd frontend && npm run dev" --port 5173
```

Após servidores iniciados, use as ferramentas MCP chrome-devtools para testar.

## Migração do Playwright

Se você está migrando de Playwright, consulte `MIGRATION-GUIDE.md` para um guia completo de conversão.

**Exemplos legados** em Python/Playwright estão disponíveis em `examples/LEGACY-PLAYWRIGHT/` para referência.

## Recursos Adicionais

- **Chrome DevTools MCP Server**: `chrome-devtools-mcp/`
- **Tool Reference**: `chrome-devtools-mcp/docs/tool-reference.md`
- **Troubleshooting**: `chrome-devtools-mcp/docs/troubleshooting.md`
- **Design Principles**: `chrome-devtools-mcp/docs/design-principles.md`

## Quando Usar

### ✅ Use DevTools MCP Testing para:
- Testar SPAs React/Vue/Angular
- Debugging de problemas de UI
- Análise de performance detalhada (Core Web Vitals)
- Inspeção de network requests
- Captura de console logs
- Testes E2E simples
- Verificação de responsividade
- Emulação de devices e network

### ⚠️ Considere alternativas para:
- Testes unitários (use Jest, Vitest)
- Testes de API pura (use Postman, curl)
- Load testing (use k6, Artillery)
- Cross-browser testing (DevTools MCP é Chrome apenas)
