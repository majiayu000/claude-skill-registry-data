---
name: "sqlite-pattern-learner"
description: "Learn from database query patterns and recommend optimized approaches"
tags:
  - "database"
  - "patterns"
  - "learning"
  - "optimization"
  - "sqlite"
version: "1.0.0"
---

# SQLite Pattern Learning

## Purpose

This skill enables you to learn from historical database query patterns and get recommendations for optimal query approaches. Use it to leverage proven patterns from similar use cases instead of reinventing solutions.

## When to Use

Use this skill when you need to:
- Find proven patterns for similar database queries
- Learn from historical query performance data
- Get recommendations for query optimization
- Record successful patterns for future reuse
- Analyze pattern statistics across domains

## Available Hooks

### sqlite.patterns.get

Get pattern recommendations based on domain and description.

**Parameters:**
- `domain` (string, required): Domain area (e.g., 'finance', 'analytics', 'ecommerce')
- `description` (string, required): Description of what you're trying to achieve
- `minConfidence` (number, optional): Minimum confidence threshold (0-1, default: 0.7)
- `maxResults` (number, optional): Maximum number of recommendations (default: 5)

**Returns:**
- `recommendations` (array): List of matching patterns with metadata
- `count` (number): Number of recommendations found

**Example:**
```javascript
const result = await fixiplug.dispatch('sqlite.patterns.get', {
  domain: 'finance',
  description: 'Calculate portfolio value at risk for risk management',
  minConfidence: 0.8,
  maxResults: 3
});

console.log(result.recommendations);
// [
//   {
//     pattern: 'finance_var_calculation',
//     description: 'Portfolio VaR using historical simulation',
//     confidence: 0.95,
//     successRate: 0.92,
//     avgPerformance: 150,
//     usageCount: 42,
//     lastUsed: '2025-11-15'
//   },
//   {
//     pattern: 'finance_monte_carlo_var',
//     description: 'VaR using Monte Carlo simulation',
//     confidence: 0.88,
//     successRate: 0.89,
//     avgPerformance: 320,
//     usageCount: 28,
//     lastUsed: '2025-11-10'
//   }
// ]
```

### sqlite.patterns.find_similar

Find patterns similar to a given description using semantic search.

**Parameters:**
- `description` (string, required): Description to find similar patterns for
- `threshold` (number, optional): Similarity threshold (0-1, default: 0.7)
- `maxResults` (number, optional): Maximum results (default: 10)
- `domain` (string, optional): Filter by domain

**Returns:**
- `similar` (array): Similar patterns with similarity scores
- `count` (number): Number of similar patterns found

**Example:**
```javascript
const similar = await fixiplug.dispatch('sqlite.patterns.find_similar', {
  description: 'Real-time customer analytics dashboard with streaming data',
  threshold: 0.75,
  maxResults: 5,
  domain: 'analytics'
});

console.log(similar.similar);
// [
//   {
//     pattern: 'realtime_dashboard_aggregation',
//     similarity: 0.92,
//     description: 'Streaming analytics with 1-second updates',
//     domain: 'analytics',
//     performance: 85
//   },
//   ...
// ]
```

### sqlite.patterns.statistics

Get pattern usage statistics and performance metrics.

**Parameters:**
- `domain` (string, optional): Filter by domain
- `timeRange` (string, optional): Time range ('day', 'week', 'month', 'all', default: 'week')
- `sortBy` (string, optional): Sort by field ('usage', 'performance', 'success', default: 'usage')

**Returns:**
- `stats` (object): Aggregate statistics
- `patterns` (array): Per-pattern statistics
- `summary` (object): High-level summary

**Example:**
```javascript
const stats = await fixiplug.dispatch('sqlite.patterns.statistics', {
  domain: 'finance',
  timeRange: 'month',
  sortBy: 'success'
});

console.log(stats.summary);
// {
//   totalPatterns: 156,
//   avgSuccessRate: 0.87,
//   avgPerformance: 245,
//   totalUsage: 1842
// }

console.log(stats.patterns.slice(0, 3));
// [
//   {
//     pattern: 'finance_var_calculation',
//     usage: 42,
//     successRate: 0.95,
//     avgPerformance: 150
//   },
//   ...
// ]
```

### sqlite.patterns.record

Record a new pattern or update an existing pattern's performance data.

**Parameters:**
- `patternName` (string, required): Unique pattern identifier
- `domain` (string, required): Domain area
- `description` (string, required): Pattern description
- `successRate` (number, optional): Success rate (0-1)
- `performance` (number, optional): Performance metric (e.g., ms)
- `metadata` (object, optional): Additional metadata

