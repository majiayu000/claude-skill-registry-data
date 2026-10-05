---
name: gcp-diagram
description: Generate professional GCP-branded architecture diagrams using Gemini image generation models. Use when the user asks to create architecture diagrams, system diagrams, data flow diagrams, deployment diagrams, database schema diagrams, or any technical diagram styled like official Google Cloud Platform documentation. Also use when asked to visualize GCP architectures, agent systems, microservices, or service topologies. Supports gemini-3-pro-image and gemini-3.1-flash-image via Vertex AI.
---

# GCP Architecture Diagram Generator

Generate publication-quality architecture diagrams styled like official Google Cloud Platform documentation using Gemini image generation.

This skill drives **Vertex AI image generation directly** and overlays official Google Cloud icon
assets via `scripts/overlay_icons.py`. For diagrams built through the **PaperBanana** MCP pipeline —
including its own GCP branding path, statistical plots, batch generation, and figure evaluation —
use the `paperbanana` skill instead.

## Workflow

### 1. Gather Architecture Details

From user description or codebase, identify:
- Components and GCP services involved
- Connections, protocols, and data flow direction
- Logical groupings (which services belong together)
- Diagram type (system overview, agent hierarchy, data flow, schema, deployment, security)

### 2. Build the Prompt

Read [references/gcp-brand.md](references/gcp-brand.md) for colors, typography, and icon guidelines. Select and fill a template from [references/templates.md](references/templates.md).

Every prompt must include these phrases:
- "professional, clean architecture diagram in the style of official Google Cloud Platform documentation"
- "GCP brand colors: blue (#4285F4), green (#34A853), yellow (#FBBC05), red (#EA4335)"
- "clean white background"
- "Google Cloud product icon style, clean lines, no 3D effects, no hexagons, modern flat design"
- "Google Cloud logo watermark at bottom left"

