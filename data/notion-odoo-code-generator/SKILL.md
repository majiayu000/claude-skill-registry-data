---
name: "Notion & Odoo Code Generator"
description: "Generate production-ready code for Notion API integrations and Odoo 18 modules with OCA compliance"
version: "1.0.0"
author: "SuperClaude Framework"
category: "development"
tags: ["notion", "odoo", "typescript", "python", "api", "oca", "owl"]
---

# Notion & Odoo Code Generator

A specialized Claude Skill for generating production-ready code for:
- **Notion API** integrations and workspace management
- **Odoo 18** module development with OCA compliance
- **Notion Clone** enhancement and feature additions

## What This Skill Does

### Notion Capabilities
- Generate TypeScript code for Notion API operations
- Create database queries with proper filtering and pagination
- Build page and block manipulation functions
- Implement webhook handlers and sync services
- Design integration patterns (API clients, cache layers, rate limiters)
- Enhance the notion-clone project at `/Users/tbwa/notion-clone/`

### Odoo Capabilities
- Create OCA-compliant Odoo 18 modules
- Generate Python models with proper field definitions
- Build XML views (form, tree, search, kanban, calendar)
- Implement OWL (Odoo Web Library) components
- Create controllers with HTTP/JSON-RPC routes
- Write XML-RPC client code for external integrations
- Follow Odoo 18 and OCA best practices

## When to Use This Skill

### Use for Notion:
- "Create a Notion database with CRM properties"
- "Query all tasks due this week from Notion"
- "Build a sync service between Notion and Supabase"
- "Add templates feature to notion-clone"
- "Implement database views in notion-clone"

### Use for Odoo:
- "Create an Odoo 18 module for inventory management"
- "Generate a Python model with compute fields and constraints"
- "Build a form view with statusbar and chatter"
- "Create an OWL component for the frontend"
- "Implement XML-RPC client to sync with external system"

### Don't Use for:
- General programming questions unrelated to Notion or Odoo
- Infrastructure setup (use DevOps skills instead)
- UI design without code generation
- Database administration

## Code Generation Standards

### TypeScript (Notion)
- Full type definitions from `@notionhq/client`
- Comprehensive error handling with try-catch
- Rate limiting for bulk operations
- Pagination support
- JSDoc comments
- Environment variable validation

### Python (Odoo)
- PEP 8 compliance
- OCA code quality standards
- Proper field types and constraints
- `@api.depends` for computed fields
- Comprehensive docstrings
- Unit test stubs

### XML (Odoo Views)
- Proper indentation and formatting
- Semantic field grouping
- Appropriate widget usage
- Statusbar for state fields
- Chatter integration where applicable

### JavaScript (OWL Components)
- Modern ES6+ syntax
- Proper component lifecycle
- Service injection with `useService`
- State management with `useState`
- Error boundaries and loading states

## Examples

### Example 1: Notion Database Query
**Input:** "Query Notion database for high-priority tasks not yet completed"

**Output:**
```typescript
import { Client } from '@notionhq/client'

const notion = new Client({
  auth: process.env.NOTION_API_KEY,
})

async function queryHighPriorityTasks(databaseId: string) {
  try {
    const response = await notion.databases.query({
      database_id: databaseId,
      filter: {
        and: [
          {
            property: 'Priority',
            select: { equals: 'High' }
          },
          {
            property: 'Status',
            select: { does_not_equal: 'Complete' }
          }
        ]
      },
      sorts: [
        {
          property: 'Due Date',
          direction: 'ascending'
        }
      ]
    })
    return response.results
  } catch (error) {
    console.error('Failed to query tasks:', error)
    throw error
  }
}
```

### Example 2: Odoo Model Definition
**Input:** "Create an Odoo model for project tasks with name, description, assigned user, and status"

