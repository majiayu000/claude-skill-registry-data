---
name: database-audit
description: Auditoria e análise de bancos de dados para identificar anomalias, inconsistências, registros órfãos, duplicatas, índices faltantes, e problemas de integridade referencial. Usar para diagnosticar problemas de dados, preparar migrações, gerar relatórios de qualidade de dados, identificar foreign keys quebradas, e otimizar estrutura de tabelas.
---

# Database Audit

Skill para auditoria completa de bancos de dados MySQL/PostgreSQL.

## Categorias de Auditoria

1. **Integridade Referencial** - FKs órfãs, relacionamentos quebrados
2. **Qualidade de Dados** - Duplicatas, NULLs indevidos, formatos inválidos
3. **Performance** - Índices faltantes, queries lentas
4. **Estrutura** - Normalização, tipos de dados inadequados

## Queries de Diagnóstico

### 1. Registros Órfãos (Foreign Keys Quebradas)

```sql
-- Template genérico para encontrar órfãos
SELECT child.*
FROM child_table child
LEFT JOIN parent_table parent ON child.parent_id = parent.id
WHERE parent.id IS NULL
  AND child.parent_id IS NOT NULL;

-- Exemplo: Contratos sem cliente
SELECT c.id, c.client_id, c.created_at
FROM contracts c
LEFT JOIN clients cl ON c.client_id = cl.id
WHERE cl.id IS NULL
  AND c.client_id IS NOT NULL;

-- Gerar relatório de todas as FKs órfãs
-- Ver script: scripts/find-orphans.sql
```

### 2. Duplicatas

```sql
-- Encontrar duplicatas por campo(s)
SELECT 
    email,
    COUNT(*) as total,
    GROUP_CONCAT(id) as ids
FROM users
GROUP BY email
HAVING COUNT(*) > 1
ORDER BY total DESC;

-- Duplicatas com critério de priorização (manter mais recente)
WITH duplicates AS (
    SELECT 
        id,
        email,
        ROW_NUMBER() OVER (
            PARTITION BY email 
            ORDER BY updated_at DESC, id DESC
        ) as rn
    FROM users
    WHERE email IS NOT NULL
)
SELECT * FROM duplicates WHERE rn > 1;

-- Duplicatas compostas (nome + documento)
SELECT 
    nome, documento,
    COUNT(*) as total,
    GROUP_CONCAT(id ORDER BY created_at) as ids
FROM fornecedores
GROUP BY nome, documento
HAVING COUNT(*) > 1;
```

### 3. Dados Inconsistentes

```sql
-- Valores negativos onde não deveriam existir
SELECT id, valor 
FROM pagamentos 
WHERE valor < 0;

-- Datas inválidas ou fora de range
SELECT id, data_evento
FROM contratos
WHERE data_evento < '2000-01-01'
   OR data_evento > DATE_ADD(NOW(), INTERVAL 5 YEAR);

-- Status inválidos
SELECT id, status, COUNT(*) as total
FROM contratos
WHERE status NOT IN ('pending', 'active', 'completed', 'cancelled')
GROUP BY status;

-- Emails inválidos
SELECT id, email
FROM users
WHERE email NOT REGEXP '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$';

-- CPF/CNPJ inválidos (tamanho)
SELECT id, documento
FROM clientes
WHERE LENGTH(REGEXP_REPLACE(documento, '[^0-9]', '')) NOT IN (11, 14);
```

### 4. Análise de NULLs

```sql
-- Porcentagem de NULLs por coluna
SELECT 
    'contracts' as tabela,
    COUNT(*) as total_registros,
    SUM(CASE WHEN client_id IS NULL THEN 1 ELSE 0 END) as client_id_nulls,
    SUM(CASE WHEN value IS NULL THEN 1 ELSE 0 END) as value_nulls,
    SUM(CASE WHEN status IS NULL THEN 1 ELSE 0 END) as status_nulls,
    ROUND(SUM(CASE WHEN client_id IS NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as pct_client_null
FROM contracts;

-- Registros com campos obrigatórios vazios
SELECT id, created_at
FROM contracts
WHERE client_id IS NULL
   OR value IS NULL
   OR event_date IS NULL;
```

