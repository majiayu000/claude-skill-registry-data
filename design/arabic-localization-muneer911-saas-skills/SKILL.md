---
name: arabic-localization
description: Provides comprehensive Arabic internationalization standards including i18n structure, translation key conventions, and tone variation guidelines for Najdi dialect, Professional Modern, and Modern Standard Arabic (MSA)
---

# Arabic Localization Standards

This skill defines the standardized approach to Arabic internationalization (i18n) for SaaS applications, covering file structure, naming conventions, and tone variations.

## File Structure

### Directory Organization

```
locales/
├── en/
│   ├── common.json
│   ├── auth.json
│   ├── dashboard.json
│   └── errors.json
└── ar/
    ├── common.json
    ├── auth.json
    ├── dashboard.json
    └── errors.json
```

### Namespace Strategy

**Core Namespaces (Always Required):**
- `common.json` - Shared UI elements, navigation, actions
- `auth.json` - Authentication, registration, password flows
- `errors.json` - Error messages, validation feedback
- `dashboard.json` - Main application interface

**Feature-Specific Namespaces:**
- `onboarding.json` - User onboarding flows
- `settings.json` - User preferences and configuration
- `billing.json` - Payments and subscriptions
- `notifications.json` - Alerts and notification messages
- `help.json` - Help center and documentation

## Translation Key Naming Conventions

### Hierarchical Structure

```json
{
  "namespace": {
    "section": {
      "component": {
        "element": "Translation"
      }
    }
  }
}
```

### Practical Examples

```json
// common.json
{
  "nav": {
    "home": "الرئيسية",
    "dashboard": "لوحة التحكم",
    "settings": "الإعدادات"
  },
  "actions": {
    "save": "حفظ",
    "cancel": "إلغاء",
    "delete": "حذف",
    "confirm": "تأكيد",
    "edit": "تعديل",
    "create": "إنشاء"
  },
  "status": {
    "loading": "جاري التحميل...",
    "success": "تم بنجاح",
    "error": "حدث خطأ",
    "empty": "لا توجد بيانات"
  }
}

// auth.json
{
  "login": {
    "title": "تسجيل الدخول",
    "email": "البريد الإلكتروني",
    "password": "كلمة المرور",
    "submit": "تسجيل الدخول",
    "forgotPassword": "نسيت كلمة المرور؟",
    "noAccount": "ليس لديك حساب؟"
  },
  "register": {
    "title": "إنشاء حساب جديد",
    "fullName": "الاسم الكامل",
    "confirmPassword": "تأكيد كلمة المرور",
    "terms": "أوافق على الشروط والأحكام",
    "submit": "إنشاء حساب"
  },
  "validation": {
    "emailRequired": "البريد الإلكتروني مطلوب",
    "emailInvalid": "صيغة البريد الإلكتروني غير صحيحة",
    "passwordTooShort": "كلمة المرور قصيرة جداً",
    "passwordMismatch": "كلمات المرور غير متطابقة"
  }
}

// errors.json
{
  "network": {
    "offline": "لا يوجد اتصال بالإنترنت",
    "timeout": "انتهت مهلة الطلب",
    "serverError": "خطأ في الخادم، يرجى المحاولة لاحقاً"
  },
  "auth": {
    "invalidCredentials": "بيانات الدخول غير صحيحة",
    "sessionExpired": "انتهت صلاحية الجلسة",
    "unauthorized": "غير مصرح لك بالوصول"
  },
  "validation": {
    "required": "هذا الحقل مطلوب",
    "invalidFormat": "الصيغة غير صحيحة",
    "tooLong": "القيمة طويلة جداً",
    "tooShort": "القيمة قصيرة جداً"
  }
}
```

### Key Naming Rules

1. **Use camelCase** for keys: `forgotPassword`, `emailAddress`
2. **Be descriptive** but concise: `loginSubmit` not `btn1`
3. **Group related translations**: `auth.login.*`, `auth.register.*`
4. **Consistent patterns**: All buttons end with action: `save`, `cancel`, `submit`
5. **Avoid redundancy**: `login.title` not `login.loginTitle`

