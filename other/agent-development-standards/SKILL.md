---
memory_layer: durable_knowledge
para_section: pages/skills/agent-development-standards
gigabrain_tags: agent-development, standards, coding-practices, cross-language, framework
openstinger_context: agent-standards-practices, development-framework
last_updated: 2026-03-30
related_docs:
  - docs_construct_ai/codebase/coding-standards/
  - docs_construct_ai/codebase/architecture/
related_skills:
  - agent-coding-standards
  - writing-plans
  - test-driven-development
frequency_percent: 100.0
success_rate_percent: 95.0
---

# Agent Development Standards

## Overview

**Core principle:** Follow ConstructAI unified agent framework standards for consistent, maintainable, and scalable agent development across Python and JavaScript.

**Framework:** Unified agent base classes, standardized configuration, cross-language testing, and deployment patterns.

## When to Use This Skill

**Trigger Conditions:**
- When developing new agents for ConstructAI platform
- Before implementing agent functionality in Python or JavaScript
- When setting up agent development environments
- When reviewing agent code for framework compliance
- When integrating agents with existing ConstructAI systems
- When deploying agents to production environments
- When establishing agent development workflows

**Mandatory Application:**
- Required for all agent development work
- Must be applied before any agent implementation
- Required for both Python and JavaScript agents
- Must be verified before agent deployment
- Required for maintaining framework consistency

## Step-by-Step Procedure

### Step 1: Framework Architecture Assessment
**Evaluate agent requirements against framework capabilities:**

```javascript
// Assess agent requirements
const agentRequirements = {
  agentType: 'specialist', // supervisor, specialist, service, coordinator, utility
  language: 'python', // python or javascript
  capabilities: ['document_processing', 'data_analysis'],
  communication: 'http', // http, websocket, message-queue
  persistence: true,
  monitoring: true,
  scaling: 'horizontal'
};

// Validate against framework capabilities
const frameworkCapabilities = {
  supportedLanguages: ['python', 'javascript'],
  agentTypes: ['supervisor', 'specialist', 'service', 'coordinator', 'utility'],
  communicationProtocols: ['http', 'websocket', 'message-queue'],
  persistence: true,
  monitoring: true,
  scaling: ['horizontal', 'vertical']
};

function validateAgentRequirements(requirements, capabilities) {
  const issues = [];
  
  if (!capabilities.supportedLanguages.includes(requirements.language)) {
    issues.push(`Unsupported language: ${requirements.language}`);
  }
  
  if (!capabilities.agentTypes.includes(requirements.agentType)) {
    issues.push(`Unsupported agent type: ${requirements.agentType}`);
  }
  
  if (!capabilities.communicationProtocols.includes(requirements.communication)) {
    issues.push(`Unsupported communication protocol: ${requirements.communication}`);
  }
  
  return {
    valid: issues.length === 0,
    issues: issues
  };
}
```

**Framework Assessment:**
- Validate agent type and language compatibility
- Ensure required capabilities are supported
- Verify communication protocols are available
- Confirm scaling and persistence requirements

### Step 2: Base Class Implementation
**Implement agent using unified base classes:**

