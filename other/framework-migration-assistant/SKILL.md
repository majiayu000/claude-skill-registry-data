---
name: framework-migration-assistant
description: Guide framework and library migrations (Express to Fastify, Angular to React, Spring MVC to Spring Boot, Django to FastAPI) with migration assessment.
---

# Framework Migration Assistant

Plan and execute framework and library migrations systematically. This skill covers migration assessment (should you migrate?), dependency mapping (what needs to change?), API translation (how do patterns map between frameworks?), incremental migration strategies (how to migrate without big-bang risk?), and coexistence patterns (how do old and new run side by side?).

## When to Use This Skill

Use this skill when you need to:

- Migrate from one web framework to another (Express to Fastify, Flask to FastAPI, Spring MVC to Spring Boot)
- Migrate frontend frameworks (Angular to React, jQuery to Vue, Create React App to Next.js)
- Upgrade a major framework version with breaking changes (Angular 14 to 17, Next.js 12 to 14, Django 3 to 5)
- Replace a deprecated library with its successor (Request to Axios, Moment.js to date-fns)
- Assess whether a migration is worth the effort
- Plan an incremental migration that minimizes disruption
- Run old and new framework code in parallel during transition
- Map API patterns and idioms between source and target frameworks

**Trigger phrases**: "migrate framework", "switch from X to Y", "framework migration", "upgrade framework", "replace library", "migration plan", "incremental migration", "coexistence pattern", "migration assessment"

## What This Skill Does

### Core Capabilities

- **Migration Assessment**: Evaluate cost, risk, and benefit of the proposed migration
- **Dependency Mapping**: Identify all dependencies on the source framework and their target equivalents
- **API Translation**: Map source framework patterns, APIs, and idioms to target framework equivalents
- **Incremental Migration Planning**: Design a phased migration that keeps the application functional throughout
- **Coexistence Patterns**: Configure old and new frameworks to run side by side
- **Testing Strategy**: Ensure feature parity through parallel testing during migration
- **Rollback Planning**: Define rollback procedures at each migration phase

### Migration Phases

```
Assessment -> Planning -> Setup -> Incremental Migration -> Validation -> Cleanup
    |            |          |              |                    |           |
    v            v          v              v                    v           v
  Go/No-Go   Roadmap    Scaffold    Migrate routes/       Feature      Remove
  decision   with deps  target      components one        parity       source
             mapping    project     at a time             testing      framework
```

## Instructions

### Phase 1: Migration Assessment

**Step 1.1: Evaluate migration drivers**

```yaml
migration_assessment:
  project: "e-commerce-api"
  source_framework: "Express.js 4.x"
  target_framework: "Fastify 4.x"

  drivers:
    - reason: "Performance requirements exceed Express capabilities"
      weight: high
      evidence: "Benchmarks show 2x throughput with Fastify for our workload"

    - reason: "TypeScript-first development"
      weight: medium
      evidence: "Fastify has built-in TypeScript support and schema validation"

    - reason: "JSON Schema validation built-in"
      weight: medium
      evidence: "Eliminates need for express-validator + Joi dependencies"

  risks:
    - risk: "Middleware ecosystem differences"
      severity: medium
      mitigation: "Audit all Express middleware and map to Fastify equivalents"

    - risk: "Team unfamiliarity with Fastify"
      severity: low
      mitigation: "Allocate 2-week learning sprint before migration begins"

    - risk: "Breaking change to internal APIs consumed by other services"
      severity: high
      mitigation: "Maintain API contract compatibility; migration is internal refactoring"
```

**Step 1.2: Inventory the migration surface**

```python
def inventory_framework_usage(codebase_path: str, framework: str) -> dict:
    """Inventory all usage of the source framework in the codebase."""
    usage = {
        "imports": [],
        "middleware": [],
        "routes": [],
        "plugins": [],
        "configuration": [],
        "test_utilities": [],
        "total_files_affected": 0,
    }

    framework_patterns = {
        "express": {
            "import": r"require\(['\"]express['\"]\)|from ['\"]express['\"]",
            "middleware": r"app\.use\(|router\.use\(",
            "routes": r"app\.(get|post|put|delete|patch)\(|router\.(get|post|put|delete|patch)\(",
            "config": r"app\.set\(|app\.enable\(|app\.disable\(",
        },
        "flask": {
            "import": r"from flask import|import flask",
            "middleware": r"@app\.before_request|@app\.after_request",
            "routes": r"@app\.route\(|@blueprint\.route\(",
            "config": r"app\.config\[",
        },
    }

    patterns = framework_patterns.get(framework.lower(), {})
    # ... scan codebase with patterns ...

    return usage
```

