---
name: white-labeling
description: Tenant branding and customization patterns for SaaS applications. Covers custom domains, theming, email customization, and brand isolation.
allowed-tools: Read, Glob, Grep, Task, mcp__perplexity__search, mcp__perplexity__reason, mcp__microsoft-learn__microsoft_docs_search, mcp__microsoft-learn__microsoft_docs_fetch
---

# White-Labeling Skill

Patterns for enabling tenant branding and customization in multi-tenant SaaS applications.

## When to Use This Skill

Use this skill when:

- **White Labeling tasks** - Working on tenant branding and customization patterns for saas applications. covers custom domains, theming, email customization, and brand isolation
- **Planning or design** - Need guidance on White Labeling approaches
- **Best practices** - Want to follow established patterns and standards

## Overview

White-labeling allows tenants to brand the application as their own. This ranges from simple logo/color changes to full custom domain support with complete brand isolation.

## White-Label Tiers

```text
+------------------------------------------------------------------+
|                   White-Label Maturity Levels                     |
+------------------------------------------------------------------+
| Level | Features                     | Complexity | Use Case      |
+-------+------------------------------+------------+---------------+
| 1     | Logo + colors                | Low        | SMB plans     |
| 2     | + Custom email sender        | Medium     | Pro plans     |
| 3     | + Custom domain (CNAME)      | Medium     | Business      |
| 4     | + Full brand isolation       | High       | Enterprise    |
| 5     | + Reseller/agency support    | Very High  | Platform      |
+-------+------------------------------+------------+---------------+
```

## Branding Configuration

### Brand Settings Model

```csharp
public sealed record TenantBranding
{
    public required Guid TenantId { get; init; }

    // Basic branding
    public required string CompanyName { get; init; }
    public string? LogoUrl { get; init; }
    public string? FaviconUrl { get; init; }

    // Colors
    public string PrimaryColor { get; init; } = "#3B82F6";
    public string SecondaryColor { get; init; } = "#1E40AF";
    public string AccentColor { get; init; } = "#F59E0B";
    public string BackgroundColor { get; init; } = "#FFFFFF";
    public string TextColor { get; init; } = "#1F2937";

    // Typography
    public string? FontFamily { get; init; }
    public string? CustomCss { get; init; }

    // Email branding
    public string? EmailFromName { get; init; }
    public string? EmailFromAddress { get; init; }
    public string? EmailHeaderHtml { get; init; }
    public string? EmailFooterHtml { get; init; }

    // Custom domain
    public string? CustomDomain { get; init; }
    public bool CustomDomainVerified { get; init; }
    public string? CustomDomainCertificateStatus { get; init; }
}
```

### Branding Service

```csharp
public interface ITenantBrandingService
{
    Task<TenantBranding> GetBrandingAsync(Guid tenantId, CancellationToken ct = default);
    Task UpdateBrandingAsync(Guid tenantId, TenantBrandingUpdate update, CancellationToken ct = default);
    Task<string> UploadLogoAsync(Guid tenantId, Stream logoStream, string contentType, CancellationToken ct = default);
    Task<CssVariables> GenerateCssVariablesAsync(Guid tenantId, CancellationToken ct = default);
}

public sealed record CssVariables
{
    public required string PrimaryColor { get; init; }
    public required string SecondaryColor { get; init; }
    public required string AccentColor { get; init; }
    public required string BackgroundColor { get; init; }
    public required string TextColor { get; init; }
    public string? FontFamily { get; init; }

    public string ToCss() => $@"
:root {{
    --color-primary: {PrimaryColor};
    --color-secondary: {SecondaryColor};
    --color-accent: {AccentColor};
    --color-background: {BackgroundColor};
    --color-text: {TextColor};
    {(FontFamily != null ? $"--font-family: {FontFamily};" : "")}
}}";
}
```

## Custom Domains

### Domain Configuration Flow

```text
Custom Domain Setup:
+------------------------------------------------------------------+
| Step | Action                        | Verification              |
+------+-------------------------------+---------------------------+
| 1    | Tenant enters custom domain   | Format validation         |
| 2    | System generates CNAME target  | Display to tenant         |
| 3    | Tenant configures DNS          | Manual step               |
| 4    | System verifies DNS            | DNS lookup                |
| 5    | System provisions SSL cert     | Let's Encrypt / managed   |
| 6    | Domain goes live               | Traffic routing           |
+------+-------------------------------+---------------------------+
```

### Domain Verification

