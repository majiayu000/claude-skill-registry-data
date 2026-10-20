---
name: frontend-quality-security-tooling
description: Use this skill to establish enterprise frontend testing strategies with Vitest v2, MSW v2, and Playwright, enforce client/SSR security with strict nonce-based CSP v3, DOMPurify Trusted Types, and React 19 Taint APIs, configure Rust-based build toolchains with Biome 2.x and Turborepo, and govern bundle budgets and MADR architectural records.
category: quality
tags:
  - testing-trophy
  - vitest-v2
  - msw-v2
  - playwright-e2e
  - frontend-security
  - strict-csp
  - biome-tooling
  - clean-architecture
user-invocable: true
---

# Frontend Quality, Security & Tooling Architecture

Bu alt uzmanlık yeteneği; 2025–2026 kurumsal test piramidini (Testing Trophy), ağ seviyesinde API mocking standartlarını (MSW v2), hermetik E2E ve görsel regresyon süreçlerini (Playwright), istemci ve SSR güvenlik protokollerini (OWASP, Strict CSP v3, Trusted Types, React 19 Taint API), Rust tabanlı ultra-hızlı derleme araçlarını (Biome 2.x, Turborepo) ve mimari liderlik yönetişimini (MADR) yönetir.

- **Ana Orkestratör Referansı:** [product-frontend-clean-architecture-development](../../SKILL.md)
- **Detaylı Sektör Araştırma Raporu:** [quality_security_tooling_architecture_deep_research.md](researches/quality_security_tooling_architecture_deep_research.md)

---

## 🚫 1. Katı Kalite ve Güvenlik Kısıtlamaları (Enforced Guardrails)

1. **Davranış Odaklı Testleme & İç Detay Yasağı:**
   * React Testing Library testlerinde bileşenin `state` veya `props` değerleri sorgulanamaz. Kullanıcının ve ekran okuyucunun algıladığı erişilebilirlik rolleri (`getByRole('button', { name: /onayla/i })`) zorunludur. `fireEvent` yasaktır; gerçekçi `userEvent.setup()` kullanılmalıdır.
2. **Ağ Seviyesinde Mocklama & `global.fetch` Yasağı:**
   * Birim ve entegrasyon testlerinde `global.fetch = vi.fn()` monkey-patching'i KESİNLİKLE yasaktır. Ağ trafiği Service Worker / Interceptors seviyesinde **MSW v2 (Mock Service Worker)** ile intercept edilmeli; aynı mock handler'ları Vitest, Storybook ve Playwright arasında paylaşılmalıdır.
3. **Hermetik E2E & Keyfi Bekleme Yasağı:**
   * Playwright testlerinde `waitForTimeout(3000)` veya sleep fonksiyonları KESİNLİKLE kullanılamaz; Playwright'ın dahili 6 adımlı eyleme geçebilirlik (auto-waiting) ve web assertion'ları (`expect(locator).toBeVisible()`) kullanılmalıdır. Kimlik doğrulama her testte tekrarlanmaz; `storageState` ile önbelleklenir.
4. **W3C Trusted Types ve XSS Koruması:**
   * Dinamik HTML enjeksiyonlarında düz string kullanımı yasaktır; `DOMPurify` bir W3C **Trusted Types API** politikasına bağlanarak `TrustedHTML` üretilmelidir.
5. **Nonce-Tabanlı Strict CSP v3:**
   * SSR / Next.js çıktılarında `'unsafe-inline'` ve `'unsafe-eval'` yasaktır. İstek başına kriptografik bir nonce üretilerek `'strict-dynamic'` CSP v3 başlığı uygulanmalıdır.
6. **SSR & RSC Veri Sızıntısı Yasağı:**
   * Sunucu sırları `server-only` modül yalıtımı ve React 19 Taint API (`experimental_taintObjectReference`) ile korunmalı; istemci bileşenlerine asla ham veritabanı modelleri geçirilmemeli, yalnızca katı DTO'lar aktarılmalıdır.
7. **Performans Bütçesi & PR Blocking:**
   * Her PR `@size-limit/preset-app` ile denetlenmeli; belirlenen JavaScript chunk bütçesini aşan değişiklikler CI aşamasında engellenmelidir.

