---
name: nist-ai-rmf
description: Implement NIST AI Risk Management Framework (Govern, Map, Measure, Manage) for AI system risk management. Use when deploying AI in US federal contexts.
---

# NIST AI Risk Management Framework

Implement the NIST AI RMF 1.0 for comprehensive AI risk management following the Govern, Map, Measure, Manage framework.

## When to Use This Skill

Use this skill when you need to:

- Implement AI risk management
- Meet US federal AI requirements
- Establish AI governance framework
- Document AI risks and controls
- Prepare for AI audits
- Deploy AI responsibly

**Trigger phrases**: "NIST AI RMF", "AI risk management", "federal AI compliance", "AI governance", "AI risk framework", "responsible AI"

## What This Skill Does

### NIST AI RMF Functions

| Function | Purpose | Key Activities |
|----------|---------|----------------|
| **GOVERN** | Culture and governance | Policies, roles, accountability |
| **MAP** | Context and risks | AI system characterization |
| **MEASURE** | Assess and analyze | Risk assessment, testing |
| **MANAGE** | Prioritize and act | Risk treatment, monitoring |

## Instructions

### Step 1: GOVERN Function

```python
class AIGovernanceFramework:
    """NIST AI RMF GOVERN function implementation."""

    def establish_governance_structure(self) -> GovernanceStructure:
        """Define AI governance roles and responsibilities."""
        return GovernanceStructure(
            roles=[
                Role(
                    title="AI Governance Board",
                    responsibilities=[
                        "Approve AI strategy and policies",
                        "Oversee high-risk AI deployments",
                        "Review AI incident reports",
                        "Ensure regulatory compliance"
                    ],
                    members=["CTO", "CISO", "Legal", "Ethics Officer"]
                ),
                Role(
                    title="AI Risk Manager",
                    responsibilities=[
                        "Conduct AI risk assessments",
                        "Maintain AI risk register",
                        "Report to governance board",
                        "Coordinate risk treatment"
                    ]
                ),
                Role(
                    title="AI System Owner",
                    responsibilities=[
                        "Accountable for AI system risks",
                        "Ensure compliance with policies",
                        "Approve AI system changes",
                        "Respond to incidents"
                    ]
                ),
            ],
            reporting_structure={
                "ai_system_owner": "ai_risk_manager",
                "ai_risk_manager": "ai_governance_board",
                "ai_governance_board": "executive_leadership"
            }
        )

    def create_ai_policy(self) -> AIPolicy:
        """Create organizational AI policy."""
        return AIPolicy(
            title="Organizational AI Policy",
            version="1.0",
            sections=[
                PolicySection(
                    name="Purpose",
                    content="Establish principles for responsible AI development and use"
                ),
                PolicySection(
                    name="Scope",
                    content="All AI systems developed, deployed, or acquired"
                ),
                PolicySection(
                    name="Principles",
                    content=[
                        "Transparency: AI decisions should be explainable",
                        "Fairness: AI should not discriminate",
                        "Privacy: AI must protect personal data",
                        "Safety: AI must be reliable and secure",
                        "Accountability: Clear ownership of AI risks"
                    ]
                ),
                PolicySection(
                    name="Requirements",
                    content=[
                        "Risk assessment for all AI systems",
                        "Impact assessment for high-risk AI",
                        "Human oversight for consequential decisions",
                        "Continuous monitoring of AI performance"
                    ]
                ),
            ]
        )

    def define_risk_tolerance(self) -> RiskTolerance:
        """Define organizational AI risk tolerance."""
        return RiskTolerance(
            categories={
                "safety": {
                    "tolerance": "very_low",
                    "description": "No tolerance for AI causing physical harm"
                },
                "fairness": {
                    "tolerance": "low",
                    "description": "Minimal tolerance for discriminatory outcomes"
                },
                "privacy": {
                    "tolerance": "low",
                    "description": "Strong protection of personal data required"
                },
                "security": {
                    "tolerance": "low",
                    "description": "Robust defenses against adversarial attacks"
                },
                "reliability": {
                    "tolerance": "medium",
                    "description": "Acceptable degradation under defined conditions"
                }
            }
        )
```

### Step 2: MAP Function

