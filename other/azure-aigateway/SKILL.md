---
name: azure-aigateway
description: >
  Design an Azure AI gateway layer for centralized model routing, policy enforcement, and operational control.
  Use this skill when users ask about centralized AI traffic management, model governance, rate limiting, or gateway patterns.
compatibility:
  models: [any-llm]
  cloud: azure
  ai: [gateway, orchestration, policy]
---

# Azure AI Gateway

Centralize LLM traffic through a controlled gateway for security, observability, policy enforcement, and cost control.

## Use This Skill When

- The user needs one entry point for multiple models (Azure OpenAI, third-party LLMs, internal models)
- The user needs to enforce token budgets, rate limits, or SLA policies
- The user needs centralized auditing and compliance logging
- The user needs intelligent fallback (model outage handling)
- The user wants to avoid client-side model management complexity

## Context: Gateway Maturity

**Immature**: Clients call models directly, no centralization  
**Developing**: Basic gateway, simple routing, minimal logging  
**Managed**: Multi-model routing, policy enforcement, token budgets, audit trails → **Target**  
**Optimized**: Real-time cost optimization, feedback-driven routing, self-healing, ML-based model selection

## Required Inputs

- **Model endpoints**: Azure OpenAI? Hugging Face? Internal models? Multiple versions?
- **Routing criteria**: Latency? Cost? Specific models for specific tasks?
- **Policy requirements**: Rate limits? Token budgets? Approval workflows?
- **Scale**: Throughput (req/sec)? Concurrent users? Peak vs. average?
- **Compliance**: PII redaction? Audit trail retention? Data residency?
- **Cost model**: Budget cap? Cost-per-department? Showback?

## Decision Tree

```
What's the primary goal of this gateway?
├─ Cost control → Route to cheaper model if accuracy acceptable
├─ Reliability → Route to alternative model on failure/timeout
├─ Governance → Enforce policies, audit all requests
├─ Performance → Route based on latency SLA
└─ Multi-tenancy → Tenant isolation, quota per tenant

Which models will the gateway route to?
├─ Single model (single Azure OpenAI deployment) → No routing needed
├─ Multiple Azure OpenAI models → Route by task/cost/latency
├─ Multiple providers (Azure OpenAI + third-party) → Handle auth differences
└─ Canary/blue-green (new model test) → Weighted routing

What policy enforcement is needed?
├─ None (simple routing only)
├─ Token budgets (cap usage per user/org)
├─ Rate limits (req/sec, concurrent, bursts)
├─ Approval workflows (route restricted requests for review)
└─ Compliance (PII redaction, output filtering, audit)

How much data volume?
├─ < 100 req/sec → Simple load balancer
├─ 100-1000 req/sec → Async processing, queue buffering
└─ > 1000 req/sec → Distributed gateway, database-backed quotas
```

## Workflow

### Phase 1: Design Gateway Architecture

```
┌─ Client Application ─┐
│  (web, mobile, API)  │
└──────────┬───────────┘
           │ (HTTPS)
           │
    ┌──────▼─────────────────────────────────────┐
    │ AI Gateway (entry point)                   │
    │                                            │
    │  1. Authenticate client (API key, JWT)    │
    │  2. Check token budget (quota system)     │
    │  3. Log request (audit trail)             │
    │  4. Validate payload (safety checks)      │
    └──────┬─────────────────────────────────────┘
           │
    ┌──────▼──────────────────┐
    │ Routing & Policy Engine │
    │                         │
    │  ├─ Route to model 1    │
    │  ├─ Route to model 2    │
    │  └─ Fallback to model 3 │
    └──────┬──────────────────┘
           │
    ┌──────▼──────────────────────────────────────────┐
    │ Model Pools                                      │
    │                                                  │
    │  [Azure OpenAI GPT-4]  → $0.03 per 1K in      │
    │  [Azure OpenAI GPT-3.5]→ $0.0015 per 1K in   │
    │  [Third-party LLaMA]   → $0.01 per 1K in     │
    │  [Custom Model (AKS)]  → On-premise            │
    └──────────────────────────────────────────────────┘
           │
    ┌──────▼──────────────────────────────────┐
    │ Observability                           │
    │                                         │
    │  ├─ Application Insights (traces)      │
    │  ├─ Log Analytics (audit logs)         │
    │  ├─ Cost Management (spend tracking)   │
    │  └─ Alerts (budget overrun, failures)  │
    └─────────────────────────────────────────┘
```

