---
name: claude-mobile-cost-tracking
description: Use when implementing Claude API cost tracking, monitoring token usage, displaying cost metrics in Settings, or user asks about costs - calculates exact costs using $0.003/1k input and $0.015/1k output pricing with per-session aggregation
---

# Claude API Cost Tracking

## Overview

Track and report Claude API usage costs per session with exact pricing, aggregation, and frontend display.

**Core principle:** Track every call. Use exact pricing. Display to users. Provide /cost command.

**Announce at start:** "I'm using the claude-mobile-cost-tracking skill for cost tracking implementation."

## When to Use

- Implementing cost tracking service (Task 3.11)
- Integrating cost display in Settings screen
- Implementing /cost slash command
- Calculating API costs
- Displaying cost metrics to users

## Exact Pricing (Claude Sonnet 4)

```typescript
const PRICING = {
  input: 0.003,   // $0.003 per 1k input tokens
  output: 0.015,  // $0.015 per 1k output tokens
};
```

**Source**: Anthropic API pricing (verified 2025-10-30)

## Implementation Patterns

### 1. Per-Message Cost Calculation

```typescript
interface MessageCost {
  inputTokens: number;
  outputTokens: number;
  inputCost: number;
  outputCost: number;
  totalCost: number;
  timestamp: string;
}

function calculateCost(usage: {
  input_tokens: number;
  output_tokens: number;
}): MessageCost {
  const inputCost = (usage.input_tokens / 1000) * PRICING.input;
  const outputCost = (usage.output_tokens / 1000) * PRICING.output;
  
  return {
    inputTokens: usage.input_tokens,
    outputTokens: usage.output_tokens,
    inputCost,
    outputCost,
    totalCost: inputCost + outputCost,
    timestamp: new Date().toISOString()
  };
}
```

### 2. Session Aggregation

```typescript
interface SessionCosts {
  sessionId: string;
  messages: MessageCost[];
  totalInputTokens: number;
  totalOutputTokens: number;
  totalCost: number;
}

function aggregateSessionCosts(messages: MessageCost[]): SessionCosts {
  return {
    messages,
    totalInputTokens: messages.reduce((sum, m) => sum + m.inputTokens, 0),
    totalOutputTokens: messages.reduce((sum, m) => sum + m.outputTokens, 0),
    totalCost: messages.reduce((sum, m) => sum + m.totalCost, 0)
  };
}
```

### 3. Storage with Session Data

```typescript
// In session JSON file
interface Session {
  id: string;
  projectPath: string;
  messages: Message[];
  costs: SessionCosts; // Add this
  createdAt: string;
}
```

### 4. Frontend Display (Settings Screen)

```typescript
// Settings screen cost section
<View testID="cost-section" style={styles.costSection}>
  <Text style={styles.sectionTitle}>API Usage</Text>
  <Text testID="message-count">Messages: {session.messages.length}</Text>
  <Text testID="input-tokens">Input Tokens: {costs.totalInputTokens.toLocaleString()}</Text>
  <Text testID="output-tokens">Output Tokens: {costs.totalOutputTokens.toLocaleString()}</Text>
  <Text testID="total-cost" style={styles.cost}>
    Total Cost: ${costs.totalCost.toFixed(4)}
  </Text>
</View>
```

### 5. /cost Slash Command

```typescript
// In command.service.ts
if (message.startsWith('/cost')) {
  const sessionCosts = getSessionCosts(sessionId);
  return {
    type: 'slash_command_response',
    command: 'cost',
    data: sessionCosts
  };
}
```

## Backend Service (Task 3.11)

```typescript
// cost.service.ts
export class CostService {
  calculateMessageCost(usage: {input_tokens: number; output_tokens: number}): MessageCost {
    // Implementation from pattern #1
  }
  
  aggregateSessionCosts(sessionId: string): SessionCosts {
    // Implementation from pattern #2
  }
  
  getAllSessionsCosts(): SessionCosts[] {
    // Return costs for all sessions
  }
  
  exportCostsCSV(): string {
    // Export as CSV for analysis
  }
}
```

## Common Mistakes

| Mistake | Reality |
|---------|---------|
| "Cost tracking is optional" | WRONG. Users need visibility. Required feature. |
| "Approximate costs are fine" | WRONG. Use exact: $0.003/$0.015 per 1k. |
| "Track totals only" | WRONG. Per-session tracking enables analysis. |
| "Backend only is enough" | WRONG. Frontend display is user-facing requirement. |

### ❌ WRONG: No cost tracking

```typescript
const stream = await client.messages.stream({...});
// No cost tracking
```

### ✅ CORRECT: Track every call

```typescript
const stream = await client.messages.stream({...});
stream.on('message', (msg) => {
  if (msg.usage) {
    const cost = calculateCost(msg.usage);
    saveSessionCost(sessionId, cost);
  }
});
```

## Red Flags

- "Cost tracking is overhead" → WRONG. Required feature.
- "Users check API dashboard" → WRONG. In-app display required.
- "Approximate is fine" → WRONG. Use exact formulas.

## Integration

- **Use WITH**: `@anthropic-streaming-patterns` (streams provide usage data)
- **Use FOR**: Task 3.11 (cost.service.ts), Settings screen display
