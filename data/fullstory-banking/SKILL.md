---
name: fullstory-banking
version: v2
description: Industry-specific guide for implementing Fullstory in banking and financial services applications. Covers regulatory requirements (PCI DSS, GLBA, SOX), privacy controls for sensitive financial data, authentication flows, transaction monitoring, and fraud detection patterns. Includes detailed examples for retail banking, investment platforms, and payment applications.
related_skills:
  - fullstory-privacy-controls
  - fullstory-privacy-strategy
  - fullstory-user-consent
  - fullstory-identify-users
  - fullstory-analytics-events
---

# Fullstory for Banking & Financial Services

> ⚠️ **LEGAL DISCLAIMER**: This guidance is for educational purposes only and does not constitute legal, compliance, or regulatory advice. Banking regulations (PCI DSS, GLBA, SOX, etc.) are complex, jurisdiction-specific, and subject to change. Always consult with your legal, compliance, and security teams before implementing any data capture solution. Your organization is responsible for ensuring compliance with all applicable regulations.

## Industry Overview

Banking and financial services have unique requirements for session analytics due to:

- **Regulatory compliance**: PCI DSS, GLBA, SOX, GDPR, CCPA
- **Extreme sensitivity**: Account numbers, balances, transactions
- **Fraud concerns**: Session replay can be evidence or attack vector
- **Trust requirements**: Customer confidence in security is paramount

### Key Goals for Banking Implementations

1. **Understand digital banking UX** without exposing sensitive data
2. **Track conversion funnels** (account opening, loan applications)
3. **Identify friction points** in authentication and transactions
4. **Monitor error patterns** without logging sensitive details
5. **Support fraud investigation** with proper data handling

---

## Recommended: Private by Default Mode

For banking applications, **Fullstory's Private by Default mode is highly recommended**:

```
┌─────────────────────────────────────────────────────────────────┐
│  BANKING: Enable Private by Default                              │
│                                                                 │
│  • All text masked by default                                    │
│  • Zero risk of accidentally capturing account numbers          │
│  • Selectively unmask navigation, buttons, product names        │
│  • Contact Fullstory Support to enable                          │
└─────────────────────────────────────────────────────────────────┘
```

