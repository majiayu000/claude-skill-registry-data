---
name: pipeline-de-notificacoes-em-tempo-real
description: Sistema de notificações push em tempo real via WebSockets para colaboração, menções (@usuario), alertas de mudanças em textos compartilhados e eventos do sistema. Ativar ao implementar colaboração em tempo real, menções (UC-133, UC-134) ou notificações do sistema (UC-229, UC-230).
---

# pipeline-de-notificacoes-em-tempo-real

## Descrição
A skill `pipeline-de-notificacoes-em-tempo-real` especifica a arquitetura de entrega de notificações push para usuários da plataforma via WebSocket (Socket.io) para eventos que exigem reação imediata (colaborador editando o mesmo documento, @menção em comentário) e via Server-Sent Events (SSE) para notificações menos urgentes (exportação pronta, lembrete de meta de escrita).

## Quando usar
Gatilhos concretos e observáveis:
- Implementação da colaboração em tempo real (UC-132, UC-133, UC-204).
- Implementação do sistema de notificações de usuário (UC-134, UC-229, UC-230).
- Implementação da entrega de resultados de jobs assíncronos (exportações, análise NLP).

Quando NÃO usar:
- Para o mecanismo de sincronização CRDT dos documentos compartilhados (ver `concorrencia-editor-texto-rico-crdt`).
- Para emails transacionais (usar serviço SMTP como SendGrid/SES).

## Pré-requisitos
- `socket.io` (servidor) + `socket.io-client` (cliente).
- Redis Pub/Sub para sincronização de mensagens entre múltiplas instâncias do servidor (horizontal scaling).
- Tabela `notifications` no banco: `(id, user_id, type, payload_json, read_at, created_at)`.

## Processo (passo a passo executável)
1. **Servidor WebSocket com Rooms por Documento:**
   - Ao conectar, o cliente autentica via Access Token JWT no handshake.
   - O servidor verifica o token e associa o socket ao `user_id`.
   - Ao abrir um documento, o cliente emite `join_document(doc_id)` → servidor adiciona o socket à room `doc:${doc_id}`.

2. **Eventos de Colaboração em Tempo Real:**
   - Cursor de colaborador: ao mover o cursor, emitir `cursor_move { user_id, position }` para a room do documento.
   - Ao outros clientes receber o evento, renderizar o cursor do colaborador com cor identificadora e tooltip com nome.

3. **Notificações de Menção (@usuario):**
   - Ao detectar `@username` no texto de um comentário (evento `comment_created`):
     - Resolver `@username` para `user_id` no banco.
     - Emitir evento `notification` diretamente para o socket do usuário mencionado na room `user:${user_id}`.
     - Persistir a notificação na tabela `notifications` para recuperação em sessões futuras.

4. **Fanout via Redis Pub/Sub (Multi-instância):**
   - Configurar `socket.io-redis` adapter para que eventos emitidos em um servidor sejam retransmitidos para todos os servidores do cluster via Redis.
   - Garantir que uma notificação gerada no servidor A seja entregue ao usuário conectado no servidor B.

5. **Notificações Não-Urgentes via SSE:**
   - Para eventos como "exportação pronta" ou "análise NLP concluída": usar SSE (`text/event-stream`) no endpoint `GET /api/notifications/stream`.
   - Manter a conexão SSE aberta e enviar `data: { type, payload }` ao completar o job.

## Parâmetros e configuração
| Parâmetro | Descrição | Padrão |
|---|---|---|
| `WS_AUTH_TIMEOUT_MS` | Tempo máximo para autenticar o handshake WebSocket | `5000` |
| `CURSOR_THROTTLE_MS` | Frequência mínima de envio de eventos de cursor | `100` |
| `NOTIFICATION_RETENTION_DAYS` | Dias para manter notificações lidas no banco | `30` |
| `SSE_HEARTBEAT_MS` | Intervalo de heartbeat SSE para manter conexão aberta | `30000` |

## Armadilhas e como evitá-las
- **Armadilha:** Escalar horizontalmente o servidor WebSocket sem um adapter Redis. Usuário A está conectado ao servidor 1 e usuário B ao servidor 2. A notificação gerada no servidor 1 nunca chega ao servidor 2, e o usuário B não recebe a menção.
  **Mitigação:** Configurar o `socket.io-redis` adapter desde o início, mesmo em desenvolvimento. O Redis pub/sub garante a entrega cruzada entre instâncias sem mudanças na lógica de emissão de eventos.

## Critérios de validação (Definition of Done)
- [ ] Uma @menção em um comentário é entregue ao usuário mencionado em menos de 500ms via WebSocket quando ele está online.
- [ ] Notificações geradas num servidor chegam a clientes conectados em outros servidores do cluster via Redis adapter.
- [ ] Notificações não lidas são recuperadas corretamente ao abrir a plataforma após período offline.

## Exemplos
**@menção em comentário:**
Maria comenta: "@joao Verificar esta cena" → servidor resolve `@joao` → emite `socket.to('user:joao-uuid').emit('notification', { type: 'mention', from: 'Maria', text: '...' })` → João vê badge de notificação no ícone de sino em tempo real.

**Cursor de colaborador:**
Maria e João editam o mesmo documento → João move cursor para parágrafo 5 → evento `cursor_move` emitido → Maria vê cursor azul "João" aparecer no parágrafo 5 do seu editor.
