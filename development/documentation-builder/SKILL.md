---
name: "Documentation Builder"
description: "Generates professional API documentation, user guides, and architectural documentation from code and specifications."
---

# Documentation Builder Skill

## Overview

The Documentation Builder Skill transforms your codebase and specifications into professional, well-structured documentation. It analyzes your code, APIs, and architecture, then generates:

- **API Documentation** - OpenAPI-style reference with authentication, endpoints, errors
- **User Guides** - Getting started, tutorials, how-tos
- **Architecture Documentation** - System design, data flows, component relationships
- **Setup Guides** - Installation, configuration, deployment instructions

**When to use this skill**:
- Starting a new project and need documentation foundation
- Updating documentation to match code changes
- Converting code into professional API reference
- Creating user onboarding materials
- Generating architectural documentation

## Quick Start

Tell the Documentation Builder what you need:

```
"Create API documentation for our REST endpoints including:
- Authentication (JWT)
- All CRUD operations
- Error responses
- Rate limiting info
- Code examples in Python and JavaScript"
```

The skill analyzes your code and generates:
1. Structured markdown documentation
2. Code examples in requested languages
3. Table of contents and navigation
4. Diagrams (if complexity warrants)

## Documentation Types

### API Documentation

**Generated sections**:
- Overview and base URL
- Authentication methods (OAuth, JWT, API Key)
- Available endpoints (organized by resource)
- Request/response schemas
- Error codes and messages
- Rate limits
- Code examples (Python, JavaScript, cURL)
- WebSocket/real-time info (if applicable)

**Quality standards**:
- ✅ All endpoints documented
- ✅ All parameters explained
- ✅ All error codes covered
- ✅ Multiple code examples per endpoint
- ✅ Common workflows documented

**Output formats**:
- Markdown (for GitHub, GitBook)
- OpenAPI/Swagger (for tooling)
- HTML (for hosting)
- PDF (for distribution)

### User Guides

**Typical sections**:
1. **Getting Started**
   - Installation/setup
   - First run/quick tutorial
   - Common first tasks

2. **Core Concepts**
   - Architecture overview
   - Key terminology
   - Mental models

3. **How-To Guides**
   - Authentication setup
   - Common workflows
   - Troubleshooting
   - Best practices

4. **Advanced Topics**
   - Configuration options
   - Performance tuning
   - Customization
   - Extending functionality

5. **Reference**
   - Configuration reference
   - Environment variables
   - Command reference
   - API reference (if applicable)

### Architecture Documentation

**Typically includes**:
- System overview diagram
- Component relationships
- Data flow diagrams
- Deployment architecture
- Technology stack
- Database schema (if applicable)
- Security considerations
- Scalability approach
- Disaster recovery plan

**Quality standards**:
- ✅ Clear system boundaries
- ✅ Component responsibilities documented
- ✅ Data flow clear and accurate
- ✅ Technology choices explained
- ✅ Future scalability addressed

## Usage Examples

### Example 1: API Documentation

```
Input:
"Generate API documentation for our Flask REST API with:
- 8 endpoints (CRUD on two resources)
- JWT authentication
- JSON request/response
- Error handling
- Include Python and JavaScript examples"

Process:
1. Analyze Flask route definitions
2. Extract endpoint signatures
3. Parse request/response validation
4. Generate OpenAPI spec
5. Create markdown with examples
6. Format for multiple platforms

Output:
- api-documentation.md (complete reference)
- openapi.json (machine-readable spec)
- api-docs.html (hosted version)
- api-docs.pdf (downloadable version)
```

### Example 2: Getting Started Guide

```
Input:
"Create a 'Getting Started' guide for developers setting up
our development environment"

Process:
1. Analyze setup scripts and configuration
2. Identify prerequisites and dependencies
3. Document installation steps
4. Create first-run tutorial
5. Add common gotchas and solutions
6. Include troubleshooting section

Output:
- getting-started.md
- Inline code examples
- Screenshots/diagrams
- Video tutorial outline
```

### Example 3: Architecture Documentation

```
Input:
"Document our microservices architecture including:
- 5 services
- Kafka message queue
- PostgreSQL database
- Redis cache
- Load balancing approach"

Process:
1. Analyze service definitions
2. Map service boundaries
3. Document data flows
4. Create architecture diagram
5. Explain technology choices
6. Document deployment approach
7. Plan for scalability

Output:
- architecture.md (comprehensive overview)
- service-diagram.png (visual representation)
- data-flow.png (data pipeline)
- deployment.md (deployment guide)
```

