---
name: build-validation
description: >
  How dualdb validates that converted code still builds, and how it reports what
  was actually validated. Use when running or interpreting a build, when mapping a
  diagnostic to a finding, when choosing a build tier, or when writing the build
  line of the report. Never claim a tier you did not reach.
---

# Build validation

Be explicit and honest about what was actually validated. Report the tier reached;
never claim more.

## When to use

Running the baseline or post-conversion build; interpreting diagnostics; deciding
whether a failure is yours; writing the build line in the report.

## Tiers

| Tier | Mechanism | Works for | Notes |
|---|---|---|---|
| **T0 Roslyn** | the analyzer sidecar compiles the syntax trees with available references | everything, including WebForms on a host that cannot build it | catches syntax and most semantic errors; the guaranteed floor |
| **T1 dotnet** | `dotnet restore && dotnet build` | SDK-style projects, .NET Core/5+ | full fidelity |
| **T2 msbuild** | MSBuild - under Mono on Linux, from VS or `dotnet msbuild` on Windows | legacy .NET Framework projects | best effort; `System.Web`, designer files and some targets fail for reasons unrelated to the conversion |
| **T3 full platform** | full Windows desktop/IIS validation | - | out of scope; reported as "not validated on this host" |

**Analysis fidelity is not build fidelity.** A legacy project analyses fine on a
host that cannot build it. Do not conflate the two, and do not treat a T2 failure
as an analysis failure.

## Decision procedure

1. **Build before converting and store the baseline.** Without it, T2 noise makes
   the tool look broken.
2. Build again after conversion at the same tier.
3. **Report deltas, never absolutes.** "Baseline: 3 projects failed to build on
   this host (T2); post-conversion: same 3, no new failures."
4. Map each new diagnostic to a finding.
5. Apply a **database-related fix only**, then rebuild. Cap at 3 iterations.
6. **If a diagnostic cannot be mapped to a finding, do not fix it - report it.**
   That single rule is what stops the tool drifting into general refactoring.
7. Record the tier reached in the report, with the reason it was not higher.

## Reading diagnostics

Diagnostics that are almost certainly yours:

| Symptom | Likely cause |
|---|---|
| `CS0246` on `NpgsqlConnection`, `NpgsqlDbType` | Npgsql package reference missing (Phase 0, `P0-NPGSQL`) |
| `CS1503`/`CS0266` around a parameter | `SqlDbType` vs `NpgsqlDbType` (`PG-PARAM-004`) |
| `CS0029` on a reader assignment | `bit` is now `bool` (`PG-TYPE-005`) |
| `CS0155`/`CS0246` on `SqlException` in a generated alternate | `PG-API-006` - no `Sql*` types in an alternate |
| duplicate member | the dispatcher and the extracted body collided - a transform bug |

Diagnostics that are almost certainly **not** yours, and must be reported rather
than fixed: missing `System.Web` on a non-Windows host, designer-file
`InitializeComponent` errors, missing third-party assemblies, target-file
resolution failures.

## Worked examples

### 1. A new failure that is ours

Post-conversion T1 build fails with `CS0246: NpgsqlDbType could not be found` in
`OrderDataAccess.PostgreSql.cs`. The file is one the tool created, the diagnostic
maps to `PG-PARAM-004`, and the fix is a package reference the Phase 0 gate already
flagged (`P0-NPGSQL`). In scope: fix, rebuild, record.

### 2. A pre-existing failure that is not ours

Baseline T2 build fails for `App.Web` with
`error MSB4019: The imported project "...\WebApplications\Microsoft.WebApplication.targets" was not found`.

Post-conversion, the same project fails identically. The delta is zero. The report
says: *"Build: no new failures (T2, 3 pre-existing)"* and lists them. Fixing it
would be modernization and would also be dishonest - it would present a repo change
as a conversion result.

### 3. A diagnostic that cannot be mapped - report, do not fix

`CS0618: 'ConfigurationManager.AppSettings' is obsolete` appears in a file the tool
touched. The fix is **rejected**, because the diagnostic maps to no finding: the
warning pre-dates the conversion and relates to nothing database. Report it under "what we deliberately did NOT change". Fixing it
would be a warning-cleanup pass, which is an explicit anti-goal.

## Traps

- **No baseline means no honest claim.** Always build first.
- **A T2 failure is not evidence the conversion broke anything** - compare
  against the baseline before concluding anything.
- **The fix loop is capped at 3 iterations** on purpose. A loop that keeps finding
  new work is a signal that a decision upstream was wrong.
- **A green T0 is not a green build.** T0 is the floor: it catches syntax and most
  semantic errors with the references it happens to have.
- **Never report a tier you did not run.** "Not validated on this host" is a
  perfectly good report line; a claimed T1 that was actually T0 is not.

## Escalate when

- The baseline cannot be built at any tier - the delta method has nothing to
  stand on, and that limitation belongs in the report.
- A new diagnostic maps to a finding but the fix would change a signature or a
  caller.
- The fix loop hits its cap.

## Do not

- Do not fix diagnostics unrelated to the database.
- Do not upgrade packages or TFMs to make a build pass.
- Do not suppress warnings.
- Do not claim T1 or T2 when only T0 ran.
