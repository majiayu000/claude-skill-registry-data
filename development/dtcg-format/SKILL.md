---
name: dtcg-format
description: Exports design tokens in Design Tokens Community Group (DTCG) format with Figma extensions for variable metadata. Use when creating DTCG-compliant token files, integrating with tools that support the standard, or exporting tokens with Figma variable information.
---

# DTCG Format

## When to use this skill

Use this skill when you need to:
- Export design tokens in the Design Tokens Community Group (DTCG) standard format
- Create token files compatible with DTCG-supporting tools
- Include Figma variable metadata in token exports
- Convert hierarchical token names to nested JSON objects
- Generate token files with proper `$type`, `$value`, and `$extensions` structure

## DTCG format overview

The Design Tokens Community Group format is a standard for representing design tokens in JSON. It uses special properties prefixed with `$` to define token metadata.

### Core properties
- **`$type`**: The token's data type (`color`, `dimension`, `string`, etc.)
- **`$value`**: The token's actual value
- **`$extensions`**: Additional metadata for tool-specific information

### Figma extensions
The format includes Figma-specific extensions for variable integration:
- **`com.figma.variableId`**: Unique identifier for the variable
- **`com.figma.scopes`**: Array of applicable scopes
- **`com.figma.modeName`**: Mode name for the token

## Token structure

### Basic token structure
```json
{
  "button": {
    "primary": {
      "background-color": {
        "$type": "color",
        "$value": "#0066CC",
        "$extensions": {
          "com.figma.variableId": "VariableID:123:456",
          "com.figma.scopes": ["FRAME_FILL", "SHAPE_FILL"]
        }
      }
    }
  }
}
```

### Hierarchical organization
Token names with slashes are converted to nested objects:
```
button/primary/hover/background-color
  ↓
{
  "button": {
    "primary": {
      "hover": {
        "background-color": { ... }
      }
    }
  }
}
```

## DTCG data types

### Color tokens
```json
{
  "color": {
    "primary": {
      "$type": "color",
      "$value": {
        "colorSpace": "srgb",
        "components": [0.0, 0.4, 0.8],
        "alpha": 1.0,
        "hex": "#0066CC"
      },
      "$extensions": {
        "com.figma.variableId": "VariableID:123:456",
        "com.figma.scopes": ["FRAME_FILL", "SHAPE_FILL"]
      }
    }
  }
}
```

### Dimension tokens
```json
{
  "spacing": {
    "md": {
      "$type": "dimension",
      "$value": "16px",
      "$extensions": {
        "com.figma.variableId": "VariableID:123:457",
        "com.figma.scopes": ["GAP"]
      }
    }
  }
}
```

### String tokens
```json
{
  "typography": {
    "family": {
      "primary": {
        "$type": "fontFamily",
        "$value": "Inter",
        "$extensions": {
          "com.figma.variableId": "VariableID:123:458",
          "com.figma.scopes": ["FONT_FAMILY"]
        }
      }
    }
  }
}
```

### Number tokens
```json
{
  "typography": {
    "weight": {
      "bold": {
        "$type": "fontWeight",
        "$value": 600,
        "$extensions": {
          "com.figma.variableId": "VariableID:123:459",
          "com.figma.scopes": ["FONT_WEIGHT"]
        }
      }
    }
  }
}
```

## Type mapping

### CSS property to DTCG type mapping
```javascript
const typeMapping = {
  // Colors
  'background-color': 'color',
  'text-color': 'color',
  'border-color': 'color',
  'shadow-color': 'color',
  
  // Dimensions
  'width': 'dimension',
  'height': 'dimension', 
  'border-radius': 'dimension',
  'padding': 'dimension',
  'margin': 'dimension',
  'gap': 'dimension',
  'border-width': 'dimension',
  
  // Typography
  'font-family': 'fontFamily',
  'font-size': 'fontSize',
  'font-weight': 'fontWeight',
  'line-height': 'lineHeight',
  'letter-spacing': 'letterSpacing',
  
  // Numbers
  'opacity': 'number',
  
  // Strings
  'font-style': 'string',
  'text-align': 'string'
};
```

### Figma type to DTCG type mapping
```javascript
const figmaTypeToDTCG = {
  'COLOR': 'color',
  'FLOAT': 'number', // or 'dimension' for sizing
  'STRING': 'string',
  'BOOLEAN': 'boolean'
};
```

## Generating DTCG format

### Basic usage
```javascript
const tokens = [
  { 
    name: 'button/primary/background-color', 
    type: 'COLOR', 
    scopes: ['FRAME_FILL'] 
  },
  { 
    name: 'spacing/md', 
    type: 'FLOAT', 
    scopes: ['GAP'] 
  }
];

const dtcgJson = generateDTCGFormat(tokens);
```

### Generated output
```json
{
  "button": {
    "primary": {
      "background-color": {
        "$type": "color",
        "$value": {
          "colorSpace": "srgb",
          "components": [1, 1, 1],
          "alpha": 1,
          "hex": "#FFFFFF"
        },
        "$extensions": {
          "com.figma.variableId": "VariableID:39:123",
          "com.figma.scopes": ["FRAME_FILL"]
        }
      }
    }
  },
  "spacing": {
    "md": {
      "$type": "number", 
      "$value": 1,
      "$extensions": {
        "com.figma.variableId": "VariableID:39:124",
        "com.figma.scopes": ["GAP"]
      }
    }
  },
  "$extensions": {
    "com.figma.modeName": "Default"
  }
}
```

## Default values by type

### Color values
```json
{
  "colorSpace": "srgb",
  "components": [1, 1, 1],  // White RGB normalized
  "alpha": 1,
  "hex": "#FFFFFF"
}
```

### Dimension values
Numeric values default to `1` with appropriate units inferred from context.

### String values
Default to the string `"string"` as placeholder.

### Number values
Default to `1` for numeric tokens.

## Extension properties

### Figma variable ID
Automatically generated in Figma format:
```json
"com.figma.variableId": "VariableID:39:123"
```

### Figma scopes
Based on CSS property mapping:
```json
"com.figma.scopes": ["FRAME_FILL", "SHAPE_FILL"]
```

### Mode information
Collection-level mode metadata:
```json
"$extensions": {
  "com.figma.modeName": "Default"
}
```

## Tool integration

### Figma integration
DTCG files with Figma extensions can be imported directly into Figma as variable collections, preserving:
- Variable types
- Scope assignments
- Hierarchical naming
- Mode organization

### Token tools compatibility
The format works with DTCG-compatible tools including:
- Style Dictionary
- Theo
- Design Tokens CLI
- Token Studio for Figma

## Best practices

1. **Consistent naming**: Use clear, hierarchical token names
2. **Appropriate types**: Match DTCG types to token usage
3. **Meaningful scopes**: Set Figma scopes that match intended usage
4. **Organized structure**: Group related tokens in logical hierarchies
5. **Default values**: Provide reasonable placeholder values for all tokens
6. **Tool compatibility**: Test exports with your target tools
7. **Documentation**: Include metadata explaining token purposes and relationships

## Examples

See [scripts/generateDTCG.js](scripts/generateDTCG.js) for the complete implementation of DTCG format generation with Figma extensions.