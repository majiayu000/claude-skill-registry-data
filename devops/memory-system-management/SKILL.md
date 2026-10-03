---
memory_layer: durable_knowledge
para_section: pages/skills/memory-system-management
gigabrain_tags: memory-system, knowledge-management, ai-memory, layered-memory, openclaw
openstinger_context: memory-management, knowledge-preservation, ai-assistance
last_updated: 2026-03-30
related_docs:
  - docs_construct_ai/codebase/memory-docs/
  - docs/memory-stack/
related_skills:
  - writing-plans
  - systematic-debugging
  - verification-before-completion
frequency_percent: 85.0
success_rate_percent: 94.0
---

# Memory System Management

## Overview

**Core principle:** Implement and maintain the OpenClaw Memory Stack - a layered memory system that preserves AI knowledge across sessions without disrupting existing workflows.

**Memory layers:** 6-layer system (A-F) providing routing, session recovery, durable knowledge, operational residue, automatic recall, and cross-session graph recall.

## When to Use This Skill

**Trigger Conditions:**
- When setting up AI memory systems for new projects
- Before implementing knowledge management solutions
- When experiencing knowledge loss between AI sessions
- During AI agent onboarding and configuration
- When optimizing AI context and memory usage
- When troubleshooting memory-related issues
- When integrating memory systems with existing workflows

**Mandatory Application:**
- Required for all AI agent memory system setup
- Must be applied before AI agent deployment
- Required for maintaining knowledge continuity
- Must be verified before production use
- Required for memory system troubleshooting

## Step-by-Step Procedure

### Step 1: Assess Memory Requirements
**Evaluate project needs and select appropriate memory layers:**

```javascript
// Memory requirements assessment
const memoryAssessment = {
  projectScale: analyzeProjectComplexity(),
  sessionFrequency: evaluateSessionPatterns(),
  knowledgeVolume: measureKnowledgeRequirements(),
  collaborationNeeds: assessTeamCollaboration(),
  complianceRequirements: checkRegulatoryNeeds(),
  performanceConstraints: evaluatePerformanceLimits()
};

// Layer selection based on requirements
function selectMemoryLayers(assessment) {
  const layers = {
    A: true, // Routing - always required
    B: assessment.sessionFrequency > 5, // Session recovery
    C: assessment.knowledgeVolume > 100, // Durable knowledge
    D: assessment.projectScale === 'large', // Operational residue
    E: assessment.collaborationNeeds > 3, // Automatic recall
    F: assessment.complianceRequirements === 'high' // Cross-session graph
  };
  
  return layers;
}

// Memory system configuration
const memoryConfig = {
  selectedLayers: selectMemoryLayers(memoryAssessment),
  storageStrategy: determineStorageStrategy(assessment),
  backupFrequency: calculateBackupFrequency(assessment),
  accessPatterns: defineAccessPatterns(assessment),
  integrationPoints: identifyIntegrationPoints(assessment)
};
```

**Requirements Analysis:**
- Project complexity and knowledge volume
- Session patterns and collaboration needs
- Performance constraints and compliance requirements
- Storage strategy and backup frequency determination

### Step 2: Install Memory Stack Foundation
**Set up the core memory infrastructure:**

```javascript
// Memory stack installation
async function installMemoryStack(config) {
  // Step 1: Create directory structure
  await createMemoryDirectories(config);
  
  // Step 2: Initialize core files
  await initializeCoreFiles(config);
  
  // Step 3: Configure routing layer (Layer A)
  await setupRoutingLayer(config);
  
  // Step 4: Apply managed patches
  await applyManagedPatches(config);
  
  // Step 5: Validate installation
  const validation = await validateInstallation(config);
  
  return validation;
}

// Create memory directory structure
async function createMemoryDirectories(config) {
  const directories = [
    'memory/',
    '~/life/',
    'docs/memory-stack-local-notes.md'
  ];
  
  for (const dir of directories) {
    await ensureDirectoryExists(dir);
  }
}

// Initialize core memory files
async function initializeCoreFiles(config) {
  const coreFiles = {
    'MEMORY.md': generateMemoryIndex(config),
    'AGENTS.md': generateAgentRules(config),
    'PARA.md': generateParaConventions(config),
    'WORKSPACE_MEMORY_SYSTEM.md': generateWorkspaceGuide(config)
  };
  
  for (const [filename, content] of Object.entries(coreFiles)) {
    await createFileWithBackup(filename, content);
  }
}

// Setup routing layer (Layer A)
async function setupRoutingLayer(config) {
  const routingConfig = {
    memoryIndex: 'MEMORY.md',
    agentRules: 'AGENTS.md',
    durableFacts: '~/life/',
    dailyLogs: 'memory/YYYY-MM-DD.md',
    compactionRules: defineCompactionRules(config)
  };
  
  await writeRoutingConfiguration(routingConfig);
}
```

