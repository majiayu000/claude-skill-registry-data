---
name: Markdown to ADF Converter
description: Convert Markdown content to Confluence's ADF (Atlassian Document Format) for creating and updating pages. Use when creating Confluence pages from README files, documentation, or any Markdown content. Handles headings, lists, code blocks, tables, links, and more.
---

# Markdown to ADF Converter

Expert assistance for converting Markdown content to Confluence's ADF (Atlassian Document Format).

## When to Use This Skill

- Converting README.md to Confluence
- Creating Confluence pages from Markdown documentation
- Updating Confluence with Markdown content
- User mentions: convert, markdown, ADF, format
- User wants to publish Markdown to Confluence

## What is ADF?

**ADF (Atlassian Document Format)** is Confluence's JSON-based document format. It represents content as a structured tree of nodes.

### Basic ADF Structure
```json
{
  "version": 1,
  "type": "doc",
  "content": [
    {
      "type": "paragraph",
      "content": [
        {
          "type": "text",
          "text": "Hello world"
        }
      ]
    }
  ]
}
```

## Conversion Reference

### Text Formatting

#### Markdown → ADF

**Bold**:
```markdown
**bold text**
```
```json
{
  "type": "text",
  "text": "bold text",
  "marks": [{"type": "strong"}]
}
```

**Italic**:
```markdown
*italic text*
```
```json
{
  "type": "text",
  "text": "italic text",
  "marks": [{"type": "em"}]
}
```

**Code (inline)**:
```markdown
`code snippet`
```
```json
{
  "type": "text",
  "text": "code snippet",
  "marks": [{"type": "code"}]
}
```

**Strikethrough**:
```markdown
~~struck text~~
```
```json
{
  "type": "text",
  "text": "struck text",
  "marks": [{"type": "strike"}]
}
```

**Underline**:
```markdown
<u>underlined</u>
```
```json
{
  "type": "text",
  "text": "underlined",
  "marks": [{"type": "underline"}]
}
```

**Combined marks**:
```markdown
***bold italic***
```
```json
{
  "type": "text",
  "text": "bold italic",
  "marks": [
    {"type": "strong"},
    {"type": "em"}
  ]
}
```

### Headings

```markdown
# Heading 1
## Heading 2
### Heading 3
```

```json
{
  "type": "heading",
  "attrs": {"level": 1},
  "content": [
    {"type": "text", "text": "Heading 1"}
  ]
},
{
  "type": "heading",
  "attrs": {"level": 2},
  "content": [
    {"type": "text", "text": "Heading 2"}
  ]
},
{
  "type": "heading",
  "attrs": {"level": 3},
  "content": [
    {"type": "text", "text": "Heading 3"}
  ]
}
```

**Note**: Confluence supports heading levels 1-6.

### Paragraphs

```markdown
This is a paragraph.

This is another paragraph.
```

```json
{
  "type": "paragraph",
  "content": [
    {"type": "text", "text": "This is a paragraph."}
  ]
},
{
  "type": "paragraph",
  "content": [
    {"type": "text", "text": "This is another paragraph."}
  ]
}
```

### Lists

#### Unordered (Bullet) List

```markdown
- Item 1
- Item 2
  - Nested item 2.1
  - Nested item 2.2
- Item 3
```

```json
{
  "type": "bulletList",
  "content": [
    {
      "type": "listItem",
      "content": [
        {
          "type": "paragraph",
          "content": [{"type": "text", "text": "Item 1"}]
        }
      ]
    },
    {
      "type": "listItem",
      "content": [
        {
          "type": "paragraph",
          "content": [{"type": "text", "text": "Item 2"}]
        },
        {
          "type": "bulletList",
          "content": [
            {
              "type": "listItem",
              "content": [
                {
                  "type": "paragraph",
                  "content": [{"type": "text", "text": "Nested item 2.1"}]
                }
              ]
            },
            {
              "type": "listItem",
              "content": [
                {
                  "type": "paragraph",
                  "content": [{"type": "text", "text": "Nested item 2.2"}]
                }
              ]
            }
          ]
        }
      ]
    },
    {
      "type": "listItem",
      "content": [
        {
          "type": "paragraph",
          "content": [{"type": "text", "text": "Item 3"}]
        }
      ]
    }
  ]
}
```

#### Ordered (Numbered) List

```markdown
1. First item
2. Second item
3. Third item
```

