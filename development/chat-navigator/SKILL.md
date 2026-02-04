---
name: chat-navigator
description: Navegação e teste conversacional de aplicações web usando Chrome DevTools. Permite testar sites através de comandos naturais em português, com suporte a contexto do Neo4j e integração automática com hooks de validação.
license: MIT
---

# Chat Navigator - Navegação Conversacional Web

Skill para testar aplicações web de forma conversacional, usando Chrome DevTools MCP com linguagem natural em português.

## Quando Usar

Use esta skill quando o usuário:
- Pedir para "navegar", "abrir", "testar" um site
- Quiser interagir com uma página web conversacionalmente
- Solicitar testes de UI/UX em linguagem natural
- Precisar verificar funcionalidades de forma exploratória

**Exemplos**:
- "Abra o localhost:3000 e clique no botão de login"
- "Navegue para o site e me diga o que tem na tela"
- "Teste o formulário de cadastro e veja se funciona"
- "Verifique se o chat está carregando corretamente"

## Características

### 🗣️ Conversacional
- Aceita comandos em português natural
- Interpreta intenções do usuário
- Fornece feedback descritivo
- Faz perguntas quando necessário

### 🧠 Inteligente
- Consulta Neo4j por contexto histórico
- Aprende com testes anteriores
- Sugere ações baseadas no contexto
- Identifica padrões conhecidos

### 🔗 Integrado
- Usa hooks de validação automaticamente
- Respeita pre-browser-validation
- Registra aprendizados no Neo4j
- Compartilha contexto entre sessões

### 🎯 Focado em Testes
- Identifica elementos interativos
- Valida estados esperados
- Reporta erros claramente
- Captura evidências (screenshots, logs)

## Fluxo de Uso

### 1. Navegação Inicial

**Usuário diz**: "Abra o localhost:3000"

**Skill faz**:
```
1. Validar URL (hook pre-browser-validation dispara)
2. Consultar Neo4j: "localhost:3000"
3. Abrir página: mcp__chrome-devtools__new_page
4. Tirar snapshot: mcp__chrome-devtools__take_snapshot
5. Descrever o que vê para o usuário
6. Sugerir próximas ações baseadas no contexto
```

**Resposta exemplo**:
```
✅ Navegado para http://localhost:3000/html/

📸 Página carregada:
- Título: "Claude Chat - Streaming Real"
- Status: 🟢 (conectado ao backend)

🧭 Toolbar de Navegação:
- ⟲ Projetos → index_projects.html
- 📁 Histórico → index_projects.html
- 📄 Outputs → output.html
- 📊 Audit → audit_dashboard.html

📝 Elementos principais:
- Campo de texto: textbox "Digite sua mensagem..."
- Botão "Enviar ➤"
- Botão "✨ Novo Chat"
- Botão "🔄" (atualizar)

💡 Sugestões:
- Testar enviar uma mensagem
- Ver arquivos em Outputs
- Verificar tool calls em Audit
```

### 2. Interação Conversacional

**Usuário diz**: "Digite 'olá mundo' e envie"

**Skill faz**:
```
1. Localizar campo de texto: textbox "Digite sua mensagem..."
2. Preencher: mcp__chrome-devtools__fill(uid="X", value="olá mundo")
3. Localizar botão: button "Enviar ➤"
4. Clicar: mcp__chrome-devtools__click(uid="Y")
5. Aguardar resposta: mcp__chrome-devtools__wait_for(text="📋", timeout=30000)
   (📋 é o botão de copiar que aparece quando resposta completa)
6. Tirar novo snapshot para ver resposta
7. Reportar resultado ao usuário
```

**Indicadores de Estado**:
- Durante processamento: "Claude está processando..." + timer + botão "Parar"
- Resposta completa: Botão "📋" (copiar) aparece na mensagem do Claude
- Botão enviar fica `disabled` durante processamento

### 3. Verificação e Validação

**Usuário diz**: "Verifique se funcionou"

**Skill faz**:
```
1. Analisar último snapshot
2. Verificar console logs (erros?)
3. Verificar network requests
4. Comparar estado esperado vs atual
5. Reportar sucesso ou falhas
6. Registrar resultado no Neo4j
```

## Comandos Suportados

### Navegação
- "Abra [URL]"
- "Navegue para [URL]"
- "Vá para [URL]"
- "Acesse [URL]"
- "Volte" / "Avance"
- "Recarregue a página"

### Interação
- "Clique em [elemento]"
- "Clique no botão [nome]"
- "Digite [texto] no campo [nome]"
- "Preencha o formulário com [dados]"
- "Selecione [opção]"
- "Arraste [elemento] para [destino]"

