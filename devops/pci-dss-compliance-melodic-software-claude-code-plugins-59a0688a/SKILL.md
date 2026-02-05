---
name: pci-dss-compliance
description: PCI DSS compliance planning for payment card handling including scope reduction, SAQ selection, and security controls
allowed-tools: Read, Glob, Grep, Write, Edit, Task
---

# PCI DSS Compliance Planning

Comprehensive guidance for Payment Card Industry Data Security Standard compliance before development begins.

## When to Use This Skill

- Building e-commerce or payment processing systems
- Integrating with payment gateways or processors
- Designing scope reduction strategies (tokenization, P2PE)
- Selecting appropriate SAQ for your business
- Preparing for PCI DSS assessments

## PCI DSS Fundamentals

### Cardholder Data Elements

| Data Element | Description | Storage Permitted? | Protection Required |
|--------------|-------------|-------------------|---------------------|
| **PAN** | Primary Account Number (16 digits) | Yes, if protected | Render unreadable |
| **Cardholder Name** | Name on card | Yes | Protect per requirement |
| **Service Code** | 3-4 digit code | Yes | Protect per requirement |
| **Expiration Date** | MM/YY | Yes | Protect per requirement |
| **CVV/CVC** | Card verification value | **NEVER** after auth | N/A - never store |
| **PIN/PIN Block** | Personal identification | **NEVER** after auth | N/A - never store |
| **Full Track Data** | Magnetic stripe data | **NEVER** after auth | N/A - never store |

### The 12 Requirements (PCI DSS 4.0)

```text
Goal 1: Build and Maintain a Secure Network and Systems
  1. Install and maintain network security controls
  2. Apply secure configurations to all system components

Goal 2: Protect Account Data
  3. Protect stored account data
  4. Protect cardholder data with strong cryptography during transmission

Goal 3: Maintain a Vulnerability Management Program
  5. Protect all systems and networks from malicious software
  6. Develop and maintain secure systems and software

Goal 4: Implement Strong Access Control Measures
  7. Restrict access to cardholder data by business need-to-know
  8. Identify users and authenticate access to system components
  9. Restrict physical access to cardholder data

Goal 5: Regularly Monitor and Test Networks
  10. Log and monitor all access to system components and cardholder data
  11. Test security of systems and networks regularly

Goal 6: Maintain an Information Security Policy
  12. Support information security with organizational policies and programs
```

## Scope Reduction Strategies

### Understanding PCI Scope

**In Scope:** Any system that stores, processes, or transmits cardholder data, OR connects to systems that do.

**Scope Reduction Goal:** Minimize systems handling raw cardholder data.

### Strategy 1: Tokenization

Replace PAN with non-sensitive token; processor stores actual card data.

```csharp
// Client-side tokenization flow
public class PaymentTokenization
{
    private readonly IPaymentGateway _gateway;

    public async Task<PaymentResult> ProcessPayment(
        string clientToken, // Token created in browser via gateway's JS
        decimal amount,
        string currency,
        CancellationToken ct)
    {
        // Server never sees raw card data - only token
        var request = new ChargeRequest
        {
            Token = clientToken,
            Amount = amount,
            Currency = currency,
            MerchantReference = Guid.NewGuid().ToString()
        };

        // Token is exchanged for payment at gateway
        var result = await _gateway.Charge(request, ct);

        // Store only the transaction reference, never card data
        return new PaymentResult
        {
            TransactionId = result.TransactionId,
            Status = result.Status,
            // Store token for recurring payments (if vaulted)
            VaultToken = result.VaultToken
        };
    }
}

// Scope: Only gateway SDK is in scope, not your entire application
```

### Strategy 2: Hosted Payment Page (Redirect)

Customer enters card data on processor's page; you never handle card data.