**Returns:**
- `success` (boolean): Whether recording succeeded
- `patternId` (string): Pattern identifier
- `updated` (boolean): Whether pattern was updated vs created

**Example:**
```javascript
const result = await fixiplug.dispatch('sqlite.patterns.record', {
  patternName: 'custom_risk_metric',
  domain: 'finance',
  description: 'Custom risk metric calculation for derivatives',
  successRate: 0.94,
  performance: 180,
  metadata: {
    author: 'trading-team',
    version: '2.1',
    complexity: 'medium'
  }
});

console.log(result.success);  // true
console.log(result.updated);  // false (new pattern)
```

## Best Practices

1. **Be Specific in Descriptions**
   - Good: "Calculate real-time customer lifetime value with cohort analysis"
   - Bad: "Calculate CLV"

2. **Set Appropriate Confidence Thresholds**
   - High-stakes: 0.9+ (financial calculations, security)
   - Standard: 0.7-0.9 (analytics, reporting)
   - Exploratory: 0.5-0.7 (research, experimentation)

3. **Record Successful Patterns**
   - When you find a pattern that works well, record it
   - Include performance metrics and success rates
   - Add metadata for context

4. **Use Domain Filtering**
   - Patterns are domain-specific
   - Cross-domain patterns may not apply
   - Be consistent with domain naming

## Common Use Cases

### Use Case 1: Query Optimization
```javascript
// Find proven patterns for your use case
const patterns = await fixiplug.dispatch('sqlite.patterns.get', {
  domain: 'ecommerce',
  description: 'Product recommendation based on purchase history',
  minConfidence: 0.8
});

// Apply the highest-confidence pattern
const topPattern = patterns.recommendations[0];
console.log(`Using pattern: ${topPattern.pattern}`);
console.log(`Success rate: ${topPattern.successRate * 100}%`);
```

### Use Case 2: Learning from Similar Work
```javascript
// Find what others have done
const similar = await fixiplug.dispatch('sqlite.patterns.find_similar', {
  description: 'Fraud detection in real-time transactions',
  domain: 'security',
  threshold: 0.7
});

// Review similar approaches
similar.similar.forEach(p => {
  console.log(`${p.pattern}: ${p.description} (similarity: ${p.similarity})`);
});
```

### Use Case 3: Performance Benchmarking
```javascript
// Check domain statistics
const stats = await fixiplug.dispatch('sqlite.patterns.statistics', {
  domain: 'analytics',
  timeRange: 'month',
  sortBy: 'performance'
});

// Find fastest patterns
const fastest = stats.patterns.slice(0, 5);
console.log('Top 5 fastest patterns:', fastest);
```

### Use Case 4: Contributing Back
```javascript
// Record your successful pattern
await fixiplug.dispatch('sqlite.patterns.record', {
  patternName: 'realtime_fraud_detection_v2',
  domain: 'security',
  description: 'Real-time fraud detection with ML scoring and rule engine',
  successRate: 0.96,
  performance: 45,  // ms
  metadata: {
    version: '2.0',
    mlModel: 'gradient-boosted-trees',
    accuracy: 0.98
  }
});
```

## Error Handling

All hooks may throw errors:
- `ValidationError`: Invalid parameters
- `ServiceError`: SQLite service unavailable
- `TimeoutError`: Request exceeded timeout
- `NotFoundError`: No patterns found

Always wrap calls in try-catch:
```javascript
try {
  const result = await fixiplug.dispatch('sqlite.patterns.get', params);
  // Use result
} catch (error) {
  if (error.name === 'ValidationError') {
    console.error('Invalid parameters:', error.validationErrors);
  } else if (error.name === 'TimeoutError') {
    console.error('Request timed out, try again');
  } else {
    console.error('Unexpected error:', error.message);
  }
}
```

## Performance Characteristics

- **Latency**: 50-200ms (typical)
- **Cache Hit Rate**: ~70% (frequently accessed patterns)
- **Concurrent Requests**: Limited by process pool (default: 4)

## Prerequisites

- SQLite Extensions Framework must be installed
- Environment variable: `SQLITE_FRAMEWORK_PATH` must be set
- Python 3.8+ with required dependencies

## Related Skills

- `sqlite-extension-generator`: Generate optimized SQLite extensions
- `sqlite-agent-amplification`: Create dynamic tools based on patterns
- `sqlite-agent-context`: Understand agent capabilities and limitations

## Version

1.0.0 - Initial release
