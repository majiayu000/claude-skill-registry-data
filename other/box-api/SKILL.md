---




name: box-api
description: Integrates with Box API to manage files, folders, collaborations, metadata,
  signatures, hubs, and AI features using the boxsdk Python SDK.
license: MIT
compatibility: opencode
metadata:
  version: "1.0.0"
  domain: coding
  triggers: box api, box python, box sdk, box files, box folders, box collaboration,
    box sign, box metadata
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
  content-types:
  - code
  - guidance
  - do-dont
  - examples
  related-skills: coding-microsoft-graph-api, coding-google-workspace-api, coding-dropbox-api




---





# Box API Integration

Integrates with the Box Content Cloud API to manage files, folders, collaborations (permissions), metadata, signatures (Box Sign), content hubs, retention policies, and AI-powered content insights using the official `boxsdk` Python library.

## TL;DR for Code Generation

- Use `boxsdk.Client(oauth)` for user auth or `boxsdk.CCGClient(client_id, client_secret, enterprise_id)` for server auth (Client Credentials Grant)
- The SDK is generated from Box's OpenAPI spec — methods follow the REST resource hierarchy
- Always paginate collections with `.items()` or `.next_marker` — Box uses marker-based pagination
- Use the `as_user(user_id)` context manager for impersonation (admin/service account only)
- Box Sign requests use the `boxsdk.sign_templates` and `boxsdk.sign_requests` resources
- Handle `boxsdk.exception.BoxAPIException` for API-level errors with `status` and `code` fields

## When to Use

Use this skill when:

- Uploading, downloading, moving, copying, or deleting files and folders
- Managing share links, collaborations (user/group permissions), and access levels
- Applying metadata templates (custom key-value schemas) to files and folders
- Creating and sending Box Sign signature requests
- Searching across content with full-text and metadata queries
- Setting up webhooks for file and folder change notifications
- Using Box AI to extract insights from documents (text generation, question answering)
- Managing retention policies and legal holds for compliance

## When NOT to Use

- Real-time collaborative document editing (use Box web app or Office Online integration)
- High-throughput file processing (Box has rate limits — use upload sessions for large files)
- Anonymous file access (Box requires authentication for every API request)
- Replacing a CDN for public content delivery (use Box shared links with appropriate settings)

## Core Workflow

1. **Create a Box Application** — Go to `https://developer.box.com` and create a new app. Choose "Client Credentials Grant (Server Auth)" for automated access, or OAuth 2.0 for user delegation. **Checkpoint:** Verify the app exists in the Box Developer Console and has the correct scopes.

2. **Authenticate** — For server auth: `auth = CCGAuth(client_id, client_secret, enterprise_id)` then `client = Client(auth)`. For user auth: use OAuth 2.0 flow with `JWTAuth` or `OAuth2`. **Checkpoint:** Call `client.users().get(user_id="me")` for user auth, or `client.users()[:1]` for service account.

3. **Choose a Resource** — Files: `client.file(file_id)`. Folders: `client.folder(folder_id)`. Users: `client.user(user_id)`. Search: `client.search.query(...)`. **Checkpoint:** Verify the resource exists by calling `.get()` on the resource object.

4. **Perform Operations** — Upload with `client.folder(folder_id).upload(file_path)`, download with `file.content()`, move with `file.move(parent_folder)`, collaborate with `client.folder(folder_id).add_collaborator(...)`. **Checkpoint:** Check the response object's `type` and `id` fields.

5. **Handle Pagination** — Use `.items()` for folder listing, `.next_marker` for search and metadata query results. Iterate with `for item in client.folder(folder_id).items():`. **Checkpoint:** Ensure the loop terminates — pagination returns empty when exhausted.

6. **Handle Errors** — Wrap in `try/except BoxAPIException`. Check `e.status` for 401 (unauthorized), 403 (forbidden), 404 (not found), 409 (conflict), 429 (rate limit). **Checkpoint:** Log `e.code` (e.g., `item_name_in_use`, `trashed_item`) for debugging.

## Implementation Patterns

### Pattern 1: Upload and Share a File

```python
import os
from boxsdk import Client, CCGAuth
from boxsdk.exception import BoxAPIException

auth = CCGAuth(
    client_id=os.environ["BOX_CLIENT_ID"],
    client_secret=os.environ["BOX_CLIENT_SECRET"],
    enterprise_id=os.environ["BOX_ENTERPRISE_ID"],
)
client = Client(auth)

def upload_and_share(folder_id: str, file_path: str) -> dict:
    """Upload a file to Box and create a shared link."""
    try:
        folder = client.folder(folder_id)
        uploaded_file = folder.upload(file_path)
        shared_link = uploaded_file.create_shared_link(
            access="open",
            unshared_at=None,
            permissions={"can_download": True, "can_preview": True},
        )
        return {
            "id": uploaded_file.id,
            "name": uploaded_file.name,
            "shared_url": shared_link["url"],
        }
    except BoxAPIException as e:
        print(f"Box API error {e.status}: {e.code} — {e.message}")
        raise

result = upload_and_share("123456789", "/tmp/report.pdf")
print(f"File shared: {result['shared_url']}")
```