**Output:**
```python
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ProjectTask(models.Model):
    _name = 'project.task.custom'
    _description = 'Project Task'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'priority desc, id desc'

    name = fields.Char(
        string='Task Name',
        required=True,
        tracking=True,
    )
    description = fields.Text(string='Description')
    user_id = fields.Many2one(
        'res.users',
        string='Assigned To',
        default=lambda self: self.env.user,
        tracking=True,
    )
    state = fields.Selection([
        ('draft', 'New'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', required=True, tracking=True)
    priority = fields.Selection([
        ('0', 'Low'),
        ('1', 'Normal'),
        ('2', 'High'),
    ], string='Priority', default='1')

    @api.constrains('name')
    def _check_name(self):
        for record in self:
            if len(record.name) < 3:
                raise ValidationError('Task name must be at least 3 characters')
```

### Example 3: OWL Component
**Input:** "Create an OWL component to display and edit a task"

**Output:**
```javascript
/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export class TaskEditor extends Component {
    static template = "module_name.TaskEditorTemplate";
    static props = {
        taskId: Number,
    };

    setup() {
        this.orm = useService("orm");
        this.notification = useService("notification");
        this.state = useState({
            task: null,
            loading: true,
        });

        onWillStart(async () => {
            await this.loadTask();
        });
    }

    async loadTask() {
        this.state.loading = true;
        try {
            const [task] = await this.orm.read(
                "project.task.custom",
                [this.props.taskId],
                ["name", "description", "user_id", "state", "priority"]
            );
            this.state.task = task;
        } catch (error) {
            this.notification.add("Failed to load task", {
                type: "danger",
            });
        } finally {
            this.state.loading = false;
        }
    }

    async onSave() {
        try {
            await this.orm.write(
                "project.task.custom",
                [this.props.taskId],
                {
                    name: this.state.task.name,
                    description: this.state.task.description,
                }
            );
            this.notification.add("Task saved", { type: "success" });
        } catch (error) {
            this.notification.add("Save failed", { type: "danger" });
        }
    }
}
```

## Environment Variables

### Notion
```bash
NOTION_API_KEY=secret_xxxxxxxxxxxxx
NOTION_DATABASE_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx  # Optional
NOTION_PAGE_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx      # Optional
```

### Odoo
```bash
ODOO_URL=http://localhost:8069
ODOO_DB=mydb
ODOO_USERNAME=admin         # For XML-RPC
ODOO_PASSWORD=admin         # For XML-RPC
ODOO_API_KEY=xxxxxxxxxxxxx  # Alternative to username/password
```

## Best Practices

### Notion
✅ Use TypeScript with full type definitions
✅ Implement proper error handling
✅ Add rate limiting for bulk operations
✅ Handle pagination correctly
✅ Validate API responses
✅ Include JSDoc comments
✅ Use environment variables for credentials

### Odoo
✅ Follow OCA guidelines and structure
✅ Use proper Python type hints
✅ Add comprehensive docstrings
✅ Implement proper access rights
✅ Include unit tests
✅ Follow PEP 8 style guide
✅ Use `@api.depends` for computed fields
✅ Add proper `_sql_constraints`

## Output Format

All responses include:

1. **Solution**: Brief explanation of the approach
2. **Code**: Production-ready code with comments
3. **Usage Example**: How to use the generated code
4. **Environment Setup**: Required configuration
5. **Error Handling**: How errors are handled
6. **Resources**: Links to relevant documentation

## Resources

### Notion
- [Official Notion API Docs](https://developers.notion.com/)
- [Notion SDK for JavaScript](https://github.com/makenotion/notion-sdk-js)
- [Notion Clone GitHub](https://github.com/jgtolentino/notion-clone.git)

### Odoo
- [Odoo 18 Documentation](https://www.odoo.com/documentation/18.0/)
- [Odoo GitHub](https://github.com/odoo/odoo)
- [OCA Guidelines](https://odoo-community.org/)
- [OWL Framework](https://github.com/odoo/owl)

## Version History

- **1.0.0** (2025-10-23): Initial release with Notion + Odoo support
  - Notion API integration code generation
  - Odoo 18 module scaffolding
  - OCA compliance
  - OWL component generation
  - Notion clone enhancement capabilities
