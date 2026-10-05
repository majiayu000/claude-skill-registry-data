---
name: ccpa-compliance
description: Implement CCPA/CPRA requirements for California consumer privacy including opt-out rights and data disclosure. Use when handling California resident data.
---

# CCPA/CPRA Compliance

Implement California Consumer Privacy Act (CCPA) and California Privacy Rights Act (CPRA) requirements for consumer privacy protection.

## When to Use This Skill

Use this skill when you need to:

- Handle California resident data
- Implement opt-out rights
- Process consumer data requests
- Disclose data practices
- Meet privacy compliance requirements
- Document data sales/sharing

**Trigger phrases**: "CCPA compliance", "CPRA", "California privacy", "do not sell", "opt-out", "consumer rights", "data disclosure"

## What This Skill Does

### CCPA/CPRA Consumer Rights

| Right | Description |
|-------|-------------|
| Right to Know | What personal information is collected |
| Right to Delete | Request deletion of personal information |
| Right to Opt-Out | Opt out of sale/sharing of data |
| Right to Correct | Correct inaccurate personal information |
| Right to Limit | Limit use of sensitive personal information |
| Non-Discrimination | No discrimination for exercising rights |

## Instructions

### Step 1: Privacy Disclosure Requirements

```python
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class PrivacyDisclosure:
    """CCPA required privacy disclosures."""
    categories_collected: List[str]
    purposes: List[str]
    categories_sold: List[str]
    categories_shared: List[str]
    retention_periods: dict
    third_parties: List[str]

class PrivacyNoticeService:
    """Generate CCPA-compliant privacy notices."""

    CCPA_CATEGORIES = [
        "Identifiers",
        "Customer records",
        "Protected classifications",
        "Commercial information",
        "Biometric information",
        "Internet activity",
        "Geolocation data",
        "Audio/visual information",
        "Professional information",
        "Education information",
        "Inferences"
    ]

    def generate_privacy_notice(self) -> PrivacyDisclosure:
        """Generate required privacy notice content."""
        return PrivacyDisclosure(
            categories_collected=self._get_collected_categories(),
            purposes=self._get_collection_purposes(),
            categories_sold=self._get_sold_categories(),
            categories_shared=self._get_shared_categories(),
            retention_periods=self._get_retention_by_category(),
            third_parties=self._get_third_parties()
        )

    def generate_at_collection_notice(self, context: str) -> dict:
        """Generate notice at point of collection."""
        return {
            "categories": self._get_categories_for_context(context),
            "purposes": self._get_purposes_for_context(context),
            "sensitive_data_notice": self._check_sensitive_data(context),
            "sale_sharing_notice": self._get_sale_sharing_notice(),
            "retention_notice": self._get_retention_notice(context),
            "links": {
                "privacy_policy": "/privacy",
                "do_not_sell": "/do-not-sell",
                "limit_use": "/limit-use"
            }
        }
```

### Step 2: Consumer Request Handling

