---
name: stata
description: Execute Stata do-files via Bash using absolute paths and automatically retrieve logs.
---

# Stata Skill

**Executable Path**: `"D:/Stata/StataMP-64.exe"`

## 1. CODE GENERATION RULES (Mandatory)
**Whenever you create or edit a `.do` file, you MUST insert these two lines at the very top:**

```stata
capture log close        // Closes any previously open logs to prevent errors
set more off             // Prevents Stata from pausing for user input (freezing)

## Operational Instructions

### Correct Execution Example
If you want to run `analysis.do` located in `D:/Project/`:

powershell -Command "& \"D:/Stata/StataMP-64.exe\" /e do
      \"D:/AutoRegMonkey/workspace/analysis.do\""

工作目录设在workspace，log文件也输出到workspace
在根目录下读取同名的log文件，那是stata的输出