```csharp
public sealed class CustomDomainService(
    IDnsVerifier dnsVerifier,
    ICertificateProvisioner certProvisioner,
    ITenantBrandingRepository repository)
{
    public async Task<DomainSetupResult> SetupDomainAsync(
        Guid tenantId,
        string domain,
        CancellationToken ct)
    {
        // Validate domain format
        if (!IsValidDomain(domain))
            return DomainSetupResult.Invalid("Invalid domain format");

        // Check if domain already in use
        if (await repository.IsDomainInUseAsync(domain, ct))
            return DomainSetupResult.Invalid("Domain already in use");

        // Generate CNAME target
        var cnameTarget = $"{tenantId}.app.yoursaas.com";

        await repository.SaveDomainConfigAsync(new DomainConfig
        {
            TenantId = tenantId,
            Domain = domain,
            CnameTarget = cnameTarget,
            Status = DomainStatus.PendingVerification
        }, ct);

        return DomainSetupResult.PendingVerification(cnameTarget);
    }

    public async Task<DomainVerificationResult> VerifyDomainAsync(
        Guid tenantId,
        CancellationToken ct)
    {
        var config = await repository.GetDomainConfigAsync(tenantId, ct);
        if (config is null)
            return DomainVerificationResult.NotConfigured();

        // Verify DNS CNAME record
        var dnsResult = await dnsVerifier.VerifyCnameAsync(
            config.Domain,
            config.CnameTarget,
            ct);

        if (!dnsResult.IsValid)
            return DomainVerificationResult.DnsFailed(dnsResult.Error);

        // Provision SSL certificate
        var certResult = await certProvisioner.ProvisionAsync(config.Domain, ct);
        if (!certResult.Success)
            return DomainVerificationResult.CertFailed(certResult.Error);

        // Update status
        config = config with
        {
            Status = DomainStatus.Active,
            CertificateExpiresAt = certResult.ExpiresAt
        };
        await repository.SaveDomainConfigAsync(config, ct);

        return DomainVerificationResult.Success();
    }
}
```

### Request Routing

```csharp
public sealed class TenantDomainMiddleware(
    RequestDelegate next,
    ITenantDomainResolver resolver)
{
    public async Task InvokeAsync(HttpContext context)
    {
        var host = context.Request.Host.Host;

        // Try to resolve tenant from custom domain
        var tenantId = await resolver.ResolveFromDomainAsync(host);

        if (tenantId.HasValue)
        {
            context.Items["TenantId"] = tenantId.Value;
            context.Items["IsCustomDomain"] = true;
        }
        else if (TryParseSubdomain(host, out var subdomain))
        {
            // Fall back to subdomain resolution
            tenantId = await resolver.ResolveFromSubdomainAsync(subdomain);
            if (tenantId.HasValue)
            {
                context.Items["TenantId"] = tenantId.Value;
                context.Items["IsCustomDomain"] = false;
            }
        }

        await next(context);
    }
}
```

## Email Customization

### Branded Email Sending

```csharp
public sealed class BrandedEmailService(
    IEmailSender emailSender,
    ITenantBrandingService branding)
{
    public async Task SendBrandedEmailAsync(
        Guid tenantId,
        string recipientEmail,
        string subject,
        string bodyHtml,
        CancellationToken ct)
    {
        var brand = await branding.GetBrandingAsync(tenantId, ct);

        // Build branded email
        var fullHtml = BuildBrandedEmail(brand, bodyHtml);

        // Use custom sender if configured
        var fromAddress = brand.EmailFromAddress ?? "noreply@yoursaas.com";
        var fromName = brand.EmailFromName ?? brand.CompanyName;

        await emailSender.SendAsync(new EmailMessage
        {
            From = new EmailAddress(fromAddress, fromName),
            To = [new EmailAddress(recipientEmail)],
            Subject = subject,
            HtmlBody = fullHtml
        }, ct);
    }

    private static string BuildBrandedEmail(TenantBranding brand, string bodyHtml)
    {
        return $@"
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: {brand.FontFamily ?? "Arial, sans-serif"}; }}
        .header {{ background-color: {brand.PrimaryColor}; padding: 20px; }}
        .content {{ padding: 20px; }}
        .footer {{ background-color: #f5f5f5; padding: 20px; font-size: 12px; }}
    </style>
</head>
<body>
    <div class='header'>
        {(brand.LogoUrl != null ? $"<img src='{brand.LogoUrl}' alt='{brand.CompanyName}' />" : $"<h1>{brand.CompanyName}</h1>")}
        {brand.EmailHeaderHtml ?? ""}
    </div>
    <div class='content'>
        {bodyHtml}
    </div>
    <div class='footer'>
        {brand.EmailFooterHtml ?? $"<p>&copy; {DateTime.UtcNow.Year} {brand.CompanyName}</p>"}
    </div>
</body>
</html>";
    }
}
```

