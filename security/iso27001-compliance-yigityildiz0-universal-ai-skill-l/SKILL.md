---
name: iso27001-compliance
description: Implement ISO 27001:2022 Information Security Management System controls (114 controls across 14 domains). Use when establishing ISMS, preparing for ISO.
---

# ISO 27001:2022 Compliance

Implement ISO 27001:2022 Information Security Management System (ISMS) with comprehensive controls for global security compliance.

## When to Use This Skill

Use this skill when you need to:

- Establish an ISMS
- Prepare for ISO 27001 certification
- Implement security controls
- Document security policies
- Achieve global compliance
- Meet enterprise customer requirements

**Trigger phrases**: "ISO 27001", "ISMS", "information security", "ISO certification", "security management", "Annex A controls"

## What This Skill Does

### ISO 27001:2022 Structure

| Clause | Focus | Key Requirements |
|--------|-------|------------------|
| 4 | Context | Scope, interested parties |
| 5 | Leadership | Policy, roles, responsibilities |
| 6 | Planning | Risk assessment, objectives |
| 7 | Support | Resources, competence, awareness |
| 8 | Operation | Risk treatment, controls |
| 9 | Performance | Monitoring, audit, review |
| 10 | Improvement | Nonconformity, continual improvement |

### Annex A Control Domains (2022)

1. Organizational controls (37 controls)
2. People controls (8 controls)
3. Physical controls (14 controls)
4. Technological controls (34 controls)

## Instructions

### Step 1: ISMS Scope Definition (Clause 4)

```python
class ISMSScope:
    """Define the ISMS scope per ISO 27001 Clause 4."""

    def __init__(self):
        self.organization = {
            "name": "Organization Name",
            "industry": "Software as a Service",
            "locations": ["Headquarters", "Data Center"],
        }

        self.scope = {
            "systems": [
                "Production infrastructure",
                "Customer data processing",
                "Internal IT systems",
            ],
            "processes": [
                "Software development",
                "Customer support",
                "Data management",
            ],
            "exclusions": [
                "Physical manufacturing (not applicable)",
            ],
        }

        self.interested_parties = [
            {"party": "Customers", "requirements": ["Data protection", "Availability"]},
            {"party": "Regulators", "requirements": ["GDPR", "Industry standards"]},
            {"party": "Employees", "requirements": ["Privacy", "Clear policies"]},
        ]

    def document_scope(self) -> str:
        """Generate ISMS scope statement."""
        return f"""
        ISMS Scope Statement

        Organization: {self.organization['name']}
        Industry: {self.organization['industry']}

        In Scope:
        - Systems: {', '.join(self.scope['systems'])}
        - Processes: {', '.join(self.scope['processes'])}

        Exclusions:
        - {', '.join(self.scope['exclusions'])}

        Applicable Standards: ISO 27001:2022
        """
```

### Step 2: Risk Assessment (Clause 6)

```python
from enum import Enum
from dataclasses import dataclass

class Likelihood(Enum):
    RARE = 1
    UNLIKELY = 2
    POSSIBLE = 3
    LIKELY = 4
    ALMOST_CERTAIN = 5

class Impact(Enum):
    NEGLIGIBLE = 1
    MINOR = 2
    MODERATE = 3
    MAJOR = 4
    SEVERE = 5

@dataclass
class Risk:
    """Information security risk per ISO 27001."""
    id: str
    asset: str
    threat: str
    vulnerability: str
    likelihood: Likelihood
    impact: Impact
    existing_controls: list[str]
    risk_owner: str

    @property
    def risk_score(self) -> int:
        return self.likelihood.value * self.impact.value

    @property
    def risk_level(self) -> str:
        score = self.risk_score
        if score <= 5:
            return "LOW"
        elif score <= 12:
            return "MEDIUM"
        elif score <= 19:
            return "HIGH"
        return "CRITICAL"

class RiskAssessment:
    """ISO 27001 compliant risk assessment."""

    def __init__(self):
        self.risks: list[Risk] = []
        self.risk_criteria = {
            "acceptable_threshold": 8,
            "review_period_days": 365,
        }

    def assess_risk(self, asset: str, threat: str, vulnerability: str) -> Risk:
        """Assess individual risk."""
        risk = Risk(
            id=f"RISK-{len(self.risks) + 1:04d}",
            asset=asset,
            threat=threat,
            vulnerability=vulnerability,
            likelihood=self._assess_likelihood(threat),
            impact=self._assess_impact(asset),
            existing_controls=self._identify_controls(vulnerability),
            risk_owner=self._assign_owner(asset)
        )

        self.risks.append(risk)

        audit_log.info(
            "risk_assessed",
            risk_id=risk.id,
            score=risk.risk_score,
            level=risk.risk_level
        )

        return risk

    def generate_risk_register(self) -> dict:
        """Generate risk register for ISMS documentation."""
        return {
            "generated_at": datetime.utcnow().isoformat(),
            "total_risks": len(self.risks),
            "by_level": self._count_by_level(),
            "risks": [self._risk_to_dict(r) for r in self.risks],
            "treatment_required": [
                r for r in self.risks
                if r.risk_score > self.risk_criteria["acceptable_threshold"]
            ]
        }
```