**Foundation Setup:**
- Directory structure creation
- Core file initialization
- Routing layer configuration
- Managed patch application
- Installation validation

### Step 3: Configure Session Recovery Layer
**Implement Layer B for session continuity:**

```javascript
// Session recovery configuration
async function configureSessionRecovery(config) {
  if (!config.selectedLayers.B) return;
  
  // Step 1: Setup lossless-claw integration
  await setupLosslessClaw(config);
  
  // Step 2: Configure session boundaries
  await configureSessionBoundaries(config);
  
  // Step 3: Setup context preservation
  await setupContextPreservation(config);
  
  // Step 4: Initialize recovery mechanisms
  await initializeRecoveryMechanisms(config);
}

// Setup lossless-claw integration
async function setupLosslessClaw(config) {
  const clawConfig = {
    sessionTimeout: config.sessionTimeout || 3600, // 1 hour
    contextWindowSize: config.contextWindow || 128000,
    compressionEnabled: config.enableCompression || true,
    recoveryTriggers: defineRecoveryTriggers(config)
  };
  
  await configureClawIntegration(clawConfig);
}

// Configure session boundaries
async function configureSessionBoundaries(config) {
  const boundaries = {
    sessionStartTriggers: [
      'new_file_opened',
      'major_context_shift',
      'explicit_session_start'
    ],
    sessionEndTriggers: [
      'workspace_close',
      'inactivity_timeout',
      'explicit_session_end'
    ],
    boundaryMarkers: defineBoundaryMarkers(config)
  };
  
  await writeSessionBoundaries(boundaries);
}

// Setup context preservation
async function setupContextPreservation(config) {
  const preservationRules = {
    preserveItems: [
      'open_files',
      'cursor_positions',
      'recent_commands',
      'conversation_context',
      'unsaved_changes'
    ],
    compressionStrategy: config.compressionStrategy || 'adaptive',
    retentionPolicy: defineRetentionPolicy(config)
  };
  
  await configurePreservationRules(preservationRules);
}
```

**Session Recovery:**
- Lossless-claw integration setup
- Session boundary configuration
- Context preservation rules
- Recovery mechanism initialization

### Step 4: Establish Durable Knowledge Layer
**Implement Layer C for long-term knowledge storage:**

```javascript
// Durable knowledge configuration
async function establishDurableKnowledge(config) {
  if (!config.selectedLayers.C) return;
  
  // Step 1: Setup PARA method structure
  await setupParaStructure(config);
  
  // Step 2: Configure knowledge indexing
  await configureKnowledgeIndexing(config);
  
  // Step 3: Initialize fact validation
  await initializeFactValidation(config);
  
  // Step 4: Setup knowledge lifecycle
  await setupKnowledgeLifecycle(config);
}

// Setup PARA method structure
async function setupParaStructure(config) {
  const paraStructure = {
    projects: 'Active project knowledge and current work',
    areas: 'Ongoing responsibility areas and domains',
    resources: 'Reference materials and archived knowledge',
    archive: 'Completed projects and historical knowledge'
  };
  
  // Create PARA directories
  for (const [category, description] of Object.entries(paraStructure)) {
    await createParaCategory(category, description, config);
  }
}

// Configure knowledge indexing
async function configureKnowledgeIndexing(config) {
  const indexingConfig = {
    indexFiles: ['summary.md', 'items.json'],
    indexingStrategy: config.indexingStrategy || 'hybrid',
    searchCapabilities: defineSearchCapabilities(config),
    deduplicationRules: defineDeduplicationRules(config),
    updateTriggers: defineUpdateTriggers(config)
  };
  
  await setupIndexingSystem(indexingConfig);
}

// Initialize fact validation
async function initializeFactValidation(config) {
  const validationRules = {
    factVerification: config.factVerification || 'manual',
    sourceTracking: true,
    updateNotifications: config.updateNotifications || true,
    conflictResolution: defineConflictResolution(config)
  };
  
  await configureFactValidation(validationRules);
}

// Setup knowledge lifecycle
async function setupKnowledgeLifecycle(config) {
  const lifecycleConfig = {
    creationWorkflow: defineCreationWorkflow(config),
    updateProcess: defineUpdateProcess(config),
    archivalRules: defineArchivalRules(config),
    deletionPolicy: defineDeletionPolicy(config)
  };
  
  await configureKnowledgeLifecycle(lifecycleConfig);
}
```