```python
# Python agent implementation
from agents.core.python.unified_agent_framework import UnifiedAgent, AgentConfig
from typing import Dict, List, Any, Optional
import asyncio

class MyConstructAIAgent(UnifiedAgent):
    """
    My ConstructAI Agent - implements specific business logic.
    
    DESCRIPTION = "Handles specialized processing for ConstructAI workflows"
    """
    
    def __init__(self, config: AgentConfig):
        # Validate framework requirements
        self._validate_framework_config(config)
        
        super().__init__(config)
        
        # Agent-specific initialization
        self.business_logic = config.custom_config.get("business_logic")
        self.workflow_integration = config.custom_config.get("workflow_integration", True)
        
    def _validate_framework_config(self, config: AgentConfig) -> None:
        """Validate configuration against framework standards."""
        required_caps = ["base_agent", "framework_compliant"]
        missing_caps = [cap for cap in required_caps if cap not in config.capabilities]
        if missing_caps:
            raise ValueError(f"Missing required framework capabilities: {missing_caps}")
            
        if config.language not in ["python", "javascript"]:
            raise ValueError(f"Unsupported language: {config.language}")
            
        if config.agent_type not in ["supervisor", "specialist", "service", "coordinator", "utility"]:
            raise ValueError(f"Unsupported agent type: {config.agent_type}")
    
    async def _executeImpl(self, workflow_state: Dict[str, Any], options: Dict[str, Any]) -> Dict[str, Any]:
        """
        Core agent logic following framework patterns.
        
        Args:
            workflow_state: Current ConstructAI workflow state
            options: Execution options
            
        Returns:
            Dict containing processing results
        """
        try:
            # Framework-compliant input validation
            self._validate_workflow_state(workflow_state)
            
            # Core business logic
            result = await self._execute_business_logic(workflow_state)
            
            # Framework-required metadata
            result.update({
                "agent_id": self.agent_id,
                "framework_version": self.version,
                "execution_timestamp": asyncio.get_event_loop().time(),
                "compliance_status": "framework_compliant"
            })
            
            return result
            
        except Exception as error:
            # Framework-compliant error handling
            await self._handle_framework_error(error, workflow_state)
            raise
    
    def _validate_workflow_state(self, workflow_state: Dict[str, Any]) -> None:
        """Validate workflow state against framework schema."""
        required_fields = ["input_data", "context", "metadata"]
        missing_fields = [field for field in required_fields if field not in workflow_state]
        if missing_fields:
            raise ValueError(f"Missing required workflow fields: {missing_fields}")
            
        # Validate metadata structure
        if "metadata" in workflow_state:
            metadata = workflow_state["metadata"]
            if not isinstance(metadata, dict):
                raise ValueError("Workflow metadata must be a dictionary")
                
            required_metadata = ["request_id", "organization_id"]
            missing_metadata = [field for field in required_metadata if field not in metadata]
            if missing_metadata:
                raise ValueError(f"Missing required metadata fields: {missing_metadata}")
    
    async def _execute_business_logic(self, workflow_state: Dict[str, Any]) -> Dict[str, Any]:
        """Implement agent-specific business logic."""
        # Agent-specific implementation
        return {
            "status": "processed",
            "data": workflow_state.get("input_data"),
            "processed_at": asyncio.get_event_loop().time()
        }
    
    async def _handle_framework_error(self, error: Exception, workflow_state: Dict[str, Any]) -> None:
        """Handle errors following framework patterns."""
        self.logger.error(f"Framework-compliant error handling: {error}")
        
        # Framework-required error reporting
        error_report = {
            "error_type": type(error).__name__,
            "error_message": str(error),
            "workflow_state": workflow_state.get("metadata", {}).get("request_id"),
            "agent_id": self.agent_id,
            "timestamp": asyncio.get_event_loop().time()
        }
        
        # Report to framework monitoring
        await self._report_to_framework_monitoring(error_report)
```

```javascript
// JavaScript agent implementation
const { UnifiedAgent, AgentConfig } = require('../javascript/unified-agent-framework');

/**
 * My ConstructAI Agent - implements specific business logic
 */
class MyConstructAIAgent extends UnifiedAgent {
  static DESCRIPTION = "Handles specialized processing for ConstructAI workflows";

  constructor(config) {
    // Validate framework requirements
    this._validateFrameworkConfig(config);
    
    super(config);
    
    // Agent-specific initialization
    this.businessLogic = config.customConfig?.businessLogic;
    this.workflowIntegration = config.customConfig?.workflowIntegration ?? true;
  }

  _validateFrameworkConfig(config) {
    /** Validate configuration against framework standards. */
    const requiredCaps = ["base_agent", "framework_compliant"];
    const missingCaps = requiredCaps.filter(cap => !config.capabilities.includes(cap));
    if (missingCaps.length > 0) {
      throw new Error(`Missing required framework capabilities: ${missingCaps.join(', ')}`);
    }
    
    if (!["python", "javascript"].includes(config.language)) {
      throw new Error(`Unsupported language: ${config.language}`);
    }
    
    if (!["supervisor", "specialist", "service", "coordinator", "utility"].includes(config.agentType)) {
      throw new Error(`Unsupported agent type: ${config.agentType}`);
    }
  }

  async _executeImpl(workflowState, options = {}) {
    /**
     * Core agent logic following framework patterns.
     *
     * @param {Object} workflowState - Current ConstructAI workflow state
     * @param {Object} options - Execution options
     * @returns {Object} Processing results
     */
    try {
      // Framework-compliant input validation
      this._validateWorkflowState(workflowState);
      
      // Core business logic
      const result = await this._executeBusinessLogic(workflowState);
      
      // Framework-required metadata
      Object.assign(result, {
        agentId: this.agentId,
        frameworkVersion: this.version,
        executionTimestamp: Date.now(),
        complianceStatus: "framework_compliant"
      });
      
      return result;
      
    } catch (error) {
      // Framework-compliant error handling
      await this._handleFrameworkError(error, workflowState);
      throw error;
    }
  }

  _validateWorkflowState(workflowState) {
    /** Validate workflow state against framework schema. */
    const requiredFields = ["inputData", "context", "metadata"];
    const missingFields = requiredFields.filter(field => !(field in workflowState));
    if (missingFields.length > 0) {
      throw new Error(`Missing required workflow fields: ${missingFields.join(', ')}`);
    }
    
    // Validate metadata structure
    if ("metadata" in workflowState) {
      const metadata = workflowState.metadata;
      if (typeof metadata !== "object" || metadata === null) {
        throw new Error("Workflow metadata must be an object");
      }
      
      const requiredMetadata = ["requestId", "organizationId"];
      const missingMetadata = requiredMetadata.filter(field => !(field in metadata));
      if (missingMetadata.length > 0) {
        throw new Error(`Missing required metadata fields: ${missingMetadata.join(', ')}`);
      }
    }
  }

  async _executeBusinessLogic(workflowState) {
    /** Implement agent-specific business logic. */
    // Agent-specific implementation
    return {
      status: "processed",
      data: workflowState.inputData,
      processedAt: Date.now()
    };
  }

  async _handleFrameworkError(error, workflowState) {
    /** Handle errors following framework patterns. */
    this.logger.error(`Framework-compliant error handling: ${error.message}`);
    
    // Framework-required error reporting
    const errorReport = {
      errorType: error.constructor.name,
      errorMessage: error.message,
      workflowState: workflowState.metadata?.requestId,
      agentId: this.agentId,
      timestamp: Date.now()
    };
    
    // Report to framework monitoring
    await this._reportToFrameworkMonitoring(errorReport);
  }
}

module.exports = { MyConstructAIAgent };
```

