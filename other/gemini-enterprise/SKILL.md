---
name: gemini-enterprise
description: Work with Google's Gemini Enterprise (Discovery Engine API) for enterprise search and conversational AI. Use when provisioning Discovery Engine apps, creating/managing data stores, ingesting documents from GCS, querying via StreamAssist or SearchService, configuring Model Armor content safety, registering external agents (A2A/Cloud Run), or integrating Discovery Engine search into ADK agents with DiscoveryEngineSearchTool. Covers the full v1alpha REST API.
---

# Gemini Enterprise (Discovery Engine API)

Build enterprise search and conversational AI with Google's Discovery Engine.

## Quick Reference

| Task | Pattern |
|------|---------|
| Provision engine | `curl POST .../engines?engineId=my-engine` |
| Create data store | `curl POST .../dataStores?dataStoreId=my-store` |
| Import documents | `curl POST .../documents:import` (GCS source) |
| Create session | `POST .../sessions` |
| Query StreamAssist | `POST .../assistants/default_assistant:streamAssist` |
| Search documents | `SearchServiceClient().search(request)` |
| ADK integration | `DiscoveryEngineSearchTool(search_engine_id=..., data_store_specs=[...])` |
| Enable Model Armor | `PATCH .../assistants/default_assistant?update_mask=customerPolicy` |
| Register agent | `POST .../assistants/default_assistant/agents` |

## Resource Hierarchy

```
projects/{project}
  └── locations/{location}          # "global" or regional (e.g., "us-central1")
      └── collections/default_collection
          ├── engines/{engine_id}
          │   ├── assistants/default_assistant
          │   │   └── agents/{agent_id}
          │   ├── sessions/{session_id}
          │   └── servingConfigs/default_config
          └── dataStores/{data_store_id}
              └── branches/default_branch
                  └── documents/{document_id}
```

**Base URL construction:**
- Global: `https://discoveryengine.googleapis.com/v1alpha/projects/{project}/locations/global/collections/default_collection`
- Regional: `https://{location}-discoveryengine.googleapis.com/v1alpha/projects/{project}/locations/{location}/collections/default_collection`

## Provisioning

Full step-by-step guide: **[references/provisioning.md](references/provisioning.md)**

**5-step flow:**
1. Enable `discoveryengine.googleapis.com` API
2. Create data stores (one per content type)
3. Upload documents to GCS and create JSONL metadata
4. Import documents into data stores
5. Create engine referencing data stores, then create default assistant

**Required IAM:** `roles/discoveryengine.admin`

## Data Store Types

| Type | Source | Content Config | Use Case |
|------|--------|---------------|----------|
| Unstructured | GCS (PDFs, HTML) | `CONTENT_REQUIRED` | SOPs, brand guidelines |
| Structured | BigQuery, JSONL | `NO_CONTENT` | Product catalogs |
| Website | URL crawl | `PUBLIC_WEBSITE` | Help center content |
| Workspace | Gmail, Calendar, Drive, Jira | Connector-based | Enterprise knowledge |

**Workspace connector warning:** Each workspace data store attached to an engine inflates the input token count. An engine with 9 data stores (including workspace connectors) can push input tokens above the 1M context limit. Always use `data_store_specs` to restrict searches to specific stores.

## Querying

### StreamAssist (Conversational)

Session-based conversational search with grounded responses and reasoning thoughts.

```python
from scripts.stream_assist_client import StreamAssistClient

client = StreamAssistClient(
    project_id="my-project",
    location="global",
    engine_id="my-engine",
)

# Create a session
session_id = client.create_session("MySession")

# Query with session context
response = client.query("What are the closing procedures?", session_id)
print(response.text)      # Grounded answer
print(response.thoughts)  # Model reasoning (if available)
```

**StreamAssist endpoint:** `POST .../assistants/default_assistant:streamAssist`

**Payload:**
```json
{
  "session": "projects/{project}/locations/{location}/collections/default_collection/engines/{engine}/sessions/{session_id}",
  "query": {"text": "your question"},
  "agentsSpec": {
    "agentSpecs": [{"agentId": "optional-agent-id"}]
  }
}
```

**Response structure:** `answer.replies[].groundedContent.content.{text, role, thought}`

Full client implementation: **[scripts/stream_assist_client.py](scripts/stream_assist_client.py)**

### SearchService (Direct)

Direct document search using the Python SDK. No session required.

```python
from google.cloud import discoveryengine_v1beta as discoveryengine

client = discoveryengine.SearchServiceClient()

request = discoveryengine.SearchRequest(
    serving_config=(
        f"projects/{project}/locations/global/collections/"
        f"default_collection/engines/{engine}/servingConfigs/default_config"
    ),
    query="closing procedures for associates",
    page_size=5,
    data_store_specs=[
        discoveryengine.SearchRequest.DataStoreSpec(
            data_store=(
                f"projects/{project}/locations/global/collections/"
                f"default_collection/dataStores/sop-store"
            )
        )
    ],
)

response = client.search(request)
for result in response:
    print(result.document.derived_struct_data)
```

