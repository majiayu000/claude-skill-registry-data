---
name: frontend-layer-infrastructure
description: Use this skill to design and implement robust frontend infrastructure and data layers, abstracting type-safe API clients, enforcing Anti-Corruption Layer (ACL) DTO mappers, resolving 401 refresh token race conditions with single-flight mutexes, orchestrating TanStack Query v5 cache with optimistic rollback, and configuring secure storage (BFF HttpOnly cookies, Expo SecureStore, and encrypted MMKV).
category: architecture
tags:
  - infrastructure
  - data-layer
  - api-repositories
  - data-mappers
  - tanstack-query
  - secure-storage
  - clean-architecture
user-invocable: true
---

# Frontend Infrastructure & Data Layer Architecture

Bu alt uzmanlık yeteneği; Clean Architecture'ın **Altyapı ve Veri Katmanı (Infrastructure / Data Layer)** prensiplerini, dış dünya entegrasyonlarını, tip güvenli API istemcilerini, Anti-Corruption Layer (ACL) DTO haritalayıcılarını, TanStack Query v5 önbellek yaşam döngüsünü ve güvenli depolama adaptörlerini yönetir.

- **Ana Orkestratör Referansı:** [product-frontend-clean-architecture-development](../../SKILL.md)
- **Detaylı Sektör Araştırma Raporu:** [infrastructure_layer_architecture_deep_research.md](researches/infrastructure_layer_architecture_deep_research.md)

---

## 🚫 1. Katı Mimari Kurallar ve Kısıtlamalar (Enforced Guardrails)

1. **Sıfır DTO Sızıntısı (Strict Anti-Corruption Layer):**
   * Backend'den dönen ham JSON yanıtları (`snake_case` alanlar, ilişkisel yabancı anahtarlar) doğrudan Presentation veya Domain katmanına verilemez. Her DTO, Altyapı katmanındaki bir Data Mapper ile Domain Entity'sine çevrilmelidir.
2. **Repository Soyutlaması & Doğrudan İstemci Çağrısı Yasağı:**
   * UI bileşenleri ham `fetch` veya Axios instance'ı çağıramaz. Tüm veri erişimleri `OrderRepository`, `UserRepository` gibi sözleşmeler (Ports) üzerinden yürütülmelidir.
3. **Tek Uçuşlu (Single-Flight) 401 Token Yenileme Koruması:**
   * Paralel giden istekler aynı anda `401 Unauthorized` aldığında birden fazla refresh isteği fırlatılamaz. Tek bir `refreshPromise` memoize edilmeli ve diğer istekler bu vaadi beklemelidir.
4. **TanStack Query v5 Katman İzolasyonu:**
   * Domain ve Altyapı katmanlarında hiçbir React Query hook'u (`useQuery`, `useMutation`) bulunamaz. TanStack Query yalnızca **Presentation Adapters (`queryOptions`)** ve UI hook'larında yer alır.
5. **Geri Alma Garantili (Rollback) Optimistic UI:**
   * Anlık UI güncellemelerinde (beğeni, sepet artırımı), `onMutate` aşamasında önbellek snapshot'ı alınmalı ve `onError` durumunda deterministik olarak geri yüklenmelidir.
6. **Web ve Mobil Güvenli Depolama Standartları:**
   * Web tarafında hassas JWT/Refresh token'lar `localStorage`'da ASLA saklanamaz (XSS riski); BFF mimarisi ve `HttpOnly; Secure; SameSite=Strict` çerezleri zorunludur.
   * Mobil/Expo tarafında `AsyncStorage` yerine donanımsal `expo-secure-store` ve şifreli `react-native-mmkv` hibrit modeli kullanılmalıdır.

---

## 🏛️ 2. Temel Mimari Yapı Taşları ve Kod Şablonları

### A. Anti-Corruption Layer (ACL) Çift Yönlü Haritalama (`toDomain` & `toDTO`)

