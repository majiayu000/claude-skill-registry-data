---
name: polars
description: "Biblioteca DataFrame rápida (Apache Arrow). Selecione, filtre, group_by, joins, avaliação preguiçosa, I/O CSV/Parquet, expression API, para fluxos de trabalho de análise de dados de alto desempenho."
---

# Polars

## Visão Geral

Polars é uma biblioteca DataFrame extremamente rápida para Python e Rust construída no Apache Arrow. Trabalhe com a API baseada em expressões do Polars, framework de avaliação preguiçosa e capacidades de manipulação de dados de alto desempenho para processamento eficiente de dados, migração de pandas e otimização de pipeline de dados.

## Início Rápido

### Instalação e Uso Básico

Instale o Polars:
```python
uv pip install polars
```

Criação básica de DataFrame e operações:
```python
import polars as pl

# Criar DataFrame
df = pl.DataFrame({
    "name": ["Alice", "Bob", "Charlie"],
    "age": [25, 30, 35],
    "city": ["NY", "LA", "SF"]
})

# Selecionar colunas
df.select("name", "age")

# Filtrar linhas
df.filter(pl.col("age") > 25)

# Adicionar colunas computadas
df.with_columns(
    age_plus_10=pl.col("age") + 10
)
```

## Conceitos Principais

### Expressões

Expressões são os blocos de construção fundamentais das operações do Polars. Elas descrevem transformações nos dados e podem ser compostas, reutilizadas e otimizadas.

**Princípios-chave:**
- Use `pl.col("column_name")` para referenciar colunas
- Encadeie métodos para construir transformações complexas
- Expressões são preguiçosas e só executam dentro de contextos (select, with_columns, filter, group_by)

**Exemplo:**
```python
# Computação baseada em expressões
df.select(
    pl.col("name"),
    (pl.col("age") * 12).alias("age_in_months")
)
```

### Avaliação Preguiçosa vs Antecipada

**Antecipada (DataFrame):** Operações executam imediatamente
```python
df = pl.read_csv("file.csv")  # Lê imediatamente
result = df.filter(pl.col("age") > 25)  # Executa imediatamente
```

**Preguiçosa (LazyFrame):** Operações constroem um plano de consulta, otimizado antes da execução
```python
lf = pl.scan_csv("file.csv")  # Não lê ainda
result = lf.filter(pl.col("age") > 25).select("name", "age")
df = result.collect()  # Agora executa consulta otimizada
```

**Quando usar preguiçosa:**
- Trabalhar com datasets grandes
- Pipelines de consulta complexos
- Quando apenas algumas colunas/linhas são necessárias
- Desempenho é crítico

**Benefícios da avaliação preguiçosa:**
- Otimização automática de consultas
- Predicate pushdown
- Projection pushdown
- Execução paralela

Para conceitos detalhados, carregue `references/core_concepts.md`.

## Operações Comuns

### Select
Selecione e manipule colunas:
```python
# Selecionar colunas específicas
df.select("name", "age")

# Selecionar com expressões
df.select(
    pl.col("name"),
    (pl.col("age") * 2).alias("double_age")
)

# Selecionar todas as colunas que correspondem a um padrão
df.select(pl.col("^.*_id$"))
```

### Filter
Filtre linhas por condições:
```python
# Condição única
df.filter(pl.col("age") > 25)

# Múltiplas condições (mais limpo do que usar &)
df.filter(
    pl.col("age") > 25,
    pl.col("city") == "NY"
)

# Condições complexas
df.filter(
    (pl.col("age") > 25) | (pl.col("city") == "LA")
)
```

### With Columns
Adicione ou modifique colunas preservando as existentes:
```python
# Adicionar novas colunas
df.with_columns(
    age_plus_10=pl.col("age") + 10,
    name_upper=pl.col("name").str.to_uppercase()
)

# Computação paralela (todas as colunas computadas em paralelo)
df.with_columns(
    pl.col("value") * 10,
    pl.col("value") * 100,
)
```

### Group By e Agregações
Agrupe dados e calcule agregações:
```python
# Agrupamento básico
df.group_by("city").agg(
    pl.col("age").mean().alias("avg_age"),
    pl.len().alias("count")
)

# Múltiplas chaves de agrupamento
df.group_by("city", "department").agg(
    pl.col("salary").sum()
)

# Agregações condicionais
df.group_by("city").agg(
    (pl.col("age") > 30).sum().alias("over_30")
)
```

Para padrões detalhados de operações, carregue `references/operations.md`.

## Agregações e Funções de Janela

### Funções de Agregação
Agregações comuns dentro do contexto `group_by`:
- `pl.len()` - contar linhas
- `pl.col("x").sum()` - somar valores
- `pl.col("x").mean()` - média
- `pl.col("x").min()` / `pl.col("x").max()` - extremos
- `pl.first()` / `pl.last()` - primeiros/últimos valores

### Funções de Janela com `over()`
Aplique agregações preservando a contagem de linhas:
```python
# Adicionar estatísticas de grupo a cada linha
df.with_columns(
    avg_age_by_city=pl.col("age").mean().over("city"),
    rank_in_city=pl.col("salary").rank().over("city")
)

# Múltiplas colunas de agrupamento
df.with_columns(
    group_avg=pl.col("value").mean().over("category", "region")
)
```

**Estratégias de mapeamento:**
- `group_to_rows` (padrão): Preserva ordem de linha original
- `explode`: Mais rápido mas agrupa linhas juntas
- `join`: Cria colunas de lista

