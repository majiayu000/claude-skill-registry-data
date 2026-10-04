---
name: title-discovery
description: Title keşif ve kurtarma — holding JSON, git history, arşiv taraması; TITLE_INVENTORY günceller. Faz 1 tetikleyici.
---

# Title Discovery Engine

## Instructions
1. `data/holding_istirak_org.json` oku (633 rol)
2. `python3 scripts/build_title_inventory.py` çalıştır
3. Git: `git log --all --diff-filter=D -- uretim/rol-kartlari/`
4. `ARCHIVE/`, `CONTEXT/INBOX/` tara
5. `ROSTER/TITLE_INVENTORY.md` güncelle — hiçbir title düşürme

**Hibrit:** Skill yoksa `/title-kesif` command inline adımlarını uygula.

## Examples
- Holding JSON → 633 satır envanter
- Git deleted `adops-ceo.md` → status: git-silinmis-kurtarilabilir

## Performance Notes
- Tek script çağrısı envanteri yeniden üretir
- Büyük diff'lerde gruplu commit

## Troubleshooting
- Git yok → envantere "git yok" notu düş
- JSON role_adet ≠ satır sayısı → uyarı ver