**Install:** `pip install google-cloud-discoveryengine`

## ADK Integration

### DiscoveryEngineSearchTool vs VertexAiSearchTool

**Always use `DiscoveryEngineSearchTool` when the agent has sub-agents.**

`VertexAiSearchTool` adds a built-in Gemini retrieval tool that **cannot coexist** with the `transfer_to_agent` function tools injected by sub-agents. The ADK's `llm_agent.py` bypass check (`len(self.tools) > 1`) doesn't account for implicit transfer tools.

`DiscoveryEngineSearchTool` wraps the SearchService REST API as a regular `FunctionTool`, so it works alongside any other tools.

### Complete ADK Setup

```python
from google.adk.agents import LlmAgent
from google.adk.tools.discovery_engine_search_tool import DiscoveryEngineSearchTool
from google.cloud import discoveryengine_v1beta as discoveryengine

project_id = "my-project"
engine_id = "my-engine"

# Build resource paths
search_engine_id = (
    f"projects/{project_id}/locations/global/collections/"
    f"default_collection/engines/{engine_id}"
)
ds_base = (
    f"projects/{project_id}/locations/global/collections/"
    f"default_collection/dataStores"
)

# Create search tool with data_store_specs filtering
search_tool = DiscoveryEngineSearchTool(
    search_engine_id=search_engine_id,
    data_store_specs=[
        discoveryengine.SearchRequest.DataStoreSpec(
            data_store=f"{ds_base}/sop-store"
        ),
        discoveryengine.SearchRequest.DataStoreSpec(
            data_store=f"{ds_base}/brand-guidelines-store"
        ),
    ],
)

# Sub-agent with function tools
analytics_agent = LlmAgent(
    name="analytics_agent",
    model="gemini-3.7-flash",
    instruction="Answer data questions using the query tool.",
    description="Answers analytics questions by querying BigQuery.",
    tools=[query_tool],
)

# Root agent: search tool coexists with sub-agent transfer tools
root_agent = LlmAgent(
    name="assistant",
    model="gemini-3.7-flash",
    instruction="Search SOPs and brand guidelines. Delegate analytics.",
    tools=[search_tool],
    sub_agents=[analytics_agent],
)
```

**Critical:** Always specify `data_store_specs` to restrict which data stores are searched. Without filtering, workspace connectors (Gmail, Calendar, etc.) inflate tokens past the 1M limit.

## Model Armor

Content safety screening applied to the Discovery Engine assistant. Filters both user prompts and model responses.

### Filters Available

| Filter | Config Key | Purpose |
|--------|-----------|---------|
| RAI Harm | `raiSettings.raiFilters` | Hate speech, sexual, harassment, dangerous |
| PI & Jailbreak | `piAndJailbreakFilterSettings` | Prompt injection, jailbreak attempts |
| SDP | `sdpSettings` | PII/sensitive data detection |
| Malicious URI | `maliciousUriFilterSettings` | Blocks malicious URLs |

### Apply to Assistant

```bash
# Get project number
PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format='value(projectNumber)')

# Create template (uses 'us' multi-region for global engines)
curl -X POST \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -H "Content-Type: application/json" \
  "https://modelarmor.us.rep.googleapis.com/v1/projects/${PROJECT_NUMBER}/locations/us/templates?templateId=my-armor" \
  -d '{
    "filterConfig": {
      "raiSettings": {
        "raiFilters": [
          {"filterType": "HATE_SPEECH", "confidenceLevel": "MEDIUM_AND_ABOVE"},
          {"filterType": "SEXUALLY_EXPLICIT", "confidenceLevel": "MEDIUM_AND_ABOVE"},
          {"filterType": "HARASSMENT", "confidenceLevel": "MEDIUM_AND_ABOVE"},
          {"filterType": "DANGEROUS", "confidenceLevel": "MEDIUM_AND_ABOVE"}
        ]
      },
      "piAndJailbreakFilterSettings": {
        "filterEnforcement": "ENABLED",
        "confidenceLevel": "MEDIUM_AND_ABOVE"
      },
      "sdpSettings": {"basicConfig": {"filterEnforcement": "ENABLED"}},
      "maliciousUriFilterSettings": {"filterEnforcement": "ENABLED"}
    }
  }'

# Enable on assistant
TEMPLATE_PATH="projects/${PROJECT_NUMBER}/locations/us/templates/my-armor"
curl -X PATCH \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -H "Content-Type: application/json" \
  -H "X-Goog-User-Project: ${PROJECT_ID}" \
  "https://discoveryengine.googleapis.com/v1/projects/${PROJECT_ID}/locations/global/collections/default_collection/engines/${ENGINE_ID}/assistants/default_assistant?update_mask=customerPolicy" \
  -d "{
    \"customerPolicy\": {
      \"modelArmorConfig\": {
        \"userPromptTemplate\": \"${TEMPLATE_PATH}\",
        \"responseTemplate\": \"${TEMPLATE_PATH}\",
        \"failureMode\": \"FAIL_OPEN\"
      }
    }
  }"
```

