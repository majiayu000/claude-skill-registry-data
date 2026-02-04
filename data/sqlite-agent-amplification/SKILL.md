---
name: "sqlite-agent-amplification"
description: "Dynamically create tools and consult peer agents for enhanced capabilities"
tags:
  - "agent"
  - "amplification"
  - "dynamic"
  - "learning"
  - "meta-programming"
version: "1.0.0"
---

# Agent Amplification

## Purpose

This skill enables agents to amplify their capabilities by:
- Creating new tools dynamically based on requirements
- Consulting specialized peer agents for expert advice
- Recording decision outcomes for machine learning
- Tracking capability evolution over time

Think of it as "meta-programming" for AI agents - giving them the ability to extend themselves.

## When to Use

Use this skill when agents need to:
- Create custom tools that don't exist yet
- Consult specialists for domain-specific problems
- Learn from past decisions and outcomes
- Track how capabilities evolve over time
- Coordinate with other agents in multi-agent systems

## Available Hooks

### sqlite.agent.create_tool

Dynamically create a new tool based on requirements.

**Parameters:**
- `name` (string, required): Tool name (snake_case)
- `description` (string, required): What the tool does
- `parameters` (object, required): Tool parameters schema (JSON Schema)
- `implementation` (string, required): Implementation language ('python', 'javascript', 'sql')
- `code` (string, optional): Custom implementation code
- `metadata` (object, optional): Additional metadata

**Returns:**
- `toolId` (string): Unique tool identifier
- `hookName` (string): FixiPlug hook name to call the tool
- `definition` (object): LLM tool definition
- `success` (boolean): Whether creation succeeded

**Example:**
```javascript
const tool = await fixiplug.dispatch('sqlite.agent.create_tool', {
  name: 'portfolio_rebalancer',
  description: 'Rebalance investment portfolio to target allocation',
  parameters: {
    type: 'object',
    properties: {
      currentHoldings: {
        type: 'object',
        description: 'Current holdings by ticker'
      },
      targetAllocation: {
        type: 'object',
        description: 'Target allocation percentages'
      },
      cashAvailable: {
        type: 'number',
        description: 'Cash available for rebalancing'
      }
    },
    required: ['currentHoldings', 'targetAllocation']
  },
  implementation: 'python',
  code: `
def rebalance(current_holdings, target_allocation, cash_available=0):
    # Custom rebalancing logic
    total_value = sum(current_holdings.values()) + cash_available
    trades = []
    for ticker, target_pct in target_allocation.items():
        target_value = total_value * target_pct
        current_value = current_holdings.get(ticker, 0)
        diff = target_value - current_value
        if abs(diff) > 0.01:  # Threshold
            trades.append({
                'ticker': ticker,
                'action': 'buy' if diff > 0 else 'sell',
                'value': abs(diff)
            })
    return {'trades': trades, 'total_value': total_value}
  `,
  metadata: {
    author: 'portfolio-agent',
    domain: 'finance',
    version: '1.0.0'
  }
});

console.log(`Created tool: ${tool.hookName}`);
// 'dynamic_tool.portfolio_rebalancer'

// Now the tool is available as a FixiPlug hook
const result = await fixiplug.dispatch(tool.hookName, {
  currentHoldings: { 'AAPL': 5000, 'GOOGL': 3000 },
  targetAllocation: { 'AAPL': 0.6, 'GOOGL': 0.4 }
});

console.log(result.trades);
// [{ ticker: 'AAPL', action: 'buy', value: 800 }]
```

### sqlite.agent.record_decision

Record a decision and its outcome for learning.

**Parameters:**
- `decision` (object, required): Decision details
  - `type` (string): Decision type
  - `context` (object): Decision context
  - `chosen` (any): What was chosen
  - `alternatives` (array): Other options considered
- `outcome` (object, required): Outcome details
  - `success` (boolean): Whether outcome was successful
  - `metrics` (object): Quantitative metrics
  - `feedback` (string): Qualitative feedback
- `metadata` (object, optional): Additional metadata

**Returns:**
- `decisionId` (string): Unique decision identifier
- `recorded` (boolean): Whether recording succeeded
- `insights` (object): Any immediate insights

**Example:**
```javascript
const record = await fixiplug.dispatch('sqlite.agent.record_decision', {
  decision: {
    type: 'algorithm-selection',
    context: {
      problemType: 'time-series-forecasting',
      dataSize: 10000,
      latencyRequirement: 100  // ms
    },
    chosen: 'ARIMA',
    alternatives: ['LSTM', 'Prophet', 'XGBoost']
  },
  outcome: {
    success: true,
    metrics: {
      accuracy: 0.94,
      latency: 85,  // ms
      memoryUsage: 120  // MB
    },
    feedback: 'ARIMA performed well for this stationary time series'
  },
  metadata: {
    agent: 'forecasting-specialist',
    timestamp: new Date().toISOString()
  }
});

console.log(`Decision recorded: ${record.decisionId}`);
console.log('Insights:', record.insights);
// { recommendation: 'ARIMA is consistently successful for stationary series' }
```