```csharp
public class HostedPaymentFlow
{
    private readonly IHostedPaymentProvider _provider;

    public async Task<string> CreatePaymentSession(
        Order order,
        CancellationToken ct)
    {
        var session = await _provider.CreateSession(new SessionRequest
        {
            Amount = order.Total,
            Currency = order.Currency,
            SuccessUrl = $"https://example.com/payment/success?order={order.Id}",
            CancelUrl = $"https://example.com/payment/cancel?order={order.Id}",
            WebhookUrl = "https://example.com/api/payment-webhook",
            Metadata = new Dictionary<string, string>
            {
                ["order_id"] = order.Id.ToString()
            }
        }, ct);

        // Redirect customer to processor's hosted page
        return session.RedirectUrl;
    }

    // Webhook receives payment confirmation - no card data
    public async Task HandleWebhook(PaymentWebhook webhook, CancellationToken ct)
    {
        // Verify webhook signature
        if (!_provider.VerifySignature(webhook))
            throw new SecurityException("Invalid webhook signature");

        // Update order status
        var orderId = Guid.Parse(webhook.Metadata["order_id"]);
        await _orderService.MarkPaid(orderId, webhook.TransactionId, ct);
    }
}
```

### Strategy 3: iFrame/Embedded Fields

Card fields are hosted by processor but appear on your page.

```html
<!-- Stripe Elements example - fields hosted by Stripe -->
<form id="payment-form">
    <div id="card-element">
        <!-- Stripe injects secure card input here -->
    </div>
    <button type="submit">Pay</button>
</form>

<script>
// Card data never touches your server
const stripe = Stripe('pk_live_xxx');
const elements = stripe.elements();
const cardElement = elements.create('card');
cardElement.mount('#card-element');

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    // Token created client-side, sent to your server
    const {token} = await stripe.createToken(cardElement);
    // Only token goes to your server
    await fetch('/api/payment', {
        method: 'POST',
        body: JSON.stringify({ token: token.id })
    });
});
</script>
```

### Strategy 4: Point-to-Point Encryption (P2PE)

Hardware encrypts card data at swipe; decryption only at processor.

```text
Card Swipe → P2PE Terminal → Encrypted → Your Systems → Processor
                                        (can't decrypt)

Benefits:
- Your systems handle encrypted data only
- Dramatically reduced scope
- Requires P2PE validated solution
```

### Scope Reduction Comparison

| Strategy | Your PCI Scope | SAQ Type | Complexity |
|----------|---------------|----------|------------|
| Store raw cards | Full environment | D | Very High |
| Tokenization (API) | Token handling systems | A-EP or D | Medium |
| iFrame/Hosted Fields | Minimal (web page) | A or A-EP | Low |
| Redirect to Processor | None (referrer only) | A | Very Low |
| P2PE Hardware | Terminal + network | P2PE | Low |

## SAQ Selection Guide

### SAQ Types Overview

| SAQ | Applies To | Requirements | Questions |
|-----|------------|--------------|-----------|
| **A** | E-commerce, all card functions outsourced | No CHD on your systems | ~24 |
| **A-EP** | E-commerce, website impacts card security | iFrame/JS approach | ~191 |
| **B** | Imprint/standalone dial terminals only | No electronic storage | ~41 |
| **B-IP** | Standalone IP-connected terminals | No electronic storage | ~82 |
| **C** | Payment app on internet-connected systems | No electronic storage | ~160 |
| **C-VT** | Virtual terminal, no electronic storage | Web-based, no storage | ~79 |
| **D** | All other merchants | Full requirements | ~329 |
| **D (SP)** | Service providers | Full requirements | ~400+ |
| **P2PE** | Using validated P2PE solution | Terminal + P2PE | ~33 |

### Decision Tree

```text
Do you store/process/transmit CHD electronically?
├─ NO: Are you e-commerce only?
│   ├─ YES: All card functions outsourced?
│   │   ├─ YES → SAQ A
│   │   └─ NO: Website controls redirect/iFrame?
│   │       ├─ YES → SAQ A-EP
│   │       └─ NO → SAQ D
│   └─ NO: Card-present only?
│       ├─ Imprint/standalone dial → SAQ B
│       ├─ Standalone IP terminals → SAQ B-IP
│       ├─ P2PE validated solution → SAQ P2PE
│       └─ Other → SAQ C or D
└─ YES: → SAQ D (full assessment)
```

