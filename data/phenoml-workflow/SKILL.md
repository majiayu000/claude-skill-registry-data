---
name: phenoml-workflow
description: Create and execute PhenoML workflows for healthcare data processing, including condition creation from clinical notes and patient registration with deduplication
---

# PhenoML Workflow Skill

## Instructions

This skill provides an end-to-end guided experience for creating and testing PhenoML workflows. The skill walks users through the complete workflow setup process using executable scripts.

### When to Use This Skill

Use this skill when users want to:

1. Set up a new PhenoML workflow from scratch
2. Create workflows for processing clinical notes into FHIR Condition resources
3. Set up patient registration workflows with deduplication
4. Test workflows with example data
5. Set up or verify FHIR provider connections

### Interactive Workflow Setup Flow

This skill provides a step-by-step interactive experience where the skill **gathers information from the user conversationally**, then **executes reusable Python scripts** with that information to create and test workflows.

**Step 0: Ensure Dependencies are Installed**
- Before running any scripts, ensure the required Python packages are installed:
  ```bash
  pip install python-dotenv phenoml
  ```
- If the user gets import errors when running scripts, guide them to install these packages

**Step 1: Check FHIR Provider Setup**
- First, locate and run `check_env.py` (search for it using glob `**/check_env.py`) to check credentials and detect instance type
- **If SHARED EXPERIMENT is detected** (experiment.app.pheno.ml):
  - **Skip FHIR provider setup entirely** - shared experiment uses a pre-configured Medplum sandbox
  - The system automatically uses "experiment-default" as the FHIR_PROVIDER_ID
  - No FHIR credentials (CLIENT_ID, CLIENT_SECRET, BASE_URL) are required
  - Proceed directly to Step 2 (Gather Workflow Requirements)
- **If on a DEDICATED INSTANCE** (e.g., acme.app.pheno.ml), ask the user if they have already created a FHIR provider
- If NO:
  - Run `check_env.py` to verify credentials
  - If FHIR credentials are missing, guide them to add the credentials to .env with examples:
    - **Medplum**: `FHIR_PROVIDER_BASE_URL=https://api.medplum.com/fhir/R4`
    - **Athena**: `FHIR_PROVIDER_BASE_URL=https://api.preview.platform.athenahealth.com/fhir/r4`
    - **Epic**: `FHIR_PROVIDER_BASE_URL=https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/R4`
    - **Cerner**: `FHIR_PROVIDER_BASE_URL=https://fhir-myrecord.cerner.com/r4/[tenant-id]`
  - Run `setup_fhir_provider.py` to create the provider
  - The script will save FHIR_PROVIDER_ID to .env automatically
- If YES: Run `check_env.py` to verify FHIR_PROVIDER_ID is set

**Step 2: Gather Workflow Requirements**
- Ask what type of data they want the workflow to process (e.g., clinical notes, patient demographics, lab results)
- Ask them to describe what the workflow should do in their own words
- Provide examples of common workflow types to help guide them

**Step 3: Refine Workflow Description**
- Based on their description, identify the workflow type (condition creation, patient registration, observation creation, or custom)
- Present a refined version of their workflow using best practices
- Show them the recommended workflow instructions and settings (dynamic_generation, etc.)
- Ask for confirmation or allow them to modify

**Step 4: Create the Workflow**
- Run `create_workflow.py` with CLI arguments:
  - `--name "Workflow Name"`
  - `--instructions "workflow instructions..."`
  - `--sample-data '{"key": "value"}'`
  - `--dynamic-generation true`
- The script will create the workflow and save WORKFLOW_ID to .env
- Show the user the created workflow details

**Step 5: Test the Workflow**
- Ask what patient/data they want to test with (or provide examples)
- Run `test_workflow.py` with CLI arguments:
  - `--input-data '{"patient_last_name": "Smith", ...}'`
- Show the execution results
- Offer to run additional tests with different data

### Key Principles

1. **Gather information conversationally** - Ask the user questions first to understand their needs
2. **Find and use the reusable scripts** - First locate the scripts using glob `**/phenoml-workflow/scripts/*.py`, then execute them with appropriate CLI arguments
3. **Always pass --env-file** - Since the scripts may be in a different directory than the user's project, always pass `--env-file /path/to/user/project/.env` to ensure the scripts find the correct .env file (use the user's current working directory)
4. **Prefer CLI arguments over .env** - For workflow-specific data (name, instructions, test data), pass via CLI args rather than adding to .env
5. **Use .env for credentials** - Guide users to store credentials (PHENOML_*, MEDPLUM_*, etc.) in .env for security
6. **Guide progressively** - Go step-by-step, ensuring each step completes before moving to the next
7. **Confirm before executing** - Before running each script, explain what it will do
8. **Provide context** - Explain why each step is necessary and what it accomplishes
9. **Offer examples** - When asking for user input, always provide clear examples