## Data I/O

### Formatos Suportados
Polars suporta leitura e escrita de:
- CSV, Parquet, JSON, Excel
- Bancos de dados (via conectores)
- Armazenamento em nuvem (S3, Azure, GCS)
- Google BigQuery
- Múltiplos/arquivos particionados

### Operações Comuns de I/O

**CSV:**
```python
# Antecipado
df = pl.read_csv("file.csv")
df.write_csv("output.csv")

# Preguiçoso (preferido para arquivos grandes)
lf = pl.scan_csv("file.csv")
result = lf.filter(...).select(...).collect()
```

**Parquet (recomendado para desempenho):**
```python
df = pl.read_parquet("file.parquet")
df.write_parquet("output.parquet")
```

**JSON:**
```python
df = pl.read_json("file.json")
df.write_json("output.json")
```

Para documentação abrangente de I/O, carregue `references/io_guide.md`.

## Transformações

### Joins
Combine DataFrames:
```python
# Inner join
df1.join(df2, on="id", how="inner")

# Left join
df1.join(df2, on="id", how="left")

# Join em nomes de colunas diferentes
df1.join(df2, left_on="user_id", right_on="id")
```

### Concatenação
Empilhe DataFrames:
```python
# Vertical (empilhar linhas)
pl.concat([df1, df2], how="vertical")

# Horizontal (adicionar colunas)
pl.concat([df1, df2], how="horizontal")

# Diagonal (união com schemas diferentes)
pl.concat([df1, df2], how="diagonal")
```

### Pivot e Unpivot
Reformate dados:
```python
# Pivot (formato amplo)
df.pivot(values="sales", index="date", columns="product")

# Unpivot (formato longo)
df.unpivot(index="id", on=["col1", "col2"])
```

Para exemplos detalhados de transformação, carregue `references/transformations.md`.

## Migração de Pandas

Polars oferece melhorias significativas de desempenho sobre pandas com uma API mais limpa. Principais diferenças:

### Diferenças Conceituais
- **Sem índice**: Polars usa apenas posições inteiras
- **Tipagem rigorosa**: Sem conversões de tipo silenciosas
- **Avaliação preguiçosa**: Disponível via LazyFrame
- **Paralelo por padrão**: Operações paralelizadas automaticamente

### Mapeamentos de Operações Comuns

| Operação | Pandas | Polars |
|-----------|--------|--------|
| Selecionar coluna | `df["col"]` | `df.select("col")` |
| Filtrar | `df[df["col"] > 10]` | `df.filter(pl.col("col") > 10)` |
| Adicionar coluna | `df.assign(x=...)` | `df.with_columns(x=...)` |
| Group by | `df.groupby("col").agg(...)` | `df.group_by("col").agg(...)` |
| Janela | `df.groupby("col").transform(...)` | `df.with_columns(...).over("col")` |

### Padrões de Sintaxe-Chave

**Pandas sequencial (lento):**
```python
df.assign(
    col_a=lambda df_: df_.value * 10,
    col_b=lambda df_: df_.value * 100
)
```

**Polars paralelo (rápido):**
```python
df.with_columns(
    col_a=pl.col("value") * 10,
    col_b=pl.col("value") * 100,
)
```

Para guia abrangente de migração, carregue `references/pandas_migration.md`.

## Melhores Práticas

### Otimização de Desempenho

1. **Use avaliação preguiçosa para datasets grandes:**
   ```python
   lf = pl.scan_csv("large.csv")  # Não use read_csv
   result = lf.filter(...).select(...).collect()
   ```

2. **Evite funções Python em caminhos críticos:**
   - Mantenha-se na expression API para paralelização
   - Use `.map_elements()` apenas quando necessário
   - Prefira operações nativas do Polars

3. **Use streaming para dados muito grandes:**
   ```python
   lf.collect(streaming=True)
   ```

4. **Selecione apenas colunas necessárias cedo:**
   ```python
   # Bom: Selecionar colunas cedo
   lf.select("col1", "col2").filter(...)

   # Ruim: Filtrar em todas as colunas primeiro
   lf.filter(...).select("col1", "col2")
   ```

5. **Use tipos de dados apropriados:**
   - Categorical para strings de baixa cardinalidade
   - Tamanhos inteiros apropriados (i32 vs i64)
   - Tipos de data para dados temporais

### Padrões de Expressão

**Operações condicionais:**
```python
pl.when(condition).then(value).otherwise(other_value)
```

**Operações de coluna em múltiplas colunas:**
```python
df.select(pl.col("^.*_value$") * 2)  # Padrão regex
```

**Manipulação de nulos:**
```python
pl.col("x").fill_null(0)
pl.col("x").is_null()
pl.col("x").drop_nulls()
```

Para melhores práticas e padrões adicionais, carregue `references/best_practices.md`.

## Recursos

Esta skill inclui documentação de referência abrangente:

### references/
- `core_concepts.md` - Explicações detalhadas de expressões, avaliação preguiçosa e sistema de tipos
- `operations.md` - Guia abrangente de todas as operações comuns com exemplos
- `pandas_migration.md` - Guia completo de migração de pandas para Polars
- `io_guide.md` - Operações de data I/O para todos os formatos suportados
- `transformations.md` - Joins, concatenação, pivots e operações de reformatação
- `best_practices.md` - Dicas de otimização de desempenho e padrões comuns

Carregue essas referências conforme necessário quando usuários precisarem de informações detalhadas sobre tópicos específicos.