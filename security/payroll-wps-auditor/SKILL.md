---
name: payroll-wps-auditor
description: WPS Payroll & Gratuity Calculator. Pre-flight audit for SIF payroll files and exact statutory end-of-service benefit calculations.
version: 3.0.0
author: AgentBoost Enterprise
enterprise: true
category: Operations & HR
---

### System Instructions
You are equipped with the `payroll-wps-auditor` deterministic tool. This tool performs pre-flight validation of SIF payroll files to prevent labor ministry infractions. It calculates exact statutory gratuity and end-of-service benefits based on current labor laws.

### Execution Protocol
Invoke the payroll audit engine by passing strictly formatted JSON:

```json
{
  "sif_file_id": "SIF_NOV_2026_GLOBAL",
  "calculation_type": "statutory_gratuity_audit",
  "employee_id": "EMP_884",
  "tenure_days": 1825,
  "base_salary_usd": 5500
}
```

Outputs
- SIF payroll file validation and error detection log.
- Precise statutory severance and gratuity calculations.
- Labor law compliance and infraction prevention report.
- Final end-of-service benefit settlement drafts.
