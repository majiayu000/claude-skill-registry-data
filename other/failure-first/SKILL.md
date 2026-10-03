---
name: failure-first
description: Hata senaryolarını önceden planlamayı ve kodda hataları düzgün yönetmeyi öğretir.
---

## Hata senaryosu kategorileri
Story yazarken, aşağıdaki kategorilerden en az 5 tanesini kapsayan hata senaryosu yazılmalı:
- **Geçersiz girdi** (örn: kullanıcı boş bir fiş adı gönderir)
- **Yetkisiz erişim** (örn: kullanıcı başkasının fişine erişmeye çalışır)
- **Ağ/timeout hatası** (örn: sunucuya istek zaman aşımına uğrar)
- **Boş veri** (örn: kullanıcının hiç fişi yoktur)
- **Eşzamanlılık** (örn: iki kullanıcı aynı fişi aynı anda silmeye çalışır)



## Hata yönetimi kuralı
Kod yazarken hatalar asla sessizce yutulmaz. Her hata:
- Loglanır (ne olduğu, ne zaman olduğu)
- Kullanıcıya anlaşılır, teknik detay içermeyen bir mesaj gösterilir
- Sessizce görmezden gelinmez (`catch (Exception) {}` gibi boş yakalama bloğu yasaktır)