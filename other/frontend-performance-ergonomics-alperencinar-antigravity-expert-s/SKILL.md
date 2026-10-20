---
name: frontend-performance-ergonomics
description: Use this skill to optimize runtime frontend performance and cross-platform ergonomics, tuning Core Web Vitals with INP under 200ms via LoAF and scheduler.yield(), adhering to React 19 Compiler rules, virtualizing lists with FlashList v2 cell recycling and TanStack Virtual v3, coordinating Android 15 edge-to-edge safe areas, and orchestrating 120fps keyboard controllers.
category: performance
tags:
  - performance
  - core-web-vitals
  - inp-optimization
  - react-compiler
  - flash-list-v2
  - android-15-edge-to-edge
  - clean-architecture
user-invocable: true
---

# Frontend Performance Engineering & Cross-Platform Ergonomics

Bu alt uzmanlık yeteneği; 2025–2026 kurumsal performans mühendisliğini, Core Web Vitals (INP $\le 200\text{ ms}$, LCP, CLS), React 19 Compiler kurallarını, Fabric mimarisi hücre geri dönüşümlü (cell recycling) liste sanallaştırmasını ve Android 15 / iOS ProMotion çapraz platform ergonomisini yönetir.

- **Ana Orkestratör Referansı:** [product-frontend-clean-architecture-development](../../SKILL.md)
- **Detaylı Sektör Araştırma Raporu:** [performance_ergonomics_architecture_deep_research.md](researches/performance_ergonomics_architecture_deep_research.md)

---

## 🚫 1. Katı Performans ve Ergonomi Kısıtlamaları (Enforced Guardrails)

1. **INP (Interaction to Next Paint) $\le 200\text{ ms}$ Bütçesi:**
   * Kullanıcı etkileşimlerinde ana iş parçacığı (main thread) 50 ms'den uzun süre kilitlenemez. Blokajlar Long Animation Frames (LoAF) API ile izlenmeli, ağır döngüler `scheduler.yield()` ile bölünmeli, CPU-yoğun işler Comlink ile Web Worker'lara aktarılmalıdır.
2. **React 19 Compiler Uyumluğu & Manuel Memoization Yasağı:**
   * React 19 Compiler aktifken bileşenlere gereksiz `useMemo`, `useCallback` ve `React.memo` yazılması anti-pattern'dir. Derleyicinin `useMemoCache` optimizasyonunu bozmamak için "Rules of React" (saf bileşenler, render anında sıfır mutasyon) eksiksiz uygulanmalıdır.
3. **`FlatList` Kesin Yasağı & Sanallaştırma Standardı:**
   * React Native'de bellek çalkantısına (memory churn) yol açan eski `FlatList` kesinlikle yasaktır; New Architecture (Fabric) destekli **`@shopify/flash-list v2`** zorunludur. Web tarafında ise **TanStack Virtual v3** kullanılmalıdır.
4. **Android 15 (SDK 35+) Zorunlu Edge-to-Edge Standardı:**
   * Sistem durum çubuğu ve jest navigasyon çubuğu şeffaf olduğu için React Native dahili `SafeAreaView` bileşeni yasaktır; **`react-native-safe-area-context`** (`useSafeAreaInsets`) zorunludur.
5. **Klavye Titreme Yasağı (Keyboard Controller):**
   * Android 15 Edge-to-Edge modunda input'u klavyenin arkasında bırakan eski `KeyboardAvoidingView` yasaktır; Reanimated UI-thread worklet'leri ile 120 FPS akıcı çalışan **`react-native-keyboard-controller`** kullanılmalıdır.
6. **Dokunma ve Haptic Ergonomisi:**
   * Dokunmatik hedefler mobil cihazlarda asgari $44\times44\text{ pt}$ / $48\times48\text{ dp}$, web'de asgari $24\times24\text{ px}$ olmalıdır. Küçük ikonlar `hitSlop` ile genişletilmeli; seçim ve tıklamalarda `expo-haptics` kullanılmalıdır.

---

## 🏛️ 2. Temel Mimari Yapı Taşları ve Kod Şablonları

