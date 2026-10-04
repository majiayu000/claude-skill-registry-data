---
name: tpl-dominio-filas-jobs
description: Template do pack (dominio/15-filas-jobs.md). Orienta o agente em regras de negocio e requisitos de produto alinhado a esse contexto.
metadata:
  version: 1.0.0
  source_template: dominio/15-filas-jobs.md
  generated_by: install_pack_templates_as_claude_skills
---

# DOMAIN: Sistema de Filas e Background Jobs

Skill gerado a partir do pack `templates-claude-code`. Arquivo de origem: `dominio/15-filas-jobs.md`. Use como baseline e adapte ao projeto antes de mudancas grandes.

## Conteudo do template

## CONTEXT
Filas quebram de formas difíceis de debugar: job nunca processado porque worker morreu
sem graceful shutdown, double processing porque job não é idempotente, fila crescendo
infinitamente porque erro não tratado gera retry loop. A infraestrutura de jobs é
tanto crítica quanto frequentemente ignorada em code review.

## STACK ASSUMPTIONS
- Queue: BullMQ (Redis, Node.js) / Sidekiq (Redis, Ruby) / Celery (Redis/RabbitMQ, Python)
- Cloud: SQS + Lambda / Cloud Tasks + Cloud Run para arquiteturas serverless
- Monitoring: Bull Board, Flower (Celery), Sidekiq Web UI, Grafana
- Storage: Redis (filas + state) + PostgreSQL (dead letter persistente)

## CORE CONCEPTS
- **Job**: unidade de trabalho com payload, retries e estratégia de backoff
- **Queue**: canal com prioridade e concorrência configurada por tipo de job
- **Worker**: processo que consome e processa jobs de uma ou mais filas
- **Idempotency**: processar o mesmo job duas vezes produz o mesmo resultado
- **Dead Letter Queue (DLQ)**: destino de jobs que falharam após N retentativas
- **Backoff**: espera crescente entre retentativas (linear ou exponencial)
- **Graceful Shutdown**: worker termina job atual antes de parar (não mata no meio)
- **Job Priority**: filas separadas por urgência (`critical`, `default`, `bulk`)

## ARCHITECTURE RULES

### Queue Design
```
critical   → concurrency: 5  | timeout: 30s  | retries: 3  | delay: 0
default    → concurrency: 20 | timeout: 60s  | retries: 5  | delay: backoff
bulk       → concurrency: 2  | timeout: 300s | retries: 10 | delay: backoff
scheduled  → concurrency: 3  | timeout: 120s | retries: 3  | delay: cron
```

### Job Idempotency Patterns
```javascript
// Pattern 1: Check-then-act com lock
async function processEmailJob(job: Job<{ userId: string; templateId: string }>) {
  const lockKey = `email:${job.data.userId}:${job.data.templateId}:${job.id}`;
  const acquired = await redis.set(lockKey, '1', 'NX', 'EX', 3600);
  if (!acquired) {
    logger.info({ jobId: job.id }, 'Job already processed, skipping');
    return; // outro worker já processou
  }
  await sendEmail(job.data);
}

// Pattern 2: Status no banco com upsert
async function processOrderJob(job: Job<{ orderId: string }>) {
  const order = await db.orders.findOne(job.data.orderId);
  if (order.status !== 'pending') return; // already processed
  await db.orders.update({ id: job.data.orderId, status: 'processing' });
  await fulfillOrder(order);
}
```

### Retry Strategy
```javascript
// BullMQ: configurar backoff exponencial
const queue = new Queue('emails', { defaultJobOptions: {
  attempts: 5,
  backoff: {
    type: 'exponential',
    delay: 1000  // 1s, 2s, 4s, 8s, 16s
  },
  removeOnComplete: { count: 1000 }, // manter últimos 1000 jobs completos
  removeOnFail: false  // manter falhos para análise → DLQ manual
}});
```

### Dead Letter Queue
```javascript
// Mover para DLQ após max retries
worker.on('failed', async (job, error) => {
  if (job.attemptsMade >= job.opts.attempts) {
    await db.deadLetterJobs.create({
      jobId: job.id,
      queue: job.queueName,
      payload: job.data,
      lastError: error.message,
      failedAt: new Date()
    });
    await alertOps('job_dead_lettered', { job: job.id, error: error.message });
  }
});
```

### Graceful Shutdown
```javascript
const worker = new Worker('jobs', processor, { connection });

process.on('SIGTERM', async () => {
  logger.info('Received SIGTERM, closing worker gracefully...');
  await worker.close(); // aguarda job atual terminar (até timeout)
  await redis.quit();
  process.exit(0);
});
```

### Long-running vs Short Jobs
- Jobs curtos (< 30s): processados diretamente pelo worker
- Jobs longos (30s-5min): progress reporting via job `updateProgress()`
- Jobs muito longos (> 5min): dividir em batches + child jobs (BullMQ job groups)
- Jobs com estado: armazenar progresso no banco, não só no job (recuperação após crash)

### Concurrency e Rate Limiting
```javascript
// Rate limit: máximo 100 chamadas/minuto para API externa
const limiter = new Bottleneck({ minTime: 600, maxConcurrent: 1 });
const worker = new Worker('api-sync', async (job) => {
  await limiter.schedule(() => callExternalApi(job.data));
});
```

