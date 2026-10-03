---
name: demographic-modeling
description: >
  This skill should be used when the user asks to "design a demographic model",
  "model a person/organisation/role", "design party relationships",
  "plan identity structures", or "work with demographic archetypes".
  Covers designing openEHR demographic models using the PARTY hierarchy,
  roles, capabilities, relationships, and identity patterns. For clinical EHR
  archetypes (OBSERVATION/EVALUATION/etc.) use `archetype-authoring`; for a
  one-off lookup of a demographic RM type with no design work, `/openehr-explain`
  suffices. This skill owns the demographic PARTY model.
argument-hint: "<task: design|review> [entity type or use-case]"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write
  - Edit
  - mcp__openehr-assistant__ckm_archetype_search
  - mcp__openehr-assistant__ckm_archetype_get
  - mcp__openehr-assistant__guide_get
  - mcp__openehr-assistant__type_specification_get
  - mcp__openehr-assistant__terminology_resolve
---

# Demographic Modeling

> The RM detail in the steps below is a working summary. The `specs/rm-demographic` guide loaded in Step 1 is authoritative — if they disagree, follow the guide (or confirm against `type_specification_get`).

## Conflict Resolution

When guides conflict, apply this priority (highest first):
1. Rules and structural constraints
2. Privacy and separation principles
3. Anti-patterns
4. Principles and examples
5. Convenience

## Step 1: Load Guides (MANDATORY)

Before any demographic modeling work, load the authoritative guides:

```
guide_get("openehr://guides/specs/rm-demographic")
guide_get("openehr://guides/archetypes/principles")
```

Load additional guides as needed:
- `guide_get("openehr://guides/specs/rm-ehr")` — for EHR/demographic separation context and cross-referencing patterns

## Step 2: Clarify Use Case

Before designing, gather requirements:

- **Entity types**: Which PARTY subtypes are needed — PERSON, ORGANISATION, GROUP, AGENT?
- **Roles**: What roles do parties play? What capabilities and time validity apply?
- **Relationships**: What relationships exist between parties? What is the directionality?
- **Deployment context**: Is this a standalone demographic service, a PMI wrapper, or embedded within an EHR system?
- **Privacy requirements**: What level of PARTY_SELF identification is appropriate for the deployment?

## Step 3: Research Before Creating

Before designing new demographic archetypes, ALWAYS search CKM first:

```
ckm_archetype_search("person")
ckm_archetype_search("organisation")
ckm_archetype_search("party identity")
```

**Reuse-first principle**: If a suitable demographic archetype exists, use it. Only create new archetypes when no existing archetype covers the concept. If a close match exists, consider specialization instead.

Use `ckm_archetype_get` to retrieve and review candidate archetypes in full before deciding. For a deeper reuse survey across varied phrasings (demographic concepts are easy to phrase several ways), dispatch the `ckm-scout` agent — it runs parallel searches and returns a ranked reuse/specialize/new recommendation without filling the main context with raw hits.

## Step 4: PARTY Hierarchy Design

### ACTOR Subtype Selection

Choose the correct ACTOR subtype for each entity:

| ACTOR Subtype | Purpose | Examples |
|---------------|---------|---------|
| PERSON | Individual human beings | Patient, clinician, next of kin |
| ORGANISATION | Legal or administrative entities | Hospital, clinic, insurer |
| GROUP | Informal or functional collections | Care team, household |
| AGENT | Non-human actors | Software agent, device |

Use `type_specification_get` to verify the RM structure of ACTOR and its subtypes when uncertain.

### ROLE Modeling

ROLE represents a party acting in a specific capacity:
- Each ROLE references its ACTOR via `performer`
- Assign `time_validity` to express when the role is active
- Use `capabilities` to describe what the role is permitted to do
- A single ACTOR may hold multiple concurrent ROLEs (e.g., a person who is both a patient and a clinician)

