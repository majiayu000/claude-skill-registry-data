---
name: ftpc-storage-write
description: Full read-write access to remote storage backends (local, FTP, SFTP, S3, Azure). Upload files, delete files, create directories, in addition to listing and downloading. Use when you need to modify files on cloud storage, FTP servers, or remote filesystems.
---

# FTPC Storage (Full Access)

Use the `ftpc` library to read and write files across storage backends.

**This skill can modify remote storage.** Confirm destructive operations with the user.

## Supported Backends

| Protocol | URL Format | Example |
|----------|------------|---------|
| Local | `file:///path` or `/path` | `/home/user/data` |
| FTP | `ftp://[user:pass@]host[:port]/path` | `ftp://ftp.example.com/pub` |
| FTPS | `ftps://[user:pass@]host[:port]/path` | `ftps://secure.example.com` |
| SFTP | `sftp://[user:pass@]host[:port]/path` | `sftp://user:pass@host/data` |
| S3 | `s3://bucket/path` | `s3://my-bucket/folder` |
| Azure Data Lake | `azure://account.dfs.core.windows.net/fs/path` | `azure://myacct.dfs.core.windows.net/data` |
| Azure Blob | `blob://account.blob.core.windows.net/container/path` | `blob://myacct.blob.core.windows.net/files` |

## Quick Start

```python
from ftpc import connect_sync

with connect_sync("s3://my-bucket") as store:
    # List files
    files = store.list("/")

    # Download
    store.download("/data.csv", "local.csv")

    # Upload
    store.upload("report.pdf", "/reports/report.pdf")

    # Create directory
    store.mkdir("/new-folder")

    # Delete file
    store.delete("/old-file.txt")
```

## All Operations

### List Directory

```python
from ftpc import connect_sync

with connect_sync("ftp://ftp.example.com") as store:
    files = store.list("/documents")
    for f in files:
        print(f"{f.name}  {'DIR' if f.is_directory else f.size}")
```

### Download File

```python
with connect_sync("sftp://user:pass@host") as store:
    store.download("/remote/file.csv", "local_file.csv")

    # With progress callback
    def progress(bytes_done: int) -> bool:
        print(f"Downloaded {bytes_done} bytes")
        return True  # False cancels transfer

    store.download("/large.zip", "out.zip", progress)
```

### Upload File

```python
with connect_sync("s3://my-bucket") as store:
    store.upload("local_report.pdf", "/reports/2024/report.pdf")

    # With progress
    def progress(bytes_done: int) -> bool:
        print(f"Uploaded {bytes_done} bytes")
        return True

    store.upload("large_backup.tar.gz", "/backups/backup.tar.gz", progress)
```

### Create Directory

```python
with connect_sync("ftp://ftp.example.com") as store:
    success = store.mkdir("/new-directory")
    if success:
        print("Directory created")
```

### Delete File

```python
with connect_sync("s3://my-bucket") as store:
    success = store.delete("/obsolete-file.txt")
    if success:
        print("File deleted")
```

## Async Usage

```python
import asyncio
from ftpc import Storage

async def main():
    async with Storage.connect("s3://bucket") as store:
        await store.upload("local.txt", "/remote.txt")
        await store.mkdir("/new-dir")
        await store.delete("/old.txt")

asyncio.run(main())
```

## Named Constructors

```python
from ftpc import Storage

# S3 with credentials
with Storage.s3(
    bucket="my-bucket",
    region="us-east-1",
    access_key_id="AKIAIOSFODNN7EXAMPLE",
    secret_access_key="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
).sync() as store:
    store.upload("data.csv", "/uploads/data.csv")

# FTP with TLS
with Storage.ftp(
    host="ftp.example.com",
    username="user",
    password="pass",
    tls=True
).sync() as store:
    store.upload("report.pdf", "/reports/report.pdf")

# SFTP with key auth
with Storage.sftp(
    host="server.example.com",
    username="deploy",
    key_filename="/home/user/.ssh/id_rsa"
).sync() as store:
    store.upload("deploy.tar.gz", "/var/releases/deploy.tar.gz")

# Azure Data Lake
with Storage.azure(
    account_url="https://myaccount.dfs.core.windows.net",
    filesystem="data",
    account_key="your-account-key"
).sync() as store:
    store.upload("dataset.parquet", "/datasets/dataset.parquet")
```

## Using Named Remotes from Config

With `~/.ftpcconf.toml`:

```toml
[prod-s3]
type = "s3"
bucket = "production-data"
region = "us-east-1"
```

```python
from ftpc.config import Config
from ftpc.clients.s3client import S3Client

config = Config.from_file()
remote = config.remotes["prod-s3"]

with S3Client(bucket_name=remote.bucket, region_name=remote.region) as client:
    client.put("local.csv", "/uploads/data.csv")
```

## FileDescriptor Structure

All `list()` calls return `List[FileDescriptor]`:

```python
@dataclass
class FileDescriptor:
    path: PurePath              # Full path
    filetype: FileType          # FILE or DIRECTORY
    size: Optional[int]         # Bytes (None for dirs)
    modified_time: Optional[datetime]

    @property
    def name(self) -> str       # Filename only

    @property
    def is_file(self) -> bool

    @property
    def is_directory(self) -> bool
```

## Dependencies

```bash
pip install ftpc            # Core (local + FTP)
pip install ftpc[sftp]      # + SFTP
pip install ftpc[s3]        # + S3
pip install ftpc[azure]     # + Azure
pip install ftpc[all]       # All backends
```