**Failure modes:**
- `FAIL_OPEN` — queries pass through if Model Armor is unavailable (recommended for production)
- `FAIL_CLOSED` — queries are blocked if Model Armor is unavailable

**Model Armor location:** Use `us` multi-region for global Discovery Engine instances. Regional endpoints (e.g., `us-central1`) cannot be applied to global assistants.

**Required:** `gcloud services enable modelarmor.googleapis.com` and `roles/modelarmor.admin`

## External Agent Registration

Register A2A or Cloud Run agents on Discovery Engine for use in StreamAssist conversations.

```bash
# Register an external agent
curl -X POST \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -H "Content-Type: application/json" \
  -H "X-Goog-User-Project: ${PROJECT_ID}" \
  "${BASE_URL}/engines/${ENGINE_ID}/assistants/default_assistant/agents?agentId=my-agent" \
  -d '{
    "displayName": "My External Agent",
    "agentEndpoint": {
      "endpointUri": "https://my-agent-abc123-uc.a.run.app"
    }
  }'
```

Route queries to a specific agent:
```json
{
  "session": "...",
  "query": {"text": "..."},
  "agentsSpec": {
    "agentSpecs": [{"agentId": "my-agent-id"}]
  }
}
```

## Error Handling

| Status | Meaning | Action |
|--------|---------|--------|
| 200/201 | Success | Parse response |
| 400 `FAILED_PRECONDITION` | Agent execution failed | Do NOT retry — fix the underlying issue |
| 400 (other) | Transient error | Retry with backoff |
| 403 | Auth error | Check credentials, IAM roles, OAuth consent |
| 429 | Rate limited | Retry with exponential backoff (2s min, 120s max) |
| 500-504 | Server error | Retry with exponential backoff |
| 409 | Already exists | Safe to ignore on create operations |

**Retry strategy (recommended):** Exponential backoff, 10 attempts max, multiplier=2, min=4s, max=120s. See [scripts/stream_assist_client.py](scripts/stream_assist_client.py) for tenacity-based implementation.

That script declares its own dependencies inline (PEP 723), so it runs without a
virtualenv:

```bash
uv run scripts/stream_assist_client.py
```

## Authentication

All API calls require:
1. **Bearer token:** `Authorization: Bearer $(gcloud auth print-access-token)` or ADC
2. **Project header:** `X-Goog-User-Project: {project_id}` (required for quota attribution)
3. **Content type:** `Content-Type: application/json`

**Python ADC pattern:**
```python
import google.auth
from google.auth.transport.requests import Request

credentials, _ = google.auth.default()
if not credentials.valid:
    credentials.refresh(Request())
headers = {
    "Authorization": f"Bearer {credentials.token}",
    "X-Goog-User-Project": project_id,
}
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `PERMISSION_DENIED` on streamAssist | Ensure `X-Goog-User-Project` header is set |
| Token overflow (>1M input tokens) | Use `data_store_specs` to filter stores; remove workspace connectors |
| Document import stuck | Check GCS permissions; verify JSONL metadata format |
| Agent returns empty response | Verify documents are indexed (check import LRO status) |
| Model Armor blocks all queries | Check confidence levels; use `FAIL_OPEN` during testing |
| VertexAiSearchTool + sub-agents fails | Switch to `DiscoveryEngineSearchTool` |
| 403 on workspace data store | Workspace connectors require user OAuth, not service account |
| Engine creation fails | Ensure data stores exist first — engine references them |
| Regional vs global mismatch | Engine and data stores must be in the same location |
| Model Armor location error | Use `us` multi-region (not `us-central1`) for global engines |

## Browser Automation (GE UI)

GE's web UI uses deep shadow DOM. Standard `document.body.innerText` returns empty for chat content.

**Only reliable text extraction:** CDP `Accessibility.getFullAXTree` — penetrates all shadow roots, returns visible text only.

**Critical patterns:**
- `@AgentName` dropdown: type `@Trend`, click `page.locator("text=Trends2Insights")`, or ArrowDown+Enter
- **Clear agent bar after first message**: `button[aria-label*="clear"]` — otherwise "continue" routes to the agent, not the root orchestrator
- **False positives**: User prompt contains pipeline keywords ("focus group", "commercial"). Track text growth from baseline.
- **Thinking is transient**: Only visible mid-response, disappears when response completes.

Full guide: **[references/browser_automation.md](references/browser_automation.md)**

## References

- **[references/api_reference.md](references/api_reference.md)** — Complete REST API endpoint reference with payloads and response formats
- **[references/provisioning.md](references/provisioning.md)** — Step-by-step provisioning guide for engines, data stores, Model Armor
- **[references/browser_automation.md](references/browser_automation.md)** — GE browser automation with Playwright + CDP (shadow DOM parsing)
- **[scripts/stream_assist_client.py](scripts/stream_assist_client.py)** — Portable StreamAssist REST client with retry logic
