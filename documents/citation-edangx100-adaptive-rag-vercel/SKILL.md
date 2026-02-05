---
name: citation
description: Formats citations and validates source attribution for answers generated from multiple document sources (ChromaDB and web search). Use when adding source references to generated answers, validating citation accuracy, or ensuring quality of source attribution across different source types.
---

# Citation and Source Attribution

## Instructions

Format citations and validate source attribution using functions in `components/generator.py`. Handles both internal knowledge base (ChromaDB) sources and external web search sources with appropriate citation formats.

**Default workflow:**

```python
# After generating answer, format citations based on source type
citations = format_citations(documents)
validated = validate_citations(answer, documents)
```

**Key capabilities:**

1. **Multi-source citation formatting** - Handle both ChromaDB and web search sources
2. **Source type detection** - Automatically detect document source type
3. **Quality validation** - Verify citations match provided documents
4. **Unified output format** - Consistent citation structure regardless of source

## Source Types and Citation Formats

### ChromaDB Sources

Documents from internal knowledge base (catalog, faq, troubleshooting collections):

**Document structure:**
```python
{
    'document': 'product_id: SKU001 | name: TechBook Pro...',
    'collection': 'catalog',  # 'faq' or 'troubleshooting'
    'metadata': {
        'source': 'techmart_catalog.csv',
        'row_index': 0
    }
}
```

**Citation format:**
- "Based on our product catalog..."
- "According to our FAQ..."
- "From our troubleshooting guide..."
- Sources: `["techmart_catalog.csv", "techmart_faq.csv"]`
- Collections: `["catalog", "faq"]`

### Web Search Sources

Documents from external web search (Exa API):

**Document structure:**
```python
{
    'document': '<web page content>',
    'collection': 'web_search',
    'source': 'https://techradar.com/article',  # URL
    'title': 'Best Gaming Laptops 2024',
    'author': 'John Doe',
    'published_date': '2024-03-15'
}
```

**Citation format:**
- Markdown hyperlinks: `[Title](URL)`
- Include publication date when available
- Sources: `["https://techradar.com/article", "https://pcmag.com/review"]`
- Collections: `["web_search"]`

## Examples

### Example 1: ChromaDB citations only

```python
# Input documents
documents = [
    {'collection': 'catalog', 'metadata': {'source': 'techmart_catalog.csv'}},
    {'collection': 'faq', 'metadata': {'source': 'techmart_faq.csv'}}
]

# Output
{
    'sources': ['techmart_catalog.csv', 'techmart_faq.csv'],
    'collections_used': ['catalog', 'faq'],
    'source_types': ['chromadb', 'chromadb'],
    'citation_format': 'internal_kb'
}
```

### Example 2: Web search citations only

```python
# Input documents
documents = [
    {
        'collection': 'web_search',
        'source': 'https://techradar.com/best-laptops',
        'title': 'Best Gaming Laptops 2024'
    },
    {
        'collection': 'web_search',
        'source': 'https://pcmag.com/laptop-review',
        'title': 'Gaming Laptop Reviews'
    }
]

# Output
{
    'sources': [
        'https://techradar.com/best-laptops',
        'https://pcmag.com/laptop-review'
    ],
    'collections_used': ['web_search'],
    'source_types': ['web', 'web'],
    'citation_format': 'web_urls',
    'formatted_citations': [
        '[Best Gaming Laptops 2024](https://techradar.com/best-laptops)',
        '[Gaming Laptop Reviews](https://pcmag.com/laptop-review)'
    ]
}
```

### Example 3: Mixed sources (ChromaDB + Web)

```python
# Input documents
documents = [
    {'collection': 'catalog', 'metadata': {'source': 'techmart_catalog.csv'}},
    {
        'collection': 'web_search',
        'source': 'https://example.com/article',
        'title': 'External Review'
    }
]

# Output
{
    'sources': [
        'techmart_catalog.csv',
        'https://example.com/article'
    ],
    'collections_used': ['catalog', 'web_search'],
    'source_types': ['chromadb', 'web'],
    'citation_format': 'mixed',
    'formatted_citations': [
        'Product Catalog',
        '[External Review](https://example.com/article)'
    ]
}
```

### Example 4: Citation validation

```python
# Validate that generated answer only uses information from provided documents
answer = "The TechBook Pro costs $1,499"
documents = [
    {'document': 'product_id: SKU001 | price: 1499.0 | name: TechBook Pro'}
]

validation = validate_citations(answer, documents)
# Returns: {'valid': True, 'grounded': True, 'hallucination_detected': False}
```

## Usage in Generator Agent

The citation skill is used AFTER generation to format and validate sources:

```python
# Step 1: Generate answer (generation_skill)
answer_result = generate_answer(query, documents)

# Step 2: Format citations (citation_skill)
citation_result = format_citations(documents)

# Step 3: Combine results
final_result = {
    'answer': answer_result['answer'],
    'sources': citation_result['sources'],
    'collections_used': citation_result['collections_used'],
    'source_types': citation_result['source_types'],
    'formatted_citations': citation_result.get('formatted_citations', [])
}
```

## Quality Checks

The citation skill performs these quality validations:

1. **Source completeness** - All documents have valid source information
2. **Format consistency** - Citations follow correct format for source type
3. **URL validation** - Web URLs are properly formed
4. **Collection verification** - Collection names are valid
5. **No hallucination** - Answer content is grounded in provided documents

## Critical Implementation Notes

- **Source type detection**: Check `collection == 'web_search'` to identify web sources
- **Unique sources**: Deduplicate sources list (multiple docs from same CSV/URL)
- **Empty documents**: Handle gracefully when no documents provided
- **Metadata extraction**: Safely handle missing metadata fields (author, published_date)
- **Markdown formatting**: Web citations use `[Title](URL)` format for proper rendering
