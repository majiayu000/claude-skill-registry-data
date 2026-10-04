---
name: dl-cost
description: Monitoring complet tokens — conso jour, blocs 5h, sessions, breakdown par modele
disable-model-invocation: true
---

# Monitoring Token Usage

## Conso aujourd'hui (par modele)
!`npx ccusage@latest daily --since $(date +%Y%m%d) --breakdown 2>/dev/null | tail -20`

## Bloc 5h actif (rate limit window)
!`npx ccusage@latest blocks --active 2>/dev/null | tail -15`

## Sessions recentes (les plus couteuses)
!`npx ccusage@latest session --since $(date -d '3 days ago' +%Y%m%d 2>/dev/null || date -v-3d +%Y%m%d 2>/dev/null) --order desc 2>/dev/null | head -30`