**Base Class Implementation:**
- Use UnifiedAgent base class for both languages
- Implement framework-required validation
- Follow standardized method signatures
- Include framework-compliant error handling
- Add required metadata to results

### Step 3: Configuration Standardization
**Implement standardized AgentConfig schema:**

```javascript
// Unified configuration schema
const agentConfigSchema = {
  // Core identification
  agentId: "unique-agent-identifier",
  agentType: "specialist", // supervisor, specialist, service, coordinator, utility
  language: "javascript", // python, javascript
  
  // Capabilities and features
  capabilities: [
    "base_agent",
    "framework_compliant",
    "document_processing",
    "data_analysis"
  ],
  
  // Core settings
  logLevel: "INFO", // DEBUG, INFO, WARN, ERROR
  maxConcurrentRequests: 10,
  timeoutSeconds: 300,
  retryAttempts: 3,
  
  // Plugin configuration
  plugins: [
    {
      name: "monitoring-plugin",
      version: "1.0.0",
      enabled: true,
      priority: 100,
      config: { endpoint: "http://monitoring:8080" },
      dependencies: ["base-plugin"]
    }
  ],
  
  // Monitoring settings
  enableMonitoring: true,
  metricsInterval: 60, // seconds
  healthCheckInterval: 30, // seconds
  
  // Communication settings
  communicationProtocol: "http", // http, websocket, message-queue
  registryUrl: "http://agent-registry:3000",
  autoRegister: true,
  
  // Feature flags
  featureFlags: {
    experimentalFeatures: false,
    debugMode: false,
    performanceMonitoring: true
  },
  
  // Custom configuration
  customConfig: {
    businessLogic: "document-analysis",
    workflowIntegration: true,
    confidenceThreshold: 0.8
  }
};

// Configuration validation
function validateAgentConfig(config) {
  const errors = [];
  
  // Required fields validation
  const requiredFields = ["agentId", "agentType", "language", "capabilities"];
  for (const field of requiredFields) {
    if (!config[field]) {
      errors.push(`Missing required field: ${field}`);
    }
  }
  
  // Agent type validation
  const validTypes = ["supervisor", "specialist", "service", "coordinator", "utility"];
  if (config.agentType && !validTypes.includes(config.agentType)) {
    errors.push(`Invalid agent type: ${config.agentType}`);
  }
  
  // Language validation
  const validLanguages = ["python", "javascript"];
  if (config.language && !validLanguages.includes(config.language)) {
    errors.push(`Invalid language: ${config.language}`);
  }
  
  // Capabilities validation
  if (config.capabilities && !Array.isArray(config.capabilities)) {
    errors.push("Capabilities must be an array");
  }
  if (config.capabilities && !config.capabilities.includes("base_agent")) {
    errors.push("Capabilities must include 'base_agent'");
  }
  
  return {
    valid: errors.length === 0,
    errors: errors
  };
}
```

