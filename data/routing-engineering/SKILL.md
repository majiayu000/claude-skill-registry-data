---
name: routing-engineering
description: >-
  Domain specialist for API routing, route discovery, middleware analysis, and parameter validation.
  Scope: route discovery patterns, automatic route detection, route mapping, middleware analysis, URL patterns, parameter validation, URL injection prevention.
  Excludes: backend business logic, database queries, security operations beyond URL injection, frontend routing.
  Triggers: "routing", "route", "URL pattern", "middleware", "parameter validation", "route discovery", "endpoint", "path", "slug".
---

# ROUTING_ENGINEERING

## DOMAIN EXPERTISE
- **Common Issues**: Route conflicts, missing route parameters, invalid middleware order, parameter validation issues, URL injection, slow routing, route versioning conflicts, route caching issues, missing error handlers, ambiguous routes
- **Common Mistakes**: Not validating route parameters, middleware order issues, overly complex route definitions, missing fallback routes, inconsistent URL patterns, not using HTTP method constraints, not handling trailing slashes, missing route aliases
- **Related Patterns**: RESTful URL conventions, resource-based routing, nested routes, route versioning, route aliases, middleware chaining, request/response pipeline, parameter validation, query string handling, slug generation
- **Problematic Patterns**: God router, catch-all routes everywhere, middleware conflicts, route explosion, dynamic routes without validation, missing 404 handling, missing 500 error handling
- **URL Injection**: SQL injection in route parameters, path traversal attacks, SSRF via route parameters, open redirect vulnerabilities
- **Parameter Validation**: Type checking, format validation, sanitization, allowlist/blocklist validation, length limits, custom validators
- **Middleware Analysis**: Middleware chain ordering, request/response modification, middleware conflicts, authentication/authorization placement, error handling middleware, logging middleware, rate limiting middleware

## MODE DETECTION
- **WRITE Mode**: Keywords: ["create", "generate", "write", "build", "implement", "add", "new", "create route", "add endpoint", "design URL pattern"]
- **REVIEW Mode**: Keywords: ["review", "analyze", "audit", "check", "find issues", "route review", "URL pattern review", "middleware analysis", "parameter validation review"]

## LOADING STRATEGY
### Write Mode (Progressive)
Load patterns based on routing requirements:
- Route discovery questions -> Load `@discovery/ROUTE-DISCOVERY.md`
- Middleware questions -> Load `@middleware/MIDDLEWARE-ANALYSIS.md`
- URL pattern questions -> Load `@validation/URL-PATTERNS.md`
- Parameter validation -> Load `@validation/PARAMETER-VALIDATION.md`

### Review Mode (Exhaustive)
Load comprehensive checklists:
- IF route review requested -> Load all routing patterns
- IF middleware review requested -> Load `@middleware/MIDDLEWARE-ANALYSIS.md`
- IF security review requested -> Load `@validation/PARAMETER-VALIDATION.md`

### Progressive Loading (Write Mode)
- **IF** request mentions "route discovery", "find routes", "endpoint listing" -> READ FILE: `@discovery/ROUTE-DISCOVERY.md`
- **IF** request mentions "middleware", "middleware chain", "request/response pipeline" -> READ FILE: `@middleware/MIDDLEWARE-ANALYSIS.md`
- **IF** request mentions "URL pattern", "RESTful URL", "slug" -> READ FILE: `@validation/URL-PATTERNS.md`
- **IF** request mentions "parameter validation", "type checking", "sanitization" -> READ FILE: `@validation/PARAMETER-VALIDATION.md`

### Comprehensive Loading (Review Mode)
- **IF** request mentions "review", "audit", "analyze" -> READ FILES: All routing patterns
- **IF** request mentions "security review" -> Load `@validation/PARAMETER-VALIDATION.md`, URL pattern patterns
- **IF** request mentions "middleware issues" -> Load `@middleware/MIDDLEWARE-ANALYSIS.md`

## CONTEXT DETECTION
### Framework Detection
- **Laravel**: routes/web.php, routes/api.php, `Route::`, artisan route:list
- **Symfony**: config/routes.yaml, src/Controller/, @Route annotations, bin/console debug:router
- **Django**: urls.py, urlpatterns, path(), include()
- **Express**: app.get(), app.post(), app.use(), Router()
- **NestJS**: @Controller(), @Get(), @Post(), @Controller decoration
- **Spring Boot**: @RequestMapping, @GetMapping, @PostMapping, @RestController
- **Flask**: @app.route(), Flask(__name__), Blueprint()
- **FastAPI**: @app.get(), @app.post(), APIRouter()
- **Go**: http.HandleFunc(), http.ServeMux(), mux.Router()
- **Ruby on Rails**: config/routes.rb, resources, root
- **ASP.NET Core**: [HttpGet], [Route], MapControllerRoute()

