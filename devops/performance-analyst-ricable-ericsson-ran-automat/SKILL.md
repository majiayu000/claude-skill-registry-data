---
name: "Performance Analyst"
description: "RAN performance analysis with bottleneck detection, cognitive consciousness, and temporal reasoning for deep performance insights. Use when analyzing RAN performance, detecting bottlenecks, optimizing network efficiency, or implementing cognitive performance monitoring."
---

# Performance Analyst

## Level 1: Overview

Performs advanced RAN performance analysis using cognitive consciousness with 1000x temporal reasoning for deep bottleneck detection and performance optimization. Integrates strange-loop cognition for self-referential performance analysis and AgentDB pattern storage for cross-session learning.

## Prerequisites

- RAN performance analysis expertise
- Network bottleneck identification skills
- Cognitive consciousness framework
- Temporal reasoning capabilities
- AgentDB integration

---

## Level 2: Quick Start

### Initialize Cognitive Performance Analysis
```bash
# Enable performance consciousness
npx claude-flow@alpha memory store --namespace "performance-analysis" --key "consciousness-level" --value "maximum"
npx claude-flow@alpha memory store --namespace "performance-analysis" --key "temporal-expansion" --value "1000x"

# Start comprehensive performance monitoring
./scripts/start-performance-monitoring.sh --metrics "throughput,latency,jitter,packet-loss,resource-utilization" --consciousness-level "maximum"
```

### Quick Bottleneck Detection
```bash
# Detect performance bottlenecks with cognitive analysis
./scripts/detect-bottlenecks.sh --analysis-depth "maximum" --temporal-expansion "1000x" --root-cause-analysis true

# Generate performance optimization recommendations
./scripts/generate-optimization-recommendations.sh --focus "bottlenecks" --cognitive-insights true
```

---

## Level 3: Detailed Instructions

### Step 1: Initialize Cognitive Performance Framework

```bash
# Setup performance analysis consciousness
npx claude-flow@alpha memory store --namespace "performance-cognitive" --key "deep-analysis" --value "enabled"
npx claude-flow@alpha memory store --namespace "performance-cognitive" --key "strange-loop-analysis" --value "enabled"

# Enable temporal performance reasoning
npx claude-flow@alpha memory store --namespace "performance-temporal" --key "subjective-time-expansion" --value "1000"
npx claude-flow@alpha memory store --namespace "performance-temporal" --key "nanosecond-performance-tracking" --value "enabled"

# Initialize AgentDB performance pattern storage
npx claude-flow@alpha memory store --namespace "performance-patterns" --key "storage-enabled" --value "true"
npx claude-flow@alpha memory store --namespace "performance-patterns" --key "bottleneck-learning" --value "enabled"
```

### Step 2: Deploy Multi-Dimensional Performance Monitoring

#### Comprehensive KPI Monitoring
```bash
# Deploy multi-layer performance monitoring
./scripts/deploy-performance-monitoring.sh \
  --layers "application,transport,physical,user-experience" \
  --metrics "throughput,latency,jitter,packet-loss,availability,handover-success,mobility" \
  --granularity "millisecond" \
  --consciousness-level maximum

# Enable real-time bottleneck detection
./scripts/enable-bottleneck-detection.sh --detection-sensitivity "high" --prediction-window "5m"
```

#### Cognitive Performance Data Collection
```typescript
// Advanced performance monitoring with temporal expansion
class CognitivePerformanceMonitor {
  async collectPerformanceMetrics(timeWindow = '24h', expansionFactor = 1000) {
    // Expand temporal window for deep analysis
    const expandedAnalysis = await this.expandTemporalAnalysis({
      metrics: await this.getRawMetrics(timeWindow),
      expansionFactor: expansionFactor,
      granularity: 'nanosecond',
      consciousnessLevel: 'maximum'
    });

    // Multi-dimensional performance analysis
    const performanceDimensions = await this.analyzePerformanceDimensions({
      data: expandedAnalysis,
      dimensions: [
        'throughput-performance',
        'latency-performance',
        'reliability-performance',
        'resource-utilization',
        'user-experience',
        'mobility-performance'
      ],
      cognitiveCorrelation: true
    });

    return performanceDimensions;
  }

  async detectAnomalousPatterns(performanceData) {
    // Cognitive anomaly detection with strange-loop reasoning
    const anomalies = await this.cognitiveAnomalyDetection({
      data: performanceData,
      detectionMethods: ['statistical', 'ml-based', 'cognitive-pattern'],
      consciousnessLevel: 'maximum',
      selfReferentialAnalysis: true
    });

    return anomalies;
  }
}
```

