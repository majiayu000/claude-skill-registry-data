---
name: portal-catalog-rag
description: Implement the semantic data catalog and its two-phase search (papers 02 and 05) — keyword MVP with ILIKE/tsvector, then hybrid RAG with pgvector + Gemini embeddings and Hit Rate@3 >= 0.8 evaluation. Use when touching /api/catalog/search, embeddings jobs, hybrid scoring, tribal notes, or the Corpus2Skill hierarchy for manuales/.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Portal Catalog RAG Skill (keyword → híbrida)

Catalog service: `! ls backend/app/services/catalog_service.py 2>/dev/null || echo "not created yet"`

## Rules — NON-NEGOTIABLE

- Dos fases con el MISMO contrato de respuesta (`CatalogHit`): MVP keyword (ILIKE/tsvector) y fase RAG híbrida; el frontend y el agente no notan la migración.
- Búsqueda híbrida = score combinado keyword + similitud coseno pgvector; NUNCA solo vectorial (los términos exactos de negocio deben seguir ganando).
- Embeddings con la API de Gemini sobre `business_name + definition + notas tribales` por campo del catálogo; dimensión fija `VECTOR(768)` (migración `enable_pgvector`, skill `portal-db-migrations`).
- Justificación explícita y documentada (paper 05): para corpus tabular homogéneo el retrieval PLANO supera a la jerarquía; la jerarquía navegable Corpus2Skill se aplica SOLO a `manuales/` y es STRETCH.
- Notas tribales SIEMPRE con condición de aplicabilidad (patrón Tk-Boost, paper 02): la nota se adjunta al hit solo si su condición aplica al contexto de la consulta.
- Evaluación obligatoria: set de 20 consultas de negocio con fuente esperada → **Hit Rate@3 >= 0.8** antes de dar por cerrada la fase híbrida.
- Endpoint protegido con JWT (cualquier rol autenticado); toda respuesta cita fuente (anti-alucinación del agente).

## Fase 1 — keyword MVP

```python
# backend/app/services/catalog_service.py
from sqlalchemy import text

KEYWORD_SQL = text("""
    SELECT f.id, f.business_name, f.definition, f.physical_name, s.name AS source,
           ts_rank(to_tsvector('spanish', f.business_name || ' ' || f.definition),
                   plainto_tsquery('spanish', :q)) AS kw_score
    FROM catalog_field f
    JOIN catalog_source s ON s.id = f.source_id
    WHERE to_tsvector('spanish', f.business_name || ' ' || f.definition)
          @@ plainto_tsquery('spanish', :q)
       OR f.business_name ILIKE '%' || :q || '%'
    ORDER BY kw_score DESC
    LIMIT :top_k
""")
```

## Fase 2 — score híbrido

```python
# backend/app/services/catalog_service.py
KW_WEIGHT, VEC_WEIGHT = 0.4, 0.6

async def hybrid_search(session, q: str, top_k: int = 10) -> list[CatalogHit]:
    """Combine tsvector keyword rank with pgvector cosine similarity."""
    q_emb = await embed_query(q)                       # Gemini embeddings API
    rows = await session.execute(text("""
        SELECT f.id, f.business_name, f.definition, f.physical_name, s.name AS source,
               coalesce(ts_rank(to_tsvector('spanish', f.business_name || ' ' || f.definition),
                                plainto_tsquery('spanish', :q)), 0) AS kw_score,
               1 - (f.embedding <=> CAST(:emb AS vector)) AS vec_score
        FROM catalog_field f JOIN catalog_source s ON s.id = f.source_id
        ORDER BY (:kw_w * coalesce(ts_rank(to_tsvector('spanish',
                    f.business_name || ' ' || f.definition),
                    plainto_tsquery('spanish', :q)), 0)
                  + :vec_w * (1 - (f.embedding <=> CAST(:emb AS vector)))) DESC
        LIMIT :top_k
    """), {"q": q, "emb": q_emb, "kw_w": KW_WEIGHT, "vec_w": VEC_WEIGHT, "top_k": top_k})
    return [await attach_tribal_notes(session, row, query=q) for row in rows]
```

## Job de embeddings del diccionario

```python
# ml/data/embed_catalog.py — batch job, run after seed or catalog edits
from google import genai

client = genai.Client(api_key=settings.GEMINI_API_KEY)

async def embed_field(field: CatalogField, notes: list[str]) -> list[float]:
    content = f"{field.business_name}. {field.definition}. " + " ".join(notes)
    result = client.models.embed_content(model="gemini-embedding-001",
                                         contents=content,
                                         config={"output_dimensionality": 768})
    return result.embeddings[0].values
```

## Notas tribales con aplicabilidad (Tk-Boost, paper 02)

```python
async def attach_tribal_notes(session, row, query: str) -> CatalogHit:
    """Attach only the notes whose applicability condition matches the query context."""
    notes = await session.execute(
        select(CatalogTribalNote).where(CatalogTribalNote.field_id == row.id))
    applicable = [n.note for n in notes.scalars()
                  if applies(n.applicability, query)]   # simple rule match in MVP
    return CatalogHit(business_name=row.business_name, definition=row.definition,
                      source=row.source, physical_name=row.physical_name,
                      tribal_notes=applicable,
                      score=KW_WEIGHT * row.kw_score + VEC_WEIGHT * row.vec_score)
```

## Evaluación Hit Rate@3 (gate de la fase híbrida)

```python
# tests/ml/test_hit_rate.py — 20 business queries with expected source
EVAL_SET = [
    ("saldo vencido de la cartera", "creditos"),
    ("cobertura de liquidez", "liquidez"),
    ("exposicion con contrapartes de swaps", "derivados"),
    # ... 20 total, curated with the team
]

async def test_hit_rate_at_3(client, any_role_token):
    hits = 0
    for query, expected_source in EVAL_SET:
        r = await client.get("/api/catalog/search", params={"q": query},
                             headers=any_role_token)
        top3 = [h["source"] for h in r.json()[:3]]
        hits += expected_source in top3
    assert hits / len(EVAL_SET) >= 0.8
```

## Fases y alcance

| Fase | Técnica | Estado |
|------|---------|--------|
| MVP | ILIKE + tsvector ranking | MUST, S2 |
| RAG plano | híbrida keyword + coseno pgvector | MUST, S3 |
| Jerarquía Corpus2Skill | resúmenes navegables SOLO para `manuales/` | STRETCH, no comprometido |