```python
from enum import Enum
from datetime import datetime, timedelta

class CCPARequestType(Enum):
    KNOW = "know"  # Right to know
    DELETE = "delete"  # Right to delete
    CORRECT = "correct"  # Right to correct
    OPT_OUT_SALE = "opt_out_sale"  # Opt out of sale
    OPT_OUT_SHARE = "opt_out_share"  # Opt out of sharing
    LIMIT_SENSITIVE = "limit_sensitive"  # Limit sensitive data use

class ConsumerRequestService:
    """Handle CCPA consumer requests."""

    RESPONSE_DEADLINE_DAYS = 45  # Can extend once by 45 days
    VERIFICATION_REQUIRED = True

    def submit_request(
        self,
        consumer_email: str,
        request_type: CCPARequestType,
        details: Optional[dict] = None
    ) -> ConsumerRequest:
        """Submit new consumer request."""
        request = ConsumerRequest(
            request_id=f"CCPA-{uuid.uuid4().hex[:8]}",
            consumer_id=self._identify_consumer(consumer_email),
            request_type=request_type,
            submitted_at=datetime.utcnow(),
            verified=False,
            status="pending_verification",
            due_date=datetime.utcnow() + timedelta(days=self.RESPONSE_DEADLINE_DAYS)
        )

        self.request_repository.save(request)

        # Send verification
        self._send_verification(consumer_email, request)

        audit_log.info(
            "ccpa_request_submitted",
            request_id=request.request_id,
            request_type=request_type.value
        )

        return request

    def process_know_request(self, request: ConsumerRequest) -> KnowResponse:
        """Process Right to Know request."""
        consumer_data = self._collect_consumer_data(request.consumer_id)

        response = KnowResponse(
            request_id=request.request_id,
            categories_collected=[
                {
                    "category": cat,
                    "sources": self._get_sources(cat),
                    "purposes": self._get_purposes(cat),
                    "third_parties": self._get_third_parties(cat),
                    "sold_to": self._get_sold_to(cat),
                    "shared_with": self._get_shared_with(cat)
                }
                for cat in self._categorize_data(consumer_data)
            ],
            specific_pieces=consumer_data if request.include_specific else None,
            retention_periods=self._get_retention_periods()
        )

        audit_log.info(
            "ccpa_know_processed",
            request_id=request.request_id
        )

        return response

    def process_delete_request(self, request: ConsumerRequest) -> DeleteResponse:
        """Process Right to Delete request."""
        # Check for exemptions
        exemptions = self._check_delete_exemptions(request.consumer_id)

        if exemptions:
            return DeleteResponse(
                request_id=request.request_id,
                status="partially_completed",
                deleted_categories=self._get_deletable_categories(request.consumer_id),
                retained_categories=exemptions,
                exemption_reasons=self._get_exemption_reasons(exemptions)
            )

        # Perform deletion
        deletion_results = self._delete_consumer_data(request.consumer_id)

        # Notify service providers
        self._notify_service_providers(request.consumer_id, "delete")

        return DeleteResponse(
            request_id=request.request_id,
            status="completed",
            deleted_categories=deletion_results.categories,
            deletion_confirmation=deletion_results.confirmation
        )

    def process_correct_request(
        self,
        request: ConsumerRequest,
        corrections: dict
    ) -> CorrectResponse:
        """Process Right to Correct request."""
        # Verify corrections are valid
        validation = self._validate_corrections(request.consumer_id, corrections)

        if not validation.valid:
            return CorrectResponse(
                request_id=request.request_id,
                status="rejected",
                reason=validation.reason
            )

        # Apply corrections
        correction_results = self._apply_corrections(request.consumer_id, corrections)

        # Notify service providers
        self._notify_service_providers(request.consumer_id, "correct", corrections)

        return CorrectResponse(
            request_id=request.request_id,
            status="completed",
            corrected_fields=correction_results.fields
        )
```

### Step 3: Opt-Out Mechanisms

```python
class OptOutService:
    """Handle CCPA opt-out requests."""

    def process_opt_out_sale(self, consumer_id: str) -> OptOutResult:
        """Process opt-out of sale of personal information."""
        # Record opt-out preference
        preference = OptOutPreference(
            consumer_id=consumer_id,
            type="sale",
            opted_out=True,
            timestamp=datetime.utcnow()
        )

        self.preference_repository.save(preference)

        # Stop selling data
        self._stop_selling(consumer_id)

        # Notify third parties
        self._notify_third_parties_stop_sale(consumer_id)

        audit_log.info(
            "ccpa_opt_out_sale",
            consumer_id=consumer_id
        )

        return OptOutResult(
            consumer_id=consumer_id,
            type="sale",
            effective_date=datetime.utcnow()
        )

    def process_opt_out_share(self, consumer_id: str) -> OptOutResult:
        """Process opt-out of sharing for cross-context behavioral advertising."""
        preference = OptOutPreference(
            consumer_id=consumer_id,
            type="share",
            opted_out=True,
            timestamp=datetime.utcnow()
        )

        self.preference_repository.save(preference)

        # Stop sharing data
        self._stop_sharing(consumer_id)

        audit_log.info(
            "ccpa_opt_out_share",
            consumer_id=consumer_id
        )

        return OptOutResult(
            consumer_id=consumer_id,
            type="share",
            effective_date=datetime.utcnow()
        )

    def process_gpc_signal(self, gpc_header: str, consumer_id: str) -> None:
        """Process Global Privacy Control signal."""
        if gpc_header == "1":
            # GPC signal present - treat as opt-out of sale/share
            self.process_opt_out_sale(consumer_id)
            self.process_opt_out_share(consumer_id)

            audit_log.info(
                "gpc_signal_processed",
                consumer_id=consumer_id
            )

    def check_opt_out_status(self, consumer_id: str) -> dict:
        """Check consumer's opt-out status."""
        return {
            "sale": self._is_opted_out(consumer_id, "sale"),
            "share": self._is_opted_out(consumer_id, "share"),
            "sensitive": self._is_limited(consumer_id, "sensitive")
        }
```

