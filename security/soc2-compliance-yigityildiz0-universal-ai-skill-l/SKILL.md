---
name: soc2-compliance
description: Implement SOC 2 Type II controls covering Trust Services Criteria (Security, Availability, Confidentiality, Processing Integrity, Privacy). Use when.
---

# SOC 2 Type II Compliance

Implement and document SOC 2 Type II controls for Trust Services Criteria to achieve enterprise-ready compliance and customer trust.

## When to Use This Skill

Use this skill when you need to:

- Prepare for SOC 2 Type II audit
- Implement Trust Services Criteria controls
- Document compliance evidence
- Build enterprise SaaS security
- Meet customer security requirements
- Establish security governance

**Trigger phrases**: "SOC 2 compliance", "SOC 2 audit", "Trust Services Criteria", "enterprise security", "security controls", "audit preparation"

## What This Skill Does

### Trust Services Criteria

| Criteria | Focus | Common Controls |
|----------|-------|-----------------|
| **Security** | Protection of systems | Access control, encryption, monitoring |
| **Availability** | System uptime | Redundancy, disaster recovery, SLAs |
| **Confidentiality** | Data protection | Classification, encryption, access limits |
| **Processing Integrity** | Data accuracy | Validation, error handling, QA |
| **Privacy** | Personal data | Consent, retention, data subject rights |

## Instructions

### Step 1: Security Controls (CC1-CC9)

#### Access Control (CC6)

```python
# Role-Based Access Control (RBAC)
from enum import Enum
from functools import wraps

class Role(Enum):
    ADMIN = "admin"
    USER = "user"
    READONLY = "readonly"

class Permission(Enum):
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    ADMIN = "admin"

ROLE_PERMISSIONS = {
    Role.ADMIN: {Permission.READ, Permission.WRITE, Permission.DELETE, Permission.ADMIN},
    Role.USER: {Permission.READ, Permission.WRITE},
    Role.READONLY: {Permission.READ},
}

def require_permission(permission: Permission):
    """Decorator to enforce permission checks."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user = get_current_user()
            user_permissions = ROLE_PERMISSIONS.get(user.role, set())
            if permission not in user_permissions:
                audit_log.warning(
                    "access_denied",
                    user_id=user.id,
                    required_permission=permission.value,
                    resource=func.__name__
                )
                raise PermissionDeniedError(f"Missing permission: {permission.value}")
            return func(*args, **kwargs)
        return wrapper
    return decorator
```

#### Authentication (CC6.1)

```python
from datetime import datetime, timedelta
import secrets
import bcrypt

class AuthenticationService:
    """SOC 2 compliant authentication service."""

    # CC6.1: Logical and physical access controls
    MIN_PASSWORD_LENGTH = 12
    PASSWORD_HISTORY_COUNT = 12
    MAX_LOGIN_ATTEMPTS = 5
    LOCKOUT_DURATION = timedelta(minutes=30)
    SESSION_TIMEOUT = timedelta(hours=24)
    MFA_REQUIRED = True

    def authenticate(self, email: str, password: str, mfa_token: str = None) -> Session:
        """Authenticate user with password and optional MFA."""
        user = self.user_repository.find_by_email(email)

        # Check account lockout
        if self._is_locked_out(user):
            audit_log.warning("auth_attempt_locked", user_id=user.id)
            raise AccountLockedError()

        # Verify password
        if not bcrypt.checkpw(password.encode(), user.password_hash):
            self._record_failed_attempt(user)
            audit_log.warning("auth_failed", user_id=user.id, reason="invalid_password")
            raise InvalidCredentialsError()

        # Verify MFA if required
        if self.MFA_REQUIRED:
            if not mfa_token or not self._verify_mfa(user, mfa_token):
                audit_log.warning("auth_failed", user_id=user.id, reason="invalid_mfa")
                raise MFARequiredError()

        # Create session
        session = self._create_session(user)
        audit_log.info("auth_success", user_id=user.id, session_id=session.id)

        return session
```

#### Encryption (CC6.7)

