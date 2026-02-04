---
name: jomonsho-incident-triage
description: 本番インシデントの調査データを収集する。
metadata:
  short-description: dumpItoMetricsJson と traces による調査手順。
---

# Incident Triage Checklist（日本語）

影響を受けたクライアントから収集する（障害/不具合時のみ）:
1) Run in DevTools Console:
   - dumpItoMetricsJson("issue-label")
   - copy(dumpItoMetricsJson("issue-label"))

2) 併せて取得:
   - Console errors around the time of failure
   - Network status codes for /api/rooms/* requests
   - Device/OS/Browser info

3) Presence 確認:
   - presenceReady / presenceDegraded
   - RTDB connectivity status

4) Room sync の状態:
   - sync.health, snapshot age, recovery attempts

結果は docs/OPERATIONS.md のインシデントテンプレに記録する。