### Step 3: Annex A Controls Implementation

#### A.5 - Organizational Controls

```python
class OrganizationalControls:
    """ISO 27001:2022 Annex A.5 - Organizational Controls."""

    # A.5.1 - Policies for information security
    def create_security_policy(self) -> SecurityPolicy:
        """Create information security policy."""
        return SecurityPolicy(
            version="1.0",
            effective_date=datetime.utcnow(),
            approved_by="CISO",
            sections=[
                "Purpose and Scope",
                "Information Security Objectives",
                "Roles and Responsibilities",
                "Policy Compliance",
                "Review and Update",
            ]
        )

    # A.5.15 - Access control
    def implement_access_control(self) -> AccessControlPolicy:
        """Implement access control policy."""
        return AccessControlPolicy(
            principles=[
                "Need-to-know basis",
                "Least privilege",
                "Separation of duties",
            ],
            authentication_requirements={
                "password_min_length": 12,
                "mfa_required": True,
                "session_timeout_minutes": 30,
            },
            authorization_model="RBAC",
        )

    # A.5.23 - Information security for cloud services
    def cloud_security_controls(self) -> CloudSecurityPolicy:
        """Define cloud security controls."""
        return CloudSecurityPolicy(
            providers=["AWS", "Azure", "GCP"],
            requirements=[
                "Data residency compliance",
                "Encryption at rest and in transit",
                "Access logging and monitoring",
                "Incident response integration",
            ],
            shared_responsibility_documented=True,
        )
```

#### A.6 - People Controls

```python
class PeopleControls:
    """ISO 27001:2022 Annex A.6 - People Controls."""

    # A.6.1 - Screening
    def background_screening(self, role: str) -> ScreeningRequirements:
        """Define screening requirements by role."""
        base_requirements = [
            "Identity verification",
            "Reference checks",
            "Right to work verification",
        ]

        role_specific = {
            "admin": ["Criminal background check", "Credit check"],
            "developer": ["Criminal background check"],
            "support": ["Criminal background check"],
        }

        return ScreeningRequirements(
            role=role,
            checks=base_requirements + role_specific.get(role, [])
        )

    # A.6.3 - Information security awareness
    def security_awareness_program(self) -> AwarenessProgram:
        """Define security awareness program."""
        return AwarenessProgram(
            frequency="annual",
            topics=[
                "Information security policy",
                "Password security",
                "Phishing awareness",
                "Data classification",
                "Incident reporting",
                "Clean desk policy",
            ],
            assessment_required=True,
            pass_threshold=80,
        )
```

#### A.8 - Technological Controls

```python
class TechnologicalControls:
    """ISO 27001:2022 Annex A.8 - Technological Controls."""

    # A.8.1 - User endpoint devices
    def endpoint_security(self) -> EndpointPolicy:
        """Define endpoint security requirements."""
        return EndpointPolicy(
            requirements=[
                "Full disk encryption",
                "Anti-malware software",
                "Automatic updates enabled",
                "Screen lock after 5 minutes",
                "USB storage disabled",
            ],
            mobile_device_management=True,
            remote_wipe_capability=True,
        )

    # A.8.9 - Configuration management
    def configuration_management(self) -> ConfigurationPolicy:
        """Implement configuration management."""
        return ConfigurationPolicy(
            baselines={
                "servers": "CIS Benchmark Level 1",
                "workstations": "CIS Benchmark Level 1",
                "network": "CIS Benchmark",
            },
            hardening_required=True,
            drift_detection=True,
            change_approval_required=True,
        )

    # A.8.24 - Use of cryptography
    def cryptography_policy(self) -> CryptographyPolicy:
        """Define cryptographic controls."""
        return CryptographyPolicy(
            algorithms={
                "symmetric": "AES-256",
                "asymmetric": "RSA-2048 or ECDSA-256",
                "hashing": "SHA-256 or SHA-3",
            },
            key_management={
                "generation": "HSM or approved key vault",
                "storage": "Hardware security module",
                "rotation_period_days": 365,
                "destruction": "Secure key zeroization",
            },
            tls_minimum_version="1.2",
        )

    # A.8.15 - Logging
    def logging_requirements(self) -> LoggingPolicy:
        """Define logging and monitoring requirements."""
        return LoggingPolicy(
            events_to_log=[
                "Authentication attempts",
                "Authorization failures",
                "System administrator actions",
                "Data access and modifications",
                "Security events",
                "Configuration changes",
            ],
            retention_days=365,
            protection="Immutable storage with integrity verification",
            review_frequency="Weekly automated, monthly manual",
        )
```

