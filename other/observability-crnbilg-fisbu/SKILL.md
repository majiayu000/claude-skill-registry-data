---
name: observability
description: Loglama, correlation ID ve health check gibi gözlemlenebilirlik kurallarını tanımlar; architect, fullstack-dev ve devops tarafından kullanılır.
---
## Loglama Kuralı
Sistem çalışırken önemli olaylar (hata, kritik işlem) loglanır. Her log satırı, ne olduğunu ve ne zaman olduğunu içerir. Hassas veri (şifre, token) asla loglanmaz.

## Correlation ID
Her istek, benzersiz bir kod (correlation ID / traceId) taşır. Bu kod, isteğin sistem içinde baştan sona takip edilmesini sağlar. Bir hata oluştuğunda, bu kod kullanıcıya gösterilebilir ("destek için bu kodu iletin" gibi) — teknik detay değil, bir referans numarasıdır.

## Health Check
Sistem, "ben hâlâ çalışıyorum, sağlıklıyım" diye kendi kendini bildiren basit bir kontrol noktası sağlar. Bu, sistemin dışarıdan (örneğin devops tarafından) izlenebilmesini sağlar — henüz gerçek uygulama olmadığı için bu, şimdilik sadece mimari/kavramsal seviyede kalır.