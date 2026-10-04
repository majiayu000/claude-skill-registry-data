---
name: computer-diagnosis
description: Comprehensive computer diagnosis and troubleshooting. Use this skill when a user reports issues with their computer (e.g., "my computer is slow", "it's freezing", "loud fan noise", "no disk space") to analyze system metrics (CPU, RAM, Disk, Network) across macOS, Windows, and Linux, and generate a detailed report with actionable recommendations.
---

# Computer Diagnosis Skill

This skill allows Claude to act as a technical support assistant. It gathers system information using Python's `psutil` library (making it cross-platform), analyzes the metrics for common issues, and provides a structured report.

## Workflow

1. **Information Gathering**:
   When a user reports an issue, execute the data collection script to snapshot the current system state.

   ```bash
   python scripts/collect_info.py > sys_info.json
   ```

2. **Data Analysis**:
   Use the analysis script to parse the collected JSON and identify critical issues (high CPU/Memory, full disks).

   ```bash
   python scripts/analyze_info.py sys_info.json > analysis_result.json
   ```

3. **Report Generation**:
   Read both `sys_info.json` and `analysis_result.json`. Present the findings to the user using the template found in `assets/report_template.md`.

## Reference Materials

- **Symptoms Guide**: See `references/symptoms.md` to map user descriptions to specific metrics.

## Notes

- The scripts rely on `psutil`. If it's missing, you may need to install it (`pip install psutil`).
- Ensure you have permission to read system states. Some disk partitions or network interfaces might throw `PermissionError`, which the script handles by skipping them.
- Always provide actionable recommendations alongside the raw data. Users want to know _how_ to fix the problem.
