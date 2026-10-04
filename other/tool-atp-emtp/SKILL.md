---
name: tool-atp-emtp
description: Python-automated ATP-EMTP cable modeling — steady-state sheath-voltage and transient studies (switching surge, lightning impulse), plus three-way cross-validation against OpenDSS and CYMCAP. Use when the user says "run ATP" / "ATP simulation", "ATP sheath voltage", "transient analysis" / "switching surge", "lightning impulse", "compare solvers" / "ATP vs OpenDSS", "validate ATP", or "ATP report". NOT for 3D cable-route visualization (use tool-blender-cable-routing).
---

# ATP-EMTP Cable Modeling Skill

Python-automated ATP-EMTP cable sheath voltage and transient analysis tool.

## Memory (read first)

`SKILL_DIR` = `{home}/.claude/skills/tool-atp-emtp/`.

**Always read `<SKILL_DIR>/atp-memory.md` before answering or running anything.**
It holds the current phase, the validated solver results (phasor + Bergeron vs the
12 CYMCAP reference cases, including which cases legitimately xfail and why), the
hard-won key learnings (e.g. the coupled-RL backward-Euler instability and the
Bergeron traveling-wave fix), and known issues. Without it you will re-derive
solved problems or quote stale validation numbers.

Update it at the end of the session when any of these change: the phase, a
validation result, a new key learning, or a known issue that got solved. Keep the
existing shape — status snapshot at the top, dated results, then learnings. Say so
in one line when you've updated it.

## Triggers

| User Says | Action |
|-----------|--------|
| "run ATP" / "ATP simulation" | Run ATP simulation for cable case |
| "ATP sheath voltage" | Steady-state sheath voltage via ATP |
| "transient analysis" / "switching surge" | Transient template simulation |
| "lightning impulse" / "lightning study" | Lightning impulse simulation |
| "compare solvers" / "ATP vs OpenDSS" | Three-way comparison (ATP vs OpenDSS vs CYMCAP) |
| "validate ATP" / "ATP validation" | Run 12 CYMCAP reference cases through ATP |
| "ATP report" | Generate report with tables and charts |

## Prerequisites

1. **ATP installed on Home PC** (Windows 11, RTX 4070 Ti SUPER)
   - `ATP_HOME` environment variable set to ATP installation directory
   - `tpbig.exe` accessible from PATH or `ATP_HOME`
   - EEUG membership required (free non-commercial): https://atp-emtp.org

2. **Python packages**: `pip install numpy pandas matplotlib`
   - Optional: `pip install pyatp` (pdb5627/pyATP) for .pl4 binary parsing

**Check ATP status**:
```bash
# On Home PC
echo %ATP_HOME%
where tpbig.exe
```

## Commands

### 1. validate — Run 12 CYMCAP reference cases

```bash
cd "30_Resources/Electrical-Engineering/Software-Tools/atp-emtp"
python validate_cymcap.py
```

Runs same 12 cases from `opendss-cable-sheath/validate_cymcap_1310.py`:
- GROUP A: 3 cases, 1500A, DLF=0.57
- GROUP B: 9 cases, 1310A, DLF=1.0
- Cable: 132kV 2000mm² Cu Milliken, corrugated Al sheath

### 2. compare — Three-way solver comparison

```bash
python compare_solvers.py
```

ATP vs OpenDSS vs CYMCAP side-by-side for all 12 cases.

### 3. sheath-voltage — Single case steady-state

```python
from atp_core import generate_atp_file
from atp_runner import run_atp
from atp_parser import parse_lis_sheath_voltages

# Generate .atp file
atp_file = generate_atp_file(
    positions=[(-0.35, 1.16), (0.0, 1.16), (0.35, 1.16)],
    phases=['A', 'B', 'C'],
    cable=CableGeometry(),
    I_load=1310,
    section_length_m=1000,
    model_type="pi"
)

# Run and parse
result = run_atp(atp_file)
voltages = parse_lis_sheath_voltages(result['lis_path'])
```

### 4. switching — Switching surge analysis

```python
from transient_templates import switching_surge_template

atp_file = switching_surge_template(
    cable=CableGeometry(),
    positions=[(-0.35, 1.16), (0.0, 1.16), (0.35, 1.16)],
    cable_length_km=10.0,
    closing_time_ms=50.0,
    timestep_us=1.0,
    duration_s=0.1,
)
```

### 5. lightning — Lightning impulse study

```python
from transient_templates import lightning_impulse_template

atp_file = lightning_impulse_template(
    cable=CableGeometry(),
    positions=[(-0.35, 1.16), (0.0, 1.16), (0.35, 1.16)],
    I_peak_kA=10.0,
    front_us=1.2,
    tail_us=50.0,
)
```

### 6. report — Generate report

```python
from report_generator import generate_validation_report
generate_validation_report(output_dir="./reports")
```

## Reference Files

| File | Purpose |
|------|---------|
| `opendss-cable-sheath/validate_cymcap_1310.py` | CableGeometry dataclass, 12 TestCase definitions, CYMCAP reference values |
| `opendss-cable-sheath/cable_sheath_core.py` | Z-matrix impedance method (for PI section model) |
| `opendss-cable-sheath/CYMCAP-Reference-Cases.md` | Canonical test case definitions |

## Tool Location

All scripts: `30_Resources/Electrical-Engineering/Software-Tools/atp-emtp/`

## Key Technical Notes

### ATP .atp File Format
- **Fixed-column FORTRAN format** — column positions are critical, off-by-one = silent failure
- Bus names limited to **6 characters**: SRCA, SRCB, SRCC, LDAA, LDAB, LDAC, SHTA, SHTB, SHTC
- Sections separated by `BLANK CARD` lines
- Timestep: 10-50μs for steady-state, 0.1-1μs for transients

### Two Model Types
1. **PI section**: Inject pre-computed impedance matrix from analytical formulas — simpler, faster
2. **LCC** (Line/Cable Constants): ATP's built-in routine with physical cable dimensions — proper frequency-dependent model

### Steady-State from Time-Domain
- ATP is a time-domain solver — need 10+ power frequency cycles for transient decay
- Extract RMS from last 5 cycles for steady-state comparison
- Simulation: 0.2s (10 cycles @50Hz) minimum for steady-state

## Related Notes

- [[CYMCAP-Reference-Cases]] - Canonical test cases
- [[OpenDSS-Cable-Sheath-Tool]] - Existing sheath voltage calculator
- [[CYMCAP]] - CYMCAP software reference
- [[Cable bonding method]] - Bonding theory
