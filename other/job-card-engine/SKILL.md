---
name: job-card-engine
description: İş kartı üretimi — JOB_CARDS/{slug}/CARD.md skeleton ve fazlı genişletme. Faz 4 tetikleyici.
---

# Job Card Engine

## Instructions
1. `ROSTER/TITLE_INVENTORY.md`'den slug seç
2. `JOB_CARDS/{slug}/CARD.md` + `INDEX.md` oluştur
3. Faz 0–1: skeleton (kimlik, misyon, RACI, KPI placeholder)
4. Faz 4+: başlıkları `H001.md`… fazlı genişlet
5. QA: `scripts/qa_check.py`

**Hibrit:** Skill yoksa `/is-karti` inline.

## Examples
- `JOB_CARDS/hq-ceo/CARD.md` — C-level skeleton
- `JOB_CARDS/adops-dir-meta/CARD.md` — Director skeleton

## Performance Notes
- 8 paralel agent title gruplarına bölünür
- CARD.md indeks; detay alt dosyalarda

## Troubleshooting
- 200 başlık tek oturumda imkânsız → INDEX placeholder + DEVAM