### sqlite.agent.consult_peers

Consult specialized peer agents for expert advice.

**Parameters:**
- `question` (string, required): Question to ask
- `domain` (string, required): Domain area
- `context` (object, optional): Additional context
- `maxPeers` (number, optional): Max peers to consult (default: 3)
- `minConfidence` (number, optional): Min confidence threshold (default: 0.7)

**Returns:**
- `advice` (array): Advice from peer agents
- `consensus` (object): Consensus recommendation
- `confidence` (number): Overall confidence

**Example:**
```javascript
const advice = await fixiplug.dispatch('sqlite.agent.consult_peers', {
  question: 'Best approach for real-time fraud detection on transaction stream?',
  domain: 'security',
  context: {
    transactionVolume: 10000,  // per second
    latencyBudget: 50,  // ms
    fraudRate: 0.02  // 2%
  },
  maxPeers: 3,
  minConfidence: 0.8
});

console.log('Advice received:');
advice.advice.forEach(a => {
  console.log(`${a.peer}: ${a.recommendation} (confidence: ${a.confidence})`);
});
// fraud-ml-specialist: Use gradient boosting with real-time scoring (0.92)
// security-architect: Combine rule-based and ML approaches (0.88)
// data-engineer: Stream processing with windowed aggregation (0.85)

console.log('Consensus:', advice.consensus);
// {
//   approach: 'hybrid-ml-rules',
//   reasoning: 'Combine fast rule-based filtering with ML scoring',
//   confidence: 0.88,
//   expectedPerformance: { latency: 35, accuracy: 0.96 }
// }
```

### sqlite.agent.track_evolution

Track how agent capabilities evolve over time.

**Parameters:**
- `capability` (string, required): Capability name
- `metrics` (object, required): Current metrics
- `timestamp` (string, optional): Timestamp (ISO 8601)
- `metadata` (object, optional): Additional metadata

**Returns:**
- `evolutionId` (string): Tracking entry ID
- `trend` (object): Capability trend analysis
- `recorded` (boolean): Success status

**Example:**
```javascript
const evolution = await fixiplug.dispatch('sqlite.agent.track_evolution', {
  capability: 'query-optimization',
  metrics: {
    avgLatency: 120,  // ms
    successRate: 0.94,
    complexity: 'medium',
    toolsUsed: 3
  },
  timestamp: new Date().toISOString(),
  metadata: {
    agent: 'database-optimizer',
    version: '2.1.0'
  }
});

console.log('Trend:', evolution.trend);
// {
//   direction: 'improving',
//   latencyChange: -15,  // 15ms faster than last week
//   successRateChange: +0.03,  // 3% better
//   recommendation: 'Current approach is working well, maintain'
// }
```

## Best Practices

### 1. Tool Creation Strategy

**When to Create Tools:**
- Specific task needed repeatedly
- Existing tools don't quite fit
- Domain-specific logic required
- Performance optimization needed

**When NOT to Create Tools:**
- One-off tasks (just do them directly)
- General tools already exist
- Overly complex requirements
- Unclear specification

### 2. Decision Recording Strategy

**Always Record:**
- Algorithm/approach selections
- Parameter tuning decisions
- Architecture choices
- Performance trade-offs

**Include Context:**
- Problem characteristics
- Constraints and requirements
- Why alternatives were rejected
- Expected vs actual outcomes

### 3. Peer Consultation Strategy

**Good Questions:**
- Specific, well-defined problems
- Domain expertise needed
- Multiple valid approaches exist
- Trade-off analysis required

**Poor Questions:**
- Too broad or vague
- Already have clear answer
- Domain not specified
- No context provided

### 4. Evolution Tracking Strategy

**Track Over Time:**
- Core capabilities (weekly/monthly)
- Critical metrics
- Success rates
- Performance characteristics

**Look for:**
- Trends (improving/degrading)
- Anomalies (sudden changes)
- Plateaus (need new approach)
- Correlations (what affects what)

## Common Use Cases

### Use Case 1: Custom Financial Tool
```javascript
// Create specialized risk calculator
const tool = await fixiplug.dispatch('sqlite.agent.create_tool', {
  name: 'var_calculator',
  description: 'Calculate Value at Risk using historical simulation',
  parameters: {
    type: 'object',
    properties: {
      returns: { type: 'array', items: { type: 'number' } },
      confidenceLevel: { type: 'number', minimum: 0, maximum: 1 }
    },
    required: ['returns', 'confidenceLevel']
  },
  implementation: 'python',
  code: `
