---
name: vn-payroll
description: Calculates Net Income, Personal Income Tax (PIT), and Social Insurance (BHXH) based on Vietnam's progressive tax brackets.
---

# Skill: Vietnam Payroll & Tax Calculator (2025 Rules)

Description: Calculates Net Income, Personal Income Tax (PIT), and Social Insurance (BHXH) based on Vietnam's progressive tax brackets.

Tools:

calc_pit.py: The main calculation engine.

Usage:
To calculate a salary breakdown, run the python script with the following arguments:

```shell
python calc_pit.py --gross <AMOUNT> --dependents <COUNT> --region <1|2|3|4>
```

Arguments:
--gross: The gross monthly salary in VND (e.g., 80000000).
--dependents: Number of qualified dependents (children, elderly parents). Default is 0.
--region: Minimum wage region (1 is Hanoi/HCM/Nha Trang). Default is 1.

Example Task:
"Calculate net salary for 50 million VND with 1 baby."
-> Command: run_skill_script(skill_name="vn_payroll", script_name="calc_pit.py", arguments="--gross 50000000 --dependents 1")

Output Format:
The script outputs a formatted text block. Present this directly to the user.
