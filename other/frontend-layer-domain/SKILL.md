---
name: frontend-layer-domain
description: Use this skill to design and implement framework-agnostic frontend domain layers, authoring pure TypeScript entities with nominal branded types, runtime validation schemas (Zod v4/TypeBox), railway-oriented Result pattern error handling, pure calculation engines, and deterministic state machines (XState v5/FSM).
category: architecture
tags:
  - domain-layer
  - clean-architecture
  - branded-types
  - result-pattern
  - state-machines
  - zod-schemas
user-invocable: true
---

# Frontend Domain Layer Architecture & Invariant Modeling

Bu alt uzmanlık yeteneği; Clean Architecture'ın en iç çekirdeği olan **Domain Katmanı (İş Mantığı, Varlıklar, Değer Nesneleri ve Durum Makineleri)** mimarisini yönetir. UI, React reaktivitesi ve ağ altyapısından tamamen bağımsız, saf TypeScript iş modelleri ve deterministik mantık kuralları inşa eder.

- **Ana Orkestratör Referansı:** [product-frontend-clean-architecture-development](../../SKILL.md)
- **Detaylı Sektör Araştırma Raporu:** [domain_layer_architecture_deep_research.md](researches/domain_layer_architecture_deep_research.md)

---

## 🚫 1. Katı Mimari Kurallar ve Kısıtlamalar (Enforced Guardrails)

1. **Framework & DOM Bağımsızlığı (Absolute Isolation):**
   * Domain ve Use Case dosyalarında `import React`, `use...` hook'ları, JSX veya tarayıcı API'leri (`window`, `document`, `localStorage`, `sessionStorage`, `fetch`, `navigator`) KESİNLİKLE bulunamaz.
   * Tüm mantık, tarayıcı taklidine (JSDOM) gerek kalmadan saf Node.js / Vitest çalışma ortamında milisaniyeler içinde test edilebilmelidir.
2. **Primitive Obsession Yasağı & Nominal Tip Güvenliği:**
   * Tüm ID'ler (`UserId`, `OrderId`) ve birim değerleri (`Money`, `Cents`) ham `string` veya `number` olarak tanımlanamaz; mutlaka `unique symbol` tabanlı **Branded Types** kullanılmalıdır.
3. **Sıfır `throw new Error()` Kuralı (Railway-Oriented Programming):**
   * Domain modelleri ve use case fonksiyonları beklenmeyen çökmeler (panic) haricinde exception fırlatamaz. Beklenen iş kuralı dallanmaları **`neverthrow` (`Result<T, E>`)** veya `ResultAsync` ile açıkça tiplenmiş olarak döndürülmelidir.
4. **Değişmezlik (Immutability):**
   * Domain entity ve value object nesneleri in-place mutasyona uğratılamaz; her işlem `Object.freeze` ile korunan yeni bir immutable kopya üretir.
5. **"Boolean Soup" Yasağı:**
   * Birbirine bağlı 3 veya daha fazla boolean bayrak (`isLoading`, `isError`, `isSuccess`, `isSubmitting`) yerine, imkansız durum kombinasyonlarını engelleyen **Deterministik Durum Makineleri (FSM / XState v5)** kullanılmalıdır.
6. **Finansal Tamsayı Kuralı:**
   * Para hesaplamalarında kayan noktalı sayı (floating point IEEE 754) aritmetiği kullanılamaz; tutarlar en küçük birimde (sent/kuruş) tam sayı (`integer`) olarak modellenmelidir.

---

## 🏛️ 2. Temel Mimari Yapı Taşları ve Kod Şablonları

### A. Branded Types ve Akıllı Oluşturucular (Smart Constructors)

TypeScript'in yapısal (structural) tip sisteminden kaynaklanan ID çapraz atama hatalarını engellemek için sıfır çalışma zamanı maliyetli nominal tipler:

```typescript
// domain/shared/brand.ts
declare const __brand: unique symbol;

export type Brand<T, TBrand extends string> = T & {
  readonly [__brand]: TBrand;
};

export type UserId = Brand<string, 'UserId'>;
export type OrderId = Brand<string, 'OrderId'>;
export type UsdCents = Brand<number, 'UsdCents'>;

export function createUserId(raw: string): UserId {
  if (!raw.startsWith('usr_') || raw.length < 10) {
    throw new Error(`Geçersiz UserId formatı: ${raw}`);
  }
  return raw as UserId;
}

export function createUsdCents(raw: number): UsdCents {
  if (!Number.isInteger(raw) || raw < 0) {
    throw new Error(`Sent değeri tam sayı ve pozitif olmalıdır: ${raw}`);
  }
  return raw as UsdCents;
}
```