## Tone Variation Guidelines

Arabic has distinct tone variations based on context and audience. This section defines three standard tones: Najdi, Professional, and Modern Standard Arabic (MSA).

### Tone Selection Matrix

| Context | Najdi | Professional | MSA |
|---------|-------|--------------|-----|
| Consumer Apps (Gulf Region) | ✅ Primary | ❌ | ⚠️ Fallback |
| B2B SaaS | ❌ | ✅ Primary | ✅ Alternative |
| Government/Formal | ❌ | ⚠️ | ✅ Primary |
| Education | ❌ | ⚠️ | ✅ Primary |
| Marketing (Gulf) | ✅ Primary | ❌ | ❌ |
| Support/Help | ✅ Preferred | ✅ Alternative | ⚠️ |

### Tone-Specific File Structure (Advanced)

For applications requiring multiple tones:

```
locales/
└── ar/
    ├── common.json          # Default (MSA)
    ├── common-najdi.json    # Najdi variant
    ├── common-pro.json      # Professional variant
    └── auth.json            # Shared across tones
```

**Implementation:**

```typescript
// Load tone-specific translations
const locale = 'ar';
const tone = user.preferences.tone || 'msa'; // 'najdi', 'professional', 'msa'

const translations = {
  ...require(`./locales/${locale}/common.json`),
  ...(tone !== 'msa' ? require(`./locales/${locale}/common-${tone}.json`) : {})
};
```

### Najdi Dialect Characteristics

**When to Use:**
- Consumer-facing apps targeting Gulf region (Saudi Arabia, Kuwait, UAE, Qatar)
- Casual, friendly interactions
- Marketing and engagement content
- Social features and community interactions

