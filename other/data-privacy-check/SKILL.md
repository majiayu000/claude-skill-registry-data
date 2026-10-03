---
name: data-privacy-check
description: >
  Use when processing, storing, or transmitting any data that might contain personally
  identifiable information (PII) or sensitive personal data. This skill provides
  procedures for identifying, protecting, and handling personal data in compliance
  with privacy regulations (POPIA, GDPR, CCPA).
---

# Data Privacy Check

## Overview
This skill defines how to handle personal and sensitive data in compliance with privacy regulations and organizational policies. Privacy violations can cause significant legal, financial, and reputational harm. Treat all potentially personal data with care.

## When to Use
- When processing data that might contain personal information
- When designing systems that collect or store user data
- When creating reports, analytics, or analysis from user data
- When sharing data between agents, companies, or external systems
- When testing systems and need sample data
- **Don't use when:** Working only with anonymized, aggregated data that cannot identify individuals

## Core Procedures

### Step 1: Identify Personal Data
Recognize these as personal data:
- **PII (Personally Identifiable Information):** Name, email, phone, ID number, address
- **Sensitive Personal Information:** Race, ethnicity, biometric data, health information, political views, religious beliefs
- **Financial Information:** Bank account, credit card, salary, financial history
- **Location Data:** GPS coordinates, address history, IP addresses
- **Behavioral Data:** Browsing history, purchase history, communication records
- **Professional Information:** Job title, employment history, performance data
- **Derived Data:** Profiles, scores, inferences about individuals

### Step 2: Apply Principles
For all personal data, apply these principles:
1. **Purpose Limitation:** Only collect/process data for specific, stated purpose
2. **Data Minimization:** Collect only what's needed, no more
3. **Storage Limitation:** Keep only as long as needed, then delete
4. **Accuracy:** Ensure data is accurate and up-to-date
5. **Confidentiality:** Protect data with appropriate security measures
6. **Accountability:** Be able to demonstrate compliance with these principles

### Step 3: Processing Rules

#### DO:
- [ ] Anonymize or pseudonymize data where possible
- [ ] Use test data (fake/synthetic) for development and testing
- [ ] Document what personal data you're processing and why
- [ ] Apply encryption for data at rest and in transit
- [ ] Limit access to personal data to those who need it
- [ ] Include privacy notices when collecting data

#### NEVER DO:
- Process personal data without clear purpose
- Share personal data outside authorized scope
- Use real personal data in test environments
- Store personal data longer than required
- Include personal data in logs or error messages
- Export personal data to external systems without authorization

### Step 4: Data Handling Checklist
- [ ] Data classification completed (personal/sensitive/aggregated)
- [ ] Purpose documented for data processing
- [ ] Data minimization applied (only necessary fields)
- [ ] Personal data anonymized or pseudonymized where possible
- [ ] Access controls applied to personal data
- [ ] Retention period defined and documented
- [ ] Export/sharing of personal data authorized and logged

### Step 5: Privacy Impact Assessment
For significant data processing:
1. What personal data will be processed?
2. What is the purpose and legal basis?
3. Who will have access?
4. What are the risks to individuals?
5. What safeguards are in place?
6. How long will data be retained?

## Quality Checklist
- [ ] All personal data identified and classified
- [ ] Purpose and legal basis documented
- [ ] Data minimization applied
- [ ] Security controls appropriate to data sensitivity
- [ ] No real personal data in test environments
- [ ] Retention period defined
- [ ] Processing logged for accountability

## Error Handling
- **Error:** Accidentally collected more personal data than needed
  **Response:** Delete unnecessary data immediately, document the over-collection
- **Error:** Found personal data in logs or test environment
  **Response:** Purge immediately from logs, replace test data with synthetic data, report to security team
- **Error:** Need to share data but unclear if authorized
  **Response:** Do NOT share until authorization confirmed, escalate to legal/compliance agent
- **Error:** Discovered data breach or unauthorized access
  **Response:** Activate incident-response skill immediately, notify Guardian/Sentinel and CEO

## Cross-Team Integration
**Related Skills:** secrets-handling, audit-trail-management, threat-modeling, incident-response
**Used By:** ALL agents that process or handle data (especially Data agents, Analytics, Legal, HR)