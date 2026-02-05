---
name: brazilian-fintech-compliance
description: Comprehensive Brazilian financial regulatory compliance guide. Use when implementing LGPD data protection, BCB regulations, PIX/Boleto standards, or financial security patterns for Brazilian market applications.
license: MIT
metadata:
  version: "1.0.0"
  author: "AegisWallet Compliance Team"
  category: "compliance"
  last-updated: "2025-11-27"
  domain: "brazilian-financial"
  expertise: ["lgpd-compliance", "bcb-regulations", "pix-standards", "data-protection", "financial-security"]
---

# Brazilian Fintech Compliance Skill

## About This Skill

This skill provides comprehensive guidance for Brazilian financial regulatory compliance, covering LGPD data protection, BCB regulations, PIX/Boleto standards, and security patterns required for fintech applications in Brazil.

## When to Use This Skill

Use this skill when:
- Implementing LGPD (Lei Geral de Proteção de Dados) compliance
- Designing PIX instant payment systems following BCB standards
- Creating Boleto payment workflows with proper regulations
- Setting up data protection and privacy controls
- Implementing Brazilian financial security patterns
- Validating compliance with BCB (Banco Central do Brasil) requirements
- Creating audit trails for financial operations
- Designing user consent management systems

## Key Compliance Areas

### 🛡️ LGPD (Lei Geral de Proteção de Dados)

#### Core Principles
- **Lawfulness, Fairness, and Transparency**: Process data lawfully and transparently
- **Purpose Limitation**: Collect data for specified, explicit, and legitimate purposes
- **Data Minimization**: Collect only necessary data for intended purposes
- **Accuracy**: Maintain accurate and up-to-date personal data
- **Storage Limitation**: Retain data only as long as necessary
- **Integrity and Confidentiality**: Ensure appropriate security of personal data
- **Accountability**: Demonstrate compliance with LGPD principles

#### Implementation Requirements
```typescript
interface LGPDCompliance {
  // Data subject rights implementation
  userRights: {
    access: boolean;        // Right to access personal data
    correction: boolean;    // Right to correct inaccurate data
    deletion: boolean;      // Right to erasure ("right to be forgotten")
    portability: boolean;   // Right to data portability
    information: boolean;   // Right to information about data processing
    objection: boolean;     // Right to object to processing
  };
  
  // Legal bases for processing
  legalBases: [
    'consent',              // Explicit consent
    'contract',             // Contract necessity
    'legal_obligation',     // Legal requirement
    'vital_interests',      // Protection of vital interests
    'public_interest',      // Public interest tasks
    'legitimate_interests'  // Legitimate interests
  ];
  
  // Data protection measures
  protectionMeasures: {
    encryption: 'AES-256',
    anonymization: 'automatic_after_retention',
    access_control: 'role_based_with_audit',
    breach_notification: '72_hours'
  };
}
```

### 🏦 BCB (Banco Central do Brasil) Regulations

#### PIX System Requirements
- Follow **BCB Circular No 4.015** for PIX implementation
- Implement **end-to-end encryption** for all transactions
- Maintain **transaction logging** for 5 years minimum
- Ensure **24/7 availability** with 99.9% uptime
- Implement **fraud detection** and prevention mechanisms
- Provide **user support** for dispute resolution

#### Open Banking Compliance
- Follow **BCB Circular No 4.842** for Open Banking
- Implement **API security** with OAuth 2.0 and TLS 1.3
- Provide **data sharing** with user consent
- Maintain **API documentation** and version control
- Implement **rate limiting** and abuse protection
- Ensure **service level agreements** (SLAs) compliance

### 💳 PIX Payment Standards

#### Technical Requirements
```typescript
interface PIXStandards {
  transactionLimits: {
    instant: {
      maximum: 1000,        // R$ 1.000 per transaction
      daily: 10000,        // R$ 10.000 per day
      monthly: 100000      // R$ 100.000 per month
    };
    scheduled: {
      maximum: 50000,      // R$ 50.000 per scheduled transaction
      advanceScheduling: 60  // Maximum 60 days in advance
    };
  };
  
  responseTimes: {
    processing: '2_seconds_maximum',
    confirmation: 'real_time',
    settlement: 'end_of_day'
  };
  
  securityMeasures: {
    multiFactorAuth: 'required_for_high_value',
    transactionLimits: 'user_configurable',
    fraudDetection: 'real_time_monitoring',
    encryption: 'end_to_end'
  };
}
```

#### Key Validation Requirements
- **PIX Key Format Validation**: CPF, CNPJ, email, phone, or random key
- **Recipient Verification**: Validate recipient identity before transfer
- **Transaction Limits**: Enforce individual and daily limits
- **Fraud Prevention**: Implement behavioral analysis and anomaly detection
- **Reversal Handling**: Support for limited transaction reversals within 24 hours

### 🧾 Boleto Payment Standards

#### Boleto Registration Requirements
```typescript
interface BoletoStandards {
  registration: {
    bankCode: '3_digit_febraban_code',
    currency: '980_for_real',
    dueDateCalculation: 'business_days_only',
    barcodeGeneration: 'modulo11_validation'
  };
  
  validation: {
    barcode: '44_digits_with_verification',
    lineCode: '47_digits_with_verification',
    amountValidation: 'decimal_precision_2',
    dueDate: 'minimum_2_business_days'
  };
  
  processing: {
    registration: 'same_day_cutoff',
    payment: 'real_time_confirmation',
    settlement: 'd_1_business_day'
  };
}
```

