---
name: weavr-ui
# prettier-ignore
description: Use when implementing Weavr UI components for secure payment flows, authentication (password/passcode), KYC/KYB verification, or card display
---

# Weavr UI Component Library

## Quick Start

```javascript
// Include: <script src="https://sandbox.weavr.io/app/secure/static/client.1.js">
window.OpcUxSecureClient.init("{{ui_key}}");
var form = window.OpcUxSecureClient.form();
var input = form.input("p", "password", { placeholder: "Password" });
input.mount(document.getElementById("password"));
form.tokenize(function(tokens) { /* Send to server */ });
```

## Core Principles

- **Tokenization**: Sensitive data tokenized client-side, never touches your servers
- **PCI Compliance**: Components qualify you for lowest PCI compliance level
- **Stepped-up Auth**: Card display components require stepped-up auth tokens

## Components

| Type | Component | Method |
|------|-----------|--------|
| Input | password, confirmPassword, passCode, confirmPassCode, cardPin | `form.input()` |
| Display | cardNumber, cvv, pin | `OpcUxSecureClient.span()` |
| Verify | kyc, kyb, consumer_kyc | `OpcUxSecureClient.kyc()` / `kyb()` / `consumer_kyc()` |

## Reference Files

- [references/components.md](references/components.md) - Full component API
- [references/styling.md](references/styling.md) - Styling and customization
