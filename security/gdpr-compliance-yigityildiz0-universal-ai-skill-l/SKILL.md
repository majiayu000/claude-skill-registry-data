---
name: gdpr-compliance
description: Implement GDPR requirements for EU data protection including data subject rights, consent management, and breach notification. Use when handling EU personal.
---

# GDPR Compliance

Implement EU General Data Protection Regulation requirements for comprehensive data protection and privacy.

## When to Use This Skill

Use this skill when you need to:

- Handle EU personal data
- Implement data subject rights
- Manage consent
- Conduct DPIAs
- Handle data breaches
- Document lawful processing

**Trigger phrases**: "GDPR compliance", "data protection", "EU privacy", "data subject rights", "DPIA", "consent management", "right to be forgotten"

## What This Skill Does

### GDPR Principles (Article 5)

| Principle | Requirement |
|-----------|-------------|
| Lawfulness | Valid legal basis for processing |
| Purpose limitation | Process only for specified purposes |
| Data minimization | Collect only what's necessary |
| Accuracy | Keep data accurate and up to date |
| Storage limitation | Don't retain longer than necessary |
| Integrity | Ensure security of personal data |
| Accountability | Demonstrate compliance |

## Instructions

### Step 1: Data Subject Rights Implementation

```python
from enum import Enum
from dataclasses import dataclass
from datetime import datetime, timedelta

class DataSubjectRightType(Enum):
    ACCESS = "access"  # Article 15
    RECTIFICATION = "rectification"  # Article 16
    ERASURE = "erasure"  # Article 17 (Right to be forgotten)
    RESTRICT = "restrict"  # Article 18
    PORTABILITY = "portability"  # Article 20
    OBJECT = "object"  # Article 21

@dataclass
class DataSubjectRequest:
    """GDPR Data Subject Request."""
    request_id: str
    subject_id: str
    right_type: DataSubjectRightType
    submitted_at: datetime
    verified: bool
    status: str
    due_date: datetime

class DataSubjectRightsService:
    """Handle GDPR data subject rights requests."""

    RESPONSE_DEADLINE_DAYS = 30  # Can extend to 90 for complex requests

    def submit_request(
        self,
        subject_email: str,
        right_type: DataSubjectRightType,
        details: dict
    ) -> DataSubjectRequest:
        """Submit new data subject request."""
        request = DataSubjectRequest(
            request_id=f"DSR-{uuid.uuid4().hex[:8]}",
            subject_id=self._identify_subject(subject_email),
            right_type=right_type,
            submitted_at=datetime.utcnow(),
            verified=False,
            status="pending_verification",
            due_date=datetime.utcnow() + timedelta(days=self.RESPONSE_DEADLINE_DAYS)
        )

        # Store request
        self.request_repository.save(request)

        # Send verification email
        self._send_verification(subject_email, request)

        audit_log.info(
            "dsr_submitted",
            request_id=request.request_id,
            right_type=right_type.value
        )

        return request

    def process_access_request(self, request: DataSubjectRequest) -> AccessResponse:
        """Process Article 15 - Right of Access."""
        subject_data = self._collect_all_data(request.subject_id)

        response = AccessResponse(
            request_id=request.request_id,
            data_categories=self._categorize_data(subject_data),
            purposes=self._get_processing_purposes(request.subject_id),
            recipients=self._get_data_recipients(request.subject_id),
            retention_periods=self._get_retention_periods(),
            source=self._get_data_sources(request.subject_id),
            automated_decisions=self._get_automated_decisions(request.subject_id),
            safeguards=self._get_transfer_safeguards(),
            data_export=self._export_data(subject_data, format="json")
        )

        audit_log.info(
            "dsr_access_processed",
            request_id=request.request_id
        )

        return response

    def process_erasure_request(self, request: DataSubjectRequest) -> ErasureResponse:
        """Process Article 17 - Right to Erasure (Right to be Forgotten)."""
        # Check if erasure can be refused
        exemptions = self._check_erasure_exemptions(request.subject_id)
        if exemptions:
            return ErasureResponse(
                request_id=request.request_id,
                status="refused",
                reason=exemptions,
                retained_data=self._get_retained_data(request.subject_id)
            )

        # Perform erasure
        systems_affected = self._identify_affected_systems(request.subject_id)
        erasure_results = []

        for system in systems_affected:
            result = self._erase_from_system(request.subject_id, system)
            erasure_results.append(result)

        # Notify recipients
        recipients = self._get_data_recipients(request.subject_id)
        self._notify_recipients_of_erasure(recipients, request.subject_id)

        audit_log.info(
            "dsr_erasure_processed",
            request_id=request.request_id,
            systems_affected=len(systems_affected)
        )

        return ErasureResponse(
            request_id=request.request_id,
            status="completed",
            systems_affected=systems_affected,
            results=erasure_results
        )

    def process_portability_request(self, request: DataSubjectRequest) -> PortabilityResponse:
        """Process Article 20 - Right to Data Portability."""
        # Only data provided by subject and processed by consent/contract
        portable_data = self._get_portable_data(request.subject_id)

        # Export in structured, machine-readable format
        export = self._export_data(
            portable_data,
            format="json",
            structured=True
        )

        return PortabilityResponse(
            request_id=request.request_id,
            data_format="application/json",
            data_export=export,
            download_link=self._generate_secure_download(export)
        )
```

