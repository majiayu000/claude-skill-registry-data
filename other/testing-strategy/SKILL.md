---
name: testing-strategy
description: Dört test katmanının (unit/integration/component/E2E) amacını ve kullanım koşullarını tanımlar; qa ve fullstack-dev tarafından kullanılır.
---

## Unit Test
İş mantığı içeren her fonksiyon için yazılır. Dışarıdaki hiçbir sisteme (veritabanı, ağ) bağlı olmadan, sadece fonksiyonun kendi mantığını kontrol eder.

## Integration Test
API + veritabanı etkileşimi içeren akışlar için yazılır. Testler, in-memory (sahte) veritabanı değil, gerçek PostgreSQL'e karşı çalışır — ama production veritabanına değil, her test için oluşturulan geçici/izole bir veritabanına (Testcontainers ile).

## Component Test
Kullanıcı arayüzü bileşenleri için yazılır. Loading, error, empty, success durumlarının her biri ayrı ayrı test edilir.

## E2E Test
Sadece kritik kullanıcı akışları için yazılır (giriş, ana iş akışı gibi — örn. kayıt→login→fiş oluştur→kategoriye ata→bütçede yansıması). Her story için E2E yazılmaz — "bu akış gerçekten kritik mi" sorusu sorulup karar verilir. Backend ve mobil için ayrı araç ve kapsam kullanılır (E2E-001):

### Backend E2E
**Araç**: Testcontainers (PostgreSQL) + Spring Boot `@SpringBootTest(webEnvironment = RANDOM_PORT)` + `TestRestTemplate`.
- **Konum**: `backend/src/e2e/java/` — normal `src/test/java`'dan AYRI bir Gradle kaynak seti (`sourceSets.e2e`), sadece `./gradlew e2eTest` ile çalışır. Argümansız `./gradlew test`/`./gradlew build` bu testleri ASLA tetiklemez.
- **Neden Testcontainers**: gerçek bir Postgres'e (ephemeral, test bitince silinir) karşı çalışır — Flyway migration'ları (V1, V2, V3...) bu taze DB'ye gerçekten uygulanır, böylece migration'ların da doğru çalıştığı dolaylı olarak kanıtlanır. Canlı Supabase'e KESİNLİKLE bağlanılmaz.
- **Kapsam**: sadece gerçekten kritik, uçtan uca (controller→service→JPA→DB) akışlar — her endpoint için değil.
- Referans: `RegisterToBudgetFlowE2ETest.java` (register→verify-email→login→category→budget→receipt→budget'ta yansıma).

### Mobil E2E
**Araç**: `integration_test` paketi (Flutter'ın resmi, güncel çözümü — `flutter_driver` deprecated).
- **Konum**: `mobile/integration_test/`. Gerçek bir simulator/emulator'da (`flutter test integration_test/x_test.dart -d <device>`) gerçek widget'ları sürer — mock'lanmış hiçbir katman yok.
- **Backend bağımlılığı**: gerçek bir backend'e ihtiyaç duyar. Production Supabase'e KESİNLİKLE bağlanılmaz — yerel/ephemeral bir backend (Testcontainers/docker Postgres + `./gradlew bootRun`, env var override'larıyla) kullanılır. `ApiClient.baseUrl`, `--dart-define=API_BASE_URL=...` ile override edilebilir (varsayılan davranış — production URL — değişmez). **ARCH-007/ADR-003**: backend `/api/v1` context-path'i altında çalışıyor — override değeri de bu segmenti içermeli (`http://localhost:8090/api/v1` gibi), aksi halde tüm istekler 404 döner.
- **Android emulator notu**: host makinenin `localhost`'una `10.0.2.2` ile erişilir.
- **Native izin diyalogları**: bildirim izni gibi native Android/iOS diyalogları Flutter widget ağacının parçası DEĞİLDİR — `pump`/`pumpAndSettle` bunları göremez/geçemez. Otomasyon için izinler test kurulumunda önceden verilir (`adb shell pm grant <paket> <izin>`), production kodunda "izni geciktir" gibi bir hack yapılmaz.
- **Kapsam/perf gözlemi**: her kritik adımın süresi ölçülüp loglanır (bkz. `timedStep` deseni) — bir adım anormal derecede yavaşsa/donarsa test BAŞARISIZ OLMAZ (bu bir SLA testi değil) ama açıkça işaretlenir ve insan gözden geçirmesi için PERF-XXX olarak backlog'a not düşülür (bkz. PERF-004 — bu deseni kullanarak gerçek bir production donma sorunu bulundu).
- Referans: `receipt_to_budget_flow_test.dart` (login→fiş ekle→kategoriye ata→bütçede yansıma; "kayıt ol" adımı backend E2E'de kapsandığı için burada API ile önceden hazırlanır, UI'dan sürülmez — OTP e-posta okunamadığı için).