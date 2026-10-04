---
name: phone-auth
description: Phone OTP authentication - country data, phone formatting, E.164 validation, rate limiting, retry patterns. Use when implementing phone verification flows. Supports Supabase and custom backends.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion
---

# Phone Auth - Phone OTP Authentication

Phone number OTP authentication with Clean Architecture. Backend handles security (OTP generation, rate limiting). Mobile handles UX (formatting, countdown, error display).

## When to Use This Skill

- Adding phone number login/signup to a Flutter app
- Implementing OTP verification flows
- User asks to "add phone auth", "phone login", or "OTP verification"

## Questions to Ask

1. **Backend type:** Supabase or Custom API?
2. **Countries data:** Local JSON (faster) or Backend API (dynamic)?

## Responsibilities

| Mobile | Backend |
|--------|---------|
| Display country picker | OTP generation (cryptographic) |
| Format phone input | OTP storage (hashed) |
| Convert to E.164 | Rate limiting |
| Show countdown timer | Expiration checking |
| Display errors | Attempt counting |
| Call backend APIs | User auth/creation |

## Reference Files

```
reference/
├── models/           # Country model (Freezed)
├── utils/            # Phone formatting, E.164 conversion
├── repositories/     # Domain interface + mock
├── providers/        # Riverpod notifier + state
└── failures/         # Sealed Failure types
```

**See:** [implementation-guide.md](implementation-guide.md) for complete file list and copy instructions.

## Workflow

1. Copy `data/countries.json` to `assets/data/`
2. Copy reference files to project (see implementation-guide.md)
3. Implement repository (Supabase or API) - see implementation-guide.md
4. Register provider in `lib/core/providers.dart`
5. Run `dart run build_runner build`
6. Use `/design` for UI components

## Core API

```dart
// Format and convert
final e164 = PhoneFormatUtils.toE164(localNumber, country);

// Send OTP
await repository.sendOtp(e164);

// Verify OTP
await repository.verifyOtp(phoneNumber, otp);
```

## Failure Types

| Type | When | UI Action |
|------|------|-----------|
| `InvalidPhoneFailure` | Bad format | Validation error |
| `RateLimitFailure(retryAfter)` | Too many sends | Countdown |
| `InvalidOtpFailure(remaining)` | Wrong OTP | Show attempts |
| `OtpExpiredFailure` | OTP timed out | Resend option |
| `MaxAttemptsFailure` | 3+ failures | Force new OTP |
| `PhoneAuthNetworkFailure` | Connection | Retry button |

## Retry Pattern

Escalating intervals: 30s → 40s → 60s → 90s → 120s

See `reference/providers/phone_auth_providers.dart` for configuration.

## Guides

| File | Content |
|------|---------|
| [implementation-guide.md](implementation-guide.md) | Step-by-step with Supabase + API examples |
| [best-practices-guide.md](best-practices-guide.md) | Security, UX patterns |
| [phone-formats-guide.md](phone-formats-guide.md) | E.164, country formats |
| [checklist.md](checklist.md) | Implementation verification |

## Checklist

- [ ] `countries.json` copied to `assets/data/`
- [ ] PhoneAuthRepository interface extends base AuthRepository
- [ ] `sendOtp(e164PhoneNumber)` and `verifyOtp(phone, otp)` implemented
- [ ] PhoneFormatUtils handles E.164 conversion
- [ ] All Failure types implemented (InvalidPhone, RateLimit, InvalidOtp, etc.)
- [ ] Retry intervals configured (30s → 40s → 60s → 90s → 120s)
- [ ] Provider registered in `lib/core/providers.dart`
- [ ] `build_runner` executed successfully
- [ ] Error messages use i18n keys

## Related Skills

- `/social-login` - Can combine with phone auth
- `/design` - Phone input and OTP UI components
- `/i18n` - Localized error messages
- `/testing` - Unit and widget tests
