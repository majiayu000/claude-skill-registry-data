---
name: fhir-software
description: Comprehensive FHIR (Fast Healthcare Interoperability Resources) software development assistant. Use when working with FHIR APIs, implementations, or healthcare data exchange. Supports FHIR R4, R4B, R5, Implementation Guides (IGs), validation, terminology, and SMART on FHIR. Ideal for building FHIR servers, clients, validators, or healthcare applications that need to process FHIR resources.
---

# FHIR Software Development Skill

Expert guidance for building robust FHIR (Fast Healthcare Interoperability Resources) software systems with comprehensive package management, spec knowledge, and development workflows.

## Core Architecture

### 1. Package/Specification Management

**Local FHIR Package Cache:**
- Use `@fhir/package-loader` or equivalent for TypeScript/Node.js environments
- For Python: `fhir-package-loader` or custom implementation using `requests` + `json`
- Cache strategy: `~/.fhir/packages/` with version-specific directories
- Support packages: `hl7.fhir.r4.core`, `hl7.fhir.r5.core`, Implementation Guides

**Package Resolution Pattern:**
```typescript
// Load and cache FHIR packages
async function loadFhirPackage(packageId: string, version?: string) {
  const cacheDir = path.join(os.homedir(), '.fhir', 'packages', packageId, version || 'current');
  if (await fs.pathExists(cacheDir)) return loadFromCache(cacheDir);
  
  const packageData = await downloadPackage(packageId, version);
  await cachePackage(cacheDir, packageData);
  return packageData;
}
```

**Document Index Structure:**
Build searchable index from package contents:
- StructureDefinitions (resources, profiles, extensions)
- SearchParameters (for API implementation)  
- ValueSets and CodeSystems (terminology)
- OperationDefinitions (custom operations)
- CapabilityStatements (server capabilities)
- Example instances

### 2. Development Workflows

#### FHIR Resource Modeling
```python
# Use Pydantic for FHIR resource modeling in Python
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Literal
from enum import Enum
import re

class PatientGender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    UNKNOWN = "unknown"

class Patient(BaseModel):
    resourceType: Literal["Patient"] = "Patient"
    id: Optional[str] = None
    active: Optional[bool] = None
    name: Optional[List[dict]] = None
    gender: Optional[PatientGender] = None
    birthDate: Optional[str] = None

    @field_validator('birthDate')
    @classmethod
    def validate_birthdate(cls, v):
        if v and not re.match(r'^\d{4}-\d{2}-\d{2}$', v):
            raise ValueError('Invalid date format, must be YYYY-MM-DD')
        return v

    class Config:
        extra = "allow"  # Allow additional FHIR elements
```

#### FHIR Server Implementation Patterns

**FastAPI + Pydantic (Python):**
```python
from fastapi import FastAPI, HTTPException
from fhir.resources.patient import Patient

app = FastAPI()

@app.post("/Patient", response_model=Patient)
async def create_patient(patient: Patient):
    # Validate against FHIR spec
    patient.validate()
    # Store in database
    saved_patient = await db.save_patient(patient)
    return saved_patient

@app.get("/Patient/{patient_id}")
async def get_patient(patient_id: str):
    patient = await db.get_patient(patient_id)
    if not patient:
        raise HTTPException(404, "Patient not found")
    return patient
```

**Express + FHIR TypeScript (Node.js):**
```typescript
import express from 'express';
import { Patient, Bundle } from 'fhir/r4';

const app = express();

app.post('/Patient', (req, res) => {
  const patient: Patient = req.body;
  
  // Validate resource type and required fields
  if (patient.resourceType !== 'Patient') {
    return res.status(400).json({
      resourceType: 'OperationOutcome',
      issue: [{
        severity: 'error',
        code: 'invalid',
        details: { text: 'Invalid resource type' }
      }]
    });
  }
  
  // Process and store
  const savedPatient = db.savePatient(patient);
  res.status(201).json(savedPatient);
});
```

### 3. FHIR Validation and Quality

#### Profile Validation
```python
from fhir.resources.core.fhirabstractmodel import FHIRAbstractModel
from fhir.resources import get_fhir_model_class
import json

def validate_against_profile(resource_data: dict, profile_url: str) -> bool:
    """Validate FHIR resource against specific profile"""
    try:
        # Load profile from package cache
        profile = load_structure_definition(profile_url)

        # Validate using fhir.resources - dynamically get the resource class
        resource_type = resource_data.get('resourceType')
        resource_class = get_fhir_model_class(resource_type)
        resource = resource_class(**resource_data)

        # Additional profile-specific validation
        return validate_profile_constraints(resource, profile)
    except Exception as e:
        print(f"Validation error: {e}")
        return False
```

