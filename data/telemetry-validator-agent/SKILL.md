---
name: telemetry-validator-agent
description: >
  AI-powered Telemetry Validator Agent that verifies instrumentation works in sandbox environments.
  Use when: (1) Validating OTel spans are emitted correctly,
  (2) Verifying correlation headers in Kafka messages,
  (3) Confirming OpenLineage events for data pipelines,
  (4) Generating validation evidence for merge approval.
  Triggers: "validate telemetry", "verify instrumentation",
  "check OTel spans", "validate correlation headers".
---

# Telemetry Validator Agent

The Telemetry Validator is the final verification layer that confirms instrumentation actually works by running services in sandbox environments and verifying expected signals arrive at the observability backend.

## Core Responsibilities

1. **Environment Setup**: Spin up isolated test environments
2. **Traffic Generation**: Send synthetic requests to exercise code paths
3. **Signal Querying**: Query OTel Collector for expected spans/metrics
4. **Header Validation**: Verify correlation headers in Kafka messages
5. **Lineage Verification**: Confirm OpenLineage events for data jobs
6. **Evidence Collection**: Capture proof of successful validation
7. **Report Generation**: Produce detailed validation reports

## Validation Process

### Step 1: Environment Setup

```python
async def setup_environment(service_name: str, commit_sha: str):
    """Deploy service to isolated namespace."""
    namespace = f"validator-{service_name}-{commit_sha[:8]}"
    
    # Create K8s namespace
    await kubectl.create_namespace(namespace)
    
    # Deploy service from PR branch
    await helm.install(
        release=service_name,
        namespace=namespace,
        values={
            "image.tag": commit_sha,
            "otel.enabled": True,
            "otel.collector": VALIDATOR_COLLECTOR_URL
        }
    )
    
    # Wait for ready
    await kubectl.wait_for_ready(namespace, timeout=120)
    
    return namespace
```

### Step 2: Synthetic Traffic Generation

```python
async def generate_traffic(service_url: str, archetype: str):
    """Generate synthetic traffic based on archetype."""
    
    if archetype == "kafka-microservice":
        # Send HTTP request that triggers Kafka produce
        response = await httpx.post(
            f"{service_url}/api/orders",
            json={"order_id": "test-123", "amount": 99.99},
            headers={"traceparent": "00-test-trace-id-test-span-id-01"}
        )
        
    elif archetype == "rest-api":
        # Send multiple HTTP requests
        for endpoint in ["/health", "/api/v1/resource"]:
            await httpx.get(f"{service_url}{endpoint}")
            
    elif archetype == "airflow-dag":
        # Trigger DAG run
        await airflow.trigger_dag(dag_id="test_dag", conf={})
        
    elif archetype == "spark-job":
        # Submit Spark job
        await spark.submit(job="test_job.py", conf={})
```

### Step 3: Signal Querying

```python
async def query_spans(
    service_name: str,
    trace_id: str,
    expected_operations: list[str]
) -> list[Span]:
    """Query OTel Collector for expected spans."""
    
    spans = await otel_client.query(
        service=service_name,
        trace_id=trace_id,
        time_range="5m"
    )
    
    found_operations = {s.operation_name for s in spans}
    missing = set(expected_operations) - found_operations
    
    if missing:
        raise ValidationError(f"Missing spans: {missing}")
    
    return spans
```

### Step 4: Attribute Validation

```python
def validate_span_attributes(span: Span, expected: dict) -> bool:
    """Validate span has required attributes."""
    
    for key, value in expected.items():
        if key not in span.attributes:
            return False
        if value != "*" and span.attributes[key] != value:
            return False
    
    return True
```

### Step 5: Kafka Header Verification

