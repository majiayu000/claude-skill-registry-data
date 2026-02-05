---
name: weavr-components
# prettier-ignore
description: Use when building applications with Weavr for payments, cards, accounts, and identity verification. Covers both API integration and secure UI components.
---

# Weavr Component Integration Guide

Build payment and banking features using Weavr's API and secure UI components.

## Architecture Overview

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Your App UI   │────▶│  Weavr Secure   │────▶│   Weavr API     │
│                 │     │  UI Components  │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
        │                       │                       │
        │                       ▼                       │
        │               Tokenized Data                  │
        │               (never raw PII)                 │
        │                       │                       │
        └───────────────────────┴───────────────────────┘
                        Your Backend
```

## Quick Start

### 1. Setup Secure UI

```html
<script src="https://sandbox.weavr.io/app/secure/static/client.1.js"></script>
```

```javascript
window.OpcUxSecureClient.init("{{ui_key}}");
```

### 2. Create Identity (Server-side)

```typescript
// POST /multi/corporates or /multi/consumers
const response = await fetch('https://sandbox.weavr.io/multi/corporates', {
  method: 'POST',
  headers: {
    'api-key': API_KEY,
    'programme-key': PROGRAMME_KEY,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    rootUser: { name, surname, email, mobile, companyPosition, dateOfBirth },
    company: { type, name, registrationNumber, registrationCountry, businessAddress },
    baseCurrency: 'GBP'
  })
});
```

### 3. Secure Password Setup (Client-side)

```javascript
var form = window.OpcUxSecureClient.form();
var input = form.input("p", "password", { placeholder: "Create Password" });
input.mount(document.getElementById("password-container"));

form.tokenize(function(tokens) {
  // Send tokens.password to your server - never see raw password
});
```

## Key Concepts

| Concept | Description |
|---------|-------------|
| **Tokenization** | Sensitive data (passwords, PINs, card numbers) are tokenized client-side |
| **Stepped-up Auth** | Card display/PIN operations require additional authentication |
| **KYC/KYB** | Identity verification flows embedded via secure components |
| **Programmes** | Your Weavr configuration determining available features |

## Component Categories

### Input Components (Collect Sensitive Data)
- `password` / `confirmPassword` - Authentication credentials
- `passCode` / `confirmPassCode` - PIN-based authentication
- `cardPin` - Physical card PIN capture

### Display Components (Show Sensitive Data)
- `cardNumber` - Full card number display
- `cvv` - Card security code display
- `pin` - Existing PIN display

### Verification Components
- `consumer_kyc()` - Consumer identity verification
- `kyc()` - Director/representative KYC
- `kyb()` - Business verification

## Common Flows

See [references/flows.md](references/flows.md) for complete implementation patterns:
- Corporate Onboarding
- Consumer Onboarding
- Card Issuance & Management
- Payment Transfers
- Authentication & Step-up

## API Reference

Full API documentation: https://weavr-multi-api.redoc.ly/

See [references/api-quick-ref.md](references/api-quick-ref.md) for endpoint summary.

## Styling

See [references/styling.md](references/styling.md) for component customization.
