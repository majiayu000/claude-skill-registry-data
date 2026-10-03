---
name: azure-functions
description: Develop, deploy, and manage Azure Functions for serverless computing. Supports HTTP triggers, timers, queues, and event-driven architectures.
triggers:
- /azure functions
- /serverless
---

# Azure Functions Development

This skill guides you through building serverless applications with Azure Functions, from local development to production deployment.

## When to use this skill

Use this skill when you need to:
- Build event-driven serverless applications
- Create HTTP APIs without managing infrastructure
- Process messages from queues or event hubs
- Schedule recurring tasks with timer triggers
- Implement microservices architecture

## Prerequisites

- Azure Functions Core Tools (func --version)
- Azure CLI or Azure subscription access
- Programming language runtime (.NET, Node.js, Python, or Java)
- Storage account for function state (created automatically)

## Guidelines

### Function App Structure

Organize your Functions project following these patterns:

```
my-functions/
├── host.json                 # Global configuration
├── local.settings.json       # Local development settings (gitignored)
├── requirements.txt          # Python dependencies
└── MyFunction/
    ├── __init__.py          # Function entry point
    ├── function.json        # Binding configuration
    └── sample.dat           # Test data
```

### Trigger Types and Use Cases

**HTTP Triggers** - API endpoints and webhooks
```python
# Python example
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    name = req.params.get('name', 'World')
    return func.HttpResponse(f"Hello, {name}!")
```

**Timer Triggers** - Scheduled tasks (cron expressions)
- Format: `{second} {minute} {hour} {day} {month} {day-of-week}`
- Example: `0 30 9 * * 1-5` (9:30 AM weekdays)

**Queue Triggers** - Process messages from Azure Storage Queues
**Event Hub Triggers** - Real-time stream processing
**Blob Triggers** - React to file uploads

### Development Workflow

**Local Development**
```bash
# Create new function app
func init MyFunctionApp --python

# Create new function
cd MyFunctionApp
func new --name HttpExample --template "HTTP trigger"

# Run locally
func start

# Test locally
curl http://localhost:7071/api/HttpExample?name=Azure
```

**Deployment Options**
1. **VS Code Extension** - Right-click deploy
2. **Azure CLI** - `func azure functionapp publish <app-name>`
3. **GitHub Actions** - CI/CD pipeline
4. **Bicep/ARM** - Infrastructure as code

### Performance Optimization

**Cold Start Mitigation**
- Use Premium plan for latency-sensitive apps
- Enable Always On (Consumption plan limitation: can't avoid cold starts)
- Use pre-warmed instances in Premium plan

**Scaling Considerations**
- Design functions to be stateless
- Use output bindings instead of manual SDK calls
- Implement idempotency for queue processing
- Set appropriate maxConcurrentRequests

### Security Best Practices

- Use Managed Identity for service authentication
- Store secrets in Azure Key Vault
- Enable Application Insights for monitoring
- Implement input validation on HTTP triggers
- Use HTTPS only (enforced by default)

## Examples

See the `examples/` directory for:
- `http-trigger/` - REST API implementation
- `queue-trigger/` - Message processing function
- `timer-trigger/` - Scheduled maintenance tasks
- `deployment-bicep/` - Infrastructure as code templates

## References

- [Azure Functions documentation](https://docs.microsoft.com/azure/azure-functions/)
- [Functions triggers and bindings](https://docs.microsoft.com/azure/azure-functions/functions-triggers-bindings)
- [Best practices](https://docs.microsoft.com/azure/azure-functions/functions-best-practices)
- [Pricing and plans](https://docs.microsoft.com/azure/azure-functions/functions-scale)
