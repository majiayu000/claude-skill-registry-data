---
name: ai-agent-governance
description: Implement the 4 Pillars Framework for AI agent governance (Lifecycle, Risk, Security, Observability). Use when deploying autonomous AI agents, implementing.
---

# AI Agent Governance - 4 Pillars Framework

Implement comprehensive governance for autonomous AI agents using the 4 Pillars Framework: Lifecycle Management, Risk Management, Security, and Observability.

## When to Use This Skill

Use this skill when you need to:

- Deploy autonomous AI agents to production
- Implement agent guardrails and safety controls
- Establish security for agentic AI systems
- Track and audit agent behavior
- Manage AI agent risks
- Comply with AI regulations (NIST AI RMF, ISO 42001)

**Trigger phrases**: "AI agent governance", "agent guardrails", "agent security", "agentic AI", "autonomous agent", "agent observability", "4 pillars", "agent lifecycle"

## What This Skill Does

### Why AI Agents Need Special Governance

Traditional software governance is insufficient for AI agents because:

| Traditional Software | AI Agents |
|---------------------|-----------|
| Deterministic | Non-deterministic |
| Predictable | Autonomous |
| Limited scope | Broad capabilities |
| Explicit programming | Emergent behaviors |
| Fixed logic | Learning and evolving |

80% of organizations have encountered risky behaviors from AI agents, including improper data exposure and unauthorized system access.

### The 4 Pillars Framework

| Pillar | Principle | Key Question |
|--------|-----------|--------------|
| Lifecycle | Separation of Duties | Can you safely promote changes through environments with rollback? |
| Risk | Defense in Depth | Do you have multiple layers of protection? |
| Security | Least Privilege | Are data sources accessible only to authorized agents? |
| Observability | Audit Everything | Can you trace every tool call, data access, and decision? |

## Instructions

### Step 1: Pillar 1 - Lifecycle Management (Separation of Duties)

```python
from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Optional
from enum import Enum

class DeploymentEnvironment(Enum):
    DEV = "development"
    STAGING = "staging"
    PROD = "production"

@dataclass
class AgentVersion:
    """Version control for AI agent configurations."""
    version_id: str
    agent_id: str
    prompt_version: str
    model_version: str
    tool_config_version: str
    created_at: datetime
    created_by: str
    changelog: str

class AgentLifecycleManager:
    """
    AI Agent Lifecycle Management.

    Pillar 1: Separation of Duties
    - Version control for agents
    - Environment promotion workflow
    - Rollback capabilities
    """

    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.versions: List[AgentVersion] = []

    def create_version(
        self,
        prompt_template: str,
        model_name: str,
        tool_config: Dict,
        created_by: str,
        changelog: str
    ) -> AgentVersion:
        """
        Create new agent version.

        Version control ensures:
        - Traceability of changes
        - Rollback capability
        - Approval workflow
        """
        version = AgentVersion(
            version_id=f"v{len(self.versions) + 1}.0.0",
            agent_id=self.agent_id,
            prompt_version=self._hash_prompt(prompt_template),
            model_version=model_name,
            tool_config_version=self._hash_config(tool_config),
            created_at=datetime.utcnow(),
            created_by=created_by,
            changelog=changelog
        )

        self.versions.append(version)

        audit_log.info(
            "agent_version_created",
            agent_id=self.agent_id,
            version_id=version.version_id,
            created_by=created_by
        )

        return version

    def promote_to_staging(
        self,
        version_id: str,
        approved_by: str,
        test_results: Dict
    ) -> bool:
        """
        Promote agent version to staging.

        Requires:
        - All automated tests passed
        - Technical review approval
        """
        # Verify tests passed
        if not self._verify_test_results(test_results):
            raise ValueError("Cannot promote: Tests not passing")

        # Record promotion
        promotion = AgentPromotion(
            version_id=version_id,
            from_env=DeploymentEnvironment.DEV,
            to_env=DeploymentEnvironment.STAGING,
            approved_by=approved_by,
            timestamp=datetime.utcnow()
        )

        self.promotions.append(promotion)

        audit_log.info(
            "agent_promoted_staging",
            agent_id=self.agent_id,
            version_id=version_id,
            approved_by=approved_by
        )

        return True

    def promote_to_production(
        self,
        version_id: str,
        approved_by: str,
        business_approval: str,
        canary_percentage: int = 10
    ) -> bool:
        """
        Promote agent to production with canary deployment.

        Requires:
        - Staging validation complete
        - Business stakeholder approval
        - Canary deployment (gradual rollout)
        """
        # Verify staging validation
        if not self._staging_validation_passed(version_id):
            raise ValueError("Cannot promote: Staging validation incomplete")

        # Deploy canary
        self._deploy_canary(version_id, canary_percentage)

        audit_log.info(
            "agent_canary_deployed",
            agent_id=self.agent_id,
            version_id=version_id,
            canary_percentage=canary_percentage,
            approved_by=approved_by,
            business_approval=business_approval
        )

        return True

    def rollback(
        self,
        to_version_id: str,
        reason: str,
        initiated_by: str
    ) -> bool:
        """
        Rollback agent to previous version.

        Critical capability:
        - Instant rollback on issues
        - Preserves audit trail
        - Triggers incident workflow
        """
        previous_version = self._get_version(to_version_id)

        if not previous_version:
            raise ValueError(f"Version {to_version_id} not found")

        # Perform rollback
        self._activate_version(to_version_id)

        audit_log.warning(
            "agent_rollback",
            agent_id=self.agent_id,
            to_version=to_version_id,
            reason=reason,
            initiated_by=initiated_by
        )

        # Trigger incident workflow
        self._create_incident(
            title=f"Agent rollback: {self.agent_id}",
            description=reason,
            severity="high"
        )

        return True
```