### Step 2: Consent Management

```python
class ConsentPurpose(Enum):
    MARKETING = "marketing"
    ANALYTICS = "analytics"
    PERSONALIZATION = "personalization"
    THIRD_PARTY_SHARING = "third_party_sharing"
    PROFILING = "profiling"

@dataclass
class Consent:
    """GDPR-compliant consent record."""
    consent_id: str
    subject_id: str
    purpose: ConsentPurpose
    granted: bool
    timestamp: datetime
    method: str  # how consent was collected
    version: str  # privacy policy version
    withdrawal_timestamp: Optional[datetime]

class ConsentManagementService:
    """GDPR Article 7 - Conditions for Consent."""

    def collect_consent(
        self,
        subject_id: str,
        purpose: ConsentPurpose,
        method: str
    ) -> Consent:
        """Record explicit, informed consent."""
        consent = Consent(
            consent_id=f"CONSENT-{uuid.uuid4().hex[:8]}",
            subject_id=subject_id,
            purpose=purpose,
            granted=True,
            timestamp=datetime.utcnow(),
            method=method,  # e.g., "checkbox", "double_opt_in"
            version=self._get_current_policy_version(),
            withdrawal_timestamp=None
        )

        self.consent_repository.save(consent)

        audit_log.info(
            "consent_collected",
            consent_id=consent.consent_id,
            purpose=purpose.value,
            method=method
        )

        return consent

    def withdraw_consent(
        self,
        subject_id: str,
        purpose: ConsentPurpose
    ) -> Consent:
        """Process consent withdrawal."""
        consent = self.consent_repository.find_active(subject_id, purpose)

        if not consent:
            raise ConsentNotFoundError(f"No active consent for {purpose.value}")

        consent.granted = False
        consent.withdrawal_timestamp = datetime.utcnow()
        self.consent_repository.save(consent)

        # Stop processing for this purpose
        self._stop_processing(subject_id, purpose)

        audit_log.info(
            "consent_withdrawn",
            consent_id=consent.consent_id,
            purpose=purpose.value
        )

        return consent

    def check_consent(
        self,
        subject_id: str,
        purpose: ConsentPurpose
    ) -> bool:
        """Check if valid consent exists for purpose."""
        consent = self.consent_repository.find_active(subject_id, purpose)

        if not consent:
            return False

        # Check if policy has been updated since consent
        if consent.version != self._get_current_policy_version():
            # May need to re-consent
            return False

        return consent.granted
```

### Step 3: Data Protection Impact Assessment (DPIA)

```python
class DPIAService:
    """GDPR Article 35 - Data Protection Impact Assessment."""

    def is_dpia_required(self, processing_activity: ProcessingActivity) -> bool:
        """Determine if DPIA is required."""
        # Article 35(3) - DPIA required for:
        triggers = [
            processing_activity.involves_profiling,
            processing_activity.involves_automated_decisions,
            processing_activity.large_scale_special_category,
            processing_activity.systematic_monitoring,
            processing_activity.new_technology,
            processing_activity.cross_border_transfer,
        ]

        return any(triggers)

    def conduct_dpia(
        self,
        processing_activity: ProcessingActivity
    ) -> DPIAReport:
        """Conduct Data Protection Impact Assessment."""
        dpia = DPIAReport(
            dpia_id=f"DPIA-{uuid.uuid4().hex[:8]}",
            processing_activity=processing_activity.name,
            date=datetime.utcnow(),
            sections=[]
        )

        # Section 1: Description of processing
        dpia.sections.append(DPIASection(
            name="Processing Description",
            content={
                "purpose": processing_activity.purpose,
                "data_categories": processing_activity.data_categories,
                "data_subjects": processing_activity.data_subjects,
                "recipients": processing_activity.recipients,
                "retention": processing_activity.retention_period,
                "technology": processing_activity.technology_used
            }
        ))

        # Section 2: Necessity and proportionality
        dpia.sections.append(DPIASection(
            name="Necessity Assessment",
            content={
                "legal_basis": processing_activity.legal_basis,
                "necessity_justification": self._assess_necessity(processing_activity),
                "proportionality": self._assess_proportionality(processing_activity),
                "data_minimization": self._assess_minimization(processing_activity)
            }
        ))

        # Section 3: Risk assessment
        risks = self._identify_risks(processing_activity)
        dpia.sections.append(DPIASection(
            name="Risk Assessment",
            content={
                "risks": [self._assess_risk(r) for r in risks],
                "overall_risk_level": self._calculate_overall_risk(risks)
            }
        ))

        # Section 4: Mitigation measures
        dpia.sections.append(DPIASection(
            name="Mitigation Measures",
            content={
                "measures": self._identify_mitigations(risks),
                "residual_risks": self._calculate_residual_risks(risks)
            }
        ))

        audit_log.info(
            "dpia_completed",
            dpia_id=dpia.dpia_id,
            processing_activity=processing_activity.name
        )

        return dpia
```