### GROUP vs ORGANISATION

- Use GROUP for informal or ad-hoc collections without a legal identity (e.g., care team, family unit)
- Use ORGANISATION for entities with a formal legal or administrative standing (e.g., registered company, government body)

## Step 5: Identity and Contact Design

### PARTY_IDENTITY

PARTY_IDENTITY holds names and designations for a party:
- Each identity has a `purpose` (e.g., legal name, alias, trading name, maiden name)
- Apply `time_validity` to capture historical names
- A party may hold multiple PARTY_IDENTITY instances simultaneously

### Identifiers

State-issued and system-assigned identifiers (e.g., NHS number, passport number, employee ID) belong in `PARTY.details`, NOT in PARTY_IDENTITY. PARTY_IDENTITY is for names only.

Use `type_specification_get("PARTY_IDENTITY")` to confirm the structure before authoring.

### CONTACT and ADDRESS

- CONTACT groups one or more ADDRESS instances under a shared `purpose` (e.g., home, work, billing)
- Each ADDRESS carries its own `time_validity`
- Prefer structured ADDRESS types over free-text where the deployment context supports it

## Step 6: Relationship Design

### PARTY_RELATIONSHIP Modeling

- PARTY_RELATIONSHIP is directional: `source` → `target`
- The source party carries the relationship instance by value in `relationships`
- The target party holds a reference back in `reverse_relationships` — by reference only, not by value
- Apply `time_validity` to express active periods for the relationship
- Assign a `details` archetype to carry relationship-specific data (e.g., next-of-kin type, guardian authority)

### Serialisation Safety

When producing EHR Extracts, relationships that reference parties outside the extract boundary must be serialised safely. Avoid assumptions that all referenced parties are included in the same extract.

## Step 7: Privacy and Separation

### Three Levels of PARTY_SELF Identification

openEHR supports three levels of identification in the EHR for privacy:
1. **Full identification**: EHR contains explicit demographic references pointing to a Party in the demographic service
2. **Coded identification**: EHR contains only a coded reference; mapping is held externally
3. **Anonymous**: EHR contains no identifying links; identification is impossible from the EHR alone

Choose the level appropriate for the deployment context and applicable data-protection regulations.

### EHR Index Service

Cross-referencing between the EHR and the demographic service is mediated by an EHR Index (or Master Patient Index). The EHR does not directly embed demographic records.

### Clinical Demographic Data in the EHR

Certain demographic-adjacent data is legitimately recorded in the EHR as clinical observations:
- Age, date of birth (as OBSERVATION or ADMIN_ENTRY)
- Biological sex, gender identity (as OBSERVATION)
- Occupation, ethnicity (as ADMIN_ENTRY or EVALUATION)

This data lives in the EHR by clinical necessity and is distinct from the authoritative demographic record in the Party service.

## Step 8: Versioning

- Demographic records use VERSIONED_PARTY, following the same change-control model as EHR content
- Every update creates a new Version; the version history is immutable
- Lifecycle states (draft, complete, deleted) apply to demographic versions
- All changes are associated with a Contribution carrying audit metadata (committer, timestamp, reason)

Ensure that any demographic archetype design accounts for which fields are expected to change over time and how version history will be navigated.

## Step 9: Quality Review

Before finalizing the demographic model, verify:

- [ ] Clear entity type selection (PERSON / ORGANISATION / GROUP / AGENT / ROLE)
- [ ] Appropriate CKM archetype reuse confirmed via search
- [ ] Identity (PARTY_IDENTITY) and identifiers (PARTY.details) correctly separated
- [ ] Roles carry `performer` reference and `time_validity`
- [ ] Relationship directionality is correct (source carries by value, target by reference)
- [ ] Privacy level chosen and documented for the deployment context
- [ ] Versioning approach defined and VERSIONED_PARTY lifecycle considered
- [ ] PMI / EHR Index integration strategy documented if applicable
