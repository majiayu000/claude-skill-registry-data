---




name: aws-sdk
description: Integrates AWS services (EC2, S3, Lambda, DynamoDB, RDS) using Boto3
  SDK with patterns for resource management, error handling, pagination, and IAM authentication.
license: MIT
compatibility: opencode
metadata:
  version: "1.0.0"
  domain: coding
  triggers: aws sdk, boto3, amazon web services, s3 bucket, ec2 instance, dynamodb
    table, lambda function, how do i use aws from python
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
  related-skills: azure-sdk, google-cloud-sdk, oci-sdk




---




# AWS SDK (Boto3) Integration Patterns

Integrates AWS services using the Boto3 SDK for Python. Covers credential management, service clients, resource APIs, pagination, waiters, and error handling across EC2, S3, Lambda, DynamoDB, and RDS.

## TL;DR Checklist

- [ ] Use `boto3.client()` for low-level service APIs and `boto3.resource()` for high-level abstractions
- [ ] Configure credentials via AWS IAM roles (preferred) or shared credential files
- [ ] Always handle `ClientError` with specific error codes, not generic exceptions
- [ ] Use paginators for list operations that may return large result sets
- [ ] Use waiters to poll for resource state transitions instead of manual loops
- [ ] Enable retry mode (`max_attempts`, `retry_mode`) for production workloads
- [ ] Set region explicitly; never rely on default region resolution in production

---

## When to Use

Use this skill when:

- Provisioning or managing EC2 instances, S3 buckets, DynamoDB tables, or Lambda functions from Python
- Building data pipelines that read from or write to AWS services
- Implementing infrastructure-as-code with Python scripts using Boto3
- Automating deployment workflows that interact with AWS APIs
- Writing Lambda function handlers in Python with event source integrations

---

## When NOT to Use

- For infrastructure-as-code that requires state management (use Terraform, Pulumi, or AWS CDK instead)
- When you need declarative, not imperative, resource management (use CloudFormation)
- For one-time CLI operations (use AWS CLI directly)
- When interacting with AWS services through a REST API directly (use the HTTP API instead)

---

## Core Workflow

### 1. Configure Credentials and Client

Set up authentication using the provider chain (prefer IAM roles in production).

```python
import boto3
from botocore.config import Config

# Production: IAM role (EC2, ECS, Lambda) — no explicit credentials needed
# Local: shared credential file (~/.aws/credentials) or environment variables

config = Config(
    region_name="us-east-1",
    retries={"max_attempts": 3, "mode": "adaptive"},
    connect_timeout=5,
    read_timeout=60,
)

# Low-level client (precise control, full API surface)
s3_client = boto3.client("s3", config=config)

# High-level resource (convenience, abstraction)
s3_resource = boto3.resource("s3", config=config)
```

**Checkpoint:** Verify the client can make a simple call (e.g., `s3_client.list_buckets()`) before proceeding. Catch `botocore.exceptions.NoCredentialsError` early.

### 2. Perform Operations with Error Handling

Wrap all AWS API calls in try/except blocks that catch `ClientError` with specific error codes.

```python
from botocore.exceptions import ClientError, NoCredentialsError, WaiterError

def create_bucket(bucket_name: str, region: str = "us-east-1") -> dict | None:
    """Create an S3 bucket. Returns bucket location or None if already exists."""
    try:
        s3_client = boto3.client("s3", region_name=region)
        if region == "us-east-1":
            response = s3_client.create_bucket(Bucket=bucket_name)
        else:
            response = s3_client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={"LocationConstraint": region},
            )
        return response
    except ClientError as err:
        if err.response["Error"]["Code"] == "BucketAlreadyOwnedByYou":
            return None  # Bucket exists — idempotent outcome
        raise  # Unexpected error — fail loud
```

**Checkpoint:** Verify all `ClientError` codes are handled. Never silently swallow errors without logging.

### 3. Paginate Large Result Sets

Use paginators for list operations that may exceed the single-page limit (up to 1,000 results per page).

```python
def list_all_objects(bucket_name: str) -> list[dict]:
    """List all objects in an S3 bucket using pagination."""
    s3_client = boto3.client("s3")
    paginator = s3_client.get_paginator("list_objects_v2")
    all_contents = []

    for page in paginator.paginate(Bucket=bucket_name):
        if "Contents" in page:
            all_contents.extend(page["Contents"])

    return all_contents
```