**Configuration Standards:**
- Use standardized AgentConfig schema
- Validate against framework requirements
- Include all required fields and settings
- Support plugin configuration
- Enable monitoring and communication settings

### Step 4: Testing Standards Implementation
**Implement cross-language testing patterns:**

```python
# Python unit tests
import pytest
import asyncio
from unittest.mock import Mock, patch
from agents.core.python.unified_agent_framework import UnifiedAgent, AgentConfig

class TestConstructAIAgent:
    """Unit tests for ConstructAI agent following framework standards."""

    @pytest.fixture
    def agent_config(self):
        """Create standardized test configuration."""
        return AgentConfig(
            agent_id="test-agent-001",
            agent_type="specialist",
            language="python",
            capabilities=["base_agent", "framework_compliant", "document_processing"],
            version="1.0.0",
            log_level="DEBUG",
            custom_config={
                "business_logic": "test-processing",
                "workflow_integration": True
            }
        )

    @pytest.fixture
    async def agent(self, agent_config):
        """Create test agent instance."""
        agent = MyConstructAIAgent(agent_config)
        await agent.initialize()
        yield agent
        await agent.cleanup()

    @pytest.mark.asyncio
    async def test_framework_compliance(self, agent_config):
        """Test agent meets framework compliance requirements."""
        agent = MyConstructAIAgent(agent_config)
        
        # Test framework capability validation
        assert "framework_compliant" in agent_config.capabilities
        assert agent_config.language in ["python", "javascript"]
        assert agent_config.agent_type in ["supervisor", "specialist", "service", "coordinator", "utility"]

    @pytest.mark.asyncio
    async def test_workflow_state_validation(self, agent):
        """Test framework-compliant workflow state validation."""
        # Valid workflow state
        valid_state = {
            "input_data": {"test": "data"},
            "context": {"domain": "test"},
            "metadata": {
                "request_id": "req-123",
                "organization_id": "org-456"
            }
        }
        
        # Should not raise exception
        agent._validate_workflow_state(valid_state)
        
        # Invalid workflow state - missing metadata
        invalid_state = {
            "input_data": {"test": "data"},
            "context": {"domain": "test"}
        }
        
        with pytest.raises(ValueError, match="Missing required workflow fields"):
            agent._validate_workflow_state(invalid_state)

    @pytest.mark.asyncio
    async def test_framework_metadata_injection(self, agent):
        """Test framework-required metadata is injected into results."""
        workflow_state = {
            "input_data": {"test": "data"},
            "context": {"domain": "test"},
            "metadata": {
                "request_id": "req-123",
                "organization_id": "org-456"
            }
        }

        with patch.object(agent, '_execute_business_logic', return_value={"status": "processed"}):
            result = await agent.execute(workflow_state)

        # Verify framework metadata
        assert result["agent_id"] == agent.agent_id
        assert "framework_version" in result
        assert "execution_timestamp" in result
        assert result["compliance_status"] == "framework_compliant"

    @pytest.mark.asyncio
    async def test_error_handling_compliance(self, agent):
        """Test error handling follows framework patterns."""
        workflow_state = {
            "input_data": {"test": "data"},
            "context": {"domain": "test"},
            "metadata": {
                "request_id": "req-123",
                "organization_id": "org-456"
            }
        }

        with patch.object(agent, '_execute_business_logic', side_effect=Exception("Test error")):
            with patch.object(agent, '_report_to_framework_monitoring') as mock_report:
                with pytest.raises(Exception, match="Test error"):
                    await agent.execute(workflow_state)

                # Verify framework error reporting
                mock_report.assert_called_once()
                error_report = mock_report.call_args[0][0]
                assert error_report["error_type"] == "Exception"
                assert error_report["error_message"] == "Test error"
                assert error_report["workflow_state"] == "req-123"
                assert error_report["agent_id"] == agent.agent_id
```