```python
async def check_kafka_headers(topic: str) -> dict:
    """Verify correlation headers in Kafka messages."""
    
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=KAFKA_BOOTSTRAP,
        consumer_timeout_ms=10000
    )
    
    for message in consumer:
        headers = dict(message.headers)
        
        required = ["traceparent", "x-obs-producer-service", "x-obs-mapping-id"]
        missing = [h for h in required if h not in headers]
        
        if not missing:
            return headers
    
    raise ValidationError(f"Missing headers in {topic}")
```

## Expected Signals by Archetype

| Archetype | Expected Signals | Validation Query |
|-----------|------------------|------------------|
| Kafka Producer | Span: `{topic} send`, Attrs: `messaging.destination`, `x-obs-*` | `spans.where(operation="send").attrs.has("x-obs-mapping-id")` |
| Kafka Consumer | Span: `{topic} receive`, Attrs: `consumer_group`, `partition`, `offset` | `spans.where(operation="receive").attrs.has("messaging.kafka.consumer.group")` |
| Airflow Task | OpenLineage RunEvent with inputs/outputs | `lineage_events.where(job.name="{dag}.{task}").has(outputs)` |
| Spark Job | OpenLineage with column lineage facet | `lineage_events.where(job.namespace="spark").facets.has("columnLineage")` |
| HTTP Handler | Span: `HTTP {method}`, Attrs: `http.route`, `http.status_code` | `spans.where(kind="SERVER").attrs.has("http.route")` |
| gRPC Server | Span: `{service}/{method}`, Attrs: `rpc.system`, `rpc.service` | `spans.where(attrs.rpc.system="grpc")` |

## Validation Report Schema

```json
{
  "validation_id": "val-2026-01-04-001",
  "repository": "orders-enricher",
  "commit_sha": "abc123def",
  "timestamp": "2026-01-04T11:00:00Z",
  "environment": "staging",
  "status": "PASSED",
  "duration_seconds": 45,
  "tests": [
    {
      "name": "otel_spans_emitted",
      "status": "PASSED",
      "expected": 3,
      "actual": 3,
      "details": "All expected spans found with correct attributes"
    },
    {
      "name": "correlation_headers_present",
      "status": "PASSED",
      "headers_validated": ["traceparent", "x-obs-producer-service", "x-obs-mapping-id"],
      "details": "All required headers present in Kafka messages"
    },
    {
      "name": "lineage_event_emitted",
      "status": "PASSED",
      "event_type": "RunEvent",
      "inputs": ["urn:kafka:prod:msk:orders_raw"],
      "outputs": ["urn:kafka:prod:msk:orders_enriched"]
    }
  ],
  "evidence": {
    "span_ids": ["span-001", "span-002", "span-003"],
    "kafka_offsets": {"orders_enriched": 12345},
    "screenshots": ["https://s3.../validation-dashboard.png"]
  },
  "recommendation": "Ready to merge. All telemetry validation checks passed."
}
```

## Scripts

- `scripts/validate_service.py`: Main validation orchestrator
- `scripts/traffic_generator.py`: Synthetic traffic generation
- `scripts/otel_client.py`: OTel Collector query client
- `scripts/kafka_inspector.py`: Kafka header inspection
- `scripts/report_generator.py`: Validation report generation

## References

- `references/expected-signals.md`: Signal expectations by archetype
- `references/validation-queries.md`: OTel query patterns
- `references/report-schema.json`: Validation report JSON schema

## Configuration

```yaml
telemetry_validator:
  enabled: true
  environment: "staging"
  timeout_seconds: 120
  otel_collector_url: "https://otel-collector.staging:4318"
  kafka_bootstrap: "kafka.staging:9092"
  retry_attempts: 3
  cleanup_after: true
```

## Integration Points

| System | Integration | Purpose |
|--------|-------------|---------|
| Kubernetes | API | Namespace creation, deployment |
| OTel Collector | OTLP/Query API | Span ingestion and querying |
| Kafka | Consumer API | Header inspection |
| OpenLineage | API | Lineage event verification |
| S3 | SDK | Evidence storage |
| GitHub | Status API | Report validation status |
