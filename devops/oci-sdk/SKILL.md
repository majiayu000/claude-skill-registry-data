---




name: oci-sdk
description: Integrates Oracle Cloud Infrastructure services (Compute, Object Storage,
  Autonomous DB, Functions) using the OCI Python SDK with config-based authentication
  and resource management.
license: MIT
compatibility: opencode
metadata:
  version: "1.0.0"
  domain: coding
  triggers: oracle cloud, oci sdk, oci python, oracle cloud infrastructure, autonomous
    database, object storage, how do i use oci from python
  archetypes:
  - tactical
  - generation
  anti_triggers:
  - brainstorming
  - vague ideation
  - code golf
  - over-engineering
  response_profile:
    verbosity: low
    directive_strength: high
    abstraction_level: operational
  role: implementation
  scope: implementation
  output-format: code
  related-skills: aws-sdk, azure-sdk, ibm-cloud-api




---




# Oracle Cloud Infrastructure (OCI) SDK Integration Patterns

Integrates Oracle Cloud Infrastructure services using the OCI Python SDK. Covers config-based authentication, Compute instance management, Object Storage CRUD, Autonomous Database operations, and Functions (FaaS) invocation with OCI-specific patterns for pagination, tagging, and composite operations.

## TL;DR Checklist

- [ ] Use `oci.config.from_file()` to load the SDK config — never hardcode credentials in source
- [ ] Initialize service clients with the config dict: `oci.core.ComputeClient(config)`
- [ ] Handle `oci.exceptions.ServiceError` with specific HTTP status codes
- [ ] Use composite operations (`ComputeClientCompositeOperations`) for multi-step provisioning
- [ ] Use pagination with `has_next_page` / `next_page` for list operations
- [ ] Use resource principals for OCI Functions and OKE workloads (no config file needed)

---

## When to Use

Use this skill when:

- Provisioning and managing Compute instances, VCNs, and Block Volumes from Python
- Building applications that read/write data to Object Storage buckets
- Managing Autonomous Database instances (ADW/ATP) programmatically
- Deploying and invoking OCI Functions (Fn Project-based serverless)
- Automating OCI resource lifecycle with Python scripts
- Implementing multi-compartment resource management with tagging

---

## When NOT to Use

- For declarative infrastructure management (use Terraform or Resource Manager stacks)
- For one-off console operations (use OCI CLI or Console)
- When you need cross-cloud orchestration (use multi-cloud abstraction libraries)
- For simple Object Storage operations from the CLI (use `oci os` CLI commands)

---

## Core Workflow

### 1. Load Configuration and Initialize Client

OCI SDK uses a config file (`~/.oci/config`) with profile-based authentication.

```python
import oci
from oci.config import validate_config
from oci.exceptions import ServiceError, ConfigFileNotFound

try:
    # Load configuration from default location (~/.oci/config)
    config = oci.config.from_file(
        file_location="~/.oci/config",
        profile_name="DEFAULT",  # Use named profiles for different environments
    )
    validate_config(config)

except ConfigFileNotFound as err:
    raise RuntimeError(
        "OCI config not found. Create ~/.oci/config with your API key."
    ) from err

# Initialize service clients
identity_client = oci.identity.IdentityClient(config)
compute_client = oci.core.ComputeClient(config)
storage_client = oci.object_storage.ObjectStorageClient(config)

# Get the tenancy OCID for compartment-scoped operations
tenancy_id = config["tenancy"]
```

**Checkpoint:** Verify authentication by calling `identity_client.get_user(config["user"])`. A successful response returns user details. Catch `ServiceError` with status 401 for auth failures.

### 2. Compute Instance Management

```python
def launch_instance(
    config: dict,
    compartment_id: str,
    availability_domain: str,
    subnet_id: str,
    image_id: str,
    instance_name: str = "py-sdk-instance",
) -> oci.core.models.Instance:
    """Launch a compute instance with specified resources."""
    compute_client = oci.core.ComputeClient(config)
    compute_ops = oci.core.ComputeClientCompositeOperations(compute_client)

    # Define instance launch details
    instance_details = oci.core.models.LaunchInstanceDetails(
        compartment_id=compartment_id,
        availability_domain=availability_domain,
        display_name=instance_name,
        shape="VM.Standard.E4.Flex",
        shape_config=oci.core.models.LaunchInstanceShapeConfigDetails(
            ocpus=1,
            memory_in_gbs=8,
        ),
        source_details=oci.core.models.InstanceSourceViaImageDetails(
            image_id=image_id,
        ),
        create_vnic_details=oci.core.models.CreateVnicDetails(
            subnet_id=subnet_id,
            assign_public_ip=True,
        ),
    )

    try:
        # Composite operation: launch + wait for RUNNING state
        response = compute_ops.launch_instance_and_wait_for_state(
            instance_details,
            wait_for_states=[oci.core.models.Instance.LIFECYCLE_STATE_RUNNING],
        )
        return response.data

    except ServiceError as err:
        if err.status == 429:
            raise RuntimeError("Rate limited — retry with backoff") from err
        if err.status == 401:
            raise PermissionError("Invalid OCI credentials") from err
        raise
```