```javascript
// JavaScript unit tests
const { expect } = require('chai');
const sinon = require('sinon');
const { MyConstructAIAgent } = require('../my-constructai-agent');

describe('MyConstructAIAgent', () => {
  let agent;
  let agentConfig;

  beforeEach(() => {
    agentConfig = {
      agentId: 'test-agent-001',
      agentType: 'specialist',
      language: 'javascript',
      capabilities: ['base_agent', 'framework_compliant', 'document_processing'],
      version: '1.0.0',
      logLevel: 'DEBUG',
      customConfig: {
        businessLogic: 'test-processing',
        workflowIntegration: true
      }
    };
  });

  afterEach(async () => {
    if (agent) {
      await agent.cleanup();
    }
  });

  describe('Framework Compliance', () => {
    it('should validate framework configuration', () => {
      agent = new MyConstructAIAgent(agentConfig);
      
      // Test framework capability validation
      expect(agentConfig.capabilities).to.include('framework_compliant');
      expect(agentConfig.language).to.be.oneOf(['python', 'javascript']);
      expect(agentConfig.agentType).to.be.oneOf(['supervisor', 'specialist', 'service', 'coordinator', 'utility']);
    });

    it('should reject invalid framework configuration', () => {
      const invalidConfig = {
        ...agentConfig,
        capabilities: ['invalid_capability'],
        language: 'invalid_language'
      };
      
      expect(() => new MyConstructAIAgent(invalidConfig))
        .to.throw('Missing required framework capabilities');
    });
  });

  describe('Workflow State Validation', () => {
    beforeEach(async () => {
      agent = new MyConstructAIAgent(agentConfig);
      await agent.initialize();
    });

    it('should validate complete workflow state', () => {
      const validState = {
        inputData: { test: 'data' },
        context: { domain: 'test' },
        metadata: {
          requestId: 'req-123',
          organizationId: 'org-456'
        }
      };
      
      // Should not throw
      expect(() => agent._validateWorkflowState(validState)).to.not.throw();
    });

    it('should reject incomplete workflow state', () => {
      const invalidState = {
        inputData: { test: 'data' },
        context: { domain: 'test' }
        // Missing metadata
      };
      
      expect(() => agent._validateWorkflowState(invalidState))
        .to.throw('Missing required workflow fields: metadata');
    });
  });

  describe('Framework Metadata', () => {
    it('should inject framework-required metadata', async () => {
      agent = new MyConstructAIAgent(agentConfig);
      await agent.initialize();

      const workflowState = {
        inputData: { test: 'data' },
        context: { domain: 'test' },
        metadata: {
          requestId: 'req-123',
          organizationId: 'org-456'
        }
      };

      const businessLogicStub = sinon.stub(agent, '_executeBusinessLogic')
        .resolves({ status: 'processed' });

      const result = await agent.execute(workflowState);

      // Verify framework metadata
      expect(result.agentId).to.equal(agent.agentId);
      expect(result).to.have.property('frameworkVersion');
      expect(result).to.have.property('executionTimestamp');
      expect(result.complianceStatus).to.equal('framework_compliant');
    });
  });

  describe('Error Handling', () => {
    it('should handle errors following framework patterns', async () => {
      agent = new MyConstructAIAgent(agentConfig);
      await agent.initialize();

      const workflowState = {
        inputData: { test: 'data' },
        context: { domain: 'test' },
        metadata: {
          requestId: 'req-123',
          organizationId: 'org-456'
        }
      };

      const businessLogicStub = sinon.stub(agent, '_executeBusinessLogic')
        .rejects(new Error('Test error'));
      const errorReportStub = sinon.stub(agent, '_reportToFrameworkMonitoring')
        .resolves();

      try {
        await agent.execute(workflowState);
        expect.fail('Should have thrown error');
      } catch (error) {
        expect(error.message).to.equal('Test error');
      }

      // Verify framework error reporting
      expect(errorReportStub).to.have.been.calledOnce;
      const errorReport = errorReportStub.firstCall.args[0];
      expect(errorReport.errorType).to.equal('Error');
      expect(errorReport.errorMessage).to.equal('Test error');
      expect(errorReport.workflowState).to.equal('req-123');
      expect(errorReport.agentId).to.equal(agent.agentId);
    });
  });
});
```

**Testing Standards:**
- Implement unit tests for both Python and JavaScript
- Test framework compliance and validation
- Verify metadata injection and error handling
- Use similar testing patterns across languages

### Step 5: Documentation Standards Application
**Create standardized agent documentation:**

```markdown
# My ConstructAI Agent

**[Specialist]** - [Brief Description]

## Overview

[Agent Name] is a [specialist] agent that [primary function].

### Key Features
- [Feature 1]: [Description]
- [Feature 2]: [Description]
- [Feature 3]: [Description]

### Capabilities
- `base_agent`: Core agent functionality
- `framework_compliant`: ConstructAI framework compliance
- `document_processing`: Document analysis and processing
- `data_analysis`: Data analysis and insights

## Configuration

### Required Configuration
```json
{
  "agentId": "unique-agent-id",
  "agentType": "specialist",
  "capabilities": ["base_agent", "framework_compliant", "document_processing"],
  "customConfig": {
    "businessLogic": "document-analysis",
    "workflowIntegration": true
  }
}
```

### Optional Configuration
```json
{
  "logLevel": "INFO",
  "maxConcurrentRequests": 10,
  "timeoutSeconds": 300,
  "customConfig": {
    "confidenceThreshold": 0.8
  }
}
```

## Usage

### Basic Usage
```python
# Python
from agents.types.specialists.my_agent.python.my_agent_agent import MyConstructAIAgent
from agents.core.python.unified_agent_framework import AgentConfig

