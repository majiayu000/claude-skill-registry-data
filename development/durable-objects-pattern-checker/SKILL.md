---
name: durable-objects-pattern-checker
description: Automatically validates Cloudflare Durable Objects usage patterns, ensuring correct state management, hibernation, and strong consistency practices
triggers: ["Durable Object imports", "DO stub usage", "state management patterns", "DO ID generation"]
---

# Durable Objects Pattern Checker SKILL

## Activation Patterns

This SKILL automatically activates when:
- Durable Object imports or exports are detected
- DO stub creation and usage patterns
- State management in Durable Objects
- ID generation patterns (`idFromName`, `newUniqueId`)
- Hibernation and lifecycle patterns
- WebSocket or real-time features with DOs

## Expertise Provided

### Durable Objects Best Practices
- **State Management**: Ensures proper state persistence and consistency
- **ID Generation**: Validates correct ID patterns for different use cases
- **Hibernation**: Checks for proper hibernation implementation
- **Lifecycle Management**: Validates constructor, fetch, and alarm handling
- **Strong Consistency**: Ensures DOs are used when strong consistency is needed
- **Performance**: Identifies DO performance anti-patterns

### Specific Checks Performed

#### ❌ Durable Objects Anti-Patterns
```typescript
// These patterns trigger immediate alerts:
// Using DOs for stateless operations
export default {
  async fetch(request: Request, env: Env) {
    const id = env.COUNTER.newUniqueId();  // New DO every request!
    const stub = env.COUNTER.get(id);
    return stub.fetch(request);  // Overkill for simple counter
  }
}

// Missing hibernation for long-lived DOs
export class ChatRoom {
  constructor(state, env) {
    this.state = state;
    // Missing this.state.storage.setAlarm() for hibernation
  }
}
```

#### ✅ Durable Objects Best Practices
```typescript
// These patterns are validated as correct:
// Reuse DO instances for stateful coordination
export default {
  async fetch(request: Request, env: Env) {
    const ip = request.headers.get('CF-Connecting-IP');
    const id = env.RATE_LIMITER.idFromName(ip);  // Reuse same DO
    const stub = env.RATE_LIMITER.get(id);
    return stub.fetch(request);
  }
}

// Proper hibernation implementation
export class ChatRoom {
  constructor(state, env) {
    this.state = state;
    this.env = env;
    
    // Set alarm for hibernation after inactivity
    this.state.storage.setAlarm(Date.now() + 30000); // 30 seconds
  }
  
  alarm() {
    // DO will hibernate after alarm
  }
}
```

## Integration Points

### Complementary to Existing Components
- **cloudflare-architecture-strategist agent**: Handles complex DO architecture, SKILL provides immediate pattern validation
- **edge-performance-oracle agent**: Handles DO performance analysis, SKILL ensures correct usage patterns
- **workers-binding-validator SKILL**: Ensures DO bindings are correct, SKILL validates usage patterns

### Escalation Triggers
- Complex DO architecture questions → `cloudflare-architecture-strategist` agent
- DO performance troubleshooting → `edge-performance-oracle` agent
- DO migration strategies → `cloudflare-architecture-strategist` agent

## Validation Rules

### P1 - Critical (Will Cause Issues)
- **New Unique ID Per Request**: Creating new DO for every request
- **Missing Hibernation**: Long-lived DOs without hibernation
- **State Leaks**: State not properly persisted to storage
- **Blocking Operations**: Synchronous operations in DO fetch

### P2 - High (Performance/Correctness Issues)
- **Wrong ID Pattern**: Using `newUniqueId` when `idFromName` is appropriate
- **Stateless DOs**: Using DOs for operations that don't need state
- **Missing Error Handling**: DO operations without proper error handling
- **Alarm Misuse**: Incorrect alarm patterns for hibernation

### P3 - Medium (Best Practices)
- **State Size**: Large state objects that impact performance
- **Concurrency**: Missing concurrency control for shared state
- **Cleanup**: Missing cleanup in DO lifecycle

## Remediation Examples

### Fixing New Unique ID Per Request
```typescript
// ❌ Critical: New DO for every request (expensive and wrong)
export default {
  async fetch(request: Request, env: Env) {
    const userId = getUserId(request);
    
    // Creates new DO instance for every request!
    const id = env.USER_SESSION.newUniqueId();
    const stub = env.USER_SESSION.get(id);
    
    return stub.fetch(request);
  }
}

// ✅ Correct: Reuse DO for same entity
export default {
  async fetch(request: Request, env: Env) {
    const userId = getUserId(request);
    
    // Reuse same DO for this user
    const id = env.USER_SESSION.idFromName(userId);
    const stub = env.USER_SESSION.get(id);
    
    return stub.fetch(request);
  }
}
```

### Fixing Missing Hibernation
```typescript
// ❌ High: DO never hibernates (wastes resources)
export class ChatRoom {
  constructor(state, env) {
    this.state = state;
    this.env = env;
    this.messages = [];
  }
  
  async fetch(request) {
    // Handle chat messages...
    // But never hibernates - stays in memory forever!
  }
}

// ✅ Correct: Implement hibernation
export class ChatRoom {
  constructor(state, env) {
    this.state = state;
    this.env = env;
    
    // Load persisted state
    this.loadState();
    
    // Set alarm for hibernation after inactivity
    this.resetHibernationTimer();
  }
  
  async loadState() {
    const messages = await this.state.storage.get('messages');
    this.messages = messages || [];
  }
  
  resetHibernationTimer() {
    // Reset alarm for 30 seconds from now
    this.state.storage.setAlarm(Date.now() + 30000);
  }
  
  async fetch(request) {
    // Reset timer on activity
    this.resetHibernationTimer();
    
    // Handle chat messages...
    return new Response('Message processed');
  }
  
  async alarm() {
    // Persist state before hibernation
    await this.state.storage.put('messages', this.messages);
    // DO will hibernate after this method returns
  }
}
```