**Checkpoint:** Instance launch is an LRO. The composite operation blocks until the instance reaches `RUNNING`. Set `wait_for_states` to control which state is sufficient for your use case.

### 3. Object Storage CRUD

```python
from oci.object_storage.models import CreateBucketDetails


class ObjectStorageManager:
    """Manage OCI Object Storage buckets and objects."""

    def __init__(self, config: dict):
        self.client = oci.object_storage.ObjectStorageClient(config)
        self.namespace = self.client.get_namespace().data

    def create_bucket(
        self, compartment_id: str, bucket_name: str
    ) -> oci.object_storage.models.Bucket:
        """Create a standard Object Storage bucket."""
        try:
            details = CreateBucketDetails(
                compartment_id=compartment_id,
                name=bucket_name,
                public_access_type="NoPublicAccess",
                storage_tier="Standard",
            )
            response = self.client.create_bucket(
                namespace_name=self.namespace,
                create_bucket_details=details,
            )
            return response.data
        except ServiceError as err:
            if err.status == 409 and "already exists" in err.message:
                # Idempotent: bucket exists
                return self.get_bucket(bucket_name)
            raise

    def get_bucket(self, bucket_name: str) -> oci.object_storage.models.Bucket:
        """Get bucket metadata."""
        response = self.client.get_bucket(
            namespace_name=self.namespace,
            bucket_name=bucket_name,
        )
        return response.data

    def upload_object(
        self, bucket_name: str, object_name: str, data: bytes
    ) -> str:
        """Upload an object. Returns the object's OCID."""
        try:
            response = self.client.put_object(
                namespace_name=self.namespace,
                bucket_name=bucket_name,
                object_name=object_name,
                put_object_body=data,
            )
            return (
                f"/n/{self.namespace}/b/{bucket_name}/o/{object_name}"
            )
        except ServiceError as err:
            raise RuntimeError(
                f"Failed to upload {object_name} to bucket {bucket_name}"
            ) from err

    def list_objects(self, bucket_name: str, prefix: str = "") -> list[str]:
        """List object names with optional prefix."""
        response = self.client.list_objects(
            namespace_name=self.namespace,
            bucket_name=bucket_name,
            prefix=prefix,
        )
        return [obj.name for obj in response.data.objects]
```

**Checkpoint:** Object Storage namespace is the tenancy's unique identifier (not configurable). Use `get_namespace()` to discover it rather than hardcoding.

### 4. Pagination for List Operations

OCI list operations return paginated results. Use the `has_next_page` and `next_page` pattern.

```python
def list_all_compartments(identity_client, tenancy_id: str) -> list[dict]:
    """List all compartments with pagination handling."""
    all_compartments = []
    page = None

    while True:
        response = identity_client.list_compartments(
            compartment_id=tenancy_id,
            page=page,
            limit=50,
        )
        all_compartments.extend(response.data)

        if response.has_next_page:
            page = response.next_page
        else:
            break

    return [
        {"id": c.id, "name": c.name, "state": c.lifecycle_state}
        for c in all_compartments
    ]
```

---

## Implementation Patterns

### Pattern 1: Autonomous Database Operations

```python
def create_autonomous_database(
    config: dict,
    compartment_id: str,
    db_name: str,
    admin_password: str,
) -> oci.database.models.AutonomousDatabase:
    """Create an Autonomous Database (ADW or ATP)."""
    db_client = oci.database.DatabaseClient(config)
    db_ops = oci.database.DatabaseClientCompositeOperations(db_client)

    details = oci.database.models.CreateAutonomousDatabaseDetails(
        compartment_id=compartment_id,
        db_name=db_name,
        display_name=f"{db_name}-adw",
        admin_password=admin_password,
        data_storage_size_in_tbs=1,
        cpu_core_count=1,
        db_workload="DW",  # "DW" for ADW, "OLTP" for ATP
        is_auto_scaling_enabled=True,
        license_model="LICENSE_INCLUDED",
    )

    try:
        response = db_ops.create_autonomous_database_and_wait_for_state(
            details,
            wait_for_states=[
                oci.database.models.AutonomousDatabase.LIFECYCLE_STATE_AVAILABLE,
            ],
        )
        return response.data
    except ServiceError as err:
        raise RuntimeError(
            f"Failed to create Autonomous DB: {err.message}"
        ) from err
```

### Pattern 2: Invoke OCI Function

```python
import json


def invoke_function(
    config: dict,
    function_id: str,
    payload: dict,
) -> dict:
    """Invoke an OCI Function with JSON payload."""
    # Functions Invoke client requires specific endpoint from the function
    fn_client = oci.functions.FunctionsManagementClient(config)

    # Get function details for invoke endpoint
    fn = fn_client.get_function(function_id).data

    # Create invocation client with function's invoke endpoint
    invoke_client = oci.functions.FunctionsInvokeClient(
        config,
        service_endpoint=fn.invoke_endpoint,
    )

    try:
        response = invoke_client.invoke_function(
            function_id=function_id,
            invoke_function_body=json.dumps(payload),
        )
        return json.loads(response.data.text)
    except ServiceError as err:
        raise RuntimeError(
            f"Function invocation failed: {err.message}"
        ) from err
```

