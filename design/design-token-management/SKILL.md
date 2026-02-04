---
name: design-token-management
description: Use when implementing design token systems, CSS variable architectures, or Style Dictionary pipelines. Covers token schemas, naming conventions, token transformations, and multi-platform token delivery for design systems.
allowed-tools: Read, Glob, Grep, Task, Skill
---

# Design Token Management

Guidance for implementing design token systems, token schemas, and multi-platform token delivery for design systems.

## When to Use This Skill

- Defining design token schemas and structures
- Implementing CSS variable architectures
- Building token transformation pipelines
- Managing token naming conventions
- Integrating with design tools (Figma, Style Dictionary)

## Token Architecture

### Token Hierarchy

```text
┌─────────────────────────────────────────────────────────────────┐
│                       TOKEN HIERARCHY                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   PRIMITIVE TOKENS (Raw Values)                                  │
│   ├── colors.blue.500: #3B82F6                                  │
│   ├── spacing.4: 1rem                                           │
│   └── font-size.base: 16px                                      │
│                                                                  │
│            ▼                                                     │
│                                                                  │
│   SEMANTIC TOKENS (Meaning/Purpose)                              │
│   ├── color.action.primary: {colors.blue.500}                   │
│   ├── spacing.component.padding: {spacing.4}                    │
│   └── typography.body.size: {font-size.base}                    │
│                                                                  │
│            ▼                                                     │
│                                                                  │
│   COMPONENT TOKENS (Component-Specific)                          │
│   ├── button.primary.background: {color.action.primary}         │
│   ├── card.padding: {spacing.component.padding}                 │
│   └── paragraph.font-size: {typography.body.size}               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Token Schema

### Core Token Model

```csharp
public class DesignTokenSet
{
    public string Name { get; set; } = string.Empty;
    public string Version { get; set; } = "1.0.0";

    // Token categories
    public ColorTokenCategory Colors { get; set; } = new();
    public TypographyTokenCategory Typography { get; set; } = new();
    public SpacingTokenCategory Spacing { get; set; } = new();
    public BorderTokenCategory Borders { get; set; } = new();
    public ShadowTokenCategory Shadows { get; set; } = new();
    public AnimationTokenCategory Animation { get; set; } = new();

    // Semantic mappings
    public SemanticTokens Semantic { get; set; } = new();

    // Component tokens
    public Dictionary<string, ComponentTokens> Components { get; set; } = new();
}

public class ColorTokenCategory
{
    // Primitive color scales
    public ColorScale Gray { get; set; } = new();
    public ColorScale Blue { get; set; } = new();
    public ColorScale Green { get; set; } = new();
    public ColorScale Red { get; set; } = new();
    public ColorScale Yellow { get; set; } = new();
    public ColorScale Purple { get; set; } = new();

    // Additional custom scales
    public Dictionary<string, ColorScale> Custom { get; set; } = new();
}

public class ColorScale
{
    public string _50 { get; set; } = string.Empty;
    public string _100 { get; set; } = string.Empty;
    public string _200 { get; set; } = string.Empty;
    public string _300 { get; set; } = string.Empty;
    public string _400 { get; set; } = string.Empty;
    public string _500 { get; set; } = string.Empty;
    public string _600 { get; set; } = string.Empty;
    public string _700 { get; set; } = string.Empty;
    public string _800 { get; set; } = string.Empty;
    public string _900 { get; set; } = string.Empty;
    public string _950 { get; set; } = string.Empty;
}

public class TypographyTokenCategory
{
    // Font families
    public Dictionary<string, string> FontFamily { get; set; } = new()
    {
        ["sans"] = "'Inter', system-ui, sans-serif",
        ["serif"] = "'Georgia', serif",
        ["mono"] = "'JetBrains Mono', monospace"
    };

    // Font sizes
    public Dictionary<string, string> FontSize { get; set; } = new()
    {
        ["xs"] = "0.75rem",
        ["sm"] = "0.875rem",
        ["base"] = "1rem",
        ["lg"] = "1.125rem",
        ["xl"] = "1.25rem",
        ["2xl"] = "1.5rem",
        ["3xl"] = "1.875rem",
        ["4xl"] = "2.25rem"
    };