Color conventions by component type:
- **Compute/Agents**: Green (#34A853)
- **Data/Analytics/BigQuery**: Orange/Yellow (#F9AB00)
- **AI/ML/Vertex AI**: Purple (#A142F4)
- **Storage/GCS**: Yellow (#FBBC05)
- **Networking/Serverless**: Teal (#12B5CB)
- **Security**: Red (#EA4335)
- **Discovery Engine/Search**: Blue (#4285F4)
- **Users/Clients**: Red ellipse (#EA4335)
- **Config/Infrastructure**: Gray (#5F6368)

### 3. Generate

Try the PaperBanana MCP tool first (`mcp__paperbanana__generate_diagram`). If unavailable, use Vertex AI directly:

```python
from google import genai
from google.genai import types

## gemini-3 image models require the global endpoint
models = [
    ("gemini-3-pro-image", "global"),
    ("gemini-3.1-flash-image", "global"),
]
for model, location in models:
    try:
        client = genai.Client(vertexai=True, project=PROJECT_ID, location=location)
        response = client.models.generate_content(
            model=model,
            contents=prompt,
            config=types.GenerateContentConfig(response_modalities=["IMAGE", "TEXT"]),
        )
        for part in response.candidates[0].content.parts:
            if part.inline_data:
                with open(output_path, "wb") as f:
                    f.write(part.inline_data.data)
                break
        break
    except Exception:
        continue  # try fallback
```

**Model priority:** `gemini-3-pro-image` (highest fidelity) > `gemini-3.1-flash-image` (faster, cheaper). Falls back automatically.

Both are the stable IDs. The `-preview` variants were retired on Vertex AI on 2026-07-17, and
`gemini-2.5-flash-image` is scheduled for shutdown 2026-10-02 — do not pin to any of them.

**IMPORTANT:** `gemini-3-*` models require `location="global"`. Using a regional endpoint (e.g., `us-central1`) will return 404.

### 4. Overlay Official GCP Icons

Gemini image generation cannot accurately reproduce trademarked GCP product logos. After generating, replace the AI-approximated icons with official ones using [scripts/overlay_icons.py](scripts/overlay_icons.py).

**113 official GCP product icons** + **21 official GCP category icons** are bundled in [assets/icons/](assets/icons/) (PNG, RGBA).

Category icons sourced from [services.google.com/fh/files/misc/category-icons.zip](https://services.google.com/fh/files/misc/category-icons.zip). SVGs also available in `assets/icons/categories/svg/`.

The script declares its own dependencies inline (PEP 723), so it needs no virtualenv:

```bash
uv run scripts/overlay_icons.py diagram.png out.png --icons "BigQuery:100,200"
uv run scripts/overlay_icons.py --list   # available icon names
```

#### Step-by-step

1. Read the generated diagram to identify GCP product icon locations (x, y coordinates)
2. Run the overlay script:

```python
import sys
sys.path.insert(0, "<skill_dir>/scripts")
from overlay_icons import overlay_icons

overlay_icons("diagram.png", "diagram_final.png", [
    {"product": "BigQuery", "x": 400, "y": 200, "size": 48},
    {"product": "Vertex AI", "x": 200, "y": 100, "size": 48},
    {"product": "Cloud Run", "x": 600, "y": 300, "size": 48},
    {"product": "Cloud Storage", "x": 400, "y": 400, "size": 48},
])
```

Or via CLI:
```bash
python scripts/overlay_icons.py diagram.png diagram_final.png \
    --icons "BigQuery:400,200 Vertex\ AI:200,100 Cloud\ Run:600,300" --size 48
```

#### Finding coordinates

Open the generated diagram with `Read` tool to visually identify where each GCP product icon should be placed. Estimate x,y pixel coordinates for the center of each product icon box.

#### Available icon categories

| Category | Products |
|----------|----------|
| analytics | BigQuery, Composer, Dataflow, Data Fusion, Dataproc, Looker, Pub/Sub |
| compute | App Engine, Compute Engine, Cloud Functions, Cloud Run, GKE, GPU |
| database | Bigtable, Datastore, Firestore, Memorystore, Cloud SQL, Spanner |
| ml | Vertex AI, AI Platform, AutoML, Dialogflow, TPU, Vision API |
| network | Cloud Armor, CDN, DNS, Load Balancing, VPC, VPN, Service Mesh |
| security | IAM, IAP, KMS, Secret Manager, SCC, Certificate Manager |
| storage | Cloud Storage, Filestore, Persistent Disk |
| devtools | Cloud Build, Cloud Shell, Container Registry, Scheduler, Tasks |
| api | API Gateway, Apigee, Endpoints |

Run `python scripts/overlay_icons.py --list` for the full mapping.

### 5. Verify Branding & Spelling (MANDATORY)

**This step is required before delivering any diagram. Do NOT skip.**

#### Branding Checklist

- [ ] Colors match GCP brand conventions from [references/gcp-brand.md](references/gcp-brand.md)
  - Compute/Agents: Green (#34A853)
  - Data/Analytics: Orange/Yellow (#F9AB00)
  - AI/ML: Purple (#A142F4)
  - Storage: Yellow (#FBBC05)
  - Networking: Teal (#12B5CB)
  - Security: Red (#EA4335)
  - Search/Discovery Engine: Blue (#4285F4)
- [ ] Background is clean white (#FFFFFF)
- [ ] All shapes are rounded rectangles, circles, or ellipses — **never hexagons**
- [ ] No 3D effects, shadows, or gradients on service boxes
- [ ] Google Cloud logo watermark at bottom left
- [ ] Official GCP product icons overlaid via Step 4 (not AI-generated approximations)

#### Spelling Checklist

**Read every label in the diagram and compare against official GCP product names:**

| Correct | Common Mistakes |
|---------|-----------------|
| BigQuery | Big Query, Bigquery, BQ |
| Cloud Run | CloudRun, Cloud run |
| Vertex AI | VertexAI, Vertex.AI, Vertex ai |
| Cloud Storage | CloudStorage, GCS (ok in code, not in diagrams) |
| Pub/Sub | PubSub, Pub Sub |
| Cloud SQL | CloudSQL |
| Kubernetes Engine | Kubernete Engine, K8s Engine |
| Discovery Engine | DiscoveryEngine |
| Agent Engine | AgentEngine |
| Model Armor | ModelArmor |
| Gemini | Gemni, Gemnini |
| Imagen | ImageGen, Image Gen |
| Memory Bank | MemoryBank |
| OpenTelemetry | Open Telemetry |

- [ ] Every GCP service name matches official spelling (check table above)
- [ ] Every custom label (agent names, data store names, dataset names) is spelled correctly
- [ ] Acronyms are consistent (e.g., don't mix "BQ" and "BigQuery" in same diagram)
- [ ] Resource IDs and region names match actual deployed values

#### Layout & Readability

- [ ] All components labeled correctly
- [ ] Connections directional with protocols noted
- [ ] Text readable at expected display size
- [ ] Layout balanced, no overlapping elements

**If any check fails, regenerate with a refined prompt. Do not deliver diagrams with branding or spelling errors.**

## Prompt Tips

- Specify layout: "top-to-bottom" or "left-to-right"
- Use shape hints: "rounded rectangle" (services), "cylinder" (databases), "ellipse" (users), "octagon" (security), "folder" (storage)
- Name every connection with its protocol
- Add "landscape orientation" for wide architectures
- Include resource IDs and regions for deployed resources
- Add "leave a blank square placeholder where each GCP product icon would go" to make overlay easier

## References

- **GCP brand colors, typography, icons**: [references/gcp-brand.md](references/gcp-brand.md)
- **Prompt templates by diagram type**: [references/templates.md](references/templates.md)
- **Official GCP icon assets (113 PNGs)**: [assets/icons/](assets/icons/) — bundled from the `diagrams` library
- **Icon overlay script**: [scripts/overlay_icons.py](scripts/overlay_icons.py)
- **GCP Product Icons PDF**: https://services.google.com/fh/files/misc/google-cloud-product-icons.pdf
- **GCP Icons Gallery**: https://cloud.google.com/icons
