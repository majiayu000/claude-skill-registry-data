---
name: ai-serving-apis
description: Put your AI behind an API. Use when you need to serve AI features as web endpoints, add AI to an existing backend, deploy AI for other services to call, wrap a DSPy program in REST or HTTP, build an AI microservice, or put a language model behind FastAPI or Flask. Also use for deploy AI model to production, AI REST API, serve DSPy program over HTTP, Docker AI service, AI endpoint for mobile app, how to productionize my AI, LLM behind a web API, AI microservice architecture, AI backend for React app, put my AI in production, AI API for frontend to call.
---

# Put Your AI Behind an API

Wrap a DSPy program in a web API so other services or a frontend can call it over HTTP. Defaults to FastAPI but adapts to the user's existing framework.

## Step 1: Gather context

Ask the user:
1. **What DSPy program are you serving?** (classification, RAG, extraction, pipeline, etc.)
2. **Is it optimized?** (do you have an `optimized.json` from `/ai-improving-accuracy`?)
3. **What endpoints do you need?** (single query, batch, health check, etc.)
4. **Do you have an existing web framework?** (FastAPI, Flask, Django — default to FastAPI)

### When NOT to serve via API

- **Internal script or notebook only** — if only your team calls the AI from Python, skip the API layer. Import the module directly. An API adds latency, deployment complexity, and a failure surface for no benefit.
- **Batch-only workloads** — if you process data on a schedule (nightly re-classification, weekly report generation), use a script or job runner (cron, Airflow). An HTTP API implies real-time request/response which is overkill for batch.
- **Frontend can call the LM provider directly** — if your app is a thin wrapper around a single LM call with no optimization or custom logic, the frontend can call the provider API directly (with a proxy for auth). You only need a DSPy API when you have optimized prompts, multi-step pipelines, or retrieval logic worth encapsulating.

| Deployment pattern | When to use |
|-------------------|-------------|
| FastAPI + Docker | Default for production microservices — most teams, most cases |
| Flask/Django integration | When adding AI to an existing backend — avoid a second service |
| Serverless (Lambda, Cloud Run) | Low-traffic or spiky workloads — pay per invocation, cold starts acceptable |
| Direct import (no API) | Internal tooling, notebooks, scripts — skip HTTP entirely |

## Step 2: Project structure

Recommended layout — keep DSPy logic separate from API code:

```
project/
├── program.py       # DSPy module (already exists from /ai-kickoff)
├── server.py        # FastAPI app — routes and startup
├── models.py        # Pydantic request/response schemas
├── config.py        # Environment configuration
├── optimized.json   # Saved optimized program (if available)
├── requirements.txt
├── Dockerfile
└── .env.example
```

## Step 3: Define request/response models

```python
# models.py
from pydantic import BaseModel, Field

class QueryRequest(BaseModel):
    """Request to the AI endpoint."""
    query: str = Field(..., description="The input to process", min_length=1)
    # Optional: let callers override the model per request
    model: str | None = Field(None, description="Override the default LM")
    temperature: float | None = Field(None, ge=0, le=2, description="Override temperature")

class QueryResponse(BaseModel):
    """Response from the AI endpoint."""
    answer: str
    # Include whatever your DSPy program outputs
    # reasoning: str | None = None
    # confidence: float | None = None

class HealthResponse(BaseModel):
    status: str = "ok"
    model: str
    optimized: bool
```

## Step 4: Load the optimized program at startup

```python
# server.py
from contextlib import asynccontextmanager
import dspy
from fastapi import FastAPI

from program import MyProgram
from config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load DSPy program once at startup."""
    # Configure the default LM
    lm = dspy.LM(settings.model_name)
    dspy.configure(lm=lm)

    # Load the program (with optimization if available)
    app.state.program = MyProgram()
    app.state.optimized = False
    try:
        app.state.program.load(settings.program_path)
        app.state.optimized = True
        print(f"Loaded optimized program from {settings.program_path}")
    except FileNotFoundError:
        print("Running unoptimized program")

    yield  # Server runs here

app = FastAPI(title="My AI API", lifespan=lifespan)
```