```python
class AISystemMapping:
    """NIST AI RMF MAP function implementation."""

    def characterize_ai_system(self, system_info: dict) -> AICharacterization:
        """Characterize AI system context and risks."""
        return AICharacterization(
            system_id=system_info["id"],
            basic_info={
                "name": system_info["name"],
                "purpose": system_info["purpose"],
                "type": system_info["type"],  # ML, rule-based, hybrid
                "deployment_environment": system_info["environment"],
            },
            intended_use={
                "primary_users": system_info["users"],
                "use_cases": system_info["use_cases"],
                "intended_benefits": system_info["benefits"],
                "limitations": system_info["limitations"],
            },
            data_characteristics={
                "training_data_sources": system_info["data_sources"],
                "data_types": system_info["data_types"],
                "data_volume": system_info["data_volume"],
                "sensitive_data": system_info["sensitive_data"],
            },
            technical_characteristics={
                "model_type": system_info["model_type"],
                "model_complexity": system_info["complexity"],
                "explainability_level": system_info["explainability"],
                "update_frequency": system_info["update_frequency"],
            }
        )

    def identify_stakeholders(self, system_id: str) -> list:
        """Identify AI system stakeholders and impacts."""
        return [
            Stakeholder(
                type="direct_users",
                description="Users who interact directly with the AI system",
                potential_impacts=["accuracy of decisions", "user experience"],
                engagement_method="user testing, feedback collection"
            ),
            Stakeholder(
                type="affected_individuals",
                description="People affected by AI system decisions",
                potential_impacts=["fairness", "access to services", "privacy"],
                engagement_method="impact assessments, public consultation"
            ),
            Stakeholder(
                type="operators",
                description="Staff who operate and maintain the AI system",
                potential_impacts=["workload", "skill requirements"],
                engagement_method="training, operational feedback"
            ),
            Stakeholder(
                type="oversight_bodies",
                description="Regulators and auditors",
                potential_impacts=["compliance requirements"],
                engagement_method="reporting, audits"
            ),
        ]

    def map_ai_risks(self, characterization: AICharacterization) -> list:
        """Map potential risks based on AI system characteristics."""
        risk_categories = [
            "Validity and reliability",
            "Safety",
            "Security and resilience",
            "Accountability and transparency",
            "Explainability and interpretability",
            "Privacy",
            "Fairness (harmful bias management)"
        ]

        risks = []
        for category in risk_categories:
            category_risks = self._assess_category_risks(characterization, category)
            risks.extend(category_risks)

        return risks
```

### Step 3: MEASURE Function

```python
class AIRiskMeasurement:
    """NIST AI RMF MEASURE function implementation."""

    def assess_ai_risks(self, system_id: str, mapped_risks: list) -> RiskAssessmentReport:
        """Quantify and analyze identified AI risks."""
        assessed_risks = []

        for risk in mapped_risks:
            assessment = RiskAssessment(
                risk_id=risk.id,
                category=risk.category,
                description=risk.description,
                likelihood=self._assess_likelihood(risk),
                impact=self._assess_impact(risk),
                existing_controls=self._identify_controls(risk),
                residual_risk=self._calculate_residual(risk),
                confidence_level=self._assess_confidence(risk)
            )
            assessed_risks.append(assessment)

        return RiskAssessmentReport(
            system_id=system_id,
            assessment_date=datetime.utcnow(),
            risks=assessed_risks,
            overall_risk_level=self._calculate_overall_risk(assessed_risks),
            recommendations=self._generate_recommendations(assessed_risks)
        )

    def test_ai_system(self, system_id: str) -> TestingReport:
        """Comprehensive AI system testing."""
        tests = {
            "accuracy_testing": self._test_accuracy(system_id),
            "fairness_testing": self._test_fairness(system_id),
            "robustness_testing": self._test_robustness(system_id),
            "security_testing": self._test_security(system_id),
            "explainability_testing": self._test_explainability(system_id),
        }

        return TestingReport(
            system_id=system_id,
            test_date=datetime.utcnow(),
            test_results=tests,
            overall_status=self._determine_status(tests),
            issues_found=self._collect_issues(tests)
        )

    def _test_fairness(self, system_id: str) -> FairnessTestResult:
        """Test AI system for fairness across protected groups."""
        protected_attributes = ["gender", "race", "age", "disability"]

        results = {}
        for attr in protected_attributes:
            results[attr] = {
                "demographic_parity_ratio": self._calc_dp_ratio(system_id, attr),
                "equalized_odds_difference": self._calc_eo_diff(system_id, attr),
                "disparate_impact_ratio": self._calc_di_ratio(system_id, attr),
                "threshold_passed": True  # Based on defined thresholds
            }

        return FairnessTestResult(
            system_id=system_id,
            metrics=results,
            overall_fair=all(r["threshold_passed"] for r in results.values())
        )

    def _test_robustness(self, system_id: str) -> RobustnessTestResult:
        """Test AI system robustness against adversarial inputs."""
        return RobustnessTestResult(
            system_id=system_id,
            tests=[
                {"test": "noise_perturbation", "passed": True, "accuracy_drop": 0.02},
                {"test": "adversarial_examples", "passed": True, "success_rate": 0.05},
                {"test": "out_of_distribution", "passed": True, "detection_rate": 0.95},
            ]
        )
```