### Verificação
- "O que tem na tela?"
- "Mostre o que está aparecendo"
- "Verifique se [condição]"
- "Tem algum erro?"
- "O [elemento] está visível?"
- "Qual o status da conexão?"

### Captura
- "Tire um screenshot"
- "Mostre os logs do console"
- "Quais requisições foram feitas?"
- "Me mostra o HTML do [elemento]"

### Contexto
- "O que você sabe sobre este site?"
- "Já testamos isso antes?"
- "Qual o contexto histórico?"
- "Salve esta informação"

## Padrões de Resposta

### Sucesso
```
✅ [Ação] concluída com sucesso

📋 Resultado:
- [Detalhe 1]
- [Detalhe 2]

💡 Próximo passo sugerido: [sugestão]
```

### Erro
```
❌ [Ação] falhou: [razão]

🔍 Detalhes:
- [Erro específico]
- [Contexto do erro]

💡 Sugestão: [como resolver]
```

### Aguardando
```
⏳ Aguardando [condição]...
```

### Informação
```
📊 [Título]

[Conteúdo estruturado]

💡 [Insights ou sugestões]
```

## Integração com Neo4j

### Consulta Antes de Navegar
```
Antes de navegar para uma URL, sempre:
1. Consultar: mcp__neo4j-memory__search_memories(query="[host]")
2. Analisar resultados
3. Incorporar contexto na resposta
4. Sugerir ações baseadas em histórico
```

### Registro Após Testes
```
Após completar uma ação importante:
1. Identificar aprendizado
2. Criar observação no Neo4j
3. Conectar com entidades relevantes
4. Exemplo: "Botão de envio demora 2s para responder"
```

## Tratamento de Erros

### URL Inválida
```
❌ URL inválida ou inacessível

Verifique:
- Protocolo correto (http/https)
- Servidor está rodando?
- Porta correta?

💡 Use: lsof -i :[porta] para verificar
```

### Elemento Não Encontrado
```
❌ Elemento "[nome]" não encontrado na página

🔍 Elementos disponíveis:
[Lista dos elementos visíveis]

💡 Talvez você quis dizer: "[sugestão]"
```

### Timeout
```
⏸️ Timeout aguardando "[condição]"

A página pode estar:
- Carregando lentamente
- Com erro de JavaScript
- Sem resposta do backend

💡 Verificar console logs?
```

## Melhores Práticas

### 1. Sempre Tirar Snapshot Primeiro
Antes de qualquer interação, capture o estado atual da página.

### 2. Aguardar Carregamentos
Use `wait_for()` após ações que causam mudanças assíncronas.

### 3. Verificar Console Logs
Após ações importantes, verifique se há erros no console.

### 4. Contexto Incremental
Mantenha contexto da sessão, não peça snapshot a cada comando trivial.

### 5. Feedback Contínuo
Sempre informe o usuário sobre o que está fazendo e o que encontrou.

### 6. Aprendizado Persistente
Registre padrões úteis no Neo4j para reusar em futuras sessões.

## Exemplos Completos

### Exemplo 1: Teste de Login
```
Usuário: "Teste o login no localhost:3000"

Skill:
1. 🔍 Consultando Neo4j...
   → localhost:3000 é o frontend do chat-simples
   → Backend em localhost:8001

2. 🌐 Navegando para http://localhost:3000...
   ✅ Página carregada

3. 📸 Analisando tela...
   → Status: 🟢 (conectado)
   → Campo de mensagem disponível
   → Botão "Enviar ➤" visível

4. ⚠️ Observação: Não encontrei formulário de login
   Este parece ser um chat direto, sem autenticação na UI.

💡 Quer que eu teste enviar uma mensagem?
```

### Exemplo 2: Interação Completa
```
Usuário: "Envie a mensagem 'teste' e veja a resposta"

Skill:
1. ✍️ Digitando "teste" no campo de mensagem...
   ✅ Campo preenchido

2. 🖱️ Clicando em "Enviar ➤"...
   ✅ Botão clicado

3. ⏳ Aguardando resposta do backend...
   ✅ Resposta recebida em 1.2s

4. 📊 Verificando resultado...
   ✅ Mensagem apareceu na tela
   ✅ Resposta do Claude recebida
   ✅ Sem erros no console

5. 💾 Registrando no Neo4j...
   → "Chat responde em ~1.2s"
   → "Funcionalidade de envio OK"

✅ Teste completado com sucesso!
```

## Páginas do Hello Agent (localhost:3000)

### Estrutura de URLs
```
http://localhost:3000/html/
├── index.html           # Chat principal (RAG Agent)
├── index_projects.html  # Lista de sessões/projetos
├── output.html          # Arquivos gerados pela sessão
├── audit_dashboard.html # Dashboard de tool calls
└── session-viewer.html  # Visualizador de sessão específica
```