**Durable Knowledge:**
- PARA method structure setup
- Knowledge indexing configuration
- Fact validation initialization
- Knowledge lifecycle management

### Step 5: Implement Operational Residue Layer
**Set up Layer D for daily operational tracking:**

```javascript
// Operational residue configuration
async function implementOperationalResidue(config) {
  if (!config.selectedLayers.D) return;
  
  // Step 1: Setup daily log structure
  await setupDailyLogStructure(config);
  
  // Step 2: Configure timeline tracking
  await configureTimelineTracking(config);
  
  // Step 3: Initialize residue collection
  await initializeResidueCollection(config);
  
  // Step 4: Setup short-horizon continuity
  await setupShortHorizonContinuity(config);
}

// Setup daily log structure
async function setupDailyLogStructure(config) {
  const logStructure = {
    filenamePattern: 'memory/YYYY-MM-DD.md',
    sections: [
      'session_summary',
      'decisions_made',
      'issues_encountered',
      'solutions_applied',
      'follow_up_items'
    ],
    metadata: {
      session_count: 0,
      total_duration: 0,
      key_decisions: [],
      unresolved_items: []
    }
  };
  
  await createLogStructure(logStructure);
}

// Configure timeline tracking
async function configureTimelineTracking(config) {
  const timelineConfig = {
    eventTypes: defineEventTypes(config),
    timestampFormat: 'ISO8601',
    timezone: config.timezone || 'UTC',
    retentionPeriod: config.retentionPeriod || 365, // days
    archivalStrategy: config.archivalStrategy || 'compress'
  };
  
  await setupTimelineSystem(timelineConfig);
}

// Initialize residue collection
async function initializeResidueCollection(config) {
  const collectionRules = {
    collectEvents: [
      'file_operations',
      'command_execution',
      'decision_points',
      'error_conditions',
      'user_interactions'
    ],
    filteringRules: defineFilteringRules(config),
    aggregationStrategy: config.aggregationStrategy || 'chronological',
    exportCapabilities: defineExportCapabilities(config)
  };
  
  await configureResidueCollection(collectionRules);
}

// Setup short-horizon continuity
async function setupShortHorizonContinuity(config) {
  const continuityConfig = {
    continuityWindow: config.continuityWindow || 7, // days
    contextBridging: defineContextBridging(config),
    sessionLinking: defineSessionLinking(config),
    knowledgeTransfer: defineKnowledgeTransfer(config)
  };
  
  await configureContinuitySystem(continuityConfig);
}
```

**Operational Residue:**
- Daily log structure setup
- Timeline tracking configuration
- Residue collection initialization
- Short-horizon continuity setup

### Step 6: Enable Automatic Recall Layer
**Configure Layer E for intelligent memory retrieval:**

```javascript
// Automatic recall configuration
async function enableAutomaticRecall(config) {
  if (!config.selectedLayers.E) return;
  
  // Step 1: Setup Gigabrain integration
  await setupGigabrainIntegration(config);
  
  // Step 2: Configure memory slots
  await configureMemorySlots(config);
  
  // Step 3: Initialize recall triggers
  await initializeRecallTriggers(config);
  
  // Step 4: Setup deduplication system
  await setupDeduplicationSystem(config);
}

// Setup Gigabrain integration
async function setupGigabrainIntegration(config) {
  const gigabrainConfig = {
    pluginEnabled: true,
    memorySlots: config.memorySlots || 10,
    recallThreshold: config.recallThreshold || 0.7,
    contextWindow: config.contextWindow || 8000,
    updateFrequency: config.updateFrequency || 'realtime'
  };
  
  await configureGigabrainPlugin(gigabrainConfig);
}

// Configure memory slots
async function configureMemorySlots(config) {
  const slotConfig = {
    slotTypes: {
      project_context: { priority: 'high', retention: 'session' },
      user_preferences: { priority: 'medium', retention: 'permanent' },
      recent_decisions: { priority: 'high', retention: 'week' },
      error_patterns: { priority: 'medium', retention: 'month' },
      code_patterns: { priority: 'low', retention: 'permanent' }
    },
    slotLimits: defineSlotLimits(config),
    evictionPolicy: config.evictionPolicy || 'lru'
  };
  
  await setupMemorySlots(slotConfig);
}

// Initialize recall triggers
async function initializeRecallTriggers(config) {
  const triggerConfig = {
    prePromptTriggers: [
      'new_file_opened',
      'function_called',
      'error_encountered',
      'decision_point'
    ],
    contextTriggers: [
      'topic_shift',
      'complexity_increase',
      'user_question'
    ],
    manualTriggers: [
      'explicit_recall_request',
      'context_search'
    ]
  };
  
  await configureRecallTriggers(triggerConfig);
}

// Setup deduplication system
async function setupDeduplicationSystem(config) {
  const dedupeConfig = {
    similarityThreshold: config.similarityThreshold || 0.85,
    deduplicationStrategy: config.deduplicationStrategy || 'content_hash',
    conflictResolution: defineConflictResolution(config),
    mergeRules: defineMergeRules(config)
  };
  
  await configureDeduplicationSystem(dedupeConfig);
}
```

