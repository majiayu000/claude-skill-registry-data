---
name: neurosurgery-literature
description: Use when searching for neurosurgery literature, developing PubMed search strategies, identifying MeSH terms, or building systematic search queries. Invoke for literature searching in neurosurgery topics.
---

# Neurosurgery Literature Search Skill

This skill guides comprehensive literature searching for neurosurgery systematic reviews.

## When to Use

Invoke this skill when the user:
- Needs to search PubMed for studies
- Wants to develop a search strategy
- Asks about MeSH terms for neurosurgery
- Needs Boolean operators help
- Mentions "literature search" or "search strategy"

## Neurosurgery MeSH Terms

### Subspecialties

| Subspecialty | MeSH Terms |
|--------------|------------|
| **Neuro-oncology** | "Brain Neoplasms", "Glioma", "Meningioma", "Pituitary Neoplasms" |
| **Vascular** | "Intracranial Aneurysm", "Arteriovenous Malformations", "Subarachnoid Hemorrhage" |
| **Spine** | "Spinal Fusion", "Laminectomy", "Intervertebral Disc Degeneration" |
| **Trauma** | "Craniocerebral Trauma", "Traumatic Brain Injury", "Decompressive Craniectomy" |
| **Functional** | "Deep Brain Stimulation", "Epilepsy Surgery", "Movement Disorders" |
| **Pediatric** | "Craniosynostoses", "Hydrocephalus", "Myelomeningocele" |

### Common Procedures

| Procedure | MeSH Term |
|-----------|-----------|
| Craniotomy | "Craniotomy" |
| Craniectomy | "Decompressive Craniectomy" |
| Shunting | "Cerebrospinal Fluid Shunts", "Ventriculoperitoneal Shunt" |
| Endoscopy | "Neuroendoscopy", "Third Ventriculostomy" |
| Radiosurgery | "Radiosurgery", "Gamma Knife Radiosurgery" |
| Spine fusion | "Spinal Fusion" |
| Discectomy | "Diskectomy" |

### Outcome Measures

| Scale | MeSH/Keyword |
|-------|--------------|
| GCS | "Glasgow Coma Scale" |
| GOS | "Glasgow Outcome Scale" |
| mRS | "modified Rankin Scale"[tw] |
| NIHSS | "NIH Stroke Scale"[tw] |
| KPS | "Karnofsky Performance Status" |

## Search Strategy Building

### Step 1: Define PICO

```
P (Population): Patients with malignant MCA infarction
I (Intervention): Decompressive craniectomy
C (Comparator): Medical management
O (Outcome): Mortality, functional outcome (mRS)
```

### Step 2: Map Concepts to MeSH + Keywords

**Population concept:**
```
"Infarction, Middle Cerebral Artery"[MeSH] OR
"malignant MCA infarction"[tiab] OR
"malignant middle cerebral artery"[tiab] OR
"space-occupying cerebral infarction"[tiab]
```

**Intervention concept:**
```
"Decompressive Craniectomy"[MeSH] OR
"decompressive surgery"[tiab] OR
"hemicraniectomy"[tiab] OR
"craniectomy"[tiab]
```

### Step 3: Combine with Boolean

```
(
  "Infarction, Middle Cerebral Artery"[MeSH] OR
  "malignant MCA infarction"[tiab] OR
  "malignant middle cerebral artery"[tiab]
)
AND
(
  "Decompressive Craniectomy"[MeSH] OR
  "decompressive surgery"[tiab] OR
  "hemicraniectomy"[tiab]
)
```

### Step 4: Apply Filters

```
AND (
  "Randomized Controlled Trial"[pt] OR
  "Controlled Clinical Trial"[pt] OR
  "randomized"[tiab] OR
  "randomised"[tiab]
)
AND "humans"[MeSH]
AND "2000/01/01"[PDAT] : "2024/12/31"[PDAT]
```

## Search Field Tags

| Tag | Field | Example |
|-----|-------|---------|
| [MeSH] | MeSH term | "Craniotomy"[MeSH] |
| [tiab] | Title/Abstract | "hemicraniectomy"[tiab] |
| [tw] | Text word | "mRS"[tw] |
| [pt] | Publication type | "Randomized Controlled Trial"[pt] |
| [PDAT] | Publication date | "2020/01/01"[PDAT] |
| [au] | Author | "Smith J"[au] |
| [ta] | Journal | "J Neurosurg"[ta] |

## Study Design Filters

### RCT Filter (Cochrane Highly Sensitive)
```
randomized controlled trial[pt] OR
controlled clinical trial[pt] OR
randomized[tiab] OR
placebo[tiab] OR
clinical trials as topic[mesh:noexp] OR
randomly[tiab] OR
trial[ti]
```

### Observational Studies Filter
```
"Cohort Studies"[MeSH] OR
"Case-Control Studies"[MeSH] OR
"retrospective"[tiab] OR
"prospective"[tiab] OR
"observational"[tiab]
```

## Key Neurosurgery Journals

```
"J Neurosurg"[ta] OR
"Neurosurgery"[ta] OR
"World Neurosurg"[ta] OR
"Acta Neurochir"[ta] OR
"J Neurotrauma"[ta] OR
"Spine"[ta] OR
"Eur Spine J"[ta] OR
"J Neurooncol"[ta] OR
"Neuro Oncol"[ta] OR
"Stroke"[ta] OR
"J Stroke Cerebrovasc Dis"[ta]
```

## Example Complete Search

### Decompressive Craniectomy for TBI

```
# Population: Traumatic brain injury
(
  "Craniocerebral Trauma"[MeSH] OR
  "Brain Injuries, Traumatic"[MeSH] OR
  "traumatic brain injury"[tiab] OR
  "TBI"[tiab] OR
  "head injury"[tiab]
)

# Intervention: Decompressive craniectomy
AND (
  "Decompressive Craniectomy"[MeSH] OR
  "decompressive surgery"[tiab] OR
  "craniectomy"[tiab] OR
  "hemicraniectomy"[tiab]
)

# Filters
AND "humans"[MeSH]
AND "2000"[PDAT] : "2024"[PDAT]
AND English[lang]
```

## Using the Search Tool

```
mcp__neuroresearch__search_pubmed(
    query="decompressive craniectomy AND traumatic brain injury",
    max_results=100,
    date_range="2015:2024"
)
```

## Documentation

Always document:
1. Date of search
2. Database(s) searched
3. Complete search string
4. Number of results
5. Limits applied
6. Grey literature sources (if searched)