#### Terminology Validation
```python
def validate_coding(coding: dict, value_set_url: str) -> bool:
    """Validate coding against ValueSet"""
    value_set = load_value_set(value_set_url)
    
    # Check if code exists in ValueSet expansion
    for concept in value_set.get('expansion', {}).get('contains', []):
        if (concept.get('code') == coding.get('code') and 
            concept.get('system') == coding.get('system')):
            return True
    return False
```

### 4. FHIR Search Implementation

#### Search Parameter Processing
```python
from typing import Dict, Any
import re

class FhirSearchProcessor:
    def __init__(self):
        self.search_params = load_search_parameters()
    
    def parse_search_query(self, resource_type: str, params: Dict[str, str]) -> Dict[str, Any]:
        """Parse FHIR search parameters into database query"""
        query = {}
        
        for param_name, param_value in params.items():
            search_param = self.get_search_parameter(resource_type, param_name)
            
            if not search_param:
                continue
                
            # Handle different search parameter types
            if search_param['type'] == 'string':
                query[param_name] = self.parse_string_search(param_value)
            elif search_param['type'] == 'token':
                query[param_name] = self.parse_token_search(param_value)
            elif search_param['type'] == 'date':
                query[param_name] = self.parse_date_search(param_value)
            elif search_param['type'] == 'reference':
                query[param_name] = self.parse_reference_search(param_value)
                
        return query
    
    def parse_token_search(self, value: str) -> Dict[str, str]:
        """Parse token search: [system]|[code]"""
        if '|' in value:
            system, code = value.split('|', 1)
            result = {}
            if system:
                result['system'] = system
            if code:
                result['code'] = code
            return result
        return {'code': value} if value else {}
```

### 5. SMART on FHIR Integration

#### OAuth 2.0 / SMART App Launch
```typescript
interface SmartConfig {
  authorizeUrl: string;
  tokenUrl: string;
  clientId: string;
  redirectUri: string;
  scopes: string[];
}

class SmartClient {
  constructor(private config: SmartConfig) {}
  
  async authorize(): Promise<string> {
    const state = generateRandomState();
    const authUrl = new URL(this.config.authorizeUrl);
    
    authUrl.searchParams.set('response_type', 'code');
    authUrl.searchParams.set('client_id', this.config.clientId);
    authUrl.searchParams.set('redirect_uri', this.config.redirectUri);
    authUrl.searchParams.set('scope', this.config.scopes.join(' '));
    authUrl.searchParams.set('state', state);
    authUrl.searchParams.set('aud', getFhirBaseUrl());
    
    return authUrl.toString();
  }
  
  async exchangeCodeForToken(code: string): Promise<TokenResponse> {
    const response = await fetch(this.config.tokenUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({
        grant_type: 'authorization_code',
        client_id: this.config.clientId,
        code,
        redirect_uri: this.config.redirectUri
      })
    });

    if (!response.ok) {
      throw new Error(`Token exchange failed: ${response.statusText}`);
    }

    return response.json();
  }
}
```

## Implementation Guides and Extensions

### Custom Profile Development
```json
{
  "resourceType": "StructureDefinition",
  "id": "my-patient-profile",
  "url": "http://example.org/fhir/StructureDefinition/MyPatient",
  "name": "MyPatientProfile",
  "status": "draft",
  "kind": "resource",
  "abstract": false,
  "type": "Patient",
  "baseDefinition": "http://hl7.org/fhir/StructureDefinition/Patient",
  "derivation": "constraint",
  "differential": {
    "element": [
      {
        "id": "Patient.identifier",
        "path": "Patient.identifier",
        "min": 1,
        "mustSupport": true
      },
      {
        "id": "Patient.name",
        "path": "Patient.name", 
        "min": 1,
        "max": "1"
      }
    ]
  }
}
```

## Testing and Validation Tools

### Unit Testing FHIR Resources
```python
import pytest
from fhir.resources.patient import Patient

def test_patient_creation():
    patient_data = {
        "resourceType": "Patient",
        "id": "example",
        "active": True,
        "name": [{
            "family": "Doe",
            "given": ["John"]
        }],
        "gender": "male"
    }
    
    patient = Patient(**patient_data)
    assert patient.resourceType == "Patient"
    assert patient.gender == "male"
    assert len(patient.name) == 1
    assert patient.name[0].family == "Doe"
```