**Step 1.3: Calculate migration effort**

```python
def estimate_migration_effort(inventory: dict) -> dict:
    """Estimate the effort required for the migration."""
    # Effort multipliers per item type (in developer-hours)
    effort_per = {
        "routes": 0.5,          # Hours per route to migrate
        "middleware": 2.0,       # Hours per middleware
        "plugins": 4.0,          # Hours per plugin/integration
        "configuration": 1.0,    # Hours per config pattern
        "test_utilities": 1.5,   # Hours per test file
    }

    total_hours = 0
    breakdown = {}

    for item_type, count in inventory.items():
        if item_type in effort_per and isinstance(count, list):
            hours = len(count) * effort_per[item_type]
            breakdown[item_type] = {
                "count": len(count),
                "hours_each": effort_per[item_type],
                "total_hours": hours,
            }
            total_hours += hours

    # Add overhead for testing, review, and unexpected issues
    overhead_multiplier = 1.5
    total_with_overhead = total_hours * overhead_multiplier

    return {
        "breakdown": breakdown,
        "raw_hours": round(total_hours, 1),
        "with_overhead": round(total_with_overhead, 1),
        "estimated_sprints": round(total_with_overhead / 40, 1),  # Assuming 40h/sprint
        "team_size_recommendation": max(1, round(total_with_overhead / 80)),
    }
```

### Phase 2: Dependency Mapping

**Step 2.1: Map framework-specific dependencies to target equivalents**

Express to Fastify example:

```yaml
dependency_mapping:
  express_to_fastify:
    # Core framework
    - source: "express"
      target: "fastify"
      notes: "Core framework replacement"

    # Middleware equivalents
    - source: "cors (express middleware)"
      target: "@fastify/cors"
      notes: "Register as Fastify plugin instead of app.use()"

    - source: "helmet"
      target: "@fastify/helmet"
      notes: "Same security headers, different registration pattern"

    - source: "express-rate-limit"
      target: "@fastify/rate-limit"
      notes: "Plugin-based, similar configuration options"

    - source: "body-parser"
      target: "built-in"
      notes: "Fastify parses JSON and URL-encoded bodies by default"

    - source: "cookie-parser"
      target: "@fastify/cookie"
      notes: "Register as plugin"

    - source: "express-session"
      target: "@fastify/session"
      notes: "Combined with @fastify/cookie"

    - source: "multer (file upload)"
      target: "@fastify/multipart"
      notes: "Different API for file handling"

    - source: "passport"
      target: "@fastify/passport"
      notes: "Fastify-native passport adapter available"

    # No direct equivalent
    - source: "express-validator"
      target: "built-in JSON Schema validation"
      notes: "Fastify uses JSON Schema for route validation; no middleware needed"

    - source: "morgan (logging)"
      target: "pino (built-in)"
      notes: "Fastify uses pino logger by default; no middleware needed"
```

**Step 2.2: Identify dependencies without equivalents**

```python
def find_unmapped_dependencies(
    source_deps: list[str],
    mapping: list[dict],
) -> list[str]:
    """Find source dependencies that have no mapped target equivalent."""
    mapped_sources = {m["source"] for m in mapping}
    unmapped = [dep for dep in source_deps if dep not in mapped_sources]

    return unmapped
    # These require custom solutions or alternative approaches
```

### Phase 3: API Translation

**Step 3.1: Express to Fastify route translation**

```typescript
// EXPRESS: Route definition
// Source: src/routes/users.ts (Express)
import { Router, Request, Response, NextFunction } from "express";
import { body, validationResult } from "express-validator";

const router = Router();

router.get("/users/:id", async (req: Request, res: Response) => {
  try {
    const user = await UserService.findById(req.params.id);
    if (!user) {
      return res.status(404).json({ error: "User not found" });
    }
    res.json(user);
  } catch (error) {
    res.status(500).json({ error: "Internal server error" });
  }
});

router.post(
  "/users",
  [body("email").isEmail(), body("name").notEmpty()],
  async (req: Request, res: Response) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }
    const user = await UserService.create(req.body);
    res.status(201).json(user);
  }
);

export default router;
```

