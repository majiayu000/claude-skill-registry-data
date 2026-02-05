---
name: yaml-driven-architecture
description: Apply YAML-driven architecture-as-code patterns for system definition, configuration management, and automated generation. Use when designing configuration schemas, building code generators, or implementing declarative architecture definitions.
---

# YAML-Driven Architecture Patterns

## Core Pipeline

```
YAML → Validation → Model → Transform → Output
```

1. **Parse**: YAML to data structures
2. **Validate**: Schema compliance (Pydantic)
3. **Model**: Type-safe internal representation
4. **Transform**: Apply templates
5. **Generate**: Code, docs, configs

## YAML Design Rules

- Maximum 4 levels deep (use references for deeper)
- Convention over configuration (provide sensible defaults)
- Filename conventions for type detection: `system.yaml` → SystemContext, `components.yaml` → ComponentView

## Schema Definition

```python
class Component(BaseModel):
    id: str
    name: str
    class Config:
        extra = "forbid"  # Catch typos
```

- Use `extra="forbid"` to catch typos
- Use kebab-case IDs
- Validate relationships bidirectionally (ensure all references exist)

## Generation Patterns

**Stateless generators**: Pure functions taking model → output
```python
def generate_module(module: ModuleView) -> str:
    return template.render(module=module)
```

**Multi-output**: Single source generates code, docs, tests

## Error Handling

- Provide context: file, line number, field name
- Suggest corrections: "Unknown field 'typ'. Did you mean 'type'?"
- Fail fast with clear messages

## Best Practices

- Validate early at YAML level
- Use anchors for repeated configurations
- Version schemas for breaking changes
- Keep logic in generators, YAML for declaration only

**Remember**: YAML is for configuration, not computation. Keep it declarative.