### Step 4: Sensitive Personal Information

```python
class SensitiveDataService:
    """Handle CPRA sensitive personal information requirements."""

    SENSITIVE_CATEGORIES = [
        "social_security_number",
        "drivers_license",
        "passport",
        "financial_account",
        "precise_geolocation",
        "racial_ethnic_origin",
        "religious_beliefs",
        "union_membership",
        "mail_email_text_content",
        "genetic_data",
        "biometric_data",
        "health_information",
        "sex_life_orientation"
    ]

    def limit_sensitive_use(self, consumer_id: str) -> LimitResult:
        """Process request to limit use of sensitive data."""
        preference = SensitiveDataPreference(
            consumer_id=consumer_id,
            limited=True,
            timestamp=datetime.utcnow()
        )

        self.preference_repository.save(preference)

        # Restrict processing
        self._restrict_sensitive_processing(consumer_id)

        audit_log.info(
            "ccpa_limit_sensitive",
            consumer_id=consumer_id
        )

        return LimitResult(
            consumer_id=consumer_id,
            effective_date=datetime.utcnow()
        )

    def check_sensitive_data_use(
        self,
        consumer_id: str,
        purpose: str
    ) -> bool:
        """Check if sensitive data can be used for purpose."""
        preference = self.preference_repository.find(consumer_id)

        if preference and preference.limited:
            # Only allow use for specific purposes
            allowed_purposes = [
                "perform_services",
                "security",
                "fraud_prevention",
                "physical_safety",
                "short_term_transient"
            ]
            return purpose in allowed_purposes

        return True
```

### Step 5: Service Provider Requirements

```python
class ServiceProviderAgreement:
    """CCPA service provider agreement requirements."""

    REQUIRED_CLAUSES = [
        "prohibition_on_selling",
        "prohibition_on_sharing",
        "prohibition_on_retention_beyond_purpose",
        "prohibition_on_use_outside_relationship",
        "certification_of_understanding",
        "compliance_with_ccpa",
        "notification_of_subcontractors",
        "assistance_with_consumer_requests",
        "audit_rights"
    ]

    def generate_spa_requirements(self) -> dict:
        """Generate service provider agreement requirements."""
        return {
            "required_clauses": self.REQUIRED_CLAUSES,
            "prohibited_activities": [
                "Selling personal information",
                "Sharing personal information",
                "Retaining data beyond business purpose",
                "Using data for own purposes",
                "Combining with other sources"
            ],
            "obligations": [
                "Process data only as instructed",
                "Implement reasonable security",
                "Assist with consumer requests",
                "Allow audits",
                "Notify of security incidents"
            ]
        }

    def validate_spa(self, agreement: dict) -> ValidationResult:
        """Validate service provider agreement meets CCPA requirements."""
        missing_clauses = []

        for clause in self.REQUIRED_CLAUSES:
            if clause not in agreement.get("clauses", []):
                missing_clauses.append(clause)

        return ValidationResult(
            valid=len(missing_clauses) == 0,
            missing_clauses=missing_clauses
        )
```

## Implementation Checklist

### Privacy Notice Requirements
- [ ] Categories of PI collected disclosed
- [ ] Collection purposes disclosed
- [ ] Categories sold/shared disclosed
- [ ] Third parties disclosed
- [ ] Retention periods disclosed
- [ ] "Do Not Sell/Share" link present
- [ ] "Limit Use" link present

### Consumer Rights
- [ ] Right to Know process implemented
- [ ] Right to Delete process implemented
- [ ] Right to Correct process implemented
- [ ] Opt-out mechanisms active
- [ ] Limit sensitive use implemented
- [ ] Non-discrimination policy documented
- [ ] Response within 45 days

### Technical Requirements
- [ ] GPC signal honored
- [ ] Cookie consent mechanism
- [ ] Opt-out preference center
- [ ] Verification process
- [ ] Request tracking system

## Quality Checklist

- [ ] Privacy policy CCPA-compliant
- [ ] Required links present on homepage
- [ ] Consumer request process tested
- [ ] Service provider agreements updated
- [ ] Employee training completed
- [ ] Record-keeping implemented
- [ ] Audit trail maintained
- [ ] Annual data inventory updated

## Related Skills

- `gdpr-compliance` - EU privacy compliance
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
