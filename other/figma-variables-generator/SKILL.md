---
name: figma-variables-generator
version: 1.1.0
description: Generate JSON files for creating Figma variable collections from text descriptions or design token data. Use when designers need to create or convert design tokens (colors, spacing, typography, etc.) into Figma variables format. Supports multiple modes (Light/Dark), code syntax definitions, variable references/aliases, and hierarchical organization. Triggers include requests to "create Figma variables", "generate variables JSON", "convert design tokens", or working with design system tokens.
---

# Figma Variables Generator

Generate properly formatted JSON files for creating Figma variable collections from text descriptions, existing design token data, or images showing design systems.

## Core Capabilities

This skill helps designers create Figma variable collections by generating the JSON format required by Figma variable import/export plugins. The output can be directly imported into Figma using plugins like "Variables Import Export" or similar tools.

### Supported Variable Types

Figma supports only **4 core variable types**:

- **Color** (`$type: "color"`) - RGB hex values, rgba, or variable references
- **Number** (`$type: "number"`) - Numeric values (spacing, sizes, radius, weights, etc.)
- **String** (`$type: "string"`) - Text values (font families, names, etc.)
- **Boolean** (`$type: "boolean"`) - True/false values

**Important**: Types like spacing, borderRadius, fontSize, fontWeight should use `number` type. Use semantic naming in your variable paths to indicate their purpose (e.g., `spacing.xs`, `radius.md`, `fontSize.body`)

### Key Features

1. **Multiple Modes**: Support for different modes (e.g., Light/Dark themes)
2. **Variable References**: Use `{collection.subcategory.variableName}` syntax to reference other variables
3. **Code Syntax**: Optional platform-specific naming conventions (WEB, iOS, ANDROID)
4. **Hierarchical Organization**: Group variables into collections, categories, and subcategories
5. **Flexible Input**: Accept design tokens from text, structured data, or images

## Workflow

### Step 0: Check for Existing JSON (For Updates or Reformatting)

**CRITICAL**: When the user asks to update, add to, or reformat an existing JSON file, you MUST:

1. **Read the existing file first** - Use the Read tool to load the current JSON
2. **Preserve all naming exactly** - Collection names, category names, subcategory names, and variable names must match EXACTLY
3. **Understand Figma's behavior**: Figma uses names as unique identifiers:
   - Same name = overwrites/updates the variable
   - Different name = creates a new variable/collection/category
4. **Maintain hierarchy** - Keep the exact same nesting structure
5. **Reorder for readability** - If JSON is messy or poorly organized, reorder it following the guidelines in Step 2.5

**Example Scenario**:
- Existing: `{"Spacing": {"space": {"sm": {"$type": "number", "$value": 8}}}}`
- User asks: "Add a medium spacing value"
- ✅ Correct: Add to existing structure: `{"Spacing": {"space": {"sm": {...}, "md": {...}}}}`
- ❌ Wrong: Create new structure: `{"Spacing": {"spacing": {"md": {...}}}}` (creates duplicate category)

### Step 1: Gather Information

Before generating the JSON, ask the user:

1. **New or Update**: Is this a new collection or updating an existing one?
   - If updating: Request the existing JSON file to preserve naming
2. **Collection Name**: What should the variable collection be named?
3. **Variable Content**: What variables need to be created? (Accept text descriptions, existing JSON, or analyze uploaded images)
4. **Modes**: Does this collection need multiple modes (e.g., Light/Dark)? What should they be named?
5. **Code Syntax**: Should code syntax be included? If yes:
   - Which platforms? (WEB, iOS, ANDROID)
   - What naming convention? (camelCase, snake_case, kebab-case, PascalCase)
6. **Organization**: How should variables be organized? (category/subcategory structure)

### Step 2: Generate JSON Structure

Create a JSON file following this structure:

### Step 2.5: Format and Order for Readability

When generating or reformatting JSON, follow these ordering principles for maximum human readability:

**1. Property Order within Each Variable**:
```json
{
  "variableName": {
    "$type": "color",           // 1. Type first
    "$value": "#ffffff",         // 2. Value second
    "$description": "...",       // 3. Description (if present)
    "$extensions": {...}         // 4. Extensions last
  }
}
```

**2. Variable Ordering within Categories**:
- **Size-based**: Order by size (xs → sm → md → lg → xl)
- **Numeric**: Order numerically (0 → 1 → 2 → 3...)
- **Semantic priority**: Order by importance (primary → secondary → tertiary)
- **Alphabetical**: Use as fallback when no other logic applies

**3. Category Ordering**:
Order categories logically:
1. Primitives/base values first (colors, raw values)
2. Semantic/functional tokens second (text, background, border)
3. Component-specific tokens last (button, card, modal)