### Step 2: Pillar 2 - Risk Management (Defense in Depth)

```python
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
import re

class AgentRiskControls:
    """
    AI Agent Risk Management.

    Pillar 2: Defense in Depth
    - Multiple overlapping defense layers
    - PII detection and redaction
    - Guardrails for inputs and outputs
    - Compliance controls
    """

    SENSITIVE_DATA_PATTERNS = {
        "ssn": r"\b\d{3}-\d{2}-\d{4}\b",
        "credit_card": r"\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b",
        "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
        "phone": r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b",
        "api_key": r"\b(sk-|pk-|api_)[A-Za-z0-9]{20,}\b"
    }

    def __init__(self):
        self.analyzer = AnalyzerEngine()
        self.anonymizer = AnonymizerEngine()

    def apply_input_guardrails(
        self,
        user_input: str,
        agent_id: str
    ) -> Dict:
        """
        Layer 1: Input Guardrails

        Validates user input before agent processing:
        - Prompt injection detection
        - Input length limits
        - Content moderation
        """
        validation_result = {
            "valid": True,
            "blocked": False,
            "warnings": [],
            "sanitized_input": user_input
        }

        # Check for prompt injection
        injection_patterns = [
            r"ignore previous instructions",
            r"disregard.*?instructions",
            r"system prompt",
            r"you are now",
            r"pretend you are",
            r"\[SYSTEM\]",
            r"<\|im_start\|>",
            r"<admin>"
        ]

        for pattern in injection_patterns:
            if re.search(pattern, user_input, re.IGNORECASE):
                validation_result["valid"] = False
                validation_result["blocked"] = True
                validation_result["block_reason"] = "prompt_injection_detected"

                audit_log.warning(
                    "guardrail_input_blocked",
                    agent_id=agent_id,
                    reason="prompt_injection",
                    pattern=pattern
                )

                return validation_result

        # Input length check (prevent resource exhaustion)
        if len(user_input) > 50000:
            validation_result["valid"] = False
            validation_result["blocked"] = True
            validation_result["block_reason"] = "input_too_long"
            return validation_result

        return validation_result

    def detect_and_redact_pii(
        self,
        text: str,
        context: str = "input"
    ) -> Dict:
        """
        Layer 2: PII Detection and Redaction

        Uses Microsoft Presidio for:
        - Pattern-based detection (SSN, credit cards, emails)
        - NER-based detection (names, addresses)
        - Automatic redaction
        """
        # Detect PII
        results = self.analyzer.analyze(
            text=text,
            language='en',
            entities=[
                "PERSON", "EMAIL_ADDRESS", "PHONE_NUMBER",
                "CREDIT_CARD", "US_SSN", "US_PASSPORT",
                "IP_ADDRESS", "MEDICAL_LICENSE"
            ]
        )

        pii_found = len(results) > 0

        if pii_found:
            # Redact PII
            anonymized = self.anonymizer.anonymize(
                text=text,
                analyzer_results=results
            )

            audit_log.warning(
                "pii_detected_and_redacted",
                context=context,
                pii_types=[r.entity_type for r in results],
                pii_count=len(results)
            )

            return {
                "pii_found": True,
                "pii_types": [r.entity_type for r in results],
                "original_text": text,
                "redacted_text": anonymized.text
            }

        return {
            "pii_found": False,
            "redacted_text": text
        }

    def apply_output_guardrails(
        self,
        agent_output: str,
        agent_id: str
    ) -> Dict:
        """
        Layer 3: Output Guardrails

        Validates agent output before returning to user:
        - PII redaction
        - Harmful content filtering
        - Prompt leakage prevention
        """
        result = {
            "safe": True,
            "modified": False,
            "sanitized_output": agent_output
        }

        # Check for PII in output
        pii_result = self.detect_and_redact_pii(agent_output, context="output")
        if pii_result["pii_found"]:
            result["modified"] = True
            result["sanitized_output"] = pii_result["redacted_text"]

        # Check for prompt leakage
        if self._detect_prompt_leakage(agent_output):
            result["safe"] = False
            result["blocked"] = True
            result["block_reason"] = "prompt_leakage"

            audit_log.warning(
                "guardrail_output_blocked",
                agent_id=agent_id,
                reason="prompt_leakage"
            )

        # Check for harmful content
        harmful_patterns = [
            r"how to hack",
            r"how to steal",
            r"illegal instructions",
            r"bypass security"
        ]

        for pattern in harmful_patterns:
            if re.search(pattern, agent_output, re.IGNORECASE):
                result["safe"] = False
                result["blocked"] = True
                result["block_reason"] = "harmful_content"

        return result

    def apply_tool_guardrails(
        self,
        agent_id: str,
        tool_name: str,
        tool_input: Dict,
        user_context: Dict
    ) -> Dict:
        """
        Layer 4: Tool Use Guardrails

        Controls what tools agent can use:
        - Tool allowlist per agent
        - Sensitive operation approval
        - Rate limiting
        """
        # Get agent's allowed tools
        allowed_tools = self._get_allowed_tools(agent_id)

        if tool_name not in allowed_tools:
            audit_log.warning(
                "tool_access_denied",
                agent_id=agent_id,
                tool_name=tool_name,
                reason="not_in_allowlist"
            )

            return {
                "allowed": False,
                "reason": f"Tool '{tool_name}' not in agent's allowlist"
            }

        # Check for sensitive operations requiring approval
        sensitive_operations = ["delete", "update", "transfer", "execute"]

        if any(op in tool_name.lower() for op in sensitive_operations):
            if not self._has_human_approval(agent_id, tool_name, tool_input):
                return {
                    "allowed": False,
                    "reason": "sensitive_operation_requires_approval",
                    "approval_required": True
                }

        # Rate limiting
        if self._is_rate_limited(agent_id, tool_name):
            return {
                "allowed": False,
                "reason": "rate_limit_exceeded"
            }

        return {"allowed": True}
```