### Pattern 2: List Folder Contents

```python
def list_folder_contents(folder_id: str) -> list[dict]:
    """List all files and subfolders in a Box folder."""
    items = []
    try:
        folder = client.folder(folder_id)
        for item in folder.items():
            items.append({
                "id": item.id,
                "name": item.name,
                "type": item.type,  # "file" or "folder"
                "size": getattr(item, "size", None),
                "created_at": getattr(item, "created_at", None),
            })
    except BoxAPIException as e:
        print(f"Error listing folder: {e}")
    return items

contents = list_folder_contents("0")  # root folder
for item in contents:
    print(f"[{item['type']}] {item['name']} ({item['id']})")
```

### Pattern 3: Apply Metadata to a File

```python
def apply_metadata(file_id: str, template_key: str, values: dict) -> dict:
    """Apply or update a metadata template on a Box file."""
    from boxsdk.object.metadata import Metadata

    try:
        file = client.file(file_id)
        metadata = file.metadata(template_key)
        return metadata.update(values)
    except BoxAPIException as e:
        if e.status == 409:
            print(f"Metadata already exists — updating instead.")
            return client.file(file_id).metadata(template_key).update(values)
        raise

metadata_values = {
    "documentType": "Invoice",
    "clientName": "Acme Corp",
    "amount": 12500.00,
    "status": "Pending Approval",
}
apply_metadata("987654321", "documentFlow", metadata_values)
```

### Pattern 4: Send Box Sign Request

```python
def send_sign_request(
    file_id: str,
    signer_email: str,
    signer_name: str,
) -> dict:
    """Send a Box Sign request for a file."""
    file = client.file(file_id)
    sign_request = client.create_sign_request(
        signers=[{"email": signer_email, "name": signer_name}],
        source_files=[file],
        parent_folder=client.folder("0"),
        is_prepare=False,
    )
    return {
        "id": sign_request.id,
        "status": sign_request.status,
        "signers": [s.email for s in sign_request.signers],
    }

result = send_sign_request("987654321", "signer@example.com", "Jane Signer")
print(f"Sign request {result['id']} sent to {result['signers']}")
```

### Pattern 5: BAD vs GOOD — Error Handling

```python
# ❌ BAD — no error differentiation, unreliable
file = client.file("nonexistent")
content = file.content()

# ✅ GOOD — typed error handling with status-based recovery
from boxsdk.exception import BoxAPIException

def safe_download_file(file_id: str) -> bytes | None:
    """Download a file with resilient error handling."""
    try:
        file = client.file(file_id).get()
        return file.content()
    except BoxAPIException as e:
        if e.status == 404:
            print(f"File {file_id} not found or trashed.")
            return None
        if e.status == 403:
            print(f"No access to file {file_id}.")
            return None
        if e.status == 429:
            print("Rate limited.")
            return None
        raise
```

## Constraints

### MUST DO
- Use CCGAuth for server-to-server apps — avoid storing user refresh tokens
- Always call `.get()` on a resource before accessing its fields (SDK uses lazy loading)
- Use marker-based pagination (`.items()` iterator) for folder listing
- Set `as_user()` for admin operations acting on behalf of managed users
- Validate file types and sizes before upload (Box has per-file size limits based on plan)

### MUST NOT DO
- Hardcode OAuth client credentials in application code
- Assume folder IDs are stable across environments — use folder names or metadata to find them
- Use `as_user()` without admin privileges — it will raise 403
- Poll folders for changes — use webhooks and event streams instead
- Upload files without checking for name conflicts (use `preflight_check` before upload)

## Output Template

Every integration function should expose:

1. **Authentication** — `CCGAuth` or `OAuth2` initialization with credentials from env
2. **Resource Selection** — `client.file()`, `client.folder()`, `client.user()`, or `client.search.query()`
3. **Operation** — Upload, download, share, collaborate, or metadata mutation
4. **Pagination** — `.items()` iterator for collections, `.next_marker` for search
5. **Error Handling** — `try/except BoxAPIException` with `e.status` and `e.code` differentiation

## Related Skills

| Skill | Purpose |
|