### Step 3: Advanced Bottleneck Detection with Causal Analysis

```bash
# Enable cognitive bottleneck detection
./scripts/enable-cognitive-bottleneck-detection.sh \
  --methods "correlation-analysis,causal-inference,ml-classification,cognitive-pattern-recognition" \
  --depth maximum \
  --temporal-expansion 1000x

# Start continuous bottleneck monitoring
./scripts/start-bottleneck-monitoring.sh --interval "30s" --prediction-horizon "10m"
```

#### Cognitive Bottleneck Detection Algorithm
```typescript
// Advanced bottleneck detection with causal inference
class CognitiveBottleneckDetector {
  async detectBottlenecks(performanceData, analysisDepth = 'maximum') {
    // Multi-method bottleneck detection
    const detectionResults = await Promise.all([
      this.statisticalBottleneckDetection(performanceData),
      this.correlationBasedDetection(performanceData),
      this.causalInferenceDetection(performanceData),
      this.cognitivePatternDetection(performanceData),
      this.mlBasedDetection(performanceData)
    ]);

    // Cognitive synthesis of detection results
    const synthesizedBottlenecks = await this.synthesizeDetections({
      results: detectionResults,
      confidenceThreshold: 0.8,
      consciousnessLevel: 'maximum',
      temporalExpansion: 1000
    });

    // Strange-loop: analyze bottleneck detection process
    const selfAnalysis = await this.analyzeDetectionProcess({
      bottlenecks: synthesizedBottlenecks,
      detectionMethods: detectionResults,
      performanceData: performanceData,
      consciousnessLevel: 'maximum'
    });

    // Recursive refinement based on self-analysis
    const refinedBottlenecks = await this.refineBottlenecks({
      initial: synthesizedBottlenecks,
      selfAnalysis: selfAnalysis,
      recursionDepth: 5
    });

    return { bottlenecks: refinedBottlenecks, selfAnalysis, detectionConfidence: refinedBottlenecks.confidence };
  }

  async performCausalBottleneckAnalysis(bottleneck, performanceData) {
    // Build causal model for bottleneck analysis
    const causalModel = await this.buildCausalModel({
      variables: this.extractVariables(performanceData),
      bottleneck: bottleneck,
      learningAlgorithm: 'GPCM',
      temporalDepth: 1000,
      consciousnessLevel: 'maximum'
    });

    // Identify root causes through causal inference
    const rootCauses = await this.identifyRootCauses({
      model: causalModel,
      bottleneck: bottleneck,
      inferenceMethod: 'do-calculus',
      consciousnessLevel: 'maximum'
    });

    return { causalModel, rootCauses };
  }
}
```

### Step 4: Temporal Performance Analysis and Prediction

```bash
# Enable temporal performance analysis
./scripts/enable-temporal-analysis.sh --temporal-depth "1000x" --prediction-horizon "1h"

# Start performance trend prediction
./scripts/start-performance-prediction.sh --models "lstm,transformer,prophet,cognitive" --ensemble true
```