    // Font weights
    public Dictionary<string, string> FontWeight { get; set; } = new()
    {
        ["normal"] = "400",
        ["medium"] = "500",
        ["semibold"] = "600",
        ["bold"] = "700"
    };

    // Line heights
    public Dictionary<string, string> LineHeight { get; set; } = new()
    {
        ["none"] = "1",
        ["tight"] = "1.25",
        ["normal"] = "1.5",
        ["relaxed"] = "1.75"
    };

    // Letter spacing
    public Dictionary<string, string> LetterSpacing { get; set; } = new()
    {
        ["tight"] = "-0.025em",
        ["normal"] = "0",
        ["wide"] = "0.025em"
    };
}

public class SpacingTokenCategory
{
    public Dictionary<string, string> Scale { get; set; } = new()
    {
        ["0"] = "0",
        ["px"] = "1px",
        ["0.5"] = "0.125rem",
        ["1"] = "0.25rem",
        ["2"] = "0.5rem",
        ["3"] = "0.75rem",
        ["4"] = "1rem",
        ["5"] = "1.25rem",
        ["6"] = "1.5rem",
        ["8"] = "2rem",
        ["10"] = "2.5rem",
        ["12"] = "3rem",
        ["16"] = "4rem",
        ["20"] = "5rem",
        ["24"] = "6rem"
    };
}

public class SemanticTokens
{
    // Action colors
    public SemanticColorGroup Action { get; set; } = new()
    {
        Primary = "{colors.blue.500}",
        PrimaryHover = "{colors.blue.600}",
        Secondary = "{colors.gray.500}",
        SecondaryHover = "{colors.gray.600}",
        Danger = "{colors.red.500}",
        DangerHover = "{colors.red.600}"
    };

    // Feedback colors
    public SemanticColorGroup Feedback { get; set; } = new()
    {
        Success = "{colors.green.500}",
        Warning = "{colors.yellow.500}",
        Error = "{colors.red.500}",
        Info = "{colors.blue.500}"
    };

    // Surface colors
    public SemanticSurfaceGroup Surface { get; set; } = new()
    {
        Background = "#FFFFFF",
        Raised = "#F9FAFB",
        Overlay = "rgba(0, 0, 0, 0.5)"
    };

    // Text colors
    public SemanticTextGroup Text { get; set; } = new()
    {
        Primary = "{colors.gray.900}",
        Secondary = "{colors.gray.600}",
        Muted = "{colors.gray.400}",
        Inverse = "#FFFFFF",
        Link = "{colors.blue.500}"
    };
}
```

## Token JSON Format

### Standard Token Format

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "name": "Brand Tokens",
  "version": "1.0.0",
  "colors": {
    "primitive": {
      "blue": {
        "50": { "value": "#EFF6FF", "type": "color" },
        "100": { "value": "#DBEAFE", "type": "color" },
        "500": { "value": "#3B82F6", "type": "color" },
        "600": { "value": "#2563EB", "type": "color" },
        "900": { "value": "#1E3A8A", "type": "color" }
      }
    },
    "semantic": {
      "action": {
        "primary": {
          "value": "{colors.primitive.blue.500}",
          "type": "color",
          "description": "Primary action color"
        },
        "primary-hover": {
          "value": "{colors.primitive.blue.600}",
          "type": "color"
        }
      }
    }
  },
  "typography": {
    "font-family": {
      "base": {
        "value": "'Inter', system-ui, sans-serif",
        "type": "fontFamily"
      },
      "heading": {
        "value": "'Inter', system-ui, sans-serif",
        "type": "fontFamily"
      }
    },
    "font-size": {
      "sm": { "value": "0.875rem", "type": "fontSize" },
      "base": { "value": "1rem", "type": "fontSize" },
      "lg": { "value": "1.125rem", "type": "fontSize" },
      "xl": { "value": "1.25rem", "type": "fontSize" }
    }
  },
  "spacing": {
    "1": { "value": "0.25rem", "type": "spacing" },
    "2": { "value": "0.5rem", "type": "spacing" },
    "4": { "value": "1rem", "type": "spacing" },
    "8": { "value": "2rem", "type": "spacing" }
  },
  "components": {
    "button": {
      "primary": {
        "background": { "value": "{colors.semantic.action.primary}" },
        "background-hover": { "value": "{colors.semantic.action.primary-hover}" },
        "text": { "value": "#FFFFFF" },
        "padding-x": { "value": "{spacing.4}" },
        "padding-y": { "value": "{spacing.2}" },
        "border-radius": { "value": "{borders.radius.md}" }
      }
    }
  }
}
```

