---
name: iso42001-ai-governance
description: Implement ISO 42001:2023 AI Management System requirements for responsible AI development and deployment. Use when governing AI systems, implementing AI.
---

# ISO 42001:2023 AI Management System

Implement ISO 42001:2023 requirements for responsible AI development, deployment, and governance.

## When to Use This Skill

Use this skill when you need to:

- Establish AI management system
- Implement responsible AI practices
- Prepare for AI-specific audits
- Document AI governance
- Manage AI risks
- Meet AI regulatory requirements

**Trigger phrases**: "ISO 42001", "AI management", "responsible AI", "AI governance", "AI ethics", "AI certification"

## What This Skill Does

### ISO 42001 Structure

| Clause | Focus | Requirements |
|--------|-------|--------------|
| 4 | Context | AI system inventory, stakeholders |
| 5 | Leadership | AI policy, governance structure |
| 6 | Planning | AI risk assessment, objectives |
| 7 | Support | Resources, competence, AI awareness |
| 8 | Operation | AI lifecycle management |
| 9 | Performance | Monitoring, measurement, audit |
| 10 | Improvement | Nonconformity, continual improvement |

## Instructions

### Step 1: AI System Inventory (Clause 4)

```python
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

class AISystemType(Enum):
    CLASSIFICATION = "classification"
    REGRESSION = "regression"
    GENERATIVE = "generative"
    RECOMMENDATION = "recommendation"
    AGENTIC = "agentic"

class RiskCategory(Enum):
    MINIMAL = "minimal"
    LIMITED = "limited"
    HIGH = "high"
    UNACCEPTABLE = "unacceptable"

@dataclass
class AISystemEntry:
    """AI system inventory entry per ISO 42001."""
    system_id: str
    name: str
    description: str
    type: AISystemType
    purpose: str
    data_sources: List[str]
    model_type: str
    deployment_status: str
    risk_category: RiskCategory
    owner: str
    stakeholders: List[str]
    impact_assessment_date: Optional[str]

class AISystemInventory:
    """Maintain inventory of all AI systems."""

    def __init__(self):
        self.systems: List[AISystemEntry] = []

    def register_system(self, system: AISystemEntry) -> str:
        """Register new AI system in inventory."""
        self.systems.append(system)

        audit_log.info(
            "ai_system_registered",
            system_id=system.system_id,
            name=system.name,
            risk_category=system.risk_category.value
        )

        return system.system_id

    def get_high_risk_systems(self) -> List[AISystemEntry]:
        """Get all high-risk AI systems requiring enhanced governance."""
        return [s for s in self.systems if s.risk_category in [RiskCategory.HIGH, RiskCategory.UNACCEPTABLE]]

    def generate_inventory_report(self) -> dict:
        """Generate AI system inventory report."""
        return {
            "total_systems": len(self.systems),
            "by_risk_category": {
                cat.value: len([s for s in self.systems if s.risk_category == cat])
                for cat in RiskCategory
            },
            "by_type": {
                t.value: len([s for s in self.systems if s.type == t])
                for t in AISystemType
            },
            "systems": [self._to_dict(s) for s in self.systems]
        }
```

### Step 2: AI Risk Assessment (Clause 6)

```python
@dataclass
class AIRisk:
    """AI-specific risk per ISO 42001."""
    risk_id: str
    ai_system_id: str
    risk_type: str  # bias, safety, privacy, security, reliability
    description: str
    likelihood: int  # 1-5
    impact: int  # 1-5
    affected_stakeholders: List[str]
    existing_controls: List[str]
    residual_risk_level: str

class AIRiskAssessment:
    """ISO 42001 AI risk assessment process."""

    AI_RISK_CATEGORIES = [
        "Bias and fairness",
        "Safety and reliability",
        "Privacy and data protection",
        "Security and robustness",
        "Transparency and explainability",
        "Accountability and governance",
        "Human oversight and control",
        "Environmental impact",
    ]

    def assess_ai_system(self, system: AISystemEntry) -> List[AIRisk]:
        """Comprehensive AI risk assessment."""
        risks = []

        for category in self.AI_RISK_CATEGORIES:
            risk = self._assess_category(system, category)
            if risk:
                risks.append(risk)

        audit_log.info(
            "ai_risk_assessment_completed",
            system_id=system.system_id,
            risks_identified=len(risks)
        )

        return risks

    def _assess_category(self, system: AISystemEntry, category: str) -> Optional[AIRisk]:
        """Assess specific risk category."""
        assessments = {
            "Bias and fairness": self._assess_bias_risk,
            "Safety and reliability": self._assess_safety_risk,
            "Privacy and data protection": self._assess_privacy_risk,
            "Transparency and explainability": self._assess_transparency_risk,
        }

        assess_func = assessments.get(category)
        if assess_func:
            return assess_func(system)
        return None

    def _assess_bias_risk(self, system: AISystemEntry) -> AIRisk:
        """Assess bias and fairness risks."""
        return AIRisk(
            risk_id=f"RISK-BIAS-{system.system_id}",
            ai_system_id=system.system_id,
            risk_type="bias",
            description="Potential for unfair outcomes across protected groups",
            likelihood=self._calculate_bias_likelihood(system),
            impact=self._calculate_bias_impact(system),
            affected_stakeholders=["End users", "Protected groups"],
            existing_controls=["Bias testing", "Fairness metrics monitoring"],
            residual_risk_level="medium"
        )
```