### 🔒 Security Implementation Patterns

#### Data Protection Architecture
```typescript
const securityImplementation = {
  encryption: {
    atRest: {
      algorithm: 'AES-256-GCM',
      keyManagement: 'hardware_security_module',
      rotationPolicy: '90_days'
    },
    inTransit: {
      protocol: 'TLS 1.3',
      certificateValidation: 'strict',
      perfectForwardSecrecy: true
    }
  },
  
  authentication: {
    methods: ['biometric', 'multi_factor', 'device_trust'],
    sessionManagement: 'short_lived_with_refresh',
    passwordPolicies: 'complex_with_regular_expiration'
  },
  
  authorization: {
    principle: 'least_privilege_access',
    rbac: 'role_based_with_context',
    auditLogging: 'comprehensive_with_tamper_protection'
  }
};
```

## Compliance Validation Framework

### Automated Compliance Checks

#### LGPD Compliance Checklist
- [ ] **Consent Management**: Explicit consent collection and recording
- [ ] **Data Mapping**: Complete inventory of personal data processing
- [ ] **Rights Implementation**: All 7 LGPD rights accessible to users
- [ ] **Data Minimization**: Only necessary data collected and processed
- [ ] **Retention Policies**: Data retention schedules defined and automated
- [ ] **Security Measures**: Appropriate technical and organizational measures
- [ ] **Breach Response**: Incident response plan with 72-hour notification
- [ ] **DPO Appointment**: Data Protection Officer designated and contactable

#### BCB Compliance Checklist
- [ ] **PIX Implementation**: Following BCB Circular No 4.015
- [ ] **Transaction Limits**: Appropriate limits configured and enforced
- [ ] **Fraud Prevention**: Detection systems implemented and monitored
- [ ] **Availability Requirements**: 99.9% uptime with proper monitoring
- [ ] **Record Keeping**: 5-year transaction history maintenance
- [ ] **User Support**: Dispute resolution mechanisms available
- [ ] **API Documentation**: Complete and up-to-date API specifications
- [ ] **Security Audits**: Regular security assessments and penetration testing

### Testing Compliance Implementation

#### Unit Testing for Compliance
```typescript
describe('LGPD Compliance Tests', () => {
  test('user consent is properly recorded', async () => {
    const consentData = {
      userId: 'user-123',
      purpose: 'payment_processing',
      granted: true,
      timestamp: new Date(),
      ipAddress: '192.168.1.1'
    };
    
    const result = await recordConsent(consentData);
    
    expect(result).toMatchObject({
      consentId: expect.any(String),
      recorded: true
    });
    
    // Verify audit log entry
    const auditLog = await getConsentAuditLog(result.consentId);
    expect(auditLog).toContain('Consent recorded for payment processing');
  });
  
  test('data anonymization after retention period', async () => {
    const expiredData = await getExpiredUserData();
    const anonymizedData = await anonymizeUserData(expiredData);
    
    expect(anonymizedData.name).toBe('Usuário Anonimizado');
    expect(anonymizedData.cpf).toBe('***.***.***-**');
    expect(anonymizedData.email).toMatch(/^[a-z]{2}\*\*\*@.*$/);
  });
});
```

#### Integration Testing for PIX
```typescript
describe('PIX Compliance Tests', () => {
  test('PIX transaction within daily limits', async () => {
    const userData = await getUserDailyTotals('user-123');
    const newTransaction = { amount: 5000 }; // R$ 5.000
    
    const dailyLimit = 10000; // R$ 10.000
    const currentTotal = userData.dailyTotal;
    
    expect(currentTotal + newTransaction.amount).toBeLessThanOrEqual(dailyLimit);
  });
  
  test('fraud detection triggers on suspicious patterns', async () => {
    const suspiciousTransaction = {
      amount: 999.99,
      recipient: 'new_user',
      timeOfDay: '02:30',
      deviceLocation: 'unusual_location'
    };
    
    const fraudScore = await calculateFraudScore(suspiciousTransaction);
    expect(fraudScore).toBeGreaterThan(0.7); // High risk threshold
  });
});
```

## Quick Reference

### Essential LGPD Terms
- **Dado Pessoal**: Personal data (any information related to an identified or identifiable person)
- **Dado Sensível**: Sensitive personal data (health, religion, political opinions, biometrics)
- **Titular**: Data subject (person to whom the personal data refers)
- **Controlador**: Controller (person who makes decisions about personal data processing)
- **Encarregado**: DPO (Data Protection Officer)

### PIX Key Formats
- **CPF**: 123.456.789-09
- **CNPJ**: 12.345.678/0001-90  
- **Email**: user@domain.com
- **Telefone**: (11) 98765-4321
- **Chave Aleatória**: 123e4567-e89b-12d3-a456-426614174000

### BCB Regulatory References
- **Circular No 4.015**: PIX system regulations
- **Circular No 4.842**: Open Banking regulations
- **Resolution No 4.827**: Security requirements for payment institutions
- **Normative Instruction No 101**: Financial data security standards

## References

For detailed implementation patterns and examples, see:
- `references/lgpd-implementation.md` - Complete LGPD implementation guide
- `references/pix-standards.md` - PIX technical specifications
- `references/boleto-processing.md` - Boleto implementation patterns
- `examples/compliance-tests.md` - Compliance testing examples
- `scripts/compliance-validator.py` - Automated compliance validation

---

**Built for Brazilian fintech compliance with enterprise-grade security and regulatory adherence.** 🇧🇷🛡️