**Linguistic Features:**
- Informal pronouns: "إنت" (you - masculine), "إنتي" (you - feminine)
- Shortened words: "شلون" instead of "كيف حالك"
- Regional expressions: "زين" (good), "يلا" (let's go)
- Casual tone with emotional warmth

**Examples:**

```json
{
  "greeting": "هلا وغلا! 👋",
  "welcome": "أهلاً فيك",
  "howAreYou": "شلونك؟",
  "good": "زين",
  "thanks": "يعطيك العافية",
  "bye": "يلا باي",
  "wait": "شوي شوي",
  "done": "تمام",
  "error": "في مشكلة",
  "help": "تبي مساعدة؟"
}
```

**Complete Example (Najdi):**

```json
// common-najdi.json
{
  "dashboard": {
    "welcome": "هلا {name}، شلونك اليوم؟",
    "empty": "ما فيه شي هنا",
    "tryAgain": "جرب مرة ثانية"
  },
  "notifications": {
    "newMessage": "عندك رسالة جديدة",
    "reminder": "لا تنسى!",
    "success": "تمام! اشتغل زين"
  }
}
```

### Professional Modern Tone

**When to Use:**
- B2B applications
- Corporate environments
- Professional services platforms
- Enterprise SaaS
- Financial applications

**Linguistic Features:**
- Formal but not archaic
- Clear, concise language
- Modern terminology for tech concepts
- Professional distance while remaining accessible
- Avoids overly formal classical structures

**Examples:**

```json
{
  "greeting": "مرحباً",
  "welcome": "أهلاً بك",
  "howAreYou": "كيف حالك؟",
  "good": "جيد",
  "thanks": "شكراً",
  "bye": "إلى اللقاء",
  "wait": "يرجى الانتظار",
  "done": "تم بنجاح",
  "error": "حدث خطأ",
  "help": "هل تحتاج مساعدة؟"
}
```

**Complete Example (Professional):**

```json
// common-pro.json
{
  "dashboard": {
    "welcome": "مرحباً {name}، نتمنى لك يوماً مثمراً",
    "empty": "لا توجد بيانات متاحة",
    "tryAgain": "حاول مرة أخرى"
  },
  "notifications": {
    "newMessage": "لديك رسالة جديدة",
    "reminder": "تذكير هام",
    "success": "تمت العملية بنجاح"
  },
  "actions": {
    "save": "حفظ التغييرات",
    "cancel": "إلغاء العملية",
    "delete": "حذف نهائي",
    "confirm": "تأكيد الإجراء"
  }
}
```

### Modern Standard Arabic (MSA)

**When to Use:**
- Government applications
- Educational platforms
- Pan-Arab audience (multi-country)
- Formal documentation
- Legal and compliance content
- Default fallback for unknown audiences

**Linguistic Features:**
- Classical grammar structures
- Formal vocabulary
- Universal comprehension across Arab world
- Minimal regional dialect influences
- Appropriate for serious/official contexts

**Examples:**

```json
{
  "greeting": "السلام عليكم",
  "welcome": "أهلاً وسهلاً بكم",
  "howAreYou": "كيف حالكم؟",
  "good": "حسناً",
  "thanks": "شكراً جزيلاً",
  "bye": "مع السلامة",
  "wait": "يُرجى الانتظار",
  "done": "اكتملت العملية",
  "error": "حدث خطأ ما",
  "help": "هل تحتاجون إلى المساعدة؟"
}
```

**Complete Example (MSA):**

```json
// common.json (default MSA)
{
  "dashboard": {
    "welcome": "مرحباً بكم {name}، نأمل أن تكونوا بخير",
    "empty": "لا توجد بيانات لعرضها",
    "tryAgain": "يُرجى المحاولة مرة أخرى"
  },
  "notifications": {
    "newMessage": "لديكم رسالة جديدة",
    "reminder": "تذكير",
    "success": "نجحت العملية"
  },
  "terms": {
    "agreement": "اتفاقية الاستخدام",
    "privacy": "سياسة الخصوصية",
    "accept": "أوافق على الشروط والأحكام"
  }
}
```

## Comparative Examples

### Same Content, Three Tones

**Scenario: Welcome Message**

```json
// Najdi
"welcome": "هلا فيك! شلونك اليوم؟ إن شاء الله بخير 🌟"

// Professional
"welcome": "مرحباً بك! نتمنى لك تجربة ممتعة ومثمرة."

// MSA
"welcome": "أهلاً وسهلاً بكم. نأمل أن تحظوا بتجربة مُرضية."
```

**Scenario: Error Message**

```json
// Najdi
"error": "في مشكلة! جرب مرة ثانية يا ريت"

// Professional
"error": "حدث خطأ. يرجى المحاولة مرة أخرى"

// MSA
"error": "حدث خطأ ما. يُرجى المحاولة مرة أخرى"
```

**Scenario: Call to Action**

```json
// Najdi
"cta": "يلا! سجّل الحين واستمتع 🚀"

// Professional
"cta": "سجّل الآن واستفد من جميع المزايا"

// MSA
"cta": "سجّلوا الآن للاستفادة من كافة الخدمات"
```

## Pluralization Rules

Arabic has complex pluralization (singular, dual, plural, many). Use i18n libraries that support ICU message format:

```json
{
  "items": {
    "zero": "لا توجد عناصر",
    "one": "عنصر واحد",
    "two": "عنصران",
    "few": "{{count}} عناصر",
    "many": "{{count}} عنصراً",
    "other": "{{count}} عنصر"
  }
}
```

**React i18next Example:**

```typescript
import { useTranslation } from 'react-i18next';

const { t } = useTranslation();

// Automatically handles pluralization
<span>{t('items', { count: itemCount })}</span>
```

## Gender-Aware Translations

Arabic adjectives and verbs change based on gender. Handle with context:

```json
{
  "welcome": {
    "male": "مرحباً بك",
    "female": "مرحباً بكِ"
  },
  "ready": {
    "male": "أنت جاهز",
    "female": "أنتِ جاهزة"
  }
}
```

**Implementation:**

```typescript
const gender = user.gender || 'neutral';
t(`welcome.${gender}`, { fallback: t('welcome.male') });
```

## Date and Time Formatting

```json
{
  "date": {
    "format": "DD/MM/YYYY",
    "months": [
      "يناير", "فبراير", "مارس", "إبريل", "مايو", "يونيو",
      "يوليو", "أغسطس", "سبتمبر", "أكتوبر", "نوفمبر", "ديسمبر"
    ],
    "days": [
      "الأحد", "الاثنين", "الثلاثاء", "الأربعاء", 
      "الخميس", "الجمعة", "السبت"
    ]
  },
  "time": {
    "am": "ص",
    "pm": "م",
    "format": "hh:mm A"
  }
}
```

**Use Hijri Calendar for Gulf Region (Optional):**

```json
{
  "calendar": {
    "type": "hijri", // or "gregorian"
    "locale": "ar-SA"
  }
}
```

## Number Formatting

Arabic uses Eastern Arabic numerals (٠١٢٣٤٥٦٧٨٩) or Western (0123456789):

```json
{
  "numbers": {
    "useEasternNumerals": true, // ١٢٣ vs 123
    "decimalSeparator": "٫",
    "thousandsSeparator": "٬"
  }
}
```

**Implementation:**

```typescript
const formatNumber = (num: number, locale: string) => {
  return new Intl.NumberFormat(locale === 'ar' ? 'ar-SA' : 'en-US').format(num);
};

formatNumber(1234567.89, 'ar'); // ١٬٢٣٤٬٥٦٧٫٨٩ or 1,234,567.89
```

## Implementation Checklist

- [ ] Namespace structure created (common, auth, errors, etc.)
- [ ] Translation keys follow camelCase convention
- [ ] Hierarchical key organization implemented
- [ ] Tone variation selected (Najdi / Professional / MSA)
- [ ] Pluralization rules configured for Arabic
- [ ] Gender-aware translations where applicable
- [ ] Date/time formatting configured
- [ ] Number formatting decided (Eastern vs Western numerals)
- [ ] RTL text direction coordinated (see `rtl-ui` skill)
- [ ] Fallback language (English) available
- [ ] i18n library configured (react-i18next, next-i18next, etc.)
- [ ] Translation validation in place (no missing keys)
- [ ] Context provided for ambiguous translations

## Common Mistakes to Avoid

1. **Using Google Translate directly** - Results in unnatural phrasing
2. **Mixing tones inconsistently** - Choose one tone and stick to it
3. **Ignoring pluralization rules** - Arabic has 6 plural forms
4. **Direct word-for-word translation** - Arabic requires restructuring
5. **Forgetting gender context** - Affects verbs and adjectives
6. **Using wrong numerals** - Eastern vs Western varies by region
7. **Hardcoding dates in UI** - Use locale-aware formatting
8. **Over-formal tone for consumer apps** - Najdi is more engaging
9. **Too casual for B2B** - Professional or MSA is appropriate
10. **Not testing with native speakers** - Always validate with target audience

## Extended Resources

### Additional Documentation

This skill includes supplementary documentation for detailed examples:

**`tone-examples.md`** - Comprehensive tone comparison examples:
- Side-by-side comparisons across all three tones
- E-commerce flow examples
- Email templates in all tones
- Dashboard content examples
- Marketing copy variations
- Real-world scenario comparisons

To access detailed examples, agents should read `tone-examples.md` located in this skill directory.

---

## Resources

For detailed tone examples and additional context, see `tone-examples.md` in this skill directory.

---

**Tone Selection Quick Guide:**

- **Gulf Region Consumer App?** → Use **Najdi**
- **B2B / Corporate Platform?** → Use **Professional**
- **Multi-Country / Formal?** → Use **MSA**
- **Unsure?** → Start with **MSA**, can always localize later