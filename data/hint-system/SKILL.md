---
name: ctf-hint-system
description: Aşamalı CTF ipucu sistemi — takılan kullanıcıya seviyeli ipucu verir. Level 1 (nudge), Level 2 (direction), Level 3 (solution). Her challenge için hint seviyesi ~/.fetih/ctf_hints.json'da takip edilir.
category: ctf
triggers:
  - "ipucu ver"
  - "hint me"
  - "give me a hint"
  - "takıldım"
  - "stuck"
  - "bunu çözemedim"
  - "nasıl ilerleyeceğim"
  - "yardım et"
tags:
  - ctf
  - hint
  - learning
  - coaching
---

# CTF Hint System

Aşamalı ipucu sistemi — kullanıcıyı çözüme yönlendirir ama hemen cevabı söylemez.

## Model

Her CTF challenge için 3 seviyeli ipucu:

| Seviye | Adı | Ne Verir | Kullanım |
|--------|-----|----------|----------|
| 1 | Nudge | Genel yönlendirme, kategori ipucu | `/hint` |
| 2 | Direction | Spesifik teknik, hangi araca/zafiyete bakılacağı | `/hint more` |
| 3 | Solution | Çözüm yolu, komutlar, flag formatı | `/hint solution` |

## Durum Takibi

Her challenge için hint seviyesi `~/.fetih/ctf_hints.json` dosyasında tutulur:

```json
{
  "challenges": {
    "web-basit-login": {
      "name": "Basit Login",
      "category": "web",
      "hint_level": 2,
      "hints_given": ["Level 1: SQL injection olabilir...", "Level 2: UNION SELECT dene..."],
      "solved": false,
      "started_at": "2026-05-29T12:00:00Z"
    }
  }
}
```

## Komutlar

- `/hint` — Level 1 ipucu (genel yönlendirme)
- `/hint more` — Level 2 ipucu (teknik yön)
- `/hint solution` — Level 3 çözüm
- `/hint status` — Mevcut hint seviyesini ve ilerlemeyi göster
- `/hint reset` — Tüm hint seviyelerini sıfırla (baştan başla)

## İpucu Stratejisi

### Level 1 (Nudge) — Genel Yönlendirme
Challenge kategorisini ve genel yaklaşımı söyle, spesifik teknik verme.

Örnekler:
- "Bu bir SQL injection challenge'ı. Input validasyonuna odaklan."
- "Dosyada gizli veri var gibi görünüyor. Dosya yapısını incelemeyi dene."
- "Bu bir buffer overflow sorusu. Stack yapısını analiz et."
- "Şifreleme kullanılmış. Kullanılan algoritmayı tespit etmeye çalış."

### Level 2 (Direction) — Teknik Yön
Spesifik aracı, zafiyeti veya tekniği söyle.

Örnekler:
- "Login formundaki username alanına `' OR 1=1--` dene. SQL injection filtrelemesi zayıf."
- "Dosyanın son 256 byte'ına bak. PKZIP header'ından sonra gizli veri var."
- "EIP'yi kontrol edebiliyorsun. Offset'i bulmak için pattern_create kullan."
- "XOR ile şifrelenmiş. Anahtar muhtemelen tek byte. Frekans analizi yap."

### Level 3 (Solution) — Çözüm
Tam çözüm yolunu ve komutları ver.

Örnekler:
- "`sqlmap -u 'http://target/login.php' --data='username=admin&password=x' --dbs` ile veritabanlarını listele. `users` tablosundan admin şifresini al."
- "`dd if=challenge.bin bs=1 skip=256 | file -` ile gizli dosyayı çıkar. Çıkan zip'in içinde flag.txt var."
- "Offset 140'da EIP kontrolü var. `p32(win_func_addr)` ile return address'i overwrite et."
- "Single-byte XOR. `xortool -b -l 1 challenge.enc` ile brute-force et. Anahtar 0x55."

## Pivot Stratejisi

3 başarısız flag denemesinde:
1. Yaklaşımı tamamen değiştir (farklı tool, farklı zafiyet sınıfı)
2. Challenge'ı yeniden sınıflandır (belki kategori yanlış?)
3. Diğer CTF oyuncularının writeup'larını kontrol et (varsa)

## Önemli Kurallar

1. **Asla direkt flag'i söyleme.** Kullanıcı `/hint solution` yazsa bile çözüm yolunu anlat, flag formatını belirt ama flag'in kendisini yazma.
2. **İlerlemeyi takip et.** Kullanıcı bir aşamayı geçtiyse onu tebrik et.
3. **Öğrenmeyi teşvik et.** Her hint bir öğrenme fırsatı olarak sun.
4. **Sabırlı ol.** Kullanıcı gerçekten takılmışsa ve ilerleyemiyorsa yardım et.
---
## References
- [Hint Seviyeleri Rehberi](./references/hint-levels.md)