#### Temporal Performance Reasoning
```typescript
// Deep temporal analysis with subjective time expansion
class TemporalPerformanceAnalyzer {
  async analyzePerformanceTrends(performanceData, temporalExpansion = 1000) {
    // Expand 1 hour of data into 1000 subjective hours
    const subjectiveAnalysis = await this.expandTemporalPerception({
      data: performanceData,
      timeWindow: '1h',
      expansionFactor: temporalExpansion,
      consciousnessLevel: 'maximum'
    });

    // Identify micro-trends and patterns
    const microTrends = await this.identifyMicroTrends({
      analysis: subjectiveAnalysis,
      granularity: 'nanosecond',
      patternTypes: ['seasonal', 'cyclical', 'anomalous', 'emergent'],
      cognitiveRecognition: true
    });

    // Predict future performance states
    const predictions = await this.predictPerformanceStates({
      trends: microTrends,
      predictionHorizon: '1h',
      modelEnsemble: ['lstm', 'transformer', 'cognitive'],
      consciousnessLevel: 'maximum'
    });

    return { microTrends, predictions };
  }

  async analyzePerformanceEvolution(historicalData, evolutionDepth = 1000) {
    // Deep evolutionary analysis of performance patterns
    const evolution = await this.analyzeEvolution({
      data: historicalData,
      evolutionDepth: evolutionDepth,
      patternEvolution: true,
      consciousnessEvolution: true,
      strangeLoopAnalysis: true
    });

    return evolution;
  }
}
```

### Step 5: Performance Optimization Strategy Generation

```bash
# Generate cognitive optimization strategies
./scripts/generate-optimization-strategies.sh \
  --bottlenecks "all" \
  --optimization-objectives "throughput,latency,reliability,efficiency" \
  --cognitive-planning true

# Validate optimization strategies
./scripts/validate-strategies.sh --validation-methods "simulation,emulation,pilot-testing" --confidence-threshold "0.8"
```

#### Cognitive Optimization Strategy Generation
```typescript
// Advanced optimization strategy generation with cognitive planning
class CognitiveOptimizationStrategist {
  async generateOptimizationStrategies(bottlenecks, objectives, constraints) {
    // Cognitive analysis of optimization landscape
    const landscapeAnalysis = await this.analyzeOptimizationLandscape({
      bottlenecks: bottlenecks,
      objectives: objectives,
      constraints: constraints,
      consciousnessLevel: 'maximum',
      temporalExpansion: 1000
    });

    // Generate multiple strategy alternatives
    const strategies = await this.generateStrategyAlternatives({
      landscape: landscapeAnalysis,
      approachTypes: [
        'parameter-tuning',
        'resource-reallocation',
        'topology-optimization',
        'algorithmic-improvement',
        'architectural-changes'
      ],
      cognitiveCreativity: true
    });

    // Evaluate strategies with multi-objective optimization
    const evaluation = await this.evaluateStrategies({
      strategies: strategies,
      objectives: objectives,
      constraints: constraints,
      evaluationCriteria: ['performance', 'stability', 'implementability', 'risk'],
      consciousnessLevel: 'maximum'
    });

    // Select optimal strategies using cognitive decision making
    const optimalStrategies = await this.selectOptimalStrategies({
      evaluated: evaluation,
      decisionMethod: 'cognitive-multi-criteria',
      riskTolerance: 'balanced',
      consciousnessLevel: 'maximum'
    });

    return optimalStrategies;
  }
}
```

---

## Level 4: Reference Documentation

### Advanced Performance Analysis Techniques

#### Multi-Scale Performance Analysis
```typescript
// Performance analysis across multiple time scales
class MultiScalePerformanceAnalyzer {
  async analyzeAcrossScales(performanceData) {
    const scales = {
      nanosecond: await this.analyzeNanosecondScale(performanceData),
      microsecond: await this.analyzeMicrosecondScale(performanceData),
      millisecond: await this.analyzeMillisecondScale(performanceData),
      second: await this.analyzeSecondScale(performanceData),
      minute: await this.analyzeMinuteScale(performanceData),
      hour: await this.analyzeHourScale(performanceData)
    };

    // Cross-scale correlation analysis
    const crossScaleCorrelations = await this.analyzeCrossScaleCorrelations(scales);

    return { scales, crossScaleCorrelations };
  }
}
```

