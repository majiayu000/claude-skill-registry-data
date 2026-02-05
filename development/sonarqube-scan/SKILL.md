---
name: sonarqube-scan
description: Run SonarQube/SonarCloud static code analysis to check code quality, detect security vulnerabilities, code smells, and bugs. Use when the user mentions SonarQube, code quality analysis, security scanning, static analysis, or wants to check for vulnerabilities.
allowed-tools: Bash, Read, Grep
---

# SonarQube Code Analysis

This skill runs SonarQube/SonarCloud scans on your Python web application to analyze code quality, detect security vulnerabilities, and identify code smells.

## When to Use This Skill

Use this skill when you need to:
- Run a SonarQube or SonarCloud scan
- Check code quality metrics
- Find security vulnerabilities
- Detect code smells and bugs
- Generate static analysis reports
- Review code coverage and technical debt

## Prerequisites

Before running a scan, ensure:
1. Python and pip are installed
2. Project is configured with SonarQube/SonarCloud credentials
3. Internet connection is available for uploading results

## How to Run a Scan

### Windows (PowerShell)

Run the PowerShell script:
```bash
powershell.exe -ExecutionPolicy Bypass -File .claude/skills/sonarqube/scripts/run_sonar_scan.ps1
```

### Linux/Mac (Bash)

Run the bash script:
```bash
bash .claude/skills/sonarqube/scripts/run_sonar_scan.sh
```

## What the Scan Does

1. **Installs pysonar** - Automatically installs the SonarQube scanner for Python
2. **Runs analysis** - Scans all Python files in the project
3. **Uploads results** - Sends results to SonarCloud for analysis
4. **Generates report** - Creates a detailed quality report with:
   - Code quality metrics
   - Security vulnerabilities
   - Code smells
   - Bugs and issues
   - Technical debt
   - Code coverage

## Understanding Results

After the scan completes:
- Visit your SonarCloud dashboard to view results
- Check the console output for immediate feedback
- Look for critical issues flagged during the scan

For detailed configuration options, see [REFERENCE.md](REFERENCE.md).

## Troubleshooting

**Issue: pysonar installation fails**
- Check your Python and pip installation
- Ensure you have internet connectivity
- Try manually installing: `pip install pysonar`

**Issue: Authentication error**
- Verify your SonarQube token is valid
- Check project key and organization are correct
- See REFERENCE.md for credential configuration

**Issue: Scan timeout**
- Large projects may take several minutes
- Check network connectivity
- Review SonarCloud service status

## Next Steps After Scanning

1. Review the SonarCloud dashboard
2. Address critical security issues first
3. Fix bugs and code smells
4. Monitor code quality trends over time
5. Integrate into CI/CD pipeline for automated scanning
