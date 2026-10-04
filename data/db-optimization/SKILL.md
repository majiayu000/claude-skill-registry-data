---
name: db-optimization
description: Otimizacao de banco de dados, caching, queries, indices. Usar automaticamente quando trabalhar com Supabase, Postgres, Firebase, ou quando performance de queries for relevante.
---

# Otimizacao de Banco de Dados -- Padrao DME

## Stacks de DB na DME

| Servico | Quando usar |
|---------|-------------|
| Supabase (Postgres) | Maioria dos projetos web, RLS, auth integrado |
| Firebase Firestore | Mobile-first, real-time sync |
| Postgres direto | Backend pesado, queries complexas |

## Checklist de performance

- Indices em colunas filtradas e ordenadas
- EXPLAIN ANALYZE em queries lentas
- Paginacao com cursor (nao offset) pra datasets grandes
- Connection pooling (Supabase ja faz)
- Evitar N+1 queries (usar JOIN ou batch)
- Cache de queries frequentes e estaticas

## Supabase RLS (obrigatorio)

```sql
-- Usuarios so veem seus proprios dados
CREATE POLICY "users_own_data" ON profiles
  FOR ALL USING (auth.uid() = user_id);
```

## Indices essenciais

```sql
-- Sempre criar indices pra foreign keys
CREATE INDEX idx_orders_user_id ON orders(user_id);
-- Indice composto pra queries frequentes
CREATE INDEX idx_orders_status_date ON orders(status, created_at DESC);
```

## Migracoes seguras

- Sempre testar migracoes em staging antes de prod
- Nunca DROP TABLE sem backup
- Adicionar colunas como nullable primeiro, depois preencher, depois NOT NULL
