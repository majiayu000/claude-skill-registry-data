---
name: signal-factory-core
description: >
  AI-powered Signal Factory Core for processing observability signals and maintaining the knowledge graph.
  Use when: (1) Developing Signal Engines (Freshness, Drift, Contract, DQ, Volume, Anomaly),
  (2) Configuring Signal Router for normalization and routing,
  (3) Designing Neptune graph schema for assets and lineage,
  (4) Implementing DynamoDB state management for incidents.
  Triggers: "create signal engine", "configure signal router",
  "design graph schema", "implement signal processing".
---

# Signal Factory Core

The Signal Factory Core is the central processing hub that transforms raw telemetry into actionable signals, maintains the knowledge graph in Neptune, and powers the RCA Copilot with pre-computed incident context.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                      SIGNAL FACTORY CORE                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────────────┐ │
│  │   Signal    │───▶│  Event Bus  │───▶│   Signal Engines    │ │
│  │   Router    │    │ (Kinesis/   │    │ ┌─────┐ ┌─────┐    │ │
│  │             │    │    MSK)     │    │ │Fresh│ │ Vol │    │ │
│  └─────────────┘    └─────────────┘    │ └─────┘ └─────┘    │ │
│        │                               │ ┌─────┐ ┌─────┐    │ │
│        │ Normalization                 │ │Drift│ │ DQ  │    │ │
│        │ + Correlation                 │ └─────┘ └─────┘    │ │
│        │ + URN Resolution              │ ┌─────┐ ┌─────┐    │ │
│        ▼                               │ │Anom │ │Cost │    │ │
│  ┌─────────────┐                       │ └─────┘ └─────┘    │ │
│  │  Canonical  │                       └─────────────────────┘ │
│  │   Signal    │                               │               │
│  │   Event     │                               ▼               │
│  └─────────────┘                       ┌───────────────────┐   │
│                                        │ State & Graph     │   │
│                                        │ ┌─────┐ ┌─────┐  │   │
│                                        │ │DDB  │ │Nept │  │   │
│                                        │ └─────┘ └─────┘  │   │
│                                        └───────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

## Signal Router

### Responsibilities

1. **Normalization**: Convert raw inputs into canonical Signal Events
2. **URN Resolution**: Standardize asset identifiers
3. **Correlation Extraction**: Extract trace_id, handoff_ids, lineage refs
4. **Schema Resolution**: Bind events to schema versions
5. **Routing**: Direct signals to appropriate engines

### Canonical Signal Event Schema

```json
{
  "event_id": "sig-2026-01-04-001",
  "event_type": "SignalEvent",
  "timestamp": "2026-01-04T10:00:00Z",
  "source": {
    "type": "kafka",
    "asset_urn": "urn:kafka:prod:msk:orders_enriched",
    "service_urn": "urn:svc:prod:commerce:orders-enricher"
  },
  "correlation": {
    "trace_id": "abc123",
    "span_id": "def456",
    "handoff_ids": {
      "kafka_offset": 12345,
      "partition": 3
    },
    "lineage_ref": "map-orders-enriched-v7"
  },
  "payload": {
    "signal_type": "volume",
    "value": 1523,
    "unit": "messages_per_minute"
  },
  "schema": {
    "id": "schema-v42",
    "version": 42,
    "registry": "confluent"
  }
}
```

## Signal Engines

### Freshness Engine

Detects stale data based on expected arrival times.

```python
class FreshnessEngine:
    async def process(self, event: SignalEvent) -> SignalState:
        asset = await self.get_asset(event.source.asset_urn)
        sla = asset.contracts.freshness.max_delay_minutes
        
        last_update = await self.get_last_update(asset.urn)
        delay = (event.timestamp - last_update).minutes
        
        if delay > sla:
            return SignalState(
                asset_urn=asset.urn,
                signal_type="freshness",
                status="BREACH",
                severity=self.calculate_severity(delay, sla),
                evidence=FreshnessEvidence(
                    expected_delay=sla,
                    actual_delay=delay,
                    last_update=last_update
                )
            )
        return SignalState(status="OK")
```

### Volume Engine

Detects anomalies in data volume.