```json
{
  "type": "orderedList",
  "content": [
    {
      "type": "listItem",
      "content": [
        {
          "type": "paragraph",
          "content": [{"type": "text", "text": "First item"}]
        }
      ]
    },
    {
      "type": "listItem",
      "content": [
        {
          "type": "paragraph",
          "content": [{"type": "text", "text": "Second item"}]
        }
      ]
    },
    {
      "type": "listItem",
      "content": [
        {
          "type": "paragraph",
          "content": [{"type": "text", "text": "Third item"}]
        }
      ]
    }
  ]
}
```

### Links

```markdown
[Link text](https://example.com)
```

```json
{
  "type": "text",
  "text": "Link text",
  "marks": [
    {
      "type": "link",
      "attrs": {
        "href": "https://example.com"
      }
    }
  ]
}
```

### Code Blocks

```markdown
```python
def hello():
    print("Hello world")
```
```

```json
{
  "type": "codeBlock",
  "attrs": {
    "language": "python"
  },
  "content": [
    {
      "type": "text",
      "text": "def hello():\n    print(\"Hello world\")"
    }
  ]
}
```

**Supported languages**: javascript, python, java, go, rust, typescript, sql, bash, json, xml, html, css, and many more.

### Blockquotes

```markdown
> This is a quote
> Multi-line quote
```

```json
{
  "type": "blockquote",
  "content": [
    {
      "type": "paragraph",
      "content": [
        {"type": "text", "text": "This is a quote"}
      ]
    },
    {
      "type": "paragraph",
      "content": [
        {"type": "text", "text": "Multi-line quote"}
      ]
    }
  ]
}
```

### Horizontal Rules

```markdown
---
```

```json
{
  "type": "rule"
}
```

### Tables

```markdown
| Header 1 | Header 2 | Header 3 |
|----------|----------|----------|
| Cell 1   | Cell 2   | Cell 3   |
| Cell 4   | Cell 5   | Cell 6   |
```

```json
{
  "type": "table",
  "content": [
    {
      "type": "tableRow",
      "content": [
        {
          "type": "tableHeader",
          "content": [
            {
              "type": "paragraph",
              "content": [{"type": "text", "text": "Header 1"}]
            }
          ]
        },
        {
          "type": "tableHeader",
          "content": [
            {
              "type": "paragraph",
              "content": [{"type": "text", "text": "Header 2"}]
            }
          ]
        },
        {
          "type": "tableHeader",
          "content": [
            {
              "type": "paragraph",
              "content": [{"type": "text", "text": "Header 3"}]
            }
          ]
        }
      ]
    },
    {
      "type": "tableRow",
      "content": [
        {
          "type": "tableCell",
          "content": [
            {
              "type": "paragraph",
              "content": [{"type": "text", "text": "Cell 1"}]
            }
          ]
        },
        {
          "type": "tableCell",
          "content": [
            {
              "type": "paragraph",
              "content": [{"type": "text", "text": "Cell 2"}]
            }
          ]
        },
        {
          "type": "tableCell",
          "content": [
            {
              "type": "paragraph",
              "content": [{"type": "text", "text": "Cell 3"}]
            }
          ]
        }
      ]
    },
    {
      "type": "tableRow",
      "content": [
        {
          "type": "tableCell",
          "content": [
            {
              "type": "paragraph",
              "content": [{"type": "text", "text": "Cell 4"}]
            }
          ]
        },
        {
          "type": "tableCell",
          "content": [
            {
              "type": "paragraph",
              "content": [{"type": "text", "text": "Cell 5"}]
            }
          ]
        },
        {
          "type": "tableCell",
          "content": [
            {
              "type": "paragraph",
              "content": [{"type": "text", "text": "Cell 6"}]
            }
          ]
        }
      ]
    }
  ]
}
```

### Images

```markdown
![Alt text](https://example.com/image.png)
```

```json
{
  "type": "mediaSingle",
  "content": [
    {
      "type": "media",
      "attrs": {
        "type": "external",
        "url": "https://example.com/image.png",
        "alt": "Alt text"
      }
    }
  ]
}
```

### Task Lists (Checkboxes)

```markdown
- [x] Completed task
- [ ] Incomplete task
```