## Step 5: Create endpoints

### Query endpoint

```python
# server.py (continued)
from fastapi import HTTPException
from models import QueryRequest, QueryResponse, HealthResponse

@app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    """Run the AI program on input."""
    program = app.state.program

    # If caller wants a different model, use dspy.context for this request only
    if request.model or request.temperature is not None:
        lm_kwargs = {}
        if request.model:
            lm_kwargs["model"] = request.model
        if request.temperature is not None:
            lm_kwargs["temperature"] = request.temperature
        override_lm = dspy.LM(**lm_kwargs) if request.model else dspy.LM(
            settings.model_name, temperature=request.temperature
        )
        with dspy.context(lm=override_lm):
            result = program(query=request.query)
    else:
        result = program(query=request.query)

    return QueryResponse(answer=result.answer)
```

### Health check

```python
@app.get("/health", response_model=HealthResponse)
async def health():
    return HealthResponse(
        model=settings.model_name,
        optimized=app.state.optimized,
    )
```

### Batch endpoint

For processing multiple inputs at once:

```python
@app.post("/query/batch", response_model=list[QueryResponse])
async def query_batch(requests: list[QueryRequest]):
    """Process multiple inputs."""
    program = app.state.program
    results = []
    for req in requests:
        result = program(query=req.query)
        results.append(QueryResponse(answer=result.answer))
    return results
```

## Step 6: Handle errors

Map DSPy errors to appropriate HTTP status codes:

```python
@app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    program = app.state.program
    try:
        if request.model or request.temperature is not None:
            override_lm = dspy.LM(
                request.model or settings.model_name,
                temperature=request.temperature,
            )
            with dspy.context(lm=override_lm):
                result = program(query=request.query)
        else:
            result = program(query=request.query)
        return QueryResponse(answer=result.answer)

    except Exception as e:
        error_msg = str(e).lower()
        # dspy.Refine raises when fail_count is exhausted -- treat as validation failure
        if "refine" in error_msg or "reward" in error_msg or "fail_count" in error_msg:
            raise HTTPException(status_code=422, detail=f"Output validation failed: {e}")
        if "rate limit" in error_msg or "429" in error_msg:
            raise HTTPException(status_code=429, detail="Rate limited by AI provider")
        if "timeout" in error_msg:
            raise HTTPException(status_code=504, detail="AI provider timed out")
        raise HTTPException(status_code=500, detail="Internal error processing request")
```

## Step 7: Environment configuration

Use pydantic-settings to manage configuration:

```python
# config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    model_name: str = "openai/gpt-4o-mini"  # or "anthropic/claude-sonnet-4-5-20250929", etc.
    program_path: str = "optimized.json"
    api_key: str = ""  # Set via environment variable

    model_config = {"env_prefix": "AI_"}

settings = Settings()
```

```
# .env.example
AI_MODEL_NAME=openai/gpt-4o-mini  # or anthropic/claude-sonnet-4-5-20250929, etc.
AI_PROGRAM_PATH=optimized.json
AI_API_KEY=your-api-key-here
```

## Step 8: Run and deploy

### Run locally

```bash
pip install fastapi uvicorn pydantic-settings
uvicorn server:app --reload --port 8000
```

Visit `http://localhost:8000/docs` for auto-generated API docs.

### Dockerfile

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
```

### requirements.txt

```
dspy>=3.0
fastapi>=0.100
uvicorn[standard]
pydantic-settings>=2.0
```

Add provider-specific packages as needed (e.g., `openai`, `anthropic`).

### Docker Compose (optional)

```yaml
# docker-compose.yml
services:
  api:
    build: .
    ports:
      - "8000:8000"
    env_file: .env
    volumes:
      - ./optimized.json:/app/optimized.json:ro
