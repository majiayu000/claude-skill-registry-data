---
name: frontend-layer-presentation
description: Use this skill to design, implement, and refactor presentation layer components across React, React Native, and Expo, enforcing the Orchestrator-Child pattern, cognitive complexity limits, thin route adapters, WAI-ARIA headless primitives, compound components with asChild slots, and semantic design tokens.
category: architecture
tags:
- presentation-layer
- orchestrator-pattern
- cognitive-complexity
- headless-ui
- compound-components
- route-adapters
user-invocable: true
---
# Frontend Presentation Layer Architecture

Bu alt uzmanlık yeteneği; Clean Architecture'ın **Sunum Katmanı (Presentation Layer)** prensiplerini, kullanıcı arayüzü modülerliğini, Headless UI entegrasyonunu, rota/ekran sınırlarını ve erişilebilirlik (WAI-ARIA) standartlarını yönetir.

*   **Ana Orkestratör:** [product-frontend-clean-architecture-development](../../SKILL.md)
*   **Derin Araştırma Raporu:** [presentation_layer_architecture_deep_research.md](researches/presentation_layer_architecture_deep_research.md)
*   **Master Mimari Raporu:** [senior_frontend_architecture_and_competencies_master_report.md](../../researches/senior_frontend_architecture_and_competencies_master_report.md)

---

## 🚫 1. KATİ MİMARİ KISITLAMALAR (MANDATORY RULES)

1. **Doğrudan Veri Çekme Yasağı (No Direct Fetching):**
   * Hiçbir UI bileşeni doğrudan API çağrısı (`fetch`, `axios`), Supabase sorgusu veya ham DTO dönüşümü yapamaz. Tüm veri akışı Domain/Infra katmanından (`useCustomHook`) veya props üzerinden aktarılmalıdır.
2. **Orchestrator / Child Ayrımı:**
   * Çok adımlı akışlarda (onboarding, checkout, form wizard) alt bileşenler bağımsız global navigasyonu (`router.push`) tetikleyemez. Olaylar `onSubmit(data)` veya `onComplete` callback'leri ile **Parent Orchestrator** bileşenine iletilir.
3. **Bilişsel Karmaşıklık & Satır Sınırı:**
   * Dosyalar maksimum **200 satır** ile sınırlandırılmalıdır.
   * **Cognitive Complexity (SonarJS) $\le 15$**, **Cyclomatic Complexity $\le 12$** ve mantıksal yuvalama derinliği $\le 3$ olmalıdır.
4. **İnce Route Adaptörü Kuralı (Thin Route Adapters):**
   * Expo Router veya Next.js App Router altındaki sayfa dosyaları (`app/**/*.tsx`) **30 satırı geçemez**. Bu dosyalar yalnızca URL parametrelerini okuyan ve Feature Orchestrator'a prop aktaran birer adaptördür; doğrudan CSS/stil veya ekran mantığı barındıramaz.
5. **Headless & Semantik Token Zorunluluğu:**
   * Modal, Popover veya Dropdown için sıfırdan `<div>` tabanlı arayüz yazılamaz; **Radix UI**, **Base UI** veya **React Aria** primitifleri kullanılmalıdır.
   * Ham renkler (`bg-blue-600`, `text-[#333]`) yasaktır; yalnızca semantik jetonlar (`bg-surface-primary`, `text-content-strong`) kullanılabilir.

---

## 🏛️ 2. MİMARİ PATTERNLER VE KOD STANDARTLARI

### 2.1. Parent Orchestrator & Discriminated Union Akış Deseni
Adım durumları tip-güvenli discriminated union ile modellenir; geçersiz durum kombinasyonları derleme zamanında engellenir:

```tsx
// features/checkout/types.ts
export type CheckoutFlowState =
  | { step: 'shipping'; data: Partial<ShippingAddress> }
  | { step: 'payment'; shipping: ShippingAddress; data: Partial<PaymentDetails> }
  | { step: 'review'; shipping: ShippingAddress; payment: PaymentDetails };
```

```tsx
// features/checkout/components/CheckoutOrchestrator.tsx
import React from 'react';
import { View, StyleSheet } from 'react-native';
import { useCheckoutOrchestrator } from '../hooks/useCheckoutOrchestrator';
import { ShippingStepView } from './steps/ShippingStepView';
import { PaymentStepView } from './steps/PaymentStepView';
import { ReviewStepView } from './steps/ReviewStepView';

export const CheckoutOrchestrator: React.FC = () => {
  const { state, isSubmitting, handleShipping, handlePayment, handleConfirm } =
    useCheckoutOrchestrator();

  return (
    <View style={styles.container}>
      {state.step === 'shipping' && (
        <ShippingStepView initialValues={state.data} onSubmit={handleShipping} />
      )}
      {state.step === 'payment' && (
        <PaymentStepView shipping={state.shipping} onSubmit={handlePayment} />
      )}
      {state.step === 'review' && (
        <ReviewStepView
          shipping={state.shipping}
          payment={state.payment}
          loading={isSubmitting}
          onConfirm={handleConfirm}
        />
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#FFFFFF' },
});
```

---