### Step 3: AI Lifecycle Management (Clause 8)

```python
class AILifecycleManager:
    """Manage AI system lifecycle per ISO 42001."""

    LIFECYCLE_STAGES = [
        "requirements",
        "design",
        "development",
        "testing",
        "deployment",
        "operation",
        "monitoring",
        "retirement"
    ]

    def __init__(self, system_id: str):
        self.system_id = system_id
        self.current_stage = "requirements"
        self.stage_history = []

    def transition_stage(
        self,
        new_stage: str,
        approval: str,
        evidence: List[str]
    ) -> bool:
        """Transition to new lifecycle stage with approval."""
        if new_stage not in self.LIFECYCLE_STAGES:
            raise ValueError(f"Invalid stage: {new_stage}")

        # Verify stage prerequisites
        prerequisites_met = self._check_prerequisites(new_stage)
        if not prerequisites_met:
            audit_log.warning(
                "stage_transition_blocked",
                system_id=self.system_id,
                from_stage=self.current_stage,
                to_stage=new_stage,
                reason="prerequisites_not_met"
            )
            return False

        # Record transition
        self.stage_history.append({
            "from_stage": self.current_stage,
            "to_stage": new_stage,
            "timestamp": datetime.utcnow().isoformat(),
            "approved_by": approval,
            "evidence": evidence
        })

        self.current_stage = new_stage

        audit_log.info(
            "ai_lifecycle_transition",
            system_id=self.system_id,
            new_stage=new_stage,
            approved_by=approval
        )

        return True

    def _check_prerequisites(self, stage: str) -> bool:
        """Check prerequisites for stage transition."""
        prerequisites = {
            "design": ["requirements_approved", "risk_assessment_complete"],
            "development": ["design_approved", "data_governance_verified"],
            "testing": ["development_complete", "test_plan_approved"],
            "deployment": ["testing_passed", "impact_assessment_approved", "human_oversight_established"],
            "operation": ["deployment_successful", "monitoring_configured"],
            "retirement": ["retirement_plan_approved", "data_disposition_planned"]
        }

        required = prerequisites.get(stage, [])
        return all(self._check_prerequisite(p) for p in required)
```

### Step 4: AI Ethics and Responsible AI

```python
class ResponsibleAIFramework:
    """Implement responsible AI principles per ISO 42001."""

    PRINCIPLES = [
        "Fairness and non-discrimination",
        "Transparency and explainability",
        "Privacy and data governance",
        "Safety and security",
        "Human oversight and control",
        "Accountability",
        "Environmental sustainability"
    ]

    def evaluate_fairness(self, model, test_data: dict) -> FairnessReport:
        """Evaluate model fairness across protected attributes."""
        protected_attributes = ["gender", "age", "ethnicity", "disability"]
        metrics = {}

        for attr in protected_attributes:
            if attr in test_data:
                metrics[attr] = {
                    "demographic_parity": self._calc_demographic_parity(model, test_data, attr),
                    "equalized_odds": self._calc_equalized_odds(model, test_data, attr),
                    "disparate_impact": self._calc_disparate_impact(model, test_data, attr),
                }

        return FairnessReport(
            model_id=model.id,
            evaluation_date=datetime.utcnow(),
            metrics=metrics,
            compliant=self._check_fairness_thresholds(metrics)
        )

    def generate_explanation(self, model, prediction, input_data) -> Explanation:
        """Generate explainable AI output."""
        return Explanation(
            prediction=prediction,
            confidence=self._get_confidence(model, input_data),
            feature_importance=self._calculate_feature_importance(model, input_data),
            decision_path=self._trace_decision_path(model, input_data),
            counterfactuals=self._generate_counterfactuals(model, input_data),
        )

    def human_oversight_check(self, decision: AIDecision) -> OversightResult:
        """Implement human oversight requirements."""
        # Determine if human review required
        requires_review = (
            decision.confidence < 0.8 or
            decision.risk_level == "high" or
            decision.impact_level == "significant"
        )

        if requires_review:
            audit_log.info(
                "human_oversight_required",
                decision_id=decision.id,
                reason="low_confidence_or_high_risk"
            )

        return OversightResult(
            decision_id=decision.id,
            automated_decision=not requires_review,
            human_review_required=requires_review,
            override_capability=True
        )
```

