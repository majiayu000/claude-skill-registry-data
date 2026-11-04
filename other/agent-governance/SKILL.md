---
name: agent-governance
description: "Agent islemlerini policy'ye gore denetle. Hassas islem oncesi governance kontrolu calistir. Tetikleyiciler: destructive komut, dosya sistemi erisimi, rate limit, butce kontrolu, trust score yonetimi."
---

# Agent Governance

## Genel Bakis

Agent'larin islemlerini policy tabanli denetleme sistemi. Her hassas islem oncesi governance kontrolu yapar, audit log'a kaydeder.

**Temel ilke:** Guven ama dogrula. Her islem loglanir, hassas islemler policy'ye gore degerlendirilir.

## Policy Dosyasi

Konum: `~/.agent-evolution/config/governance.yaml`

Her agent icin tanimlanmis:
- **trust_level**: 0-1000 arasi guven skoru
- **filesystem**: allowed/denied dizin listeleri
- **rate_limits**: Saatlik islem limitleri
- **budget**: Gunluk maliyet limiti

## Calisma Modlari

| Mod | Davranis |
|-----|----------|
| `audit-only` | Logla + uyar, engelleme (baslangic modu) |
| `blocking` | Logla + engelle (2 hafta veri sonrasi) |

## Kullanim

### Islem Oncesi Kontrol

Her hassas islem oncesi:
```
exec: ~/.agent-evolution/scripts/oracle-governance.sh check <agent> <action> <args>
```

Ornekler:
```
exec: ~/.agent-evolution/scripts/oracle-governance.sh check primary-agent exec "ls -la ~/clawd"
# → ALLOW (allowed filesystem)

exec: ~/.agent-evolution/scripts/oracle-governance.sh check social-agent exec "cat ~/.ssh/id_rsa"
# → DENY (denied filesystem)

exec: ~/.agent-evolution/scripts/oracle-governance.sh check primary-agent exec "rm -rf /tmp/test"
# → WARN (destructive action)
```

### Audit Log Goruntuleme

```
exec: ~/.agent-evolution/scripts/oracle-governance.sh audit --last 10
exec: ~/.agent-evolution/scripts/oracle-governance.sh audit primary-agent --last 5
```

### Haftalik Rapor

```
exec: ~/.agent-evolution/scripts/oracle-governance.sh report --weekly
```

### Trust Score Yonetimi

```
exec: ~/.agent-evolution/scripts/oracle-governance.sh trust primary-agent        # mevcut skoru goster
exec: ~/.agent-evolution/scripts/oracle-governance.sh trust social-agent +50      # skor artir
exec: ~/.agent-evolution/scripts/oracle-governance.sh trust finance-agent -100      # skor azalt
exec: ~/.agent-evolution/scripts/oracle-governance.sh trust tithonos =750   # skor ayarla
```

### Istatistikler

```
exec: ~/.agent-evolution/scripts/oracle-governance.sh stats
```

## Hassas Islem Kategorileri

| Kategori | Ornekler | Varsayilan Davranis |
|----------|----------|---------------------|
| **Destructive** | rm -rf, git push --force, drop table | WARN + log |
| **Financial** | trade, transfer, payment | DENY + log |
| **External** | curl POST, webhook, smtp | WARN + log |
| **Filesystem denied** | ~/.ssh, ~/.aws erisimi | DENY + log |
| **Rate limit** | exec_per_hour asildi | WARN + log |

## Entegrasyon Kurallari

1. **Yeni agent olusturuldiginda**: governance.yaml'a entry ekle
2. **Trust ihlali tespit edildiginde**: trust score dusur + Discord alert
3. **2 hafta audit-only sonrasi**: Veriyi analiz et, blocking'e gec
4. **Haftalik**: `oracle-governance.sh report --weekly` calistir

## Iliskili Dosyalar

- Policy: `~/.agent-evolution/config/governance.yaml`
- Script: `~/.agent-evolution/scripts/oracle-governance.sh`
- Audit DB: `~/.agent-evolution/governance/audit.db`
- Trust Scores: `~/.agent-evolution/governance/trust-scores.json`