## Token Transformation Pipeline

### Token Processor Service

```csharp
public class TokenProcessor
{
    public async Task<Dictionary<string, string>> ResolveTokensAsync(
        DesignTokenSet tokenSet)
    {
        var resolved = new Dictionary<string, string>();

        // First pass: primitive tokens (no references)
        ResolvePrimitives(tokenSet, resolved);

        // Second pass: semantic tokens (reference primitives)
        ResolveSemanticTokens(tokenSet.Semantic, resolved);

        // Third pass: component tokens (reference semantic)
        foreach (var (componentName, tokens) in tokenSet.Components)
        {
            ResolveComponentTokens(componentName, tokens, resolved);
        }

        return resolved;
    }

    private void ResolveSemanticTokens(
        SemanticTokens semantic,
        Dictionary<string, string> resolved)
    {
        // Resolve token references like {colors.blue.500}
        foreach (var property in semantic.GetType().GetProperties())
        {
            var value = property.GetValue(semantic);
            if (value is string strValue && strValue.StartsWith("{"))
            {
                var resolvedValue = ResolveReference(strValue, resolved);
                resolved[$"semantic.{property.Name}"] = resolvedValue;
            }
        }
    }

    private string ResolveReference(
        string reference,
        Dictionary<string, string> resolved)
    {
        // Extract path from {colors.blue.500}
        var path = reference.Trim('{', '}');

        if (resolved.TryGetValue(path, out var value))
        {
            return value;
        }

        throw new TokenResolutionException($"Cannot resolve token reference: {reference}");
    }
}
```

## Output Formats

### CSS Variables Generator

```csharp
public class CssTokenGenerator : ITokenOutputGenerator
{
    public string Generate(Dictionary<string, string> tokens)
    {
        var sb = new StringBuilder();
        sb.AppendLine(":root {");

        foreach (var (name, value) in tokens)
        {
            var cssVarName = ToCssVariableName(name);
            sb.AppendLine($"  --{cssVarName}: {value};");
        }

        sb.AppendLine("}");
        return sb.ToString();
    }

    private string ToCssVariableName(string tokenPath)
    {
        // colors.blue.500 -> color-blue-500
        return tokenPath
            .Replace(".", "-")
            .Replace("_", "-")
            .ToLowerInvariant();
    }
}
```

### SCSS Variables Generator

```csharp
public class ScssTokenGenerator : ITokenOutputGenerator
{
    public string Generate(Dictionary<string, string> tokens)
    {
        var sb = new StringBuilder();
        sb.AppendLine("// Design Tokens - Auto-generated");
        sb.AppendLine();

        // Group by category
        var grouped = tokens.GroupBy(t => t.Key.Split('.')[0]);

        foreach (var group in grouped)
        {
            sb.AppendLine($"// {group.Key}");
            foreach (var (name, value) in group)
            {
                var scssVarName = ToScssVariableName(name);
                sb.AppendLine($"${scssVarName}: {value};");
            }
            sb.AppendLine();
        }

        return sb.ToString();
    }
}
```

### Tailwind Config Generator

```csharp
public class TailwindTokenGenerator : ITokenOutputGenerator
{
    public string Generate(Dictionary<string, string> tokens)
    {
        var config = new
        {
            theme = new
            {
                extend = new
                {
                    colors = BuildColorConfig(tokens),
                    spacing = BuildSpacingConfig(tokens),
                    fontSize = BuildFontSizeConfig(tokens),
                    fontFamily = BuildFontFamilyConfig(tokens)
                }
            }
        };

        return $"module.exports = {JsonSerializer.Serialize(config, new JsonSerializerOptions { WriteIndented = true })}";
    }
}
```

