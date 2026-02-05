---
name: patterns/strategy
description: Strategy Pattern pattern for C development
---

# Strategy Pattern

Define a family of algorithms as interchangeable function pointers. Clients select which algorithm to use at runtime without changing calling code.

## ikigai Application

**LLM Provider abstraction:** Each provider (OpenAI, Anthropic, Google) implements same interface:
```c
typedef struct {
    res_t (*send)(void *ctx, ik_message_t **msgs, size_t count);
    res_t (*stream)(void *ctx, ik_message_t **msgs, chunk_cb cb);
} ik_llm_provider_t;
```

**Selection:** Config determines which provider vtable is used. REPL calls through interface, unaware of provider.

**Testing:** Inject mock provider that returns canned responses.

**Future:** Tool execution strategies, different database backends.