### Available Scripts

**Important:**
1. Before running any script, first locate it using glob `**/phenoml-workflow/scripts/*.py` to find the correct path.
2. Always pass `--env-file` pointing to the user's project .env file (their current working directory).

#### 0. check_env.py

**Purpose:** Safely verifies which environment variables are set without exposing their values

**How it works:**
- Loads .env file using python-dotenv
- Checks presence of required credentials (returns TRUE/FALSE only)
- Never exposes actual credential values
- Provides clear guidance on missing credentials

**Usage:**
```bash
# Check all credentials (pass user's .env path)
python3 /path/to/check_env.py --env-file /user/project/.env

# JSON output only
python3 /path/to/check_env.py --env-file /user/project/.env --json

# Verbose output (formatted + JSON)
python3 /path/to/check_env.py --env-file /user/project/.env --verbose
```

**Security:**
- This script is designed to prevent credential leakage in LLM conversations
- It only reports TRUE/FALSE for each credential, never the actual values
- Safe to run in any context where credentials need to be verified

**Outputs:**
- Formatted status report with ✅/❌ indicators
- Guidance on missing credentials
- Exit code 1 if core credentials are missing

#### 1. setup_fhir_provider.py

**Purpose:** Creates a FHIR provider using credentials from .env

**How it works:**
- Reads FHIR credentials from .env (FHIR_PROVIDER_BASE_URL, FHIR_PROVIDER_CLIENT_ID, FHIR_PROVIDER_CLIENT_SECRET)
- Creates the FHIR provider in PhenoML
- Saves FHIR_PROVIDER_ID to .env

**Usage:**
```bash
# Create provider using .env credentials
python3 /path/to/setup_fhir_provider.py --env-file /user/project/.env

# With custom name and provider type
python3 /path/to/setup_fhir_provider.py --env-file /user/project/.env --name "My FHIR Server" --provider athena
```

**Required .env variables:**
- PHENOML_USERNAME, PHENOML_PASSWORD, PHENOML_BASE_URL
- FHIR_PROVIDER_BASE_URL, FHIR_PROVIDER_CLIENT_ID, FHIR_PROVIDER_CLIENT_SECRET

**Example FHIR_PROVIDER_BASE_URL values:**
- **Medplum**: `https://api.medplum.com/fhir/R4`
- **Athena**: `https://api.preview.platform.athenahealth.com/fhir/r4`
- **Epic**: `https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/R4`
- **Cerner**: `https://fhir-myrecord.cerner.com/r4/[tenant-id]`

**Optional .env variables:**
- FHIR_PROVIDER_NAME (default: "FHIR Server")
- FHIR_PROVIDER_TYPE (default: "medplum")
- FHIR_AUTH_METHOD (default: "client_secret")

**Outputs:**
- FHIR_PROVIDER_ID saved to .env

#### 2. create_workflow.py

**Purpose:** Creates a PhenoML workflow from .env or CLI arguments

**How it works:**
- Reads workflow configuration from CLI args or .env
- Creates the workflow in PhenoML
- Saves WORKFLOW_ID to .env

**Usage:**
```bash
# Create workflow with CLI arguments (recommended)
python3 /path/to/create_workflow.py \
  --env-file /user/project/.env \
  --name "Extract Conditions" \
  --instructions "You are a helpful agent who..." \
  --sample-data '{"patient_last_name": "Smith", "diagnosis_text": "Patient presents with generalized anxiety disorder"}' \
  --dynamic-generation true

# Create workflow using .env variables
python3 /path/to/create_workflow.py --env-file /user/project/.env
```

**Required:**
- FHIR_PROVIDER_ID in .env (from setup_fhir_provider.py)
  - **Note:** For shared experiment (experiment.app.pheno.ml), FHIR_PROVIDER_ID is optional and defaults to "experiment-default"
- Workflow name, instructions, and sample data (via CLI args or .env)

**Optional .env variables:**
- WORKFLOW_NAME, WORKFLOW_INSTRUCTIONS, WORKFLOW_SAMPLE_DATA (JSON string)
- WORKFLOW_DYNAMIC_GENERATION (true/false), WORKFLOW_VERBOSE (true/false)

**Outputs:**
- WORKFLOW_ID saved to .env

#### 3. test_workflow.py

**Purpose:** Tests a workflow with test data from CLI arguments, .env, or JSON file

**How it works:**
- Reads workflow ID from CLI arg or .env
- Reads test data from CLI arg, .env, or JSON file
- Executes the workflow
- Displays results