### Generated Tailwind Output

```javascript
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: 'var(--color-action-primary)',
          hover: 'var(--color-action-primary-hover)',
        },
        success: 'var(--color-feedback-success)',
        warning: 'var(--color-feedback-warning)',
        error: 'var(--color-feedback-error)',
      },
      spacing: {
        '1': 'var(--spacing-1)',
        '2': 'var(--spacing-2)',
        '4': 'var(--spacing-4)',
        '8': 'var(--spacing-8)',
      },
      fontSize: {
        'sm': 'var(--font-size-sm)',
        'base': 'var(--font-size-base)',
        'lg': 'var(--font-size-lg)',
      }
    }
  }
}
```

## Token API

### REST Endpoints

```text
GET    /api/tokens                   # List all token sets
GET    /api/tokens/{id}              # Get token set by ID
POST   /api/tokens                   # Create token set
PUT    /api/tokens/{id}              # Update token set
DELETE /api/tokens/{id}              # Delete token set

GET    /api/tokens/{id}/resolved     # Get resolved (flattened) tokens
GET    /api/tokens/{id}/css          # Get CSS variables output
GET    /api/tokens/{id}/scss         # Get SCSS variables output
GET    /api/tokens/{id}/tailwind     # Get Tailwind config
GET    /api/tokens/{id}/json         # Get JSON format (for tools)

POST   /api/tokens/import            # Import from Figma/Style Dictionary
POST   /api/tokens/validate          # Validate token references
```

### Token Response

```json
{
  "data": {
    "id": "tokens-123",
    "name": "Brand Tokens v2",
    "version": "2.0.0",
    "categories": ["colors", "typography", "spacing", "shadows"],
    "tokenCount": 156,
    "outputs": {
      "css": "/api/tokens/tokens-123/css",
      "scss": "/api/tokens/tokens-123/scss",
      "tailwind": "/api/tokens/tokens-123/tailwind"
    },
    "lastModified": "2025-01-15T10:30:00Z"
  }
}
```

## Naming Conventions

### Token Naming Pattern

```text
Category.Variant.Property.State

Examples:
- color.action.primary.default
- color.action.primary.hover
- color.feedback.success
- typography.heading.size.large
- spacing.component.padding
- border.radius.medium
- shadow.elevation.low
```

### Best Practices

| Convention | Good | Bad |
|------------|------|-----|
| Semantic naming | `color.action.primary` | `color.blue` |
| Consistent casing | `font-size-base` | `FontSizeBase` |
| Hierarchical | `spacing.component.padding` | `component-padding` |
| Descriptive | `color.text.muted` | `color.gray-400` |
| Platform-agnostic | `elevation.low` | `box-shadow-1` |

## Design Tool Integration

### Figma Tokens Import

```csharp
public class FigmaTokenImporter
{
    public async Task<DesignTokenSet> ImportAsync(string figmaFileId)
    {
        var figmaTokens = await _figmaClient.GetTokensAsync(figmaFileId);

        return new DesignTokenSet
        {
            Name = figmaTokens.Name,
            Colors = MapFigmaColors(figmaTokens.Colors),
            Typography = MapFigmaTypography(figmaTokens.Typography),
            Spacing = MapFigmaSpacing(figmaTokens.Spacing)
        };
    }
}
```

### Style Dictionary Integration

```json
{
  "source": ["tokens/**/*.json"],
  "platforms": {
    "css": {
      "transformGroup": "css",
      "buildPath": "build/css/",
      "files": [{
        "destination": "variables.css",
        "format": "css/variables"
      }]
    },
    "scss": {
      "transformGroup": "scss",
      "buildPath": "build/scss/",
      "files": [{
        "destination": "_variables.scss",
        "format": "scss/variables"
      }]
    }
  }
}
```

## Related Skills

- `multi-site-theming` - Per-tenant theme customization
- `headless-api-design` - Token API delivery
- `content-type-modeling` - Token sets as content
