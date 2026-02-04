---
name: go-db-query
description: Skills for querying Gene Ontology annotation databases in DuckDB format. Use this for queries about GO annotations, genes, terms, evidence codes, or taxonomic relationships in GO-DB databases (db/*.ddb files). Particularly useful for hierarchical queries using closure tables to find genes annotated to terms and their descendants.
---

# GO-DB Query Skill

## Overview

This skill provides expertise for querying GO-DB DuckDB databases containing Gene Ontology (GO) annotations. GO-DB databases store annotations linking genes/proteins to GO terms, along with the full GO ontology structure. The key feature is the use of **closure tables** that enable efficient hierarchical queries across the ontology graph.

Use this skill when working with queries involving:
- Finding genes annotated to specific GO terms (including descendants)
- Analyzing evidence codes and annotation sources
- Exploring ontology hierarchies and term relationships
- Computing annotation statistics by taxon, evidence, or other dimensions
- Identifying unique or redundant annotations using ontological reasoning

## Core Concepts

### Closure Tables

Closure tables are the heart of GO-DB querying. They contain the **transitive closure** of ontological relationships:

- **isa_partof_closure**: Contains all is-a and part-of relationships, both direct and inferred
  - Example: If "protein kinase" is-a "kinase" and "kinase" is-a "catalytic activity", the table includes all three relationships plus the transitive "protein kinase" → "catalytic activity"

- **How to use**: Join annotations with closure tables to find all genes annotated to a term OR its descendants

```sql
-- Find all yeast kinases (including specific types like protein kinase)
SELECT DISTINCT a.db_object_symbol, a.db_object_id
FROM gaf_association a
INNER JOIN isa_partof_closure ipc ON a.ontology_class_ref = ipc.subject
WHERE ipc.object = 'GO:0016301'  -- kinase activity
  AND a.db_object_taxon LIKE '%559292%';  -- yeast
```

### Database Structure

Available databases are located in `db/*.ddb`:
- Organism-specific: `sgd.ddb` (yeast), `fb.ddb` (fly), `pombase.ddb` (fission yeast)
- Taxonomic groups: `mammal.ddb`, `fungi.ddb`, `plant.ddb`
- GOA databases: `goa_human.ddb`, `goa_uniprot_all.ddb`

## Query Patterns

### 1. Finding Genes by GO Term (with Closure)

The most common pattern: find all genes annotated to a term or its descendants.

**Pattern:**
```sql
SELECT DISTINCT
    a.db_object_symbol,
    a.ontology_class_ref,
    t.label AS term_label
FROM gaf_association a
INNER JOIN isa_partof_closure ipc ON a.ontology_class_ref = ipc.subject
INNER JOIN term_label t ON a.ontology_class_ref = t.id
WHERE ipc.object = '<GO_TERM_ID>'
  AND a.db_object_taxon LIKE '%<TAXON_ID>%';
```

**Why use closure:** Without the closure join, only direct annotations are found. The closure captures all annotations to descendant terms (e.g., "protein kinase", "lipid kinase" when searching for "kinase").

### 2. Counting and Grouping Annotations

Aggregate annotations by dimensions like evidence type, taxon, or assigned_by.

**Pattern:**
```sql
SELECT
    evidence_type,
    COUNT(*) AS annotation_count,
    COUNT(DISTINCT db_object_id) AS unique_genes
FROM gaf_association
WHERE <filters>
GROUP BY evidence_type
ORDER BY annotation_count DESC;
```

Combine with closure tables to count within ontology subtrees.

### 3. Finding Unique Contributions

Identify annotations that are not redundant with more specific annotations from other sources.

**Pattern:**
```sql
SELECT a.*
FROM gaf_association a
WHERE NOT EXISTS (
    SELECT 1
    FROM gaf_association a2
    INNER JOIN isa_partof_closure ipc ON a2.ontology_class_ref = ipc.subject
    WHERE a2.supporting_references != a.supporting_references
      AND ipc.object = a.ontology_class_ref  -- a2 is to a child term
      AND a2.db_object_id = a.db_object_id
);
```

**Logic:** An annotation is unique if no child-term annotation exists from a different source for the same gene.

### 4. Exploring Term Hierarchies

Navigate the ontology structure itself using edge and closure tables.

**Find direct children:**
```sql
SELECT DISTINCT e.subject, t.label
FROM edge e
INNER JOIN term_label t ON e.subject = t.id
WHERE e.object = '<GO_TERM_ID>'
  AND e.predicate = 'rdfs:subClassOf';
```

**Find all ancestors:**
```sql
SELECT DISTINCT ipc.object, t.label
FROM isa_partof_closure ipc
INNER JOIN term_label t ON ipc.object = t.id
WHERE ipc.subject = '<GO_TERM_ID>';
```

### 5. Genes Annotated to Multiple Terms

Find genes with annotations to both T1 and T2 (or their descendants).

**Pattern:**
```sql
SELECT DISTINCT a1.db_object_symbol, a1.db_object_id
FROM gaf_association a1
INNER JOIN isa_partof_closure ipc1 ON a1.ontology_class_ref = ipc1.subject
INNER JOIN gaf_association a2 ON a1.db_object_id = a2.db_object_id
INNER JOIN isa_partof_closure ipc2 ON a2.ontology_class_ref = ipc2.subject
WHERE ipc1.object = '<GO_TERM_1>'
  AND ipc2.object = '<GO_TERM_2>';
```

**Logic:** Self-join gaf_association on gene ID, then join each side with closure tables to check ancestry.

## Executing Queries

### Command Line Usage

```bash
# Query a specific database
duckdb db/sgd.ddb "SELECT COUNT(*) FROM gaf_association"

# Interactive mode
duckdb db/sgd.ddb
D SELECT * FROM term_label WHERE label LIKE '%kinase%' LIMIT 10;
D .quit

# Export results to CSV
duckdb db/goa_human.ddb "COPY (SELECT ...) TO 'results.csv' (HEADER, DELIMITER ',')"
```

### Finding the Right Database

- **Organism-specific queries**: Use organism database (e.g., `sgd.ddb` for yeast)
- **Cross-species analysis**: Use taxonomic group (e.g., `mammal.ddb`)
- **Human-focused**: Use `goa_human.ddb`
- **Comprehensive queries**: Use `goa_uniprot_all.ddb` (largest, >400M annotations)

Check available databases:
```bash
ls -lh db/*.ddb
```

## Key Tables Reference

### gaf_association
Main annotation table with columns:
- `db_object_symbol`, `db_object_id`: Gene identifier and symbol
- `ontology_class_ref`: GO term ID (e.g., "GO:0016301")
- `evidence_type`: Evidence code (e.g., "IEA", "IDA")
- `db_object_taxon`: NCBI taxon ID (e.g., "taxon:9606")
- `aspect`: GO aspect - "P" (process), "F" (function), "C" (component)
- `supporting_references`: Reference IDs
- `assigned_by`: Annotation source

### isa_partof_closure
Transitive closure table with columns:
- `subject`: Descendant term ID
- `predicate`: Relationship type
- `object`: Ancestor term ID

### term_label
Term ID to label mapping:
- `id`: GO term ID
- `label`: Human-readable label

### entailed_edge
All ontology relationships (including inferred):
- `subject`, `predicate`, `object`

For complete schema documentation, refer to `references/schema.md`.

## Query Workflow

When handling a query request:

1. **Understand the question**: Identify what data is being requested
2. **Determine if closure is needed**: Most queries benefit from closure tables to capture hierarchical relationships
3. **Find the GO term ID**: Use term_label to search by label if needed
4. **Select the right database**: Choose based on organism/scope
5. **Build the query**: Start with the appropriate pattern from `references/common_queries.md`
6. **Add filters**: Refine by taxon, evidence, date, etc.
7. **Execute and verify**: Run via `duckdb` and check results make sense
8. **Add labels for readability**: Join with term_label to show human-readable names

## Common Taxon IDs

- 9606: Human
- 10090: Mouse
- 559292: S. cerevisiae (yeast)
- 7227: D. melanogaster (fly)
- 284812: S. pombe (fission yeast)

## Common Evidence Codes

**Experimental**: IDA, IMP, IGI, IPI, IEP
**Computational**: IEA, ISS, ISO, ISA, ISM, IBA
**Curator/Author**: TAS, NAS, IC, ND

## Resources

### references/schema.md
Complete schema documentation including:
- Detailed table structures and column descriptions
- Ontology table relationships
- Closure table explanations
- Index information
- Database statistics

### references/common_queries.md
Comprehensive SQL examples for all query patterns:
- Pattern 1: Find genes by term (with closure)
- Pattern 2: Count/group annotations
- Pattern 3: Find unique/redundant annotations
- Pattern 4: Explore term hierarchies
- Pattern 5: Genes with multiple term annotations
- Pattern 6: Evidence analysis
- Pattern 7: Reference/citation analysis

Load these references when detailed examples or schema information is needed to construct queries.

## Tips

- **Start simple**: Begin with basic queries and add complexity incrementally
- **Use EXPLAIN**: Check query plans for complex queries
- **LIMIT during development**: Add LIMIT to test queries on large databases
- **Check indices**: Closure tables have indices on subject/object pairs for performance
- **Validate term IDs**: Verify GO term IDs exist in term_label before running queries
- **Consider performance**: Closure joins can be expensive on very large databases; filter early when possible