```typescript
// FASTIFY: Equivalent route definition
// Target: src/routes/users.ts (Fastify)
import { FastifyInstance, FastifyRequest, FastifyReply } from "fastify";

// JSON Schema for validation (replaces express-validator)
const createUserSchema = {
  body: {
    type: "object",
    required: ["email", "name"],
    properties: {
      email: { type: "string", format: "email" },
      name: { type: "string", minLength: 1 },
    },
  },
  response: {
    201: {
      type: "object",
      properties: {
        id: { type: "string" },
        email: { type: "string" },
        name: { type: "string" },
      },
    },
  },
};

export default async function userRoutes(fastify: FastifyInstance) {
  fastify.get<{ Params: { id: string } }>(
    "/users/:id",
    async (request, reply) => {
      const user = await UserService.findById(request.params.id);
      if (!user) {
        return reply.status(404).send({ error: "User not found" });
      }
      return user; // Fastify auto-serializes the return value
    }
  );

  fastify.post<{ Body: { email: string; name: string } }>(
    "/users",
    { schema: createUserSchema },
    async (request, reply) => {
      // Validation is automatic via schema; 400 returned if invalid
      const user = await UserService.create(request.body);
      return reply.status(201).send(user);
    }
  );
}
```

**Step 3.2: Flask to FastAPI route translation**

```python
# FLASK: Source
from flask import Flask, request, jsonify
from functools import wraps

app = Flask(__name__)

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"error": "Unauthorized"}), 401
        # Validate token...
        return f(*args, **kwargs)
    return decorated

@app.route("/users/<int:user_id>", methods=["GET"])
@require_auth
def get_user(user_id):
    user = UserService.find_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.to_dict())

@app.route("/users", methods=["POST"])
@require_auth
def create_user():
    data = request.get_json()
    if not data.get("email") or not data.get("name"):
        return jsonify({"error": "email and name required"}), 400
    user = UserService.create(data)
    return jsonify(user.to_dict()), 201
```

```python
# FASTAPI: Target
from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel, EmailStr

app = FastAPI()

# Pydantic model replaces manual validation
class CreateUserRequest(BaseModel):
    email: EmailStr
    name: str

class UserResponse(BaseModel):
    id: int
    email: str
    name: str

# Dependency injection replaces decorators
async def require_auth(authorization: str = Header(...)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Unauthorized")
    # Validate token...
    return authorization

@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, auth: str = Depends(require_auth)):
    user = await UserService.find_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/users", response_model=UserResponse, status_code=201)
async def create_user(data: CreateUserRequest, auth: str = Depends(require_auth)):
    # Validation is automatic via Pydantic model
    user = await UserService.create(data.dict())
    return user
```

**Step 3.3: Spring MVC to Spring Boot migration**

```java
// SPRING MVC: web.xml + XML configuration (source)
// web.xml
// <servlet>
//   <servlet-name>dispatcher</servlet-name>
//   <servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class>
// </servlet>

// applicationContext.xml
// <bean id="userService" class="com.example.service.UserServiceImpl"/>
// <bean id="dataSource" class="org.apache.commons.dbcp.BasicDataSource">
//   <property name="driverClassName" value="org.postgresql.Driver"/>
//   <property name="url" value="jdbc:postgresql://localhost/mydb"/>
// </bean>

@Controller
@RequestMapping("/users")
public class UserController {
    @Autowired
    private UserService userService;

    @RequestMapping(value = "/{id}", method = RequestMethod.GET)
    @ResponseBody
    public User getUser(@PathVariable Long id) {
        return userService.findById(id);
    }
}
```

