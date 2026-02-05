---
name: refactoring/techniques
description: Refactoring Techniques refactoring skill
---

# Refactoring Techniques

Catalog of refactoring operations with C examples. Each technique is a behavior-preserving transformation.

## Extract Function

**When:** Long function, repeated code block, code needs a name.

```c
// Before
void process_message(msg_t *msg) {
    // validate
    if (msg->type < 0 || msg->type > MAX_TYPE) return;
    if (msg->payload == NULL) return;
    if (msg->len == 0) return;
    // ... 50 more lines
}

// After
static bool is_valid_message(const msg_t *msg) {
    return msg->type >= 0 && msg->type <= MAX_TYPE
        && msg->payload != NULL
        && msg->len > 0;
}

void process_message(msg_t *msg) {
    if (!is_valid_message(msg)) return;
    // ... cleaner
}
```

**Note:** In ikigai, avoid static helpers due to LCOV issues. Inline is often better.

## Introduce Parameter Object

**When:** Multiple functions share the same parameter group.

```c
// Before
res_t send_request(const char *host, uint16_t port, const char *path,
                   int32_t timeout_ms, bool use_tls);

// After
typedef struct {
    const char *host;
    uint16_t port;
    const char *path;
    int32_t timeout_ms;
    bool use_tls;
} http_request_opts_t;

res_t send_request(const http_request_opts_t *opts);
```

## Replace Magic Number with Constant

**When:** Literal values appear in logic.

```c
// Before
if (retry_count > 3) { ... }
char buffer[4096];

// After
#define MAX_RETRIES 3
#define READ_BUFFER_SIZE 4096

if (retry_count > MAX_RETRIES) { ... }
char buffer[READ_BUFFER_SIZE];
```

## Replace Conditional with Strategy

**When:** Switch/if-else selecting behavior by type.

```c
// Before
void handle_event(event_t *e) {
    switch (e->type) {
        case EVENT_CLICK: handle_click(e); break;
        case EVENT_KEY: handle_key(e); break;
        case EVENT_RESIZE: handle_resize(e); break;
    }
}

// After - vtable pattern
typedef struct {
    void (*handle)(void *ctx, event_t *e);
} event_handler_vtable_t;

void handle_event(event_handler_vtable_t *vtable, void *ctx, event_t *e) {
    vtable->handle(ctx, e);
}
```

## Extract Variable

**When:** Complex expression needs a name.

```c
// Before
if (msg->flags & FLAG_URGENT && msg->priority > 5 && !msg->processed) {

// After
bool needs_immediate_processing =
    (msg->flags & FLAG_URGENT) && msg->priority > 5 && !msg->processed;
if (needs_immediate_processing) {
```

## Inline Function

**When:** Function body is as clear as its name, or only called once.

```c
// Before
static int32_t get_port(config_t *cfg) {
    return cfg->port;
}
// ... later
int32_t port = get_port(cfg);

// After
int32_t port = cfg->port;
```

## Replace Nested Conditional with Guard Clauses

**When:** Deep nesting from validation checks.

```c
// Before
res_t process(input_t *in) {
    if (in != NULL) {
        if (in->data != NULL) {
            if (in->len > 0) {
                // actual work
            }
        }
    }
    return OK(NULL);
}

// After
res_t process(input_t *in) {
    if (in == NULL) return ERR(ctx, ERR_INVALID_ARG, "null input");
    if (in->data == NULL) return ERR(ctx, ERR_INVALID_ARG, "null data");
    if (in->len == 0) return ERR(ctx, ERR_INVALID_ARG, "empty data");

    // actual work - no nesting
    return OK(result);
}
```

## Consolidate Duplicate Conditional

**When:** Same condition checked in multiple places.

```c
// Before
if (is_debug_mode()) log_debug("Starting");
// ... code ...
if (is_debug_mode()) log_debug("Step 1");
// ... code ...
if (is_debug_mode()) log_debug("Done");

// After
void process(bool debug) {
    if (debug) log_debug("Starting");
    // ... code ...
    if (debug) log_debug("Step 1");
    // ... code ...
    if (debug) log_debug("Done");
}
// Check once at call site, pass flag down
```

## Rename for Clarity

**When:** Name doesn't convey purpose.

```c
// Before
int32_t n;
char *s;
void proc(data_t *d);

// After
int32_t message_count;
char *session_id;
void process_incoming_message(data_t *message);
```

## Workflow

1. **Identify smell** - Use smells.md checklist
2. **Select technique** - Match smell to transformation
3. **Verify tests pass** - Before refactoring
4. **Apply transformation** - One at a time
5. **Verify tests still pass** - After refactoring
6. **Commit** - Small, focused commits