### Phase 2: Implement Gateway (Choose Stack)

**Option 1: Azure API Management + Logic Apps (low-code)**
```
Client → [API Management] → [Logic App] → [Model endpoints]

Benefits: 
- Built-in rate limiting, throttling
- Policy enforcement (transformations, auth)
- Analytics and metrics

Limitations:
- Limited model-specific logic
- Async processing harder
```

**Option 2: Custom Service (Node.js, Python, Go)**
```bash
# App Service or Container Apps
az containerapp create \
  --resource-group $RG \
  --name "ai-gateway" \
  --image "myacr.azurecr.io/ai-gateway:latest" \
  --target-port 8000 \
  --environment-variables \
    OPENAI_ENDPOINT="https://myai.openai.azure.com/" \
    OPENAI_KEY="@keyvault(openai-key)" \
    FALLBACK_MODEL="gpt-35-turbo"
```

**Option 3: Azure Service Fabric / Kubernetes (scale-out)**
```
Each node = independent gateway instance
Database = shared quota store (Redis, SQL)
Enables high-throughput, multi-region
```

### Phase 3: Configure Routing Rules

1. **Cost-optimized routing**:
   ```python
   # Python pseudo-code
   def route_to_model(prompt, required_accuracy=0.9):
       # Try cheap model first
       try:
           response = gpt35_turbo.call(prompt, timeout=2)
           if quality_score(response) >= required_accuracy:
               return response
       except Timeout:
           pass
       
       # Fallback to expensive but reliable model
       response = gpt4.call(prompt, timeout=5)
       return response
   
   # Cost breakdown
   # 1000 requests: 700 via GPT-3.5 ($1.05) + 300 via GPT-4 ($9.00) = $10.05
   # vs. Direct to GPT-4: 1000 × $0.03 = $30
   ```

2. **Latency-optimized routing**:
   ```
   SLA: Response < 500ms
   
   Route 1: Model A (avg 100ms) → Use for 80% of traffic
   Route 2: Model B (avg 300ms) → Use for 20% of traffic
   Route 3: Model C (avg 1500ms) → Failover only if others fail
   ```

3. **Canary / Blue-Green**:
   ```
   New Model (v2):
   └─ 5% of traffic for 1 hour
      ├─ Monitor error rate, latency, cost
      └─ If healthy, shift to 50%, then 100%
   
   Old Model (v1):
   └─ 95% of traffic (safe)
   ```

### Phase 4: Enforce Policies

1. **Rate limiting** (prevent abuse):
   ```
   Per-client:
   ├─ 10 requests/sec (burst)
   ├─ 100,000 requests/day
   └─ 500 concurrent connections
   
   Global:
   ├─ 100,000 requests/sec (max capacity)
   └─ Backpressure: Queue & retry with exponential backoff
   ```

2. **Token budgeting** (control cost):
   ```python
   class TokenQuota:
       def __init__(self, daily_limit=1_000_000):
           self.limit = daily_limit
           self.used = 0  # Track in Redis/database
       
       def check_and_deduct(self, tokens_needed):
           current = redis.get(f"quota:{user_id}")
           if current + tokens_needed > self.limit:
               raise QuotaExceededError(f"Budget exceeded")
           redis.incr(f"quota:{user_id}", tokens_needed)
   
   # Cost cap: $100/day per customer
   # If usage exceeds budget, reject or queue for review
   ```

3. **Approval workflows** (for sensitive operations):
   ```
   Request: "Summarize confidential document X"
   ├─ Payload > 10K tokens? → Route to human review
   ├─ Contains PII pattern? → Route to compliance team
   └─ User has restricted tag? → Require manager approval
   
   Approved → Route to model
   Rejected → Return error with reason
   ```

