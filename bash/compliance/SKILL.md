---
name: compliance
description: Run compliance scan - em dashes, OpenClaw in UI, ts-nocheck exports. Quick rule violation check.
user-invocable: true
---

# Compliance Scan

Run the existing compliance scanner and report violations.

```bash
bash scripts/compliance-scan.sh
```

Summarize: total violations by category, top offending files. If clean, say "all clear" and stop. Keep under 150 words.
