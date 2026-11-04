---
name: gdpr-expert
description: GDPR and data privacy compliance for WordPress. Manage consent, data requests, privacy settings, and compliance documentation.
tools_required: [wp_create_post, wp_update_post, wp_options, wp_users, woo_customers, email]
always_on: false
group: compliance
order: 2
requires: [privacy-policy-generator]
---

# GDPR Expert

Data privacy compliance management for WordPress and WooCommerce.

## When to Use This Skill

- Managing GDPR compliance
- Handling data subject requests (DSR)
- Configuring consent management
- Creating compliance documentation
- Auditing data collection practices
- Responding to privacy inquiries

## Core Capabilities

### Data Subject Rights
- Right to access (SAR - Subject Access Request)
- Right to rectification
- Right to erasure ("right to be forgotten")
- Right to data portability
- Right to object to processing
- Right to restrict processing

### Consent Management
- Cookie consent configuration
- Marketing consent tracking
- Explicit opt-in mechanisms
- Consent withdrawal handling
- Consent records maintenance

### Documentation
- Privacy policy creation
- Data processing records
- DPA (Data Processing Agreements)
- Cookie policy management
- Compliance audit trails

## Workflow

### Handling a Data Access Request

1. **Verify Identity**
   - Confirm requester identity
   - Log the request
   - Acknowledge within 72 hours

2. **Gather Data**
   - Export user data with `wp_users`
   - Export customer data with `woo_customers`
   - Check for third-party data

3. **Compile Response**
   - Format data clearly
   - Explain data categories
   - List data sources

4. **Respond**
   - Send data via `email`
   - Document response
   - Complete within 30 days

### Handling a Deletion Request

1. **Verify Request**
   - Confirm identity
   - Check for legal holds
   - Assess retention requirements

2. **Delete Data**
   - Remove user account
   - Anonymize order history
   - Delete marketing profiles

3. **Confirm**
   - Send confirmation email
   - Document completion
   - Update records

## GDPR Compliance Checklist

### Legal Basis
- [ ] Lawful basis documented for each processing activity
- [ ] Consent obtained where required
- [ ] Legitimate interest assessments completed
- [ ] Contract necessity documented for orders

### Rights
- [ ] Subject access request process in place
- [ ] Deletion process documented
- [ ] Data portability mechanism available
- [ ] Objection handling procedure defined

### Security
- [ ] Data encrypted in transit (SSL)
- [ ] Data encrypted at rest
- [ ] Access controls implemented
- [ ] Breach notification procedure defined

### Documentation
- [ ] Privacy policy published
- [ ] Cookie policy published
- [ ] Data processing records maintained
- [ ] DPAs signed with processors

### Consent
- [ ] Cookie consent banner active
- [ ] Marketing opt-in required
- [ ] Consent records maintained
- [ ] Withdrawal mechanism available

## Data Categories

### User Data
- Account information (name, email)
- Profile data
- Login history
- Activity logs

### Customer Data
- Order history
- Billing address
- Shipping address
- Payment methods (tokenized)

### Behavioral Data
- Page views
- Product interactions
- Search history
- Cart contents

## Response Templates

### Access Request Acknowledgment
```
Subject: Your Data Access Request - Received

Dear [Name],

We have received your request for a copy of your personal data held by [Company]. 

We will provide your data within 30 days as required by GDPR. If we need any additional information to verify your identity, we will contact you.

Reference Number: [#]

Best regards,
[Company] Privacy Team
```

### Deletion Confirmation
```
Subject: Your Data Has Been Deleted

Dear [Name],

As requested, we have deleted your personal data from our systems. This includes:

- Your user account
- Contact information
- Marketing preferences
- [Other categories]

Some data may be retained for legal obligations (e.g., order records for tax purposes), but has been anonymized where possible.

If you have any questions, please contact us.

Best regards,
[Company] Privacy Team
```

## Best Practices

1. **Document everything** - Maintain compliance records
2. **Respond promptly** - 30-day deadline is firm
3. **Verify identity** - Prevent unauthorized access
4. **Minimize data** - Only collect what's needed
5. **Encrypt sensitive data** - Security is fundamental
6. **Train staff** - Everyone handles data properly
7. **Regular audits** - Quarterly compliance checks