### Step 3: Pillar 3 - Security (Least Privilege)

```python
from functools import wraps
from typing import Callable
import hashlib
import secrets

class AgentRole(Enum):
    READ_ONLY = "read_only"
    STANDARD = "standard"
    ELEVATED = "elevated"
    ADMIN = "admin"

@dataclass
class AgentCredential:
    """Secure credential for AI agent."""
    credential_id: str
    agent_id: str
    role: AgentRole
    api_key_hash: str
    created_at: datetime
    expires_at: datetime
    scopes: List[str]

class AgentSecurityManager:
    """
    AI Agent Security Controls.

    Pillar 3: Least Privilege
    - Service principals for agents
    - Role-based access control (RBAC)
    - Secrets management
    - API key rotation
    """

    def create_agent_credential(
        self,
        agent_id: str,
        role: AgentRole,
        scopes: List[str],
        expires_days: int = 90
    ) -> Dict:
        """
        Create secure credential for agent.

        Least Privilege:
        - Define specific scopes
        - Time-limited credentials
        - Role-based permissions
        """
        # Generate secure API key
        api_key = f"agent_{secrets.token_urlsafe(32)}"
        api_key_hash = hashlib.sha256(api_key.encode()).hexdigest()

        credential = AgentCredential(
            credential_id=f"cred_{secrets.token_hex(8)}",
            agent_id=agent_id,
            role=role,
            api_key_hash=api_key_hash,
            created_at=datetime.utcnow(),
            expires_at=datetime.utcnow() + timedelta(days=expires_days),
            scopes=scopes
        )

        # Store credential (hash only, never plain key)
        self.credential_store.save(credential)

        audit_log.info(
            "agent_credential_created",
            agent_id=agent_id,
            credential_id=credential.credential_id,
            role=role.value,
            scopes=scopes,
            expires_at=credential.expires_at.isoformat()
        )

        # Return API key only once (store securely)
        return {
            "credential_id": credential.credential_id,
            "api_key": api_key,  # Only returned at creation
            "expires_at": credential.expires_at.isoformat(),
            "warning": "Store API key securely. It cannot be retrieved again."
        }

    def define_agent_permissions(
        self,
        agent_id: str,
        role: AgentRole
    ) -> Dict[str, List[str]]:
        """
        Define permissions based on agent role.

        RBAC Matrix:
        - READ_ONLY: Query data, no modifications
        - STANDARD: Normal operations
        - ELEVATED: Sensitive operations with approval
        - ADMIN: Full access (rare, audited)
        """
        permission_matrix = {
            AgentRole.READ_ONLY: {
                "data": ["read"],
                "tools": ["query", "search", "retrieve"],
                "actions": []
            },
            AgentRole.STANDARD: {
                "data": ["read", "create"],
                "tools": ["query", "search", "retrieve", "create"],
                "actions": ["respond", "summarize", "analyze"]
            },
            AgentRole.ELEVATED: {
                "data": ["read", "create", "update"],
                "tools": ["query", "search", "retrieve", "create", "update"],
                "actions": ["respond", "summarize", "analyze", "execute"]
            },
            AgentRole.ADMIN: {
                "data": ["read", "create", "update", "delete"],
                "tools": ["*"],
                "actions": ["*"]
            }
        }

        permissions = permission_matrix.get(role, permission_matrix[AgentRole.READ_ONLY])

        # Store permissions
        self._store_agent_permissions(agent_id, permissions)

        return permissions

    def require_permission(self, required_scope: str):
        """
        Decorator to enforce permission checks on agent operations.

        Usage:
        @agent_security.require_permission("data:update")
        def update_customer_record(agent_id, record_id, data):
            ...
        """
        def decorator(func: Callable):
            @wraps(func)
            def wrapper(agent_id: str, *args, **kwargs):
                # Get agent's permissions
                permissions = self._get_agent_permissions(agent_id)

                # Parse scope
                resource, action = required_scope.split(":")

                # Check permission
                if action not in permissions.get(resource, []):
                    audit_log.warning(
                        "agent_permission_denied",
                        agent_id=agent_id,
                        required_scope=required_scope,
                        available_permissions=permissions
                    )
                    raise PermissionError(
                        f"Agent {agent_id} lacks permission: {required_scope}"
                    )

                # Log access
                audit_log.info(
                    "agent_permission_granted",
                    agent_id=agent_id,
                    scope=required_scope
                )

                return func(agent_id, *args, **kwargs)
            return wrapper
        return decorator

    def rotate_credentials(
        self,
        agent_id: str,
        initiated_by: str
    ) -> Dict:
        """
        Rotate agent credentials.

        Best practice:
        - Regular rotation (90 days)
        - Immediate rotation on compromise
        - Zero-downtime rotation
        """
        # Get current credential
        current_cred = self.credential_store.get_active(agent_id)

        if not current_cred:
            raise ValueError(f"No active credential for agent {agent_id}")

        # Create new credential with same permissions
        new_cred = self.create_agent_credential(
            agent_id=agent_id,
            role=current_cred.role,
            scopes=current_cred.scopes
        )

        # Mark old credential for deprecation (grace period)
        current_cred.expires_at = datetime.utcnow() + timedelta(hours=24)
        self.credential_store.update(current_cred)

        audit_log.info(
            "agent_credential_rotated",
            agent_id=agent_id,
            old_credential_id=current_cred.credential_id,
            new_credential_id=new_cred["credential_id"],
            initiated_by=initiated_by
        )

        return new_cred
```

