---
name: cybersecurity-master-orchestrator
description: FETIH Siber Güvenlik Ana Orkestratörü — 912+ skill ile tüm siber güvenlik alanlarını kapsar. Tehdit avı, zararlı yazılım analizi, dijital adli bilişim, olay müdahalesi, bulut güvenliği, ağ güvenliği, web uygulama güvenliği, API güvenliği, sızma testi, red team, SOC operasyonları, OT/ICS güvenliği ve daha 25+ alt kategori. ljagiello/ctf-skills ve Eyadkelleh/awesome-claude-skills-security entegre edildi.
tags: [cybersecurity, siber-güvenlik, orchestrator, master, threat-hunting, malware-analysis, forensics, incident-response, cloud-security, network-security, pentest, red-team, soc, mitre-attack, nist-csf]
triggers:
  - "siber güvenlik"
  - "cybersecurity"
  - "güvenlik analizi"
  - "tehdit avı"
  - "zararlı yazılım"
  - "adli bilişim"
  - "forensics"
  - "olay müdahalesi"
  - "incident response"
  - "sızma testi"
  - "pentest"
  - "güvenlik denetimi"
  - "security audit"
  - "zafiyet taraması"
  - "vulnerability"
  - "tehdit istihbaratı"
  - "threat intelligence"
  - "cloud security"
  - "ağ güvenliği"
  - "SOC"
  - "SIEM"
  - "EDR"
  - "XDR"
  - "MITRE ATT&CK"
  - "NIST CSF"
  - "ISO 27001"
  - "seclists"
  - "wordlist"
  - "fuzzing payload"
  - "LLM security"
  - "prompt injection"
  - "jailbreak"
  - "bug bounty"
  - "pentest advisor"
  - "web shell detect"
  - "API key leak"
  - "XSS payload"
  - "SQL injection payload"
  - "password list"
adapted_for: fetih
---

# FETIH Siber Güvenlik Ana Orkestratörü

FETIH'in siber güvenlik operasyonlarını yürütürken başvurduğu ana katalog. **912+ özel skill** ile tüm siber güvenlik yaşam döngüsünü kapsar: tespit → analiz → müdahale → iyileştirme → önleme.

**Kapsam:** 32 alt kategori · 743 cybersecurity skill · 291 MITRE ATT&CK tekniği · 14/14 ATT&CK taktiği · NIST CSF uyumlu · ljagiello/ctf-skills & Eyadkelleh/awesome-claude-security entegrasyonu
> **Red Team skill'leri** (29 adet) → `skills/red-teaming/red-team-operations/` dizininde

---

## Kategori Rehberi

Bir siber güvenlik görevi geldiğinde, aşağıdaki tablodan ilgili kategoriyi belirle ve o kategorideki skill'leri yükle:

| # | Kategori | Skill | Açıklama |
|---|----------|-------|----------|
| 1 | **Tehdit Avı** | 63 | Proaktif tehdit arama, anomali tespiti, YARA/Sigma kuralları, SIEM/EDR sorguları |
| 2 | **Bulut Güvenliği** | 63 | AWS, Azure, GCP güvenlik denetimi, IAM, S3, bulut log analizi |
| 3 | **SOC Operasyonları** | 62 | SIEM yönetimi, alert triyajı, log yönetimi, vaka yönetimi, shift el kitabı, SecLists pattern-matching |
| 4 | **Tehdit İstihbaratı** | 50 | IOC analizi, tehdit aktörü profilleme, MISP, STIX/TAXII, APT takibi |
| 5 | **Web Uygulama Güvenliği** | 50 | OWASP Top 10, SQLi, XSS, CSRF, SSRF, WAF bypass, API güvenlik testi, SecLists fuzzing, bug bounty |
| 6 | **Ağ Güvenliği** | 43 | Nmap, Wireshark, IDS/IPS, firewall denetimi, ağ segmentasyonu, paket analizi |
| 7 | **Zararlı Yazılım Analizi** | 42 | Statik/dinamik analiz, sandbox, Ghidra, IDA, bellek forensik, unpacking, web shell tespiti |
| 8 | **Dijital Adli Bilişim** | 37 | Disk imajı, dosya sistemi, timeline, silinmiş dosya kurtarma, steganografi |
| 9 | **Kimlik ve Erişim Yönetimi** | 39 | IAM, MFA, SSO, PAM, Zero Trust, Azure AD/Entra ID, Active Directory, API key tarama, SecLists password/username |
| 10 | **OT/ICS Güvenliği** | 29 | SCADA, PLC, DCS, Modbus, endüstriyel kontrol sistemleri güvenliği |
| 11 | **Konteyner Güvenliği** | 29 | Docker, Kubernetes, container escape, image scanning, runtime security |
| 12 | **API Güvenliği** | 28 | REST/GraphQL güvenliği, OWASP API Top 10, OAuth2, JWT, rate limiting |
| 13 | **Olay Müdahalesi** | 26 | IR playbook, kontaminasyon, eradikasyon, kurtarma, post-mortem, iletişim |
| 14 | **Zafiyet Yönetimi** | 25 | CVSS, SSVC, patch yönetimi, zafiyet tarama, risk önceliklendirme |
| 15 | **Sızma Testi** | 23 | Metodoloji, raporlama, exploitation, post-exploitation, temizlik, pentest advisor, wordlist, rapor jeneratörü |
| 16 | **Sıfır Güven Mimarisi** | 18 | Zero Trust ilkeleri, mikro-segmentasyon, sürekli doğrulama, ZTNA |
| 17 | **Uç Nokta Güvenliği** | 17 | EDR/XDR, endpoint hardening, malware önleme, cihaz kontrolü |
| 18 | **DevSecOps** | 17 | CI/CD güvenliği, SAST/DAST, supply chain, container scanning, IaC güvenliği |
| 19 | **Oltalma Savunması** | 15 | Email güvenliği, SPF/DKIM/DMARC, phishing analizi, kullanıcı eğitimi |
| 20 | **Kriptografi** | 15 | Algoritma analizi, TLS/SSL, PKI, şifreleme denetimi, key yönetimi |
| 21 | **Fidye Yazılım Savunması** | 13 | Playbook, yedekleme, önleme, fidye analizi, kurtarma stratejileri |
| 22 | **Mobil Güvenlik** | 13 | Android/iOS güvenliği, APK analizi, mobil malware, MDM |
| 23 | **Uyum ve Yönetişim** | 5 | NIST CSF, ISO 27001, SOC 2, PCI DSS, GRC |
| 24 | **Tedarik Zinciri Güvenliği** | 3 | SBOM, üçüncü parti risk, yazılım tedarik zinciri |
| 25 | **Aldatma Teknolojisi** | 3 | Honeypot, deception, tuzak sistemler |
| 26 | **Kablosuz Ağ Güvenliği** | 2 | WiFi, Bluetooth, RF güvenliği |
| 27 | **Firmware Güvenliği** | 2 | UEFI, BIOS, firmware analizi |
| 28 | **Yapay Zeka Güvenliği** | 4 | AI/ML güvenliği, adversarial ML, model güvenliği, LLM security testing, CTF AI/ML attacks |
| 29 | **Gizlilik Uyumu** | 2 | GDPR, KVKK, veri gizliliği |
| 30 | **Sosyal Mühendislik** | 1 | Pretexting, phishing, vishing, fiziksel güvenlik |
| 31 | **Veri Koruma** | 1 | DLP, veri sınıflandırma, şifreleme |
| 32 | **Blockchain Güvenliği** | 1 | Smart contract, kripto para, DeFi güvenliği |

---

## Triage Akışı

Bir siber güvenlik görevi geldiğinde FETIH şu akışı izler:

### 1. Kategori Tespiti

```bash
# Görev tipini belirle
# - "Bir zararlı yazılım analiz et" → malware-analysis/
# - "AWS S3 bucket'larını denetle" → cloud-security/
# - "Loglarda anomali ara" → threat-hunting/ veya soc-operations/
# - "Web uygulamasını test et" → web-application-security/
# - "Olay müdahalesi başlat" → incident-response/
# - "Nmap ile ağ tara" → network-security/
# - "Red team operasyonu planla" → skills/red-teaming/red-team-operations/
```

### 2. İlgili Skill'i Yükle

Kategori belirlendikten sonra o kategorideki spesifik skill'i ara:

```bash
# Örnek: threat-hunting kategorisinde "registry persistence" ile ilgili skill
ls skills/cybersecurity/threat-hunting/*registry*persistence*/
cat skills/cybersecurity/threat-hunting/hunting-for-registry-persistence-mechanisms/SKILL.md
```

### 3. Skill Zinciri

Bir görev birden fazla kategoriyi tetikleyebilir. Örnek zincirler:

```
Zararlı yazılım olayı:
  malware-analysis/ → incident-response/ → threat-hunting/ → digital-forensics/

Bulut ihlali:
  cloud-security/ → incident-response/ → identity-access-management/ → compliance-governance/

Web saldırısı:
  web-application-security/ → incident-response/ → network-security/ → threat-intelligence/
```

---

## MITRE ATT&CK Kapsamı

Bu katalog **291 benzersiz MITRE ATT&CK tekniğini** kapsar (14/14 taktik):

