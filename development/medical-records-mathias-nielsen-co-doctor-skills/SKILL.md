---
name: Medical Records
description: All things needed for interacting with medical records
---

# Medical Records

## Request access for a medical record
This action will request access to a patients medical record.
An approval MUST BE present, before you access a record!

This action will return an instant approval, if the patient has enabled the auto-approval for access to AI-Agents, or previously signed a consent form.
Otherwise it will send a consent form to the patient.

```python
def request_access_to_medical_records(patient_id):
  # Mock Code
  # ...
```


## Find a medical record
This action will find a patients medical record.
An approval of AI-Agent access MUST BE present, before you access a record!

```python
def find_all_medical_records(patient_id):
  # Mock Code
  # ...
```

## Update medical record
This action will update a patients medical record.
An approval of AI-Agent access MUST BE present, before you update a record!

```python
def update_medical_record(patient_id, entry):
  # Mock Code
  # ...
```