### 5. Índices Faltantes

```sql
-- MySQL: Colunas usadas em WHERE/JOIN sem índice
-- Identificar manualmente após EXPLAIN de queries lentas

-- Listar índices existentes
SHOW INDEX FROM contracts;

-- Sugestões comuns:
-- - Colunas de FK sempre indexadas
-- - Colunas usadas em WHERE frequentemente
-- - Colunas usadas em ORDER BY
-- - Colunas de status + data (índice composto)

-- Criar índice sugerido
CREATE INDEX idx_contracts_status_date ON contracts(status, event_date);
CREATE INDEX idx_contracts_client ON contracts(client_id);
```

### 6. Análise de Tabelas

```sql
-- MySQL: Estatísticas de tabelas
SELECT 
    table_name,
    table_rows as linhas_estimadas,
    ROUND(data_length / 1024 / 1024, 2) as dados_mb,
    ROUND(index_length / 1024 / 1024, 2) as indices_mb,
    ROUND((data_length + index_length) / 1024 / 1024, 2) as total_mb
FROM information_schema.tables
WHERE table_schema = DATABASE()
ORDER BY (data_length + index_length) DESC;

-- Colunas sem uso aparente (análise manual)
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_schema = DATABASE()
  AND table_name = 'contracts';
```

### 7. Relatório de Integridade

```sql
-- Script consolidado de auditoria
-- Executa todas as verificações e gera relatório

-- 1. Contagem total por tabela
SELECT 'clients' as tabela, COUNT(*) as total FROM clients
UNION ALL
SELECT 'contracts', COUNT(*) FROM contracts
UNION ALL
SELECT 'payments', COUNT(*) FROM payments;

-- 2. Órfãos por relacionamento
SELECT 
    'contracts_sem_client' as problema,
    COUNT(*) as total
FROM contracts c
LEFT JOIN clients cl ON c.client_id = cl.id
WHERE cl.id IS NULL AND c.client_id IS NOT NULL

UNION ALL

SELECT 
    'payments_sem_contract',
    COUNT(*)
FROM payments p
LEFT JOIN contracts c ON p.contract_id = c.id
WHERE c.id IS NULL AND p.contract_id IS NOT NULL;
```

## Workflow de Auditoria

```
1. Executar análise de estrutura (tabelas, colunas, índices)
2. Identificar relacionamentos e FKs
3. Verificar integridade referencial
4. Buscar duplicatas em campos únicos
5. Validar formatos e ranges de dados
6. Analisar distribuição de NULLs
7. Gerar relatório consolidado
8. Propor correções priorizadas
```

## Output: Relatório de Auditoria

```markdown
# Relatório de Auditoria - [DATABASE]
Data: YYYY-MM-DD

## Resumo Executivo
- Total de tabelas analisadas: X
- Problemas críticos: Y
- Problemas moderados: Z

## Integridade Referencial
| Relacionamento | Órfãos | Ação Sugerida |
|----------------|--------|---------------|
| contracts.client_id → clients.id | 15 | Investigar/Remover |

## Duplicatas
| Tabela | Campo | Duplicatas | IDs Afetados |
|--------|-------|------------|--------------|
| users | email | 23 | 101,102,... |

## Dados Inconsistentes
| Tabela | Problema | Registros | Query |
|--------|----------|-----------|-------|
| payments | Valores negativos | 5 | SELECT... |

## Recomendações
1. [CRÍTICO] Resolver órfãos em contracts
2. [ALTO] Adicionar índice em contracts.status
3. [MÉDIO] Limpar duplicatas de email
```

## Scripts Disponíveis

- `scripts/full-audit.sql` - Auditoria completa
- `scripts/find-orphans.sql` - Busca órfãos automaticamente
- `scripts/find-duplicates.sql` - Busca duplicatas
- `scripts/generate-report.php` - Gera relatório em Markdown
