---
name: prd-from-codebase
description: >
  Generates a complete Product Requirements Document (PRD) in Markdown from an existing codebase.
  Use this skill whenever the user wants to document software without documentation, understand what a project does,
  generate a product document from code, map application features, identify system agents/roles,
  or mentions terms such as "PRD", "document the project", "generate product documentation",
  "what does this code do", "map features", "understand the codebase", "reverse PRD", or similar.
  The skill uses the available tools (bash, view, etc.) to autonomously explore the codebase
  before generating the document—the user does not need to manually paste any code.
metadata:
  author: Ronnasayd Machado - github.com/Ronnasayd
  version: "1.0.0"
---

# PRD from Codebase

Generates a structured, professional PRD from the autonomous analysis of an existing codebase, using the available tools to explore files, dependencies, routes, and project structure.

---

## Execution Flow

### PHASE 1 — Project Discovery

Before writing any part of the PRD, execute the discovery steps below in order. **Do not skip any steps.** Use `bash_tool` and `view` for each one.

#### 1.1 Locate the project

If the user provided a path, use it. Otherwise, search in this order:

```bash
ls /mnt/user-data/uploads/        # uploaded files
ls /home/claude/                  # working directory
find / -name "package.json" -o -name "requirements.txt" -o -name "go.mod" 2>/dev/null | head -20
```

#### 1.2 Map the high-level structure

```bash
find <ROOT> -type f \
  ! -path "*/node_modules/*" \
  ! -path "*/.git/*" \
  ! -path "*/dist/*" \
  ! -path "*/__pycache__/*" \
  ! -path "*/build/*" \
  ! -path "*/.next/*" \
  | head -120
```

Then use `view <ROOT>` to obtain a two-level tree view.

#### 1.3 Identify the technology stack

Read the relevant manifest/dependency files. Read **every** file that exists:

| File                                               | Stack                                       |
| -------------------------------------------------- | ------------------------------------------- |
| `package.json`                                     | Node / JS / TS                              |
| `requirements.txt` / `pyproject.toml` / `setup.py` | Python                                      |
| `go.mod`                                           | Go                                          |
| `Cargo.toml`                                       | Rust                                        |
| `pom.xml` / `build.gradle`                         | Java / Kotlin                               |
| `Gemfile`                                          | Ruby                                        |
| `composer.json`                                    | PHP                                         |
| `*.csproj` / `*.sln`                               | .NET / C#                                   |
| `Dockerfile` / `docker-compose.yml`                | Infrastructure                              |
| `.env.example` / `.env.sample`                     | Environment variables and external services |

#### 1.4 Read the project's entry files

Read them in the following priority order:

1. `README.md` or `README.rst` (existing project overview)
2. Main configuration files (`config.js`, `settings.py`, `appsettings.json`, etc.)
3. Application entry point (`main.py`, `index.js`, `app.py`, `server.ts`, `Program.cs`, `main.go`, etc.)

#### 1.5 Map modules and domains

Identify the domain/module folders (e.g. `src/`, `app/`, `modules/`, `services/`, `controllers/`, `features/`).

For each main module, read its index file or the most representative file:

```bash
# Example for Node/TypeScript projects:
find <ROOT>/src -name "index.*" | head -30

# Example for Python projects:
find <ROOT> -name "__init__.py" | head -30
```

#### 1.6 Discover routes and endpoints

Search for routing patterns according to the project's stack:

```bash
# Express / Fastify / Koa (JS)
grep -r "router\.\|app\.get\|app\.post\|app\.put\|app\.delete\|app\.patch" <ROOT>/src --include="*.js" --include="*.ts" -l

# FastAPI / Flask / Django (Python)
grep -r "@app\.\|@router\.\|path(" <ROOT> --include="*.py" -l

# Go (gin/chi/echo)
grep -r "\.GET\|\.POST\|\.PUT\|\.DELETE\|Handle\|HandleFunc" <ROOT> --include="*.go" -l

# Rails
find <ROOT> -name "routes.rb"
```

Then read the discovered files to extract the endpoints.

#### 1.7 Identify agents, roles, and entities

Search for:

- Data models/entities (`models/`, `entities/`, `schemas/`)
- Business services (`services/`, `usecases/`, `handlers/`)
- External integrations (`integrations/`, `adapters/`, `clients/`, `providers/`)
- Authentication and user roles (search for `"role"`, `"permission"`, `"auth"`, `"guard"`, `"middleware"`)
- Workers/jobs/schedulers (search for `"queue"`, `"worker"`, `"cron"`, `"scheduler"`, `"job"`)

```bash
grep -r "role\|permission\|admin\|user\|auth" <ROOT>/src --include="*.ts" --include="*.js" --include="*.py" -l | head -15
```

#### 1.8 Map integrations and data flows

Identify external services and data flows:

```bash
# Search for SDK imports, HTTP clients, and queue libraries
grep -r "import\|require\|from" <ROOT>/src --include="*.ts" --include="*.js" --include="*.py" | \
  grep -iE "stripe|sendgrid|twilio|s3|sqs|redis|rabbitmq|kafka|openai|anthropic|firebase|supabase|prisma|mongoose|sequelize|typeorm|axios|fetch|httpx|requests" | \
  head -40
```

---

### PHASE 2 — Synthesis and PRD Generation

Using all the collected information, generate the PRD by following **exactly** the template in `references/prd-template.md`.

**Generation rules:**

- Write in clear, product-oriented language—not overly technical, but not vague either.
- Every section must contain real information extracted from the code—**never leave generic sections or placeholders**.
- If a section does not apply (e.g. no workers), omit it entirely.
- Infer the product/system name from `package.json` (`name` field), the `README`, or the root folder name.
- When listing endpoints, use the format `METHOD /path — inferred description`.
- When describing features, use short, direct bullet points.
- Add a `⚠️ Analysis Limitations` section at the end if any part of the codebase could not be analyzed.

### PHASE 3 — Save the file

Save the generated PRD to:

```text
/mnt/user-data/outputs/<project-name>-prd.md
```

Then use `present_files` to deliver it to the user.

---

## Analysis Best Practices

- **Do not assume**—if you could not find something, explicitly state that.
- **Prioritize code over comments**—the code is the source of truth.
- **Read at least 5–10 core files** before writing anything.
- **Search for tests** (`__tests__/`, `tests/`, `spec/`)—they reveal expected behavior.
- **Inspect environment variables**—they often reveal external services and critical configuration.
- If the project is very large (>500 files), focus on the modules with the highest connectivity (most imported).

---

## Read Before Generating

→ `references/prd-template.md` — Required PRD template
→ `references/stack-hints.md` — Language/framework-specific tips for locating routes, models, and services