### A. LoAF Telemetri ve `yieldToMain` Görev Parçalama (Web)

```typescript
// performance/yieldToMain.ts
export async function yieldToMain(): Promise<void> {
  if ('scheduler' in window && typeof (window as any).scheduler.yield === 'function') {
    return (window as any).scheduler.yield();
  }
  // 0-clamp MessageChannel macrotask devri (setTimeout yerine)
  return new Promise((resolve) => {
    const channel = new MessageChannel();
    channel.port1.onmessage = () => resolve();
    channel.port2.postMessage(null);
  });
}

// Ağır döngüyü INP bütçesi (< 16ms frame) içinde yürütme
export async function processInChunks<T>(items: T[], fn: (item: T) => void) {
  let lastYield = performance.now();
  for (const item of items) {
    fn(item);
    if (performance.now() - lastYield > 16) {
      await yieldToMain();
      lastYield = performance.now();
    }
  }
}
```

### B. Mobil Liste: `@shopify/flash-list v2` Yüksek Hızlı Akış

```tsx
// components/FeedList.tsx
import React, { useCallback } from 'react';
import { View, Text, StyleSheet, Dimensions } from 'react-native';
import { FlashList, ListRenderItem } from '@shopify/flash-list';
import * as Haptics from 'expo-haptics';

interface FeedItem {
  id: string;
  title: string;
}

const { height: SCREEN_HEIGHT } = Dimensions.get('window');

const FeedCard = React.memo(({ item }: { item: FeedItem }) => (
  <View style={styles.card}>
    <Text style={styles.title}>{item.title}</Text>
  </View>
));

export function FeedList({ data }: { data: FeedItem[] }) {
  const renderItem: ListRenderItem<FeedItem> = useCallback(
    ({ item }) => <FeedCard item={item} />,
    []
  );

  return (
    <FlashList
      data={data}
      renderItem={renderItem}
      keyExtractor={(item) => item.id}
      // Boş alanları (blank spaces) sıfırlayan pre-warming tamponu
      drawDistance={SCREEN_HEIGHT * 1.5}
      showsVerticalScrollIndicator={false}
      // v2'de estimatedItemSize zorunluluğu kalkmıştır; Fabric senkron ölçer
    />
  );
}

const styles = StyleSheet.create({
  card: { padding: 16, margin: 8, minHeight: 48, backgroundColor: '#fff', borderRadius: 8 },
  title: { fontSize: 16, fontWeight: '600' },
});
```

### C. Android 15 Edge-to-Edge & Frame-Perfect Klavye Formu

```tsx
// screens/ChatInputScreen.tsx
import React from 'react';
import { StyleSheet, TextInput, View, Platform } from 'react-native';
import { KeyboardGestureArea, useKeyboardHandler } from 'react-native-keyboard-controller';
import Animated, { useSharedValue, useAnimatedStyle } from 'react-native-reanimated';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

export function ChatInputScreen() {
  const insets = useSafeAreaInsets();
  const keyboardHeight = useSharedValue(0);

  // UI Thread üzerinde 120 FPS senkronize çalışan klavye kancası
  useKeyboardHandler({
    onMove: (e) => {
      'worklet';
      keyboardHeight.value = e.height;
    },
    onInteractive: (e) => {
      'worklet';
      keyboardHeight.value = e.height; // Parmağın kaydırma hareketini 1:1 takip eder
    },
  }, []);

  const animatedStyle = useAnimatedStyle(() => {
    const baseOffset = keyboardHeight.value > 0 ? 0 : insets.bottom;
    return {
      transform: [{ translateY: -Math.max(keyboardHeight.value, 0) }],
      paddingBottom: baseOffset + 8,
    };
  });

  return (
    <View style={styles.container}>
      <KeyboardGestureArea interpolator="ios" style={{ flex: 1 }}>
        <View style={{ flex: 1, paddingTop: insets.top }} />
      </KeyboardGestureArea>

      <Animated.View style={[styles.inputBar, animatedStyle]}>
        <TextInput placeholder="Mesaj yazın..." style={styles.input} />
      </Animated.View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#F9FAFB' },
  inputBar: { backgroundColor: '#fff', borderTopWidth: 1, borderColor: '#eee', padding: 12 },
  input: { height: 44, backgroundColor: '#F3F4F6', borderRadius: 22, paddingHorizontal: 16 },
});
```

