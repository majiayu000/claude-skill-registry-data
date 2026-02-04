---
name: plan-document
description: Use this skill every user want to create test plan.
---

# Plan Document

## Purpose
- Create test plan document from the given context

## Test Step Rules
1. Every UI action must reference `data-testid`.
2. Example:
   - Click `data-testid="add_user"`
   - Fill `data-testid="full_name"` with "<value>"
   - Verify `data-testid="dialog_user"` closes
3. Always resolve selectors using the collect-selector skill rules.

## Test plan must following template
```
# Scenario Planning

- Code: [SCN-1]
- Feature: <Feature Name>
- Scenario: <Short Title>
- Date: <YYYY-MM-DD>
- Environment: // Check from tests/.env
    - BASE_URL,
    - AUTH_EMAIL,
    - AUTH_PASSWORD

## Context
- Product area: User Management - Core Module
- Goals: Ensure basic user creation functionality works correctly with valid data
- Risks: Form submission failure, network issues, permission validation

## Scenario Details
### Goal: 
  1. <outcome>
### Test File To Generate: 
  1. <plan_test_file_path rule : tests/{feature_name}/{scenario-code}-{kebab-case-scenario}.spec.ts>
### Preconditions: 
  1. <auth/seed/flags>
### Component Path: 
  1. <src all component and sub component that use on test steps>
### Page Route: 
  1. </pageroute>
### API Route: 
  1. </apiroute>
### Test Data: 
  1. <constant data>
### Steps:
  1. <step>
  2. <step>
  ...
### Expected Results:
  - <assert URL/UI/effect>
### Notes: <logs/analytics/cleanup>
```

## Output Format
Return a markdown string containing the generated test plan with the template below.