```python
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class EncryptionService:
    """SOC 2 compliant encryption service."""

    # CC6.7: Encryption of data in transit and at rest
    ALGORITHM = "AES-256-GCM"
    KEY_ROTATION_DAYS = 90

    def __init__(self, key_vault: KeyVault):
        self.key_vault = key_vault

    def encrypt_data(self, data: bytes, classification: str) -> EncryptedData:
        """Encrypt sensitive data with appropriate key."""
        key = self.key_vault.get_current_key(classification)

        fernet = Fernet(key.value)
        encrypted = fernet.encrypt(data)

        audit_log.info(
            "data_encrypted",
            classification=classification,
            key_id=key.id,
            data_size=len(data)
        )

        return EncryptedData(
            ciphertext=encrypted,
            key_id=key.id,
            algorithm=self.ALGORITHM
        )
```

### Step 2: Availability Controls (A1)

```python
class AvailabilityMonitor:
    """SOC 2 Availability criteria implementation."""

    # A1.1: System availability monitoring
    SLA_TARGET = 99.9  # percent
    HEALTH_CHECK_INTERVAL = 30  # seconds

    def __init__(self):
        self.metrics = MetricsCollector()
        self.alerting = AlertingService()

    async def health_check(self) -> HealthStatus:
        """Comprehensive system health check."""
        checks = {
            "database": self._check_database(),
            "cache": self._check_cache(),
            "storage": self._check_storage(),
            "external_apis": self._check_external_apis(),
        }

        results = await asyncio.gather(*checks.values(), return_exceptions=True)
        status = HealthStatus(
            healthy=all(r.healthy for r in results if not isinstance(r, Exception)),
            checks={k: r for k, r in zip(checks.keys(), results)},
            timestamp=datetime.utcnow()
        )

        self.metrics.record("health_check", status)

        if not status.healthy:
            await self.alerting.send_alert(
                severity="critical",
                message="System health check failed",
                details=status.to_dict()
            )

        return status

    def calculate_uptime(self, period: timedelta) -> float:
        """Calculate system uptime for SLA reporting."""
        incidents = self.incident_repository.find_by_period(period)
        total_downtime = sum(i.duration for i in incidents)
        total_time = period.total_seconds()

        uptime = ((total_time - total_downtime) / total_time) * 100
        return round(uptime, 3)
```

### Step 3: Confidentiality Controls (C1)

```python
class DataClassification(Enum):
    """Data classification levels per SOC 2 C1."""
    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    RESTRICTED = "restricted"

class DataProtectionService:
    """SOC 2 Confidentiality controls."""

    # C1.1: Confidential information identification
    CLASSIFICATION_RULES = {
        "ssn": DataClassification.RESTRICTED,
        "credit_card": DataClassification.RESTRICTED,
        "email": DataClassification.CONFIDENTIAL,
        "name": DataClassification.INTERNAL,
    }

    def classify_data(self, data: dict) -> dict:
        """Automatically classify data based on content."""
        classification = DataClassification.PUBLIC

        for field, value in data.items():
            field_class = self._detect_classification(field, value)
            if field_class.value > classification.value:
                classification = field_class

        audit_log.info(
            "data_classified",
            classification=classification.value,
            fields=list(data.keys())
        )

        return {
            "data": data,
            "classification": classification,
            "handling_requirements": self._get_handling_requirements(classification)
        }

    def _get_handling_requirements(self, classification: DataClassification) -> dict:
        """Get data handling requirements by classification."""
        requirements = {
            DataClassification.RESTRICTED: {
                "encryption": "required",
                "access_logging": "required",
                "retention_days": 365,
                "deletion": "secure_wipe",
            },
            DataClassification.CONFIDENTIAL: {
                "encryption": "required",
                "access_logging": "required",
                "retention_days": 730,
                "deletion": "standard",
            },
        }
        return requirements.get(classification, {})
```

### Step 4: Processing Integrity Controls (PI1)

```python
class ProcessingIntegrityService:
    """SOC 2 Processing Integrity controls."""

    # PI1.1: Processing accuracy and completeness
    def validate_input(self, data: dict, schema: Schema) -> ValidationResult:
        """Validate input data against schema."""
        errors = []
        warnings = []

        for field, rules in schema.fields.items():
            value = data.get(field)

            if rules.required and value is None:
                errors.append(f"Missing required field: {field}")
                continue

            if value is not None:
                if not self._validate_type(value, rules.type):
                    errors.append(f"Invalid type for {field}")
                if not self._validate_constraints(value, rules.constraints):
                    errors.append(f"Constraint violation for {field}")

        result = ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )

        audit_log.info(
            "data_validated",
            valid=result.valid,
            error_count=len(errors),
            schema=schema.name
        )

        return result

    def ensure_idempotency(self, operation_id: str) -> IdempotencyResult:
        """Ensure operation idempotency to prevent duplicate processing."""
        existing = self.idempotency_store.get(operation_id)

        if existing:
            audit_log.info("operation_duplicate", operation_id=operation_id)
            return IdempotencyResult(duplicate=True, result=existing)

        return IdempotencyResult(duplicate=False, result=None)
```