### Step 5: AI Monitoring and Performance (Clause 9)

```python
class AIMonitoringService:
    """Monitor AI system performance per ISO 42001."""

    def __init__(self, system_id: str):
        self.system_id = system_id
        self.metrics_store = MetricsStore()
        self.alerting = AlertingService()

    def monitor_model_performance(self) -> PerformanceReport:
        """Monitor and report model performance metrics."""
        metrics = {
            "accuracy": self._calculate_accuracy(),
            "precision": self._calculate_precision(),
            "recall": self._calculate_recall(),
            "f1_score": self._calculate_f1(),
            "latency_p95": self._calculate_latency_p95(),
            "throughput": self._calculate_throughput(),
        }

        # Check for performance degradation
        if self._detect_degradation(metrics):
            self.alerting.send_alert(
                severity="warning",
                message=f"Performance degradation detected for {self.system_id}",
                metrics=metrics
            )

        return PerformanceReport(
            system_id=self.system_id,
            timestamp=datetime.utcnow(),
            metrics=metrics
        )

    def monitor_data_drift(self, reference_data, production_data) -> DriftReport:
        """Monitor for data drift in AI inputs."""
        drift_metrics = {
            "psi": self._calculate_psi(reference_data, production_data),
            "ks_statistic": self._calculate_ks_statistic(reference_data, production_data),
            "feature_drift": self._calculate_feature_drift(reference_data, production_data),
        }

        drift_detected = any(
            v > threshold for v, threshold in
            zip(drift_metrics.values(), [0.2, 0.1, 0.15])
        )

        if drift_detected:
            audit_log.warning(
                "data_drift_detected",
                system_id=self.system_id,
                drift_metrics=drift_metrics
            )

        return DriftReport(
            system_id=self.system_id,
            drift_detected=drift_detected,
            metrics=drift_metrics,
            recommendation="retrain" if drift_detected else "continue"
        )

    def monitor_fairness(self) -> FairnessMonitoringReport:
        """Continuous fairness monitoring."""
        current_metrics = self._calculate_fairness_metrics()
        baseline_metrics = self._get_baseline_fairness_metrics()

        deviations = {
            metric: abs(current - baseline)
            for metric, (current, baseline) in
            zip(current_metrics.keys(),
                zip(current_metrics.values(), baseline_metrics.values()))
        }

        fairness_alert = any(d > 0.05 for d in deviations.values())

        return FairnessMonitoringReport(
            system_id=self.system_id,
            current_metrics=current_metrics,
            baseline_metrics=baseline_metrics,
            deviations=deviations,
            alert=fairness_alert
        )
```

## Documentation Requirements

### Required Documents
- [ ] AI Management System Policy
- [ ] AI System Inventory
- [ ] AI Risk Assessment Methodology
- [ ] AI Risk Treatment Plan
- [ ] AI Impact Assessment Template
- [ ] Responsible AI Guidelines

### Required Records
- [ ] AI risk assessments
- [ ] Impact assessments for high-risk systems
- [ ] Model validation and testing results
- [ ] Fairness and bias evaluations
- [ ] Human oversight records
- [ ] Incident and near-miss reports

## Quality Checklist

- [ ] AI system inventory complete
- [ ] Risk assessments performed for all AI systems
- [ ] High-risk systems identified and documented
- [ ] Responsible AI principles implemented
- [ ] Human oversight mechanisms established
- [ ] Monitoring and alerting configured
- [ ] Audit trail maintained
- [ ] Continuous improvement process in place

## Related Skills

- `nist-ai-rmf` - NIST AI Risk Management Framework
- `ai-agent-governance` - AI agent-specific governance
- `iso27001-compliance` - Information security management

---

**Version**: 1.0.0
**Last Updated**: December 2025
**Based on**: AI Templates compliance_governance/compliance_frameworks/


### Iterative Refinement Strategy
This skill is optimized for an iterative approach:
1. **Execute**: Perform the core steps defined above.
2. **Review**: Critically analyze the output (coverage, quality, completeness).
3. **Refine**: If targets aren't met, repeat the specific implementation steps with improved context.
4. **Loop**: Continue until the definition of done is satisfied.