**Usage:**
```bash
# Test with CLI arguments (recommended)
python3 /path/to/test_workflow.py \
  --env-file /user/project/.env \
  --input-data '{"patient_last_name": "Rippin", "patient_first_name": "Clay", "diagnosis_text": "generalized anxiety disorder"}'

# Test with JSON file
python3 /path/to/test_workflow.py \
  --env-file /user/project/.env \
  --input-file test_data.json

# Save results to file
python3 /path/to/test_workflow.py \
  --env-file /user/project/.env \
  --input-data '{"patient": "Smith"}' \
  --output-file results.json
```

**Required:**
- WORKFLOW_ID in .env (from create_workflow.py) or via --workflow-id
- Test data (via --input-data, --input-file, or WORKFLOW_TEST_DATA in .env)

**Outputs:**
- Workflow execution results displayed in console
- Optional: JSON file with results (--output-file)

### Example Skill Usage Flow

When a user asks to "create a workflow to process clinical notes", follow this flow:

1. **Locate the Scripts:**
   - Use glob `**/phenoml-workflow/scripts/*.py` to find all available scripts
   - Note their paths for use in subsequent steps

2. **Check Prerequisites and Detect Instance Type:**
   - Run `check_env.py` to verify credentials and detect instance type
   - If credentials are missing, guide user to add them to .env

3. **Handle FHIR Provider Based on Instance Type:**

   **If SHARED EXPERIMENT detected (experiment.app.pheno.ml):**
   - Skip FHIR provider setup entirely
   - Inform user: "You're on the shared experiment, which uses a pre-configured Medplum sandbox. No FHIR setup needed!"
   - Proceed directly to step 6 (Gather Workflow Requirements)

   **If on a DEDICATED INSTANCE (e.g., acme.app.pheno.ml):**
   - Ask: "Have you already set up a FHIR provider connection? (yes/no)"

4. **If NO - Set Up Provider (dedicated instance only):**
   - Run `check_env.py` to verify FHIR credentials
   - If FHIR credentials are missing, guide user to add them to .env with examples:
     - **Medplum**: `FHIR_PROVIDER_BASE_URL=https://api.medplum.com/fhir/R4`
     - **Athena**: `FHIR_PROVIDER_BASE_URL=https://api.preview.platform.athenahealth.com/fhir/r4`
     - **Epic**: `FHIR_PROVIDER_BASE_URL=https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/R4`
     - **Cerner**: `FHIR_PROVIDER_BASE_URL=https://fhir-myrecord.cerner.com/r4/[tenant-id]`
   - Run `setup_fhir_provider.py`
   - Script will save FHIR_PROVIDER_ID to .env

5. **If YES - Verify Provider (dedicated instance only):**
   - Run `check_env.py` to verify FHIR_PROVIDER_ID is set
   - If not found, run `setup_fhir_provider.py`

6. **Gather Workflow Requirements:**
   - "What kind of data will this workflow process?"
   - "What should the workflow do with this data?"
   - Present common examples to help clarify

7. **Create the Workflow:**
   - Gather workflow details conversationally (name, instructions, sample data structure)
   - Determine if dynamic_generation should be true/false based on workflow type
   - Run `create_workflow.py` with CLI arguments (always include --env-file):
   ```bash
   python3 /path/to/create_workflow.py \
     --env-file /user/project/.env \
     --name "Workflow Name" \
     --instructions "Detailed instructions..." \
     --sample-data '{"key": "value"}' \
     --dynamic-generation true
   ```
   - Script will save WORKFLOW_ID to .env

8. **Test the Workflow:**
   - Ask what data they want to test with
   - Run `test_workflow.py` with CLI arguments (always include --env-file):
   ```bash
   python3 /path/to/test_workflow.py \
     --env-file /user/project/.env \
     --input-data '{"patient_last_name": "Smith", ...}'
   ```
   - Shows execution results
   - User can test multiple times with different data

9. **Follow-Up:**
   - Ask if they want to test with different data
   - Offer to create additional workflows
   - Provide next steps for production use

### Available Workflow Templates

#### Condition Creation Workflow
- **Purpose**: Extract conditions from clinical notes or structured diagnosis data
- **Use when**: Processing unstructured clinical documentation, diagnosis text, or medical notes
- **Dynamic Generation**: Yes (handles natural language input)
- **Sample Data Structure**:
  ```python
  {
      "patient_last_name": "Smith",
      "patient_first_name": "John", 
      "diagnosis_text": "patient presents with generalized anxiety disorder"
  }
  ```

#### Patient Registration Workflow  
- **Purpose**: Register new patients with automatic deduplication checking
- **Use when**: Onboarding new patients or checking for existing patient records
- **Dynamic Generation**: No (template-based processing)
- **Sample Data Structure**:
  ```python
  {
      "last_name": "Johnson",
      "first_name": "Sarah",
      "dob": "1985-05-15",
      "gender": "female", 
      "identifier": "PAT001234"
  }
  ```

### Setup Requirements

