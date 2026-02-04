---
name: classdiagram-to-neo4j
description: Extract entities, properties, and relationships from UML class diagrams (images) and populate Neo4j graph database. Supports TMF-style diagrams, schema diagrams, and other UML class diagrams. Uses vision models for extraction and generates Cypher queries for Neo4j population.
---

# Class Diagram to Neo4j Extraction Skill

## Overview

This skill extracts structured data from UML class diagrams (images) and populates Neo4j graph databases. It's designed for:
- TMF (TM Forum) API specification diagrams
- UML class diagrams
- Entity-relationship diagrams
- Schema diagrams

## Workflow

### 1. **Image Analysis**
   - Use vision models (GPT-4 Vision, Claude Vision, etc.) to analyze diagram images
   - Extract text, boxes, lines, and relationships
   - Identify entities, properties, and relationships

### 2. **Structured Extraction**
   - Parse entities (classes) with their properties
   - Extract relationships (associations, inheritance, etc.)
   - Capture cardinality and relationship metadata
   - Handle color coding and visual indicators

### 3. **Data Normalization**
   - Convert to structured format (YAML/JSON)
   - Normalize entity names and types
   - Standardize relationship types
   - Handle references and aliases

### 4. **Neo4j Population**
   - Generate Cypher queries
   - Create nodes with properties
   - Create relationships with metadata
   - Handle constraints and indexes

## Usage Patterns

### Pattern 1: Direct Image → Neo4j

```python
from classdiagram_to_neo4j import extract_and_populate

# Extract from image and populate Neo4j
extract_and_populate(
    image_path="diagrams/product_offering.png",
    neo4j_uri="bolt://localhost:7687",
    neo4j_user="neo4j",
    neo4j_password="password"
)
```

### Pattern 2: Extract → Review → Populate

```python
from classdiagram_to_neo4j import extract_diagram, populate_neo4j

# Step 1: Extract to JSON/YAML
data = extract_diagram(
    image_path="diagrams/product_offering.png",
    output_format="json",
    output_path="extracted.json"
)

# Step 2: Review/edit JSON if needed
# ... manual review ...

# Step 3: Populate Neo4j
populate_neo4j(
    data=data,
    neo4j_uri="bolt://localhost:7687",
    neo4j_user="neo4j",
    neo4j_password="password"
)
```

### Pattern 3: Batch Processing

```python
from classdiagram_to_neo4j import extract_diagram, populate_neo4j

# Process multiple diagrams
diagrams = [
    "diagrams/product_offering.png",
    "diagrams/category.png",
    "diagrams/pricing.png"
]

for diagram_path in diagrams:
    data = extract_diagram(diagram_path, output_format="json")
    populate_neo4j(
        data=data,
        neo4j_uri="bolt://localhost:7687",
        neo4j_user="neo4j",
        neo4j_password="password"
    )
```

## Diagram Types Supported

### TMF-Style Diagrams
- ProductOffering hub diagrams
- Category relationships
- Specification diagrams
- Reference entity diagrams

### UML Class Diagrams
- Classes with attributes
- Associations with multiplicities
- Inheritance hierarchies
- Aggregations and compositions

### Schema Diagrams
- Database schemas
- API schemas
- Domain models

## Extraction Process

### Step 1: Vision Analysis

The vision model analyzes the image and extracts:
- **Entities**: Boxes/classes with names
- **Properties**: Attributes within entities
- **Relationships**: Lines/arrows between entities
- **Metadata**: Cardinality, roles, types
- **Visual Indicators**: Colors, borders, dashed lines

### Step 2: Structured Output

Extracted data is normalized into:

```yaml
meta:
  source: "diagrams/product_offering.png"
  extracted_at: "2024-01-01T00:00:00Z"
  diagram_type: "uml_class"

entities:
  ProductOffering:
    label: "ProductOffering"
    properties:
      - name: "id"
        type: "string"
        required: true
      - name: "name"
        type: "string"
        required: true
      - name: "isBundle"
        type: "boolean"
        required: false

relationships:
  - from: "ProductOffering"
    to: "ProductSpecification"
    type: "has_specification"
    cardinality: "0..1"
    direction: "out"
    properties:
      role: null
```

### Step 3: Neo4j Population

Generates Cypher queries:

```cypher
// Create schema block
MERGE (sb:SchemaBlock {id: 'tmf620_productoffering'})
SET sb.title = 'ProductOffering Diagram',
    sb.artifact = 'diagrams/productoffering.png';

// Create entities with FQN
MERGE (e:Entity {fqn: 'tmf620_productoffering#ProductOffering'})
SET e.name = 'ProductOffering',
    e.specId = 'tmf620_productoffering',
    e.kind = 'Entity';

// Create fields
MERGE (f:Field {fqn: 'tmf620_productoffering#ProductOffering.name'})
SET f.name = 'name',
    f.type = 'string',
    f.required = true;

// Link field to entity
MATCH (e:Entity {fqn: 'tmf620_productoffering#ProductOffering'})
MATCH (f:Field {fqn: 'tmf620_productoffering#ProductOffering.name'})
MERGE (e)-[:HAS_FIELD]->(f);

// Create relationships
MATCH (from:Entity {fqn: 'tmf620_productoffering#ProductOffering'})
MATCH (to:Entity {fqn: 'tmf620_productoffering#ProductSpecification'})
MERGE (from)-[r:RELATES_TO {
    type: 'has_specification',
    fromCardinality: '0..1',
    toCardinality: '1',
    direction: 'out'
}]->(to);
```

