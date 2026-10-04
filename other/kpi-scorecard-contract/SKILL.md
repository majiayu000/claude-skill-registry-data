---
name: kpi-scorecard-contract
description: Use this skill whenever writing KPI calculation logic, dashboard metric queries, reporting cadence automation, baseline-freeze logic, or any code that produces institutional or platform-level performance metrics. This defines the 7 KPI families, their formulas, cadence, baseline rules, and the contract for reporting to Ministry Viewers and Procurement Reviewers. Load before writing any metrics, reporting, or analytics code.
---

This skill defines the KPI scorecard contract for the Myelin platform. KPIs are the platform's accountability mechanism toward institutions, regulators, and commercial buyers. Every formula here is the authoritative calculation. Do not approximate, abbreviate, or substitute alternate formulas.

---

## KPI Families — Overview

Seven families. Each family has one or more named metrics.

| # | Family | Audience | Cadence |
|---|--------|---------|---------|
| 1 | Learner Completion | Admin, Ministry Viewer | Monthly |
| 2 | Core Curriculum Coverage | Admin, Regulator Auditor | Monthly |
| 3 | Competency Attainment | Admin, Employer | Monthly |
| 4 | Time-to-Competency | Admin, Procurement Reviewer | Monthly |
| 5 | Instructor Capacity | Admin | Monthly |
| 6 | Pilot Conversion Readiness | Admin, Procurement Reviewer | Weekly during pilot |
| 7 | Demo-to-Pilot Conversion | Super Admin | Weekly |

---

## Family 1 — Learner Completion

### 1.1 Module Completion Rate

```
completionRate = completedEnrollments / totalEnrollments
```

- `completedEnrollments`: enrollments where all required modules have status COMPLETED within the cohort window
- `totalEnrollments`: all active enrollments in the cohort as of the measurement date
- Scope: per cohort, per programme, per tenant
- Exclude: enrollments with status WITHDRAWN or SUSPENDED

```javascript
async function computeModuleCompletionRate(cohortId, programmeId, tenantId, asOfDate) {
  const result = await db.query(`
    SELECT
      COUNT(*) FILTER (WHERE e.status = 'COMPLETED') AS completed,
      COUNT(*) FILTER (WHERE e.status NOT IN ('WITHDRAWN','SUSPENDED')) AS total
    FROM enrollments e
    WHERE e.cohort_id = $1
      AND e.programme_id = $2
      AND e.tenant_id = $3
      AND e.enrolled_at <= $4
  `, [cohortId, programmeId, tenantId, asOfDate]);

  const { completed, total } = result.rows[0];
  return total > 0 ? parseFloat(completed) / parseFloat(total) : null;
}
```

### 1.2 On-Time Completion Rate

```
onTimeRate = completedOnTime / totalEnrollments
```

- `completedOnTime`: enrollments where `completed_at <= cohort.end_date`

---

## Family 2 — Core Curriculum Coverage

### 2.1 Mandatory Module Delivery Rate

```
deliveryRate = modulesDelivered / mandatoryModulesInProgramme
```

- `modulesDelivered`: modules with at least one learner completion in the tenant
- `mandatoryModulesInProgramme`: modules flagged `required: true` in the programme definition
- This metric flags tenants that have activated the platform but not deployed the full curriculum

### 2.2 Simulation Scenario Activation Rate

```
activationRate = activatedScenarios / totalScenariosLicensed
```

- A scenario is "activated" when at least one learner has completed it in the measurement period
- LOTO must always be 100% activated for v1 — it is release-blocking

---

## Family 3 — Competency Attainment

### 3.1 Simulation First-Pass Rate

```
firstPassRate = learnersPassingOnFirstAttempt / learnersAttemptingScenario
```

- `learnersPassingOnFirstAttempt`: learners who completed all 7 LOTO steps without a session reset
- Scope: per scenario, per cohort

### 3.2 Simulation Mastery Rate

```
masteryRate = learnersCompletingScenario / learnersAttemptingScenario
```

- Completion regardless of attempt count
- Target threshold for programme endorsement: >= 0.80

### 3.3 Average Attempts to Mastery

```
avgAttempts = SUM(sessionCount per learner) / learnersCompletingScenario
```

- `sessionCount`: number of distinct simulation sessions per learner before first SESSION_COMPLETE
- Lower is better; elevated values surface in the instructor view as cohort-level coaching signals

---

## Family 4 — Time-to-Competency

### 4.1 Median Time to First Simulation Pass

```
medianTime = MEDIAN(firstPassTimestamp - enrollmentTimestamp) for all completers
```

- Measured in calendar days from enrollment to first SESSION_COMPLETE
- Median (not mean) — resistant to outliers from long-inactive enrollments
- Report alongside the 25th and 75th percentile for distribution visibility

### 4.2 Average Active Learning Hours

```
avgLearningHours = SUM(activeSessionMinutes per learner) / learnerCount / 60
```

- `activeSessionMinutes`: sum of minutes where tab visibility was active during a learning session
- Excludes time where the tab was hidden (enforced by the Page Visibility API in the simulator)

---

## Family 5 — Instructor Capacity

### 5.1 Learner-to-Instructor Ratio

```
ratio = activeLearnersInPeriod / activeInstructorsInPeriod
```