```json
{
  "type": "taskList",
  "content": [
    {
      "type": "taskItem",
      "attrs": {
        "state": "DONE"
      },
      "content": [
        {
          "type": "text",
          "text": "Completed task"
        }
      ]
    },
    {
      "type": "taskItem",
      "attrs": {
        "state": "TODO"
      },
      "content": [
        {
          "type": "text",
          "text": "Incomplete task"
        }
      ]
    }
  ]
}
```

## Confluence-Specific Extensions

### Info Panel (Callout)

```markdown
> ℹ️ **Info**
> This is important information
```

```json
{
  "type": "panel",
  "attrs": {
    "panelType": "info"
  },
  "content": [
    {
      "type": "paragraph",
      "content": [
        {"type": "text", "text": "This is important information"}
      ]
    }
  ]
}
```

**Panel types**: `info`, `note`, `warning`, `error`, `success`

### Expand/Collapse

```markdown
<details>
<summary>Click to expand</summary>
Hidden content here
</details>
```

```json
{
  "type": "expand",
  "attrs": {
    "title": "Click to expand"
  },
  "content": [
    {
      "type": "paragraph",
      "content": [
        {"type": "text", "text": "Hidden content here"}
      ]
    }
  ]
}
```

### Status Badge

```markdown
Status: `DONE` or `IN_PROGRESS`
```

```json
{
  "type": "status",
  "attrs": {
    "text": "DONE",
    "color": "green"
  }
}
```

**Colors**: `neutral`, `purple`, `blue`, `red`, `yellow`, `green`

### Mentions

```markdown
@username
```

```json
{
  "type": "mention",
  "attrs": {
    "id": "user-account-id",
    "text": "@username"
  }
}
```

### Emojis

```markdown
:smile: :+1: :rocket:
```

```json
{
  "type": "emoji",
  "attrs": {
    "shortName": ":smile:",
    "text": "😀"
  }
}
```

## Complete Example

### Markdown Input
```markdown
# Project Documentation

## Overview

This is a **sample project** with `code examples`.

### Features

- Feature 1
- Feature 2
  - Sub-feature A
  - Sub-feature B

### Installation

```bash
npm install my-package
```

For more info, visit [our website](https://example.com).

> **Note**: This is still in beta.

| Command | Description |
|---------|-------------|
| `start` | Start server |
| `test`  | Run tests   |
```

### ADF Output
```json
{
  "version": 1,
  "type": "doc",
  "content": [
    {
      "type": "heading",
      "attrs": {"level": 1},
      "content": [
        {"type": "text", "text": "Project Documentation"}
      ]
    },
    {
      "type": "heading",
      "attrs": {"level": 2},
      "content": [
        {"type": "text", "text": "Overview"}
      ]
    },
    {
      "type": "paragraph",
      "content": [
        {"type": "text", "text": "This is a "},
        {
          "type": "text",
          "text": "sample project",
          "marks": [{"type": "strong"}]
        },
        {"type": "text", "text": " with "},
        {
          "type": "text",
          "text": "code examples",
          "marks": [{"type": "code"}]
        },
        {"type": "text", "text": "."}
      ]
    },
    {
      "type": "heading",
      "attrs": {"level": 3},
      "content": [
        {"type": "text", "text": "Features"}
      ]
    },
    {
      "type": "bulletList",
      "content": [
        {
          "type": "listItem",
          "content": [
            {
              "type": "paragraph",
              "content": [{"type": "text", "text": "Feature 1"}]
            }
          ]
        },
        {
          "type": "listItem",
          "content": [
            {
              "type": "paragraph",
              "content": [{"type": "text", "text": "Feature 2"}]
            },
            {
              "type": "bulletList",
              "content": [
                {
                  "type": "listItem",
                  "content": [
                    {
                      "type": "paragraph",
                      "content": [{"type": "text", "text": "Sub-feature A"}]
                    }
                  ]
                },
                {
                  "type": "listItem",
                  "content": [
                    {
                      "type": "paragraph",
                      "content": [{"type": "text", "text": "Sub-feature B"}]
                    }
                  ]
                }
              ]
            }
          ]
        }
      ]
    },
    {
      "type": "heading",
      "attrs": {"level": 3},
      "content": [
        {"type": "text", "text": "Installation"}
      ]
    },
    {
      "type": "codeBlock",
      "attrs": {"language": "bash"},
      "content": [
        {
          "type": "text",
          "text": "npm install my-package"
        }
      ]
    },
    {
      "type": "paragraph",
      "content": [
        {"type": "text", "text": "For more info, visit "},
        {
          "type": "text",
          "text": "our website",
          "marks": [
            {
              "type": "link",
              "attrs": {"href": "https://example.com"}
            }
          ]
        },
        {"type": "text", "text": "."}
      ]
    },
    {
      "type": "panel",
      "attrs": {"panelType": "note"},
      "content": [
        {
          "type": "paragraph",
          "content": [
            {
              "type": "text",
              "text": "Note",
              "marks": [{"type": "strong"}]
            },
            {"type": "text", "text": ": This is still in beta."}
          ]
        }
      ]
    },
    {
      "type": "table",
      "content": [
        {
          "type": "tableRow",
          "content": [
            {
              "type": "tableHeader",
              "content": [
                {
                  "type": "paragraph",
                  "content": [{"type": "text", "text": "Command"}]
                }
              ]
            },
            {
              "type": "tableHeader",
              "content": [
                {
                  "type": "paragraph",
                  "content": [{"type": "text", "text": "Description"}]
                }
              ]
            }
          ]
        },
        {
          "type": "tableRow",
          "content": [
            {
              "type": "tableCell",
              "content": [
                {
                  "type": "paragraph",
                  "content": [
                    {
                      "type": "text",
                      "text": "start",
                      "marks": [{"type": "code"}]
                    }
                  ]
                }
              ]
            },
            {
              "type": "tableCell",
              "content": [
                {
                  "type": "paragraph",
                  "content": [{"type": "text", "text": "Start server"}]
                }
              ]
            }
          ]
        },
        {
          "type": "tableRow",
          "content": [
            {
              "type": "tableCell",
              "content": [
                {
                  "type": "paragraph",
                  "content": [
                    {
                      "type": "text",
                      "text": "test",
                      "marks": [{"type": "code"}]
                    }
                  ]
                }
              ]
            },
            {
              "type": "tableCell",
              "content": [
                {
                  "type": "paragraph",
                  "content": [{"type": "text", "text": "Run tests"}]
                }
              ]
            }
          ]
        }
      ]
    }
  ]
}
```