### D. Web Dinamik Sanallaştırma: TanStack Virtual v3

```tsx
// components/WebVirtualList.tsx
import React, { useRef } from 'react';
import { useVirtualizer } from '@tanstack/react-virtual';

export function WebVirtualList({ items }: { items: { id: string; text: string }[] }) {
  const parentRef = useRef<HTMLDivElement>(null);

  const virtualizer = useVirtualizer({
    count: items.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 50,
    overscan: 4, // Beyaz flaşları önleyen DOM tamponu
  });

  return (
    <div ref={parentRef} style={{ height: '500px', overflowY: 'auto', contain: 'strict' }}>
      <div style={{ height: `${virtualizer.getTotalSize()}px`, position: 'relative' }}>
        {virtualizer.getVirtualItems().map((vRow) => (
          <div
            key={vRow.key}
            data-index={vRow.index}
            ref={virtualizer.measureElement} // Dinamik ResizeObserver ölçümü
            style={{
              position: 'absolute',
              top: 0,
              left: 0,
              width: '100%',
              transform: `translateY(${vRow.start}px)`,
              padding: '12px',
              borderBottom: '1px solid #eee',
              minHeight: '24px', // WCAG 2.2 AA 24px kuralı
            }}
          >
            {items[vRow.index].text}
          </div>
        ))}
      </div>
    </div>
  );
}
```

---

## ⚠️ 3. Kaçınılması Gereken Anti-Pattern'lar

| Anti-Pattern | Neden Zararlı? | Doğru Kurumsal Yaklaşım |
| :--- | :--- | :--- |
| **`FlatList` Kullanımı** | Windowing sürekli mount/unmount eder; 120 Hz panellerde beyaz alan ve lag yaratır. | `@shopify/flash-list v2` (Fabric Cell Recycling) kullanın. |
| **Android'de `KeyboardAvoidingView`** | Android 15 Edge-to-Edge altında hesaplamaları şaşırır, input'u klavyenin arkasında bırakır. | Reanimated tabanlı `react-native-keyboard-controller` kullanın. |
| **React Compiler varken Manuel Memo** | Gereksiz closure ve runtime dizi karşılaştırma ek yükü yaratır. | Saf bileşen yazın; optimizasyonu derleyiciye bırakın. |
| **LCP Görselinde `loading="lazy"`** | Görsel indirmesini 1 saniyeden fazla geciktirerek LCP skorunu çökertir. | LCP görseline `fetchpriority="high"` ve `decoding="async"` verin. |
| **Küçük Dokunma Hedefleri** | $44\times44\text{ pt}$ altındaki alanlar yanlış basımlara ve zayıf erişilebilirliğe yol açar. | `hitSlop` ile fiziksel basma alanını genişletin ve haptic ekleyin. |

---

## 📋 4. Doğrulama ve Kabul Kriterleri (Checklist)

- [ ] Web INP skoru 200 ms altında; uzun döngüler `scheduler.yield()` ile parçalanıyor.
- [ ] React 19 Compiler aktif projelerde manuel `useMemo`/`useCallback` kullanılmıyor; render saflığı korunuyor.
- [ ] LCP görselinde `fetchpriority="high"` aktif; `loading="lazy"` kaldırılmış.
- [ ] Tüm görsellerde CLS'i sıfırlamak için CSS `aspect-ratio` tanımlı.
- [ ] React Native listelerinde `FlatList` kesinlikle yok; `@shopify/flash-list v2` kullanılıyor.
- [ ] Android 15 için `edgeToEdgeEnabled: true` ve `useSafeAreaInsets()` aktif.
- [ ] Form ve chat ekranlarında `react-native-keyboard-controller` kullanılıyor.
- [ ] Dokunma hedefleri asgari $44\times44\text{ pt}$ ($hitSlop$ dahil) ve `expo-haptics` ile destekleniyor.