- `activeLearnersInPeriod`: learners with at least one learning event in the measurement month
- `activeInstructorsInPeriod`: lecturers who reviewed at least one submission or logged a cohort activity

### 5.2 Submission Review Turnaround Time

```
avgTurnaround = AVG(reviewedAt - submittedAt) across all submissions in period
```

- Measured in hours
- SLA target: <= 72 hours from submission to first review outcome
- Surface in the admin dashboard with a count of submissions exceeding 72 hours

---

## Family 6 — Pilot Conversion Readiness

Used during pilot period only. Replaces the standard monthly cadence with weekly reporting.

### 6.1 Pilot Learner Activation Rate

```
activationRate = learnersWithAtLeastOneSimAttempt / totalPilotLearnerEnrollments
```

- Measures whether enrolled learners are actually using the platform
- Target: >= 0.70 by week 4 of pilot

### 6.2 Pilot NPS Proxy (Engagement Signal)

Not a formal NPS survey — a session engagement proxy:

```
engagementScore = (completingSessions + assistModeUsedSessions) / totalSessions
```

- Sessions where the learner reached at least step 4 count as "engaging"
- Reported as a 0–1 ratio with weekly delta

### 6.3 Demo-to-Pilot Conversion Rate

```
conversionRate = pilotsStartedFromDemo / totalDemoSessions
```

- `pilotsStartedFromDemo`: tenants who completed a demo session and signed a pilot agreement within 30 days
- Measured at the Super Admin level only — not visible to individual tenants

---

## Family 7 — Demo-to-Pilot (Super Admin Only)

### 7.1 Demo Session Completion Rate

```
demoCompletionRate = demosReachingWaypoint5 / totalDemoSessionsStarted
```

- The 5-waypoint demo must reach all 5 waypoints to count as "completed"
- Incomplete demos (abandoned at waypoint 1–4) are tracked separately for drop-off analysis

### 7.2 Time from Demo to Pilot Agreement

```
avgConversionDays = AVG(pilotAgreementDate - demoSessionDate) for converted tenants
```

---

## Baseline Freeze Rule

KPI baselines are frozen at cohort start and at the end of the pilot's first month. Retroactive changes to baseline data are prohibited. If the programme definition changes after baseline freeze, the delta must be calculated against the original baseline — not recalculated from scratch.

```javascript
async function freezeKPIBaseline(cohortId, programmeId, tenantId) {
  const exists = await getKPIBaseline(cohortId, programmeId, tenantId);
  if (exists) throw new Error('BASELINE_ALREADY_FROZEN');

  const baseline = {
    cohortId,
    programmeId,
    tenantId,
    frozenAt:            new Date().toISOString(),
    totalEnrollments:    await countEnrollments(cohortId, tenantId),
    mandatoryModules:    await countMandatoryModules(programmeId, tenantId),
    scenariosLicensed:   await countLicensedScenarios(tenantId)
  };

  await db.query(`
    INSERT INTO kpi_baselines
      (baseline_id, cohort_id, programme_id, tenant_id, frozen_at,
       total_enrollments, mandatory_modules, scenarios_licensed)
    VALUES ($1,$2,$3,$4,$5,$6,$7,$8)
  `, [generateUUID(), cohortId, programmeId, tenantId, baseline.frozenAt,
      baseline.totalEnrollments, baseline.mandatoryModules, baseline.scenariosLicensed]);

  return baseline;
}
```

---

## Reporting Cadence Automation

KPI snapshots are computed and stored nightly. They are not computed on demand from live data — dashboards read from the snapshot table.

```javascript
async function runKPISnapshotJob(measurementDate) {
  const tenants = await getActiveTenants();

  for (const tenant of tenants) {
    const cohorts = await getActiveCohorts(tenant.tenantId);
    for (const cohort of cohorts) {
      const snapshot = await computeAllKPIs(cohort, tenant, measurementDate);
      await insertKPISnapshot({
        snapshotId:      generateUUID(),
        tenantId:        tenant.tenantId,
        cohortId:        cohort.cohortId,
        measurementDate,
        snapshot:        JSON.stringify(snapshot),
        computedAt:      new Date().toISOString()
      });
    }
  }

  await writeAuditEntry('KPI_SNAPSHOT_JOB_COMPLETE', {
    metadata: { measurementDate, tenantCount: tenants.length }
  });
}
```

Weekly KPIs (Family 6, 7) run on the nightly job but are only surfaced to the dashboard in weekly aggregates.

---

## Role-Scoped KPI Access

| Role | Families visible |
|------|-----------------|
| Admin | 1, 2, 3, 4, 5, 6 (own tenant only) |
| Ministry Viewer | 1, 2, 3 (read-only, own tenant) |
| Procurement Reviewer | 4, 6 (anonymised cohort view) |
| Regulator Auditor | 2, 3 (read-only, own tenant) |
| Super Admin | All families, all tenants |

---

## What Not To Do

- Do not compute KPIs from live data on dashboard load — always read from snapshot table
- Do not recalculate baselines after the baseline freeze date
- Do not expose Family 7 (Demo-to-Pilot) metrics to tenant-level Admin roles
- Do not use mean for time-based distribution metrics — use median with percentile band
- Do not count WITHDRAWN or SUSPENDED enrollments in completion rate denominators
- Do not include hidden-tab time in active learning hours calculations
