---
name: dfd-analysis
description: Deep DFD understanding from images and text. Multi-phase analysis protocol that extracts entities, maps data flows, contextualizes security boundaries, and produces structured DFD features JSON for threat modeling.
allowed-tools: Read, Glob, Grep
---

# DFD Analysis Skill

> **Purpose:** Enable models to deeply understand Data Flow Diagrams from **images**, **text descriptions**, or **structured input** — then produce a detailed, validated DFD features JSON optimized for threat modeling and diagram rendering.

---

## When to Use

| Trigger | Action |
|---------|--------|
| User provides a DFD image/screenshot | Activate **Image Analysis Mode** → read `image-analysis.md` |
| User provides structured system description (JSON) | Activate **Text Analysis Mode** |
| User describes a system in natural language | Activate **Text Analysis Mode** (parse into structured input first) |
| User provides both image + text | Activate **Hybrid Mode** (image as primary, text as supplement) |
| Need to validate/review existing DFD JSON | Activate **Validation Mode** (Phase 5 only) |

---

## 5-Phase Analysis Protocol

Every DFD analysis follows these phases sequentially. **No phase may be skipped.**

### Phase 1 — Input Classification

Determine input type and prepare for analysis.

| Input Type | Detection | Preparation |
|------------|-----------|-------------|
| **Image** | File/URL with image extension, or vision input | Read `image-analysis.md` → extract visual elements |
| **Structured JSON** | Has `structured_input` with `users`, `systempurpose`, `keyfeatures` etc. | Parse directly |
| **Natural Language** | Free-form text describing a system | Convert to structured input format first |
| **Hybrid** | Image + any text/JSON | Parse image first, merge with text data |

**For natural language → structured input conversion:**

Extract these fields from the description:
- `users` — Who interacts with the system?
- `systempurpose` — What does the system do?
- `keyfeatures` — What are the main capabilities?
- `hostingenvironment` — Where is it deployed?
- `sensitivedata` — What sensitive/PII data exists?
- `thirdpartyservices` — What external services are used?
- `accessmethods` — How do users access it?
- `datastores` — What data stores exist?
- `cybercontrols` — What security controls exist?
- `assets` — What valuable data needs protection? (optional)
- `threat_actors` — What threat actors are relevant? (optional)

---

### Phase 2 — Entity Extraction

Extract the three core DFD element types. Refer to `json-schema.md` for naming rules.

#### 2a. External Entities

- **Sources:** `users` + `thirdpartyservices` fields
- **Rules:**
  - Capitalize properly: `customers` → `Customers`
  - Normalize third-party names: `google login` → `Google SSO`, `stripe payment` → `Stripe`
  - Include all user types AND external service providers

#### 2b. Processes

- **Source:** `keyfeatures` field
- **Rules:**
  - Each feature becomes a process, capitalize each word
  - For payment services: add `Process Payment` only if no explicit checkout/pay feature
  - Keep process names action-oriented: `Login`, `Search Products`, `Checkout And Pay`

#### 2c. Data Stores

- **Derived from:** processes (NOT directly from input)
- **Naming rules:**
  - `Manage [Entity]` → `[Entity] Database`
  - `Manage [Entity]s` → `[Entity] Database` (singular)
  - Special: `Manage Blog Posts` → `Blog Database`
  - Logical derivation: `Search Products` → `Product Database`
- **Exclusions:**
  - No `User Database` if SSO handles auth externally
  - No `Payment Database` if payments handled by third-party

---

### Phase 3 — Flow Mapping

Map all data flows following strict Source → Process → Target pattern.

#### Hard Rules (NEVER violate)

| Rule | Violation Example | Correct Form |
|------|-------------------|--------------|
| No direct entity↔data store flows | `Customer → User Database` | `Customer → Login → User Database` |
| No direct entity↔entity flows | `Stripe → Customer` | `Stripe → Process Payment → Customer` |
| Every flow passes through a process | `Product DB → Customer` | `Product DB → Search Products → Customer` |
| Include return flows | One-way only | Add reverse flow (query results, confirmations) |

#### Entity-to-Process Matching

Use these mappings to connect external entities to processes. See `json-schema.md` for the complete mapping table.

| External Entity Type | Matches Processes Containing |
|---------------------|------------------------------|
| Payment (Stripe, PayPal, Razorpay) | payment, pay, checkout, transaction, billing |
| Search (Elastic, Algolia) | search, browse, find, query, discover |
| Auth (Google SSO, Auth0, Okta) | login, auth, sign, authenticate |
| AI (OpenAI, Claude, Gemini) | generate, analyze, predict, recommend, chat |
| Communication (Twilio, SendGrid) | notify, message, email, sms, alert |
| Maps (Google Maps, Mapbox) | map, location, track, navigate, delivery |
| Storage (S3, Azure Blob) | upload, download, store, backup |

