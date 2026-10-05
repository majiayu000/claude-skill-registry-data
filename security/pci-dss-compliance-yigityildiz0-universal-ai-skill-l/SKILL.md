---
name: pci-dss-compliance
description: Implement PCI-DSS v4.0 requirements for payment card data security. Use when handling payment card data, preparing for PCI audits, securing payment systems.
---

# PCI-DSS v4.0 Compliance

Implement PCI Data Security Standard v4.0 requirements for secure handling of payment card data.

## When to Use This Skill

Use this skill when you need to:

- Process payment card data
- Prepare for PCI-DSS audit
- Implement payment security controls
- Secure cardholder data environments
- Meet merchant compliance requirements
- Document PCI controls

**Trigger phrases**: "PCI DSS", "PCI compliance", "payment security", "card data", "cardholder data", "payment processing"

## What This Skill Does

### PCI-DSS v4.0 Requirements

| Requirement | Focus | Controls |
|-------------|-------|----------|
| 1 | Network Security | Firewalls, network segmentation |
| 2 | Secure Configurations | Hardening, defaults removal |
| 3 | Account Data Protection | Encryption, key management |
| 4 | Transmission Security | TLS, encryption in transit |
| 5 | Malware Protection | Anti-malware, vulnerability management |
| 6 | Secure Development | Secure SDLC, code review |
| 7 | Access Restriction | Need-to-know, least privilege |
| 8 | User Identification | Authentication, MFA |
| 9 | Physical Access | Physical security controls |
| 10 | Logging & Monitoring | Audit trails, monitoring |
| 11 | Security Testing | Penetration testing, scanning |
| 12 | Security Policies | Policies, procedures, training |

## Instructions

### Step 1: Cardholder Data Environment (CDE) Definition

```python
from enum import Enum
from dataclasses import dataclass

class DataClassification(Enum):
    PAN = "primary_account_number"
    CVV = "card_verification_value"
    PIN = "personal_identification_number"
    TRACK_DATA = "magnetic_stripe_data"
    CARDHOLDER_NAME = "cardholder_name"
    EXPIRATION = "expiration_date"
    SERVICE_CODE = "service_code"

@dataclass
class CDEAsset:
    """Asset within the Cardholder Data Environment."""
    asset_id: str
    name: str
    type: str  # server, database, application, network
    data_elements: list[DataClassification]
    location: str
    owner: str
    segmented: bool

class CDEInventory:
    """Maintain inventory of CDE assets."""

    def __init__(self):
        self.assets: list[CDEAsset] = []

    def add_asset(self, asset: CDEAsset) -> None:
        """Add asset to CDE inventory."""
        self.assets.append(asset)

        audit_log.info(
            "cde_asset_added",
            asset_id=asset.asset_id,
            name=asset.name,
            data_elements=[d.value for d in asset.data_elements]
        )

    def generate_data_flow_diagram(self) -> dict:
        """Generate CDE data flow diagram."""
        return {
            "assets": [self._asset_to_dict(a) for a in self.assets],
            "data_flows": self._map_data_flows(),
            "network_segments": self._identify_segments(),
            "entry_points": self._identify_entry_points()
        }
```

### Step 2: Requirement 3 - Protect Stored Account Data

```python
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import hashlib

class PANProtection:
    """PCI-DSS Requirement 3: Protect stored account data."""

    # 3.3: PANs must be rendered unreadable
    def mask_pan(self, pan: str) -> str:
        """Mask PAN for display - show only first 6 and last 4."""
        if len(pan) < 13:
            raise ValueError("Invalid PAN length")

        # PCI-DSS 3.4: Only first 6 and last 4 digits may be displayed
        return f"{pan[:6]}{'*' * (len(pan) - 10)}{pan[-4:]}"

    def encrypt_pan(self, pan: str, key_id: str) -> EncryptedPAN:
        """Encrypt PAN for storage."""
        # PCI-DSS 3.5: Strong cryptography required
        key = self.key_vault.get_key(key_id)

        fernet = Fernet(key.value)
        encrypted = fernet.encrypt(pan.encode())

        audit_log.info(
            "pan_encrypted",
            key_id=key_id,
            pan_last_four=pan[-4:]
        )

        return EncryptedPAN(
            ciphertext=encrypted,
            key_id=key_id,
            algorithm="AES-256"
        )

    def tokenize_pan(self, pan: str) -> str:
        """Tokenize PAN to remove from scope."""
        # Generate format-preserving token
        token = self.tokenization_service.tokenize(
            value=pan,
            format="numeric",
            length=len(pan)
        )

        audit_log.info(
            "pan_tokenized",
            pan_last_four=pan[-4:],
            token_last_four=token[-4:]
        )

        return token

    def hash_pan(self, pan: str) -> str:
        """One-way hash for PAN comparison (not for retrieval)."""
        # PCI-DSS allows keyed cryptographic hash
        return hashlib.sha256(
            (pan + self.hash_salt).encode()
        ).hexdigest()


class KeyManagement:
    """PCI-DSS 3.6: Cryptographic key management."""

    KEY_ROTATION_PERIOD_DAYS = 365
    KEY_TYPES = ["DEK", "KEK", "PIN_KEY"]

    def generate_key(self, key_type: str) -> CryptoKey:
        """Generate new cryptographic key."""
        if key_type not in self.KEY_TYPES:
            raise ValueError(f"Invalid key type: {key_type}")

        key = CryptoKey(
            id=f"KEY-{uuid.uuid4().hex[:12]}",
            type=key_type,
            algorithm="AES-256",
            created_at=datetime.utcnow(),
            expires_at=datetime.utcnow() + timedelta(days=self.KEY_ROTATION_PERIOD_DAYS),
            status="active"
        )

        # Store in HSM
        self.hsm.store_key(key)

        audit_log.info(
            "crypto_key_generated",
            key_id=key.id,
            key_type=key_type,
            expires_at=key.expires_at.isoformat()
        )

        return key

    def rotate_key(self, old_key_id: str) -> CryptoKey:
        """Rotate cryptographic key."""
        old_key = self.hsm.get_key(old_key_id)
        new_key = self.generate_key(old_key.type)

        # Re-encrypt data with new key
        self._reencrypt_data(old_key_id, new_key.id)

        # Retire old key
        old_key.status = "retired"
        self.hsm.update_key(old_key)

        audit_log.info(
            "crypto_key_rotated",
            old_key_id=old_key_id,
            new_key_id=new_key.id
        )

        return new_key
```