### Step 4: Statement of Applicability (SoA)

```python
class StatementOfApplicability:
    """Generate ISO 27001 Statement of Applicability."""

    def __init__(self):
        self.controls = self._load_annex_a_controls()

    def generate_soa(self) -> dict:
        """Generate complete Statement of Applicability."""
        soa = {
            "version": "1.0",
            "date": datetime.utcnow().isoformat(),
            "approved_by": "Information Security Manager",
            "controls": []
        }

        for control in self.controls:
            soa["controls"].append({
                "id": control.id,
                "name": control.name,
                "applicable": control.is_applicable,
                "justification": control.justification,
                "implementation_status": control.status,
                "evidence_reference": control.evidence_ref,
            })

        return soa

    def export_soa_document(self) -> str:
        """Export SoA as formatted document."""
        soa = self.generate_soa()
        return f"""
        Statement of Applicability
        ISO 27001:2022

        Version: {soa['version']}
        Date: {soa['date']}
        Approved By: {soa['approved_by']}

        Control Implementation Summary:
        - Total Controls: {len(soa['controls'])}
        - Applicable: {sum(1 for c in soa['controls'] if c['applicable'])}
        - Implemented: {sum(1 for c in soa['controls'] if c['implementation_status'] == 'implemented')}
        - Planned: {sum(1 for c in soa['controls'] if c['implementation_status'] == 'planned')}
        """
```

### Step 5: Internal Audit (Clause 9)

```python
class InternalAudit:
    """ISO 27001 internal audit process."""

    def plan_audit(self, scope: list[str]) -> AuditPlan:
        """Create internal audit plan."""
        return AuditPlan(
            audit_id=f"AUDIT-{datetime.utcnow().year}-{uuid.uuid4().hex[:6]}",
            scope=scope,
            objectives=[
                "Verify ISMS conformity to ISO 27001:2022",
                "Evaluate effectiveness of controls",
                "Identify improvement opportunities",
            ],
            schedule=self._generate_schedule(scope),
            auditors=self._assign_auditors(scope),
            criteria=["ISO 27001:2022", "Internal policies"],
        )

    def conduct_audit(self, plan: AuditPlan) -> AuditFindings:
        """Document audit findings."""
        findings = AuditFindings(
            audit_id=plan.audit_id,
            findings=[],
            observations=[],
            opportunities_for_improvement=[],
        )

        # Audit each area in scope
        for area in plan.scope:
            area_findings = self._audit_area(area)
            findings.findings.extend(area_findings.nonconformities)
            findings.observations.extend(area_findings.observations)
            findings.opportunities_for_improvement.extend(area_findings.ofis)

        return findings

    def generate_audit_report(self, findings: AuditFindings) -> AuditReport:
        """Generate formal audit report."""
        return AuditReport(
            audit_id=findings.audit_id,
            executive_summary=self._create_summary(findings),
            detailed_findings=findings.findings,
            recommendations=self._generate_recommendations(findings),
            conclusion=self._determine_conclusion(findings),
        )
```

## Documentation Requirements

### Required ISMS Documents

- [ ] Information Security Policy
- [ ] Scope of the ISMS
- [ ] Risk Assessment Methodology
- [ ] Risk Treatment Plan
- [ ] Statement of Applicability
- [ ] Information Security Objectives
- [ ] Roles and Responsibilities

### Required Records

- [ ] Risk assessment results
- [ ] Risk treatment results
- [ ] Competence evidence
- [ ] Monitoring and measurement results
- [ ] Internal audit program and results
- [ ] Management review results
- [ ] Nonconformities and corrective actions

## Quality Checklist

- [ ] ISMS scope defined and documented
- [ ] Risk assessment completed
- [ ] All Annex A controls evaluated
- [ ] Statement of Applicability complete
- [ ] Required procedures documented
- [ ] Internal audit conducted
- [ ] Management review performed
- [ ] Continual improvement process established

## Related Skills

- `soc2-compliance` - SOC 2 implementation
- `iso42001-ai-governance` - AI management systems
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