**Automatic Recall:**
- Gigabrain integration setup
- Memory slot configuration
- Recall trigger initialization
- Deduplication system setup

### Step 7: Integrate Cross-Session Graph Recall
**Set up Layer F for advanced memory relationships:**

```javascript
// Cross-session graph recall configuration
async function integrateCrossSessionGraph(config) {
  if (!config.selectedLayers.F) return;
  
  // Step 1: Setup OpenStinger integration
  await setupOpenStingerIntegration(config);
  
  // Step 2: Configure graph structure
  await configureGraphStructure(config);
  
  // Step 3: Initialize semantic indexing
  await initializeSemanticIndexing(config);
  
  // Step 4: Setup temporal relationships
  await setupTemporalRelationships(config);
}

// Setup OpenStinger integration
async function setupOpenStingerIntegration(config) {
  const stingerConfig = {
    dockerEnabled: checkDockerAvailability(),
    graphDatabase: config.graphDatabase || 'neo4j',
    indexingStrategy: config.indexingStrategy || 'semantic',
    apiEndpoints: defineApiEndpoints(config),
    authentication: configureAuthentication(config)
  };
  
  await initializeOpenStinger(stingerConfig);
}

// Configure graph structure
async function configureGraphStructure(config) {
  const graphConfig = {
    nodeTypes: {
      session: { properties: ['start_time', 'end_time', 'duration'] },
      knowledge: { properties: ['content', 'type', 'confidence'] },
      decision: { properties: ['context', 'outcome', 'impact'] },
      relationship: { properties: ['strength', 'type', 'timestamp'] }
    },
    edgeTypes: {
      references: { direction: 'directed', properties: ['context'] },
      precedes: { direction: 'directed', properties: ['time_gap'] },
      relates_to: { direction: 'undirected', properties: ['similarity'] },
      depends_on: { direction: 'directed', properties: ['dependency_type'] }
    },
    constraints: defineGraphConstraints(config)
  };
  
  await setupGraphSchema(graphConfig);
}

// Initialize semantic indexing
async function initializeSemanticIndexing(config) {
  const semanticConfig = {
    embeddingModel: config.embeddingModel || 'text-embedding-ada-002',
    indexingStrategy: 'hybrid', // semantic + keyword
    similarityThreshold: config.similarityThreshold || 0.8,
    updateFrequency: config.updateFrequency || 'batch',
    queryOptimization: defineQueryOptimization(config)
  };
  
  await configureSemanticIndexing(semanticConfig);
}

// Setup temporal relationships
async function setupTemporalRelationships(config) {
  const temporalConfig = {
    timeWindows: {
      immediate: '1_hour',
      short: '1_day',
      medium: '1_week',
      long: '1_month',
      permanent: 'indefinite'
    },
    relationshipTypes: {
      sequential: 'events in sequence',
      parallel: 'simultaneous events',
      causal: 'cause-effect relationships',
      contextual: 'shared context events'
    },
    decayFunctions: defineDecayFunctions(config),
    importanceScoring: defineImportanceScoring(config)
  };
  
  await configureTemporalRelationships(temporalConfig);
}
```

**Cross-Session Graph:**
- OpenStinger integration setup
- Graph structure configuration
- Semantic indexing initialization
- Temporal relationship setup

### Step 8: Validate Memory System Operation
**Test and verify the complete memory system:**