### Step 4: Breach Notification

```python
class BreachNotificationService:
    """GDPR Article 33-34 - Breach Notification."""

    AUTHORITY_NOTIFICATION_HOURS = 72  # Within 72 hours

    def report_breach(self, breach_details: dict) -> BreachRecord:
        """Record and assess personal data breach."""
        breach = BreachRecord(
            breach_id=f"BREACH-{uuid.uuid4().hex[:8]}",
            discovered_at=datetime.utcnow(),
            description=breach_details["description"],
            data_categories=breach_details["data_categories"],
            subjects_affected=breach_details["subjects_affected"],
            cause=breach_details["cause"],
            status="under_investigation"
        )

        # Assess risk to individuals
        risk_assessment = self._assess_breach_risk(breach)
        breach.risk_level = risk_assessment.level

        self.breach_repository.save(breach)

        audit_log.critical(
            "data_breach_reported",
            breach_id=breach.breach_id,
            subjects_affected=breach.subjects_affected
        )

        return breach

    def notify_authority(self, breach: BreachRecord) -> AuthorityNotification:
        """Notify supervisory authority within 72 hours."""
        notification = AuthorityNotification(
            breach_id=breach.breach_id,
            submitted_at=datetime.utcnow(),
            content={
                "nature_of_breach": breach.description,
                "categories_of_data": breach.data_categories,
                "approximate_subjects": breach.subjects_affected,
                "dpo_contact": self._get_dpo_contact(),
                "likely_consequences": self._assess_consequences(breach),
                "measures_taken": self._get_remediation_measures(breach),
                "measures_proposed": self._get_proposed_measures(breach)
            }
        )

        # Submit to authority
        self._submit_to_authority(notification)

        audit_log.info(
            "authority_notified",
            breach_id=breach.breach_id,
            notification_time=notification.submitted_at.isoformat()
        )

        return notification

    def notify_subjects(self, breach: BreachRecord) -> SubjectNotification:
        """Notify affected data subjects if high risk."""
        # Article 34 - Only required if high risk to rights and freedoms
        if breach.risk_level != "high":
            return None

        notification = SubjectNotification(
            breach_id=breach.breach_id,
            content={
                "plain_language_description": self._create_plain_description(breach),
                "dpo_contact": self._get_dpo_contact(),
                "likely_consequences": self._describe_consequences(breach),
                "measures_taken": self._describe_remediation(breach),
                "recommended_actions": self._get_subject_recommendations(breach)
            }
        )

        # Send to affected subjects
        self._send_notifications(breach.affected_subjects, notification)

        audit_log.info(
            "subjects_notified",
            breach_id=breach.breach_id,
            subjects_notified=len(breach.affected_subjects)
        )

        return notification
```

### Step 5: Records of Processing Activities

```python
class ProcessingActivityRecord:
    """GDPR Article 30 - Records of Processing Activities."""

    def create_ropa(self) -> ROPA:
        """Create Records of Processing Activities."""
        return ROPA(
            organization=self._get_organization_details(),
            dpo_contact=self._get_dpo_contact(),
            activities=[
                self._document_activity(a) for a in self._get_all_activities()
            ]
        )

    def _document_activity(self, activity: ProcessingActivity) -> dict:
        """Document individual processing activity."""
        return {
            "name": activity.name,
            "controller": self._get_controller_details(),
            "purposes": activity.purposes,
            "legal_basis": activity.legal_basis,
            "data_categories": activity.data_categories,
            "data_subjects": activity.data_subject_categories,
            "recipients": activity.recipients,
            "third_country_transfers": activity.transfers,
            "safeguards": activity.transfer_safeguards,
            "retention_period": activity.retention,
            "security_measures": activity.security_measures,
        }
```

## Documentation Requirements

### Required Documents
- [ ] Privacy Policy
- [ ] Records of Processing Activities (ROPA)
- [ ] Data Processing Agreements
- [ ] DPIA reports (where required)
- [ ] Consent records
- [ ] Breach response procedures

### Required Records
- [ ] Data subject requests and responses
- [ ] Consent records
- [ ] Processing activity records
- [ ] Breach notifications
- [ ] DPIA assessments

## Quality Checklist

- [ ] Lawful basis documented for all processing
- [ ] Privacy notices published
- [ ] Consent mechanisms implemented
- [ ] Data subject rights procedures in place
- [ ] DPIA process established
- [ ] Breach notification procedures ready
- [ ] ROPA maintained
- [ ] DPO appointed (if required)
- [ ] Training completed

## Related Skills

- `ccpa-compliance` - California privacy compliance
- `soc2-compliance` - SOC 2 privacy criteria
- `security-review` - Security controls

---

**Version**: 1.0.0
**Last Updated**: December 2025
**Based on**: AI Templates compliance_governance/privacy_protection/


### Iterative Refinement Strategy
This skill is optimized for an iterative approach:
1. **Execute**: Perform the core steps defined above.
2. **Review**: Critically analyze the output (coverage, quality, completeness).
3. **Refine**: If targets aren't met, repeat the specific implementation steps with improved context.
4. **Loop**: Continue until the definition of done is satisfied.