**4. Indentation and Formatting**:
- Use 2-space indentation
- Each property on its own line
- Consistent spacing between objects
- No trailing commas

**Example of Well-Ordered JSON**:
```json
{
  "Design System": {
    "primitives": {
      "gray": {
        "100": {"$type": "color", "$value": "#f7f7f7"},
        "200": {"$type": "color", "$value": "#e1e1e1"},
        "300": {"$type": "color", "$value": "#cfcfcf"}
      }
    },
    "semantic": {
      "text": {
        "primary": {"$type": "color", "$value": "{Design System.primitives.gray.300}"},
        "secondary": {"$type": "color", "$value": "{Design System.primitives.gray.200}"}
      }
    },
    "spacing": {
      "xs": {"$type": "number", "$value": 4},
      "sm": {"$type": "number", "$value": 8},
      "md": {"$type": "number", "$value": 16},
      "lg": {"$type": "number", "$value": 24},
      "xl": {"$type": "number", "$value": 32}
    }
  }
}
```

### Step 3: Generate the JSON File

Create a JSON file following this structure:

```json
{
  "Collection Name": {
    "category": {
      "subcategory": {
        "variableName": {
          "$type": "color",
          "$value": {
            "Light": "#ffffff",
            "Dark": "#000000"
          },
          "$extensions": {
            "codeSyntax": {
              "WEB": "categorySubcategoryVariableName"
            }
          }
        }
      }
    }
  }
}
```

### Step 4: Apply Naming Conventions

When code syntax is requested:

**camelCase** (default for WEB):
- `foreground.base` → `foregroundBase`
- `background.interactive.primary` → `backgroundInteractivePrimary`

**snake_case** (common for Python, some backend systems):
- `foreground.base` → `foreground_base`
- `background.interactive.primary` → `background_interactive_primary`

**kebab-case** (common for CSS):
- `foreground.base` → `foreground-base`
- `background.interactive.primary` → `background-interactive-primary`

**PascalCase** (common for some component systems):
- `foreground.base` → `ForegroundBase`
- `background.interactive.primary` → `BackgroundInteractivePrimary`

### Step 5: Convert Units to Pixels

**CRITICAL**: Figma only works with pixel values. Always convert relative units to pixels:

**Common Conversions** (assuming 16px base font size):
- `1rem` → `16` (pixels)
- `2rem` → `32` (pixels)
- `0.875rem` → `14` (pixels)
- `1em` → `16` (pixels, context-dependent)
- `1.5em` → `24` (pixels, context-dependent)

**Percentage/Viewport Units** (ask user for context if needed):
- `100%` → ask for parent container size
- `50vw` → ask for viewport width or use common breakpoint
- `10vh` → ask for viewport height or use common breakpoint

**Other Units**:
- `1pt` → `1.333` (pixels)
- `1pc` → `16` (pixels, 1 pica = 12 points)

When encountering unit-based values, automatically convert to pixels without units in the JSON output.

**Example**:
- Input: `font-size: 1.5rem` → Output: `"$value": 24`
- Input: `spacing: 2rem` → Output: `"$value": 32`
- Input: `line-height: 1.5em` → Output: `"$value": 24`

### Step 6: Handle Variable References

For variables that reference other variables (aliases), use the reference syntax:

```json
{
  "Semantic Colors": {
    "text": {
      "primary": {
        "$type": "color",
        "$value": {
          "Light": "{Color Primitives.gray.gray900}",
          "Dark": "{Color Primitives.gray.gray100}"
        }
      }
    }
  }
}
```

The reference format is: `{CollectionName.category.subcategory.variableName}`

## Examples

### Example 1: Simple Color Tokens

**Input**: "Create a collection called 'Brand Colors' with primary (#389fba), secondary (#c9a0dc), and white (#ffffff) colors for light and dark modes"

**Output**:
```json
{
  "Brand Colors": {
    "primary": {
      "$type": "color",
      "$value": {
        "Light": "#389fba",
        "Dark": "#389fba"
      }
    },
    "secondary": {
      "$type": "color",
      "$value": {
        "Light": "#c9a0dc",
        "Dark": "#c9a0dc"
      }
    },
    "white": {
      "$type": "color",
      "$value": {
        "Light": "#ffffff",
        "Dark": "#ffffff"
      }
    }
  }
}
```

### Example 2: Spacing Scale with Code Syntax

**Input**: "Create a spacing scale collection with values 0, 8, 16, 24, 32px. Use camelCase for web."