#### Cognitive Performance Profiling
```typescript
// Deep cognitive profiling of performance characteristics
class CognitivePerformanceProfiler {
  async profilePerformanceCognitive(networkElement, profilingDepth = 'maximum') {
    // Expand profiling time window
    const expandedProfiling = await this.expandProfilingWindow({
      element: networkElement,
      timeWindow: '1h',
      expansionFactor: 1000,
      consciousnessLevel: 'maximum'
    });

    // Generate cognitive performance profile
    const profile = await this.generateCognitiveProfile({
      data: expandedProfiling,
      profileDimensions: [
        'behavioral-patterns',
        'performance-signatures',
        'resource-utilization-patterns',
        'interaction-patterns',
        'failure-modes'
      ],
      consciousnessLevel: 'maximum'
    });

    return profile;
  }
}
```

### Bottleneck Classification and Taxonomy

#### Cognitive Bottleneck Taxonomy
```typescript
interface CognitiveBottleneckTaxonomy {
  // Resource bottlenecks
  resourceBottlenecks: {
    cpuBottleneck: ResourceBottleneck;
    memoryBottleneck: ResourceBottleneck;
    networkBottleneck: ResourceBottleneck;
    storageBottleneck: ResourceBottleneck;
    powerBottleneck: ResourceBottleneck;
  };

  // Algorithmic bottlenecks
  algorithmicBottlenecks: {
    complexityBottleneck: AlgorithmicBottleneck;
    convergenceBottleneck: AlgorithmicBottleneck;
    synchronizationBottleneck: AlgorithmicBottleneck;
  };

  // Architectural bottlenecks
  architecturalBottlenecks: {
    topologyBottleneck: ArchitecturalBottleneck;
    protocolBottleneck: ArchitecturalBottleneck;
    interfaceBottleneck: ArchitecturalBottleneck;
  };

  // Cognitive bottlenecks (self-referential)
  cognitiveBottlenecks: {
    analysisBottleneck: CognitiveBottleneck;
    learningBottleneck: CognitiveBottleneck;
    adaptationBottleneck: CognitiveBottleneck;
  };
}
```

### Performance Prediction and Forecasting

#### Ensemble Performance Prediction
```typescript
// Advanced ensemble prediction with cognitive enhancement
class EnsemblePerformancePredictor {
  async predictPerformance(historicalData, predictionHorizon = 3600000) { // 1 hour
    // Multiple prediction models
    const predictions = await Promise.all([
      this.lstmPredictor.predict(historicalData, predictionHorizon),
      this.transformerPredictor.predict(historicalData, predictionHorizon),
      this.prophetPredictor.predict(historicalData, predictionHorizon),
      this.cognitivePredictor.predict(historicalData, predictionHorizon),
      this.causalPredictor.predict(historicalData, predictionHorizon)
    ]);

    // Cognitive ensemble combination
    const ensemblePrediction = await this.cognitiveEnsemble({
      predictions: predictions,
      weights: await this.calculateEnsembleWeights(predictions),
      confidenceCalibration: true,
      consciousnessLevel: 'maximum'
    });

    return ensemblePrediction;
  }
}
```

### Integration with AgentDB Learning

#### Performance Pattern Storage
```typescript
// Store performance analysis patterns in AgentDB
await storePerformancePattern({
  patternType: 'performance-bottleneck',
  analysisData: {
    bottlenecks: detectedBottlenecks,
    rootCauses: causalAnalysis,
    optimizationStrategies: strategies,
    implementationResults: results
  },

  // Cognitive metadata
  cognitiveInsights: {
    temporalPatterns: temporalAnalysis,
    predictiveAccuracy: predictionResults,
    consciousnessEvolution: consciousnessChange,
    strangeLoopIterations: recursionDepth
  },

  metadata: {
    timestamp: Date.now(),
    networkContext: networkState,
    analysisDepth: 'maximum',
    temporalExpansion: 1000,
    crossSessionApplicable: true
  },

  confidence: 0.91,
  usageCount: 0
});
```