```java
// SPRING BOOT: Auto-configuration + annotations (target)
@SpringBootApplication
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}

// application.yml replaces XML configuration
// spring:
//   datasource:
//     url: jdbc:postgresql://localhost/mydb
//     driver-class-name: org.postgresql.Driver

@RestController  // Replaces @Controller + @ResponseBody
@RequestMapping("/users")
public class UserController {
    private final UserService userService;

    // Constructor injection (preferred over @Autowired)
    public UserController(UserService userService) {
        this.userService = userService;
    }

    @GetMapping("/{id}")  // Replaces @RequestMapping with method
    public ResponseEntity<User> getUser(@PathVariable Long id) {
        return userService.findById(id)
            .map(ResponseEntity::ok)
            .orElse(ResponseEntity.notFound().build());
    }
}
```

### Phase 4: Incremental Migration Strategy

**Step 4.1: Set up the coexistence pattern**

Run both frameworks simultaneously during migration:

Express + Fastify coexistence (proxy pattern):

```typescript
// gateway.ts - Route traffic between Express and Fastify
import express from "express";
import { createProxyMiddleware } from "http-proxy-middleware";

const app = express();

// Migrated routes go to Fastify (running on port 3001)
const migratedRoutes = ["/api/v1/products", "/api/v1/categories"];

for (const route of migratedRoutes) {
  app.use(
    route,
    createProxyMiddleware({
      target: "http://localhost:3001",
      changeOrigin: true,
    })
  );
}

// Non-migrated routes stay on Express
app.use("/api/v1/users", usersRouter);
app.use("/api/v1/orders", ordersRouter);

app.listen(3000);
```

Flask + FastAPI coexistence (mount pattern):

```python
# main.py - Run both WSGI and ASGI apps
from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
from flask_app import create_flask_app

# New FastAPI app for migrated routes
fastapi_app = FastAPI()

# Mount Flask app for non-migrated routes
flask_app = create_flask_app()
fastapi_app.mount("/legacy", WSGIMiddleware(flask_app))

# Migrated routes on FastAPI
@fastapi_app.get("/api/v1/products")
async def list_products():
    return await ProductService.list_all()
```

**Step 4.2: Migrate route by route**

```yaml
migration_order:
  # Start with simple, low-risk routes
  - phase: 1
    routes:
      - "GET /api/health"
      - "GET /api/products"
      - "GET /api/products/:id"
    risk: low
    validation: "Compare response bodies between old and new"

  # Move to routes with middleware dependencies
  - phase: 2
    routes:
      - "POST /api/products"
      - "PUT /api/products/:id"
      - "DELETE /api/products/:id"
    risk: medium
    validation: "Run integration test suite against new implementation"

  # Migrate routes with complex middleware chains
  - phase: 3
    routes:
      - "POST /api/orders"
      - "GET /api/orders/:id"
      - "POST /api/payments"
    risk: high
    validation: "Full end-to-end testing, canary deployment"

  # Migrate remaining routes and remove old framework
  - phase: 4
    routes: "all remaining"
    risk: medium
    validation: "Feature parity testing, performance benchmarks"
```

**Step 4.3: Feature parity testing**

```typescript
// migration-parity.test.ts
// Run the same tests against both implementations to verify parity

describe("Migration Parity: GET /api/products", () => {
  const expressBaseUrl = "http://localhost:3000";
  const fastifyBaseUrl = "http://localhost:3001";

  it("should return identical response structure", async () => {
    const [expressRes, fastifyRes] = await Promise.all([
      fetch(`${expressBaseUrl}/api/products`),
      fetch(`${fastifyBaseUrl}/api/products`),
    ]);

    const expressBody = await expressRes.json();
    const fastifyBody = await fastifyRes.json();

    expect(expressRes.status).toBe(fastifyRes.status);
    expect(expressBody).toEqual(fastifyBody);
  });

  it("should return identical headers", async () => {
    const [expressRes, fastifyRes] = await Promise.all([
      fetch(`${expressBaseUrl}/api/products`),
      fetch(`${fastifyBaseUrl}/api/products`),
    ]);

    // Compare relevant headers (ignoring server-specific ones)
    const relevantHeaders = ["content-type", "cache-control"];
    for (const header of relevantHeaders) {
      expect(expressRes.headers.get(header)).toBe(
        fastifyRes.headers.get(header)
      );
    }
  });
});
```

### Phase 5: Validation and Cleanup

**Step 5.1: Performance comparison**