config = AgentConfig(
    agent_id="my-agent",
    agent_type="specialist",
    capabilities=["base_agent", "framework_compliant"],
    custom_config={"business_logic": "document-analysis"}
)

agent = MyConstructAIAgent(config)
await agent.initialize()

result = await agent.execute(workflow_state)
```

```javascript
// JavaScript
const { MyConstructAIAgent } = require('./agents/types/specialists/my-agent/javascript');

const config = {
  agentId: 'my-agent',
  agentType: 'specialist',
  capabilities: ['base_agent', 'framework_compliant'],
  customConfig: { businessLogic: 'document-analysis' }
};

const agent = new MyConstructAIAgent(config);
await agent.initialize();

const result = await agent.execute(workflowState);
```

### Workflow Integration
```javascript
// Example workflow state
const workflowState = {
  inputData: {
    documents: ["doc1.pdf", "doc2.pdf"],
    requirements: ["requirement1", "requirement2"]
  },
  context: {
    domain: "construction",
    priority: "high",
    deadline: "2026-02-01"
  },
  metadata: {
    requestId: "req-123",
    organizationId: "org-456",
    userId: "user-789"
  }
};

const result = await agent.execute(workflowState, {
  confidenceThreshold: 0.9,
  processingMode: "thorough"
});
```

## API Reference

### Methods

#### `initialize()`
Initializes the agent and registers with the agent registry.
```javascript
await agent.initialize()  // Returns: boolean
```

#### `execute(workflowState, options)`
Executes the agent's primary logic.
```javascript
const result = await agent.execute(workflowState, options)  // Returns: Object
```

#### `cleanup()`
Cleans up agent resources and unregisters from registry.
```javascript
await agent.cleanup()  // Returns: void
```

### Events

#### `progress`
Emitted during execution to report progress.
```javascript
agent.addProgressCallback((agent, progress, step) => {
  console.log(`Progress: ${progress}% - ${step}`);
});
```

#### `error`
Emitted when errors occur during execution.
```javascript
agent.addErrorCallback((agent, error) => {
  console.error('Agent error:', error);
});
```

#### `completion`
Emitted when execution completes successfully.
```javascript
agent.addCompletionCallback((agent, result) => {
  console.log('Execution completed:', result);
});
```

## Error Handling

### Common Errors
- **ValidationError**: Input validation failed
  - Check workflow state structure
  - Verify required fields are present
- **TimeoutError**: Processing exceeded timeout
  - Increase `timeoutSeconds` in configuration
  - Check for performance issues
- **CapabilityError**: Agent lacks required capabilities
  - Add missing capabilities to agent configuration
  - Verify agent type supports required operations

### Error Response Format
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Missing required workflow fields: metadata",
    "details": {
      "missing_fields": ["metadata"],
      "workflow_state": {...}
    }
  },
  "agent_id": "agent-123",
  "timestamp": "2026-01-16T10:30:00Z"
}
```

## Testing

### Running Tests
```bash
# Python
pytest tests/agents/types/specialists/my_agent/python/ -v

# JavaScript
npm test -- --grep "MyConstructAIAgent"
```

### Test Coverage Requirements
- **Unit Tests**: > 80% coverage
- **Integration Tests**: All communication paths tested
- **Framework Tests**: Framework compliance verified
- **Cross-Language Tests**: Consistent behavior across Python/JavaScript

## Monitoring

### Health Checks
- **Endpoint**: `GET /health/[agent_id]`
- **Response**: Agent health status and framework compliance

### Metrics
- **requests_total**: Total requests processed
- **execution_time**: Average execution time
- **error_rate**: Percentage of failed requests
- **compliance_score**: Framework compliance rating

## Deployment

### Environment Variables
```bash
AGENT_ID=my-agent-001
AGENT_TYPE=specialist
REGISTRY_URL=http://agent-registry:3000
LOG_LEVEL=INFO
```

### Docker Deployment
```dockerfile
FROM constructai/agent-base:latest
COPY . /app
RUN npm install
EXPOSE 3000
CMD ["npm", "start"]
```

## Troubleshooting

