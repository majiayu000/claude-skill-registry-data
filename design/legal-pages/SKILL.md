---
name: legal-pages
description: Required legal pages for UK/HU lead generation websites. Privacy Policy, Cookie Policy. GDPR compliant. Bilingual templates (EN/HU).
---

# Legal Pages Skill

**No legal pages = No production deploy.**

## Purpose

Produces GDPR-compliant legal pages. Templates only, not legal advice.

## Scope

| ✅ Supported | ❌ Out of Scope |
|-------------|----------------|
| UK lead gen sites | E-commerce checkout |
| Hungarian lead gen sites | SaaS terms |
| Service business websites | Membership systems |
| Quote/contact forms | Payment processing |

## Skill Output

| Artefact | Required | Format |
|----------|----------|--------|
| Privacy Policy | ✅ Always | `/privacy-policy.astro` |
| Cookie Policy | If cookies | `/cookie-policy.astro` |
| Terms of Service | If booking | `/terms.astro` |
| Business Details | ✅ Always | Filled in templates |

## Input Required

```yaml
legal_info:
  country: UK | HU
  language: en | hu
  business_name: "Company Ltd"
  trading_name: "Brand Name"        # If different
  company_number: "12345678"        # If Ltd/Kft
  address: "Full registered address"
  email: "hello@domain.com"
  phone: "+44 1234 567890"
  vat_number: ""                    # Optional
  
cookies_used:
  analytics: true                   # GA4
  marketing: false                  # FB Pixel, Google Ads
  
form_fields:
  - name
  - email
  - phone
  - message
```

## Blocking Conditions (STOP)

| Condition | Result |
|-----------|--------|
| Missing business_name | STOP |
| Missing address | STOP |
| Missing email | STOP |
| Analytics true + no Cookie Policy | STOP |
| Country not UK/HU | STOP - different templates needed |

## Required Pages by Country

### UK (English)

| Page | URL | Regulator |
|------|-----|-----------|
| Privacy Policy | `/privacy-policy` | ICO (ico.org.uk) |
| Cookie Policy | `/cookie-policy` | ICO |

### Hungary (Hungarian)

| Page | URL | Regulator |
|------|-----|-----------|
| Adatvédelmi Tájékoztató | `/adatvedelem` | NAIH (naih.hu) |
| Cookie (Süti) Szabályzat | `/cookie-szabalyzat` | NAIH |

## Form Consent Rules

### Required Consent (kötelező)

```astro
<!-- Privacy consent - REQUIRED for form submission -->
<label class="flex items-start gap-2">
  <input type="checkbox" name="privacyConsent" required />
  <span class="text-sm">
    <!-- EN -->
    I agree to the <a href="/privacy-policy">Privacy Policy</a>. *
    <!-- HU -->
    Elfogadom az <a href="/adatvedelem">Adatvédelmi Tájékoztatót</a>. *
  </span>
</label>
```

### Optional Consent (opcionális)

```astro
<!-- Marketing consent - MUST NOT be required -->
<label class="flex items-start gap-2">
  <input type="checkbox" name="marketingConsent" />
  <span class="text-sm">
    <!-- EN -->
    I agree to receive marketing communications.
    <!-- HU -->
    Hozzájárulok marketing célú megkeresésekhez.
  </span>
</label>
```

**Rule: Marketing checkbox MUST NOT have `required` attribute.**

## Third-Party Services (categorized)

### Analytics (require cookie consent)

| Service | Privacy Policy |
|---------|---------------|
| Google Analytics | policies.google.com/privacy |
| Plausible | plausible.io/privacy |

### Marketing (require cookie consent)

| Service | Privacy Policy |
|---------|---------------|
| Facebook Pixel | facebook.com/privacy |
| Google Ads | policies.google.com/privacy |

### Infrastructure (no consent needed)

| Service | Privacy Policy |
|---------|---------------|
| Cloudflare | cloudflare.com/privacypolicy |
| Resend | resend.com/legal/privacy-policy |

## Footer Links

```astro
<!-- EN -->
<a href="/privacy-policy">Privacy Policy</a>
<a href="/cookie-policy">Cookie Policy</a>

<!-- HU -->
<a href="/adatvedelem">Adatvédelem</a>
<a href="/cookie-szabalyzat">Cookie szabályzat</a>
```

**Must be visible on every page.**

## Cookie Banner

Cross-reference: `astro-security` skill handles cookie banner implementation.

This skill provides content only:
- Cookie categories
- Cookie descriptions
- Consent text (EN/HU)

## Legal Disclaimer

> **This skill provides templates, not legal advice.**
> 
> Client must review and approve all legal content before production.
> After client approval, responsibility transfers to client.

## Forbidden

- ❌ Production without Privacy Policy
- ❌ Analytics without Cookie Policy
- ❌ Fake/placeholder business details
- ❌ Required marketing consent checkbox
- ❌ Missing form privacy consent
- ❌ Copy from other website verbatim

## References

- [privacy-en.md](references/privacy-en.md) — UK Privacy Policy template
- [privacy-hu.md](references/privacy-hu.md) — Hungarian Adatvédelmi Tájékoztató
- [cookies-en.md](references/cookies-en.md) — UK Cookie Policy template
- [cookies-hu.md](references/cookies-hu.md) — Hungarian Cookie szabályzat
- [business-intake.md](references/business-intake.md) — Required client info

## Definition of Done

- [ ] Privacy Policy exists (correct language)
- [ ] Cookie Policy exists (if analytics/marketing)
- [ ] Real business details included
- [ ] Correct regulator referenced (ICO/NAIH)
- [ ] Footer links on every page
- [ ] Form privacy consent checkbox (required)
- [ ] Marketing consent NOT required
- [ ] Client reviewed and approved