### 2.2. "Shotgun Surgery" Önleme: Logic-First Extraction
Bileşen 150 satırı aştığında körü körüne 5 küçük JSX dosyasına bölünmez (birlikte değişen şeylerin parçalanması "Shotgun Surgery" anti-pattern'ine yol açar).
* **Adım 1:** Hesaplama ve yan etkiler bir **Custom Hook**'a (`useFeatureLogic.ts`) taşınır.
* **Adım 2:** Veri dönüşümleri saf fonksiyonlara (`formatters.ts`) taşınır.
* **Adım 3:** Yalnızca bağımsız re-render sınırı veya tekrar kullanılabilirlik gerektiren yapraklar izole bileşene dönüştürülür.

---

### 2.3. İnce Route Adapter (Expo Router & Next.js Standardı)
Rota dosyası ekranın detayını bilmez; salt URL parametrelerini köprüler:

```tsx
// app/(app)/checkout/[id].tsx
import React from 'react';
import { useLocalSearchParams } from 'expo-router';
import { CheckoutOrchestrator } from '@/features/checkout/components/CheckoutOrchestrator';

export default function CheckoutRoute() {
  const { id } = useLocalSearchParams<{ id: string }>();
  if (!id) throw new Error('checkoutId parametresi eksik.');

  return <CheckoutOrchestrator checkoutId={id} />;
}
```

*Detaylı Auth Guard ve FOUC önleme desenleri için: [Bölüm 3: Route Boundaries](researches/presentation_layer_architecture_deep_research.md#bölüm-3-router-vs-screen-boundary-expo-router--nextjs-app-router)*

---

### 2.4. Compound Components ve Slot (`asChild`) Deseni
"Prop Soup" krizini önlemek ve WAI-ARIA erişilebilirliğini korumak için Compound bileşenler ve Radix Slot yapısı kullanılır:

```tsx
import * as React from 'react';
import * as DialogPrimitive from '@radix-ui/react-dialog';

export const Dialog = DialogPrimitive.Root;
export const DialogTrigger = DialogPrimitive.Trigger;

export const DialogContent = React.forwardRef<
  React.ElementRef<typeof DialogPrimitive.Content>,
  React.ComponentPropsWithoutRef<typeof DialogPrimitive.Content>
>(({ className, children, ...props }, ref) => (
  <DialogPrimitive.Portal>
    <DialogPrimitive.Overlay className="fixed inset-0 bg-black/50 backdrop-blur-sm" />
    <DialogPrimitive.Content
      ref={ref}
      className="fixed left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 bg-surface-elevated p-6 shadow-xl"
      {...props}
    >
      {children}
    </DialogPrimitive.Content>
  </DialogPrimitive.Portal>
));
DialogContent.displayName = 'DialogContent';
```

*Odak yönetimi (Focus Traps) ve Roving Tabindex için: [Bölüm 4: Headless Primitifleri](researches/presentation_layer_architecture_deep_research.md#bölüm-4-headless-ui-primitifleri-ve-wai-aria-mimarisi)*

---

### 2.5. Tailwind CSS v4 Semantik Jetonlar & Tip-Güvenli i18n
Ham renk paleti sınıfları kısıtlanır, yalnızca semantik token sınıfları üretilir:

```css
/* theme.css */
@import "tailwindcss";

@theme {
  --color-*: initial; /* Ham paleti sıfırla */
  --color-surface-base: var(--surface-base);
  --color-surface-elevated: var(--surface-elevated);
  --color-content-primary: var(--content-primary);
  --color-action-brand: var(--action-brand);
}
```

*Sıfır hardcoded metin ve ESLint kuralları için: [Bölüm 5: Tasarım Jetonları](researches/presentation_layer_architecture_deep_research.md#bölüm-5-tasarım-jetonları-ve-yerelleştirme-korkulukları)*

---

## 📋 3. UYGULAMA VE KOD DENETİM KONTROL LİSTESİ

Sunum katmanında herhangi bir kod yazılmadan veya incelenmeden önce aşağıdaki maddeler doğrulanmalıdır:

* [ ] **Bileşen Boyutu & Karmaşıklık:** Dosya $\le 200$ satır mı? Cognitive Complexity $\le 15$ mi?
* [ ] **Orchestrator İzolasyonu:** Alt bileşenler navigatörü doğrudan tetiklemek yerine `onSubmit` / `onAction` callback'i mi kullanıyor?
* [ ] **Route Adapter:** `app/` altındaki sayfa dosyası 30 satırın altında ve yalnızca parametre eşleme mi yapıyor?
* [ ] **Headless & A11y:** Modal/Dropdown/Tabs bileşenlerinde Radix UI veya Base UI primitifleri kullanıldı mı (Focus Trap, Esc desteği, ARIA rolleri)?
* [ ] **Compound Yapı:** 10'dan fazla prop alan monolitik yapılar Compound Component (`Dialog.Root`, `Dialog.Content`) desenine geçirildi mi?
* [ ] **Stil & Jetonlar:** Ham CSS/renkler yerine yalnızca `@theme` semantik sınıfları (`bg-surface-*`) kullanıldı mı?
* [ ] **Yerelleştirme:** JSX içinde hiçbir sabit metin bırakılmadan `t('module.key')` kullanıldı mı?