### Step 4: Pillar 4 - Observability (Audit Everything)

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.trace import Status, StatusCode
from prometheus_client import Counter, Histogram, Gauge
import hashlib
import json

class AgentObservability:
    """
    AI Agent Observability.

    Pillar 4: Audit Everything
    - Distributed tracing
    - Structured logging
    - Metrics collection
    - Data lineage
    """

    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self._setup_tracing()
        self._setup_metrics()

    def _setup_tracing(self):
        """Initialize OpenTelemetry tracing."""
        provider = TracerProvider()

        exporter = OTLPSpanExporter(
            endpoint="http://localhost:4317",
            insecure=True
        )

        provider.add_span_processor(BatchSpanProcessor(exporter))
        trace.set_tracer_provider(provider)

        self.tracer = trace.get_tracer(__name__)

    def _setup_metrics(self):
        """Initialize Prometheus metrics."""
        self.agent_requests = Counter(
            'agent_requests_total',
            'Total agent requests',
            ['agent_name', 'status']
        )

        self.agent_latency = Histogram(
            'agent_request_duration_seconds',
            'Agent request latency',
            ['agent_name'],
            buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0]
        )

        self.llm_tokens = Counter(
            'llm_tokens_total',
            'LLM tokens used',
            ['agent_name', 'model', 'token_type']
        )

        self.llm_cost = Counter(
            'llm_cost_usd_total',
            'LLM cost in USD',
            ['agent_name', 'model']
        )

        self.guardrail_triggers = Counter(
            'guardrail_triggers_total',
            'Guardrail triggers',
            ['agent_name', 'guardrail_name']
        )

    def trace_agent_execution(
        self,
        user_query: str,
        user_id: str,
        session_id: str
    ):
        """
        Create root span for agent execution.

        Traces capture end-to-end workflow:
        Query → Reasoning → Tool calls → Response
        """
        return self.tracer.start_as_current_span(
            "agent.execute",
            kind=trace.SpanKind.SERVER,
            attributes={
                "agent.name": self.agent_name,
                "query.text": user_query[:200],
                "query.length": len(user_query),
                "user.id": user_id,
                "session.id": session_id
            }
        )

    def trace_llm_call(
        self,
        model: str,
        prompt: str,
        parameters: Dict
    ):
        """
        Trace LLM API call.

        Captures:
        - Model and parameters
        - Token usage and cost
        - Latency
        """
        prompt_hash = hashlib.sha256(prompt.encode()).hexdigest()[:16]

        return self.tracer.start_as_current_span(
            "llm.call",
            kind=trace.SpanKind.CLIENT,
            attributes={
                "gen_ai.system": "openai",
                "gen_ai.request.model": model,
                "gen_ai.request.max_tokens": parameters.get("max_tokens", 1000),
                "gen_ai.request.temperature": parameters.get("temperature", 0.7),
                "gen_ai.prompt.hash": prompt_hash,
                "gen_ai.prompt.length": len(prompt)
            }
        )

    def trace_tool_invocation(
        self,
        tool_name: str,
        tool_input: Dict
    ):
        """
        Trace tool invocation.

        Captures what external systems agent accessed.
        """
        return self.tracer.start_as_current_span(
            f"tool.{tool_name}",
            kind=trace.SpanKind.INTERNAL,
            attributes={
                "tool.name": tool_name,
                "tool.input.size": len(json.dumps(tool_input)),
                "tool.input.keys": list(tool_input.keys())
            }
        )

    def log_agent_decision(
        self,
        decision: str,
        reasoning: str,
        confidence: float,
        alternatives: List[str],
        context: Dict
    ):
        """
        Log agent decision with reasoning.

        Critical for:
        - Debugging (why did agent do that?)
        - Auditing (what influenced decision?)
        - Compliance (demonstrate accountability)
        """
        decision_log = {
            "event_type": "agent_decision",
            "timestamp": datetime.utcnow().isoformat(),
            "agent_name": self.agent_name,

            # Decision details
            "decision": decision,
            "reasoning": reasoning[:500],
            "confidence": confidence,
            "alternatives_considered": alternatives,

            # Context
            "user_id": context.get("user_id"),
            "session_id": context.get("session_id"),
            "trace_id": context.get("trace_id"),

            # Governance
            "decision_id": str(uuid.uuid4()),
            "reviewable": True,
            "automated": True
        }

        logger.info("Agent decision", extra=decision_log)

    def record_llm_usage(
        self,
        model: str,
        prompt_tokens: int,
        completion_tokens: int,
        cost: float,
        latency: float
    ):
        """Record LLM usage metrics."""
        self.llm_tokens.labels(
            agent_name=self.agent_name,
            model=model,
            token_type="prompt"
        ).inc(prompt_tokens)

        self.llm_tokens.labels(
            agent_name=self.agent_name,
            model=model,
            token_type="completion"
        ).inc(completion_tokens)

        self.llm_cost.labels(
            agent_name=self.agent_name,
            model=model
        ).inc(cost)

    def record_guardrail_trigger(
        self,
        guardrail_name: str,
        trigger_reason: str,
        blocked_action: str
    ):
        """Log guardrail trigger."""
        self.guardrail_triggers.labels(
            agent_name=self.agent_name,
            guardrail_name=guardrail_name
        ).inc()

        logger.warning("Guardrail triggered", extra={
            "event_type": "guardrail_trigger",
            "agent_name": self.agent_name,
            "guardrail_name": guardrail_name,
            "trigger_reason": trigger_reason,
            "blocked_action": blocked_action,
            "timestamp": datetime.utcnow().isoformat()
        })