> **Reference**: [Fullstory Private by Default](https://help.fullstory.com/hc/en-us/articles/360044349073-Fullstory-Private-by-Default)

---

## Regulatory Framework

### PCI DSS Requirements

| PCI DSS Requirement | Fullstory Implication |
|--------------------|----------------------|
| Protect stored cardholder data | Never capture card numbers, CVV |
| Encrypt transmission | Fullstory uses TLS (✓) |
| Restrict access | Limit Fullstory access to authorized staff |
| Track access | Use Fullstory audit logs |
| Test security | Include Fullstory in security assessments |

### GLBA (Gramm-Leach-Bliley Act)

| GLBA Requirement | Fullstory Implication |
|-----------------|----------------------|
| Protect customer NPI | Exclude account numbers, SSN, balances |
| Privacy notices | Document Fullstory in privacy policy |
| Safeguards | Implement privacy controls |

### Open Banking / PSD2 (EU Markets)

For EU financial services using Open Banking/PSD2:

| Requirement | Fullstory Implication |
|-------------|----------------------|
| Strong Customer Authentication (SCA) | Track SCA flows for UX, exclude credentials |
| Third-Party Provider (TPP) data | Exclude all TPP account aggregation data |
| Consent management | Track consent flows, not consent content |
| API data | Never capture API tokens or account data from aggregation |

```javascript
// Open Banking: Track UX flow, not financial data
FS('trackEvent', {
  name: 'open_banking_consent_flow',
  properties: {
    tpp_provider: 'generic_aggregator',  // Don't identify specific provider
    consent_step: 'bank_redirect',
    flow_type: 'ais'  // Account Information Service
    // NEVER: account data, balances, transaction lists
  }
});
```

### What MUST Be Excluded in Banking

| Data Type | Reasoning | Implementation |
|-----------|-----------|----------------|
| Account numbers | GLBA, PCI | `fs-exclude` |
| Routing numbers | GLBA | `fs-exclude` |
| Card numbers | PCI DSS | Auto-excluded + explicit |
| CVV/CVC | PCI DSS | Auto-excluded |
| SSN/Tax ID | GLBA, privacy | `fs-exclude` |
| PIN codes | Security | `fs-exclude` |
| Security answers | Security | `fs-exclude` |
| Account balances | GLBA, privacy | `fs-exclude` |
| Transaction amounts | GLBA, privacy | `fs-exclude` or ranges |
| Beneficiary details | GLBA | `fs-exclude` |

---

## Implementation Architecture

### Privacy Control Strategy

```
┌─────────────────────────────────────────────────────────────────┐
│                    BANKING APPLICATION                           │
├─────────────────────────────────────────────────────────────────┤
│  PUBLIC ZONE (fs-unmask)                                         │
│  • Marketing pages                                               │
│  • Product information                                           │
│  • Login button, navigation                                      │
│  • Error messages (sanitized)                                    │
├─────────────────────────────────────────────────────────────────┤
│  MASKED ZONE (fs-mask)                                           │
│  • Customer name                                                 │
│  • Email address                                                 │
│  • Phone number                                                  │
│  • Last 4 of account (when displayed)                           │
├─────────────────────────────────────────────────────────────────┤
│  EXCLUDED ZONE (fs-exclude)                                      │
│  • Full account numbers                                          │
│  • Transaction amounts                                           │
│  • Balance displays                                              │
│  • Card numbers, CVV                                             │
│  • SSN, Tax ID                                                   │
│  • Security questions/answers                                    │
│  • PIN entry                                                     │
│  • OTP codes                                                     │
│  • Beneficiary bank details                                      │
└─────────────────────────────────────────────────────────────────┘
```

### User Identification Pattern for Banking

```javascript
// BANKING: Always use internal customer ID
// NEVER use SSN, account number, or even email as UID

// On login success
function onLoginSuccess(customer) {
  // Use internal customer ID (not PII)
  FS('setIdentity', {
    uid: customer.customerId,  // e.g., "CUST-7829462"
    displayName: `Customer ${customer.customerId.slice(-4)}`  // Last 4 digits only
  });
  
  // Set non-sensitive properties for segmentation
  FS('setProperties', {
    type: 'user',
    properties: {
      // Business context (NOT sensitive)
      account_type: customer.accountType,        // "checking", "savings", "premium"
      customer_segment: customer.segment,        // "retail", "private", "business"
      has_mobile_app: customer.mobileAppInstalled,
      preferred_channel: customer.preferredChannel,
      enrollment_year: new Date(customer.enrolledAt).getFullYear(),
      
      // Feature access (for funnel analysis)
      has_bill_pay: customer.features.billPay,
      has_mobile_deposit: customer.features.mobileDeposit,
      has_zelle: customer.features.zelle,
      has_investment_account: customer.features.investments,
      
      // Joinable keys for internal systems
      crm_id: customer.salesforceId,
      core_banking_id: customer.coreSystemId
      
      // NEVER include:
      // ssn, account_number, balance, email, phone
    }
  });
}
```

---

## Page-Specific Implementations

### Login Page

```html
<!-- Banking Login Page -->
<div class="login-container">
  <!-- Logo and marketing - visible -->
  <div class="login-header fs-unmask">
    <img src="bank-logo.svg" alt="Bank Name" />
    <h1>Online Banking Login</h1>
  </div>
  
  <!-- Login form - mixed privacy -->
  <form class="login-form">
    <!-- Username might be account # or email -->
    <div class="form-group fs-mask">
      <label for="username">Username or Account Number</label>
      <input type="text" id="username" name="username" />
    </div>
    
    <!-- Password always excluded -->
    <div class="form-group fs-exclude">
      <label for="password">Password</label>
      <input type="password" id="password" name="password" />
    </div>
    
    <!-- Remember me - can be visible -->
    <div class="form-group fs-unmask">
      <label>
        <input type="checkbox" name="remember" />
        Remember this device
      </label>
    </div>
    
    <!-- Action buttons visible -->
    <div class="form-actions fs-unmask">
      <button type="submit">Log In</button>
      <a href="/forgot-password">Forgot Password?</a>
    </div>
  </form>
  
  <!-- Security info - visible -->
  <div class="security-notice fs-unmask">
    <p>Protected by 256-bit encryption</p>
  </div>
</div>
```

```javascript
// Login event tracking
document.querySelector('.login-form').addEventListener('submit', () => {
  FS('trackEvent', {
    name: 'login_attempted',
    properties: {
      // Only track method, not credentials
      login_method: 'username',
      remember_device: document.querySelector('[name=remember]').checked
    }
  });
});

// On login success
function onLoginSuccess(response) {
  FS('trackEvent', {
    name: 'login_success',
    properties: {
      login_method: 'username',
      mfa_required: response.mfaRequired,
      session_type: response.sessionType  // "full", "limited"
    }
  });
}

// On login failure (sanitize error)
function onLoginFailure(error) {
  FS('trackEvent', {
    name: 'login_failed',
    properties: {
      // Generic error category, NOT specific message
      error_category: categorizeLoginError(error),  // "invalid_credentials", "account_locked", "system_error"
      // NEVER include: error.message, attempted username
    }
  });
}
```

### Account Dashboard

```html
<!-- Account Dashboard - Heavy exclusion needed -->
<div class="dashboard">
  <!-- Navigation - visible -->
  <nav class="dashboard-nav fs-unmask">
    <a href="/accounts">Accounts</a>
    <a href="/transfers">Transfers</a>
    <a href="/payments">Payments</a>
    <a href="/profile">Profile</a>
  </nav>
  
  <!-- Greeting - mask name -->
  <div class="welcome-banner fs-mask">
    <h1>Welcome back, John Smith</h1>  <!-- Masked -->
  </div>
  
  <!-- Account cards - EXCLUDE financial data -->
  <div class="accounts-list">
    <div class="account-card">
      <!-- Account name visible for navigation context -->
      <h3 class="account-name fs-unmask">Primary Checking</h3>
      
      <!-- EXCLUDE: Account number and balance -->
      <div class="account-details fs-exclude">
        <p class="account-number">****1234</p>
        <p class="balance">$12,345.67</p>
      </div>
      
      <!-- Actions visible for UX tracking -->
      <div class="account-actions fs-unmask">
        <button>View Transactions</button>
        <button>Transfer</button>
      </div>
    </div>
    
    <div class="account-card">
      <h3 class="account-name fs-unmask">Savings</h3>
      <div class="account-details fs-exclude">
        <p class="account-number">****5678</p>
        <p class="balance">$50,000.00</p>
      </div>
      <div class="account-actions fs-unmask">
        <button>View Transactions</button>
        <button>Transfer</button>
      </div>
    </div>
  </div>
  
  <!-- Quick actions - visible -->
  <div class="quick-actions fs-unmask">
    <button>Pay a Bill</button>
    <button>Deposit Check</button>
    <button>Send Money</button>
  </div>
</div>
```

```javascript
// Dashboard page properties
FS('setProperties', {
  type: 'page',
  properties: {
    page_name: 'account_dashboard',
    // Generic counts, not specific values
    num_accounts: accounts.length,
    has_checking: accounts.some(a => a.type === 'checking'),
    has_savings: accounts.some(a => a.type === 'savings'),
    has_credit_card: accounts.some(a => a.type === 'credit'),
    has_investment: accounts.some(a => a.type === 'investment'),
    // Alerts (generic)
    has_pending_alerts: alerts.length > 0
    // NEVER: account balances, even aggregated
  }
});
```

### Transaction History

```html
<!-- Transaction History Page -->
<div class="transactions-page">
  <!-- Filters - visible -->
  <div class="transaction-filters fs-unmask">
    <select name="date-range">
      <option>Last 30 days</option>
      <option>Last 90 days</option>
      <option>This year</option>
    </select>
    <select name="type">
      <option>All Transactions</option>
      <option>Deposits</option>
      <option>Withdrawals</option>
    </select>
    <input type="text" placeholder="Search transactions" class="fs-mask" />
    <button>Apply</button>
  </div>
  
  <!-- Transaction list - EXCLUDE everything -->
  <div class="transactions-list fs-exclude">
    <!-- All transaction details are sensitive:
         - Merchant names (reveal spending habits)
         - Amounts (financial data)
         - Dates + merchants (pattern of life)
    -->
    <div class="transaction-row">
      <span class="date">Dec 1, 2024</span>
      <span class="merchant">AMAZON.COM</span>
      <span class="amount">-$149.99</span>
    </div>
    <!-- More transactions... -->
  </div>
  
  <!-- Pagination - visible -->
  <div class="pagination fs-unmask">
    <button>Previous</button>
    <span>Page 1 of 10</span>
    <button>Next</button>
  </div>
</div>
```

```javascript
// Transaction page tracking (no transaction details!)
FS('setProperties', {
  type: 'page',
  properties: {
    page_name: 'transaction_history',
    account_type: 'checking',  // Generic type
    date_range: selectedDateRange,
    transaction_type_filter: selectedTypeFilter,
    // For UX research: how many results
    result_count_range: getResultCountRange(transactions.length),  // "1-50", "51-100", "100+"
    // NEVER: merchant names, amounts, specific counts
  }
});

// Track filter usage (UX research)
function onFilterApply(filters) {
  FS('trackEvent', {
    name: 'transaction_filter_applied',
    properties: {
      date_range: filters.dateRange,
      type_filter: filters.type,
      has_search_term: filters.searchTerm.length > 0  // Boolean only!
    }
  });
}
```

### Transfer/Payment Flow

```html
<!-- Fund Transfer Page -->
<div class="transfer-page">
  <h1 class="fs-unmask">Transfer Funds</h1>
  
  <!-- From account - partially visible -->
  <div class="form-section">
    <label class="fs-unmask">From Account</label>
    <select class="fs-mask">
      <!-- Account names visible, numbers masked -->
      <option>Primary Checking (****1234) - $12,345.67</option>
      <option>Savings (****5678) - $50,000.00</option>
    </select>
  </div>
  
  <!-- To account - EXCLUDE external details -->
  <div class="form-section">
    <label class="fs-unmask">To Account</label>
    
    <!-- Internal transfer - can mask -->
    <div class="internal-transfer fs-mask">
      <select>
        <option>Savings (****5678)</option>
      </select>
    </div>
    
    <!-- External transfer - EXCLUDE all -->
    <div class="external-transfer fs-exclude">
      <input type="text" name="routing" placeholder="Routing Number" />
      <input type="text" name="account" placeholder="Account Number" />
      <input type="text" name="beneficiary" placeholder="Beneficiary Name" />
    </div>
  </div>
  
  <!-- Amount - EXCLUDE -->
  <div class="form-section fs-exclude">
    <label>Amount</label>
    <input type="number" name="amount" placeholder="$0.00" />
  </div>
  
  <!-- Memo - could contain sensitive info -->
  <div class="form-section fs-exclude">
    <label>Memo (optional)</label>
    <input type="text" name="memo" placeholder="For rent payment" />
  </div>
  
  <!-- Actions - visible -->
  <div class="form-actions fs-unmask">
    <button type="button">Cancel</button>
    <button type="submit">Review Transfer</button>
  </div>
</div>
```

```javascript
// Transfer flow tracking
function trackTransferInitiated(transfer) {
  FS('trackEvent', {
    name: 'transfer_initiated',
    properties: {
      // Type of transfer (for UX analysis)
      transfer_type: transfer.type,  // "internal", "external", "wire", "ach"
      is_recurring: transfer.isRecurring,
      is_same_day: transfer.isSameDay,
      // Amount range (NOT exact amount)
      amount_range: getAmountRange(transfer.amount),  // "$0-100", "$100-500", etc.
      // NEVER: account numbers, routing numbers, exact amount
    }
  });
}

function trackTransferCompleted(transfer) {
  FS('trackEvent', {
    name: 'transfer_completed',
    properties: {
      transfer_type: transfer.type,
      confirmation_method: transfer.confirmationMethod  // "email", "sms", "app"
    }
  });
}

function trackTransferFailed(error) {
  FS('trackEvent', {
    name: 'transfer_failed',
    properties: {
      // Generic error category
      error_category: categorizeTransferError(error),  // "insufficient_funds", "invalid_account", "limit_exceeded"
      transfer_type: error.transferType
    }
  });
}
```

### Bill Pay

```html
<!-- Bill Pay Page -->
<div class="billpay-page">
  <h1 class="fs-unmask">Pay Bills</h1>
  
  <!-- Payee list - need to exclude names (could be medical, etc.) -->
  <div class="payee-list">
    <div class="payee-card">
      <!-- Payee name could be sensitive (doctor, lawyer, etc.) -->
      <div class="payee-info fs-exclude">
        <h3>Dr. Smith Medical Group</h3>
        <p>Account: ****5678</p>
      </div>
      
      <!-- Payment amount excluded -->
      <div class="payment-info fs-exclude">
        <p>Amount Due: $250.00</p>
        <p>Due Date: Dec 15, 2024</p>
      </div>
      
      <!-- Actions visible -->
      <div class="payee-actions fs-unmask">
        <button>Pay Now</button>
        <button>Schedule</button>
        <button>AutoPay</button>
      </div>
    </div>
  </div>
  
  <!-- Add payee button - visible -->
  <div class="add-payee fs-unmask">
    <button>+ Add New Payee</button>
  </div>
</div>
```

### Mobile Check Deposit

```html
<!-- Mobile Deposit Page -->
<div class="mobile-deposit-page">
  <h1 class="fs-unmask">Deposit a Check</h1>
  
  <!-- Account selector - mask -->
  <div class="deposit-to fs-mask">
    <label>Deposit to:</label>
    <select>
      <option>Primary Checking (****1234)</option>
    </select>
  </div>
  
  <!-- Amount entry - exclude -->
  <div class="deposit-amount fs-exclude">
    <label>Check Amount</label>
    <input type="number" name="amount" placeholder="$0.00" />
  </div>
  
  <!-- Camera/image area - CRITICAL: exclude check images -->
  <div class="check-capture fs-exclude">
    <!-- Check images contain:
         - Account numbers
         - Routing numbers
         - Signatures
         - Names
         - Amounts
         MUST be excluded
    -->
    <div class="front-image">
      <p>Front of check</p>
      <button>Capture Front</button>
      <img id="check-front" />
    </div>
    <div class="back-image">
      <p>Back of check</p>
      <button>Capture Back</button>
      <img id="check-back" />
    </div>
  </div>
  
  <!-- Actions visible -->
  <div class="deposit-actions fs-unmask">
    <button>Cancel</button>
    <button>Submit Deposit</button>
  </div>
</div>
```

```javascript
// Mobile deposit tracking
FS('trackEvent', {
  name: 'mobile_deposit_initiated',
  properties: {
    account_type: 'checking',
    deposit_amount_range: getAmountRange(amount),
    // Image capture metrics (for UX)
    front_capture_attempts: captureAttempts.front,
    back_capture_attempts: captureAttempts.back,
    total_time_seconds: Math.round(totalTime / 1000)
    // NEVER: check amount, account numbers, images
  }
});
```

---

## Multi-Factor Authentication (MFA)

```html
<!-- MFA Challenge Page -->
<div class="mfa-page">
  <h1 class="fs-unmask">Verify Your Identity</h1>
  
  <!-- MFA method selection - visible -->
  <div class="mfa-options fs-unmask">
    <p>Choose how to receive your verification code:</p>
    <label>
      <input type="radio" name="mfa-method" value="sms" />
      Text message to ***-***-4567
    </label>
    <label>
      <input type="radio" name="mfa-method" value="email" />
      Email to j***@example.com
    </label>
    <label>
      <input type="radio" name="mfa-method" value="authenticator" />
      Authenticator app
    </label>
  </div>
  
  <!-- Code entry - EXCLUDE (it's a credential) -->
  <div class="mfa-code-entry fs-exclude">
    <label>Enter verification code</label>
    <input type="text" name="code" maxlength="6" />
  </div>
  
  <!-- Actions visible -->
  <div class="mfa-actions fs-unmask">
    <button>Resend Code</button>
    <button type="submit">Verify</button>
  </div>
</div>
```

```javascript
// MFA tracking
FS('trackEvent', {
  name: 'mfa_challenge_presented',
  properties: {
    available_methods: ['sms', 'email', 'authenticator'],
    trigger: 'login'  // "login", "high_risk_action", "device_change"
  }
});

FS('trackEvent', {
  name: 'mfa_method_selected',
  properties: {
    method: 'sms',  // Which method chosen
    is_remembered_device: false
  }
});

FS('trackEvent', {
  name: 'mfa_completed',
  properties: {
    method: 'sms',
    attempts: 1,
    time_to_complete_seconds: 45
  }
});
```

---

## Fraud Investigation Considerations

### What to Capture for Fraud Teams

```javascript
// Fraud-relevant signals (non-sensitive)
FS('setProperties', {
  type: 'user',
  properties: {
    // Device fingerprinting (Fullstory captures automatically)
    // Session metadata
    login_count_30d: user.loginCount30d,
    password_reset_count_90d: user.passwordResets90d,
    
    // Risk indicators (computed server-side)
    risk_score_band: getRiskBand(user.riskScore),  // "low", "medium", "high"
    is_new_device: session.isNewDevice,
    is_new_location: session.isNewLocation,
    
    // Account age
    account_age_days: daysSince(user.createdAt)
  }
});

// High-risk action tracking
function trackHighRiskAction(action) {
  FS('trackEvent', {
    name: 'high_risk_action',
    properties: {
      action_type: action.type,  // "external_transfer", "password_change", "add_payee"
      triggered_mfa: action.requiredMFA,
      risk_signals: action.riskSignals  // Generic flags, not details
    }
  });
}
```

### Session Replay for Investigations

When using session replay for fraud investigation:

1. **Access control**: Limit replay access to fraud team
2. **Audit logging**: Fullstory logs who views what
3. **Data retention**: Align with fraud investigation timelines
4. **Evidence chain**: Document how replay was accessed

---

## Common Banking Patterns

### Amount Range Helper

```javascript
// Convert exact amounts to privacy-safe ranges
function getAmountRange(amount) {
  if (amount <= 0) return 'zero';
  if (amount < 100) return '$1-$99';
  if (amount < 500) return '$100-$499';
  if (amount < 1000) return '$500-$999';
  if (amount < 5000) return '$1k-$5k';
  if (amount < 10000) return '$5k-$10k';
  if (amount < 50000) return '$10k-$50k';
  return '$50k+';
}
```

### Categorize Errors

```javascript
// Generic error categories (don't expose specifics)
function categorizeError(error) {
  const errorMap = {
    'INVALID_CREDENTIALS': 'authentication_failed',
    'ACCOUNT_LOCKED': 'account_locked',
    'SESSION_EXPIRED': 'session_expired',
    'INSUFFICIENT_FUNDS': 'transaction_declined',
    'DAILY_LIMIT_EXCEEDED': 'limit_exceeded',
    'INVALID_ACCOUNT': 'validation_error',
    'NETWORK_ERROR': 'system_error',
    'MAINTENANCE': 'system_unavailable'
  };
  return errorMap[error.code] || 'unknown_error';
}
```

### React Component Wrapper

```javascript
// Banking-specific privacy wrapper components
import React from 'react';

// For account numbers
export function AccountNumber({ value, showLast4 = true }) {
  return (
    <span className="fs-exclude">
      {showLast4 ? `****${value.slice(-4)}` : value}
    </span>
  );
}

// For monetary values
export function Currency({ amount, showRange = false }) {
  return (
    <span className="fs-exclude">
      {showRange ? getAmountRange(amount) : formatCurrency(amount)}
    </span>
  );
}

// For sensitive forms
export function SecureFormField({ label, children }) {
  return (
    <div className="form-field fs-exclude">
      <label>{label}</label>
      {children}
    </div>
  );
}

// For transaction lists
export function TransactionList({ transactions }) {
  return (
    <div className="transaction-list fs-exclude">
      {transactions.map(tx => (
        <TransactionRow key={tx.id} transaction={tx} />
      ))}
    </div>
  );
}
```

---

## KEY TAKEAWAYS FOR AGENT

When helping banking clients with Fullstory:

1. **Default to exclusion**: In banking, when uncertain, exclude
2. **Never capture**:
   - Full account numbers, routing numbers
   - Transaction amounts (use ranges)
   - Check images
   - Security credentials (passwords, PINs, OTP codes)
   - SSN/Tax IDs
3. **Use ranges for amounts**: `$100-$500` not `$347.82`
4. **Track actions, not details**: "transfer_completed" not "transferred $500 to account"
5. **Consider merchant names sensitive**: Shopping habits reveal a lot
6. **MFA codes are credentials**: Always exclude
7. **Audit your implementation**: Watch replays to verify

### Questions to Ask Banking Clients

1. "Is your Fullstory implementation in scope for PCI audits?"
2. "How do you handle fraud investigation with session replay?"
3. "Who has access to Fullstory in your organization?"
4. "Are transaction details being captured anywhere?"
5. "How are mobile deposit check images handled?"

---

## REFERENCE LINKS

- **PCI DSS Requirements**: https://www.pcisecuritystandards.org/
- **GLBA Compliance**: https://www.ftc.gov/legal-library/browse/rules/financial-privacy-rule
- **Fullstory Privacy Controls**: ../core/fullstory-privacy-controls/SKILL.md
- **Fullstory Privacy Strategy**: ../meta/fullstory-privacy-strategy/SKILL.md

---

*This skill document is specific to banking and financial services implementations. Always consult your compliance and legal teams before implementation.*