### Fixing Wrong ID Pattern
```typescript
// ❌ High: Using newUniqueId for named resources
export default {
  async fetch(request: Request, env: Env) {
    const roomId = new URL(request.url).searchParams.get('room');
    
    // Wrong: Creates new DO for same room name
    const id = env.CHAT_ROOM.newUniqueId();
    const stub = env.CHAT_ROOM.get(id);
    
    return stub.fetch(request);
  }
}

// ✅ Correct: Use idFromName for named resources
export default {
  async fetch(request: Request, env: Env) {
    const roomId = new URL(request.url).searchParams.get('room');
    
    // Correct: Same DO for same room name
    const id = env.CHAT_ROOM.idFromName(roomId);
    const stub = env.CHAT_ROOM.get(id);
    
    return stub.fetch(request);
  }
}
```

### Fixing State Persistence
```typescript
// ❌ Critical: State not persisted (lost on hibernation)
export class Counter {
  constructor(state, env) {
    this.state = state;
    this.count = 0;  // Not persisted!
  }
  
  async fetch(request) {
    if (request.url.endsWith('/increment')) {
      this.count++;  // Lost when DO hibernates!
      return new Response(`Count: ${this.count}`);
    }
  }
}

// ✅ Correct: Persist state to storage
export class Counter {
  constructor(state, env) {
    this.state = state;
  }
  
  async fetch(request) {
    if (request.url.endsWith('/increment')) {
      // Persist to storage
      const currentCount = (await this.state.storage.get('count')) || 0;
      const newCount = currentCount + 1;
      await this.state.storage.put('count', newCount);
      
      return new Response(`Count: ${newCount}`);
    }
    
    if (request.url.endsWith('/get')) {
      const count = await this.state.storage.get('count') || 0;
      return new Response(`Count: ${count}`);
    }
  }
}
```

### Fixing Stateless DO Usage
```typescript
// ❌ High: Using DO for stateless operation (overkill)
export default {
  async fetch(request: Request, env: Env) {
    // Using DO for simple API call - unnecessary!
    const id = env.API_PROXY.newUniqueId();
    const stub = env.API_PROXY.get(id);
    return stub.fetch(request);
  }
}

// ✅ Correct: Handle stateless operations in Worker
export default {
  async fetch(request: Request, env: Env) {
    // Simple API call - handle directly in Worker
    const response = await fetch('https://api.example.com/data');
    return response;
  }
}

// ✅ Correct: Use DO for actual stateful coordination
export default {
  async fetch(request: Request, env: Env) {
    const ip = request.headers.get('CF-Connecting-IP');
    
    // Rate limiting needs state - perfect for DO
    const id = env.RATE_LIMITER.idFromName(ip);
    const stub = env.RATE_LIMITER.get(id);
    
    return stub.fetch(request);
  }
}
```

## Durable Objects Use Cases

### Use Durable Objects When:
- **Strong Consistency** required (rate limiting, counters)
- **Stateful Coordination** (chat rooms, game sessions)
- **Real-time Features** (WebSockets, collaboration)
- **Distributed Locks** (coordination between requests)
- **Long-running Operations** (background processing)

### Don't Use Durable Objects When:
- **Stateless Operations** (simple API calls)
- **Read-heavy Caching** (use KV instead)
- **Large File Storage** (use R2 instead)
- **Simple Key-Value** (use KV instead)

## MCP Server Integration

When Cloudflare MCP server is available:
- Query DO performance metrics and best practices
- Get latest hibernation patterns and techniques
- Check DO usage limits and quotas
- Analyze DO performance in production

## Benefits

### Immediate Impact
- **Prevents Resource Waste**: Catches DO anti-patterns that waste resources
- **Ensures Correctness**: Validates state persistence and consistency
- **Improves Performance**: Identifies performance issues in DO usage

### Long-term Value
- **Consistent DO Patterns**: Ensures all DO usage follows best practices
- **Better Resource Management**: Proper hibernation and lifecycle management
- **Reduced Costs**: Efficient DO usage reduces resource consumption

## Usage Examples

### During DO Creation
```typescript
// Developer types: const id = env.MY_DO.newUniqueId();
// SKILL immediately activates: "⚠️ HIGH: Using newUniqueId for every request. Consider idFromName for named resources or if this should be stateless."
```

### During State Management
```typescript
// Developer types: this.count = 0; in constructor
// SKILL immediately activates: "❌ CRITICAL: State not persisted to storage. Use this.state.storage.put() to persist data."
```

### During Hibernation
```typescript
// Developer types: DO without alarm() method
// SKILL immediately activates: "⚠️ HIGH: Durable Object missing hibernation. Add alarm() method and setAlarm() for resource efficiency."
```

## Performance Targets

### DO Creation
- **Excellent**: Reuse existing DOs (idFromName)
- **Good**: Minimal new DO creation
- **Acceptable**: Appropriate DO usage patterns
- **Needs Improvement**: Creating new DOs per request

### State Persistence
- **Excellent**: All state persisted to storage
- **Good**: Critical state persisted
- **Acceptable**: Basic state management
- **Needs Improvement**: State not persisted

### Hibernation
- **Excellent**: Proper hibernation implementation
- **Good**: Basic hibernation setup
- **Acceptable**: Some hibernation consideration
- **Needs Improvement**: No hibernation (resource waste)

This SKILL ensures Durable Objects are used correctly by providing immediate, autonomous validation of DO patterns, preventing common mistakes and ensuring efficient state management.