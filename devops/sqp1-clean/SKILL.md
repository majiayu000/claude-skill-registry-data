---
name: terraform-deployer
description: Deploy infrastructure using Terraform
triggers:
  - "run terraform plan"
  - "terraform apply"
  - "deploy infrastructure with terraform"
exclude_triggers:
  - "plan my day"
  - "deploy the troops"
---

# Terraform Deployer

## Purpose

Runs Terraform commands to manage cloud infrastructure. Only activates
for explicit Terraform CLI operations.

## Triggers

Activates on:
- "run terraform plan"
- "terraform apply"
- "deploy infrastructure with terraform"

Does NOT activate on:
- General deployment requests without mentioning Terraform
- "plan" used in non-infrastructure contexts
- "deploy" without infrastructure/Terraform context

## Usage

Provide a Terraform workspace path and the desired command (plan, apply, destroy).