```

### Step 5: Complete Agent Governance Implementation

```python
class AIAgentGovernance:
    """
    Complete AI Agent Governance implementing all 4 Pillars.

    Usage:
        governance = AIAgentGovernance("customer-service-agent")

        # Process user request with full governance
        response = governance.process_request(
            user_input="Help me with my order",
            user_id="user123",
            session_id="sess456"
        )
    """

    def __init__(self, agent_id: str, agent_config: Dict):
        self.agent_id = agent_id
        self.config = agent_config

        # Initialize all 4 pillars
        self.lifecycle = AgentLifecycleManager(agent_id)
        self.risk = AgentRiskControls()
        self.security = AgentSecurityManager()
        self.observability = AgentObservability(agent_id)

    def process_request(
        self,
        user_input: str,
        user_id: str,
        session_id: str
    ) -> Dict:
        """
        Process user request with full governance.

        Applies all 4 pillars:
        1. Lifecycle: Uses versioned agent configuration
        2. Risk: Input/output guardrails, PII detection
        3. Security: Permission checks, authentication
        4. Observability: Tracing, logging, metrics
        """
        # Start trace (Pillar 4: Observability)
        with self.observability.trace_agent_execution(
            user_input, user_id, session_id
        ) as span:
            try:
                # Pillar 2: Input guardrails
                input_validation = self.risk.apply_input_guardrails(
                    user_input, self.agent_id
                )

                if not input_validation["valid"]:
                    span.set_attribute("agent.status", "blocked_input")
                    return {
                        "status": "blocked",
                        "reason": input_validation.get("block_reason")
                    }

                # Pillar 2: PII detection
                pii_result = self.risk.detect_and_redact_pii(
                    user_input, context="input"
                )
                safe_input = pii_result["redacted_text"]

                # Pillar 3: Verify agent permissions
                self.security.require_permission("data:read")(
                    lambda aid: None
                )(self.agent_id)

                # Process with agent (using versioned config from Pillar 1)
                agent_response = self._execute_agent(safe_input)

                # Pillar 2: Output guardrails
                output_validation = self.risk.apply_output_guardrails(
                    agent_response, self.agent_id
                )

                if not output_validation["safe"]:
                    span.set_attribute("agent.status", "blocked_output")
                    return {
                        "status": "blocked",
                        "reason": output_validation.get("block_reason")
                    }

                # Pillar 4: Log decision
                self.observability.log_agent_decision(
                    decision="respond",
                    reasoning="User query processed successfully",
                    confidence=0.9,
                    alternatives=[],
                    context={
                        "user_id": user_id,
                        "session_id": session_id,
                        "trace_id": span.get_span_context().trace_id
                    }
                )

                span.set_attribute("agent.status", "success")

                return {
                    "status": "success",
                    "response": output_validation["sanitized_output"]
                }

            except Exception as e:
                span.set_status(Status(StatusCode.ERROR, str(e)))
                span.record_exception(e)

                audit_log.error(
                    "agent_execution_failed",
                    agent_id=self.agent_id,
                    error=str(e)
                )

                raise