## Advanced Features

### Multi-Format Output

Generate documentation in multiple formats simultaneously:
- **Markdown** - Git-friendly, searchable
- **OpenAPI/Swagger** - Automated tooling
- **HTML** - Web hosting
- **PDF** - Downloadable/offline
- **Docusaurus** - Site generation ready
- **MkDocs** - Wiki generation ready

### Language-Specific Examples

Auto-generate code examples in multiple languages:
- Python
- JavaScript/TypeScript
- Java
- Go
- C#
- Ruby
- cURL/Bash

### Automatic Diagram Generation

Creates diagrams for complex systems:
- Architecture diagrams
- Data flow diagrams
- Entity relationship diagrams
- Deployment topology diagrams
- Sequence diagrams (for workflows)

### Maintenance Documentation

Keeps documentation in sync:
- Update signatures as code changes
- Regenerate examples
- Version documentation
- Create changelogs

## Best Practices

### 1. Clear Specifications
Provide context so skill understands your system:
```
"Create API docs for our payment processing endpoint
that uses Stripe, includes webhook handling, and PCI compliance notes"
```

Instead of:
```
"Document the payment API"
```

### 2. Code Examples Matter
Specify what examples would be most useful:
```
"Include examples showing:
- Successful payment processing flow
- Handling failed payments
- Setting up webhook handlers
- Common error scenarios"
```

### 3. Audience Awareness
Tell the skill who will read the docs:
```
"Write for mid-level Python developers who know requests
but may be new to async patterns"
```

### 4. Format for Purpose
Different docs serve different purposes:
- **API Docs**: For developers integrating your service
- **User Guides**: For end users
- **Architecture**: For team maintenance
- **Deployment**: For operations teams

### 5. Keep Current
Regenerate when significant changes occur:
- New endpoints or features
- Changed authentication approach
- Updated architecture
- Performance optimizations

## Customization Options

### Code Example Languages
Specify which languages to include:
```json
{
  "example_languages": ["python", "javascript", "typescript"],
  "include_curl": true,
  "include_postman": true
}
```

### Documentation Sections
Choose which sections to include:
```json
{
  "sections": [
    "overview",
    "authentication",
    "endpoints",
    "errors",
    "examples",
    "webhooks",
    "rate_limiting"
  ]
}
```

### Styling & Branding
Customize appearance:
```json
{
  "brand": {
    "company_name": "MyCompany",
    "logo_url": "https://...",
    "primary_color": "#007AFF"
  }
}
```

### Output Targets
Specify destination formats:
```json
{
  "outputs": [
    "markdown",
    "openapi.json",
    "html",
    "pdf",
    "docusaurus"
  ]
}
```

## Integration Points

### With Version Control
- Commit documentation updates
- Track documentation changes
- Maintain doc history
- Create documentation branches

### With CI/CD
- Generate docs on every commit
- Validate documentation accuracy
- Publish to GitHub Pages
- Create doc versioning

### With API Platforms
- Export to API Marketplaces
- Sync with API gateways
- Update API management tools
- Generate SDKs from docs

## Performance Considerations

- **Small API** (5-10 endpoints): 2-3 minutes
- **Medium API** (20-50 endpoints): 5-10 minutes
- **Large System** (complex architecture): 15-20 minutes

Estimated tokens:
- API documentation: 8K-12K
- User guide: 10K-15K
- Architecture docs: 12K-18K
- Combined full suite: 20K-30K

## Quality Checklist

✅ **Documentation is complete when**:
- All public APIs documented
- All parameters explained
- All error codes covered
- Examples are accurate and runnable
- Formatting is consistent
- Navigation is clear
- Search works (if applicable)
- Mobile-friendly (if web-based)
- Up-to-date with current code
- Includes troubleshooting guide

## Troubleshooting

### Missing Endpoints
**Cause**: Code structure not analyzed properly
**Solution**: Provide explicit endpoint list

### Unclear Examples
**Cause**: Context not specific enough
**Solution**: Provide actual code or detailed descriptions

### Formatting Issues
**Cause**: Complex markdown structure
**Solution**: Specify desired output format (Markdown, HTML, etc.)

---

For technical implementation details, see REFERENCE.md
