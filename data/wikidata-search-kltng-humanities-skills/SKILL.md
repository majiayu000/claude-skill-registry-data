---
name: wikidata-search
description: Search for items and properties on Wikidata and retrieve external identifiers. Use when an agent needs to (1) search for Wikidata items by label or alias, (2) get entity details including labels, descriptions, aliases, (3) retrieve external identifiers (authority control IDs) for an entity, (4) look up properties or claims for items. Triggers on queries mentioning Wikidata, Q-IDs, P-IDs, authority control, external identifiers, or structured knowledge base lookups.
---

# Wikidata Search Skill

Search and retrieve data from Wikidata, the free knowledge base.

## API Endpoint

Base URL: `https://www.wikidata.org/w/api.php`

## Core Functions

### 1. Search Items (wbsearchentities)

Search for entities by label or alias.

```bash
curl 'https://www.wikidata.org/w/api.php?action=wbsearchentities&search=QUERY&language=en&format=json&type=item&limit=10'
```

Parameters:
- `search`: Search term (required)
- `language`: Language code (default: en)
- `type`: `item` (Q-entities) or `property` (P-entities)
- `limit`: Max results (1-50, default: 7)
- `continue`: Offset for pagination

Response fields per result:
- `id`: Entity ID (e.g., Q42)
- `label`: Primary label
- `description`: Short description
- `aliases`: Alternative names
- `url`: Wikidata page URL

### 2. Get Entity Details (wbgetentities)

Retrieve full entity data including claims/identifiers.

```bash
curl 'https://www.wikidata.org/w/api.php?action=wbgetentities&ids=Q42&format=json&props=labels|descriptions|aliases|claims'
```

Parameters:
- `ids`: Pipe-separated entity IDs (max 50)
- `props`: `labels|descriptions|aliases|claims|sitelinks|info`
- `languages`: Filter languages (e.g., `en|fr|de`)

### 3. Get Claims Only (wbgetclaims)

Retrieve claims for specific entity/property.

```bash
curl 'https://www.wikidata.org/w/api.php?action=wbgetclaims&entity=Q42&property=P31&format=json'
```

## Extracting External Identifiers

External identifiers are stored as claims with datatype `external-id`. Common identifier properties:

| Property | Name                   | Example                |
| -------- | ---------------------- | ---------------------- |
| P214     | VIAF ID                | 75121530               |
| P227     | GND ID                 | 119033364              |
| P244     | Library of Congress ID | n79023811              |
| P213     | ISNI                   | 0000 0001 2144 9326    |
| P345     | IMDb ID                | nm0001354              |
| P646     | Freebase ID            | /m/0282x               |
| P349     | NDL ID                 | 00621256               |
| P268     | BnF ID                 | 11888092r              |
| P269     | IdRef ID               | 026927608              |
| P906     | SELIBR ID              | 182099                 |
| P396     | SBN author ID          | IT\\ICCU\\CFIV\\000163 |

To extract identifiers from `wbgetentities` response:
```python
# claims = response['entities']['Q42']['claims']
# For each property P:
#   claims[P][0]['mainsnak']['datavalue']['value'] -> identifier string
```

## Python Script Usage

Use `scripts/wikidata_api.py` for programmatic access:

```python
from scripts.wikidata_api import WikidataAPI

wd = WikidataAPI()

# Search for items
results = wd.search("Albert Einstein", language="en", limit=5)

# Get entity with identifiers
entity = wd.get_entity("Q937", props=["labels", "descriptions", "claims"])

# Get external identifiers only
identifiers = wd.get_identifiers("Q937")
# Returns: {'P214': '75121530', 'P227': '118529579', ...}
```

## Response Handling

### Search Response Structure
```json
{
  "searchinfo": {"search": "query"},
  "search": [
    {
      "id": "Q42",
      "label": "Douglas Adams",
      "description": "English writer and humorist",
      "aliases": ["Douglas Noël Adams"],
      "url": "//www.wikidata.org/wiki/Q42"
    }
  ]
}
```

### Entity Response Structure
```json
{
  "entities": {
    "Q42": {
      "type": "item",
      "id": "Q42",
      "labels": {"en": {"language": "en", "value": "Douglas Adams"}},
      "descriptions": {"en": {"language": "en", "value": "..."}},
      "claims": {
        "P31": [...],  // instance of
        "P214": [{"mainsnak": {"datavalue": {"value": "113230702"}}}]  // VIAF
      }
    }
  }
}
```

## Best Practices

1. **Rate limiting**: Add 500ms-1s delay between requests
2. **Batch requests**: Use pipe-separated IDs (max 50 per request)
3. **Set User-Agent**: Include contact info in headers
4. **Filter props**: Request only needed properties to reduce payload
5. **Handle missing data**: Not all entities have all properties
