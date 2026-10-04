---
name: "db-mariadb"
description: "Fornece padrões de administração e engenharia para MariaDB baseados na documentação oficial (mariadb.com/docs). Cobre motores de armazenamento (InnoDB, Aria, ColumnStore, MyRocks), tunagem do InnoDB Buffer Pool, Galera Cluster, MariaDB MaxScale, Mariabackup e otimização EXPLAIN FORMAT=JSON."
---

# Habilidade de IA: Engenharia e Administração de MariaDB (db-mariadb)

Esta skill orienta a inteligência artificial a atuar como especialista no banco de dados **MariaDB**, fundamentada rigorosamente na documentação oficial da MariaDB Corporation e MariaDB Foundation ([mariadb.com/docs](https://mariadb.com/docs)). Cobre motores de armazenamento plugáveis, arquitetura Galera Cluster, otimização do InnoDB, backups físicos e alta disponibilidade com MaxScale.

---

## 🧭 Motores de Armazenamento Plugáveis (Storage Engines)

Ao contrário de outros SGBDs relacionais, o MariaDB permite escolher motores de armazenamento específicos por tabela:

- **InnoDB**: Motor padrão transacional OLTP com suporte a ACID, chave estrangeira e *row-level locking*.
- **Aria**: Motor padrão não-transacional otimizado para substituição do MyISAM e processamento de tabelas temporárias em disco.
- **ColumnStore**: Motor de armazenamento orientado a colunas projetado para processamento analítico (OLAP) de grande escala e Big Data.
- **MyRocks**: Motor baseado em RocksDB com estrutura LSM-Tree (*Log-Structured Merge-tree*) otimizado para alta taxa de gravação e compressão máxima de dados.
- **Spider**: Motor de estilhaçamento (*sharding*) transparente que conecta múltiplas instâncias remotas do MariaDB.

---

## 🛠️ Performance Tuning e Dimensionamento (`my.cnf`)

### 1. Memória e Buffer Pool (InnoDB)
```ini
[mysqld]
# Alocar de 50% a 70% da RAM em servidores dedicados a banco OLTP
innodb_buffer_pool_size = 16G
innodb_buffer_pool_instances = 16
innodb_log_file_size = 2G
innodb_flush_log_at_trx_commit = 1
innodb_file_per_table = 1

# Gerenciamento de conexões e threads
max_connections = 500
thread_handling = pool-of-threads
thread_pool_size = 16
```

### 2. Análise de Consultas e Planos de Execução
Utilize `EXPLAIN FORMAT=JSON` para inspecionar o custo relativo das suboperações e estatísticas do otimizador:

```sql
EXPLAIN FORMAT=JSON
SELECT c.name, COUNT(o.id) as total_orders
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
WHERE c.status = 'ACTIVE'
GROUP BY c.id;
```

---

## ⚙️ Alta Disponibilidade e Replicação

### 1. Galera Cluster (Multi-Master Síncrono)
- Replicação síncrona baseada em certificação para nós ativos.
- Garante perda de dados zero (*RPO = 0*) e failover instantâneo.
```ini
[mysqld]
# Configuração básica de nó Galera
wsrep_on = ON
wsrep_provider = /usr/lib/galera/libgalera_smm.so
wsrep_cluster_name = "production_galera_cluster"
wsrep_cluster_address = "gcomm://10.0.0.1,10.0.0.2,10.0.0.3"
wsrep_sst_method = mariabackup
```

### 2. MariaDB MaxScale
- Proxy inteligente de camada 7 para MariaDB.
- Oferece divisão automática de leitura e escrita (*Read/Write Split*), mascaramento de dados sensíveis e proteção contra ataques de negação de serviço (DoS) e SQL Injection.

### 3. Backups Físicos Online com Mariabackup
- Ferramenta nativa open source para cópia física não bloqueante de tabelas InnoDB e Aria:
```bash
# Executando backup físico completo sem bloquear gravações
mariabackup --backup --target-dir=/var/backups/mariadb/full --user=backup_user --password=secret

# Preparando o backup para restauração (consistência de logs)
mariabackup --prepare --target-dir=/var/backups/mariadb/full
```

---

## 🔒 Hardening e Conformidade de Segurança (OWASP ASVS & CIS MariaDB Benchmark)

- **Criptografia em Repouso e em Trânsito**:
  - Habilite criptografia nativa de tabelas InnoDB (`innodb_encrypt_tables = ON`, `innodb_encrypt_log = ON`).
  - Force conexões TLS 1.3 (`ssl = ON`, `require_secure_transport = ON`).
- **Autenticação Segura e Controle de Acesso**:
  - Remova usuários anônimos e bancos de teste (`mariadb-secure-installation`).
  - Utilize o plugin de autenticação `ed25519` ou `caching_sha2_password` para todas as contas de usuário.
- **Auditoria (`server_audit`)**: Habilite o plugin `server_audit` para auditoria de conexões, consultas DDL e acessos a dados sensíveis.

---

## 🔗 Integração com Outras Skills

- Para integrar MariaDB em ecossistemas de desenvolvimento backend, consulte [backend-developer](../../roles/backend-developer/SKILL.md).
- Para diretrizes gerais de administração de bancos de dados relacionais e NoSQL, consulte [dba-database-administrator](../../roles/dba-database-administrator/SKILL.md).
- Para validação de controles de segurança em bancos de dados (V8/V14), consulte [appsec-owasp-asvs](../../security/appsec/appsec-owasp-asvs/SKILL.md), [cis-controls](../../security/grc-compliance/cis-controls/SKILL.md) e [security-privacy](../../security/grc-compliance/security-privacy/SKILL.md).