**Output**:
```json
{
  "Spacing": {
    "space": {
      "0": {
        "$type": "number",
        "$value": 0,
        "$extensions": {
          "codeSyntax": {
            "WEB": "space0"
          }
        }
      },
      "1": {
        "$type": "number",
        "$value": 8,
        "$extensions": {
          "codeSyntax": {
            "WEB": "space1"
          }
        }
      },
      "2": {
        "$type": "number",
        "$value": 16,
        "$extensions": {
          "codeSyntax": {
            "WEB": "space2"
          }
        }
      },
      "3": {
        "$type": "number",
        "$value": 24,
        "$extensions": {
          "codeSyntax": {
            "WEB": "space3"
          }
        }
      },
      "4": {
        "$type": "number",
        "$value": 32,
        "$extensions": {
          "codeSyntax": {
            "WEB": "space4"
          }
        }
      }
    }
  }
}
```

### Example 3: Unit Conversion from rem to pixels

**Input**: "Create typography tokens: body is 1rem, heading-sm is 1.25rem, heading-md is 1.5rem, heading-lg is 2rem"

**Output**:
```json
{
  "Typography": {
    "fontSize": {
      "body": {
        "$type": "number",
        "$value": 16,
        "$extensions": {
          "codeSyntax": {
            "WEB": "fontSizeBody"
          }
        }
      },
      "headingSm": {
        "$type": "number",
        "$value": 20,
        "$extensions": {
          "codeSyntax": {
            "WEB": "fontSizeHeadingSm"
          }
        }
      },
      "headingMd": {
        "$type": "number",
        "$value": 24,
        "$extensions": {
          "codeSyntax": {
            "WEB": "fontSizeHeadingMd"
          }
        }
      },
      "headingLg": {
        "$type": "number",
        "$value": 32,
        "$extensions": {
          "codeSyntax": {
            "WEB": "fontSizeHeadingLg"
          }
        }
      }
    }
  }
}
```

### Example 4: Semantic Colors with References

**Input**: "Create semantic colors that reference primitives. Text primary should use gray900 in light mode and gray100 in dark mode."

**Output**:
```json
{
  "Semantic Colors": {
    "text": {
      "primary": {
        "$type": "color",
        "$value": {
          "Light": "{Primitives.gray.gray900}",
          "Dark": "{Primitives.gray.gray100}"
        },
        "$extensions": {
          "codeSyntax": {
            "WEB": "textPrimary"
          }
        }
      }
    }
  }
}
```

### Example 5: Updating an Existing Collection

**Existing JSON**:
```json
{
  "Spacing": {
    "space": {
      "xs": {
        "$type": "number",
        "$value": 4
      },
      "sm": {
        "$type": "number",
        "$value": 8
      }
    }
  }
}
```

**User Request**: "Add medium (16px) and large (24px) spacing values"

**Correct Output** (preserves naming and structure):
```json
{
  "Spacing": {
    "space": {
      "xs": {
        "$type": "number",
        "$value": 4
      },
      "sm": {
        "$type": "number",
        "$value": 8
      },
      "md": {
        "$type": "number",
        "$value": 16
      },
      "lg": {
        "$type": "number",
        "$value": 24
      }
    }
  }
}
```

**❌ Incorrect Output** (would create duplicates in Figma):
```json
{
  "Spacing": {
    "spacing": {
      "md": {
        "$type": "number",
        "$value": 16
      },
      "lg": {
        "$type": "number",
        "$value": 24
      }
    }
  }
}
```
*This is wrong because the category name changed from "space" to "spacing", which would create a separate category in Figma instead of adding to the existing one.*

### Example 6: Reformatting Messy Plugin-Generated JSON

**Messy Input** (from plugin, poorly ordered):
```json
{
  "Colors": {
    "button": {
      "hover": {"$value": "#2563eb", "$type": "color"},
      "default": {"$value": "#3b82f6", "$type": "color"},
      "pressed": {"$value": "#1d4ed8", "$type": "color"}
    },
    "text": {
      "tertiary": {"$value": "#9ca3af", "$type": "color"},
      "primary": {"$value": "#111827", "$type": "color"},
      "secondary": {"$value": "#6b7280", "$type": "color"}
    },
    "gray": {
      "900": {"$value": "#111827", "$type": "color"},
      "500": {"$value": "#6b7280", "$type": "color"},
      "100": {"$value": "#f3f4f6", "$type": "color"}
    }
  }
}
```