### FHIR Server Testing
```python
import httpx
import pytest

@pytest.fixture
async def fhir_client():
    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        yield client

async def test_patient_crud(fhir_client):
    # Create patient
    patient_data = {"resourceType": "Patient", "active": True}
    create_response = await fhir_client.post("/Patient", json=patient_data)
    assert create_response.status_code == 201
    
    patient_id = create_response.json()["id"]
    
    # Read patient
    read_response = await fhir_client.get(f"/Patient/{patient_id}")
    assert read_response.status_code == 200
    
    # Update patient
    updated_data = read_response.json()
    updated_data["active"] = False
    update_response = await fhir_client.put(f"/Patient/{patient_id}", json=updated_data)
    assert update_response.status_code == 200
    
    # Delete patient
    delete_response = await fhir_client.delete(f"/Patient/{patient_id}")
    assert delete_response.status_code == 204
```

## Common Patterns and Best Practices

### Resource References and Includes
```python
def resolve_references(resource: dict, include_params: List[str]) -> dict:
    """Resolve _include parameters for FHIR search"""
    included_resources = []
    
    for include_param in include_params:
        source_type, search_param = include_param.split(':', 1)
        
        if resource.get('resourceType') == source_type:
            ref_values = extract_reference_values(resource, search_param)
            
            for ref_value in ref_values:
                referenced_resource = load_resource_by_reference(ref_value)
                if referenced_resource:
                    included_resources.append(referenced_resource)
    
    return {
        'resourceType': 'Bundle',
        'type': 'searchset',
        'entry': [{'resource': resource}] + [{'resource': r} for r in included_resources]
    }
```

### Batch and Transaction Processing
```python
async def process_bundle(bundle: dict) -> dict:
    """Process FHIR Bundle with batch or transaction semantics"""
    response_entries = []
    transaction_mode = bundle.get('type') == 'transaction'
    
    try:
        if transaction_mode:
            await db.begin_transaction()
            
        for entry in bundle.get('entry', []):
            request = entry.get('request', {})
            resource = entry.get('resource')
            
            response_entry = await process_bundle_entry(request, resource)
            response_entries.append(response_entry)
            
        if transaction_mode:
            await db.commit_transaction()
            
    except Exception as e:
        if transaction_mode:
            await db.rollback_transaction()
        raise
    
    return {
        'resourceType': 'Bundle',
        'type': 'transaction-response' if transaction_mode else 'batch-response',
        'entry': response_entries
    }
```

### Error Handling and OperationOutcome
```python
def create_operation_outcome(severity: str, code: str, details: str) -> dict:
    """Create FHIR OperationOutcome for error reporting"""
    return {
        'resourceType': 'OperationOutcome',
        'issue': [{
            'severity': severity,
            'code': code,
            'details': {'text': details}
        }]
    }

# Usage in API endpoints
try:
    result = validate_fhir_resource(resource_data)
except ValidationError as e:
    return create_operation_outcome('error', 'invalid', str(e)), 400
```

## Quick Reference Commands

### Package Management
```bash
# Install FHIR packages
npm install @types/fhir @fhir/package-loader
pip install fhir.resources fhir-package-loader

# Load core FHIR packages
fhir-package-loader install hl7.fhir.r4.core 4.0.1
fhir-package-loader install hl7.fhir.us.core 5.0.1
```

### Validation Tools
```bash
# FHIR Validator (Java)
java -jar validator_cli.jar resource.json -version 4.0.1

# HAPI FHIR Validator
curl -X POST "http://localhost:8080/fhir/$validate" \
  -H "Content-Type: application/fhir+json" \
  -d @patient.json
```

### Development Server Setup
```bash
# Python FastAPI FHIR Server
uvicorn main:app --reload --port 8000

# Node.js Express FHIR Server  
npm start
```

## Integration Points

- **EHR Systems**: Epic, Cerner, AllScripts FHIR APIs
- **Cloud Platforms**: AWS HealthLake, Azure FHIR, Google Healthcare API
- **Terminology Services**: UMLS, SNOMED CT, LOINC
- **Security**: OAuth 2.0, JWT, SMART on FHIR scopes
- **Interoperability**: HL7 v2 to FHIR conversion, CDA to FHIR

For detailed implementation guidance, reference the FHIR specification at https://hl7.org/fhir/ and implementation guides at https://fhir.org/guides/registry/