```

## Implementation Checklist

### Pillar 1: Lifecycle Management
- [ ] Version control for agent prompts/configs
- [ ] Dev → Staging → Prod environments
- [ ] CI/CD pipeline for agent deployments
- [ ] Canary deployment capability
- [ ] Instant rollback procedures
- [ ] Approval workflow for production changes

### Pillar 2: Risk Management
- [ ] Input guardrails active
- [ ] Output guardrails active
- [ ] Tool use guardrails active
- [ ] PII detection operational
- [ ] Content moderation implemented
- [ ] Drift detection configured

### Pillar 3: Security
- [ ] Service principals for agents
- [ ] RBAC implemented
- [ ] Secrets management integrated
- [ ] Credential rotation automated
- [ ] API rate limiting active
- [ ] TLS for all communications

### Pillar 4: Observability
- [ ] OpenTelemetry tracing instrumented
- [ ] Structured audit logging
- [ ] Prometheus metrics exported
- [ ] Grafana dashboards created
- [ ] Alert rules configured
- [ ] Data lineage tracked

## Quality Checklist

- [ ] All 4 pillars implemented
- [ ] Agent versioning in place
- [ ] Guardrails tested with adversarial inputs
- [ ] Rollback tested and documented
- [ ] Credentials rotated regularly
- [ ] Audit trail complete and searchable
- [ ] Compliance mapping documented
- [ ] Incident response procedures ready

## Compliance Framework Mapping

### SOC 2 Integration

| SOC 2 Control | 4 Pillars Coverage |
|---------------|-------------------|
| CC6.1 Access Controls | Pillar 3: Security (RBAC) |
| CC6.7 Encryption | Pillar 3: Security (TLS) |
| CC7.2 System Monitoring | Pillar 4: Observability |
| CC8.1 Change Management | Pillar 1: Lifecycle |

### ISO 42001 Integration

| ISO 42001 Clause | 4 Pillars Coverage |
|-----------------|-------------------|
| AI System Lifecycle | Pillar 1: Lifecycle Management |
| AI Risk Management | Pillar 2: Risk Management |
| AI Security | Pillar 3: Security |
| AI Performance Monitoring | Pillar 4: Observability |

### NIST AI RMF Integration

| NIST Function | 4 Pillars Coverage |
|--------------|-------------------|
| GOVERN | Pillar 1 + Pillar 3 |
| MAP | Pillar 2 (risk identification) |
| MEASURE | Pillar 4 (monitoring) |
| MANAGE | All 4 pillars |

## Related Skills

- `nist-ai-rmf` - NIST AI Risk Management Framework
- `iso42001-ai-governance` - ISO 42001 AI Management System
- `soc2-compliance` - SOC 2 implementation
- `security-review` - Security vulnerability review

---

**Version**: 1.0.0
**Last Updated**: December 2025
**Based on**: AI Templates compliance_governance/ai_agent_governance/


### Iterative Refinement Strategy
This skill is optimized for an iterative approach:
1. **Execute**: Perform the core steps defined above.
2. **Review**: Critically analyze the output (coverage, quality, completeness).
3. **Refine**: If targets aren't met, repeat the specific implementation steps with improved context.
4. **Loop**: Continue until the definition of done is satisfied.