```bash
# Benchmark both implementations with identical load
# Using autocannon (Node.js) or wrk

# Express (old)
npx autocannon -c 100 -d 30 http://localhost:3000/api/products

# Fastify (new)
npx autocannon -c 100 -d 30 http://localhost:3001/api/products

# Compare: latency (p50, p95, p99), throughput (req/sec), error rate
```

**Step 5.2: Cleanup checklist**

```markdown
## Post-Migration Cleanup

- [ ] Remove source framework dependency from package.json / requirements.txt
- [ ] Remove source framework middleware and plugins
- [ ] Remove the coexistence proxy/gateway layer
- [ ] Remove migration parity tests (replace with standard integration tests)
- [ ] Update CI/CD pipeline configuration (if framework-specific steps exist)
- [ ] Update Dockerfile and deployment configuration
- [ ] Update documentation and README
- [ ] Update monitoring and alerting (framework-specific metrics may change)
- [ ] Archive or delete migration tooling scripts
- [ ] Communicate migration completion to dependent teams
```

**Step 5.3: Rollback procedure**

```yaml
rollback_plan:
  trigger_conditions:
    - "Error rate exceeds 1% in production"
    - "P95 latency exceeds 500ms (2x baseline)"
    - "Critical functionality regression confirmed"

  procedure:
    - step: "Revert the routing configuration to send traffic to the old framework"
      command: "kubectl rollout undo deployment/api-gateway"
      time: "< 2 minutes"

    - step: "Verify old framework is serving traffic correctly"
      command: "curl -s http://api.example.com/api/health"
      time: "< 1 minute"

    - step: "Investigate the root cause before re-attempting migration"
      owner: "Migration team"
      time: "Variable"
```

## Best Practices

- Always start with a thorough assessment before committing to migration; some migrations cost more than the benefit they deliver
- Migrate incrementally (route by route, component by component) rather than all at once; incremental migration is reversible, big-bang migration is not
- Maintain feature parity tests that run against both old and new implementations throughout the migration
- Keep the old framework running in production until the new framework has been validated under real traffic
- Map every dependency on the source framework before starting; undiscovered dependencies cause mid-migration surprises
- Use the coexistence pattern (proxy, adapter, or mount) so that partially migrated applications remain fully functional
- Automate the parity comparison between old and new implementations to catch regressions early
- Plan the migration order from simplest routes to most complex; early wins build team confidence and reveal migration patterns
- Document the API translation patterns (source idiom to target idiom) as a reference for the team during migration
- Set clear completion criteria and a timeline; migrations that drag on indefinitely lose momentum and accumulate maintenance burden for both frameworks

## Common Pitfalls

- **Rewriting business logic during migration**: A framework migration should change the framework layer, not the business logic. If you find yourself rewriting domain code, stop and separate the concerns first.
- **Migrating without tests**: If the existing code lacks tests, write them before migrating. Without tests, you cannot verify that the migration preserves behavior.
- **Ignoring framework-specific behavior differences**: Frameworks handle edge cases differently (error serialization, header normalization, streaming, WebSocket lifecycle). Test edge cases explicitly.
- **Underestimating middleware migration**: Middleware is often the hardest part of a framework migration because it involves cross-cutting concerns. Map all middleware early and plan for custom implementations where no direct equivalent exists.
- **Skipping the coexistence phase**: Attempting to migrate everything in a single release creates a binary success/failure scenario with no rollback path. Always use a coexistence pattern.
- **Neglecting performance validation**: The target framework may perform differently under your specific workload. Benchmark with realistic data and traffic patterns, not just synthetic benchmarks.
- **Forgetting about error handling differences**: Error middleware, exception handlers, and error response formats often differ significantly between frameworks. Audit error handling paths carefully.
- **Not communicating with consumers**: If your API has external consumers, verify that the migration does not change observable behavior (response format, header values, status codes, error shapes).
- **Leaving migration scaffolding in place**: The coexistence proxy, parity tests, and dual-framework configuration add complexity. Remove them promptly after migration is complete.
- **Migrating for the wrong reasons**: "The new framework is trendy" is not sufficient justification for a migration. Ensure there is a clear, measurable benefit that outweighs the migration cost.