```typescript
// infrastructure/mappers/userMapper.ts
import { z } from 'zod';
import { UserProfile } from '../../domain/models/user';
import { UserId } from '../../domain/shared/brand';

export const UserDtoSchema = z.object({
  user_id: z.string().uuid(),
  first_name: z.string(),
  last_name: z.string(),
  is_active: z.union([z.literal(1), z.literal(0)]),
  registered_timestamp: z.number(),
});
export type UserDto = z.infer<typeof UserDtoSchema>;

export class UserMapper {
  public static toDomain(raw: unknown): UserProfile {
    const dto = UserDtoSchema.parse(raw); // "Parse, Don't Validate"
    return {
      id: dto.user_id as UserId,
      fullName: `${dto.first_name} ${dto.last_name}`.trim(),
      isActive: dto.is_active === 1,
      registeredAt: new Date(dto.registered_timestamp * 1000),
    };
  }

  public static toDTO(domain: UserProfile): Record<string, unknown> {
    const [firstName, ...rest] = domain.fullName.split(' ');
    return {
      user_id: domain.id,
      first_name: firstName,
      last_name: rest.join(' '),
      is_active: domain.isActive ? 1 : 0,
    };
  }
}
```

### B. Single-Flight Token Manager & Yetkili Fetch Adaptörü

```typescript
// infrastructure/http/tokenManager.ts
export class TokenManager {
  private static refreshPromise: Promise<string> | null = null;

  public static async getValidToken(
    refreshTokenFn: () => Promise<string | null>,
    saveTokensFn: (tokens: { accessToken: string }) => Promise<void>
  ): Promise<string> {
    if (this.refreshPromise) {
      return this.refreshPromise; // Devam eden tekil isteğe abone ol
    }

    this.refreshPromise = (async () => {
      try {
        const refreshToken = await refreshTokenFn();
        if (!refreshToken) throw new Error('Refresh token bulunamadı');

        const res = await fetch('https://api.example.com/v1/auth/refresh', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ refreshToken }),
        });

        if (!res.ok) throw new Error('Oturum süresi doldu');
        const data = await res.json();
        await saveTokensFn(data);
        return data.accessToken;
      } finally {
        this.refreshPromise = null; // Kilidi serbest bırak
      }
    })();

    return this.refreshPromise;
  }
}
```

### C. TanStack Query v5: Query Key Factory & `queryOptions`

```typescript
// presentation/adapters/queries/todoQueries.ts
import { queryOptions } from '@tanstack/react-query';
import { TodoRepository } from '../../../infrastructure/repositories/todoRepository';

export const todoKeys = {
  all: ['todos'] as const,
  lists: () => [...todoKeys.all, 'list'] as const,
  list: (filter: string) => [...todoKeys.lists(), { filter }] as const,
  details: () => [...todoKeys.all, 'detail'] as const,
  detail: (id: string) => [...todoKeys.details(), id] as const,
};

export const todoQueries = {
  list: (filter = 'all', repo: TodoRepository) =>
    queryOptions({
      queryKey: todoKeys.list(filter),
      queryFn: ({ signal }) => repo.getTodos(filter, signal),
      staleTime: 1000 * 60 * 2, // 2 dakika taze
    }),

  detail: (id: string, repo: TodoRepository) =>
    queryOptions({
      queryKey: todoKeys.detail(id),
      queryFn: ({ signal }) => repo.getTodoById(id, signal),
      staleTime: 1000 * 60 * 5,
      enabled: Boolean(id),
    }),
};
```

### D. Rollback Garantili Optimistic Update Mutasyonu

```typescript
// presentation/hooks/useToggleTodo.ts
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { todoKeys } from '../adapters/queries/todoQueries';
import { Todo } from '../../domain/models/todo';

export function useToggleTodo(todoRepo: TodoRepository) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (todo: Todo) => todoRepo.toggleTodo(todo.id, !todo.completed),
    onMutate: async (todo) => {
      // 1. İlgili sorguların devam eden fetch işlemlerini iptal et
      await queryClient.cancelQueries({ queryKey: todoKeys.all });

      // 2. Rollback için snapshot al
      const previousTodos = queryClient.getQueryData<Todo[]>(todoKeys.list('all'));

      // 3. İyimser güncelleme yap
      queryClient.setQueryData<Todo[]>(todoKeys.list('all'), (old = []) =>
        old.map((t) => (t.id === todo.id ? { ...t, completed: !t.completed } : t))
      );

      return { previousTodos };
    },
    onError: (_err, _todo, context) => {
      // 4. Hata durumunda snapshot'ı geri yükle (Rollback)
      if (context?.previousTodos) {
        queryClient.setQueryData(todoKeys.list('all'), context.previousTodos);
      }
    },
    onSettled: () => {
      // 5. Sunucuyla son durumu eşitle
      queryClient.invalidateQueries({ queryKey: todoKeys.all });
    },
  });
}
```