### BAD vs GOOD: Config Handling

```python
# ❌ BAD — Hardcoded credentials and manual client setup without error handling
import oci
config = {
    "user": "ocid1.user.oc1..aaaa...",
    "key_file": "/home/user/oci_key.pem",
    "tenancy": "ocid1.tenancy.oc1...",
    "region": "us-ashburn-1",
    "fingerprint": "12:34:56:78:90:ab:cd:ef:...",
}
identity = oci.identity.IdentityClient(config)
user = identity.get_user(config["user"])
print(user.data)

# ✅ GOOD — Config file with validation and error handling
from oci.config import from_file, validate_config
from oci.exceptions import ServiceError, ConfigFileNotFound

try:
    config = from_file()
    validate_config(config)
except ConfigFileNotFound:
    raise RuntimeError("Create ~/.oci/config with your API key")

identity = oci.identity.IdentityClient(config)
try:
    user = identity.get_user(config["user"]).data
    print(f"Authenticated as: {user.name}")
except ServiceError as err:
    if err.status == 401:
        raise PermissionError("Invalid OCI credentials — check key/fingerprint")
    raise
```

### BAD vs GOOD: Object Storage Upload

```python
# ❌ BAD — No namespace discovery, no error handling
storage = oci.object_storage.ObjectStorageClient(config)
storage.put_object(
    namespace_name="ax1b2c3d4e5f",
    bucket_name="my-bucket",
    object_name="data.json",
    put_object_body='{"key": "value"}',
)

# ✅ GOOD — Namespace discovery + structured error handling
def upload_config(config: dict, bucket_name: str, data: bytes) -> str:
    storage = oci.object_storage.ObjectStorageClient(config)
    try:
        namespace = storage.get_namespace().data
    except ServiceError as err:
        raise RuntimeError("Cannot discover Object Storage namespace") from err

    try:
        storage.put_object(
            namespace_name=namespace,
            bucket_name=bucket_name,
            object_name="config.json",
            put_object_body=data,
        )
        return f"/n/{namespace}/b/{bucket_name}/o/config.json"
    except ServiceError as err:
        if err.status == 404:
            raise FileNotFoundError(f"Bucket '{bucket_name}' not found") from err
        raise
```

---

## Constraints

### MUST DO
- Load config from `~/.oci/config` using `oci.config.from_file()` — never hardcode user OCID, key, or tenancy
- Use `validate_config()` after loading to catch common configuration errors early
- Use composite operations (`*ClientCompositeOperations`) for resource creation that needs state waiting
- Handle `ServiceError` with specific status codes: 401 (auth), 404 (not found), 409 (conflict), 429 (rate limit)
- Use pagination with `has_next_page` / `next_page` for list operations (>100 results)
- Use resource principals for OCI Functions and OKE workloads where config files are unavailable

### MUST NOT DO
- Hardcode OCIDs, private key paths, or tenancy identifiers in application source code
- Ignore pagination on list operations — OCI defaults to 50-100 results per page
- Use synchronous patterns for long-running operations without composite operations
- Share API key private keys across environments — use separate keys per environment
- Assume Object Storage namespace — always discover it via `get_namespace()`

---

## Output Template

When implementing an OCI SDK integration, structure your output as:

1. **Config Loading** — `oci.config.from_file()` with validation
2. **Service Client Init** — Per-service client from config dict
3. **Operation** — Resource creation with composite ops for LROs
4. **Error Handling** — `ServiceError` with status code branching
5. **Pagination** — `while` loop with `has_next_page` for list operations
6. **Return Value** — Parsed `.data` attribute from response objects

---

## Related Skills

| Skill | Purpose |
|---|---|
| `aws-sdk` | AWS SDK integration patterns |
| `azure-sdk` | Azure SDK integration patterns |
| `ibm-cloud-api` | IBM Cloud API integration patterns |
| `google-cloud-sdk` | Google Cloud SDK integration patterns |

---

## Live References

- [OCI Python SDK Documentation](https://docs.oracle.com/en-us/iaas/tools/python/latest/) — Official SDK reference
- [OCI Python SDK Quickstart](https://docs.oracle.com/en-us/iaas/tools/python/latest/quickstart.html) — Getting started guide
- [OCI Python SDK GitHub](https://github.com/oracle/oci-python-sdk) — Source code and examples
- [OCI Python SDK Examples](https://github.com/oracle/oci-python-sdk/tree/master/examples) — Runable example scripts
- [OCI Config File Format](https://docs.oracle.com/en-us/iaas/Content/API/Concepts/sdkconfig.htm) — SDK config file reference
- [OCI API Key Management](https://docs.oracle.com/en-us/iaas/Content/API/Concepts/apisigningkey.htm) — How to create API keys
- [OCI Resource Principal](https://docs.oracle.com/en-us/iaas/Content/Identity/Tasks/callingservicesfrominstances.htm) — Auth for OKE/Functions