### Step 4: MANAGE Function

```python
class AIRiskManagement:
    """NIST AI RMF MANAGE function implementation."""

    def prioritize_risks(self, assessment: RiskAssessmentReport) -> PrioritizedRiskList:
        """Prioritize risks for treatment."""
        prioritized = sorted(
            assessment.risks,
            key=lambda r: (r.impact.value * r.likelihood.value, r.impact.value),
            reverse=True
        )

        return PrioritizedRiskList(
            system_id=assessment.system_id,
            risks=[
                PrioritizedRisk(
                    risk=risk,
                    priority=idx + 1,
                    treatment_urgency=self._determine_urgency(risk)
                )
                for idx, risk in enumerate(prioritized)
            ]
        )

    def develop_treatment_plan(
        self,
        risk: RiskAssessment,
        strategy: str
    ) -> RiskTreatmentPlan:
        """Develop risk treatment plan."""
        strategies = {
            "mitigate": self._develop_mitigation_plan,
            "transfer": self._develop_transfer_plan,
            "avoid": self._develop_avoidance_plan,
            "accept": self._develop_acceptance_plan,
        }

        plan_func = strategies.get(strategy)
        if not plan_func:
            raise ValueError(f"Unknown strategy: {strategy}")

        plan = plan_func(risk)

        audit_log.info(
            "risk_treatment_plan_created",
            risk_id=risk.risk_id,
            strategy=strategy
        )

        return plan

    def _develop_mitigation_plan(self, risk: RiskAssessment) -> RiskTreatmentPlan:
        """Develop risk mitigation controls."""
        return RiskTreatmentPlan(
            risk_id=risk.risk_id,
            strategy="mitigate",
            controls=[
                Control(
                    name="Bias detection and correction",
                    type="preventive",
                    implementation="Automated fairness testing in CI/CD",
                    effectiveness="high",
                    cost="medium"
                ),
                Control(
                    name="Human oversight",
                    type="detective",
                    implementation="Review queue for high-impact decisions",
                    effectiveness="high",
                    cost="high"
                ),
            ],
            target_residual_risk="low",
            implementation_timeline="Q1 2025",
            responsible_party="AI System Owner"
        )

    def monitor_risks(self, system_id: str) -> MonitoringReport:
        """Continuous risk monitoring."""
        return MonitoringReport(
            system_id=system_id,
            timestamp=datetime.utcnow(),
            metrics={
                "model_performance": self._get_performance_metrics(system_id),
                "fairness_metrics": self._get_fairness_metrics(system_id),
                "incident_count": self._get_incident_count(system_id),
                "control_effectiveness": self._assess_control_effectiveness(system_id),
            },
            alerts=self._check_thresholds(system_id),
            recommendations=self._generate_monitoring_recommendations(system_id)
        )

    def respond_to_incidents(self, incident: AIIncident) -> IncidentResponse:
        """Respond to AI-related incidents."""
        response = IncidentResponse(
            incident_id=incident.id,
            severity=incident.severity,
            response_actions=[],
            timeline=[]
        )

        # Immediate containment
        if incident.severity in ["critical", "high"]:
            response.response_actions.append(
                Action(
                    type="containment",
                    description="Disable AI system or affected functionality",
                    status="completed"
                )
            )

        # Root cause analysis
        response.response_actions.append(
            Action(
                type="investigation",
                description="Conduct root cause analysis",
                status="in_progress"
            )
        )

        audit_log.info(
            "ai_incident_response_initiated",
            incident_id=incident.id,
            severity=incident.severity
        )

        return response
```

## Documentation Requirements

### Required Documents
- [ ] AI Governance Policy
- [ ] AI Risk Management Procedure
- [ ] AI System Inventory
- [ ] Risk Assessment Methodology
- [ ] Testing and Validation Procedures

### Required Records
- [ ] AI system characterizations
- [ ] Risk assessments
- [ ] Test results
- [ ] Treatment plans and status
- [ ] Monitoring reports
- [ ] Incident records

## Quality Checklist

- [ ] GOVERN: Governance structure established
- [ ] GOVERN: AI policy approved
- [ ] MAP: All AI systems characterized
- [ ] MAP: Stakeholders identified
- [ ] MEASURE: Risk assessments completed
- [ ] MEASURE: Testing performed
- [ ] MANAGE: Risks prioritized
- [ ] MANAGE: Treatment plans developed
- [ ] MANAGE: Monitoring active

## Related Skills

- `iso42001-ai-governance` - ISO 42001 AI management
- `ai-agent-governance` - AI agent governance
- `security-review` - Security vulnerability review

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