### Debug Mode
Enable debug logging for detailed execution traces:
```json
{
  "logLevel": "DEBUG",
  "customConfig": {
    "debug_mode": true
  }
}
```

### Common Issues
1. **Agent not registering**: Check registry URL and network connectivity
2. **Framework validation errors**: Verify agent configuration against schema
3. **Communication failures**: Check protocol compatibility
4. **Performance issues**: Monitor resource usage and scaling

## Contributing

### Code Style
- Follow language-specific linting rules
- Use descriptive commit messages
- Include tests for all new features
- Update documentation for API changes

### Review Process
1. Create feature branch
2. Implement with framework compliance
3. Update documentation
4. Submit pull request
5. Framework compliance review
6. Code review and approval
7. Merge to main branch

## License

Copyright 2026 ConstructAI. All rights reserved.
```

**Documentation Standards:**
- Follow standardized README template
- Include configuration examples for both languages
- Document API methods and events
- Provide usage examples and troubleshooting
- Include testing and deployment information

### Step 6: Deployment Standards Implementation
**Apply unified deployment patterns:**

```yaml
# GitHub Actions CI/CD pipeline
name: Agent CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        language: [python, javascript]
        node-version: [16.x, 18.x]
        python-version: [3.9, 3.11]

    steps:
    - uses: actions/checkout@v3

    - name: Setup Python ${{ matrix.python-version }}
      if: matrix.language == 'python'
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}

    - name: Setup Node.js ${{ matrix.node-version }}
      if: matrix.language == 'javascript'
      uses: actions/setup-node@v3
      with:
        node-version: ${{ matrix.node-version }}

    - name: Install dependencies
      run: |
        if [ "${{ matrix.language }}" == "python" ]; then
          pip install -r requirements.txt
          pip install -r requirements-dev.txt
        else
          npm ci
        fi

    - name: Run linting
      run: |
        if [ "${{ matrix.language }}" == "python" ]; then
          flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
          black --check .
        else
          npm run lint
        fi

    - name: Run tests
      run: |
        if [ "${{ matrix.language }}" == "python" ]; then
          pytest --cov=agents --cov-report=xml
        else
          npm run test:coverage
        fi

    - name: Upload coverage reports
      uses: codecov/codecov-action@v3

  security:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3

    - name: Run security scan
      uses: securecodewarrior/github-action-security-scan@v1
      with:
        language: 'mixed'

  deploy:
    needs: [test, security]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'

    steps:
    - uses: actions/checkout@v3

    - name: Build and push Docker image
      run: |
        docker build -t constructai/${{ github.event.repository.name }}:${{ github.sha }} .
        docker push constructai/${{ github.event.repository.name }}:${{ github.sha }}

    - name: Deploy to staging
      run: |
        kubectl set image deployment/agent-${{ github.event.repository.name }} \
          agent-${{ github.event.repository.name }}=constructai/${{ github.event.repository.name }}:${{ github.sha }}
```

**Deployment Standards:**
- Use standardized CI/CD pipelines
- Support cross-language testing
- Include security scanning
- Implement automated deployment
- Follow containerization best practices

### Step 7: Code Review Standards Application
**Apply framework-specific code review checklist:**

```markdown
# Code Review Checklist - ConstructAI Agent Framework

## General Requirements
- [ ] **Functionality**: Agent meets requirements and works as expected
- [ ] **Framework Compliance**: Agent uses unified base classes and patterns
- [ ] **Configuration**: Agent uses standardized AgentConfig schema
- [ ] **Documentation**: Agent documentation follows standardized template
- [ ] **Testing**: Unit and integration tests cover all functionality (>80% coverage)
- [ ] **Cross-Language Consistency**: Agent behavior consistent across Python/JavaScript

## Agent-Specific Requirements
- [ ] **Base Class Usage**: Agent extends UnifiedAgent appropriately
- [ ] **Capability Declaration**: Agent declares appropriate capabilities for its functions
- [ ] **Error Handling**: Proper error handling with framework-compliant logging
- [ ] **Lifecycle Management**: Agent implements proper initialize/execute/cleanup pattern
- [ ] **Communication**: Agent follows standardized communication protocols
- [ ] **Monitoring**: Agent integrates with monitoring and health check systems

## Code Quality Requirements
- [ ] **Language Standards**: Code follows Python/JavaScript best practices
- [ ] **Naming Conventions**: Variables, functions, and classes use consistent naming
- [ ] **Code Organization**: Clear separation of concerns and modular structure
- [ ] **Performance**: Code performs efficiently and handles scaling requirements
- [ ] **Security**: No security vulnerabilities or unsafe patterns
- [ ] **Maintainability**: Code is well-documented and easy to understand