## Key Features

### 1. **Scalable Data Model**
   - Uses stable labels (`:Entity`, `:RefType`, `:SchemaBlock`) instead of per-class labels
   - Uses FQN (Fully Qualified Name) for entity identity: `<specId>#<entityName>`
   - Uses generic `RELATES_TO` relationship type with `type` property
   - Avoids label explosion and supports namespacing
   - See `references/SCALABLE_RELATIONSHIP_MODEL.md`

### 2. **Provenance Tracking**
   - Tracks source diagram via `SchemaBlock` nodes
   - Uses FQN for entity identity (supports multiple versions)
   - Maintains extraction metadata (`specId`, `extracted_at`)
   - Links entities to schema blocks via `CONTAINS_ENTITY`

### 3. **Conflict Resolution**
   - Handles duplicate entities
   - Merges properties intelligently
   - Resolves relationship conflicts

### 4. **Validation**
   - Validates extracted data structure before population
   - Checks for missing required fields
   - Verifies relationship consistency
   - Validates cardinality formats
   - Can be disabled with `--no-validate` flag

### 5. **Property Persistence**
   - Properties are stored as `:Field` nodes
   - Fields linked to entities via `HAS_FIELD` relationships
   - Property metadata (type, required, default) fully persisted

## Configuration

### Vision Model Settings

```yaml
vision:
  provider: "openai"  # or "anthropic"
  model: "gpt-4o"  # or "claude-3-5-sonnet-20241022"
  max_tokens: 8000
  temperature: 0.1
  use_structured_output: true  # Uses JSON mode when available
```

### Neo4j Settings

```yaml
neo4j:
  uri: "bolt://localhost:7687"
  user: "neo4j"
  password: "password"
  database: "neo4j"
  create_constraints: true
  create_indexes: true
```

### Extraction Settings

```yaml
extraction:
  include_properties: true
  include_methods: false
  normalize_names: true
  handle_references: true
  extract_cardinality: true
```

## Output Formats

### YAML Format

See `schema_examples/tmf620/productoffering_hub.core.example.yaml` for example.

### JSON Format

```json
{
  "meta": {
    "source": "diagrams/product_offering.png",
    "extracted_at": "2024-01-01T00:00:00Z"
  },
  "entities": {
    "ProductOffering": {
      "label": "ProductOffering",
      "properties": [...]
    }
  },
  "relationships": [...]
}
```

### Cypher Format

See `schema_examples/neo4j/tmf620_productoffering_scalable_model.cypher` for example.

## Integration with Existing Tools

### With TMF MCP Builder

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "scripts"))

from extract_and_populate import extract_and_populate
from neo4j import GraphDatabase

# Extract and populate
extract_and_populate(
    image_path="diagrams/tmf620_productoffering.png",
    neo4j_password="password"
)

# Query for relevant subgraph
driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))
with driver.session() as session:
    result = session.run("""
        MATCH (e:Entity {name: 'ProductOffering'})-[r:RELATES_TO*1..2]->(related)
        WHERE r.type IN ['has_specification', 'has_price']
        RETURN e, r, related
    """)
    # Process results...
driver.close()
```

## Best Practices

1. **Pre-process Images**
   - Ensure high resolution
   - Remove noise and artifacts
   - Standardize format (PNG preferred)

2. **Validate Extraction**
   - Review extracted YAML/JSON
   - Verify entity names
   - Check relationship cardinalities

3. **Incremental Updates**
   - Use merge strategies
   - Track changes
   - Maintain provenance

4. **Query Optimization**
   - Create indexes on common properties
   - Use relationship type filters
   - Limit hop depth

5. **Error Handling**
   - Handle missing entities
   - Validate relationships
   - Log extraction issues

## Examples

See `examples/` directory for:
- Simple UML class diagram extraction
- TMF ProductOffering diagram extraction
- Batch processing example
- Custom extraction rules

## References

- `references/SCALABLE_RELATIONSHIP_MODEL.md` - Relationship modeling approach
- `references/VISION_EXTRACTION_PROMPTS.md` - Vision model prompts
- `NEO4J_REQUIREMENTS.md` - Neo4j server version requirements
- `schema_examples/neo4j/` - Example Cypher scripts

## Neo4j Server Requirements

**Important**: Relationship property indexes require Neo4j server version **4.3+**.

- The `requirements.txt` specifies the Python driver version, not the server version
- Check your Neo4j server version: `neo4j version` or `CALL dbms.components()`
- See `NEO4J_REQUIREMENTS.md` for full compatibility details

## Troubleshooting

### Common Issues

1. **Low Extraction Quality**
   - Increase image resolution
   - Use better vision model
   - Provide more context in prompts

2. **Missing Relationships**
   - Check diagram clarity
   - Verify relationship detection logic
   - Review extraction output

3. **Neo4j Population Errors**
   - Check constraints
   - Verify relationship types
   - Review Cypher syntax

4. **Performance Issues**
   - Batch operations
   - Use transactions
   - Create indexes

## Future Enhancements

- Support for sequence diagrams
- Support for activity diagrams
- Multi-page diagram handling
- Automatic relationship inference
- Diagram versioning and diff