## Theming Architecture

### CSS Variables Approach

```text
Frontend Theming:
+------------------------------------------------------------------+
| Approach     | Pros                    | Cons                   |
+--------------+-------------------------+------------------------+
| CSS Vars     | Runtime switching       | Browser support        |
| CSS-in-JS    | Dynamic, scoped         | Bundle size            |
| Compiled CSS | Performance             | Build per tenant       |
| Tailwind     | Utility classes         | Config complexity      |
+--------------+-------------------------+------------------------+

Recommended: CSS Variables with fallbacks
```

### Dynamic Theme Loading

```typescript
// Frontend: Load tenant branding
async function loadTenantBranding(tenantId: string): Promise<void> {
  const response = await fetch(`/api/branding/${tenantId}`);
  const branding = await response.json();

  // Apply CSS variables
  const root = document.documentElement;
  root.style.setProperty('--color-primary', branding.primaryColor);
  root.style.setProperty('--color-secondary', branding.secondaryColor);
  root.style.setProperty('--color-accent', branding.accentColor);

  // Update favicon
  if (branding.faviconUrl) {
    const favicon = document.querySelector('link[rel="icon"]');
    if (favicon) favicon.href = branding.faviconUrl;
  }

  // Update title
  document.title = `${branding.companyName} - App`;
}
```

### Server-Side Rendering

```csharp
// Inject branding into SSR HTML
public sealed class BrandingTagHelper : TagHelper
{
    private readonly ITenantContext _tenantContext;
    private readonly ITenantBrandingService _branding;

    public override async Task ProcessAsync(TagHelperContext context, TagHelperOutput output)
    {
        var brand = await _branding.GetBrandingAsync(_tenantContext.TenantId);
        var cssVars = await _branding.GenerateCssVariablesAsync(_tenantContext.TenantId);

        output.TagName = "style";
        output.Content.SetHtmlContent(cssVars.ToCss());
    }
}
```

## Brand Isolation

### Complete Isolation (Enterprise)

```text
Full White-Label Features:
- Custom domain (no reference to parent brand)
- Custom email domain (SPF/DKIM configured)
- Custom app name in browser
- Custom error pages
- Custom help/docs URL
- No "Powered by" footer
- Custom terms/privacy links
- Isolated analytics
```

### Isolation Configuration

```csharp
public sealed record BrandIsolationConfig
{
    public bool HideParentBrand { get; init; }
    public bool UseCustomErrorPages { get; init; }
    public string? CustomHelpUrl { get; init; }
    public string? CustomTermsUrl { get; init; }
    public string? CustomPrivacyUrl { get; init; }
    public bool IsolateAnalytics { get; init; }
    public string? CustomAnalyticsId { get; init; }
}
```

## Implementation Checklist

```text
Level 1 (Basic):
[ ] Logo upload with validation
[ ] Primary/secondary color selection
[ ] Color preview before save
[ ] CSS variables generation

Level 2 (Email):
[ ] Custom from name
[ ] Custom from address (verify domain)
[ ] Email header/footer HTML
[ ] Email preview

Level 3 (Domain):
[ ] Custom domain input
[ ] CNAME verification
[ ] SSL certificate provisioning
[ ] Request routing by domain

Level 4 (Full Isolation):
[ ] Hide parent branding
[ ] Custom error pages
[ ] Custom help/docs links
[ ] Isolated analytics

Level 5 (Reseller):
[ ] Sub-tenant management
[ ] Billing pass-through
[ ] White-label admin portal
```

## Anti-Patterns

| Anti-Pattern | Problem | Solution |
| ------------ | ------- | -------- |
| Hardcoded colors | Can't customize | CSS variables |
| Logo in code | Deployment per change | Dynamic asset loading |
| Email templates with brand | Per-tenant templates | Template + brand merge |
| No preview | Surprises | Preview before publish |
| Immediate publish | Mistakes visible | Draft/publish workflow |

## References

Load for detailed implementation:

- `references/branding-architecture.md` - Technical architecture
- `references/custom-domains.md` - Domain setup details

## Related Skills

- `tenant-provisioning` - Provisioning branded resources
- `settings-hierarchy` - Org/team/user customization
- `self-service-onboarding` - Branded onboarding

## MCP Research

For current white-labeling patterns:

```text
perplexity: "SaaS white-labeling 2024" "custom domain SSL provisioning"
microsoft-learn: "Azure CDN custom domains" "App Service custom domains"
```
