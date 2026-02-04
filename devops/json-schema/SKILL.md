---
name: json-schema
# prettier-ignore
description: Use when working with JSON Schema for validation, including draft-07, 2019-09, and 2020-12 specifications
---

# JSON Schema

## Quick Start

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "required": ["id", "name"],
  "properties": {
    "id": { "type": "integer", "minimum": 1 },
    "name": { "type": "string", "minLength": 1 },
    "email": { "type": "string", "format": "email" },
    "tags": {
      "type": "array",
      "items": { "type": "string" },
      "uniqueItems": true
    }
  },
  "additionalProperties": false
}
```

## Core Keywords

- **Types**: `string`, `number`, `integer`, `boolean`, `array`, `object`, `null`
- **String**: `minLength`, `maxLength`, `pattern`, `format`
- **Number**: `minimum`, `maximum`, `exclusiveMinimum`, `exclusiveMaximum`, `multipleOf`
- **Array**: `items`, `minItems`, `maxItems`, `uniqueItems`, `contains`
- **Object**: `properties`, `required`, `additionalProperties`, `patternProperties`
- **Composition**: `allOf`, `anyOf`, `oneOf`, `not`
- **Conditional**: `if`/`then`/`else`
- **References**: `$ref`, `$defs` (or `definitions` in draft-07)

## Common Formats

`date-time`, `date`, `time`, `email`, `uri`, `uuid`, `ipv4`, `ipv6`, `regex`

## Ajv (JavaScript Validator)

```typescript
import Ajv from 'ajv';
import addFormats from 'ajv-formats';

const ajv = new Ajv({ allErrors: true });
addFormats(ajv);

const validate = ajv.compile(schema);
if (!validate(data)) console.log(validate.errors);
```

## Reference Files

- [references/keywords.md](references/keywords.md) - Complete keyword reference
- [references/composition.md](references/composition.md) - allOf/anyOf/oneOf patterns
- [references/ajv.md](references/ajv.md) - Ajv configuration and usage
