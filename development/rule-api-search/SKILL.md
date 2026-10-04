---
name: rule-api-search
description: MANDATORY when editing files matching ["api/src/search/**/*.py"]. When working on OpenSearch integration in api/src/search/
---

# API Search (OpenSearch) Rules

## Index Configuration

ALWAYS centralize analyzer configuration in `DEFAULT_INDEX_ANALYSIS`. NEVER define custom analyzers per-index. ALWAYS use configurable shards and replicas via config objects.

Example from codebase:
```python
# From api/src/search/opensearch_config.py pattern
DEFAULT_INDEX_ANALYSIS = {
    "analysis": {
        "filter": {
            "snowball_filter": {"type": "snowball", "language": "English"}
        },
        "analyzer": {
            "default_analyzer": {
                "type": "custom",
                "tokenizer": "standard",
                "filter": ["lowercase", "snowball_filter"],
            }
        },
    }
}
```

## Query Building

ALWAYS use the `opensearch_query_builder` module for constructing search queries. NEVER build raw OpenSearch DSL dicts inline in service or route code. ALWAYS use structured filter, aggregation, and sort builders.

Example from codebase:
```python
# From api/src/search/opensearch_query_builder.py pattern
def build_opportunity_search_query(
    search_params: OpportunitySearchParams,
) -> dict:
    query = {
        "query": {
            "bool": {
                "must": _build_must_clauses(search_params),
                "filter": _build_filter_clauses(search_params),
            }
        },
        "sort": _build_sort(search_params.sort_by),
        "size": search_params.page_size,
        "from": search_params.page_offset,
    }
    return query
```

## Response Transformation

ALWAYS use typed `SearchResponse` objects for transforming OpenSearch responses. NEVER return raw OpenSearch response dicts to the service layer. ALWAYS map OpenSearch `_source` fields to domain model attributes.

Example from codebase:
```python
# From api/src/search/opensearch_response.py pattern
class SearchResponse:
    total_count: int
    records: list[dict]
    aggregations: dict

    @classmethod
    def from_opensearch_response(cls, response: dict) -> "SearchResponse":
        hits = response["hits"]
        return cls(
            total_count=hits["total"]["value"],
            records=[hit["_source"] for hit in hits["hits"]],
            aggregations=response.get("aggregations", {}),
        )
```

## Batch Indexing

ALWAYS use dedicated load tasks for bulk indexing operations (e.g., `load_opportunities`, `load_agencies`). NEVER index documents one-at-a-time in production code. ALWAYS use the OpenSearch bulk API for batch operations.

Example from codebase:
```python
# From api/src/search/backend/load_opportunities.py pattern
def load_opportunities_to_index(
    db_session: db.Session, search_client: OpensearchClient
) -> None:
    opportunities = get_all_opportunities(db_session)
    documents = [transform_opportunity_to_document(opp) for opp in opportunities]
    search_client.bulk_upsert(index_name, documents)
```

## Index Management

ALWAYS provide create and delete operations for index management. ALWAYS apply the centralized `DEFAULT_INDEX_ANALYSIS` settings when creating indexes. NEVER hard-code index names — use config-driven naming with optional namespace prefix.

## Query Explain

ALWAYS support the explain endpoint for query debugging. This allows developers to understand why specific results rank higher/lower.

## Count Optimization

ALWAYS use `count(DISTINCT(primary_key))` for record count queries rather than fetching all records. NEVER use `len(results)` for total count — use the OpenSearch `total` value from the response.

## Logging

ALWAYS begin every search module with `logger = logging.getLogger(__name__)`. ALWAYS log search queries and result counts for debugging. NEVER log full search result payloads (too verbose). NEVER log user search terms as PII.

---

## Context Enrichment

When generating significant search code (new index, query builder changes, new search endpoint), enrich your context:
- Call `get_architecture_section("api")` from the `simpler-grants-context` MCP server to understand search architecture
- Call `get_rule_detail("api-adapters")` for OpenSearch adapter patterns
- Call `get_rule_detail("api-routes")` for search endpoint patterns
- Call `get_rule_detail("api-services")` for service layer search integration
- Consult **Compound Knowledge** for indexed documentation on search patterns

## Related Rules

When working on search, also consult these related rules:
- **`api-adapters.mdc`** — OpenSearch client adapter in `adapters/search/`
- **`api-routes.mdc`** — search endpoint route handlers
- **`api-services.mdc`** — service functions that call search
- **`api-database.mdc`** — data models that feed search indexes
- **`cross-domain.mdc`** — structured logging conventions

## Specialist Validation

When generating or significantly modifying search code:

**For simple changes (< 20 lines, filter addition, sort update):**
No specialist invocation needed — the directives in this rule file are sufficient.

**For moderate changes (new query builder, response transformation update):**
Invoke `codebase-conventions-reviewer` to validate against project conventions.

**For complex changes (new index, analyzer changes, bulk indexing pipeline):**
Invoke the following specialists (run in parallel where possible):
- `performance-oracle` — validate query efficiency, index sizing, bulk operation performance
- `kieran-python-reviewer` — Python-specific quality review
