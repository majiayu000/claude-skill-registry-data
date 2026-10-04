---
name: "db-sqlite"
description: "Fornece padrões de engenharia e otimização para SQLite baseados na documentação oficial (sqlite.org/docs.html). Cobre arquitetura Serverless, modo WAL (Write-Ahead Logging), pragmas de desempenho, índices cobridores e parciais, FTS5, JSON1 e extensão WITHOUT ROWID."
---

# Habilidade de IA: Engenharia e Otimização de SQLite (db-sqlite)

Esta skill orienta a inteligência artificial a atuar como especialista no banco de dados **SQLite**, fundamentada rigorosamente na documentação oficial ([sqlite.org/docs.html](https://sqlite.org/docs.html)). Cobre padrões de engenharia de software para bancos embarcados (*embedded*), tunagem de alta concorrência via WAL mode, pragmas de performance, índices parciais e tabelas `WITHOUT ROWID`.

---

## 🧭 Arquitetura Embarcada e Modo WAL (Write-Ahead Logging)

Ao contrário dos bancos cliente-servidor, o SQLite opera como um motor embarcado no mesmo processo da aplicação.

### 1. Configuração Recomendada de Concorrência e PRAGMAs
Por padrão, o SQLite opera em modo Rollback Journal (que bloqueia leituras durante gravações). Para habilitar leituras concorrentes com gravações, ative obrigatoriamente o modo **WAL**:

```sql
-- Ativar modo Write-Ahead Logging (persistido no arquivo da base)
PRAGMA journal_mode = WAL;

-- Sincronização segura para WAL (desempenho 10x superior sem perda de consistência)
PRAGMA synchronous = NORMAL;

-- Manter tabela temporária em memória RAM
PRAGMA temp_store = MEMORY;

-- Aumentar tamanho do cache de memória (ex: 64MB = 16000 páginas de 4KB)
PRAGMA cache_size = -64000;

-- Definir tempo limite de espera para evitar SQLITE_BUSY em escritas concorrentes
PRAGMA busy_timeout = 5000;

-- Habilitar verificação de chaves estrangeiras
PRAGMA foreign_keys = ON;
```

---

## 🛠️ Estratégias de Indexação e Modelagem de Alto Desempenho

### 1. Tabelas `WITHOUT ROWID`
- Para tabelas associativas (N:M) ou tabelas com Chave Primária natural composta ou alfanumérica (ex: UUID/TEXT), utilize a cláusula `WITHOUT ROWID` para economizar espaço de armazenamento e eliminar uma busca B-Tree dupla:
```sql
CREATE TABLE user_roles (
    user_id TEXT NOT NULL,
    role_id TEXT NOT NULL,
    assigned_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),
    PRIMARY KEY (user_id, role_id)
) WITHOUT ROWID;
```

### 2. Índices Parciais e Índices em Expressões
- **Índice Parcial**: Indexe apenas os registros relevantes da tabela:
```sql
CREATE INDEX idx_active_subscriptions 
ON subscriptions (user_id) 
WHERE status = 'ACTIVE';
```
- **Índice em Expressão**: Indexe o resultado de funções deterministicas ou dados extraídos de JSON:
```sql
CREATE INDEX idx_user_email_domain 
ON users (substr(email, instr(email, '@') + 1));
```

---

## 🔍 Busca Textual (FTS5) e Manipulação de JSON

### 1. Suporte Nativo a JSON
O SQLite possui suporte nativo a JSON (JSON1 extension habilitada por padrão):
```sql
CREATE TABLE user_settings (
    user_id INTEGER PRIMARY KEY,
    data TEXT CHECK (json_valid(data))
);

-- Extraindo valores formatados
SELECT json_extract(data, '$.theme') AS theme FROM user_settings;
```

### 2. Busca de Texto Completo (Full-Text Search - FTS5)
```sql
CREATE VIRTUAL TABLE documents_fts USING fts5(
    title,
    body,
    tokenize = 'porter ascii'
);

-- Consulta por frase ou prefixo com ordenação por relevância (bm25)
SELECT title, bm25(documents_fts) AS rank 
FROM documents_fts 
WHERE documents_fts MATCH 'sqlite AND performance*' 
ORDER BY rank;
```

---

## ⚙️ Diretrizes para Aplicação e Deploy

1. **Tratamento do erro `SQLITE_BUSY`**: Garanta que o driver SQLite da aplicação implemente o `busy_timeout` ou trate a exceção com retentativas e backoff exponencial.
2. **Backups Online Não-Bloqueantes**: Utilize a API nativa de backup do SQLite (`sqlite3_backup_init` ou o comando CLI `.backup`) em vez de copiar diretamente o arquivo `.db` enquanto a aplicação está em execução.

---

## 🔒 Hardening e Criptografia em Bancos Embarcados (OWASP MASVS & ASVS)

- **Criptografia em Repouso**: Em sistemas operacionais móveis ou desktop, adote **SEE (SQLite Encryption Extension)** ou **SQLCipher** (AES-256) para proteger arquivos `.db` contra exfiltração física ou engenharia reversa.
- **Proteção de Permissões no SO**: Restrinja as permissões do arquivo de banco de dados (`chmod 600`) para acesso exclusivo do processo proprietário da aplicação.
- **Mitigação de SQL Injection**: Obrigatoriamente utilize parâmetros vinculados (*prepared statements*) em vez de concatenação de strings em `sqlite3_exec`.

---

## 🔗 Integração com Outras Skills

- Para integrar SQLite em aplicações desktop, mobile ou embarcadas em Python/C/Rust, consulte [lang-python](../../languages/lang-python/SKILL.md), [lang-c](../../languages/lang-c/SKILL.md) e [lang-rust](../../languages/lang-rust/SKILL.md).
- Para diretrizes gerais de administração de bancos de dados relacionais, consulte [dba-database-administrator](../../roles/dba-database-administrator/SKILL.md).
- Para requisitos de segurança em armazenamento móvel e embarcado, consulte [appsec-owasp-masvs](../../security/appsec/appsec-owasp-masvs/SKILL.md) e [appsec-owasp-asvs](../../security/appsec/appsec-owasp-asvs/SKILL.md).
