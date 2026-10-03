---
name: azure-storage
description: Work with Azure Blob, Table, Queue, and File storage. Implement data persistence, message queuing, and file management solutions.
triggers:
- /azure storage
- /blob storage
---

# Azure Storage Services

This skill covers working with Azure Storage services including Blob, Table, Queue, and File storage for various data persistence scenarios.

## When to use this skill

Use this skill when you need to:
- Store files and unstructured data (Blob)
- Build NoSQL data stores (Table)
- Implement asynchronous messaging (Queue)
- Share files across VMs (File)
- Design data archival strategies

## Prerequisites

- Azure subscription with storage account
- Storage account access keys or SAS tokens
- Azure SDK for your programming language
- Understanding of storage redundancy options (LRS, GRS, ZRS)

## Guidelines

### Storage Account Configuration

**Naming**
- Globally unique, lowercase, alphanumeric only
- 3-24 characters (e.g., `mycorpprodstorage`)

**Performance Tiers**
- **Standard**: HDD-backed, cost-effective for most workloads
- **Premium**: SSD-backed, low latency for intensive applications

**Access Tiers**
- **Hot**: Frequently accessed data (higher storage, lower access cost)
- **Cool**: Infrequently accessed (30+ days retention)
- **Archive**: Rarely accessed (180+ days, retrieval latency hours)

### Blob Storage

**Container Organization**
```
mycontainer/
├── uploads/           # User uploaded files
├── processed/         # Post-processing results
├── archived/          # Old data (Archive tier)
└── temp/              # Temporary files (lifecycle policy to delete)
```

**SDK Usage (Python example)**
```python
from azure.storage.blob import BlobServiceClient

blob_service = BlobServiceClient.from_connection_string(conn_str)
container = blob_service.get_container_client("mycontainer")

# Upload
with open("file.txt", "rb") as f:
    container.upload_blob("path/file.txt", f, overwrite=True)

# Download
blob = container.get_blob_client("path/file.txt")
with open("downloaded.txt", "wb") as f:
    f.write(blob.download_blob().readall())
```

**Security**
- Use SAS tokens with expiration for temporary access
- Enable soft delete for blob recovery
- Use private endpoints for internal access
- Enable blob versioning for audit trails

### Table Storage

**Entity Design**
- PartitionKey: Group related entities for query efficiency
- RowKey: Unique identifier within partition
- Keep entity size under 1MB

```python
from azure.data.tables import TableClient

table = TableClient.from_connection_string(conn_str, "mytable")

entity = {
    "PartitionKey": "User",
    "RowKey": "user123",
    "Name": "John Doe",
    "Email": "john@example.com"
}
table.create_entity(entity)
```

### Queue Storage

**Message Processing Pattern**
```python
from azure.storage.queue import QueueClient

queue = QueueClient.from_connection_string(conn_str, "myqueue")

# Send message
queue.send_message(json.dumps({"task": "process", "id": 123}))

# Receive and process
messages = queue.receive_messages(max_messages=32)
for msg in messages:
    try:
        data = json.loads(msg.content)
        process_task(data)
        queue.delete_message(msg)
    except Exception:
        # Message will become visible again after visibility timeout
        pass
```

### Best Practices

**Performance**
- Use block blobs for files > 100MB
- Enable CDN for frequently accessed static content
- Use batch operations for multiple entities
- Implement exponential backoff for retries

**Cost Optimization**
- Implement lifecycle policies for tier transitions
- Delete temporary data automatically
- Use Premium tier only when latency is critical
- Monitor storage analytics for optimization opportunities

**Data Protection**
- Enable point-in-time restore for blobs
- Use immutable storage for compliance
- Encrypt data at rest and in transit
- Regular backup testing and validation

## Examples

See the `examples/` directory for:
- `blob-upload.py` - File upload implementation
- `table-crud.py` - Table storage operations
- `queue-processor.py` - Message queue consumer
- `lifecycle-policy.json` - Storage lifecycle rules

## References

- [Azure Storage documentation](https://docs.microsoft.com/azure/storage/)
- [Blob storage SDK](https://docs.microsoft.com/azure/storage/blobs/storage-quickstart-blobs-python)
- [Table storage SDK](https://docs.microsoft.com/azure/cosmos-db/table/how-to-use-python)
- [Queue storage SDK](https://docs.microsoft.com/azure/storage/queues/storage-quickstart-queues-python)