## Framework Integration Requirements
- [ ] **Registry Integration**: Agent properly registers with agent registry
- [ ] **Plugin System**: Agent supports plugin configuration if applicable
- [ ] **Feature Flags**: Agent respects feature flag configurations
- [ ] **Environment Variables**: Agent properly handles environment configuration
- [ ] **Health Checks**: Agent implements health check endpoints
- [ ] **Metrics**: Agent exposes appropriate monitoring metrics

## Testing Requirements
- [ ] **Unit Tests**: All agent methods have corresponding unit tests
- [ ] **Integration Tests**: Agent works correctly with other framework components
- [ ] **Framework Tests**: Agent passes framework compliance validation
- [ ] **Cross-Language Tests**: Agent behavior consistent across implementations
- [ ] **Performance Tests**: Agent meets performance requirements under load
- [ ] **Error Scenario Tests**: Agent handles all documented error conditions

## Documentation Requirements
- [ ] **README**: Complete README following standardized template
- [ ] **API Documentation**: All public methods and events documented
- [ ] **Configuration Guide**: Clear configuration instructions for both languages
- [ ] **Usage Examples**: Practical examples for both Python and JavaScript
- [ ] **Troubleshooting Guide**: Common issues and resolution steps
- [ ] **Deployment Guide**: Environment setup and deployment instructions

## Security Requirements
- [ ] **Input Validation**: All inputs validated and sanitized
- [ ] **Authentication**: Proper authentication checks where required
- [ ] **Authorization**: Appropriate permission checks implemented
- [ ] **Data Protection**: Sensitive data handled securely
- [ ] **Audit Logging**: Security events properly logged
- [ ] **Dependency Security**: No vulnerable third-party dependencies

## Performance Requirements
- [ ] **Response Time**: Agent responds within specified time limits
- [ ] **Resource Usage**: Agent uses resources efficiently
- [ ] **Scalability**: Agent handles increased load appropriately
- [ ] **Memory Management**: No memory leaks or excessive memory usage
- [ ] **Concurrent Requests**: Agent handles concurrent requests correctly
- [ ] **Timeout Handling**: Agent properly handles and recovers from timeouts

## Approval Criteria
- [ ] **All General Requirements**: Met
- [ ] **All Agent-Specific Requirements**: Met
- [ ] **All Code Quality Requirements**: Met
- [ ] **All Framework Integration Requirements**: Met
- [ ] **All Testing Requirements**: Met (>80% coverage)
- [ ] **All Documentation Requirements**: Met
- [ ] **All Security Requirements**: Met
- [ ] **All Performance Requirements**: Met
- [ ] **2 Framework Reviews**: Approved by framework maintainers
- [ ] **Cross-Language Validation**: Consistent behavior verified
```

**Code Review Standards:**
- Use comprehensive framework-specific checklist
- Require framework compliance validation
- Ensure cross-language consistency
- Verify all quality and security requirements
- Require multiple approvals for framework changes

## Success Criteria

- [ ] Agent follows unified framework architecture
- [ ] Base classes implemented correctly for both languages
- [ ] Standardized configuration schema applied
- [ ] Cross-language testing patterns implemented
- [ ] Standardized documentation created
- [ ] Deployment standards followed
- [ ] Code review checklist completed
- [ ] Framework compliance verified

## Common Pitfalls

1. **Framework Non-Compliance** - Always use UnifiedAgent base classes
2. **Configuration Inconsistency** - Follow standardized AgentConfig schema
3. **Language-Specific Code** - Maintain consistency across Python/JavaScript
4. **Missing Documentation** - Create complete standardized documentation
5. **Inadequate Testing** - Implement comprehensive cross-language tests
6. **Deployment Issues** - Follow standardized deployment patterns
7. **Security Oversights** - Implement all security requirements
8. **Performance Problems** - Meet all performance requirements

## Cross-References

### Related Procedures
- [Agent Coding Standards](skills/agent-coding-standards/SKILL.md) - Language-specific coding standards
- [Writing Skills](skills/writing-skills/SKILL.md) - Documentation and skill creation
- [Test Driven Development](skills/test-driven-development/SKILL.md) - Testing methodology

### Related Skills
- `agent-coding-standards` - Language-specific implementation standards
- `writing-plans` - Planning agent development
- `verification-before-completion` - Quality assurance for agents

### Related Agents
- `DevForge_AI_Team` - Agent development assistance
- `QualityForge_AI_Team` - Framework compliance verification