## Security Controls Implementation

### Requirement 3: Protect Stored Account Data

```csharp
// PAN masking (display only first 6, last 4)
public static class PanMasking
{
    public static string Mask(string pan)
    {
        if (string.IsNullOrEmpty(pan) || pan.Length < 13)
            return pan;

        // First 6 (BIN) + masked middle + last 4
        var first6 = pan[..6];
        var last4 = pan[^4..];
        var maskedLength = pan.Length - 10;

        return $"{first6}{new string('*', maskedLength)}{last4}";
    }

    // Example: 4111111111111111 → 411111******1111
}

// Strong cryptography for stored PAN (when storage required)
public class PanEncryption
{
    private readonly IKeyManagement _keyManager;

    public async Task<EncryptedPan> Encrypt(string pan, CancellationToken ct)
    {
        // Use AES-256 minimum
        var key = await _keyManager.GetCurrentKey("pan-encryption", ct);

        using var aes = Aes.Create();
        aes.Key = key.KeyMaterial;
        aes.GenerateIV();

        using var encryptor = aes.CreateEncryptor();
        var plainBytes = Encoding.UTF8.GetBytes(pan);
        var encryptedBytes = encryptor.TransformFinalBlock(plainBytes, 0, plainBytes.Length);

        return new EncryptedPan
        {
            EncryptedData = Convert.ToBase64String(encryptedBytes),
            KeyId = key.KeyId,
            IV = Convert.ToBase64String(aes.IV)
        };
    }
}
```

### Requirement 4: Encrypt Transmission

```csharp
// TLS 1.2+ enforcement
public static class TlsConfiguration
{
    public static void ConfigureSecureDefaults()
    {
        // Disable older protocols
        ServicePointManager.SecurityProtocol =
            SecurityProtocolType.Tls12 |
            SecurityProtocolType.Tls13;
    }
}

// ASP.NET Core configuration
public class Program
{
    public static void Main(string[] args)
    {
        var builder = WebApplication.CreateBuilder(args);

        builder.WebHost.ConfigureKestrel(options =>
        {
            options.ConfigureHttpsDefaults(https =>
            {
                https.SslProtocols = SslProtocols.Tls12 | SslProtocols.Tls13;
            });
        });

        // ... rest of configuration
    }
}
```

### Requirement 8: Authentication

```csharp
// Multi-factor authentication for CDE access
public class PciMfaPolicy
{
    public bool RequiresMfa(string userId, string resourcePath)
    {
        // MFA required for all CDE access
        var cdeResources = new[]
        {
            "/admin/payments",
            "/api/transactions",
            "/reports/cardholder"
        };

        return cdeResources.Any(r =>
            resourcePath.StartsWith(r, StringComparison.OrdinalIgnoreCase));
    }
}

// Password policy (PCI DSS 4.0)
public class PciPasswordPolicy : IPasswordPolicy
{
    public PasswordRequirements GetRequirements()
    {
        return new PasswordRequirements
        {
            MinimumLength = 12,          // 4.0 increased from 7
            RequireComplexity = true,    // Multiple character types
            MaxAgeInDays = 90,           // Force change every 90 days
            HistoryCount = 4,            // Can't reuse last 4
            LockoutThreshold = 10,       // Lock after 10 failed attempts
            LockoutDurationMinutes = 30,
            IdleTimeoutMinutes = 15      // Session timeout for CDE access
        };
    }
}
```

### Requirement 10: Logging and Monitoring

