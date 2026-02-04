---
name: patterns/proxy
description: Proxy Pattern pattern for C development
---

# Proxy Pattern

Provide surrogate for another object to control access. Proxy has same interface as real object. Adds behavior transparently.

## ikigai Application

**Potential uses:**

*Lazy loading:* Database connection proxy that connects on first query, not at startup.

*Logging proxy:* Wrap LLM client to log all requests/responses without modifying client code.

*Caching proxy:* Cache repeated database queries or LLM responses.

*Rate limiting:* Proxy that throttles API calls.

**Implementation:** Proxy struct holds pointer to real object, implements same interface, adds behavior before/after delegating.

**Current status:** Not explicitly used yet. Consider when adding cross-cutting concerns to existing interfaces without modification.
