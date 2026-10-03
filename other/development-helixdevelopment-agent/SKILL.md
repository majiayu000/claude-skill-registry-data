---
name: documentation
description: Write effective technical documentation including READMEs, API docs, architecture decisions, and inline code documentation.
triggers:
- /documentation
- /docs
---

# Technical Documentation Writing

This skill guides you through creating effective technical documentation that helps users understand, use, and contribute to your software.

## When to use this skill

Use this skill when you need to:
- Write README files for projects
- Document APIs and interfaces
- Create architecture documentation
- Write inline code documentation
- Maintain project wikis or knowledge bases

## Prerequisites

- Understanding of the target audience
- Knowledge of the system being documented
- Familiarity with documentation tools (Markdown, Sphinx, Docusaurus)
- Access to code and subject matter experts

## Guidelines

### Documentation Types

**README.md** - Project entry point
- Project description and purpose
- Installation instructions
- Quick start guide
- Links to detailed documentation
- Contribution guidelines

**API Documentation** - Interface reference
- Endpoint descriptions
- Request/response examples
- Authentication details
- Error codes and handling

**Architecture Decision Records (ADRs)** - Design decisions
- Context and problem statement
- Decision drivers
- Considered options
- Decision outcome
- Consequences

**Code Comments** - Inline explanations
- Why, not what (code shows what)
- Complex algorithms
- Non-obvious behavior
- Public API documentation

### README Structure

```markdown
# Project Name

Brief description of what the project does and its main purpose.

## Features

- Core feature 1
- Core feature 2
- Core feature 3

## Installation

```bash
# Clone the repository
git clone https://github.com/user/repo.git

# Install dependencies
npm install

# Configure environment
cp .env.example .env
```

## Quick Start

```bash
# Run the application
npm start
```

Visit `http://localhost:3000` to see the application.

## Documentation

- [API Reference](docs/api.md)
- [Architecture](docs/architecture.md)
- [Contributing](CONTRIBUTING.md)

## License

[MIT](LICENSE)
```

### API Documentation

**OpenAPI/Swagger Example**
```yaml
openapi: 3.0.0
info:
  title: Orders API
  version: 1.0.0
paths:
  /orders:
    post:
      summary: Create a new order
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required: [customer_id, items]
              properties:
                customer_id:
                  type: integer
                  description: ID of the customer
                items:
                  type: array
                  items:
                    type: object
                    properties:
                      product_id:
                        type: integer
                      quantity:
                        type: integer
      responses:
        201:
          description: Order created successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Order'
```

### Code Documentation

**Docstring Standards**
```python
def process_payment(order_id: int, amount: Decimal) -> PaymentResult:
    """
    Process a payment for the given order.
    
    Args:
        order_id: The unique identifier of the order
        amount: The payment amount (must be positive)
    
    Returns:
        PaymentResult containing transaction_id and status
    
    Raises:
        OrderNotFoundError: If the order doesn't exist
        InvalidAmountError: If amount is negative or zero
        PaymentGatewayError: If the payment processor fails
    
    Example:
        >>> result = process_payment(123, Decimal("99.99"))
        >>> print(result.status)
        'success'
    """
```

**Documentation Principles**
- Document intent, not implementation
- Keep examples runnable
- Update docs with code changes
- Use consistent terminology

### Architecture Documentation

**C4 Model Approach**
1. **Context Diagram** - System in its environment
2. **Container Diagram** - High-level tech stack
3. **Component Diagram** - Major building blocks
4. **Code Diagram** - Detailed implementation

**ADR Template**
```markdown
# ADR 001: Use PostgreSQL for Primary Database

## Status
Accepted

## Context
We need a relational database for our application data.

## Decision
We will use PostgreSQL as our primary database.

## Consequences
- Team familiarity with PostgreSQL
- ACID compliance for data integrity
- Need to manage database migrations
```

### Documentation Best Practices

**Writing Style**
- Use active voice
- Be concise and specific
- Include code examples
- Use diagrams for complex concepts
- Define acronyms on first use

**Maintenance**
- Review docs with code reviews
- Version documentation with code
- Track documentation issues
- Regular cleanup of outdated content

**Accessibility**
- Use semantic Markdown
- Add alt text to images
- Ensure good contrast in diagrams
- Provide text alternatives

## Examples

See the `examples/` directory for:
- `readme-template.md` - Complete README template
- `api-docs-example/` - API documentation samples
- `adr-template.md` - Architecture Decision Record format
- `style-guide.md` - Documentation style guidelines

## References

- [Documentation as Code](https://www.writethedocs.org/guide/docs-as-code/)
- [Markdown Guide](https://www.markdownguide.org/)
- [Diátaxis Framework](https://diataxis.fr/)
- [Write the Docs](https://www.writethedocs.org/)
- [C4 Model](https://c4model.com/)