### B. Değer Nesnesi (Value Object): Değişmez `Money` Modeli

```typescript
// domain/money/Money.ts
import { UsdCents, createUsdCents } from '../shared/brand';

export type Currency = 'USD' | 'EUR' | 'TRY';

export class Money {
  readonly amount: UsdCents;
  readonly currency: Currency;

  private constructor(amount: UsdCents, currency: Currency) {
    this.amount = amount;
    this.currency = currency;
    Object.freeze(this);
  }

  public static fromCents(cents: number, currency: Currency = 'USD'): Money {
    return new Money(createUsdCents(cents), currency);
  }

  public add(other: Money): Money {
    if (this.currency !== other.currency) {
      throw new Error(`Para birimleri uyuşmuyor: ${this.currency} !== ${other.currency}`);
    }
    return new Money((this.amount + other.amount) as UsdCents, this.currency);
  }

  public subtract(other: Money): Money {
    if (this.currency !== other.currency) {
      throw new Error(`Para birimleri uyuşmuyor: ${this.currency} !== ${other.currency}`);
    }
    const diff = this.amount - other.amount;
    if (diff < 0) throw new Error('Bakiye negatife düşemez.');
    return new Money(diff as UsdCents, this.currency);
  }

  public equals(other: Money): boolean {
    return this.amount === other.amount && this.currency === other.currency;
  }
}
```

### C. Tipli Domain Hataları ve Demiryolu Yönelimli Use Case

```typescript
// domain/errors/CheckoutErrors.ts
import { Money } from '../money/Money';

export type CheckoutDomainError =
  | { readonly _tag: 'InsufficientFundsError'; readonly currentBalance: Money; readonly requiredAmount: Money }
  | { readonly _tag: 'CouponExpiredError'; readonly couponCode: string; readonly expiredAt: Date }
  | { readonly _tag: 'ProductOutOfStockError'; readonly productId: string; readonly availableQuantity: number }
  | { readonly _tag: 'OrderNotInDraftStateError'; readonly currentStatus: string };
```

```typescript
// usecases/ProcessCheckoutUseCase.ts
import { Result, ResultAsync, ok, err, safeTry } from 'neverthrow';
import { Order, OrderId, UserId } from '../domain/order/Order';
import { Money } from '../domain/money/Money';
import { CheckoutDomainError } from '../domain/errors/CheckoutErrors';

export interface PaymentGatewayPort {
  charge(userId: UserId, amount: Money): ResultAsync<string, CheckoutDomainError>;
}

export interface InventoryPort {
  reserveStock(orderId: OrderId): ResultAsync<void, CheckoutDomainError>;
}

export class ProcessCheckoutUseCase {
  constructor(
    private readonly paymentGateway: PaymentGatewayPort,
    private readonly inventory: InventoryPort
  ) {}

  public execute(order: Order, couponCode?: string): ResultAsync<Order, CheckoutDomainError> {
    return safeTry(async function* (this: ProcessCheckoutUseCase) {
      if (order.status !== 'DRAFT') {
        return err<Order, CheckoutDomainError>({
          _tag: 'OrderNotInDraftStateError',
          currentStatus: order.status,
        });
      }

      // Asenkron adımlar (Hata anında doğrudan early-return yapar)
      yield* this.inventory.reserveStock(order.id);
      yield* this.paymentGateway.charge(order.customerId, order.total);

      order.markAsPaid();
      return ok(order);
    }.bind(this));
  }
}
```

### D. Saf Hesaplama Motoru (Pure Pricing Engine) & JSDOM'suz Vitest

```typescript
// domain/pricing/pricingEngine.ts
import { Money, toMoney } from '../money/Money';

export interface PricingRule {
  readonly tierThreshold: number;
  readonly discountPercentage: number;
}

export interface CalculationInput {
  readonly unitPrice: Money;
  readonly quantity: number;
  readonly tieredRules: readonly PricingRule[];
  readonly taxRate: number; // örn: 0.20
}

export function calculateOrderSummary(input: CalculationInput) {
  const rawSubtotal = input.unitPrice.amount * input.quantity;

  const activeTier = [...input.tieredRules]
    .sort((a, b) => b.tierThreshold - a.tierThreshold)
    .find((r) => input.quantity >= r.tierThreshold);

  const discountRate = activeTier ? activeTier.discountPercentage / 100 : 0;
  const discountAmount = Math.round(rawSubtotal * discountRate);
  const taxableAmount = rawSubtotal - discountAmount;
  const taxAmount = Math.round(taxableAmount * input.taxRate);
  const total = taxableAmount + taxAmount;

  return {
    subtotal: Money.fromCents(rawSubtotal),
    discountAmount: Money.fromCents(discountAmount),
    taxAmount: Money.fromCents(taxAmount),
    total: Money.fromCents(total),
  };
}
```

