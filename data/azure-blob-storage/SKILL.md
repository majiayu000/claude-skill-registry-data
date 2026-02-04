---
name: azure-blob-storage
description: Connect to and interact with Azure Blob Storage (ADLS Gen2). Use when working with Azure blob storage, listing containers, reading files, uploading data, or when user mentions Azure storage, blob containers, or ADLS. Handles authentication, container operations, and blob management.
version: 1.0.0
---

# Azure Blob Storage Skill

## Overview

This skill enables interaction with Azure Blob Storage and Azure Data Lake Storage Gen2 (ADLS Gen2). It provides capabilities for authenticating, listing containers/blobs, reading blob content, and managing blob metadata.

## When to Use

- User mentions Azure Blob Storage, Azure Storage, or ADLS
- Need to list containers or blobs in a storage account
- Read data files from blob storage (CSV, JSON, Parquet)
- Upload or download files to/from blob storage
- Get blob metadata (size, last modified, content type)
- Work with hierarchical namespace (ADLS Gen2) directories

## Prerequisites

Environment variables must be configured:
- `AZURE_STORAGE_ACCOUNT_NAME`: Storage account name
- `AZURE_STORAGE_ACCOUNT_KEY`: Storage account key **OR**
- `AZURE_STORAGE_CONNECTION_STRING`: Complete connection string

## Authentication

### Option 1: Account Name + Key
```python
from azure.storage.blob import BlobServiceClient

account_name = os.getenv("AZURE_STORAGE_ACCOUNT_NAME")
account_key = os.getenv("AZURE_STORAGE_ACCOUNT_KEY")
account_url = f"https://{account_name}.blob.core.windows.net"

blob_service_client = BlobServiceClient(account_url, credential=account_key)
```

### Option 2: Connection String
```python
from azure.storage.blob import BlobServiceClient

connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
blob_service_client = BlobServiceClient.from_connection_string(connection_string)
```

### Option 3: Managed Identity (for Azure-hosted apps)
```python
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

account_name = os.getenv("AZURE_STORAGE_ACCOUNT_NAME")
account_url = f"https://{account_name}.blob.core.windows.net"
credential = DefaultAzureCredential()

blob_service_client = BlobServiceClient(account_url, credential=credential)
```

## Common Operations

### List Containers
```python
from azure.storage.blob import BlobServiceClient

blob_service_client = BlobServiceClient(account_url, credential=account_key)

print("Containers in storage account:")
containers = blob_service_client.list_containers()
for container in containers:
    print(f"  - {container.name}")
```

### List Blobs in a Container
```python
container_client = blob_service_client.get_container_client("my-container")

print("Blobs in container 'my-container':")
blobs = container_client.list_blobs()
for blob in blobs:
    print(f"  - {blob.name} ({blob.size} bytes, modified: {blob.last_modified})")
```

### Filter Blobs by Prefix (Directory-like)
```python
# List all blobs in "2024/sales/" path
blobs = container_client.list_blobs(name_starts_with="2024/sales/")
for blob in blobs:
    print(f"  - {blob.name}")
```

### Download Blob Content
```python
blob_client = blob_service_client.get_blob_client(
    container="my-container",
    blob="data/file.csv"
)

# Download to stream
download_stream = blob_client.download_blob()
content = download_stream.readall()
print(f"Downloaded {len(content)} bytes")

# Download to file
with open("local_file.csv", "wb") as file:
    download_stream = blob_client.download_blob()
    file.write(download_stream.readall())
```

### Read CSV/JSON/Parquet from Blob
```python
import pandas as pd
from io import BytesIO

blob_client = blob_service_client.get_blob_client(
    container="data-container",
    blob="sales/2024/sales.csv"
)

# Download blob content
download_stream = blob_client.download_blob()
content = download_stream.readall()

# Read with pandas
if blob.name.endswith('.csv'):
    df = pd.read_csv(BytesIO(content))
elif blob.name.endswith('.json'):
    df = pd.read_json(BytesIO(content))
elif blob.name.endswith('.parquet'):
    df = pd.read_parquet(BytesIO(content))

print(f"Loaded DataFrame with {len(df)} rows and {len(df.columns)} columns")
```

### Get Blob Metadata
```python
blob_client = blob_service_client.get_blob_client(
    container="my-container",
    blob="data/file.parquet"
)

properties = blob_client.get_blob_properties()
print(f"Blob: {properties.name}")
print(f"Size: {properties.size} bytes")
print(f"Content Type: {properties.content_settings.content_type}")
print(f"Last Modified: {properties.last_modified}")
print(f"ETag: {properties.etag}")
```

### Upload Blob
```python
blob_client = blob_service_client.get_blob_client(
    container="my-container",
    blob="output/result.csv"
)

# Upload from local file
with open("local_result.csv", "rb") as data:
    blob_client.upload_blob(data, overwrite=True)

# Upload from string/bytes
content = "col1,col2\nvalue1,value2"
blob_client.upload_blob(content.encode('utf-8'), overwrite=True)
```

### Check if Blob Exists
```python
blob_client = blob_service_client.get_blob_client(
    container="my-container",
    blob="data/file.csv"
)

if blob_client.exists():
    print("Blob exists")
else:
    print("Blob does not exist")
```

## Error Handling

```python
from azure.core.exceptions import ResourceNotFoundError, AzureError

try:
    blob_client = blob_service_client.get_blob_client(
        container="my-container",
        blob="data/file.csv"
    )
    content = blob_client.download_blob().readall()
except ResourceNotFoundError:
    print("Blob not found - check container and blob name")
except AzureError as e:
    print(f"Azure error: {e.message}")
except Exception as e:
    print(f"Unexpected error: {str(e)}")
```

## Best Practices

1. **Use Specific Paths**: Always specify full blob paths including container
2. **Handle Large Files**: For large files (>100MB), use streaming downloads
3. **Batch Operations**: When listing many blobs, use pagination
4. **Connection Reuse**: Reuse `BlobServiceClient` instance for multiple operations
5. **Error Handling**: Always wrap blob operations in try/except blocks
6. **Authentication**: Prefer managed identity in production over account keys

## Security Notes

- **Never commit** account keys or connection strings to version control
- Use environment variables or Azure Key Vault for credentials
- In production, use managed identities instead of account keys
- Apply least-privilege access using SAS tokens or Azure RBAC

## Extensibility

This skill is designed for Azure Blob Storage. For other cloud providers:
- **AWS S3**: Create separate `aws-s3` skill following similar pattern
- **Google Cloud Storage**: Create `gcs-storage` skill
- **MinIO**: Create `minio` skill for S3-compatible storage

## Common Use Cases

1. **Data Discovery**: List containers and blobs to find datasets
2. **Data Ingestion**: Download files for processing or profiling
3. **Data Export**: Upload transformed data back to blob storage
4. **Metadata Collection**: Get file sizes, types, and modification dates
5. **Directory Traversal**: Use prefixes to navigate ADLS Gen2 directories

## Troubleshooting

- **Authentication Errors**: Verify env variables are set correctly
- **Permission Denied**: Check storage account access policies and RBAC roles
- **Blob Not Found**: Confirm container and blob names (case-sensitive)
- **Network Issues**: Check firewall rules and network connectivity
- **Large File Timeouts**: Increase timeout or use chunked downloads
