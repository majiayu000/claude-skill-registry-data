---
name: autosave-e-historico-de-versoes
description: Implementa autosave com debounce, versionamento por snapshots e restauração de versões anteriores usando diff-match-patch. Ativar ao implementar persistência do editor, histórico de edições (UC-124, UC-125) ou recuperação de dados em queda de conexão.
---

# autosave-e-historico-de-versoes

## Descrição
A skill `autosave-e-historico-de-versoes` define o mecanismo de persistência automática dos documentos do editor e o sistema de versionamento que permite ao escritor restaurar qualquer estado anterior do seu manuscrito. Ela usa debounce para evitar escrita excessiva no banco, snapshots periódicos completos para pontos de restauração e diffs compactos para armazenar o histórico entre snapshots sem duplicar conteúdo.

## Quando usar
Gatilhos concretos e observáveis:
- Implementação do autosave no `core_editor` (UC-004).
- Implementação do histórico de versões e restauração (UC-124, UC-125).
- Implementação do salvamento sem perda de progresso em queda de conexão (UC-414).

Quando NÃO usar:
- Para colaboração CRDT em tempo real (usar `concorrencia-editor-texto-rico-crdt`).
- Para backup em nuvem de toda a conta do usuário (escopo de infraestrutura).

## Pré-requisitos
- Biblioteca diff: `diff-match-patch` (Google) ou `fast-diff`.
- Tabela `document_versions`: `(id, document_id, version_number, snapshot_json, diff_patch, created_at, is_snapshot)`.
- Suporte a `IndexedDB` no frontend para buffer offline.

## Processo (passo a passo executável)
1. **Autosave com Debounce:**
   - A cada mudança no conteúdo do editor (`editor.on('update')`), disparar um timer debounced de `AUTOSAVE_DEBOUNCE_MS`.
   - Ao expirar o timer: serializar o documento (`editor.getJSON()`) e enviar para `PATCH /api/documents/:id` em background (sem bloquear a UI).
   - Em caso de falha de rede (offline), salvar o JSON no `IndexedDB` local e reenviar quando a conexão for restaurada.

2. **Buffer Offline (IndexedDB):**
   - Criar store `pending_saves` no IndexedDB com schema: `{ doc_id, content_json, timestamp }`.
   - Ao detectar que a conexão foi restaurada (`navigator.onLine = true`), processar a fila de `pending_saves` em ordem cronológica.
   - Exibir badge "Salvo localmente — aguardando conexão" na barra de status do editor durante modo offline.

3. **Snapshots Periódicos (Versionamento):**
   - A cada `SNAPSHOT_INTERVAL_MINUTES` minutos de edição ativa, ou ao fechar o documento, criar um snapshot completo no banco: `is_snapshot = true`, `snapshot_json = editor.getJSON()`.
   - Limitar o total de snapshots por documento a `MAX_SNAPSHOTS_PER_DOC` (remover os mais antigos).

4. **Diffs Entre Salvamentos:**
   - Entre snapshots, armazenar apenas o `diff_patch` (formato diff-match-patch) entre a versão anterior e a atual para compactar o histórico.

5. **Interface de Restauração:**
   - Painel "Histórico de versões" lista todas as versões com timestamp e pré-visualização do título da primeira linha.
   - Ao selecionar uma versão, exibir o conteúdo em modo de leitura somente com botão "Restaurar esta versão".
   - Ao restaurar, criar um novo snapshot da versão atual antes de sobrescrever (nunca perder o estado mais recente).

## Parâmetros e configuração
| Parâmetro | Descrição | Padrão |
|---|---|---|
| `AUTOSAVE_DEBOUNCE_MS` | Tempo de debounce antes de disparar o autosave | `2000` (2s) |
| `SNAPSHOT_INTERVAL_MINUTES` | Intervalo entre snapshots periódicos completos | `10` |
| `MAX_SNAPSHOTS_PER_DOC` | Número máximo de snapshots por documento | `50` |
| `OFFLINE_QUEUE_MAX_SIZE` | Número máximo de salvamentos no buffer offline | `100` |

## Armadilhas e como evitá-las
- **Armadilha:** Disparar uma chamada de API a cada tecla pressionada pelo usuário. Um escritor que digita 60 palavras por minuto geraria ~300 requisições por minuto, sobrecarregando o servidor e criando latência perceptível no editor.
  **Mitigação:** O debounce de `AUTOSAVE_DEBOUNCE_MS = 2000ms` garante que apenas uma requisição seja disparada após 2 segundos de pausa na digitação. Combinado com o buffer IndexedDB offline, isso garante zero perda de dados com carga mínima no servidor.

## Critérios de validação (Definition of Done)
- [ ] Nenhuma alteração feita pelo usuário é perdida após queda de conexão e posterior reconexão (testado com simulação de offline no DevTools).
- [ ] A interface de histórico lista todas as versões dos últimos 30 dias e permite restaurar qualquer uma em menos de 3 segundos.

## Exemplos
**Autosave bem-sucedido:**
Usuário para de digitar → após 2s debounce → `PATCH /api/documents/123` enviado silenciosamente → status bar exibe "Salvo às 14:32".

**Restauração de versão:**
Usuário abre "Histórico" → seleciona versão de ontem → pré-visualiza → clica "Restaurar" → sistema cria snapshot da versão atual → substitui conteúdo → status bar: "Versão de ontem restaurada. Desfazer disponível."