import numpy as np

def calculate_var(returns, confidence_level):
    sorted_returns = np.sort(returns)
    index = int((1 - confidence_level) * len(sorted_returns))
    var = sorted_returns[index]
    return {'var': float(var), 'confidence': confidence_level}
  `
});

// Use the tool
const var95 = await fixiplug.dispatch(tool.hookName, {
  returns: [-0.02, 0.01, -0.03, 0.02, -0.01],
  confidenceLevel: 0.95
});
console.log('VaR (95%):', var95.var);
```

### Use Case 2: Learning from Decisions
```javascript
// Try approach A
const resultA = await someComplexTask();

// Record what happened
await fixiplug.dispatch('sqlite.agent.record_decision', {
  decision: {
    type: 'approach-selection',
    context: { taskType: 'data-pipeline', dataVolume: '1TB' },
    chosen: 'stream-processing',
    alternatives: ['batch-processing', 'hybrid']
  },
  outcome: {
    success: resultA.success,
    metrics: {
      processingTime: resultA.duration,
      throughput: resultA.recordsPerSec,
      cost: resultA.totalCost
    },
    feedback: resultA.issues || 'Worked well'
  }
});

// Later, system learns: "stream-processing works well for 1TB data"
```

### Use Case 3: Multi-Agent Collaboration
```javascript
// Agent needs advice on complex problem
const advice = await fixiplug.dispatch('sqlite.agent.consult_peers', {
  question: 'How to optimize this slow database query?',
  domain: 'database',
  context: {
    queryType: 'complex-join',
    tableSize: '100M rows',
    currentLatency: '5s',
    targetLatency: '500ms'
  }
});

// Apply consensus recommendation
const approach = advice.consensus.approach;
console.log(`Using approach: ${approach}`);
```

### Use Case 4: Self-Improvement Tracking
```javascript
// Weekly capability tracking
setInterval(async () => {
  const metrics = await measurePerformance();

  await fixiplug.dispatch('sqlite.agent.track_evolution', {
    capability: 'code-generation',
    metrics: {
      avgQuality: metrics.quality,
      successRate: metrics.success,
      avgTime: metrics.time
    }
  });
}, 7 * 24 * 60 * 60 * 1000);  // Weekly
```

## Performance Characteristics

- **Tool Creation**: ~1-3 seconds
- **Decision Recording**: ~100-300ms
- **Peer Consultation**: ~1-5 seconds (depends on peers available)
- **Evolution Tracking**: ~50-150ms

## Error Handling

Possible errors:
- `ValidationError`: Invalid parameters
- `ToolCreationError`: Tool creation failed
- `ServiceError`: SQLite service unavailable
- `TimeoutError`: Request timed out
- `PeerConsultationError`: No peers available

Example:
```javascript
try {
  const tool = await fixiplug.dispatch('sqlite.agent.create_tool', params);
} catch (error) {
  if (error.name === 'ToolCreationError') {
    console.error('Tool creation failed:', error.reason);
    console.error('Suggestions:', error.suggestions);
  } else if (error.name === 'ValidationError') {
    console.error('Invalid parameters:', error.validationErrors);
  } else {
    console.error('Unexpected error:', error.message);
  }
}
```

## Advanced Features

### Dynamic Tool Registration

Created tools are automatically registered as FixiPlug hooks:
```javascript
const tool = await fixiplug.dispatch('sqlite.agent.create_tool', {...});
// Tool is now available at: tool.hookName

// Can be called directly
await fixiplug.dispatch(tool.hookName, params);

// Or exposed to LLMs via adapters
const adapter = new AnthropicAdapter(agent);
const tools = await adapter.getToolDefinitions();
// Includes dynamically created tools
```

### Peer Network

Peer consultation leverages a network of specialized agents:
- Each peer has expertise domains
- Confidence scores indicate certainty
- Consensus algorithm weighs expertise + confidence
- Historical success rates influence recommendations

### Learning Loop

Decision recording enables continuous learning:
1. Record decisions + outcomes
2. System learns patterns (what works when)
3. Future recommendations improve
4. Capability evolution tracked automatically

## Prerequisites

- SQLite Extensions Framework installed
- Environment variable: `SQLITE_FRAMEWORK_PATH`
- Python 3.8+ (for Python-based tools)
- Node.js 16+ (for JavaScript-based tools)

## Related Skills

- `sqlite-pattern-learner`: Find proven patterns
- `sqlite-extension-generator`: Generate optimized code
- `sqlite-agent-context`: Understand agent capabilities

## Version

1.0.0 - Initial release