### API Style Detection
- **REST API**: Resource-based routes, HTTP methods (GET, POST, PUT, DELETE), /api/v1/ patterns
- **GraphQL**: /graphql endpoint, schema queries, mutations
- **gRPC**: Protocol Buffers, service definitions
- **WebSocket**: /ws, /socket.io endpoints, WebSocket upgrades

### Version Detection
- **URL Path Versioning**: /api/v1/users, /api/v2/users
- **Header Versioning**: Accept: application/vnd.api.v1+json
- **Query Parameter Versioning**: /api/users?version=1

## EXECUTION PROTOCOL

### Phase 1: Clarification
1. **Detect Mode**: WRITE vs REVIEW based on keywords
2. **Detect Context**: Framework, API style, versioning strategy
3. **Load Patterns**: Progressive (write) or Exhaustive (review)
4. **Detect Multi-Domain**: Check if additional skills needed (database, security, API)

### Phase 2: Planning
1. Load relevant routing pattern references
2. Design routes according to framework conventions
3. Apply parameter validation
4. Implement middleware chains with proper ordering
5. Create RESTful URL patterns
6. Follow framework-specific routing patterns
7. Prevent URL injection vulnerabilities

### Phase 3: Execution
1. Load all routing checklist references
2. Systematically check each category:
   - Route discovery (missing routes, conflicts)
   - Middleware analysis (ordering, conflicts, missing middleware)
   - URL patterns (RESTful compliance, inconsistent patterns)
   - Parameter validation (type checking, sanitization)
   - Security (URL injection, path traversal)
3. Provide prioritized issues with severity levels

### Phase 4: Validation
- Verify routes follow framework conventions
- Check middleware ordering is correct
- Ensure parameter validation is comprehensive
- Validate URL patterns are RESTful
- Check for URL injection vulnerabilities
- Check for cross-references (MUST be within skill only)


### Write Mode Output
```markdown
## Route Implementation: [Endpoint/Resource]

### Framework: [Laravel/Symfony/Django/Express/NestJS/etc.]

### Route Definition
```language
[Framework-specific route definition]
```

### Middleware Chain
- [Middleware 1]: [Purpose]
- [Middleware 2]: [Purpose]
- [Middleware 3]: [Purpose]

### Parameter Validation
- [Parameter]: [Type], [Validation rules]

### URL Pattern
- [RESTful URL]: [Description]
- [Slug generation]: [If applicable]

### Related Patterns
@discovery/[specific-pattern].md
```

### Review Mode Output
```markdown
## Routing Review Report

### Critical Issues
1. **[Issue Name]**: [File:line]
   - Severity: CRITICAL
   - Category: [Route Conflict/Middleware/Security/Parameter Validation]
   - Description: [Issue details]
   - Impact: [Routing failure / Security vulnerability / Performance issue]
   - Fix: [Recommended action]
   - Reference: @discovery/[specific-pattern].md or @validation/[specific-pattern].md

### High Priority Issues
[Same format as Critical]

### Medium Priority Issues
[Same format as Critical]

### Low Priority Issues
[Same format as Critical]

### Route Discovery Issues
- **Missing Routes**: [Routes that should exist]
- **Route Conflicts**: [Conflicting route definitions]
- **Ambiguous Routes**: [Routes that match too broadly]

### Middleware Analysis
- **Order Issues**: [Middleware in wrong order]
- **Conflicts**: [Middleware conflicts]
- **Missing Middleware**: [Required middleware missing]

### URL Pattern Issues
- **RESTful Compliance**: [Non-RESTful patterns]
- **Inconsistent Patterns**: [Inconsistent URL structures]
- **Missing Versioning**: [No version strategy]

### Parameter Validation Issues
- **Missing Validation**: [Parameters not validated]
- **Weak Validation**: [Insufficient validation rules]
- **Type Issues**: [Type checking problems]

### Security Issues
- **URL Injection**: [Potential injection vulnerabilities]
- **Path Traversal**: [Path traversal risks]
- **Open Redirects**: [Open redirect vulnerabilities]

### Recommendations
1. [Routing improvement]
2. [Middleware reordering]
3. [Parameter validation enhancement]
4. [URL pattern improvement]

