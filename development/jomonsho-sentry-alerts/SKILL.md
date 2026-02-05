---
name: jomonsho-sentry-alerts
description: Jomonsho 向けの Sentry ops アラートと Discord 通知を設定する。
metadata:
  short-description: ops.* アラート設定手順。
---

# Sentry Alerts for Jomonsho（日本語）

前提（必要なときだけ実施）:
- NEXT_PUBLIC_SENTRY_DSN and SENTRY_DSN set.
- Discord integration installed with channel ID.

推奨フィルタ（Errors -> Number of Errors, event.type:default）:
- message:"[ops] presence.degraded" level:warning
- message:"[ops] room.sync.health" level:warning
- message:"[ops] room.join.retrying" level:warning
- message:"[ops] room.access.error" level:warning
- message:"[safe-update] failure" level:warning

しきい値（初期値）:
- Critical: Above 1 for test, then raise to 3-10 per 10m window.
- Warning optional; disable or set very high.

Actions:
- Discord notification for Critical only (reduce noise).

アラート設定は docs/OPERATIONS.md に記録する。