## Common Patterns

### README.md to Confluence

1. **Extract title** from first H1
2. **Convert sections** to H2/H3
3. **Preserve code blocks** with language tags
4. **Convert tables** for command reference
5. **Add info panels** for warnings/notes
6. **Link to external resources**

### API Documentation

1. **Endpoint sections** as H2
2. **Parameters** as tables
3. **Code examples** with language highlighting
4. **Response schemas** as code blocks
5. **Status codes** as tables

### Architecture Docs

1. **Diagrams** as images
2. **Decision records** with info panels
3. **Component lists** as bullet lists
4. **Tech stack tables**

## Limitations and Workarounds

### Not Directly Supported

**Markdown feature → Workaround**:

- **HTML tags** → Convert to ADF equivalent or plain text
- **Footnotes** → Use numbered references in text
- **Definition lists** → Use tables or headings
- **Complex nested structures** → Flatten or use expand sections

### Confluence Enhancements

Add these Confluence-specific elements to improve readability:

1. **Info panels** for important notes
2. **Expand sections** for optional details
3. **Status badges** for project status
4. **Task lists** for checklists
5. **Color coding** in tables

## How I'll Help

When converting Markdown to ADF, I will:

1. **Parse the Markdown**: Understand structure and content
2. **Convert to ADF**: Build proper JSON structure
3. **Enhance for Confluence**: Add panels, badges, etc.
4. **Validate**: Ensure valid ADF format
5. **Create/Update**: Use `/confluence-create-page` or `/confluence-update-page`
6. **Preview**: Show you what will be created

## Example Interaction

**You**: "Convert my README.md to a Confluence page"

**Me**: "I'll convert your README.md to Confluence ADF format.

[Reads README.md]

I see:
- Title: "My Project"
- Sections: Overview, Installation, Usage, API Reference
- Code blocks in bash and javascript
- A table of CLI commands
- Some warnings/notes

Converting to ADF with enhancements:
- Converting code blocks with proper language tags
- Tables for command reference
- Info panels for warnings
- Links preserved

Ready to create the Confluence page. Which space should I use?"

**You**: "Space 123456"

**Me**: [Uses `/confluence-create-page` with converted ADF]
"Created page 'My Project' in space 123456!
Link: https://your-domain.atlassian.net/wiki/spaces/123456/pages/..."