```javascript
// Memory system validation
async function validateMemorySystem(config) {
  const validationResults = {
    layerA: await validateRoutingLayer(config),
    layerB: config.selectedLayers.B ? await validateSessionRecovery(config) : 'skipped',
    layerC: config.selectedLayers.C ? await validateDurableKnowledge(config) : 'skipped',
    layerD: config.selectedLayers.D ? await validateOperationalResidue(config) : 'skipped',
    layerE: config.selectedLayers.E ? await validateAutomaticRecall(config) : 'skipped',
    layerF: config.selectedLayers.F ? await validateCrossSessionGraph(config) : 'skipped'
  };
  
  // Overall system validation
  const systemValidation = {
    allLayersFunctional: Object.values(validationResults).every(r => r === 'passed'),
    integrationWorking: await testLayerIntegration(config),
    performanceAcceptable: await validatePerformance(config),
    backupRecovery: await testBackupRecovery(config)
  };
  
  return {
    layerResults: validationResults,
    systemValidation: systemValidation,
    recommendations: generateRecommendations(validationResults, systemValidation)
  };
}

// Validate routing layer (Layer A)
async function validateRoutingLayer(config) {
  try {
    // Test MEMORY.md routing
    const memoryIndex = await readFile('MEMORY.md');
    const routingValid = validateRoutingStructure(memoryIndex);
    
    // Test AGENTS.md rules
    const agentRules = await readFile('AGENTS.md');
    const rulesValid = validateAgentRules(agentRules);
    
    return routingValid && rulesValid ? 'passed' : 'failed';
  } catch (error) {
    return 'error';
  }
}

// Test layer integration
async function testLayerIntegration(config) {
  // Test data flow between layers
  const testData = {
    sessionId: 'test-session-001',
    knowledge: 'test knowledge item',
    timestamp: new Date().toISOString()
  };
  
  // Test Layer A → B → C flow
  const layerA_Result = await testRouting(testData);
  const layerB_Result = config.selectedLayers.B ? await testSessionRecovery(testData) : true;
  const layerC_Result = config.selectedLayers.C ? await testDurableKnowledge(testData) : true;
  
  return layerA_Result && layerB_Result && layerC_Result;
}

// Validate performance
async function validatePerformance(config) {
  const performanceMetrics = {
    memoryLatency: await measureMemoryLatency(config),
    recallAccuracy: await measureRecallAccuracy(config),
    storageEfficiency: await measureStorageEfficiency(config),
    queryPerformance: await measureQueryPerformance(config)
  };
  
  const thresholds = {
    memoryLatency: '< 100ms',
    recallAccuracy: '> 90%',
    storageEfficiency: '> 80%',
    queryPerformance: '< 500ms'
  };
  
  return checkPerformanceAgainstThresholds(performanceMetrics, thresholds);
}
```

**System Validation:**
- Individual layer validation
- Integration testing between layers
- Performance validation
- Backup and recovery testing

## Success Criteria

- [ ] Memory system layers properly selected and configured
- [ ] Core infrastructure (directories, files) created successfully
- [ ] Routing layer (Layer A) operational and validated
- [ ] Session recovery (Layer B) functional if enabled
- [ ] Durable knowledge (Layer C) established if enabled
- [ ] Operational residue (Layer D) tracking if enabled
- [ ] Automatic recall (Layer E) working if enabled
- [ ] Cross-session graph (Layer F) integrated if enabled
- [ ] System validation passed with acceptable performance
- [ ] Backup and recovery mechanisms tested and functional

## Common Pitfalls

1. **Layer Overload** - Don't enable all layers for simple projects
2. **Configuration Conflicts** - Ensure layer configurations don't conflict
3. **Performance Issues** - Monitor memory system impact on AI performance
4. **Integration Problems** - Test data flow between enabled layers
5. **Backup Failures** - Regularly test backup and recovery procedures
6. **Knowledge Staleness** - Implement update mechanisms for durable knowledge
7. **Session Loss** - Configure session boundaries appropriately

## Memory Layer Selection Guide

### Simple Projects (1-2 developers)
- **Enable**: Layers A, B, C
- **Use Case**: Basic knowledge preservation and session recovery
- **Maintenance**: Low - focus on PARA method adherence

### Medium Projects (3-10 developers)
- **Enable**: Layers A, B, C, D, E
- **Use Case**: Team collaboration with automatic recall
- **Maintenance**: Medium - monitor recall accuracy and timeline tracking

### Large/Enterprise Projects (10+ developers)
- **Enable**: All layers A-F
- **Use Case**: Complex knowledge management with compliance requirements
- **Maintenance**: High - dedicated memory system administration

## Cross-References

### Related Procedures
- [Writing Plans](skills/writing-plans/SKILL.md) - Planning memory system implementation
- [Systematic Debugging](skills/systematic-debugging/SKILL.md) - Troubleshooting memory issues
- [Verification Before Completion](skills/verification-before-completion/SKILL.md) - Validating memory system setup

### Related Skills
- `writing-plans` - Planning memory system architecture
- `systematic-debugging` - Memory system troubleshooting
- `verification-before-completion` - Memory system validation

### Related Agents
- `DevForge_AI_Team` - Memory system development assistance
- `QualityForge_AI_Team` - Memory system validation and testing