Before creating workflows, ensure you have:
1. **Python packages installed:** `pip install python-dotenv phenoml`
2. PhenoML credentials (username, password, base_url)
3. **For shared experiment (experiment.app.pheno.ml):** No additional setup needed - uses pre-configured Medplum sandbox
4. **For dedicated instances:** FHIR server connection details (client_id, client_secret, base_url)

### Step-by-Step Workflow Creation

#### 1. Environment Setup
First, create a `.env` file with PhenoML and FHIR provider credentials:
```env
# PhenoML credentials
PHENOML_USERNAME=your_username
PHENOML_PASSWORD=your_password
PHENOML_BASE_URL=your_base_url

# FHIR Provider credentials
FHIR_PROVIDER_BASE_URL=https://api.medplum.com/fhir/R4
FHIR_PROVIDER_CLIENT_ID=your_client_id
FHIR_PROVIDER_CLIENT_SECRET=your_client_secret
```

**Example FHIR_PROVIDER_BASE_URL values:**
- **Medplum**: `https://api.medplum.com/fhir/R4`
- **Athena**: `https://api.preview.platform.athenahealth.com/fhir/r4`
- **Epic**: `https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/R4`
- **Cerner**: `https://fhir-myrecord.cerner.com/r4/[tenant-id]`

#### 2. Initialize Client and FHIR Provider
```python
from phenoml import Client
from dotenv import load_dotenv
import os

# Load environment
load_dotenv()
client = Client(
    username=os.getenv("PHENOML_USERNAME"),
    password=os.getenv("PHENOML_PASSWORD"),
    base_url=os.getenv("PHENOML_BASE_URL")
)

# Create FHIR provider
fhir_provider = client.fhir_provider.create(
    name="Your FHIR Server",
    provider="medplum",  # or other provider type
    auth_method="client_secret",
    base_url="https://your-fhir-server.com/fhir/R4",
    client_id="your-client-id",
    client_secret="your-client-secret"
)
provider_id = fhir_provider.data.id
```

#### 3. Create Workflow
```python
# For condition creation
workflow = client.workflows.create(
    name="Extract Conditions from Notes",
    workflow_instructions=""" You are a helpful agent who can create new condition resources from data inputs whether they are in natural language or structured data. First find the patient identifier based on the name of the patient provided. Then create a new condition resource with a full description of the condition and the patient identifier.""",
    sample_data={
        "patient_last_name": "Rippin",
        "patient_first_name": "Clay", 
        "diagnosis_text": "Patient presents with generalized anxiety disorder"
    },
    fhir_provider_id=provider_id,
    verbose=False,
    dynamic_generation=True
)
workflow_id = workflow.workflow_id

# For patient registration
workflow = client.workflows.create(
    name="Register New Patient",
    workflow_instructions="""You are a helpful agent who can create new patients in the fhir server if they do not already exist. First find the patient identifier based on the first and last name of the patient provided. If no patient identifier is found then create a new patient resource using the first name, last name, and any other relevant information you have. If the patient identifier is found then do nothing.""",
    sample_data={
        "last_name": "Smith",
        "first_name": "John",
        "dob": "1990-01-01",
        "gender": "male",
        "identifier": "PAT123"
    },
    fhir_provider_id=provider_id,
    verbose=False,
    dynamic_generation=False
)
workflow_id = workflow.workflow_id
```

#### 4. Execute Workflow
```python
# Execute with real data
result = client.workflows.execute(
    id=workflow_id,
    input_data={
        "patient_last_name": "Wilson",
        "patient_first_name": "Emma",
        "diagnosis_text": "Patient presents with generalized anxiety disorder"
    }
)
```

### When to Use Each Template

**Use Condition Creation when:**
- Processing clinical notes or documentation
- Converting diagnosis text to structured FHIR resources
- Working with unstructured medical data
- Need dynamic interpretation of medical content

**Use Patient Registration when:**
- Onboarding new patients to the system
- Need to check for duplicate patient records
- Working with structured patient demographic data
- Want consistent patient resource creation

### Error Handling

Always include proper error handling:
```python
try:
    workflow_id = client.workflows.create(...)
    print(f"✅ Workflow created: {workflow_id}")
except Exception as e:
    print(f"❌ Failed to create workflow: {e}")

try:
    result = client.workflows.execute(id=workflow_id, input_data=data)
    print("✅ Workflow executed successfully")
except Exception as e:
    print(f"❌ Workflow execution failed: {e}")
```

### Best Practices

1. **Use descriptive workflow names** that clearly indicate their purpose
2. **Set dynamic_generation=True** for unstructured text processing
3. **Set dynamic_generation=False** for structured data templates
4. **Test workflows with sample data** before processing real patient information
5. **Handle errors gracefully** with appropriate user feedback
6. **Validate input data** before workflow execution
7. **Use verbose=True** during development to see workflow DAG details