### E. Mobil (React Native / Expo) Hibrit Güvenli Depolama Mimarisi

```typescript
// infrastructure/storage/secureMmkvStorage.ts
import * as SecureStore from 'expo-secure-store';
import { MMKV } from 'react-native-mmkv';
import * as Crypto from 'expo-crypto';

const MMKV_KEY_ALIAS = 'app_mmkv_encryption_key';
let storageInstance: MMKV | null = null;

export async function getSecureStorage(): Promise<MMKV> {
  if (storageInstance) return storageInstance;

  let encryptionKey = await SecureStore.getItemAsync(MMKV_KEY_ALIAS);
  if (!encryptionKey) {
    const randomBytes = await Crypto.getRandomBytesAsync(32);
    encryptionKey = Array.from(randomBytes).map((b) => b.toString(16).padStart(2, '0')).join('');
    await SecureStore.setItemAsync(MMKV_KEY_ALIAS, encryptionKey, {
      keychainAccessible: SecureStore.WHEN_UNLOCKED_THIS_DEVICE_ONLY,
    });
  }

  storageInstance = new MMKV({
    id: 'secure-app-cache',
    encryptionKey,
  });

  return storageInstance;
}
```

---

## ⚠️ 3. Kaçınılması Gereken Anti-Pattern'lar

| Anti-Pattern | Neden Zararlı? | Doğru Kurumsal Yaklaşım |
| :--- | :--- | :--- |
| **DTO Sızıntısı (Leaky DTOs)** | Backend bir alanı değiştirdiğinde 40 UI bileşeni kırılır. | ACL Data Mapper sınıfı ile DTO'yu saf Domain Entity'sine çevirin. |
| **`useApi<T>` Jenerik Tuzağı** | TanStack Query'nin `select`, `staleTime`, `queryFn` ve tip çıkarımını baltalar. | Hiyerarşik `queryOptions` ve Query Key Factory kullanın. |
| **`localStorage`'da JWT Tutulması** | XSS veya 3. parti scriptler ile token'lar tek satırda çalınabilir. | Web'de BFF HttpOnly çerezleri; mobilde `expo-secure-store` kullanın. |
| **Paralel 401 Fırtınası** | 5 paralel istek aynı anda refresh atarak oturum iptaline yol açar. | Single-Flight Promise Memoization ile tek bir yenileme isteği işletin. |
| **Rollback'siz Optimistic UI** | Ağ hatasında ekran yanlış durumu göstermeye devam eder. | `onMutate (snapshot)` ve `onError (rollback)` ikilisini zorunlu kılın. |

---

## 📋 4. Doğrulama ve Kabul Kriterleri (Checklist)

- [ ] Hiçbir UI bileşeninde ham DTO veya snake_case alan kullanılmıyor; tüm veriler Mapper'dan geçiyor.
- [ ] UI bileşenleri doğrudan `fetch` veya Axios çağırmıyor; Repository arayüzleri tüketiliyor.
- [ ] 401 durumunda paralel isteklerin hepsi tek bir refresh promise'ine bağlanıyor.
- [ ] TanStack Query sorguları `queryOptions` ve hiyerarşik Query Key Factory ile tanımlanmış.
- [ ] Optimistic update yapılan tüm mutasyonlarda hata durumunda snapshot geri yükleme (rollback) mevcut.
- [ ] Web tarafında `localStorage` içinde oturum token'ı bulunmuyor (BFF HttpOnly çerezi aktif).
- [ ] Mobil/Expo tarafında `AsyncStorage` kullanılmıyor; donanımsal Keychain/Keystore ve AES şifreli MMKV kullanılıyor.
