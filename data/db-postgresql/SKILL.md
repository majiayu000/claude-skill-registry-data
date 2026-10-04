---
name: "db-postgresql"
description: "Fornece padrões de administração e engenharia para PostgreSQL baseizados na documentação oficial (postgresql.org/docs). Cobre arquitetura MVCC, tunagem de Autovacuum, tipos avançados (JSONB, PostGIS), estratégia de índices (B-Tree, GIN, GiST, BRIN), análise EXPLAIN ANALYZE BUFFERS, replicação e PgBouncer."
---

# Habilidade de IA: Engenharia e Administração de PostgreSQL (db-postgresql)

Esta skill orienta a inteligência artificial a atuar como especialista no banco de dados **PostgreSQL**, fundamentada rigorosamente na documentação oficial da PostgreSQL Global Development Group ([postgresql.org/docs](https://www.postgresql.org/docs/)). Cobre modelagem avançada, controle de concorrência MVCC, tuning de memória e disco, estratégias de indexação e alta disponibilidade.

---

## 🧭 Arquitetura e Controle de Concorrência (MVCC)

### 1. Multi-Version Concurrency Control (MVCC) e Autovacuum
- **Visibilidade de Tuplas**: O PostgreSQL cria versões de linhas (*tuples*) para leituras não bloqueantes.
- **Tunagem do Autovacuum**:
  - Configure o Autovacuum para evitar o inchaço de tabelas (*bloat*) e o congelamento de IDs de transação (*transaction ID wraparound*):
  ```ini
  # postgresql.conf
  autovacuum = on
  autovacuum_vacuum_scale_factor = 0.05
  autovacuum_analyze_scale_factor = 0.02
  autovacuum_max_workers = 4
  autovacuum_vacuum_cost_limit = 1000
  ```
  - Em tabelas com alto volume de gravação/atualização, ajuste parâmetros individualmente via `ALTER TABLE tbl SET (autovacuum_vacuum_scale_factor = 0.01);`.

### 2. Dimensionamento de Memória (`postgresql.conf`)
- `shared_buffers`: 25% a 40% da RAM total do sistema dedicada ao cache de páginas.
- `work_mem`: Memória atribuída por operação de ordenação ou hash join por nó de consulta. Defina com cautela para evitar consumo excessivo de RAM sob concorrência.
- `maintenance_work_mem`: Memória alocada para `VACUUM`, `CREATE INDEX` e `ALTER TABLE`.
- `effective_cache_size`: Estimativa da memória disponível para cache do sistema operacional (ajuda o query planner a decidir entre index scan e seq scan).

---

## 🛠️ Estratégias de Indexação e Tipos Avançados

### 1. Tipos de Índices
- **B-Tree**: Tipo padrão. Utilize clausulas `INCLUDE` para coberturas de índice (*Index Only Scan*).
- **GIN (Generalized Inverted Index)**: Essencial para colunas `JSONB`, busca em texto completo (*Full-Text Search*) e tipos `array`.
- **GiST (Generalized Search Tree)**: Ideal para dados geográficos (PostGIS) e tipos de intervalo (*range types*).
- **BRIN (Block Range Index)**: Alta performance e pegada de memória mínima para tabelas gigantes ordenadas por tempo (ex: logs, telemetria).

### 2. JSONB e Consultas Semiestruturadas
- Prefira `JSONB` sobre `JSON` devido ao pre-parsing e suporte a índices GIN:
```sql
CREATE TABLE app_events (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    payload jsonb NOT NULL,
    created_at timestamptz DEFAULT clock_timestamp()
);

-- Criando índice GIN no campo JSONB
CREATE INDEX idx_events_payload_gin ON app_events USING gin (payload);

-- Consulta otimizada usando operador de contenção (@>)
SELECT * FROM app_events WHERE payload @> '{"event_type": "user_signup"}';
```

---

## 🔍 Otimização de Consultas com EXPLAIN

Para diagnosticar gargalos de desempenho, utilize sempre o comando com suporte a contadores de buffer:

```sql
EXPLAIN (ANALYZE, BUFFERS, VERBOSE)
SELECT u.id, u.email, o.total_amount
FROM users u
JOIN orders o ON u.id = o.user_id
WHERE u.created_at >= '2026-01-01' AND o.status = 'COMPLETED';
```
- **Alertas de Atenção**:
  - `Sequential Scan` em tabelas com milhões de linhas (falta de índice apropriado).
  - `Sort Method: external merge Disk` (indica necessidade de aumentar `work_mem`).
  - `Loops` elevados em `Nested Loop Join` (avaliar substituição por `Hash Join` ou adicionar índice na chave estrangeira).

---

## ⚙️ Alta Disponibilidade e Connection Pooling

- **PgBouncer**: Proxy de alto desempenho para pooling de conexões (modo `transaction`).
- **Replicação**:
  - **Streaming Replication**: Replicação física de nível de bloco para standby de leitura e failover.
  - **Logical Replication**: Replicação seletiva de tabelas/publicações para integração de microsserviços.
- **Ferramentas de Failover**: Patroni (com etcd/consul) para alta disponibilidade com failover automático do nó líder.

---

## 🔒 Hardening e Conformidade de Segurança (OWASP ASVS & CIS PostgreSQL Benchmark)

- **Criptografia em Trânsito**: Force conexões cifradas TLS 1.3/1.2 (`ssl = on`, `ssl_min_protocol_version = 'TLSv1.2'`).
- **Controle de Acesso Estrito (`pg_hba.conf`)**: Proíba autenticação `trust` ou `md5`; exija `scram-sha-256` para todas as conexões remotas.
- **Princípio do Menor Privilégio e Row Level Security (RLS)**:
  - Nunca execute aplicações como superusuário `postgres`.
  - Habilite RLS para isolamento de dados multitenant (`ALTER TABLE tbl ENABLE ROW LEVEL SECURITY;`).
- **Auditoria (`pgaudit`)**: Habilite a extensão `pgaudit` para registrar operações DDL e modificações de tabelas sensíveis sem sobrecarregar o log de sistema.

---

## 🔗 Integração com Outras Skills

- Para integrar PostgreSQL em aplicações backend, consulte [backend-developer](../../roles/backend-developer/SKILL.md) e [lang-python](../../languages/lang-python/SKILL.md).
- Para diretrizes gerais de administração de bancos de dados, consulte [dba-database-administrator](../../roles/dba-database-administrator/SKILL.md).
- Para validação de requisitos de segurança em bancos de dados (V8/V14), consulte [appsec-owasp-asvs](../../security/appsec/appsec-owasp-asvs/SKILL.md), [cis-controls](../../security/grc-compliance/cis-controls/SKILL.md) e [security-privacy](../../security/grc-compliance/security-privacy/SKILL.md).