### Elementos Comuns por Página

**index.html (Chat)**:
- `textbox "Digite sua mensagem..."` - Campo de entrada
- `button "Enviar ➤"` - Enviar mensagem
- `button "✨ Novo Chat"` - Nova sessão
- `StaticText "🟢"` - Status conexão (🟢=ok, ⚫=offline)
- `link "📄 Outputs"` - Ir para outputs

**index_projects.html (Projetos)**:
- `link "⟲ Chat"` - Voltar ao chat
- `heading "🗂️ [projeto]"` - Grupo de sessões
- `StaticText "✨ Atual"` - Sessão ativa
- `button "🗑️"` - Deletar sessão

**output.html (Outputs)**:
- `link "← Voltar ao Chat"` - Voltar
- `button "Atualizar"` - Refresh lista
- Lista de arquivos com Download/Excluir

**audit_dashboard.html (Audit)**:
- Cards: Total chamadas, Erros, Latência, Tools
- Gráfico de chamadas por tool
- Tabela com histórico de tool calls

## Limitações

- **Chrome apenas**: Usa Chrome DevTools MCP
- **Localhost preferível**: Melhor para apps locais
- **JavaScript necessário**: SPAs funcionam melhor
- **Sem multi-tab complexo**: Foco em fluxo linear

## Troubleshooting

### "Hook não está funcionando"
- Verificar settings.local.json
- Confirmar que hook está habilitado
- Testar manualmente a validação

### "Neo4j não retorna contexto"
- Verificar conexão: cypher-shell -u neo4j -p password
- Popular dados de teste
- Usar queries mais específicas

### "Elementos não são encontrados"
- Tirar snapshot verbose: take_snapshot(verbose=true)
- Aguardar carregamento completo
- Verificar se página usa shadow DOM

## Próximas Melhorias

- [ ] Suporte a múltiplas tabs simultâneas
- [ ] Gravação de sessões de teste
- [ ] Geração automática de scripts de teste
- [ ] Comparação visual com screenshots de referência
- [ ] Relatórios de teste estruturados

---

## Modo 2: Validação RAG 🧪

### Quando Usar
Valida a suite de testes do RAG Agent (test_all.py) no projeto hello-agent.

**Comandos que ativam este modo**:
- "Valide os testes RAG"
- "Execute test_all.py"
- "Verifique documentos.db"
- "Rode os testes do RAG Agent"
- "Teste o sistema RAG"

### Funcionamento

1. **Pré-validação**: Verifica test_all.py e documentos.db existem
2. **Execução**: Roda test_all.py (6 módulos de teste)
3. **Parse**: Analisa output procurando [OK], [FAIL], [WARN]
4. **Armazenamento**: Salva resultado no Turso KvStore
5. **Report**: Apresenta status detalhado ao usuário

### Módulos Testados

- **Imports**: Dependências (apsw, sqlite-vec, fastembed, mcp)
- **Database**: Banco documentos.db e embeddings
- **FastEmbed**: Modelo BAAI/bge-small-en-v1.5 (384D)
- **Search**: Busca semântica com similarity scores
- **MCP Server**: Ferramentas search_documents, get_document, etc
- **Config**: RAG_AGENT_OPTIONS e configuração

### Exemplo de Uso

```
Usuário: "Valide os testes RAG"

Skill:
🔍 Iniciando validação RAG...

✅ Pré-validação OK
  - test_all.py encontrado
  - documentos.db acessível (11 docs)

🧪 Executando suite de testes...
  [1/6] imports ✓
  [2/6] database ✓
  [3/6] fastembed ✓
  [4/6] search ✓
  [5/6] mcp_server ✓
  [6/6] config ✓

✅ VALIDAÇÃO COMPLETA: 6/6 PASS

📊 Detalhes:
  • Banco: 11 docs, 11 embeddings
  • Modelo: BAAI/bge-small-en-v1.5 (384D)
  • MCP Tools: search_documents, get_document, list_sources, count_documents
  • Top search: "Politica_Uso_IA.docx" (87% similarity)

💾 Resultado salvo no Turso: rag_validation:1703350800

💡 Sistema 100% operacional! Pronto para responder consultas RAG.
```

### Quando Falhas Ocorrem

Se testes falharem, o sistema:
1. Identifica módulos com falha
2. Classifica tipo de erro
3. **Automaticamente** ativa Modo 3 (Refatoração)
4. Tenta corrigir até 3 vezes

---

## Modo 3: Refatoração Automática 🔧

### Quando Usar

