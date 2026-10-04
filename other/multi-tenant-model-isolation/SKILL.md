---
name: multi-tenant-model-isolation
description: Review multi-tenant AI deployments for cross-tenant context leakage, LoRA adapter contamination, shared inference worker risks, system prompt bleed, and tenant isolation failures in model serving infrastructure.
last_reviewed: 2026-04-30
---

# Multi-Tenant Model Isolation

## First Principle

**In a multi-tenant AI system, every shared resource is a potential cross-tenant channel. The question is not whether leakage is possible, but whether you have closed each channel.**

Multi-tenant LLM deployments share compute, memory, and sometimes model weights across customers. This is economically necessary and technically achievable — but only when every isolation boundary is explicitly implemented and verified. The threat is not always an active attacker; it is often a configuration gap that allows one tenant's context to influence another tenant's session through shared inference state, caching, or adapter contamination.

## Attack Mental Model

1. **System prompt bleed** — a shared inference worker processes requests from multiple tenants sequentially. Improper KV cache scoping causes residual context from Tenant A's system prompt to influence Tenant B's response.
2. **LoRA adapter contamination** — a shared base model uses per-tenant LoRA adapters loaded dynamically. An adapter loading failure or misconfiguration causes one tenant's adapter to remain active for another tenant's requests.
3. **Cross-tenant RAG retrieval** — a shared vector store is used for multiple tenants' RAG pipelines. Insufficient metadata filtering allows one tenant's documents to be retrieved for another tenant's queries.
4. **Tenant identifier injection** — a tenant's input contains a crafted tenant ID or header that causes the serving layer to process the request under a different tenant's context, accessing that tenant's data or configuration.

## Control Lens

| Principle | What It Means Here |
|---|---|
| **Validate** | Tenant identity is established from a cryptographically verified credential, not from user-supplied headers or request body fields. |
| **Scope** | All data access, cache lookups, RAG retrievals, and adapter loads are scoped by tenant ID as a mandatory, non-overridable parameter. |
| **Isolate** | KV cache, conversation context, system prompt, and adapter state are fully flushed between tenants on shared inference workers. Cross-tenant state persistence is architecturally prevented. |
| **Enforce** | Cross-tenant access attempts — detected through ID mismatches, failed scoping filters, or access pattern anomalies — trigger immediate alerts and session termination. |

## MTI.1 Inference Worker Isolation and Context Flushing

**The core vulnerability:** Shared inference workers that process multiple tenants' requests must guarantee that no state from one tenant's session persists to influence another tenant's session. Improper KV cache management is the most common failure mode.

### Check

- Is KV cache state fully invalidated between requests from different tenants on the same worker?
- Are system prompts loaded per-tenant from a tenant-scoped configuration, and is the loading verified before each request — not assumed from previous state?
- Is there a test that verifies tenant isolation by submitting a sensitive Tenant A request followed by a Tenant B request on the same worker, then checking that Tenant B's response contains no information from Tenant A's context?

### Action

- **Enforce explicit cache flush between tenants:**

```python
class TenantAwareInferenceWorker:
    def __init__(self, model):
        self.model = model
        self.current_tenant_id: str | None = None

    def handle_request(self, request: InferenceRequest) -> InferenceResponse:
        if request.tenant_id != self.current_tenant_id:
            self.flush_tenant_state()
            self.current_tenant_id = request.tenant_id
            self.load_tenant_config(request.tenant_id)

        return self.model.generate(
            system_prompt=self.tenant_config.system_prompt,
            messages=request.messages,
        )

    def flush_tenant_state(self):
        self.model.clear_kv_cache()
        self.tenant_config = None
        self.current_tenant_id = None
        # Also clear any in-process conversation state
```

- **Prefer tenant-dedicated worker pools over shared workers for high-isolation requirements.** For tenants with strict data isolation requirements, assign dedicated inference worker processes rather than relying on runtime isolation between shared workers.
- **Implement a cross-tenant isolation smoke test in CI.** Before every deployment, run a test that submits a canary token in Tenant A's system prompt, then queries Tenant B for the token. Any positive result is a P0 isolation failure.

### Failure Modes

- An inference worker caches the previous tenant's KV state for performance. The next request arrives from a different tenant before the cache expires. The new tenant's response is influenced by the prior tenant's system prompt content.
- A LoRA adapter for Tenant A fails to unload due to a CUDA memory management bug. Tenant B's subsequent request is processed with Tenant A's adapter active, producing responses conditioned on Tenant A's fine-tuning.

## MTI.2 Data Layer Tenant Scoping

**The core vulnerability:** Shared data stores (vector databases, conversation history tables, configuration stores) used across tenants must enforce tenant scoping at the query level, not the application level. An application-level bug that omits a tenant filter exposes all tenant data to all other tenants.

### Check

- Is tenant scoping enforced by a database-level row access policy or collection-level access control — not only by application-layer WHERE clauses?
- Can a tenant ID be supplied by the user in a request body or header in a way that overrides the server-determined tenant ID from the authenticated credential?
- Are RAG vector stores partitioned per tenant at the collection or namespace level, or only filtered by metadata?

### Action

- **Enforce tenant scoping at the data layer using row-level security or collection isolation:**

```python
# PostgreSQL row-level security for tenant isolation
# In migration:
# ALTER TABLE conversation_history ENABLE ROW LEVEL SECURITY;
# CREATE POLICY tenant_isolation ON conversation_history
#   USING (tenant_id = current_setting('app.current_tenant_id')::uuid);

def get_db_connection(tenant_id: str) -> Connection:
    conn = pool.acquire()
    # Set tenant context for row-level security
    conn.execute("SET app.current_tenant_id = %s", (str(tenant_id),))
    return conn
```

- **Derive tenant ID from the authenticated credential only.** The serving layer must extract `tenant_id` from the verified JWT or session token — never from a request body field, URL parameter, or header that the client controls.
- **Partition vector store namespaces per tenant.** Do not use a single collection with a metadata filter as your only tenant isolation mechanism. Use per-tenant collections or namespaces so that a missing filter is a hard miss, not a full-corpus leak.

### Minimum Deliverable Per Review

- [ ] KV cache flush: explicit invalidation between different-tenant requests on shared workers
- [ ] Cross-tenant smoke test: CI test verifying canary token in Tenant A is not returned to Tenant B
- [ ] Tenant ID source: tenant_id derived from authenticated credential; client-supplied values rejected
- [ ] Data layer scoping: row-level security or collection-level isolation; not only application WHERE clause
- [ ] Vector store partitioning: per-tenant namespace/collection isolation for RAG pipelines
- [ ] LoRA adapter isolation: verified unload between tenants; dedicated worker pools for high-isolation tiers

## Quick Win

**Add a cross-tenant isolation smoke test to your deployment pipeline.** Inject a unique canary string in Tenant A's system prompt, then query Tenant B for it in the same environment. This single test catches the most common KV cache and context bleed failures before they reach production.

## References

- Model caching security → [model-caching-security/SKILL.md](../model-caching-security/SKILL.md)
- Data leakage prevention → [data-leakage-prevention/SKILL.md](../data-leakage-prevention/SKILL.md)
- RAG security → [rag-security/SKILL.md](../rag-security/SKILL.md)
- Severity wording → [severity-and-reporting.md](../../references/severity-and-reporting.md)
