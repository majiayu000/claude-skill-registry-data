---
name: Diagnosis.
description: An important skill, to help agents assist doctors with diagnosising patients.

---

# Diagnosis tasks

## Extrapolate symptoms
This action can extrapolate and gather symptoms from natural language input

```python
from langchain.chat_models import init_chat_model
from entities import DetectionEntity, SymptomsOutputState

def extrapolate_symptoms(text: str, score: float = 0.95): -> SymptomsOutputState
  # Documentation: https://docs.aws.amazon.com/comprehend-medical/latest/dev/gettingstarted-api.html
  model = init_chat_model("aws.comprehendmedical.detect-entities-v2");
  response = model.invoke(text);
  high_confidence = []
  low_confidence = []

  for entity in response:
    if entity.score >= score:
      high_confidence.append(entity)
    else:
      low_confidence.append(entity)

  return SymptomsOutputState(
    high_confidence=high_confidence,
    confidence_below_treshold=low_confidence
  )
```

## Find potential diagnosis
This action will find potential diagnosis, based on common external resources

```python
def find_potential_diagnose(symptoms):
  """ This function will return 1 or more diagnosis, based on array of symptoms """
  # Mock Code
  # ...
```

## Suggest Next Steps
In case a diagnosis is inconclusive, but more tests is needed, this task will find the best next step to in the diagnosis 

```python
def find_next_steps(symptoms, diagnosis):
  # Mock Code
  # ...
```