#### Authentication Flows

- SSO: `User → Login → SSO Provider` + `SSO Provider → Login → User`
- Include callback flows where applicable

#### Flow Numbering

- Sequential: `1.`, `2.`, `3.`...
- Use arrow symbol: `→`
- Format: `"1. Source → Process → Target"`

---

### Phase 4 — Security Contextualization

Build the security layer on top of the functional DFD.

#### 4a. Trust Boundaries

Hierarchical zones with nesting support. Standard zones:

| Zone | Contains | Nesting |
|------|----------|---------|
| Internet Zone | External users | Children: per-user-type networks |
| DMZ | Public-facing processes | — |
| Application Zone | Business logic processes | — |
| Data Zone | Databases, file storage | — |
| External Services Zone | Third-party entities | — |
| PCI Zone | Payment processes (if card data) | — |
| Admin Zone | Admin processes | — |

Determine boundaries based on: deployment environment, data sensitivity, data flow patterns.

#### 4b. Assets

Identify valuable data that needs protection.

- **Priority:** Use input `assets` if provided; otherwise derive from `sensitivedata` + processes/data stores
- **IDs:** A01, A02, A03...
- **Sensitivity:** `high` | `medium` | `low`
- **Common assets:** User Credentials, Payment Data, Personal Information, Health Records, Business Data, API Keys/Secrets

#### 4c. Security Controls

Categorize from `cybercontrols` input.

- **IDs:** C01, C02, C03...
- **Types:** `authentication` | `authorization` | `encryption_transit` | `encryption_rest` | `monitoring` | `network` | `access_control`
- Associate with relevant nodes (processes) and edges (flow numbers)
- See `json-schema.md` for type-to-control mapping

#### 4d. Threat Actors

- **Priority:** Use input `threat_actors` if provided; otherwise infer from system type + assets
- **IDs:** T01, T02, T03...
- **Categories:** `external` | `insider` | `third_party` | `automated`
- Associate with target assets (by ID) and entry points (external entities)

---

### Phase 5 — Validation & Orphan Resolution

**This phase is mandatory. Do NOT skip.**

#### Step 1: Orphan Detection

Scan all external entities, processes, and data stores. Any that don't appear in ANY data flow → orphan list.

#### Step 2: Orphan Resolution

Apply these rules systematically:

| Orphan Type | Resolution Strategy |
|-------------|---------------------|
| **Orphan Process** | Match to entity whose ROLE relates to the function. Inventory → Store Managers/Vendors. Payment → Payment entities. Admin → Admins. Then connect to appropriate data store. |
| **Orphan External Entity** | Match to process that needs that entity type. User-type → user-facing processes. Service-type → integration processes. |
| **Orphan Data Store** | Match to process that would read/write that data. User DB → Login. Order DB → Checkout. Product DB → Search/Inventory. |

**After adding orphan flows:** number them sequentially after the last existing flow.

#### Step 3: Cross-Validation Checklist

- [ ] Every external entity appears in at least one flow
- [ ] Every process appears in at least one flow
- [ ] Every data store appears in at least one flow
- [ ] No direct entity↔data store flows exist
- [ ] No direct entity↔entity flows exist
- [ ] All flows follow Source → Process → Target pattern
- [ ] Return flows exist for query/response patterns
- [ ] Trust boundary components match actual entity/process/store names exactly
- [ ] All asset `associatedNodes` reference real node names
- [ ] All control `associatedEdges` reference real flow numbers
- [ ] All threat actor `entryPoints` reference real external entities
- [ ] All threat actor `targetAssets` reference real asset IDs
- [ ] IDs are sequential with no gaps (A01-A0N, C01-C0N, T01-T0N)

---

## Output

Produce a single JSON object matching the schema in `json-schema.md`.

**Format rules:**
- No markdown code fences in output
- Proper capitalization on all names
- Empty arrays `[]` for categories with no items
- No placeholder text
- Arrow symbol `→` in data flows

---

## Supplementary Files

| File | When to Read |
|------|-------------|
| `image-analysis.md` | When input contains a DFD image or screenshot |
| `json-schema.md` | Always — contains the output schema, all mapping rules, and naming conventions |
| `examples.md` | When you need reference input→output pairs |

---

## Anti-Patterns

| ❌ Don't | ✅ Do |
|----------|-------|
| Skip orphan resolution | Always run Phase 5 |
| Connect entities directly to data stores | Route through processes |
| Use generic names ("Database 1") | Use descriptive names ("Product Database") |
| Guess at unclear image elements | Flag uncertainty, ask user |
| Copy input verbatim without normalization | Capitalize, normalize third-party names |
| Add unnecessary data stores | Derive only from processes |
| Omit return flows | Include bidirectional flows for request/response |