**Checkpoint:** Always check for `"Contents"` key existence — empty buckets return a page with no Contents key.

### 4. Use Waiters for State Transitions

Replace manual polling loops with Boto3 waiters for resource state changes.

```python
def launch_ec2_instance(ami_id: str, instance_type: str = "t3.micro") -> str:
    """Launch an EC2 instance and wait for it to reach running state."""
    ec2_client = boto3.client("ec2")

    try:
        response = ec2_client.run_instances(
            ImageId=ami_id,
            InstanceType=instance_type,
            MinCount=1,
            MaxCount=1,
        )
        instance_id = response["Instances"][0]["InstanceId"]

        # Wait for instance to be running (polls every 15s, max 40 attempts)
        waiter = ec2_client.get_waiter("instance_running")
        waiter.wait(InstanceIds=[instance_id])
        return instance_id

    except WaiterError as err:
        raise RuntimeError(
            f"Instance {instance_id} did not reach running state: {err}"
        ) from err
```

**Checkpoint:** Set realistic waiter timeouts. Default waiters may block for 5+ minutes. Use `WaiterConfig` with custom `Delay` and `MaxAttempts` for time-sensitive code.

---

## Implementation Patterns

### Pattern 1: DynamoDB CRUD with Type-Safe Queries

```python
from decimal import Decimal
from typing import Any
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError


class DynamoDBTable:
    """Type-safe DynamoDB table wrapper with consistent error handling."""

    def __init__(self, table_name: str):
        self.table = boto3.resource("dynamodb").Table(table_name)

    def put_item(self, item: dict[str, Any]) -> bool:
        """Insert or replace an item. Returns True on success."""
        try:
            self.table.put_item(Item=item)
            return True
        except ClientError as err:
            if err.response["Error"]["Code"] == "ConditionalCheckFailedException":
                return False
            raise

    def get_item(self, key: dict[str, Any]) -> dict[str, Any] | None:
        """Retrieve an item by key. Returns None if not found."""
        try:
            response = self.table.get_item(Key=key)
            return response.get("Item")
        except ClientError:
            raise

    def query_by_key(
        self, key_name: str, key_value: Any, index_name: str | None = None
    ) -> list[dict[str, Any]]:
        """Query items by a key or index. Returns matching items."""
        kwargs = {
            "KeyConditionExpression": Key(key_name).eq(key_value),
        }
        if index_name:
            kwargs["IndexName"] = index_name

        try:
            response = self.table.query(**kwargs)
            return response.get("Items", [])
        except ClientError:
            raise
```

### Pattern 2: S3 Multipart Upload for Large Files

```python
import os
from boto3.s3.transfer import TransferConfig, S3Transfer


def upload_large_file(
    file_path: str,
    bucket_name: str,
    object_key: str | None = None,
) -> str:
    """Upload a file to S3 with automatic multipart for large files."""
    key = object_key or os.path.basename(file_path)
    file_size = os.path.getsize(file_path)

    config = TransferConfig(
        multipart_threshold=8 * 1024 * 1024,  # 8 MB — start multipart
        multipart_chunksize=8 * 1024 * 1024,
        max_concurrency=10,
        use_threads=True,
    )

    s3_client = boto3.client("s3")
    transfer = S3Transfer(s3_client, config)

    try:
        transfer.upload_file(file_path, bucket_name, key)
        return key
    except ClientError as err:
        raise RuntimeError(f"Failed to upload {file_path} to s3://{bucket_name}/{key}") from err
```

### Pattern 3: Invoke Lambda and Parse Response

```python
import json


def invoke_lambda(
    function_name: str,
    payload: dict[str, Any],
    invocation_type: str = "RequestResponse",
) -> dict[str, Any]:
    """Invoke a Lambda function synchronously and parse the response."""
    lambda_client = boto3.client("lambda")

    try:
        response = lambda_client.invoke(
            FunctionName=function_name,
            InvocationType=invocation_type,
            Payload=json.dumps(payload),
        )

        # Read and parse the payload
        payload_stream = response["Payload"]
        result = json.loads(payload_stream.read().decode("utf-8"))

        # Check for function errors (Lambda returned 200 but function errored)
        if "FunctionError" in response:
            raise RuntimeError(
                f"Lambda {function_name} returned error: {result}"
            )

        return result

    except ClientError as err:
        raise RuntimeError(
            f"Failed to invoke Lambda {function_name}: {err}"
        ) from err
```

