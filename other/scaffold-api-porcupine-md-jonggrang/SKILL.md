---
name: scaffold-api
description: Generate API endpoint with route, controller, validation, and tests
type: scaffold
project_types: [web-app, api]
trigger: "create endpoint, create API, add route"
inputs:
  - name: name
    description: Resource/endpoint name (e.g. users, products, orders)
    required: true
  - name: method
    description: HTTP method (GET, POST, PUT, PATCH, DELETE)
    required: false
    default: "CRUD"
  - name: path
    description: API path prefix
    required: false
    default: "/api/{{input.name}}"
---

## Context

Project {{project_name}} uses stack {{stack}}.
You will create an API endpoint for the resource "{{input.name}}".

Read AGENTS.md for conventions that apply to this project.
Read existing route files to understand the patterns used.

## Instructions

1. **Analyze existing patterns**
   - Read existing route files in the project
   - Identify patterns: router setup, middleware usage, error handling, response format
   - Follow conventions defined in AGENTS.md

2. **Create route file**
   - Path: according to project convention (usually `src/routes/{{input.name}}.ts`)
   - Implement {{input.method}} endpoints
   - If CRUD: GET (list), GET/:id (detail), POST (create), PUT/:id (update), DELETE/:id (delete)

3. **Create validation schema**
   - Path: according to convention (e.g. `src/validators/{{input.name}}.ts`)
   - Use the validation library already used in the project (Zod, Joi, etc.)
   - Validate all input fields

4. **Create service/controller** (if the project uses this pattern)
   - Business logic separate from route handler
   - Database operations via existing ORM/query builder

5. **Register route**
   - Add to router registry / main app file
   - Ensure path and middleware are correct

6. **Create tests**
   - Path: according to convention (e.g. `tests/{{input.name}}.test.ts`)
   - Test cases:
     - Happy path for each endpoint
     - Validation errors (invalid input)
     - Not found (for endpoints with :id)
     - Auth/permission errors (if auth middleware exists)

## Script

```bash
#!/bin/bash
# Detect project structure
if [ -d "src/routes" ]; then
  echo "Route directory: src/routes/"
elif [ -d "src/api" ]; then
  echo "Route directory: src/api/"
elif [ -d "routes" ]; then
  echo "Route directory: routes/"
fi

# Detect validation library
if grep -q "zod" package.json 2>/dev/null; then
  echo "Validation: Zod"
elif grep -q "joi" package.json 2>/dev/null; then
  echo "Validation: Joi"
elif grep -q "class-validator" package.json 2>/dev/null; then
  echo "Validation: class-validator"
fi
```

## Validation

- [ ] Route file created and follows existing pattern
- [ ] Validation schema complete for all input fields
- [ ] Route registered in main app/router
- [ ] Tests created and passing
- [ ] Typecheck passing
- [ ] Lint passing
- [ ] Response format consistent with existing endpoints
