---
name: refresh-token
description: 'Quy tắc JWT refresh token service trong SASUCO InvoiceEasy. Dùng khi: implement TokenRefreshService, auto refresh access token trước khi hết hạn, JWT decode client-side, smart scheduling với setTimeout (không dùng setInterval), login start service, logout stop service, retry logic tối đa 3 lần, cấu hình REFRESH_THRESHOLD 30 giây, JwtUtils decode.'
---

# JWT Refresh Token Service — SASUCO InvoiceEasy

## Tổng Quan

**JWT-based Smart Refresh Service (v2.0)** — Background service tự động làm mới access token trước khi hết hạn:

- ✅ Decode JWT client-side để lấy `exp` timestamp
- ✅ Schedule **một lần** `setTimeout` (KHÔNG dùng `setInterval`)
- ✅ Gọi API refresh DUY NHẤT khi token còn 30 giây
- ✅ Retry tối đa 3 lần nếu thất bại, sau đó logout

---

## File Structure

```
/shared/services/api/
├── TokenManager.ts           ← Hiện có — lưu/đọc tokens
├── TokenRefreshService.ts    ← NEW v2.0 — Smart scheduling
├── JwtUtils.ts               ← NEW — JWT decode utility
├── ApiClient.ts              ← Hiện có
└── index.ts                  ← Cập nhật export
```

---

## Configuration

```typescript
const CONFIG = {
  REFRESH_THRESHOLD: 30 * 1000,   // 30 giây trước khi hết hạn
  RETRY_DELAY: 5 * 1000,          // 5 giây giữa các retry
  MAX_RETRIES: 3,                  // Tổng số lần thử
}
```

---

## Service API

```typescript
class TokenRefreshService {
  static start(): void          // Gọi SAU KHI login thành công
  static stop(): void           // Gọi KHI logout
  static isRunning(): boolean
  static refreshNow(): Promise<boolean>  // Manual (debug)
  static getNextRefreshTime(): number | null
}
```

---

## Flow Chuẩn

```
LOGIN thành công
    ↓
Decode JWT → lấy exp
    ↓
delay = (exp - 30s) - now
    ↓
setTimeout(() => refreshToken(), delay)
    ↓
[Token còn 30 giây] setTimeout fires
    ↓
Gọi API /auth/refresh-token
    ↓
Thành công? → Lưu tokens mới → Schedule lại refresh
    ↓ Thất bại
Wait 5s → Retry (tối đa 3 lần)
    ↓ Hết retry
Logout user
```

---

## State Management

```typescript
interface ServiceState {
  timeoutId: NodeJS.Timeout | null  // setTimeout ID (KHÔNG phải interval)
  isRunning: boolean
  isRefreshing: boolean             // Mutex flag — ngăn concurrent refresh
  retryCount: number
  nextRefreshTime: number | null
  lastRefreshTime: number
}
```

---

## Nguyên Tắc Quan Trọng

- ✅ Dùng **`setTimeout`** — KHÔNG dùng `setInterval`
- ✅ Decode JWT client-side — KHÔNG gọi API kiểm tra token
- ✅ `isRefreshing` mutex — KHÔNG cho phép concurrent refresh
- ✅ `stop()` phải gọi `clearTimeout()` ngay lập tức khi logout
- ❌ KHÔNG check token bằng cách polling mỗi N giây

---

## Retry Logic (Loop-based, KHÔNG dùng đệ quy)

```typescript
// ✅ ĐúNG: Loop-based retry
let retried = 0
while (retried < CONFIG.MAX_RETRIES) {
  retried++
  await new Promise(resolve => setTimeout(resolve, CONFIG.RETRY_DELAY))
  const retrySuccess = await callRefreshApi()
  if (retrySuccess) {
    // Lưu tokens mới, schedule lại, reset retry count
    scheduleNextRefresh()
    state.retryCount = 0
    return
  }
}
// Hết retry → Logout user
AuthService.logout()

// ❌ SAI: Recursive retry (gây stack overflow)
async function performRefresh() {
  const success = await callRefreshApi()
  if (!success) performRefresh() // ❌
}
```

---

## Tích Hợp với AuthService

```typescript
// Sau khi login thành công:
const tokens = await AuthService.login(credentials)
TokenManager.saveTokens(tokens)
TokenRefreshService.start()  // Bắt đầu background service

// Khi logout:
TokenRefreshService.stop()   // Dừng service TRƯỚC khi clear tokens
TokenManager.clearTokens()
redirectToLogin()
```