```python
class VolumeEngine:
    async def process(self, event: SignalEvent) -> SignalState:
        asset = await self.get_asset(event.source.asset_urn)
        baseline = await self.get_baseline(asset.urn, window="7d")
        
        current = event.payload.value
        z_score = (current - baseline.mean) / baseline.stddev
        
        if abs(z_score) > 3:  # 3-sigma anomaly
            return SignalState(
                status="ANOMALY",
                evidence=VolumeEvidence(
                    expected=baseline.mean,
                    actual=current,
                    z_score=z_score
                )
            )
```

### Schema Drift Engine

Detects breaking schema changes.

```python
class DriftEngine:
    async def process(self, event: SignalEvent) -> SignalState:
        current = await self.get_schema(event.schema.id)
        previous = await self.get_schema(f"schema-v{event.schema.version - 1}")
        
        compatibility = await self.check_compatibility(previous, current)
        
        if not compatibility.is_backward:
            return SignalState(
                status="DRIFT",
                evidence=DriftEvidence(
                    breaking_changes=compatibility.changes,
                    affected_consumers=await self.get_consumers(event.source.asset_urn)
                )
            )
```

### Contract Engine

Validates data against contracts.

### DQ Engine

Processes Deequ results and quality metrics.

### Anomaly Engine

ML-based anomaly detection across all metrics.

### Cost Engine

Tracks and allocates compute costs.

## Neptune Graph Schema

### Node Types

```gremlin
// Asset nodes
g.addV('Asset')
  .property('urn', 'urn:kafka:prod:msk:orders_enriched')
  .property('type', 'kafka-topic')
  .property('tier', 1)
  .property('owner', 'orders-team')

// Service nodes
g.addV('Service')
  .property('urn', 'urn:svc:prod:commerce:orders-enricher')
  .property('language', 'java')
  .property('framework', 'spring-boot')

// Incident nodes
g.addV('Incident')
  .property('id', 'INC-2026-01-04-001')
  .property('status', 'ACTIVE')
  .property('severity', 'P1')

// Evidence nodes
g.addV('Evidence')
  .property('type', 'schema_drift')
  .property('confidence', 0.95)
```

### Edge Types

```gremlin
// Lineage edges
g.V(service).addE('PRODUCES').to(topic)
g.V(service).addE('CONSUMES').from(topic)

// Incident edges
g.V(incident).addE('AFFECTS').to(asset)
g.V(incident).addE('SUPPORTED_BY').to(evidence)

// Schema edges
g.V(schema_v42).addE('SUPERSEDES').to(schema_v41)
```

## DynamoDB State Tables

### SignalState Table

```json
{
  "pk": "urn:kafka:prod:msk:orders_enriched",
  "sk": "signal#freshness",
  "status": "OK",
  "last_value": 1523,
  "last_update": "2026-01-04T10:00:00Z",
  "ttl": 1704448800
}
```

### IncidentContextCache Table

```json
{
  "pk": "INC-2026-01-04-001",
  "incident_id": "INC-2026-01-04-001",
  "primary_asset": "urn:kafka:prod:msk:orders_enriched",
  "top_evidence": ["schema_drift_v42", "volume_drop_10am"],
  "blast_radius": ["consumer-a", "consumer-b", "delta-table"],
  "timeline": [...],
  "updated_at": "2026-01-04T10:05:00Z"
}
```

## Scripts

- `scripts/signal_router.py`: Main routing and normalization
- `scripts/freshness_engine.py`: Freshness signal processing
- `scripts/volume_engine.py`: Volume anomaly detection
- `scripts/drift_engine.py`: Schema drift detection
- `scripts/graph_writer.py`: Neptune graph operations
- `scripts/state_manager.py`: DynamoDB state operations

## References

- `references/signal-schema.json`: Canonical signal event schema
- `references/graph-schema.md`: Neptune graph model
- `references/engine-configs/`: Per-engine configuration

## Configuration

```yaml
signal_factory:
  router:
    input_topic: "raw-telemetry"
    output_topic: "canonical-signals"
  engines:
    freshness:
      enabled: true
      check_interval_seconds: 60
    volume:
      enabled: true
      baseline_window_days: 7
    drift:
      enabled: true
  storage:
    neptune:
      endpoint: "wss://neptune.us-east-1.amazonaws.com:8182/gremlin"
    dynamodb:
      signal_state_table: "SignalState"
      incident_cache_table: "IncidentContextCache"
```
