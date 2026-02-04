---
name: privacy-compliance
description: GDPR, CCPA, and privacy compliance guidance for data protection. Use when handling personal data, implementing consent management, or ensuring regulatory compliance across jurisdictions.
---

# Privacy Compliance Skill

This skill provides guidance for GDPR, CCPA, and other privacy regulations.

## Key Regulations

| Regulation | Region | Key Requirements |
|------------|--------|------------------|
| GDPR | EU/EEA | Consent, data rights, breach notification |
| CCPA/CPRA | California | Right to know, delete, opt-out |
| LGPD | Brazil | Similar to GDPR |
| PIPEDA | Canada | Consent, limited collection |

## GDPR Requirements

### Lawful Bases for Processing
1. Consent
2. Contract
3. Legal obligation
4. Vital interests
5. Public task
6. Legitimate interests

### Data Subject Rights
- Right to access
- Right to rectification
- Right to erasure ("right to be forgotten")
- Right to data portability
- Right to object

## Implementation Patterns

### Consent Management
```python
@dataclass
class Consent:
    user_id: str
    purpose: str
    granted_at: datetime
    withdrawn_at: datetime | None
    version: str
```

### Data Minimization
```python
# Only collect what's necessary
class UserRegistration(BaseModel):
    email: str  # Required for account
    name: str   # Required for personalization
    # Don't collect: age, gender, location unless needed
```

### Data Retention
```python
RETENTION_POLICIES = {
    "user_data": timedelta(days=365 * 2),
    "logs": timedelta(days=90),
    "analytics": timedelta(days=365),
}
```

## Privacy Checklist

- [ ] Privacy policy published and accessible
- [ ] Consent obtained before data collection
- [ ] Data subject rights implemented
- [ ] Data minimization practiced
- [ ] Retention policies defined
- [ ] Breach notification process ready
- [ ] DPA (Data Processing Agreement) with vendors