### Step 3: Requirement 4 - Transmission Security

```python
class TransmissionSecurity:
    """PCI-DSS Requirement 4: Protect cardholder data in transit."""

    # 4.2: Strong cryptography for transmission
    TLS_MINIMUM_VERSION = "TLS1.2"
    ALLOWED_CIPHER_SUITES = [
        "TLS_AES_256_GCM_SHA384",
        "TLS_CHACHA20_POLY1305_SHA256",
        "TLS_AES_128_GCM_SHA256",
    ]

    def validate_tls_config(self, endpoint: str) -> TLSValidationResult:
        """Validate TLS configuration for endpoint."""
        import ssl
        import socket

        context = ssl.create_default_context()
        context.minimum_version = ssl.TLSVersion.TLSv1_2

        try:
            with socket.create_connection((endpoint, 443)) as sock:
                with context.wrap_socket(sock, server_hostname=endpoint) as ssock:
                    version = ssock.version()
                    cipher = ssock.cipher()

                    return TLSValidationResult(
                        endpoint=endpoint,
                        valid=True,
                        tls_version=version,
                        cipher_suite=cipher[0],
                        certificate_valid=True
                    )
        except ssl.SSLError as e:
            return TLSValidationResult(
                endpoint=endpoint,
                valid=False,
                error=str(e)
            )

    def enforce_tls_policy(self) -> dict:
        """Define TLS enforcement policy."""
        return {
            "minimum_version": self.TLS_MINIMUM_VERSION,
            "allowed_ciphers": self.ALLOWED_CIPHER_SUITES,
            "certificate_requirements": {
                "minimum_key_size": 2048,
                "signature_algorithm": ["sha256", "sha384", "sha512"],
                "validity_period_days": 398
            },
            "hsts_enabled": True,
            "hsts_max_age": 31536000
        }
```

### Step 4: Requirement 8 - Authentication

```python
class PCIAuthentication:
    """PCI-DSS Requirement 8: Identify users and authenticate access."""

    # 8.2: Authentication requirements
    MIN_PASSWORD_LENGTH = 12  # v4.0 increased from 7
    PASSWORD_COMPLEXITY = True
    PASSWORD_HISTORY = 4
    MAX_LOGIN_ATTEMPTS = 6
    LOCKOUT_DURATION = timedelta(minutes=30)
    MFA_REQUIRED_FOR_CDE = True

    def validate_password(self, password: str) -> PasswordValidationResult:
        """Validate password meets PCI requirements."""
        errors = []

        if len(password) < self.MIN_PASSWORD_LENGTH:
            errors.append(f"Password must be at least {self.MIN_PASSWORD_LENGTH} characters")

        if self.PASSWORD_COMPLEXITY:
            if not any(c.isupper() for c in password):
                errors.append("Password must contain uppercase letter")
            if not any(c.islower() for c in password):
                errors.append("Password must contain lowercase letter")
            if not any(c.isdigit() for c in password):
                errors.append("Password must contain digit")
            if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
                errors.append("Password must contain special character")

        return PasswordValidationResult(
            valid=len(errors) == 0,
            errors=errors
        )

    def enforce_mfa(self, user: User, access_type: str) -> MFARequirement:
        """Determine and enforce MFA requirements."""
        # 8.4: MFA required for all access to CDE
        requires_mfa = (
            access_type == "cde_access" or
            user.has_cde_access or
            user.is_admin
        )

        if requires_mfa and not user.mfa_enabled:
            audit_log.warning(
                "mfa_required_not_enabled",
                user_id=user.id,
                access_type=access_type
            )
            raise MFARequiredError("MFA must be enabled for CDE access")

        return MFARequirement(
            required=requires_mfa,
            methods=["totp", "hardware_token", "push_notification"]
        )
```