```csharp
// PCI-compliant audit logging
public class PciAuditLogger
{
    private readonly ILogger _logger;
    private readonly TimeProvider _timeProvider;

    public void LogCdeAccess(CdeAccessEvent accessEvent)
    {
        // PCI requires: who, what, when, where, success/failure
        var entry = new AuditEntry
        {
            Timestamp = _timeProvider.GetUtcNow(),
            UserId = accessEvent.UserId,
            UserName = accessEvent.UserName,
            EventType = accessEvent.EventType.ToString(),
            Resource = accessEvent.Resource,
            Action = accessEvent.Action,
            SourceIp = accessEvent.SourceIp,
            Success = accessEvent.Success,
            Details = accessEvent.Details
        };

        // Never log actual card data
        _logger.LogInformation(
            "CDE_ACCESS: User={UserId} Action={Action} Resource={Resource} Success={Success} IP={SourceIp}",
            entry.UserId,
            entry.Action,
            entry.Resource,
            entry.Success,
            entry.SourceIp);

        // Retain logs for minimum 1 year
        // Immediately available for 3 months
    }

    public void LogSecurityEvent(SecurityEvent secEvent)
    {
        // Security events to log:
        // - All access to CHD
        // - All actions by admin/root
        // - All invalid access attempts
        // - Creation/deletion of system objects
        // - Initialization of audit logs
        // - Stopping/pausing of audit logs
    }
}
```

## Network Segmentation

### CDE Network Isolation

```text
┌─────────────────────────────────────────────────────────────┐
│                     Corporate Network                        │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              Cardholder Data Environment             │   │
│  │  ┌──────────┐    ┌──────────┐    ┌──────────┐       │   │
│  │  │ Payment  │    │ Database │    │   Admin  │       │   │
│  │  │  Server  │────│  Server  │────│ Jumphost │       │   │
│  │  └──────────┘    └──────────┘    └──────────┘       │   │
│  │       │                               │              │   │
│  │       │ ← Firewall/ACLs →            │              │   │
│  └───────┼──────────────────────────────┼──────────────┘   │
│          │                               │                  │
│    ┌─────▼─────┐                   ┌─────▼─────┐           │
│    │  Web App  │                   │   Admin   │           │
│    │ (no CHD)  │                   │  Worksta. │           │
│    └───────────┘                   └───────────┘           │
└─────────────────────────────────────────────────────────────┘
```

### Firewall Rules for CDE

```yaml
# Example firewall rules
CDE_Ingress:
  - Allow: Payment API (443) from Web Tier only
  - Allow: SSH (22) from Jumphost only
  - Allow: Database (5432) from Payment Server only
  - Deny: All other

CDE_Egress:
  - Allow: Payment Processor API (443)
  - Allow: NTP (123) to approved servers
  - Allow: Syslog (514) to SIEM
  - Deny: All other
```

## PCI Compliance Checklist

### Before Development

- [ ] Identify all payment flows
- [ ] Select scope reduction strategy
- [ ] Choose appropriate SAQ type
- [ ] Establish CDE boundaries
- [ ] Review vendor PCI compliance (AOCs)

### Architecture & Design

- [ ] Document network segmentation
- [ ] Define encryption strategy (storage and transit)
- [ ] Design access control model
- [ ] Plan audit logging approach
- [ ] Ensure no CVV/PIN storage

### Development

- [ ] Never log card data
- [ ] Implement TLS 1.2+ only
- [ ] Apply PAN masking for display
- [ ] Enforce MFA for CDE access
- [ ] Follow secure coding (Req 6)

### Testing & Assessment

- [ ] Vulnerability scanning (internal/external quarterly)
- [ ] Penetration testing (annual)
- [ ] Segmentation testing (if segmented)
- [ ] Application security testing

## Cross-References

- **Security Frameworks**: `security-frameworks` for control mapping
- **Data Classification**: `data-classification` for CHD handling
- **License Compliance**: `license-compliance` for payment SDK terms

## Resources

- [PCI SSC Document Library](https://www.pcisecuritystandards.org/document_library/)
- [PCI DSS 4.0 Quick Reference Guide](https://www.pcisecuritystandards.org/document_library/?document=pci_dss)
- [SAQ Instructions and Guidelines](https://www.pcisecuritystandards.org/document_library/?category=saqs)