**Reformatted Output** (properly ordered for readability):
```json
{
  "Colors": {
    "gray": {
      "100": {
        "$type": "color",
        "$value": "#f3f4f6"
      },
      "500": {
        "$type": "color",
        "$value": "#6b7280"
      },
      "900": {
        "$type": "color",
        "$value": "#111827"
      }
    },
    "text": {
      "primary": {
        "$type": "color",
        "$value": "#111827"
      },
      "secondary": {
        "$type": "color",
        "$value": "#6b7280"
      },
      "tertiary": {
        "$type": "color",
        "$value": "#9ca3af"
      }
    },
    "button": {
      "default": {
        "$type": "color",
        "$value": "#3b82f6"
      },
      "hover": {
        "$type": "color",
        "$value": "#2563eb"
      },
      "pressed": {
        "$type": "color",
        "$value": "#1d4ed8"
      }
    }
  }
}
```

**Improvements Made**:
1. ✅ Reordered categories: primitives (gray) → semantic (text) → component (button)
2. ✅ Reordered variables: numeric order (100→500→900), semantic order (primary→secondary→tertiary), state order (default→hover→pressed)
3. ✅ Consistent property order: `$type` before `$value`
4. ✅ Proper 2-space indentation
5. ✅ Better readability for human review

## Important Notes

1. **Updating Existing Collections**: When adding to or updating an existing JSON file:
   - **Always read the existing file first** before making changes
   - **Preserve exact naming**: Collection, category, subcategory, and variable names are unique identifiers
   - **Figma's overwrite behavior**: Same name = updates existing, different name = creates new
   - **Maintain hierarchy**: Keep the same nesting structure to avoid creating duplicates
   - Example: If you have `{"Spacing": {"space": {...}}}`, adding new values must use `"space"` not `"spacing"` or `"spaces"`

2. **Only 4 Variable Types**: Figma's variable system only supports `color`, `number`, `string`, and `boolean`. DO NOT use types like `spacing`, `borderRadius`, `fontSize`, or `fontWeight` - these are invalid and will cause import errors. Instead:
   - Use `number` for spacing, radius, font sizes, weights, dimensions
   - Use `string` for font families and text values
   - Use semantic naming in your variable paths to indicate purpose (e.g., `spacing.sm`, `fontSize.body`, `radius.lg`)

3. **Pixel Values Only**: Figma only accepts pixel values for numeric types. Always convert rem, em, %, vw, vh, pt, and other units to pixels:
   - 1rem = 16px (standard base)
   - 1em = 16px (context-dependent)
   - 1pt = 1.333px
   - Ask user for context if percentage or viewport units are present

4. **Single Mode Collections**: If only one mode is needed, omit the mode structure and use direct values:
   ```json
   {
     "Collection": {
       "variable": {
         "$type": "color",
         "$value": "#ffffff"
       }
     }
   }
   ```

5. **Code Syntax is Optional**: Only include `$extensions.codeSyntax` when explicitly requested by the user

6. **Consistent Hierarchy**: Maintain consistent depth in variable paths (e.g., all variables at same nesting level within a category)

7. **Valid Color Formats**:
   - Hex: `#ffffff`, `#fff`
   - RGB object: `{r: 1, g: 1, b: 1}` (values 0-1)
   - RGBA: `rgba(255, 255, 255, 0.5)`
   - Variable reference: `{collection.path.to.variable}`

8. **File Naming**: Use descriptive names like `brand-colors.json`, `spacing-tokens.json`, `semantic-colors.json`

9. **Reformatting Plugin-Generated JSON**: When a user provides JSON from a plugin that's hard to read:
   - Preserve all names exactly (collections, categories, variables)
   - Reorder for readability following Step 2.5 guidelines
   - Fix property order: `$type` → `$value` → `$description` → `$extensions`
   - Apply consistent 2-space indentation
   - Order variables logically (size-based, numeric, semantic, or alphabetical)
   - Order categories logically (primitives → semantic → components)

## Common Patterns

### Pattern 1: Primitive + Semantic Collections

Create two collections: one for primitives (base colors, raw values) and one for semantic tokens (purpose-based references).

### Pattern 2: Multi-Platform Syntax

When supporting multiple platforms, include all in the same variable:

```json
{
  "$extensions": {
    "codeSyntax": {
      "WEB": "backgroundPrimary",
      "iOS": "backgroundColor.primary",
      "ANDROID": "background_color_primary"
    }
  }
}
```

### Pattern 3: Complex Hierarchies

For design systems with deep organization:

```json
{
  "Design System": {
    "component": {
      "button": {
        "background": {
          "primary": {
            "default": { ... },
            "hover": { ... },
            "pressed": { ... }
          }
        }
      }
    }
  }
}
```

## Deliverable

Always create the JSON file and provide it to the user in `/mnt/user-data/outputs/` with a clear, descriptive filename. Include a brief summary of what was generated and how to import it into Figma.
