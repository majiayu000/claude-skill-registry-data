---
name: "dba-database-administrator"
description: "Fornece padrões de engenharia de software e administração de bancos de dados (DBA) para sistemas SQL e NoSQL. Cobre modelagem de dados, estratégias de indexação, otimização de consultas (EXPLAIN), controle de concorrência (ACID/BASE), replicação, alta disponibilidade, backups (PITR), conexões TLS seguras por padrão e segurança em PostgreSQL, MariaDB, SQLite e MongoDB."
---

# Habilidade de IA: Administrador de Banco de Dados (DBA Specialist)

Esta skill orienta a inteligência artificial a atuar como **Administrador de Banco de Dados (DBA - Database Administrator)**, especializada no planejamento, provisionamento, otimização, segurança e manutenção contínua de bancos de dados **relacionais (SQL)** e **não-relacionais (NoSQL / Document-oriented)**. A skill adota as melhores práticas de engenharia de dados, cobrindo o ciclo de vida completo da informação em ambientes de produção.

---

## 🧭 Princípios Fundamentais e Arquitetura de Dados

### 1. Relacional (SQL) vs. Não-Relacional (NoSQL)
- **Sistemas Relacionais (RDBMS)**:
  - **Garantias ACID**: Atomicidade, Consistência, Isolamento e Durabilidade.
  - **Modelagem Normalizada (3NF)** para OLTP (redução de redundância e garantia de integridade referencial) e **Modelagem Dimensional (Star/Snowflake Schema)** para OLAP/Data Warehouse.
- **Sistemas Não-Relacionais (NoSQL)**:
  - **Teorema CAP & Modelo BASE**: *Basically Available, Soft-state, Eventual consistency*. Escolha pragmática entre Consistência (CP) e Disponibilidade (AP) sob partição de rede.
  - **Modelagem Orientada a Documentos / Chave-Valor**: Desnormalização consciente baseada nos padrões de acesso de leitura e escrita da aplicação.

### 2. Estratégias Globais de Indexação
- **B-Tree**: Índice padrão para pesquisas de igualdade e intervalos em dados ordenáveis.
- **Índices Compostos**: Ordem estrita de colunas baseada na seletividade (colunas de igualdade primeiro, seguidas por colunas de intervalo).
- **Índices Especiais**: GIN/GiST para busca textual e dados semiestruturados (JSON/JSONB), TTL para expiração automática de dados e parciais para filtrar subconjuntos frequentes.

### 3. Análise e Otimização de Consultas (Performance Tuning)
- Inspeção de planos de execução (`EXPLAIN` / `EXPLAIN ANALYZE`).
- Eliminação de varreduras completas (*Full Table Scans* / *Collection Scans*) em tabelas de grande porte.
- Dimensionamento adequado de memória para buffers de leitura, ordenação e cache de páginas.

### 4. Alta Disponibilidade, Replicação e Backup
- **Replicação**: Primário-Réplica (síncrona/assíncrona) para separação de leitura e failover.
- **Backup & Disaster Recovery**:
  - **Backup Lógico**: Exportação em scripts SQL/BSON (ex: `pg_dump`, `mariadb-dump`, `mongodump`).
  - **Backup Físico / PITR**: Captura de arquivos de dados com arquivamento contínuo de logs de transação (WAL/Binlog) para *Point-In-Time Recovery*.
- **Connection Pooling**: Mitigação do custo de criação de conexões usando proxies dedicados (ex: PgBouncer, MaxScale, Mongos).

---

## 🛠️ Subskills Especializadas por Banco de Dados

Para diretrizes de implementação técnica profunda, sintaxes e comandos de cada SGBD, consulte as subskills dedicadas:

| Banco de Dados | Tipo | Documentação Oficial de Referência | Skill Relacionada |
| :--- | :--- | :--- | :--- |
| **PostgreSQL** | Relacional (SQL) | [postgresql.org/docs](https://www.postgresql.org/docs/) | [db-postgresql](../../databases/db-postgresql/SKILL.md) |
| **MariaDB** | Relacional (SQL) | [mariadb.com/docs](https://mariadb.com/docs) | [db-mariadb](../../databases/db-mariadb/SKILL.md) |
| **SQLite** | Relacional Embedded | [sqlite.org/docs.html](https://sqlite.org/docs.html) | [db-sqlite](../../databases/db-sqlite/SKILL.md) |
| **MongoDB** | NoSQL (Documentos) | [mongodb.com/pt-br/docs](https://www.mongodb.com/pt-br/docs/) | [db-mongodb](../../databases/db-mongodb/SKILL.md) |

---

## 🧰 Checklist de Práticas de Segurança e Hardening (DBA)

1. **Princípio do Menor Privilégio (RBAC)**: Contas de aplicação devem possuir apenas os privilégios mínimos necessários (`SELECT`, `INSERT`, `UPDATE`, `DELETE`), proibindo o uso de superusuários (`postgres`, `root`).
2. **Criptografia em trânsito (Conexões seguras por padrão)**:
   - **Postura padrão**: toda conexão remota DEVE ser cifrada via TLS/SSL, com verificação de certificado do servidor. Em produção, recuse `disable`, `allow`, `prefer` e `require` "nu" (sem verificar o servidor).
   - **PostgreSQL (server)** — em `postgresql.conf`:
     - `ssl = on`
     - `ssl_min_protocol_version = 'TLSv1.2'` (mínimo; para política estrita usar somente `TLSv1.3` fixando min+max = `'TLSv1.3'`)
     - `ssl_tls13_ciphers = 'TLS_AES_256_GCM_SHA384:TLS_AES_128_GCM_SHA256:TLS_CHACHA20_POLY1305_SHA256'` (AEAD-only em TLS 1.3)
     - `ssl_key_file` com `chmod 0600`; `ssl_cert_file`; `ssl_ca_file` para verificação de client-cert
   - **PostgreSQL (hba)** — em `pg_hba.conf`, forçar TLS e rejeitar não-TLS:
     ```
     hostssl  all  all  0.0.0.0/0  scram-sha-256  clientcert=verify-ca
     hostnossl all  all  0.0.0.0/0  reject
     ```
   - **PostgreSQL (client / connection string)** — usar **`sslmode=verify-full`** + `sslrootcert=<CA>` (verifica cadeia + hostname). `require` apenas cifra, mas é vulnerável a MITM. Em aplicações Node.js (pg/Drizzle) e PgBouncer, force `verify-full`.
   - **Verificação de que a conexão está cifrada (Postgres)**:
     ```sql
     SELECT ssl, version, cipher FROM pg_stat_ssl WHERE pid = pg_backend_pid();  -- ssl=t => cifrada
     ```
   - **MariaDB/MySQL**: `tls_version = TLSv1.2,TLSv1.3`, conta com `REQUIRE SSL` via `GRANT ... REQUIRE SSL`, client com `--ssl-verify-server-cert` on.
   - **MongoDB**: servidor `--tlsMode requireSSL`; client `tls=true` + `tlsCAFile`; manter `tlsAllowInvalidCertificates=false` e `tlsAllowInvalidHostnames=false`.
   - **SQLite**: embarcado, sem listener de rede e **sem TLS próprio** — proteja o transporte do arquivo (compartilhamento criptografado) ou use **SQLCipher** (AES-256) para criptografia em repouso.
   - **Em repouso (*Encryption at Rest*)**: discos e volumes cifrados (AES-256) ou criptografia nativa de tabelas/coleções; senhas/hash sempre com algoritmos fortes (ex: `scram-sha-256`).
3. **Auditoria e Monitoramento**:
   - Habilitação de logs de consultas lentas (*Slow Query Log*) e auditoria de ações administrativas.
   - Monitoramento ativo de IOPS, taxa de cache hit, uso de CPU, saturação de conexões e lag de replicação.

---

## 🔗 Integração com Outras Skills

- Para integrar acesso a banco de dados em aplicações backend resilientes, consulte [backend-developer](../backend-developer/SKILL.md) e [clean-code-reusability](../../engineering-practices/clean-code-reusability/SKILL.md).
- Para provisionamento de infraestrutura de bancos de dados via IaC, Docker e Kubernetes, consulte [devops-engineer](../devops-engineer/SKILL.md) e [cloud-aws](../../cloud-infra/cloud-aws/SKILL.md).
- Para requisitos de conformidade de dados, retenção e privacidade (LGPD/GDPR), consulte [security-privacy](../../security/grc-compliance/security-privacy/SKILL.md) e [pci-dss-compliance](../../security/grc-compliance/pci-dss-compliance/SKILL.md).
