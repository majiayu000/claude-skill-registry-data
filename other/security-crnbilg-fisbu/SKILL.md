---
name: security
description: Güvenlik kurallarını (auth, injection, secret yönetimi gibi) tanımlar; architect, fullstack-dev, reviewer ve devops tarafından kullanılır.
---

## Güvenlik Kontrol Listesi
Kod incelenirken şu güvenlik risklerine bakılır:
- Yetkisiz erişim (bir kullanıcının başkasının verisine erişebilmesi)
- SQL/veri enjeksiyonu
- Secret sızıntısı (kod içine gömülmüş şifre/token)

## Secret Yönetimi
`.env` dosyası `.gitignore`'a eklenir ve hiçbir zaman commit edilmez. Hiçbir secret (şifre, token, API key) koda veya git geçmişine gömülmez.

## Yetkilendirme Kuralı
Her endpoint, isteği yapan kullanıcının o kaynağa erişim yetkisi olup olmadığını kontrol eder. Yetkisiz erişimde, kaynağın varlığını sızdırmamak için bazen 403 yerine 404 dönülebilir (güvenlik açısından daha az bilgi verir).

## Auth Mimarisi Kararı
Kimlik doğrulama yöntemi (JWT, cookie session gibi) seçilirken güvenlik, ölçeklenebilirlik ve mobil uyumluluk birlikte değerlendirilir. Bu, geri dönüşü zor bir karar olduğu için ADR olarak kaydedilir.