### Step 5: Requirement 10 - Logging and Monitoring

```python
class PCIAuditLogging:
    """PCI-DSS Requirement 10: Log and monitor access."""

    # 10.2: Audit events to log
    REQUIRED_EVENTS = [
        "user_access_cardholder_data",
        "actions_by_admin_or_root",
        "access_to_audit_trails",
        "invalid_logical_access_attempts",
        "use_of_identification_mechanisms",
        "initialization_of_audit_logs",
        "creation_deletion_system_objects"
    ]

    def log_cde_access(
        self,
        user_id: str,
        action: str,
        resource: str,
        data_elements: list[str],
        outcome: str
    ) -> None:
        """Log access to cardholder data environment."""
        # 10.3: Required audit trail entries
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "user_id": user_id,
            "action": action,
            "resource": resource,
            "data_elements": data_elements,
            "outcome": outcome,
            "source_ip": get_client_ip(),
            "source_location": self._geolocate_ip(get_client_ip()),
            "device_id": get_device_id(),
        }

        # Write to immutable log
        self.audit_store.write(entry)

        # Real-time alerting for suspicious activity
        if outcome == "failure" or action in ["delete", "export"]:
            self._evaluate_alert(entry)

    def configure_log_retention(self) -> LogRetentionPolicy:
        """Configure log retention per PCI requirements."""
        # 10.7: Retain audit trail history for at least one year
        return LogRetentionPolicy(
            retention_period_days=365,
            immediately_available_days=90,  # 3 months immediately available
            archive_storage="encrypted_cold_storage",
            integrity_protection="digital_signatures"
        )

    def setup_log_monitoring(self) -> MonitoringConfig:
        """Configure log monitoring and alerting."""
        return MonitoringConfig(
            real_time_alerts=[
                Alert(
                    name="multiple_failed_logins",
                    condition="failed_login_count > 5 within 5 minutes",
                    severity="high"
                ),
                Alert(
                    name="admin_action_outside_hours",
                    condition="admin_action and not business_hours",
                    severity="medium"
                ),
                Alert(
                    name="bulk_data_access",
                    condition="records_accessed > 1000 in single session",
                    severity="high"
                ),
            ],
            daily_review=True,
            automated_analysis=True
        )
```

### Step 6: Requirement 11 - Security Testing

```python
class PCISecurityTesting:
    """PCI-DSS Requirement 11: Regularly test security."""

    def schedule_vulnerability_scans(self) -> ScanSchedule:
        """Schedule vulnerability scans per PCI requirements."""
        # 11.3: Internal and external vulnerability scans
        return ScanSchedule(
            internal_scans={
                "frequency": "quarterly",
                "scope": "all_cde_systems",
                "passing_criteria": "no_high_or_critical_vulnerabilities"
            },
            external_scans={
                "frequency": "quarterly",
                "vendor": "PCI_ASV",  # Approved Scanning Vendor
                "scope": "external_facing_systems",
                "passing_criteria": "asv_compliant_scan"
            },
            after_significant_changes=True
        )

    def schedule_penetration_tests(self) -> PenTestSchedule:
        """Schedule penetration tests per PCI requirements."""
        # 11.4: Penetration testing
        return PenTestSchedule(
            frequency="annual",
            scope=[
                "Network layer testing",
                "Application layer testing",
                "Segmentation validation",
            ],
            methodology="industry_accepted",  # PTES, OWASP, etc.
            retesting_required_for_findings=True
        )

    def validate_segmentation(self) -> SegmentationTest:
        """Validate network segmentation."""
        # 11.4.5: Segmentation testing
        return SegmentationTest(
            frequency="at_least_annually",
            methodology=[
                "Port scanning from non-CDE to CDE",
                "Protocol analysis",
                "Firewall rule validation",
                "Data flow analysis"
            ],
            passing_criteria="no_unauthorized_access_paths"
        )
```

## Documentation Requirements

### Required Documents
- [ ] CDE network diagram
- [ ] Data flow diagram
- [ ] Asset inventory
- [ ] Security policies
- [ ] Incident response plan
- [ ] Change management procedures

### Required Evidence
- [ ] Vulnerability scan reports (quarterly)
- [ ] Penetration test reports (annual)
- [ ] Firewall rule reviews (semi-annual)
- [ ] User access reviews (quarterly)
- [ ] Log review evidence
- [ ] Training records

## Quality Checklist

- [ ] CDE scope defined and documented
- [ ] All 12 requirements addressed
- [ ] Cardholder data encrypted
- [ ] Strong cryptography implemented
- [ ] MFA enabled for CDE access
- [ ] Logging and monitoring active
- [ ] Vulnerability scans passing
- [ ] Penetration testing completed
- [ ] Policies documented and approved

## Related Skills

- `soc2-compliance` - SOC 2 implementation
- `security-review` - Security vulnerability review
- `dependency-security-audit` - Dependency scanning

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