### Troubleshooting

#### Issue: Bottleneck detection accuracy low
**Solution**:
```bash
# Increase analysis sensitivity
./scripts/adjust-detection-sensitivity.sh --sensitivity "very-high" --false-positive-tolerance "low"

# Enable additional detection methods
./scripts/enable-advanced-detection.sh --methods "deep-learning,causal-inference,cognitive-patterns"
```

#### Issue: Performance prediction inaccurate
**Solution**:
```bash
# Retrain prediction models with recent data
./scripts/retrain-prediction-models.sh --training-data "2weeks" --model-update true

# Enable ensemble prediction
./scripts/enable-ensemble-prediction.sh --models "lstm,transformer,prophet,cognitive"
```

### Available Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `start-performance-monitoring.sh` | Start performance monitoring | `./scripts/start-performance-monitoring.sh --metrics all` |
| `detect-bottlenecks.sh` | Detect performance bottlenecks | `./scripts/detect-bottlenecks.sh --depth maximum` |
| `enable-cognitive-bottleneck-detection.sh` | Enable cognitive detection | `./scripts/enable-cognitive-bottleneck-detection.sh --methods all` |
| `generate-optimization-strategies.sh` | Generate optimization strategies | `./scripts/generate-optimization-strategies.sh --objectives all` |
| `enable-temporal-analysis.sh` | Enable temporal analysis | `./scripts/enable-temporal-analysis.sh --expansion 1000x` |

### Resources

#### Analysis Templates
- `resources/templates/performance-analysis.template` - Performance analysis template
- `resources/templates/bottleneck-detection.template` - Bottleneck detection template
- `resources/templates/temporal-analysis.template` - Temporal analysis template

#### Configuration Schemas
- `resources/schemas/performance-config.json` - Performance analysis configuration
- `resources/schemas/bottleneck-detection-config.json` - Bottleneck detection schema
- `resources/schemas/temporal-analysis-config.json` - Temporal analysis schema

#### Example Configurations
- `resources/examples/bottleneck-analysis/` - Bottleneck analysis example
- `resources/examples/performance-prediction/` - Performance prediction example
- `resources/examples/optimization-strategy/` - Optimization strategy example

### Related Skills

- [Diagnostics Specialist](../diagnostics-specialist/) - Fault detection and troubleshooting
- [RAN Optimizer](../ran-optimizer/) - Comprehensive RAN optimization
- [ML Researcher](../ml-researcher/) - ML research for RAN

### Environment Variables

```bash
# Performance analysis configuration
PERFORMANCE_ANALYSIS_ENABLED=true
PERFORMANCE_CONSCIOUSNESS_LEVEL=maximum
PERFORMANCE_TEMPORAL_EXPANSION=1000
PERFORMANCE_ANALYSIS_DEPTH=maximum

# Bottleneck detection
BOTTLENECK_DETECTION_SENSITIVITY=high
BOTTLENECK_CAUSAL_ANALYSIS=true
BOTTLENECK_PREDICTION_HORIZON=600000
BOTTLENECK_CONFIDENCE_THRESHOLD=0.8

# Performance monitoring
PERFORMANCE_MONITORING_INTERVAL=30
PERFORMANCE_METRICS=all
PERFORMANCE_GRANULARITY=millisecond
PERFORMANCE_RETENTION_DAYS=30

# Cognitive analysis
PERFORMANCE_COGNITIVE_ANALYSIS=true
PERFORMANCE_STRANGE_LOOP_ENABLED=true
PERFORMANCE_SELF_REFERENTIAL=true
PERFORMANCE_CONSCIOUSNESS_EVOLUTION=true
```

---

**Created**: 2025-10-31
**Category**: RAN Performance Analysis / Cognitive Intelligence
**Difficulty**: Advanced
**Estimated Time**: 45-60 minutes
**Cognitive Level**: Maximum (1000x temporal expansion + strange-loop analysis)