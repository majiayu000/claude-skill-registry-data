---
name: isolamento-de-banco-de-dados-com-rls
description: Implementa isolamento logico de dados por tenant em PostgreSQL compartilhado usando politicas declarativas de Row-Level Security.
---
# isolamento-de-banco-de-dados-com-rls

## Descrição
A skill `isolamento-de-banco-de-dados-com-rls` implementa o isolamento lógico e rigoroso dos dados de múltiplos inquilinos (tenants) que compartilham as mesmas tabelas físicas do PostgreSQL. Ela usa políticas declarativas de Row-Level Security (RLS) para garantir que cada usuário ou organização visualize e modifique exclusivamente os próprios dados, sem exigir schemas separados por tenant e sem sacrificar a performance transacional.

## Quando usar
Gatilhos concretos e observáveis:
- A equipe modela ou modifica tabelas relacionais compartilhadas em ambiente SaaS (ex: `manuscritos`, `notas`, `entidades`).
- Ocorre a revisão de segurança ou auditoria de isolamento de dados da plataforma.
- Um novo microsserviço ou endpoint que acessa o banco compartilhado é implementado.

Quando NÃO usar:
- Para dados proprietários de internos de sistema (ex: tabelas de logs técnicos sem PII de usuários).
- Em ambientes de desenvolvimento local mono-tenant (onde o overhead de RLS é desnecessário).

## Pré-requisitos
- PostgreSQL versão 14 ou superior.
- ORM configurado para usar conexões parametrizadas (prepared statements) sem reuso indevido de plano de execução entre tenants.
- Middleware de autenticação capaz de injetar o `tenant_id` em cada transação de banco.

## Processo (passo a passo executável)
1. **Adição da Chave de Tenant (Tenant Key):**
   - Adicionar a coluna `tenant_id UUID NOT NULL` em todas as tabelas de dados de usuário.
   - Configurar o índice composto como chave primária:
     ```sql
     ALTER TABLE manuscritos ADD COLUMN tenant_id UUID NOT NULL;
     CREATE UNIQUE INDEX idx_manuscritos_tenant ON manuscritos (tenant_id, id);
     ```
2. **Ativação do RLS:**
   - Habilitar o mecanismo de filtragem em nível de linha da tabela:
     ```sql
     ALTER TABLE manuscritos ENABLE ROW LEVEL SECURITY;
     ALTER TABLE manuscritos FORCE ROW LEVEL SECURITY;
     ```
3. **Criação de Políticas Declarativas:**
   - Criar as políticas de leitura e escrita baseadas na variável de sessão local:
     ```sql
     CREATE POLICY tenant_isolation_select ON manuscritos
       FOR SELECT USING (tenant_id = current_setting('app.current_tenant_id', true)::UUID);

     CREATE POLICY tenant_isolation_insert ON manuscritos
       FOR INSERT WITH CHECK (tenant_id = current_setting('app.current_tenant_id', true)::UUID);

     CREATE POLICY tenant_isolation_update ON manuscritos
       FOR UPDATE USING (tenant_id = current_setting('app.current_tenant_id', true)::UUID);
     ```
4. **Vinculação de Sessão por Requisição:**
   - No middleware do servidor (ex: gateway Node.js/FastAPI), ao iniciar cada transação, injetar a variável local de contexto:
     ```sql
     BEGIN;
     SET LOCAL app.current_tenant_id = 'uuid-do-tenant-autenticado';
     -- Executar queries normalmente
     COMMIT;
     ```
5. **Prevenção de Vazamento via Cache:**
   - Configurar o ORM para desativar o plano de execução compartilhado (shared prepared statement plan) entre sessões de tenants distintos para evitar que o PostgreSQL otimize e cache um plano baseado nos dados de outro inquilino.

## Parâmetros e configuração
- `TENANT_ID_COLUMN`: Nome padrão da coluna de identificador de inquilino. Padrão: `"tenant_id"`.
- `SESSION_TENANT_VAR`: Nome da variável de sessão local PostgreSQL que carrega o tenant ativo. Padrão: `"app.current_tenant_id"`.
- `RLS_BYPASS_ROLE`: Papel do PostgreSQL (role) autorizado a ignorar políticas RLS para operações de superusuário administrativo. Padrão: `"rls_admin"`.

## Armadilhas e como evitá-las
- **Armadilha:** Full Table Scans por Ausência de Índices: sem indexar a coluna `tenant_id`, o PostgreSQL executa varreduras completas da tabela física inteira em cada consulta que aplica o filtro RLS. Para uma tabela com 50 tenants e 1 milhão de linhas, isso eleva a latência de milissegundos para segundos.
  **Mitigação:** Indexar a chave de tenant de forma composta na chave primária da tabela imediatamente ao criar a coluna. A query EXPLAIN ANALYZE deve confirmar que todas as consultas sob RLS usam `Index Scan` e não `Seq Scan` em produção (RLS Policy Patterns, 2024).

## Critérios de validação (Definition of Done)
- [ ] O overhead de latência transacional adicionado pelo RLS é inferior a 10% do tempo de resposta base das queries sem RLS no ambiente de carga de produção.
- [ ] Nenhum tenant consegue ler, escrever ou deletar dados de outro tenant em 100% dos testes de penetração de isolamento.

## Fundamentação científica
- RLS Policy Patterns (2024) - PostgreSQL Row Level Security Best Practices - pgConf 2024
- HTAP for SaaS (2025) - Hybrid Transactional Analytical Processing in Multi-Tenant SaaS - VLDB 2025
- GDPR Multi-Tenant (2023) - GDPR Compliance Patterns in Multi-Tenant Cloud Applications - IEEE CLOUD 2023

## Requisitos do projeto relacionados
- RF-130 (banco de dados isolado)
- RF-129 (dados criptografados)

## Maturidade e riscos de adoção
**Nível:** Consolidada.
*O RLS do PostgreSQL é um mecanismo de produção maduro e amplamente utilizado por plataformas SaaS de grande escala, como Supabase.*

## Exemplos
**Operação correta (Tenant A lendo seus dados):**
```sql
SET LOCAL app.current_tenant_id = 'tenant-A-uuid';
SELECT * FROM manuscritos; -- Retorna apenas manuscritos do Tenant A
```
**Tentativa bloqueada (Tenant A tentando ler dados do Tenant B):**
```sql
SET LOCAL app.current_tenant_id = 'tenant-A-uuid';
SELECT * FROM manuscritos WHERE tenant_id = 'tenant-B-uuid'; -- Retorna 0 linhas (Bloqueado por RLS)
```
**Caso de falha conhecido:**
Query de administrador sem papel `rls_admin` vazar dados de todos os tenants por falta de `FORCE ROW LEVEL SECURITY` na tabela.