---

## 🏛️ 2. Temel Mimari Yapı Taşları ve Kod Şablonları

### A. Vitest v2 + MSW v2 Entegrasyon Test Şablonu

```typescript
// features/auth/LoginForm.test.tsx
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { http, HttpResponse } from 'msw';
import { server } from '../../test/mocks/server';
import { LoginForm } from './LoginForm';

describe('LoginForm Integration Test', () => {
  it('geçerli bilgilerle giriş yapıldığında yükleme ve başarı durumunu erişilebilir gösterir', async () => {
    const user = userEvent.setup();
    render(<LoginForm />);

    // 1. Erişilebilir rollerle elemanları bul
    const emailInput = screen.getByRole('textbox', { name: /e-posta/i });
    const passwordInput = screen.getByLabelText(/şifre/i);
    const submitBtn = screen.getByRole('button', { name: /giriş yap/i });

    // 2. Gerçekçi kullanıcı etkileşimi (Mock / Test verisi)
    await user.type(emailInput, 'user@example.com');
    await user.type(passwordInput, 'mock-test-password-123');
    await user.click(submitBtn);

    // 3. Durum doğrulaması
    expect(submitBtn).toBeDisabled();
    expect(await screen.findByRole('alert')).toHaveTextContent(/hoş geldiniz/i);
  });

  it('sunucu 401 döndürdüğünde hata uyarısını gösterir', async () => {
    server.use(
      http.post('/api/auth/login', () => {
        return HttpResponse.json({ message: 'Hatalı şifre' }, { status: 401 });
      })
    );

    const user = userEvent.setup();
    render(<LoginForm />);

    await user.type(screen.getByRole('textbox', { name: /e-posta/i }), 'dev@test.com');
    await user.type(screen.getByLabelText(/şifre/i), 'yanlis');
    await user.click(screen.getByRole('button', { name: /giriş yap/i }));

    expect(await screen.findByRole('alert')).toHaveTextContent(/hatalı şifre/i);
  });
});
```

### B. Playwright Hermetik E2E ve Görsel Regresyon

```typescript
// e2e/checkout-visual.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Checkout Flow & Visual Regression', () => {
  test.use({ storageState: 'e2e/.auth/user.json' }); // Önbelleklenmiş oturum

  test('ödeme sayfası layout kayması yaşamamalı ve siparişi tamamlamalı', async ({ page }) => {
    await page.clock.setFixedTime(new Date('2026-10-12T10:00:00Z')); // Deterministik zaman
    await page.goto('/checkout');

    const paymentCard = page.locator('[data-testid="payment-card"]');
    await expect(paymentCard).toBeVisible();

    // Görsel regresyon kontrolü (Pixelmatch)
    await expect(paymentCard).toHaveScreenshot('payment-card.png', {
      animations: 'disabled',
      maxDiffPixelRatio: 0.005, // %0.5 tolerans
      mask: [page.locator('.dynamic-timestamp')],
    });

    // Otomatik beklemeli etkileşim
    await page.getByRole('button', { name: /ödemeyi tamamla/i }).click();
    await expect(page.getByRole('heading', { name: /siparişiniz alındı/i })).toBeVisible();
  });
});
```

### C. W3C Trusted Types + DOMPurify Güvenli HTML Fabrikası

```typescript
// security/trustedHtml.ts
import DOMPurify from 'dompurify';

export const safeHtmlPolicy = (() => {
  if (typeof window !== 'undefined' && (window as any).trustedTypes) {
    try {
      return (window as any).trustedTypes.createPolicy('dompurify-policy', {
        createHTML: (raw: string) => DOMPurify.sanitize(raw, {
          FORBID_TAGS: ['script', 'iframe', 'object'],
          FORBID_ATTR: ['onerror', 'onload', 'onclick'],
        }),
      });
    } catch {
      // Politika zaten kayıtlı
    }
  }
  return { createHTML: (raw: string) => DOMPurify.sanitize(raw) };
})();
```

### D. Next.js Nonce Tabanlı Strict CSP v3 Middleware

