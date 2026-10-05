---
name: specsfy-specialist-postgres
description: Modelar, consultar, migrar e operar PostgreSQL com integridade, índices, concorrência, segurança, performance e recuperação. Use para schemas, SQL, EXPLAIN, locks, isolation, migrations, roles, backup ou tuning em Postgres; não use para bancos diferentes sem confirmar semântica.
---

# PostgreSQL

## Fluxo

1. Descobrir versão, extensões, volume, crescimento, workload e owner dos dados.
2. Modelar invariantes com tipos, constraints, chaves e relações.
3. Escrever a consulta correta e medir o plano com dados representativos.
4. Selecionar índices pelo workload, não por colunas isoladas.
5. Analisar locks, duração da transação, isolation e concorrência.
6. Planejar migration, compatibilidade entre versões da aplicação e rollback.
7. Validar backup, restore, monitoramento e capacidade no ambiente alvo.

## Padrões

- Preferir constraints do banco para invariantes que sempre devem valer.
- Evitar `SELECT *`, tipos imprecisos e índices redundantes.
- Não adicionar índice sem ler escrita, tamanho, seletividade e plano.
- Manter transações curtas e ordem de locks consistente.
- Usar `EXPLAIN (ANALYZE, BUFFERS)` somente em ambiente seguro para executar a consulta.
- Aplicar expand/contract em mudanças incompatíveis ou de alto volume.
- Conceder o mínimo privilégio e separar papéis de migration, aplicação e leitura.

## Validação

- Testar integridade, concorrência e queries críticas.
- Comparar planos e métricas antes/depois com cardinalidade realista.
- Estimar lock e tempo de rewrite de DDL.
- Provar restore periodicamente; backup sem restore testado não basta.

Leia [references/standards.md](references/standards.md) para tipos, índices,
concorrência, segurança, migrations e operação.