## ROUTING TABLE
| Trigger | Action |
|---------|--------|
| Business event → queue.add() | Enfileirar job com payload + options |
| Worker: dequeue job | Processar → sucesso → remove | falha → retry com backoff |
| Job: max retries excedido | Mover para DLQ + alertar ops |
| SIGTERM ao worker | Graceful shutdown: aguardar job atual + fechar |
| Cron: scheduled job trigger | Verificar que não há outro instance rodando (distributed lock) |
| POST /admin/jobs/retry/:id | Re-enfileirar job da DLQ |
| POST /admin/jobs/retry-all | Re-enfileirar todos os jobs da DLQ de uma queue |
| GET /admin/jobs/dashboard | Bull Board / Sidekiq UI com stats em tempo real |
| GET /admin/jobs/dead-letter | Listar DLQ com filtros por queue e data |
| POST /admin/jobs/pause/:queue | Pausar processamento de uma queue (manutenção) |
| POST /admin/jobs/resume/:queue | Retomar processamento |
| GET /admin/jobs/health | Tamanho das filas + lag + taxa de erro + workers ativos |
| POST /admin/jobs/bulk-enqueue | Enfileirar batch de jobs para reprocessamento |

## CRITICAL RULES
1. Todo job DEVE ser idempotente — processado 2x não pode ter efeito colateral duplo
2. Graceful shutdown obrigatório — SIGTERM não pode matar job no meio da execução
3. DLQ com alertas — job morto sem notificação = dado silenciosamente perdido
4. Jobs longos: progress reporting + checkpoint no banco para recuperação após crash
5. Scheduled jobs: distributed lock para garantir single execution em múltiplos workers
6. Nunca enfileirar jobs dentro de transaction de banco (job pode processar antes do commit)
7. Separar filas por prioridade — bulk jobs não bloqueiam jobs críticos
8. Rate limiting em jobs que chamam APIs externas com limite
9. Job payload deve ser small e serializável — armazenar dados grandes no banco, payload com ID
10. Timeout por job configurado e menor que timeout do graceful shutdown

## COMMON PITFALLS

### ❌ Job não idempotente gera double processing
```javascript
// ERRADO: se job for processado 2x, cria 2 invoices
async function processInvoiceJob(job) {
  await createInvoice(job.data.orderId); // pode criar 2 se reprocessado
}

// CORRETO: verificar existência antes de criar
async function processInvoiceJob(job) {
  const exists = await db.invoices.findOne({ orderId: job.data.orderId });
  if (exists) return; // idempotente
  await createInvoice(job.data.orderId);
}
```

### ❌ Enfileirar dentro de transaction
```javascript
// ERRADO: job pode processar ANTES do commit — vê dados não existentes
await db.transaction(async (trx) => {
  const order = await trx.orders.create({ ... });
  await queue.add('process-order', { orderId: order.id }); // enfileirado aqui
  // se commit demorar, worker já processou e não encontrou o order
});

// CORRETO: enfileirar APÓS commit
const order = await db.orders.create({ ... });
await queue.add('process-order', { orderId: order.id }); // após commit
```

### ❌ Sem graceful shutdown
```javascript
// ERRADO: SIGTERM mata processo imediatamente — job fica em estado inconsistente
process.on('SIGTERM', () => process.exit(0));

// CORRETO: aguardar job atual completar
process.on('SIGTERM', async () => {
  logger.info('Graceful shutdown initiated');
  await worker.close(); // aguarda job atual (com timeout de 30s)
  process.exit(0);
});
```

### ❌ Payload enorme no job
```javascript
// ERRADO: 500KB de dados no payload → Redis fica saturado
await queue.add('send-report', { csvData: largeStringWith500KB });

// CORRETO: armazenar no S3/banco, passar apenas referência
const reportId = await db.reports.create({ data: largeData });
await queue.add('send-report', { reportId }); // payload tiny
```

## QUALITY GATES
- [ ] 100% dos jobs têm mecanismo de idempotência
- [ ] Graceful shutdown implementado em todos os workers
- [ ] DLQ configurada com alertas em produção
- [ ] Filas separadas por prioridade (critical/default/bulk)
- [ ] Jobs longos com progress reporting e checkpoint
- [ ] Scheduled jobs com distributed lock
- [ ] Enfileiramento sempre fora de transactions de banco
- [ ] Payload de jobs contém apenas IDs de referência (não dados grandes)
- [ ] Rate limiter em jobs que chamam APIs externas
- [ ] Dashboard de monitoramento de filas acessível ao time de ops

## FORBIDDEN
- Jobs sem mecanismo de idempotência (ausência = double processing em produção)
- SIGTERM handler que encerra processo sem await no job atual
- DLQ sem alertas (dados perdidos silenciosamente)
- Payload de job com objetos grandes (> 1KB) — usar referências por ID
- Enfileirar jobs dentro de transações de banco de dados
- Scheduled jobs sem distributed lock em deploy multi-instância
- Queue única para todos os tipos de jobs (bulk bloqueia crítico)
- Jobs sem timeout configurado (pode rodar indefinidamente)