```

## Step 9: Verify it works

After starting the server, test the endpoints:

```bash
# Health check
curl http://localhost:8000/health

# Query endpoint
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "test question"}'

# Check auto-generated docs
open http://localhost:8000/docs
```

## Key patterns

- **Load once, serve many.** Load the program and LM at startup via lifespan, not per request.
- **`dspy.context()` for per-request overrides.** Isolates model/temperature changes without affecting other concurrent requests — critical because `dspy.configure()` sets global state.
- **Separate DSPy from API code.** Keep `program.py` independent — the same module runs in scripts, tests, and the API.
- **Map DSPy errors to HTTP codes.** `dspy.Refine` exhaustion → 422, rate limits → 429, timeouts → 504.

## DSPy-specific production patterns

### Saving and loading optimized programs

```python
# After optimization
optimized_program.save("./artifacts/v1.json")

# At server startup
program = MyProgram()
program.load("./artifacts/v1.json")
```

The `save()`/`load()` API serializes optimized prompts, demos, and weights — no training data or optimizer needed at deploy time.

### Observability with MLflow

```python
import mlflow

mlflow.dspy.autolog()  # auto-traces all DSPy calls
mlflow.set_experiment("production-qa-api")
```

This gives you latency breakdowns, token counts, and full prompt/response logs per request. For the full MLflow guide, see `/dspy-mlflow`.

### Thread safety

`dspy.configure()` sets global state. For concurrent requests with per-request overrides, always use `dspy.context()`:

```python
@app.post("/query")
async def query(request: QueryRequest):
    if request.model:
        with dspy.context(lm=dspy.LM(request.model)):
            result = program(query=request.query)
    else:
        result = program(query=request.query)
    return QueryResponse(answer=result.answer)
```

## Gotchas

- **Creating a new `dspy.LM()` instance on every request.** Claude tends to put `dspy.LM()` inside the route handler. LM initialization has overhead (connection pooling, auth validation). Configure the default LM once at startup; only create per-request LM instances when the caller explicitly overrides the model via `dspy.context()`.
- **Loading the optimized program inside the route handler.** `program.load()` reads from disk and deserializes — doing it per request adds latency and can cause file handle exhaustion under load. Always load in the lifespan handler and store on `app.state`.
- **Using `async def` routes but calling DSPy synchronously.** DSPy LM calls are blocking I/O. In an `async def` FastAPI route, a blocking call ties up the event loop. Either use `def` (sync) routes so FastAPI runs them in a thread pool, or wrap DSPy calls in `asyncio.to_thread()`.
- **Forgetting that `dspy.configure()` is global state.** Claude often calls `dspy.configure()` inside a route to change the model per request. This mutates global state and causes race conditions under concurrent load. Use `dspy.context()` (context manager) for per-request overrides instead.
- **Returning raw DSPy `Prediction` objects from the API.** Claude sometimes returns `result` directly instead of mapping to a Pydantic response model. `Prediction` objects are not JSON-serializable by FastAPI — always extract the fields you need into your response model.

## Cross-references

> Install any skill: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill <name>`

- Scaffold a new project with API structure — see `/ai-kickoff`
- Build the RAG program to serve — see `/ai-searching-docs`
- Monitor your deployed API — see `/ai-monitoring`
- Optimize API costs in production — see `/ai-cutting-costs`
- Trace requests end-to-end with MLflow — see `/dspy-mlflow`
- Define input/output contracts for your DSPy program — see `/dspy-signatures`
- Fix errors in your deployed AI — see `/ai-fixing-errors`
- **Install `/ai-do` if you do not have it** — it routes any AI problem to the right skill and is the fastest way to work: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill ai-do`

## Additional resources

- For worked examples (RAG API, classification API, streaming), see [examples.md](examples.md)
- For DSPy API details (LM, context, save/load), see [reference.md](reference.md)