| ATT&CK Taktiği | Teknik Sayısı | Kapsam |
|---|---|---|
| 🔎 Keşif (Reconnaissance) | 12 | ✅ |
| 🏗️ Kaynak Geliştirme | 7 | ✅ |
| 🚪 İlk Erişim (Initial Access) | 18 | ✅ |
| ⚡ Çalıştırma (Execution) | 18 | ✅ |
| 🔩 Kalıcılık (Persistence) | 36 | ✅ |
| ⬆️ Yetki Yükseltme | 11 | ✅ |
| 🥷 Savunma Atlatma | 48 | ✅ |
| 🔑 Kimlik Bilgisi Erişimi | 27 | ✅ |
| 🗺️ Keşif (Discovery) | 20 | ✅ |
| ↔️ Yatay Hareket | 9 | ✅ |
| 📦 Toplama (Collection) | 13 | ✅ |
| 📡 Komuta Kontrol (C2) | 20 | ✅ |
| 📤 Sızıntı (Exfiltration) | 12 | ✅ |
| 💥 Etki (Impact) | 6 | ✅ |

---

## NIST CSF Uyumu

Tüm skill'ler NIST Cybersecurity Framework 2.0 ile uyumludur:

- **Govern (GV)**: Yönetişim, risk yönetimi, tedarik zinciri
- **Identify (ID)**: Varlık yönetimi, risk değerlendirme
- **Protect (PR)**: Erişim kontrolü, eğitim, veri güvenliği
- **Detect (DE)**: Sürekli izleme, anomali tespiti
- **Respond (RS)**: Müdahale planlama, iletişim, analiz
- **Recover (RC)**: Kurtarma planlama, iyileştirme

---

## Mapping Dosyaları (Hızlı Erişim)

Bu dizinde 6 adet index dosyası bulunur. **FETIH, skill aramaya başlamadan ÖNCE bu index'lere bakar.** Böylece 725 SKILL.md dosyasını tek tek taramak yerine direkt sonuca ulaşır.

| Dosya | Ne İşe Yarar | Kullanım |
|---|---|---|
| `quick-ref.md` | **Tüm aramaların ilk adresi.** ATT&CK tekniği → skill eşlemesini tek satırda verir | `grep T1055 quick-ref.md` |
| `mitre-attack-coverage.md` | 291 tekniğin tam taktik bazlı dökümü | Taktik bazlı keşif |
| `mitre-attack-index.md` | Teknik → kapsayan skill'ler | Detaylı MITRE araması |
| `nist-csf-index.md` | NIST CSF kategorisi → skill'ler | Compliance görevleri |
| `tool-index.md` | 233 araç → hangi skill'lerde kullanıldığı | "nmap ile ilgili ne var?" |
| `category-full-index.md` | Kategori → tüm skill listesi | Tam envanter |

```bash
# Örnek: T1055 process injection için anında sonuç
grep T1055 quick-ref.md
# → 13 alt-teknik ve toplam 20+ skill listelenir

# Örnek: NIST CSF Detect kategorisinde ne var?
grep "DE\." nist-csf-index.md
# → DE.CM, DE.AE, DE.DP kategorilerindeki tüm skill'ler

# Örnek: nmap hangi skill'lerde kullanılıyor?
grep "^## nmap" tool-index.md -A 30
```

---

## Hızlı Kullanım

```bash
# FETIH'e siber güvenlik görevi ver:
fetih -p "bu sunucuda zararlı yazılım analizi yap"

# FETIH otomatik olarak:
# 1. cybersecurity/ orkestratörünü okur
# 2. malware-analysis/ kategorisini seçer
# 3. En uygun skill'i yükler (örn: analyzing-memory-dumps-with-volatility)
# 4. Skill'deki adımları uygular
# 5. Sonuçları raporlar

# Belirli bir kategoriye yönlendir:
fetih -p "AWS S3 bucket güvenlik denetimi yap"  # → cloud-security/
fetih -p "ağdaki anomali trafiği analiz et"     # → network-security/ veya threat-hunting/
fetih -p "web uygulamasında XSS testi yap"      # → web-application-security/
fetih -p "olay müdahale sürecini başlat"         # → incident-response/
```

---

## Skill Geliştirme

Bu katalog sürekli genişlemektedir. Yeni bir siber güvenlik skill'i eklemek için CONTRIBUTING.md'deki rehberi takip edin. Her skill şu yapıda olmalıdır:

```yaml
---
name: skill-adi
description: Kısa açıklama
tags: [kategori, araclar, teknikler]
triggers: ["tetikleyici anahtar kelimeler"]
category: ana-kategori
mitre_attack: [TXXXX]
nist_csf: [XX.XX-XX]
---
```

**Toplam:** 725 SKILL.md · 32 kategori · Son güncelleme: 2026-05-25
> **Red Team skill'leri** → `skills/red-teaming/red-team-operations/` (29 skill)

<!--
  ⚔ Bu skill FETIH AI Agent icin gelistirilmistir — https://github.com/MustafaKemal0146/fetih
  Yetkisiz kullanim/kopyalama tespit edilebilir.
  hash: 0ebaf06640ac922e
-->