```typescript
// middleware.ts
import { NextResponse, type NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  const nonce = Buffer.from(crypto.randomUUID()).toString('base64');
  const isDev = process.env.NODE_ENV === 'development';

  const cspHeader = `
    default-src 'self';
    script-src 'self' 'nonce-${nonce}' 'strict-dynamic' ${isDev ? "'unsafe-eval'" : ''};
    style-src 'self' 'nonce-${nonce}';
    img-src 'self' blob: data: https:;
    font-src 'self';
    object-src 'none';
    base-uri 'self';
    frame-ancestors 'none';
    require-trusted-types-for 'script';
    upgrade-insecure-requests;
  `.replace(/\s{2,}/g, ' ').trim();

  const headers = new Headers(request.headers);
  headers.set('x-nonce', nonce);
  headers.set('Content-Security-Policy', cspHeader);

  const res = NextResponse.next({ request: { headers } });
  res.headers.set('Content-Security-Policy', cspHeader);
  return res;
}
```

### E. Rust Tabanlı Hızlı Toolchain: Biome (`biome.json`)

```json
{
  "$schema": "https://biomejs.dev/schemas/1.9.4/schema.json",
  "vcs": { "enabled": true, "clientKind": "git", "useIgnoreFile": true },
  "organizeImports": { "enabled": true },
  "linter": {
    "enabled": true,
    "rules": {
      "recommended": true,
      "security": { "noDangerouslySetInnerHtml": "error" }
    }
  },
  "formatter": {
    "enabled": true,
    "indentStyle": "space",
    "indentWidth": 2,
    "lineWidth": 100
  }
}
```

---

## ⚠️ 3. Kaçınılması Gereken Anti-Pattern'lar

| Anti-Pattern | Neden Zararlı? | Doğru Kurumsal Yaklaşım |
| :--- | :--- | :--- |
| **`global.fetch = vi.fn()`** | HTTP header ve serialization doğrulamalarını atlar; kırılgan sahte sözleşmeler üretir. | Ağ seviyesinde çalışan MSW v2 handler'ları kullanın. |
| **Bileşen State'ini Test Etmek** | Refactoring sırasında testlerin bozulmasına yol açar (false negatives). | `getByRole` ile kullanıcının gördüğü çıktıyı doğrulayın. |
| **Playwright'ta `waitForTimeout`** | CI sürelerini uzatır ve ağ dalgalanmalarında flakiness yaratır. | Dahili auto-waiting ve `expect(locator).toBeVisible()` kullanın. |
| **CSP'de `'unsafe-inline'`** | Tüm XSS koruma kalkanını tamamen işlevsiz kılar. | Nonce-tabanlı Strict CSP v3 ve `'strict-dynamic'` kullanın. |
| **Server Modellerini Client'a Taşımak** | Parola hash'leri ve Stripe müşteri ID'leri istemci bundle'ına sızar. | `server-only`, React 19 Taint API ve DAL DTO projeksiyonları kullanın. |

---

## 📋 4. Doğrulama ve Kabul Kriterleri (Checklist)

- [ ] Tüm testler Vitest v2 ile koşuyor; Jest ve Babel bağımlılıkları temizlenmiş.
- [ ] React Testing Library testlerinde `getByRole` ve `userEvent.setup()` kullanılıyor.
- [ ] Ağ çağrıları MSW v2 ile mock'lanmış; `global.fetch = vi.fn()` bulunmuyor.
- [ ] Playwright E2E testlerinde keyfi bekleme (`sleep`) yok; oturumlar `storageState` ile korunuyor.
- [ ] Dinamik HTML render eden yerlerde DOMPurify + Trusted Types politikası uygulanıyor.
- [ ] Next.js SSR'da nonce-tabanlı Strict CSP v3 devrede (`'unsafe-inline'` yok).
- [ ] Sunucu modelleri `server-only` ve React 19 Taint API ile korunuyor; yalnızca DTO'lar aktarılıyor.
- [ ] Kod formatlama ve linting Biome 2.x ile yürütülüyor.
- [ ] CI pipeline'ında `@size-limit/preset-app` paket bütçesi denetimi aktif.
- [ ] Büyük mimari kararlar kod deposunda MADR formatında versiyonlanmış.