Ativado **automaticamente** quando Modo 2 detecta falhas, ou via comandos manuais:

- "Refatore automaticamente"
- "Corrija os testes RAG"
- "Aplique ruff --fix"
- "Tente corrigir automaticamente"

### Funcionamento

1. **Análise**: Identifica testes falhando e classifica erros
2. **Estratégia**: Escolhe abordagem (ruff fix, import, syntax)
3. **Aplicação**: Executa `ruff check --fix` no código
4. **Re-validação**: Roda test_all.py novamente
5. **Loop**: Repete até passar ou max 3 tentativas

### Tipos de Erro Suportados

| Tipo | Auto-fix? | Estratégia |
|------|-----------|------------|
| ImportError | ✅ Sim | ruff check --select I --fix |
| SyntaxError | ✅ Sim | ruff format + ruff check --fix |
| AttributeError | ⚠️ Parcial | ruff check --fix |
| AssertionError | ❌ Não | Requer intervenção manual |
| FileNotFoundError | ❌ Não | Requer intervenção manual |

### Limitações

- **Apenas erros sintáticos/formatação**: Não corrige lógica complexa
- **Max 3 tentativas**: Evita loops infinitos
- **Não instala pacotes**: pip install requer confirmação manual
- **Não modifica testes**: Apenas código fonte (mcp_server, core/*)

### Exemplo de Uso

```
Usuário: "Valide e corrija se necessário"

Skill:
🔍 Validando RAG...

❌ FALHAS DETECTADAS: 2/6

📋 Testes falhando:
  ❌ imports - ModuleNotFoundError: No module named 'mcp'
  ❌ config - AttributeError: 'Options' object has no attribute 'model'

🔧 REFATORAÇÃO AUTOMÁTICA ATIVADA

━━━ TENTATIVA 1/3 ━━━

🔍 Análise:
  → imports: Dependency 'mcp' não instalada
  → config: Typo em nome de atributo

🛠️ Aplicando correções...
  ✓ ruff check --fix config.py
  ✓ 1 arquivo corrigido: config.py

🧪 Re-validando...
  ✅ config: PASS agora!
  ❌ imports: ainda falhando (precisa instalar)

━━━ TENTATIVA 2/3 ━━━

💡 Estratégia: Erro requer pip install mcp

⚠️ AÇÃO MANUAL NECESSÁRIA:
   O erro "ModuleNotFoundError: No module named 'mcp'" requer:
   → pip install mcp

   Deseja que eu execute? [s/N]
```

### Quando Desiste

Refatoração automática para quando:
- Atingiu max 3 tentativas
- Erro requer intervenção manual (logic, files)
- Nenhum arquivo foi modificado pelo ruff
- Situação piorou após tentativa

Nestes casos, reporta ao usuário e sugere próximos passos.

---

## Integração Turso + Neo4j

### Turso (KvStore)

Armazena resultados de validação para histórico:

```python
# Estrutura salva
{
  "key": "rag_validation:1703350800",
  "value": {
    "status": "success",
    "passed": 6,
    "total": 6,
    "tests": {
      "teste_de_imports": "pass",
      "teste_de_banco_de_dados": "pass",
      ...
    },
    "timestamp": 1703350800
  }
}
```

### Neo4j (Grafo)

Registra sessões de refatoração para análise histórica:

```cypher
(RAGAgent)-[:HAD_SESSION]->(RefactoringSession {
  timestamp: 1703350800,
  attempts: 2,
  success: true,
  files_modified: ["config.py"],
  errors_fixed: ["AttributeError"]
})
```

---

## Comandos Completos (Todos os Modos)

### Modo 1: Navegação Web
- "Abra localhost:3000"
- "Clique em [elemento]"
- "Digite [texto]"
- "Tire um screenshot"

### Modo 2: Validação RAG
- "Valide os testes RAG"
- "Execute test_all.py"
- "Verifique documentos.db"
- "Histórico de validações" (consulta Turso)

### Modo 3: Refatoração
- "Refatore automaticamente" (ou ativação automática)
- "Corrija os testes falhando"
- "Aplique ruff --fix"

---

## Como Ativar

Esta skill tem 3 modos operacionais ativados automaticamente:

### Modo 1: Navegação Web (padrão)
**Triggers**: "abra", "navegue", "clique", "teste [site]"

### Modo 2: Validação RAG (NOVO)
**Triggers**: "valide", "teste rag", "test_all", "documentos.db"

### Modo 3: Refatoração (NOVO)
**Triggers**: Automático (quando Modo 2 falha) ou "refatore", "corrija"

**Não use** esta skill para:
- Leitura de código fonte
- Manipulação de arquivos locais
- Tarefas que não envolvem browser ou testes RAG
