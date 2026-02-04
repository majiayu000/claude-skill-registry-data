---
name: rca-copilot-agent
description: >
  AI-powered RCA Copilot for root cause analysis and incident explanation.
  Use when: (1) Building incident context retrieval from Neptune and DynamoDB,
  (2) Implementing evidence ranking and root cause candidate generation,
  (3) Creating natural language incident explanations,
  (4) Generating recommended remediation actions.
  Triggers: "explain incident", "find root cause", "diagnose data issue",
  "what caused the alert", "RCA for incident".
---

# RCA Copilot Agent

The RCA Copilot is the AI-powered interface that transforms raw observability data into actionable incident explanations. It leverages the Neptune knowledge graph and DynamoDB context cache to achieve sub-2-minute MTTR for Tier-1 incidents.

## Core Responsibilities

1. **Context Retrieval**: Fetch pre-computed incident context from cache
2. **Graph Expansion**: Query Neptune for blast radius and lineage
3. **Evidence Ranking**: Score and rank root cause candidates
4. **Explanation Generation**: Produce natural language incident summaries
5. **Action Recommendation**: Suggest remediation steps and runbooks

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         RCA COPILOT                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                  Context Builder                         │   │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐   │   │
│  │  │ Cache   │  │ Graph   │  │Evidence │  │Timeline │   │   │
│  │  │ Fetch   │  │ Expand  │  │ Rank    │  │ Build   │   │   │
│  │  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘   │   │
│  │       │            │            │            │         │   │
│  │       └────────────┴────────────┴────────────┘         │   │
│  │                         │                               │   │
│  │                         ▼                               │   │
│  │              ┌─────────────────────┐                   │   │
│  │              │   Incident Context  │                   │   │
│  │              │   (Structured)      │                   │   │
│  │              └──────────┬──────────┘                   │   │
│  └─────────────────────────┼───────────────────────────────┘   │
│                            │                                   │
│  ┌─────────────────────────┼───────────────────────────────┐   │
│  │                         ▼                               │   │
│  │              ┌─────────────────────┐                   │   │
│  │              │   LLM Interface     │                   │   │
│  │              │  (Claude/Bedrock)   │                   │   │
│  │              └──────────┬──────────┘                   │   │
│  │                         │                               │   │
│  │              ┌─────────────────────┐                   │   │
│  │              │ Explanation + Actions│                  │   │
│  │              └─────────────────────┘                   │   │
│  │                   Explanation Engine                    │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Context Builder

### Cache Fetch (O(1) Latency)

```python
async def fetch_incident_context(incident_id: str) -> IncidentContext:
    """Fetch pre-computed context from DynamoDB cache."""
    
    response = await dynamodb.get_item(
        TableName="IncidentContextCache",
        Key={"pk": incident_id}
    )
    
    return IncidentContext(
        incident_id=response["incident_id"],
        primary_asset=response["primary_asset"],
        top_evidence=response["top_evidence"],
        blast_radius=response["blast_radius"],
        timeline=response["timeline"]
    )
```

### Graph Expansion

```python
async def expand_blast_radius(asset_urn: str, depth: int = 3) -> BlastRadius:
    """Query Neptune for downstream affected assets."""
    
    query = f"""
    g.V().has('urn', '{asset_urn}')
      .repeat(out('PRODUCES', 'FEEDS_INTO').simplePath())
      .times({depth})
      .dedup()
      .valueMap(true)
    """
    
    downstream = await neptune.execute(query)
    
    return BlastRadius(
        source=asset_urn,
        affected_assets=downstream,
        depth=depth
    )
```

### Evidence Ranking

```python
def rank_evidence(evidence_list: list[Evidence]) -> list[RankedEvidence]:
    """Rank root cause candidates by confidence and recency."""
    
    scored = []
    for e in evidence_list:
        score = (
            e.confidence * 0.4 +           # Base confidence
            recency_score(e.timestamp) * 0.3 +  # Recent = higher
            correlation_score(e) * 0.3     # Correlated to incident
        )
        scored.append(RankedEvidence(evidence=e, score=score))
    
    return sorted(scored, key=lambda x: x.score, reverse=True)
```

### Timeline Construction

```python
async def build_timeline(incident_id: str, window: str = "1h") -> Timeline:
    """Construct incident timeline from events."""
    
    events = await get_events_for_incident(incident_id, window)
    
    return Timeline(
        incident_id=incident_id,
        events=[
            TimelineEvent(
                timestamp=e.timestamp,
                event_type=e.type,
                description=e.summary,
                asset=e.asset_urn
            )
            for e in sorted(events, key=lambda x: x.timestamp)
        ]
    )
```

## Explanation Engine

### LLM Prompt Template

