---
name: Billing
description: A set of skills to handle billing the patients, government or health insurance. 
---

# Billing

## Claim health insurance
This action will create an incidient at the insurance company.

```python
def create_incident(patient_id, incident_report, reciept):
  # Mock Code
  # ...
```

## Send patient invoice
In case the patient is uninsured, and it is not part of the government-paid-program, invoice the patient directly.

```python
def create_invoice(patient_id, reciept):
  # Mock Code
  # ...
```

## Claim government grants
For all treatments part of the government-program, request subsidy from the government.

```python
def request_government_subsidy(treatment_program_id, patient_id, incident_report, receipt):
  # Mock Code
  # ...
```