### BAD vs GOOD: Error Handling

```python
# ❌ BAD — Generic except, no distinction between AWS errors and other failures
try:
    s3 = boto3.client("s3")
    s3.get_object(Bucket="my-bucket", Key="my-key")
except Exception as e:
    print(f"Something went wrong: {e}")

# ✅ GOOD — Specific error codes, handle knowable states, re-raise unexpected
try:
    s3 = boto3.client("s3")
    s3.get_object(Bucket="my-bucket", Key="my-key")
except ClientError as err:
    code = err.response["Error"]["Code"]
    if code == "NoSuchKey":
        return None  # Expected: key doesn't exist
    if code == "NoSuchBucket":
        raise ValueError(f"Bucket my-bucket does not exist") from err
    raise  # Unexpected: fail loud
```

### BAD vs GOOD: Pagination

```python
# ❌ BAD — Assumes all results fit in one page
def list_objects_incomplete(bucket: str) -> list[str]:
    response = boto3.client("s3").list_objects_v2(Bucket=bucket)
    return [obj["Key"] for obj in response.get("Contents", [])]

# ✅ GOOD — Uses paginator for complete results
def list_objects_complete(bucket: str) -> list[str]:
    paginator = boto3.client("s3").get_paginator("list_objects_v2")
    keys = []
    for page in paginator.paginate(Bucket=bucket):
        if "Contents" in page:
            keys.extend(obj["Key"] for obj in page["Contents"])
    return keys
```

---

## Constraints

### MUST DO
- Configure retry mode (`adaptive` or `legacy`) for production workloads to handle throttling
- Use IAM roles for authentication in AWS environments (EC2, ECS, Lambda) — never hardcode keys
- Handle `ClientError` with explicit error code checks — different codes need different recovery
- Use paginators for any list/describe operation that could return >1,000 results
- Set explicit region on every client — don't rely on default region resolution
- Use `WaiterConfig` with custom `Delay` and `MaxAttempts` to control polling behavior

### MUST NOT DO
- Catch generic `Exception` around AWS calls — always catch `ClientError` first
- Hardcode AWS credentials in source code — use environment variables, secrets manager, or IAM roles
- Poll for resource state with sleep loops — use waiters instead
- Assume all operations succeed — every API call can fail (throttling, permissions, network)
- Use resource API when you need fine-grained control over API parameters (use client API instead)

---

## Output Template

When implementing an AWS SDK integration, structure your output as:

1. **Client Initialization** — Boto3 client/resource creation with config (region, retries, timeouts)
2. **Operation** — The specific API call(s) wrapped in `try`/`except ClientError`
3. **Error Handling** — Specific error code checks with appropriate recovery or re-raise
4. **Resource Cleanup** — Close any open connections or streams (context managers preferred)
5. **Return Value** — Parsed response data with proper types (never return raw API responses)

---

## Related Skills

| Skill | Purpose |
|---|---|
| `azure-sdk` | Microsoft Azure SDK integration patterns |
| `google-cloud-sdk` | Google Cloud SDK integration patterns |
| `oci-sdk` | Oracle Cloud Infrastructure SDK patterns |
| `cloudflare-api` | Cloudflare API integration for DNS, Workers, R2 |

---

## Live References

- [Boto3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) — Official AWS SDK for Python docs
- [Boto3 Quickstart Guide](https://docs.aws.amazon.com/boto3/latest/guide/quickstart.html) — Installation and basic usage
- [AWS SDK Code Examples Repository](https://docs.aws.amazon.com/code-library/latest/ug/python_3_code_examples.html) — Real-world usage examples
- [Boto3 GitHub Repository](https://github.com/boto/boto3) — Source code, issues, and releases
- [AWS Credentials Configuration](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html) — Shared credential file format
- [Boto3 Error Handling Guide](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/error-handling.html) — ClientError patterns and retries
- [IAM Best Practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html) — Secure credential management