### E. Deterministik Durum Makineleri (FSM & XState v5)

```typescript
// machines/authMachine.ts (Sıfır bağımlılık Discriminated Union FSM)
export type AuthState =
  | { readonly status: 'unauthenticated' }
  | { readonly status: 'authenticating'; readonly email: string }
  | { readonly status: 'authenticated'; readonly token: string }
  | { readonly status: 'error'; readonly message: string };

export type AuthEvent =
  | { readonly type: 'LOGIN_SUBMIT'; readonly email: string }
  | { readonly type: 'LOGIN_SUCCESS'; readonly token: string }
  | { readonly type: 'LOGIN_FAILURE'; readonly error: string }
  | { readonly type: 'LOGOUT' };

export function authReducer(state: AuthState, event: AuthEvent): AuthState {
  switch (state.status) {
    case 'unauthenticated':
    case 'error':
      return event.type === 'LOGIN_SUBMIT' ? { status: 'authenticating', email: event.email } : state;
    case 'authenticating':
      if (event.type === 'LOGIN_SUCCESS') return { status: 'authenticated', token: event.token };
      if (event.type === 'LOGIN_FAILURE') return { status: 'error', message: event.error };
      return state;
    case 'authenticated':
      return event.type === 'LOGOUT' ? { status: 'unauthenticated' } : state;
    default: {
      const _exhaustive: never = state;
      return _exhaustive;
    }
  }
}
```

---

## ⚠️ 3. Kaçınılması Gereken Anti-Pattern'lar

| Anti-Pattern | Neden Zararlı? | Doğru Kurumsal Yaklaşım |
| :--- | :--- | :--- |
| **Primitive Obsession** | `UserId` ve `OrderId` birbirinin yerine geçebilir, derleyici uyarmadan hata oluşur. | `Brand<string, 'Tag'>` nominal damgalaması ve smart constructors kullanın. |
| **Floating-Point Para** | `0.1 + 0.2 = 0.30000000000000004` kuruş farkı ve finansal açık üretir. | Daima tamsayı (Cents/Kuruş) tabanlı `Money` Value Object kullanın. |
| **Hook Spaghetti / Logic in `useEffect`** | İş mantığı React render döngüsüne hapsolur; test edilemez ve taşınamaz. | İş mantığını saf interactor sınıflarına taşıyın; hook sadece UI adaptörü olsun. |
| **Boolean Soup** | $2^N$ imkansız durum kombinasyonu (hem loading hem error gibi) yarış durumu yaratır. | Sonlu durum makineleri (FSM) veya XState v5 ile deterministik modelleme yapın. |
| **Görünmez İstisnalar (`throw`)** | Hata imzası kaybolur, çağıran bileşen neyin patlayacağını bilemez. | `neverthrow` (`Result<T, E>`) ve `_tag` ayrık tipleriyle açık hata döndürün. |

---

## 📋 4. Doğrulama ve Kabul Kriterleri (Checklist)

- [ ] Domain modellerinde veya use case fonksiyonlarında hiçbir React veya tarayıcı API'si bulunmuyor.
- [ ] Tüm entity ID'leri nominal Branded Type (`Brand<string, 'EntityName'>`) olarak damgalanmış.
- [ ] Finansal ve parasal alanlar tamsayı (sent/kuruş) `Money` sınıfı ile modellenmiş.
- [ ] Use Case fonksiyonları exception fırlatmıyor; `Result<T, DomainError>` döndürüyor.
- [ ] Dış veri doğrulamalarında Zod v4 (`@zod/mini`) veya TypeBox kullanılıyor.
- [ ] Çok adımlı akışlar "Boolean Soup" yerine deterministik FSM durum geçişleriyle yönetiliyor.
- [ ] Birim testler JSDOM gerektirmeden saf Vitest Node.js ortamında çalışıyor.