4. **Input/output filtering**:
   ```
   Input validation:
   ├─ Reject prompts with SQL injection patterns
   ├─ Reject attempts to override system prompt
   └─ Redact email/SSN before sending to model
   
   Output filtering:
   ├─ Block generation of malware/illegal content
   ├─ Redact PII before returning to user
   └─ Flag hallucinated data if confidence low
   ```

### Phase 5: Implement Observability

1. **Log every request** (for audit):
   ```csharp
   // C# - Log to Application Insights
   var properties = new Dictionary<string, string>
   {
       { "ClientId", clientId },
       { "Model", selectedModel },
       { "TokensIn", tokensIn.ToString() },
       { "TokensOut", tokensOut.ToString() },
       { "Cost", cost.ToString() },
       { "LatencyMs", latency.ToString() },
       { "Status", response.StatusCode.ToString() }
   };
   
   telemetryClient.TrackEvent("ai_gateway_request", properties);
   ```

2. **Cost tracking**:
   ```bash
   # Daily cost by model
   customMetrics
   | where name == "ai_gateway_cost"
   | extend Model = tostring(customDimensions.model)
   | summarize TotalCost = sum(value) by Model, bin(timestamp, 1d)
   ```

3. **Alerts**:
   - Budget exceeded: >$500/day
   - Model failure: 5+ consecutive timeouts
   - Latency spike: p95 > 2000ms
   - Abuse pattern: 1000+ req/min from single IP

### Phase 6: Deploy & Manage

1. **Deploy gateway**:
   ```bash
   # Container Apps
   az containerapp up \
     --source . \
     --build-env-vars "GATEWAY_VERSION=1.0" \
     --environment-variables "OPENAI_ENDPOINT=..." \
     --secrets "openai-key=$(az keyvault secret show --vault-name $KV --name openai-key --query value)"
   ```

2. **Monitor SLA**:
   ```
   Target SLA: 99.9% uptime
   ├─ Availability: Measure successful responses / total requests
   ├─ Latency p95: < 500ms
   ├─ Cost per request: < $0.002
   └─ Error rate: < 0.1%
   ```

3. **Update routes (zero-downtime)**:
   ```
   Current: 100% → Model A
   Step 1: 90% → Model A, 10% → Model B (canary)
   Step 2: Monitor for 1 hour
   Step 3: 50% → Model A, 50% → Model B (if healthy)
   Step 4: 0% → Model A, 100% → Model B (complete)
   ```

## Output Contract

1. **Gateway Architecture**
   - Deployment topology (App Service, Container Apps, API Mgmt)
   - Model endpoints and routing rules
   - Fallback and failover strategy

2. **Policy & Control Definitions**
   - Rate limits (req/sec, daily cap)
   - Token budgets (cost cap per user/org)
   - Approval workflows for restricted operations
   - Input/output filtering rules

3. **Security & Compliance**
   - Authentication (API key, JWT, mTLS?)
   - Authorization (RBAC roles)
   - PII/sensitive data handling
   - Audit trail requirements

4. **Monitoring & Cost**
   - Observability dashboards (latency, errors, cost)
   - Alerts for anomalies and budget overrun
   - Cost breakdown by model/user/department
   - SLO targets (availability, latency, cost)

5. **Operational Runbook**
   - Deployment and rollback procedures
   - How to add/remove models
   - Incident response (model outage, quota exhausted)

## Guardrails

- **Never bypass policy checks**: All requests through gateway, no direct model access.
- **Protect API keys**: Store model endpoints and secrets in Key Vault, never in code.
- **Implement rate limiting**: Prevent token stuffing and DDoS attacks.
- **Log for compliance**: Maintain audit trail for sensitive operations.
- **Plan for failover**: At least 2 model endpoints, automatic switchover on failure.
- **Monitor cost closely**: Set budget alerts; can spiral quickly with large batch jobs.
- **Test routing changes**: Use canary deployment before full rollout.
- **Enforce timeouts**: Prevent hanging requests from consuming resources indefinitely.