### Step 5: Privacy Controls (P1-P8)

```python
class PrivacyService:
    """SOC 2 Privacy criteria implementation."""

    # P1: Privacy notice
    # P2: Choice and consent
    # P3: Collection
    # P4: Use, retention, and disposal
    # P5: Access
    # P6: Disclosure
    # P7: Quality
    # P8: Monitoring and enforcement

    def record_consent(
        self,
        user_id: str,
        purpose: str,
        scope: list[str],
        expiry: datetime = None
    ) -> Consent:
        """Record user consent for data processing."""
        consent = Consent(
            user_id=user_id,
            purpose=purpose,
            scope=scope,
            granted_at=datetime.utcnow(),
            expires_at=expiry,
            version=self.get_privacy_policy_version()
        )

        self.consent_repository.save(consent)

        audit_log.info(
            "consent_recorded",
            user_id=user_id,
            purpose=purpose,
            scope=scope
        )

        return consent

    def handle_data_subject_request(
        self,
        user_id: str,
        request_type: DataSubjectRequestType
    ) -> DataSubjectResponse:
        """Handle data subject rights requests (GDPR, CCPA)."""
        audit_log.info(
            "dsr_received",
            user_id=user_id,
            request_type=request_type.value
        )

        if request_type == DataSubjectRequestType.ACCESS:
            return self._handle_access_request(user_id)
        elif request_type == DataSubjectRequestType.DELETE:
            return self._handle_deletion_request(user_id)
        elif request_type == DataSubjectRequestType.PORTABILITY:
            return self._handle_portability_request(user_id)
```

### Step 6: Audit Logging

```python
import structlog
from datetime import datetime

class AuditLogger:
    """Comprehensive audit logging for SOC 2 compliance."""

    def __init__(self):
        self.logger = structlog.get_logger("audit")

    def log(
        self,
        event: str,
        severity: str = "info",
        user_id: str = None,
        resource: str = None,
        action: str = None,
        outcome: str = None,
        **details
    ):
        """Log audit event with required SOC 2 fields."""
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event": event,
            "severity": severity,
            "user_id": user_id or get_current_user_id(),
            "source_ip": get_client_ip(),
            "resource": resource,
            "action": action,
            "outcome": outcome,
            "request_id": get_request_id(),
            "session_id": get_session_id(),
            **details
        }

        # Log to immutable audit store
        self.logger.info(event, **entry)

        # Also store in database for reporting
        self.audit_repository.save(AuditEntry(**entry))

# Global audit logger
audit_log = AuditLogger()
```

## Evidence Collection Checklist

### Security Evidence
- [ ] Access control policies documented
- [ ] RBAC implementation screenshots
- [ ] Encryption configuration evidence
- [ ] Penetration test results
- [ ] Vulnerability scan reports

### Availability Evidence
- [ ] Uptime reports for audit period
- [ ] Incident response documentation
- [ ] Disaster recovery test results
- [ ] SLA compliance reports

### Confidentiality Evidence
- [ ] Data classification matrix
- [ ] Encryption key management procedures
- [ ] Access request/approval logs
- [ ] Data handling procedures

### Processing Integrity Evidence
- [ ] Input validation documentation
- [ ] Error handling procedures
- [ ] Change management records
- [ ] QA test results

### Privacy Evidence
- [ ] Privacy policy current version
- [ ] Consent management records
- [ ] Data subject request logs
- [ ] Retention policy documentation

## Quality Checklist

- [ ] All 5 Trust Services Criteria addressed
- [ ] Control descriptions documented
- [ ] Evidence mapped to controls
- [ ] Testing procedures defined
- [ ] Exceptions documented
- [ ] Remediation plans in place
- [ ] Audit trail complete
- [ ] Policies reviewed and approved

## Related Skills

- `iso27001-compliance` - ISO 27001 implementation
- `security-review` - Security vulnerability review
- `gdpr-compliance` - GDPR compliance

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