```python
EXPLANATION_PROMPT = """
You are an expert data observability engineer analyzing an incident.

## Incident Context
- Incident ID: {incident_id}
- Primary Asset: {primary_asset}
- Severity: {severity}
- Detection Time: {detection_time}

## Timeline
{timeline}

## Evidence (ranked by confidence)
{evidence}

## Blast Radius
Affected downstream assets:
{blast_radius}

## Your Task
1. Explain the root cause in plain language
2. Describe the impact on downstream consumers
3. Recommend immediate actions
4. Suggest preventive measures

Keep the explanation concise but complete. Focus on actionable insights.
"""
```

### Explanation Generation

```python
async def generate_explanation(context: IncidentContext) -> Explanation:
    """Generate natural language incident explanation."""
    
    prompt = EXPLANATION_PROMPT.format(
        incident_id=context.incident_id,
        primary_asset=context.primary_asset,
        severity=context.severity,
        detection_time=context.detection_time,
        timeline=format_timeline(context.timeline),
        evidence=format_evidence(context.ranked_evidence),
        blast_radius=format_blast_radius(context.blast_radius)
    )
    
    response = await bedrock.invoke(
        model="anthropic.claude-3-sonnet",
        prompt=prompt,
        max_tokens=1000
    )
    
    return Explanation(
        root_cause=extract_root_cause(response),
        impact=extract_impact(response),
        actions=extract_actions(response),
        prevention=extract_prevention(response)
    )
```

## Output Format

### Copilot Response

```json
{
  "incident_id": "INC-2026-01-04-001",
  "query_latency_ms": 1823,
  "root_cause": {
    "summary": "Schema validation failed at ingestion gateway",
    "details": "Field total_amount expected double, received string",
    "confidence": 0.94
  },
  "evidence": [
    {
      "type": "schema_rejection",
      "description": "94% reject rate increase after 12:10Z",
      "confidence": 0.94
    },
    {
      "type": "deployment_correlation",
      "description": "Rejections started 2 minutes after orders-api deployment",
      "confidence": 0.87
    }
  ],
  "impact": {
    "blast_radius": ["orders_enriched topic", "bronze.orders_enriched", "silver.orders"],
    "affected_teams": ["orders-team", "analytics-team"],
    "data_loss_estimate": "~5000 events not ingested"
  },
  "recommended_actions": [
    {
      "action": "rollback",
      "target": "orders-api",
      "command": "kubectl rollout undo deployment/orders-api",
      "urgency": "immediate"
    },
    {
      "action": "runbook",
      "target": "schema_mismatch",
      "url": "https://runbooks.internal/schema-mismatch",
      "urgency": "follow-up"
    }
  ],
  "prevention": [
    "Enable schema compatibility check in CI pipeline",
    "Add contract validation gate for orders-api endpoint"
  ]
}
```

## API Endpoints

### Query Incident

```
POST /api/v1/incidents/{incident_id}/explain
```

### Ask Natural Language

```
POST /api/v1/ask
{
  "question": "Why is the orders dashboard stale?",
  "context": {
    "asset_urn": "urn:dashboard:prod:orders-overview"
  }
}
```

### Get Blast Radius

```
GET /api/v1/assets/{asset_urn}/blast-radius?depth=3
```

## Scripts

- `scripts/context_builder.py`: Incident context assembly
- `scripts/graph_queries.py`: Neptune Gremlin queries
- `scripts/evidence_ranker.py`: Evidence scoring and ranking
- `scripts/explanation_engine.py`: LLM-powered explanations
- `scripts/action_recommender.py`: Remediation suggestions

## References

- `references/prompt-templates/`: LLM prompt templates
- `references/runbook-mapping.md`: Incident type to runbook mapping
- `references/action-catalog.md`: Available remediation actions

## Configuration

```yaml
rca_copilot:
  enabled: true
  context_builder:
    cache_table: "IncidentContextCache"
    graph_endpoint: "wss://neptune.us-east-1.amazonaws.com:8182/gremlin"
  explanation_engine:
    provider: "bedrock"
    model: "anthropic.claude-3-sonnet"
    max_tokens: 1000
    temperature: 0.3
  api:
    port: 8080
    rate_limit: 100  # requests per minute
  sla:
    max_latency_ms: 120000  # 2 minutes
```

## Integration Points

| System | Integration | Purpose |
|--------|-------------|---------|
| DynamoDB | SDK | Context cache retrieval |
| Neptune | Gremlin | Graph queries |
| Bedrock | API | LLM inference |
| Slack | Webhook | Alert delivery |
| PagerDuty | API | Incident escalation |
| S3 | SDK | Runbook storage |

## Performance Requirements

- **Cache hit latency**: < 10ms
- **Graph expansion**: < 500ms for depth=3
- **LLM generation**: < 2000ms
- **Total query latency**: < 2 minutes (SLA for Tier-1)
